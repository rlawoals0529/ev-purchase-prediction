# 018 - Fresh k20 source-allTE + OOF-validated high-res blend

Date: 2026-09-29

## Goal

Continue after the 90/10 source-allTE/high-res rank blend scored **0.94634 public**. Replace leaderboard-only weight tuning with a fresh complete 20-fold source model and actual OOF validation of the high-res blend.

## A. Fresh 20-fold source-allTE

Re-ran the experiment-015 source-support + all-column nested-TE shallow LightGBM with 20 outer folds, fold seed 0, TE seed 0, model seed 0. The run was single-process because concurrent folds exceeded container memory.

Result:

- pooled OOF AUC: **0.9462612139**
- mean fold AUC: **0.9462731149**
- fold std: **0.0012111505**
- delta vs experiment-015 k10 OOF 0.9462042: **+0.0000570**

Fold AUCs:

`0.9462523290, 0.9475631070, 0.9463222551, 0.9466920810, 0.9450468405, 0.9476968939, 0.9477996916, 0.9467723480, 0.9481653352, 0.9461038023, 0.9475351953, 0.9456430875, 0.9458564980, 0.9440016912, 0.9435416033, 0.9459569378, 0.9452295048, 0.9464233254, 0.9473601658, 0.9454996056`

This independently reproduces the public research reference `lgbF_k20_s0 = 0.946262` to ~8e-7 pooled AUC.

Test prediction correlations:

- Spearman vs our k10 source-allTE test prediction: **0.9999380663**
- Spearman vs our high-resolution additive test prediction: **0.9951405455**

Generated standalone:

- `candidate_source_allte_k20_seed0.csv`

## B. Recreate high-resolution OOF

Re-ran the exact experiment-004 high-resolution additive LightGBM using its original 3 stratified folds / seed 42.

Fold AUCs:

- 0.9444885436
- 0.9455807887
- 0.9454437233

Pooled OOF: **0.9451653307**

This matches the recorded experiment-004 OOF 0.945165 and fold values. The regenerated test prediction matches `ev_purchase_submission_v3_highres.csv` with max absolute difference **2.8e-11**, so the OOF and existing test file are aligned to effectively numerical identity.

## C. OOF rank-blend sweep

Rank-transform the full source-k20 OOF and the high-res OOF, then combine with a single global weight.

Selected points (high-res weight -> OOF):

- 0.0% -> 0.946261214
- 5.0% -> 0.946281021
- 7.5% -> 0.946287897
- 10.0% -> 0.946292730
- 12.5% -> 0.946295596
- 15.0% -> **0.946296662**
- 17.5% -> 0.946295662
- 20.0% -> 0.946292884
- 25.0% -> 0.946281579
- 30.0% -> 0.946262357

Fine-grid maximum is around **15.25% high-res**, AUC **0.946296681**.

To avoid choosing the weight on the same labels used to report the result, a 5-fold meta-validation was run. On each meta-training split the weight was chosen from a fixed grid, then applied to the held-out split.

Chosen rank-blend high-res weights by meta fold:

`[0.15, 0.15, 0.15, 0.15, 0.15]`

Meta-OOF AUC: **0.946296662**.

This makes 85/15 a stable, label-backed blend rather than a public-LB probe.

## D. OOF logit blend

A probability-logit blend was also checked. Coarse OOF values:

- 10.0% high-res -> 0.946295405
- 12.5% -> 0.946299601
- 15.0% -> 0.946302033
- 17.5% -> **0.946302661**
- 20.0% -> 0.946301595

Five-fold meta-validation selected **17.5% high-res in every fold**:

`[0.175, 0.175, 0.175, 0.175, 0.175]`

Meta-OOF AUC: **0.946302661**, +0.00004145 over the standalone k20 source model.

Generated:

- `candidate_source_k20_highres_rank_85_15_lex.csv`
- `candidate_source_k20_highres_logit_82p5_17p5.csv`

## Decision

The public result already established that adding a small amount of high-res diversity helps our source-allTE family: k10 90/10 rank scored **0.94634**, our current public best.

For the next attempt, prefer **k20 85/15 rank**. It combines the stronger 20-fold source model with the exact high-res model and its weight is selected consistently by five independent meta-validation splits. It also keeps the same rank-blend construction that already improved the public leaderboard.

The **k20 82.5/17.5 logit** file is a secondary candidate. Its OOF is slightly higher than the rank blend, but the improvement is only ~0.000006 and rank blending has direct leaderboard evidence plus less sensitivity to probability calibration.
