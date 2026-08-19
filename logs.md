# LOG FILE
This is a file that log the interaction between human developer and AI coding partner. This document is presented with this format:
- timestamp: [timestamp when user prompt the AI coding partner]
- prompt: [what human developer has instructed to AI coding partner]
- changes made by AI coding partner: [what changes AI coding partner has made in response to human developer's prompt]
- recap: [summarise from AI coding partner so far]
## v0.1.0

Interactions below are reconstructed from the Claude session transcripts in `logs/v0.1.0/` (2026-08-08 → 2026-08-17).

### 2026-08-08 — Scaffold, architecture, and initial build

- timestamp: 2026-08-08 07:12 UTC
- prompt: Analyze this codebase and create a CLAUDE.md file for future Claude Code instances.
- changes made by AI coding partner: none — the working directory was empty, so no analysis was possible.
- recap: The directory contains no files yet; project setup must come first.

- timestamp: 2026-08-08 07:14 UTC
- prompt: Scaffold a Model–View–Controller ttkbootstrap application.
- changes made by AI coding partner: created `requirements.txt`, `model.py`, `view.py`, `controller.py`, `main.py`.
- recap: A minimal single-file MVC scaffold is in place.

- timestamp: 2026-08-08 07:59 UTC
- prompt: Create a real-world MVC folder structure and move the scaffold files into it.
- changes made by AI coding partner: created `app/models`, `app/views`, `app/controllers` (each with `__init__.py`) and moved the scaffold files accordingly.
- recap: The project now follows a conventional MVC package layout.

- timestamp: 2026-08-08 08:42 UTC
- prompt: Read CLAUDE.md, ARCHITECTURE.md, DEVELOPMENT.md, and API.md and propose changes for the current project.
- changes made by AI coding partner: analyzed the docs; produced a plan for a full MVC implementation with social-scientist-friendly features.
- recap: The docs define a coherent MVC design; a build plan was proposed.

- timestamp: 2026-08-08 08:44 UTC
- prompt: Suggestion accepted — implement it.
- changes made by AI coding partner: built the full MVC application: `AppState` (observer state), `TopicResult`, `BaseAlgorithm` + `BERTopicAlgorithm`, `DataLoader`, `ProjectService`, controllers, and the first UI panels.
- recap: The minimal scaffold became a complete MVC application with BERTopic support.

- timestamp: 2026-08-08 17:41 UTC
- prompt: Create a global menu manager in the views folder for File → Save / Load / New (prints are fine for now), and keep the default Window menu.
- changes made by AI coding partner: created `app/views/menu_manager.py` and wired it into `main_window.py`.
- recap: A global `MenuManager` assembles the top-level menu bar.

- timestamp: 2026-08-08 17:57 UTC
- prompt: Menu commands will clutter `menu_manager.py`; split into one file per menu parent (File, Edit, View).
- changes made by AI coding partner: created `app/views/menus/` with `base_menu.py`, `file_menu.py`, `edit_menu.py`, `view_menu.py`; slimmed `menu_manager.py`.
- recap: Each top-level menu now lives in its own class that handles its child commands.

- timestamp: 2026-08-08 18:24 UTC
- prompt: Change to a 3-column layout: outer PanedWindow (toolbox left, Notebook right), inner PanedWindow (summary frame left, parameters right).
- changes made by AI coding partner: rewrote the layout in `main_window.py` using `ttk.PanedWindow` and a `ttk.Notebook`.
- recap: The main window now matches the requested 3-column paned layout.

### 2026-08-10 — Panel extraction and the wizard

- timestamp: 2026-08-10 08:01 UTC
- prompt: Refactor `main_window.py` by moving the toolbox, summary, and algorithm-parameter frames to their own files.
- changes made by AI coding partner: created `toolbox_panel.py`, `summary_panel.py`, `algorithm_settings_panel.py`; `main_window.py` now only assembles them.
- recap: The three content areas are now dedicated panel classes.

- timestamp: 2026-08-10 09:03 UTC
- prompt: Create a wizard-style flow for creating a new topic model: hidden-tab Notebook with Next/Previous buttons and 4 panels (algorithm choice + file picker, preview, hyperparameters, summary).
- changes made by AI coding partner: created `app/views/wizard/` with `panel_algorithm.py`, `panel_preview.py`, `panel_hyperparams.py`, `panel_summary.py`, `wizard_main.py`; linked it from the File menu.
- recap: A 4-step Topic Model Wizard guides setup: algorithm/file → preview → hyperparameters → summary.

### 2026-08-11 — Loading panel

- timestamp: 2026-08-11 20:03 UTC
- prompt: Implement a loading panel: Train closes the wizard, opens the loading panel, and closes it when training completes and the result shows in the summary panel.
- changes made by AI coding partner: created `app/views/panels/loading_panel.py` with an indeterminate progress bar; wired the wizard's Train action to it.
- recap: Users now get visible progress feedback while training runs.

- timestamp: 2026-08-11 20:37 UTC
- prompt: Move the loading panel logic to the main window — its parent was the wizard, so it closed when the wizard closed; make it subscribe to AppState.
- changes made by AI coding partner: moved `show_loading_panel()` to `MainWindow`; the wizard no longer owns the panel; the panel closes itself when `analysis_in_progress` becomes false.
- recap: The loading panel now persists past wizard closure and auto-closes on completion.

### 2026-08-12 — Observer cleanup and summary tables

- timestamp: 2026-08-12 12:32 UTC
- prompt: Investigate why BERTopic throws `'bool' object is not iterable`; compare with `notebooks/test_sample.ipynb`.
- changes made by AI coding partner: investigated the parameter plumbing between UI, state, and `BERTopicAlgorithm.train()`.
- recap: Identified how a boolean/mismatched parameter reaches BERTopic's expected sequence.

- timestamp: 2026-08-12 19:30 UTC
- prompt: Implement weak references in `AppState` so destroyed subscribers are collected by the garbage collector.
- changes made by AI coding partner: reworked `app/models/app_state.py` — observers stored via `weakref.WeakMethod`, `notify()`/`process_events()` drop dead references.
- recap: Subscribed widgets no longer leak memory after destruction.

- timestamp: 2026-08-12 20:36 UTC
- prompt: In the summary panel, implement table views for doc topics and topics, shown only when a result exists.
- changes made by AI coding partner: `summary_panel.py` now renders Treeview tables for topics and per-document assignments after a result is available.
- recap: Results display as structured tables instead of plain labels.

### 2026-08-13 — Modular hyperparameters

- timestamp: 2026-08-13 21:02 UTC
- prompt: Read BERTopicHyperparams.md and implement its instructions.
- changes made by AI coding partner: created `app/views/panels/hyperparams/` with `base_section.py`, `bertopic_section.py`, `umap_section.py`, `hdbscan_section.py`; refactored the wizard's hyperparameter panel to use them; added prefixed param keys (`umap_*`, `hdbscan_*`).
- recap: BERTopic/UMAP/HDBSCAN settings are now modular, reusable sections with collision-free state keys.

### 2026-08-14 — Wizard fixes, tables, save/load, dependencies

- timestamp: 2026-08-14 05:45 UTC
- prompt: Investigate why the wizard's Next/Previous buttons disappear.
- changes made by AI coding partner: fixed pack order in `wizard_main.py` (the notebook was consuming all vertical space).
- recap: Navigation buttons are visible again.

- timestamp: 2026-08-14 06:08 UTC
- prompt: Investigate why only the BERTopic section appears in the wizard's hyperparameter panel (scroll issue?).
- changes made by AI coding partner: made the hyperparameter panel scrollable so UMAP/HDBSCAN sections are reachable.
- recap: Confirmed a scroll issue — the sections existed but were pushed off-screen.

- timestamp: 2026-08-14 06:13 UTC / 06:18 UTC
- prompt: "It is loading indefinitely" / "it runs indefinitely when clicking Next from the algorithm to hyperparameter panel."
- changes made by AI coding partner: investigated the analysis pipeline and LoadingPanel close conditions.
- recap: The LoadingPanel only appears on Train; the wizard's Next button does not start training.

- timestamp: 2026-08-14 07:49 UTC
- prompt: Remove the mousewheel behavior so the section can be verified first.
- changes made by AI coding partner: removed `_on_mousewheel` and `bind_all` from `panel_hyperparams.py`.
- recap: Scroll is now explicit via the scrollbar.

- timestamp: 2026-08-14 07:51 UTC
- prompt: Now the whole section has disappeared, including BERTopic.
- changes made by AI coding partner: restored the section-instantiation block that was accidentally removed in the prior edit.
- recap: All three sections render again in the wizard.

- timestamp: 2026-08-14 07:55 UTC
- prompt: Still getting `invalid command name ".!loadingpanel.!frame.!label"` — investigate the weak-ref cleanup mechanism.
- changes made by AI coding partner: guarded `LoadingPanel` state updates against destroyed widgets; tightened `AppState` observer cleanup.
- recap: Callbacks no longer touch destroyed widgets during the poll loop.

- timestamp: 2026-08-14 08:01 UTC
- prompt: Implement all three hyperparameter sections inside `algorithm_settings_panel.py`.
- changes made by AI coding partner: `algorithm_settings_panel.py` now instantiates BERTopic/UMAP/HDBSCAN sections when BERTopic is selected.
- recap: The main window's settings panel reuses the modular hyperparameter sections.

- timestamp: 2026-08-14 08:26 UTC
- prompt: Increase the sash thickness to 8.
- changes made by AI coding partner: increased canvas/sash thickness (8) in the hyperparameter UI.
- recap: The sash is easier to grab.

- timestamp: 2026-08-14 09:32 UTC
- prompt: Implement the algorithm settings sections inside a scrollable area (no mousewheel).
- changes made by AI coding partner: `algorithm_settings_panel.py` now wraps the sections in a Canvas + Scrollbar.
- recap: The settings panel scrolls like the wizard panel.

- timestamp: 2026-08-14 09:40 UTC
- prompt: In `summary_panel.py`, implement `_create_table()` with a Tableview and a separate probability column.
- changes made by AI coding partner: refactored `_create_table()`; the document-assignments table got a dedicated probability column.
- recap: Tables show terms/weights and topics/probabilities in separate columns.

- timestamp: 2026-08-14 09:50 UTC
- prompt: For the topics table, split each top term and its probability into its own column (7 columns total).
- changes made by AI coding partner: topics table is now `("Topic ID", "Word 1", "Weight 1", "Word 2", "Weight 2", "Word 3", "Weight 3")`.
- recap: The topics table shows the top 3 terms with their weights side by side.

- timestamp: 2026-08-14 10:18 UTC
- prompt: Do the same for the doc-topics table in `summary_panel.py`.
- changes made by AI coding partner: doc-topics table is now `("Doc Index", "Topic 1", "Prob 1", "Topic 2", "Prob 2", "Topic 3", "Prob 3")`.
- recap: Per-document assignments also display as 7 columns.

- timestamp: 2026-08-14 10:29 UTC
- prompt: Implement `_on_save()` and `_on_load()` in `file_menu.py`; the save extension is `.stella`.
- changes made by AI coding partner: added filedialog save/load; wired to `ProjectService`.
- recap: Projects can now be saved to and loaded from `.stella` files.

- timestamp: 2026-08-14 11:48 UTC
- prompt: Read `requirements.txt` and update it if needed.
- changes made by AI coding partner: expanded `requirements.txt` beyond `ttkbootstrap` to the full dependency set.
- recap: Dependencies now reflect what the project actually uses.

- timestamp: 2026-08-14 12:07 UTC
- prompt: Lock all dependency versions to the versions installed on this laptop.
- changes made by AI coding partner: pinned versions (e.g. ttkbootstrap==2.2.0, bertopic==0.17.4, pandas==2.2.2, numpy==1.26.4, matplotlib==3.9.2, seaborn==0.13.2, plotly==5.24.1, scikit-learn==1.x).
- recap: Reproducible environment via pinned requirements.

### 2026-08-16 — Visualizations, retrain, and bug fixes

- timestamp: 2026-08-16 10:37 UTC
- prompt: Create a BERTopic visualization panel in a new folder under `panels`, instantiate it into `toolbox_panel.py`, and render `current_result.visualize_topics()` via pywebview.
- changes made by AI coding partner: created `app/views/panels/visualizations/bertopic_viz_panel.py`; added `pywebview==5.2.1`; wired into the toolbox.
- recap: Interactive BERTopic plots render in a webview window.

- timestamp: 2026-08-16 10:46 UTC
- prompt: `WebViewException('pywebview must be run on a main thread.')` — try running it on the main thread.
- changes made by AI coding partner: `main.py` now calls `multiprocessing.freeze_support()`; the visualization launches in a separate process.
- recap: The webview now runs off the main thread correctly.

- timestamp: 2026-08-16 10:54 UTC
- prompt: The visualization takes several seconds and the app looks frozen — show an indeterminate loading panel until it displays.
- changes made by AI coding partner: the viz panel toggles `analysis_in_progress` and a loading indicator during figure generation.
- recap: Users get feedback while the plot builds.

- timestamp: 2026-08-16 11:59 UTC
- prompt: `self.state` overrides the widget's `state`; rename all occurrences to `self.appState` and type it as `AppState`.
- changes made by AI coding partner: renamed `self.state` → `self.appState: AppState` across all panels and controllers.
- recap: No more accidental overriding of the Tk widget `state` property.

- timestamp: 2026-08-16 12:07 UTC
- prompt: Implement the remaining visualization buttons: `visualize_heatmap()`, `visualize_barchart()`, `visualize_term_rank()`, `visualize_hierarchy()`.
- changes made by AI coding partner: generalized the viz panel with a `_on_request_visualization(method_name, title)` launcher and four buttons.
- recap: All four BERTopic visualizations are available from the toolbox.

- timestamp: 2026-08-16 12:15 UTC
- prompt: Make the device scale identical to pywebview's scale — the heatmap is blurry.
- changes made by AI coding partner: added per-monitor DPI awareness (ctypes, Windows) in the webview launcher.
- recap: Crisp, correctly-scaled plots.

- timestamp: 2026-08-16 12:24 UTC
- prompt: Add a Retrain button in `algorithm_settings_panel.py` that retrains with the current hyperparameters; keep it above the scrollable area.
- changes made by AI coding partner: added `Retrain Model with Current Params` (needs `AnalysisController`) above the scrollable sections.
- recap: Users can re-run training with tweaked parameters from the main window.

- timestamp: 2026-08-16 12:29 UTC
- prompt: Investigate why Retrain reverts parameters to defaults and trains with defaults.
- changes made by AI coding partner: traced the UI↔state disconnect; bound each section's widgets to `algorithm_params` via traces.
- recap: Parameter changes now flow to state; Retrain uses the shown values.

- timestamp: 2026-08-16 12:40 UTC
- prompt: After training, the summary panel doesn't display the result — does it receive the state-changed notification?
- changes made by AI coding partner: verified subscription; added debug logging to `_on_state_changed`.
- recap: Subscriber is correct; the problem was in the pipeline, not the notification.

- timestamp: 2026-08-16 12:48 UTC
- prompt: It prints `current_result = False` — the issue is in the training pipeline.
- changes made by AI coding partner: added pipeline debug logging to `AnalysisController` (load count, process return, exceptions).
- recap: Isolated the failure to the training path.

- timestamp: 2026-08-16 20:39 UTC
- prompt: `TypeError: 'numpy.float64' object is not iterable` in `bertopic.py` — related to `calculate_probabilities`?
- changes made by AI coding partner: fixed the 1-D `probs` case (single topic) by reshaping before mapping.
- recap: Single-topic runs no longer crash the doc-probability mapping.

- timestamp: 2026-08-16 21:12 UTC
- prompt: The doc-topic table assigns almost every document to Topic 0 despite 8 topics — investigate.
- changes made by AI coding partner: fixed the internal-cluster-id → final-topic-id mapping in the `probs` extraction.
- recap: Documents now map to the correct topics.

### 2026-08-17 — Housekeeping

- timestamp: 2026-08-17 07:10 UTC
- prompt: Create a `.gitignore` and exclude all `.pyc` files (and anything else that shouldn't be tracked).
- changes made by AI coding partner: added `.gitignore` excluding `__pycache__`, `*.pyc`, virtual envs, IDE files, etc.
- recap: Compiled artifacts stay out of version control.

## v0.1.1