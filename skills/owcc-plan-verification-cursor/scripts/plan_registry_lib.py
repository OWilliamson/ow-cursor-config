"""Read/write Cursor composer.planRegistry in state.vscdb for plan-registry.py."""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

_SCRIPT_DIR = Path(__file__).resolve().parent
_VR_SCRIPTS = Path.home() / ".cursor" / "skills" / "owcc-plan-validation-report" / "scripts"
if not _VR_SCRIPTS.is_dir():
    _hub = _SCRIPT_DIR.parent.parent / "owcc-plan-validation-report" / "scripts"
    if _hub.is_dir():
        _VR_SCRIPTS = _hub
if str(_VR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_VR_SCRIPTS))

import plan_lib  # noqa: E402

REGISTRY_KEY = "composer.planRegistry"
HEADERS_KEY = "composer.composerHeaders"
WAIT_TIMEOUT_S = 30
WAIT_INTERVAL_S = 2
BUSY_RECENT_SECONDS = 120
PLAN_BUILD_PROMPT_MARKERS = (
    "Implement the plan as specified",
    "Do NOT edit the plan file itself",
)

EXIT_OK = 0
EXIT_INCOMPLETE_TODOS = 1
EXIT_BUSY_TIMEOUT = 3
EXIT_AMBIGUOUS_COMPOSER = 4
EXIT_COMPOSER_NOT_IN_HEADERS = 5
EXIT_PLAN_NOT_REGISTERED = 6
EXIT_CANNOT_DETECT_INVOKING = 7

COMPOSER_ID_ENV_KEYS = (
    "CURSOR_CONVERSATION_ID",
    "CURSOR_COMPOSER_ID",
    "COMPOSER_ID",
)
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
DEFAULT_RETRO_STATE_PATH = (
    Path.home() / ".cursor/hooks/agent-retro-meter/state.json"
)
DEFAULT_TRANSCRIPT_MAX_AGE_S = 3600
LAST_REASSIGN_MARKER_MAX_AGE_S = 7 * 86400


@dataclass
class ComposerCandidate:
    composer_id: str
    name: str
    unified_mode: str
    last_updated_at: int
    referenced_plans: list[dict[str, Any]]


@dataclass
class SyncResult:
    plan_path: Path
    plan_id: str
    composer_id: str
    created: bool
    actions: list[str] = field(default_factory=list)
    dry_run: bool = False


@dataclass
class ReassignResult:
    plan_path: Path
    plan_id: str
    composer_id: str
    actions: list[str] = field(default_factory=list)
    dry_run: bool = False
    previous_created_by: str | None = None
    previous_built_by: dict[str, list[str]] = field(default_factory=dict)
    resolved_via: str | None = None
    detected_invoking_composer_id: str | None = None


def default_vscdb_path() -> Path:
    candidates = [
        Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "state.vscdb",
        Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "state.vscdb",
    ]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.insert(
            0,
            Path(appdata) / "Cursor" / "User" / "globalStorage" / "state.vscdb",
        )
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def default_backup_dir() -> Path:
    return Path.home() / ".cursor/backups"


def normalize_plan_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def plan_id_from_path(plan_path: Path) -> str:
    name = plan_path.name
    if name.endswith(".plan.md"):
        return name[: -len(".plan.md")]
    if name.endswith(".md"):
        return name[: -len(".md")]
    return name


def uri_paths_match(stored_uri: dict[str, Any], plan_path: Path) -> bool:
    candidates: list[str] = []
    for key in ("fsPath", "path"):
        val = stored_uri.get(key)
        if isinstance(val, str) and val:
            candidates.append(val)
    ext = stored_uri.get("external")
    if isinstance(ext, str) and ext.startswith("file://"):
        parsed = urlparse(ext)
        candidates.append(unquote(parsed.path))
    if not candidates:
        return False
    target = str(plan_path)
    for c in candidates:
        try:
            if normalize_plan_path(c) == plan_path:
                return True
        except (OSError, ValueError):
            continue
        if c == target:
            return True
    return False


def make_file_uri(plan_path: Path) -> dict[str, Any]:
    fs = str(plan_path)
    return {
        "$mid": 1,
        "fsPath": fs,
        "external": f"file://{fs}",
        "path": fs,
        "scheme": "file",
    }


def _connect(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(str(db_path), timeout=5.0)


def _read_json_value(conn: sqlite3.Connection, key: str) -> Any:
    row = conn.execute("SELECT value FROM ItemTable WHERE key = ?", (key,)).fetchone()
    if not row:
        return None
    return json.loads(row[0])


def _write_json_value(conn: sqlite3.Connection, key: str, value: Any) -> None:
    payload = json.dumps(value, separators=(",", ":"))
    conn.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        (key, payload),
    )
    conn.commit()


def load_registry(db_path: Path | None = None) -> dict[str, Any]:
    path = db_path or default_vscdb_path()
    if not path.is_file():
        return {}
    conn = _connect(path)
    try:
        data = _read_json_value(conn, REGISTRY_KEY)
        return data if isinstance(data, dict) else {}
    finally:
        conn.close()


def save_registry(registry: dict[str, Any], db_path: Path | None = None) -> None:
    path = db_path or default_vscdb_path()
    conn = _connect(path)
    try:
        _write_json_value(conn, REGISTRY_KEY, registry)
    finally:
        conn.close()


def load_composer_headers(db_path: Path | None = None) -> dict[str, Any]:
    path = db_path or default_vscdb_path()
    if not path.is_file():
        return {}
    conn = _connect(path)
    try:
        data = _read_json_value(conn, HEADERS_KEY)
        return data if isinstance(data, dict) else {}
    finally:
        conn.close()


def save_composer_headers(headers: dict[str, Any], db_path: Path | None = None) -> None:
    path = db_path or default_vscdb_path()
    conn = _connect(path)
    try:
        _write_json_value(conn, HEADERS_KEY, headers)
    finally:
        conn.close()


def plan_ref_for_composer_header(plan_path: Path) -> dict[str, str]:
    plan_path = normalize_plan_path(plan_path)
    uri = f"file://{plan_path}"
    return {"type": "file", "uri": uri}


def _header_plan_ref_matches(ref: dict[str, Any], plan_path: Path) -> bool:
    if not isinstance(ref, dict) or ref.get("type") != "file":
        return False
    uri = ref.get("uri")
    if isinstance(uri, str):
        try:
            if normalize_plan_path(urlparse(uri).path if uri.startswith("file:") else uri) == plan_path:
                return True
        except (OSError, ValueError):
            pass
        return uri.endswith(plan_path.name)
    return False


def find_composer_in_headers(
    composer_id: str,
    db_path: Path | None = None,
) -> dict[str, Any] | None:
    headers = load_composer_headers(db_path)
    for c in headers.get("allComposers") or []:
        if isinstance(c, dict) and c.get("composerId") == composer_id:
            return c
    return None


def ensure_composer_references_plan_in_headers(
    composer_id: str,
    plan_path: Path,
    db_path: Path | None = None,
    *,
    bump_last_updated: bool = True,
) -> bool:
    """Add file plan ref to composer.composerHeaders; return True if changed."""
    plan_path = normalize_plan_path(plan_path)
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return False

    changed = False
    ref_entry = plan_ref_for_composer_header(plan_path)
    now_ms = int(time.time() * 1000)

    for c in composers:
        if not isinstance(c, dict) or c.get("composerId") != composer_id:
            continue
        refs = c.get("referencedPlans")
        if not isinstance(refs, list):
            refs = []
            c["referencedPlans"] = refs
        if not any(_header_plan_ref_matches(r, plan_path) for r in refs if isinstance(r, dict)):
            refs.append(ref_entry)
            changed = True
        if bump_last_updated:
            c["lastUpdatedAt"] = now_ms
            changed = True
        break
    else:
        raise SystemExit(
            EXIT_COMPOSER_NOT_IN_HEADERS,
            f"Composer {composer_id} not found in {HEADERS_KEY}.allComposers.\n"
            "Open that Agent chat once in Cursor so it appears in headers, then retry.",
        )

    if changed:
        save_composer_headers(headers, db_path)
    return changed


