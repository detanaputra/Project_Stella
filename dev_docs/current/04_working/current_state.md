# Current State

#working #current_state #cycle4

## Current Position

Cycle 1 (v0.1.0), Cycle 2 (v0.2.0), and Cycle 3 (v0.3.0) are **closed and released** on `main`. Cycle 4 (v0.4.0) is built and **at the close stage**: all four work packages (topic refinement, retire pywebview, UI polish, document exploration) are complete and committed on the `v0.4.0` branch, SKUs are documented (`v0.4.0.md`, SKU-04-01…06), and the cycle record + review are written. The cycle-4 review and snapshot are done; the close-docs commit and the release to `main` remain.

## What Is Stable

- Released v0.1.0 application (BERTopic training, wizard, result tables, `.stella` save/load, pywebview visualizations, retrain).
- **Released v0.2.0:** README + Apache 2.0 license; MouseWheel scrolling in both parameter panels; topic quality metrics (NPMI, C_V, UMass via Gensim + hand-rolled Topic Diversity) shown as 4 gauges in a dynamic "Metrics" tab.
- **Cycle 4 (v0.4.0) built on the `v0.4.0` branch (not yet released):** topic refinement (merge/delete/label), document exploration (search + detail + topic filter), pywebview retired, metrics explanations, centred dialogs, MVP option limiting.
- `cycle_plan.md` documents v0.1.0, v0.2.0, and v0.3.0 (completed) and v0.4.0 (completed and ready to close); `ideas.md` is the raw idea capture area.
- Cycle records: `cycle_0.md` (retrospective), `cycle_1.md` + `cycle_1_review.md`, `cycle_2.md` + `cycle_2_review.md`, `cycle_3.md` + `cycle_3_review.md`, `cycle_4.md` + `cycle_4_review.md`.
- Control layer: `decisions.md` (D-001..D-023), `repository_structure.md`, `snapshot_workflow.md`.
- Working layer: `source_of_truth.md`, `current_state.md`, `tasks.md`, `cycle_plan.md`, `ideas.md`.
- Knowledge layer: `reflection.md`, SKU files under `dev_docs/current/05_knowledge/skus/` (cycle-coded: `v0.1.0.md` SKU-01-01…25 with v0.1.1 merged, `v0.2.0.md` SKU-02-01…04, `v0.3.0.md` SKU-03-01…04, `v0.4.0.md` SKU-04-01…06).
- GitHub remote `origin` → github.com/detanaputra/Project_Stella.
- `dev_docs/snapshots/cycle_1_close/`, `cycle_2_close/`, `cycle_3_close/`, and `cycle_4_close/` — frozen handoffs of the cycle-1, cycle-2, cycle-3, and cycle-4 close states.

## In Progress

- Cycle 4 close: `cycle_4.md` + `cycle_4_review.md` written and the cycle-4 snapshot taken; the close-docs commit and the release to `main` (D-017) remain.

## Deferred

- Later cycles (post-graduation): LDA/NMF algorithms, multi-model support, embedded matplotlib charts, batch processing.

## Immediate Next Step

Close Cycle 4: commit the cycle-close docs batch, then release v0.4.0 to `main` per D-017.
