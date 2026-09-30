# 020 - Public plateau + target-encoding name collision

Date: 2026-09-29

## Public feedback

Two 20-fold source-allTE/high-resolution rank blends both scored **0.94636** publicly:

- 90% source-allTE / 10% high-res: **0.94636**
- 87.5% source-allTE / 12.5% high-res: **0.94636**

This is the current public best. The identical score across nearby weights suggests further micro-tuning of this blend is low-value at current leaderboard precision.

## Implementation audit

The current `train_source_allte.py` builds target-encoding names with `col[:6]`.

Both:

- `Charging_Stations_Near_Home`
- `Charging_Stations_Near_Work`

truncate to `Chargi`, so the Home and Work TE columns overwrite each other at smoothing 10 and smoothing 100.

Confirmed locally:

- TE specs generated: 41
- unique TE names: 39
- collisions: 2
- current total matrix width: 79
- intended collision-free width: 81

A collision-free naming screen was started on frozen fold 0 against the existing baseline AUC **0.946859646**, but the local execution environment timed out during the full LightGBM fit before a trustworthy corrected AUC was produced. No leaderboard candidate is claimed from this branch yet.

## Decision

- Do not spend another submission on the existing 85/15 blend until a new signal is available.
- Prioritize validating the corrected 81-feature source-allTE representation.
- If the corrected fold result improves meaningfully, run full CV and package a new own-model candidate.
- Otherwise move to an aligned XGBoost companion for measured model-family diversity.
