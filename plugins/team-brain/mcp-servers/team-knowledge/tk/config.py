"""Load sources.json with ${VAR:-default} expansion and glob helpers."""
from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def expand(value: Any) -> Any:
    """Recursively expand ${VAR} / ${VAR:-default} and a leading ~ in strings."""
    if isinstance(value, str):
        out = _VAR.sub(lambda m: os.environ.get(m.group(1)) or (m.group(2) or ""), value)
        return os.path.expanduser(out) if out.startswith("~") else out
    if isinstance(value, list):
        return [expand(v) for v in value]
    if isinstance(value, dict):
        return {k: expand(v) for k, v in value.items()}
    return value


def default_config_path() -> Path:
    env = os.environ.get("TEAM_KNOWLEDGE_CONFIG")
    if env:
        return Path(os.path.expanduser(env))
    brain = os.path.expanduser(os.environ.get("TEAM_BRAIN_DIR") or "~/team-brain")
    return Path(brain) / "mcp" / "sources.json"


def load_config(path: Path | None = None) -> dict:
    path = path or default_config_path()
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    cfg = expand(raw)
    cfg.setdefault("cache_dir", os.path.expanduser("~/.cache/team-brain/team-knowledge"))
    cfg["sources"] = [s for s in cfg.get("sources", []) if s.get("enabled", True)]
    names = [s["name"] for s in cfg["sources"]]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise ValueError(f"duplicate source names in {path}: {sorted(dupes)}")
    cfg["_path"] = str(path)
    return cfg


@lru_cache(maxsize=512)
def glob_to_regex(pattern: str) -> re.Pattern:
    """Glob with ** support: '**/' = any dirs (incl. none), '**' = anything, '*' = within a segment."""
    i, out = 0, []
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def matches(path: str, includes: list[str], excludes: list[str] | None = None) -> bool:
    if excludes and any(glob_to_regex(p).match(path) for p in excludes):
        return False
    return any(glob_to_regex(p).match(path) for p in includes)
