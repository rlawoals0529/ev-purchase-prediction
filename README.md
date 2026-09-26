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

The current candidate is a small LightGBM model on the raw competition features, with `id`
excluded.

| | AUC |
| --- | ---: |
| fold 1 | 0.940837 |
| fold 2 | 0.942491 |
| fold 3 | 0.941993 |
| mean | **0.941773** |
| OOF | **0.941759** |

Three folds fit in **48.6 seconds** in the run that produced these numbers. The fold spread is
small, and reducing the trees from 31 leaves to 15 improved all three folds.

The first CatBoost attempt is still in the history. It ran for four minutes without completing a
fold in the environment I was using, which made it a bad control for fast iteration. I kept the
code and the failed experiment rather than rewriting the story around the model that worked.

## Run it

Put Kaggle's `train.csv`, `test.csv`, and `sample_submission.csv` under `data/`, then:

```bash
python -m venv .venv
# activate the environment for your shell
pip install -r requirements.txt
python scripts/train_baseline.py
```

The script checks the train/test columns and submission ids before fitting anything. It writes the
fold scores to `results/lightgbm_baseline.json` and the averaged test predictions to
`submissions/lightgbm_baseline.csv`.

## Experiments

Every meaningful run gets a short record under [`experiments/`](experiments/). Failed runs stay in
the log.

- [`001 - CatBoost baseline`](experiments/001-catboost-baseline.md): stopped on runtime, no score
- [`002 - LightGBM baseline`](experiments/002-lightgbm-baseline.md): 0.941684 mean CV
- [`003 - smaller trees`](experiments/003-smaller-trees.md): 0.941773 mean CV, current candidate

I also tested a histogram gradient boosting model and simple blends. The best three-model OOF blend
was only about 0.000054 above the current single model and the blend weights were chosen on those
same OOF predictions, so I am not adding that complexity yet.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, results,
and model artifacts are ignored by git.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small
train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Status

Local validation is measured. The next number that matters is the public Kaggle AUC from the current
candidate; it stays `pending` in the experiment log until the file is actually submitted.

MIT © James Kim
