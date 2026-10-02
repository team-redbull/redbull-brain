---
title: Where to look — multi-node LLM inference, InfiniBand/RDMA, NCCL and kernel tuning questions
type: knowledge
area: gpu
tags: [vllm, llm-d, lws, nccl, rdma, infiniband, roce, sriov, tuning, hugepages, numa, doc-map]
applies_to: [ocp-4.16, ocp-4.20, ocp-4.22]
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# Inference / HPC / fabric / kernel-tuning: which source answers what

A routing table for `team-knowledge` `search` (use the `sources` argument to focus). All are **docs-only snapshots**
of the default branch (no code at a ref) — check against the versions actually installed (see
`knowledge/meta/fleet-versions.md`; add-on versions such as vLLM image, GPU Operator and Network Operator come from the cluster).
Snapshots do not replace RHOKP: where Red Hat documents a supported OpenShift procedure (Node Tuning Operator,
PerformanceProfile, GPU Operator on OCP), RHOKP wins.

| Question | Start in sources | Then |
|---|---|---|
| vLLM flags, parallelism (tensor/pipeline/expert), quantization, serving config | `vllm` | `lws` (multi-node deployment), `kserve`/`kserve-website` (serving runtime) |
| Multi-node inference on Kubernetes (LeaderWorkerSet), queueing/quotas | `lws`, `kueue` | `vllm` multi-node pages |
| Prefill/decode disaggregation, wide expert parallelism, cache-aware routing | `llm-d` | `dynamo`, `sglang`, `tensorrt-llm` (alternative stacks), `ray-docs` (KubeRay / Ray Serve) |
| NCCL hangs, slow collectives, env vars (`NCCL_*`), topology | `nccl` | `rdma-core`, `ucx`, `nvidia-network-operator-docs` |
| InfiniBand/RoCE/RDMA in pods: device plugin, MOFED, secondary networks | `nvidia-network-operator-docs`, `sriov-network-operator` | `multus-cni`, `rdma-core`, `linux-kernel-docs` (infiniband) |
| GPU Operator, MIG, DCGM/telemetry on OpenShift | `nvidia-cloud-native-docs` | RHOKP (OCP-specific install), `gpu-operator` |
| Hugepages, NUMA, CPU topology, IRQ affinity, scheduler, sysctl | `linux-kernel-docs`, `tuned` | RHOKP: Node Tuning Operator, PerformanceProfile, Topology/CPU Manager |
| Alert fired on a node/cluster | `openshift-runbooks` | `prometheus-docs` + Grafana MCP (`Moby / <cluster>` datasource) |

## Caveats

- `linux-kernel-docs` is upstream `master`; the RHCOS kernel on our nodes is older and patched — confirm a sysctl or
  parameter exists on the node (`oc debug node/<node>`) before recommending it.
- NVIDIA's XID error catalogue and docs.portworx.com/docs.nvidia.com pages beyond the mirrored repos are **not** here.
- No skills or MCP servers for these topics exist in the official marketplaces; community ones are tiny and unreviewed
  (see the scan notes in the MR/commit history) — none are installed.

## History

- 2026-10-03: created with the first inference/HPC/fabric/kernel doc snapshots.
