#!/usr/bin/env python3
"""Mirror the Portworx Enterprise docs (latest version) into docs/upstream/portworx as Markdown-ish text.

docs.portworx.com has no public source repo, so this crawls the site's own sitemap. Unversioned URLs
(/portworx-enterprise/<page>) are the latest release; the version is read from the versions menu.
Run on a connected host, then commit the result (docs/upstream is generated — don't hand-edit):

    python3 scripts/sync-portworx-docs.py [--base https://docs.portworx.com] [--product portworx-enterprise]

Stdlib only. Polite: 4 workers, retries, identifies itself.
"""
import argparse, concurrent.futures as cf, re, sys, time, urllib.request
from html.parser import HTMLParser
from pathlib import Path

SKIP = {"script", "style", "nav", "footer", "header", "aside", "form", "svg", "noscript", "button"}
BLOCK = {"p", "div", "section", "article", "li", "tr", "table", "ul", "ol", "pre", "blockquote", "br"}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.in_main, self.pre = [], 0, False, False
        self.has_main = False
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "main" or (tag == "article" and not self.has_main):
            self.in_main = self.has_main = True
        if tag == "title":
            self._in_title = True
        if tag in SKIP:
            self.skip += 1
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag == "pre":
            self.pre = True
            self.out.append("\n\n```\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "pre":
            self.pre = False
            self.out.append("\n```\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        elif tag in BLOCK or tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self.skip:
            self.out.append(data if self.pre else re.sub(r"\s+", " ", data))

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+\n", "\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip() + "\n"


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "team-brain-docs-sync/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://docs.portworx.com")
    ap.add_argument("--product", default="portworx-enterprise")
    a = ap.parse_args()
    root = Path(__file__).resolve().parent.parent / "docs/upstream" / a.product.replace("portworx-enterprise", "portworx")
    sm = get(f"{a.base}/{a.product}/sitemap.xml")
    urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", sm)
            if not re.search(rf"/{a.product}/\d+\.\d+(/|$)", u)]  # latest only
    print(f"{len(urls)} pages")
    seen = []  # per-page "Version: X.Y" banner; unversioned URLs are the latest release
    if root.exists():
        for p in root.rglob("*.md"):
            p.unlink()
    root.mkdir(parents=True, exist_ok=True)

    def one(u):
        try:
            ex = Extract()
            ex.feed(get(u))
            body = ex.text()
            m = re.search(r"^Version:\s*(\d+\.\d+)\s*$", body, re.M)
            if m:
                seen.append(m.group(1))
            body = re.sub(r"^(Skip to main content|Version:\s*\S+)\s*$\n?", "", body, flags=re.M)
            body = re.sub(r"\n{3,}", "\n\n", body)
            if len(body) < 80:
                return u, "empty"
            rel = u.split(f"/{a.product}/", 1)[-1].strip("/") or "index"
            f = root / (rel + ".md")
            f.parent.mkdir(parents=True, exist_ok=True)
            title = re.sub(r"\s*\|.*$", "", ex.title).strip() or rel
            f.write_text(f"# {title}\n\nSource: {u} (Portworx Enterprise latest)\n\n{body}", encoding="utf-8")
            return u, "ok"
        except Exception as e:
            return u, f"error: {e}"

    ok = bad = 0
    with cf.ThreadPoolExecutor(4) as ex:
        for u, st in ex.map(one, urls):
            if st == "ok":
                ok += 1
            else:
                bad += 1
                print(f"  skip {u}: {st}", file=sys.stderr)
    latest = max(set(seen), key=seen.count) if seen else "unknown"
    print(f"latest version (from page banners): {latest}")
    (root / ".upstream").write_text(
        f"site: {a.base}/{a.product}/\nversion: {latest}\npages: {ok}\nsynced: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
    print(f"wrote {ok} pages to {root} ({bad} skipped)")


if __name__ == "__main__":
    main()
