# Agent retro — Cursor hooks reference

## After a hook nudge (operator)

Treat the injected line as a **signal**, not a full retro: open a **new chat**, attach **`@cursor-session-retro`**, paste **redacted** excerpts from the JSONL row or the original session, then run the retro workflow in the main skill.

**Setup guide (install, configure, test):** [`~/.cursor/hooks/agent-retro-meter/README.md`](../../hooks/agent-retro-meter/README.md).

User-level hooks in `~/.cursor/hooks.json` call [`~/.cursor/hooks/agent-retro-meter/run.sh`](~/.cursor/hooks/agent-retro-meter/run.sh), which runs [`meter.py`](../../hooks/agent-retro-meter/meter.py). The meter records per-generation tool usage and wall time, compares thresholds from **[`config.yaml`](../../hooks/agent-retro-meter/config.yaml)** (PyYAML), appends one JSON line per trigger to a log file, and optionally returns `followup_message` for the `stop` (and optionally `subagentStop`) hook.

**Plain-language terms:** In **`config.yaml`**, read the large comment block at the top (composer vs subagent, what “tools” counts, what “nudge” does). The hook **[README](../../hooks/agent-retro-meter/README.md)** has the same glossary under **“Glossary for config.yaml”**.

**Credits:** Cursor hook payloads do not include billing or credit balances. Use **tool count** and **wall time** (and subagent metrics) as practical proxies until usage fields exist.

## Log file location and rotation

- Default log: `~/.cursor/logs/agent-retro-triggers.jsonl` (see `paths.log` in `config.yaml`)
- Override: set `paths.log` in `config.yaml` (or use another file via `AGENT_RETRO_CONFIG` pointing at a YAML that sets `paths.log`)
- **Rotate** (keep history, start a fresh file):

```bash
mv ~/.cursor/logs/agent-retro-triggers.jsonl \
   ~/.cursor/logs/agent-retro-triggers-$(date +%Y%m%d-%H%M%S).jsonl
touch ~/.cursor/logs/agent-retro-triggers.jsonl
chmod 600 ~/.cursor/logs/agent-retro-triggers.jsonl
```

- Prefer **file permissions** `600` on JSONL if prompts may contain secrets.

## State file

- Default: `~/.cursor/hooks/agent-retro-meter/state.json` (`paths.state` in `config.yaml`)
- Override: change `paths.state` in your YAML config file
- Safe to delete if stuck (you lose dedup counters; next trigger may re-log if thresholds still met for an old generation—unlikely).

## Configuration (`config.yaml`)

Primary file: [`~/.cursor/hooks/agent-retro-meter/config.yaml`](../../hooks/agent-retro-meter/config.yaml). The file starts with a **term glossary** (what “tools”, “threshold”, “nudge”, etc. mean). Requires **PyYAML** (`pip install --user -r ~/.cursor/hooks/agent-retro-meter/requirements.txt`).

| Key | Default | Plain meaning |
|-----|---------|---------------|
| `paths.log` | `~/.cursor/logs/…jsonl` | Where each trigger writes **one JSON line** (may store your full prompt). |
| `paths.state` | `…/state.json` | Internal counters / dedup; safe to delete if corrupted. |
| `composer.min_tools` | `0` | **0 = off.** Else: fire when this **main Agent turn** had at least this many **agent tool invocations** (Read, Shell, Grep, …). |
| `composer.min_wall_ms` | `0` | **0 = off.** Else: fire when **real time** from Send → turn finished ≥ this many **milliseconds**. |
| `composer.require_both` | `false` | If **true**: fire only when **both** limits are **> 0** and **both** crossed (**AND**). Quieter for tool-heavy, short plan turns. If either limit is `0`, behaves as **OR**. |
| `composer.nudge` | `true` | If **true**: also allow an **auto follow-up** message after a trigger. If **false**: **log only**. |
| `composer.nudge_template` | `null` | **`null`** = built-in message with `{reasons}`. Custom string must include `{reasons}`. |
| `subagent.min_tools` | `0` | **0 = off.** For **Task** runs: Cursor’s `tool_call_count` threshold. |
| `subagent.min_ms` | `0` | **0 = off.** For **Task** runs: Cursor’s `duration_ms` threshold. |
| `subagent.nudge` | `false` | Same as composer nudge, but for sub-agent stop; usually **false**. |
| `subagent.nudge_template` | `null` | Same as composer. |

