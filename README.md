## PROCON: Conditional Conformal Intent Verification under Geometric Likelihood Failure and Distribution Shift

This repository contains the frozen experimental artifacts, row-level evaluation tables, and verification scripts for AISTATS 2027 Submission 982. All files correspond directly to the manuscript tables and the 26-page Supplementary Material PDF.

* **Submission ID:** AISTATS 2027 Submission 982.


* **Configuration Hash:** SHA-256 7906e610dc04d145b507ac1e2b25c2c94d4c70b25b03f64bec96911b52efb9e0.


* **Freeze Timestamp:** 2026-10-01T06:35:24+00:00 recorded in frozen_config.json.


* **Primary Benchmark:** Banking77 across 10 structured task and seed pairs with 20 calibration redraws per pair.


* **Complementary Benchmark:** CLINC150 across 5 seeds for likelihood inversion and covariate shift diagnostics.



## 1. Executive Summary and Rebuttal Verification

This artifact suite provides direct empirical verification for every technical question raised during peer review.

* **Strict Conformal Validity:** Across 200 primary draws in e4_all_draws.csv, 193 draws have zero fallback cells and match strict Equation 2 identically.


* **Residual Parent Mass:** Tracing frozen_config.json shows the 7 sparse cell-draws occurred only in unsplit residual parent cells in tasks T0 and R1.


* **Exchangeability Diagnostics:** Two-sample Kolmogorov-Smirnov tests in score_distributions.csv yield p > 0.05 on all 5 seeds for BGE-M3 Mahalanobis-PCA.
* **Mixture Shift Cure:** Conditioning on semantic cells removes Banking77 intent-frequency skew, lowering global FPR from 6.04% to 4.88% and mean cell FPR to 5.00%.


* **Hierarchical Gain:** Hierarchical PROCON wins 8 of 10 pre-registered evaluations in primary_tests.csv compared to 5 of 10 for flat clustering.


* **Centered Shift Bound:** Centering the Radon-Nikodym bound around 1 recovers the nominal target at zero shift and requires only 19 samples instead of 399.


* **Geometric Inversion:** Executed sweeps in cov_pca_PROCON.ipynb and Supplement Table 31 quantify affine radial contraction and RealNVP log-likelihood gaps.



### Table 1: Primary Banking77 Localization and Pre-Registered Win Summary

| Router | Global FPR | Own Mean FPR | Cluster4 Worst | Pre-Reg Wins |
| --- | --- | --- | --- | --- |
| Global | 6.04% | 6.04% | 8.11% | Baseline |
| Semantic Cluster | 5.37% | 5.30% | 6.21% | 5 of 10 |
| Hierarchical PROCON | 4.88% | 5.00% | 6.15% | 8 of 10 |
| Predicted Intent | 4.30% | 4.13% | 5.60% | 3 of 10 |
| Semantic Proximity | 4.79% | 4.84% | 7.62% | 0 of 10 |

Values in the first four metric columns reflect BGE-M3 Mahalanobis-PCA at alpha = 0.05 and m = 2000 from e4_table_E3AB.csv and Supplement Table 6. The final column reports total wins out of 10 evaluations across all 5 score families and 2 reference partitions from primary_tests.csv.

### Table 2: Same-Partition Worst-Cell FPR Reduction

| Partition | Routed Cells | Global Worst | Localized Worst | Reduction |
| --- | --- | --- | --- | --- |
| cluster4 | 4.0 | 8.08% | 6.15% | -1.93 pp |
| semantic_cluster | 8.0 | 9.22% | 7.89% | -1.33 pp |
| semantic_proximity | 5.0 | 31.88% | 6.24% | -25.64 pp |
| predicted_intent | 48.8 | 29.07% | 17.69% | -11.38 pp |

Comparing Global calibration evaluated across the cells of each partition in e5_local_risk_by_cell.csv and Supplement Table 14 against Localized PROCON in e4_table_E3AB.csv and Supplement Table 6 confirms that localization reduces worst-cell false rejection on every partition.

## 2. Point-by-Point Reviewer Traceability Guide

* **Reviewer EH2V:** Fallback verification is in e4_all_draws.csv, exchangeability tests are in score_distributions.csv, and pre-registered contrasts are in primary_tests.csv.


* **Reviewer bpcj:** Orthogonal proximity evaluations are in Supplement Table 19, same-partition reductions are in Supplement Table 14, and Far-OOS AUROCs are in near_oos.csv.


* **Reviewer LAda:** Multi-score and orthogonal wins over flat clustering are in primary_tests.csv, e4_by_pair.csv, and e8_resolution_sweep.csv.


* **Program Chairs:** Table 1 and Table 2 RNG stream checks are in e4_all_draws.csv and e8_all_draws.csv, and exponential-tilt code is in cov_pca_PROCON.ipynb.



## 3. Repository File Inventory

All files are placed in the root directory to match the traceability map in Supplement Section I.1 and Table 32.

* **Frozen Metadata:** frozen_config.json and tasks.json store the SHA-256 hash, Ward hierarchy labels, proximity edges, fit-side intent fractions, and held-out OOS splits.


* **Primary Localization:** primary_tests.csv, e4_table_E3AB.csv, e4_table_E3A.csv, e4_table_E3B.csv, e4_by_pair.csv, and e4_all_draws.csv record all 24,400 draw evaluations.


* **Heterogeneity Diagnostics:** e5_local_risk_by_cell.csv, e5_heterogeneity_draws.csv, and e5_test_power.csv store cellwise global FPR and exact binomial test power.


* **Proximity Curves:** e6_summary.csv, e6_curve_oos_quantile.csv, e6_curve_fit_percentile.csv, e7_regions.csv, and e7_summary_per_pair.csv contain proximity stratifications.


* **Resolution Sweeps:** e8_resolution_sweep.csv, e8_all_draws.csv, e9_summary.csv, e9_cell_calibration_size.csv, and e3_variance_decomposition.csv track resolution trade-offs.


* **Exchangeability Suite:** score_distributions.csv, near_oos.csv, selective_accuracy.csv, multiseed_summary.csv, calibration_size_sweep.csv, calibration_sweep.csv, and statistical_tests.csv.


* **CLINC150 Benchmarks:** reference_comparison_procon_clinc150.csv and cov_pca_PROCON.ipynb reproduce the Gaussian PCA likelihood sweep and oracle covariate shift tests.



## 4. Result-Level Reproduction Instructions

1. Install standard scientific Python dependencies via `pip install pandas numpy` to run the aggregation checks.


2. Verify the SHA-256 hash, pre-registered win rule, and 42.8x fit-pool intent frequency skew in frozen_config.json.


3. Group e4_all_draws.csv by score, alpha, calibration size, and method to reproduce e4_by_pair.csv and e4_table_E3AB.csv to floating-point precision.


4. Filter e4_all_draws.csv for zero-fallback draws on BGE-M3 Mahalanobis-PCA to confirm that 193 of 200 draws satisfy strict Equation 2 with 6.1560% worst regional FPR.


5. Inspect primary_tests.csv to verify that Hierarchical PROCON achieves 8 of 10 pre-registered wins across cluster4 and prox5 reference partitions.


6. Open cov_pca_PROCON.ipynb to inspect the executed 5-seed CLINC150 covariate shift simulation and the multi-seed Gaussian PCA radial contraction sweep.
