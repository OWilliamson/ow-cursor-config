# Agent retro meter (Cursor hooks)

This package records **per–user-message (generation)** tool usage and wall time in Cursor Agent, compares thresholds from a **YAML config file**, writes **one JSON line per trigger** to a log file, and optionally asks Cursor to **auto-submit a short follow-up** (`followup_message`) suggesting a session retro.

It pairs with the personal skill **`@cursor-session-retro`** ([`~/.cursor/skills/cursor-session-retro/SKILL.md`](../../skills/cursor-session-retro/SKILL.md)), which defines *how* to run a retro once you are nudged or you invoke the skill manually.

## Glossary for config.yaml

| Term | Meaning |
|------|--------|
| **Composer** | The main Cursor Agent chat (the thread where you type prompts). |
| **Turn / generation** | One user message plus the agent’s work until that reply completes. Thresholds apply **per turn**. |
| **Tool call** (`min_tools`) | Each time the agent uses a Cursor capability in that turn—e.g. read a file, run a terminal command, search the repo, call MCP—Cursor counts it. This is **not** “CLI tools installed on your PC” in the abstract; it is **agent tool invocations**. |
| **Wall time** (`min_wall_ms`) | Real clock time from **Send** on your message until the agent **finishes** that turn (milliseconds). Catches slow or stuck-feeling runs even when tool count is low. |
| **Threshold** | A limit you set on tool count and/or wall time. Default is **OR** (either limit can trigger). Set `composer.require_both: true` for **AND** (both must cross)—quieter when plans spike tool count but finish in under your wall clock budget. |
| **Trigger** | Append **one JSON line** to `paths.log` with model, prompt, reasons, etc. Optionally send a **nudge** (see below). |
| **Nudge** | If enabled, the `stop` hook returns `followup_message`; Cursor may **auto-submit** that text as the next user message (e.g. suggesting `@cursor-session-retro`). Turn off if you only want silent logging. |
| **Subagent** | A **Task** sub-session (explore / shell / …). `subagent.*` keys use Cursor’s metrics for that child run, separate from the main composer turn. |

## What it does (high level)

1. **`sessionStart`** — remembers `composer_mode` (`agent` / `ask` / `edit`) for the conversation.
2. **`beforeSubmitPrompt`** — stores the user **prompt**, `generation_id`, and a timestamp when the message is sent.
3. **`postToolUse`** — increments **tool count** and sums **tool durations** (ms) for that `generation_id`.
4. **`stop`** — when the assistant turn ends, computes **wall time** (ms) from submit to stop. If any enabled threshold is met, appends a line to the JSONL log and (by default) returns `followup_message` **once per generation**.
5. **`subagentStop`** — optional logging for **Task** subagents using Cursor’s `tool_call_count` and `duration_ms`; separate thresholds; **nudge off by default**.

**Billing / credits:** Hook JSON does **not** include credit usage. Use **tool count** and **wall time** (and subagent metrics) as proxies.

## Requirements

- **Python 3** on `PATH` as `python3` (the wrapper calls `python3 …/meter.py`).
- **PyYAML** — install once so `meter.py` can read `config.yaml`:

```bash
pip install --user -r ~/.cursor/hooks/agent-retro-meter/requirements.txt
```

  On some Linux distros: `sudo apt install python3-yaml` instead.

