from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

TARGET = "Will_Buy_EV"


def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(data_dir / "train.csv")
    test = pd.read_csv(data_dir / "test.csv")
    sample = pd.read_csv(data_dir / "sample_submission.csv")

    features = [c for c in train.columns if c != TARGET]
    if features != list(test.columns):
        raise ValueError("train/test feature columns differ")
    if list(sample.columns) != ["id", TARGET] or not sample["id"].equals(test["id"]):
        raise ValueError("sample submission does not match test ids")

    return train, test, sample


def prepare(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, list[str]]:
    y = train[TARGET].eq("Yes").astype("int8")
    x = train.drop(columns=[TARGET, "id"]).copy()
    x_test = test.drop(columns=["id"]).copy()

    categorical = x.select_dtypes(include=["object", "bool"]).columns.tolist()
    for column in categorical:
        values = pd.concat([x[column], x_test[column]], ignore_index=True).astype(str)
        categories = pd.Index(values.unique())
        x[column] = pd.Categorical(x[column].astype(str), categories=categories)
        x_test[column] = pd.Categorical(x_test[column].astype(str), categories=categories)

    return x, x_test, y, categorical


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--folds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train, test, sample = load_data(args.data_dir)
    x, x_test, y, categorical = prepare(train, test)

    # One feature per branch makes this an additive boosted model. Combined with a much larger
    # bin budget, it can model fine-grained one-column structure without spending tree depth on
    # interactions that did not help the first baseline.
    interaction_constraints = [[i] for i in range(x.shape[1])]
    cv = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=args.seed)

    oof = np.zeros(len(x), dtype=float)
    prediction = np.zeros(len(x_test), dtype=float)
    fold_scores: list[float] = []
    fold_seconds: list[float] = []
    best_iterations: list[int] = []

    for fold, (train_idx, valid_idx) in enumerate(cv.split(x, y), start=1):
        started = time.perf_counter()
        model = lgb.LGBMClassifier(
            objective="binary",
            n_estimators=900,
            learning_rate=0.06,
            num_leaves=255,
            min_child_samples=10,
            feature_fraction=1.0,
            bagging_fraction=0.95,
            bagging_freq=1,
            reg_lambda=2.0,
            max_bin=16384,
            interaction_constraints=interaction_constraints,
            random_state=args.seed + fold,
            n_jobs=-1,
            verbosity=-1,
        )
        model.fit(
            x.iloc[train_idx],
            y.iloc[train_idx],
            eval_set=[(x.iloc[valid_idx], y.iloc[valid_idx])],
            eval_metric="auc",
            categorical_feature=categorical,
            callbacks=[
                lgb.early_stopping(60, verbose=False),
                lgb.log_evaluation(0),
            ],
        )

        valid_prediction = model.predict_proba(
            x.iloc[valid_idx], num_iteration=model.best_iteration_
        )[:, 1]
        oof[valid_idx] = valid_prediction
        prediction += (
            model.predict_proba(x_test, num_iteration=model.best_iteration_)[:, 1] / args.folds
        )

        score = float(roc_auc_score(y.iloc[valid_idx], valid_prediction))
        elapsed = time.perf_counter() - started
        fold_scores.append(score)
        fold_seconds.append(float(elapsed))
        best_iterations.append(int(model.best_iteration_))
        print(f"fold {fold}: {score:.6f}  best_iteration={model.best_iteration_}  {elapsed:.1f}s")

    mean_auc = float(np.mean(fold_scores))
    std_auc = float(np.std(fold_scores))
    oof_auc = float(roc_auc_score(y, oof))
    print(f"mean AUC: {mean_auc:.6f} +/- {std_auc:.6f}")
    print(f"OOF AUC:  {oof_auc:.6f}")

    Path("submissions").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    submission = sample.copy()
    submission[TARGET] = prediction
    submission.to_csv("submissions/highres_additive.csv", index=False)

    metrics = {
        "model": "LightGBM high-resolution additive",
        "folds": args.folds,
        "seed": args.seed,
        "fold_auc": fold_scores,
        "mean_auc": mean_auc,
        "std_auc": std_auc,
        "oof_auc": oof_auc,
        "best_iterations": best_iterations,
        "fold_seconds": fold_seconds,
        "max_bin": 16384,
        "num_leaves": 255,
        "min_child_samples": 10,
        "interaction_constraints": "one feature per branch",
    }
    Path("results/highres_additive.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
