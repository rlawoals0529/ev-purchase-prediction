# 005 - Frequency features

Date: 2026-09-26

Question:
Do repeated raw values carry useful signal that the high-resolution additive trees are not already
capturing?

Change:
Keep experiment 004's folds and LightGBM settings. Add one unsupervised frequency feature for each
raw predictor, computed from the combined train/test feature values without using the target. The
original columns stay in the model.

Validation:
Fold AUCs: not completed
Mean AUC: not completed
Std: not completed
OOF AUC: not completed
Runtime: stopped after 180 seconds before completing the full run

Delta from 004:
not measured

Kaggle:
Public AUC: not submitted

What happened:
Doubling the feature count while keeping the 16,384-bin additive model made the run too slow for the
iteration loop I want here. I stopped it rather than changing settings mid-run and reporting a
number from a different experiment.

Decision:
revert. The question is still useful, but adding frequency copies of every column is too expensive
in this form.

Next:
Test only the two high-cardinality numeric columns, income and commute distance. Those are the
places where repeated exact values can plausibly add information beyond the raw numeric split while
keeping the model close to experiment 004 in size.
