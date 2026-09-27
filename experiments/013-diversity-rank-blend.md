# 013 - Diversity rank blend

Date: 2026-09-26

Question:
Can one fixed, diversity-aware rank blend improve the 0.94615 public reference without continuing to search weights against the public leaderboard?

Change:
Rank-normalize four already-generated prediction streams and combine them with weights fixed before submission:

- 45% engineered XGBoost
- 30% engineered LightGBM
- 20% high-resolution additive LightGBM
- 5% fold-safe target-encoding logistic model

The XGBoost and engineered LightGBM models are almost redundant, but both are individually strong. The high-resolution model is less correlated with them, and the target-encoding logistic branch is another independently trained ranking with different inductive bias. The logistic branch is intentionally kept at only 5% because its local holdout AUC was lower than the tree models even though it adds diversity.

Measured test rank correlations before submission:

- XGB vs engineered LGB: 0.999302
- XGB vs high-resolution: 0.995254
- XGB vs TE-logit: 0.995330
- high-resolution vs TE-logit: 0.994719

Kaggle:
Current reference: **0.94615** public
Candidate file: `candidate_best_diversity_v1.csv`
Public AUC: pending

Decision rule:
Submit this exact blend once. If it does not improve the reference, do not tune nearby weights on the public leaderboard. The next change should add a genuinely different model family or feature representation.

Decision:
pending
