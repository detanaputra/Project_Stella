# Tasks

#working #tasks #cycle3 #implementation

## Working Rule

During active development, append brief points rather than trying to place everything perfectly. Consolidation and restructuring happen at checkpoints and cycle end.

When choosing between options:
- prefer the smaller implementation
- prefer the more traceable implementation
- prefer the implementation that gets the next working step done cleanly

---

## Cycle 1 Close Tasks (documentation hardening)

- [x] create `cycle_1.md` and `cycle_1_review.md`
- [x] create `dev_docs/current/03_control/decisions.md` (D-001..D-019, with commit refs)
- [x] create `dev_docs/current/03_control/repository_structure.md` (file→role mapping)
- [x] create `dev_docs/current/05_knowledge/reflection.md` (cycle learnings)
- [x] create `dev_docs/current/04_working/source_of_truth.md` (authority map + conflict resolution)
- [x] create `dev_docs/current/04_working/current_state.md`
- [x] create `dev_docs/current/04_working/tasks.md`
- [x] upgrade `ROADMAP.md` to cycle_plan format (goal / outcomes / focus / success signal / status)
- [x] create `dev_docs/current/03_control/snapshot_workflow.md`
- [x] create `dev_docs/snapshots/cycle_1_close/` (frozen handoff)
- [x] create `dev_docs/current/02_contracts/` (`code_map.md`, contract index)
- [x] create `dev_docs/current/05_knowledge/references.md`
- [x] triage + renumber SKU files with cycle-coded IDs, move to `dev_docs/current/05_knowledge/skus/`
- [x] delete duplicate `claude.md`; link `audit.md` from `cycle_1_review.md`

## Drift Remediation (detect-drift run)

- [x] delete leftover scaffold `app/controllers/controller.py` (also `model.py`/`view.py` remain — see note below)
- [x] rewrite `dev_docs/current/02_contracts/api.md` to match the codebase
- [x] update `dev_docs/current/01_system/architecture.md` (delete Folder Structure; fix Flows 1–3, registry, tests, layer paths)
- [x] fix code so views call the controller (ARCH-3/ARCH-4): wizard panels, preview panel, viz panel, settings schema
- [x] decide whether to delete leftover scaffold `app/models/model.py` and `app/views/view.py` (unimported; flagged, not deleted) — deleted

## Cycle 2 Opening Tasks

### A. v0.2.0 planning
- [x] write remaining v0.2.0 `ROADMAP.md` entries in cycle_plan form (goal / outcomes / focus / success signal / status)
- [x] decide Cycle 2 scope: README + Apache 2.0 license, MouseWheel scrolling, topic quality metrics (new "Metrics" tab); LDA/NMF deferred to a later cycle
- [x] open the cycle-2 start handoff set (codebase + `current_state.md` + `source_of_truth.md` + task-relevant notes)

### B. SKU/evidence follow-ups
- [x] add commit refs to the v0.1.0 SKUs when the build commits are identified
- [x] decide whether to keep a `/evidence`-style home for `logs/` transcripts — resolved: `logs.md` archived to `dev_docs/snapshots/cycle_1_close/`; no `/evidence` home needed (transcripts are not required evidence per canonical SHAPR)

### C. Document-control continuity
- [x] update `current_state.md` at the end of this hardening pass
- [x] keep `audit.md` and any status doc in sync with the changes they record — resolved: `audit.md` archived to `dev_docs/snapshots/cycle_1_close/` (cycle-1 review evidence; no longer active)

## Cycle 2 Implementation Tasks (v0.2.0)

### GitHub presentation
- [x] write README with description, goal, and benefits of the application
- [x] add Apache 2.0 license file

### User Interface
- [x] attach MouseWheel event to the scrollable container in `algorithm_settings_panel.py` (main window settings panel)
- [x] attach MouseWheel event to the scrollable container in the wizard's `panel_hyperparams.py`

### Topic quality (Metrics tab)
- [x] add `quality_metrics` field to `TopicResult` (contract `api.md` + dataclass) — D-021
- [x] add `gensim` to `requirements.txt` (pinned)
- [x] implement topic quality service: NPMI/C_V/UMass via Gensim `CoherenceModel` + hand-rolled Topic Diversity
- [x] wire the pipeline to compute metrics in the background after training and set `result.quality_metrics`
- [x] implement `MetricPanel` (ttk.Frame; matplotlib gauge/donut charts, one per metric)
- [x] wire `MainWindow` to add the "Metrics" tab (after Analysis) once a result exists; keep it while `current_result` holds a model