- **Cursor** with [Agent hooks](https://cursor.com/docs/agent/hooks) enabled (normal desktop install).

## Setup

### 1. Install files (this repo layout)

You should have:

```
~/.cursor/
├── hooks.json                          # hook registration
├── hooks/
│   └── agent-retro-meter/
│       ├── README.md                   # this file
│       ├── config.yaml                 # thresholds & paths (edit this)
│       ├── requirements.txt            # PyYAML
│       ├── run.sh                      # executable
│       └── meter.py                    # invoked by run.sh
└── skills/
    └── cursor-session-retro/
        └── SKILL.md                  # retro workflow (optional but recommended)
```

### 2. Make scripts executable

```bash
chmod +x ~/.cursor/hooks/agent-retro-meter/run.sh
chmod +x ~/.cursor/hooks/agent-retro-meter/meter.py   # optional
```

### 3. Register hooks in `~/.cursor/hooks.json`

User-level hooks run with working directory **`~/.cursor/`**, so commands use the `./hooks/...` prefix.

If **`hooks.json` already exists**, merge the `hooks` entries (append to each hook array) instead of overwriting unrelated hooks.

Minimal entries (match what ships in a fresh install):

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      { "command": "./hooks/agent-retro-meter/run.sh", "timeout": 5 }
    ],
    "beforeSubmitPrompt": [
      { "command": "./hooks/agent-retro-meter/run.sh", "timeout": 5 }
    ],
    "postToolUse": [
      { "command": "./hooks/agent-retro-meter/run.sh", "timeout": 5 }
    ],
    "stop": [{ "command": "./hooks/agent-retro-meter/run.sh", "timeout": 15 }],
    "subagentStop": [
      { "command": "./hooks/agent-retro-meter/run.sh", "timeout": 15 }
    ]
  }
}
```

### 4. Restart Cursor (or reload hooks)

Save `hooks.json`, then confirm under **Cursor Settings → Hooks** that scripts appear and run without errors. Use the **Hooks** output channel if something fails.

### 5. Configure thresholds (`config.yaml`)

Edit **`~/.cursor/hooks/agent-retro-meter/config.yaml`**. The shipped file lists every option with **comment lines** (`# …`) documenting defaults and examples; the **active** YAML keys use the same safe defaults (`0` = threshold off) until you change them.

Set at least one composer threshold for real use, for example:

```yaml
composer:
  min_tools: 35
  min_wall_ms: 900000   # 15 minutes
```

Changes are picked up on the **next hook invocation** (mtime-based cache). Restart Cursor is not required for config edits.

**Optional:** use a different file path (only supported override via environment):

```bash
export AGENT_RETRO_CONFIG=/path/to/alternate-retro-config.yaml
```

(Launch Cursor from a context that inherits this variable, or set it in your desktop session.)

## Configuration reference (`config.yaml`)

See the **comment block at the top of `config.yaml`** for the same glossary in-line while you edit.

| Key | Default | What it does |
|-----|---------|----------------|
| `paths.log` | `~/.cursor/logs/…jsonl` | File where each **trigger** appends one JSON line (may include your **full prompt**—treat as sensitive). |
| `paths.state` | `…/state.json` | Internal dedup/counters so each turn logs **at most once**; not human-readable. |
| `composer.min_tools` | `0` | **Off if 0.** Otherwise: trigger when this turn’s **agent tool call count** (Read, Shell, Grep, …) is **≥** this number. |
| `composer.min_wall_ms` | `0` | **Off if 0.** Otherwise: trigger when **elapsed ms** for the whole turn (send → stop) is **≥** this. |
| `composer.require_both` | `false` | If **true**, both `min_tools` and `min_wall_ms` must be **> 0** and **both** crossed before a trigger (**AND**). If either threshold is `0`, AND is skipped (**OR**). |
| `composer.nudge` | `true` | If **true** and a trigger fires: Cursor may auto-send a follow-up suggesting `@cursor-session-retro`. If **false**: log only. |
| `composer.nudge_template` | `null` | **`null`** = built-in English message with `{reasons}`. Or set your own string; must use `{reasons}` where the list of fired rules should appear. |
| `subagent.min_tools` | `0` | **Off if 0.** For **Task** sub-agents: trigger if Cursor’s `tool_call_count` **≥** this. |
| `subagent.min_ms` | `0` | **Off if 0.** For **Task** sub-agents: trigger if Cursor’s `duration_ms` **≥** this. |
| `subagent.nudge` | `false` | Same idea as composer nudge, but for `subagentStop`; usually **false** so sub-tasks do not auto-continue the parent. |
| `subagent.nudge_template` | `null` | Same as composer; `{reasons}` supported. |

**Choosing thresholds:** With `require_both: false`, either axis can fire alone. With `require_both: true`, tool-heavy **plan** runs that finish quickly usually **will not** trigger unless wall time also exceeds `min_wall_ms`. Example: `min_tools: 48` plus `min_wall_ms: 900000` catches long, heavy turns without firing on short plan spikes alone.

## Plan-heavy Cursor runs (efficiency + fewer false triggers)

**Why plans spike the meter:** one user message can spawn many reads/greps/edits while the agent maps the repo before changing anything—high **tool count** in one **generation**.

