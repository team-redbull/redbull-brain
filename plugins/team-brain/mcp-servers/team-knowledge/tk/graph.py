"""Link graph over the documents of one source: who links to whom, and which pages share tags.

Built from the text alone (stdlib only), so a page found by `search` can be followed to its neighbours
without more searches. Edges come from Markdown links, `[[wikilinks]]` and `path/to/page.md` mentions in
backticks; tags and area come from the brain's frontmatter.
"""
from __future__ import annotations

import math
import posixpath
import re
from collections import defaultdict

from .textindex import _FRONTMATTER, doc_title

_MD_LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)")
_WIKI = re.compile(r"\[\[([^\]|#]+)")
_TICK = re.compile(r"`([A-Za-z0-9_.\-/]+\.(?:md|rst|adoc))`")
_TAGS = re.compile(r"^tags:\s*\[(.*?)\]\s*$", re.M)
_AREA = re.compile(r"^area:\s*(\S+)\s*$", re.M)
_EXT = (".md", ".rst", ".adoc", ".markdown")


class Graph:
    def __init__(self, texts: dict[str, str]):
        ids = set(texts)
        by_base: dict[str, list[str]] = defaultdict(list)
        for i in ids:
            base = posixpath.basename(i)
            by_base[base].append(i)
            by_base[base.rsplit(".", 1)[0]].append(i)
        self.title, self.tags, self.area = {}, {}, {}
        self.out: dict[str, list[str]] = {}
        self.back: dict[str, list[str]] = defaultdict(list)
        for i, text in texts.items():
            self.title[i] = doc_title(i, text)
            fm = _FRONTMATTER.match(text)
            head = fm.group(1) if fm else ""
            t = _TAGS.search(head)
            self.tags[i] = [x.strip().strip("\"'") for x in t.group(1).split(",") if x.strip()] if t else []
            a = _AREA.search(head)
            self.area[i] = a.group(1) if a else ""
            found: list[str] = []
            here = posixpath.dirname(i)
            for m in _MD_LINK.finditer(text):
                target = m.group(1).split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                for cand in (posixpath.normpath(posixpath.join(here, target)), target.lstrip("/")):
                    hit = self._match(cand, ids)
                    if hit:
                        found.append(hit)
                        break
            for m in _TICK.finditer(text):  # repo-root paths in backticks, the brain's usual way to cite a page
                hit = self._match(m.group(1), ids)
                if hit:
                    found.append(hit)
            for m in _WIKI.finditer(text):
                cands = by_base.get(m.group(1).strip()) or []
                if len(cands) == 1:
                    found.append(cands[0])
            self.out[i] = [x for x in dict.fromkeys(found) if x != i]
        for i, targets in self.out.items():
            for t in targets:
                self.back[t].append(i)
        self.tag_pages: dict[str, list[str]] = defaultdict(list)
        for i, tags in self.tags.items():
            for t in tags:
                self.tag_pages[t].append(i)

    @staticmethod
    def _match(cand: str, ids: set[str]) -> str | None:
        if cand in ids:
            return cand
        for ext in _EXT:  # links written without extension, or to a directory index
            for c in (cand + ext, posixpath.join(cand, "_index" + ext), posixpath.join(cand, "index" + ext),
                      posixpath.join(cand, "README" + ext)):
                if c in ids:
                    return c
        return None

    def similar(self, doc_id: str, limit: int) -> list[tuple[str, list[str]]]:
        """Pages sharing tags, rarest tags weighing most; same area breaks ties."""
        n = len(self.title) or 1
        scores: dict[str, float] = defaultdict(float)
        shared: dict[str, list[str]] = defaultdict(list)
        for t in self.tags.get(doc_id, []):
            pages = self.tag_pages[t]
            for other in pages:
                if other != doc_id:
                    scores[other] += math.log(1 + n / len(pages))
                    shared[other].append(t)
        for other in scores:
            if self.area.get(other) and self.area[other] == self.area.get(doc_id):
                scores[other] += 0.5
        ranked = sorted(scores, key=lambda o: (-scores[o], o))[:limit]
        return [(o, shared[o]) for o in ranked]

    def stats(self) -> str:
        edges = sum(len(v) for v in self.out.values())
        orphans = sum(1 for i in self.title if not self.out[i] and not self.back.get(i))
        return f"{len(self.title)} pages, {edges} links, {len(self.tag_pages)} tags, {orphans} unlinked pages"
