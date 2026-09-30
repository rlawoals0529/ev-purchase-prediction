# Experiments

One file per change that was worth measuring. Failed and neutral runs stay here on purpose.

The project finished at **0.94636 public ROC AUC**, starting from a **0.94168** submitted baseline.

## Sequence

| experiment | focus | result |
| --- | --- | --- |
| 001 | CatBoost baseline | runtime failure, kept |
| 002 | LightGBM baseline | first measured control |
| 003 | smaller trees | **0.94168 public** |
| 004 | high-resolution additive | **0.94548 public** |
| 005-009 | frequency, buckets, exact values, digits | mixed/rejected screens |
| 010 | engineered LGB + XGB | **0.94607 / 0.94610 public** |
| 011 | cross-generation rank blend | **0.94615 public** |
| 012 | native CatBoost branch | prepared / later revisited |
| 013 | diversity rank blend | **0.94617 public** |
| 014 | lexicographic tie-break | **0.94617 public**, neutral |
| 015 | source support + all-column TE | generator-aware k10 core |
| 016 | post-source-allTE screens | several structural rejects |
| 017 | k20 continuation + hedges | higher-fold branch |
| 018 | completed k20 source-allTE | **~0.9462612 pooled OOF** |
| 019 | k20 blend grid | **0.94636 public** |
| 020 | aligned multimodel + CatBoost bag | local OOF gain |
| 021 | multimodel public test + tie-break | **0.94633 global; 0.94636 tie-only** |
| 022 | forensic generator audit | boundary/source investigations |
| 023 | hard-edge public test | **0.94636**, neutral |
| 024 | replication, constraints, ID audit | no new validated signal |
| 025 | final public summary | project closed at **0.94636** |

## Experiment template

Each record should answer:

```markdown
# NNN - short name

Date:

Question:
What exactly am I trying to learn from this run?

Change:
One variable if possible. If it is not one variable, say so.

Validation:
Fold AUCs:
Mean/pooled AUC:
Runtime:

Kaggle:
Public AUC:

What happened:
What changed in the numbers, including disagreements between local validation and public score.

Decision:
keep / revert / needs another run

Next:
The next smallest useful question.
```

Deleting failed experiments would make the final model look much simpler than the work that produced it, so the misses remain part of the record.
