# 014 - Lexicographic tie-break

Date: 2026-09-26

Question:
Can the 4,811 exact ties created by experiment 013's rank average be resolved without changing any ordering the current best already expresses?

Change:
Start from `candidate_best_diversity_v1.csv`. Preserve every non-tied ordering exactly. For rows tied by the blend, use the continuous engineered XGBoost score as the first tie-breaker and engineered LightGBM as the second. Convert the resulting lexicographic order to unique rank scores.

Validation:
No new target fit. The transformation changes only exact ties in the experiment 013 ranking.

- rows: 286,571
- exact ties before: 4,811
- exact ties after: 0
- non-tied pair ordering changes: 0

Kaggle:
Reference: **0.94617** public
Candidate: `candidate_best_diversity_lexsort_v2.csv`
Public AUC: **0.94617**
Delta: **0.00000** at displayed precision

What happened:
Removing the exact ties did not move the displayed public AUC. That closes this path: the remaining gap is not coming from rank collisions created by the blend.

Decision:
revert as an improvement idea. Keep experiment 013 as the current measured reference. Do not spend more submissions on tie-breaking or adjacent blend weights.