**Make plan execution leaner (agent behavior):**

- Put **scope in the prompt** (which folder, which report, “do not search the whole repo”).
- **Attach** the key files or a short tree instead of letting the agent discover everything.
- Prefer **smaller steps** (“plan only, then stop” vs “plan and implement in one message”) so one generation does less work.
- If you use **Task / explore**, give a tight task string so sub-agents do not fan out.

**Make the meter less sensitive during those runs (config):**

1. Set **`composer.require_both: true`** so a burst of tools **without** a long wall clock does not fire alone.
2. Raise **`composer.min_tools`** (e.g. 55–70) if AND mode still fires too often on real plans.
3. Raise **`composer.min_wall_ms`** if only very long sessions should count.
4. Temporarily set **`composer.nudge: false`** if you still want JSONL logs but no auto follow-up while tuning.

## Log format (JSONL)

Each trigger is **one JSON object per line** in the file configured as `paths.log` (default `~/.cursor/logs/agent-retro-triggers.jsonl`).

Composer rows include the **full user prompt** (sensitive). Subagent rows set `"prompt": null` and include `subagent_task` instead.

Typical composer line (pretty-printed):

```json
{
  "triggered_at": "2026-04-20T12:00:00Z",
  "scope": "composer",
  "hook_event": "stop",
  "conversation_id": "…",
  "generation_id": "…",
  "model": "…",
  "composer_mode": "agent",
  "subagent_type": null,
  "subagent_task": null,
  "reasons": ["tools>=35"],
  "metrics": {
    "tool_count": 40,
    "wall_ms": 120000,
    "post_tool_duration_sum_ms": 45000
  },
  "prompt": "…"
}
```

**Rotation** (archive and start a new file):

```bash
mv ~/.cursor/logs/agent-retro-triggers.jsonl \
   ~/.cursor/logs/agent-retro-triggers-$(date +%Y%m%d-%H%M%S).jsonl
touch ~/.cursor/logs/agent-retro-triggers.jsonl
chmod 600 ~/.cursor/logs/agent-retro-triggers.jsonl
```

## Manual test (no Cursor UI)

From a terminal (uses a **throwaway config** under `/tmp`):

```bash
cat > /tmp/retro-demo-config.yaml <<'EOF'
version: 1
paths:
  log: /tmp/agent-retro-demo.jsonl
  state: /tmp/agent-retro-demo-state.json
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
export AGENT_RETRO_CONFIG=/tmp/retro-demo-config.yaml
rm -f /tmp/agent-retro-demo.jsonl /tmp/agent-retro-demo-state.json
M=~/.cursor/hooks/agent-retro-meter/meter.py

echo '{"hook_event_name":"sessionStart","conversation_id":"c1","composer_mode":"agent"}' | python3 "$M"
echo '{"hook_event_name":"beforeSubmitPrompt","conversation_id":"c1","generation_id":"g1","model":"m","prompt":"hello"}' | python3 "$M"
echo '{"hook_event_name":"postToolUse","conversation_id":"c1","generation_id":"g1","duration":10}' | python3 "$M"
echo '{"hook_event_name":"stop","conversation_id":"c1","generation_id":"g1","model":"m","status":"completed","loop_count":0}' | python3 "$M"

cat /tmp/agent-retro-demo.jsonl
```

You should see one JSON line; the last command’s stdout may include `followup_message`.

## Behavior guarantees

- **Fail-open:** `meter.py` exits `0` and prints `{}` on parse or internal errors so the agent is not blocked (errors may appear on stderr).
- **Idempotency:** At most **one log line** and **one composer nudge** per `generation_id` after thresholds cross.
- **State lock:** `state.json` updates use `flock` to reduce corruption if hooks overlap.

## Related docs

- Retro skill + hook overview: [`~/.cursor/skills/cursor-session-retro/SKILL.md`](../../skills/cursor-session-retro/SKILL.md)
- YAML keys / schema / extra troubleshooting: [`~/.cursor/skills/cursor-session-retro/reference-hooks.md`](../../skills/cursor-session-retro/reference-hooks.md)
- Official hooks: [Cursor Hooks documentation](https://cursor.com/docs/agent/hooks)
