# Reflection

#reflection #methodology #shapr #learning

## Simple Notes Capture Rule
Append short bullet points during active development; do not worry about perfect note placement. Consolidation happens at checkpoints and cycle end.

## Purpose
Captures methodological reflections, operational learnings, design tensions, and emerging insights arising during SHAPR-based development cycles.

Ideas recorded here may later inform:
- cycle records
- SKUs
- paper writing
- framework refinement

---

## Cycle 1 Consolidated Quick Capture

Methodological learnings from the build (see `dev_docs/cycle_record_notes/cycle_1.md` §6 for the full set):

- **Algorithm-agnostic architecture pays early.** A central `AppState` plus `BaseAlgorithm` let the UI ignore algorithm internals — the foundation for future LDA/NMF.
- **Widget lifetime follows its parent.** A panel owned by a transient view (the wizard) dies with it; tie persistent UI to state at the app level.
- **Strong observer references leak.** Subscribers that outlive their widgets keep them alive; use weak references — and still guard callbacks against destroyed widgets.
- **Tk geometry is pack-order dependent.** A greedily-expanding widget packed first starves everything after it; off-screen-but-instantiated widgets are a view concern.
- **Parameter values cross many layers.** UI → state → algorithm: validate types at the algorithm boundary; bind the form to state (traces) or retrains silently use stale defaults.
- **Attribute shadowing is silent breakage.** `self.state` clobbered the Tk widget `state` property — rename before it bites.
- **BERTopic's output shape varies.** Single-topic `probs` are 1-D; internal cluster ids differ from final topic ids — normalize/translate before mapping.
- **Webview wants a main thread.** A separate process satisfies pywebview and keeps the Tk loop responsive.
- **Pinned dependencies are non-negotiable** for a tool distributed to researchers.
- **Debug-logging wins.** Instrument each pipeline stage; a vague symptom becomes a specific failing stage.

## Cycle 1 Review Learnings

From the audit-based review (`dev_docs/cycle_record_notes/cycle_1_review.md` §4):

- **Audit before you fix.** A read-only, verified audit turns "review the whole codebase" into a prioritized, tractable fix list.
- **The parameter boundary is the risk surface** — the audit's core finding matched the painful bugs of the build cycle.
- **Distinguish structural from value changes** — a form that rebuilds on every keystroke destroys itself mid-edit.
- **Thread-safe UI dispatch is the linchpin** — several fixes only became safe once state reached the UI on the main thread.
- **A guard on `None` collides with "no result yet"** — use a distinct sentinel and initialise before the code that reads it.
- **`--force-with-lease` makes force-pushes safe** when rebasing shared branches.
- **A committed ignore file is half the fix** — already-tracked artifacts need explicit untracking.
- **A status doc is only truth if it's current** — update `audit.md` in the same change as the fix.
- **Verify commits reached `main` before deleting a branch.**

## Cycle 2 Consolidated Quick Capture

- **A footprint check before adopting a research library can save gigabytes.** OCTIS (0.13 MB package) pulls torch (~106 MB wheel, ~500 MB+ installed), spacy, sentence-transformers — 1–2 GB installed and 1 GB+ on a PyInstaller bundle — plus a `scikit-learn==1.1.0` pin incompatible with Python 3.11+. Gensim's `CoherenceModel` covered all three coherence measures at a fraction of the footprint.
- **Gensim's sliding-window coherence uses multiprocessing by default.** `c_v`/`c_npmi` raise "bootstrapping phase" errors from a GUI background thread on macOS spawn — force `processes=1` (and it is fast for research corpora).
- **Store evaluation output on the result object, not app state.** `TopicResult.quality_metrics` keeps each model's metrics with its result — the multi-model-ready shape, with no parallel state to keep in sync.
- **A render guard keyed on `None` collides with "no result yet".** The MetricPanel's first render was skipped until a sentinel distinct from `None` was used (D-014 pattern).
- **The single-event observer stays cheap when subscribers guard.** Expensive work belongs in controllers' background threads; subscribers compare the field they care about and skip work if unchanged.

## Cycle 3 Consolidated Quick Capture

- **Explore-before-build pays off.** The `to_dict()` feasibility probe in the notebook came before any design commitment — it ruled out kaleido (plotly upgrade + Chrome) and made the intertopic map easy. A cheap Explore check (can we read the rendered data?) saved the Build phase from a wrong dependency and a wrong strategy.
- **Design evolves through Use, not just upfront.** The lazy→pre-generation and `file://`→localhost changes came from real-app testing, not the initial design. The Use phase surfaced what the design could not anticipate (slow tabs, blank browser windows) — the cycle loop working as intended.
- **Front-load expensive once-only work into the wait the user already endures.** Pre-generating during training (≈2s) made every tab and click instant. The principle generalises: batch once-only work into an existing wait rather than spreading it across interactions.
- **SKU triage is about the user's point of view.** "No trivia, only meaningful information, specifically from the user's point of view" — SKUs should capture user-visible decisions and transferable insights, not implementation gotchas (colormaps, color-string parsing).
- **Formalising the ideation flow gave the cycle a clean front door.** ideas.md (raw) → cycle_plan.md (refined) → tasks.md (committed) meant the scope was decided before any code.
- **The human's cognitive workflows are worth capturing, not delegating.** The handoff/development/ideas flows in `workflow.mmd` are the real work the human does; documenting them keeps the human the epistemic authority.

