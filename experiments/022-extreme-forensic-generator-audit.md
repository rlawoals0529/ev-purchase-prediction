# 022 - Extreme forensic generator audit

Date: 2026-09-29

## Why this branch

The public score plateaued at **0.94636** after k10/k20 source-allTE LightGBM, high-res rank blending, CatBoost/XGBoost diversification, and tie-breaking. The global multimodel branch improved aligned OOF but scored only 0.94633 public, while a multimodel tie-break remained 0.94636. This experiment deliberately moves away from micro-blend tuning and treats S6E9 as a synthetic-generator forensics problem.

## Data facts rechecked

Train has 668,665 rows, test 286,571, target positive rate 0.174645.

The two generator-heavy numeric columns are extremely repetitive:
- Annual_Income_USD: 13,214 unique values in train.
- Daily_Commute_km: 805 unique values in train.

The original 10k source is documented as NumPy `RandomState(101)` synthetic data. Public reconstruction work recovered the core purchase rule as a probit mechanism:

`1.2 * income/100000 + 0.6 * concern + 2 * subsidy_yes - 1 * anxiety_medium - 3 * anxiety_high + N(0,1) > 5.5`

The mechanism by itself scores about 0.93769 AUC on our competition train, so it cannot replace the generator-aware model. The competition generator adds repeated-value artifacts that the source-support/TE model captures.

## Deterministic income edges

Two regions are perfectly pure in the current competition train:

- `Annual_Income_USD >= 170537`: 393 / 393 positive.
- `31004 <= Annual_Income_USD <= 41970`: 0 / 1,257 positive.

The purity holds independently in every fold of the frozen 10-fold split. In test these affect 156 and 494 rows respectively.

Applying only these two rules to the independent probit score raises full-train AUC from **0.93769045** to **0.93778015**, delta **+0.00008970**.

A second independent check was run on fold 0 with a plain shallow LightGBM using only the raw competition columns. The rules again helped:

- base LightGBM fold-0 AUC: **0.94238977**
- with only the two income hard edges: **0.94253257**
- delta: **+0.00014280**

Therefore the edge gain is not an artifact of the probit formula or of the source-allTE model. It transfers across structurally different rankers.

A strong independent S6E9 pipeline also keeps exactly these two rules in its final post-processing. It measured additional candidate edges such as commute >= 83 km and a special 30k/no-subsidy cell as essentially neutral, so those extras are not promoted.

### Candidate

`candidate_best_k20_highres_hardedges_v1.csv`

Construction:
1. start from our public-best family: k20 source-allTE + high-res 87.5/12.5 rank blend;
2. force income >= 170537 to the top;
3. force income 31004..41970 to the bottom;
4. preserve the existing ordering within each forced region and outside them.

Secondary only: `candidate_best_k20_highres_hardedges4_extreme.csv` adds the two near-neutral extra rules and should not be submitted before the two-rule version.

## Tokenized / GPT-style numeric linear model

A public lead suggested a generator-aware linear/logistic model with tokenized numeric representations. We reproduced the underlying idea transparently using sparse exact-value, digit, substring/prefix/suffix, quantized-bin, and core DGP terms instead of importing predictions.

First frozen-fold result: about **0.94562 AUC**. This is interesting diversity but clearly below the ~0.9468 strong-tree fold, so it is rejected as a standalone candidate.

## Hierarchical empirical-Bayes lookup screen

Cross-fitted residual experts were tested around the probit prior.

Best early result came from exact income residual correction:
- probit prior: **0.937690**
- exact-income residual correction, smoothing ~10: **0.940595**

Commute residual corrections added very little. More specific income x context cells began to overfit. This confirms that exact income contains stable generator residual structure independent of the human-written buying formula, but direct lookup is not competitive with the source-allTE tree model.

## Range-anxiety reconstruction check

Range anxiety is highly structured but not deterministic in competition train. A shallow decision tree on commute, charging infrastructure, home charging, city and car-count reaches roughly 0.93-0.94 accuracy, and high commute strongly shifts probability toward Medium/High anxiety. This supports the source-generator story but does not expose a clean new leak.

## Jev / foundation-model direction

Jev was investigated as requested. Current benchmark material says classical models remain difficult to beat on structured tabular data with abundant labels. There is no directly available Jev integration in this environment. The useful concept is instead a bounded **mixture-of-experts / decision layer**: keep the validated generator/tree ranking for normal rows and allow deterministic source-mechanism experts to act only in regions where evidence is overwhelming.

TabPFN/foundation-model replacement is similarly unattractive for 668k rows; the source structure and repeated values are better matched by specialized generator features than generic few-shot tabular inference.

## Public-methodology findings

Recent Kaggle discussion reports:
- one competitor: best single-model OOF ~0.946274, best blend ~0.946378, public ~0.94652;
- another competitor reports a 10-fold XGBoost at **0.94652 CV** and logistic regression at **0.94640 CV**.

Those numbers imply there may still be honest signal above our local 0.94626-0.94629 regime, but no reproducible implementation for the 0.94652 XGB has been disclosed. We will not copy public prediction files.

A lossguide / max-leaves / max-bin=1024 XGBoost architecture was screened on our stronger source-allTE representation. On this CPU it reached about **0.94367 fold-0 AUC after 250 rounds** and was still climbing when the execution window ended. This is not enough evidence to promote it and it is too expensive here for a blind full run.

## Decision

**Promote** the two-rule hard-edge candidate as the next structurally justified submission.

Continue research on:
- generator-aware XGBoost variants when compute allows;
- Jev-style gated experts rather than global blending;
- source-label / original-data priors if they can be reconstructed reproducibly;
- specialized corrections only where they improve frozen OOF or are fold-stable deterministic regions.

Reject for now:
- global CatBoost/XGB weighting for public submissions;
- tokenized sparse linear model as standalone;
- broad income x context memorization;
- extra weak hard-edge rules.
