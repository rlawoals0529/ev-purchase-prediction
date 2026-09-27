# 008 - Exact-value categories

Date: 2026-09-26

Question:
Can LightGBM use repeated exact income and commute values better when they are available as
categorical identities as well as raw numbers?

Change:
Start from experiment 004. Keep the raw numeric columns and add two categorical copies:
`Annual_Income_USD` as an exact string value and `Daily_Commute_km` as an exact string value. Same
outer folds, seed and high-resolution additive model.

Validation:
Fold 1 AUC: 0.943669
Experiment 004 fold 1: 0.944489
Delta on fold 1: **-0.000820**
Runtime: 28.2 seconds for fold 1

Full mean/std/OOF: not run

Kaggle:
Public AUC: not submitted

What happened:
The exact categorical copies made the first held-out fold materially worse. The model appears to
handle these continuous values better through the high-resolution numeric representation than by
learning large categorical partitions.

Decision:
revert. Stop after fold 1 and do not submit.

Next:
Test digit-derived numeric features. Unlike frequency or exact-category copies, decimal digits can
represent periodic structure that an additive threshold model cannot express directly.
