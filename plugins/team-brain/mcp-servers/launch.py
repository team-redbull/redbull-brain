#!/usr/bin/env python3
"""Run a third-party MCP server from the archive shipped inside this plugin (air gap: nothing to download).

    launch.py <server> [args…]        # what .mcp.json calls
    launch.py --check                 # show, per server, which binary would run on this machine

Order: $TEAM_BRAIN_MCP_<SERVER>_BIN if set → the archive in vendor/<server>/ for this OS/CPU (sha256 checked
against vendor/manifest.json, unpacked once into the cache) → the binary on PATH. Stdlib only.
Archives are refreshed on a connected host with scripts/fetch-mcp-binaries.py.
"""
import hashlib, json, os, platform, shutil, subprocess, sys, tarfile, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
ARCH = {"amd64": "x86_64", "x64": "x86_64", "aarch64": "arm64"}


def plat():
    machine = platform.machine().lower()
    return f"{platform.system().lower()}-{ARCH.get(machine, machine)}"


def cache_dir():
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.environ.get("TEAM_KNOWLEDGE_CACHE") \
        or os.path.join(os.path.expanduser("~"), ".cache", "team-brain")
    return Path(base) / "mcp-bin"


def resolve(name):
    """Return (path, how). Raises SystemExit with an actionable message when nothing can run."""
    override = os.environ.get(f"TEAM_BRAIN_MCP_{name.upper().replace('-', '_')}_BIN")
    if override:
        return override, "env override"
    manifest = json.loads((VENDOR / "manifest.json").read_text()) if (VENDOR / "manifest.json").is_file() else {}
    spec = manifest.get(name)
    if not spec:
        sys.exit(f"launch.py: no MCP server {name!r} in {VENDOR / 'manifest.json'} (known: {', '.join(manifest) or 'none'})")
    exe = spec["binary"] + (".exe" if os.name == "nt" else "")
    asset = spec["assets"].get(plat())
    if asset:
        out = cache_dir() / name / spec["version"] / plat() / exe
        if not out.is_file():
            archive = VENDOR / name / asset["file"]
            if hashlib.sha256(archive.read_bytes()).hexdigest() != asset["sha256"]:
                sys.exit(f"launch.py: {archive} does not match the sha256 in manifest.json — refusing to run it")
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.with_name(out.name + f".{os.getpid()}.tmp")
            if archive.name.endswith(".zip"):
                with zipfile.ZipFile(archive) as z, z.open(exe) as src, open(tmp, "wb") as dst:
                    shutil.copyfileobj(src, dst)
            else:
                with tarfile.open(archive) as t, t.extractfile(exe) as src, open(tmp, "wb") as dst:
                    shutil.copyfileobj(src, dst)
            os.chmod(tmp, 0o755)
            os.replace(tmp, out)
        return str(out), f"vendored {spec['version']}"
    found = shutil.which(spec["binary"])
    if found:
        return found, "PATH"
    sys.exit(f"launch.py: no {spec['binary']} archive for {plat()} in the plugin (have: {', '.join(spec['assets'])}) "
             f"and none on PATH. Add the platform in scripts/fetch-mcp-binaries.py on a connected host, or set "
             f"TEAM_BRAIN_MCP_{name.upper()}_BIN.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--check":
        manifest = json.loads((VENDOR / "manifest.json").read_text())
        for name in manifest:
            try:
                path, how = resolve(name)
                print(f"{name}: {path} ({how})")
            except SystemExit as e:
                print(f"{name}: NOT AVAILABLE — {e}")
        return
    path, _ = resolve(sys.argv[1])
    argv = [path, *sys.argv[2:]]
    if os.name == "nt":  # no exec on Windows: stay as the parent and pass stdio through
        sys.exit(subprocess.call(argv))
    os.execv(path, argv)


if __name__ == "__main__":
    main()
