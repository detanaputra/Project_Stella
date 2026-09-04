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

## Hands-off areas

`mmd_charts/` and `notebooks/` are the human's **personal working directory** — for experimenting with and learning the codebase manually, without LLM help. **Do not touch, modify, or archive them unless the human explicitly asks.** They are not part of the SHAPR documentation or the app code.

## Expected evidence

What counts as evidence in SHAPR (from the canonical papers, arXiv `2602.12443` and `2603.25660`):

- **The repository is the evidence layer.** Evidence is the *translation* of an interaction into artefact changes, documented in the repo — source code, cycle records, decisions, SKUs, snapshots, evaluation data. Git commits support traceability of artefact changes.
- **Chat transcripts are not required evidence.** Interaction with an AI becomes research evidence only when translated into artefact changes and documented in the repository. Conversations are "cognitive scaffolding" — optional raw material, not the formal record.
- **Evidence types** (per `2602.12443` Table 4): source code; configuration/environment files; prompts and AI interaction records; planning/PRD documentation; design sketches and architectural notes; evaluation notes and test records; reflective journals and analytic memos; version history/change logs.
- **Lightweight and tool-agnostic.** No specific logging tool or format is mandated; reflective notes linked to specific artefact versions are sufficient.
- **SKU evidence.** Attach the git commit hash and/or code `file:line`; a chat-transcript reference is optional raw proof, never a substitute for the documented artefact.

## Component index — load what you need

| Component | File | Use when |
|---|---|---|
| Overview / structure | `README.md` | Always — start here |
| From-scratch guide | `from_scratch_guide.md` | Starting a brand-new project with SHAPR — plain-English walkthrough |
| SKUs | `sku_instruction.md` | Writing, upgrading, or revising Structured Knowledge Units |
| Cycle records & reviews | `cycle_record_instruction.md` | Writing `cycle_n.md` or `cycle_n_review.md` |
| Working docs | `working_docs_instruction.md` | Maintaining `current_state.md`, `tasks.md`, `source_of_truth.md`, `cycle_plan.md`, `ideas.md` |
| Control layer | `control_layer_instruction.md` | Maintaining `decisions.md`, `snapshot_workflow.md`, `coding_protocol.md`, `implementation_stack.md`, `shapr_obsidian_setup.md` |
| Knowledge layer | `knowledge_layer_instruction.md` | Maintaining `reflection.md`, `paper.md`, `references.md`, `SHAPR_future.md` |
| System & contracts | `system_contracts_instruction.md` | Maintaining design/spec notes (`01_system`) or interface contracts (`02_contracts`) |
| Tags, links, IDs, evidence | `conventions_instruction.md` | Any file — the cross-cutting taxonomy and linking rules |

## Current state

This folder is **guidance only** — it does not track the project's current state. For live state, see the authoritative working docs: `dev_docs/current/04_working/current_state.md` (active phase), `dev_docs/current/04_working/source_of_truth.md` (file authority), and `dev_docs/current/03_control/repository_structure.md` (repo layout).
