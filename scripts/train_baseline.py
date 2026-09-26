from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

TARGET = "Will_Buy_EV"


def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(data_dir / "train.csv")
    test = pd.read_csv(data_dir / "test.csv")

    if TARGET not in train.columns:
        raise ValueError(f"{TARGET!r} is missing from train.csv")
    if TARGET in test.columns:
        raise ValueError(f"{TARGET!r} should not be present in test.csv")

    train_features = [c for c in train.columns if c != TARGET]
    if train_features != list(test.columns):
        raise ValueError("train/test feature columns differ or are in a different order")

    return train, test


def prepare_features(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series | None, list[str]]:
    y = train[TARGET].copy()
    x = train.drop(columns=[TARGET]).copy()
    x_test = test.copy()

    ids = None
    if "id" in x.columns:
        ids = x_test["id"].copy()
        x = x.drop(columns=["id"])
        x_test = x_test.drop(columns=["id"])

    categorical = [
        c
        for c in x.columns
        if pd.api.types.is_object_dtype(x[c])
        or isinstance(x[c].dtype, pd.CategoricalDtype)
        or pd.api.types.is_bool_dtype(x[c])
    ]

    for column in categorical:
        x[column] = x[column].fillna("__MISSING__").astype(str)
        x_test[column] = x_test[column].fillna("__MISSING__").astype(str)

    return x, x_test, y, ids, categorical


def train_cv(
    x: pd.DataFrame,
    x_test: pd.DataFrame,
    y: pd.Series,
    categorical: list[str],
    folds: int,
    seed: int,
) -> tuple[np.ndarray, list[float], list[int]]:
    splitter = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    test_prediction = np.zeros(len(x_test), dtype=float)
    fold_scores: list[float] = []
    best_iterations: list[int] = []

    for fold, (train_idx, valid_idx) in enumerate(splitter.split(x, y), start=1):
        x_train = x.iloc[train_idx]
        y_train = y.iloc[train_idx]
        x_valid = x.iloc[valid_idx]
        y_valid = y.iloc[valid_idx]

        model = CatBoostClassifier(
            iterations=1500,
            learning_rate=0.05,
            depth=7,
            loss_function="Logloss",
            eval_metric="AUC",
            l2_leaf_reg=5.0,
            random_seed=seed + fold,
            allow_writing_files=False,
            verbose=False,
            thread_count=-1,
        )
        model.fit(
            x_train,
            y_train,
            cat_features=categorical,
            eval_set=(x_valid, y_valid),
            early_stopping_rounds=100,
            verbose=False,
        )

        valid_prediction = model.predict_proba(x_valid)[:, 1]
        score = roc_auc_score(y_valid, valid_prediction)
        fold_scores.append(float(score))
        best_iterations.append(int(model.get_best_iteration()))

        test_prediction += model.predict_proba(x_test)[:, 1] / folds
        print(f"fold {fold}: {score:.6f}  best_iteration={model.get_best_iteration()}")

    return test_prediction, fold_scores, best_iterations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train, test = load_data(args.data_dir)
    x, x_test, y, ids, categorical = prepare_features(train, test)

    prediction, fold_scores, best_iterations = train_cv(
        x=x,
        x_test=x_test,
        y=y,
        categorical=categorical,
        folds=args.folds,
        seed=args.seed,
    )

    mean_score = float(np.mean(fold_scores))
    std_score = float(np.std(fold_scores))
    print(f"mean AUC: {mean_score:.6f} +/- {std_score:.6f}")

    submission_dir = Path("submissions")
    result_dir = Path("results")
    submission_dir.mkdir(exist_ok=True)
    result_dir.mkdir(exist_ok=True)

    submission = pd.DataFrame({TARGET: prediction})
    if ids is not None:
        submission.insert(0, "id", ids.to_numpy())
    submission.to_csv(submission_dir / "catboost_baseline.csv", index=False)

    metrics = {
        "model": "CatBoostClassifier",
        "folds": args.folds,
        "seed": args.seed,
        "features": len(x.columns),
        "categorical_features": len(categorical),
        "fold_auc": fold_scores,
        "mean_auc": mean_score,
        "std_auc": std_score,
        "best_iterations": best_iterations,
    }
    (result_dir / "catboost_baseline.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
