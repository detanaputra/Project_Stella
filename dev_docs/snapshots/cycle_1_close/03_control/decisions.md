# Design Decisions

#decision #design #learn

## Simple Notes Capture Rule
Append short bullet points during active development; do not worry about perfect note placement. Consolidation happens at cycle end.

Append when the point is about:
- something you have decided
- something you want to lock for now
- something that affects implementation consistency

## Purpose
Record the important architectural and implementation decisions made during the project (ADR-style decision log).

- includes reasoning and trade-offs
- evolves across cycles
- **source of truth for design decisions**
- referenced by `dev_docs/cycle_record_notes/cycle_1.md` §7 and `cycle_1_review.md` instead of duplicating rationale

## Status
- `active` — governs the current phase
- `revised` — replaced or amended
- `deprecated` — no longer applies

---

## Cycle 1 Decisions

### D-001: MVC with an algorithm-agnostic `BaseAlgorithm` over a central `AppState`
#### Status
active
#### Context
The UI must not depend on BERTopic internals; LDA/NMF are planned. Cycle 1 built the whole application from a single-file MVC scaffold.
#### Decision
Package-per-layer MVC (`app/models`, `app/views`, `app/controllers`); a central `AppState` (observer pattern) as the single state store; `BaseAlgorithm` + `BERTopicAlgorithm` behind it.
#### Rationale
Centralized state plus an algorithm abstraction keeps views independent of algorithm internals, so a new algorithm is additive rather than a refactor.
#### Consequences
Panels and controllers stay decoupled and testable; every algorithm integration point goes through `BaseAlgorithm`.
#### Review Trigger
When adding LDA/NMF — confirm the abstraction still fits without per-algorithm UI changes.

### D-002: 4-step wizard setup flow
- **Status:** active
- **Decision:** Non-technical users set up a model through a 4-step wizard (algorithm/file → preview → hyperparameters → summary), not one dense form.
- **Rationale:** Sequential steps lower cognitive load for researchers without programming skills.

### D-003: Transient UI (loading panel) owned by `MainWindow`, driven by state
### Status
active
### Context
The loading panel was parented to the wizard, so it was destroyed when the wizard closed.
### Decision
`show_loading_panel()` moved to `MainWindow`; the panel subscribes to `AppState` and closes itself when `analysis_in_progress` turns false.
### Rationale
A widget's lifetime follows its parent — tying transient UI to state at the app level lets it outlive the view that triggered it.
### Review Trigger
Any new modal/overlay UI — confirm it is owned at the level it must outlive.

### D-004: Weak-ref observers in `AppState`
- **Status:** active
- **Decision:** Observers stored via `weakref.WeakMethod`; `notify()`/`process_events()` drop dead references; `LoadingPanel` state updates guarded against destroyed widgets.
- **Consequences:** Subscribed widgets are garbage-collected after destruction; stale Tk callbacks no longer touch destroyed widgets.

### D-005: Modular hyperparameter sections with prefixed state keys
#### Status
active
#### Decision
`app/views/panels/hyperparams/` with `base_section.py`, `bertopic_section.py`, `umap_section.py`, `hdbscan_section.py`; prefixed keys (`umap_*`, `hdbscan_*`); reused in both the wizard and the main-window settings panel.
#### Rationale
One implementation, two surfaces; prefixes prevent key collisions between algorithm parameter families.

### D-006: Results as 7-column tables
- **Status:** active
- **Decision:** Topics table `("Topic ID", "Word 1", "Weight 1", …, "Word 3", "Weight 3")`; doc-topics table `("Doc Index", "Topic 1", "Prob 1", …, "Topic 3", "Prob 3")`, shown only when a result exists.
- **Rationale:** Interleaved term/weight (and topic/probability) columns keep data scannable and the two tables consistent.

### D-007: `.stella` project file via `ProjectService`
- **Status:** active
- **Decision:** Save/load through `_on_save()`/`_on_load()` in `file_menu.py` with a `.stella` extension, wired to `ProjectService`.
- **Rationale:** A project-file format (rather than raw exports) gives users session continuity.

### D-008: Pinned requirements
- **Status:** active
- **Decision:** All dependency versions pinned to the installed set (ttkbootstrap==2.2.0, bertopic==0.17.4, pandas==2.2.2, numpy==1.26.4, matplotlib==3.9.2, seaborn==0.13.2, plotly==5.24.1).
- **Rationale:** Reproducibility is non-negotiable for a tool shipped to researchers.

