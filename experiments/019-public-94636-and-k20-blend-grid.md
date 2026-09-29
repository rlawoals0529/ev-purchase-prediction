# 019 - Public 0.94636 and k20 blend grid

Date: 2026-09-29

## Public result

The 87.5% source-allTE / 12.5% high-resolution additive rank blend scored **0.94636 public AUC**.

This is the current project public best:

- previous best: 0.94634 from 90/10 source-allTE/high-res
- new best: **0.94636** from 87.5/12.5
- gain over previous best: **+0.00002**
- gain over the older 0.94617 ceiling: **+0.00019**

Interpretation: the leaderboard trend from 90/10 to 87.5/12.5 points slightly toward more high-res weight, but the change is small enough that it should be treated as a local interpolation signal rather than proof of a broad optimum.

## Stronger primary model

The completed 20-fold source-allTE model has pooled OOF **0.9462612**, versus **0.9462042** for the 10-fold model, a gain of **+0.0000570**. Its test rank is ~0.999938 correlated with the 10-fold model, so it is a refinement rather than a new signal source.

## New k20 blend candidates

Using only our own predictions, generated:

- `candidate_source_k20_highres_rank_87p5_12p5_lex.csv`
- `candidate_source_k20_highres_rank_85_15_lex.csv`

Both use the completed k20 source-allTE prediction as primary and the existing high-resolution additive model as secondary, with deterministic lexicographic tie breaking.

## Decision

Use **k20 87.5/12.5** as the next submission candidate. It combines the locally stronger primary model with the currently best public blend weight. Hold k20 85/15 as the next directional test only if 87.5/12.5 continues to improve or at least holds the public score.
