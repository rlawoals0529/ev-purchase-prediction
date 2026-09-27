# 006 - Focused frequency features

Date: 2026-09-26

Question:
Do exact-value frequencies help on the two numeric columns with the most repeated fine-grained
structure?

Change:
Start from experiment 004 unchanged and add only two target-free features: the combined train/test
frequency of `Annual_Income_USD` and `Daily_Commute_km`. Same folds, seed, model and raw columns.

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
Run on the fixed folds. If this does not beat 0.945165 OOF by a useful margin, move to fold-safe
target-derived features rather than adding more unsupervised copies.
