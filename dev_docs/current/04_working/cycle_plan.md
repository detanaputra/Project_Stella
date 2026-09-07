# Cycle Plan

#working #plan #cycles

The multi-cycle roadmap. Each version/cycle entry uses the cycle_plan form (goal / outcomes / focus / success signal / status). Raw, undeveloped ideas live in `ideas.md` and are promoted here once refined.

## Version 0.5.0

### Main goal
Harden the codebase with a committed test suite, then deliver the designed model-persistence feature so researchers can save and reload their full work (result, model, and visualisations) without retraining.

### Main outcomes
- **WP1 — Test suite** — a committed `pytest` suite for the model + controller layer (headless, no GUI): `AppState`, `DataLoader`, `BERTopicAlgorithm` (train + merge/delete on a small corpus), controllers, `Exporter`, `topic_quality`, `ProjectService` (current behavior). Adds `requirements-dev.txt` (pytest, black, flake8, isort, mypy). Reusable fixtures in `conftest.py`, including a small-corpus BERTopic model fixture.
- **WP2 — Persistence, model layer** — `model_id` on `TopicResult`; `save_model(model, path)` / `load_model(path)` on `BaseAlgorithm`; BERTopic implementation via native `model.save()` / `BERTopic.load()`; a `save → load → compare` round-trip test that doubles as the feasibility check (embedding-model include/exclude, size).
- **WP3 — Persistence, service + UI** — `ProjectService` reworked to a single-file zip bundle (`.stella` = archive) holding `project.json` (state + full result data) + `model/{model_id}/` + `viz/{model_id}/`; timestamp model-id + editable display name; controller save/load methods; save/load dialogs updated. Existing `ProjectService` tests updated; new round-trip tests added.

### Primary focus
- Test suite first (hardening; de-risks the persistence rework)
- Model persistence (the user-visible feature)

### Success signal
`pytest` passes on the model/controller layer; a user can save a project, reload it, and see the same topics, metrics, and visualisations — with the trained model restored (no retrain).

### Status
Completed and ready to close.

## Version 0.4.0

### Main goal
Give researchers control over their topic model — refine topics (merge/delete/label) with a clear selection UI — and close the remaining UX gaps (retire the unused pywebview route, explain the metrics, fix dialog placement, limit MVP options).

### Main outcomes
- **Topic refinement** — select topics in the results table (leading checkbox column, whole-row toggle, row highlight) → merge, delete, or label:
  - Delete via native `model.delete_topics([t])` (documents → outlier -1); Merge via native `model.merge_topics(texts, [t1, t2, …])`; Label stores `{topic_id: label}` on the result (shown in the topics table)
  - Re-derive pipeline after any mutation: rebuild `TopicResult` → recompute `quality_metrics` → regenerate the 5 PNGs + 5 HTMLs → update state (background thread + loading panel)
  - Extract the "build `TopicResult` from a fitted model" logic out of `BERTopicAlgorithm.train` into a shared helper
  - Icon + text toolbar (ttkbootstrap `icon=` + `text=`, `icon_only=False`) after the basic stats, before the topics table; buttons disabled by default (delete 1+, merge 2+, label 1); merge/delete confirmation dialogs
- **Retire pywebview** — remove `request_visualization` + `_launch_bertopic_webview`, drop the `pywebview` dependency, remove `multiprocessing.freeze_support()` from `main.py`
- **Metrics-tab explanations for beginners** — plain-language meaning for each metric gauge
- **Fix dialog placement** — anchor the Export/Settings dialogs to the centre of the main window
- **MVP option limiting** — sentence-transformer model limited to `all-MiniLM-L6-v2`; language limited to English
- **Document exploration** *(emerged during Cycle 4)* — find documents and see their topics:
  - **Topic filter** — selecting topics in the topics table filters the Document Assignments table to docs whose Topic 1 (argmax) is one of the selected topics; combines AND with the search filter
  - **Search** — a search box + "Search" button above the Document Assignments table (not per-keystroke); case-insensitive substring match on the document text; a "Clear" resets to all docs
  - **Column refactor** — the Document Assignments table shows Doc Index · Document · Topic 1 · Prob 1; the Document cell shows the first 50 chars, or the substring around the query match when searching
  - **Detail window** — a "Detail" button (enabled when one doc row is selected) opens a centered Top-Level window showing Doc Index, all topic→probability pairs, and the full document in a scrollable read-only Text (paragraphs supported)
  - **Data plumbing** — store `original_texts` in the result metadata at training time (currently only preprocessed texts are kept) and carry it through refinement (`_build_result` + `merge_topics`/`delete_topics`)

### Primary focus
- Topic refinement (the main feature)
- Retire pywebview (dead-code cleanup)

### Success signal
A user can select topics in the results table, merge/delete/label them (with confirmation), and see the tables, metrics, and visualisations update — with the pywebview route gone and the remaining UX gaps closed.

### Status
Completed.

## Version 0.3.0

### Main goal
Bring the BERTopic visualisations into the app as in-app tabs and restructure the main-window layout.

### Main outcomes
- 5 visualisation tabs (topics, heatmap, barchart, hierarchy, term_rank) in the main Notebook, after Metrics, shown only when a result exists
- Each tab: a static matplotlib chart (from Plotly `to_dict()` data) + an "Open interactive" button that opens the Plotly HTML in the default browser
- All 5 static PNGs + 5 offline HTML files pre-generated in the pipeline after metrics (tabs and "Open interactive" are instant; the HTML files are stable)
- Layout restructure: toolbox removed; parameter panel moved to a persistent left column; Export and Settings become top-level panels under File Menu (theme switcher stays in the Settings panel)