def backup_db(db_path: Path | None = None) -> Path:
    src = db_path or default_vscdb_path()
    if not src.is_file():
        raise FileNotFoundError(f"state database not found: {src}")
    dest_dir = default_backup_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = dest_dir / f"state.vscdb.{stamp}"
    shutil.copy2(src, dest)
    return dest


def find_entry(registry: dict[str, Any], plan_path: Path) -> tuple[str | None, dict[str, Any] | None]:
    plan_path = normalize_plan_path(plan_path)
    pid = plan_id_from_path(plan_path)
    if pid in registry and isinstance(registry[pid], dict):
        entry = registry[pid]
        if uri_paths_match(entry.get("uri") or {}, plan_path):
            return pid, entry
    for key, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        if uri_paths_match(entry.get("uri") or {}, plan_path):
            return key, entry
    return None, None


def _composer_references_plan(composer: dict[str, Any], plan_path: Path) -> bool:
    refs = composer.get("referencedPlans") or []
    if not isinstance(refs, list):
        return False
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        uri = ref.get("uri")
        if isinstance(uri, str):
            try:
                if normalize_plan_path(urlparse(uri).path if uri.startswith("file:") else uri) == plan_path:
                    return True
            except (OSError, ValueError):
                if uri == str(plan_path) or uri.endswith(plan_path.name):
                    return True
        elif isinstance(uri, dict) and uri_paths_match(uri, plan_path):
            return True
    return False


def list_composer_candidates(
    plan_path: Path,
    db_path: Path | None = None,
) -> list[ComposerCandidate]:
    plan_path = normalize_plan_path(plan_path)
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers") or []
    out: list[ComposerCandidate] = []
    if not isinstance(composers, list):
        return out
    for c in composers:
        if not isinstance(c, dict):
            continue
        cid = c.get("composerId")
        if not cid or not _composer_references_plan(c, plan_path):
            continue
        out.append(
            ComposerCandidate(
                composer_id=str(cid),
                name=str(c.get("name") or ""),
                unified_mode=str(c.get("unifiedMode") or ""),
                last_updated_at=int(c.get("lastUpdatedAt") or 0),
                referenced_plans=list(c.get("referencedPlans") or []),
            )
        )
    return out


def is_composer_uuid(value: str) -> bool:
    return bool(_UUID_RE.match(value.strip()))


def project_slug_for_workspace(workspace_root: Path) -> str:
    """
    Cursor agent-transcripts folder name under ~/.cursor/projects/.

    Linux workspaces under /home/<user>/… use slug home-<user>-… (path relative to
    /home, not Path.home()). Using only Path.home() drops the username segment and
    breaks transcript-based invoking-chat detection.
    """
    root = normalize_plan_path(workspace_root)
    bases: list[Path] = []
    root_s = str(root)
    if root_s.startswith("/home/"):
        bases.append(Path("/home"))
    home = Path.home().resolve()
    if home not in bases:
        bases.append(home)
    for base in bases:
        try:
            rel = root.relative_to(base)
            return "home-" + rel.as_posix().replace("/", "-")
        except ValueError:
            continue
    return root.name.replace("_", "-")


