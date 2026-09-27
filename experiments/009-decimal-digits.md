# 009 - Decimal digit features

Date: 2026-09-26

Question:
Is there useful periodic structure in income and commute values that threshold-only additive trees
cannot express directly?

Change:
Start from experiment 004. Add numeric digit features only for the two high-resolution columns:
income units/tens/hundreds/thousands/ten-thousands and commute tenths/ones/tens. Keep the raw
columns, folds, seed and model unchanged.

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
Run fold 1 first. Continue only if it beats the 0.944489 reference rather than adding feature count
for no measurable gain.
