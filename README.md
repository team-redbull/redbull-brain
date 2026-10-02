# team-brain

The shared, versioned memory of the platform team: what we know about our Kubernetes/OpenShift
fleet, how we fix things, what broke and why, and the tools (skills + MCP servers) Claude Code uses
to work on our clusters.

Claude Code both **reads** from this repo (before troubleshooting) and **writes** to it (after it
learns something), through merge requests that a human approves.

## Layout

| Path | What lives there | Who writes |
|---|---|---|
| `knowledge/` | Curated team knowledge — how *our* clusters behave, quirks, decisions, gotchas | Humans + Claude (via MR) |
| `runbooks/` | Step-by-step procedures (node replacement, cert rotation, MCP rollout…) | Humans + Claude (via MR) |
| `incidents/YYYY/` | Postmortems, one file per incident | Humans + Claude (via MR) |
| `inbox/` | Raw learnings Claude captured, waiting to be curated into the folders above | Claude |
| `docs/upstream/` | Pinned mirrors of upstream docs (Kubernetes, OpenShift) for air-gapped lookup | `scripts/sync-upstream-docs.sh` |
| `mcp/` | `sources.json` (what team-knowledge searches) + docs for every MCP server the team uses | Humans |
| `plugins/team-brain/` | The Claude Code plugin: skills, hooks, and the **team-knowledge MCP server** | Humans |
| `deploy/openshift/` | Shared deployment: RHOKP + team-knowledge over HTTP for the whole team | Humans |
| `scripts/` | Validation, index generation, upstream doc sync | Humans |
| `INDEX.md` | Generated table of contents (do not edit by hand) | `scripts/brain.py index` |

## Offline knowledge: the team-knowledge MCP server

The plugin ships one zero-dependency MCP server that searches, in a single call:

- **the brain** itself — our quirks, runbooks, postmortems
- **Red Hat Offline Knowledge Portal** — OCP/ACM/MCE/RHEL docs, KCS solutions, CVEs, errata
- **Argo CD docs** from your internal mirror
- **HyperShift** and **Cluster API** — docs *and source code*, at the exact branch/tag a cluster runs
- **Kubernetes docs** pinned to 1.35 (newest OCP in the fleet) in `docs/upstream/`; version map in `knowledge/meta/fleet-versions.md`
- **Ecosystem docs** (AKO, Envoy, KServe, vLLM, LWS, Prometheus, Grafana, Metal3, GPU operator…) as docs-only snapshots in `docs/upstream/` (HyperShift and Ironic are full code+docs mirrors); Portworx as a crawl — catalog in `knowledge/meta/doc-sources-catalog.md`
- **Grafana MCP** — metrics from our single Grafana (one Prometheus datasource per cluster)

Details, RHOKP setup and the shared-deployment option: [`mcp/README.md`](mcp/README.md).

## How the learning loop works

```
 work session in any repo / cluster
        │
        ├─ SessionStart hook ── pulls the brain, tells Claude where it is + what's in it
        │
        ├─ Claude hits a problem ──► /team-brain:brain-lookup  (search knowledge, incidents, upstream docs)
        │
        ├─ Claude learns something non-obvious ──► /team-brain:brain-learn
        │        writes inbox/ or knowledge/ on a learn/* branch ──► push ──► GitLab MR
        │
        └─ Stop hook ── after a long session with no capture, asks Claude once:
                         "did this session produce durable knowledge?"

 human reviews MR ──► merge ──► everyone's next session pulls it
 periodically: /team-brain:brain-curate  (promote inbox → knowledge, dedupe, mark stale)
```

Nothing lands on `main` without a human approving the MR. Claude never pushes to `main`.

## Setup (once per engineer)

```bash
# 1. Clone the brain to the standard location (the hooks look here)
git clone git@gitlab.internal:platform/team-brain.git ~/team-brain
#    or anywhere else, and export TEAM_BRAIN_DIR=/path/to/team-brain in your shell profile

# 2. Register the repo as a plugin marketplace and install the plugin (user scope = all projects)
claude plugin marketplace add ~/team-brain
claude plugin install team-brain@team-brain

# 3. Point the MCP server at your internal endpoints (shell profile), then fetch mirrors
export GIT_MIRROR_BASE=https://gitlab.internal/mirrors
export RHOKP_SOLR_URL=http://rhokp.internal:8983  RHOKP_URL=https://rhokp.internal
export ARGOCD_DOCS_URL=https://docs-mirror.internal/argo-cd/stable
python3 ~/team-brain/plugins/team-brain/mcp-servers/team-knowledge/server.py --sync --warm --check

# 4. Check
claude plugin list          # team-brain@team-brain  ✔ enabled
# inside claude: /mcp  → plugin:team-brain:team-knowledge connected
```

Requirements on the workstation: `git`, `jq`, `python3` (≥3.9, stdlib only), and optionally
`glab` for opening merge requests automatically. Without `glab`, Claude pushes the branch and
prints the MR link.

To push the plugin to the whole team without each person running step 2, add the marketplace and
plugin to managed settings (see `docs/ADMIN.md`).

## Writing rules (for humans and Claude alike)

1. **Every file has frontmatter** — see `docs/FRONTMATTER.md`. CI rejects files without it.
2. **No secrets, ever.** No tokens, pull secrets, kubeconfigs, BMC passwords, internal IPs of
   management networks. CI scans for them. Use `<REDACTED>` or a placeholder.
3. **State the scope.** OCP/K8s version, hardware, cluster type (hosted / standalone / SNO).
   A fix for 4.16 on Dell XE9680 is not a fix for everything.
4. **Say how you know.** `verified` (tested on a cluster), `observed` (seen once), `hypothesis`.
5. **Prefer editing an existing page over adding a new one.** Search first.

## Daily commands

```bash
python3 scripts/brain.py validate      # frontmatter + secret scan + links
python3 scripts/brain.py index         # regenerate INDEX.md
python3 scripts/brain.py stale --days 180   # pages whose last_verified is old
scripts/sync-upstream-docs.sh          # refresh pinned upstream docs (connected host only)
```
