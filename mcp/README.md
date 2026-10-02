# MCP servers

## team-knowledge (built in, zero dependencies)

One MCP server that gives Claude offline, version-aware search over everything the team relies on:

| Source | Kind | What Claude gets |
|---|---|---|
| `brain` | this repo | our knowledge, runbooks, incidents, inbox |
| `rhokp` | Red Hat Offline Knowledge Portal (Solr) | OCP / ACM / MCE / RHEL docs, **KCS solutions**, CVEs, errata |
| `argocd-docs` | your mirrored Argo CD docs site (MkDocs) | Argo CD docs |
| `hypershift` | git mirror of openshift/hypershift | docs + API types + controller code **at any branch/tag** |
| `cluster-api` | git mirror of kubernetes-sigs/cluster-api | the CAPI book, proposals + code at any tag |
| `kubernetes-docs` | `docs/upstream/kubernetes` (pinned 1.35, newest fleet version) | upstream Kubernetes docs |
| `ako`, `envoy`, `envoy-gateway`, `gateway-api`, `kserve`, `kserve-website`, `vllm`, `lws`, `kueue` | git mirrors | load balancing, proxy, model serving, inference workloads |
| `prometheus-docs`, `prometheus-operator`, `grafana-docs`, `openshift-runbooks`, `etcd-docs` | git mirrors | monitoring docs, alert runbooks |
| `portworx-docs`, `metal3-docs`, `ironic`, `gpu-operator`, `node-feature-discovery`, `ovn-kubernetes`, `multus-cni`, `assisted-service` | git mirrors | storage, bare metal, GPU, networking, Agent installs |
| `cluster-api-provider-agent`, `cluster-api-provider-metal3`, `baremetal-operator` | git mirrors | now enabled |
| *(disabled)* `argo-cd` | git mirror | flip `"enabled": true` |

Tools: `list_sources`, `search`, `read`, `search_code`, `read_code`, `find_definition`, `list_refs`.

Why one server instead of five: one install, one config, one place to fix TLS/proxy problems,
and a single `search` that ranks results across all sources so Claude checks *our* notes and
Red Hat's KCS in the same call.

Code: `plugins/team-brain/mcp-servers/team-knowledge/` — Python ≥ 3.9 stdlib + `git`. Nothing to
`pip install`, so nothing to mirror. Config: `mcp/sources.json` (this folder).

### Two ways to run it

**A. Per engineer (stdio, default).** The plugin starts it automatically. Each laptop keeps its own
git mirrors and indexes under `~/.cache/team-brain/`.

```bash
export GIT_MIRROR_BASE=https://gitlab.internal/mirrors        # where your mirrors live
export RHOKP_SOLR_URL=http://rhokp.internal:8983              # or a local podman RHOKP
export RHOKP_URL=https://rhokp.internal                        # web UI, for links
export ARGOCD_DOCS_URL=https://docs-mirror.internal/argo-cd/stable
SRV=~/team-brain/plugins/team-brain/mcp-servers/team-knowledge/server.py
python3 $SRV --sync     # clone/fetch hypershift, cluster-api, …   (first run: a few minutes)
python3 $SRV --warm     # build indexes (otherwise built on first query)
python3 $SRV --check    # what's reachable
python3 $SRV --call search '{"query": "NodePool stuck Updating", "version": "4.20"}'
```

**B. Shared for the team (streamable HTTP on OpenShift)** — recommended once more than a few
people use it: one RHOKP, one set of mirrors, indexes rebuilt every 6 h.

```bash
oc apply -k deploy/openshift          # after creating the 3 secrets listed in kustomization.yaml
```

Then each engineer points Claude Code at it instead of the local server — put this in
`~/.claude.json` / a project `.mcp.json` (see `mcp/clients/http.mcp.json`) and set
`TEAM_KNOWLEDGE_TOKEN` in their shell:

```json
{ "mcpServers": { "team-knowledge": {
    "type": "http",
    "url": "https://team-knowledge-team-knowledge.apps.mgmt.internal/mcp",
    "headers": { "Authorization": "Bearer ${TEAM_KNOWLEDGE_TOKEN}" } } } }
```

and disables the plugin's local copy with `claude mcp` / `/mcp` (or keep both: different names).

## RHOKP setup

1. On a connected host: `podman login registry.redhat.io`, pull
   `registry.redhat.io/offline-knowledge-portal/rhokp-rhel9:latest`, push it to the internal
   registry (or `skopeo copy` → `oc-mirror`/disk transfer). Red Hat refreshes content roughly weekly;
   re-mirror on a schedule.
