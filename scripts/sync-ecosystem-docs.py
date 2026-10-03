#!/usr/bin/env python3
"""Fetch ONLY the documentation of ecosystem projects into docs/upstream/<name>/ (pinned snapshots).

HyperShift, Ironic, Cluster API and the Agent provider are full git mirrors (code + docs at any ref,
see mcp/sources.json). Everything below is docs-only: sparse, shallow, blobless clone of the default
branch (or REF override), keep only .md/.rst/.adoc files. Run on a connected host, or inside the air
gap with UPSTREAM_GIT_BASE pointing at an internal mirror, then commit the result.

    python3 scripts/sync-ecosystem-docs.py              # all
    python3 scripts/sync-ecosystem-docs.py vllm kserve  # only these
    REF_vllm=v0.11.0 python3 scripts/sync-ecosystem-docs.py vllm   # pin one to the installed version

docs/upstream is generated: don't hand-edit it.
"""
import os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

BASE = os.environ.get("UPSTREAM_GIT_BASE", "https://github.com")
ROOT = Path(__file__).resolve().parent.parent
EXT = (".md", ".markdown", ".rst", ".adoc", ".txt", ".mdx")  # .mdx is stored as .md (the indexer reads .md)

# name: (repo, [paths in repo])  — default branch unless REF_<name> (dashes -> underscores) is set
SOURCES = {
    "ako": ("vmware/load-balancer-and-ingress-services-for-kubernetes", [
        "docs", "README.md", "CHANGELOG.md", "AKO_GATEWAY_CHANGELOG.md", "ako-operator/README.md",
        "ako-crd-operator/README.md", "ako-crd-operator/CHANGELOG.md"]),
    "envoy": ("envoyproxy/envoy", ["docs/root"]),
    "envoy-gateway": ("envoyproxy/gateway", ["site/content/en/latest"]),
    "kserve": ("kserve/kserve", ["docs", "README.md", "charts", "kernelcache/mcv/docs", "ROADMAP.md"]),
    "kserve-website": ("kserve/website", ["docs"]),
    "prometheus-docs": ("prometheus/docs", ["docs"]),
    "prometheus-operator": ("prometheus-operator/prometheus-operator", ["Documentation", "README.md"]),
    "grafana-docs": ("grafana/grafana", ["docs/sources"]),
    "mcp-grafana": ("grafana/mcp-grafana", ["README.md", "docs"]),
    "vllm": ("vllm-project/vllm", ["docs", "examples", "README.md"]),
    "lws": ("kubernetes-sigs/lws", ["site/content/en/docs", "docs", "keps", "README.md"]),
    "metal3-docs": ("metal3-io/metal3-docs", ["docs", "design"]),
    "baremetal-operator": ("metal3-io/baremetal-operator", [
        "docs", "README.md", "config/README.md", "ironic-deployment/README.md"]),
    "cluster-api-provider-metal3": ("metal3-io/cluster-api-provider-metal3", ["docs", "README.md"]),
    "ip-address-manager": ("metal3-io/ip-address-manager", ["docs", "README.md"]),
    "ironic-standalone-operator": ("metal3-io/ironic-standalone-operator", ["docs", "README.md"]),
    "ironic-image": ("metal3-io/ironic-image", ["docs", "README.md"]),
    "gateway-api": ("kubernetes-sigs/gateway-api", ["site/content", "geps"]),
    "gpu-operator": ("NVIDIA/gpu-operator", ["README.md", "docs"]),
    "node-feature-discovery": ("kubernetes-sigs/node-feature-discovery", ["docs"]),
    "kueue": ("kubernetes-sigs/kueue", ["site/content/en/docs", "keps"]),
    "ovn-kubernetes": ("ovn-org/ovn-kubernetes", ["docs"]),
    "multus-cni": ("k8snetworkplumbingwg/multus-cni", ["docs", "README.md"]),
    "openshift-runbooks": ("openshift/runbooks", ["alerts"]),
    "assisted-service": ("openshift/assisted-service", ["docs"]),
    "etcd-docs": ("etcd-io/website", ["content/en/docs"]),
    # inference / HPC / fabrics / kernel tuning
    "llm-d": ("llm-d/llm-d", ["docs", "guides", "README.md"]),
    "sglang": ("sgl-project/sglang", ["docs/docs", "docs/cookbook"]),
    "tensorrt-llm": ("NVIDIA/TensorRT-LLM", ["docs/source"]),
    "dynamo": ("ai-dynamo/dynamo", ["docs"]),
    "ray-docs": ("ray-project/ray", ["doc/source/serve", "doc/source/cluster/kubernetes"]),
    "nccl": ("NVIDIA/nccl", ["docs"]),
    "ucx": ("openucx/ucx", ["docs"]),
    "rdma-core": ("linux-rdma/rdma-core", [
        "Documentation", "README.md", "infiniband-diags/man", "libibverbs/man", "librdmacm/man",
        "libibumad/man", "providers/mlx5/man"]),
    "nvidia-cloud-native-docs": ("NVIDIA/cloud-native-docs", [
        "gpu-operator", "openshift", "mig", "gpu-telemetry", "container-toolkit", "driver-containers", "kubernetes"]),
    "nvidia-network-operator-docs": ("Mellanox/network-operator-docs", ["docs"]),
    "sriov-network-operator": ("k8snetworkplumbingwg/sriov-network-operator", ["doc"]),
    "tuned": ("redhat-performance/tuned", ["doc"]),
    "linux-kernel-docs": ("torvalds/linux", [
        "Documentation/admin-guide/mm", "Documentation/admin-guide/kernel-parameters.txt",
        "Documentation/admin-guide/cputopology.rst", "Documentation/admin-guide/numastat.rst",
        "Documentation/admin-guide/pm", "Documentation/scheduler", "Documentation/infiniband",
        "Documentation/core-api/irq", "Documentation/networking/ip-sysctl.rst",
        "Documentation/networking/scaling.rst", "Documentation/networking/rds.rst",
        "Documentation/networking/tcp-thin.rst", "Documentation/admin-guide/perf",
        "Documentation/admin-guide/sysctl"]),
}


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True,
                          env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}).stdout.strip()


