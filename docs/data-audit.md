# data audit

Checked before the first measured baseline.

| | train | test |
| --- | ---: | ---: |
| rows | 668,665 | 286,571 |
| feature columns including `id` | 14 | 14 |
| missing cells | 0 | 0 |
| duplicate rows | 0 | 0 |

The target is `Yes` for 116,779 of 668,665 training rows, or **17.4645%**.

`id` is unique and contiguous: training runs from 0 through 668,664 and test starts at 668,665.
That makes it a row identifier rather than a feature I want the model to learn, so it is excluded
from training and copied back only when the submission is written.

## Train/test drift

I checked numeric columns with standardized mean difference and categorical columns with total
variation distance. The largest absolute numeric standardized mean difference is **0.0048**
(`Number_of_Cars_Owned`). The largest categorical total variation distance is **0.0017**
(`Range_Anxiety_Level`).

Those are small enough that I do not see an obvious train/test distribution shift that calls for a
special validation split. I am using shuffled stratified folds and keeping the split seed fixed.

## Strong single-feature signals

These are descriptive target rates, not model claims:

- `Subsidy_Available`: 27.47% Yes when available, 0.58% when not available.
- `Range_Anxiety_Level`: 18.90% Yes for Low, 4.17% for Medium, 0.14% for High.
- `Home_Charging_Possible`: 19.58% Yes for Yes, 12.71% for No.
- `Environmental_Concern_Level` has the strongest linear correlation with the binary target among
  the small-range numeric fields.

The large differences are reasons to expect a straightforward tabular model to work well. They are
not a reason to hand-code a rule from the full training target, because the competition metric is
still measured on unseen rows.
