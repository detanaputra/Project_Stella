# Knowledge Layer Instruction

How to maintain the **research/methodological layer** (`05_knowledge` in the example): `reflection.md`, `paper.md`, `references.md`, `SHAPR_future.md`.

Source: `example_docs/current/05_knowledge/`.

This layer is about SHAPR-the-framework and the research output, **not** project code. It is the end of the knowledge pipeline: *capture → cycle-record consolidation → reflection / paper.*

## `reflection.md` — the reflection engine

Purpose (from the file): *captures methodological reflections, operational learnings, design tensions, and emerging insights arising during SHAPR-based development cycles.* Ideas here **may later inform: cycle records, SKUs, paper writing, framework refinement.**

Structure: a Simple Notes Capture Rule at top, then **cycle-consolidated bullet blocks**:
```
## Cycle 1 Consolidated Quick Capture
## Cycle 2 Starting Reflection
## Reflection — <topic>          <- e.g. "context control, document drift, and SHAPR handoff discipline"
## Cycle 3 Closing Reflection — <title>
### Cycle 4 Reflection — Current architectural learning
### Quick Capture — <insight>
```
Write it as append-first capture during cycles, consolidated per cycle. It is the home for methodological learnings that are *about the process* (e.g. source-of-truth stabilisation is a meaningful SHAPR activity, not mere cleanup; cycle depth can be personalised to the researcher's prior knowledge).

## `paper.md` — the thesis/paper working draft

Working notes toward the eventual research write-up. Sections used in the example:
- **Key Ideas / Key Sentences** — the SHAPR one-liners worth citing (e.g. *"SHAPR enables structured traceability in AI-assisted research software development"*).
- **Observations** — what the case studies showed.
- **Patterns / Insights** — e.g. *snapshot → reset → next cycle improves clarity*.
- **Drafted paragraphs** — ready-to-adapt prose (long-context rationale, incremental scalability through controlled refactoring, the human-captures / AI-consolidates collaboration pattern).
- **Quick Capture** — commentary and thesis-positioning notes.

## `references.md`

A plain grouped URL list — the SHAPR arXiv papers (`2602.12443`, `2603.25660`) and tooling links, grouped under `# SHAPR` / `# Obsidian` headings.

## `SHAPR_future.md` — the framework definition

SHAPR = **Solo, Human-centred, AI-assisted PRactice**, an "operationalisation layer" for Action Design Research. Core components: **Interaction Workspace** · **SHAPR Cycle** (Explore → Build → Use → Evaluate → Learn) · **Research Artefact** · **Repository Workspace** · **SKUs**. Also contains the SKU drafting template (see `sku_instruction.md`). Methodological positioning: DSR as macro-methodology, SHAPR as the micro-level operational framework.

## Knowledge flow

```
append-first capture (decisions.md / tasks.md / ideas.md / reflection.md)
        →  cycle_n.md record (consolidation)
        →  cycle_n_review.md (evaluation)
        →  reflection.md / paper.md (research output)
```

The human directs scope and judgement; AI is used to consolidate, restructure, and align notes at deliberate checkpoints — not to decide what is true.

## Current state

This folder is **guidance only** — it does not track the project's current state. For live state, see the authoritative working docs: `dev_docs/current/04_working/current_state.md` (active phase), `dev_docs/current/04_working/source_of_truth.md` (file authority), and `dev_docs/current/03_control/repository_structure.md` (repo layout).
