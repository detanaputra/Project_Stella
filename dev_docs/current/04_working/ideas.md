# Ideas

#working #ideas

Raw capture of undeveloped ideas — no format pressure; a holding area. Ideas here are **not committed**; they are refined and promoted to `cycle_plan.md` (or `tasks.md`) once they mature.

## Cycle 3 candidates
- **Visualisation tabs + layout restructure** — bring the BERTopic visualisations into the main Notebook as tabs (same level as the Metrics tab). Each tab shows a static matplotlib chart plus an "Open interactive" button that opens the Plotly HTML in the default browser. Then restructure the layout: remove the toolbox (redundant once the tabs exist), move the parameter panel to the left column, and demote the Export/Settings tabs (Settings becomes a panel under the File Menu).
  - **Confirmed approach (`to_dict()`):** BERTopic's `visualize_*` return Plotly figures only, but `fig.to_dict()` exposes the rendered data — topic x/y coords, sizes, labels; heatmap z-matrix; bar data; dendrogram coordinates — as a plain dict (verified in `notebooks/test_training.ipynb`). Re-plot statically with matplotlib; no kaleido / Chrome / plotly-upgrade needed.
  - **Effort:** feasible for all five visualisations — the intertopic distance map is now easy too (scatter from the exposed x/y); heatmap → `imshow`, barchart → `bar`, hierarchy → dendrogram.
  - **Side benefit:** the interactive path opens in the default browser; the pywebview separate-process route (D-009) stays for now and is retired only after the new path is confirmed working.
  - **Decided scope:**
    - 5 viz tabs (topics, heatmap, barchart, hierarchy, term_rank), placed after Metrics; appear only when a result exists
    - Export and Settings become top-level panels under File Menu (File → Export / File → Settings); theme switcher stays in the Settings panel for now
    - Params panel: persistent left column (no collapse toggle for now)
    - Static charts: generated on-demand (lazy) when a tab is first opened
  - **Design (settled):**
    - New service `app/models/services/static_viz.py`: `plotly_fig_to_mpl(fig_dict)` dispatches on trace type (scatter / heatmap / bar); `static_chart(model, viz_name)` wrapper; `save_static_charts(model, output_dir)` batch → PNGs
    - Clean matplotlib defaults (not pixel-matched to Plotly); intertopic point sizes scaled for readability; heatmap uses `YlGn` colormap
    - Hierarchy: simpler representation for now (MVP) — not a faithful dendrogram
    - **Pre-generation:** the pipeline generates all 5 static PNGs + 5 offline HTML files after metrics (user waits during training anyway); tabs display the PNGs, "Open interactive" opens the pre-generated HTML — no lazy/on-click generation, so the HTML files are stable
    - **Served over localhost:** interactive HTML is opened via a tiny local HTTP server (http://localhost) instead of file:// — browsers handle http reliably (file:// intermittently opens a blank tab)
    - Verification: headless smoke test (train small corpus → convert all 5 → save PNGs)

## Deferred to Other Cycle (backlog)
- Topic refinement (merge/delete topics) — targeted for cycle 4; from `cycle_2_review.md` §3. Scope: select a topic → merge or delete → input user interpretation for the topic. Risk: metrics must be recalculated after each refinement (§5).
- Metrics-tab explanations for beginners (the gauges show numbers with no plain-language meaning) — from `cycle_2_review.md` §3
- Post-graduation backlog: LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing

## Housekeeping / engineering

- Test suite — no committed `tests/` exists; `architecture.md` and `development.md` note it is planned (view testing deferred until the suite is added)
- PyInstaller packaging / distribution — planned in `CLAUDE.md` (Week 5 optional, GitHub Releases for researchers); no `.spec`/`dist/` build exists
- CI workflow — documented in `development.md` (GitHub Actions); no `.github/workflows/` exists
- `data_contracts.md` extraction — `02_contracts/README.md` open gap: currently folded into `api.md`; consider extracting if it grows

## Human tasks

- `cycle_0.md` retrospective — environment-setup cycle; to be written by the human (in `current_state.md` Deferred)

## For Brainstorming
*(raw holding area — promotes to the Cycle candidates section once refined)*