# Cycle 5

#cycle5 #formal_record #build #shapr

## Cycle Title
Harden the codebase with a committed test suite, then deliver model persistence so researchers can save and reload their full work — result, model, and visualisations — without retraining (v0.5.0).

## 1. Context

The released v0.4.0 app (topic refinement + document exploration) let the user *act on* topics, but the cycle-4 review flagged **no automated tests** as the top risk, and the deferred persistence design (captured fully in `ideas.md`) was still unbuilt — saving a project restored state and result data, but not the trained model or the visualisations. Cycle 5 covered the v0.5.0 build (2026-09-06 → 2026-09-08), delivered as three work packages, reconstructed as 1 SKU (`SKU-05-01`) in `dev_docs/current/05_knowledge/skus/v0.5.0.md`. WP1 (test suite) was treated as trivial and produced no SKU.

Cycle framing:
- **Main goal:** harden the codebase with a committed test suite, then deliver the designed model-persistence feature so researchers can save and reload their full work (result, model, and visualisations) without retraining.
- **Main outcomes:** 3 work packages delivered (see §3).
- **Success signal:** `pytest` passes on the model/controller layer; a user can save a project, reload it, and see the same topics, metrics, and visualisations — with the trained model restored (no retrain).

## 2. Explore

Design questions investigated and the answers the cycle converged on:

- **2.1 Test suite first, or persistence first?** The cycle-4 review ranked "no automated tests" as the top risk, and the persistence rework touches `ProjectService`, `AppState`, and the algorithm layer — exactly the code a suite should protect. Decided: **test suite first** (hardening; de-risks the persistence rework). The suite covers current behavior; persistence tests land with WP2/WP3, not before.
- **2.2 How to persist the BERTopic model?** The feasibility check (a `save → load → compare` round-trip test) showed BERTopic's native `model.save(path)` writes a **single pickle file, not a directory** — passing a directory path raises `IsADirectoryError`. Decision: each model lives in a per-model directory (`model/{model_id}/`) with the pickle written as `model.pt` inside it; `save_model`/`load_model` on `BaseAlgorithm` keep persistence algorithm-agnostic. Embedding model excluded from the save (smaller bundle; the embedding model is a fixed dependency, `all-MiniLM-L6-v2`).
- **2.3 What shape should `project.json` take?** The first draft assumed a single model (`algorithm_params`/`result` at the top level). The user rejected that as not multi-model-ready. Decision: **Option A** — a `models` dict keyed by `model_id`, each entry holding `selected_algorithm`, `algorithm_params`, and `result`. `current_model_id` (which model is active) is deferred to the multi-model cycle.
- **2.4 What should the exports look like?** `to_json` should mirror `project.json` (all models, no texts/original_texts); the single CSV became two — `to_csv_topics` and `to_csv_assignments` — each with a **Model ID** column so exports stay meaningful when multiple models exist. Button titles carry semantic meaning ("Export Topics", "Export Document Assignments", "Export Model Record (JSON)").
- **2.5 How to identify a model?** A timestamp `model_id` generated at training time (in `_build_result`). An editable display name is deferred to a future cycle per the design.

## 3. Build

### 3.1 WP1 — Test suite
- `requirements-dev.txt` (pytest, black, flake8, isort, mypy — pinned) and `pytest.ini` (`pythonpath = .`, `testpaths = tests`).
- `tests/` + `conftest.py` with reusable fixtures, including a small-corpus BERTopic model fixture (`SAMPLE_TEXTS`, `trained_result`/`fresh_result`).
- 38 tests covering the model + controller layer headless: `AppState` (subscribe/notify/process_events, weakref pruning, `call_on_main`), `DataLoader` (load_texts, load_preview, validate_file, CSV/encoding edge cases), `BERTopicAlgorithm` (train → `TopicResult` shape; merge/delete → updated result; `_build_result`), controllers (`AppController`, `AnalysisController` against a stub state), and services (`Exporter`, `topic_quality`, `static_viz`, `ProjectService`).
- The suite immediately caught a real bug: `nr_topics='auto'` crashed on corpora with no outliers ("Found array with 0 sample(s)") — fixed with a retry-without-reduction fallback in `bertopic.py`.

### 3.2 WP2 — Persistence, model layer
- `model_id` field on `TopicResult`, generated at training time.
- `save_model(model, path)` / `load_model(path)` abstract methods on `BaseAlgorithm`.
- BERTopic implementation via native `model.save()` / `BERTopic.load()` — writes/reads `model.pt` inside the per-model directory (the single-file-not-folder behavior drove the layout).
- The `save → load → compare` round-trip test doubles as the feasibility check (embedding-model include/exclude, size).
- D-024 recorded (test discipline); the Detail-button bug (stale `_doc_filter_label` reference → `TclError` on re-render) fixed in `summary_panel.py`.

### 3.3 WP3 — Persistence, service + UI
- `ProjectService` reworked to a single-file zip bundle: `.stella` = archive holding `project.json` (state + full result data) + `model/{model_id}/` + `viz/{model_id}/`.
- `project.json` uses the **Option A** `models` dict (multi-model-ready); `_rebuild_result` converts JSON string keys back to int topic ids on load.
- `Exporter` reworked to match: `to_json(state)` outputs the same shape as `project.json` (all models, no texts); `to_csv_topics`/`to_csv_assignments` add a Model ID column; `_iter_models` yields each model.
- Controller save/load methods and the save/load dialogs updated (the `.stella` file UX is unchanged; the format is internal).
- Existing `ProjectService` tests updated; new round-trip tests added.

## 4. Use

