---
title: day2 Helm chart — OAuth auto-syncs, KubeletConfig and IDMS stay on manual sync
type: knowledge
area: gitops
tags: [argocd, helm, day2, oauth, kubeletconfig, idms, sync-policy]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [roi]
source: team-decision
---

# day2 chart sync policy

Every cluster is deployed through a Helm chart; day-2 config ships in a `day2` chart delivered by
Argo CD. It contains OAuth config, KubeletConfig and ImageDigestMirrorSet (IDMS).

## Decision

- **OAuth** — automated sync.
- **KubeletConfig, IDMS** — manual sync. KubeletConfig changes roll out through the Machine Config
  Operator and reboot nodes pool by pool, so they should land in a chosen window, not whenever Git
  changes. (Owner: add the IDMS-specific reason.)

## Scope & caveats

Per-resource sync behaviour inside one Argo CD Application needs per-resource handling (e.g.
splitting into separate Applications, or sync-options annotations) — document the mechanism used
here once settled.

## History

- 2026-10-03: seeded
