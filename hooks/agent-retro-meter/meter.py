#!/usr/bin/env python3
"""
Cursor user hook: agent retro meter — thresholds, JSONL logging, optional stop/subagentStop nudge.

Reads hook JSON from stdin; writes optional JSON to stdout for hooks that consume it.
Always exits 0 (fail-open) unless explicitly changed.
"""

from __future__ import annotations

import copy
import fcntl
import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore[assignment]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _expand(p: str) -> Path:
    return Path(p).expanduser().resolve()


def _default_config() -> dict[str, Any]:
    home = Path.home()
    return {
        "version": 1,
        "paths": {
            "log": str(home / ".cursor" / "logs" / "agent-retro-triggers.jsonl"),
            "state": str(home / ".cursor" / "hooks" / "agent-retro-meter" / "state.json"),
        },
        "composer": {
            "min_tools": 0,
            "min_wall_ms": 0,
            # If true, trigger only when BOTH thresholds are non-zero AND both crossed (stricter).
            "require_both": False,
            "nudge": True,
            "nudge_template": None,
        },
        "subagent": {
            "min_tools": 0,
            "min_ms": 0,
            "nudge": False,
            "nudge_template": None,
        },
    }


def _merge_overlay(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for section in ("paths", "composer", "subagent"):
        if section in overlay and isinstance(overlay[section], dict):
            out.setdefault(section, {})
            out[section].update(overlay[section])
    return out


def _as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    if s in ("1", "true", "yes", "on"):
        return True
    if s in ("0", "false", "no", "off", ""):
        return default
    return default


def _normalize_config(raw: dict[str, Any]) -> dict[str, Any]:
    cfg = _default_config()
    merged = _merge_overlay(cfg, raw)
    merged["paths"]["log"] = str(merged["paths"].get("log") or cfg["paths"]["log"])
    merged["paths"]["state"] = str(merged["paths"].get("state") or cfg["paths"]["state"])
    c = merged["composer"]
    c["min_tools"] = _as_int(c.get("min_tools"), 0)
    c["min_wall_ms"] = _as_int(c.get("min_wall_ms"), 0)
    c["require_both"] = _as_bool(c.get("require_both"), False)
    c["nudge"] = _as_bool(c.get("nudge"), True)
    nt = c.get("nudge_template")
    if nt is not None and str(nt).strip() == "":
        nt = None
    c["nudge_template"] = nt
    s = merged["subagent"]
    s["min_tools"] = _as_int(s.get("min_tools"), 0)
    s["min_ms"] = _as_int(s.get("min_ms"), 0)
    s["nudge"] = _as_bool(s.get("nudge"), False)
    st = s.get("nudge_template")
    if st is not None and str(st).strip() == "":
        st = None
    s["nudge_template"] = st
    return merged


_CONFIG_CACHE: dict[str, Any] | None = None
_CONFIG_CACHE_KEY: tuple[str, float | None] | None = None


def get_config() -> dict[str, Any]:
    """Load config.yaml (PyYAML). Cached until file mtime changes."""
    global _CONFIG_CACHE, _CONFIG_CACHE_KEY
    path = Path(
        os.environ.get(
            "AGENT_RETRO_CONFIG",
            str(Path.home() / ".cursor" / "hooks" / "agent-retro-meter" / "config.yaml"),
        )
    ).expanduser()
    try:
        mtime = path.stat().st_mtime if path.exists() else None
    except OSError:
        mtime = None
    key = (str(path.resolve()), mtime)
    if _CONFIG_CACHE is not None and _CONFIG_CACHE_KEY == key:
        return _CONFIG_CACHE

    cfg = _default_config()
    if path.exists():
        if yaml is None:
            sys.stderr.write(
                "[agent-retro-meter] PyYAML is not installed; ignoring "
                f"{path}. Install: pip install --user pyyaml "
                f"(see {path.parent / 'requirements.txt'})\n"
            )
        else:
            try:
                text = path.read_text(encoding="utf-8")
                loaded = yaml.safe_load(text)
                if loaded is None:
                    loaded = {}
                if isinstance(loaded, dict):
                    cfg = _normalize_config(loaded)
                else:
                    sys.stderr.write(f"[agent-retro-meter] Config must be a mapping: {path}\n")
            except Exception as exc:  # pragma: no cover
                sys.stderr.write(f"[agent-retro-meter] Failed to read {path}: {exc}\n")
    else:
        cfg = _default_config()

    _CONFIG_CACHE = cfg
    _CONFIG_CACHE_KEY = key
    return cfg


def _log_path() -> Path:
    raw = get_config()["paths"]["log"]
    path = _expand(str(raw))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _state_path() -> Path:
    raw = get_config()["paths"]["state"]
    path = _expand(str(raw))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _read_json_stdin() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def _with_state(mutator) -> None:
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with open(path, "r+", encoding="utf-8") as fp:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            fp.seek(0)
            raw = fp.read()
            if raw.strip():
                try:
                    state = json.loads(raw)
                except json.JSONDecodeError:
                    state = {"sessions": {}, "generations": {}, "subagent_logged_keys": []}
            else:
                state = {"sessions": {}, "generations": {}, "subagent_logged_keys": []}
            if "sessions" not in state:
                state["sessions"] = {}
            if "generations" not in state:
                state["generations"] = {}
            if "subagent_logged_keys" not in state:
                state["subagent_logged_keys"] = []

            mutator(state)

            fp.seek(0)
            fp.truncate()
            fp.write(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
            fp.flush()
        finally:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass


def _prune_generations(state: dict[str, Any], max_entries: int = 80) -> None:
    gens = state.get("generations", {})
    if len(gens) <= max_entries:
        return
    items = sorted(
        gens.items(),
        key=lambda kv: kv[1].get("submitted_ms", 0),
        reverse=True,
    )[:max_entries]
    state["generations"] = dict(items)


def _prune_subagent_keys(state: dict[str, Any], max_keys: int = 200) -> None:
    keys = state.get("subagent_logged_keys", [])
    if len(keys) > max_keys:
        state["subagent_logged_keys"] = keys[-max_keys:]


def handle_session_start(data: dict[str, Any]) -> dict[str, Any]:
    conv = data.get("conversation_id") or data.get("session_id")
    if not conv:
        return {}

    def mut(state: dict[str, Any]) -> None:
        state["sessions"][str(conv)] = {
            "composer_mode": data.get("composer_mode"),
            "session_started_ms": _now_ms(),
        }

    _with_state(mut)
    return {}


def handle_before_submit_prompt(data: dict[str, Any]) -> dict[str, Any]:
    gid = data.get("generation_id")
    if not gid:
        return {}
    conv = data.get("conversation_id")

    def mut(state: dict[str, Any]) -> None:
        state["generations"][str(gid)] = {
            "conversation_id": conv,
            "prompt": data.get("prompt") or "",
            "submitted_ms": _now_ms(),
            "model": data.get("model"),
            "tool_count": 0,
            "post_tool_duration_sum_ms": 0,
            "composer_trigger_logged": False,
            "composer_nudge_sent": False,
        }
        _prune_generations(state)

    _with_state(mut)
    return {}


def handle_post_tool_use(data: dict[str, Any]) -> dict[str, Any]:
    gid = data.get("generation_id")
    if not gid:
        return {}

    duration = data.get("duration")
    if duration is None:
        duration = 0
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 0

    def mut(state: dict[str, Any]) -> None:
        g = state["generations"].setdefault(
            str(gid),
            {
                "conversation_id": data.get("conversation_id"),
                "prompt": "",
                "submitted_ms": _now_ms(),
                "model": data.get("model"),
                "tool_count": 0,
                "post_tool_duration_sum_ms": 0,
                "composer_trigger_logged": False,
                "composer_nudge_sent": False,
            },
        )
        g["tool_count"] = int(g.get("tool_count", 0)) + 1
        g["post_tool_duration_sum_ms"] = int(g.get("post_tool_duration_sum_ms", 0)) + duration
        if g.get("model") is None and data.get("model"):
            g["model"] = data.get("model")

    _with_state(mut)
    return {}


def _composer_session_mode(state: dict[str, Any], conversation_id: str | None) -> str | None:
    if not conversation_id:
        return None
    sess = state.get("sessions", {}).get(str(conversation_id))
    if not sess:
        return None
    return sess.get("composer_mode")


def handle_stop(data: dict[str, Any]) -> dict[str, Any]:
    gid = data.get("generation_id")
    if not gid:
        print(json.dumps({}))
        return {}

    ccfg = get_config()["composer"]
    min_tools = _as_int(ccfg.get("min_tools"), 0)
    min_wall = _as_int(ccfg.get("min_wall_ms"), 0)
    require_both = _as_bool(ccfg.get("require_both"), False)
    nudge_on = _as_bool(ccfg.get("nudge"), True)

    out: dict[str, Any] = {}
    log_line: dict[str, Any] | None = None

    def mut(state: dict[str, Any]) -> None:
        nonlocal log_line, out
        g = state["generations"].get(str(gid))
        if not g:
            return
        if g.get("composer_trigger_logged"):
            return

        tool_count = int(g.get("tool_count", 0))
        sum_dur = int(g.get("post_tool_duration_sum_ms", 0))
        submitted = int(g.get("submitted_ms", _now_ms()))
        wall_ms = max(0, _now_ms() - submitted)
        reasons: list[str] = []

        tools_hit = min_tools > 0 and tool_count >= min_tools
        wall_hit = min_wall > 0 and wall_ms >= min_wall
        and_mode = require_both and min_tools > 0 and min_wall > 0
        if and_mode:
            if not (tools_hit and wall_hit):
                return
            if tools_hit:
                reasons.append(f"tools>={min_tools}")
            if wall_hit:
                reasons.append(f"wall_ms>={min_wall}")
        else:
            if tools_hit:
                reasons.append(f"tools>={min_tools}")
            if wall_hit:
                reasons.append(f"wall_ms>={min_wall}")

        if not reasons:
            return

        conv = g.get("conversation_id") or data.get("conversation_id")
        mode = _composer_session_mode(state, str(conv) if conv else None)
        model = data.get("model") or g.get("model")

        log_line = {
            "triggered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "composer",
            "hook_event": "stop",
            "conversation_id": conv,
            "generation_id": str(gid),
            "model": model,
            "composer_mode": mode,
            "subagent_type": None,
            "subagent_task": None,
            "reasons": reasons,
            "metrics": {
                "tool_count": tool_count,
                "wall_ms": wall_ms,
                "post_tool_duration_sum_ms": sum_dur,
            },
            "prompt": g.get("prompt"),
        }

        g["composer_trigger_logged"] = True

        if nudge_on and not g.get("composer_nudge_sent"):
            reasons_txt = ", ".join(reasons)
            tmpl = ccfg.get("nudge_template") or (
                "Session retro: thresholds crossed ({reasons}). Run @cursor-session-retro in a new chat; scrub secrets if pasting excerpts."
            )
            try:
                msg = tmpl.format(reasons=reasons_txt)
            except (KeyError, ValueError):
                msg = (
                    f"Session retro: thresholds crossed ({reasons_txt}). "
                    "Run @cursor-session-retro in a new chat; scrub secrets if pasting excerpts."
                )
            out["followup_message"] = msg
            g["composer_nudge_sent"] = True

    _with_state(mut)

    if log_line is not None:
        try:
            append_jsonl(_log_path(), log_line)
        except OSError:
            pass

    print(json.dumps(out))
    return out


def _subagent_dedup_key(data: dict[str, Any]) -> str:
    parts = [
        str(data.get("parent_conversation_id") or ""),
        str(data.get("task") or ""),
        str(data.get("subagent_type") or ""),
        str(data.get("tool_call_count") or ""),
        str(data.get("duration_ms") or ""),
        str(data.get("status") or ""),
    ]
    return "|".join(parts)


def handle_subagent_stop(data: dict[str, Any]) -> dict[str, Any]:
    scfg = get_config()["subagent"]
    min_tools = _as_int(scfg.get("min_tools"), 0)
    min_ms = _as_int(scfg.get("min_ms"), 0)
    nudge_sub = _as_bool(scfg.get("nudge"), False)

    tool_count = int(data.get("tool_call_count") or 0)
    duration_ms = int(data.get("duration_ms") or 0)
    reasons: list[str] = []
    if min_tools > 0 and tool_count >= min_tools:
        reasons.append(f"subagent_tools>={min_tools}")
    if min_ms > 0 and duration_ms >= min_ms:
        reasons.append(f"subagent_duration_ms>={min_ms}")

    if not reasons:
        print(json.dumps({}))
        return {}

    key = _subagent_dedup_key(data)
    out: dict[str, Any] = {}
    log_line: dict[str, Any] | None = None

    def mut(state: dict[str, Any]) -> None:
        nonlocal log_line
        logged = state.setdefault("subagent_logged_keys", [])
        if key in logged:
            return
        logged.append(key)
        _prune_subagent_keys(state)

        log_line = {
            "triggered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope": "subagent",
            "hook_event": "subagentStop",
            "conversation_id": data.get("conversation_id"),
            "generation_id": data.get("generation_id"),
            "model": data.get("model"),
            "composer_mode": None,
            "subagent_type": data.get("subagent_type"),
            "subagent_task": data.get("task"),
            "reasons": reasons,
            "metrics": {
                "tool_call_count": tool_count,
                "duration_ms": duration_ms,
            },
            "prompt": None,
        }

    _with_state(mut)

    if log_line is None:
        print(json.dumps({}))
        return {}

    try:
        append_jsonl(_log_path(), log_line)
    except OSError:
        pass

    if nudge_sub:
        reasons_txt = ", ".join(log_line["reasons"])
        tmpl = scfg.get("nudge_template") or (
            "Subagent run crossed thresholds ({reasons}). Consider @cursor-session-retro with the subagent task summary; scrub secrets."
        )
        try:
            msg = tmpl.format(reasons=reasons_txt)
        except (KeyError, ValueError):
            msg = (
                f"Subagent run crossed thresholds ({reasons_txt}). "
                "Consider @cursor-session-retro; scrub secrets."
            )
        out["followup_message"] = msg

    print(json.dumps(out))
    return out


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main() -> None:
    try:
        data = _read_json_stdin()
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    hook = data.get("hook_event_name") or data.get("hookEventName")
    try:
        if hook == "sessionStart":
            handle_session_start(data)
            print(json.dumps({}))
        elif hook == "beforeSubmitPrompt":
            handle_before_submit_prompt(data)
            print(json.dumps({}))
        elif hook == "postToolUse":
            handle_post_tool_use(data)
            print(json.dumps({}))
        elif hook == "stop":
            handle_stop(data)
        elif hook == "subagentStop":
            handle_subagent_stop(data)
        else:
            print(json.dumps({}))
    except Exception:
        sys.stderr.write("[agent-retro-meter] " + traceback.format_exc())
        print(json.dumps({}))


if __name__ == "__main__":
    main()
