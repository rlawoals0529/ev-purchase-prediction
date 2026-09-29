# 020 - Aligned multimodel ensemble + CatBoost seed bag

Date: 2026-09-29

## Context

The k20 source-allTE/high-res 90/10 and 87.5/12.5 submissions both scored **0.94636 public**, so further micro-adjustments to that two-model weight were stopped. The next axis was model-family diversity on the same strong 79-feature source-support + nested-TE representation.

All results below use the same frozen 10 outer folds (seed 0) and aligned validation rows.

## Single-model aligned OOF

- LightGBM: **0.9462042093**
- XGBoost: **0.9461942267**
- CatBoost seed 0: **0.9462002906**

OOF rank correlations:

- LGB / XGB: **0.9992542**
- LGB / CatBoost: **0.9977188**
- XGB / CatBoost: **0.9977586**

CatBoost is therefore the useful diversification member.

## Three-model blend before seed bagging

Best coarse rank mixture tested:

- 40% LGB / 10% XGB / 50% CatBoost
- pooled OOF: **0.9462709165**

This is +0.0000667 over aligned LGB alone.

## CatBoost model-seed bagging

Same features, folds and TE seed; only CatBoost model seed changes.

Single-seed OOF:

- seed 0: **0.9462002906**
- seed 1: **0.9461999412**
- seed 2: **0.9462112312**

Seed bags:

- seed 0 + 1 average: **0.9462471760**
- seed 0 + 1 + 2 average: **0.9462661060**

The bagging improvement is real and monotonic across the first three seeds.

## Best aligned ensemble after 3-seed CatBoost bag

Coarse rank-weight screen around the CatBoost-heavy optimum:

- 30% LGB / 10% XGB / 60% CB-bag3: 0.9462903626
- **25% LGB / 10% XGB / 65% CB-bag3: 0.9462906134**
- 35% LGB / 10% XGB / 55% CB-bag3: 0.9462891335

Selected aligned core: **25% LGB / 10% XGB / 65% CatBoost bag3**, OOF **0.9462906134**.

That is +0.0000864 over the original aligned source-allTE LGB.

## Submission candidates

The previously successful high-resolution additive model is kept as an external diversity component in rank space.

Generated from our own predictions only:

- `candidate_cb_bag3_multimodel_highres_rank_87p5_12p5_lex.csv`
- `candidate_cb_bag3_multimodel_highres_rank_90_10_lex.csv`
- `candidate_cb_bag3_multimodel_highres_rank_85_15_lex.csv`

Primary next candidate: **87.5% multimodel core / 12.5% high-res** because 12.5% high-res already produced the current 0.94636 public best with the source-allTE core.

The new 87.5/12.5 ranking has Spearman correlation **0.9994628393** to the current k20 87.5/12.5 public-best candidate, so it changes substantially more ordering than the k10→k20 refinement while remaining validation-backed.

## Decision

Promote `candidate_cb_bag3_multimodel_highres_rank_87p5_12p5_lex.csv` as the next submission. Do not return to fine-grained source/high-res weight probing unless this more diverse model-family ensemble fails to move the leaderboard.
