---
title: oc-mirror runs against the shared registry overwrite each other's redhat-operator-index catalog
type: knowledge
area: registry-mirroring
tags: [oc-mirror, catalogsource, fbc, redhat-operator-index, disconnected]
applies_to: [ocp-4.20]
confidence: verified
last_verified: 2026-09-02
owners: [roi]
source: team-discussion
---

# oc-mirror runs overwrite each other's operator catalog in the shared registry

## Symptom

An operator that was mirrored earlier (e.g. LVMO) disappears from OperatorHub / its
CatalogSource after someone else mirrors a different operator (e.g. MCE). Its images are still in
the registry, but the catalog no longer lists it.

## Cause

Several engineers run `oc-mirror` (mirror-to-disk → disk-to-mirror) into the same disconnected
registry. Each run pushes its **filtered** catalog to the same tag
(`redhat/redhat-operator-index:v4.20`), so the last push wins and replaces the catalog contents of
earlier runs.

## Fix / workaround

- Red Hat support (case opened for this) recommends setting `targetCatalog` / `targetTag` per
  operator so each run publishes its own catalog image instead of sharing one tag.
- Rejected alternatives: re-mirroring everything each time (2× storage, messy); mirroring the full
  unfiltered catalog (operators try to upgrade to bundles that aren't in the registry); editing the
  catalog JSON by hand.
- Planned: a Go tool (operator-registry `declcfg`) that reads the FBC from every catalog image
  under a dedicated registry path and unions them into one index containing only what is actually
  mirrored — cumulative instead of replaced.

## Scope & caveats

Applies to any shared registry where more than one person runs filtered `oc-mirror`. Seen on 4.20.

## History

- 2026-10-03: seeded from team notes
