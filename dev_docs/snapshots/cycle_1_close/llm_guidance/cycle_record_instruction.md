# Cycle Record Instruction

How to write **cycle records** (`cycle_n.md`) and **cycle reviews** (`cycle_n_review.md`) — SHAPR's formal per-cycle artefacts.

Source: `example_docs/cycle_record_notes/` (cycles 0–4) and `example_docs/current/04_working/source_of_truth.md` (their role).

## The SHAPR cycle

Each cycle is one pass of the loop: **Explore → Build (Design-as-Build) → Use → Evaluate → Learn**. A cycle has a clear boundary (snapshot at start/end), a record, and a review.

## Roles of cycle artefacts (per `source_of_truth.md`)

- `cycle_n.md` and `cycle_n_review.md` are **cycle-end formal records** — historical evidence of the cycle.
- They are **not** the primary cycle-start control notes (that role belongs to `current_state.md`).
- Cycle records reference rationale rather than duplicating it: the **Key Decisions** section points to `decisions.md`.

## Filename and tag-line conventions

- `cycle_record_notes/cycle_0.md` … `cycle_N.md`, plus one `cycle_N_review.md` per cycle.
- Tag line after the title: `#cycle4 #formal_record #derived_signals #shapr` (cycle records) and `#cycle4 #review #evaluation #shapr` (reviews).

## `cycle_n.md` — the record

The **standardised template** (used from cycle 3 onward — use this):

```
# Cycle N

#cycle<N> #formal_record #shapr [ + domain tags ]

## Cycle Title          <- one-line theme of the cycle
## 1. Context           <- why this cycle, what problem/focus
## 2. Explore           <- design questions investigated (subsections allowed)
## 3. Build             <- what was built; subsections per artefact
## 4. Use               <- how the artefact was exercised/tested
## 5. Evaluate          <- what worked well / limitations
## 6. Learn             <- the consolidated learnings (the knowledge output)
## 7. Key Decisions Reinforced <- summary; detailed rationale lives in decisions.md
## 8. Outputs of Cycle N       <- notes/control artefacts, code artefacts, design knowledge
## 9. Cycle Outcome     <- overall verdict on the cycle
## 10. Likely Next Cycle Direction
```

The **early variant** (cycle 0) numbered 11 sections: 1. Context · 2. Explore · 3. Build (Design-as-Build) · 4. Use · 5. Evaluate · 6. Learn · 7. Key Decisions · 8. Outputs (Artefacts) · 9. Issues Identified at Cycle Close · 10. Readiness for Next Cycle · 11. Closing Reflection. Use the standardized 10-section form for new records; keep the "Issues at close / Readiness for next cycle" ideas inside **9. Cycle Outcome** and **10. Likely Next Cycle Direction**.

The **Learn** section is where the cycle's knowledge units live — write the transferable insights there (they are the practical SKUs of the cycle).

## `cycle_n_review.md` — the review

The **standardised review** (use this):

```
# Cycle N Review

#cycle<N> #review #evaluation #shapr

## Review Summary
## 1. What Went Well
## 2. Main Strengths of Cycle N
## 3. Constraints and Remaining Gaps
## 4. Key Learnings Confirmed
## 5. Risks to Watch Moving Forward
## 6. Review of Cycle Objective
## 7. Recommended Follow-On Direction   <- options (Option A / Option B)
## 8. Review Verdict
```

The **early variant** (cycle 0 review) was looser: Overall Assessment → What Is Already Strong → High-Impact Issues to Fix (each with Recommendation) → What Not to Fix Now → Recommended "Good Enough" Close → Learning Points → Readiness Verdict.

Write the review **from the perspective of a fresh reader/chat examining the artefacts**, not the author's voice. It should be genuinely critical — the example uses it to catch note drift, duplicate contracts, missing links, and tag inconsistencies, not just to praise.

## Workflow position

- The cycle record consolidates the accumulated evidence of the cycle (notes, decisions, quick captures, outputs) — produced from evidence, not memory.
- The review evaluates that record.
- Together they feed `reflection.md` and the eventual paper.

## Mapping to this project (Stella)

Stella currently documents by **version** (v0.1.0, v0.1.1), not by cycle. If you add cycle structure: v0.1.0 maps naturally to a *build cycle* and v0.1.1 to an *audit-and-release cycle*. Each would get a `cycle_N.md` + `cycle_N_review.md` under `dev_docs/cycle_record_notes/`.
