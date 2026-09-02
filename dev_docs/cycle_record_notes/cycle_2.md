# Cycle 2

#cycle2 #formal_record #build #shapr

## Cycle Title
Ship the v0.2.0 feature set: GitHub presentation, MouseWheel scrolling, and topic quality metrics.

## 1. Context

The project needed to extend the released v0.1.0 application with the v0.2.0 feature set: publish the project on GitHub (README + Apache 2.0 license), improve parameter-panel scrolling ergonomics, and give users topic quality metrics. This cycle covered the v0.2.0 build (2026-08-27), reconstructed as 4 SKUs (SKU-02-01…04) in `dev_docs/current/05_knowledge/skus/v0.2.0.md`.

Cycle framing:
- **Main goal:** README + Apache 2.0 license; MouseWheel scrolling in the parameter panels; topic quality metrics (NPMI, C_V, UMass, Topic Diversity) in a new "Metrics" tab.
- **Main outcomes:** GitHub-ready repo; wheel-scrollable parameter panels; Gensim-based topic quality with a dynamic Metrics tab.
- **Success signal:** a user can scroll parameters without grabbing the scrollbar and see topic quality in the Metrics tab.

## 2. Explore

Design questions investigated and the answers the cycle converged on:

- **2.1 Which metric library?** OCTIS was initially named, but a footprint check showed it is infeasible (torch ~106 MB wheel, 1–2 GB installed, `scikit-learn==1.1.0` pin incompatible with Python 3.11+). Gensim's `CoherenceModel` covers all three coherence measures; Topic Diversity is hand-rolled.
- **2.2 Where do the metrics live?** On `TopicResult.quality_metrics` (not a parallel `AppState` field) so each model's metrics travel with its result — multi-model-ready.
- **2.3 Where are the metrics shown?** A new "Metrics" tab (added to the main Notebook after Analysis once a result exists), not the summary tab.
- **2.4 How to handle the single-event observer as the app grows?** Keep `STATE_CHANGED`; adopt a cheap-subscriber discipline (expensive work in controllers' background threads; subscribers guard on the field they care about).

## 3. Build

### 3.1 Planning & contract (WP1)
ROADMAP v0.2.0 decided; decisions D-020/021/022 recorded; `TopicResult.quality_metrics` added to the contract (`api.md`) and the dataclass.

### 3.2 GitHub presentation (WP2)
README (description, goal, benefits) + Apache 2.0 LICENSE.

### 3.3 MouseWheel scrolling (WP3)
MouseWheel bound to the scrollable canvas and recursively to the parameter widgets in `algorithm_settings_panel.py` and the wizard's `panel_hyperparams.py`; cross-platform (Windows/macOS `<MouseWheel>` with delta normalization, Linux `<Button-4>`/`<Button-5>`).

### 3.4 Topic quality backend (WP4)
`topic_quality` service: NPMI/C_V/UMass via Gensim `CoherenceModel` (with `processes=1` to avoid multiprocessing issues from a GUI background thread) + hand-rolled Topic Diversity. Pipeline computes metrics in the background and sets `result.quality_metrics`.

### 3.5 Metrics tab UI (WP5)
`MetricPanel` (ttk.Frame) rendering 4 matplotlib gauge/donut charts; `MainWindow` adds the "Metrics" tab after Analysis once a result exists, removes it when cleared.

## 4. Use

- App run headless: panels build, wheel handlers fire, Metrics tab appears/disappears with the result.
- Topic quality service verified on synthetic data (all 4 metrics computed).
- README + license present in the repo.

## 5. Evaluate

### 5.1 What worked well
- Gensim over OCTIS: all three coherence measures at a fraction of the footprint.
- `processes=1` fix: reliable coherence from a GUI background thread.
- Metrics on `TopicResult`: multi-model-ready without parallel state.
- Dynamic Metrics tab: clean lifecycle tied to state.

### 5.2 Remaining limitations / issues found
- Gensim's `c_v`/`c_npmi` default to multiprocessing, which fails from a GUI background thread on macOS spawn — forced `processes=1`.
- The MetricPanel render guard keyed on `None` skipped the first render — fixed with a sentinel distinct from `None` (D-014 pattern).
- C_V is the slowest coherence measure; it runs in the background pipeline, not the UI.

## 6. Learn

Consolidated insights (the cycle's knowledge output):

- **A footprint check before adopting a research library can save gigabytes** of bundle size and dependency conflicts (OCTIS vs Gensim).
- **Store evaluation output on the result object**, not app state — the multi-model-ready shape.
- **Gensim's sliding-window coherence uses multiprocessing by default** — force `processes=1` in a GUI app.
- **A render guard keyed on `None` collides with "no result yet"** — use a distinct sentinel.
- **The single-event observer stays cheap when subscribers guard** instead of recalculating.

## 7. Key Decisions Reinforced

- Gensim `CoherenceModel` for coherence + hand-rolled Topic Diversity (D-020).
- Metrics stored on `TopicResult.quality_metrics` (D-021).
- Single-event observer with cheap-subscriber discipline (D-022).

*Detailed rationale for each is recorded in `dev_docs/current/03_control/decisions.md`.*

## 8. Outputs of Cycle 2

### Notes / control artefacts
- `dev_docs/current/05_knowledge/skus/v0.2.0.md` — SKU-02-01…04 (cycle-coded; from the design-changing commits).
- `ROADMAP.md` — v0.2.0 section (planned → completed).
- `dev_docs/current/03_control/decisions.md` — D-020…D-022.

### Code artefacts
- `app/models/services/topic_quality.py` — metric service.
- `app/views/panels/metric_panel.py` — gauge panel.
- `app/views/main_window.py` — Metrics tab wiring.
- `app/views/panels/algorithm_settings_panel.py`, `app/views/wizard/panel_hyperparams.py` — MouseWheel.
- `app/controllers/analysis_controller.py` — pipeline metric computation.
- `app/models/topic_result.py` — `quality_metrics` field.
- `README.md`, `LICENSE`, `requirements.txt` (gensim).

### Design knowledge
- The consolidated learnings in §6, plus the SKU-level insights in `dev_docs/current/05_knowledge/skus/v0.2.0.md`.

## 9. Cycle Outcome

Cycle 2 delivered the v0.2.0 feature set: a GitHub-ready repo (README + Apache 2.0 license), wheel-scrollable parameter panels, and topic quality metrics (NPMI, C_V, UMass, Topic Diversity) shown as 4 gauges in a dynamic "Metrics" tab. All five work packages were committed to `v0.2.0` and pushed. **Status: complete; pending release to `main`.**

## 10. Likely Next Cycle Direction

**Cycle 3** would release v0.2.0 to `main` (merge → verify → delete → fresh branch, per D-017) and then take on the post-graduation backlog: LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing.
