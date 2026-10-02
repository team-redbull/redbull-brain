---
title: Frontmatter schema
type: reference
area: meta
tags: [meta, schema]
applies_to: []
confidence: verified
last_verified: 2026-10-03
owners: [platform-team]
---

# Frontmatter schema

Every Markdown file under `knowledge/`, `runbooks/`, `incidents/`, `inbox/`, `mcp/servers/`
starts with a YAML block. `scripts/brain.py validate` enforces it.

```yaml
---
title: HyperShift NodePool stuck in "Updating" after CAPI pre-drain hook timeout
type: knowledge            # knowledge | runbook | incident | inbox | mcp | reference
area: hypershift           # see CLAUDE.md for the list
tags: [nodepool, capi, drain]
applies_to: [ocp-4.16, ocp-4.17, mce-2.7]   # versions / hardware / cluster types; [] = general
confidence: observed       # verified | observed | hypothesis
last_verified: 2026-10-03  # date someone last confirmed this is still true
owners: [roi]              # who to ask
source: claude-session     # optional: incident id, MR, ticket, "claude-session", upstream URL
---
```

Incidents additionally require:

```yaml
severity: sev2             # sev1 | sev2 | sev3 | sev4
status: resolved           # open | mitigated | resolved
clusters: [site2-gpu-03]   # cluster names (no IPs)
started: 2026-10-01T09:12+03:00
resolved: 2026-10-01T11:40+03:00
```

Rules

- `title` is a sentence that would match what someone greps for during an outage.
- `applies_to` uses short tokens: `ocp-4.16`, `k8s-1.29`, `mce-2.7`, `hgx-h200`, `xe9680`,
  `vsphere-8`, `sno`, `hosted-cp`.
- `confidence` is honest. A single observation is `observed`, not `verified`.
