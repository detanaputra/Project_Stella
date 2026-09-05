# Naming Conventions

#contract #naming #control

## Purpose

Define the naming rules for this project — files, modules, classes, functions, constants, state keys, and documentation IDs. This is the **naming-rule truth** for AI-assisted coding: generated code should follow these conventions so the codebase stays consistent and drift-free.

## Python code

### Files and modules

- `snake_case.py` — e.g. `app_state.py`, `data_loader.py`, `algorithm_settings_panel.py`.
- Package-per-layer: `app/models`, `app/views`, `app/controllers`; sub-packages by role (`app/models/services`, `app/views/panels`, `app/views/wizard`, `app/views/menus`, `app/views/panels/hyperparams`). (`panels/visualizations/` was removed in v0.3.0 WP2 — static-visualisation panels live directly under `panels/`.)

### Classes

- `PascalCase` — e.g. `AppState`, `TopicResult`, `MainWindow`.
- Role suffixes:

| Role | Suffix | Examples |
|---|---|---|
| Panel (ttk.Frame) | `*Panel` | `SummaryPanel`, `MetricPanel`, `AlgorithmSettingsPanel`, `StaticVizPanel`, `ExportPanel`, `PreviewPanel`, `HyperparamPanel` |
| Modal overlay (Toplevel) | `*Panel` | `LoadingPanel` |
| Controller | `*Controller` | `AppController`, `AnalysisController` |
| Algorithm | `*Algorithm` | `BaseAlgorithm`, `BERTopicAlgorithm` |
| Service | `*Service` or descriptive | `ProjectService`, `DataLoader`, `Exporter`, `TopicVisualizer`, `TopicProcessor` |
| Menu | `*Menu` | `BaseMenu`, `FileMenu`, `EditMenu` |
| Hyperparameter section | `*Section` | `BaseHyperparamSection`, `BERTopicSection`, `UMAPSection`, `HDBSCANSection` |
| Wizard | `TopicModelWizard` | `wizard_main.py` |

### Methods and functions

- `snake_case` — e.g. `on_file_selected`, `run_analysis`, `get_param_schema`, `load_texts`.
- Controller event handlers use the `on_<noun>_<verb>` pattern (`on_file_selected`, `on_algorithm_changed`, `on_param_changed`).

### Constants

- `UPPER_SNAKE_CASE` — e.g. `AVAILABLE_ALGORITHMS`, `STATE_CHANGED`.

## State and parameter keys

- Prefixed by family to prevent collisions (D-005): `bertopic_*`, `umap_*`, `hdbscan_*` — e.g. `umap_n_neighbors`, `hdbscan_min_cluster_size`, `bertopic_top_n_words`.

## Wizard and menu file naming

- Wizard panels: `panel_<step>.py` — `panel_algorithm.py`, `panel_preview.py`, `panel_hyperparams.py`, `panel_summary.py`; main: `wizard_main.py`.
- Menus: one file per menu parent — `base_menu.py`, `file_menu.py`, `edit_menu.py`.

## Documentation and IDs

- Doc files: `snake_case.md` — e.g. `current_state.md`, `source_of_truth.md`, `repository_structure.md`.
- Decision IDs: `D-###` (sequential across the log).
- SKU IDs: `SKU-NN-NN` (cycle-coded, restart per cycle).
- Cycle records: `cycle_N.md` + `cycle_N_review.md`.
- Tags: inline `#tag` on the first 1–3 lines of a note (no YAML frontmatter).

## Anti-patterns

- **Do not shadow Tk widget properties with instance attributes** — `self.state` clobbers the widget `state` property; use `self.appState` (SKU-01-12).
- **Keep the algorithm registry key distinct from the class name** — the registry key is the display name (`"BERTopic"`); the class is `BERTopicAlgorithm`.
- **Spelling is not normalized** — `BERTopicVisualisation` uses the British spelling; match the existing name rather than "correcting" it.

## Authority

Authoritative for naming-rule truth. If code and this note disagree → the disagreement is **drift**; the current task must explicitly decide whether to update the code, the note, or both (see `dev_docs/current/04_working/source_of_truth.md`).
