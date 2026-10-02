---
title: Offline doc sources catalog — what each team-knowledge source is authoritative for and which ref to use
type: knowledge
area: meta
tags: [sources, team-knowledge, refs, catalog]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# Offline doc sources catalog

Config: `mcp/sources.json` (per engineer) and `deploy/openshift/shared-sources.json` (shared server).
Version → ref rules: `knowledge/meta/fleet-versions.md`. **When Red Hat's downstream docs (RHOKP) and an
upstream source disagree, RHOKP/KCS wins for what we run**; upstream tells you how it works internally.

| Source | Area | Good for | Ref to use |
|---|---|---|---|
| `rhokp` | all | OCP/ACM/MCE docs, KCS, CVEs, errata | filter `version: "4.NN"` |
| `hypershift`, `cluster-api` | hypershift | HostedCluster/NodePool/CAPI behaviour and code | `release-4.NN` / CAPI tag from go.mod |
| `cluster-api-provider-agent`, `cluster-api-provider-metal3`, `baremetal-operator`, `metal3-docs`, `ironic` | baremetal | Agent/Metal3 machines, BareMetalHost states, BMC drivers | tag matching OCP's baremetal components; `main` for concepts |
| `assisted-service` | baremetal | Agent-based installs, InfraEnv/Agent CRs | `release-ocm-*` / tag of the installed MCE |
| `ako` | networking | our L4/L7 load balancing and ingress (**not MetalLB** — see `knowledge/networking/ingress-load-balancing-is-ako-not-metallb.md`) | tag = AKO version installed on the cluster |
| `envoy`, `envoy-gateway`, `gateway-api` | networking | proxy config, Gateway API semantics, CRD fields | Envoy `release/v1.NN` as used by the product; Gateway API tag = installed CRD bundle |
| `ovn-kubernetes`, `multus-cni` | networking | default CNI behaviour, secondary networks | match OCP minor where a release branch exists |
| `kserve`, `kserve-website` | gpu / ai | InferenceService/ServingRuntime APIs. RHOAI ships its own build — verify against RHOKP | tag of KServe in the installed RHOAI/ODH |
| `vllm` | gpu / ai | serving flags, quantization, parallelism, engine code | tag = vLLM version in the serving image |
| `lws`, `kueue` | gpu / ai | multi-node inference (LeaderWorkerSet), quotas/queueing | tag = installed operator version |
| `gpu-operator`, `node-feature-discovery` | gpu | ClusterPolicy, drivers, MIG, NFD labels | tag = installed operator version |
| `prometheus-docs`, `prometheus-operator` | observability | PromQL, alerting, ServiceMonitor/PrometheusRule | OCP bundles its own build; docs are general |
| `openshift-runbooks` | observability | per-alert runbooks (check first when an alert fires) | `master` (runbooks are not versioned per minor) |
| `grafana-docs`, `mcp-grafana` | observability | dashboards, datasources, provisioning; MCP tool names and flags | tag = Grafana / mcp-grafana version we run |
| `portworx-docs` | storage | Portworx install, upgrades, storage classes, DR | branch/tag = installed Portworx version |
| `etcd-docs` | openshift | etcd defrag, backup/restore, tuning (OCP wraps etcd with its own operator) | general |
| `kubernetes-docs` | kubernetes | Kubernetes concepts and APIs | pinned 1.35 only (see fleet-versions) |
| `argocd-docs`, `argo-cd` | gitops | Argo CD docs / source | `stable` docs; tag of installed Argo CD for source |
| `brain` | all | **our** quirks, runbooks, incidents — read first | — |

## Gotchas when mixing sources

- Upstream default branches are ahead of what we run. Say which ref your claim comes from.
- Operators on OCP (monitoring, ingress, CNI) are managed by CVO — upstream flags often can't be set directly.
  Check RHOKP for the supported way before suggesting a change.
- Source repo names and doc paths in `sources.json` were written without network access; if a source returns
  nothing, check `list_sources` doc counts and fix the globs, then record the fix here.

## History

- 2026-10-03: created with the initial source set.
