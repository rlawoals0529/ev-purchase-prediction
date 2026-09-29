# 021 - Multimodel public rejection + tie-only reuse

Date: 2026-09-29

## Public result

Submission `candidate_cb_bag3_multimodel_highres_rank_87p5_12p5_lex.csv` scored **0.94633** public.

Current best remains **0.94636**, achieved by the source-allTE/high-res family (`candidate_source_k20_highres_rank_87p5_12p5_lex.csv` and `candidate_source_k20_highres_rank_90_10_lex.csv`).

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

This candidate therefore preserves every non-tied ordering decision from the current best and changes only ambiguous rows.

Generated:

- `candidate_source_k20_highres_87p5_12p5_multimodel_tiebreak.csv`
- `candidate_source_k20_highres_90_10_multimodel_tiebreak.csv`

The existing 87.5/12.5 candidate was reconstructed exactly before swapping the tie-break key, confirming the transformation changes only tie ordering.

## External methodology check

Recent public Kaggle notebooks/discussions report that tiny improvements in this competition can come from tie-breaking / micro-blending rather than globally stronger models. These references were used for methodology only; no third-party predictions were imported.

## Decision

Submit the 87.5/12.5 multimodel tie-break variant before any further global CatBoost/XGBoost blend. It is the minimum-change test from the current 0.94636 best.
