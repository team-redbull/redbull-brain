# docs/upstream

Pinned, unmodified mirrors of upstream documentation for offline search. Regenerate with
`scripts/sync-upstream-docs.sh` (Kubernetes), `scripts/sync-ecosystem-docs.py` (ecosystem projects) and
`scripts/sync-portworx-docs.py` (Portworx); never edit by hand. Each subfolder has a `.upstream` file with the
repo, ref and commit it came from.

- `kubernetes/` — kubernetes/website `content/en/docs` (CC BY 4.0, © The Kubernetes Authors)
- `portworx/` — crawl of docs.portworx.com (latest release)
- `ako/ envoy/ envoy-gateway/ kserve/ kserve-website/ vllm/ lws/ kueue/ gateway-api/ prometheus-*/ grafana-docs/ mcp-grafana/
  metal3-docs/ baremetal-operator/ cluster-api-provider-metal3/ gpu-operator/ node-feature-discovery/ ovn-kubernetes/
  multus-cni/ openshift-runbooks/ assisted-service/ etcd-docs/` — docs-only snapshots of each project (default branch
  unless pinned with `REF_<name>`); licences are the upstream projects' own

OpenShift / ACM / MCE product documentation is served by RHOKP (see `mcp/README.md`), not mirrored here.
