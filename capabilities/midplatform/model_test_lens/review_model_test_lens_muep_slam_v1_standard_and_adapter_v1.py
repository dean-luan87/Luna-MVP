# -*- coding: utf-8 -*-
"""Verify MUEP V1 standard + SLAM Evaluation Adapter V1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_test_lens.adapters.slam.ate_calculator_v1 import (  # noqa: E402
    compute_ate_rmse_m,
    compute_drift_rate,
    compute_tracking_stability,
)
from capabilities.midplatform.model_test_lens.adapters.slam.procrustes_alignment_v1 import align_procrustes  # noqa: E402
from capabilities.midplatform.model_test_lens.adapters.slam.slam_diagnostic_engine_v1 import run_slam_diagnostics  # noqa: E402
from capabilities.midplatform.model_test_lens.adapters.slam.slam_evaluation_adapter_v1 import build_demo_envelope  # noqa: E402
from capabilities.midplatform.model_test_lens.standards.muep.muep_scoring_v1 import (  # noqa: E402
    compute_muep_final_score,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-MUEP-SLAM-Adapter-v1-001"
FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MUEP_SLAM_V1_STANDARD_AND_ADAPTER_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_MUEP_SLAM_V1_STANDARD_AND_ADAPTER_FAILED"

REQUIRED_STANDARD_FILES = [
    "capabilities/midplatform/model_test_lens/standards/muep/muep_input_schema_v1.json",
    "capabilities/midplatform/model_test_lens/standards/muep/muep_output_schema_v1.json",
    "capabilities/midplatform/model_test_lens/standards/muep/muep_scoring_model_v1.json",
    "capabilities/midplatform/model_test_lens/standards/muep/failure_mode_taxonomy_v1.json",
    "capabilities/midplatform/model_test_lens/standards/slam/slam_metric_spec_v1.json",
    "capabilities/midplatform/model_test_lens/standards/slam/slam_scoring_model_v1.json",
]

REQUIRED_ADAPTER_FILES = [
    "capabilities/midplatform/model_test_lens/adapters/slam/ate_calculator_v1.py",
    "capabilities/midplatform/model_test_lens/adapters/slam/procrustes_alignment_v1.py",
    "capabilities/midplatform/model_test_lens/adapters/slam/slam_diagnostic_engine_v1.py",
    "capabilities/midplatform/model_test_lens/adapters/slam/slam_evaluation_adapter_v1.py",
    "capabilities/midplatform/model_test_lens/static_site/slam_diagnostic_panels.js",
]

REQUIRED_STANDARD_FILES_EXTRA = [
    "capabilities/midplatform/model_test_lens/standards/slam/slam_scoring_model_v2.json",
]

REQUIRED_EXAMPLES = [
    "capabilities/midplatform/model_test_lens/examples/slam_orb_luna_street_scene_envelope_example_v1.json",
    "capabilities/midplatform/model_test_lens/examples/slam_orb_luna_street_scene_envelope_example_slim_v1.json",
]


def _check_files_exist() -> list[str]:
    missing = []
    for rel in REQUIRED_STANDARD_FILES + REQUIRED_STANDARD_FILES_EXTRA + REQUIRED_ADAPTER_FILES + REQUIRED_EXAMPLES:
        if not (_REPO_ROOT / rel).is_file():
            missing.append(rel)
    return missing


def _check_ate_calculator() -> list[str]:
    errors = []
    est = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    gt = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    ate = compute_ate_rmse_m(est, gt)
    if ate > 1e-6:
        errors.append(f"identity trajectory ATE expected ~0, got {ate}")
    drift = compute_drift_rate(0.1, 10.0)
    if abs(drift - 0.01) > 1e-6:
        errors.append(f"drift_rate expected 0.01, got {drift}")
    stability = compute_tracking_stability(["OK", "OK", "LOST"])
    if abs(stability - 2 / 3) > 1e-6:
        errors.append(f"tracking stability expected 0.667, got {stability}")
    return errors


def _check_envelope() -> list[str]:
    errors = []
    env = build_demo_envelope(downsample=6)
    required_keys = ["muep", "metrics", "failure_modes", "boundary_flags"]
    for k in required_keys:
        if k not in env:
            errors.append(f"envelope missing key: {k}")
    muep = env.get("muep", {})
    out = muep.get("output", {})
    metrics = out.get("metrics", {})
    if "final_score" not in metrics:
        errors.append("muep.output.metrics.final_score missing")
    slam = env.get("metrics", {}).get("slam", {})
    for k in ("ate_rmse_m", "drift_rate", "tracking_stability", "slam_score", "rpe_rmse_m"):
        if k not in slam:
            errors.append(f"metrics.slam.{k} missing")
    diag = env.get("diagnostics") or {}
    if diag.get("engine_version") != "slam_diagnostic_engine_v1":
        errors.append("diagnostics.engine_version missing or wrong")
    inner = diag.get("diagnostics") or {}
    for k in ("error_curve", "drift_heatmap", "failure_timeline"):
        if k not in inner or not inner[k]:
            errors.append(f"diagnostics.diagnostics.{k} missing or empty")
    layer_types = {l.get("layer_type") for l in env.get("visualization_layers") or []}
    for lt in ("error_curve", "drift_heatmap", "failure_timeline"):
        if lt not in layer_types:
            errors.append(f"visualization_layers missing {lt}")
    if env.get("boundary_flags", {}).get("candidate_only") is not True:
        errors.append("boundary_flags.candidate_only must be true")
    if env.get("readiness_effect", {}).get("runtime_ready") is not False:
        errors.append("readiness_effect.runtime_ready must be false")
    return errors


def _check_muep_scoring() -> list[str]:
    score = compute_muep_final_score(1.0, 1.0, 1.0)
    if abs(score - 1.0) > 1e-9:
        return [f"muep perfect score expected 1.0, got {score}"]
    score2 = compute_muep_final_score(0.0, 0.0, 0.0)
    if score2 != 0.0:
        return [f"muep zero score expected 0.0, got {score2}"]
    return []


def _check_diagnostic_engine() -> list[str]:
    errors = []
    pred = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    gt = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    aligned = align_procrustes(pred, gt)
    if aligned.residual_rmse_m > 1e-4:
        errors.append(f"procrustes identity rmse expected ~0, got {aligned.residual_rmse_m}")
    out = run_slam_diagnostics({"trajectory": pred, "ground_truth_trajectory": gt})
    if "error_curve" not in out.get("diagnostics", {}):
        errors.append("run_slam_diagnostics missing error_curve")
    return errors


def run_review() -> dict:
    checks: dict[str, list[str]] = {}
    checks["files_exist"] = _check_files_exist()
    checks["ate_calculator"] = _check_ate_calculator()
    checks["diagnostic_engine"] = _check_diagnostic_engine()
    checks["envelope"] = _check_envelope()
    checks["muep_scoring"] = _check_muep_scoring()

    all_errors = [e for errs in checks.values() for e in errs]
    decision = FINAL_DECISION_GO if not all_errors else FINAL_DECISION_FAILED

    return {
        "phase_id": PHASE_ID,
        "final_decision": decision,
        "checks": checks,
        "error_count": len(all_errors),
        "governance": {
            "candidate_only": True,
            "runtime_ready": False,
            "model_execution_on_page": False,
        },
    }


def main() -> int:
    result = run_review()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
