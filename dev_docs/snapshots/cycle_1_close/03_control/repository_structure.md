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
| `ARCHITECTURE.md` | `01_system/architecture.md` | MVC structure, data flows, patterns — content exists at root |
| `API.md` | `02_contracts` (function + data contracts) | Component contracts (BaseAlgorithm, AppState, TopicResult) |
| `BERTopicHyperparams.md` | `02_contracts` (parameter contract) | Hyperparameter reference |

### Control (03)
| File | SHAPR role | Notes |
|---|---|---|
| `DEVELOPMENT.md` | 03_control — setup/testing/deploy protocol | Partial: covers setup/testing/deployment |
| `requirements.txt` | 03_control — implementation stack (pinned) | Deps only |
| `CLAUDE.md` / `claude.md` | 03_control — AI instruction/handoff notes | **Duplicates** (identical bytes) — delete one |
| `dev_docs/03_control/decisions.md` | ADR decision log | Created in Cycle 1 Review |
| `dev_docs/03_control/repository_structure.md` | This note | |
| `dev_docs/llm_guidance/*` | 03_control — instructions for AI sessions | New; load-by-component; keeps context small |

### Working (04)
| File | SHAPR role | Notes |
|---|---|---|
| `ROADMAP.md` | ≈ `04_working/cycle_plan.md` | v0.1.0 features documented; v0.2.0 empty; missing `Primary focus` / `Success signal` fields |
| *(missing)* `source_of_truth.md`, `current_state.md`, `tasks.md`, `ideas.md` | 04_working | **Gap — none exist yet** |

### Knowledge (05)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/guide.md` | SKU definition (05_knowledge) | Source: arXiv 2603.25660 §6 |
| `dev_docs/v0.1.0.md`, `v0.1.1.md` | SKU knowledge units | 44 + 11 SKUs; reconstructed from `logs.md`; need global IDs, triage, evidence links |
| `dev_docs/05_knowledge/reflection.md` | reflection | Created from cycle learnings |
| *(missing)* `paper.md`, `references.md` | 05_knowledge | **Gap** |

### Cycles (evidence of the cycle)
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/cycle_record_notes/cycle_1.md` | cycle record | Build cycle (v0.1.0) |
| `dev_docs/cycle_record_notes/cycle_1_review.md` | cycle review | Audit-and-release review (v0.1.1) |
| `audit.md` | Review evidence | The findings behind `cycle_1_review.md` — link it from the review |

### Evidence / raw data
| File | SHAPR role | Notes |
|---|---|---|
| `logs.md` + `logs/` | Raw interaction data | The Explore-phase proof; source for SKUs. Not yet linked to SKU IDs / commits |

### Reference
| File | SHAPR role | Notes |
|---|---|---|
| `dev_docs/example_docs/` | Reference vault | The SHAPR example these conventions come from; not part of this project's own docs |

## Authority notes

- **Git history and cycle snapshots have different roles** (from `snapshot_workflow.md`): Git = history; snapshots = frozen handoff artefacts.
- **Source of truth by role** will be defined in `source_of_truth.md` (04_working) — **pending**; until then, the codebase is authoritative for implementation truth and this note for file roles.
- **Anti-drift rule:** the docs map existing files to roles; do **not** copy root docs into `dev_docs/` (copying creates drift). If a file is moved, update this note in the same change.

## Known gaps (short list)

1. `04_working` empty — no `source_of_truth.md`, `current_state.md`, `tasks.md`, `ideas.md`.
2. `ROADMAP.md` ≈ `cycle_plan.md` but missing the template's `Primary focus` / `Success signal` / `Status` fields.
3. No `code_map.md` (note↔code mapping) — biggest drift-killer still absent.
4. `logs.md`/`logs/` not linked to SKU IDs or commit refs; no `/evidence` convention.
5. `audit.md` not referenced from `cycle_1_review.md`.
6. `claude.md` duplicate of `CLAUDE.md` (delete).
7. SKU files need triage + global IDs + evidence links.