**Optional environment variable:** `AGENT_RETRO_CONFIG=/path/to/config.yaml` — only use this if the config file should live outside the default path.

**Idempotency:** At most **one log line and one composer nudge** per `generation_id` after thresholds cross. Subagent rows dedupe on a composite key of task, counts, duration, status.

## JSONL schema (one JSON object per line)

| Field | Composer | Subagent |
|-------|----------|----------|
| `triggered_at` | ISO-8601 UTC | same |
| `scope` | `"composer"` | `"subagent"` |
| `hook_event` | `"stop"` | `"subagentStop"` |
| `conversation_id` | from state / hook | from hook |
| `generation_id` | from hook | from hook (may be null) |
| `model` | from hook | from hook |
| `composer_mode` | from `sessionStart` (`agent` / `ask` / `edit`) | `null` |
| `subagent_type` | `null` | e.g. `explore` |
| `subagent_task` | `null` | task string |
| `reasons` | e.g. `["tools>=30"]` | e.g. `["subagent_tools>=10"]` |
| `metrics` | `tool_count`, `wall_ms`, `post_tool_duration_sum_ms` | `tool_call_count`, `duration_ms` |
| `prompt` | full user prompt (sensitive) | `null` |

## Example log lines

```json
{"triggered_at":"2026-04-20T12:00:00Z","scope":"composer","hook_event":"stop","conversation_id":"…","generation_id":"…","model":"…","composer_mode":"agent","subagent_type":null,"subagent_task":null,"reasons":["tools>=30"],"metrics":{"tool_count":32,"wall_ms":600000,"post_tool_duration_sum_ms":45000},"prompt":"…"}
```

```json
{"triggered_at":"2026-04-20T12:05:00Z","scope":"subagent","hook_event":"subagentStop","conversation_id":"…","generation_id":null,"model":"…","composer_mode":null,"subagent_type":"explore","subagent_task":"Map the auth module","reasons":["subagent_duration_ms>=120000"],"metrics":{"tool_call_count":15,"duration_ms":180000},"prompt":null}
```

## Troubleshooting

1. **Cursor Settings → Hooks** — confirm `hooks.json` loads and scripts run without errors.
2. **Hooks output channel** — stderr from `meter.py` includes tracebacks on parse errors (agent still proceeds; fail-open).
3. **No log lines** — thresholds may be `0` (disabled). Set e.g. `composer.min_tools: 25` in `config.yaml` for a dry run.
4. **Double nudge** — should not happen per generation; if it does, file a bug with Cursor hook `stop` semantics and set `composer.nudge: false` temporarily.

## Dry run (CLI)

```bash
cat > /tmp/retro-cli-config.yaml <<'EOF'
version: 1
paths:
  log: /tmp/retro-test.jsonl
  state: /tmp/retro-test-state.json
composer:
  min_tools: 1
  min_wall_ms: 0
  nudge: true
  nudge_template: null
subagent:
  min_tools: 0
  min_ms: 0
  nudge: false
  nudge_template: null
EOF
export AGENT_RETRO_CONFIG=/tmp/retro-cli-config.yaml
rm -f /tmp/retro-test.jsonl /tmp/retro-test-state.json
M=~/.cursor/hooks/agent-retro-meter/meter.py
echo '{"hook_event_name":"sessionStart","conversation_id":"c1","composer_mode":"agent"}' | python3 "$M"
echo '{"hook_event_name":"beforeSubmitPrompt","conversation_id":"c1","generation_id":"g1","model":"m","prompt":"hi"}' | python3 "$M"
echo '{"hook_event_name":"postToolUse","conversation_id":"c1","generation_id":"g1","duration":1}' | python3 "$M"
echo '{"hook_event_name":"stop","conversation_id":"c1","generation_id":"g1","model":"m","status":"completed","loop_count":0}' | python3 "$M"
cat /tmp/retro-test.jsonl
```

You should see one JSONL row and stdout containing `followup_message`.
