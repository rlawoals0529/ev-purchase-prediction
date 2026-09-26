# 001 - CatBoost baseline

Date: 2026-09-26

Question:
What score do we get from a strong tabular baseline before feature engineering or ensembling?

Change:
This was the original control: five-fold stratified CV, raw competition features, `id` excluded
from the model, categorical columns passed directly to CatBoost, and early stopping on each
validation fold.

Validation:
Fold AUCs: not produced
Mean AUC: not produced
Std: not produced
Runtime: stopped after 240 seconds without completing the first fold in this environment

Kaggle:
Public AUC: not submitted

What happened:
The model was too slow for the iteration loop I want here. The dataset has 668,665 training rows,
and waiting several minutes before seeing even one fold makes every later comparison expensive.
There is no score to compare because I stopped the run rather than change the configuration halfway
through and still call it the same experiment.

The exact attempt is kept at [`scripts/archive/catboost_attempt.py`](../scripts/archive/catboost_attempt.py).

Decision:
revert as the working baseline. Keep the failed run in the history.

Next:
Try the same raw features with a faster tree implementation and keep the validation split fixed.
