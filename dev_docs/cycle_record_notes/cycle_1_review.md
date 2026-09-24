# Cycle 1 Review

#cycle1 #review #evaluation #shapr

## Review Summary

A read-only audit of the Cycle 1 build (run 2026-08-17 → 2026-08-18, reconstructed as 10 SKUs, SKU-01-16…25, in `dev_docs/current/05_knowledge/skus/v0.1.0.md`) read all 45 Python files plus the docs and training notebook and found **22 findings**: H1–H6 (high), M1–M8 (medium), L1–L8 (low). The BERTopic **parameter plumbing** between UI, state, and `train()` was the core risk. All 22 were fixed and released: v0.1.0 merged to `main`, the `v0.2.0` branch created, and `ROADMAP.md` documents the released feature set.

**Evidence:** `dev_docs/snapshots/cycle_1_close/audit.md` — the complete findings list with fix statuses that underpins this review.

## 1. What Went Well

- **Audit-first:** the review was read-only — no code was touched before findings were accepted, preserving the clean Cycle 1 baseline.
- **Verified fixes:** headless tests after the M-batch; a dedicated live-Tk test after the M3 startup-crash fix; the H1 fix verified live by the human ("The test works great").
- **Clean release procedure:** merge → verify on `main` → delete local branch → fresh `v0.2.0` branch from `main`.
- **One commit per severity class** kept the fix history readable and each batch a testable unit.

## 2. Main Strengths of Cycle 1

- **MVC + algorithm-agnostic design** (`BaseAlgorithm`, central `AppState`) — the UI stayed independent of algorithm internals and scales to LDA/NMF.
- **Modular hyperparameter sections** with prefixed state keys — reused in two surfaces (wizard + settings panel) with no key collisions.
- **Browser-based visualizations** via pywebview in a separate process — interactive Plotly plots without bundling a browser engine.
- **Pinned dependencies** — a reproducible environment, essential for a tool distributed to researchers.
- **`.stella` project-file format** and `ProjectService` — session continuity for users.
- **Weak-ref observer lifecycle** in `AppState` — destroyed widgets are garbage-collected; callbacks guard against stale widgets.

## 3. Constraints and Remaining Gaps

Findings the review identified in the Cycle 1 artefact (severity-ordered; all fixed during the review):

### 3.1 High (H1–H6) — fixed
- **H1** parameter form rebuilt itself on every keystroke, destroying the edit mid-typing → `AlgorithmSettingsPanel._render()` rebuilds only on structural change — `10b822e`.
- **H2–H6** wizard default-parameter sync; the five documented BERTopic hyperparameters wired into `train()`; parameter UI shown before the first run; exception-safe event polling; default parameter initialization — `a02d9f5`.

### 3.2 Medium (M1–M8) — fixed
Thread-safe UI dispatch (`AppState.call_on_main`), training re-entrancy guard, matplotlib figure cleanup, summary-panel rebuild guard + row cap, real export panel and offline Plotly visualizer, DataLoader CSV/encoding edge cases, debug-print removal, HDBSCAN `min_cluster_size` — `fdd421b`. The M3 rebuild guard then needed its own follow-up fix (initialization order + a sentinel distinct from `None` so the placeholder renders on a fresh start) — `0383ce1`.

### 3.3 Low (L1–L8) — fixed
- dead views / stub menus removed (real Edit menu, theme switcher on App Settings), parameter validation (UMAP/ngram clamps), LoadingPanel stacking guard, stop-words path handling, notebook bugs, project-load validation, milestone-based progress; `audit.md` updated including the L2 status — `86f8dd5`.

### 3.4 Process gaps
- **No committed `.gitignore`** — the `.claude` folder was "tracked" only because nothing ignored it. Root cause fixed and compiled artifacts untracked — `baa3443`.
- **`audit.md` drifted from truth** — L2 was already fixed but the status was not recorded; the doc is now updated in the same change as each fix.

## 4. Key Learning Confirmed

To allow topic model practitioners to control and reproduce their topic models when doing topic modelling analysis, develop functionality that exposes the algorithm's hyperparameters to the user through the interface, because the ability to set and adjust the model parameters is essential for researchers to tailor the automated topic extraction to their data and document the configuration for reproducibility.

## 5. Risks to Watch Moving Forward

- **Parameter plumbing (UI ↔ state ↔ `train()`)** remains the top risk surface — validate types at the algorithm boundary on every new parameter.
- **Status-doc drift** — `audit.md`, and any status doc, must stay in sync with the code change that fixes it.
- **Guard implementation** — previously-fixed guards (sentinel + init order) can regress silently; keep the distinct-sentinel pattern.
- **Forward-branch coordination** — force-pushes to shared branches must use `--force-with-lease`.
- **Unverified happy-path claims** — the release was only trusted after fixes were actually verified, not assumed.

## 6. Review of Cycle Objective

Cycle 1's objective was a complete, runnable v0.1.0. The review confirmed the feature set existed and the happy path ran, but **the codebase was not release-safe until the review's findings were fixed**. After all 22 fixes, the objective is met and v0.1.0 is released: `ROADMAP.md` documents the six feature categories, and the `v0.2.0` branch is ready.

## 7. Recommended Follow-On Direction

- **Option A — v0.2.0 feature list:** write the v0.2.0 `ROADMAP.md` entries (LDA/NMF algorithms, embedded matplotlib charts, document search/filter, batch processing) and open `current_state.md` for the cycle.
- **Option B — working/control scaffolding:** create `source_of_truth.md`, `tasks.md`, `decisions.md`, and `current_state.md` so future cycles capture decisions and state as they happen instead of reconstructing from logs.

## 8. Review Verdict

**Release.** Cycle 1 delivered a complete, now-audited application; all 22 findings are fixed and recorded in `audit.md`; v0.1.0 is released from `main` and documented in `ROADMAP.md`; the `v0.2.0` branch is ready for the next feature set.
