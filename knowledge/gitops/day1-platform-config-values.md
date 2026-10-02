---
title: day1 platform-config — per-cluster values files, merge order, mastertag, DHCP values and segment allocation
type: knowledge
area: gitops
tags: [day1, platform-config, hostedcluster, mastertag, dhcp, segments, values-merge]
applies_to: [hosted-cp, ocp-4.16, ocp-4.20, ocp-4.22]
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: gitops-day1/platform-config README and workflow
---

# day1 `platform-config` (HostedCluster values)

The values repo for hosted-cluster provisioning (air-gapped GitLab project `gitops-day1/platform-config`;
a GitHub mirror exists). Argo CD never renders anything from it directly — it is only a `ref: values`
source. The charts live elsewhere: `gitops-day1-argocd-platform` (ApplicationSet cascade) and
`helm-charts-hostedclusters-setup` (what a hosted cluster gets). It also owns the cluster OCP versions
that day2 reads — see `knowledge/gitops/day2-sites-tree-discovery-and-version-layers.md`.

## Layout and merge order

```
sites/configValues.yaml                       # global, every cluster
sites/<site>/values.yaml                      # site-wide
sites/<site>/mces/<mce>/values.yaml           # MCE-wide (its `mastertag` = default for hosted clusters under it)
sites/<site>/mces/<mce>/version.yaml          # the MCE hub's own version: `mastertag` only (hand-maintained)
sites/<site>/mces/<mce>/hostedClusters/<cluster>.yaml   # one file per hosted cluster
```

Last value wins, layered over the chart's own `values.yaml`. No `<env>` level here (env is only in the name).

- **Lists are replaced, not appended** (a site `dns.servers` discards the global one; use `dns.extraServers`).
- **Mappings deep-merge** (a cluster's `failover` block only needs the fields that differ).
- `mastertag: <major>.<minor>.<patch>-<arch>` in the cluster file is the cluster's OCP version.
  Upgrading a cluster = one-line edit here, **after** the day2 `ocp-versions/<new>/` layers exist (day2 footgun).

## `dhcp_values` and day2 registration

- `dhcp_values` is the only key this repo owns (`dhcp_api`, `crossplane` are chart-owned). A cluster file with no
  `dhcp_values` block renders no DHCP scope. Field reference and CI validator live in `dhcp_scope_manager`
  (`scripts/validate_dhcp_values.py --sites-dir <repo>/sites`).
- `day2.copy_to_sigs: [<team>, …]` — each name makes the hostedclusters-setup Job create the cluster's folder in that
  sig's day2 repo (which is what registers it for day2). Empty list = nothing registered. Lists replace per layer.

## Segment allocation flow (push → values)

1. Push a branch (not `main`) adding/changing `sites/*/mces/*/hostedClusters/*.yaml`.
2. CI runs `scripts/allocate_segment.py` → POSTs `allocate-segment {cluster, values_branch}` to the workflows
   orchestrator API (secret URL; the API has no auth, so never print it).
3. The workflow appends `vlanId` + a `dhcp_values` block **on that branch** (CI-skip commit), the script waits and pulls it.
4. **Merging to `main` is what creates the DHCP scope** — Argo CD reads `main` only.
   The real pipeline is GitLab CI (`generate_mc_files`); the GitHub workflow copy only exercises the allocation step.

## Adding a cluster

Drop `<cluster>.yaml` under the right MCE. Also register the cluster in the MCE's Argo under the exact same name and
make sure the day2 folder exists (via `copy_to_sigs` or by hand).

## History

- 2026-10-03: created from the repo README, `configValues.yaml` comments and the allocate-segment workflow.
