# App Development Roadmap

## Version 0.2.0


## Version 0.1.0

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
