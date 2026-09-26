# 001 - CatBoost baseline

Date: 2026-09-26

Question:
What score do we get from a strong tabular baseline before feature engineering or ensembling?

Change:
This is the control. Five-fold stratified CV, raw competition features, `id` excluded from the
model, categorical columns passed directly to CatBoost, and early stopping on each validation
fold.

Validation:
Fold AUCs: pending
Mean AUC: pending
Std: pending
Runtime: pending

Kaggle:
Public AUC: pending

What happened:
Not run yet. This file exists before the result so the experiment is not rewritten around the
number we get.

Decision:
pending

Next:
Run the baseline unchanged. Inspect fold spread before changing features.
