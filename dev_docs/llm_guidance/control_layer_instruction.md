# Control Layer Instruction

How to maintain the **process/governance layer** (`03_control` in the example): `decisions.md`, `snapshot_workflow.md`, `coding_protocol.md`, `implementation_stack.md`, `repository_structure.md`, `shapr_obsidian_setup.md`.

Source: `example_docs/current/03_control/`.

Control notes are **reusable and stable across cycles** — they are *not* cycle narratives. Update them when the process changes, not per cycle.

## `decisions.md` — the decision log (most-used file here)

An ADR-style log: *source of truth for design decisions and rationale.* It evolves across cycles.

**Simple Notes Capture Rule** (top of the file): append short bullet points during active development; consolidation happens at cycle end. Append when a point is about something you *decided*, something you want to *lock for now*, or something that *affects implementation consistency*. Formalise later.

**Entry formats** — three have been used; match the level of the decision:

1. **Early simple entries** (DD-001…DD-004):
   ```
   ## DD-001
   ### Decision
   Use a modular architecture separating core components.
   ### Why
   Improves traceability, reuse, and extensibility.
   ### Status
   ### Notes
   ```
2. **Titled entries** (D-005…D-020), grouped under cycle-boundary headings (`## Cycle 1 Decisions`, `## Cycle 1 / Cycle 2 Boundary Decisions`, `## Cycle 2 Opening Decisions`):
   ```
   ### D-016: Cycle 2 will prioritise backend workflow stabilisation over feature expansion
   ```
3. **Full ADR schema** (D-021 onward) — use for significant architectural decisions:
   ```
   ## D-021: <Title>
   ### Status            <- active / revised / deprecated
   ### Context
   ### Decision
   ### Rationale
   ### Consequences
   ### Review Trigger    <- when this decision should be revisited
   ```
   Optional extra fields seen: `### Operational Implications`, `### Guidance for Chat Use`, `### Constraint`.

**Quick Captures** — appended insights, kept as lightweight bullets:
```
### Cycle 4 Quick Capture — Derived signals should become a reusable market-pattern layer
```

ID scheme: `DD-###` (early) then `D-###`. Status values: `active` / `revised` / `deprecated`.

## `snapshot_workflow.md` — the cycle-boundary protocol

Defines the standard snapshot process that creates clear cycle boundaries. This note is a *reusable control note* — it must NOT contain cycle achievements or reflections (those belong in cycle records, `tasks.md`, or knowledge notes).

Core principle: `docs/current/` is the active working source of truth; **a snapshot is the frozen handoff artefact** for a cycle boundary.

**Standard procedure:**
1. Review current notes — update `current_state`, `tasks`, cycle-status note; fix inconsistencies.
2. Freeze `docs/current/` as the snapshot's source of truth.
3. Create the snapshot copy — `Cycle_01/` folder or a **zipped handoff package** for the next chat.
4. Preserve traceability — include system, contract, control, working, and knowledge notes.
5. Use the snapshot as the handoff artefact for the next chat/cycle (continue from the frozen state plus explicit new decisions).

**Minimum update set before snapshotting:** `current_state`, `tasks`, relevant changed system/contract/control notes. Preferred additional: cycle status note, formal cycle record if closing a cycle.

**Snapshot triggers:** end of cycle, first runnable V0 flow, major architecture shift, pre-refactor baseline, pre-new-chat handoff.

## `shapr_obsidian_setup.md` — the vault conventions

- **Vault structure:** `project_root/ → docs/current/ + docs/snapshots/ + code/`. During a cycle work only in `docs/current/`. At cycle end copy `current → snapshots/cycle_X` and **never modify snapshots**.
- **Graph pollution:** exclude `docs/snapshots/` in Obsidian (Files & Links → Excluded files) to keep the graph clean.
- **JSON vs Markdown:** humans read Markdown, systems read JSON. (Rule: *Humans read Markdown, systems read JSON.*)
- **Tag system** (also in `conventions_instruction.md`).
- **Mental model:** Folders (primary structure) → *where to go*; Tags (secondary) → *what it means*; Links → *how it connects*.

## Other control notes

- `coding_protocol.md` — the human–AI coding process rules.
- `implementation_stack.md` — the chosen tech stack and rationale.
- `repository_structure.md` — the explicit repo layout (the example treats this as worth its own note; Git and cycle snapshots have *different* roles — Git is history, snapshots are frozen handoffs).

## Current state in this repo (Stella)

`dev_docs/current/03_control/decisions.md` exists with D-001…D-019 (ADR schema, commit refs). The v0.1.1 audit (`audit.md`) and the SKU files in `dev_docs/current/05_knowledge/skus/` contain further decisions; port the substantive ones there with the full ADR schema and add commit refs as they arise.