## Cycle 2 Close Tasks

- [x] consolidate SKUs: create `v0.2.0.md` (SKU-02-01…04); merge v0.1.1 into `v0.1.0.md`; cycle-coded IDs
- [x] write `cycle_2.md` cycle record (build + review)
- [x] take a cycle-2 close snapshot (`dev_docs/snapshots/cycle_2_close/`)
- [x] update `ROADMAP.md` v0.2.0 status → Completed

## Cycle 3 Opening Tasks

- [x] brainstorm the v0.3.0 scope (per `cycle_2_review.md` §7) — decided: visualisation tabs + layout restructure; topic refinement deferred to cycle 4
- [x] write the `cycle_plan.md` v0.3.0 section
- [x] open `current_state.md` for the cycle

## Cycle 3 Implementation Tasks (v0.3.0)

### WP1 — Static viz service + visualisation tabs
- [x] `to_dict()` → matplotlib converter (dispatch on trace type: scatter, heatmap, bar, dendrogram) for the 5 visualisations
- [x] add 5 viz tabs (topics, heatmap, barchart, hierarchy, term_rank) to the main Notebook after Metrics, shown only when a result exists
- [x] pre-generate all 5 static PNGs + 5 offline HTML files in the pipeline after metrics (replaced the original lazy/on-click design)
- [x] "Open interactive" button per tab → opens the Plotly HTML in the default browser (served over a local http://localhost server)

### WP2 — Layout restructure
- [x] remove the toolbox panel (and the dead `toolbox_panel.py` / `bertopic_viz_panel.py`)
- [x] move the parameter panel to a persistent left column
- [x] Export and Settings → top-level panels under File Menu (theme switcher stays in the Settings panel)

## Cycle 3 Close Tasks

- [x] write `cycle_3.md` cycle record (drafted)
- [x] write `cycle_3_review.md` (drafted)
- [x] take the cycle-3 close snapshot (`dev_docs/snapshots/cycle_3_close/`)
- [x] release v0.3.0 to `main` (merge → verify → delete → fresh branch, D-017) — PR #3 (`e646fe4`)
- [x] commit the cycle-close docs batch (`be0a130`)

## Cycle 4 Opening Tasks

- [x] decide Cycle 4 scope (per `ideas.md` Cycle 4 candidates — retire pywebview, topic refinement, metrics-tab plain-language explanations, fix dialog placement, MVP option limiting)
- [x] write the `cycle_plan.md` v0.4.0 section
- [x] update `current_state.md` for the cycle

## Cycle 4 Implementation Tasks (v0.4.0)

### WP1 — Topic refinement
- [x] refactor: extract "build `TopicResult` from a fitted model" out of `BERTopicAlgorithm.train` into a reusable helper (shared by training and refinement; keeps the doc-topic probability mapping correct after `topic_mapper_` remaps ids)
- [x] implement refinement operations: delete via native `model.delete_topics([t])` (documents → outlier -1); merge via native `model.merge_topics(texts, [t1, t2, …])` (needs `result.metadata['texts']`)
- [x] implement label support: store `{topic_id: label}` on the result; show the label in the topics table
- [x] implement the re-derive pipeline: rebuild `TopicResult` (topics, doc_topics, `model_info`) → recompute `quality_metrics` → regenerate 5 PNGs + 5 HTMLs → update `state.current_result` (background thread + loading panel)
- [x] add controller methods for merge/delete/label that run the re-derive pipeline
- [x] SummaryPanel: add a leading checkbox column (☐/☑ glyph toggle) to the topics table; clicking anywhere on a row toggles; mirror into native selection (`selectmode="none"`, `selection_add`/`selection_remove`) for row highlight
- [x] SummaryPanel: add a toolbar (ttkbootstrap `icon=` + `text=`, `icon_only=False`) after the basic stats, before the topics table — merge (`sign-merge-left`), delete (`trash`), label (`tag`)
- [x] button enablement: all disabled by default; delete enabled when 1+ topics selected; merge enabled when 2+ topics selected; label enabled when exactly 1 topic selected
- [x] confirmation dialogs for merge and delete; run the pipeline only after the user confirms

### WP2 — Retire pywebview
- [x] remove `request_visualization` + `_generate_visualization` + `_launch_bertopic_webview` from `app_controller.py`
- [x] drop `pywebview==5.2.1` from `requirements.txt`
- [x] remove `multiprocessing.freeze_support()` from `main.py`

### WP3 — Metrics-tab explanations for beginners
- [x] add plain-language explanations for each metric gauge (NPMI, C_V, UMass, Topic Diversity) in `metric_panel.py`

### WP3 — Fix dialog placement
- [x] anchor the Export/Settings dialogs to the centre of the main window (`open_export_dialog` / `open_settings_dialog` in `main_window.py`)

### WP3 — MVP option limiting
- [x] limit the sentence-transformer model options to `all-MiniLM-L6-v2` only (`bertopic_section.py`)
- [x] limit the language option to English only (`bertopic_section.py`)

### WP4 — Document exploration
- [x] store `original_texts` in the result metadata at training time (controller sets it after processing); carry it through refinement (`_build_result` + `merge_topics`/`delete_topics` copy it)
- [x] refactor the Document Assignments table columns to Doc Index · Document · Topic 1 · Prob 1 (drop the Topic 2/3 columns)
- [x] Document cell: first 50 chars normally; when searching, show the substring around the query match
- [x] add a search Entry + "Search" button above the Document Assignments table (not per-keystroke); case-insensitive substring match on the full document text; a "Clear" resets to all docs
- [x] add a "Detail" button (enabled when exactly one doc row is selected) that opens a centered Top-Level window
- [x] Detail window: shows Doc Index, all topic→probability pairs, and the full document in a scrollable read-only Text (paragraphs supported)
- [x] topic filter: selecting topics in the topics table filters the Document Assignments table to docs whose Topic 1 is one of the selected topics (combines AND with the search filter)

## Cycle 4 Close Tasks

- [x] document SKUs (`v0.4.0.md` — SKU-04-01…06)
- [x] write `cycle_4.md` cycle record
- [x] update `reflection.md` (Cycle 4 consolidated quick capture)
- [x] update `current_state.md`
- [x] take the cycle-4 close snapshot (`dev_docs/snapshots/cycle_4_close/`)
- [x] write `cycle_4_review.md`
- [x] commit the cycle-close docs batch (`23f5bac`)
- [x] release v0.4.0 to `main` (merge → verify → delete → fresh branch, D-017) — PR #4 (`e951036`), branch deleted, `v0.5.0` created

## Cycle 5 Opening Tasks

- [x] decide Cycle 5 scope (test suite first, then model persistence — per the Cycle 4 close assessment)
- [x] write the `cycle_plan.md` v0.5.0 section
- [x] update `current_state.md` for the cycle

## Cycle 5 Implementation Tasks (v0.5.0)

### WP1 — Test suite
- [x] add `requirements-dev.txt` (pytest, black, flake8, isort, mypy)
- [x] set up `tests/` + `conftest.py` with reusable fixtures (incl. a small-corpus BERTopic model fixture)
- [x] test `AppState` (subscribe/notify/process_events, weakref pruning, `call_on_main`)
- [x] test `DataLoader` (load_texts, load_preview, validate_file, CSV/encoding edge cases)
- [x] test `BERTopicAlgorithm` (train on a small corpus → `TopicResult` shape; merge/delete → updated result; `_build_result`)
- [x] test controllers (`AppController.on_file_selected`/`on_algorithm_changed`; `AnalysisController.run_analysis` against a stub state)
- [x] test services (`Exporter`, `topic_quality`, `static_viz`, `ProjectService` current behavior)

### WP2 — Persistence, model layer
- [x] add `model_id` to `TopicResult` (generated at training time)
- [x] add `save_model(model, path)` / `load_model(path)` to `BaseAlgorithm`
- [x] implement BERTopic `save_model`/`load_model` via native `model.save()`/`BERTopic.load()` (embedding-model include/exclude decision)
- [x] write the `save → load → compare` round-trip test (doubles as the feasibility check)

### WP3 — Persistence, service + UI
- [x] rework `ProjectService` to a single-file zip bundle (`.stella` = archive): `project.json` (state + full result data) + `model/{model_id}/` + `viz/{model_id}/`
- [x] timestamp model-id + editable display name (model-id done; display name deferred to a future cycle per the design)
- [x] update controller save/load methods (verified: delegate unchanged, ProjectService signature stable)
- [x] update the save/load dialogs (file → archive) (verified: `.stella` file UX unchanged; the format is internal)
- [x] update existing `ProjectService` tests + add new round-trip tests

## Small Operational Tasks

- [x] add remote GitHub repository — `origin` → github.com/detanaputra/Project_Stella
- [x] connect local Git repository to GitHub remote
- [x] confirm `.gitignore` still matches project needs after GitHub setup
