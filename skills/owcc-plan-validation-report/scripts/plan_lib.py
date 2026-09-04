"""Shared plan frontmatter parser and Build sizing metrics for Cursor plan tools."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Chunk thresholds (pass 2 — split suggestions only; not qualitative verify).
TODO_WEIGHT_SPLIT = 5.0
TODO_WEIGHT_WATCH = 4.0  # shown in compact agent brief; split at TODO_WEIGHT_SPLIT
PHASE_TOTAL_WEIGHT_SPLIT = 6.0  # compared to median phase weight, not raw sum alone
PHASE_TODO_COUNT_SPLIT = 10
PHASE_WEIGHT_IMBALANCE_RATIO = 1.6  # phase total vs median total (split hints)
PHASE_BALANCE_RATIO = 1.35  # vs median: heavier/lighter phase labels in report
BODY_TOKENS_PER_PHASE_ADD = 900  # marker / add_phases hint only (body spread)
PHASES_MAX_BEFORE_MERGE_SIGNAL = 10
PHASES_MERGE_MIN = 3  # merge_phases hint from this count when todos/phase sparse
TODOS_PER_PHASE_MERGE_SIGNAL = 2.5  # avg below → over-phased
MIN_TODOS_FOR_MERGE_SIGNAL = 8
MERMAID_LINES_HEAVY = 40
REF_FILE_HEAVY_BYTES = 50_000
REF_BYTES_PLAN_HEAVY = REF_FILE_HEAVY_BYTES * 3

# Display bands (not split triggers).
TODO_WEIGHT_THRESHOLD = TODO_WEIGHT_SPLIT
PHASE_WEIGHT_THRESHOLD = PHASE_TOTAL_WEIGHT_SPLIT
PLAN_HEAVY_THRESHOLD = 6.5

VALID_STATUSES = frozenset({"pending", "in_progress", "completed", "cancelled"})

# owcc-plan-improve OUTPUTS.md — body §1–10 (H2) after a single title H1.
PLAN_BODY_SECTION_HEADINGS: tuple[str, ...] = (
    "Rules",
    "Aims",
    "Scope",
    "Target shape",
    "Stages",
    "Additions",
    "Modifications",
    "Removals",
    "Decisions",
    "Reference",
)

PATH_RE = re.compile(
    r"(?:~/[\w./-]+|~/.cursor/[\w./-]+"
    r"|(?:\./)?(?:packs|src-plugins|tests|tools|\.cursor|vendor|docs|local)/[\w./-]+"
    r"|(?:\./)?[\w.-]+/[\w./-]+\.(?:py|sh|md|json|yaml|yml))",
    re.IGNORECASE,
)
# Bare filenames and backtick paths: some_script.py, `src/foo.py`
FILE_EXT = r"py|sh|md|json|yaml|yml|js|ts|tsx|go|rb|pl|pm|plan\.md|schema\.json"
FILE_EXT_TAIL_RE = re.compile(rf"\.(?:{FILE_EXT})$", re.IGNORECASE)
FILE_REF_RE = re.compile(
    rf"(?:`([^`]+\.(?:{FILE_EXT}))`)"
    rf"|(?:\b([\w][\w.-]*\.(?:{FILE_EXT}))\b)",
    re.IGNORECASE,
)
KNOWN_PATH_PREFIX_RE = re.compile(
    r"^(?:\./)?(?:packs|src-plugins|tests|tools|\.cursor|vendor|docs|local)/",
    re.IGNORECASE,
)
# Prose or shorthand with a slash but not a repo path (MIB/OID, 10s/3, README/config).
PSEUDO_PATH_RE = re.compile(
    r"^(?:[A-Z]{2,}|[\d]+[a-z]*)/[A-Za-z0-9+.-]+$",
    re.IGNORECASE,
)
BROKEN_ENCODED_PATH_RE = re.compile(r"^\d+projects/", re.IGNORECASE)
# Small per-todo slice of plan context (baseline still counts fully in plan weight).
PLAN_CONTEXT_TODO_SHARE = 0.08
REF_COUNT_IN_PLAN_WEIGHT = 0.15  # per plausible file ref in plan weight
REF_COUNT_PLAN_CAP = 18
REF_BYTES_PLAN_DIVISOR = 250_000.0
REF_BYTES_PLAN_CAP = 2.5
TODO_REF_FILE_WEIGHT = 0.35  # per file ref mentioned in todo content
TODO_REF_HEAVY_BYTE_WEIGHT = 1.0  # per 50KiB in todo-specific refs (capped)
# Recommended phase count: round(plan_weight / this). Raise = fewer phases.
PLAN_WEIGHT_PER_PHASE_THRESHOLD = 12.0
PHASE_COUNT_IN_PLAN_CONTEXT = 0.85
REF_FILE_COUNT_MARKER_THRESHOLD = 12
OVERLOADED_RE = re.compile(r"\b(and|then|also)\b", re.IGNORECASE)
PHASE_HEADING_RE = re.compile(r"^##\s+Phase\s", re.MULTILINE | re.IGNORECASE)
VERIFY_ID_RE = re.compile(r"(?:^|-)verify(?:-|$)", re.IGNORECASE)
IMPLEMENT_LIKE_RE = re.compile(
    r"^(add|create|implement|update|rewrite|rename|wire|build|fix|remove|migrate|refactor)",
    re.IGNORECASE,
)

ESTIMATE_SCORES = {
    "files": {"few": 0.0, "some": 0.8, "many": 1.6},
    "edits": {"small": 0.0, "medium": 1.0, "large": 2.0},
    "tool_uses": {"low": 0.0, "med": 1.0, "medium": 1.0, "high": 2.0},
}


@dataclass
class TodoItem:
    id: str
    content: str
    status: str
    phase_name: str | None = None
    index: int = 0
    phase_index: int | None = None


@dataclass
class PlanData:
    path: Path
    meta: dict[str, Any]
    body: str
    todos: list[TodoItem] = field(default_factory=list)
    is_project: bool = False


@dataclass
class TodoMetrics:
    todo: TodoItem
    weight: float
    why: list[str] = field(default_factory=list)
    missing_verify: bool = False
    overloaded: bool = False
    path_count: int = 0
    content_weight: float = 0.0
    plan_context_share: float = 0.0
    todo_ref_weight: float = 0.0
    ref_file_count: int = 0


@dataclass
class PlanMetrics:
    todo_count: int = 0
    pair_count: int = 0
    missing_verify_count: int = 0
    body_tokens_est: int = 0
    distinct_paths: int = 0
    phase_heading_count: int = 0
    stop_if_count: int = 0
    is_project: bool = False
    phase_count: int = 0
    shape: str = "flat"
    chunk_native_pairs: int = 0
    max_phase_todos: int = 0


def read_plan(path: str | Path) -> PlanData:
    p = Path(path).expanduser().resolve()
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{p}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{p}: malformed frontmatter fences")
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2]
    if not isinstance(meta, dict):
        raise ValueError(f"{p}: frontmatter must be a mapping")
    data = PlanData(path=p, meta=meta, body=body)
    data.is_project = bool(meta.get("isProject"))
    data.todos = _collect_todos(meta, data.is_project)
    return data


def _collect_todos(meta: dict[str, Any], is_project: bool) -> list[TodoItem]:
    items: list[TodoItem] = []
    idx = 0
    if is_project and meta.get("phases"):
        for pi, phase in enumerate(meta["phases"] or []):
            name = phase.get("name") if isinstance(phase, dict) else None
            for t in (phase.get("todos") or []) if isinstance(phase, dict) else []:
                if not isinstance(t, dict):
                    continue
                tid = str(t.get("id") or f"todo-{idx}")
                content = _content_str(t.get("content"))
                status = str(t.get("status") or "pending")
                items.append(
                    TodoItem(
                        id=tid,
                        content=content,
                        status=status,
                        phase_name=name,
                        index=idx,
                        phase_index=pi,
                    )
                )
                idx += 1
    else:
        for t in meta.get("todos") or []:
            if not isinstance(t, dict):
                continue
            tid = str(t.get("id") or f"todo-{idx}")
            content = _content_str(t.get("content"))
            status = str(t.get("status") or "pending")
            items.append(
                TodoItem(
                    id=tid,
                    content=content,
                    status=status,
                    phase_name=None,
                    index=idx,
                )
            )
            idx += 1
    return items


def _content_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def load_estimates(path: str | Path | None) -> dict[str, dict[str, str]]:
    if not path:
        return {}
    p = Path(path).expanduser()
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("estimates JSON must be an object keyed by todo id")
    out: dict[str, dict[str, str]] = {}
    for k, v in raw.items():
        if isinstance(v, dict):
            out[str(k)] = {str(kk): str(vv).lower() for kk, vv in v.items()}
    return out


def is_verify_todo(todo: TodoItem) -> bool:
    cid = todo.id.lower()
    if cid.startswith("verify-") or cid.endswith("-verify"):
        return True
    if VERIFY_ID_RE.search(todo.id):
        return True
    text = todo.content.lower()
    return text.startswith("verify ") or text.startswith("validation:")


def is_implement_like(todo: TodoItem) -> bool:
    if is_verify_todo(todo):
        return False
    if IMPLEMENT_LIKE_RE.match(todo.content):
        return True
    return not todo.content.lower().startswith("confirm ")


def has_verify_pair(todos: list[TodoItem], index: int) -> bool:
    todo = todos[index]
    if is_verify_todo(todo):
        return True
    tid = todo.id
    candidates = {
        f"verify-{tid}",
        f"{tid}-verify",
        f"verify-{tid.replace('-', '_')}",
    }
    for j, other in enumerate(todos):
        if j == index:
            continue
        if other.id in candidates or other.id.lower() in {c.lower() for c in candidates}:
            return True
        if is_verify_todo(other) and abs(j - index) <= 1:
            return True
    return False


def is_phase_validation_todo(todo: TodoItem) -> bool:
    lid = todo.id.lower()
    content = todo.content.lower()
    return (
        "validate-phase" in lid
        or lid.startswith("phase-validation")
        or ("phase" in content and "gate" in content)
    )


def is_final_audit_todo(todo: TodoItem) -> bool:
    lid = todo.id.lower()
    content = todo.content.lower()
    return (
        "completion-audit" in lid
        or "final-validation" in lid
        or lid.endswith("-audit")
        or "completion audit" in content
        or "final validation" in content
    )


def is_scaffold_todo(todo: TodoItem) -> bool:
    return "scaffold" in todo.id.lower() or todo.content.lower().startswith(
        ("create tests/", "create test_")
    )


def is_pack_validate_todo(todo: TodoItem) -> bool:
    lid = todo.id.lower()
    content = todo.content.lower()
    return "pack-validate" in lid or "opspack-check-pack" in content


def phase_has_validation_gate(todos: list[TodoItem], phase_index: int | None) -> bool:
    if phase_index is None:
        return False
    return any(
        t.phase_index == phase_index and is_phase_validation_todo(t)
        for t in todos
    )


def phase_has_pack_validate(todos: list[TodoItem], phase_index: int | None) -> bool:
    if phase_index is None:
        return False
    return any(
        t.phase_index == phase_index and is_pack_validate_todo(t) for t in todos
    )


def qualifies_verify_coverage(todos: list[TodoItem], index: int) -> bool:
    """Structural verification coverage (qualitative pass — not chunk sizing)."""
    todo = todos[index]
    if is_verify_todo(todo) or is_phase_validation_todo(todo) or is_final_audit_todo(todo):
        return True
    if is_scaffold_todo(todo):
        return True
    if has_verify_pair(todos, index):
        return True
    if phase_has_validation_gate(todos, todo.phase_index):
        return True
    if "mirror" in todo.id.lower() and phase_has_pack_validate(todos, todo.phase_index):
        return True
    if is_pack_validate_todo(todo):
        return True
    return False


def implement_needs_verify(todos: list[TodoItem], index: int) -> bool:
    t = todos[index]
    if not is_implement_like(t):
        return False
    return not qualifies_verify_coverage(todos, index)


def distinct_paths_in_text(text: str) -> set[str]:
    return {r for r in PATH_RE.findall(text) if _is_plausible_file_reference(r)}


def _is_plausible_file_reference(raw: str) -> bool:
    """Drop slash-phrases, broken %20 paths, and extensionless prose."""
    s = raw.strip().strip("`").rstrip("/")
    if len(s) < 4 or "@" in s:
        return False
    if s.lower() in (".plan.md", "plan.md"):
        return False
    if BROKEN_ENCODED_PATH_RE.match(s):
        return False
    if "/packs/packs/" in s.replace("\\", "/"):
        return False
    if PSEUDO_PATH_RE.match(s):
        return False
    if FILE_EXT_TAIL_RE.search(s):
        return True
    if s.startswith("~/") or s.startswith("./") or KNOWN_PATH_PREFIX_RE.match(s):
        return "/" in s and len(s.split("/")) >= 2
    return False


def file_references_in_text(text: str) -> set[str]:
    """Path-like strings plus bare/script filenames (e.g. some_script.py)."""
    refs: set[str] = set()
    for m in PATH_RE.finditer(text):
        refs.add(m.group(0))
    for m in FILE_REF_RE.finditer(text):
        refs.add((m.group(1) or m.group(2) or "").strip())
    return {r for r in refs if _is_plausible_file_reference(r)}


def collect_plan_file_references(plan: PlanData) -> set[str]:
    refs = file_references_in_text(plan.body)
    for t in plan.todos:
        refs |= file_references_in_text(t.content)
    return refs


def _find_bare_filename(name: str, workspace: Path, max_hits: int = 6) -> list[Path]:
    if "/" in name or name.startswith("."):
        return []
    hits: list[Path] = []
    try:
        for p in workspace.rglob(name):
            if p.is_file():
                hits.append(p)
                if len(hits) >= max_hits:
                    break
    except OSError:
        return []
    return hits


def resolve_file_reference(
    raw: str, workspace: Path
) -> tuple[Path | None, int | None, str]:
    """Return (resolved path, size bytes, status)."""
    raw = raw.strip().strip("`")
    if not raw:
        return None, None, "skipped"
    p = Path(raw)
    if raw == "~" or raw.startswith("~/") or raw.startswith("~/.cursor/"):
        try:
            p = Path(raw).expanduser()
        except RuntimeError:
            return None, None, "skipped"
    elif "/" in raw or raw.startswith("./"):
        p = (workspace / raw.lstrip("./")).resolve()
    else:
        matches = _find_bare_filename(raw, workspace)
        if not matches:
            return None, None, "missing"
        if len(matches) > 1:
            p = matches[0]
            try:
                return p, p.stat().st_size, "ambiguous"
            except OSError:
                return None, None, "skipped"
        p = matches[0]
    try:
        if not p.is_file():
            return None, None, "missing"
        size = p.stat().st_size
        if size > REF_FILE_MAX_STAT:
            return p, size, "large"
        if size >= REF_FILE_HEAVY_BYTES:
            return p, size, "heavy"
        return p, size, "ok"
    except OSError:
        return None, None, "skipped"


def referenced_file_stats(
    plan: PlanData, workspace: Path
) -> list[tuple[str, int | None, str]]:
    """Each distinct file reference: (as written, bytes or None, status)."""
    refs = collect_plan_file_references(plan)
    rows: list[tuple[str, int | None, str]] = []
    for raw in sorted(refs):
        _path, size, status = resolve_file_reference(raw, workspace)
        rows.append((raw, size, status))
    return rows


def referenced_file_stats_for_text(
    text: str, workspace: Path
) -> list[tuple[str, int | None, str]]:
    rows: list[tuple[str, int | None, str]] = []
    for raw in sorted(file_references_in_text(text)):
        _path, size, status = resolve_file_reference(raw, workspace)
        rows.append((raw, size, status))
    return rows


def todo_content_base_weight(
    todo: TodoItem,
    estimates: dict[str, dict[str, str]],
) -> tuple[float, list[str]]:
    """Todo weight from prose only — file refs are scored in todo_reference_weight."""
    why: list[str] = []
    w = 0.0
    content_len = len(todo.content)
    if content_len > 220:
        w += min(2.5, content_len / 120.0)
        why.append("long content")
    if OVERLOADED_RE.search(todo.content):
        w += 1.5
        why.append("possibly overloaded wording")
    est = estimates.get(todo.id)
    eb, ew = _estimate_bonus(est)
    w += eb
    why.extend(ew)
    return round(w, 2), why


def todo_reference_weight(
    todo: TodoItem, workspace: Path
) -> tuple[float, int, list[str]]:
    """Extra weight from files referenced in this todo's content only."""
    rows = referenced_file_stats_for_text(todo.content, workspace)
    if not rows:
        return 0.0, 0, []
    why: list[str] = []
    w = TODO_REF_FILE_WEIGHT * len(rows)
    byte_bonus = 0.0
    for _raw, size, status in rows:
        if size and status in ("ok", "heavy", "large"):
            byte_bonus += min(1.5, (size / REF_FILE_HEAVY_BYTES) * TODO_REF_HEAVY_BYTE_WEIGHT)
    w += min(3.0, byte_bonus)
    why.append(f"{len(rows)} file ref(s) in todo")
    if byte_bonus:
        why.append("heavy referenced file(s)")
    return round(w, 2), len(rows), why


