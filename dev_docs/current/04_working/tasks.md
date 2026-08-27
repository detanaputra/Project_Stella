# Tasks

#working #tasks #cycle2 #implementation

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
- [x] triage + renumber SKU files with global IDs, move to `dev_docs/current/05_knowledge/skus/`
- [x] delete duplicate `claude.md`; link `audit.md` from `cycle_1_review.md`

## Drift Remediation (detect-drift run)

- [x] delete leftover scaffold `app/controllers/controller.py` (also `model.py`/`view.py` remain — see note below)
- [x] rewrite `dev_docs/current/02_contracts/api.md` to match the codebase
- [x] update `dev_docs/current/01_system/architecture.md` (delete Folder Structure; fix Flows 1–3, registry, tests, layer paths)
- [x] fix code so views call the controller (ARCH-3/ARCH-4): wizard panels, preview panel, viz panel, settings schema
- [ ] decide whether to delete leftover scaffold `app/models/model.py` and `app/views/view.py` (unimported; flagged, not deleted)

## Cycle 2 Opening Tasks

### A. v0.2.0 planning
- [x] write remaining v0.2.0 `ROADMAP.md` entries in cycle_plan form (goal / outcomes / focus / success signal / status)
- [x] decide Cycle 2 scope: README + Apache 2.0 license, MouseWheel scrolling, topic quality metrics (new "Metrics" tab); LDA/NMF deferred to a later cycle
- [ ] open the cycle-2 start handoff set (codebase + `current_state.md` + `source_of_truth.md` + task-relevant notes)

### B. SKU/evidence follow-ups
- [ ] add commit refs to the v0.1.0 SKUs when the build commits are identified
- [ ] decide whether to keep a `/evidence`-style home for `logs/` transcripts

### C. Document-control continuity
- [ ] update `current_state.md` at the end of this hardening pass
- [ ] keep `audit.md` and any status doc in sync with the changes they record

## Cycle 2 Implementation Tasks (v0.2.0)

### GitHub presentation
- [ ] write README with description, goal, and benefits of the application
- [ ] add Apache 2.0 license file

### User Interface
- [x] attach MouseWheel event to the scrollable container in `algorithm_settings_panel.py` (main window settings panel)
- [ ] attach MouseWheel event to the scrollable container in the wizard's `panel_hyperparams.py`

### Topic quality (Metrics tab)
- [x] add `quality_metrics` field to `TopicResult` (contract `api.md` + dataclass) — D-021
- [ ] add `gensim` to `requirements.txt` (pinned)
- [ ] implement topic quality service: NPMI/C_V/UMass via Gensim `CoherenceModel` + hand-rolled Topic Diversity
- [ ] wire the pipeline to compute metrics in the background after training and set `result.quality_metrics`
- [ ] implement `MetricPanel` (ttk.Frame; matplotlib gauge/donut charts, one per metric)
- [ ] wire `MainWindow` to add the "Metrics" tab (after Analysis) once a result exists; keep it while `current_result` holds a model

## Deferred to Later Cycles

- [ ] LDA/NMF algorithms (exercises the `BaseAlgorithm` abstraction — D-001)
- [ ] embedded matplotlib charts (vs. browser-only visualizations)
- [ ] document search/filter
- [ ] batch processing
- [ ] multi-model support ("Model 1", "Model 2", …) — metrics already stored per-`TopicResult` (D-021)

## Small Operational Tasks

- [x] add remote GitHub repository — `origin` → github.com/detanaputra/Project_Stella
- [x] connect local Git repository to GitHub remote
- [x] confirm `.gitignore` still matches project needs after GitHub setup
