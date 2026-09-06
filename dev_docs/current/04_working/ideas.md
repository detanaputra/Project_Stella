# Ideas

#working #ideas

Raw capture of undeveloped ideas — no format pressure; a holding area. Ideas here are **not committed**; they are refined and promoted to `cycle_plan.md` (or `tasks.md`) once they mature. Once they are promoted, they are then deleted from this file.

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
- Post-graduation backlog:
  - LDA/NMF algorithms (exercises the `BaseAlgorithm` abstraction — D-001)
  - Multi-model support ("Model 1", "Model 2", …) — metrics already stored per-`TopicResult` (D-021)
  - Embedded matplotlib charts
  - Batch processing

## Housekeeping / engineering

- Test suite — committed `tests/` exists (v0.5.0, WP1) covering the model + controller layer; view testing deferred
- PyInstaller packaging / distribution — planned in `CLAUDE.md` (Week 5 optional, GitHub Releases for researchers); no `.spec`/`dist/` build exists
- CI workflow — documented in `development.md` (GitHub Actions); no `.github/workflows/` exists
- `data_contracts.md` extraction — `02_contracts/README.md` open gap: currently folded into `api.md`; consider extracting if it grows