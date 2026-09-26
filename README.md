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

## Current state

The repository is set up before the first baseline run. I am intentionally not putting a score
here until it has been reproduced from a committed pipeline.

The first pass is deliberately boring:

1. load the competition data without changing row order or ids;
2. establish a stratified cross-validation baseline;
3. log fold-level ROC AUC, not only the mean;
4. train one strong tabular model with minimal feature work;
5. generate a submission from exactly that pipeline;
6. only then start feature and ensemble experiments.

## Experiments

Every meaningful run gets a short record under [`experiments/`](experiments/). A run records the
hypothesis, the exact change, fold scores, public score when submitted, and whether the change stays.
Failed runs stay in the log.

## Data

Competition data is not committed to this repository. Put Kaggle's files under `data/` locally;
that directory is ignored by git.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## What I am measuring

The mean CV score matters, but it is not the only number worth keeping. I also want the spread
across folds, training time, feature count, and the gap between local validation and the public
leaderboard. A tiny gain that doubles complexity is not automatically a better model.

## Status

Baseline next. Results will replace this section once the first run is reproducible.
