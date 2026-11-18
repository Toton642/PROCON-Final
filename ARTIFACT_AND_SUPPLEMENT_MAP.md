## Artifact and Supplementary Material Navigation Guide (Submission 982)

This guide maps all appendices, mathematical proofs, raw CSV evaluation tables, frozen JSON configurations, and executed notebooks for AISTATS 2027 Submission 982.

## 1. Where to Find Appendices A through I (26-Page Supplementary PDF)

The Program Chairs AI Review noted that Appendices A through H are not inside the 11-page main manuscript PDF. All appendices are located in the 26-page Supplementary Material PDF uploaded on OpenReview (and included in this repository as `Supplementary_Material.pdf`):

* **Appendix A (Pages 1 to 2):** Full proof of Theorem 1, finite-threshold certifiability boundary ($m_g \ge 19$ at $\alpha_g = 0.05$), tie-breaking, and hierarchical certification.
* **Appendix B (Pages 2 to 3):** Proofs of Proposition 2 (Gaussian radial inversion), affine preprocessing contraction on $\mathbb{S}^{q-1}$, Theorem 3 (RealNVP flow criterion), and Corollary 7.
* **Appendix C (Pages 4 to 5):** Proof of Theorem 4 (Radon-Nikodym change of measure and Hölder transport bounds), singular components, and importance weight error bounds.
* **Appendix D (Pages 5 to 8):** Frozen Banking77 configuration (SHA-256 `7906e610...`), task definitions (T0, P1 to P4, R1), routing definitions, metric formulas, and leakage audit.
* **Appendix E (Pages 8 to 15):** Complete Banking77 tables (Tables 6 to 22), pair-level E3A and E3B breakdowns, cross-score sensitivity, resolution sweeps, and binomial power.
* **Appendix F (Pages 15 to 20):** Five-seed global Banking77 diagnostics, calibration-size sweeps, target-alpha sweeps, and exact binomial tests (Tables 23 to 29, Figures 3 to 4).
* **Appendix G (Pages 21 to 23):** Complementary CLINC150 five-seed benchmarks, latent geometry visualizations, ROC/PR curves, and Gaussian PCA sweep (Tables 30 to 31, Figures 5 to 8).
* **Appendix H (Page 23):** CLINC150 synthetic exponential-tilt covariate shift diagnostic and Banking77 length-ordered Adaptive Conformal Inference (ACI) simulation (Figure 9).
* **Appendix I (Pages 23 to 26):** Authoritative file inventory, 24,400-row reaggregation audit, reproducibility scope disclosure, and Manuscript-to-Artifact Traceability Map (Table 32).

## 2. Raw CSV, JSON, and Notebook Files Provided in This Repository

While the 26-page Supplementary Material PDF presents the formatted summary tables, this repository provides the underlying raw CSV, JSON, and Jupyter notebook artifacts listed in Supplement Section I.1 and Table 32 so reviewers can inspect every column and draw directly.

