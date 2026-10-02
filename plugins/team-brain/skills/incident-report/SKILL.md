---
name: incident-report
description: Write a blameless postmortem for an outage or degradation on one of our clusters into the team brain (incidents/YYYY/), with timeline, impact, root cause, contributing factors and action items, and open it as a merge request. Use when the user asks for a postmortem, incident report, RCA or "write up what happened".
---

# Incident report

## 1. Gather facts (ask only for what you can't find)

From this session, the user, and the cluster (read-only commands only):
- clusters affected (names, OCP version, topology: hosted/standalone, hardware)
- start / detection / mitigation / resolution times (with timezone, default Asia/Jerusalem)
- user-visible impact (which workloads, how many nodes/GPUs, data loss yes/no)
- the trigger, the root cause, contributing factors
- what fixed it, and what was tried that didn't
- evidence: key log lines, events, alert names (redacted)

Search the brain for related history first (skill `team-brain:brain-lookup`) — repeats matter.

## 2. Open a worktree and write

```bash
BRAIN="${TEAM_BRAIN_DIR:-$HOME/team-brain}"
WT="$(bash "$BRAIN/plugins/team-brain/scripts/brain-git.sh" start incident '<slug>')"
```

Copy `$WT/templates/incident.md` to `$WT/incidents/<yyyy>/<yyyy-mm-dd>-<slug>.md` and fill it in.
Keep it blameless: describe systems and decisions, not people's failings.

If the incident revealed durable knowledge (a quirk, a fix procedure), also create or update the
matching `knowledge/` or `runbooks/` page in the same worktree and link it from the report.
Mark root cause `hypothesis` if it isn't confirmed.

Apply the redaction rules from the `brain-learn` skill.

## 3. Review and submit

Show the user the summary + action items, wait for go-ahead, then:

```bash
bash "$BRAIN/plugins/team-brain/scripts/brain-git.sh" submit "$WT" "incident(<area>): <one-line summary>"
```
