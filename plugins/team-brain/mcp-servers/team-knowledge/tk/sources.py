"""Source adapters. Each adapter exposes: available(), search(), read(); git_repo adds code tools."""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import ssl
import subprocess
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .config import matches
from .graph import Graph
from .textindex import BM25Index, Chunk, chunk_document, load_or_build, snippet

TEXT_EXT = (".md", ".markdown", ".adoc", ".asciidoc", ".txt", ".rst")
MAX_FILE_BYTES = 2_000_000
_REF_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/\-+]{0,200}$")


class SourceError(Exception):
    pass


def _hit(source, chunk: Chunk, score: float, query: str) -> dict:
    return {
        "source": source,
        "id": chunk.doc_id,
        "title": chunk.title,
        "heading": chunk.heading,
        "location": chunk.location or chunk.doc_id,
        "snippet": snippet(chunk.text, query),
        "score": round(score, 3),
        "meta": chunk.meta,
    }


# --------------------------------------------------------------------------------------------
class Source:
    kind = "base"

    def __init__(self, cfg: dict, cache_dir: str):
        self.cfg = cfg
        self.name = cfg["name"]
        self.description = cfg.get("description", "")
        self.cache_dir = cache_dir
        self._lock = threading.Lock()

    def available(self) -> tuple[bool, str]:
        raise NotImplementedError

    def search(self, query: str, limit: int, **kw) -> list[dict]:
        raise NotImplementedError

    def read(self, doc_id: str, **kw) -> dict:
        raise NotImplementedError

    def warm(self) -> str:
        return "nothing to warm"

    def texts(self, ref: str | None = None) -> tuple[str, dict[str, str]]:
        """(signature, {doc id: text}) of every document, for the link graph. Sources without files can't."""
        raise SourceError(f"{self.name} ({self.kind}) has no link graph")

    def graph(self, ref: str | None = None) -> Graph:
        sig, texts = self.texts(ref)
        with self._lock:
            cached = getattr(self, "_graph", None)
            if not cached or cached[0] != sig:
                cached = self._graph = (sig, Graph(texts))
            return cached[1]


# --------------------------------------------------------------------------------------------
class MarkdownDir(Source):
    """A directory of Markdown/AsciiDoc files (the brain, upstream Kubernetes docs, a docs mirror)."""

    kind = "markdown_dir"

    def __init__(self, cfg, cache_dir):
        super().__init__(cfg, cache_dir)
        self.root = Path(cfg["root"]).resolve()
        self.include = cfg.get("include", ["**/*"])
        self.exclude = cfg.get("exclude", [])
        self.base_url = cfg.get("base_url", "")

    def available(self):
        return (self.root.is_dir(), str(self.root) if self.root.is_dir() else f"missing dir {self.root}")

    def _files(self) -> list[tuple[str, os.stat_result]]:
        out = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for fn in filenames:
                if not fn.lower().endswith(TEXT_EXT):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, self.root).replace(os.sep, "/")
                if matches(rel, self.include, self.exclude):
                    st = os.stat(full)
                    if st.st_size <= MAX_FILE_BYTES:
                        out.append((rel, st))
        out.sort()
        return out

    def _index(self) -> BM25Index:
        with self._lock:
            files = self._files()
            sig = hashlib.sha256(
                "|".join(f"{r}:{s.st_mtime_ns}:{s.st_size}" for r, s in files).encode()
            ).hexdigest()

            def build():
                chunks = []
                for rel, _ in files:
                    text = (self.root / rel).read_text(encoding="utf-8", errors="replace")
                    chunks.extend(chunk_document(rel, text, self._location(rel)))
                return chunks

            return load_or_build(self.cache_dir, self.name, sig, build)

    def _location(self, rel: str) -> str:
        return f"{self.base_url.rstrip('/')}/{rel}" if self.base_url else str(self.root / rel)

    def texts(self, ref=None):
        files = self._files()
        sig = hashlib.sha256("|".join(f"{r}:{s.st_mtime_ns}:{s.st_size}" for r, s in files).encode()).hexdigest()
        cached = getattr(self, "_graph", None)
        if cached and cached[0] == sig:
            return sig, {}
        return sig, {rel: (self.root / rel).read_text(encoding="utf-8", errors="replace") for rel, _ in files}

    def search(self, query, limit, **kw):
        return [_hit(self.name, c, s, query) for s, c in self._index().search(query, limit)]

    def read(self, doc_id, **kw):
        p = (self.root / doc_id).resolve()
        if self.root not in p.parents or not p.is_file():
            raise SourceError(f"{doc_id!r} is not a file in source {self.name}")
        return {"title": doc_id, "location": self._location(doc_id),
                "text": p.read_text(encoding="utf-8", errors="replace")}

    def warm(self):
        idx = self._index()
        return f"{idx.n} chunks"


