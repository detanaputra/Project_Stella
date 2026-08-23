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

## Reflection — Post-hoc reconstruction vs. capture-as-you-go

The SKU files (`dev_docs/current/05_knowledge/skus/v0.1.0.md`, `v0.1.1.md`) were **reconstructed after the fact from `logs.md`** — one pass over chat transcripts. SHAPR's working rule is the opposite: *capture lightweight notes during work, consolidate at checkpoints and cycle end.*

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
- **The SKU/evidence linkage is the next frontier** — global SKU IDs, commit refs, and a `/evidence`-style home for transcripts would make the knowledge layer independently auditable.
