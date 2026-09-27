# 007 - Cross-fit target buckets

Date: 2026-09-26

Question:
Can repeated income and commute values expose outcome structure that the raw additive splits miss?

Change:
Keep experiment 004's model and outer folds. Add fold-safe smoothed target encodings for four
predefined keys: exact integer income, income rounded down to $100, income rounded down to $1,000,
and integer commute distance. Training encodings are produced by an inner split so a row never uses
its own target. Validation and test mappings are learned only from the outer training fold.

Validation:
Fold 1 AUC: 0.944028
Experiment 004 fold 1: 0.944489
Delta on fold 1: **-0.000461**
Runtime: 25.0 seconds for the first fold

Full mean/std/OOF: not run

Kaggle:
Public AUC: not submitted

What happened:
The first held-out fold missed the reference by 0.000461, which is large relative to the gains I am
willing to chase here. Since this experiment was required to improve consistently across folds, I
stopped instead of spending two more folds to confirm a candidate that had already failed its first
check.

Decision:
revert. Do not submit.

Next:
Try representing repeated high-cardinality numeric values as categorical identities while keeping
the raw numeric columns. That lets the model decide how to group exact values without hand-built
target means.
