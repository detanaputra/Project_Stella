# Cycle 1

#cycle1 #formal_record #build #shapr

## Cycle Title
Build the interactive BERTopic topic-modelling desktop application — the v0.1.0 feature set.

## 1. Context

The project needed a first complete, runnable release of a topic-modelling GUI for non-technical social scientists: upload CSV/TXT, train a BERTopic model, view structured results, export, and visualise interactively — with zero programming required. This cycle covered the entire build (2026-08-08 → 2026-08-17), reconstructed as 44 SKUs in `dev_docs/v0.1.0.md` from `logs.md`.

Cycle framing:
- **Main goal:** ship the v0.1.0 feature set (MVC app, wizard setup, loading feedback, result tables, save/load, visualizations, retrain).
- **Main outcomes:** full MVC application with BERTopic support; 4-step setup wizard; modular hyperparameters; result tables; `.stella` project files; pinned dependencies; pywebview visualizations.
- **Success signal:** a user can upload data, train, view topics, retrain with tweaked params, save/load, and export plots — without crashes on the happy path.

## 2. Explore

Design questions investigated and the answers the cycle converged on:

- **2.1 What starting structure?** A minimal single-file MVC scaffold (`model.py` / `view.py` / `controller.py` / `main.py`), then expanded into `app/models`, `app/views`, `app/controllers` packages.
- **2.2 How to keep the UI algorithm-agnostic?** Centralised `AppState` (observer pattern) + `BaseAlgorithm` abstraction so LDA/NMF can be added later without refactoring the UI.
- **2.3 How should a non-technical user set up a model?** A 4-step wizard (algorithm/file → preview → hyperparameters → summary) rather than one dense form.
- **2.4 Who owns transient UI (the loading panel)?** Parented to the wizard it disappeared with it — ownership had to move to the main window, tied to state.
- **2.5 Why does BERTopic throw `'bool' object is not iterable`?** Parameter types were mismatched across the UI → state → `BERTopicAlgorithm.train()` boundary.
- **2.6 Why did result tables mis-assign topics?** Two shape issues: 1-D `probs` (single-topic run) and a missing internal-cluster-id → final-topic-id mapping.
- **2.7 How to render interactive BERTopic plots?** pywebview — but it throws `WebViewException` unless launched off the Tk main thread.

## 3. Build

### 3.1 MVC scaffold → full application
Scaffolded the single-file MVC, moved it into `app/models` + `app/views` + `app/controllers`, then built the full layer set: `AppState` (observer state), `TopicResult`, `BaseAlgorithm` + `BERTopicAlgorithm`, `DataLoader`, `ProjectService`, controllers, first UI panels.

### 3.2 Menus
`MenuManager` assembling the top-level bar, then split into one class per menu parent (`base_menu.py`, `file_menu.py`, `edit_menu.py`, `view_menu.py`).

### 3.3 Layout, panels, wizard
- 3-column paned layout (toolbox / Notebook; summary / parameters) with `ttk.PanedWindow`.
- Content areas extracted into `toolbox_panel.py`, `summary_panel.py`, `algorithm_settings_panel.py`.
- 4-step Topic Model Wizard in `app/views/wizard/` (algorithm+file → preview → hyperparameters → summary).

### 3.4 Loading panel
`loading_panel.py` with an indeterminate progress bar, wired to the wizard's Train; then moved to `MainWindow` and subscribed to `AppState` so it persists past wizard closure and auto-closes when `analysis_in_progress` turns false.

### 3.5 Observer lifecycle
`AppState` observers stored via `weakref.WeakMethod`; `notify()`/`process_events()` drop dead references; `LoadingPanel` state updates guarded against destroyed widgets.

### 3.6 Modular hyperparameters
`app/views/panels/hyperparams/` with `base_section.py`, `bertopic_section.py`, `umap_section.py`, `hdbscan_section.py`; wizard panel refactored to use them; prefixed state keys (`umap_*`, `hdbscan_*`); scrollable (Canvas + Scrollbar, no mousewheel); sections also instantiated in `algorithm_settings_panel.py`; sash thickness 8.

### 3.7 Result tables
`summary_panel.py` `_create_table()` with Treeview tables, shown only when a result exists; topics table and doc-topics table both widened to 7 columns (term/weight pairs, topic/probability pairs).

### 3.8 Save/load & dependencies
`_on_save()`/`_on_load()` in `file_menu.py` (extension `.stella`, wired to `ProjectService`); `requirements.txt` expanded to the full set and pinned to installed versions (ttkbootstrap 2.2.0, bertopic 0.17.4, …).

### 3.9 Visualizations
`bertopic_viz_panel.py` rendering BERTopic's native Plotly figures via pywebview 5.2.1; `multiprocessing.freeze_support()` in `main.py` so the webview launches in a separate process; loading indicator during figure generation; per-monitor DPI awareness (ctypes) for crisp scaling; generalized `_on_request_visualization(method_name, title)` launcher covering topics, heatmap, barchart, term rank, hierarchy.

### 3.10 Retrain & pipeline fixes
`Retrain Model with Current Params` button above the scrollable settings; each hyperparameter section's widgets bound to `algorithm_params` via traces so Retrain uses shown values; `self.state` renamed to `self.appState: AppState` (stop shadowing the widget `state` property); pipeline debug logging in `AnalysisController`.

## 4. Use

- Wizard flow exercised end-to-end: algorithm/file → preview → hyperparameters → summary → Train.
- Loading panel observed during training; Next/Previous navigation verified after the pack-order fix.
- Retrain run from the main window with tweaked hyperparameters.
- Result tables inspected for doc-topic assignments and topics after training and after retrain.
- Project saved to and loaded from `.stella`.
- All five BERTopic visualizations opened in the webview (topics, heatmap, bar chart, term rank, hierarchy).

