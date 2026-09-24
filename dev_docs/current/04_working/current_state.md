# Current State

#working #current_state #cycle5

## Current Position

Cycle 1 (v0.1.0), Cycle 2 (v0.2.0), Cycle 3 (v0.3.0), and Cycle 4 (v0.4.0) are **closed and released** on `main` (Cycle 4 via PR #4, `e951036`). **Cycle 5 (v0.5.0) is built and at the close stage** on the `v0.5.0` branch: all three work packages are complete — WP1 (test suite, 38 tests), WP2 (persistence, model layer), WP3 (persistence, service + UI, incl. multi-model-ready exports). The cycle record, review, snapshot, and release to `main` remain.

## What Is Stable

- Released v0.1.0 application (BERTopic training, wizard, result tables, `.stella` save/load, pywebview visualizations, retrain).
- **Released v0.2.0:** README + Apache 2.0 license; MouseWheel scrolling in both parameter panels; topic quality metrics (NPMI, C_V, UMass via Gensim + hand-rolled Topic Diversity) shown as 4 gauges in a dynamic "Metrics" tab.
- **Released v0.4.0:** topic refinement (merge/delete/label), document exploration (search + detail + topic filter), pywebview retired, metrics explanations, centred dialogs, MVP option limiting.
- **Cycle 5 (v0.5.0) on the `v0.5.0` branch (not yet released):** committed `pytest` suite (38 tests), model persistence (zip-bundle `.stella` with a multi-model-ready `models` dict), and multi-model-ready exports (topics/assignments CSV + model-record JSON).
- `cycle_plan.md` documents v0.1.0–v0.4.0 (completed) and v0.5.0 (completed and ready to close); `ideas.md` is the raw idea capture area.
- Cycle records: `cycle_0.md` (retrospective), `cycle_1.md` + `cycle_1_review.md`, `cycle_2.md` + `cycle_2_review.md`, `cycle_3.md` + `cycle_3_review.md`, `cycle_4.md` + `cycle_4_review.md`.
- Control layer: `decisions.md` (D-001..D-024), `repository_structure.md`, `snapshot_workflow.md`.
- Working layer: `source_of_truth.md`, `current_state.md`, `tasks.md`, `cycle_plan.md`, `ideas.md`.
- Knowledge layer: `reflection.md`, SKU files under `dev_docs/current/05_knowledge/skus/` (cycle-coded: `v0.1.0.md` SKU-01-01…25 with v0.1.1 merged, `v0.2.0.md` SKU-02-01…04, `v0.3.0.md` SKU-03-01…04, `v0.4.0.md` SKU-04-01…06).
- GitHub remote `origin` → github.com/detanaputra/Project_Stella.
- `dev_docs/snapshots/cycle_1_close/`, `cycle_2_close/`, `cycle_3_close/`, and `cycle_4_close/` — frozen handoffs of the cycle-1, cycle-2, cycle-3, and cycle-4 close states.

## In Progress

- Cycle 5 close: all three work packages complete; the cycle record, review, snapshot, and release to `main` (D-017) remain.

## Deferred

- Later cycles (post-graduation): LDA/NMF algorithms, multi-model support, embedded matplotlib charts, batch processing.

## Immediate Next Step

Close Cycle 5: write `cycle_5.md` + `cycle_5_review.md`, take the cycle-5 snapshot, commit the close docs, then release v0.5.0 to `main` per D-017.
