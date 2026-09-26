# experiments

One file per change that was worth measuring.

I am keeping this deliberately small. The useful part of an experiment is the comparison, not a
page of narrative written after the result is known.

Current sequence:

```text
001-catboost-baseline.md    runtime failure, kept on purpose
002-lightgbm-baseline.md    first measured control
003-smaller-trees.md        current submission candidate
```

Each record should answer:

```markdown
# 001 - short name

Date:

Question:
What exactly am I trying to learn from this run?

Change:
One variable if possible. If it is not one variable, say so.

Validation:
Fold AUCs:
Mean AUC:
Std:
Runtime:

Kaggle:
Public AUC:

What happened:
What changed in the numbers, including fold spread.

Decision:
keep / revert / needs another run

Next:
The next smallest useful question.
```

A failed experiment stays here. Deleting the misses makes the final model look simpler than the
work that produced it.
