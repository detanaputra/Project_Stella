# Paper — Working Draft

#paper #shapr #methodology

Working notes toward the eventual research write-up. This is the **output** of the knowledge pipeline (capture → cycle record → reflection → paper); it consolidates the methodological learnings from the Stella case study into citable prose. Draft status — sections are placeholders and pointers, not finished text.

**Raw material:** `dev_docs/current/05_knowledge/reflection.md`, `dev_docs/cycle_record_notes/` (cycle_1 + review, cycle_2 + review), `dev_docs/current/05_knowledge/skus/`, `dev_docs/current/03_control/decisions.md`.

## Key Ideas / Key Sentences

- SHAPR = **Solo, Human-centred, AI-assisted PRactice** — an operationalisation layer over Action Design Research (ADR).
- *"SHAPR enables structured traceability in AI-assisted research software development."*
- The cycle is **Explore → Build → Use → Evaluate → Learn**; the workflow rule is **Think → Code → Learn → Update (2 mins) → Repeat**.
- *"You cannot SHAPR everything"* — triage to decisions and learnings that influence behaviour and future choices.
- The human is the **epistemic authority**; the AI is a junior developer whose output is evaluated, not trusted.
- Evidence is the **translation of an interaction into artefact changes, documented in the repository** — not the chat transcript itself.

## Observations

- **Case study:** Stella, a topic-modelling GUI for non-technical social scientists, built solo with AI assistance over two cycles (v0.1.0 build + audit/release; v0.2.0 metrics).
- **Cycle 1 (v0.1.0):** full MVC application (wizard, result tables, `.stella` save/load, pywebview visualizations, retrain); 25 SKUs after triage.
- **Cycle 1 review (v0.1.1):** a read-only audit found 22 issues; fixes by severity, one commit per class; released.
- **Cycle 2 (v0.2.0):** README + Apache 2.0 license, MouseWheel scrolling, topic quality metrics (NPMI, C_V, UMass, Topic Diversity) via Gensim; 4 SKUs.
- **Footprint check:** OCTIS (0.13 MB package) would have pulled torch (~1–2 GB installed); Gensim's `CoherenceModel` covered all three coherence measures at a fraction of the footprint.

## Patterns / Insights

- **Audit-as-cycle-review** — the v0.1.1 audit was, in SHAPR terms, a review of Cycle 1 rather than a new cycle; this reframing produced `cycle_1_review.md`.
- **SKU triage** — 55 SKUs including trivial ones (sash thickness, `.gitignore`) were consolidated to 25 design-changing SKUs; a numbering scheme is a contract, and changing it has a documentation ripple.
- **Footprint checks before adopting research libraries** — a quick wheel-size/dependency check can save gigabytes of bundle size and dependency conflicts.
- **Human-captures / AI-consolidates** — the human directs scope and judgement; the AI consolidates, restructures, and aligns notes at deliberate checkpoints.
- **Snapshot → reset → next cycle improves clarity** — frozen snapshots at cycle boundaries give each cycle a clean baseline.

## Drafted Paragraphs

*(ready-to-adapt prose; currently placeholders)*

- **Methodology paragraph:** This project applies SHAPR — a solo, human-centred, AI-assisted practice framework — to the development of Stella, a topic-modelling desktop application for non-technical social scientists. SHAPR operationalises Action Design Research by making explicit the roles, artefacts, reflective practices, and lightweight governance mechanisms needed for accountability in AI-assisted development. The framework's evidence and traceability mechanism links human decisions, AI-assisted development, and artefact evolution, enabling transparency, reproducibility, and systematic refinement.

- **Collaboration pattern paragraph:** Throughout the project, the human researcher acted as the epistemic authority, directing scope and judging the AI's output against constraints, while the AI acted as a junior developer — drafting code, consolidating notes, and restructuring documentation at deliberate checkpoints. This division of labour kept the human in control of what is true while leveraging the AI's capacity for boilerplate and consolidation.

## Quick Capture

- Thesis positioning: the paper argues that SHAPR enables structured traceability in solo AI-assisted research software development, demonstrated through the Stella case study — where every design decision (D-001…D-022), knowledge unit (SKU-01-01…25, SKU-02-01…04), and cycle record is traceable to a documented artefact.
- Open question: does the audit-as-review reframing generalise, or was it specific to this project's v0.1.1 situation?
