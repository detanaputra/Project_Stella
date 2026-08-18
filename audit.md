# Codebase Audit — Project Stella (Topic Modelling GUI)

**Audited:** 2026-08-18 · **Scope:** full `app/` package, `main.py`, docs, notebook
**Method:** line-by-line read of all 45 Python source files + grep for wiring of public methods; no code modified.
**Files under `__pycache__` skipped; `notebooks/` reviewed for consistency only.**

All findings reference `file:line` in the current tree. Severity = likelihood × impact for the target audience (non-technical social scientists, sensitive local data, reproducibility matters).

---

## Summary

The MVC skeleton is coherent and the code compiles cleanly, but the BERTopic path — the only shipping algorithm — has **parameter plumbing that is partially broken, partially dead, and partially lying** (settings collected in the UI are never passed to the model; two entry points train with *different* effective parameters). There is no automated test suite, and several defects will only surface with real data (small corpora, all-numeric CSVs, non-UTF-8 files).

**Top 5 things to fix first:**
1. Hyperparameter form destroys/rebuilds itself on every keystroke — parameter entry is effectively broken (see H-1).
2. Wizard "Default Settings" silently changes model behavior vs. the main-window path (H-2).
3. Five UI hyperparameters are collected but never applied by `train()` (H-3).
4. Parameter UI is invisible until the *first* analysis completes (H-4).
5. Any exception in one observer callback freezes all future UI updates (H-5).

---

## HIGH severity

### H1 — Parameter form rebuilds itself on every keystroke (data entry broken)
`app/views/panels/algorithm_settings_panel.py:77-98` + `app/views/panels/hyperparams/base_section.py:17-19`

> **Status: FIXED** (commit on `worktree-code-audit`). `_render()` now rebuilds the form only when a structural render key changes (`selected_algorithm`, `selected_file_path`, `current_result` presence); parameter-value writes update state and the retrain button without destroying the widgets.

Every hyperparameter widget binds a `trace_add("write", …)` that calls `AppController.on_param_changed` → `appState.notify()` → `AlgorithmSettingsPanel._on_state_changed` → `_render()` **destroys and recreates all three sections**. So typing a multi-digit value (e.g. "15" into N Neighbors) rebuilds the form after the first digit: the widget is destroyed mid-edit, focus is lost, and the remaining digits go nowhere.

**Impact:** Users cannot reliably enter or adjust parameters — the primary reason the tool exists. Also makes every keystroke expensive (full rebuild).
**Recommendation:** `_render()` should only rebuild on structural state changes (new file, new algorithm, result arrived), not on every parameter write. Guard with a "building" flag or compare a version counter; do not destroy/recreate the section while its own trace is firing.

### H2 — Wizard "Default Settings" silently applies different parameters than the algorithm's defaults
`app/views/wizard/wizard_main.py:101-105, 119-131`

> **Status: FIXED** (commit on `worktree-code-audit`). `_handle_train` now applies `get_current_params()` only when `settings_mode == "custom"`; otherwise it calls `app_controller.on_algorithm_changed(...)`, resetting to the algorithm defaults.

```python
if self.current_step != 2 or self.panel_algo.get_current_values()["settings_mode"] == "custom":
    custom_params = self.panel_hyper.get_current_params()
    self.appState.algorithm_params.update(custom_params)
```
Train only happens from step 3, so `current_step != 2` is **always True at train time** — the "skip" branch never works. Choosing "Default Settings" still overwrites `algorithm_params` with the *widget* defaults from `get_params()`, which differ from `BERTopicAlgorithm.get_default_params()` (most importantly `bertopic_calculate_probabilities`: section default **False** vs algorithm default **True**). Meanwhile the main-window retrain path starts with `algorithm_params = {}` (never initialized at startup — see H6) and trains with the algorithm's own defaults.

**Result:** the same "default" model trains with `calculate_probabilities=True` from one entry point and `False` from the other → different `doc_topics` (probabilities vs. hard `{t:1.0}` assignments). For a tool whose whole selling point is reproducibility, this is a silent inconsistency.
**Recommendation:** delete the dead condition; when `settings_mode == "default"`, call `on_algorithm_changed(name)` (or set `algorithm_params = algo.get_default_params()`); only `update()` when `"custom"`.