def compute_plan_context_weight(
    body_tokens_est: int,
    mermaid_lines: int,
    ref_file_count: int,
    ref_bytes: int,
    phase_count: int = 1,
    todo_count: int = 0,
) -> float:
    """Plan baseline: body, diagrams, refs, phase count, todo count.

    Also distributed per todo (see build_todo_chunk_metrics). Intentionally
    counted again in total plan weight when summing phase weights — by design.
    """
    w = 0.001 * body_tokens_est
    w += 0.01 * mermaid_lines
    capped_refs = min(ref_file_count, REF_COUNT_PLAN_CAP)
    w += REF_COUNT_IN_PLAN_WEIGHT * capped_refs
    w += min(REF_BYTES_PLAN_CAP, ref_bytes / REF_BYTES_PLAN_DIVISOR)
    w += PHASE_COUNT_IN_PLAN_CONTEXT * max(1, phase_count)
    if todo_count > 0:
        w += 0.06 * min(todo_count, 30)
    return round(w, 2)


def compute_total_plan_weight(
    plan_context_weight: float,
    phase_rows: list[PhaseChunkMetrics],
) -> float:
    """context baseline + sum(phase weights); each phase weight = sum(todo weights)."""
    work = sum(pr.total_weight for pr in phase_rows)
    return round(plan_context_weight + work, 2)


