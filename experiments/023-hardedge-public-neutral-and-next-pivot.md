# 023 - Hard-edge public neutral; retire post-processing branch

Date: 2026-09-29

## Public result

The two-rule hard-edge candidate from experiment 022 was submitted after passing frozen-fold purity checks and two independent local-model checks.

**Public leaderboard score: 0.94636**, exactly the same as the existing best family.

Therefore the hard-edge modification is public-rank-neutral at leaderboard precision. This is a failed transfer for submission purposes.

## Decision

Retire this entire axis for remaining submissions:

- no additional deterministic income-boundary forcing;
- no more lexicographic tie-break variants;
- no more tiny high-res/source-allTE blend-weight changes;
- no extra near-neutral commute or 30k special-case rules.

The public result is stronger evidence than the local fold improvements: the edge rules can improve generic validation rankers while making no measurable difference once applied to the already-strong 0.94636 family.

## Research after the result

A source-label-prior branch was re-audited before spending another attempt. Public code confirms that original-source labels have been used in several ways, including exact original value target means and nearest original-row label matching. A strong 190+ experiment pipeline reports that **similarity to original rows was neutral/negative**, while a separate triple-feature LightGBM using original target means, digits, frequencies, generator flags and triple target encoding reached roughly the same public plateau (~0.94636).

This means simple original-label means are not enough by themselves and should not be promoted as the next submission.

The next useful search must materially change how repeated generator values enter the loss/model, rather than append another static feature. Priority directions:

1. replication-aware/group-aware learning or residual boosting on repeated income identities;
2. models whose objective operates on value groups or corrects replicate-count dominance;
3. new current competition methods that can be reproduced with our own predictions and validated on frozen folds;
4. only then a final submission if the gain is materially above the 0.94620-0.94629 local regime or is supported by a genuinely independent signal.

## Submission rule

Do not create/promote another Kaggle CSV from this branch until it beats the current source-allTE family on aligned frozen OOF by a meaningful margin, not merely a few 1e-5, or demonstrates a clearly new validated signal source.