# --------------------------------------------------------------------------------------------
class GitRepo(Source):
    """A local git clone/mirror. Docs are indexed at a ref; code is searched with git grep at any ref."""

    kind = "git_repo"

    def __init__(self, cfg, cache_dir):
        super().__init__(cfg, cache_dir)
        self.path = cfg["path"]
        self.remote = cfg.get("remote", "")
        self.default_ref = cfg.get("default_ref", "main")
        self.docs = cfg.get("docs", [])
        self.code_include = cfg.get("code_include", [])
        self.code_exclude = cfg.get("code_exclude", ["vendor/**"])
        self.web_url = cfg.get("web_url", "")

    # -- git plumbing -------------------------------------------------------------------------
    def _git(self, *args, input_bytes: bytes | None = None, timeout: int = 60, check=True) -> bytes:
        p = subprocess.run(["git", "-C", self.path, *args], input=input_bytes,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        if check and p.returncode != 0:
            raise SourceError(p.stderr.decode(errors="replace").strip()[:500] or f"git {args[0]} failed")
        return p.stdout

    def available(self):
        if not os.path.isdir(self.path):
            return False, f"missing clone {self.path} (run: server.py --sync)"
        try:
            self._git("rev-parse", "--git-dir", timeout=10)
            return True, f"{self.path} @ {self.default_ref}"
        except Exception as e:  # noqa: BLE001
            return False, str(e)

    def resolve(self, ref: str | None) -> tuple[str, str]:
        ref = (ref or self.default_ref).strip()
        if not _REF_OK.match(ref):
            raise SourceError(f"invalid ref {ref!r}")
        for cand in (ref, f"origin/{ref}", f"refs/tags/{ref}"):
            out = self._git("rev-parse", "--verify", "--quiet", f"{cand}^{{commit}}", check=False, timeout=10)
            if out.strip():
                return ref, out.decode().strip()
        raise SourceError(f"ref {ref!r} not found in {self.name}; use list_refs to see what exists")

    def _ls(self, sha: str) -> list[str]:
        return self._git("ls-tree", "-r", "--name-only", "-z", sha, timeout=60).decode(errors="replace").split("\0")

    def _cat_many(self, sha: str, paths: list[str]) -> dict[str, str]:
        if not paths:
            return {}
        req = "".join(f"{sha}:{p}\n" for p in paths).encode()
        raw = self._git("cat-file", "--batch", input_bytes=req, timeout=300)
        out, pos = {}, 0
        for p in paths:
            nl = raw.index(b"\n", pos)
            header = raw[pos:nl].decode(errors="replace").split()
            pos = nl + 1
            if len(header) < 3 or header[1] == "missing":
                continue
            size = int(header[2])
            if header[1] == "blob" and size <= MAX_FILE_BYTES:
                out[p] = raw[pos:pos + size].decode("utf-8", errors="replace")
            pos += size + 1
        return out

    def _blob_url(self, sha: str, path: str, line: int | None = None) -> str:
        if not self.web_url:
            return path
        return f"{self.web_url.rstrip('/')}/-/blob/{sha}/{path}" + (f"#L{line}" if line else "")

    # -- docs ---------------------------------------------------------------------------------
    def _doc_index(self, ref: str | None) -> tuple[BM25Index, str, str]:
        ref, sha = self.resolve(ref)
        with self._lock:
            def build():
                paths = [p for p in self._ls(sha) if p.lower().endswith(TEXT_EXT) and matches(p, self.docs)]
                chunks = []
                for p, text in self._cat_many(sha, paths).items():
                    chunks.extend(chunk_document(p, text, self._blob_url(sha, p), {"ref": ref}))
                return chunks

            key = hashlib.sha256(f"{self.name}:{ref}".encode()).hexdigest()[:12]
            idx = load_or_build(self.cache_dir, f"{self.name}-{key}", f"{sha}:{self.docs}", build)
            return idx, ref, sha

    def texts(self, ref=None):
        ref, sha = self.resolve(ref)
        sig = f"{sha}:{self.docs}"
        cached = getattr(self, "_graph", None)
        if cached and cached[0] == sig:
            return sig, {}
        paths = [p for p in self._ls(sha) if p.lower().endswith(TEXT_EXT) and matches(p, self.docs)]
        return sig, self._cat_many(sha, paths)

    def search(self, query, limit, ref=None, **kw):
        if not self.docs:
            return []
        idx, ref, _ = self._doc_index(ref)
        return [_hit(self.name, c, s, query) for s, c in idx.search(query, limit)]

    def read(self, doc_id, ref=None, **kw):
        ref, sha = self.resolve(ref)
        text = self._cat_many(sha, [doc_id]).get(doc_id)
        if text is None:
            raise SourceError(f"{doc_id!r} not found at {ref}")
        return {"title": f"{doc_id} @ {ref}", "location": self._blob_url(sha, doc_id), "text": text}

    def warm(self):
        if not self.docs:
            return "code only"
        idx, ref, sha = self._doc_index(None)
        return f"{idx.n} doc chunks @ {ref} ({sha[:10]})"

    # -- code ---------------------------------------------------------------------------------
    def _pathspecs(self, path: str | None) -> list[str]:
        if path:
            return [f":(glob){path}"]
        specs = [f":(glob){p}" for p in self.code_include] or ["."]
        specs += [f":(glob,exclude){p}" for p in self.code_exclude]
        return specs

    def grep(self, pattern: str, ref=None, path=None, regex=True, ignore_case=False, limit=60) -> dict:
        ref, sha = self.resolve(ref)
        args = ["git", "-C", self.path, "grep", "-n", "-I", "--no-color", "--full-name"]
        args += ["-E"] if regex else ["-F"]
        if ignore_case:
            args.append("-i")
        args += ["-e", pattern, sha, "--", *self._pathspecs(path)]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        hits, truncated = [], False
        try:
            assert proc.stdout is not None
            for raw in proc.stdout:
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                # format: <sha>:<path>:<lineno>:<text>
                parts = line.split(":", 3)
                if len(parts) < 4:
                    continue
                _, fpath, lno, text = parts
                hits.append({"path": fpath, "line": int(lno), "text": text.strip()[:240],
                             "url": self._blob_url(sha, fpath, int(lno))})
                if len(hits) >= limit:
                    truncated = True
                    break
        finally:
            proc.kill() if truncated else None
            _, err = proc.communicate(timeout=30)
        if proc.returncode not in (0, 1, -9) and not hits and not truncated:
            raise SourceError(err.decode(errors="replace").strip()[:500])
        return {"ref": ref, "sha": sha, "hits": hits, "truncated": truncated}

    def show(self, path: str, ref=None, start=1, end=None) -> dict:
        ref, sha = self.resolve(ref)
        if path.startswith("-") or ".." in path.split("/"):
            raise SourceError("invalid path")
        text = self._cat_many(sha, [path]).get(path)
        if text is None:
            raise SourceError(f"{path!r} not found at {ref}")
        lines = text.splitlines()
        start = max(1, int(start or 1))
        end = min(len(lines), int(end) if end else start + 299, start + 799)
        return {"ref": ref, "sha": sha, "path": path, "start": start, "end": end, "total": len(lines),
                "url": self._blob_url(sha, path, start), "lines": lines[start - 1:end]}

    def refs(self, pattern: str = "", limit: int = 60) -> list[str]:
        out = self._git("for-each-ref", "--sort=-version:refname", "--format=%(refname:short)",
                        "refs/tags", "refs/heads", "refs/remotes", timeout=30).decode().split()
        out = [r for r in out if not r.endswith("/HEAD")]
        if pattern:
            out = [r for r in out if pattern.lower() in r.lower()]
        return out[:limit]

    def definition(self, symbol: str, ref=None) -> dict:
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]{0,100}$", symbol):
            raise SourceError("symbol must be a Go identifier (e.g. NodePool, HostedClusterSpec)")
        pat = (rf"^type {symbol}( |\[)|^func (\([^)]*\) )?{symbol}\(|^\s+{symbol}\s+[^\s]+\s+`json:"
               rf"|^\s*kind: {symbol}\s*$|^\s+{symbol}( |\s*=)")
        res = self.grep(pat, ref=ref, regex=True, limit=40)
        # Order: type definitions first, then funcs, then fields/consts/CRDs.
        def rank(h):
            t = h["text"]
            return 0 if t.startswith(f"type {symbol}") else 1 if t.startswith("func") else 2
        res["hits"].sort(key=rank)
        block = None
        if res["hits"] and rank(res["hits"][0]) < 2:
            h = res["hits"][0]
            shown = self.show(h["path"], ref=res["sha"], start=max(1, h["line"] - 8), end=h["line"] + 150)
            lines, depth, cut = shown["lines"], 0, None
            for i, ln in enumerate(lines[8:], start=8):
                depth += ln.count("{") - ln.count("}")
                if depth <= 0 and "}" in ln:
                    cut = i + 1
                    break
            shown["lines"] = lines[:cut] if cut else lines
            shown["end"] = shown["start"] + len(shown["lines"]) - 1
            block = shown
        res["definition"] = block
        return res

    # -- sync ---------------------------------------------------------------------------------
    def sync(self) -> str:
        if os.path.isdir(self.path):
            self._git("remote", "update", "--prune", timeout=1800)
            return f"fetched {self.path}"
        if not self.remote:
            return f"skip: {self.path} missing and no remote configured"
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        p = subprocess.run(["git", "clone", "--mirror", "--quiet", self.remote, self.path],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3600)
        if p.returncode:
            return f"clone failed: {p.stderr.decode(errors='replace').strip()[:300]}"
        return f"cloned {self.remote} -> {self.path}"