def sync(name, work):
    repo, paths = SOURCES[name]
    ref = os.environ.get("REF_" + name.replace("-", "_"))
    clone = Path(work) / name
    cmd = ["git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--no-checkout"]
    if ref:
        cmd += ["--branch", ref]
    run(*cmd, f"{BASE}/{repo}.git", str(clone))
    run("git", "sparse-checkout", "set", "--no-cone", *[f"/{p}" for p in paths], cwd=clone)
    run("git", "checkout", "--quiet", cwd=clone)
    sha = run("git", "rev-parse", "HEAD", cwd=clone)
    branch = ref or run("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=clone)
    dest = ROOT / "docs/upstream" / name
    if dest.exists():
        shutil.rmtree(dest)
    n = 0
    for p in paths:
        src = clone / p
        files = [src] if src.is_file() else [f for f in src.rglob("*") if f.is_file()]
        for f in files:
            if f.suffix.lower() in EXT:
                out = dest / f.relative_to(clone)
                if out.suffix.lower() == ".mdx":
                    out = out.with_suffix(".md")
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)
                n += 1
    dest.mkdir(parents=True, exist_ok=True)
    (dest / ".upstream").write_text(
        f"repo: {repo}\nref: {branch}\ncommit: {sha}\npaths: {', '.join(paths)}\n"
        f"synced: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
    return n, branch, sha[:10]


def main():
    names = sys.argv[1:] or list(SOURCES)
    bad = [n for n in names if n not in SOURCES]
    if bad:
        sys.exit(f"unknown: {', '.join(bad)}; known: {', '.join(SOURCES)}")
    failed = []
    with tempfile.TemporaryDirectory() as work:
        for n in names:
            try:
                files, branch, sha = sync(n, work)
                print(f"{n}: {files} files @ {branch} {sha}")
                shutil.rmtree(Path(work) / n, ignore_errors=True)
            except subprocess.CalledProcessError as e:
                failed.append(n)
                print(f"{n}: FAILED {(e.stderr or '').strip()[:200]}", file=sys.stderr)
    if failed:
        sys.exit(f"failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