## 5. Evaluate

### 5.1 What worked well
- MVC separation held: panels, controllers, and state stayed decoupled and individually testable.
- The wizard materially lowered setup complexity for a non-technical flow.
- Modular hyperparameter sections were reused in two surfaces (wizard + settings panel) with no key collisions.
- Interactive Plotly visualizations rendered crisply via the separate-process webview.

### 5.2 Remaining limitations / issues found
- Wizard nav buttons vanished (pack order — the notebook consumed all vertical space).
- Hyperparameter panel scrolled sections off-screen; then a bad edit removed all three sections.
- `invalid command name ".!loadingpanel…"` during weak-ref cleanup (callbacks touching destroyed widgets).
- `current_result = False` after training — subscriber was fine; failure was in the training pipeline.
- Retrain silently trained with defaults because UI widgets and state were disconnected until traces were bound.
- `'numpy.float64' object is not iterable` on single-topic runs; doc-topic table collapsed to Topic 0 on multi-topic runs until the cluster-id mapping was fixed.
- Visualization freeze: several seconds with no feedback until a loading indicator was added.

## 6. Learn

Consolidated insights (the cycle's knowledge output):

- **Algorithm-agnostic architecture pays early.** A centralized `AppState` plus `BaseAlgorithm` let the UI ignore algorithm internals — the foundation for future LDA/NMF.
- **Widget lifetime follows its parent.** A panel owned by a transient view (the wizard) dies with it; tie persistent UI to `AppState` at the app level instead.
- **Strong observer references leak.** Subscribers outliving their widgets keep them alive; weak references break the cycle — and callbacks must still guard against destroyed widgets.
- **Tk geometry is pack-order dependent.** A greedily-expanding widget packed first starves everything after it; off-screen-but-instantiated widgets are a view concern.
- **Parameter values cross many layers.** UI → state → algorithm: types must be validated at the algorithm boundary, and the form must be bound to state (traces) or retrains silently use stale defaults.
- **Attribute shadowing is silent breakage.** `self.state` clobbered the Tk widget `state` property; rename before it bites.
- **BERTopic's output shape varies.** Single-topic `probs` are 1-D; internal cluster ids differ from final topic ids — normalize/translate before mapping documents.
- **Webview wants a main thread.** Launching the Plotly webview in a separate process satisfies pywebview and keeps the Tk loop responsive.
- **Pinned dependencies are non-negotiable** for a tool distributed to researchers — reproducibility beats "latest."
- **Debug-logging wins.** Instrument each pipeline stage; a vague symptom becomes a specific failing stage.

## 7. Key Decisions Reinforced

- MVC with algorithm-agnostic `BaseAlgorithm` + central `AppState` (observer, weak-ref).
- 4-step wizard flow for non-technical setup.
- Loading panel owned by `MainWindow`, driven by `analysis_in_progress`.
- Modular hyperparameter sections with prefixed state keys.
- Results as 7-column tables (term/weight and topic/probability pairs).
- `.stella` project file format; `ProjectService` for persistence.
- Pinned `requirements.txt`.
- Browser-based visualizations via pywebview in a separate process (no embedded browser engine).

*Detailed rationale for each is recorded in `dev_docs/03_control/decisions.md`.*

## 8. Outputs of Cycle 1

### Notes / control artefacts
- `dev_docs/v0.1.0.md` — 44 SKUs (this cycle's knowledge units).
- `CLAUDE.md`, `ARCHITECTURE.md`, `API.md`, `DEVELOPMENT.md` — project docs (root).
- `BERTopicHyperparams.md` — hyperparameter reference.

### Code artefacts
- `app/models/` — `app_state.py`, `topic_result.py`, `algorithms/base_algorithm.py`, `algorithms/bertopic.py`.
- `app/views/` — `menu_manager.py`, `menus/`, `main_window.py`, `panels/` (`loading_panel.py`, `summary_panel.py`, `toolbox_panel.py`, `algorithm_settings_panel.py`, `hyperparams/`, `visualizations/`), `wizard/`.
- `app/controllers/` — app + analysis controllers.
- `app/services/` — `data_loader.py`, `project_service.py`.
- `main.py`, `requirements.txt` (pinned), `.gitignore`.

### Design knowledge
- The 10 consolidated learnings in §6, plus the SKU-level insights in `dev_docs/v0.1.0.md`.

## 9. Cycle Outcome

Cycle 1 produced a complete, runnable v0.1.0 application: BERTopic training with visible progress, structured result tables, retrain-in-place, `.stella` save/load, and five interactive webview visualizations. Every happy-path blocker found (param plumbing, topic mapping, retrain-stale-params, single-topic crash) was resolved in-cycle. Outstanding: the code had never been audited as a whole — correctness beyond the happy path was unknown. **Status: functionally complete; not yet releasable without an audit.**

## 10. Likely Next Cycle Direction

**The audit-and-harden work is `cycle_1_review.md`** (read-only audit with prioritized findings, fixes by severity, then release v0.1.0 and scaffold v0.2.0 — reconstructed as the v0.1.1 SKUs in `dev_docs/v0.1.1.md`). After that review closes, the next real cycle is **Cycle 2 — v0.2.0 feature set**: LDA/NMF algorithms, embedded matplotlib charts, document search/filter, batch processing. Write the v0.2.0 `ROADMAP.md` entries and open `current_state.md` for the cycle.
