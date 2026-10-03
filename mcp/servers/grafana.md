---
title: Grafana MCP server (mcp-grafana) — query per-cluster Prometheus through our single Grafana
type: mcp
area: observability
tags: [mcp, grafana, prometheus, metrics]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# Grafana MCP (`mcp-grafana`)

- **Upstream:** `grafana/mcp-grafana` (Go, Apache-2.0), pinned **v2.0.0**.
- **Installed with the plugin — nothing to download inside the air gap.** The release archives for
  linux-x86_64, darwin-arm64 and windows-x86_64 are committed in
  `plugins/team-brain/mcp-servers/vendor/grafana/` with their sha256 in `vendor/manifest.json`.
  `mcp-servers/launch.py grafana` checks the sha256, unpacks the binary for your OS/CPU once into the plugin
  cache and runs it. `python3 plugins/team-brain/mcp-servers/launch.py --check` shows what would run.
  Other platform: add it in `scripts/fetch-mcp-binaries.py` on a connected host, or point
  `TEAM_BRAIN_MCP_GRAFANA_BIN` at a binary you already have.
- **Registered in:** `plugins/team-brain/.mcp.json` as `grafana` (stdio). Tool names in Claude Code:
  `mcp__plugin_team-brain_grafana__<tool>`.
- **Config (shell profile, never in git):**
  - `GRAFANA_URL` — our single Grafana
  - `GRAFANA_SERVICE_ACCOUNT_TOKEN` — read-only (Viewer) service account token
  - Internal CA: Go reads the system trust store; otherwise export `SSL_CERT_FILE=<ca bundle>`.
- **How we start it (and why):**
  - `--disable-write` — no create/update tools; the token should be Viewer anyway.
  - `--usage-stats=disabled` + `GRAFANA_USAGE_STATS=disabled` — by default v2 reports anonymous usage
    statistics to Grafana Labs; that must never be attempted from our network.
  - `--enabled-tools=search,datasource,prometheus,loki,alerting,dashboard,folder,navigation` — drops incident,
    on-call, Tempo, Pyroscope, plugin install, raw API, provisioning, rendering and the `docs` tools (which look
    up grafana.com). Add a category here only when we actually run that backend.
- Without `GRAFANA_URL` the server starts and every call fails; engineers who don't need metrics can disable it
  with `/mcp`.

## Usage rules

Our layout is **one Prometheus datasource per cluster**, named `Moby / <cluster-name>`. Follow
`knowledge/observability/grafana-one-datasource-per-cluster-prometheus.md`: resolve the datasource first
(`list_datasources` with `name`), always pass `datasourceUid`, one query per cluster, say which cluster each
result is from.

## Tools (26, listed from the vendored v2.0.0 binary with our flags)

| Tool | Use |
|---|---|
| `list_datasources` (`name`, `type`, `limit` ≤ 100, `offset`) | find `Moby / <cluster>` and its UID. Default page is 50 and the fleet has more datasources than that — filter by `name` instead of paging |
| `get_datasource`, `check_datasources_health` | details / is the cluster's Prometheus reachable from Grafana |
| `query_prometheus` (`datasourceUid`, `expr`, `endTime` required; `queryType` instant\|range, `startTime`, `stepSeconds`) | PromQL against one cluster |
| `query_prometheus_histogram` | histogram quantiles |
| `list_prometheus_metric_names`, `list_prometheus_metric_metadata`, `list_prometheus_label_names`, `list_prometheus_label_values` | discover what a cluster exposes (all take `datasourceUid`) |
| `alerting_rules_read`, `alerting_silences_read`, `alerting_manage_routing` | alert rules and state (`datasource_uid` for a cluster's own rules), silences, routing |
| `search_dashboards`, `search_folders`, `get_dashboard_summary`, `get_dashboard_by_uid`, `get_dashboard_property`, `get_dashboard_panel_queries`, `list_dashboard_versions` | existing dashboards and the queries behind their panels |
| `generate_deeplink` | a Grafana link to hand to a human |
| `query_loki_logs`, `query_loki_stats`, `query_loki_patterns`, `list_loki_label_names`, `list_loki_label_values`, `analyze_loki_labels` | only useful if a Loki datasource exists |

Tool names and arguments change between releases (v2 renamed the alerting tools): after bumping the version,
re-list the tools and fix this table.

## What is verified

- Verified on 2026-10-03 on a connected macOS arm64 machine: archives match the release checksums, the launcher
  unpacks and starts the binary, the tool list above, no usage-statistics attempt with our flags.
- **Not verified:** any call against our real Grafana (auth, datasource names, CA), and the linux/windows
  binaries have only been checksum-verified, not run.

## Updating

Connected host: `VERSION_grafana=<tag> python3 scripts/fetch-mcp-binaries.py grafana`, update the pin in that
script, bump the plugin version, re-list the tools, commit.

## History

- 2026-10-03: added; not yet exercised against our Grafana.
- 2026-10-03: binary vendored in the plugin (v2.0.0), read-only flags, usage statistics disabled, tool table
  taken from the binary.
