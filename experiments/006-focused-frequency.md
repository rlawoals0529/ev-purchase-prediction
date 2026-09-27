# 006 - Focused frequency features

Date: 2026-09-26

Question:
Do exact-value frequencies help on the two numeric columns with the most repeated fine-grained
structure?

Change:
Start from experiment 004 unchanged and add only two target-free features: the combined train/test
frequency of `Annual_Income_USD` and `Daily_Commute_km`. Same folds, seed, model and raw columns.

Validation:
Fold AUCs: 0.944453, 0.945516, 0.945345
Mean AUC: 0.945105
Std: 0.000466
OOF AUC: 0.945100
Runtime: 90.6 seconds across three folds
Best iterations: 540, 491, 515

Delta from 004:
OOF AUC: **-0.000065**

Kaggle:
Public AUC: not submitted

What happened:
The two frequency features made every fold slightly worse or effectively flat. The runtime also
rose enough that there is no reason to keep them for a negative local result.

Decision:
revert. Do not submit.

Next:
Move to fold-safe target-derived features on repeated income and commute buckets. Those can test
whether the repeated values carry outcome structure rather than just population-frequency signal.
