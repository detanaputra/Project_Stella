# Conventions Instruction

Cross-cutting conventions from the SHAPR example: tags, links, IDs, the evidence layer, snapshots, and the operating rules. Apply these in any component file.

Source: `example_docs/current/03_control/shapr_obsidian_setup.md`, `example_docs/current/05_knowledge/paper.md`, and the file conventions throughout the vault.

## Tags

Tag lines live on the **first 1–3 lines** of a note (the example is inconsistent about before/after the H1 title; **place them at the very top** — that is the convention the review flags as correct). No YAML frontmatter is used in the example — tags are inline `#tag` text.

**Taxonomy:**

| Group | Tags |
|---|---|
| SHAPR phases | `#explore` `#build` `#use` `#evaluate` `#learn` |
| Knowledge | `#concept` `#design` `#decision` `#implementation` `#experiment` |
| Artefacts | `#artifact` `#module` `#pattern` `#strategy` |
| Working / process | `#working` `#tasks` `#control` `#workflow` `#traceability` `#shapr` `#plan` `#cycles` |
| Cycle & review | `#cycle<N>` `#formal_record` `#review` `#evaluation` |
| Notes on note-type | `#reflection` `#methodology` `#learning` `#mapping` `#source_of_truth` |

**Usage:** classify the note at the top; use inline tags to capture insights (`#learn`) or record decisions (`#decision`) mid-note.

## Links

Four coexisting styles — use the one that fits:

1. **Short wiki links** `[[basename]]` (Obsidian-resolved, no `.md`) — e.g. `[[reflection]]`, `[[SHAPR_future]]`.
2. **Full-path wiki links** `[[docs/current/01_system/indicator_engine]]` — dominant in system notes and `snapshot_workflow.md`.
3. **Snapshot-path wiki links** `[[cycle_snapshots/cycle_00/04_working/current_state]]` — for referencing frozen historical state.
4. **Inline backticked filenames** `current_state.md`, `decisions.md` — the convention inside `source_of_truth.md` and `instructions.md`, where files are treated as authoritative artefacts rather than graph nodes.

Mental model: **Folders → where to go; Tags → what it means; Links → how it connects.**

## IDs

- **Cycles:** filename `cycle_n.md` / `cycle_n_review.md` + `#cycle<N>` tag + a `## Cycle Title` heading.
- **Decisions:** `DD-###` (early), then `D-###`, sequential across the log, grouped under cycle-boundary headings.
- **Runs/experiments:** timestamp-based `run_id`.
- **SKUs:** use a **global sequential** `SKU-NNN` (do not restart per file/version). Reference in commit messages as `Ref: SKU-042 — …`.
- **Timestamps:** the example systemizes none; **Stella's SKU files do use UTC timestamps — keep them**, they are a traceability strength.

## Evidence layer

SHAPR needs a verifiable trail, not just prose:

- **Git/GitHub = the evidence layer.** Use meaningful commit messages; reference SKUs/decisions (`Ref: SKU-042 — Implemented …`).
- **Interaction log = raw data.** Store exported chat threads (JSON/PDF) as evidence of the Explore phase — Stella keeps these in `logs/` with `logs.md` as the index.
- **Snapshot + diff = cycle traceability.** ZIP-based cycle snapshots plus diff-style comparison between successive states preserve cycle boundaries and show what changed.
- **SKU = the evaluated outcome** of the evidence, linking *Context + Design Decision + Observation + Insight*.

## Snapshot conventions

- Work only in `docs/current/` during a cycle; at cycle end copy to `docs/snapshots/cycle_X` and **never modify snapshots**.
- Exclude `docs/snapshots/` from the Obsidian graph (Files & Links → Excluded files).
- A snapshot is the frozen **handoff artefact** for the next chat/cycle — see `control_layer_instruction.md` for the procedure and the minimum pre-snapshot update set.
- **Git and snapshots have different roles:** Git = history; snapshots = frozen handoff states.

## Operating rules (the anti-burnout contract)

- **Think → Code → Learn → Update (2 mins) → Repeat.** Not "document everything."
- **If documentation slows you down, you are doing too much.** Capture lightweight during work (append-first), consolidate at checkpoints and cycle end.
- **The human is the epistemic authority.** AI suggestions are evaluated against constraints; the human decides what is true. The AI may consolidate/restructure notes, never assert truth.
- **Prefer the smaller, more traceable implementation** that gets the next working step done cleanly.
- **Don't SKU everything** — triage to decisions and learnings that matter (see `sku_instruction.md`).
