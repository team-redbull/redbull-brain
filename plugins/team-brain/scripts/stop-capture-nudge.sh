#!/usr/bin/env bash
# Stop hook: after a substantial session that captured nothing, ask Claude ONCE whether it
# learned something worth keeping. Cheap: no model call, just counts tool uses in the transcript.
#
# Tunables (env):
#   BRAIN_NUDGE_MIN_TOOLS   tool calls before a session counts as "substantial" (default 20)
#   BRAIN_NUDGE_DISABLE=1   turn the nudge off
set -uo pipefail

[ "${BRAIN_NUDGE_DISABLE:-0}" = "1" ] && exit 0

input="$(cat)"
# Already continuing because of a Stop hook -> let Claude stop (prevents loops).
[ "$(jq -r '.stop_hook_active // false' <<<"$input")" = "true" ] && exit 0

session_id="$(jq -r '.session_id // "unknown"' <<<"$input")"
transcript="$(jq -r '.transcript_path // empty' <<<"$input")"
[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0

state_dir="${CLAUDE_PLUGIN_DATA:-$HOME/.cache/team-brain}"
mkdir -p "$state_dir"
marker="$state_dir/nudged-$session_id"
[ -f "$marker" ] && exit 0

# Housekeeping: drop markers older than 14 days.
find "$state_dir" -name 'nudged-*' -mtime +14 -delete 2>/dev/null || true

tool_uses="$(grep -oE '"type": ?"tool_use"' "$transcript" 2>/dev/null | wc -l | tr -d ' ')"
[ "${tool_uses:-0}" -ge "${BRAIN_NUDGE_MIN_TOOLS:-20}" ] || exit 0

# Skip if this session already captured (skill used) or is working inside the brain repo itself.
if grep -qE 'brain-learn|brain-curate|incident-report' "$transcript" 2>/dev/null; then exit 0; fi
brain="${TEAM_BRAIN_DIR:-$HOME/team-brain}"
cwd="$(jq -r '.cwd // empty' <<<"$input")"
case "$cwd" in "$brain"*) exit 0 ;; esac

touch "$marker"

jq -n '{
  decision: "block",
  reason: "Before finishing: this was a substantial session and nothing was captured to the team brain. Check whether it produced durable, non-obvious knowledge — a root cause, a workaround, a version- or hardware-specific quirk, a procedure that worked, or an assumption that turned out wrong. If yes, briefly tell the user what you would capture and use the team-brain:brain-learn skill (it asks for confirmation before pushing). If not, reply with one short line saying nothing needed capturing, and stop. Do not repeat your previous answer."
}'
