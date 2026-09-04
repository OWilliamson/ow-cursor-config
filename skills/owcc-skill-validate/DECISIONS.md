# Decisions

Enumerated decisions for `/owcc-skill-validate`, IN **[SKILL.md](SKILL.md)** workflow order. Norms source: [../owcc-skill-improve/VALIDATION.md](../owcc-skill-improve/VALIDATION.md).

## 1. Target skill directory

**Workflow:** 5.3.1

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Absolute path** | Directory containing `SKILL.md` | Operator gave a path | That directory |
| **@ attachment** | Resolve folder of attached `SKILL.md` or skill folder | `@` on skill file/folder | Package root |
| **Pasted package** | Content only; ask for path IF needed for report | Operator pasted full package | In-memory inventory |
| **Ask once** | Do not guess | Ambiguous or missing | Chat question |

---

## 2. Shape policy

**Workflow:** 5.3.3

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Enforce new shape** | `CS-PKG-SHAPE`, `CS-PKG-SKILL-SPINE`, `CS-PKG-WORKFLOW-SYNC`, no live `reference-*` are Critical | Always (no legacy mode) | Every target audit |

---

## 3. Agent question filter

**Workflow:** 5.3.3 / §6.2

| Option | Description | Choose when | Apply to |
|--------|-------------|-------------|----------|
| **Run** | Ask mechanical/shape/CS-* questions from improve VALIDATION | Always for structure and norms | Agent questions list |
| **Skip** | Do not ask fidelity gate, improve RESPONSE readiness, or self-improve dual-target | Always for those improve-only items | Filtered out |
| **Override failure** | On fail: report AND stop; never RETURN TO improve §5 to fix | Always | Failure handling |