def agent_transcripts_base_dir(workspace_root: Path) -> Path | None:
    """Directory containing per-composer transcript folders, or None."""
    root = normalize_plan_path(workspace_root)
    projects = Path.home() / ".cursor/projects"
    primary = projects / project_slug_for_workspace(root)
    candidate = primary / "agent-transcripts"
    if candidate.is_dir():
        return candidate
    # Fallback: Cursor slug can differ slightly; match workspace directory name suffix.
    suffix = root.name
    if projects.is_dir():
        for child in sorted(projects.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if not child.is_dir():
                continue
            if suffix in child.name and (child / "agent-transcripts").is_dir():
                return child / "agent-transcripts"
    return None


def workspace_root_for_plan(plan_path: Path) -> Path:
    """
    Repo/workspace root for agent-transcript discovery.

    Plans live at <workspace>/.cursor/plans/*.plan.md — not under the plans dir itself.
    """
    p = normalize_plan_path(plan_path)
    if p.parent.name == "plans" and p.parent.parent.name == ".cursor":
        return p.parent.parent.parent
    return p.parent


def composer_id_from_env() -> str | None:
    for key in COMPOSER_ID_ENV_KEYS:
        raw = os.environ.get(key, "").strip()
        if raw and is_composer_uuid(raw):
            return raw
    return None


def _iter_retro_generations(
    retro_state_path: Path | None = None,
) -> list[tuple[int, str, str]]:
    """Return [(submitted_ms, conversation_id, prompt), ...] from agent-retro-meter."""
    path = retro_state_path or DEFAULT_RETRO_STATE_PATH
    if not path.is_file():
        return []
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    generations = state.get("generations")
    if not isinstance(generations, dict):
        return []
    out: list[tuple[int, str, str]] = []
    for gen in generations.values():
        if not isinstance(gen, dict):
            continue
        conv = gen.get("conversation_id")
        if not conv or not is_composer_uuid(str(conv)):
            continue
        try:
            submitted = int(gen.get("submitted_ms") or 0)
        except (TypeError, ValueError):
            submitted = 0
        out.append((submitted, str(conv), str(gen.get("prompt") or "")))
    return out


def composer_id_from_retro_recent_plan_operation(
    plan_path: Path | None = None,
    *,
    retro_state_path: Path | None = None,
    max_age_s: int = 180,
) -> str | None:
    """
    Composer for the latest user message that @'d this plan or invoked plan-change-composer.

    Avoids picking another tab that only has a newer transcript mtime from Plan UI Build.
    """
    plan_basename = plan_path.name if plan_path is not None else None
    plan_stem = plan_basename.removesuffix(".plan.md") if plan_basename else None
    cutoff = int(time.time() * 1000) - max_age_s * 1000
    best_ms = -1
    best_conv: str | None = None
    for submitted, conv, prompt in _iter_retro_generations(retro_state_path):
        if submitted < cutoff:
            continue
        if plan_basename:
            # Specific plan: require that plan in the prompt (not any plan-change-composer).
            if plan_basename not in prompt and (not plan_stem or plan_stem not in prompt):
                continue
        elif "plan-change-composer" not in prompt:
            continue
        if submitted >= best_ms:
            best_ms = submitted
            best_conv = conv
    return best_conv


def composer_id_from_retro_meter(
    *,
    retro_state_path: Path | None = None,
    allowed_composer_ids: set[str] | None = None,
) -> str | None:
    """
    Composer for the most recent user generation (current Agent turn).

    When allowed_composer_ids is set, only considers those conversation_ids
    (excludes ghost composers absent from composer.composerHeaders).
    """
    best_ms = -1
    best_conv: str | None = None
    for submitted, conv, _prompt in _iter_retro_generations(retro_state_path):
        if allowed_composer_ids is not None and conv not in allowed_composer_ids:
            continue
        if submitted >= best_ms:
            best_ms = submitted
            best_conv = conv
    return best_conv


def composer_id_from_recent_transcript(
    workspace_root: Path | None = None,
    *,
    max_age_s: int = DEFAULT_TRANSCRIPT_MAX_AGE_S,
) -> str | None:
    """Composer UUID from the newest agent transcript jsonl in this workspace."""
    root = normalize_plan_path(workspace_root or Path.cwd())
    base = agent_transcripts_base_dir(root)
    if base is None:
        return None
    now = time.time()
    best: tuple[float, str] | None = None
    for child in base.iterdir():
        if not child.is_dir():
            continue
        cid = child.name
        if not is_composer_uuid(cid):
            continue
        transcript = child / f"{cid}.jsonl"
        if not transcript.is_file():
            continue
        age_s = now - transcript.stat().st_mtime
        if age_s > max_age_s:
            continue
        mtime = transcript.stat().st_mtime
        if best is None or mtime > best[0]:
            best = (mtime, cid)
    return best[1] if best else None


def _header_composer_ids(db_path: Path | None = None) -> set[str]:
    headers = load_composer_headers(db_path)
    out: set[str] = set()
    for c in headers.get("allComposers") or []:
        if isinstance(c, dict) and c.get("composerId"):
            out.add(str(c["composerId"]))
    return out


def detect_invoking_composer(
    *,
    workspace_root: Path | None = None,
    retro_state_path: Path | None = None,
    plan_path: Path | None = None,
    db_path: Path | None = None,
) -> tuple[str | None, str]:
    """
    Authoritative invoking composer only (correct or unknown).

    Returns (composer_id, source_label). source_label is 'none' when not found.

    Sources (no retro-meter, transcript mtime, or header heuristics):
      1. CURSOR_* / COMPOSER_ID environment
      2. last-reassign.json for this plan (written by plan-change-composer-invoke hook)

    Manual reassign without --composer must use one of these or exit 7.
    """
    del workspace_root, retro_state_path  # not used; kept for call-site compatibility

    from_env = composer_id_from_env()
    if from_env:
        return from_env, "env"

    if plan_path is None:
        return None, "none"

    in_headers = _header_composer_ids(db_path)
    allowed: set[str] | None = in_headers if in_headers else None

    from_marker = composer_id_from_last_reassign_marker(plan_path)
    if from_marker and (allowed is None or from_marker in allowed):
        return from_marker, "last-reassign-marker"

    return None, "none"


_CANNOT_DETECT_INVOKING_MSG = """\
Cannot detect target Agent chat (no heuristic fallbacks).

Use one of:
  • @plan-change-composer + @plan in the target Agent tab (hook writes last-reassign.json)
  • --composer <uuid> from ~/.cursor/projects/.../agent-transcripts/<uuid>/
  • CURSOR_CONVERSATION_ID / CURSOR_COMPOSER_ID / COMPOSER_ID in the shell environment

Then Developer: Reload Window, close/reopen the .plan.md tab, Build on the plan file.
"""


def require_invoking_composer(
    plan_path: Path,
    db_path: Path | None = None,
) -> tuple[str, str]:
    """Resolve invoking composer or exit EXIT_CANNOT_DETECT_INVOKING."""
    invoking, source = detect_invoking_composer(plan_path=plan_path, db_path=db_path)
    if not invoking:
        raise SystemExit(EXIT_CANNOT_DETECT_INVOKING, _CANNOT_DETECT_INVOKING_MSG)
    require_composer_in_headers(invoking, db_path)
    return invoking, source


def require_composer_in_headers(composer_id: str, db_path: Path | None = None) -> None:
    if find_composer_in_headers(composer_id, db_path) is None:
        raise SystemExit(
            EXIT_COMPOSER_NOT_IN_HEADERS,
            f"Composer {composer_id} is not in {HEADERS_KEY}.allComposers.\n"
            "Open that Agent chat once in the sidebar, then retry.",
        )


def _promote_registry_owner(
    entry: dict[str, Any],
    composer_id: str,
    *,
    exclusive_referenced_by: bool = True,
) -> list[str]:
    """Make composer_id registry owner: createdBy + referencedBy."""
    actions: list[str] = []
    prev_created = entry.get("createdBy")
    if prev_created != composer_id:
        entry["createdBy"] = composer_id
        actions.append("set createdBy (registry owner / adoptPlan parity)")

    refs = entry.get("referencedBy")
    if not isinstance(refs, list):
        refs = []
    refs = [str(x) for x in refs if x]

    if exclusive_referenced_by:
        removed = [x for x in refs if x != composer_id]
        if refs != [composer_id]:
            entry["referencedBy"] = [composer_id]
            actions.append(
                f"exclusive referencedBy (dropped {len(removed)} other composer(s))"
            )
        edited = entry.setdefault("editedBy", [])
        if not isinstance(edited, list):
            edited = []
            entry["editedBy"] = edited
        for other in removed:
            if _ensure_list_unique_append(edited, other):
                actions.append(f"archived {other} in editedBy")
    else:
        if composer_id in refs:
            refs = [composer_id] + [x for x in refs if x != composer_id]
        else:
            refs = [composer_id] + refs
        if refs != entry.get("referencedBy"):
            entry["referencedBy"] = refs
            actions.append("moved composer to front of referencedBy")
    return actions


def demote_composer_header(
    composer_id: str,
    db_path: Path | None = None,
    *,
    last_updated_at: int = 1,
    dry_run: bool = False,
) -> bool:
    """Lower header lastUpdatedAt so Plan UI does not prefer this tab for Build."""
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return False
    changed = False
    for c in composers:
        if isinstance(c, dict) and c.get("composerId") == composer_id:
            if c.get("lastUpdatedAt") != last_updated_at:
                c["lastUpdatedAt"] = last_updated_at
                changed = True
            break
    if changed and not dry_run:
        save_composer_headers(headers, db_path)
    return changed


def strip_plan_from_other_composer_headers(
    plan_path: Path,
    keep_composer_id: str,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
    demote_stripped: bool = True,
) -> list[str]:
    """
    Remove this plan from referencedPlans on every composer except keep_composer_id.

    Stops other Agent tabs from satisfying getPlanForComposer / Plan UI Build locally
    when registry.createdBy points elsewhere.
    """
    plan_path = normalize_plan_path(plan_path)
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return []

    stripped: list[str] = []
    changed = False
    for c in composers:
        if not isinstance(c, dict):
            continue
        cid = c.get("composerId")
        if not cid or cid == keep_composer_id:
            continue
        refs = c.get("referencedPlans")
        if not isinstance(refs, list):
            continue
        new_refs = [
            r
            for r in refs
            if not (isinstance(r, dict) and _header_plan_ref_matches(r, plan_path))
        ]
        if len(new_refs) != len(refs):
            c["referencedPlans"] = new_refs
            stripped.append(str(cid))
            changed = True
            if demote_stripped:
                c["lastUpdatedAt"] = 1

    if changed and not dry_run:
        save_composer_headers(headers, db_path)
    return stripped


def is_plan_build_prompt(prompt: str) -> bool:
    return any(marker in prompt for marker in PLAN_BUILD_PROMPT_MARKERS)


PLAN_CHANGE_COMPOSER_MARKERS = (
    "plan-change-composer",
    "/plan-change-composer",
)
_PLAN_PATH_IN_TEXT_RE = re.compile(
    r"(?:/[\w./~+-]+|[\w./~+-]+/)?[\w.-]+\.plan\.md",
    re.IGNORECASE,
)
LAST_REASSIGN_MARKER_PATH = (
    Path.home() / ".cursor/plan-change-composer/last-reassign.json"
)


def is_plan_change_composer_prompt(prompt: str) -> bool:
    text = prompt.lower()
    return any(marker in text for marker in PLAN_CHANGE_COMPOSER_MARKERS)


def plan_paths_from_prompt_text(prompt: str) -> list[Path]:
    """Absolute or basename paths to .plan.md embedded in user text."""
    seen: set[str] = set()
    out: list[Path] = []
    for match in _PLAN_PATH_IN_TEXT_RE.finditer(prompt):
        raw = match.group(0).strip()
        try:
            path = normalize_plan_path(raw)
        except (OSError, ValueError):
            continue
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out


def _plan_paths_from_attachment_value(value: Any, seen: set[str], out: list[Path]) -> None:
    if isinstance(value, str):
        if ".plan.md" not in value.lower():
            return
        for match in _PLAN_PATH_IN_TEXT_RE.finditer(value):
            try:
                path = normalize_plan_path(match.group(0))
            except (OSError, ValueError):
                continue
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            out.append(path)
        return
    if isinstance(value, dict):
        for key in ("path", "fsPath", "filePath", "uri", "external", "name"):
            if key in value:
                _plan_paths_from_attachment_value(value[key], seen, out)
        for nested in value.values():
            if isinstance(nested, (dict, list, str)):
                _plan_paths_from_attachment_value(nested, seen, out)
        return
    if isinstance(value, list):
        for item in value:
            _plan_paths_from_attachment_value(item, seen, out)


def plan_paths_from_attachments(attachments: Any) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    _plan_paths_from_attachment_value(attachments, seen, out)
    return out


def plan_paths_from_hook_data(hook_data: dict[str, Any]) -> list[Path]:
    prompt = str(hook_data.get("prompt") or "")
    seen = {str(p) for p in plan_paths_from_prompt_text(prompt)}
    out = list(plan_paths_from_prompt_text(prompt))
    for path in plan_paths_from_attachments(hook_data.get("attachments")):
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out


def read_last_reassign_marker(
    plan_path: Path | None = None,
) -> dict[str, Any] | None:
    path = LAST_REASSIGN_MARKER_PATH
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    if plan_path is not None:
        try:
            marked = normalize_plan_path(Path(str(data.get("plan_path") or "")))
            if marked != normalize_plan_path(plan_path):
                return None
        except (OSError, ValueError):
            return None
    return data


def composer_id_from_last_reassign_marker(
    plan_path: Path,
    *,
    max_age_s: int = LAST_REASSIGN_MARKER_MAX_AGE_S,
) -> str | None:
    data = read_last_reassign_marker(plan_path)
    if not data:
        return None
    try:
        age_ms = int(time.time() * 1000) - int(data.get("reassigned_at_ms") or 0)
    except (TypeError, ValueError):
        return None
    if age_ms > max_age_s * 1000:
        return None
    cid = data.get("composer_id")
    if cid and is_composer_uuid(str(cid)):
        return str(cid)
    return None


def write_last_reassign_marker(
    plan_path: Path,
    composer_id: str,
    *,
    actions: list[str] | None = None,
) -> None:
    LAST_REASSIGN_MARKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "plan_path": str(normalize_plan_path(plan_path)),
        "composer_id": composer_id,
        "reassigned_at_ms": int(time.time() * 1000),
        "actions": actions or [],
        "reload_window_required": True,
    }
    LAST_REASSIGN_MARKER_PATH.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def reassign_from_hook(
    conversation_id: str,
    hook_data: dict[str, Any],
    *,
    db_path: Path | None = None,
) -> list[ReassignResult]:
    """
    Exclusive reassign for each .plan.md in the hook prompt/attachments.

    Uses hook conversation_id (authoritative) instead of transcript heuristics.
    """
    plan_paths = plan_paths_from_hook_data(hook_data)
    if not plan_paths:
        return []
    results: list[ReassignResult] = []
    for plan_path in plan_paths:
        result = reassign_plan_host(
            plan_path,
            conversation_id,
            db_path=db_path,
            prefer_invoking=False,
            exclusive_host=True,
        )
        write_last_reassign_marker(plan_path, conversation_id, actions=result.actions)
        results.append(result)
    return results


