# 011 - Cross-generation rank blend

Date: 2026-09-26

Question:
Does the older high-resolution additive model still contain enough different ranking information to improve the new 0.94610 XGBoost candidate?

Change:
Do not blend the engineered LightGBM and XGBoost first because their test rankings are almost identical. Instead, rank-normalize the 0.94610 engineered XGBoost predictions and the 0.94548 high-resolution additive predictions, then combine them with two predetermined weights:

- 80% XGBoost / 20% high-resolution additive
- 70% XGBoost / 30% high-resolution additive

The test-set rank correlation between the two source models is about 0.99525. That is still high, but materially lower than the roughly 0.99930 correlation between engineered LGB and XGB.

Validation:
No new target fit. This is a post-model rank ensemble of two already measured submissions.

Kaggle:
XGBoost source: **0.94610** public
High-resolution source: **0.94548** public
80/20 blend: **0.94615** public
70/30 blend: **0.94615** public

What happened:
The 80/20 blend improved the XGBoost source by **+0.00005**. Moving another ten points of weight to the older model did not change the displayed public AUC at all. That is enough evidence to stop searching this blend axis rather than spending submissions on 75/25, 85/15, or other nearby weights.

Decision:
keep 0.94615 as the current public best. Close the weight search.

Next:
Use a genuinely different learner or representation so the next submission can add ranking diversity rather than reweighting the same two prediction sets.
