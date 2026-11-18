"""Run this cell immediately after notebook cell 41 finishes the BGE-128 refit."""

import json
from pathlib import Path

import numpy as np


required = [
    "flow_val_scores",
    "flow_test_scores",
    "val_in_scope_mask",
    "y_test_oos",
    "conformal_threshold",
    "evaluate_binary",
    "ALPHA",
]
missing = [name for name in required if name not in globals()]
if missing:
    raise RuntimeError(
        "Run this cell after the BGE-128 refit and scoring cell. "
        f"Missing notebook variables: {missing}"
    )

bge_val_scores = np.asarray(flow_val_scores, dtype=float).reshape(-1)
bge_test_scores = np.asarray(flow_test_scores, dtype=float).reshape(-1)
bge_calibration_scores = bge_val_scores[np.asarray(val_in_scope_mask, dtype=bool)]
bge_test_labels = np.asarray(y_test_oos, dtype=int).reshape(-1)

if len(bge_calibration_scores) != 3000:
    raise ValueError(
        f"Expected 3,000 in-scope calibration scores, got {len(bge_calibration_scores)}"
    )
if len(bge_test_scores) != len(bge_test_labels):
    raise ValueError("BGE test scores and test labels have different lengths")
if not np.isfinite(bge_calibration_scores).all() or not np.isfinite(bge_test_scores).all():
    raise ValueError("BGE score arrays contain non-finite values")

bge_tau, bge_zero_based_index = conformal_threshold(
    bge_calibration_scores,
    alpha=ALPHA,
)
bge_metrics = evaluate_binary(
    bge_test_scores,
    bge_test_labels,
    bge_tau,
    alpha=ALPHA,
)

payload = {
    "Configuration": "BGE-large-en-v1.5 + PCA-128 + RealNVP-256",
    "Seed": 42,
    "Alpha": float(ALPHA),
    "Calibration Size": int(len(bge_calibration_scores)),
    "Order Statistic Index Zero Based": int(bge_zero_based_index),
    "Order Statistic Rank One Based": int(bge_zero_based_index + 1),
    "Threshold": float(bge_tau),
    "AUROC": float(bge_metrics["AUROC"]),
    "AUPRC": float(bge_metrics["AUPRC"]),
    "Macro F1": float(bge_metrics["Macro F1"]),
    "OOS Detection Rate": float(bge_metrics["OOS Detection Rate"]),
    "Empirical FPR": float(bge_metrics["Empirical FPR"]),
    "Finite Sample FPR Guarantee": True,
    "Empirical FPR At Or Below Alpha": bool(
        bge_metrics["Empirical FPR"] <= float(ALPHA)
    ),
}

Path("bge128_calibration_metrics.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True),
    encoding="utf-8",
)
np.savez_compressed(
    "bge128_calibration_artifact.npz",
    validation_scores=bge_val_scores,
    calibration_scores=bge_calibration_scores,
    test_scores=bge_test_scores,
    test_labels=bge_test_labels,
    threshold=np.asarray([bge_tau], dtype=float),
    alpha=np.asarray([ALPHA], dtype=float),
)

print(json.dumps(payload, indent=2, sort_keys=True))
print("Saved bge128_calibration_metrics.json")
print("Saved bge128_calibration_artifact.npz")