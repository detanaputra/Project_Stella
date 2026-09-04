# Cycle 3 Review

#cycle3 #review #evaluation #shapr

## Review Summary
The visualisation path and the main-window layout structure were revisited in this cycle. Visualisations are now pre-generated within the training process, specifically after the metric computation step. This made the toolbox panel — which showed buttons to launch visualisations — redundant. Therefore, the toolbox was removed, and the hyperparameter panel, previously on the right side, now sits on the left, opening space for the visualisation tabs.

## 1. What Went Well
1. Visualisation tabs and the interactive button open quickly, as all the visualisations are pre-generated during the training process.
2. Layout restructuring reduced redundancy and made the layout more intuitive.

## 2. Main Strength
1. All generative processes that require the user to wait are pooled into the training process, where an indeterminate loading panel is shown. This eliminates the micro-waiting of lazy loading (generating on demand). Despite lazy loading's advantage (only generating what users need, emphasising space efficiency), the micro-waiting introduces a slight delay that makes the software seem unresponsive. Therefore, the pre-generated visualisation path was chosen.

## 3. Constraint and Remaining Gaps
1. The top-level panels spawn at seemingly random locations and need to be fixed to the centre of the main window.

## 4. Key Learning Confirmed
To allow topic model practitioners to explore and interpret their models when doing topic modelling analysis, develop functionality that enables users to view the visualisations directly in the application, because visual inspection of the model output is essential for evaluating the usefulness and interpretability of the automated topic extraction.

## 5. Risks to Watch Moving Forward
Large corpora and limited computing resources will increase the waiting time.

## 6. Review of Cycle Objective
Cycle 3's objective was a complete, runnable v0.3.0. The review confirmed the feature set existed and the happy path ran. After all commits, the objective is met and v0.3.0 is ready to be merged to main.

## 7. Recommended Follow-On Direction
Start cycle 4.

## 8. Review Verdict
Release.
