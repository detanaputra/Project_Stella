# Ideas

#working #ideas

Raw capture of undeveloped ideas — no format pressure; a holding area. Ideas here are **not committed**; they are refined and promoted to `cycle_plan.md` (or `tasks.md`) once they mature. Once they are promoted, they are then deleted from this file.

## Cycle 4 candidates
- **Retire pywebview** — the separate-process route (D-009) is now unused (no view calls `request_visualization`); the localhost path is confirmed working. Retire it: remove `request_visualization` + `_launch_bertopic_webview`, drop the `pywebview` dependency, and remove `multiprocessing.freeze_support()` from `main.py`.
- **Topic refinement** — select topics in the results table → merge, delete, or label (from `cycle_2_review.md` §3). Design settled in Cycle 4 planning:
  - **Delete** — native `model.delete_topics([t])`; the deleted topic's documents are mapped to the outlier topic (-1), as BERTopic does natively. Mutates the model in place.
  - **Merge** — native `model.merge_topics(texts, [t1, t2, …])`; needs the training docs (`result.metadata['texts']`). UX: multi-select two or more rows → click Merge.
  - **Label** — in scope: store a user interpretation per topic (`{topic_id: label}`) on the result; shown in the topics table (no model mutation).
  - **Re-derive pipeline** — after any mutation: rebuild `TopicResult` (topics, doc_topics, `model_info`) from the mutated model → recompute `quality_metrics` → regenerate the 5 PNGs + 5 HTMLs → update `state.current_result` (tables, gauges, viz tabs re-render). Runs in a background thread with the loading panel.
  - **Refactor** — extract the "build `TopicResult` from a fitted model" logic out of `BERTopicAlgorithm.train` into a reusable helper, shared by training and refinement (keeps the doc-topic probability mapping correct after `topic_mapper_` remaps ids).
  - **UI** — SummaryPanel (`summary_panel.py`): refinement toolbar placed after the basic stats and before the topics table; icon-only buttons via ttkbootstrap `icon=` + `icon_only=True` (Bootstrap Icons glyphs, e.g. merge → `git-merge`, delete → `trash`, label → `tag`). Toolbar [Merge Selected] [Delete Selected] [Label…], all disabled by default. Delete enabled when 1+ topics selected; Merge enabled when 2+ topics selected; Label enabled when exactly 1 topic selected. Merge and Delete both pop a confirmation dialog — the re-derive pipeline runs only after the user confirms.
  - **Selection mechanism** — Treeview/Tableview have no native checkboxes (maintainer-confirmed), so the topics table gets a leading checkbox column (☐/☑ glyph toggle). Clicking **anywhere on a row** toggles its checkbox and updates a selected-topic set; the state is mirrored into the Treeview's native selection (`selectmode="none"`, `selection_add`/`selection_remove`) so the row also highlights with the theme's selection color — glyph and highlight stay in sync. Selection resets when the result changes (after refinement), which is correct since topic ids change.
  - **Risk** — metrics must be recalculated after each refinement (§5) — handled by the re-derive pipeline.
- **Metrics-tab explanations for beginners** — the gauges show numbers with no plain-language meaning; add beginner-facing explanations for each metric (from `cycle_2_review.md` §3).
- **Fix dialog placement** — the top-level Export/Settings dialogs spawn at seemingly random locations; anchor them to the centre of the main window (`cycle_3_review.md` §3).
- **MVP option limiting** — for the MVP, limit the sentence-transformer model options to `all-MiniLM-L6-v2` only, and the language option to English only.

## Deferred to Other Cycle (backlog)

- **Model persistence + project folder** *(deferred from Cycle 4 — designed, not built; targeted for the next cycle)* — the "rename the temp output path" idea grew into a model-identity + persistence feature. Design settled in Cycle 4 planning:
  - **Single `.stella` file = a zip bundle** containing the project folder tree: `project.json` (state + full result data), `model/`, and `viz/`. Portable: the one file moves everything. (Not a plain JSON file, and not a loose folder — a single-file archive.)
  - **Model id** — timestamp-based internal id (e.g. `20260905-193012`) plus a display name (editable in a future cycle; "Model 1/2" style). The id names the per-model subfolders: `model/{model_id}/` and `viz/{model_id}/`.
  - **Persistence scope** — save/load must restore the result data (topics, doc_topics, `quality_metrics`, `model_info`), the visualisations (files), and the topic model itself. Today `.stella` saves only `model_info` and `load_project` resets `current_result` to `None` (user must retrain).
  - **Model format — per-algorithm native save/load behind a `BaseAlgorithm` contract (Option B)** — add `save_model(model, path)` / `load_model(path)` to `BaseAlgorithm`; `path` is the per-model directory `model/{model_id}/`, and each algorithm fills it with its library's native serialization: BERTopic → `model.save()`/`BERTopic.load()` (folder), LDA (gensim) → `lda.save()`/`LdaModel.load()` (folder), NMF (sklearn) → `joblib.dump`/`load` (file). The app never knows the algorithm — the persistence twin of D-001. (Rejected: pickling the whole result — version-fragile and a code-execution risk for shared projects.)
  - **Result data stays JSON** — topics, doc_topics, `quality_metrics`, `model_info` live in `project.json`, so the UI (tables, gauges, viz tabs) restores instantly without loading the model; the model loads lazily when something needs it (regeneration, topic refinement).
  - **AppState** — no new field for now; `current_result.model_id` is the id. A `current_model_id` field only arrives with multi-model.
  - **Output layout** — inside the bundle: `model/{model_id}/` (per-model model save) and `viz/{model_id}/` (per-model 5 PNGs + 5 HTMLs); `TopicVisualizer` must serve the current model's dir, not one fixed dir.
  - **Feasibility check needed** — BERTopic `save()`/`load()` in this environment (embedding-model include/exclude — excluding keeps the bundle small and re-instantiates by name from the local sentence-transformers cache; including is self-contained but larger), and resulting size, before committing.
- Post-graduation backlog: LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing

## Housekeeping / engineering

- Test suite — no committed `tests/` exists; `architecture.md` and `development.md` note it is planned (view testing deferred until the suite is added)
- PyInstaller packaging / distribution — planned in `CLAUDE.md` (Week 5 optional, GitHub Releases for researchers); no `.spec`/`dist/` build exists
- CI workflow — documented in `development.md` (GitHub Actions); no `.github/workflows/` exists
- `data_contracts.md` extraction — `02_contracts/README.md` open gap: currently folded into `api.md`; consider extracting if it grows
