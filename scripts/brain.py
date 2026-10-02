#!/usr/bin/env python3
"""team-brain maintenance: validate | index | stale. Stdlib only (Python >= 3.9).

  python3 scripts/brain.py validate          frontmatter schema + secret scan + broken internal links
  python3 scripts/brain.py index [--check]   regenerate INDEX.md (--check: fail if out of date)
  python3 scripts/brain.py stale --days 180  pages whose last_verified is older than N days
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = ["knowledge", "runbooks", "incidents", "inbox", "mcp/servers", "docs"]
SKIP_DIRS = {"docs/upstream"}
TYPES = {"knowledge", "runbook", "incident", "inbox", "mcp", "reference"}
AREAS = {"openshift", "kubernetes", "hypershift", "baremetal", "vsphere", "networking", "storage", "gpu",
         "observability", "registry-mirroring", "gitops", "security", "meta"}
CONFIDENCE = {"verified", "observed", "hypothesis"}
REQUIRED = ["title", "type", "area", "tags", "applies_to", "confidence", "last_verified", "owners"]
INCIDENT_REQUIRED = ["severity", "status", "clusters", "started"]
DIR_TYPE = {"knowledge": "knowledge", "runbooks": "runbook", "incidents": "incident", "inbox": "inbox",
            "mcp/servers": "mcp"}

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----")),
    ("pull-secret auth", re.compile(r'"auth"\s*:\s*"[A-Za-z0-9+/=]{24,}"')),
    ("kubeconfig key/cert data", re.compile(r"(?:client-key-data|client-certificate-data|certificate-authority-data)\s*:\s*[A-Za-z0-9+/=]{40,}")),
    ("OpenShift OAuth token", re.compile(r"sha256~[A-Za-z0-9_-]{20,}")),
    ("JWT / service-account token", re.compile(r"eyJhbGciOi[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("GitLab token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("RHOKP / Red Hat access key", re.compile(r"rhn-support-[A-Za-z0-9]+_[A-Za-z0-9_]{10,}")),
    ("bearer token", re.compile(r"[Bb]earer\s+[A-Za-z0-9._~+/-]{30,}")),
    ("password assignment", re.compile(r"(?i)\b(?:password|passwd|pwd|secret)\b\s*[:=]\s*[\"']?(?!<|\$\{|\$\(|\"\"|''|REDACTED|changeme|xxx)[^\s\"'<>{}]{6,}")),
]
ALLOW_MARK = "brain:allow-secret"

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK = re.compile(r"\[\[([^\]]+)\]\]|\]\((?!https?://|#|mailto:)([^)\s]+\.md)(?:#[^)]*)?\)")


def parse_frontmatter(text: str) -> dict | None:
    """Minimal YAML subset: `key: scalar` and `key: [a, b]` (enough for our schema)."""
    m = FM.match(text)
    if not m:
        return None
    out: dict = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.split(" #", 1)[0].strip()
        if val.startswith("[") and val.endswith("]"):
            out[key.strip()] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        else:
            out[key.strip()] = val.strip("'\"")
    return out


def content_files() -> list[Path]:
    files = []
    for d in CONTENT_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            rel = p.relative_to(ROOT).as_posix()
            if any(rel.startswith(s + "/") for s in SKIP_DIRS) or p.name == "README.md":
                continue
            files.append(p)
    return files


def all_text_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT).as_posix()
        if not p.is_file() or rel.startswith((".git/", "docs/upstream/")) or "/__pycache__/" in f"/{rel}":
            continue
        if p.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".sh", ".py", ".txt", ".toml", ".adoc", ".env"} \
                or p.name in {"Containerfile", "Dockerfile"}:
            out.append(p)
    return out


def scan_secrets() -> list[str]:
    errs = []
    self_path = Path(__file__).resolve()
    for p in all_text_files():
        if p.resolve() == self_path:
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            if ALLOW_MARK in line:
                continue
            for label, rx in SECRET_PATTERNS:
                if rx.search(line):
                    errs.append(f"{p.relative_to(ROOT)}:{n}: possible {label} — redact it "
                                f"(or append '{ALLOW_MARK}' if it is a harmless example)")
    return errs


def validate() -> int:
    errors, warnings = [], []
    for p in content_files():
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8", errors="replace")
        if p.name.startswith("_template"):
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing frontmatter (see docs/FRONTMATTER.md)")
            continue
        for k in REQUIRED:
            if k not in fm:
                errors.append(f"{rel}: missing '{k}'")
        if fm.get("type") and fm["type"] not in TYPES:
            errors.append(f"{rel}: type '{fm['type']}' not in {sorted(TYPES)}")
        if fm.get("area") and fm["area"] not in AREAS:
            warnings.append(f"{rel}: new area '{fm['area']}' — add it to AREAS in scripts/brain.py and CLAUDE.md if intended")
        if fm.get("confidence") and fm["confidence"] not in CONFIDENCE:
            errors.append(f"{rel}: confidence must be one of {sorted(CONFIDENCE)}")
        lv = fm.get("last_verified", "")
        try:
            if dt.date.fromisoformat(lv) > dt.date.today() + dt.timedelta(days=1):
                errors.append(f"{rel}: last_verified is in the future")
        except ValueError:
            if lv:
                errors.append(f"{rel}: last_verified '{lv}' is not YYYY-MM-DD")
        for k in ("tags", "applies_to", "owners"):
            if k in fm and not isinstance(fm[k], list):
                errors.append(f"{rel}: '{k}' must be a [list]")
        for d, t in DIR_TYPE.items():
            if rel.startswith(d + "/") and fm.get("type") and fm["type"] != t:
                errors.append(f"{rel}: files under {d}/ must have type '{t}'")
        if fm.get("type") == "incident":
            for k in INCIDENT_REQUIRED:
                if k not in fm:
                    errors.append(f"{rel}: incident missing '{k}'")
        if "<Title>" in text or "YYYY-MM-DD" in text.split("## History")[0]:
            warnings.append(f"{rel}: still contains template placeholders")
        for m in LINK.finditer(text):
            target = (m.group(1) or m.group(2)).split("|")[0].strip()
            cand = [ROOT / target, p.parent / target]
            if not any(c.exists() for c in cand):
                warnings.append(f"{rel}: link to missing page '{target}'")
    errors += scan_secrets()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR:   {e}")
    print(f"\n{len(content_files())} pages checked — {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def render_index() -> str:
    groups: dict[tuple[str, str], list[tuple[str, dict]]] = {}
    for p in content_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("docs/"):
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace")) or {}
        groups.setdefault((fm.get("type", "?"), fm.get("area", "?")), []).append((rel, fm))
    order = ["knowledge", "runbook", "incident", "inbox", "mcp"]
    lines = ["# Team brain index", "",
             "_Generated by `python3 scripts/brain.py index` — do not edit by hand._", ""]
    for t in order + sorted({k[0] for k in groups} - set(order)):
        areas = sorted(a for (tt, a) in groups if tt == t)
        if not areas:
            continue
        heading = {"knowledge": "Knowledge", "runbook": "Runbooks", "incident": "Incidents",
                   "inbox": "Inbox (uncurated)", "mcp": "MCP servers"}.get(t, t.capitalize())
        lines += [f"## {heading}", ""]
        for a in areas:
            lines += [f"### {a}", "", "| Page | Applies to | Confidence | Verified |", "|---|---|---|---|"]
            for rel, fm in sorted(groups[(t, a)], key=lambda x: x[1].get("title", x[0]).lower()):
                applies = ", ".join(fm.get("applies_to") or []) or "general"
                title = fm.get("title", rel).replace("|", "\\|")
                lines.append(f"| [{title}]({rel}) | {applies} | {fm.get('confidence', '?')} | {fm.get('last_verified', '?')} |")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def index(check: bool) -> int:
    target = ROOT / "INDEX.md"
    new = render_index()
    if check:
        if not target.exists() or target.read_text(encoding="utf-8") != new:
            print("INDEX.md is out of date — run: python3 scripts/brain.py index")
            return 1
        print("INDEX.md up to date")
        return 0
    target.write_text(new, encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")
    return 0


def stale(days: int) -> int:
    cutoff = dt.date.today() - dt.timedelta(days=days)
    rows = []
    for p in content_files():
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace")) or {}
        try:
            lv = dt.date.fromisoformat(fm.get("last_verified", ""))
        except ValueError:
            continue
        if lv < cutoff and fm.get("type") != "incident":
            rows.append((lv, p.relative_to(ROOT).as_posix(), ", ".join(fm.get("owners") or [])))
    for lv, rel, owners in sorted(rows):
        print(f"{lv}  {rel}  ({owners or 'no owner'})")
    print(f"{len(rows)} pages not verified since {cutoff}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    ip = sub.add_parser("index")
    ip.add_argument("--check", action="store_true")
    sp = sub.add_parser("stale")
    sp.add_argument("--days", type=int, default=180)
    a = ap.parse_args()
    sys.exit({"validate": lambda: validate(), "index": lambda: index(a.check),
              "stale": lambda: stale(a.days)}[a.cmd]())


if __name__ == "__main__":
    main()
