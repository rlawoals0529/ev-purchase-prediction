from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, early_stopping, log_evaluation
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

TARGET = "Will_Buy_EV"


def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(data_dir / "train.csv")
    test = pd.read_csv(data_dir / "test.csv")
    sample = pd.read_csv(data_dir / "sample_submission.csv")

    if TARGET not in train.columns:
        raise ValueError(f"{TARGET!r} is missing from train.csv")
    if TARGET in test.columns:
        raise ValueError(f"{TARGET!r} should not be present in test.csv")

    train_features = [c for c in train.columns if c != TARGET]
    if train_features != list(test.columns):
        raise ValueError("train/test feature columns differ or are in a different order")
    if list(sample.columns) != ["id", TARGET]:
        raise ValueError("sample_submission.csv does not have the expected columns")
    if not sample["id"].equals(test["id"]):
        raise ValueError("sample submission ids do not match test.csv")

    return train, test, sample


def prepare_features(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, list[str]]:
    y = train[TARGET].eq("Yes").astype("int8")
    x = train.drop(columns=[TARGET, "id"]).copy()
    x_test = test.drop(columns=["id"]).copy()

    categorical = x.select_dtypes(include=["object", "bool"]).columns.tolist()

    # LightGBM expects train and test to use the same category codes. Build each
    # category vocabulary once from the union, then reuse it on both frames.
    for column in categorical:
        categories = pd.Index(
            pd.concat([x[column], x_test[column]], ignore_index=True).astype(str).unique()
        )
        x[column] = pd.Categorical(x[column].astype(str), categories=categories)
        x_test[column] = pd.Categorical(x_test[column].astype(str), categories=categories)

    return x, x_test, y, categorical


def train_cv(
    x: pd.DataFrame,
    x_test: pd.DataFrame,
    y: pd.Series,
    categorical: list[str],
    folds: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, list[float], list[int], list[float], list[np.ndarray]]:
    splitter = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    out_of_fold = np.zeros(len(x), dtype=float)
    test_prediction = np.zeros(len(x_test), dtype=float)
    fold_scores: list[float] = []
    best_iterations: list[int] = []
    fold_seconds: list[float] = []
    importances: list[np.ndarray] = []

    for fold, (train_idx, valid_idx) in enumerate(splitter.split(x, y), start=1):
        started = time.perf_counter()
        model = LGBMClassifier(
            objective="binary",
            n_estimators=700,
            learning_rate=0.08,
            num_leaves=15,
            min_child_samples=100,
            feature_fraction=0.95,
            bagging_fraction=0.95,
            bagging_freq=1,
            reg_lambda=2.0,
            random_state=seed + fold,
            n_jobs=-1,
            verbosity=-1,
        )
        model.fit(
            x.iloc[train_idx],
            y.iloc[train_idx],
            eval_set=[(x.iloc[valid_idx], y.iloc[valid_idx])],
            eval_metric="auc",
            categorical_feature=categorical,
            callbacks=[early_stopping(45, verbose=False), log_evaluation(0)],
        )

        valid_prediction = model.predict_proba(
            x.iloc[valid_idx], num_iteration=model.best_iteration_
        )[:, 1]
        out_of_fold[valid_idx] = valid_prediction
        test_prediction += (
            model.predict_proba(x_test, num_iteration=model.best_iteration_)[:, 1] / folds
        )

        score = float(roc_auc_score(y.iloc[valid_idx], valid_prediction))
        elapsed = time.perf_counter() - started
        fold_scores.append(score)
        best_iterations.append(int(model.best_iteration_))
        fold_seconds.append(float(elapsed))
        importances.append(model.feature_importances_.copy())

        print(
            f"fold {fold}: {score:.6f}  "
            f"best_iteration={model.best_iteration_}  {elapsed:.1f}s"
        )

    return (
        out_of_fold,
        test_prediction,
        fold_scores,
        best_iterations,
        fold_seconds,
        importances,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--folds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train, test, sample = load_data(args.data_dir)
    x, x_test, y, categorical = prepare_features(train, test)

    (
        out_of_fold,
        prediction,
        fold_scores,
        best_iterations,
        fold_seconds,
        importances,
    ) = train_cv(
        x=x,
        x_test=x_test,
        y=y,
        categorical=categorical,
        folds=args.folds,
        seed=args.seed,
    )

    mean_score = float(np.mean(fold_scores))
    std_score = float(np.std(fold_scores))
    oof_score = float(roc_auc_score(y, out_of_fold))
    print(f"mean AUC: {mean_score:.6f} +/- {std_score:.6f}")
    print(f"OOF AUC:  {oof_score:.6f}")

    submission_dir = Path("submissions")
    result_dir = Path("results")
    submission_dir.mkdir(exist_ok=True)
    result_dir.mkdir(exist_ok=True)

    submission = sample.copy()
    submission[TARGET] = prediction
    submission.to_csv(submission_dir / "lightgbm_baseline.csv", index=False)

    mean_importance = np.mean(np.vstack(importances), axis=0)
    feature_importance = sorted(
        zip(x.columns.tolist(), mean_importance.tolist()),
        key=lambda item: item[1],
        reverse=True,
    )
    metrics = {
        "model": "LightGBM",
        "folds": args.folds,
        "seed": args.seed,
        "features": len(x.columns),
        "categorical_features": categorical,
        "fold_auc": fold_scores,
        "mean_auc": mean_score,
        "std_auc": std_score,
        "oof_auc": oof_score,
        "best_iterations": best_iterations,
        "fold_seconds": fold_seconds,
        "total_fit_seconds": float(sum(fold_seconds)),
        "feature_importance": feature_importance,
    }
    (result_dir / "lightgbm_baseline.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
