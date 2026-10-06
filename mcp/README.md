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
| `hypershift`, `ironic` | **full git mirrors** | code + docs at any ref |
| `ako`, `envoy`, `envoy-gateway`, `gateway-api`, `kserve`, `kserve-website`, `vllm`, `lmcache`, `mooncake`, `lws`, `kueue`, `prometheus-docs`, `prometheus-operator`, `grafana-docs`, `mcp-grafana`, `openshift-runbooks`, `etcd-docs`, `portworx-docs`, `metal3-docs`, `baremetal-operator`, `cluster-api-provider-metal3`, `gpu-operator`, `node-feature-discovery`, `ovn-kubernetes`, `multus-cni`, `assisted-service`, `llm-d`, `sglang`, `tensorrt-llm`, `dynamo`, `ray-docs`, `nccl`, `ucx`, `rdma-core`, `nvidia-cloud-native-docs`, `nvidia-network-operator-docs`, `sriov-network-operator`, `tuned`, `linux-kernel-docs` | **docs-only snapshots** in `docs/upstream/<name>` | documentation only, no code, no git history |
| `cluster-api-provider-agent` | git mirror | enabled |
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

Red Hat also publishes its own RHOKP MCP server, `okp-mcp` (Apache-2.0). It is Python with third-party
dependencies, so it cannot ship as a binary in the plugin: it runs from its container image. It is optional —
`mcp/servers/okp-mcp.md` compares the two and `deploy/openshift/okp-mcp.yaml` deploys it next to RHOKP.
team-knowledge stays the cross-source entry point.

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

## Full mirrors vs docs-only snapshots

- **Full git mirrors** (`git clone --mirror`: every branch, tag and all history; code *and* docs searchable at any `ref`):
  `hypershift`, `ironic`, plus `cluster-api`, `cluster-api-provider-agent` and (optional) `argo-cd`.
  Create these under `$GIT_MIRROR_BASE` with the same `org/repo` path as upstream
  (`openshift/hypershift`, `openstack/ironic`, `kubernetes-sigs/cluster-api`, `openshift/cluster-api-provider-agent`,
  `argoproj/argo-cd`), then `server.py --sync`.
- **Docs-only snapshots** (everything else): `python3 scripts/sync-ecosystem-docs.py [name…]` fetches just the
  documentation folders (shallow, sparse) into `docs/upstream/<name>`; Kubernetes and Portworx have their own
  scripts. Commit the result. In the air gap set `UPSTREAM_GIT_BASE` to an internal mirror. Snapshots follow the
  default branch; pin one to the installed version with `REF_<name>=<tag>` (e.g. `REF_vllm=v0.11.0`).
  Snapshots cannot be queried "at ref" — treat them as latest-docs and verify against the installed version.

Repo names, default branches and doc paths were checked against GitHub on 2026-10-03. Upstream layouts drift
(Gateway API moved `site-src` → `site/content`): rerun the script and fix paths that yield zero files.

**Portworx has no public docs repo** (`portworx/px-docs` is an archived 2018 snapshot); `portworx-docs` is a crawl of
docs.portworx.com (latest release, 3.7 at last sync) via `python3 scripts/sync-portworx-docs.py`
(on macOS Python: `SSL_CERT_FILE=/etc/ssl/cert.pem`).

## Grafana MCP (metrics)

Separate stdio server (`mcp-grafana`), registered in `plugins/team-brain/.mcp.json`. Setup and the
one-datasource-per-cluster rules: `mcp/servers/grafana.md`.

## Kubernetes MCP (cluster access)

`kubernetes-mcp-server`, registered as `kubernetes`. It uses the kubeconfig of the shell that started Claude with
full rights (write, exec, Secrets); each call is approved in the permission prompt. Rules (pass `context` on every
call) and how to restrict a machine: `mcp/servers/kubernetes.md`.

## Third-party MCP servers ship inside the plugin

The air gap has no GitHub, so a server we depend on is committed as its release archives:

```
plugins/team-brain/mcp-servers/
  launch.py                 # picks the archive for this OS/CPU, checks sha256, unpacks once, runs it
  vendor/manifest.json      # server -> version, binary name, archive + sha256 per platform
  vendor/grafana/*.tar.gz|zip
  vendor/kubernetes/*.mcpb  # MCP bundle = zip with the binary inside
  kubernetes.toml           # full access; kubeconfig viewer disabled; how to restrict a machine
```

- Engineers do nothing: installing/updating the plugin brings the binary. `python3 launch.py --check` shows
  what would run; `TEAM_BRAIN_MCP_<SERVER>_BIN` overrides it.
- Add or bump a server (connected host): edit `SERVERS` in `scripts/fetch-mcp-binaries.py`, run it (archives
  are verified against the release checksums file), register it in `.mcp.json` as
  `python3 ${CLAUDE_PLUGIN_ROOT}/mcp-servers/launch.py <server> <flags>`, add `mcp/servers/<name>.md`, bump
  the plugin version. Each platform is ~17–25 MB per version in git history, so bump deliberately.
- Before vendoring anything, run it once and read its startup log: `mcp-grafana` v2 reports usage statistics
  to its vendor unless told not to.

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