## Cycle 4 Consolidated Quick Capture

- **Verify the library before assuming it lacks a feature.** I proposed implementing topic deletion the hard way after assuming BERTopic had no native delete — it has `delete_topics`. The same discipline caught a non-existent ttkbootstrap `git-merge` icon before it crashed at render. Reading the actual source (or glyphmap), not just the docs page, rules out both false negatives and runtime surprises.
- **A shared builder keeps two paths identical.** Extracting "build `TopicResult` from a fitted model" out of `train()` into `_build_result` means training and refinement produce the same result shape — and the doc-topic probability mapping stays correct after BERTopic's `topic_mapper_` remaps ids on merge/delete.
- **Refinement is "train-and-publish minus the training".** Mutating the model invalidates the metrics and the pre-generated visualisations; the re-derive pipeline reuses the existing services rather than writing new derivation logic.
- **Treeview has no checkboxes — the pattern is a glyph column plus mirrored native selection.** `selectmode="none"` makes the click handler the single source of truth, so the native selection can't fight the checkbox.
- **A widget's built-in search can be a trap.** Tableview's search filters *displayed* cells, so it would only match the 50-char snippet, not the full document — when the requirement is full-data search with a custom snippet, filter the data yourself.
- **Keep the user-facing texts separate from the training texts.** The model trains on preprocessed text; the user reads the original. Storing `original_texts` (and carrying it through refinement) is the difference between search that works and search against noise.
- **Deferring with a captured design beats cramming.** The "rename temp path" idea grew into a model-persistence design; recording it fully in `ideas.md` and deferring kept the cycle focused and gave the next cycle a ready-made spec.

## Reflection — SKU consolidation: a numbering scheme is a contract

The v0.1.0/v0.1.1 SKUs were too micro (25 + 11, many trivial). Consolidating to design-changing commits only (25 across cycle 1, 4 for cycle 2) and switching to cycle-coded IDs (`SKU-01-NN`, `SKU-02-NN`) made the knowledge layer scannable and aligned with the triage rule. The cost: the merge required updating every cross-reference (cycle records, repository structure, reflection, llm_guidance) — a reminder that a numbering scheme is a contract, and changing it has a documentation ripple.

## Reflection — Post-hoc reconstruction vs. capture-as-you-go

The SKU file (`dev_docs/current/05_knowledge/skus/v0.1.0.md`, holding the merged v0.1.0 + v0.1.1 SKUs) was **reconstructed after the fact from `logs.md`** — one pass over chat transcripts. SHAPR's working rule is the opposite: *capture lightweight notes during work, consolidate at checkpoints and cycle end.*

- Strengths of what happened: timestamps on every SKU and a clean 4-field format gave the reconstruction strong traceability (the example vault timestamps almost nothing).
- Cost: reconstruction is lossy and expensive — it cannot recover what the transcript never recorded, and it risks translating the AI's framing rather than the human's intent.
- Going forward: capture brief notes at cycle boundaries (this is what `current_state.md` / `tasks.md` / `decisions.md` are for), and let the cycle record be a consolidation, not a reconstruction.

## Reflection — SHAPR triage: you cannot SKU everything

The reconstruction produced **55 SKUs including trivial ones** (sash thickness, `.gitignore`, dependency pinning). The SHAPR paper is explicit: *"You cannot SHAPR everything… Users need to learn which tasks justify an SKU (e.g., Architectural Decision) and which do not (e.g., Centering a Div)."*

- A SKU should capture a decision or learning that **influences behaviour and future choices**.
- Housekeeping, one-line fixes, and cosmetic tweaks belong in a changelog or `tasks.md`, not the knowledge layer.
- Retro-fit rule for the existing SKU files: keep the ones with a transferable insight; demote the rest.

## Reflection — The audit as a cycle review

The v0.1.1 audit was, in SHAPR terms, a **review of Cycle 1** rather than a new cycle — this reframing produced `cycle_1_review.md`. Pattern worth keeping:

- The review is a *fresh, critical* read of the artefact, not the author's recap. Its verdict ("Release") only became trustworthy once the fixes were actually verified, not assumed.

## Future Generalisation Points

- **LDA/NMF will be the real test of the algorithm-agnostic design** (`D-001`) — if the UI needs per-algorithm branches, the abstraction is wrong.
- **The parameter-plumbing risk recurs on every new parameter.** The pattern is known (`D-010`, `D-013`); apply it at the boundary, not after the bug.
- **The SKU/evidence linkage is the next frontier** — cycle-coded SKU IDs, commit refs, and a `/evidence`-style home for transcripts would make the knowledge layer independently auditable.
