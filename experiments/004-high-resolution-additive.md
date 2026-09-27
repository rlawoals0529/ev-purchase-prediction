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
Public AUC: **0.94548**
Submission: `ev_purchase_submission_v3_highres.csv`
Public minus OOF: **+0.000315**
Public improvement over experiment 003: **+0.00380**

What happened:
The public score confirmed the local jump instead of reversing it. The public/OOF gap is only
0.000315, so the same fixed split is still giving a useful signal for model selection. All three
folds improved locally, and the external score moved by almost the same amount as the OOF result.

This is also the first change large enough that I do not have to argue about fourth-decimal noise.
The result fits the data audit: income has far more distinct values than the default LightGBM bin
budget can keep separate, while much of the target structure is close to additive.

Decision:
keep. This is the measured reference for the next round.

Next:
Try fold-safe frequency and target-derived features without changing the validation split. Do not
use the 0.94548 leaderboard score to choose feature thresholds.
