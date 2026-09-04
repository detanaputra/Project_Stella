# Repository Structure

#control #structure #traceability #shapr

## Purpose
Define the current repository layout and map existing (pre-SHAPR) files to their SHAPR framework roles, so future sessions — human and AI — know which artefacts are authoritative for what without re-reading everything.

This note is a **reusable control note**. Update it in the same change as any structural move.

## SHAPR role hierarchy (target)

| Role | Folder | What it holds |
|---|---|---|
| System | `01_system` | design/spec — what the system *is* (architecture, module designs) |
| Contracts | `02_contracts` | stable interfaces that anchor AI-assisted coding (function/data/naming/code_map) |
| Control | `03_control` | process/governance — how the work is run (decisions, snapshot, protocols) |
| Working | `04_working` | live operational state (current_state, tasks, source_of_truth, cycle_plan, ideas) |
| Knowledge | `05_knowledge` | research/methodological output (reflection, paper, references) |
| Cycles | `cycle_record_notes` | formal `cycle_n.md` + `cycle_n_review.md` |
| Artefact | `code/` (here: `app/`) | the research artefact |
| Evidence | `evidence/` | raw chat exports, run outputs — the proof layer |

## Current layout — existing files mapped to SHAPR roles

### Research artefact (code)
| File | Role | Notes |
|---|---|---|
| `app/` (models/views/controllers/services) | Research Artefact | The implementation truth — what actually exists and runs |
| `main.py` | Entry point | `multiprocessing.freeze_support()` for the webview process |
| `notebooks/`, `sample_dataset.csv/.xlsx` | Explore-phase artefacts / test data | — |

### System & contracts
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/current/01_system/architecture.md` | `01_system` — design/spec | Moved from root; MVC structure, data flows, patterns |
| `dev_docs/current/02_contracts/api.md` | `02_contracts` — function + data contracts | Moved from root; BaseAlgorithm, AppState, TopicResult contracts |
| `dev_docs/current/02_contracts/bertopic_hyperparams.md` | `02_contracts` — parameter contract | Moved from root; hyperparameter reference |

### Control (03)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/current/03_control/development.md` | 03_control — setup/testing/deploy protocol | Moved from root; covers setup/testing/deployment |
| `requirements.txt` | 03_control — implementation stack (pinned) | Deps only |
| `claude.md` (a.k.a. `CLAUDE.md` on case-insensitive macOS) | 03_control — AI instruction/handoff notes | Single tracked file (lowercase); not a duplicate |
| `dev_docs/current/03_control/decisions.md` | ADR decision log | Created in Cycle 1 Review |
| `dev_docs/current/03_control/repository_structure.md` | This note | |
| `dev_docs/llm_guidance/*` | 03_control — instructions for AI sessions | New; load-by-component; keeps context small |

### Working (04)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/current/04_working/cycle_plan.md` | 04_working — cycle plan | The multi-cycle roadmap (goal / outcomes / focus / success signal / status); moved from root `ROADMAP.md` |
| `dev_docs/current/04_working/ideas.md` | 04_working — ideas | Raw idea capture; refined and promoted to `cycle_plan.md` |
| `dev_docs/current/04_working/source_of_truth.md`, `current_state.md`, `tasks.md` | 04_working | Created in Cycle 1 Close hardening |

### Knowledge (05)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/llm_guidance/sku_instruction.md` | SKU definition | Distilled from arXiv 2603.25660; `guide.md` removed |
| `dev_docs/current/05_knowledge/skus/v0.1.0.md` | SKU knowledge units | 25 SKUs (SKU-01-01…25, cycle-coded; combined from 36 original; v0.1.1 merged here) |
| `dev_docs/current/05_knowledge/skus/v0.2.0.md` | SKU knowledge units | 4 SKUs (SKU-02-01…04, cycle-coded; from the design-changing commits of Cycle 2) |
| `dev_docs/current/05_knowledge/skus/v0.3.0.md` | SKU knowledge units | 3 SKUs (SKU-03-01…03, cycle-coded; WP1 — visualisation tabs) |
| `dev_docs/current/05_knowledge/reflection.md` | reflection | Created from cycle learnings |
| `dev_docs/current/05_knowledge/references.md` | references | SHAPR papers + project guides |
| `dev_docs/current/05_knowledge/paper.md` | paper | Working draft toward the research write-up |

### Cycles (evidence of the cycle)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/cycle_record_notes/cycle_1.md` | cycle record | Build cycle (v0.1.0) |
| `dev_docs/cycle_record_notes/cycle_1_review.md` | cycle review | Audit-and-release review (v0.1.1) |
| `dev_docs/cycle_record_notes/cycle_2.md` | cycle record | Build cycle (v0.2.0) |
| `dev_docs/cycle_record_notes/cycle_2_review.md` | cycle review | Review of the v0.2.0 build (verdict: Release) |
| `dev_docs/snapshots/cycle_1_close/audit.md` | Review evidence (archived) | The findings behind `cycle_1_review.md` (linked as its Evidence) |

### Evidence / raw data
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/snapshots/cycle_1_close/logs.md` | Raw interaction data (archived) | The Explore-phase proof; source for the cycle-1 SKUs. Archived at cycle-1 close; no `/evidence` home needed (transcripts are not required evidence per canonical SHAPR) |

### Reference
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/example_docs/` | Reference vault | The SHAPR example these conventions come from; not part of this project's own docs |

## Authority notes

- **Git history and cycle snapshots have different roles** (from `snapshot_workflow.md`): Git = history; snapshots = frozen handoff artefacts.
- **Source of truth by role** is defined in `dev_docs/current/04_working/source_of_truth.md` (created); the codebase remains authoritative for implementation truth.
- **Anti-drift rule:** the docs map existing files to roles; do **not** copy root docs into `dev_docs/` (copying creates drift). If a file is moved, update this note in the same change.

## Known gaps (short list)

1. ~~`04_working` empty~~ — `source_of_truth.md`, `current_state.md`, `tasks.md`, `cycle_plan.md`, `ideas.md` created.
2. ~~`ROADMAP.md` missing cycle_plan fields~~ — resolved: upgraded with goal / outcomes / focus / success signal / status.
3. ~~No `code_map.md`~~ — resolved: created in `02_contracts/`.
4. ~~`logs.md`/`logs/` not yet linked to SKU IDs or commit refs; no `/evidence` convention~~ — resolved: `logs.md` archived to `dev_docs/snapshots/cycle_1_close/`; no `/evidence` home needed (transcripts are not required evidence per canonical SHAPR).
5. ~~`audit.md` not referenced~~ — resolved: linked from `cycle_1_review.md` as its Evidence.
6. ~~`claude.md` duplicate~~ — resolved: single tracked file (lowercase `claude.md`), no duplicate.
7. SKU files triaged + cycle-coded IDs applied; v0.1.0 evidence links added (build SKUs → `7b88c71`/`f0573ff`; audit-fix SKUs → their own commits).
8. ~~`naming_conventions.md` (contracts)~~ and ~~`paper.md` (knowledge)~~ — resolved: created in `02_contracts/` and `05_knowledge/`.
9. `dev_docs/snapshots/cycle_1_close/` and `dev_docs/snapshots/cycle_2_close/` are the cycle snapshots taken so far; subsequent cycles should follow `snapshot_workflow.md`.
