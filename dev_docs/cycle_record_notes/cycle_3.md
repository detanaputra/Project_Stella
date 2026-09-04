# Cycle 3

#cycle3 #formal_record #build #shapr

## Cycle Title
Bring the BERTopic visualisations into the app as in-app tabs and restructure the main-window layout (v0.3.0).

## 1. Context

The released v0.2.0 app showed topic quality metrics in a "Metrics" tab, but the BERTopic visualisations still opened only in the browser. The user wanted them *inside* the app as tabs, and the main-window layout (toolbox left, notebook right, params buried in the Analysis tab) needed a cleaner structure. This cycle covered the v0.3.0 build (2026-09-04), reconstructed as 4 SKUs (SKU-03-01…04) in `dev_docs/current/05_knowledge/skus/v0.3.0.md`.

Cycle framing:
- **Main goal:** in-app visualisation tabs (static matplotlib + "Open interactive") and a layout restructure (params left, toolbox removed, Export/Settings → File Menu).
- **Main outcomes:** 5 viz tabs; pre-generated static PNGs + HTML in the pipeline; interactive HTML served over localhost; clean PanedWindow layout.
- **Success signal:** a user can open each of the 5 visualisations as a tab, see a static chart, and click "Open interactive" for the full Plotly figure in the browser — with the toolbox gone and parameters on the left.

## 2. Explore

Design questions investigated and the answers the cycle converged on:

- **2.1 How to display BERTopic visualisations statically in-app?** BERTopic's `visualize_*` return Plotly figures only. Kaleido needs a plotly upgrade plus an installed Chrome; embedding a browser widget is heavy. The user discovered that `fig.to_dict()` exposes the rendered data (coordinates, sizes, labels, matrices) as a plain dict — re-plot with matplotlib (already pinned), no new dependency.
- **2.2 Lazy or pre-generated?** The first design generated static charts lazily on tab open and HTML on click. The user found the tabs slow and hit reliability issues → pre-generate all 5 PNGs + 5 HTMLs in the pipeline after metrics (the user already waits during training).
- **2.3 file:// or localhost?** The "Open interactive" browser window intermittently opened blank even with a complete file — browsers are unreliable at `file://` → serve the viz directory over a tiny local HTTP server.
- **2.4 What layout?** With visualisations as tabs, the toolbox (which only launched them) became redundant → remove it, move params to a persistent left column, demote Export/Settings to File Menu dialogs.

## 3. Build

### 3.1 Static viz service (WP1)
`app/models/services/static_viz.py`: `plotly_fig_to_mpl(fig_dict)` dispatches on trace type (scatter / heatmap / bar / lines); `static_chart(model, viz_name)` wrapper; `save_static_charts(model, output_dir)` batch → PNGs. Per-viz styling: topics/hierarchy axes hidden, term-rank axis labels, hierarchy topic labels on the y-axis.

### 3.2 Visualisation tabs (WP1)
`StaticVizPanel` displays the pre-generated PNG + an "Open interactive" button; `MainWindow` adds 5 viz tabs (topics, heatmap, barchart, hierarchy, term_rank) after Metrics when a result exists, removed on clear.

### 3.3 Pre-generation + localhost (WP1)
The pipeline generates all 5 static PNGs + 5 offline HTML files after the quality metrics. Interactive HTML is served over a local HTTP server (127.0.0.1, ephemeral port) and opened as `http://localhost/<file>`.

### 3.4 Layout restructure (WP2)
Toolbox removed; parameter panel moved to a persistent left column; Export and App Settings demoted to File Menu dialogs (File → Export..., File → Settings...); the Analysis tab holds only the summary. Dead `toolbox_panel.py` / `bertopic_viz_panel.py` deleted.

## 4. Use

- App run headless: tabs appear/disappear with the result; dialogs open from the File menu.
- User tested in the real app: tabs open fast, the blank-tab issue is gone, the hierarchy renders with topic labels, and the main window is "more clean."

