# 002 - LightGBM baseline

Date: 2026-09-26

Question:
Can I get a stable raw-feature baseline fast enough that later experiments are cheap to repeat?

Change:
Same 13 model features with `id` excluded. Three-fold stratified CV with native categorical
features, 31 leaves, learning rate 0.08, and early stopping. The split seed stays fixed at 42.

Validation:
Fold AUCs: 0.940770, 0.942360, 0.941921
Mean AUC: 0.941684
Std: 0.000670
OOF AUC: 0.941673
Fit time: 37.95 seconds across the three folds
Best iterations: 384, 318, 365

Kaggle:
Public AUC: pending

What happened:
The fold spread is small enough to use this as a control, and the whole CV loop finishes in under
a minute on the machine I used for the run. That makes it much more useful than the first CatBoost
attempt even before there is a leaderboard score.

No feature engineering was added. Train and test have no missing values, `id` is a contiguous row
identifier and is not used as a predictor, and the measured train/test distribution drift is very
small.

Decision:
keep as the first measured control.

Next:
Test whether a smaller tree is enough. The feature space is small, and extra leaves may be fitting
noise rather than useful interactions.
