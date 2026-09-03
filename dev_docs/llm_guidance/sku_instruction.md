# SKU Instruction

How to write a **Structured Knowledge Unit (SKU)** — SHAPR's fundamental unit of captured knowledge.

Source of the definition: the four components in `from_scratch_guide.md` (this folder) and the SHAPR arXiv paper 2603.25660 (linked in `dev_docs/current/05_knowledge/references.md`).

## What an SKU is

A structured representation of an insight derived from a development cycle that explains **how a specific design decision influences artefact behaviour**. It converts an AI interaction into an auditable, citable record: *"I evaluated an AI-generated artefact against constraints."*

## The four core components (mandatory)

| Component | Answers | Guidance |
|---|---|---|
| **Context** | What design situation or problem was addressed? | The situation *before* the decision — the problem, bug, or requirement. |
| **Design Decision** | What implementation or modification was applied? | Concrete: what changed, where (file paths), and ideally the commit ref. |
| **Observation** | What outcome or behaviour was observed during evaluation? | What actually happened when it ran / was used — the evidence. |
| **Insight** | Why did the outcome occur, and what does it mean? | The transferable interpretation — the reason the decision generalises or warns. |

## The fuller drafting template (use when a SKU is part of a cycle)

The example's concrete SKU template (`SHAPR_future.md:53-59`) adds fields beyond the four core ones:

```
**Cycle ID:** [ProjectName_C01]
**Phase:** Build/Evaluate
**AI Interaction:** [Summarize prompt and AI suggestion]
**Design Decision:** [What did you change in the code?]
**Observation:** [What happened when you ran the code?]
**SKU Insight:** [Why did this happen, and what does it mean for the research?]
```

When you have them, also record: **timestamp** (UTC), **SKU ID**, and **evidence link** (commit hash / `file:line` / chat-transcript reference).

## IDs and evidence links

- Use a **cycle-coded sequential ID** — `SKU-[cycle]-[number]`, e.g. `SKU-02-01` — where the first segment is the cycle number and the second is the sequential number within that cycle. IDs restart per cycle (not per version file). (The v0.1.0/v0.1.1 files used a global `SKU-001`… sequence; v0.2.0 onward is cycle-coded.)
- Reference SKUs in commit messages and other docs in the example's style: `Ref: SKU-02-01 — Implemented Polars switch to reduce RAM.`
- Attach evidence: the git commit hash, the code file/line, and (for raw proof) a reference to the chat transcript in `logs/`. Evidence is what makes an SKU verifiable.

## Triage — which interactions deserve an SKU

SHAPR explicitly says *"you cannot SHAPR everything."* Write an SKU when the interaction produced a **learning that affects behaviour or future decisions**:

- an architectural or design decision (and its rationale/trade-offs)
- a bug whose **root cause** reveals something about the stack (e.g. BERTopic probs shape, Tk pack order, pywebview main-thread rule)
- a contract or interface change
- a refactor with observable consequences
- a methodological learning about the human–AI process itself

**Do NOT** write a SKU for: trivial tweaks (e.g. a sash thickness), housekeeping (e.g. `.gitignore`), dependency pinning, one-line fixes with no transferable lesson. Those belong in a changelog or `tasks.md`, not the knowledge layer. (The current Stella files violate this — 55 SKUs including trivial ones. Triage them when revising.)

## Where SKUs live vs. adjacent artefacts

- **`decisions.md`** — the ADR-style log of accepted design decisions (see `control_layer_instruction.md`). Use this for decisions you want to *lock as governing*.
- **`reflection.md`** — methodological reflections and emerging insights (see `knowledge_layer_instruction.md`).
- **SKUs** — the portable, structured insight units. The example treats SKUs as the nominal knowledge unit; the operational equivalents in the vault are decision entries and reflection bullets.

Knowledge flow: **capture (append-first) → cycle record consolidation → reflection/paper**. A SKU can feed any of those stages.

## Tags

Tag SKU-bearing files at the top with the knowledge tags, e.g. `#decision #design #learn` (full taxonomy in `conventions_instruction.md`).

## Current state

This folder is **guidance only** — it does not track the project's current state. For live state, see the authoritative working docs: `dev_docs/current/04_working/current_state.md` (active phase), `dev_docs/current/04_working/source_of_truth.md` (file authority), and `dev_docs/current/03_control/repository_structure.md` (repo layout).
