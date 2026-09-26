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
Public AUC: **0.94168**
Submission: `ev_purchase_submission_v2.csv`

What happened:
All three folds improved, although the gain is small. The public score landed only 0.000079 below
the OOF AUC, which is close enough that I trust this split as a useful local reference rather than
changing the validation scheme around one leaderboard result.

I tested blending this model with the 31-leaf run and with a histogram gradient boosting model.
The best three-model OOF blend reached 0.941813, only about 0.000054 above this model by itself.
That number was selected on the same OOF predictions, so I am not treating it as evidence that the
extra complexity will generalize.

Decision:
keep as the measured baseline. It is no longer the best local candidate.

Next:
Use the same folds to test whether more resolution on income and an additive tree structure can
capture signal the small-tree baseline is smoothing away.
