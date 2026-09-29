# 024 - Replication residuals, interaction constraints, and ID/order audit

Date: 2026-09-29

## Context

The experiment-022 two-rule hard-edge submission returned the same public score as the incumbent: **0.94636**. Experiment 023 therefore retired boundary forcing, tie-breaking, and micro-blend tuning. This experiment asks whether repeated-value structure can be exploited through a different objective/post-hoc expert, whether additive interaction constraints transfer to the stronger source-allTE representation, or whether row-generation order leaks signal.

## Fast aligned screening harness

The source-allTE feature builder was rewritten with a vectorized nested target encoder so a fold can be reconstructed in seconds rather than minutes. A 350-tree LightGBM surrogate uses the same source-support/all-column-TE representation but `max_bin=255`, `learning_rate=0.05` for fast screening.

Frozen fold 0:

- canonical full source-allTE reference: **0.946859646**
- fast 350-tree surrogate: **0.946808619**
- difference: **-0.000051027**

This is close enough to use as an architecture screen, but not as a replacement final model.

## Replication-aware exact-income correction

On a raw shallow LightGBM, exact-income group correction looked very strong:

- raw LightGBM fold 0: ~**0.94239**
- best regularized exact-income logit correction: ~**0.94388**
- apparent gain: ~**+0.00149**
- Newton residual group correction also gained ~**+0.00123**

However, the effect disappears once the model already includes source support and nested income target encodings.

On the fast source-allTE surrogate:

- base: **0.946808619**
- best tested exact-income correction: **0.946817001**
- delta: **+0.000008382**

Decision: **reject** post-hoc replication/group correction. The strong feature representation has already absorbed essentially all of the repeated-income signal.

A replication-weighted training-objective variant was started but did not finish within the available CPU execution window, so no result is claimed for that variant.

## Interaction-constraint screen

A fresh public discussion suggested additive/high-resolution trees can help simpler digit-based models. Tested directly on the stronger source-allTE representation using the same 350-tree fold-0 harness.

- unconstrained fast source-allTE: **0.946808619**
- strict additive LightGBM (`interaction_constraints=[[feature_i], ...]`): **0.946191896**
- delta: **-0.000616723**

Shorter exploratory screens that separated the income family or income+commute families were also clearly weaker before convergence and were not escalated. More complex constraint layouts became computationally unattractive in this environment.

Decision: **reject strict additive transfer**. The additive trick is not portable to our already-encoded representation; useful cross-feature interactions remain important.

## ID / generation-order audit

Because none of the strong models use `id`, generation-order leakage was checked as a genuinely independent axis.

Leak-safe target-encoding screens of `id mod period` across small periods produced only chance-level signal (best early screens around **0.501-0.502 AUC**). Target autocorrelations for lags from 1 through thousands were approximately zero (roughly within a few 1e-3). Sequential chunk target-rate standard deviations were approximately the binomial sampling expectation from chunk sizes 64 through 32768.

Decision: **no evidence of a useful ID, periodic, or batch-order leak**.

## Original-source labels / matching re-audit

Before promoting original-source target priors, public reproducible work was rechecked. Original target means and nearest-original-row label matching have already been tested by independent pipelines. A 190+ experiment project reports original-row similarity / neighborhood target statistics as neutral or negative; another triple-TE LightGBM using original target means, digits, frequencies, and generator flags reaches approximately the same public plateau (~0.94636).

Decision: simple original-label priors are not a new submission-worthy axis.

## Current conclusion

The repeated-income artifact is real, but source-support + nested all-column TE already captures almost all exploitable signal. The latest public 0.94636 result plus these screens materially strengthens the evidence that post-processing and another static generator feature are exhausted.

Do not spend another submission on:
- hard edges;
- exact-income residual corrections;
- strict additive source-allTE;
- ID/modulo/order features;
- simple original-target priors;
- small blend/tie-break changes.

A new submission should require either a genuinely new reproducible model family with aligned OOF improvement beyond the current core, or a fresh competition-specific mechanism that survives frozen-fold validation by a meaningful margin.
