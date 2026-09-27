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
Fold AUCs: pending
Mean AUC: pending
Std: pending
OOF AUC: pending
Runtime: pending

Delta from 004:
pending

Kaggle:
Public AUC: not submitted

What happened:
Not run yet. This record exists before seeing the result.

Decision:
pending

Next:
Run on the fixed folds. Only submit if the gain is large enough to survive fold noise; otherwise
leave it in the history and move to fold-safe target-derived features.
