# Working Docs Instruction

How to maintain the **live working set** (`04_working` in the example): `current_state.md`, `source_of_truth.md`, `tasks.md`, `cycle_plan.md`, `ideas.md`.

Source: `example_docs/current/04_working/`.

These are the *mutable* notes updated during a cycle and consolidated at cycle boundaries. They are the input to cycle records, not the records themselves.

## The authority map (`source_of_truth.md`)

This is the project's **file-authority map** — which artefact is authoritative for which kind of truth. Its purpose is to stop document drift when code and notes evolve at different speeds, multiple notes overlap, or a new chat starts with only a subset of artefacts.

**Authority by role:**

| Kind of truth | Authoritative artefact |
|---|---|
| Implementation | uploaded **codebase** (what exists, what runs) |
| Active phase | `current_state.md` |
| Cycle-start control | `current_state.md` (not a separate note) |
| File authority / conflict interpretation | `source_of_truth.md` |
| Task truth | `tasks.md` (execution note, not design rationale) |
| Decision & rationale | `decisions.md` |
| Subsystem design | the focused design note (e.g. `architecture.md`, `indicator_engine.md`) |
| Contract | the contract note (`function_contracts.md`, `data_contracts.md`, `naming_conventions.md`, `code_map.md`) |

**Conflict Resolution Rule** — if artefacts disagree, resolve in this order:
1. active task instruction in the current chat
2. uploaded codebase (implementation truth)
3. `current_state.md` (active phase truth)
4. `source_of_truth.md` (file authority)
5. `decisions.md` (accepted rationale)
6. focused design / contract notes
7. older background notes

**Chat-Start Handoff Rule** (from cycle 3 onward): the default handoff set for a new development chat is *the codebase + `current_state.md` + `source_of_truth.md` + only task-relevant notes*. This keeps AI-assisted work accurate and controllable.

If code and contract disagree → treat as **drift**; the current task must explicitly decide whether to update code, update contract, or both.

## `current_state.md`

The single live status note: current position, active cycle/phase, what's stable / in progress / deferred, immediate next step. It is authoritative for describing the present phase over older or broader notes. At cycle start it becomes the cycle-start control note.

## `tasks.md`

Execution truth. Conventions:
- **Working Rule:** append brief points during active development; consolidation happens at checkpoints and cycle end.
- When choosing between options: *prefer the smaller implementation · prefer the more traceable implementation · prefer the one that gets the next working step done cleanly.*
- Checkbox groups (`- [x]` / `- [ ]`) organized by cycle phase (e.g. "Cycle N Close Tasks", "Cycle N+1 Opening Tasks", "Deferred to Later Cycles", "Small Operational Tasks").

## `cycle_plan.md`

The multi-cycle roadmap. Per-cycle entry fields:
- **Main goal** — the one-sentence aim.
- **Main outcomes** — bullet list of concrete deliverables.
- **Primary focus** — the priorities (optional; used for later cycles).
- **Success signal** — how you know the cycle achieved its aim.
- **Status** — one of `Completed.` / `Completed and ready to close.` / `Planned.`

Plus a "Working Principles" block (e.g. small controlled enhancements over uncontrolled expansion; note consolidation is a checkpoint activity, not continuous) and a Review Rule (review at cycle end, major shifts, drift).

## `ideas.md`

Raw capture of undeveloped ideas — no format pressure; it is a holding area.

## Append-first capture rule (applies to all working docs)

During active development: append short bullets, don't chase perfect placement, consolidate later. This is the core anti-burnout rule — *if documentation slows you down, you are doing too much.*

## Current state

This folder is **guidance only** — it does not track the project's current state. For live state, see the authoritative working docs: `dev_docs/current/04_working/current_state.md` (active phase), `dev_docs/current/04_working/source_of_truth.md` (file authority), and `dev_docs/current/03_control/repository_structure.md` (repo layout).
