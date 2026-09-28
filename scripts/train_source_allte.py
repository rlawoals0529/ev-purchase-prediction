"""Generator-aware LightGBM for Playground S6E9.

Reconstructs target-free source support from the verified RandomState(101)
sequence and adds leak-safe nested target encodings. Public projects were used
for methodology only; no external predictions are read by this script.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

TARGET = "Will_Buy_EV"
INC = "Annual_Income_USD"
COM = "Daily_Commute_km"
CAT_MAPS = {
    "Gender": {"Male": 0, "Female": 1, "Other": 2},
    "City_Type": {"Rural": 0, "Suburban": 1, "Urban": 2},
    "Current_Car_Type": {"Hatchback": 0, "Sedan": 1, "SUV": 2, "Truck": 3},
    "Home_Charging_Possible": {"No": 0, "Yes": 1},
    "Subsidy_Available": {"No": 0, "Yes": 1},
    "Range_Anxiety_Level": {"Low": 0, "Medium": 1, "High": 2},
}
RAW = [
    "Age", INC, COM, "Number_of_Cars_Owned", "Charging_Stations_Near_Home",
    "Charging_Stations_Near_Work", "Environmental_Concern_Level",
] + list(CAT_MAPS)
OTHER = [
    "Age", "Charging_Stations_Near_Home", "Charging_Stations_Near_Work",
    "Environmental_Concern_Level", "Number_of_Cars_Owned", "Gender",
    "City_Type", "Current_Car_Type", "Home_Charging_Possible",
    "Subsidy_Available", "Range_Anxiety_Level",
]
DIG = ["inc_d1", "inc_d2", "inc_d3", "inc_d4", "com_d_dec", "com_d1"]


def encode(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col, mapping in CAT_MAPS.items():
        out[col] = out[col].map(mapping).astype("int8")
    return out


def reconstruct_source_support(n: int = 10_000) -> tuple[np.ndarray, np.ndarray]:
    """Re-run source RNG through income and commute; labels are never reconstructed."""
    rng = np.random.RandomState(101)
    rng.randint(25, 70, n)
    rng.choice(["Male", "Female", "Other"], n, p=[0.52, 0.45, 0.03])
    income = np.maximum(rng.normal(85_000, 35_000, n), 30_000).astype(int).astype(float)
    rng.choice(["Urban", "Suburban", "Rural"], n, p=[0.50, 0.35, 0.15])
    rng.choice([1, 2, 3, 4], n, p=[0.40, 0.40, 0.15, 0.05])
    rng.choice(["Sedan", "SUV", "Hatchback", "Truck"], n, p=[0.40, 0.35, 0.15, 0.10])
    commute = np.maximum(rng.normal(40, 25, n), 5).round(1)
    return income, commute


def value_stats(all_values: np.ndarray, source_values: np.ndarray, decimals: int, prefix: str) -> pd.DataFrame:
    key = np.round(all_values * 10**decimals).astype(np.int64)
    source_key = np.round(source_values * 10**decimals).astype(np.int64)
    unique, inverse, count = np.unique(key, return_inverse=True, return_counts=True)
    source_unique, source_count = np.unique(source_key, return_counts=True)

    idx = np.searchsorted(source_unique, unique)
    idx_clip = np.minimum(idx, len(source_unique) - 1)
    found = source_unique[idx_clip] == unique
    count_source = np.where(found, source_count[idx_clip], 0)

    share = count / len(key)
    share_source = count_source / len(source_key)
    lift = share / np.where(share_source > 0, share_source, 1 / len(source_key))

    unique_float = unique / 10**decimals
    source_float = source_unique / 10**decimals
    pos = np.searchsorted(source_float, unique_float)
    lo = source_float[np.clip(pos - 1, 0, len(source_float) - 1)]
    hi = source_float[np.clip(pos, 0, len(source_float) - 1)]
    d_lo, d_hi = unique_float - lo, hi - unique_float
    distance = np.where(d_lo <= d_hi, -d_lo, d_hi)
    distance[found] = 0.0
    rank = count.argsort().argsort() / len(count)

    return pd.DataFrame({
        f"{prefix}_cnt": count[inverse].astype(np.float32),
        f"{prefix}_cnt_orig": count_source[inverse].astype(np.float32),
        f"{prefix}_lift": np.log1p(lift[inverse]).astype(np.float32),
        f"{prefix}_novel": (~found)[inverse].astype(np.float32),
        f"{prefix}_dist_orig": distance[inverse].astype(np.float32),
        f"{prefix}_freqrank": rank[inverse].astype(np.float32),
    })


def static_features(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    all_raw = pd.concat([train[RAW], test[RAW]], ignore_index=True)
    source_income, source_commute = reconstruct_source_support()
    parts = [
        all_raw.reset_index(drop=True),
        value_stats(all_raw[INC].to_numpy(float), source_income, 1, "inc"),
        value_stats(all_raw[COM].to_numpy(float), source_commute, 1, "com"),
    ]
    inc10 = np.round(all_raw[INC].to_numpy() * 10).astype(np.int64)
    com10 = np.round(all_raw[COM].to_numpy() * 10).astype(np.int64)
    parts.append(pd.DataFrame({
        "inc_d_dec": inc10 % 10,
        "inc_d1": (inc10 // 10) % 10,
        "inc_d2": (inc10 // 100) % 10,
        "inc_d3": (inc10 // 1000) % 10,
        "inc_d4": (inc10 // 10000) % 10,
        "inc_mod100": ((inc10 % 1000) == 0).astype(np.int8),
        "inc_mod1000": ((inc10 % 10000) == 0).astype(np.int8),
        "inc_is_int": ((inc10 % 10) == 0).astype(np.int8),
        "inc_is_30k": (inc10 == 300000).astype(np.int8),
        "com_d_dec": com10 % 10,
        "com_d1": (com10 // 10) % 10,
        "com_is_int": ((com10 % 10) == 0).astype(np.int8),
        "com_is_5": (com10 == 50).astype(np.int8),
    }).astype(np.float32))
    return pd.concat(parts, axis=1)


def make_key(df: pd.DataFrame, col: str, binwidth: float | None = None) -> np.ndarray:
    values = df[col].to_numpy(float)
    if binwidth is not None:
        values = np.floor(values / binwidth)
        decimals = 0
    else:
        decimals = 1
    return np.round(values * 10**decimals).astype(np.int64)


def te_fit_apply(key_fit: np.ndarray, y_fit: np.ndarray, key_apply: np.ndarray, m: float, prior: float) -> np.ndarray:
    unique, inverse = np.unique(key_fit, return_inverse=True)
    sums = np.bincount(inverse, weights=y_fit, minlength=len(unique))
    count = np.bincount(inverse, minlength=len(unique)).astype(float)
    encoded = (sums + m * prior) / (count + m)
    idx = np.searchsorted(unique, key_apply)
    idx_clip = np.minimum(idx, len(unique) - 1)
    found = unique[idx_clip] == key_apply
    return np.where(found, encoded[idx_clip], prior).astype(np.float32)


def te_specs():
    specs = [
        (INC, 3, None), (COM, 3, None),
        (INC, 3, 100), (INC, 3, 500), (INC, 3, 2000),
        (COM, 3, 1), (COM, 3, 5),
    ]
    for smooth in (10, 100):
        specs += [(col, smooth, None) for col in OTHER + DIG]
        specs += [(INC, smooth, 1000)]
    return specs


def add_nested_te(static: pd.DataFrame, train: pd.DataFrame, test: pd.DataFrame, y: np.ndarray,
                  train_idx: np.ndarray, valid_idx: np.ndarray, seed: int):
    n_train = len(train)
    X_train = static.iloc[train_idx].reset_index(drop=True).copy()
    X_valid = static.iloc[valid_idx].reset_index(drop=True).copy()
    X_test = static.iloc[n_train:].reset_index(drop=True).copy()
    raw_all = pd.concat([train, test], ignore_index=True)
    inner = list(StratifiedKFold(5, shuffle=True, random_state=seed).split(np.zeros(len(train_idx)), y[train_idx]))

    for col, smooth, binwidth in te_specs():
        source = static if col in DIG else raw_all
        all_key = make_key(source, col, binwidth)
        train_key = all_key[train_idx]
        prior = float(y[train_idx].mean())
        encoded_train = np.zeros(len(train_idx), dtype=np.float32)
        for inner_train, inner_valid in inner:
            encoded_train[inner_valid] = te_fit_apply(
                train_key[inner_train], y[train_idx][inner_train], train_key[inner_valid],
                smooth, float(y[train_idx][inner_train].mean()),
            )
        name = f"te_{col[:6]}" + (f"_b{binwidth:g}" if binwidth else "") + f"_m{smooth:g}"
        X_train[name] = encoded_train
        X_valid[name] = te_fit_apply(train_key, y[train_idx], all_key[valid_idx], smooth, prior)
        X_test[name] = te_fit_apply(train_key, y[train_idx], all_key[n_train:], smooth, prior)
    return X_train, X_valid, X_test


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    parser.add_argument("--output", default="artifacts/source_allte_k10")
    parser.add_argument("--fold", type=int, required=True)
    parser.add_argument("--folds", type=int, default=10)
    parser.add_argument("--seed-te", type=int, default=0)
    parser.add_argument("--seed-model", type=int, default=0)
    args = parser.parse_args()

    data = Path(args.data)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    train = encode(pd.read_csv(data / "train.csv"))
    test = encode(pd.read_csv(data / "test.csv"))
    y = train[TARGET].eq("Yes").astype(np.int8).to_numpy()

    static = static_features(train, test)
    columns = RAW + [
        "inc_cnt", "inc_cnt_orig", "inc_lift", "inc_novel", "inc_dist_orig", "inc_freqrank",
        "com_cnt", "com_cnt_orig", "com_lift", "com_novel", "com_dist_orig", "com_freqrank",
        "inc_d_dec", "inc_d1", "inc_d2", "inc_d3", "inc_d4", "inc_mod100", "inc_mod1000",
        "inc_is_int", "inc_is_30k", "com_d_dec", "com_d1", "com_is_int", "com_is_5",
    ]
    static = static[columns]

    folds = list(StratifiedKFold(args.folds, shuffle=True, random_state=0).split(train, y))
    train_idx, valid_idx = folds[args.fold]
    started = time.time()
    X_train, X_valid, X_test = add_nested_te(
        static, train, test, y, train_idx, valid_idx, args.seed_te,
    )

    params = dict(
        objective="binary", metric="auc", learning_rate=0.02,
        max_depth=5, num_leaves=32, min_child_samples=10,
        feature_fraction=0.30, bagging_fraction=0.80, bagging_freq=1,
        lambda_l1=0.071, lambda_l2=2.0, max_bin=1024,
        verbose=-1, num_threads=8, seed=args.seed_model,
    )
    dtrain = lgb.Dataset(X_train, y[train_idx], free_raw_data=False)
    dvalid = lgb.Dataset(X_valid, y[valid_idx], reference=dtrain)
    model = lgb.train(
        params, dtrain, 20_000, valid_sets=[dvalid],
        callbacks=[lgb.early_stopping(300, verbose=False)],
    )
    valid_pred = model.predict(X_valid, num_iteration=model.best_iteration)
    test_pred = model.predict(X_test, num_iteration=model.best_iteration)
    auc = float(roc_auc_score(y[valid_idx], valid_pred))
    np.savez_compressed(
        output / f"fold{args.fold}.npz",
        idx=valid_idx, pred=valid_pred, test=test_pred,
    )
    result = {
        "fold": args.fold,
        "auc": auc,
        "best_iteration": int(model.best_iteration),
        "seconds": time.time() - started,
        "features": int(X_train.shape[1]),
        "params": params,
    }
    (output / f"fold{args.fold}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
