"""Small BM25 index over heading-sized chunks of Markdown / AsciiDoc / plain text.

Stdlib only. Built lazily per source, cached to disk as a pickle keyed by a content signature.
"""
from __future__ import annotations

import math
import os
import pickle
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

_TOKEN = re.compile(r"[a-z0-9_]+(?:[.\-/:][a-z0-9_]+)*")
_SPLIT = re.compile(r"[.\-/:]")
_HEADING = re.compile(r"^(#{1,4}|={1,4})\s+(.+?)\s*#*\s*$")
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_TITLE_FM = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.M)

STOP = frozenset(
    "a an and are as at be by can do does for from get got how i if in into is it its of on or out "
    "so than that the then there these this to up was we were what when where which why will with "
    "you your".split()
)

CHUNK_MAX = 2500
INDEX_FORMAT = 4  # bump when tokenization or chunking changes, to invalidate caches


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for m in _TOKEN.finditer(text.lower()):
        tok = m.group(0)
        if tok not in STOP:
            out.append(tok)
        if any(c in tok for c in ".-/:"):
            out.extend(p for p in _SPLIT.split(tok) if p and p not in STOP)
    return out


@dataclass
class Chunk:
    doc_id: str
    title: str
    heading: str
    text: str
    location: str = ""      # URL or path shown to the user
    meta: dict = field(default_factory=dict)


def doc_title(doc_id: str, text: str) -> str:
    fm = _FRONTMATTER.match(text)
    if fm:
        t = _TITLE_FM.search(fm.group(1))
        if t:
            return t.group(1)
    for line in text.splitlines()[:40]:
        h = _HEADING.match(line)
        if h:
            return h.group(2)
    return os.path.basename(doc_id)


def chunk_document(doc_id: str, text: str, location: str = "", meta: dict | None = None) -> list[Chunk]:
    title = doc_title(doc_id, text)
    body = _FRONTMATTER.sub("", text, count=1)
    chunks: list[Chunk] = []
    heading, buf = "", []

    def flush():
        joined = "\n".join(buf).strip()
        if not joined:
            return
        while joined:
            part, joined = joined[:CHUNK_MAX], joined[CHUNK_MAX:]
            if joined:  # cut at a paragraph boundary when possible
                cut = part.rfind("\n\n")
                if cut > CHUNK_MAX // 2:
                    joined = part[cut:] + joined
                    part = part[:cut]
            chunks.append(Chunk(doc_id, title, heading, part.strip(), location, meta or {}))

    for line in body.splitlines():
        h = _HEADING.match(line)
        if h:
            flush()
            heading, buf = h.group(2), []
        else:
            buf.append(line)
    flush()
    if not chunks:
        chunks.append(Chunk(doc_id, title, "", body[:CHUNK_MAX], location, meta or {}))
    return chunks


class BM25Index:
    k1, b = 1.2, 0.75

    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.lengths: list[int] = []
        for i, c in enumerate(chunks):
            # Title + heading count double so a page *about* the term outranks a passing mention.
            toks = tokenize(f"{c.title} {c.heading}") * 2 + tokenize(c.text)
            self.lengths.append(len(toks) or 1)
            for tok, tf in Counter(toks).items():
                self.postings[tok].append((i, tf))
        self.postings = dict(self.postings)
        self.avgdl = (sum(self.lengths) / len(self.lengths)) if self.lengths else 1.0
        self.n = len(chunks)

    def search(self, query: str, limit: int = 10, per_doc: int = 1) -> list[tuple[float, Chunk]]:
        terms = list(dict.fromkeys(tokenize(query)))
        if not terms or not self.n:
            return []
        scores: dict[int, float] = defaultdict(float)
        matched: dict[int, int] = defaultdict(int)
        for t in terms:
            plist = self.postings.get(t)
            if not plist:
                continue
            idf = math.log(1 + (self.n - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, tf in plist:
                dl = self.lengths[i]
                scores[i] += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
                matched[i] += 1
        # Drop chunks that share only a stray word with a multi-term query.
        if len(terms) >= 3:
            need = max(2, math.ceil(len(terms) * 0.34))
            scores = defaultdict(float, {i: s for i, s in scores.items() if matched[i] >= need})
        phrase = query.lower().strip()
        if len(phrase) > 6:
            for i in list(scores):
                if phrase in self.chunks[i].text.lower():
                    scores[i] *= 1.5
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        out, seen = [], Counter()
        for i, s in ranked:
            c = self.chunks[i]
            if seen[c.doc_id] >= per_doc:
                continue
            seen[c.doc_id] += 1
            out.append((s, c))
            if len(out) >= limit:
                break
        return out


def snippet(text: str, query: str, width: int = 320) -> str:
    terms = [t for t in tokenize(query) if len(t) > 2]
    low = text.lower()
    pos = -1
    for t in sorted(terms, key=len, reverse=True):
        pos = low.find(t)
        if pos >= 0:
            break
    start = max(0, pos - width // 3) if pos >= 0 else 0
    s = " ".join(text[start:start + width].split())
    return ("…" if start else "") + s + ("…" if start + width < len(text) else "")


def load_or_build(cache_dir: str, name: str, signature: str, builder) -> BM25Index:
    """Return a cached index if the signature matches, else build and cache it."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"{name}.idx.pkl")
    try:
        with open(path, "rb") as f:
            fmt, sig, idx = pickle.load(f)
        if fmt == INDEX_FORMAT and sig == signature:
            return idx
    except (OSError, EOFError, pickle.UnpicklingError, ValueError, AttributeError):
        pass
    idx = BM25Index(builder())
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump((INDEX_FORMAT, signature, idx), f, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(tmp, path)
    return idx
