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
to **0.94548**, the engineered sweep pushed both single models above 0.946, and the current best is
a fixed diversity-aware rank blend:

| experiment | model | public AUC |
| --- | --- | ---: |
| 003 | small LightGBM baseline | 0.94168 |
| 004 | high-resolution additive LightGBM | 0.94548 |
| 010 | engineered LightGBM | 0.94607 |
| 010 | engineered XGBoost | 0.94610 |
| 011 | 80% XGBoost / 20% high-resolution rank blend | 0.94615 |
| 011 | 70% XGBoost / 30% high-resolution rank blend | 0.94615 |
| 013 | diversity rank blend | **0.94617** |
| 014 | lexicographic tie-break | **0.94617** |

Experiment 013 combines XGBoost, LightGBM, the older high-resolution additive model, and a small
fold-safe target-encoding logistic branch. Experiment 014 removed all 4,811 exact ties from that
ranking without changing any already-ordered pair, but the displayed public score stayed unchanged.
That closes both nearby blend-weight search and tie-breaking as useful next steps.

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
- [`011 - cross-generation rank blend`](experiments/011-cross-generation-rank-blend.md): **0.94615 public** at both predetermined weights
- [`012 - CatBoost native`](experiments/012-catboost-native.md): prepared as a distinct-model branch, not yet measured
- [`013 - diversity rank blend`](experiments/013-diversity-rank-blend.md): **0.94617 public**
- [`014 - lexicographic tie-break`](experiments/014-lexicographic-tiebreak.md): **0.94617 public**, no gain

The important part of the sequence is that failed or slow ideas stay visible. The last two results
also show the difference between a real new signal and leaderboard micro-tuning: adding a small
diverse model moved the score; resolving rank ties did not.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, results,
and model artifacts are ignored by git.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small
train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Status

**0.94617** is the current public best. With the remaining submission budget limited, the next slot
is reserved for a materially stronger external or independently validated ranking, not another local
weight or tie experiment.

MIT © James Kim
