# App Development Roadmap

## Version 0.2.0

### Main goal
- General description to be displayed in github repo
- smoother parameter scrolling
- display topic quality metric to the user, using Octis (https://github.com/MIND-Lab/OCTIS). Topic quality to be implemented in this version:
    - NPMI coherence
    - C_V coherence
    - UMass coherence
    - Topic Diversity

### Main outcomes
- README with description, goal, and benefit of the application to be displayed in github repo
- MouseWheel scrolling in the settings panel (no sash grabbing)
- summary tab now contain topic quality metric instead of topic result. topic result is moved to the next tab called Topic Model.
- [postponed to very last feature to add] LDA/NMF algorithms, embedded charts, search/filter, batch processing

### Primary focus
- General description of the project in Readme file
- UI scrolling ergonomics
- Redesign the summary to display topic quality metric.
- [postponed to very last feature to add] exercising the algorithm-agnostic abstraction with a second algorithm

### Success signal
- A user can scroll parameters without touching the sash.
- user can see their topic quality in the summary tab

### Status
Planned.

### Project Management
- Write readme file and put the description, goal, and benefit of this application.

### User Interface
- Attach MouseWheel event to scrollable container in algorithm_settings_panel.py so user can scroll down or up without grabbing shash.

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
