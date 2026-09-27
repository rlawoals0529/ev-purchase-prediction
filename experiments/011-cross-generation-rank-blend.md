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
70/30 blend: pending

What happened:
The 80/20 blend improved the XGBoost source by **+0.00005**. That is a very small gain, so I am not treating it as evidence for a broad blend-weight search. It is only enough to justify the second weight that was fixed before seeing the result.

Decision rule:
The first predetermined blend improved, so submit the already-prepared 70/30 point once. After that, stop searching blend weights against the public leaderboard regardless of whether it wins.

Decision:
keep the 80/20 result as the current public best. Test the one remaining predetermined 70/30 blend.
