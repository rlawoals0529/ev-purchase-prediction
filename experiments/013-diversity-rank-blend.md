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
Previous reference: **0.94615** public
Candidate file: `candidate_best_diversity_v1.csv`
Public AUC: **0.94617**
Delta: **+0.00002**

What happened:
The fixed diversity blend improved the displayed public score by 0.00002. The gain is small, but it is consistent with the reason for the experiment: add a little non-tree ranking information without replacing the stronger tree predictions.

One implementation detail matters for the next step. Rank averaging produced 4,811 exact ties across the 286,571 test rows. ROC AUC only cares about ordering, so those tied groups leave ranking information unused even though the component models can distinguish the rows.

Decision:
keep. 0.94617 becomes the current public reference. Do not search nearby blend weights. Test one deterministic tie-breaking refinement that preserves every non-tied ordering from this submission.
