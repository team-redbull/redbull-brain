---
title: Querying metrics — one Grafana, one Prometheus datasource per cluster named "Moby / <cluster-name>"
type: knowledge
area: observability
tags: [grafana, prometheus, mcp, datasource, multi-cluster]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# One Grafana, one Prometheus datasource per cluster

## Layout

- Every cluster has its **own** Prometheus. There is **one** Grafana for the whole fleet.
- Grafana has one Prometheus datasource per cluster, named **`Moby / <cluster-name>`**
  (e.g. `Moby / site2-gpu-03`).
- A query only ever sees one cluster — the one behind the datasource it is sent to.

## Rules for Claude (Grafana MCP, see `mcp/servers/grafana.md`)

1. **Resolve the datasource first.** Call `list_datasources` with `name: "<cluster-name>"` (substring match)
   and take the `uid` of `Moby / <cluster-name>`. Don't list everything: a page is 50 datasources (max 100) and
   the fleet has more, so an unfiltered list silently misses clusters. If the name is ambiguous or missing,
   stop and ask — never guess a UID.
2. **Pass the datasource UID on every Prometheus query.** Never rely on the default datasource; it is an
   arbitrary cluster.
3. **Say which cluster each number comes from** in your answer.
4. **Fleet-wide questions = one query per datasource.** List the `Moby / *` datasources (`name: "Moby"`,
   page with `offset` until a page comes back short), run the same query
   against each, and report which clusters answered and which failed or timed out. Don't extrapolate.
5. **Set an explicit time range and step.** Prefer instant queries or short ranges first; large ranges across
   many datasources are slow.
6. **Metrics are evidence, not a diagnosis.** Pair them with `oc` output and brain pages; recording rules and
   alert names differ between OCP minors, so check the cluster's version (`knowledge/meta/fleet-versions.md`)
   and the alert's runbook (`openshift-runbooks` source) before drawing conclusions.
7. Never put the Grafana URL, token or dashboard links with embedded tokens into brain pages.

## Not yet verified

- Authentication assumption: a read-only Grafana service account (Viewer) via `GRAFANA_SERVICE_ACCOUNT_TOKEN`.
- Nothing here has been run against our real Grafana yet. Tool names and arguments are taken from the vendored
  `mcp-grafana` v2.0.0 binary (`mcp/servers/grafana.md`).

## History

- 2026-10-03: created from the platform team's description of the Grafana layout.
- 2026-10-03: datasource lookup by `name` filter and paging limits, from the v2.0.0 tool schema.
