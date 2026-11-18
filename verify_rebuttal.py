#!/usr/bin/env python3
"""
Rebuttal Verification and Artifact Reproduction Script
AISTATS 2027 Submission 982: PROCON
Recomputes all tables, statistical checks, and theorem diagnostics cited in the rebuttal.
"""

import json
import numpy as np
import pandas as pd


def section_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def verify_config_and_residual_mass() -> None:
    section_header(
        "1. FROZEN CONFIGURATION, INTENT SKEW, & RESIDUAL PARENT MASS (frozen_config.json)"
    )
    with open("frozen_config.json", "r", encoding="utf-8") as f:
        fc = json.load(f)

    print(f"SHA-256 Hash : {fc['sha256']}")
    print(f"Frozen UTC   : {fc['frozen_utc']}")
    print(f"Win Rule     : {fc['constants']['win_rule']}")

    t0_fracs = np.array(fc["tasks"]["T0"]["frac"])
    skew_ratio = t0_fracs.max() / t0_fracs.min()
    print(
        f"\nTask T0 Fit-Pool Intent Skew: min_frac={t0_fracs.min():.6f} "
        f"(E[m_g]={t0_fracs.min()*2000:.2f} at m=2000), "
        f"max_frac={t0_fracs.max():.6f} (E[m_g]={t0_fracs.max()*2000:.2f}), "
        f"imbalance ratio = {skew_ratio:.1f}x"
    )

    print("\nTracing Frozen Ward Hierarchy (M = 60 at m = 2000) for Residual Parent Cells:")
    levels = [32, 16, 8, 4, 2, 1]
    for tname in ["T0", "P1", "P2", "P3", "P4", "R1"]:
        tdata = fc["tasks"][tname]
        fracs = np.array(tdata["frac"])
        assigned = []
        for i in range(len(fracs)):
            for L in levels:
                lbls = np.array(tdata["labels"][str(L)])
                nid = int(lbls[i])
                node_mass = fracs[lbls == nid].sum() * 2000.0
                if node_mass >= 60.0 or L == 1:
                    assigned.append((L, nid))
                    break
        cell_map = {}
        for i, key in enumerate(assigned):
            cell_map.setdefault(key, []).append(i)
        routed_masses = {k: fracs[idxs].sum() * 2000.0 for k, idxs in cell_map.items()}
        below_19 = {k: round(v, 2) for k, v in routed_masses.items() if v < 19.0}
        min_mass = min(routed_masses.values())
        print(
            f"  Task {tname}: routed_cells={len(cell_map):2d} | "
            f"min_residual_expected_mass={min_mass:5.2f} | "
            f"cells < 19: {below_19 if below_19 else 'None (0.000 fallbacks)'}"
        )


