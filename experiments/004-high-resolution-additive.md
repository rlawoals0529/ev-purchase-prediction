# 004 - High-resolution additive trees

Date: 2026-09-26

Question:
Is the 0.9417 plateau partly a resolution problem rather than a lack of model capacity?

Why I tried it:
A useful public ablation in the competition discussion separated two ideas that are easy to mix
together: giving LightGBM more bins for high-cardinality numeric values, and preventing it from
spending branch depth on feature interactions. I wanted to test that on my own fixed folds instead
of copying somebody else's leaderboard number.

Change:
Same raw competition columns and the same 3 stratified folds as experiment 003. LightGBM now uses
`max_bin=16384`, `num_leaves=255`, `min_child_samples=10`, and singleton interaction constraints so
one branch cannot mix features. No target encoding, external data, pseudo-labels, or leaderboard
feedback is used in training.

Validation:
Fold AUCs: 0.944489, 0.945581, 0.945444
Mean AUC: **0.945171**
Std: 0.000486
OOF AUC: **0.945165**
Best iterations: 635, 609, 563

Delta from 003:
OOF AUC: **+0.003406**

Kaggle:
Public AUC: pending
Submission: `ev_purchase_submission_v3_highres.csv`

What happened:
This is the first change large enough that I do not have to argue about fourth-decimal noise. All
three folds moved by roughly the same amount, and the fold spread narrowed. The result also fits
the data audit: income has far more distinct values than the default LightGBM bin budget can keep
separate, while much of the target structure is close to additive.

Decision:
keep. This is the new submission candidate.

Next:
Submit it unchanged. If the public score tracks local validation again, move on to fold-safe
frequency/target encoding rather than tuning this model against the public leaderboard.
