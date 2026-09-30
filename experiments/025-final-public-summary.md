# 025 - Final public leaderboard summary

Date: 2026-09-29

## Final public plateau

The project finished with a public ROC AUC of **0.94636**, up from the original submitted baseline of **0.94168**.

Several independently modified versions of the final source-allTE/high-resolution family converged to the same displayed public score:

| candidate | public AUC |
| --- | ---: |
| `candidate_source_k20_highres_rank_90_10_lex.csv` | **0.94636** |
| `candidate_source_k20_highres_rank_87p5_12p5_lex.csv` | **0.94636** |
| `candidate_source_k20_highres_87p5_12p5_multimodel_tiebreak.csv` | **0.94636** |
| `candidate_best_k20_highres_hardedges_v1.csv` | **0.94636** |
| `candidate_cb_bag3_multimodel_highres_rank_87p5_12p5_lex.csv` | 0.94633 |
| k10 source-allTE / high-res 87.5 / 12.5 rank blend | 0.94634 |

The repeated 0.94636 result across fold-count, blend-weight, tie-break, and hard-edge variants is strong evidence that this model family reached a genuine public plateau at the displayed leaderboard precision.

## Validation-backed core

The final family came from the generator-aware source-support + nested target-encoding LightGBM branch.

- 10-fold source-allTE pooled OOF: **0.9462042093**
- 20-fold source-allTE pooled OOF: **0.9462612**
- k10 to k20 test-rank Spearman correlation: ~**0.999938**

The k20 model improved aligned OOF, but its public blend tied the k10-family best rather than visibly exceeding it.

## What helped

The main improvements came from:

- shallow boosted trees instead of the original baseline configuration;
- high-resolution treatment of repeated continuous values;
- generator/source-support reconstruction using the verified RandomState(101) process;
- leak-safe nested target encodings for exact and bucketed income/commute values;
- conservative rank blending with the independently useful high-resolution additive model;
- increasing the source-allTE outer fold count from 10 to 20 for a small OOF gain.

## What did not transfer

Useful-looking local ideas that did not improve the public leaderboard included:

- global CatBoost/XGBoost multimodel weighting;
- multimodel tie-breaking;
- deterministic hard-edge income rules;
- exact-income residual corrections on top of source-allTE;
- strict additive interaction constraints;
- ID/modulo/generation-order features;
- simple original-source label priors;
- further micro-adjustments of the source/high-resolution blend weight.

Failed and neutral experiments remain in the repository rather than being removed after the fact.

## Known implementation note

The existing source-allTE feature builder abbreviates TE feature names with `col[:6]`. This causes the home/work charging-station target-encoding names to collide, leaving 79 columns instead of the intended 81 in that implementation. The issue was identified late in the project. A corrected full run was not completed and therefore was **not** promoted as a submission or claimed as an improvement.

## Final decision

Keep **0.94636** as the final public best for this project. Do not spend additional submissions on nearby post-processing or blend-weight variants without a genuinely new model family or a clearly validated new signal source.

All submitted predictions were produced from this project's own models. Public notebooks, discussions, and repositories were used only to study reproducible methodology; third-party prediction CSVs were not imported into submissions.
