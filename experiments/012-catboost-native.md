# 012 - Native CatBoost branch

Date: 2026-09-26

Question:
Can a learner with native ordered categorical statistics add useful ranking information beyond the engineered XGBoost/LightGBM branch?

Why this next:
Experiment 011 showed that reweighting the same prediction family has mostly saturated. CatBoost is different enough to be useful even if its standalone score is only close to the current best because its categorical handling and ordered statistics can change the ranking on rows where the boosting models agree.

Change:
Train CatBoost on the raw competition columns plus a small, fixed set of target-free representations: exact-string copies and coarse buckets for income/commute, decimal digits for those two high-cardinality numeric columns, and exact-value frequencies. Use the same stratified outer-fold idea and early stopping. No pseudo-labels, external labels, or leaderboard-selected thresholds.

Validation:
Fold AUCs: pending
Mean AUC: pending
OOF AUC: pending
Runtime: pending

Kaggle:
Current reference: **0.94615** public
CatBoost public AUC: pending

Decision rule:
Submit the CatBoost prediction once if its local score is competitive. If it is close to the current branch and its test ranking is meaningfully less correlated with XGBoost, test one fixed rank blend. Do not tune CatBoost/XGBoost weights against the public leaderboard.

Decision:
pending