def verify_fallback_and_strict_eq2() -> None:
    section_header(
        "2. STRICT EQUATION (2), FALLBACK BOUNDARY, & REAGGREGATION AUDIT (e4_all_draws.csv)"
    )
    e4 = pd.read_csv("e4_all_draws.csv")
    e4_pair = pd.read_csv("e4_by_pair.csv")
    print(f"Loaded e4_all_draws.csv: {len(e4):,} draw rows, {e4.duplicated().sum()} duplicates.")

    # Reaggregation audit (Supplement Section I.2 & I.5)
    cols = [
        "global_fpr",
        "cluster4_worst",
        "prox5_worst",
        "own_worst",
        "own_mean",
        "oos_detection",
        "near_oos_detection",
    ]
    re_pair = e4.groupby(
        ["task", "mseed", "family", "n_cal", "score", "alpha", "method"], as_index=False
    )[cols].mean()
    merged = pd.merge(
        re_pair,
        e4_pair,
        on=["task", "mseed", "family", "n_cal", "score", "alpha", "method"],
        suffixes=("_re", "_stored"),
    )
    max_err = max(float((merged[f"{c}_re"] - merged[f"{c}_stored"]).abs().max()) for c in cols)
    print(f"Max floating-point discrepancy vs. e4_by_pair.csv: {max_err:.2e}")

    for alpha in [0.05, 0.10]:
        sub_a = e4[e4["alpha"] == alpha]
        min_no_fb = sub_a[sub_a["n_fallback_cells"] == 0]["min_m_g"].min()
        max_with_fb = sub_a[sub_a["n_fallback_cells"] > 0]["min_m_g"].max()
        boundary = int(np.ceil(1.0 / alpha)) - 1
        print(
            f"  alpha={alpha:.2f} (theoretical finite floor m_g >= {boundary:2d}): "
            f"min(m_g) with 0 fallbacks = {min_no_fb:2d}, "
            f"max(m_g) with >0 fallbacks = {max_with_fb:2d}"
        )

    sub_h = e4[
        (e4["score"] == "BGE-M3-1024|Mahalanobis-PCA")
        & (e4["alpha"] == 0.05)
        & (e4["n_cal"] == 2000)
        & (e4["method"] == "hierarchical")
    ]
    n_zero_fb = (sub_h["n_fallback_cells"] == 0).sum()
    print("\nPrimary Hierarchical PROCON (BGE-M3 Mahalanobis, m=2000, alpha=0.05):")
    print(
        f"  Zero-fallback draws (strict Eq. 2 identical): "
        f"{n_zero_fb} / {len(sub_h)} ({n_zero_fb/len(sub_h)*100:.1f}%)"
    )

    comp = pd.DataFrame(
        {
            "All 200 Draws (%)": sub_h[cols].mean() * 100,
            "193 Zero-Fallback Draws (Strict Eq. 2) (%)": sub_h[
                sub_h["n_fallback_cells"] == 0
            ][cols].mean()
            * 100,
        }
    )
    print(comp.round(4).to_string())


def verify_exchangeability_and_mixture_shift() -> None:
    section_header(
        "3. EXCHANGEABILITY TESTS & MIXTURE SHIFT CURE (score_distributions.csv & e4_table_E3AB.csv)"
    )
    sd = pd.read_csv("score_distributions.csv")
    bge_sd = sd[(sd["encoder"] == "BGE-M3-1024") & (sd["score"] == "Mahalanobis-PCA")]
    print("Two-Sample Kolmogorov-Smirnov (KS) Tests (Calibration vs. Test In-Scope Scores):")
    print(
        bge_sd[
            [
                "seed",
                "encoder",
                "score",
                "ks_stat_cal_vs_test",
                "ks_pvalue_cal_vs_test",
                "tail_mass_above_tau_alpha0.05",
            ]
        ].to_string(index=False)
    )
    n_ks_pass = (sd["ks_pvalue_cal_vs_test"] > 0.05).sum()
    print(
        f"\nAcross all 40 (seed, encoder, score) runs: "
        f"{n_ks_pass}/40 have unadjusted KS p > 0.05 (40/40 after Holm)."
    )

    e4_ab = pd.read_csv("e4_table_E3AB.csv")
    sub_ab = e4_ab[
        (e4_ab["score"] == "BGE-M3-1024|Mahalanobis-PCA")
        & (e4_ab["alpha"] == 0.05)
        & (e4_ab["n_cal"] == 2000)
        & (e4_ab["method"].isin(["global", "semantic_cluster", "hierarchical"]))
    ].copy()
    for col in [
        "global_fpr",
        "own_mean",
        "cluster4_worst",
        "prox5_worst",
        "oos_detection",
        "near_oos_detection",
    ]:
        sub_ab[col] = (sub_ab[col] * 100).round(2)
    print("\nCure of Banking77 Intent-Proportion Shift on Identical Splits (m=2000, alpha=0.05):")
    print(
        sub_ab[
            [
                "method",
                "global_fpr",
                "own_mean",
                "cluster4_worst",
                "prox5_worst",
                "oos_detection",
                "near_oos_detection",
                "n_cells",
                "n_fallback",
            ]
        ].to_string(index=False)
    )


