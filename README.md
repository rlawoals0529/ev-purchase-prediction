# ev-purchase-prediction

Predicting whether someone will buy an EV, with every model compared on the same folds.

This is my entry for Kaggle's **Playground Series - Season 6, Episode 9**. The target is
`Will_Buy_EV`, and submissions are scored by ROC AUC.

## The rule

**A change does not count as an improvement until it beats the same validation setup.**

The public leaderboard is useful as a check, but I do not want to tune the project by chasing
one public number. Every model, feature change and ensemble goes through the same cross-validation
scheme first. If CV and the leaderboard disagree, that disagreement is something to investigate,
not something to hide.

## Current baseline

[`scripts/train_baseline.py`](scripts/train_baseline.py) is the first control: five-fold stratified
cross-validation with CatBoost, raw competition features, `id` excluded from training, categorical
columns passed directly to the model, and early stopping inside each fold.

The script writes the fold scores to `results/catboost_baseline.json` and the averaged test
prediction to `submissions/catboost_baseline.csv`. I am intentionally not putting a score in this
README until that exact committed pipeline has produced it.

## Run it

Put Kaggle's `train.csv` and `test.csv` under `data/`, then:

```bash
python -m venv .venv
# activate the environment for your shell
pip install -r requirements.txt
python scripts/train_baseline.py
```

The script checks that train and test use the same feature columns before fitting anything. It
prints every fold AUC and the mean/std rather than only the final average.

## Experiments

Every meaningful run gets a short record under [`experiments/`](experiments/). A run records the
hypothesis, the exact change, fold scores, public score when submitted, and whether the change stays.
Failed runs stay in the log.

[`001-catboost-baseline`](experiments/001-catboost-baseline.md) was written before the baseline
score is known.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, and model
artifacts are ignored by git.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## What I am measuring

The mean CV score matters, but it is not the only number worth keeping. I also want the spread
across folds, training time, feature count, and the gap between local validation and the public
leaderboard. A tiny gain that doubles complexity is not automatically a better model.

## Status

Baseline code committed. CV and public leaderboard scores are still pending and will be filled in
from the actual run, not estimated from somebody else's notebook.
