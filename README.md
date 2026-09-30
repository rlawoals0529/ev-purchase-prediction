# EV Purchase Prediction

My entry for Kaggle's **Playground Series - Season 6, Episode 9**. The task is to predict `Will_Buy_EV`, scored by ROC AUC.

I kept this repo as the experiment trail, not just the final submission. Model changes had to survive aligned validation before I treated them as improvements.

## Final result

The first submitted LightGBM baseline scored **0.94168** publicly. The final source-aware ensemble reached **0.94636**.

| stage | model | public AUC |
| --- | --- | ---: |
| baseline | small LightGBM | 0.94168 |
| high-resolution | additive LightGBM | 0.94548 |
| engineered sweep | LightGBM | 0.94607 |
| engineered sweep | XGBoost | 0.94610 |
| cross-generation blend | XGBoost + high-resolution | 0.94615 |
| diversity blend | multi-model rank blend | 0.94617 |
| source-aware k10 | source-allTE + high-resolution | 0.94634 |
| source-aware k20 | 90% source-allTE / 10% high-resolution | **0.94636** |
| source-aware k20 | 87.5% source-allTE / 12.5% high-resolution | **0.94636** |
| tie-only multimodel reuse | k20 blend + multimodel tie-break | **0.94636** |
| hard-edge stress test | k20 blend + deterministic edge rules | **0.94636** |

Several different fold counts, blend weights, tie-breakers, and hard-edge tweaks all came back at **0.94636**. At that point, moving the ranking around without a new signal stopped being useful.

## Approach

The final family came down to three things:

1. **Generator-aware source support**
   - reconstructed target-free support from the verified `RandomState(101)` source process;
   - frequency, novelty, lift, and distance-to-source features for repeated income and commute values.

2. **Leak-safe nested target encoding**
   - exact and bucketed income/commute encodings;
   - low-cardinality raw feature encodings at multiple smoothing levels;
   - all target encodings are cross-fit inside each outer fold.

3. **Model and generation diversity**
   - shallow LightGBM as the strongest core;
   - a high-resolution additive model retained because its ranking remained usefully different;
   - XGBoost and CatBoost were tested as aligned companion models, but their global public blend did not beat the final LightGBM-based family.

Source-allTE moved from **0.9462042 OOF with 10 folds** to about **0.9462612 OOF with 20 folds**. The public score stayed at 0.94636. I kept both numbers because the small local gain did not translate into a visible leaderboard gain.

## Experiment rule

**A change does not count as an improvement just because it looks clever or moves one public number.**

I used frozen or aligned validation wherever possible, and I left the failed, neutral, and slow experiments in the repo. Deleting them after seeing the final score would make the path look cleaner than it was.

That includes rejected branches such as:

- strict additive interaction constraints;
- exact-income residual corrections on top of source-allTE;
- ID/modulo/generation-order features;
- global CatBoost/XGBoost ensemble weighting;
- multimodel tie-breaking;
- deterministic income-boundary hard edges;
- repeated micro-adjustments to blend weights.

## Reproduce the core model

Put Kaggle's `train.csv`, `test.csv`, and `sample_submission.csv` under `data/`, then create an environment and install the requirements.

```bash
python -m venv .venv
# activate the environment for your shell
pip install -r requirements.txt
```

Original baseline:

```bash
python scripts/train_baseline.py
```

High-resolution additive branch:

```bash
python scripts/train_highres_additive.py
```

Source-support + nested-TE model, one outer fold at a time:

```bash
python scripts/train_source_allte.py \
  --data data \
  --output artifacts/source_allte_k20 \
  --fold 0 \
  --folds 20 \
  --seed-te 0 \
  --seed-model 0
```

The heavier sweeps were run fold-by-fold because the full training matrix is memory-intensive on a small CPU environment. Generated submissions, datasets, metrics, and model artifacts are intentionally ignored by git.

## Experiments

Every meaningful run is recorded under [`experiments/`](experiments/). Highlights from the sequence:

- [`003 - smaller trees`](experiments/003-smaller-trees.md): **0.94168 public**
- [`004 - high-resolution additive`](experiments/004-high-resolution-additive.md): **0.945165 OOF, 0.94548 public**
- [`010 - two-model candidate sweep`](experiments/010-two-model-candidate-sweep.md): **0.94607 LGB / 0.94610 XGB public**
- [`011 - cross-generation rank blend`](experiments/011-cross-generation-rank-blend.md): **0.94615 public**
- [`013 - diversity rank blend`](experiments/013-diversity-rank-blend.md): **0.94617 public**
- [`015 - source support + all-column TE`](experiments/015-source-support-allte.md): generator-aware feature family and 10-fold source-allTE model
- [`016 - post source-allTE screens`](experiments/016-post-source-allte-screens.md): additive, XGBoost-constraint, histogram, and sparse-logistic screens
- [`017 - k20 resume and hedges`](experiments/017-k20-resume-and-hedges.md): higher-fold continuation and conservative own-model blends
- [`018 - complete k20 source-allTE`](experiments/018-complete-k20-source-allte.md): **~0.9462612 pooled OOF**
- [`019 - public 0.94636 and k20 blend grid`](experiments/019-public-94636-and-k20-blend-grid.md): first **0.94636** family
- [`020 - aligned multimodel + CatBoost bag`](experiments/020-aligned-multimodel-catboost-bag.md): aligned OOF ensemble improved locally, but not publicly
- [`021 - multimodel public reject + tie-break`](experiments/021-multimodel-public-reject-and-tiebreak.md): **0.94633** global multimodel; tie-only reuse returned **0.94636**
- [`022 - forensic generator audit`](experiments/022-extreme-forensic-generator-audit.md): deeper generator-structure and boundary analysis
- [`023 - hard-edge public neutral`](experiments/023-hardedge-public-neutral-and-next-pivot.md): hard-edge candidate returned **0.94636**
- [`024 - replication, constraints, and ID audit`](experiments/024-replication-constraints-id-audit.md): rejected residual correction, strict additive transfer, and ID/order leakage
- [`025 - final public summary`](experiments/025-final-public-summary.md): final leaderboard and project conclusions

## Data and ownership

Competition data is not committed to this repository. `data/`, generated submissions, results, and model artifacts are ignored by git.

All submitted predictions were produced from models trained in this project or deterministic combinations of those predictions. Public notebooks, repositories, and Kaggle discussions were used to study methodology and reproduce ideas, **not** as sources of third-party prediction CSVs.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Known implementation note

The current source-allTE script abbreviates target-encoding feature names with the first six characters of the source column. That causes the home/work charging-station TE names to collide, leaving 79 features instead of the intended 81 in that implementation. The issue was discovered late; a corrected full cross-validation run was not completed, so it is documented rather than claimed as an improvement.

## Status

**Final public best: 0.94636 ROC AUC.**

I am treating this run as finished. I would only reopen it for a genuinely different model family or a new signal that survives validation, not another nearby blend or post-processing tweak.

MIT © James Kim
