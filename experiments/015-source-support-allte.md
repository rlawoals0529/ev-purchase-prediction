# 015 - Source-support + multi-resolution all-TE LightGBM

Date: 2026-09-28

## Goal

Move beyond the saturated blend/tie-break family by modeling the synthetic generator structure directly, while keeping all predictions original to this repository.

Public work was used only for methodology/ablation guidance. No external prediction CSV was imported or blended.

## Research basis

Two independent public projects were especially useful:

- `congmnguyen/tabular-ml-lab`: verified the original-source RNG sequence and found gains from low-smoothing target encoding / shallow boosting.
- `happyc0der/kaggle-s6e9-ev-purchases`: 190+ measured experiments; strongest reproducible recipe used original-source support statistics, nested multi-resolution income/commute TE, TE on raw/digit features, and shallow heavily column-subsampled trees.

The 10,000-row source covariates were reconstructed locally from the documented `np.random.RandomState(101)` draw sequence. Source labels were not reconstructed or used.

## Local data observations

Competition train has 668,665 rows but only 13,214 distinct `Annual_Income_USD` values and 805 distinct `Daily_Commute_km` values. Examples:

- income = 30000 appears 61,605 times
- income = 86095 appears 1,082 times
- commute = 5.0 appears 144,280 times

Leak-safe five-fold univariate TE screens:

- exact income, smoothing 2: **0.712189 OOF AUC**
- exact income, smoothing 20: **0.710591**
- income bin 100, smoothing 2: **0.703771**
- income modulo 1000, smoothing 2: **0.618415**
- commute exact, smoothing 2: **0.550948**

This supports treating repeated generator identities as signal rather than ordinary continuous values.

## Failed/neutral screen

A first 148-feature LightGBM with exact/binned/remainder keys, nested smoothing 2/20 TE and transductive frequencies reached only:

- fold 0 AUC: **0.945077002**
- best iteration: 627

Decision: reject this formulation. It underused source-support features and the stronger multi-resolution all-column TE recipe.

## Final tested recipe

Ten outer stratified folds, seed 0. For each outer fold:

- regenerate the original source income/commute support from RandomState(101)
- per-value train+test frequency
- original-support count
- frequency lift vs. source
- novelty flag
- nearest-source signed distance
- frequency rank
- income/commute digit features
- nested 5-fold TE, smoothing 3 for:
  - income exact
  - commute exact
  - income bins 100 / 500 / 2000
  - commute bins 1 / 5
- nested TE at smoothing 10 and 100 for every raw/digit feature plus income bin 1000
- LightGBM depth 5 / 32 leaves / feature_fraction 0.30 / bagging 0.80 / max_bin 1024

The source-support features are target-free. All target encodings for outer-training rows are inner-fold OOF, and outer-validation labels never enter their encoding maps.

## Measured 10-fold results

| Fold | AUC | Best iteration |
|---:|---:|---:|
| 0 | 0.946859646 | 1033 |
| 1 | 0.946495414 | 1363 |
| 2 | 0.946256849 | 1224 |
| 3 | 0.947262973 | 1237 |
| 4 | 0.947074166 | 1324 |
| 5 | 0.946531900 | 1411 |
| 6 | 0.944856970 | 1968 |
| 7 | 0.944644893 | 1365 |
| 8 | 0.945792469 | 1646 |
| 9 | 0.946340341 | 1378 |

- **Pooled OOF AUC: 0.946204209**
- mean fold AUC: **0.946211562**
- fold std: **0.000832850**

The pooled result independently reproduces the public methodology reference (~0.946216 OOF) to about 0.00001.

## Test-prediction diversity

Spearman rank correlation of this model to existing repo candidates:

- engineered XGB: 0.998123
- engineered LGB: 0.997731
- high-resolution additive LGB: 0.995318
- best diversity candidate: 0.998381
- 70/30 XGB/high-res: 0.998272
- hard-edge candidate: 0.998076

The model is meaningfully different from the current family, especially from the older high-resolution model, but no new blend was selected because we do not have aligned OOF predictions for the existing public-score candidates. The next submission should therefore be the standalone validated model rather than an unvalidated weight tweak.

## Output

Generated locally:

`candidate_source_allte_k10_v1.csv`

286,571 test rows, `id` order preserved, prediction range `[5.187e-06, 0.999690]`.

## Decision

**Promote as the next standalone Kaggle submission.**

This is structurally different from experiments 010-014 and has substantially stronger validation evidence than another rank-blend/tie-break variation.
