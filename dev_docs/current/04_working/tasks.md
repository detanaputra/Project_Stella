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

## Cycle 2 Opening Tasks

### A. v0.2.0 planning
- [ ] write remaining v0.2.0 `ROADMAP.md` entries in cycle_plan form (goal / outcomes / focus / success signal / status)
- [ ] decide Cycle 2 scope: README, MouseWheel scrolling first; LDA/NMF later
- [ ] open the cycle-2 start handoff set (codebase + `current_state.md` + `source_of_truth.md` + task-relevant notes)

### B. SKU/evidence follow-ups
- [ ] add commit refs to the v0.1.0 SKUs when the build commits are identified
- [ ] decide whether to keep a `/evidence`-style home for `logs/` transcripts

### C. Document-control continuity
- [ ] update `current_state.md` at the end of this hardening pass
- [ ] keep `audit.md` and any status doc in sync with the changes they record

## Deferred to Later Cycles

- [ ] LDA/NMF algorithms (exercises the `BaseAlgorithm` abstraction — D-001)
- [ ] embedded matplotlib charts (vs. browser-only visualizations)
- [ ] document search/filter
- [ ] batch processing

## Small Operational Tasks

- [ ] write README with description, goal, and benefits of the application (v0.2.0)
- [ ] attach MouseWheel event to the scrollable container in `algorithm_settings_panel.py` (v0.2.0)
- [ ] add remote GitHub repository later
- [ ] connect local Git repository to GitHub remote
- [ ] confirm `.gitignore` still matches project needs after GitHub setup
