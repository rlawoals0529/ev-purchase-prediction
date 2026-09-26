# 003 - Smaller trees

Date: 2026-09-26

Question:
Does reducing tree capacity improve generalization on the same folds?

Change:
Only the LightGBM tree shape changed from the previous run: `num_leaves` from 31 to 15. I also
raised the estimator ceiling to 700 so early stopping could choose the useful number of smaller
trees. The data, folds, seed, learning rate and raw features stayed the same.

Validation:
Fold AUCs: 0.940837, 0.942491, 0.941993
Mean AUC: 0.941773
Std: 0.000693
OOF AUC: 0.941759
Fit time: 48.61 seconds across the three folds
Best iterations: 597, 408, 544

Delta from 002:
Mean AUC: +0.000090
OOF AUC: +0.000086

Kaggle:
Public AUC: pending

What happened:
All three folds improved, although the gain is small. The extra runtime is about eleven seconds for
the full CV run, which is cheap enough to keep. This is a better trade than adding another model or
an ensemble for a similarly small local gain.

I tested blending this model with the 31-leaf run and with a histogram gradient boosting model.
The best three-model OOF blend reached 0.941813, only about 0.000054 above this model by itself.
That number was selected on the same OOF predictions, so I am not treating it as evidence that the
extra complexity will generalize.

Decision:
keep. This is the current submission candidate.

Next:
Submit this unchanged and record the public AUC before doing any leaderboard-driven work.
