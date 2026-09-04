# Current State

#working #current_state #cycle3

## Current Position

Cycle 1 (v0.1.0 build) is **closed**: released on `main`, recorded in `dev_docs/cycle_record_notes/cycle_1.md`, and reviewed in `cycle_1_review.md` (verdict: Release, all 22 audit findings fixed). **Cycle 2 (v0.2.0) is closed and released**: all five work packages shipped on the `v0.2.0` branch (README + license, MouseWheel scrolling, topic quality metrics), recorded in `cycle_2.md` + `cycle_2_review.md` (verdict: Release), snapshotted in `dev_docs/snapshots/cycle_2_close/`, and merged to `main` via PR #2 (commit `993cc53`). **Cycle 3 (v0.3.0) is open**: the `v0.3.0` branch was created fresh from `main` (D-017); the scope is decided (visualisation tabs + layout restructure) and recorded in `cycle_plan.md`; implementation not yet started.

## What Is Stable

- Released v0.1.0 application (BERTopic training, wizard, result tables, `.stella` save/load, pywebview visualizations, retrain).
- **Released v0.2.0:** README + Apache 2.0 license; MouseWheel scrolling in both parameter panels; topic quality metrics (NPMI, C_V, UMass via Gensim + hand-rolled Topic Diversity) shown as 4 gauges in a dynamic "Metrics" tab.
- `cycle_plan.md` documents v0.1.0 (completed), v0.2.0 (completed), and v0.3.0 (planned); `ideas.md` is the raw idea capture area.
- Cycle records: `cycle_1.md` + `cycle_1_review.md`, `cycle_2.md` + `cycle_2_review.md`.
- Control layer: `decisions.md` (D-001..D-022), `repository_structure.md`, `snapshot_workflow.md`.
- Working layer: `source_of_truth.md`, `current_state.md`, `tasks.md`, `cycle_plan.md`, `ideas.md`.
- Knowledge layer: `reflection.md`, SKU files under `dev_docs/current/05_knowledge/skus/` (cycle-coded: `v0.1.0.md` SKU-01-01…25 with v0.1.1 merged, `v0.2.0.md` SKU-02-01…04, `v0.3.0.md` SKU-03-01…03).
- GitHub remote `origin` → github.com/detanaputra/Project_Stella.
- `dev_docs/snapshots/cycle_1_close/` and `dev_docs/snapshots/cycle_2_close/` — frozen handoffs of the cycle-1 and cycle-2 close states.

## In Progress

- Cycle 3 implementation: WP1 — static viz service + visualisation tabs (see `cycle_plan.md` v0.3.0).

## Deferred

- Later cycles (post-graduation): LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing.
- A `cycle_0.md` retrospective (environment-setup cycle) — to be written by the human.

## Immediate Next Step

Start WP1: the `to_dict()` → matplotlib converter + the 5 viz tabs, then WP2 (layout restructure) per `cycle_plan.md` v0.3.0.