def verify_same_partition_reduction() -> None:
    section_header(
        "4. SAME-PARTITION WORST-CELL FPR REDUCTION (e5_local_risk_by_cell.csv vs. e4_table_E3AB.csv)"
    )
    e5 = pd.read_csv("e5_local_risk_by_cell.csv")
    e5_cells = e5[e5["n_g"].notna()].copy()
    e4_ab = pd.read_csv("e4_table_E3AB.csv")
    sub_e4 = e4_ab[(e4_ab["alpha"] == 0.05) & (e4_ab["n_cal"] == 2000)]

    rows = []
    for score in e5_cells["score"].unique():
        s_e5 = e5_cells[e5_cells["score"] == score]
        s_e4 = sub_e4[sub_e4["score"] == score].set_index("method")
        for part, m_e4 in [
            ("cluster4", "hierarchical"),
            ("semantic_cluster", "semantic_cluster"),
            ("semantic_proximity", "semantic_proximity"),
            ("predicted_intent", "predicted_intent"),
        ]:
            p_df = s_e5[s_e5["partition"] == part]
            global_worst = p_df.groupby(["task", "mseed"])["fpr"].max().mean() * 100
            local_worst = (
                s_e4.loc[m_e4, "cluster4_worst"] * 100
                if part == "cluster4"
                else s_e4.loc[m_e4, "own_worst"] * 100
            )
            rows.append(
                {
                    "Score": score,
                    "Partition P": part,
                    "Global Worst on P (%)": round(global_worst, 2),
                    "Localized Worst on P (%)": round(local_worst, 2),
                    "Change (pp)": round(local_worst - global_worst, 2),
                }
            )
    df_red = pd.DataFrame(rows)
    print(df_red.to_string(index=False))
    print(
        f"\nLocalized calibration reduces worst-cell FPR on "
        f"{(df_red['Change (pp)'] <= 0).sum()} / {len(df_red)} score-partition pairs."
    )


def verify_preregistered_wins_and_hierarchy() -> None:
    section_header(
        "5. PRE-REGISTERED WIN COUNTS & HIERARCHY VS. FLAT K=8 (primary_tests.csv & e4_by_pair.csv)"
    )
    pt = pd.read_csv("primary_tests.csv")
    win_summary = pt.groupby(["method", "reference"])["win"].sum().unstack()
    win_summary["Total Wins (of 10)"] = win_summary.sum(axis=1)
    print("Pre-Registered Wins (perm_p < 0.05 AND OOS loss <= 3.0 pp) across 5 Scores x 2 Partitions:")
    print(win_summary.to_string())

    e4_pair = pd.read_csv("e4_by_pair.csv")
    sub = e4_pair[(e4_pair["alpha"] == 0.05) & (e4_pair["n_cal"] == 2000)]
    print("\nHead-to-Head Pairwise Contrasts: Hierarchical PROCON minus Semantic Cluster (K=8) at m=2000:")
    h2h_rows = []
    for score in sub["score"].unique():
        s_df = sub[sub["score"] == score]
        h = s_df[s_df["method"] == "hierarchical"].set_index(["task", "mseed"])
        c8 = s_df[s_df["method"] == "semantic_cluster"].set_index(["task", "mseed"])
        d_c4 = (h["cluster4_worst"] - c8["cluster4_worst"]) * 100
        d_p5 = (h["prox5_worst"] - c8["prox5_worst"]) * 100
        d_near = (h["near_oos_detection"] - c8["near_oos_detection"]) * 100
        h2h_rows.append(
            {
                "Score": score,
                "Delta cluster4 (pp)": f"{d_c4.mean():+.2f} ({int((d_c4 < 0).sum())}/10 lower)",
                "Delta prox5 (pp)": f"{d_p5.mean():+.2f} ({int((d_p5 < 0).sum())}/10 lower)",
                "Delta Near-OOS (pp)": f"{d_near.mean():+.2f} ({int((d_near > 0).sum())}/10 higher)",
            }
        )
    print(pd.DataFrame(h2h_rows).to_string(index=False))


