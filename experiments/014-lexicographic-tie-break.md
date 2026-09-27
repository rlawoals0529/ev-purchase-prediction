# 014 - Lexicographic tie break

Date: 2026-09-26

Question:
Can the 0.94617 diversity blend improve by resolving only its exact prediction ties, without changing any ordering the blend already expressed?

Change:
Start from experiment 013's submitted ranking. It contains 4,811 duplicate prediction positions across 286,571 test rows because weighted rank sums are discrete.

Preserve the experiment 013 ordering everywhere its score differs. Inside exact-tie groups only, order rows by the continuous engineered XGBoost prediction. If XGBoost itself ties, use the continuous engineered LightGBM prediction as a final deterministic key. Convert the resulting lexicographic order back to strictly unique rank scores.

This is not a new fit and it does not search weights. It only supplies an ordering where experiment 013 previously declared rows equal.

Validation:
Rows: 286,571
Exact ties before: 4,811
Exact ties after: 0
Non-tied experiment 013 orderings changed: 0

Kaggle:
Current reference: **0.94617** public
Candidate file: `candidate_best_diversity_lexsort_v2.csv`
Public AUC: pending

Decision rule:
Submit once. Keep it only if the score improves or remains competitive. Do not iterate through alternative tie-break keys based on public results.

Decision:
pending