# --------------------------------------------------------------------------------------------
def _http_get(url: str, cfg: dict, timeout: int = 20, params: dict | None = None) -> bytes:
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    ctx = None
    if url.startswith("https"):
        ctx = ssl.create_default_context(cafile=cfg.get("ca_file") or None)
        if cfg.get("insecure_skip_verify"):
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "team-knowledge-mcp/0.1",
                                               "Accept": "application/json"})
    token = cfg.get("bearer_token")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    # Air-gapped: never let a corporate proxy env var send internal lookups elsewhere unless asked.
    handlers = [] if cfg.get("use_env_proxy") else [urllib.request.ProxyHandler({})]
    if ctx is not None:
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    opener = urllib.request.build_opener(*handlers)
    with opener.open(req, timeout=timeout) as r:
        return r.read()


_TAGS = re.compile(r"<[^>]+>")


def _strip_html(s: str) -> str:
    return html.unescape(_TAGS.sub(" ", s or "")).strip()


class MkDocsSite(Source):
    """A mirrored MkDocs site (Argo CD, HyperShift, Metal3 docs…) via its search/search_index.json."""

    kind = "mkdocs_site"

    def __init__(self, cfg, cache_dir):
        super().__init__(cfg, cache_dir)
        self.url = cfg["url"].rstrip("/")
        self.index_url = cfg.get("index_url") or f"{self.url}/search/search_index.json"
        self.ttl = int(cfg.get("refresh_hours", 24)) * 3600
        self._docs: list[dict] | None = None
        self._loaded_at = 0.0

    def available(self):
        try:
            _http_get(self.index_url, self.cfg, timeout=5)
            return True, self.index_url
        except Exception as e:  # noqa: BLE001
            return False, f"{self.index_url}: {e}"

    def _load(self) -> list[dict]:
        if self._docs is None or time.time() - self._loaded_at > self.ttl:
            data = json.loads(_http_get(self.index_url, self.cfg, timeout=60))
            self._docs = data.get("docs", [])
            self._loaded_at = time.time()
        return self._docs

    def _index(self) -> BM25Index:
        with self._lock:
            docs = self._load()
            sig = hashlib.sha256(json.dumps([d.get("location") for d in docs]).encode()
                                 + str(sum(len(d.get("text", "")) for d in docs)).encode()).hexdigest()

            def build():
                chunks, titles = [], {}
                for d in docs:
                    loc = d.get("location", "")
                    page = loc.split("#", 1)[0]
                    if "#" not in loc:
                        titles[page] = _strip_html(d.get("title", ""))
                for d in docs:
                    loc = d.get("location", "")
                    page = loc.split("#", 1)[0]
                    text = _strip_html(d.get("text", ""))
                    if not text:
                        continue
                    heading = _strip_html(d.get("title", "")) if "#" in loc else ""
                    chunks.append(Chunk(page or "index", titles.get(page, page), heading, text,
                                        f"{self.url}/{loc}"))
                return chunks

            return load_or_build(self.cache_dir, self.name, sig, build)

    def search(self, query, limit, **kw):
        return [_hit(self.name, c, s, query) for s, c in self._index().search(query, limit)]

    def read(self, doc_id, **kw):
        page = doc_id.split("#", 1)[0]
        parts = []
        for d in self._load():
            loc = d.get("location", "")
            if loc.split("#", 1)[0] == page:
                title = _strip_html(d.get("title", ""))
                parts.append((f"## {title}\n\n" if "#" in loc else f"# {title}\n\n") + _strip_html(d.get("text", "")))
        if not parts:
            raise SourceError(f"page {doc_id!r} not found in {self.name}")
        return {"title": page, "location": f"{self.url}/{page}", "text": "\n\n".join(parts)}

    def warm(self):
        return f"{self._index().n} chunks"


