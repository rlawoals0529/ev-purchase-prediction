# 021 - Multimodel public rejection + tie-only reuse

Date: 2026-09-29

## Public results

Submission `candidate_cb_bag3_multimodel_highres_rank_87p5_12p5_lex.csv` scored **0.94633** public.

Current best remained **0.94636**, achieved by the source-allTE/high-res family (`candidate_source_k20_highres_rank_87p5_12p5_lex.csv` and `candidate_source_k20_highres_rank_90_10_lex.csv`).

Decision: **reject global CatBoost/XGBoost weighting for public submissions**. Although the aligned OOF tree ensemble improved to ~0.9462906, that gain did not transfer to the public split.

## Lower-risk tie-only reuse

Rather than give the multimodel ensemble global weight, keep the successful 87.5% k20 source-allTE / 12.5% high-res weighted-rank ordering completely unchanged and use the stronger multimodel ordering only to break exact weighted-rank ties.

For the 87.5/12.5 primary weighted rank:

- unique primary scores before tie-breaking: **276,245** of 286,571 rows
- tied groups: **10,087**
- rows belonging to tied groups: **20,413**
- maximum tie-group size: **4**
- rows whose final unique rank changes when multimodel becomes the first tie-break key: **10,127**
- maximum rank displacement: **3 positions**
- Spearman correlation vs the current 0.94636 file: effectively 1.0 (**0.9999999999973**)

Generated:

- `candidate_source_k20_highres_87p5_12p5_multimodel_tiebreak.csv`
- `candidate_source_k20_highres_90_10_multimodel_tiebreak.csv`

The existing 87.5/12.5 candidate was reconstructed exactly before swapping the tie-break key, confirming the transformation changes only tie ordering.

## Tie-break public result

`candidate_source_k20_highres_87p5_12p5_multimodel_tiebreak.csv` scored **0.94636** public, exactly matching the incumbent.

The tie-only reuse therefore preserved the score but did not improve it. This closes the multimodel tie-break branch as public-rank-neutral at leaderboard precision.

## External methodology check

Recent public Kaggle notebooks/discussions were used for methodology only; no third-party prediction files were imported. Every submitted prediction in this project comes from our own trained models or deterministic combinations of those predictions.

## Decision

- Reject global CatBoost/XGBoost weighting for the final submission family.
- Treat multimodel tie-breaking as neutral rather than an improvement.
- Keep the k20 source-allTE/high-resolution rank blend as the public-best core.
