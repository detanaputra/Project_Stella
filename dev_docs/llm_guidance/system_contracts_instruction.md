# System & Contracts Instruction

How to maintain the **design/spec layer** (`01_system`) and the **contract layer** (`02_contracts`) from the example vault.

Source: `example_docs/current/01_system/` and `example_docs/current/02_contracts/`.

## `01_system` — design/spec layer (what the system *is*)

Long-form conceptual design notes. One file per major module/subsystem plus a system-wide overview.

Typical files: `architecture.md` (high-level structure + flow), `prd.md` (product requirements), `api_design.md`, module engines (`indicator_engine.md`, `strategy_engine.md`, `backtesting_engine.md`, `execution_engine.md`, `data_layer.md`, `database.md`, `llm_integration.md`, `ui_design.md`), with `strategies/` for sub-concepts.

Common internal structure (from `architecture.md`):
```
# <Title>

#architecture #design #module #scope

## Purpose        <- what the note defines, in a few bullets
## High-Level Flow
<data → engine → signals → strategy → backtest → output>
## <module sections>
```
Design notes may carry **"Explainability and SHAPR Value"** sections (why the design matters methodologically) and `With [[...]]` dependency blocks referencing other notes.

Deferred subsystems get **placeholder notes** (a few lines noting the deferral) rather than being absent — this keeps links valid and records the intentional deferral.

## `02_contracts` — contract layer (stable interfaces that anchor AI-assisted coding)

These are the **machine-facing stability layer**: explicit, reusable contracts that prevent drift during AI-assisted coding. They change deliberately, not casually.

| File | Defines | Authoritative for |
|---|---|---|
| `function_contracts.md` | callable signatures | callable-interface truth |
| `data_contracts.md` | schemas / field rules | structure, schema, field truth |
| `naming_conventions.md` | file/module/function/indicator naming rules | naming-rule truth |
| `code_map.md` | the note↔code mapping | module-responsibility truth |
| `strategy_schema.md` | full JSON-schema-like spec for strategies | strategy configuration truth |

**`code_map.md`** structure:
```
## Purpose        <- "define the stable note-to-code mapping ... reduces drift between
                     conceptual system notes, actual code files, function contracts"
## Current Code Structure    <- flat list of code files
## Note-to-Code Mapping      <- per-subsystem: note → code mapping
```

## Drift rule (from `source_of_truth.md`)

If **code and contract disagree**: the disagreement is **drift**; the current task must explicitly decide whether to update the code, update the contract, or both. Contracts are authoritative for interface alignment, refactoring discipline, and cross-module consistency.

## Mapping to this project (Stella)

Stella already has equivalent documents at the repo root:
- `dev_docs/current/01_system/architecture.md` — the architecture note, moved into the `01_system` role.
- `dev_docs/current/02_contracts/api.md` — serves the function + data contract role.
- `dev_docs/current/02_contracts/bertopic_hyperparams.md` — the parameter contract.
- `CLAUDE.md` ≈ project overview

If the project formalises SHAPR folders, these can be linked (wiki-style or inline) rather than duplicated. `code_map.md` (note↔code) is the one contract Stella does **not** have — it would map the SKU/decision docs to `app/` files.
