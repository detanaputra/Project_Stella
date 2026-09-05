# Cycle Plan

#working #plan #cycles

The multi-cycle roadmap. Each version/cycle entry uses the cycle_plan form (goal / outcomes / focus / success signal / status). Raw, undeveloped ideas live in `ideas.md` and are promoted here once refined.

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
