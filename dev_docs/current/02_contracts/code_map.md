# Code Map

#contract #module #mapping #control

## Purpose
Define the stable note-to-code mapping for the current implementation state. Reduces drift between conceptual notes, actual code files, and function contracts.

## Current Code Structure

- `main.py` — entry point; `multiprocessing.freeze_support()` for the webview process
- `app/controllers/` — `app_controller.py`, `analysis_controller.py`
- `app/models/` — `app_state.py` (observer state), `topic_result.py` (standardized output)
- `app/models/algorithms/` — `base_algorithm.py`, `bertopic.py`
- `app/models/services/` — `data_loader.py`, `processor.py`, `exporter.py`, `visualizer.py`, `project_service.py`, `topic_quality.py`
- `app/views/` — `main_window.py`, `menu_manager.py`
- `app/views/menus/` — `base_menu.py`, `file_menu.py`, `edit_menu.py`
- `app/views/panels/` — `toolbox_panel.py`, `summary_panel.py`, `metric_panel.py`, `algorithm_settings_panel.py`, `loading_panel.py`, `export_panel.py`
- `app/views/panels/hyperparams/` — `base_section.py`, `bertopic_section.py`, `umap_section.py`, `hdbscan_section.py`
- `app/views/panels/visualizations/` — `bertopic_viz_panel.py`
- `app/views/wizard/` — `wizard_main.py`, `panel_algorithm.py`, `panel_preview.py`, `panel_hyperparams.py`, `panel_summary.py`

## Note-to-Code Mapping

| Note / doc | Code it covers |
|---|---|
| `dev_docs/current/01_system/architecture.md` | Overall MVC structure, data flow, `main_window.py` layout (2-column paned, Notebook) |
| `dev_docs/current/02_contracts/api.md` | Contracts for `BaseAlgorithm`, `AppState`, `TopicResult`; service signatures |
| `dev_docs/current/02_contracts/bertopic_hyperparams.md` | `app/models/algorithms/bertopic.py`; `app/views/panels/hyperparams/*` |
| `dev_docs/current/03_control/decisions.md` | Decisions map to commits across `app/` (see each decision's commit ref) |
| `dev_docs/cycle_record_notes/*` | Development process across the whole artefact |
| `dev_docs/current/05_knowledge/skus/v0.1.0.md` (SKUs) | Knowledge units; refer to the files named in each SKU's Context/Decision |
| `dev_docs/current/05_knowledge/skus/v0.2.0.md` (SKUs) | Knowledge units for the v0.2.0 metrics feature; refer to the files named in each SKU's Context/Decision |
| `dev_docs/snapshots/cycle_1_close/audit.md` | Audit evidence (archived); findings reference files across `app/` |
| `dev_docs/current/04_working/cycle_plan.md` | Feature-level plan; not tied to specific files |

## Contract layer boundaries

- **Function contracts:** authoritative in `dev_docs/current/02_contracts/api.md` — callable signatures for `BaseAlgorithm`, `AppState`, services.
- **Data contracts:** authoritative in `dev_docs/current/02_contracts/api.md` + `app/models/topic_result.py` (`TopicResult`), `app/models/app_state.py` (`AppState`).
- **Parameter contract:** authoritative in `dev_docs/current/02_contracts/bertopic_hyperparams.md` — the 14 documented hyperparameters wired into `train()`.

If code and contract disagree → treat as **drift**; explicitly decide whether to update code, contract, or both (see `dev_docs/current/04_working/source_of_truth.md`).

## Updating this map

Update `code_map.md` in the same change as any file move/rename or module restructure. The map is the note↔code stability contract.