### D-009: Browser-based visualizations via pywebview in a separate process
#### Status
active
#### Context
`WebViewException('pywebview must be run on a main thread.')` — the Tk main loop is occupied by the UI.
#### Decision
`main.py` calls `multiprocessing.freeze_support()`; visualizations launch in a separate process; per-monitor DPI awareness (ctypes) for crisp scaling.
#### Rationale
Renders BERTopic's native Plotly figures without bundling a browser engine.
#### Review Trigger
If packaging (PyInstaller) changes process behavior, re-verify the webview launch path.

### D-010: Retrain bound to the shown parameters via widget traces
- **Status:** active
- **Decision:** Each hyperparameter section's widgets bound to `algorithm_params` via traces.
- **Rationale:** The form and the state are separate stores — they must stay in sync or retrains silently use stale defaults.

---

## Cycle 1 Review Decisions

### D-011: Read-only audit first; fixes by severity, one commit per class
- **Status:** active
- **Decision:** A read-only `audit.md` (H1–H6 / M1–M8 / L1–L8) precedes any change; fixes grouped by severity, one commit per class (`10b822e`, `a02d9f5`, `fdd421b`, `86f8dd5`).
- **Rationale:** Preserves a clean baseline and keeps fix history readable; each batch is one testable unit.
- **Review Trigger:** At the next release gate — repeat the read-only audit pattern.

### D-012: The parameter form re-renders only on structural change (H1 fix)
#### Status
active
#### Context
`AlgorithmSettingsPanel._render()` rebuilt the form on every keystroke, destroying the edit mid-typing.
#### Decision
The form re-renders only on structural changes, never per keystroke. — commit `10b822e`
#### Rationale
Distinguish structural from value changes to avoid a rebuild loop triggered by the very keystroke it receives.

### D-013: Thread-safe UI dispatch via `AppState.call_on_main`
#### Status
active
#### Context
Several M-findings only became safe once state changes reached the UI on the main thread.
#### Decision
All UI updates are dispatched through `AppState.call_on_main` (thread-safe dispatch). — commit `fdd421b`
#### Rationale
The linchpin M-fix — other fixes depend on main-thread delivery of state.

### D-014: Summary-panel render guard: distinct sentinel + init before build (M3 fix)
#### Status
active
#### Context
`AttributeError: 'SummaryPanel' object has no attribute '_last_result'` — the guard read the attribute before init, and keying on `None` collided with the legitimate "no result yet" state.
#### Decision
The attribute is set before `_build_ui()` runs `_render()`, and a sentinel distinct from `None` renders the placeholder on a fresh start. — commit `0383ce1`
#### Rationale
A guard on `None` cannot distinguish "not yet built" from "no result"; a distinct sentinel plus correct init order resolves both.

### D-015: Committed `.gitignore` with `.claude/` exclusion
- **Status:** active
- **Decision:** Project `.gitignore` created (`.claude/`, `__pycache__`, `*.pyc`, venvs, IDE files) and already-tracked artifacts untracked. — commit `baa3443`
- **Rationale:** A committed ignore file is only half the fix — tracked artifacts need explicit untracking.

### D-016: Force-push policy — `--force-with-lease` only
- **Status:** active
- **Decision:** Reconcile stale branches by rebasing onto current `main`; push with `--force-with-lease`.
- **Rationale:** Safe force-push — fails if the remote moved unexpectedly.

### D-017: Release workflow — merge → verify → delete → fresh branch from `main`
#### Status
active
#### Context
The audit branch was merged and deleted on GitHub; local state had to be reconciled without losing work.
#### Decision
Release procedure: merge to `main` → verify every commit reached `main` → delete local branch (prune stale remote ref) → create a fresh branch from `main` for the next version.
#### Rationale
Verifying before deleting prevents silent work loss; branching fresh from `main` gives a clean baseline for the next release.

### D-018: `ROADMAP.md` as the categorized version feature record
- **Status:** active
- **Decision:** `ROADMAP.md` documents the v0.1.0 feature set under six level-3 categories; the v0.2.0 section left empty. — commit `50ec71c`
- **Rationale:** Categorized, versioned features make the roadmap scannable and scaffold the next version.

### D-019: Normalize BERTopic output shape before mapping documents
- **Status:** active
- **Decision:** Reshape 1-D `probs` (single-topic runs) before mapping; translate internal cluster ids → final topic ids in the `probs` extraction.
- **Rationale:** BERTopic's output shape and cluster-id space vary by run; code must normalize before mapping documents to topics.

---

## Cycle 1 Quick Captures

- **Quick Capture — BERTopic's `probs` shape and cluster-id mapping are the two correctness cliffs** of the doc-topic table; every future algorithm export must normalize the same way.
- **Quick Capture — parameter plumbing (UI ↔ state ↔ `train()`) is the top risk surface.** The audit flagged it; the build bugs matched. Validate types at the algorithm boundary on every new parameter.
