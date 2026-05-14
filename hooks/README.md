# Cursor Agent hooks (`hooks/`)

**What this is:** [Cursor Agent hooks](https://cursor.com/docs/agent/hooks) run small programs on lifecycle events (for example when a session starts, after each tool use, or when a turn stops). They receive JSON on **stdin** and may return JSON on **stdout** (for example a `followup_message` nudge). This directory holds **hook implementations**—the scripts and config they need.

**Registration:** Which hooks run is defined in **[`hooks.json`](../hooks.json)** at the **same level** as this `hooks/` folder. After install into `~/.cursor/`, paths in `hooks.json` are relative to that directory (for example `./hooks/agent-retro-meter/run.sh`).

## Contents

| Item | What it does |
|------|----------------|
| [agent-retro-meter/](agent-retro-meter/) | **Metrics + optional nudge:** counts tool use and wall time per Composer turn (and optional Task subagent metrics), compares **YAML** thresholds, appends **JSONL** log lines, and can suggest a follow-up (e.g. session retro). See [agent-retro-meter/README.md](agent-retro-meter/README.md) for glossary, setup, and `config.yaml` keys. |
| [agent-retro-meter/run.sh](agent-retro-meter/run.sh) | **Shell entrypoint** Cursor invokes; forwards to Python `meter.py` with the right environment. |
| [agent-retro-meter/meter.py](agent-retro-meter/meter.py) | **Python** logic: parse hook payload, update counters/timers, evaluate thresholds, write logs, emit hook response. |
| [agent-retro-meter/config.yaml](agent-retro-meter/config.yaml) | **Thresholds** (tool count, wall time, subagent options), log path, nudge text, and composer/subagent toggles. |
| [agent-retro-meter/requirements.txt](agent-retro-meter/requirements.txt) | **Python deps** (e.g. PyYAML) for `meter.py`. |

**Pairing:** The **cursor-session-retro** skill (under `../skills/cursor-session-retro/`) describes how to run a retro after a nudge or when you invoke it manually.
