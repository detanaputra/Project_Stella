# Cycle 4

#cycle4 #formal_record #build #shapr

## Cycle Title
Give researchers control over their topic model and their documents — topic refinement, document exploration, and cleanup (v0.4.0).

## 1. Context

The released v0.3.0 app (in-app visualisation tabs + layout restructure) let the user *look at* topics, but not *act on* them or on the documents behind them. Cycle 4 covered the v0.4.0 build (2026-09-05 → 2026-09-06), reconstructed as 6 SKUs (`SKU-04-01…06`) in `dev_docs/current/05_knowledge/skus/v0.4.0.md`. WP2 (retire pywebview) and WP3 (UI polish) were deliberately small/trivial work packages and produced no SKUs.

Cycle framing:
- **Main goal:** topic refinement (merge/delete/label) with a clear selection UI, document exploration (search + detail + topic filter), plus cleanup (retire the unused pywebview route) and polish (metrics explanations, centred dialogs, MVP option limiting).
- **Main outcomes:** 4 work packages delivered (see §3).
- **Success signal:** a user can select topics in the results table, merge/delete/label them with confirmation, find and inspect documents, and see the tables, metrics, and visualisations re-derive after each change.

## 2. Explore

Design questions investigated and the answers the cycle converged on:

- **2.1 How to merge/delete topics?** The initial assumption was that BERTopic had no native delete. Reading the library source (not just the docs page) showed `delete_topics(topics_to_delete)` and `merge_topics(docs, topics_to_merge)` — both mutate the model in place; delete maps deleted topics to the outlier -1 and needs no docs, merge needs the training documents.
- **2.2 How to select topics without native checkboxes?** Neither `ttk.Treeview` nor ttkbootstrap's `Tableview` has a checkbox column (maintainer-confirmed). Decision: a leading ☐/☑ glyph column, click-anywhere-to-toggle, mirrored into the Treeview's native selection so rows also highlight.
- **2.3 How to find a document / filter the Document Assignments?** Tableview ships a search bar, but it filters *displayed* cell values and is Enter-triggered. Decision: keep Treeview, search the full original text with a Search button; filter by selected topics (argmax) combined AND with the query.
- **2.4 What about the "rename temp path" idea?** It grew into a model-identity + persistence design (single-file zip bundle with `project.json` + `model/{model_id}/` + `viz/{model_id}/`, timestamp model-id, per-algorithm save/load behind `BaseAlgorithm`). Decided to **defer to the next cycle** — designed, not built — because of its scope (AppState, save/load rework, BERTopic save/load feasibility check).

## 3. Build

### 3.1 WP1 — Topic refinement
- `_build_result()` extracted from `train()` into a shared helper used by training and refinement (SKU-04-01).
- Native merge/delete via `model.merge_topics(texts, […])` / `model.delete_topics([…])`; label stored on `TopicResult.topic_labels` (no model mutation).
- Re-derive pipeline: rebuild result → recompute metrics → regenerate the 5 PNGs + 5 HTMLs → update state, in a background thread (SKU-04-03).
- Topics table: leading checkbox column, whole-row toggle, row highlighted via mirrored native selection; icon+text toolbar (merge/delete/label) after the basic stats, before the topics table; selection-gated enablement (delete 1+, merge 2+, label 1); merge/delete confirmation dialogs (SKU-04-02).

### 3.2 WP2 — Retire pywebview
- Removed `request_visualization`/`_generate_visualization`/`_launch_bertopic_webview`, the `pywebview` dependency, and `multiprocessing.freeze_support()`. D-009 marked deprecated.

### 3.3 WP3 — UI polish
- Plain-language "What do these mean?" explanations for the metrics gauges.
- Export/Settings/Loading/Wizard dialogs centred on the main window (shared `center_on_parent` helper; withdraw → position → deiconify avoids the position flash).
- MVP option limiting: sentence-transformer model → `all-MiniLM-L6-v2` only; language → English only.

### 3.4 WP4 — Document exploration
- `original_texts` stored in the result (and carried through refinement) so search/display use the reader's text, not the preprocessed training text (SKU-04-04).
- Document Assignments table refactored to Doc Index · Document · Topic 1 · Prob 1; full-text search via a Search button (not per-keystroke); the Document cell shows the query-match context when searching (SKU-04-05).
- "Detail" button opens a centred Top-Level window with Doc Index, all topic→probability pairs, and the full document in a scrollable read-only Text.
- Topic filter: checking topics in the topics table filters the Document Assignments to docs whose Topic 1 is one of the selected topics, combined AND with search (SKU-04-06).

## 4. Use

- Headless verification of every WP: `py_compile` on all changed modules, import checks of the model/controller/view layers, and ttkbootstrap glyphmap checks for the toolbar icons.
- User testing in the real app surfaced: the dialog position flash (fixed with the withdraw/deiconify pattern), icon-only buttons being unclear (changed to icon + text), and the drifted topic-filter requirement (re-wired into WP4).

## 5. Evaluate

