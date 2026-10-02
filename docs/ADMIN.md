---
title: Rolling the team-brain plugin out to every engineer
type: reference
area: meta
tags: [meta, rollout, managed-settings]
applies_to: []
confidence: observed
last_verified: 2026-10-03
owners: [platform-team]
---

# Rolling out team-brain

## Option A — each engineer installs (simplest)

See README "Setup". Two commands per person.

## Option B — project-level auto-suggest

Commit this into the `.claude/settings.json` of the repos the team works in (ClickCluster,
operators, GitOps repos). When someone trusts the folder, Claude Code offers to install the plugin:

```json
{
  "extraKnownMarketplaces": {
    "team-brain": {
      "source": { "source": "git", "url": "git@gitlab.internal:platform/team-brain.git" }
    }
  },
  "enabledPlugins": { "team-brain@team-brain": true }
}
```

## Option C — managed settings (enforced fleet-wide)

Put the same two keys in the managed settings file on engineer workstations
(Linux: `/etc/claude-code/managed-settings.json`). Check the exact keys and source-type
names against your Claude Code version's settings reference before rolling out —
`claude plugin validate .` and `/plugin` will show whether the marketplace resolved.

## Air-gapped notes

- The marketplace is just this git repo on the internal GitLab — no internet needed.
- MCP servers in `plugins/team-brain/.mcp.json` must be binaries/images available offline;
  see `mcp/README.md`.
- `docs/upstream/` is synced on a connected host and committed (or pushed via Git LFS).

## Updating the plugin

Bump `version` in `plugins/team-brain/.claude-plugin/plugin.json` when hooks/skills change.
Engineers get it on `claude plugin marketplace update team-brain` (or automatically if
auto-update is on for the marketplace).

## Environment each engineer needs

- `GRAFANA_URL`, `GRAFANA_SERVICE_ACCOUNT_TOKEN` — read-only service account for the Grafana MCP
  (`mcp/servers/grafana.md`); `mcp-grafana` binary on `PATH`.
- Mirror creation and `GIT_MIRROR_BASE`: `mcp/README.md` ("Mirrors to create before `--sync`").
- Bump `version` in `plugins/team-brain/.claude-plugin/plugin.json` whenever hooks, skills or `.mcp.json` change.
