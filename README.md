# ev-purchase-prediction

Predicting whether someone will buy an EV, with every model compared on the same folds.

This is my entry for Kaggle's **Playground Series - Season 6, Episode 9**. The target is
`Will_Buy_EV`, and submissions are scored by ROC AUC.

## The rule

**A change does not count as an improvement until it beats the same validation setup.**

The public leaderboard is useful as a check, but I do not want to tune the project by chasing
one public number. Every model and feature change goes through the same stratified folds first. If
CV and the leaderboard disagree, that disagreement is something to investigate rather than hide.

## Current result

The first submitted baseline scored **0.94168** publicly against **0.941759** OOF. The
high-resolution additive model then moved to **0.94548 public** against **0.945165 OOF**.

| experiment | OOF AUC | public AUC |
| --- | ---: | ---: |
| 003 - smaller trees | 0.941759 | 0.94168 |
| 004 - high-resolution additive | **0.945165** | **0.94548** |

The second model improved OOF by **+0.003406** and the public score by **+0.00380**. Its public
score is only 0.000315 above OOF, so I am keeping the validation split fixed rather than rebuilding
it around leaderboard feedback.

Experiment 004 changes the shape of the model rather than adding a pile of features: LightGBM gets
a much larger numeric bin budget and each tree branch is restricted to one feature. No target
encoding, external data, pseudo-labels, or public-score tuning was used to get the 0.94548 result.

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

Both scripts check the train/test columns and submission ids before fitting anything. Generated
submissions, metrics and model artifacts are ignored by git.

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

The important part of the sequence is that 004 survived both local validation and the public
leaderboard, while the next several ideas did not clear the same local reference. I am leaving
those misses visible instead of turning every attempted feature into part of the final pipeline.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, results,
and model artifacts are ignored by git.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small
train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Status

**0.94548** is the current public best. The validation setup has tracked both submitted scores
closely, and none of experiments 005-009 earned another leaderboard submission. The EV track is
stable enough to pause while the other competition repos get their first measured baselines.

MIT © James Kim