### 5.1 What worked well
- Native BERTopic ops meant merge/delete needed no reimplementation — just a shared result-builder so training and refinement stay consistent.
- Refinement reuses the existing metric/visualisation services (re-derive pipeline), so no new derivation logic.
- The checkbox-glyph + mirrored-native-selection pattern gives a clear multi-select UX without a custom widget.
- Full-text search with a Search button avoids the per-keystroke cost and the "search only matches the 50-char snippet" trap.
- Deferring the persistence design (fully specified) kept the cycle focused and gave the next cycle a ready-made spec.

### 5.2 Remaining limitations / issues found
- The ☐/☑ checkbox glyphs may render inconsistently across platforms (could switch to images or ✓/empty).
- Document search is substring-only — no phrase/fuzzy matching yet.
- The Document Assignments table is capped at 200 shown rows even under a filter (a count label shows the true total).
- `AppState` was deliberately left unchanged (no `current_model_id`); multi-model remains a future change.

## 6. Learn

Consolidated insights (the cycle's knowledge output, detailed in `v0.4.0.md` SKUs):

- **Verify the library before assuming it lacks a feature** — BERTopic has native `delete_topics`; the ttkbootstrap `git-merge` icon does not exist. Reading the actual source/glyphmap before designing prevents both false negatives and runtime crashes (SKU-04-01, SKU-04-05).
- **A single result-builder keeps two code paths identical** when a mutation can remap internal ids (`topic_mapper_`) (SKU-04-01).
- **A model mutation invalidates every artifact derived from it** — treat refinement as "train-and-publish minus the training" (SKU-04-03).
- **Treeview has no checkboxes — a glyph column plus mirrored native selection is the pattern** (SKU-04-02).
- **Keep the user-facing texts separate from the training texts** — or search/display silently degrade (SKU-04-04).
- **A widget's built-in search can be a trap** — it matches what is rendered, not what the user means to search (SKU-04-05).
- **Two filter axes (by-topic, by-content) compose with AND** (SKU-04-06).

## 7. Key Decisions Reinforced

- **D-009 (deprecated):** the pywebview separate-process route is retired; the localhost route (D-023) replaced it and is confirmed working.
- **D-021:** storing evaluation output on `TopicResult` (per-model) made the refinement re-derive pipeline natural.
- **D-001 / algorithm-agnostic design:** refinement operations sit on the algorithm layer (`BERTopicAlgorithm.merge_topics`/`delete_topics`), keeping views algorithm-agnostic.

*Detailed rationale for each is recorded in `dev_docs/current/03_control/decisions.md`.*

## 8. Outputs of Cycle 4

### Notes / control artefacts
- `dev_docs/current/05_knowledge/skus/v0.4.0.md` — SKU-04-01…06 (cycle-coded; WP1 + WP4; WP2/WP3 trivial).
- `dev_docs/current/03_control/decisions.md` — D-009 status → deprecated.
- `dev_docs/current/04_working/cycle_plan.md` — v0.4.0 section (completed and ready to close).
- `dev_docs/current/04_working/tasks.md` — Cycle 4 implementation tasks by work package; close tasks.
- `dev_docs/current/05_knowledge/reflection.md` — Cycle 4 consolidated quick capture.

### Code artefacts
- `app/models/algorithms/bertopic.py` — `_build_result`; `merge_topics`/`delete_topics`.
- `app/models/topic_result.py` — `topic_labels` field.
- `app/controllers/app_controller.py` — merge/delete/label + the refinement re-derive pipeline.
- `app/views/panels/summary_panel.py` — checkbox topics table, refinement toolbar, document search + topic filter, Detail button.
- `app/views/panels/document_detail.py` — `DocumentDetailWindow` (new).
- `app/views/window_utils.py` — `center_on_parent` (new).
- Polish/cleanup across `app/controllers/analysis_controller.py`, `app/views/main_window.py`, `app/views/panels/{metric_panel,loading_panel,hyperparams/bertopic_section}.py`, `main.py`, `requirements.txt`.

### Design knowledge
- The consolidated learnings in §6, plus the SKU-level insights in `dev_docs/current/05_knowledge/skus/v0.4.0.md`.
- A fully-specified **model persistence + project folder** design (deferred; captured in `ideas.md`).

## 9. Cycle Outcome

Cycle 4 delivered the v0.4.0 feature set: topic refinement (merge/delete/label with a checkbox selection UI and confirmation dialogs), document exploration (full-text search, detail view, topic filter), plus pywebview retirement, metrics explanations, centred dialogs, and MVP option limiting. **Status: complete; pending release to `main`.**

## 10. Likely Next Cycle Direction

**Cycle 5** would release v0.4.0 to `main` (merge → verify → delete → fresh branch, per D-017) and then take on the designed-but-deferred **model persistence + project folder** — a single-file zip bundle with `project.json` + `model/{model_id}/` + `viz/{model_id}/`, timestamp model-ids plus an editable display name, and per-algorithm save/load behind `BaseAlgorithm` — starting with a BERTopic `save()`/`load()` feasibility check — and then the post-graduation backlog (LDA/NMF, multi-model, document search/filter hardening, batch processing).