def phase_split_reasons(
    pr: PhaseChunkMetrics, phase_rows: list[PhaseChunkMetrics]
) -> list[str]:
    """Why a phase may need splitting — avoids count-only triggers on mirrored dual-plugin work."""
    why: list[str] = []
    if pr.max_todo_weight >= TODO_WEIGHT_SPLIT:
        why.append(f"max todo weight {pr.max_todo_weight} >= {TODO_WEIGHT_SPLIT}")
    elif pr.todo_count >= PHASE_TODO_COUNT_SPLIT:
        why.append(f"{pr.todo_count} todos in phase (>= {PHASE_TODO_COUNT_SPLIT})")
    if len(phase_rows) >= 2:
        med_weight = sorted(p.total_weight for p in phase_rows)[len(phase_rows) // 2]
        threshold = max(PHASE_TOTAL_WEIGHT_SPLIT, med_weight * PHASE_WEIGHT_IMBALANCE_RATIO)
        if (
            pr.total_weight >= threshold
            and pr.max_todo_weight >= TODO_WEIGHT_WATCH
            and pr.total_weight > med_weight
        ):
            why.append(
                f"phase weight {pr.total_weight} vs median {med_weight:.1f} "
                f"(threshold {threshold:.1f})"
            )
    elif (
        pr.total_weight >= PHASE_TOTAL_WEIGHT_SPLIT
        and pr.max_todo_weight >= TODO_WEIGHT_WATCH
    ):
        why.append(f"phase total weight {pr.total_weight} >= {PHASE_TOTAL_WEIGHT_SPLIT}")
    return why


def recommend_phase_count(
    total_plan_weight: float,
    over_phased: bool,
    current_phase_count: int,
) -> int:
    """Plan weight vs single threshold. No per-todo-count bumps."""
    recommended = max(
        1,
        int(round(total_plan_weight / PLAN_WEIGHT_PER_PHASE_THRESHOLD)),
    )
    if over_phased:
        return max(1, min(current_phase_count, recommended))
    return recommended


def compute_plan_metrics(plan: PlanData) -> PlanMetrics:
    m = PlanMetrics()
    m.todo_count = len(plan.todos)
    m.body_tokens_est = max(1, len(plan.body) // 4)
    m.distinct_paths = len(collect_plan_file_references(plan))
    m.phase_heading_count = len(PHASE_HEADING_RE.findall(plan.body))
    m.stop_if_count = len(re.findall(r"(?i)\*\*stop-if\*\*|^###\s+stop-if", plan.body, re.MULTILINE))
    m.is_project = plan.is_project
    if plan.is_project and plan.meta.get("phases"):
        m.shape = "project"
        m.phase_count = len(plan.meta.get("phases") or [])
        counts: list[int] = []
        by_phase: dict[int, list[TodoItem]] = {}
        for t in plan.todos:
            pi = t.phase_index if t.phase_index is not None else 0
            by_phase.setdefault(pi, []).append(t)
        for phase_todos in by_phase.values():
            counts.append(len(phase_todos))
        m.max_phase_todos = max(counts) if counts else 0
        m.chunk_native_pairs = m.max_phase_todos
    else:
        m.shape = "flat"
        m.chunk_native_pairs = sum(
            1 for i, t in enumerate(plan.todos) if is_implement_like(t) and has_verify_pair(plan.todos, i)
        )
    pairs = 0
    missing = 0
    for i, t in enumerate(plan.todos):
        if is_implement_like(t):
            if qualifies_verify_coverage(plan.todos, i):
                pairs += 1
            else:
                missing += 1
    m.pair_count = pairs
    m.missing_verify_count = missing
    return m


def _estimate_bonus(est: dict[str, str] | None) -> tuple[float, list[str]]:
    if not est:
        return 0.0, []
    bonus = 0.0
    why: list[str] = []
    for key, table in ESTIMATE_SCORES.items():
        val = est.get(key)
        if not val:
            continue
        score = table.get(val.lower(), 0.0)
        if score:
            bonus += score
            why.append(f"est {key} {val}")
    return bonus, why


def build_todo_chunk_metrics(
    todo: TodoItem,
    plan: PlanData,
    estimates: dict[str, dict[str, str]],
    workspace: Path,
    plan_context_weight: float,
    todo_count: int,
) -> TodoMetrics:
    """Final todo weight = content + small plan-context share + todo-specific file refs."""
    missing = implement_needs_verify(plan.todos, todo.index)
    content_w, why = todo_content_base_weight(todo, estimates)
    ref_w, ref_n, ref_why = todo_reference_weight(todo, workspace)
    why.extend(ref_why)
    share = 0.0
    if todo_count > 0:
        share = round(
            (plan_context_weight / todo_count) * PLAN_CONTEXT_TODO_SHARE,
            2,
        )
        if share > 0:
            why.append(f"plan context share +{share}")
    total = round(content_w + share + ref_w, 2)
    paths = file_references_in_text(todo.content)
    overloaded = bool(OVERLOADED_RE.search(todo.content)) and len(paths) >= 2
    return TodoMetrics(
        todo=todo,
        weight=total,
        why=why,
        missing_verify=missing,
        overloaded=overloaded,
        path_count=len(paths),
        content_weight=content_w,
        plan_context_share=share,
        todo_ref_weight=ref_w,
        ref_file_count=ref_n,
    )


# --- Qualitative (pass 1) and chunk (pass 2) reports ---

UUID_ID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)
MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
FORBIDDEN_BODY_LABELS = (
    "Execution route:",
    "Plan shape:",
    "Native chunks:",
    "Plan-change-composer role:",
)
QUOTED_EDIT_PROHIBITION_RE = re.compile(
    r"do\s+not\s+edit\s+the\s+plan\s+file\s+itself",
    re.I,
)
ORCHESTRATOR_MARKERS_RE = re.compile(
    r"(?i)authoritative\s+build\s+file|orchestrator\s+only|"
    r"stop-if:.*(?:build\s+on\s+this\s+file|plan\s+ui\s+build)",
)


def is_buildable_plan(plan: PlanData) -> bool:
    """False for orchestrator/index plans that must not receive a build execution contract."""
    return not ORCHESTRATOR_MARKERS_RE.search(plan.body)
REF_FILE_MAX_STAT = 2_000_000


@dataclass
class QualitativeFinding:
    severity: str  # error | warn | info
    code: str
    message: str
    todo_id: str | None = None


@dataclass
class ChunkMarker:
    """Plan-level ratio/metric vs threshold for agent orientation."""

    name: str
    value: float
    threshold: float
    status: str  # ok | watch | trigger
    note: str


@dataclass
class ChunkSplitSuggestion:
    """Directional split hint — not a generic 'plan is heavy'."""

    action: str  # split_todo | split_phase | add_phases | merge_phases
    target: str
    metric_value: float
    band: str  # low | med | high
    why: list[str]

    @property
    def scope(self) -> str:
        if self.action == "split_todo":
            return "todo"
        if self.action == "split_phase":
            return "phase"
        return "plan"


def _complexity_band(score: float, med_at: float, high_at: float) -> str:
    if score >= high_at:
        return "high"
    if score >= med_at:
        return "med"
    return "low"


def mermaid_metrics(body: str) -> tuple[int, int, int]:
    blocks = MERMAID_BLOCK_RE.findall(body)
    lines = sum(b.count("\n") + 1 for b in blocks)
    nodes = sum(len(re.findall(r"[|\[\(]", b)) for b in blocks)
    return len(blocks), lines, nodes


def resolve_workspace_root(plan: PlanData, workspace: Path | None) -> Path:
    if workspace is not None:
        return workspace.expanduser().resolve()
    start = plan.path.parent
    for parent in [start, *start.parents]:
        if (parent / ".git").is_dir():
            return parent
    return start


def qualitative_findings(plan: PlanData) -> list[QualitativeFinding]:
    """Hygiene / Build-ready findings that are NOT covered by validate_structure.

    Do not call validate_structure here — peers RUN plan-validate-structure.py
    (and the write-report script) separately so structure is not double-counted.
    """
    findings: list[QualitativeFinding] = []
    for t in plan.todos:
        if not t.content:
            findings.append(
                QualitativeFinding("error", "empty_content", "Todo has empty content", t.id)
            )
        if UUID_ID_RE.match(t.id):
            findings.append(
                QualitativeFinding(
                    "error",
                    "uuid_todo_id",
                    "Todo id looks like a Plan UI UUID — use stable kebab-case ids",
                    t.id,
                )
            )
    if plan.is_project:
        root = plan.meta.get("todos") or []
        if root and not (isinstance(root, list) and len(root) == 0):
            findings.append(
                QualitativeFinding(
                    "error",
                    "isproject_root_todos",
                    "isProject: true but root todos is not empty — use todos: []",
                )
            )
    for label in FORBIDDEN_BODY_LABELS:
        if re.search(rf"\*\*{re.escape(label)}\*\*", plan.body, re.I):
            findings.append(
                QualitativeFinding(
                    "warn",
                    "operator_line_in_body",
                    f"Body contains operator-only '**{label}**' — remove from plan body",
                )
            )
    if QUOTED_EDIT_PROHIBITION_RE.search(plan.body):
        findings.append(
            QualitativeFinding(
                "warn",
                "quoted_edit_prohibition",
                "Body quotes Cursor's injected edit prohibition — remove; use Plan file edit rule (status-only exception) without quoting it",
            )
        )
    if is_buildable_plan(plan) and not re.search(
        r"(?i)plan\s+file\s+edit\s+rule", plan.body
    ):
        findings.append(
            QualitativeFinding(
                "warn",
                "missing_plan_file_edit_rule",
                "Execution contract missing Plan file edit rule (status-only exception)",
            )
        )
    return findings


def phases_for_chunking(plan: PlanData) -> list[tuple[str, list[TodoItem]]]:
    if plan.is_project and plan.meta.get("phases"):
        by_pi: dict[int, list[TodoItem]] = {}
        for t in plan.todos:
            pi = t.phase_index if t.phase_index is not None else 0
            by_pi.setdefault(pi, []).append(t)
        out: list[tuple[str, list[TodoItem]]] = []
        for pi in sorted(by_pi):
            name = by_pi[pi][0].phase_name or f"phase-{pi}"
            out.append((name, by_pi[pi]))
        return out
    return [("(single phase)", list(plan.todos))]


@dataclass
class PhaseChunkMetrics:
    name: str
    todo_count: int
    total_weight: float
    max_todo_weight: float
    avg_weight: float
    band: str
    complexity: str  # low | med | high


@dataclass
class ChunkAgentBrief:
    """Straightforward pass-2 summary for the plan-check agent to judge actions."""

    recommended_phases: int
    current_phases: int
    plan_context_weight: float
    plan_weight: float
    phases_may_require_splitting: list[str]
    todos_may_require_splitting: list[str]
    merge_phases_suggested: bool
    add_phases_suggested: bool
    homogeneous_work_suggested: bool
    redundant_grep_verify: bool
    individual_todo_weights: list[tuple[str, float]]
    overweighted_phases: list[tuple[str, float]]  # name, phase weight
    underweighted_phases: list[tuple[str, float]]


def _is_over_phased(
    phase_count: int,
    todos_per_phase_avg: float,
    todo_count: int,
) -> bool:
    if todos_per_phase_avg >= TODOS_PER_PHASE_MERGE_SIGNAL:
        return False
    if todo_count < MIN_TODOS_FOR_MERGE_SIGNAL:
        return False
    return phase_count >= PHASES_MERGE_MIN or phase_count >= PHASES_MAX_BEFORE_MERGE_SIGNAL


def detect_homogeneous_work(plan: PlanData) -> bool:
    """True when implement todos look like same low-risk work (lean candidate)."""
    impl = [t for t in plan.todos if not VERIFY_ID_RE.search(t.id)]
    if len(impl) < 2:
        return False
    doc_like = sum(
        1
        for t in impl
        if "docs/" in t.content.lower()
        or re.search(r"\b(?:write|create|update|add)\b.*\bdocs/", t.content, re.I)
    )
    if doc_like >= max(2, int(len(impl) * 0.75)):
        return True
    verb_hits = 0
    for t in impl:
        m = IMPLEMENT_LIKE_RE.match(t.content.strip())
        if m and m.group(1).lower() in ("write", "create", "update", "add"):
            verb_hits += 1
    return verb_hits >= max(2, int(len(impl) * 0.75))


def detect_redundant_grep_verify(plan: PlanData) -> bool:
    """True when a verify todo only repeats grep/test from prior implement todo."""
    for i, t in enumerate(plan.todos):
        if not VERIFY_ID_RE.search(t.id) or i == 0:
            continue
        prev = plan.todos[i - 1]
        if VERIFY_ID_RE.search(prev.id):
            continue
        if not re.match(r"^(?:Confirm|Run|test -f|grep)", t.content.strip(), re.I):
            continue
        paths = set(PATH_RE.findall(prev.content)) | set(
            m.group(1) or m.group(2) or ""
            for m in FILE_REF_RE.finditer(prev.content)
            if m.group(1) or m.group(2)
        )
        paths = {p for p in paths if p}
        if paths and all(p in t.content for p in paths):
            return True
    return False


def phase_balance_classification(
    phase_rows: list[PhaseChunkMetrics],
) -> tuple[list[tuple[str, float]], list[tuple[str, float]], float]:
    """Over/under vs median phase weight (sum of todo weights). Needs ≥2 phases."""
    if len(phase_rows) < 2:
        return [], [], 0.0
    weights = sorted(pr.total_weight for pr in phase_rows)
    median = weights[len(weights) // 2]
    if median <= 0:
        return [], [], 0.0
    heavier_than = median * PHASE_BALANCE_RATIO
    lighter_than = median / PHASE_BALANCE_RATIO
    overweight = [
        (pr.name, pr.total_weight)
        for pr in phase_rows
        if pr.total_weight > heavier_than
    ]
    underweight = [
        (pr.name, pr.total_weight)
        for pr in phase_rows
        if pr.total_weight < lighter_than
    ]
    overweight.sort(key=lambda x: x[1], reverse=True)
    underweight.sort(key=lambda x: x[1])
    return overweight, underweight, median


@dataclass
class ChunkReportData:
    plan_path: str
    metrics: PlanMetrics
    todo_rows: list[TodoMetrics]
    phase_rows: list[PhaseChunkMetrics]
    plan_weight: float
    plan_context_weight: float
    plan_band: str
    plan_complexity: str
    mermaid_blocks: int
    mermaid_lines: int
    ref_file_count: int
    ref_files: list[tuple[str, int | None, str]]
    ref_bytes_total: int
    split_suggestions: list[ChunkSplitSuggestion]
    plan_markers: list[ChunkMarker]
    phase_count: int
    todos_per_phase_avg: float
    body_tokens_per_phase: float
    agent_brief: ChunkAgentBrief


def _marker_status(value: float, threshold: float, higher_is_bad: bool = True) -> str:
    if higher_is_bad:
        if value >= threshold:
            return "trigger"
        if value >= threshold * 0.75:
            return "watch"
        return "ok"
    if value <= threshold:
        return "trigger"
    if value <= threshold * 1.25:
        return "watch"
    return "ok"


def build_agent_brief(
    plan_context_weight: float,
    plan_weight: float,
    recommended_phases: int,
    current_phases: int,
    suggestions: list[ChunkSplitSuggestion],
    todo_rows: list[TodoMetrics],
    phase_rows: list[PhaseChunkMetrics],
    *,
    homogeneous_work_suggested: bool = False,
    redundant_grep_verify: bool = False,
) -> ChunkAgentBrief:
    overweight, underweight, _median = phase_balance_classification(phase_rows)
    return ChunkAgentBrief(
        recommended_phases=recommended_phases,
        current_phases=current_phases,
        plan_context_weight=plan_context_weight,
        plan_weight=plan_weight,
        phases_may_require_splitting=[
            s.target for s in suggestions if s.action == "split_phase"
        ],
        todos_may_require_splitting=[
            s.target for s in suggestions if s.action == "split_todo"
        ],
        merge_phases_suggested=any(s.action == "merge_phases" for s in suggestions),
        add_phases_suggested=recommended_phases > current_phases,
        homogeneous_work_suggested=homogeneous_work_suggested,
        redundant_grep_verify=redundant_grep_verify,
        individual_todo_weights=[
            (tm.todo.id, tm.weight)
            for tm in sorted(todo_rows, key=lambda x: x.todo.id)
        ],
        overweighted_phases=overweight,
        underweighted_phases=underweight,
    )


def _format_phase_balance_list(phases: list[tuple[str, float]]) -> str:
    if not phases:
        return "none"
    return ", ".join(f"{name} (weight {w})" for name, w in phases)


def format_agent_brief_lines(brief: ChunkAgentBrief) -> list[str]:
    def _join(names: list[str]) -> str:
        return ", ".join(names) if names else "none"

    heavy = [
        (tid, w)
        for tid, w in brief.individual_todo_weights
        if w >= TODO_WEIGHT_WATCH
    ]
    heavy.sort(key=lambda x: x[1], reverse=True)
    heavy_line = (
        ", ".join(f"{tid}={w}" for tid, w in heavy)
        if heavy
        else f"none (watch threshold {TODO_WEIGHT_WATCH})"
    )

    lines = [
        "## Chunk report (pass 2)",
        "",
        f"**Phases:** recommend {brief.recommended_phases} "
        f"(current {brief.current_phases}; plan weight {brief.plan_weight})",
        f"**Overweighted phases:** {_format_phase_balance_list(brief.overweighted_phases)}",
        f"**Underweighted phases:** {_format_phase_balance_list(brief.underweighted_phases)}",
        f"**Phase splits:** {_join(brief.phases_may_require_splitting)}",
        f"**Todo splits:** {_join(brief.todos_may_require_splitting)}",
        f"**Heavy todos (≥{TODO_WEIGHT_WATCH}, split at {TODO_WEIGHT_SPLIT}):** {heavy_line}",
    ]
    flags: list[str] = []
    if brief.merge_phases_suggested:
        flags.append("merge_phases (do not add more phases)")
    if brief.add_phases_suggested:
        flags.append("add_phases")
    if brief.homogeneous_work_suggested:
        flags.append("homogeneous_work (lean candidate)")
    if brief.redundant_grep_verify:
        flags.append("redundant_grep_verify (dismissible under lean)")
    if flags:
        lines.append(f"**Flags:** {'; '.join(flags)}")
    lines.append("")
    lines.append("_Judge from this block and split actions._")
    return lines


def format_split_summary_lines(
    suggestions: list[ChunkSplitSuggestion],
) -> list[str]:
    if not suggestions:
        return ["**Split actions:** none"]
    parts = [f"{s.action} → {s.target}" for s in suggestions]
    return [f"**Split actions:** {'; '.join(parts)}"]


def evaluate_chunk_splits(
    metrics: PlanMetrics,
    phase_rows: list[PhaseChunkMetrics],
    todo_rows: list[TodoMetrics],
    phase_count: int,
    body_tokens_per_phase: float,
    todos_per_phase_avg: float,
    mermaid_lines: int,
    ref_bytes: int,
    ref_file_count: int,
) -> tuple[list[ChunkSplitSuggestion], list[ChunkMarker]]:
    suggestions: list[ChunkSplitSuggestion] = []
    markers: list[ChunkMarker] = []

    markers.append(
        ChunkMarker(
            "body_tokens_per_phase",
            round(body_tokens_per_phase, 1),
            float(BODY_TOKENS_PER_PHASE_ADD),
            _marker_status(body_tokens_per_phase, BODY_TOKENS_PER_PHASE_ADD),
            "High → plan may need more phases (if not over-phased)",
        )
    )
    markers.append(
        ChunkMarker(
            "phase_count",
            float(phase_count),
            float(PHASES_MAX_BEFORE_MERGE_SIGNAL),
            _marker_status(float(phase_count), float(PHASES_MAX_BEFORE_MERGE_SIGNAL)),
            "Very high with few todos each → merge_phases, not add_phases",
        )
    )
    markers.append(
        ChunkMarker(
            "referenced_file_count",
            float(ref_file_count),
            float(REF_FILE_COUNT_MARKER_THRESHOLD),
            _marker_status(float(ref_file_count), float(REF_FILE_COUNT_MARKER_THRESHOLD)),
            "Many distinct file refs (paths + bare names) → heavier plan context",
        )
    )
    markers.append(
        ChunkMarker(
            "referenced_files_kib",
            round(ref_bytes / 1024.0, 1),
            round(REF_BYTES_PLAN_HEAVY / 1024.0, 1),
            _marker_status(ref_bytes, REF_BYTES_PLAN_HEAVY),
            "Large refs → more context per Build; consider narrower todos",
        )
    )
    markers.append(
        ChunkMarker(
            "mermaid_lines",
            float(mermaid_lines),
            float(MERMAID_LINES_HEAVY),
            _marker_status(mermaid_lines, MERMAID_LINES_HEAVY),
            "Large diagrams → planning complexity",
        )
    )

    over_phased = _is_over_phased(
        phase_count, todos_per_phase_avg, metrics.todo_count
    )
    if over_phased:
        suggestions.append(
            ChunkSplitSuggestion(
                action="merge_phases",
                target="(whole plan)",
                metric_value=round(todos_per_phase_avg, 1),
                band="high",
                why=[
                    f"{phase_count} phases with avg {todos_per_phase_avg:.1f} todos/phase "
                    f"(<{TODOS_PER_PHASE_MERGE_SIGNAL})",
                    "Do not add more phases — merge or flatten milestones",
                ],
            )
        )

    # 3 — Todo too large
    for tm in todo_rows:
        if tm.weight >= TODO_WEIGHT_SPLIT:
            suggestions.append(
                ChunkSplitSuggestion(
                    action="split_todo",
                    target=tm.todo.id,
                    metric_value=tm.weight,
                    band=_complexity_band(tm.weight, 2.0, TODO_WEIGHT_SPLIT),
                    why=tm.why or [f"todo weight {tm.weight} >= {TODO_WEIGHT_SPLIT}"],
                )
            )

    # 2 — Phase too large (split this phase into more phases)
    for pr in phase_rows:
        phase_why = phase_split_reasons(pr, phase_rows)
        if phase_why:
            suggestions.append(
                ChunkSplitSuggestion(
                    action="split_phase",
                    target=pr.name,
                    metric_value=pr.total_weight,
                    band=pr.complexity,
                    why=phase_why,
                )
            )

    suggestions.sort(key=lambda s: s.metric_value, reverse=True)
    return suggestions, markers


def build_chunk_report(
    plan: PlanData,
    estimates: dict[str, dict[str, str]],
    workspace: Path | None = None,
) -> ChunkReportData:
    metrics = compute_plan_metrics(plan)
    ws = resolve_workspace_root(plan, workspace)
    phases = phases_for_chunking(plan)
    phase_count = max(1, len(phases))
    todo_count = max(1, len(plan.todos))
    todos_per_phase_avg = metrics.todo_count / phase_count
    body_tokens_per_phase = metrics.body_tokens_est / phase_count

    m_blocks, m_lines, _m_nodes = mermaid_metrics(plan.body)
    ref_stats = referenced_file_stats(plan, ws)
    ref_bytes = sum(b or 0 for _, b, st in ref_stats if st in ("ok", "heavy", "large"))
    ref_file_count = len(ref_stats)

    plan_context_weight = compute_plan_context_weight(
        metrics.body_tokens_est,
        m_lines,
        ref_file_count,
        ref_bytes,
        phase_count,
        metrics.todo_count,
    )

    todo_rows: list[TodoMetrics] = []
    for i, todo in enumerate(plan.todos):
        todo.index = i
        todo_rows.append(
            build_todo_chunk_metrics(
                todo, plan, estimates, ws, plan_context_weight, todo_count
            )
        )

    phase_rows: list[PhaseChunkMetrics] = []
    for name, ptodos in phases:
        weights = []
        for t in ptodos:
            tm = next((r for r in todo_rows if r.todo.id == t.id), None)
            weights.append(tm.weight if tm else 0.0)
        total = sum(weights)
        mx = max(weights) if weights else 0.0
        avg = total / max(1, len(weights))
        complexity = _complexity_band(total, 3.0, PHASE_TOTAL_WEIGHT_SPLIT)
        phase_rows.append(
            PhaseChunkMetrics(
                name=name,
                todo_count=len(ptodos),
                total_weight=round(total, 2),
                max_todo_weight=round(mx, 2),
                avg_weight=round(avg, 2),
                band=complexity,
                complexity=complexity,
            )
        )

    plan_weight = compute_total_plan_weight(plan_context_weight, phase_rows)
    plan_band = _complexity_band(plan_weight, 5.0, PLAN_HEAVY_THRESHOLD)
    plan_complexity = plan_band

    over_phased = _is_over_phased(
        phase_count, todos_per_phase_avg, metrics.todo_count
    )
    homogeneous = detect_homogeneous_work(plan)
    redundant_grep = detect_redundant_grep_verify(plan)

    suggestions, plan_markers = evaluate_chunk_splits(
        metrics,
        phase_rows,
        todo_rows,
        phase_count,
        body_tokens_per_phase,
        todos_per_phase_avg,
        m_lines,
        ref_bytes,
        ref_file_count,
    )

    recommended_phases = recommend_phase_count(
        plan_weight,
        over_phased,
        phase_count,
    )

    agent_brief = build_agent_brief(
        plan_context_weight,
        plan_weight,
        recommended_phases,
        phase_count,
        suggestions,
        todo_rows,
        phase_rows,
        homogeneous_work_suggested=homogeneous,
        redundant_grep_verify=redundant_grep,
    )

    return ChunkReportData(
        plan_path=str(plan.path),
        metrics=metrics,
        todo_rows=todo_rows,
        phase_rows=phase_rows,
        plan_weight=plan_weight,
        plan_context_weight=plan_context_weight,
        plan_band=plan_band,
        plan_complexity=plan_complexity,
        mermaid_blocks=m_blocks,
        mermaid_lines=m_lines,
        ref_file_count=ref_file_count,
        ref_files=ref_stats,
        ref_bytes_total=ref_bytes,
        split_suggestions=suggestions,
        plan_markers=plan_markers,
        phase_count=phase_count,
        todos_per_phase_avg=round(todos_per_phase_avg, 1),
        body_tokens_per_phase=round(body_tokens_per_phase, 1),
        agent_brief=agent_brief,
    )


# --- Structural validation (plan-validate-close) ---


def _normalize_title_text(text: str) -> str:
    return " ".join(text.strip().split())


def _body_h1_title(body: str) -> tuple[str | None, str | None]:
    """Return (title, error_code) — first non-empty body line must be the only H1."""
    h1_titles: list[str] = []
    started = False
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# ") and not stripped.startswith("##"):
            text = stripped[2:].strip()
            if not text:
                return None, "empty_title"
            h1_titles.append(text)
            started = True
            continue
        if not started:
            if stripped.startswith("##"):
                return None, "missing_title"
            return None, "content_before_title"
    if not h1_titles:
        return None, "missing_title"
    if len(h1_titles) > 1:
        return None, "multiple_titles"
    return h1_titles[0], None


def _body_h2_headings(body: str) -> list[str]:
    headings: list[str] = []
    for line in body.splitlines():
        if line.startswith("## ") and not line.startswith("###"):
            headings.append(line[3:].strip())
    return headings


def validate_body_outline(plan: PlanData) -> list[ValidationIssue]:
    """Title H1 + §1–10 ## headings in OUTPUTS.md order (owcc-plan-improve)."""
    issues: list[ValidationIssue] = []
    title, title_err = _body_h1_title(plan.body)
    if title_err == "missing_title":
        issues.append(
            ValidationIssue(
                "error",
                "missing_title",
                "Plan body must start with a single # title H1 (see owcc-plan-improve OUTPUTS.md)",
            )
        )
    elif title_err == "empty_title":
        issues.append(ValidationIssue("error", "empty_title", "Plan title H1 is empty"))
    elif title_err == "multiple_titles":
        issues.append(
            ValidationIssue(
                "error",
                "multiple_titles",
                "Plan body has more than one # H1 — use one title only",
            )
        )
    elif title_err == "content_before_title":
        issues.append(
            ValidationIssue(
                "error",
                "content_before_title",
                "Plan body has content before the # title H1",
            )
        )

    name = plan.meta.get("name")
    if title and isinstance(name, str) and name.strip():
        if _normalize_title_text(title) != _normalize_title_text(name):
            issues.append(
                ValidationIssue(
                    "error",
                    "title_name_mismatch",
                    f"Body title H1 must match frontmatter name: "
                    f"'{_normalize_title_text(title)}' vs '{_normalize_title_text(name)}'",
                )
            )

    found = _body_h2_headings(plan.body)
    expected = list(PLAN_BODY_SECTION_HEADINGS)
    if found != expected:
        if len(found) != len(expected):
            issues.append(
                ValidationIssue(
                    "error",
                    "section_count",
                    f"Plan body must have exactly {len(expected)} ## sections "
                    f"(Rules … Reference); found {len(found)}",
                )
            )
        for i, exp in enumerate(expected):
            if i >= len(found):
                break
            if found[i] != exp:
                issues.append(
                    ValidationIssue(
                        "error",
                        "section_order",
                        f"Expected ## {exp} at section position {i + 1}, "
                        f"found ## {found[i]}",
                    )
                )
                break
        missing = [h for h in expected if h not in found]
        extra = [h for h in found if h not in expected]
        if missing and not any(i.code == "section_order" for i in issues):
            issues.append(
                ValidationIssue(
                    "error",
                    "missing_sections",
                    "Missing required sections: " + ", ".join(missing),
                )
            )
        if extra and not any(i.code == "section_order" for i in issues):
            issues.append(
                ValidationIssue(
                    "error",
                    "extra_sections",
                    "Unexpected or misordered sections: " + ", ".join(extra),
                )
            )
    return issues


@dataclass
class ValidationIssue:
    severity: str  # error | warn
    code: str
    message: str


def validate_structure(plan: PlanData) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_body_outline(plan))
    todos = plan.todos

    if not todos:
        issues.append(ValidationIssue("error", "no_todos", "No todos found in frontmatter"))

    if re.search(r"^###\s+Progress tracking\s*$", plan.body, re.MULTILINE | re.IGNORECASE):
        issues.append(
            ValidationIssue(
                "error",
                "progress_tracking_section",
                "Plan body has ### Progress tracking — remove; use todos/phases only",
            )
        )

    if plan.is_project:
        phases = plan.meta.get("phases")
        if not phases:
            issues.append(
                ValidationIssue(
                    "error",
                    "isproject_no_phases",
                    "isProject: true but phases array is missing or empty",
                )
            )
        elif isinstance(phases, list):
            for i, phase in enumerate(phases):
                if not isinstance(phase, dict):
                    continue
                name = phase.get("name") or f"phase-{i}"
                ptodos = phase.get("todos") or []
                if not ptodos:
                    issues.append(
                        ValidationIssue("error", "empty_phase", f"Phase '{name}' has no todos")
                    )
                    continue
                def _is_phase_validation_todo(todo: dict) -> bool:
                    lid = str(todo.get("id", "")).lower()
                    lcontent = _content_str(todo.get("content")).lower()
                    return (
                        "validate-phase" in lid
                        or lid.startswith("phase-validation")
                        or "phase validation" in lcontent
                        or "phase gate" in lcontent
                    )

                def _is_final_validation_todo(todo: dict) -> bool:
                    lid = str(todo.get("id", "")).lower()
                    lcontent = _content_str(todo.get("content")).lower()
                    return (
                        "completion-audit" in lid
                        or "final-validation" in lid
                        or lid.endswith("-audit")
                        or "final validation" in lcontent
                        or "completion audit" in lcontent
                    )

                last = ptodos[-1]
                if isinstance(last, dict):
                    last_ok = _is_phase_validation_todo(last)
                    if not last_ok and _is_final_validation_todo(last) and len(ptodos) >= 2:
                        penultimate = ptodos[-2]
                        if isinstance(penultimate, dict):
                            last_ok = _is_phase_validation_todo(penultimate)
                    if not last_ok:
                        issues.append(
                            ValidationIssue(
                                "error",
                                "missing_phase_validation",
                                f"Phase '{name}' lacks phase-validation todo "
                                f"(last or penultimate when last is completion-audit)",
                            )
                        )
    else:
        flat = plan.meta.get("todos") or []
        if plan.is_project and flat:
            issues.append(
                ValidationIssue(
                    "warn",
                    "duplicate_flat_todos",
                    "isProject plan still has root todos — prefer phases as source of truth",
                )
            )

    seen_ids: set[str] = set()
    for t in todos:
        if not t.id:
            issues.append(ValidationIssue("error", "missing_id", "Todo missing id"))
            continue
        if t.id in seen_ids:
            issues.append(ValidationIssue("error", "duplicate_id", f"Duplicate todo id: {t.id}"))
        seen_ids.add(t.id)
        if t.status not in VALID_STATUSES:
            issues.append(
                ValidationIssue(
                    "error",
                    "bad_status",
                    f"Todo '{t.id}' has invalid status '{t.status}'",
                )
            )

    for i, t in enumerate(todos):
        if implement_needs_verify(todos, i):
            issues.append(
                ValidationIssue(
                    "warn",
                    "missing_verify",
                    f"Implement-like todo '{t.id}' has no verify coverage",
                )
            )

    final_ok = False
    if todos:
        last = todos[-1]
        lid = last.id.lower()
        lcontent = last.content.lower()
        final_ok = (
            "completion-audit" in lid
            or "final-validation" in lid
            or lid.endswith("-audit")
            or "final validation" in lcontent
            or "completion audit" in lcontent
        )
    if todos and not final_ok:
        issues.append(
            ValidationIssue(
                "error",
                "missing_final_validation",
                "Last todo is not a final-validation / completion-audit gate",
            )
        )

    has_edit_rule = bool(
        re.search(r"(?i)plan\s+file\s+edit\s+rule", plan.body)
        and re.search(r"(?i)status-only\s+exception", plan.body)
    )
    if (
        is_buildable_plan(plan)
        and not has_edit_rule
        and re.search(r"(?i)update\s+`?status`?\s+in\s+frontmatter", plan.body)
    ):
        issues.append(
            ValidationIssue(
                "warn",
                "body_status_edit",
                "Plan mentions updating frontmatter status without Plan file edit rule (status-only exception)",
            )
        )

    return issues


def _slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-") or "plan"


def plan_report_basename(plan_path: str | Path) -> str:
    """Slugified frontmatter name: or plan file stem."""
    plan = read_plan(plan_path)
    name = plan.meta.get("name")
    if isinstance(name, str) and name.strip():
        return _slugify(name.strip())
    return Path(plan_path).stem


def validation_report_path(
    plan_path: str | Path, workspace: Path | None = None
) -> Path:
    """Full path for .cursor/plans/reports/<plan-name>.validation.json."""
    plan = read_plan(plan_path)
    ws = resolve_workspace_root(plan, workspace)
    basename = plan_report_basename(plan_path)
    return ws / ".cursor" / "plans" / "reports" / f"{basename}.validation.json"