### H3 — Documented BERTopic hyperparameters are collected but never used
`app/views/panels/hyperparams/bertopic_section.py:124-134` vs `app/models/algorithms/bertopic.py:56-88` and `BERTopicHyperparams.md`

> **Status: FIXED** (commit on `worktree-code-audit`). `train()` now consumes all documented params: `bertopic_ngram_range` → `CountVectorizer`, `bertopic_top_n_words`/`bertopic_nr_topics`/`bertopic_low_memory` → `BERTopic(...)`, `bertopic_language` → language-aware stop-words. `nr_topics` is normalized ("auto"/"None"/int-string). Topic extraction iterates actual topic ids and the probs mapping falls back to hard assignments if column counts don't align after reduction. `get_default_params()` mirrors the UI section defaults.

The UI collects and stores (and the wizard serializes) `bertopic_language`, `bertopic_top_n_words`, `bertopic_ngram_range`, `bertopic_nr_topics`, `bertopic_low_memory` — but `train()` never reads any of them:
- `CountVectorizer(stop_words="english")` has **no `ngram_range`** (bertopic.py:73).
- `top_n_words`, `nr_topics`, `low_memory`, `language` are never passed to `BERTopic(...)`.
- `BERTopicHyperparams.md` step 3 explicitly instructs "Pass the hyperparameter setting value to each object in bertopic.py, specifically in train()" — not done.

Only `bertopic_min_topic_size`, `bertopic_embedding_model`, `bertopic_calculate_probabilities`, and the `umap_*` / `hdbscan_*` keys are actually consumed.

**Impact:** users who change "N-gram range", "NR Topics", "Top N Words", or "Language" get identical results — a confusing, reproducibility-damaging silent failure.
**Recommendation:** either wire them (vectorizer `ngram_range`, `nr_topics`, `top_n_words` in `model.get_topic_info(…)/reduce_topics`, BERTopic `low_memory`, language-aware stop-words) or remove them from the UI. Also normalize `bertopic_nr_topics` ("None" string, ints) to the type BERTopic expects.

### H4 — Parameter UI is invisible until the first analysis completes
`app/views/panels/algorithm_settings_panel.py:92-98`

> **Status: FIXED** (commit on `worktree-code-audit`). The `if self.appState.current_result:` gate is removed — the BERTopic/UMAP/HDBSCAN sections now render on a fresh start, before any analysis.

```python
if self.appState.selected_algorithm == "BERTopic":
    if self.appState.current_result:   # <- gated on a result
        BERTopicSection(...).pack(...)
        UMAPSection(...).pack(...)
        HDBSCANSection(...).pack(...)
```
On a fresh start (`current_result is None`) the right-hand settings pane is empty except the disabled Retrain button. The panel that *would* render the sections pre-training — `app/views/panels/settings_panel.py` — is **never instantiated** (dead code, see L1). The wizard's custom panel does show them, but only via the wizard.

**Impact:** first run always trains with defaults; user cannot inspect or tune parameters up front. Contradicts the "parameter forms auto-generate" design and the wizard flow.
**Recommendation:** drop the `if self.appState.current_result:` gate (render sections whenever `selected_algorithm == "BERTopic"`).

### H5 — One bad observer callback permanently freezes the UI
`app/views/main_window.py:84-88` + `app/models/app_state.py:61-83`

> **Status: FIXED** (commit on `worktree-code-audit`). `process_events()` wraps each callback in `try/except` (traceback printed, other observers still notified) and `_poll_state_events` re-schedules the 100 ms timer in a `finally`.

```python
def _poll_state_events(self):
    self.appState.process_events()        # ← exception here propagates
    self.after(100, self._poll_state_events)
```
`process_events()` invokes every observer callback with no try/except. If any callback raises (e.g. `TclError` from a widget destroyed mid-render, a layout error, a formatting bug on a new result), `self.after(...)` never re-registers — **event polling stops permanently** and the UI silently stops updating.