- `pytest` runs headless on the model/controller layer — 38 tests pass.
- User testing in the real app surfaced: the Detail button staying disabled when `calculate_probabilities=False` (stale widget reference on re-render — tracked to the `_doc_filter_label` `TclError`), the single-model assumption in `project.json` (reworked to Option A), and the export semantics (reworked to match `project.json` + split CSVs with Model ID). The user also made a layout tweak to the export panel (description frame + `wraplength`).

## 5. Evaluate

### 5.1 What worked well
- **The suite paid for itself immediately** — it caught the `nr_topics='auto'` crash that manual testing had missed, before release.
- **Native BERTopic save/load was straightforward** once the single-file-not-folder behavior was understood; the round-trip test doubled as the feasibility check, so no separate spike was needed.
- **Option A (`models` dict) makes the format multi-model-ready** at near-zero cost now, avoiding a breaking format change when multi-model lands.
- **D-024 (tests travel with the change)** keeps the suite in lockstep with the code — the persistence rework updated its tests in the same commits.
- **The zip-bundle design held** — one `.stella` file carries state, result, model, and visualisations, so reload restores the full work without retraining.

### 5.2 Remaining limitations / issues found
- **Editable display name deferred** — model-ids are timestamps only; renaming a model in the UI is a future cycle.
- **`current_model_id` / multi-model UI deferred** — the format is ready, but the app still shows one model at a time.
- **View layer not covered by tests** — the suite is model + controller only (headless); view testing remains deferred.
- **`pytest-cov` not in dev deps yet** — coverage reporting is documented but not wired in.
- **The `.stella` format changed** (single JSON → zip bundle); the old format is not loaded by the new `ProjectService`.

## 6. Learn

Consolidated insights (the cycle's knowledge output, detailed in `v0.5.0.md` SKU):

- **A test suite pays for itself before release** — the first committed suite caught a real crash (`nr_topics='auto'` on no-outlier corpora) that manual testing had missed.
- **Read the library's actual serialization behavior before designing the path layout** — BERTopic `save()` writes one pickle file, not a directory; the per-model directory with `model.pt` inside follows from that.
- **Persist the model and everything derived from it together** — result, model, and visualisations in one bundle means reload restores the full work without retraining.
- **A multi-model-ready format costs little now and avoids a breaking change later** — the `models` dict keyed by `model_id` is the cheap version of "design for the next cycle".
- **Tests must travel with the change** (D-024) — a suite that lags the code silently loses its value.

## 7. Key Decisions Reinforced

- **D-024 (new):** design-changing implementations must be accompanied by automated tests — feature additions add tests; retired paths modify/remove their tests; contract changes update the tests that exercise them.
- **D-001 / algorithm-agnostic design:** `save_model`/`load_model` sit on `BaseAlgorithm`, so persistence stays algorithm-agnostic (LDA/NMF will implement the same interface).
- **D-008 / pinned dependencies:** `requirements-dev.txt` extends the pinned-stack discipline to the dev toolchain.
- **D-021:** the result carries its own identity (`model_id`) and data, which made the multi-model-ready `models` dict natural.

*Detailed rationale for each is recorded in `dev_docs/current/03_control/decisions.md`.*

## 8. Outputs of Cycle 5

### Notes / control artefacts
- `dev_docs/current/03_control/decisions.md` — D-024 (test discipline).
- `dev_docs/current/04_working/cycle_plan.md` — v0.5.0 section (completed and ready to close).
- `dev_docs/current/04_working/tasks.md` — Cycle 5 implementation tasks by work package; close tasks.
- `dev_docs/current/04_working/current_state.md` — Cycle 5 status (at the close stage).
- `dev_docs/current/05_knowledge/skus/v0.5.0.md` — SKU-05-01 (cycle-coded; WP2/WP3 persistence; WP1 trivial).

### Code artefacts
- `tests/` — 38 tests + `conftest.py` (fixtures incl. a small-corpus BERTopic model); `pytest.ini`; `requirements-dev.txt`.
- `app/models/topic_result.py` — `model_id` field.
- `app/models/algorithms/base_algorithm.py` — `save_model`/`load_model` abstract methods.
- `app/models/algorithms/bertopic.py` — `save_model`/`load_model` (native save/load, `model.pt` in the per-model dir); `model_id` in `_build_result`; `nr_topics='auto'` retry-without-reduction fix.
- `app/models/services/project_service.py` — zip-bundle save/load (`.stella` = `project.json` + `model/{model_id}/` + `viz/{model_id}/`), Option A `models` dict, `_rebuild_result` int-key conversion.
- `app/models/services/exporter.py` — multi-model-ready `to_json` (mirrors `project.json`, no texts), `to_csv_topics`/`to_csv_assignments` with Model ID column, `_iter_models`.
- `app/views/panels/summary_panel.py` — Detail-button fix (stale `_doc_filter_label` reference).
- `app/views/panels/export_panel.py` — layout tweak (description frame + `wraplength`).

### Design knowledge
- The consolidated learnings in §6.
- A multi-model-ready persistence format (Option A `models` dict) — `current_model_id` and editable display names deferred to the multi-model cycle.

## 9. Cycle Outcome

Cycle 5 delivered the v0.5.0 feature set: a committed `pytest` suite (38 tests) for the model + controller layer, model persistence (zip-bundle `.stella` with a multi-model-ready `models` dict, per-algorithm save/load behind `BaseAlgorithm`), and multi-model-ready exports. **Status: complete; pending release to `main`.**

## 10. Likely Next Cycle Direction

**Cycle 6** would release v0.5.0 to `main` (merge → verify → delete → fresh branch, per D-017) and then take on the post-graduation backlog: **LDA/NMF algorithms** (the real test of the algorithm-agnostic design — D-001), **multi-model support** (`current_model_id`, editable display names, model switching), document search/filter hardening, and batch processing — plus extending the suite to the view layer and wiring in coverage reporting.
