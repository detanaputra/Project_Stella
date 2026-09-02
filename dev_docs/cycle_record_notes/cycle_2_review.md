# Cycle 2 Review

#cycle2 #review #evaluation #shapr

## Review Summary
Topic quality metric visualizations are implemented, utilizing Gensim coherence instead of OCTIS.

## 1. What Went Well
1. 4 topic quality metrics are displayed in the new Metrics tab.
2. Topic quality backend using Gensim coherence and hand-rolled Topic Diversity instead of OCTIS.
3. Quality-of-life update: MouseWheel scrolling in the parameter panels is enabled.

## 2. Main Strength of Cycle 2
Design decision to use Gensim instead of OCTIS for a more efficient footprint. OCTIS depends on Torch, which may inflate the footprint size to 1 GB+ once downloaded — all that size for metrics that Gensim's `CoherenceModel` already provides (the three coherence measures), plus a trivial diversity formula.

## 3. Constraint and Remaining Gaps
1. Current topic quality metrics in the Metrics tab display the numbers without any explanation, which is not user-friendly for beginners. To be implemented in the upcoming cycle.
2. Topic refinement functionality (merge, delete, etc.) remains unimplemented. To be implemented in the next cycle.

## 4. Key Learning Confirmed
To allow topic model practitioners to assess topic quality when doing topic modelling analysis, develop functionality that enables users to measure topic quality metrics such as topic coherence and topic diversity, because of the requirement to evaluate the accuracy and usefulness of the automated topic extraction.

## 5. Risks to Watch Moving Forward
When topic refinement is implemented in the next cycle, the risk of stale metrics can surface. To mitigate that, recalculate the metrics every time the user does topic refinement.

## 6. Review of Cycle Objective
Cycle 2's objective was a complete, runnable v0.2.0. The review confirmed the feature set existed and the happy path ran. After all commits, the objective is met and v0.2.0 is ready to be merged to main.

## 7. Recommended Follow-On Direction
Start cycle 3 by creating a v0.3.0 branch after successfully merging the v0.2.0 branch to main. Afterwards, start brainstorming to discuss the implementation of cycle 3.

## 8. Review Verdict
Release.
