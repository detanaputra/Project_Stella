# LLM Guidance — SHAPR Documentation Conventions

A set of instruction files that let a future Claude session produce or update SHAPR-compliant documentation for this project **without re-reading `dev_docs/example_docs/`**. Each file covers one component. Load only the file(s) relevant to the task — that keeps context small.

Provenance: these files distill the conventions from `dev_docs/example_docs/` (a SHAPR framework example vault) and the SKU definition in `dev_docs/guide.md`. The source arXiv papers are `2602.12443` and `2603.25660` (linked in `example_docs/current/05_knowledge/references.md`).

## Core philosophy (applies to all components)

- SHAPR = **Solo, Human-centred, AI-assisted PRactice** — an operationalisation layer over Action Design Research (ADR).
- The cycle is **Explore → Build → Use → Evaluate → Learn**. The workflow rule: **Think → Code → Learn → Update (2 mins) → Repeat**.
- **Not:** *Think → Code → Document everything → Burn out.* Rule of thumb: *if documentation slows you down, you are doing too much.*
- The human researcher is the **epistemic authority**; the AI is a junior developer whose output is evaluated, not trusted.
- **Capture lightweight notes during work (append-first); consolidate at checkpoints and cycle end.** Never reconstruct everything from memory at the end of a project.
- An SKU turns *"I asked AI"* into *"I evaluated an AI-generated artefact against constraints."* It is evidence, not prose.

## Component index — load what you need

| Component | File | Use when |
|---|---|---|
| Overview / structure | `README.md` | Always — start here |
| SKUs | `sku_instruction.md` | Writing, triaging, or revising Structured Knowledge Units |
| Cycle records & reviews | `cycle_record_instruction.md` | Writing `cycle_n.md` or `cycle_n_review.md` |
| Working docs | `working_docs_instruction.md` | Maintaining `current_state.md`, `tasks.md`, `source_of_truth.md`, `cycle_plan.md`, `ideas.md` |
| Control layer | `control_layer_instruction.md` | Maintaining `decisions.md`, `snapshot_workflow.md`, `coding_protocol.md`, `implementation_stack.md`, `shapr_obsidian_setup.md` |
| Knowledge layer | `knowledge_layer_instruction.md` | Maintaining `reflection.md`, `paper.md`, `references.md`, `SHAPR_future.md` |
| System & contracts | `system_contracts_instruction.md` | Maintaining design/spec notes (`01_system`) or interface contracts (`02_contracts`) |
| Tags, links, IDs, evidence | `conventions_instruction.md` | Any file — the cross-cutting taxonomy and linking rules |

## Current state of this project (Stella)

- **Code:** `app/` (ttkbootstrap MVC — models/views/controllers). Supporting docs: `CLAUDE.md`, `ARCHITECTURE.md`, `API.md`, `DEVELOPMENT.md`, `ROADMAP.md`, `audit.md`.
- **Interaction log:** `logs.md` (+ raw transcripts under `logs/`). This is the *raw data* source for SKUs.
- **Current SKU files:** `dev_docs/v0.1.0.md` (44 SKUs) and `dev_docs/v0.1.1.md` (11 SKUs) — flat, one SKU per log interaction, timestamped, grouped by date. They follow the 4-field format but predate the fuller SHAPR conventions (no global SKU IDs, no cycle structure, no evidence/commit links, no triage).
- **Known gaps vs the example:** SKU IDs restart between versions (both start at SKU 001); every log interaction is an SKU (no triage); no cycle records/reviews; no working/control/knowledge scaffolding beyond the SKU files; no commit-ID or code-location evidence links; no tags.
- **Example vault:** `dev_docs/example_docs/` — read once for reference; the conventions you need are in these instruction files.
