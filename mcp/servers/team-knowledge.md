---
title: team-knowledge MCP server — offline search over brain, RHOKP, Argo CD docs, HyperShift, CAPI, K8s docs
type: mcp
area: meta
tags: [mcp, rhokp, argocd, hypershift, cluster-api, search]
applies_to: []
confidence: verified
last_verified: 2026-10-03
owners: [platform-team]
---

# team-knowledge

- **Code:** `plugins/team-brain/mcp-servers/team-knowledge/` (Python stdlib + git)
- **Config:** `mcp/sources.json` (per engineer) · `deploy/openshift/shared-sources.json` (shared)
- **Transport:** stdio (plugin default) or streamable HTTP at `/mcp` with bearer token
- **Tool names in Claude Code:** `mcp__plugin_team-brain_team-knowledge__<tool>` when started by
  the plugin; `mcp__team-knowledge-shared__<tool>` for the shared HTTP deployment.

| Tool | Use it for |
|---|---|
| `search` | first stop: one query across every source; RHOKP filters `product`, `version`, `doc_kind` |
| `read` | full text of a hit (paged with `offset`) |
| `list_refs` | pick the HyperShift/CAPI branch or tag matching the cluster |
| `search_code` | `git grep` at a ref — where is this error/condition produced? |
| `find_definition` | Go type/func/field or CRD kind → definition block |
| `read_code` | a file or line range at a ref |
| `list_sources` | what's configured and reachable |

## Operating notes

- First query on a new ref builds that ref's doc index (seconds for HyperShift/CAPI docs).
- Indexes live in `$TEAM_KNOWLEDGE_CACHE` (default `~/.cache/team-brain/team-knowledge`); delete
  to force a rebuild.
- `server.py --check` diagnoses unreachable sources (TLS, wrong URL, missing clone).