### Primary focus
- In-app visualisation tabs (static matplotlib via `to_dict()`)
- Main-window layout restructure

### Success signal
A user can open each of the 5 visualisations as a tab inside the app, see a static chart, and click "Open interactive" to get the full Plotly figure in the browser — with the toolbox gone and parameters on the left.

### Status
Completed.

## Version 0.2.0

### Main goal
- Publish the project on GitHub: README (description, goal, benefits) and Apache 2.0 license
- MouseWheel scrolling in the parameter panels (no scrollbar grabbing)
- Show topic quality metrics in a new "Metrics" tab:
    - NPMI coherence
    - C_V coherence
    - UMass coherence
    - Topic Diversity

### Main outcomes
- README with description, goal, and benefit of the application
- Apache 2.0 License file in the repo
- MouseWheel scrolling in the parameter panels
- New "Metrics" tab (after the Analysis tab) shows topic quality metrics — 4 gauge/donut charts, one per metric
- [deferred to a later cycle] LDA/NMF algorithms, embedded charts, search/filter, batch processing
- Topic quality metrics computed with Gensim (`CoherenceModel`); Topic Diversity implemented in-app

### Primary focus
- GitHub repo presentation (README + license)
- UI scrolling ergonomics
- Topic quality metrics in a new "Metrics" tab
- [deferred to a later cycle] exercising the algorithm-agnostic abstraction with a second algorithm

### Success signal
- A user can scroll parameters without touching the scrollbar
- A user can see their topic quality in the Metrics tab

### Status
Completed.

### Project Management
- Write the README with the application's description, goal, and benefits

### User Interface
- Attach a MouseWheel event to the scrollable containers in `algorithm_settings_panel.py` and the wizard's `panel_hyperparams.py` so users can scroll up/down without grabbing the scrollbar

### Results & Export
- Compute and display topic quality metrics in a new "Metrics" tab (added to the main Notebook after the Analysis tab once a result exists) — 4 gauge/donut charts, one per metric, each showing the model's single (averaged) value:
    - NPMI, C_V, UMass coherence via Gensim's `CoherenceModel`
    - Topic Diversity implemented in-app (not provided by Gensim)
- Coherence computed on the training corpus, using each topic's top-10 words
- Metrics computed in the background during the training pipeline; the Metrics tab stays visible while `current_result` holds a model

## Version 0.1.0 (done)

### Main goal
Deliver a complete, audited, releasable BERTopic topic-modelling desktop application for non-technical researchers.

### Main outcomes
- BERTopic training with configurable hyperparameters (below)
- Guided 4-step wizard, result tables, `.stella` save/load, browser visualizations, retrain
- 22 audit findings fixed; v0.1.0 released from `main`

### Primary focus
- core topic modelling reliability
- data loading and validation
- result export and interactive visualization

### Success signal
A user can upload data, train, view topics, retrain, save/load, and export — zero crashes on the happy path, and every audit finding resolved.

### Status
Completed.

### Core Topic Modelling
- BERTopic algorithm with configurable hyperparameters: language, embedding model, top-N words, n-gram range, minimum topic size, number of topics, low-memory mode, and probability calculation
- UMAP dimensionality reduction (neighbors, components, metric, low-memory) and HDBSCAN clustering (min samples, min cluster size, metric)
- Training runs in a background thread so the UI stays responsive, with stage-based progress reporting
- Standardized `TopicResult` output: top terms per topic, per-document topic assignments, and model metadata for reproducibility

### Data Loading & Validation
- CSV and TXT file loading with a 10-line preview
- Validation with research guidance: small/moderate sample-size warnings and average document-length checks
- Robust CSV handling: automatic text-column detection, NaN/empty-row filtering, and UTF-8 → Latin-1 encoding fallback

### User Interface
- Main window with Analysis, Export, and App Settings tabs
- Summary panel: document/topic counts, top topics, and per-document topic assignments
- Algorithm settings panel with BERTopic, UMAP, and HDBSCAN parameter sections
- Export panel: CSV, JSON, methodology report, and browser visualizations
- App Settings tab with a ttkbootstrap theme switcher
- File and Edit menus (new/save/load project, exit; cut/copy/paste/undo/redo)
- Topic Model Wizard for guided project setup
- Modal loading panel with live status updates

### Results & Export
- Summary statistics and top-topic tables
- Export to CSV, JSON, and a methodology report (Markdown)
- Interactive Plotly visualizations (topics, heatmap, barchart, hierarchy) exported as offline HTML and opened in the browser

### Project Management
- Save and load project state (`.stella` files) with validation of algorithm and parameters

### Reliability & Robustness
- Thread-safe UI updates via a main-thread event dispatcher
- Re-entrancy guard preventing duplicate training runs
- Exception-isolated event processing so one bad callback cannot freeze the UI
- Parameter validation: UMAP neighbor clamping for small corpora, n-gram range clamping
- Offline-capable visualizations (plotly.js embedded, no CDN required)

## Working Principles

- Small controlled enhancements over uncontrolled expansion.
- Note consolidation is a checkpoint activity, not continuous.
- Prefer the smaller, more traceable implementation that gets the next working step done cleanly.

## Review Rule

Review this plan at cycle end, on major shifts, or when drift recurs.