def _misrouted_entry(
    reg_id: str,
    entry: dict[str, Any],
    plan_path: Path,
    composer_id: str,
    db_path: Path | None,
) -> dict[str, Any]:
    owner = str(entry.get("createdBy") or "")
    owner_header = find_composer_in_headers(owner, db_path) if owner else None
    return {
        "plan_id": reg_id,
        "plan_path": plan_path,
        "owner_composer_id": owner,
        "owner_name": str((owner_header or {}).get("name") or owner),
        "offender_composer_id": composer_id,
    }


def _plan_path_from_registry_entry(entry: dict[str, Any]) -> Path | None:
    uri = entry.get("uri")
    if not isinstance(uri, dict):
        return None
    for key in ("fsPath", "path"):
        val = uri.get(key)
        if isinstance(val, str) and val:
            try:
                return normalize_plan_path(val)
            except (OSError, ValueError):
                pass
    ext = uri.get("external")
    if isinstance(ext, str) and ext.startswith("file://"):
        try:
            return normalize_plan_path(unquote(urlparse(ext).path))
        except (OSError, ValueError):
            pass
    return None


def plan_file_exists(plan_path: Path) -> bool:
    """True when the registry URI points at a .plan.md that still exists on disk."""
    try:
        return normalize_plan_path(plan_path).is_file()
    except (OSError, ValueError):
        return False


