# ev-purchase-prediction

Predicting whether someone will buy an EV, with every model compared on the same folds.

This is my entry for Kaggle's **Playground Series - Season 6, Episode 9**. The target is
`Will_Buy_EV`, and submissions are scored by ROC AUC.

## The rule

**A change does not count as an improvement until it beats the same validation setup.**

The public leaderboard is useful as a check, but I do not want to tune the project by chasing
one public number. Every model and feature change goes through the same validation scheme first.
If CV and the leaderboard disagree, that disagreement is something to investigate rather than hide.

## Current result

The first submitted baseline scored **0.94168** publicly. The high-resolution additive model moved
to **0.94548**, the engineered sweep pushed both single models above 0.946, and a cross-generation
rank blend is now the public best:

| experiment | model | public AUC |
| --- | --- | ---: |
| 003 | small LightGBM baseline | 0.94168 |
| 004 | high-resolution additive LightGBM | 0.94548 |
| 010 | engineered LightGBM | 0.94607 |
| 010 | engineered XGBoost | 0.94610 |
| 011 | 80% XGBoost / 20% high-resolution rank blend | **0.94615** |

The blend gain over XGBoost is only **+0.00005**. That is enough to keep the result, but not enough
to justify searching arbitrary weights against the public leaderboard. Experiment 011 therefore has
one remaining predetermined point, 70/30, and stops there.

## Run it

Put Kaggle's `train.csv`, `test.csv`, and `sample_submission.csv` under `data/`, then:

```bash
python -m venv .venv
# activate the environment for your shell
pip install -r requirements.txt
python scripts/train_highres_additive.py
```

For the original control instead:

```bash
python scripts/train_baseline.py
```

The heavier engineered sweep is run as a Kaggle notebook rather than pretending it is a cheap
local baseline. Generated submissions, metrics and model artifacts are ignored by git.

## Experiments

Every meaningful run gets a short record under [`experiments/`](experiments/). Failed runs stay in
the log.

- [`001 - CatBoost baseline`](experiments/001-catboost-baseline.md): stopped on runtime, no score
- [`002 - LightGBM baseline`](experiments/002-lightgbm-baseline.md): 0.941684 mean CV
- [`003 - smaller trees`](experiments/003-smaller-trees.md): 0.941759 OOF, **0.94168 public**
- [`004 - high-resolution additive`](experiments/004-high-resolution-additive.md): **0.945165 OOF, 0.94548 public**
- [`005 - frequency features`](experiments/005-frequency-features.md): stopped on runtime
- [`006 - focused frequency`](experiments/006-focused-frequency.md): 0.945100 OOF, reverted
- [`007 - cross-fit target buckets`](experiments/007-crossfit-target-buckets.md): first fold regressed, stopped
- [`008 - exact-value categories`](experiments/008-exact-value-categories.md): first fold regressed, stopped
- [`009 - decimal digits`](experiments/009-decimal-digits.md): stopped on runtime
- [`010 - two-model candidate sweep`](experiments/010-two-model-candidate-sweep.md): **0.94607 LGB / 0.94610 XGB public**
- [`011 - cross-generation rank blend`](experiments/011-cross-generation-rank-blend.md): **0.94615 public** at 80/20

The important part of the sequence is that failed or slow feature ideas stay visible. Experiment
010 did not replace that history with one giant final pipeline; it tested a larger feature set in a
separate, measured branch and produced two independently scored submissions. Experiment 011 then
used a less redundant older model for a small ensemble gain rather than blending two nearly identical
rankings.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, results,
and model artifacts are ignored by git.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small
train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Status

**0.94615** is the current public best. The remaining point in experiment 011 is the already-fixed
70% XGBoost / 30% high-resolution blend. After that result, the next improvement attempt should
come from a genuinely different model or feature representation rather than more public weight search.

MIT © James Kim
