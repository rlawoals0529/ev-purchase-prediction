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

Using only this repository's predictions, package two deterministic rank blends between:

- primary: `candidate_source_allte_k10_v1.csv`
- secondary: `ev_purchase_submission_v3_highres.csv`

Their test rank correlation is **0.9953182399**.

Generated:

- 90% source-allTE / 10% high-res: `candidate_sourceallte_highres_rank_90_10_lex.csv`
- 85% source-allTE / 15% high-res: `candidate_sourceallte_highres_rank_85_15_lex.csv`

For exact weighted-rank ties, ordering is resolved lexicographically by continuous source-allTE prediction, high-res prediction, then id. Both files contain 286,571 unique ranks with the correct `id,Will_Buy_EV` schema.

## Decision

- Keep `candidate_source_allte_k10_v1.csv` as the validation-backed primary candidate.
- Prefer the **90/10** file as the next hedge if a second attempt is available; it uses less unvalidated secondary weight.
- Do not claim the 20-fold model yet. Resume only when the full fresh 20-fold OOF can be completed and compared honestly to 0.9462042.