# --------------------------------------------------------------------------------------------
class RhokpSolr(Source):
    """Red Hat Offline Knowledge Portal: product docs, KCS solutions/articles, CVEs, errata.

    Queries the portal's Solr core directly (default http://<host>:8983/solr/portal/select).
    Field names and edismax weights follow Red Hat's own okp-mcp (Apache-2.0).
    """

    kind = "rhokp_solr"
    FL = ("id,allTitle,title,heading_h1,view_uri,documentKind,product,documentation_version,"
          "lastModifiedDate,score,portal_synopsis,cve_threatSeverity")
    QF = "title^5 heading_h1^3 allTitle^3 portal_synopsis main_content content^2 all_content^1"

    def __init__(self, cfg, cache_dir):
        super().__init__(cfg, cache_dir)
        self.url = cfg["url"].rstrip("/")
        self.core = cfg.get("core", "portal")
        self.portal_url = cfg.get("portal_url", "").rstrip("/")   # the RHOKP web UI, for links
        self.default_product = cfg.get("default_product", "")

    @property
    def select(self):
        return f"{self.url}/solr/{self.core}/select"

    def available(self):
        try:
            data = json.loads(_http_get(self.select, self.cfg, timeout=5, params={"q": "*:*", "rows": 0, "wt": "json"}))
            return True, f"{self.select} ({data.get('response', {}).get('numFound', '?')} documents)"
        except Exception as e:  # noqa: BLE001
            return False, f"{self.select}: {e}"

    @staticmethod
    def _phrase(v: str) -> str:
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def _link(self, doc: dict) -> str:
        uri = (doc.get("view_uri") or doc.get("id") or "")
        uri = uri[: -len("/index.html")] if uri.endswith("/index.html") else uri
        return f"{self.portal_url}{uri}" if self.portal_url and uri.startswith("/") else uri

    def search(self, query, limit, product=None, version=None, doc_kind=None, **kw):
        fq = []
        product = product if product is not None else self.default_product
        if product:
            fq.append(f"product:{self._phrase(product)}")
        if version:
            fq.append(f"documentation_version:{self._phrase(version)}")
        if doc_kind:
            fq.append(f"documentKind:{self._phrase(doc_kind)}")
        params = {
            "q": query, "defType": "edismax", "qf": self.QF, "fl": self.FL, "rows": limit, "wt": "json",
            "hl": "true", "hl.fl": "main_content", "hl.snippets": "2", "hl.fragsize": "300",
            "hl.method": "unified", "hl.defaultSummary": "true",
        }
        if fq:
            params["fq"] = fq
        data = json.loads(_http_get(self.select, self.cfg, timeout=30, params=params))
        hl = data.get("highlighting", {})
        hits = []
        for d in data.get("response", {}).get("docs", []):
            frag = " … ".join(hl.get(d.get("id"), {}).get("main_content", []) or [])
            frag = _strip_html(frag.replace("<em>", "**").replace("</em>", "**")) or _strip_html(d.get("portal_synopsis", ""))
            title = d.get("title") or d.get("allTitle") or d.get("heading_h1") or d.get("id")
            if isinstance(title, list):
                title = title[0]
            meta = {k: d[k] for k in ("documentKind", "product", "documentation_version", "lastModifiedDate",
                                      "cve_threatSeverity") if d.get(k)}
            hits.append({"source": self.name, "id": d.get("view_uri") or d.get("id"), "title": title,
                         "heading": "", "location": self._link(d), "snippet": " ".join(frag.split())[:400],
                         "score": round(float(d.get("score", 0)), 3), "meta": meta})
        return hits

    def read(self, doc_id, **kw):
        fq = f"id:{self._phrase(doc_id)} OR view_uri:{self._phrase(doc_id)}"
        params = {"q": "*:*", "fq": fq, "rows": 1, "wt": "json",
                  "fl": "id,title,allTitle,view_uri,main_content,product,documentation_version,documentKind"}
        docs = json.loads(_http_get(self.select, self.cfg, timeout=30, params=params)).get("response", {}).get("docs", [])
        if not docs:
            raise SourceError(f"document {doc_id!r} not found in RHOKP")
        d = docs[0]
        title = d.get("title") or d.get("allTitle") or doc_id
        if isinstance(title, list):
            title = title[0]
        body = d.get("main_content") or ""
        if isinstance(body, list):
            body = "\n\n".join(body)
        return {"title": title, "location": self._link(d), "text": _strip_html(body) if "<" in body else body}


KINDS = {c.kind: c for c in (MarkdownDir, GitRepo, MkDocsSite, RhokpSolr)}


def build_sources(cfg: dict) -> dict[str, Source]:
    out = {}
    for s in cfg["sources"]:
        cls = KINDS.get(s.get("kind"))
        if not cls:
            raise ValueError(f"source {s.get('name')}: unknown kind {s.get('kind')!r}; known: {sorted(KINDS)}")
        out[s["name"]] = cls(s, cfg["cache_dir"])
    return out
