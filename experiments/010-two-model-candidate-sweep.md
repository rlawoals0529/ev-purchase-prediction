# 010 - Two-model candidate sweep

Date: 2026-09-26

Question:
Can a more explicit synthetic-data feature set push past the 0.945165 OOF / 0.94548 public reference without tuning directly against the public leaderboard?

Plan:
Run one fixed 5-fold scheme with two independent tree models. Both see the same raw columns plus decimal digit decomposition, target-free value frequencies, a small set of explicit interactions, and fold-safe target encodings for income and commute keys. The LightGBM and XGBoost predictions are then compared separately and as rank blends.

Why this next:
Public competition ablations repeatedly point to digit decomposition, frequency features and leak-free target encoding as the main reproducible gains above the raw-feature plateau. The useful part for this repo is not the published leaderboard number; it is whether those ideas improve our own frozen validation split.

Validation:
LGB fold AUCs: not recorded in repo yet
LGB OOF AUC: not recorded in repo yet
XGB fold AUCs: not recorded in repo yet
XGB OOF AUC: not recorded in repo yet
Best rank-blend OOF AUC: not recorded in repo yet

Kaggle:
Reference before this experiment: **0.94548** public from experiment 004
LightGBM public AUC: **0.94607**
XGBoost public AUC: **0.94610**
Best public improvement over experiment 004: **+0.00062**

What happened:
Both models cleared the previous public reference independently, and they landed almost on top of each other. XGBoost is ahead by 0.00003. Their test-set rankings are also very similar, so a direct LGB/XGB blend is more likely to be a small refinement than a new source of signal.

Decision:
keep both as measured candidates. XGBoost is the current public best at 0.94610.

Next:
Blend the stronger XGBoost candidate with the older high-resolution additive model instead of only blending the two nearly identical engineered models. That gives the ensemble a more distinct second ranking while keeping the experiment small.
