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
Fold AUCs: not completed
Mean AUC: not completed
Std: not completed
OOF AUC: not completed
Runtime: stopped after 90 seconds before fold 1 completed

Delta from 004:
not measured

Kaggle:
Public AUC: not submitted

What happened:
The added digit block made the 16,384-bin additive model too slow for the current iteration loop.
There was no held-out score before the 90-second stop, so there is no evidence to keep the change.

Decision:
revert for now. The idea may be worth revisiting with a cheaper model specifically for digit
features, but not by making the current high-resolution model much larger.

Next:
Keep experiment 004 as the EV reference and spend the next iteration budget on a different
competition rather than burning submissions or runtime on unvalidated variants.
