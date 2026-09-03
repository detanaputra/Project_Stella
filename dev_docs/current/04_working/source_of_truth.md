# Source of Truth

#working #control #source_of_truth

## Purpose
Defines which artefacts are authoritative for different kinds of truth in this project.

Reduces ambiguity when:
- code and notes evolve at different speeds
- multiple markdown files overlap in subject matter
- a new chat begins with only a subset of project artefacts
- AI assistance is used for design, coding, or review

Include this file in cycle-start handoff bundles.

## Core Principle
Different files serve different roles. Authority is assigned by role, not by recency.

## Authority Map

### 1. Implementation truth
**Authoritative artefact:** the codebase (`app/`, `main.py`)

The code is the primary source of truth for what currently exists, what functions/modules actually do, what interfaces are implemented, and what behaviour is runnable.

If a markdown note conflicts with the current code, the code is assumed to represent implementation truth unless the current task is explicitly to change the code to match the note.

### 2. Active phase truth
**Authoritative artefact:** `current_state.md`

Primary source of truth for: current project position, active cycle/phase, current development focus, what is stable / in progress / deferred, and the immediate next step.

### 3. Cycle-start control truth
**Authoritative artefact:** `current_state.md`

At cycle start, `current_state.md` is the authoritative note for active cycle framing, scope, priorities, implementation position, and immediate next-step control. This project does not use a separate cycle-start control note by default.

`cycle_record_notes/cycle_n.md` and `cycle_n_review.md` are **cycle-end artefacts**, not cycle-start control notes.

### 4. File authority and control truth
**Authoritative artefact:** `source_of_truth.md` (this file)

Primary source of truth for: which files are authoritative for which roles, how to interpret conflicts, and which notes are active control artefacts.

### 5. Task truth
**Authoritative artefact:** `tasks.md`

Primary source of truth for: what work is planned, what is active, what to do next, and minimum completion targets. It is an execution note, not a design-rationale note.

### 6. Decision and rationale truth
**Authoritative artefact:** `dev_docs/current/03_control/decisions.md`

Primary source of truth for: why important design choices were made, which decisions are accepted, what trade-offs were chosen, and what governs the current phase until explicitly revised. `cycle_record_notes` point here instead of duplicating rationale.

### 7. Plan / roadmap truth
**Authoritative artefact:** `dev_docs/current/04_working/cycle_plan.md`

Primary source of truth for the version/cycle roadmap: what each version is mainly trying to achieve and its status. Review at cycle end.

### 8. Subsystem design truth
**Authoritative artefact:** the relevant design doc — `dev_docs/current/01_system/architecture.md` (structural), `dev_docs/current/02_contracts/api.md` (component interfaces), `dev_docs/current/02_contracts/bertopic_hyperparams.md` (algorithm parameters), plus focused notes under `dev_docs/`.

Authoritative only within their own subsystem and only if they have not fallen behind the current phase. If a focused design note has drifted behind `current_state.md`, `decisions.md`, and the codebase, treat it as background until refreshed.

### 9. Contract truth
**Authoritative artefact:** the contract roles — `dev_docs/current/02_contracts/api.md` (function/data contracts), `dev_docs/current/02_contracts/bertopic_hyperparams.md` (parameter contract), `dev_docs/current/02_contracts/code_map.md` (note↔code mapping).

If code and contract disagree → the disagreement is **drift**; the current task must explicitly decide whether to update the code, the contract, or both.

### 10. Knowledge truth
**Authoritative artefact:** the SKU files (`dev_docs/current/05_knowledge/skus/`) and `dev_docs/current/05_knowledge/reflection.md`.

Historical record of insights and learnings. Consult for precedent, but it does not govern the current phase.

## Conflict Resolution Rule

If artefacts disagree, resolve in this order:

1. active task instruction in the current chat
2. uploaded codebase for implementation truth
3. `current_state.md` for active phase truth
4. `source_of_truth.md` for file authority and conflict interpretation
5. `decisions.md` for accepted rationale
6. focused design or contract notes (`dev_docs/current/01_system/architecture.md`, `dev_docs/current/02_contracts/api.md`, `dev_docs/current/02_contracts/bertopic_hyperparams.md`, `dev_docs/current/02_contracts/code_map.md`) for subsystem guidance
7. older background notes / historical knowledge (SKU files, cycle records)

Apply this order consciously when drift is detected.

## Chat-Start Handoff Rule

Default handoff set for a new development chat:

- the current codebase (`app/`)
- `current_state.md`
- `source_of_truth.md`
- `dev_docs/current/03_control/repository_structure.md` (file roles)
- only additional notes directly relevant to that chat's task
- `dev_docs/llm_guidance/` instruction files relevant to the task

## Cycle-End Artefact Rule

`cycle_n.md` and `cycle_n_review.md` are cycle-end formal records, review artefacts, and historical evidence. They are valuable for traceability, reflection, and handoff into the next cycle — but they are not the primary cycle-start control notes.

## Practical Working Rule

At the start of a chat, do not assume all uploaded notes are equally important. Identify the active task, identify which files are authoritative for that task, and treat the rest as supporting context only.

## Review Rule

Review this file when the project structure changes substantially, new authoritative notes are introduced, the cycle workflow changes, or note drift recurs despite the current control pattern. The goal is clear authority and reduced drift, not bureaucratic completeness.