| Artifact File | Rows | Supplement Reference | Primary Contents |
| :--- | :---: | :--- | :--- |
| `frozen_config.json` | JSON | Section D.1, Table 5 | SHA-256 hash, Ward tree labels, proximity edges, intent fractions |
| `tasks.json` | JSON | Section D.2, Table 5 | Held-out OOS intent lists and E3A/E3B pair definitions |
| `primary_tests.csv` | 40 | Table 1, Table 3, Table 32 | Paired contrasts, bootstrap CIs, sign-flip p-values, pre-reg wins |
| `e4_table_E3AB.csv` | 122 | Main Table 1, Supp Table 6 | Pooled E3A+E3B metrics across 5 scores, $\alpha \in \{0.05, 0.10\}$, $m \in \{1000, 2000\}$ |
| `e4_table_E3A.csv` | 122 | Section E.2, Tables 7 to 8 | Block E3A aggregates across 5 model seeds on task T0 |
| `e4_table_E3B.csv` | 122 | Section E.2, Tables 9 to 10 | Block E3B aggregates across 5 OOS tasks at model seed 42 |
| `e4_by_pair.csv` | 1,220 | Tables 7 to 10, Table 12 | Pair-level means across 20 calibration redraws |
| `e4_all_draws.csv` | 24,400 | Section I.2, Table 32 | All 24,400 draw-level evaluations and fallback counts |
| `e3_variance_decomposition.csv` | 60 | Section 6, Supp Table 21 | Model-seed vs. held-out OOS task variance components |
| `e5_local_risk_by_cell.csv` | 6,580 | Section E.5 | Cellwise false-rejection rates under global calibration |
| `e5_heterogeneity_draws.csv` | 4,000 | Supp Table 14, Table 32 | Draw-level cellwise max FPR, dispersion, and Holm counts |
| `e5_test_power.csv` | 18 | Supp Table 22, Table 32 | Exact binomial exceedance test power by cell size $n_g$ |
| `e6_summary.csv` | 20 | Section 4.1, Supp Table 16 | Clustered Spearman $\rho$ and logit slopes across 120 clusters |
| `e6_curve_oos_quantile.csv` | 400 | Main Figure 2, Supp Table 17 | 20-bin OOS semantic-proximity detection curves |
| `e6_curve_fit_percentile.csv` | 200 | Supp Table 18, Table 32 | 10-bin fit-percentile companion proximity aggregation |
| `e7_regions.csv` | 6,050 | Section E.8 | Regional in-scope/OOS counts, local FPR, and detection |
| `e7_summary_per_pair.csv` | 200 | Supp Table 20 | Pair-level regional Spearman rank correlations |
| `e8_resolution_sweep.csv` | 80 | Main Table 2, Supp Table 13 | Fixed-resolution sweep across $K \in \{1, 2, 4, 8, 16, 32, 57\}$ |
| `e8_all_draws.csv` | 16,000 | Section E.4 | All 16,000 draw-level rows for the resolution sweep |
| `e9_summary.csv` | 30 | Main Table 4, Supp Table 15 | Calibration-mass FPR standard deviation vs. Beta reference |
| `e9_cell_calibration_size.csv` | 1,935 | Section E.6 | Per-cell calibration-mass subsampling diagnostics |
| `score_distributions.csv` | 40 | Rebuttal Q2 & W4 | Two-sample KS exchangeability p-values and RealNVP NLL means |
| `near_oos.csv` | 480 | Rebuttal W3 | Stratified Near-OOS and Far-OOS AUROC, AUPRC, and Macro F1 |
| `selective_accuracy.csv` | 40 | Rebuttal W3 | In-scope intent accuracy before and after conformal abstention |
| `multiseed_summary.csv` | 32 | Supp Figure 3, Supp Table 23 | 5-seed global Banking77 means, SDs, and 95% CIs |
| `calibration_size_sweep.csv` | 640 | Supp Figure 4, Supp Table 24 | Global calibration-size stability sweep ($m \in \{250, 500, 1000, 2000\}$) |
| `calibration_sweep.csv` | 240 | Supp Table 25 | 30-point target-alpha sweep ($\alpha \in [0.01, 0.30]$) |
| `statistical_tests.csv` | 160 | Supp Tables 26 to 29 | Exact one-sided binomial and Holm-adjusted exceedance tests |
| `reference_comparison_procon_clinc150.csv` | 12 | Supp Table 30, Table 32 | Verified 5-seed CLINC150 and Banking77 summary |
| `cov_pca_PROCON.ipynb` | Notebook | Supp Table 31, Section H.1 | Executed CLINC150 PCA likelihood sweep and oracle shift code |
| `verify_rebuttal.py` | Script | Section I.5 | Self-contained Python script verifying all rebuttal tables |

## 3. Quick Map from Reviewer Questions to Repository Files

* **Strict Equation (2) and Fallback Cutoff (Reviewer EH2V Q1/W2, PC Review):** Run `python3 verify_rebuttal.py` (Sections 1 and 2) or inspect `e4_all_draws.csv` and `frozen_config.json`.
* **Global 6.04% FPR Diagnosis and KS Exchangeability Control (Reviewer EH2V Q2/W3, Reviewer bpcj Q2/W4):** Run `python3 verify_rebuttal.py` (Section 3) or inspect `score_distributions.csv`, `statistical_tests.csv`, and `e4_table_E3AB.csv`.
* **Same-Partition Worst-Cell FPR Reduction (Reviewer bpcj W2, Reviewer EH2V Q3):** Run `python3 verify_rebuttal.py` (Section 4) or compare `e5_local_risk_by_cell.csv` (Supplement Table 14) with `e4_table_E3AB.csv` (Supplement Table 6).
* **Hierarchy vs. Flat Clustering Across Scores, Proximity Bins, and $m=1000$ (Reviewer EH2V W1/Q3, Reviewer bpcj Q1/Q3, Reviewer LAda):** Run `python3 verify_rebuttal.py` (Section 5) or inspect `primary_tests.csv`, `e4_by_pair.csv`, and `e8_resolution_sweep.csv`.
* **Far-OOS Detector Power and Selective Accuracy (Reviewer bpcj W3):** Inspect `near_oos.csv`, `e6_curve_oos_quantile.csv` (Supplement Table 17), and `selective_accuracy.csv`.
* **Centered Hölder Shift Bound and Radial/Flow Inversion Quantification (Reviewer EH2V W4, Reviewer bpcj W1, PC Review):** Run `python3 verify_rebuttal.py` (Section 6) or inspect `cov_pca_PROCON.ipynb` (Cells 4 and 7) and `score_distributions.csv`.