def strip_plan_from_all_composer_headers(
    plan_path: Path,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """Remove plan from referencedPlans on every composer (orphan / prune cleanup)."""
    plan_path = normalize_plan_path(plan_path)
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return []

    stripped: list[str] = []
    changed = False
    for c in composers:
        if not isinstance(c, dict):
            continue
        cid = c.get("composerId")
        if not cid:
            continue
        refs = c.get("referencedPlans")
        if not isinstance(refs, list):
            continue
        new_refs = [
            r
            for r in refs
            if not (isinstance(r, dict) and _header_plan_ref_matches(r, plan_path))
        ]
        if len(new_refs) != len(refs):
            c["referencedPlans"] = new_refs
            stripped.append(str(cid))
            changed = True

    if changed and not dry_run:
        save_composer_headers(headers, db_path)
    return stripped


def prune_orphan_registry_entries(
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
    skip_backup: bool = False,
) -> list[str]:
    """
    Drop registry rows whose .plan.md file no longer exists; strip header refs.

    Completed hub plans removed from disk leave zombie rows that block unrelated
    native Builds via referencedBy / header creep.
    """
    registry = load_registry(db_path)
    removed: list[str] = []
    changed = False

    for reg_id, entry in list(registry.items()):
        if not isinstance(entry, dict):
            continue
        plan_path = _plan_path_from_registry_entry(entry)
        if plan_path is None or plan_file_exists(plan_path):
            continue
        removed.append(str(reg_id))
        if dry_run:
            continue
        del registry[reg_id]
        changed = True
        strip_plan_from_all_composer_headers(plan_path, db_path, dry_run=False)

    if changed and not dry_run:
        if not skip_backup:
            backup_db(db_path)
        save_registry(registry, db_path)
    return removed


def evict_composer_registry_participation_if_not_owner(
    composer_id: str,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
    skip_backup: bool = False,
) -> list[str]:
    """
    Remove composer_id from referencedBy / builtBy on plans it does not own.

    Header eviction alone leaves registry participation that misrouted_builds uses.
    """
    registry = load_registry(db_path)
    touched: list[str] = []
    changed = False

    for reg_id, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        owner = entry.get("createdBy")
        if not owner or str(owner) == composer_id:
            continue
        plan_path = _plan_path_from_registry_entry(entry)
        entry_changed = False

        ref_by = entry.get("referencedBy")
        if isinstance(ref_by, list):
            new_ref = [x for x in ref_by if str(x) != composer_id]
            if len(new_ref) != len(ref_by):
                entry["referencedBy"] = new_ref
                entry_changed = True

        built_by = entry.get("builtBy")
        if isinstance(built_by, dict) and composer_id in built_by:
            built_by = dict(built_by)
            del built_by[composer_id]
            entry["builtBy"] = built_by
            entry_changed = True

        if entry_changed:
            touched.append(
                plan_path.name if plan_path is not None else str(reg_id)
            )
            if not dry_run:
                registry[reg_id] = entry
                changed = True

    if changed and not dry_run:
        if not skip_backup:
            backup_db(db_path)
        save_registry(registry, db_path)
    return touched


def _registry_entries_for_header_plan_ref(
    registry: dict[str, Any],
    ref: dict[str, Any],
    plan_path_hint: Path | None = None,
) -> list[tuple[str, dict[str, Any], Path]]:
    """Match a header referencedPlans entry to registry rows."""
    matches: list[tuple[str, dict[str, Any], Path]] = []
    if not isinstance(ref, dict) or ref.get("type") != "file":
        return matches
    uri = ref.get("uri")
    if not isinstance(uri, str):
        return matches
    try:
        path = normalize_plan_path(
            urlparse(uri).path if uri.startswith("file:") else uri
        )
    except (OSError, ValueError):
        return matches
    for key, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        if uri_paths_match(entry.get("uri") or {}, path):
            matches.append((key, entry, path))
        elif plan_path_hint and path == plan_path_hint:
            matches.append((key, entry, path))
    return matches


def misrouted_plan_builds_for_composer(
    composer_id: str,
    prompt: str,
    db_path: Path | None = None,
    *,
    hook_data: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Plan UI Build submitted in composer_id when registry.createdBy is another tab.

    Only considers plans tied to this Build (hook attachments/prompt) or still
    listed on this tab's referencedPlans after eviction. Ignores missing .plan.md
    files and never scans the full registry when the Build payload names no plan.
    """
    if not is_plan_build_prompt(prompt):
        return []
    registry = load_registry(db_path)
    out: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    hook_payload = hook_data if hook_data is not None else {"prompt": prompt}

    def _append_if_misrouted(
        reg_id: str,
        entry: dict[str, Any],
        plan_path: Path,
    ) -> None:
        if not plan_file_exists(plan_path):
            return
        owner = entry.get("createdBy")
        if not owner or str(owner) == composer_id:
            return
        path_key = str(plan_path)
        if path_key in seen_paths:
            return
        seen_paths.add(path_key)
        out.append(
            _misrouted_entry(reg_id, entry, plan_path, composer_id, db_path)
        )

    for plan_path in plan_paths_from_hook_data(hook_payload):
        _reg_id, entry = find_entry(registry, plan_path)
        if entry is None:
            continue
        _append_if_misrouted(
            _reg_id or plan_id_from_path(plan_path), entry, plan_path
        )

    header = find_composer_in_headers(composer_id, db_path)
    if header is not None:
        for ref in header.get("referencedPlans") or []:
            if not isinstance(ref, dict):
                continue
            for reg_id, entry, plan_path in _registry_entries_for_header_plan_ref(
                registry, ref
            ):
                _append_if_misrouted(reg_id, entry, plan_path)

    if not out:
        scoped_paths: set[str] = set()
        for plan_path in plan_paths_from_hook_data(hook_payload):
            scoped_paths.add(str(plan_path))
        if header is not None:
            for ref in header.get("referencedPlans") or []:
                if not isinstance(ref, dict):
                    continue
                for _rid, _entry, plan_path in _registry_entries_for_header_plan_ref(
                    registry, ref
                ):
                    if plan_file_exists(plan_path):
                        scoped_paths.add(str(plan_path))

        if not scoped_paths:
            return out

        for reg_id, entry in registry.items():
            if not isinstance(entry, dict):
                continue
            plan_path = _plan_path_from_registry_entry(entry)
            if plan_path is None or str(plan_path) not in scoped_paths:
                continue
            if not plan_file_exists(plan_path):
                continue
            owner = entry.get("createdBy")
            if not owner or str(owner) == composer_id:
                continue
            ref_by = [str(x) for x in (entry.get("referencedBy") or [])]
            built_by = entry.get("builtBy") or {}
            if composer_id not in ref_by and composer_id not in built_by:
                continue
            path_key = str(plan_path)
            if path_key in seen_paths:
                continue
            seen_paths.add(path_key)
            out.append(
                _misrouted_entry(
                    str(reg_id), entry, plan_path, composer_id, db_path
                )
            )

    return out


def prepare_composer_for_native_plan_build(
    composer_id: str,
    hook_data: dict[str, Any],
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """
    Hygiene before Plan UI Build: prune deleted plans, evict foreign ties on this tab.
    """
    actions: list[str] = []
    pruned = prune_orphan_registry_entries(db_path, dry_run=dry_run)
    if pruned:
        actions.append("pruned orphan registry: " + ", ".join(pruned))
    evicted_headers = evict_registry_plans_from_composer_if_not_owner(
        composer_id, db_path, dry_run=dry_run
    )
    if evicted_headers:
        actions.append(
            "evicted foreign header refs: " + ", ".join(evicted_headers)
        )
    evicted_registry = evict_composer_registry_participation_if_not_owner(
        composer_id, db_path, dry_run=dry_run
    )
    if evicted_registry:
        actions.append(
            "evicted foreign registry participation: "
            + ", ".join(evicted_registry)
        )
    return actions


def claim_native_build_for_composer(
    composer_id: str,
    plan_paths: list[Path],
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """
    Point registry + headers at composer_id for plans being built natively here.

    Replaces mandatory @plan-change-composer before first Build when the user
    pressed Build from this Agent tab.
    """
    actions: list[str] = []
    for plan_path in plan_paths:
        if not plan_file_exists(plan_path):
            continue
        registry = load_registry(db_path)
        _reg_id, entry = find_entry(registry, plan_path)
        if entry is None:
            continue
        owner = str(entry.get("createdBy") or "")
        if owner == composer_id:
            continue
        if dry_run:
            actions.append(f"would claim native Build host for {plan_path.name}")
            continue
        result = reassign_plan_host(
            plan_path,
            composer_id,
            db_path=db_path,
            skip_wait=True,
            exclusive_host=True,
        )
        actions.append(
            f"claimed native Build host for {plan_path.name} "
            f"(was {result.previous_created_by or 'unset'})"
        )
    return actions


def heal_plan_build_for_owner_composer(
    composer_id: str,
    hook_data: dict[str, Any],
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """
    Before an allowed Plan UI Build: evict foreign plans from this tab and
    reinforce exclusive headers for every owned plan in the Build payload.
    """
    actions: list[str] = []
    evicted = evict_registry_plans_from_composer_if_not_owner(
        composer_id, db_path, dry_run=dry_run
    )
    if evicted:
        actions.append("evicted non-owner refs: " + ", ".join(evicted))

    registry = load_registry(db_path)
    seen: set[str] = set()
    for plan_path in plan_paths_from_hook_data(hook_data):
        _reg_id, entry = find_entry(registry, plan_path)
        if entry is None or str(entry.get("createdBy") or "") != composer_id:
            continue
        key = str(plan_path)
        if key in seen:
            continue
        seen.add(key)
        if dry_run:
            actions.append(f"would reinforce exclusive host for {plan_path.name}")
            continue
        actions.extend(
            reinforce_exclusive_plan_host(plan_path, composer_id, db_path)
        )

    header = find_composer_in_headers(composer_id, db_path)
    if header is not None:
        for ref in header.get("referencedPlans") or []:
            if not isinstance(ref, dict):
                continue
            for _rid, entry, plan_path in _registry_entries_for_header_plan_ref(
                registry, ref
            ):
                if str(entry.get("createdBy") or "") != composer_id:
                    continue
                key = str(plan_path)
                if key in seen:
                    continue
                seen.add(key)
                if dry_run:
                    actions.append(
                        f"would reinforce exclusive host for {plan_path.name}"
                    )
                    continue
                actions.extend(
                    reinforce_exclusive_plan_host(
                        plan_path, composer_id, db_path
                    )
                )
    return actions


def evict_registry_plans_from_composer_if_not_owner(
    composer_id: str,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """
    On any user message in a tab: drop plan refs whose registry.createdBy is elsewhere.

    Stops stale tabs from keeping the Plan UI Build button after reassign.
    """
    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return []
    registry = load_registry(db_path)
    target: dict[str, Any] | None = None
    for c in composers:
        if isinstance(c, dict) and c.get("composerId") == composer_id:
            target = c
            break
    if target is None:
        return []

    refs = target.get("referencedPlans")
    if not isinstance(refs, list):
        return []

    evicted_names: list[str] = []
    new_refs: list[dict[str, Any]] = []
    changed = False
    for ref in refs:
        if not isinstance(ref, dict):
            new_refs.append(ref)
            continue
        drop = False
        for _rid, entry, plan_path in _registry_entries_for_header_plan_ref(
            registry, ref
        ):
            if not plan_file_exists(plan_path):
                drop = True
                evicted_names.append(plan_path.name)
                break
            owner = entry.get("createdBy")
            if owner and str(owner) != composer_id:
                drop = True
                evicted_names.append(plan_path.name)
                break
        if drop:
            changed = True
        else:
            new_refs.append(ref)

    if not changed:
        return evicted_names

    target["referencedPlans"] = new_refs
    target["lastUpdatedAt"] = 1
    if not dry_run:
        save_composer_headers(headers, db_path)
    return evicted_names


def reinforce_exclusive_plan_host(
    plan_path: Path,
    owner_composer_id: str,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> list[str]:
    """
    Headers-only: strip plan from other composers, demote them, bump owner lastUpdatedAt.
    Safe to call from hooks immediately before Plan UI Build.
    """
    actions: list[str] = []
    stripped = strip_plan_from_other_composer_headers(
        plan_path,
        owner_composer_id,
        db_path,
        dry_run=dry_run,
        demote_stripped=True,
    )
    if stripped:
        actions.append(
            "stripped referencedPlans from: " + ", ".join(stripped)
        )
    if not dry_run:
        if find_composer_in_headers(owner_composer_id, db_path) is not None:
            ensure_composer_references_plan_in_headers(
                owner_composer_id, plan_path, db_path, bump_last_updated=False
            )
            bump_target_header_above_others(plan_path, owner_composer_id, db_path)
            actions.append("owner header supremacy lastUpdatedAt")
        else:
            actions.append(
                f"owner {owner_composer_id} not in headers (open that chat once)"
            )
    return actions


def bump_target_header_above_others(
    plan_path: Path,
    composer_id: str,
    db_path: Path | None = None,
    *,
    dry_run: bool = False,
) -> int:
    """Set target lastUpdatedAt strictly above every composer that still references the plan."""
    plan_path = normalize_plan_path(plan_path)
    candidates = list_composer_candidates(plan_path, db_path)
    max_ts = max((c.last_updated_at for c in candidates), default=0)
    target_ms = max(int(time.time() * 1000), max_ts + 1)

    headers = load_composer_headers(db_path)
    composers = headers.get("allComposers")
    if not isinstance(composers, list):
        return target_ms

    changed = False
    for c in composers:
        if isinstance(c, dict) and c.get("composerId") == composer_id:
            if c.get("lastUpdatedAt") != target_ms:
                c["lastUpdatedAt"] = target_ms
                changed = True
            break

    if changed and not dry_run:
        save_composer_headers(headers, db_path)
    return target_ms


def other_composers_with_plan_in_headers(
    plan_path: Path,
    except_composer_id: str,
    db_path: Path | None = None,
) -> list[str]:
    """Composer ids that still have this plan in composerHeaders.referencedPlans."""
    plan_path = normalize_plan_path(plan_path)
    return [
        c.composer_id
        for c in list_composer_candidates(plan_path, db_path)
        if c.composer_id != except_composer_id
    ]


def resolve_composer_for_plan(
    plan_path: Path,
    composer_id: str | None = None,
    db_path: Path | None = None,
    *,
    prefer_invoking: bool = True,
    authoritative_only: bool = False,
    workspace_root: Path | None = None,
) -> tuple[str, list[ComposerCandidate], str]:
    """
    Resolve target composer for reassign.

    Returns (composer_id, candidates, resolved_via).
    resolved_via: explicit | invoking:<source> | header_max_lastUpdatedAt (legacy flag only)

    authoritative_only: for plan-change-composer — env/marker or exit 7, no header guess.
    """
    plan_path = normalize_plan_path(plan_path)
    candidates = list_composer_candidates(plan_path, db_path)

    if composer_id:
        require_composer_in_headers(composer_id, db_path)
        return composer_id, candidates, "explicit"

    ws_root = workspace_root or workspace_root_for_plan(plan_path)
    if prefer_invoking:
        invoking, source = detect_invoking_composer(
            workspace_root=ws_root,
            plan_path=plan_path,
            db_path=db_path,
        )
        if invoking:
            require_composer_in_headers(invoking, db_path)
            return invoking, candidates, f"invoking:{source}"
        if authoritative_only:
            raise SystemExit(EXIT_CANNOT_DETECT_INVOKING, _CANNOT_DETECT_INVOKING_MSG)

    if not candidates:
        registry = load_registry(db_path)
        _, entry = find_entry(registry, plan_path)
        if entry is None:
            raise SystemExit(
                EXIT_PLAN_NOT_REGISTERED,
                f"No registry row for plan: {plan_path}\n"
                "Register by @-mentioning the plan in Agent chat first.",
            )
        raise SystemExit(
            EXIT_COMPOSER_NOT_IN_HEADERS,
            f"No composer references this plan in {HEADERS_KEY}.\n"
            "Open the target Agent chat, @-mention the plan, or pass --composer <uuid>.",
        )

    max_ts = max(c.last_updated_at for c in candidates)
    top = [c for c in candidates if c.last_updated_at == max_ts]
    if len(top) > 1:
        lines = [
            "Ambiguous composer for this plan (multiple chats with same lastUpdatedAt):",
            "Could not detect invoking chat; pass --composer <uuid> from this Agent session.",
            "",
        ]
        for c in top:
            lines.append(
                f"  {c.composer_id}  {c.name!r}  mode={c.unified_mode}  updated={c.last_updated_at}"
            )
        lines.append("")
        lines.append("Re-run with: --composer <uuid>")
        raise SystemExit(EXIT_AMBIGUOUS_COMPOSER, "\n".join(lines))

    import sys

    print(
        "warning: could not detect invoking composer; using newest header lastUpdatedAt. "
        "Pass --composer <this-chat-uuid> to force the current Agent chat.",
        file=sys.stderr,
    )
    return top[0].composer_id, candidates, "header_max_lastUpdatedAt"


def incomplete_todo_ids(plan_path: Path) -> list[str]:
    plan = plan_lib.read_plan(plan_path)
    return [
        t.id
        for t in plan.todos
        if t.status not in ("completed", "cancelled")
    ]


def _composer_header_recently_touched(
    composer: dict[str, Any],
    *,
    now_ms: int | None = None,
) -> bool:
    updated = int(composer.get("lastUpdatedAt") or 0)
    if not updated:
        return False
    now = now_ms if now_ms is not None else int(time.time() * 1000)
    return (now - updated) < BUSY_RECENT_SECONDS * 1000


def composer_has_recent_plan_build_turn(
    composer_id: str,
    *,
    retro_state_path: Path | None = None,
    max_age_s: int = BUSY_RECENT_SECONDS,
) -> bool:
    """True when retro-meter shows a recent Plan UI Build prompt on this composer."""
    cutoff = int(time.time() * 1000) - max_age_s * 1000
    for submitted, conv, prompt in _iter_retro_generations(retro_state_path):
        if conv != composer_id or submitted < cutoff:
            continue
        if any(marker in prompt for marker in PLAN_BUILD_PROMPT_MARKERS):
            return True
    return False


def _composer_is_actively_busy_on_plan(
    composer: dict[str, Any],
    plan_path: Path,
    *,
    now_ms: int | None = None,
    retro_state_path: Path | None = None,
) -> tuple[bool, str | None]:
    """
    True only for a likely in-flight Plan Build on this plan.

    Ignores stale hasBlockingPendingActions when lastUpdatedAt is old.
    Ignores mere sidebar recency — requires blocking+recent, or a recent
    Plan Build turn in agent-retro-meter.
    """
    if not _composer_references_plan(composer, plan_path):
        return False, None
    cid = str(composer.get("composerId") or "")
    recent = _composer_header_recently_touched(composer, now_ms=now_ms)

    if composer.get("hasBlockingPendingActions") and recent:
        return True, f"composer {cid} hasBlockingPendingActions (recent)"

    if composer_has_recent_plan_build_turn(cid, retro_state_path=retro_state_path):
        return True, f"composer {cid} has recent Plan Build turn (retro-meter)"

    return False, None


def _built_by_lock_is_live(
    other_cid: str,
    plan_path: Path,
    db_path: Path | None = None,
    *,
    now_ms: int | None = None,
) -> tuple[bool, str | None]:
    """
  True when builtBy[other] likely reflects a running Build.

  Stale locks (UI idle, unregisterBuild missed) leave builtBy set but the
  holder is not blocking and not recently active on this plan — do not wait.
  """
    header = find_composer_in_headers(other_cid, db_path)
    if header is None:
        return False, None
    busy, reason = _composer_is_actively_busy_on_plan(
        header, plan_path, now_ms=now_ms
    )
    if busy and reason:
        return True, f"builtBy lock on {other_cid}: {reason}"
    return False, None


def is_plan_busy(
    plan_path: Path,
    composer_id: str,
    db_path: Path | None = None,
) -> tuple[bool, list[str]]:
    """
    True when another composer likely has an in-flight Plan Build.

    Only composers listed in registry builtBy are checked — not every tab that
    ever @'d the plan (that caused spurious 300s waits).
    """
    plan_path = normalize_plan_path(plan_path)
    reasons: list[str] = []
    now_ms = int(time.time() * 1000)
    registry = load_registry(db_path)
    _, entry = find_entry(registry, plan_path)
    if entry:
        built_by = entry.get("builtBy") or {}
        if isinstance(built_by, dict):
            for other_cid in built_by:
                if other_cid == composer_id:
                    continue
                live, reason = _built_by_lock_is_live(
                    other_cid, plan_path, db_path, now_ms=now_ms
                )
                if live and reason:
                    reasons.append(reason)

    return bool(reasons), reasons


def wait_until_quiet(
    plan_path: Path,
    composer_id: str,
    db_path: Path | None = None,
    timeout_s: int = WAIT_TIMEOUT_S,
    interval_s: int = WAIT_INTERVAL_S,
) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        busy, reasons = is_plan_busy(plan_path, composer_id, db_path)
        if not busy:
            return True
        print(f"waiting: {'; '.join(reasons)}", flush=True)
        time.sleep(interval_s)
    return False


def _ensure_list_unique_append(lst: list[str], value: str) -> bool:
    if value in lst:
        return False
    lst.append(value)
    return True


def sync_plan(
    plan_path: Path,
    composer_id: str | None = None,
    *,
    dry_run: bool = False,
    db_path: Path | None = None,
) -> SyncResult:
    plan_path = normalize_plan_path(plan_path)
    incomplete = incomplete_todo_ids(plan_path)
    if incomplete:
        raise SystemExit(
            EXIT_INCOMPLETE_TODOS,
            f"Plan has incomplete todos ({len(incomplete)}): {', '.join(incomplete)}\n"
            "Complete layer A (@owcc-plan-build) before sync.",
        )

    cid, _candidates, _via = resolve_composer_for_plan(
        plan_path, composer_id, db_path, prefer_invoking=not bool(composer_id)
    )

    if not dry_run and not wait_until_quiet(plan_path, cid, db_path):
        raise SystemExit(
            EXIT_BUSY_TIMEOUT,
            f"Timed out after {WAIT_TIMEOUT_S}s waiting for other agents on this plan.",
        )

    plan = plan_lib.read_plan(plan_path)
    todo_ids = [t.id for t in plan.todos]
    plan_name = str(plan.meta.get("name") or plan_id_from_path(plan_path))
    pid = plan_id_from_path(plan_path)
    now_ms = int(int(time.time() * 1000))

    registry = load_registry(db_path)
    existing_id, entry = find_entry(registry, plan_path)
    created = False
    actions: list[str] = []

    if entry is None:
        created = True
        entry = {
            "id": pid,
            "name": plan_name,
            "uri": make_file_uri(plan_path),
            "createdBy": cid,
            "editedBy": [cid],
            "referencedBy": [cid],
            "builtBy": {cid: list(todo_ids)},
            "lastUpdatedAt": now_ms,
            "createdAt": now_ms,
        }
        registry[pid] = entry
        actions.extend(["created registry row", "set createdBy", "set builtBy"])
    else:
        reg_id = existing_id or pid
        if _ensure_list_unique_append(entry.setdefault("referencedBy", []), cid):
            actions.append("appended referencedBy")
        if _ensure_list_unique_append(entry.setdefault("editedBy", []), cid):
            actions.append("appended editedBy")
        entry["builtBy"] = {cid: list(todo_ids)}
        actions.append("replaced builtBy")
        entry["lastUpdatedAt"] = now_ms
        entry["name"] = plan_name
        registry[reg_id] = entry

    result = SyncResult(
        plan_path=plan_path,
        plan_id=existing_id or pid,
        composer_id=cid,
        created=created,
        actions=actions,
        dry_run=dry_run,
    )

    if dry_run:
        return result

    backup_db(db_path)
    save_registry(registry, db_path)
    return result


def adopt_plan_registry(
    plan_path: Path,
    composer_id: str,
    *,
    dry_run: bool = False,
    skip_backup: bool = False,
    db_path: Path | None = None,
    exclusive_referenced_by: bool = False,
) -> ReassignResult:
    """Mirror Cursor PlanStorageService.adoptPlan — set createdBy and bump registry."""
    plan_path = normalize_plan_path(plan_path)
    registry = load_registry(db_path)
    reg_id, entry = find_entry(registry, plan_path)
    if entry is None:
        raise SystemExit(
            EXIT_PLAN_NOT_REGISTERED,
            f"No registry row for plan: {plan_path}\n"
            "Register by @-mentioning the plan in Agent chat or run plan-check first.",
        )

    pid = reg_id or plan_id_from_path(plan_path)
    prev_created = entry.get("createdBy")
    prev_built = dict(entry.get("builtBy") or {})
    actions: list[str] = []

    actions.extend(
        _promote_registry_owner(
            entry, composer_id, exclusive_referenced_by=exclusive_referenced_by
        )
    )
    entry["lastUpdatedAt"] = int(time.time() * 1000)
    if _ensure_list_unique_append(entry.setdefault("editedBy", []), composer_id):
        actions.append("appended editedBy")

    registry[pid] = entry
    result = ReassignResult(
        plan_path=plan_path,
        plan_id=pid,
        composer_id=composer_id,
        actions=actions,
        dry_run=dry_run,
        previous_created_by=str(prev_created) if prev_created else None,
        previous_built_by=prev_built,
    )

    if dry_run:
        return result

    if not skip_backup:
        backup_db(db_path)
    save_registry(registry, db_path)
    return result


def clear_plan_built_by(
    plan_path: Path,
    *,
    except_composer: str | None = None,
    dry_run: bool = False,
    skip_backup: bool = False,
    db_path: Path | None = None,
) -> list[str]:
    """Mirror unregisterBuild for all composers (or all except one). Returns removed ids."""
    plan_path = normalize_plan_path(plan_path)
    registry = load_registry(db_path)
    reg_id, entry = find_entry(registry, plan_path)
    if entry is None:
        raise SystemExit(EXIT_PLAN_NOT_REGISTERED, f"No registry row for plan: {plan_path}")

    built_by = entry.get("builtBy") or {}
    if not isinstance(built_by, dict):
        built_by = {}

    removed: list[str] = []
    for cid in list(built_by.keys()):
        if except_composer and cid == except_composer:
            continue
        del built_by[cid]
        removed.append(cid)

    if not removed and except_composer is None and not built_by:
        return removed

    entry["builtBy"] = built_by
    entry["lastUpdatedAt"] = int(time.time() * 1000)
    registry[reg_id or plan_id_from_path(plan_path)] = entry

    if dry_run:
        return removed

    if not skip_backup:
        backup_db(db_path)
    save_registry(registry, db_path)
    return removed


def prime_register_build(
    plan_path: Path,
    composer_id: str,
    *,
    dry_run: bool = False,
    skip_backup: bool = False,
    db_path: Path | None = None,
) -> list[str]:
    """
    Mirror Plan UI registerBuild(uri, composerId, todoIds) on the target composer.

    Cursor routes Build via registry.createdBy (getHandleIfLoaded) and sets
    builtBy[composerId] on Build start. Pre-binding both reduces ghost-host wins.
    """
    plan_path = normalize_plan_path(plan_path)
    registry = load_registry(db_path)
    reg_id, entry = find_entry(registry, plan_path)
    if entry is None:
        raise SystemExit(EXIT_PLAN_NOT_REGISTERED, f"No registry row for plan: {plan_path}")

    todo_ids = incomplete_todo_ids(plan_path)
    entry["builtBy"] = {composer_id: list(todo_ids)}
    entry["lastUpdatedAt"] = int(time.time() * 1000)
    registry[reg_id or plan_id_from_path(plan_path)] = entry

    if dry_run:
        return ["prime builtBy (registerBuild parity)"]

    if not skip_backup:
        backup_db(db_path)
    save_registry(registry, db_path)
    return ["prime builtBy (registerBuild parity)"]


def reassign_plan_host(
    plan_path: Path,
    composer_id: str | None = None,
    *,
    dry_run: bool = False,
    clear_built_by: bool = True,
    prime_build: bool = True,
    skip_wait: bool = True,
    prefer_invoking: bool = True,
    workspace_root: Path | None = None,
    db_path: Path | None = None,
    exclusive_host: bool = True,
) -> ReassignResult:
    """
    Point plan registry + composer headers at target composer for the next Plan UI Build.

    Mirrors Cursor adoptPlan + unregisterBuild + registerComposerReference (headers).
    Does not cancel in-flight generations or edit composer conversation blobs.
    """
    plan_path = normalize_plan_path(plan_path)
    ws_root = workspace_root or workspace_root_for_plan(plan_path)
    prefer = prefer_invoking and not bool(composer_id)
    cid, _candidates, resolved_via = resolve_composer_for_plan(
        plan_path,
        composer_id,
        db_path,
        prefer_invoking=prefer,
        authoritative_only=prefer,
        workspace_root=ws_root,
    )
    if not dry_run:
        busy, busy_reasons = is_plan_busy(plan_path, cid, db_path)
        if busy:
            msg = "; ".join(busy_reasons)
            if skip_wait:
                print(
                    f"warning: {msg}\n"
                    "reassign proceeding immediately (default). "
                    "Cancel the other Plan Build or pass --wait to block up to "
                    f"{WAIT_TIMEOUT_S}s.",
                    file=__import__("sys").stderr,
                )
            elif not wait_until_quiet(plan_path, cid, db_path):
                raise SystemExit(
                    EXIT_BUSY_TIMEOUT,
                    f"Timed out after {WAIT_TIMEOUT_S}s waiting for other agents on this plan.\n"
                    f"Still busy: {msg}\n"
                    "Cancel the other Plan Build, or re-run without --wait (default).",
                )

    if not dry_run:
        backup_db(db_path)

    removed_builders: list[str] = []
    if clear_built_by:
        removed_builders = clear_plan_built_by(
            plan_path,
            except_composer=None,
            dry_run=dry_run,
            skip_backup=True,
            db_path=db_path,
        )

    result = adopt_plan_registry(
        plan_path,
        cid,
        dry_run=dry_run,
        skip_backup=True,
        db_path=db_path,
        exclusive_referenced_by=exclusive_host,
    )
    result.resolved_via = resolved_via
    result.detected_invoking_composer_id = detect_invoking_composer(
        workspace_root=ws_root,
        plan_path=plan_path,
        db_path=db_path,
    )[0]

    if prime_build and not dry_run:
        result.actions.extend(
            prime_register_build(
                plan_path, cid, skip_backup=True, db_path=db_path
            )
        )
    elif prime_build and dry_run:
        result.actions.append("prime builtBy (registerBuild parity)")

    stripped_headers: list[str] = []
    if exclusive_host:
        if not dry_run:
            reinforce_actions = reinforce_exclusive_plan_host(
                plan_path, cid, db_path
            )
            stripped_headers = [
                a.split(": ", 1)[-1]
                for a in reinforce_actions
                if a.startswith("stripped referencedPlans from:")
            ]
            if reinforce_actions:
                result.actions.extend(reinforce_actions)
        else:
            stripped_headers = strip_plan_from_other_composer_headers(
                plan_path, cid, db_path, dry_run=True
            )
            if stripped_headers:
                result.actions.append(
                    "stripped referencedPlans from other composer(s): "
                    + ", ".join(stripped_headers)
                )

    header_changed = False
    if not dry_run and not exclusive_host:
        header_changed = ensure_composer_references_plan_in_headers(
            cid, plan_path, db_path, bump_last_updated=False
        )
    elif not dry_run and exclusive_host:
        header_changed = True
    else:
        header_changed = find_composer_in_headers(cid, db_path) is not None
    if header_changed:
        result.actions.append(
            "target composer referencedPlans + supremacy lastUpdatedAt"
        )
    if removed_builders:
        result.actions.append(f"cleared builtBy for: {', '.join(removed_builders)}")

    if not dry_run:
        # Re-load after adopt for accurate post-state in callers
        registry = load_registry(db_path)
        _, entry = find_entry(registry, plan_path)
        if entry:
            result.previous_built_by = dict(entry.get("builtBy") or {})

    return result


def execution_state_summary(
    plan_path: Path,
    composer_id: str | None = None,
    db_path: Path | None = None,
) -> dict[str, Any]:
    """Diagnostics for plan-change-composer: registry + header resolution hints."""
    summary = show_summary(plan_path, composer_id, db_path)
    plan_path_norm = normalize_plan_path(plan_path)
    entry = summary.get("registry_entry") or {}
    built_by = entry.get("builtBy") or {}
    host_composer: str | None = None
    if isinstance(built_by, dict) and len(built_by) == 1:
        host_composer = next(iter(built_by.keys()))
    elif entry.get("createdBy"):
        host_composer = entry.get("createdBy")

    target = summary.get("resolved_composer_id")
    header = find_composer_in_headers(target, db_path) if target else None
    ws_root = workspace_root_for_plan(plan_path)
    invoking, invoking_source = detect_invoking_composer(
        workspace_root=ws_root, plan_path=plan_path, db_path=db_path
    )
    marker = read_last_reassign_marker(plan_path_norm)
    owner = entry.get("createdBy")
    refs = entry.get("referencedBy") or []
    except_cid = str(owner or target or "")
    other_header_hosts = (
        other_composers_with_plan_in_headers(plan_path_norm, except_cid, db_path)
        if except_cid
        else [c.composer_id for c in list_composer_candidates(plan_path_norm, db_path)]
    )
    exclusive_ok = (
        bool(owner)
        and isinstance(refs, list)
        and len(refs) == 1
        and refs[0] == owner
        and not other_header_hosts
    )

    return {
        **summary,
        "likely_build_host_composer_id": host_composer,
        "target_composer_in_headers": header is not None,
        "target_has_pending_plan": bool(header.get("hasPendingPlan")) if header else None,
        "cursor_build_routing": (
            "Plan UI: getHandleIfLoaded(registry.createdBy) submits Build; "
            "other tabs with referencedPlans can still capture Build — reassign uses exclusive host"
        ),
        "detected_invoking_composer_id": invoking,
        "detected_invoking_source": invoking_source,
        "last_reassign_marker": marker,
        "other_plan_header_hosts": other_header_hosts,
        "exclusive_host_ok": exclusive_ok,
    }


def show_summary(
    plan_path: Path,
    composer_id: str | None = None,
    db_path: Path | None = None,
) -> dict[str, Any]:
    plan_path = normalize_plan_path(plan_path)
    plan = plan_lib.read_plan(plan_path)
    registry = load_registry(db_path)
    reg_id, entry = find_entry(registry, plan_path)

    status_counts: dict[str, int] = {}
    for t in plan.todos:
        status_counts[t.status] = status_counts.get(t.status, 0) + 1

    candidates = list_composer_candidates(plan_path, db_path)
    resolved: str | None = None
    resolve_error: str | None = None
    resolved_via: str | None = None
    ws_root = workspace_root_for_plan(plan_path)
    try:
        resolved, _, resolved_via = resolve_composer_for_plan(
            plan_path,
            composer_id,
            db_path,
            prefer_invoking=not bool(composer_id),
            workspace_root=ws_root,
        )
    except SystemExit as exc:
        resolve_error = str(exc)

    invoking, invoking_source = detect_invoking_composer(
        workspace_root=ws_root, plan_path=plan_path, db_path=db_path
    )

    return {
        "plan_path": str(plan_path),
        "plan_id": reg_id,
        "registered": entry is not None,
        "registry_entry": entry,
        "todo_status_counts": status_counts,
        "all_complete": not incomplete_todo_ids(plan_path),
        "composer_candidates": [
            {
                "composer_id": c.composer_id,
                "name": c.name,
                "unified_mode": c.unified_mode,
                "last_updated_at": c.last_updated_at,
            }
            for c in candidates
        ],
        "resolved_composer_id": resolved,
        "resolved_via": resolved_via,
        "resolve_error": resolve_error,
        "detected_invoking_composer_id": invoking,
        "detected_invoking_source": invoking_source,
    }
