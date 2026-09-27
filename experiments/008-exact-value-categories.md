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
Not run yet.

Decision:
pending

Next:
Run fold 1 first. Continue only if it at least matches the 0.944489 reference fold before spending
the remaining runtime.
