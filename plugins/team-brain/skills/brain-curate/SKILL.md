---
name: brain-curate
description: Curate the team brain — promote inbox captures into knowledge/runbooks, merge duplicates, flag stale pages, fix frontmatter — and open one merge request with every decision explained. Use when the user asks to curate, clean up, tidy or review the brain or its inbox.
disable-model-invocation: true
---

# Curate the team brain

```bash
BRAIN="${TEAM_BRAIN_DIR:-$HOME/team-brain}"
WT="$(bash "$BRAIN/plugins/team-brain/scripts/brain-git.sh" start curate 'inbox-review')"
cd "$WT"
python3 scripts/brain.py stale --days 180
ls inbox/
```

For **each inbox item** decide one of:
- **promote** → move to `knowledge/<area>/` or `runbooks/<area>/`, set `type`, tidy wording
- **merge** → fold into an existing page (add to it, extend `applies_to`, add a `## History` line), delete the inbox file
- **keep** → still unclear; leave it, note what's missing
- **discard** → wrong, duplicate, or not durable; delete it

Also:
- look for near-duplicate pages (same symptom/error string) and merge them
- for stale pages, do **not** delete; list them in the MR so owners can re-verify
- fix frontmatter errors reported by `python3 scripts/brain.py validate`

Never raise a page's `confidence` during curation unless there's new evidence.

Present the decision table to the user (item → decision → reason), wait for approval, then:

```bash
bash "$BRAIN/plugins/team-brain/scripts/brain-git.sh" submit "$WT" "brain(curate): inbox review $(date +%F)"
```

Put the decision table in the MR description (edit it after `submit` with `glab mr update` if
needed).