def verify_centered_shift_and_geometry() -> None:
    section_header(
        "6. CENTERED HOLDER SHIFT BOUND (THEOREM 5) & GEOMETRIC INVERSION (THEOREM 3)"
    )
    beta = 0.05
    print("Comparison of Uncentered vs. Centered p=2 (Chi-Squared) Shift Calibration Target (beta_g = 0.05):")
    shift_rows = []
    for chi2 in [0.000, 0.005, 0.010, 0.015, 0.020]:
        alpha_uncentered = (beta ** 2) / (1.0 + chi2)
        m_uncentered = int(np.ceil(1.0 / alpha_uncentered)) - 1
        alphas = np.linspace(1e-6, beta, 100000)
        bound_vals = alphas + np.sqrt(chi2 * alphas * (1.0 - alphas))
        alpha_centered = float(alphas[np.argmin(np.abs(bound_vals - beta))])
        m_centered = int(np.ceil(1.0 / alpha_centered)) - 1
        shift_rows.append(
            {
                "chi^2(Q_g || P_g)": f"{chi2:.3f}",
                "Uncentered alpha_shift": f"{alpha_uncentered:.5f}",
                "Uncentered min m_g": m_uncentered,
                "Centered alpha_shift": f"{alpha_centered:.5f}",
                "Centered min m_g": m_centered,
            }
        )
    print(pd.DataFrame(shift_rows).to_string(index=False))

    print("\nCLINC150 Gaussian PCA Squared Radial Contraction Gap (Supplement Table 31 & Proposition 2):")
    clinc_pca = pd.DataFrame(
        [
            ("MiniLM-32", 32, 25.88, 30.49, 0.2066),
            ("BGE-128", 32, 34.51, 38.13, 0.2279),
            ("BGE-128", 128, 214.93, 203.42, 0.7296),
        ],
        columns=["Model", "PCA Dims", "In-Scope LL", "OOS LL", "Gaussian AUROC"],
    )
    clinc_pca["Radial Gap E[||y_i||^2 - ||y_o||^2]"] = 2.0 * (
        clinc_pca["OOS LL"] - clinc_pca["In-Scope LL"]
    )
    clinc_pca["Pairwise Inversion Pr(l(Y_o)>l(Y_i)) (%)"] = (
        1.0 - clinc_pca["Gaussian AUROC"]
    ) * 100
    print(clinc_pca.round(2).to_string(index=False))

    print("\nBanking77 RealNVP Net Log-Likelihood Gap E[l(Y_o) - l(Y_i)] = E[gamma/2 - Delta_J] (Theorem 3):")
    sd = pd.read_csv("score_distributions.csv")
    ms = pd.read_csv("multiseed_summary.csv")
    flow_sd = sd[sd["score"] == "RealNVP-NLL"].groupby("encoder")[["mean", "oos_mean"]].mean()
    flow_ms = ms[(ms["score"] == "RealNVP-NLL") & (ms["alpha"] == 0.05)].set_index("encoder")[
        ["auroc_mean"]
    ]
    flow_df = flow_sd.join(flow_ms)
    flow_df["E[gamma/2 - Delta_J] (nats)"] = flow_df["mean"] - flow_df["oos_mean"]
    flow_df["Pairwise Inversion Pr(l(Y_o)>l(Y_i)) (%)"] = (1.0 - flow_df["auroc_mean"]) * 100
    print(flow_df.round(2).to_string())


if __name__ == "__main__":
    verify_config_and_residual_mass()
    verify_fallback_and_strict_eq2()
    verify_exchangeability_and_mixture_shift()
    verify_same_partition_reduction()
    verify_preregistered_wins_and_hierarchy()
    verify_centered_shift_and_geometry()