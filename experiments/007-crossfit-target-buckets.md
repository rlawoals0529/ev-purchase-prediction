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
Run on the fixed folds. Submit only if the gain is consistent across folds and large enough to
clear experiment 004 rather than fourth-decimal noise.
