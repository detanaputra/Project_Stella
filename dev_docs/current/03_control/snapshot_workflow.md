# Snapshot Workflow

#control #workflow #traceability #shapr

## Purpose
Define the standard snapshot process used to create clear SHAPR cycle boundaries in this project.

This note is a reusable control note. It is **not** a cycle narrative and should stay stable across cycles.

## Core Principle

> `dev_docs/current/` is the active working source of truth.
> A snapshot is a frozen copy of `dev_docs/current/` at a cycle boundary — the handoff artefact for the next chat/cycle.

## Working Rule

### Active working set
Everything that participates in the current cycle lives under `dev_docs/current/`:
- system notes (`01_system/`)
- contract notes (`02_contracts/`)
- control notes (`03_control/`)
- working notes (`04_working/`)
- knowledge notes (`05_knowledge/`)

Stable/historical folders stay outside `current/` (never copied into snapshots):
- `dev_docs/cycle_record_notes/` — the formal cycle records and reviews (themselves the historical record)
- `dev_docs/llm_guidance/` — the instruction files
- `dev_docs/snapshots/` — the frozen copies

### Snapshot set
Create a snapshot only at meaningful milestones:
- end of a cycle
- first runnable version flow
- major architecture shift
- pre-refactor baseline
- pre-new-chat handoff

## Standard Snapshot Procedure

### 1. Review current notes
Before snapshotting:
- update `dev_docs/current/04_working/current_state.md`
- update `dev_docs/current/04_working/tasks.md`
- ensure control notes reflect actual decisions
- remove or fix obvious inconsistencies

### 2. Freeze the current state
Treat `dev_docs/current/` as the source of truth for the snapshot.

### 3. Create snapshot copy
Copy the whole `current/` folder into a cycle snapshot folder:

`cp -r dev_docs/current dev_docs/snapshots/cycle_<N>_close/`

So `dev_docs/snapshots/cycle_<N>_close/` holds a frozen copy of `01_system/`, `02_contracts/`, `03_control/`, `04_working/`, and `05_knowledge/` (`cycle_record_notes/` stays outside `current/` — it is already the historical record). Optionally also produce a zipped handoff package for the next chat.

### 4. Preserve traceability
The snapshot should preserve: control, working, knowledge, contract, and cycle-record notes. **Do not modify a snapshot after it is frozen.**

### 5. Use snapshot as handoff artefact
When starting a new chat or new cycle:
- treat the snapshot as the formal handoff artefact
- continue development from the frozen state plus any explicit new decisions

## What Should Be Updated Before a Snapshot

Minimum update set:
- `current_state.md`
- `tasks.md`
- relevant changed control/decision notes
- formal cycle record and review if closing a cycle

## What Should Not Go Into This Note

Do not place here:
- current cycle achievements
- cycle-specific reflections
- temporary task lists
- narrative progress updates

Those belong in: `current_state.md`, `tasks.md`, formal cycle records, `reflection.md`/`paper.md`.

## Current State

`dev_docs/snapshots/cycle_1_close/` was taken **before** the `current/` layout existed — it holds the pre-reorg doc set (guide, untriaged SKUs, 03_control, 05_knowledge, cycle records, llm_guidance) and is frozen as-is. From cycle 2 onward, snapshots are created by copying `dev_docs/current/` into `dev_docs/snapshots/cycle_N_close/` per Step 3 above.

## Related
- `dev_docs/current/03_control/repository_structure.md`
- `dev_docs/current/04_working/source_of_truth.md`
