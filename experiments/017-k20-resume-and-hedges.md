# 017 - Resume 20-fold source-allTE + hedge packaging

Date: 2026-09-28

## Goal

Continue after experiment 016 with the validation-backed source-support + all-column nested-TE LightGBM. Prioritize a reproducible 20-fold confirmation and package conservative own-model hedge submissions while avoiding public-prediction borrowing.

## Fresh 20-fold reproduction

Configuration is the same source-support/all-TE shallow LightGBM family as experiment 015, outer folds changed from 10 to 20, fold seed 0, TE/model seed 0.

The previous partial run had reported fold 0 = 0.946312 and fold 1 = 0.947537. A fresh rerun was started because those artifacts were not available locally. Fresh completed folds:

- fold 0: **0.9462523290** (best iteration 1521)
- fold 2: **0.9463222551** (best iteration 1281)
- fold 4: **0.9450468405** (best iteration 1516)

These values are close enough to confirm the model family is behaving normally, but fold 0 differs from the earlier partial check by about 0.00006. Therefore the earlier partial numbers should not be used as authoritative evidence for the final 20-fold OOF.

The local execution container could not hold two concurrent full folds; the second process was memory-killed. The run was stopped after three completed fresh folds rather than claiming an incomplete pooled OOF.

## Public-methodology check

A current Kaggle discussion reports a 10-fold XGBoost single-model CV around 0.94652 and logistic regression around 0.94640, but no reproducible implementation details were disclosed in the material found. No external predictions were used.

## Own-model hedge files

Using only this repository's predictions, package deterministic rank blends between:

- primary: `candidate_source_allte_k10_v1.csv`
- secondary: `ev_purchase_submission_v3_highres.csv`

Their test rank correlation is **0.9953182399**.

Generated initial hedges:

- 90% source-allTE / 10% high-res: `candidate_sourceallte_highres_rank_90_10_lex.csv`
- 85% source-allTE / 15% high-res: `candidate_sourceallte_highres_rank_85_15_lex.csv`

For exact weighted-rank ties, ordering is resolved lexicographically by continuous source-allTE prediction, high-res prediction, then id. Files contain 286,571 unique ranks with the correct `id,Will_Buy_EV` schema.

## Public result

The user submitted the **90/10** hedge on 2026-09-28. Kaggle public AUC: **0.94634**.

This is the best score produced by this repository so far and improves the previous 0.94617 best by **+0.00017**.

Because the standalone source-allTE public score has not been observed in this experiment log, the 0.94634 result does not by itself prove that exactly 10% high-res is optimal. It does establish that this cross-generation ranking is competitive and worth a narrow local leaderboard sweep now that attempts are available.

Additional deterministic controls generated from the same two own-model predictions:

- 92.5% / 7.5%: `candidate_sourceallte_highres_rank_92p5_7p5_lex.csv`
- 87.5% / 12.5%: `candidate_sourceallte_highres_rank_87p5_12p5_lex.csv`
- 95% / 5%: `candidate_sourceallte_highres_rank_95_5_lex.csv`
- 82.5% / 17.5%: `candidate_sourceallte_highres_rank_82p5_17p5_lex.csv`

## Decision

- **0.94634 from 90/10 is the current public best.**
- Next preference: **87.5/12.5**, a small move toward the diverse high-res ranking.
- If it improves, continue toward 85/15; if it degrades, test 92.5/7.5 or revert to 90/10.
- Keep `candidate_source_allte_k10_v1.csv` as the validation-backed primary model; submit it when a clean measurement of the blend contribution is worth an attempt.
- Do not claim the 20-fold model yet. Resume only when the full fresh 20-fold OOF can be completed and compared honestly to 0.9462042.
