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

The first submitted baseline scored **0.94168** publicly against **0.941759** OOF. That 0.000079
gap is small enough that I am keeping the split fixed rather than rebuilding validation around the
leaderboard.

The current candidate changes the shape of the model rather than adding a pile of features:
LightGBM gets a much larger numeric bin budget and each tree branch is restricted to one feature.

| | AUC |
| --- | ---: |
| fold 1 | 0.944489 |
| fold 2 | 0.945581 |
| fold 3 | 0.945444 |
| mean | **0.945171** |
| OOF | **0.945165** |
| public | pending |

That is **+0.003406 OOF** over the submitted baseline on exactly the same folds. No target encoding,
external data, pseudo-labels, or public-score tuning is involved in this run.

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
- [`004 - high-resolution additive`](experiments/004-high-resolution-additive.md): **0.945165 OOF**, current candidate

The jump in 004 is large enough to treat as a real change. The next branch of work is fold-safe
frequency and target encoding, but only after the unchanged 004 submission gets an external score.

## Data

Competition data is not committed to this repository. `data/`, generated submissions, results,
and model artifacts are ignored by git.

The first [`data audit`](docs/data-audit.md) found no missing cells or duplicate rows and very small
train/test drift. The target is positive for 17.4645% of training rows.

Competition: [Predicting Electric Vehicle Purchases](https://www.kaggle.com/competitions/playground-series-s6e9)

## Status

One public score is recorded and tracks local validation closely. Experiment 004 is now the next
submission candidate; its public AUC stays `pending` until Kaggle actually scores the file.

MIT © James Kim