**Impact:** any panel render bug bricks the whole app's reactivity.
**Recommendation:** wrap `process_events` (or per-callback) in `try/except`, and/or always re-schedule `after` in a `finally`.

### H6 — `algorithm_params` is never initialized to defaults
`app/models/algorithms/__init__.py` / `app/controllers/app_controller.py:32-41` / `main.py`

> **Status: FIXED** (commit on `worktree-code-audit`). `AppController.__init__` seeds `algorithm_params` from the selected algorithm's `get_default_params()` when the dict is empty, so the main-window retrain path and the wizard share one set of defaults.

`AppState.algorithm_params` starts `{}`. `on_algorithm_changed` (the only path that sets defaults) is only reachable from the dead `SettingsPanel` and wizard's combobox. So the main-window path trains with whatever is in state — `{}` on a fresh launch — relying on `train()`'s hard-coded fallbacks. There is no single source of truth for "current effective parameters".

**Impact:** hard to predict/display which params a run actually used (`model_info['params']` will show `{}` or the partial dict); makes H2's inconsistency worse and breaks the "always show model configuration" UX promise.
**Recommendation:** initialize `algorithm_params = get_default_params()` at startup and whenever the algorithm changes.

---

## MEDIUM severity

### M1 — Thread-unsafe UI calls & unsynchronized shared state
- `app/views/panels/visualizations/bertopic_viz_panel.py:116-161`: `_process_visualization` runs in a worker thread and calls `self.after(0, …)` (lines 122, 128, 160) — Tkinter is not thread-safe; `after` from a non-main thread can raise or misbehave.
- `app/controllers/analysis_controller.py:35-45, 57-59, 82-86`: mutates `AppState` fields from the worker thread while the main thread reads them in `process_events`. The queue *is* safe, but field reads/writes have no lock or barrier (works under CPython's GIL today, fragile tomorrow; also visible to `multiprocessing` code in the viz panel).
- `analysis_controller.py:20-28`: no re-entrancy guard — two rapid "Run" clicks spawn two training threads.

> **Status: FIXED** (commit on `worktree-code-audit`). `run_analysis` now has a re-entrancy guard: it returns early if `analysis_in_progress` and sets the flag **synchronously** before spawning the worker thread, so a rapid double-click is caught. Thread→UI marshaling is centralized in `AppState.call_on_main(callback)` (a second queue drained by `process_events` on the main thread); `bertopic_viz_panel` and the new `ExportPanel` route all `messagebox` calls through it instead of `self.after` from worker threads. Shared `AppState` field writes from the worker remain GIL-protected — acceptable for the single-worker design.

### M2 — Matplotlib figure leak in results renderer
`app/views/panels/results_panel.py:93-121` — `plt.subplots()` on every render, widget destroyed but `plt.close(fig)` never called → figures accumulate in memory. Dormant today (ResultsPanel is dead code, L1) but will bite the moment the panel is wired.

> **Status: FIXED** (commit on `worktree-code-audit`). `ResultsPanel` was tracked/closed its matplotlib figure — but the panel was **dead code and has since been deleted** in the L1 cleanup, which supersedes this fix. No figure leak remains because the panel no longer exists; if a results panel is reintroduced, the `_current_fig` + `plt.close` pattern from the M2 fix should be carried over.

### M3 — SummaryPanel rebuilds a full per-document table on every notify
`app/views/panels/summary_panel.py:36-72, 128-146` — `_render()` destroys and re-inserts a Treeview row **per document** on every state change (which fires on every parameter keystroke — see H1). With thousands of documents the UI stalls. `results_panel.py:84` caps at 10 topics; `summary_panel` does not cap `doc_topics`.

> **Status: FIXED** (commit on `worktree-code-audit`). `_render()` now early-returns when `result is self._last_result` — the panel depends only on the `TopicResult`, so parameter writes no longer re-insert the per-document table at all. The document-assignment table is additionally capped at 200 rows with a "Showing first 200 of N documents." label.

### M4 — `to_json` / interactive viz are unreachable; the only "browser export" writes fake HTML
- `Exporter.to_json` (exporter.py:18) is never called anywhere — JSON export is a stated MVP success criterion (CLAUDE.md) but has no UI entry point.
- `TopicVisualizer.visualize` (visualizer.py:13) is never called; the real BERTopic viz goes through the webview panel. If it *were* wired, it writes **"Interactive plot placeholder"** HTML pretending to be a real plot — misleading.

> **Status: FIXED** (commit on `worktree-code-audit`). A real **Export tab** (`app/views/panels/export_panel.py`) replaces the mock-up label: Export CSV / JSON / Methodology Report plus "Open Visualizations in Browser". `AppController` gained `self.exporter`/`self.visualizer` and `export_csv`/`export_json`/`export_methodology_report`/`export_visualizations`. `TopicVisualizer.visualize` now calls the real BERTopic figure methods (`visualize_topics`, `visualize_heatmap`, `visualize_barchart`, `visualize_hierarchy`) and writes offline HTML to `~/.bertopic-gui/viz`; the "placeholder" branch is gone. The viz export runs off the main thread so the UI stays responsive while the ~4 plots build.

### M5 — Offline promise broken by CDN plotly
`bertopic_viz_panel.py:142` — `include_plotlyjs='cdn'` requires internet; the app markets offline/privacy. Bundle plotly.js locally (`include_plotlyjs=True` or `'directory'`).

> **Status: FIXED** (commit on `worktree-code-audit`). Both the webview panel and `TopicVisualizer` now write with `include_plotlyjs=True`, embedding plotly.js so the HTML works fully offline.

### M6 — DataLoader CSV edge cases
`app/models/services/data_loader.py:56,69` — `df.select_dtypes(include=['object']).columns[0]`:
- `IndexError` if the CSV has no string column (e.g. numeric-only data) — crash path in `load_preview`, error-only in `validate`.
- picks the **first** object column blindly (an ID/date column is used as the document).
- `astype(str)` turns NaN cells into the string `"nan"` — bogus documents.
- UTF-8 only for .txt (SPSS/Excel exports are often Latin-1) → `UnicodeDecodeError`.
- `validate_file` calls `load_texts` which reads the **entire** file, then `load_preview` reads again.

> **Status: FIXED** (commit on `worktree-code-audit`). `DataLoader` now raises a clear `ValueError` ("No text column found…") instead of an `IndexError` when the CSV has no object column; NaN cells and empty/whitespace rows are dropped before training (no more literal `"nan"` documents); `.txt` and CSV files try `utf-8` then fall back to `latin-1`. Shared `_read_csv`/`_read_text_file`/`_pick_text_column` helpers are used by both `load_texts` and `load_preview`.

### M7 — Debug prints left in production paths
- `bertopic.py:140-141` printed the full `topics_list` and `doc_topics` on **every training run** — **removed** in the H3 fix.
- `summary_panel.py:33` still prints on every state change.
- `analysis_controller.py:32,45,72,79,87` etc.

> **Status: FIXED** (commit on `worktree-code-audit`). All routine progress prints removed from `bertopic.py`, `summary_panel.py`, and `analysis_controller.py`. The only remaining `print` is the `traceback.print_exc()` in the failure path of `analysis_controller._execute_pipeline`, kept deliberately: `analysis_error` stores only `str(e)`, so the stderr traceback is the sole record of a failed run for support. (The `EditMenu`/`ViewMenu`/`WindowMenu` stub prints are intentional placeholders for unimplemented menu actions — tracked under L1.)

### M8 — HDBSCAN config inconsistent with the notebook & BERTopic defaults
`bertopic.py:66-70` sets only `min_samples` (no `min_cluster_size`); the training notebook (notebooks/test_training.ipynb cell 2) sets `min_cluster_size=min_topic_size`. Two "same" training functions drift apart — cluster sizes / topics will differ. (The notebook also has its own bugs — see L6.)

> **Status: FIXED** (commit on `worktree-code-audit`). The HDBSCAN clusterer now sets `min_cluster_size` (defaulting to the same value as `bertopic_min_topic_size`, i.e. 10), exposed in the UI as a new "Min Cluster Size" spinbox in the HDBSCAN section and wired through `get_default_params()` / `get_params()` / `train()`.

---

## LOW / hygiene

### L1 — Dead & duplicated views
`app/views/main_window.py:10-13` imports `InputPanel`, `SettingsPanel`, `ProcessingPanel`, `ResultsPanel` — **none are instantiated** in `_build_ui`. `SettingsPanel` duplicates `AlgorithmSettingsPanel`, `EditMenu`/`ViewMenu`/`WindowMenu` are stubs, and the "Export"/"App Settings" tabs are placeholders. Two parallel settings UIs already drift (one shows sections pre-result, the other hides them).

> **Status: FIXED** (commit on `worktree-code-audit`). Dead imports removed and the unreachable panels deleted (`input_panel.py`, `settings_panel.py`, `processing_panel.py`, `results_panel.py`) — their functions are covered by ToolboxPanel, SummaryPanel, LoadingPanel, and the Export tab (M4). The print-only stub `ViewMenu`/`WindowMenu` were deleted; the menubar is now File/Edit only. The Edit menu forwards real `<<Cut>>/<<Copy>>/<<Paste>>/<<Undo>>/<<Redo>>` events to the focused widget instead of printing. The " App Settings " tab is now a real ttkbootstrap **theme switcher** instead of a mockup label. (Deleting `results_panel.py` supersedes the M2 figure-leak fix — see the M2 note.)

### L2 — Committed build artifacts & `.DS_Store`
`git ls-files` includes dozens of `*.pyc` files and `.DS_Store`; `.gitignore` was added later and cannot untrack them — every source edit produces a visible modified-`.pyc` in `git status` (visible right now). Remove with `git rm --cached`.

> **Status: FIXED** (commits `d368334` and `f0573ff` on `main`). Compiled artifacts and `.DS_Store` removed from tracking; `git ls-files` reports zero `*.pyc`/`.DS_Store` and the working tree is clean.

### L3 — No parameter validation
- `umap_n_neighbors` default 15 vs small corpora → UMAP raises (`n_neighbors` > `n_samples`); `validate_file` only warns. Clamp or error early.
- `ngram start > end` (spinboxes allow 3→1) — currently harmless because H2 ignores it, but a crash once wired.
- `nr_topics` Combobox mixes `"auto"`, `"None"`, and ints (bertopic_section.py:93) — type instability.

> **Status: FIXED** (commit on `worktree-code-audit`). `train()` clamps `umap_n_neighbors` to `max(2, len(texts)-1)` so the 15-neighbor default no longer crashes on a small corpus. The BERTopic n-gram spinboxes clamp `start ≤ end` (swapping both widgets so the UI, state, and the wizard's `get_params()` agree). The `nr_topics` type instability is covered by the existing normalization in `train()` ("auto"/"None"/int-string → int or `None`).

### L4 — `AppState.process_events` observer bookkeeping
`app/models/app_state.py:71-80` — replaces `self._observers` with `live_observers` **after** iterating; an observer added during notify is kept; a dead-ref cleanup happens. Fine, but `notify()` no-ops if observers subscribe *after* the event is queued (a panel subscribing in its `__init__` then immediately expecting a notification — most panels call `_render()` themselves, so OK). Also `LoadingPanel` subscribes once per instance; multiple `show_loading_panel()` calls can stack modal dialogs.

> **Status: FIXED** (commit on `worktree-code-audit`). The observer bookkeeping was already correct; the actionable defect — stacking modal `LoadingPanel`s — is fixed: `MainWindow.show_loading_panel` now reuses the open instance (lift/focus) instead of creating a new Toplevel on every call. Verified with a live-Tk test.

### L5 — Processor swallows `custom_stopwords_path=None`
`processor.py:22-26` — `open(None)` raises `TypeError`, caught by the bare `except: pass`; it "works" but hides the fact that the option is never used from the UI (the controller always passes `None`).

> **Status: FIXED** (commit on `worktree-code-audit`). `None`/empty path now means "no custom stop-words" and is skipped cleanly; a provided-but-missing path raises a clear `ValueError` instead of being silently swallowed; when a path is supplied, custom stop-words genuinely apply during preprocessing.

### L6 — Notebook bugs (notebooks/test_training.ipynb)
- cell 3: `train(texts=df["Abstract"], params=params)` — `params` lands inside `**params` as the key `'params'`, so every configured default is silently ignored (trains with hard-coded defaults).
- cell 2: `'algorithm': "self.algorithm_name"` — a literal string, not the attribute.

> **Status: FIXED** (commit on `worktree-code-audit`). Cell 3 now calls `train(texts=df["Abstract"], **params)` so the configured defaults actually reach the model; the `model_info` `algorithm` is now the literal `'BERTopic'`. While rewriting the cell I also fixed a latent off-by-one in the topic-extraction loop (`range(len(keys)-1)` → iterate `sorted(keys)`, skipping `-1`) and removed a leftover commented-out HDBSCAN block.

### L7 — Project save/load incompleteness
`project_service.py:26-38` — `load_project` sets `algorithm_params` from file but never validates `selected_algorithm` against `AVAILABLE_ALGORITHMS`; a stale/altered `.stella` can put the app in an error state at train time.

> **Status: FIXED** (commit on `worktree-code-audit`). `load_project` now validates the algorithm name (unknown → falls back to BERTopic), merges any loaded params over `get_default_params()` so a partial/old `.stella` still trains with a complete set, and clears a recorded data path that no longer exists so the UI prompts for a fresh file instead of crashing confusingly at train time.

### L8 — Progress reporting is effectively binary
`analysis_controller.py` sets `analysis_progress` only to `"0%"`/`"100%"`; `update_progress` updates status text only. The determinate bar in `processing_panel` jumps 0→100. Acceptable for MVP, but it's a visible gap to the user's promised "X%".

> **Status: FIXED** (commit on `worktree-code-audit`). `analysis_progress` now follows pipeline milestones: 0% → 10% (load) → 25% (init) → 40% (preprocessing) → 70% (training) → 100% (done), mapped from the processor's stage callbacks. Still milestone-based (not per-document), but the determinate bar no longer jumps straight 0→100.

---

## Recommendations (priority order)

**Blocking (fix before handing to users):**
1. H1 — stop rebuilding the form on every param trace.
2. H2 — fix the wizard condition; default mode must apply `get_default_params()`.
3. H3 — wire the four documented BERTopic params into `train()` or remove from UI.
4. H4 — show the hyperparameter UI before the first run.

**High value (next):**
5. H5 — make `process_events`/`_poll_state_events` exception-safe.
6. H6 — initialize `algorithm_params` to defaults at startup; make it the single source of truth for "effective params".
7. M6 — robust CSV column detection + encoding fallbacks (this is the app's main input surface).
8. M1 — re-entrancy guard on `run_analysis`; move thread→UI communication through a queue; stop calling Tkinter from threads.
9. M5 — offline plotly.

**Housekeeping:**
10. L2 — `git rm --cached` the committed artifacts.
11. M7 / L1 — remove debug prints; delete or wire the dead panels; decide one settings UI.
12. M3 — cap rows in the document-assignment table (or paginate).
13. L6 — fix the notebook `params=` bug and the literal `algorithm` string.
14. Add a minimal smoke test (train on sample CSV → export → render) — currently none.

---

## What looks good
- Clean MVC separation; `AppState` + observer queue is a sound pattern for a Tkinter app with worker threads.
- `TopicResult` / `BaseAlgorithm` contracts are stable and would make LDA/NMF plug in cleanly.
- `UMAP(random_state=8)` fixed → deterministic reruns (good for reproducibility once H1–H6 are resolved).
- `validate_file` warns on small/moderate samples — a genuinely thoughtful touch for the audience.
- Dependencies are pinned and versioned.

*Audit produced read-only; no source files were modified.*
