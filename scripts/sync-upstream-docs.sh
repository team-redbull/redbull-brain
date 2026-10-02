#!/usr/bin/env bash
# Refresh pinned upstream docs under docs/upstream/ (searched by the team-knowledge MCP server).
# Run on a host that can reach the git source — upstream GitHub on a connected host, or your
# internal mirror inside the air gap (set UPSTREAM_GIT_BASE). Commit the result (or move it across
# the gap with your usual transfer process).
#
#   K8S_DOCS_REF=release-1.31 scripts/sync-upstream-docs.sh
#
# OpenShift / ACM / MCE product docs are NOT mirrored here: RHOKP already serves them, with KCS.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="${UPSTREAM_GIT_BASE:-https://github.com}"
K8S_REF="${K8S_DOCS_REF:-release-1.35}"   # newest OCP in the fleet (4.22 = Kubernetes 1.35); bump with the fleet
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

sparse_copy() {  # <repo> <ref> <subdir-in-repo> <dest-under-docs/upstream>
  local repo="$1" ref="$2" sub="$3" dest="$ROOT/docs/upstream/$4"
  echo "==> $repo@$ref:$sub -> docs/upstream/$4"
  git clone --quiet --depth 1 --branch "$ref" --filter=blob:none --sparse "$BASE/$repo.git" "$WORK/$4"
  git -C "$WORK/$4" sparse-checkout set "$sub"
  local sha; sha="$(git -C "$WORK/$4" rev-parse HEAD)"
  rm -rf "$dest"; mkdir -p "$dest"
  cp -a "$WORK/$4/$sub/." "$dest/"
  # Hugo shortcodes and front matter stay; they are harmless for full-text search.
  printf 'repo: %s\nref: %s\ncommit: %s\npath: %s\nsynced: %s\n' "$repo" "$ref" "$sha" "$sub" "$(date -u +%FT%TZ)" > "$dest/.upstream"
  echo "    $(find "$dest" -name '*.md' | wc -l) markdown files, commit ${sha:0:10}"
}

sparse_copy kubernetes/website "$K8S_REF" content/en/docs kubernetes
# Add more as needed, e.g. Gateway API:
# sparse_copy kubernetes-sigs/gateway-api main site-src gateway-api

echo "Done. Review 'git status docs/upstream', then commit."
