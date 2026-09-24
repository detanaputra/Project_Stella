# Cycle 5 Review

#cycle5 #review #evaluation #shapr

## Review Summary
Cycle 5 delivered three work packages: a committed `pytest` suite (38 tests) for the model + controller layer, model persistence (a zip-bundle `.stella` with a multi-model-ready `models` dict and per-algorithm save/load behind `BaseAlgorithm`), and multi-model-ready exports. The feature set is implemented and committed on `v0.5.0`, and the cycle record is written. The review confirms the objective was met, with a few gaps worth carrying forward.

## 1. What Went Well
1. **Test suite first.** Hardening preceded the persistence rework, so the riskiest change (save/load, `ProjectService`, the algorithm layer) was protected by tests from the start — and the suite immediately caught a real crash (`nr_topics='auto'` on no-outlier corpora) that manual testing had missed.
2. **The round-trip test doubled as the feasibility check.** The `save → load → compare` test answered the BERTopic save/load question (single file, not a directory; embedding-model include/exclude) without a separate spike.
3. **Option A (`models` dict) made the format multi-model-ready at near-zero cost.** The user's pushback on the single-model `project.json` produced a format that won't need a breaking change when multi-model lands.
4. **D-024 (tests travel with the change)** kept the suite in lockstep — the persistence rework updated its tests in the same commits.

## 2. Main Strengths of Cycle 5
1. **The zip-bundle design.** One `.stella` file carries state, result, model, and visualisations, so reload restores the full work without retraining — the cycle's success signal, delivered as a single coherent artefact.
2. **Persistence stayed algorithm-agnostic.** `save_model`/`load_model` on `BaseAlgorithm` mean LDA/NMF implement the same interface; the BERTopic specifics (single-file pickle, `model.pt` in a per-model dir) are contained in the implementation.
3. **The suite is headless and fast.** Model + controller coverage runs without a GUI, so it can gate every change (and eventually CI) without a display.

## 3. Constraints and Remaining Gaps
1. **Editable display name deferred** — model-ids are timestamps only; renaming a model in the UI is a future cycle.
2. **`current_model_id` / multi-model UI deferred** — the format is ready, but the app still shows one model at a time.
3. **View layer not covered by tests** — the suite is model + controller only; UI regressions (like the Detail-button bug this cycle) are still caught by manual testing.
4. **`pytest-cov` not wired in** — coverage reporting is documented but not part of the dev toolchain yet.
5. **The `.stella` format changed** (single JSON → zip bundle); the old format is not loaded by the new `ProjectService`.

## 4. Key Learning Confirmed
To allow topic model practitioners to preserve and resume their analysis work when doing topic modelling analysis, develop functionality that persists the trained model together with its results and visualisations in a single project bundle, because the ability to save and reload the full work without retraining is essential for researchers to continue their analysis across sessions and reproduce their findings.

## 5. Risks to Watch Moving Forward
1. **Multi-model support is the next large change** — `current_model_id`, model switching, and display names touch `AppState`, the controllers, and the UI; the format is ready, but the state/UI work is substantial.
2. **The suite must stay in lockstep (D-024)** — a suite that lags the code silently loses its value; every design-changing commit must carry its tests.
3. **The embedding-model-excluded save decision** — if a future cycle adds a second embedding model, a saved model may not be self-contained; re-verify the include/exclude choice when the model options expand.
4. **Untested view layer** — UI regressions are only caught by manual testing until view coverage is added.

## 6. Review of Cycle Objective
The objective — a committed test suite, then model persistence so researchers can save and reload their full work without retraining — was met. All three work packages are implemented, committed, and documented. The success signal (pytest passes on the model/controller layer; save → reload restores the same topics, metrics, and visualisations with the trained model) is satisfied by the implementation.

## 7. Recommended Follow-On Direction
- **Option A — release, then the post-graduation backlog:** release v0.5.0 to `main`, then take on **LDA/NMF** (the real test of the algorithm-agnostic design — D-001) and **multi-model support** (`current_model_id`, editable display names, model switching), then search/filter hardening and batch processing.
- **Option B — release, then extend the suite first:** release v0.5.0, then add view-layer tests and coverage reporting before the backlog.

Either way, the release is the immediate next step.

## 8. Review Verdict
**Release.** The v0.5.0 feature set is complete and coherent; the remaining gaps (display names, multi-model UI, view-layer tests, coverage) are follow-on hardening, not blockers.
