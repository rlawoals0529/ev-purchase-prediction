# 018 - Completed 20-fold source-allTE

Date: 2026-09-29

## Goal

Finish the fresh 20-fold version of the source-support + all-column nested-TE shallow LightGBM from experiment 015 and compare it honestly against the completed 10-fold model.

## Result

Full 20-fold OOF completed across all 668,665 train rows.

- pooled OOF AUC: **0.9462612139**
- mean fold AUC: **0.9462731149**
- fold std: **0.0012111505**
- 10-fold reference OOF: **0.9462042**
- pooled gain vs k10: **+0.0000570**

Fold AUCs:

`[0.9462523290, 0.9475631070, 0.9463222551, 0.9466920810, 0.9450468405, 0.9476968939, 0.9477996916, 0.9467723480, 0.9481653352, 0.9461038023, 0.9475351953, 0.9456430875, 0.9458564980, 0.9440016912, 0.9435416033, 0.9459569378, 0.9452295048, 0.9464233254, 0.9473601658, 0.9454996056]`

## Test-prediction relationship

- Spearman(k20, k10): **0.9999380663**
- Spearman(k20, high-res): **0.9951405455**

The 20-fold model is therefore a refinement of the same signal family rather than a new independent source of ranking diversity.

## Submission files

- standalone: `candidate_source_allte_k20_seed0.csv`
- 95/5 high-res rank blend: `candidate_source_k20_highres_rank_95_5_lex.csv`
- 92.5/7.5: `candidate_source_k20_highres_rank_92.5_7.5_lex.csv`
- 90/10: `candidate_source_k20_highres_rank_90_10_lex.csv`
- 87.5/12.5: `candidate_source_k20_highres_rank_87.5_12.5_lex.csv`
- 85/15: `candidate_source_k20_highres_rank_85_15_lex.csv`

All are built only from this repository's own predictions.

## Current interpretation

The previously submitted k10 90/10 source-allTE/high-res rank blend scored **0.94634 public**, improving the prior project best of 0.94617 by +0.00017.

Because k20 improves honest OOF by +0.000057 while preserving nearly the same test ordering, the next model-derived candidate should be **k20 90/10 high-res** unless the pending k10 87.5/12.5 public result gives stronger evidence that the blend weight should move.

## Seed-bag screen

A fresh k20 seed-1 fold-0 run was attempted, but it exceeded the execution timeout before producing an artifact. No score or conclusion is claimed from that incomplete run.
