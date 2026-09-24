# Ideas

#working #ideas

Raw capture of undeveloped ideas — no format pressure; a holding area. Ideas here are **not committed**; they are refined and promoted to `cycle_plan.md` (or `tasks.md`) once they mature. Once they are promoted, they are then deleted from this file.

## Deferred to Other Cycle (backlog)

- Post-graduation backlog:
  - LDA/NMF algorithms (exercises the `BaseAlgorithm` abstraction — D-001)
  - Multi-model support ("Model 1", "Model 2", …) — metrics already stored per-`TopicResult` (D-021)
  - Embedded matplotlib charts
  - Batch processing

## Housekeeping / engineering

- Test suite — committed `tests/` exists (v0.5.0, WP1) covering the model + controller layer; view testing deferred
- PyInstaller packaging / distribution — planned in `CLAUDE.md` (Week 5 optional, GitHub Releases for researchers); no `.spec`/`dist/` build exists
- CI workflow — documented in `development.md` (GitHub Actions); no `.github/workflows/` exists
- `data_contracts.md` extraction — `02_contracts/README.md` open gap: currently folded into `api.md`; consider extracting if it grows