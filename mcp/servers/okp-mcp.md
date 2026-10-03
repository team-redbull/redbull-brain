---
title: Red Hat okp-mcp — Red Hat's own MCP server for RHOKP (optional; team-knowledge already searches RHOKP)
type: mcp
area: meta
tags: [mcp, rhokp, okp-mcp, kcs, solr]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
source: claude-session
---

# okp-mcp (Red Hat Offline Knowledge Portal MCP)

- **Upstream:** `rhel-lightspeed/okp-mcp` (Apache-2.0). Python 3.12 with third-party dependencies (fastmcp, httpx,
  pydantic…), run with `uv`. Server name "RHEL OKP Knowledge Base": its query shaping is centred on RHEL.
- **There is no binary to ship.** Unlike the Grafana and Kubernetes servers it cannot be vendored as one file:
  inside the air gap it runs from its container image,
  `quay.io/redhat-user-workloads/rhel-lightspeed-tenant/rhel-knowledge-bridge`, mirrored to the internal
  registry. It is therefore **not installed by the plugin**.
- **Both need RHOKP itself** (`registry.redhat.io/offline-knowledge-portal/rhokp-rhel9`, ~10 GB, access key):
  okp-mcp and our `team-knowledge` `rhokp` source are two clients of the same Solr index
  (`<rhokp>:8983/solr/portal`). Neither works until RHOKP is running — setup in `mcp/README.md`.

## Which one to use

| | `team-knowledge` (`rhokp` source) | `okp-mcp` |
|---|---|---|
| Ships with the plugin | yes (stdlib Python) | no (container image) |
| Searches | RHOKP **and** the brain, HyperShift/CAPI code, all doc snapshots in one call | RHOKP only |
| Filters | `product`, `version`, `doc_kind` | Red Hat's intent detection, document outline/section reading, CVE and errata lookups |
| Maintained by | us | Red Hat |

Default: `team-knowledge`. Add okp-mcp when RHOKP answers are poor for a class of questions — it reads long
documents by section and knows the portal's content types better than our generic query.

## Running it

- **Shared (OpenShift):** `deploy/openshift/okp-mcp.yaml` — optional, not in the default kustomization. It has no
  authentication, so no Route is created; reach it with `oc -n team-knowledge port-forward svc/okp-mcp 8000`.
- **Laptop:** `podman run` the image in the same pod as RHOKP with `MCP_TRANSPORT=streamable-http` and
  `MCP_SOLR_URL=http://localhost:8983`.
- **Client:** `mcp/clients/okp-mcp.mcp.json` (`http://localhost:8000/mcp`).
- Leave `MCP_GLITCHTIP_DSN` unset: with a DSN it sends exception reports to that endpoint.

## What is verified

Read from the upstream repository (README, deployment template, source layout) on 2026-10-03. **Nothing here has
been run**: not the image, not the manifest, not against an RHOKP — RHOKP needs a Red Hat access key that was not
available where this was written.

## History

- 2026-10-03: added as an optional server.
