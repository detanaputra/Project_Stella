# Cycle 4 Review

#cycle4 #review #evaluation #shapr

## Review Summary
Cycle 4 delivered four work packages: topic refinement (merge/delete/label with a checkbox selection UI), document exploration (full-text search, detail view, topic filter), pywebview retirement, and UI polish. The feature set is implemented and committed on `v0.4.0`, SKUs are documented (`SKU-04-01…06`), and the cycle record is written. The review confirms the objective was met, with a few gaps worth carrying forward.

## 1. What Went Well
1. **Native BERTopic ops, no reimplementation.** Merge/delete use BERTopic's own `merge_topics`/`delete_topics`; the work was in the shared `_build_result` and the re-derive pipeline, not in re-deriving topic logic.
2. **The re-derive pipeline reuses existing services.** After a mutation, metrics and visualisations are recomputed with the same services the training pipeline uses — no new derivation code.
3. **Document exploration is a coherent feature.** Search (full-text, button-triggered), the Detail window, and the topic filter compose cleanly and answer the two real questions: "which topic is this document in?" and "which documents are in this topic?"
4. **Cleanup and polish were kept small.** WP2 (dead-code removal) and WP3 (metrics explanations, centred dialogs, MVP limiting) were low-risk and correctly excluded from the SKUs.

## 2. Main Strengths of Cycle 4
1. **The checkbox-glyph + mirrored-native-selection pattern** is a clean answer to a real Tk limitation (no native checkboxes) — click-anywhere-to-toggle with row highlight, driven by one handler.
2. **Deferring the persistence design with a full spec.** The "rename temp path" idea grew into a model-identity + persistence design; capturing it completely in `ideas.md` and deferring kept the cycle focused and gave the next cycle a ready-made spec.
3. **SKU triage held.** 6 SKUs for two substantial features; WP2/WP3 correctly judged trivial.

## 3. Constraints and Remaining Gaps
1. **No committed test suite.** Verification was headless `py_compile`/import checks plus user testing — not automated tests. The doc-topic mapping after a merge/delete relies on BERTopic's probability remapping and has only been verified by inspection, not a real-corpus smoke test.
2. **☐/☑ checkbox glyphs may render inconsistently across platforms** — a build-time risk that needs a visual check on Windows/Linux.
3. **Document search is substring-only** — no phrase or fuzzy matching; the Document Assignments table is capped at 200 shown rows even under a filter.
4. **`original_texts` is set by the controller at training time.** Any future path that builds a result without it (e.g., a load-from-disk path) would silently lose search/display.
5. **`AppState` was deliberately left unchanged** — no `current_model_id`; multi-model remains a future change.

## 4. Key Learning Confirmed
To let topic model practitioners treat topic modelling as an iterative, interpretable process rather than a one-shot output, develop functionality that lets them act on the model (merge, delete, and label topics) and interrogate it against the data (search and inspect the documents behind each topic), because a model is only useful to a researcher when they can refine it and verify its topics against the actual documents.

## 5. Risks to Watch Moving Forward
1. **The deferred persistence design is large** — a single-file zip bundle, model-id subfolders, and per-algorithm save/load behind `BaseAlgorithm`. The BERTopic `save()`/`load()` feasibility check (embedding-model include/exclude, size) is a gate before committing to it.
2. **No automated tests** — regression risk grows with each feature; the model layer is unit-testable headless and should get a suite.
3. **Cross-platform rendering** — the checkbox glyphs and the icon+text toolbar need a visual pass on Windows/Linux before release.

## 6. Review of Cycle Objective
The objective — topic refinement with a clear selection UI, document exploration, and cleanup/polish — was met. All four work packages are implemented, committed, and documented. The success signal (select topics → merge/delete/label with confirmation, find and inspect documents, see metrics/visualisations re-derive) is satisfied by the implementation.

## 7. Recommended Follow-On Direction
- **Option A — release, then the designed feature:** release v0.4.0 to `main`, then take on the deferred **model persistence + project folder** (starting with the BERTopic save/load feasibility check), then the post-graduation backlog.
- **Option B — release, then harden first:** release v0.4.0, then add the committed test suite and search improvements (phrase/fuzzy, uncapped table) before the persistence feature.

Either way, the release is the immediate next step.

## 8. Review Verdict
**Release.** The v0.4.0 feature set is complete and coherent; the remaining gaps (test suite, cross-platform glyph check, real-corpus smoke test of refinement) are follow-on hardening, not blockers.