2. Get an access key from the Red Hat Customer Portal RHOKP page; store it as a secret, never in git.
3. Run it:
   - laptop: `podman run -d --name rhokp -p 8080:8080 -p 8983:8983 -e ACCESS_KEY=… -e SOLR_JETTY_HOST=0.0.0.0 <image>`
   - cluster: `deploy/openshift/rhokp.yaml` (Solr port stays cluster-internal behind a NetworkPolicy)
4. Check: `curl "$RHOKP_SOLR_URL/solr/portal/select?q=*:*&rows=0"` → `numFound` > 0.

`search` accepts `product`, `version` and `doc_kind` filters for RHOKP, e.g.
`{"query": "etcd defrag", "product": "Red Hat OpenShift Container Platform", "version": "4.20", "doc_kind": "Solution"}`.

Red Hat also publishes its own RHOKP MCP server (`okp-mcp`, Apache-2.0, Python 3.12 + `uv`). It does
more RHEL-specific query shaping. If you mirror its image you can run it alongside and add it to
`plugins/team-brain/.mcp.json`; team-knowledge stays the cross-source entry point.

## Argo CD docs mirror

`mkdocs_site` reads the site's `search/search_index.json`, which every MkDocs build (including
argo-cd.readthedocs.io) publishes. If your mirror is a git checkout of `argoproj/argo-cd` instead
of a built site, enable the `argo-cd` git source (its `docs/**/*.md` get indexed) or use a
`markdown_dir` source pointed at the checkout's `docs/`.

The same `mkdocs_site` kind works for any other MkDocs mirror you have (HyperShift's published
docs, Metal3, Tekton…) — add an entry, no code change.

## HyperShift / CAPI: pick the right ref

The code at `main` is not what your clusters run. Have Claude call `list_refs` and use the branch
matching the hub: HyperShift `release-4.NN` for the OCP/MCE stream; Cluster API tags `v1.x.y`
(check the CAPI version vendored in that HyperShift branch with
`search_code repo=hypershift path="go.mod" pattern="sigs.k8s.io/cluster-api "`).

## Mirrors to create before `--sync`

Every `git_repo` source needs a mirror under `$GIT_MIRROR_BASE` with the same `org/repo` path as
upstream. Sources whose mirror is missing just report "clone failed" — they don't break the others.
Disk is the main cost: `grafana/grafana`, `envoyproxy/envoy`, `vllm-project/vllm` and `openstack/ironic`
are large (full `--mirror` clones); drop their `docs`-only value if space matters.

```
openshift/hypershift  openshift/cluster-api-provider-agent  openshift/runbooks  openshift/assisted-service
kubernetes-sigs/cluster-api  kubernetes-sigs/lws  kubernetes-sigs/kueue  kubernetes-sigs/gateway-api
kubernetes-sigs/node-feature-discovery  vmware/load-balancer-and-ingress-services-for-kubernetes
envoyproxy/envoy  envoyproxy/gateway  kserve/kserve  kserve/website  vllm-project/vllm
prometheus/docs  prometheus-operator/prometheus-operator  grafana/grafana  grafana/mcp-grafana
portworx/pxdocs  metal3-io/metal3-docs  metal3-io/baremetal-operator  metal3-io/cluster-api-provider-metal3
openstack/ironic  NVIDIA/gpu-operator  ovn-org/ovn-kubernetes  k8snetworkplumbingwg/multus-cni  etcd-io/website
argoproj/argo-cd (optional)
```

Repo names and doc paths were written without network access — run `server.py --sync --check` and
fix any `docs` globs that match nothing (`list_sources` shows doc counts).

Pick the ref per cluster from `knowledge/meta/fleet-versions.md`; never rely on `main` for a cluster.

## Grafana MCP (metrics)

Separate stdio server (`mcp-grafana`), registered in `plugins/team-brain/.mcp.json`. Setup and the
one-datasource-per-cluster rules: `mcp/servers/grafana.md`.

## Adding a source

Append an object to `mcp/sources.json`:

| kind | required | optional |
|---|---|---|
| `markdown_dir` | `root` | `include`, `exclude`, `base_url` |
| `git_repo` | `path` | `remote`, `default_ref`, `docs`, `code_include`, `code_exclude`, `web_url` |
| `mkdocs_site` | `url` | `index_url`, `refresh_hours`, `ca_file`, `insecure_skip_verify` |
| `rhokp_solr` | `url` | `core`, `portal_url`, `default_product`, `ca_file`, `bearer_token` |

All string values support `${VAR}` / `${VAR:-default}`. HTTP sources ignore `HTTP(S)_PROXY` unless
`"use_env_proxy": true`, so internal lookups never leak to a proxy by accident.

Document every server the team uses in `mcp/servers/<name>.md`.
