---
title: day2 GitOps — a folder is the registration, day1 owns the OCP version, and what silently breaks (phantom apps, missing version layers, orphaned workloads)
type: knowledge
area: gitops
tags: [argocd, applicationset, day2, sites-tree, mastertag, ocp-versions, upi, exclusions]
applies_to: [hosted-cp, ocp-4.16, ocp-4.20, ocp-4.22]
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: gitops-day2-prod/ARCHITECTURE.md
---

# day2 GitOps: how it works and how it bites

Condensed from `gitops-day2-prod` (`ARCHITECTURE.md` is the full guide; it is a searchable source
when `gitops-day2-prod` is enabled in `mcp/sources.json`). Topology: `knowledge/openshift/fleet-topology-hub-mce-hosted.md`.

## The model

> **Folders say WHERE things run. The day1 repo says WHICH VERSION runs there.**

- Team repo `sigs/<team>/sites/<site>/<env>/mces/<mce>/<cluster>/<chart>/{<chart>.yaml,values.yaml}`.
  `<env>` is `prod|prep|test`. Standalone clusters: `sites/<site>/<env>/upi/<cluster>/`.
- **A directory existing = registration.** No marker file. Discovery is `directories:` generators only
  (`*` never crosses `/`, so depth is enforced by the engine). Never use a `files:` generator for
  discovery: its glob is a git pathspec and `*` crosses `/` (caused a production incident).
- Chain (each renders the next): `groups` (prod-hub) → `mces` (prod-hub) → `clusters` (on the MCE's Argo)
  → `operators` → `deploy` → leaf app `<team>-<cluster>-<chart>-deploy` (the real workload).
- Config layers: `operators/<chart>/` (team default) → `operators/<chart>/ocp-versions/<v>/` →
  site/env/MCE/cluster values → `defaults/{hub,mces,hosted-clusters,upi}/<chart>/` → cluster folder.
  Most specific wins. Values and deploy config (`<chart>.yaml`: `repourl`, `targetRevision`, `path`,
  `projectNamespace`, `syncPolicy`) are separate stacks. Every slot uses `ignoreMissingValueFiles`.
- Version: `mastertag: 4.16.27-x86_64` in day1 → `ocpVersion 4.16.27` (**full patch version**, not minor).
  UPI clusters may carry their own `version.yaml` (`mastertag` only) or be version-less.
- Labels: `day2.gitops/{team,env,site,mce,cluster,chart,ocp-version,role}` →
  `argocd app sync -l day2.gitops/chart=<c>,day2.gitops/ocp-version=<full-version>`
  (`ocp-version=4.20` matches nothing; labels are per Argo instance).

## Things that fail silently

| Symptom | Cause | Fix |
|---|---|---|
| Cluster/MCE has no apps | git can't track empty dirs | add `.gitkeep` |
| Phantom Application whose destination "does not exist" | stray directory under `mces/` or an MCE folder (anything that isn't a cluster, except `in-cluster/`) | remove it; render check's day1-parity lint names it (not for `upi/`) |
| After a cluster upgrade a pinned chart falls back to team default | `ocp-versions/<new-full-version>/` didn't exist when day1 flipped `mastertag` — **applies to z-streams too**, in every sig that pins the chart | create the layer **before** the day1 MR merges; render-verify against the new tag |
| A `targetRevision` pin is ignored | defaults config (layer 3) outranks `ocp-versions/` (layer 2) | keep pins in `operators/`; defaults carry only `repourl`/`projectNamespace`/`syncPolicy` |
| Deploy config renders empty repoURL | key must be all-lowercase `repourl` | fix the key |
| Deleted folder, workload still running | no resources-finalizers: only the Application CR goes, workloads are orphaned | intentional; for teardown `argocd app delete <app>-deploy --cascade` **after** the wrapper is gone |
| Exclusion has no effect | typo in chart or cluster name in `defaults/<scope>/exclusions.yaml` is inert | CI lint catches it; run `render_chain.py snapshot` |
| Chart exists in defaults and in a cluster folder | XOR rule: duplicate app name, CI fails | name the cluster in `exclusions.yaml` for a deliberate full override |
| Charts keep deploying to a UPI cluster after its folder was deleted | `<team>-<cluster>-operators` ApplicationSet stays on the UPI Argo | delete it by hand (`APPLY-UPI.md` §8) |

## Rules to keep

- **One invariant:** at every commit each MCE/cluster/chart is emitted by exactly one generator entry →
  one `git mv`, never copy-then-delete.
- Never touch the template line `namespace: gitops-{{ .Values.repository }}` (renders `gitops-`, known and
  frozen: changing it deletes and recreates every app).
- Chart version branches are **frozen**; a fix is a new branch + new pin, never a push.
- Leaf apps are manual-sync (only `dhcp-api-token` auto-syncs); platform layers self-heal, so a bad render syncs at once.
- **Verify before merge:** `python3 tools/render-verify/render_chain.py snapshot --out /tmp/before` on main,
  apply change, snapshot again, `compare` → must end `IDENTITY OK`; `snapshot` exits 1 on lint failures.
- `example-chart` folders are demos; never ship them to prod.

## Runbook pointers (ARCHITECTURE.md Part III)

Upgrade hosted cluster = one-line day1 edit (R1); MCE = day1 `version.yaml` (R2, hand-maintained);
chart upgrade by pin (R3); add chart to one cluster / whole fleet (R4/R5); new hosted cluster needs
the Argo registration under the exact name **and** a day1 file (R6); decommission (R8); exclude (R10); UPI (R11).

## Scope & caveats

Describes the layout as of the 2026-10 repo state (single commit history in the mirrors we read). If the
tree layout changes, only `mcesAppset.yaml` and `upiAppset.yaml` encode it.

## History

- 2026-10-03: created from the day2 repo's ARCHITECTURE.md and READMEs.
