# 016 - Post source-allTE screens

Date: 2026-09-28

## Goal

Continue from experiment 015 without spending submissions on tiny unmeasured variants. Test structurally distinct ideas that could plausibly explain the newly reported ~0.9464-0.9465 CV models, and reject them quickly on the same frozen folds when they fail.

## A. Additive logistic on transformed nested TEs

Hypothesis: the recovered generator is close to additive, so log-odds transformed nested target encodings plus source-support features may combine better linearly than with trees.

Frozen setup: 10 outer folds, fold seed 0; same source-support and nested-TE family as experiment 015; C=1 selected before expanding past fold 0 after C=0.1 was essentially flat there.

Measured folds:

- fold 0: **0.946467**
- fold 1: **0.945911**
- fold 2: **0.945805**

Decision: **reject**. Fold 0 was flattering; the next two folds fall well behind the tree recipe.

## B. XGBoost with cross-feature interactions forbidden

Hypothesis: a public ablation on a simpler feature set reported a large gain from forbidding feature interactions. Re-test that idea on the stronger 81-column source-support + all-TE representation.

First sanity-check the unconstrained implementation against an independent reference on frozen fold 0:

- our unconstrained XGB fold 0: **0.946881**
- independent reference fold 0: ~**0.946865**

The implementation therefore reproduces correctly to ~0.00002.

Then change only the XGBoost interaction constraints so each tree path can use one feature only:

- additive-constrained XGB fold 0: **0.946596**
- delta vs unconstrained: **-0.000285**

Decision: **reject**. The no-interaction gain from the simpler public baseline does not transfer to the stronger all-TE representation.

## C. LightGBM histogram-resolution increase

Hypothesis: income has 13,214 distinct values, so max_bin=1024 may still leave resolution on the table.

Frozen fold 0, identical 81-column all-TE LightGBM except max_bin:

- max_bin=1024: **0.946853**
- max_bin=16384: **0.946867**
- delta: **+0.000014**

Decision: **reject as neutral**. The gain is far below the experiment noise floor and does not justify a full CV run.

## D. Sparse exact-value logistic regression

Hypothesis: the reported ~0.94640 logistic model might be a sparse additive lookup model over exact repeated income/commute values rather than smoothed target encodings.

Representation: one-hot exact income and commute, several income/commute resolutions, digits and low-cardinality raw variables, plus the recovered core linear mechanism variables.

Frozen fold 0:

- L2 logistic, C=0.1: **0.945956**
- L2 logistic, C=1.0: **0.945483**

Decision: **reject**. This does not reproduce the reported strong logistic regime.

## E. 20-fold confirmation

A 20-fold version of the experiment-015 LightGBM was started because independent paired testing reports a small but real gain from 10 to 20 folds. Before the local execution environment interrupted the long run, the completed folds matched the independent implementation extremely closely:

- fold 0: ours **0.946312**, reference **0.946302**
- fold 1: ours **0.947537**, reference **0.947526**

This confirms the 20-fold implementation direction, but the run is **not complete** and no 20-fold candidate is claimed here.

## F. Conservative cross-generation hedges

Experiment 011 already showed that the older high-resolution additive model can add useful diversity: a 20% rank weight improved engineered XGB from 0.94610 to 0.94615 public. Its rank correlation to the new experiment-015 source-allTE prediction is 0.995318, almost identical to its correlation with the older XGB family.

Because experiment 015 is locally stronger than the old XGB, use less secondary weight rather than copying the old 80/20 choice. Two deterministic secondary files were generated from our own predictions only:

- 90% source-allTE / 10% high-resolution additive
- 85% source-allTE / 15% high-resolution additive

Both are rank blends. Exact weighted-rank ties are resolved lexicographically by the continuous source-allTE prediction, then the continuous high-resolution prediction, while preserving every non-tied primary ordering.

Decision: treat these as **secondary submission hedges only**. The standalone experiment-015 model remains the validation-backed primary candidate because aligned OOF for the older public-score models is unavailable.

## Current recommendation

1. Submit `candidate_source_allte_k10_v1.csv` first if it has not already been scored.
2. With attempts available, the **90/10 source-allTE/high-res lexicographic rank blend** is the next defensible hedge.
3. Do not spend attempts on the additive-XGB, max-bin, or sparse-logistic branches above; they failed controlled local checks.
