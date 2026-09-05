# Current State

#working #current_state #cycle4

## Current Position

Cycle 1 (v0.1.0), Cycle 2 (v0.2.0), and Cycle 3 (v0.3.0) are **closed and released** on `main`. Cycle 3 shipped WP1 (in-app visualisation tabs) and WP2 (layout restructure), recorded in `cycle_3.md` + `cycle_3_review.md` (verdict: Release), snapshotted in `dev_docs/snapshots/cycle_3_close/`, and merged to `main` via PR #3 (commit `e646fe4`). The `v0.4.0` branch is open for Cycle 4; its scope has not been decided yet.

## What Is Stable

- Released v0.1.0 application (BERTopic training, wizard, result tables, `.stella` save/load, pywebview visualizations, retrain).
- **Released v0.2.0:** README + Apache 2.0 license; MouseWheel scrolling in both parameter panels; topic quality metrics (NPMI, C_V, UMass via Gensim + hand-rolled Topic Diversity) shown as 4 gauges in a dynamic "Metrics" tab.
- `cycle_plan.md` documents v0.1.0, v0.2.0, and v0.3.0 (all completed); `ideas.md` is the raw idea capture area.
- Cycle records: `cycle_0.md` (retrospective), `cycle_1.md` + `cycle_1_review.md`, `cycle_2.md` + `cycle_2_review.md`, `cycle_3.md` + `cycle_3_review.md`.
- Control layer: `decisions.md` (D-001..D-023), `repository_structure.md`, `snapshot_workflow.md`.
- Working layer: `source_of_truth.md`, `current_state.md`, `tasks.md`, `cycle_plan.md`, `ideas.md`.
- Knowledge layer: `reflection.md`, SKU files under `dev_docs/current/05_knowledge/skus/` (cycle-coded: `v0.1.0.md` SKU-01-01…25 with v0.1.1 merged, `v0.2.0.md` SKU-02-01…04, `v0.3.0.md` SKU-03-01…04).
- GitHub remote `origin` → github.com/detanaputra/Project_Stella.
- `dev_docs/snapshots/cycle_1_close/`, `cycle_2_close/`, and `cycle_3_close/` — frozen handoffs of the cycle-1, cycle-2, and cycle-3 close states.

## In Progress

- Cycle 3 close is complete: `cycle_3.md` + `cycle_3_review.md`, the cycle-3 snapshot, and the release to `main` (PR #3, `e646fe4`) are all done.
- Cycle 4 opening: scope decision pending (candidates in `ideas.md`).

## Deferred

- Later cycles (post-graduation): LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing.

## Immediate Next Step

Open Cycle 4: decide scope per the Cycle 4 candidates in `ideas.md` (retire pywebview, topic refinement, metrics-tab explanations), write the `cycle_plan.md` v0.4.0 section, and update `current_state.md`.