## 5. Evaluate

### 5.1 What worked well
- `to_dict()` → matplotlib: all 5 visualisations render in-app with no new dependency (no kaleido / Chrome / plotly upgrade).
- Pre-generation: tabs and "Open interactive" are instant; the HTML files are stable (never regenerated on click).
- Localhost serving: blank browser tabs gone.
- Clean layout: persistent params panel + notebook of analysis/viz tabs.

### 5.2 Remaining limitations / issues found
- Pre-generation adds ~2s to training on the sample corpus — fine now, but revisit for large corpora (lazy/on-demand).
- The hierarchy needed a y-axis-label fix (labels belong on the y-axis, not the x-axis).
- `ttk.Notebook.insert` with an integer index fails when the notebook has few tabs — dynamic tabs are appended with `"end"`.
- The pywebview separate-process route (D-009) is now unused; kept until the new path is confirmed, then retired.

## 6. Learn

Consolidated insights (the cycle's knowledge output):

- **A Plotly figure's rendered data is reusable** — `fig.to_dict()` exposes coordinates, sizes, labels, and matrices, so a research GUI can re-plot them with matplotlib and ship no browser engine.
- **Front-load expensive once-only work into the wait the user already endures** — pre-generating during training makes every interaction instant.
- **Serve local HTML over localhost, not `file://`** — `file://` causes intermittent blank tabs and stale caching across browsers.
- **Put frequently-used controls in a persistent panel; demote infrequent actions to the menu** — the tab bar should hold navigable content, not utility panels.

## 7. Key Decisions Reinforced

- D-023: in-app visualisation tabs — static matplotlib via `to_dict()`, pre-generated in the pipeline, interactive HTML over localhost.
- D-009 (revised in practice): the pywebview separate-process route is no longer used by any view; kept until the new path is confirmed working.

*Detailed rationale for each is recorded in `dev_docs/current/03_control/decisions.md`.*

## 8. Outputs of Cycle 3

### Notes / control artefacts
- `dev_docs/current/05_knowledge/skus/v0.3.0.md` — SKU-03-01…04 (cycle-coded; WP1 + WP2).
- `dev_docs/current/03_control/decisions.md` — D-023.
- `dev_docs/current/04_working/cycle_plan.md` — v0.3.0 section (completed and ready to close).

### Code artefacts
- `app/models/services/static_viz.py` — `to_dict()` → matplotlib converter + `save_static_charts`.
- `app/views/panels/static_viz_panel.py` — static chart tab + "Open interactive".
- `app/views/main_window.py` — 5 viz tabs; layout restructure (params left, toolbox removed).
- `app/views/menus/file_menu.py` — Export... / Settings... dialogs.
- `app/controllers/analysis_controller.py` — pre-generation step in the pipeline.
- `app/controllers/app_controller.py` — `get_static_chart_path` / `open_interactive_viz`.
- `app/models/services/visualizer.py` — localhost HTTP server; `term_rank` added to the batch.

### Design knowledge
- The consolidated learnings in §6, plus the SKU-level insights in `dev_docs/current/05_knowledge/skus/v0.3.0.md`.

## 9. Cycle Outcome

Cycle 3 delivered the v0.3.0 feature set: 5 in-app visualisation tabs (static matplotlib charts + "Open interactive"), pre-generated in the pipeline and served over localhost, plus a clean layout restructure (persistent params panel, toolbox removed, Export/Settings → File Menu). All work packages were committed to `v0.3.0` and pushed. **Status: complete; pending release to `main`.**

## 10. Likely Next Cycle Direction

**Cycle 4** would release v0.3.0 to `main` (merge → verify → delete → fresh branch, per D-017) and then take on the post-graduation backlog: topic refinement (select a topic → merge/delete → input user interpretation, with metric recalculation), pywebview retirement, and the remaining deferred items (LDA/NMF, multi-model, search/filter, batch).
