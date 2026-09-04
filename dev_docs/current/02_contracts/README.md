# Contracts — Role Index

#contract #index #control

## Purpose
Assigns each contract **role** to its authoritative artefact. The actual contract *content* lives in the root files (do not duplicate them here — duplication creates drift). This folder adds the pieces that did not exist (`code_map.md`) and documents the role boundaries.

## Role assignments

| Contract role | Authoritative artefact | Status |
|---|---|---|
| Function contracts (callable signatures) | `api.md` (this folder) — `BaseAlgorithm`, `AppState`, services | In place |
| Data contracts (schemas / fields) | `api.md` + `app/models/topic_result.py`, `app/models/app_state.py` | In place |
| Parameter contract (algorithm hyperparameters) | `bertopic_hyperparams.md` (this folder) | In place |
| Code map (note↔code) | `code_map.md` (this folder) | ✅ created |
| Naming conventions | `naming_conventions.md` (this folder) | ✅ created |

## Drift rule

If code and contract disagree → the disagreement is **drift**. The current task must explicitly decide whether to update the code, the contract, or both. Contracts are authoritative for interface alignment, refactoring discipline, and cross-module consistency.

## Governing source

- Authority-by-role and conflict resolution: `dev_docs/current/04_working/source_of_truth.md` (Contract truth → this layer).
- Full repository layout and role mapping: `dev_docs/current/03_control/repository_structure.md`.

## Open gaps

1. ~~**`naming_conventions.md`** — a naming-rules note (file/module/function naming) does not exist yet.~~ — resolved: created.
2. **`data_contracts.md` as a standalone note** — currently folded into `api.md`; consider extracting if it grows.
