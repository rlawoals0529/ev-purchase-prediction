# 010 - Two-model candidate sweep

Date: 2026-09-26

Question:
Can a more explicit synthetic-data feature set push past the 0.945165 OOF / 0.94548 public reference without tuning directly against the public leaderboard?

Plan:
Run one fixed 5-fold scheme with two independent tree models. Both see the same raw columns plus decimal digit decomposition, target-free value frequencies, a small set of explicit interactions, and fold-safe target encodings for income and commute keys. The LightGBM and XGBoost predictions are then compared separately and as rank blends.

Why this next:
Public competition ablations repeatedly point to digit decomposition, frequency features and leak-free target encoding as the main reproducible gains above the raw-feature plateau. The useful part for this repo is not the published leaderboard number; it is whether those ideas improve our own frozen validation split.

Validation:
LGB fold AUCs: pending
LGB OOF AUC: pending
XGB fold AUCs: pending
XGB OOF AUC: pending
Best rank-blend OOF AUC: pending
Runtime: pending

Kaggle:
Current reference: 0.94548 public from experiment 004
Next submission: pending OOF results

Decision rule:
Submit the stronger single model first. Submit the second only if it is close enough to be a useful diverse component. Submit one rank blend only if it improves OOF. Do not search blend weights using the public leaderboard.

Notebook:
`ev_s6e9_candidate_sweep.ipynb` is prepared for Kaggle because this sweep is substantially heavier than the local baseline runs.

Decision:
pending

Next:
Run the notebook on Kaggle, record the fold/OOF results, then use the remaining submission budget on the best-supported candidates rather than arbitrary variants.
