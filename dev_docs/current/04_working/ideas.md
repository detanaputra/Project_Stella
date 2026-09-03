# Ideas

#working #ideas

Raw capture of undeveloped ideas — no format pressure; a holding area. Ideas here are **not committed**; they are refined and promoted to `cycle_plan.md` (or `tasks.md`) once they mature.

## Cycle 3 candidates

- Metrics-tab explanations for beginners (the gauges show numbers with no plain-language meaning) — from `cycle_2_review.md` §3
- Topic refinement (merge/delete topics) — from `cycle_2_review.md` §3; note the risk: metrics must be recalculated after each refinement (§5)
- Post-graduation backlog: LDA/NMF algorithms, multi-model support, embedded matplotlib charts, document search/filter, batch processing

## Housekeeping / engineering

- Test suite — no committed `tests/` exists; `architecture.md` and `development.md` note it is planned (view testing deferred until the suite is added)
- PyInstaller packaging / distribution — planned in `CLAUDE.md` (Week 5 optional, GitHub Releases for researchers); no `.spec`/`dist/` build exists
- CI workflow — documented in `development.md` (GitHub Actions); no `.github/workflows/` exists
- `data_contracts.md` extraction — `02_contracts/README.md` open gap: currently folded into `api.md`; consider extracting if it grows

## Human tasks

- `cycle_0.md` retrospective — environment-setup cycle; to be written by the human (in `current_state.md` Deferred)

## For Brainstorming
- explore the idea of using pywebview package to display BERTopic visualisation that is currently using Plotly. if possible, every visualisation will have their own tab on the same level with newly created metric tab. This will render tolbox section useless. this way, parameter panel that is currently on the right side, can be moved to the left side replacing toolbox and opening new space for the many visualisation tab. demote the export tab and setting tab.
- since setting tab is demoted, it will need its own panel that can be called under File Menu.