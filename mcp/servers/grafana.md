---
title: Grafana MCP server (mcp-grafana) — query per-cluster Prometheus through our single Grafana
type: mcp
area: observability
tags: [mcp, grafana, prometheus, metrics]
applies_to: []
confidence: hypothesis
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# Grafana MCP (`mcp-grafana`)

- **Upstream:** `grafana/mcp-grafana` (Go, Apache-2.0). Mirrored as a source (`mcp-grafana`) so Claude can read
  its README/code; the binary itself must be mirrored into the air gap separately.
- **Registered in:** `plugins/team-brain/.mcp.json` as `grafana` (stdio). Tool names in Claude Code:
  `mcp__plugin_team-brain_grafana__<tool>`.
- **Config (shell profile, never in git):**
  - `GRAFANA_URL` — our single Grafana
  - `GRAFANA_SERVICE_ACCOUNT_TOKEN` — read-only (Viewer) service account token
- **Binary:** put `mcp-grafana` on `PATH` (release binary from the internal mirror). Without
  `GRAFANA_URL` the server starts and fails on first call; engineers who don't need metrics can disable it
  with `/mcp`.

## Usage rules

Our layout is **one Prometheus datasource per cluster**, named `Moby / <cluster-name>`. Follow
`knowledge/observability/grafana-one-datasource-per-cluster-prometheus.md`: `list_datasources` first, always
pass the datasource UID, one query per cluster, say which cluster each result is from.

## Tools expected (verify against the deployed version)

| Tool | Use |
|---|---|
| `list_datasources` | find `Moby / <cluster>` and its UID |
| `query_prometheus` | PromQL against a datasource UID (instant or range) |
| `list_prometheus_metric_names`, `list_prometheus_label_values` | discover what a cluster exposes |
| `search_dashboards`, `get_dashboard_by_uid` | existing dashboards |
| alert rule tools | what is firing / configured |

Names and arguments change between releases; read the `mcp-grafana` source at the version we run before
relying on them, and fix this table. Confidence stays `hypothesis` until someone has run it end to end.

## History

- 2026-10-03: added; not yet exercised against our Grafana.
