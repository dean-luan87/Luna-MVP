# -*- coding: utf-8 -*-
"""SLAM Evaluation Adapter V1 — unify ORB / VINS / Kimera outputs into MUEP envelope."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

_REPO_ROOT = Path(__file__).resolve().parents[5]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_test_lens.adapters.slam.ate_calculator_v1 import (  # noqa: E402
    ate_to_score,
    compute_ate_rmse_m,
    compute_drift_rate,
    compute_path_length_m,
    compute_tracking_stability,
    compute_trajectory_smoothness,
    drift_to_penalty,
)
from capabilities.midplatform.model_test_lens.adapters.slam.slam_diagnostic_engine_v1 import (  # noqa: E402
    SLAM_DIAGNOSTIC_WEIGHTS_V2,
    compute_slam_score_v2,
    run_slam_diagnostics,
)

from capabilities.midplatform.model_test_lens.standards.muep.muep_scoring_v1 import (  # noqa: E402
    build_muep_metrics_block,
    clamp01,
)

SLAM_WEIGHTS = {
    "ate_score": 0.5,
    "stability": 0.2,
    "drift_penalty": 0.2,
    "structural_quality": 0.1,
}

# V2 diagnostic scoring — preferred when diagnostics block present
SLAM_WEIGHTS_V2 = dict(SLAM_DIAGNOSTIC_WEIGHTS_V2)


@dataclass
class SlamAdapterConfig:
    backend: str = "orb_slam"
    dataset: str = "luna_street_scene_v1"
    ate_ref_m: float = 0.5
    drift_ref: float = 0.05


def compute_slam_score(
    ate_m: float,
    stability: float,
    drift_rate: float,
    structural_quality: float,
    *,
    ate_ref_m: float = 0.5,
    drift_ref: float = 0.05,
) -> float:
    ate_score = ate_to_score(ate_m, ate_ref_m)
    drift_penalty = drift_to_penalty(drift_rate, drift_ref)
    return clamp01(
        SLAM_WEIGHTS["ate_score"] * ate_score
        + SLAM_WEIGHTS["stability"] * clamp01(stability)
        + SLAM_WEIGHTS["drift_penalty"] * drift_penalty
        + SLAM_WEIGHTS["structural_quality"] * clamp01(structural_quality)
    )


def infer_failure_modes(
    *,
    ate_m: float,
    drift_rate: float,
    stability: float,
    tracking_lost_frames: int,
    loop_closure_ok: bool,
    ate_threshold_m: float = 0.15,
    drift_threshold: float = 0.03,
    stability_threshold: float = 0.9,
) -> List[str]:
    modes: List[str] = []
    if drift_rate > drift_threshold or ate_m > ate_threshold_m:
        modes.append("drift")
    if stability < stability_threshold:
        modes.append("tracking_lost")
    if tracking_lost_frames > 0:
        if "tracking_lost" not in modes:
            modes.append("tracking_lost")
    if not loop_closure_ok:
        modes.append("loop_closure_failure")
    if stability < 0.75:
        modes.append("low_confidence_collapse")
    return modes


def adapt_slam_run_to_envelope(
    slam_run: Mapping[str, Any],
    *,
    config: Optional[SlamAdapterConfig] = None,
    envelope_id: str = "slam_evaluation_envelope_v1",
    phase_ref: str = "Phase-P1-Midplatform-Model-Test-Lens-MUEP-SLAM-Adapter-v1-001",
) -> Dict[str, Any]:
    """Convert raw SLAM backend output + GT into Model Test Lens envelope with MUEP block."""
    cfg = config or SlamAdapterConfig()
    est_traj = slam_run.get("trajectory") or slam_run.get("estimated_trajectory") or []
    gt_traj = slam_run.get("ground_truth_trajectory") or []
    tracking_states = slam_run.get("per_frame_tracking_state") or []
    keyframes = slam_run.get("keyframes") or []
    tracking_state = str(slam_run.get("tracking_state", "OK")).upper()

    ate_m = compute_ate_rmse_m(est_traj, gt_traj)
    path_len = compute_path_length_m(gt_traj or est_traj)
    drift_rate = compute_drift_rate(ate_m, path_len)
    stability = compute_tracking_stability(tracking_states) if tracking_states else (
        1.0 if tracking_state == "OK" else 0.0
    )

    diagnostics_block = run_slam_diagnostics(
        {
            "trajectory": est_traj,
            "ground_truth_trajectory": gt_traj,
            "timestamps": slam_run.get("timestamps"),
            "per_frame_tracking_state": tracking_states,
            "keyframes": keyframes,
            "loop_closure_frames": slam_run.get("loop_closure_frames") or [],
            "loop_closure_correct": slam_run.get("loop_closure_correct", True),
            "metadata": {
                "dataset": slam_run.get("dataset", cfg.dataset),
                "model": slam_run.get("backend", cfg.backend),
            },
        },
        ate_ref_m=cfg.ate_ref_m,
        drift_ref=cfg.drift_ref,
    )
    diag_metrics = diagnostics_block["metrics"]
    ate_m = float(diag_metrics["ATE"])
    drift_rate = float(diag_metrics["drift_rate"])
    stability = float(diag_metrics["tracking_stability"])
    slam_score = float(diag_metrics["slam_score_v2"])
    failure_modes = diagnostics_block["failure_modes"]
    aligned_traj = diagnostics_block["alignment"]["aligned_trajectory"]
    traj_smooth = compute_trajectory_smoothness(est_traj)
    map_consistency = float(slam_run.get("map_consistency_score", 0.85))
    loop_closure_ok = bool(slam_run.get("loop_closure_correct", True))
    loop_closure_stability = float(slam_run.get("loop_closure_stability", 0.88 if loop_closure_ok else 0.4))

    structural_quality = clamp01(
        0.4 * map_consistency + 0.4 * traj_smooth + 0.2 * (1.0 if loop_closure_ok else 0.3)
    )
    # V1 scalar score kept for backward compat; V2 diagnostic score is primary
    slam_score_v1 = compute_slam_score(
        ate_m, stability, drift_rate, structural_quality,
        ate_ref_m=cfg.ate_ref_m, drift_ref=cfg.drift_ref,
    )

    robustness = {
        "motion_blur_sensitivity": float(slam_run.get("motion_blur_sensitivity", 0.22)),
        "low_light_degradation": float(slam_run.get("low_light_degradation", 0.18)),
        "loop_closure_stability": loop_closure_stability,
        "robustness_score_normalized": clamp01(
            1.0
            - 0.35 * float(slam_run.get("motion_blur_sensitivity", 0.22))
            - 0.35 * float(slam_run.get("low_light_degradation", 0.18))
            - 0.30 * (1.0 - loop_closure_stability)
        ),
    }

    muep_metrics = build_muep_metrics_block(
        primary_metric_name="ATE_rmse_m",
        primary_metric_value=ate_m,
        primary_metric_score_normalized=ate_to_score(ate_m, cfg.ate_ref_m),
        robustness=robustness,
        structural_score=structural_quality,
        structural_notes=[
            f"trajectory_smoothness={traj_smooth:.3f}",
            f"map_consistency={map_consistency:.3f}",
            f"loop_closure_correct={loop_closure_ok}",
        ],
    )

    lost_frames = sum(1 for s in tracking_states if str(s).upper() not in {"OK", "TRACKED", "TRACKING"})
    if not failure_modes:
        failure_modes = infer_failure_modes(
            ate_m=ate_m,
            drift_rate=drift_rate,
            stability=stability,
            tracking_lost_frames=lost_frames,
            loop_closure_ok=loop_closure_ok,
        )

    confidence = clamp01(0.5 * stability + 0.3 * structural_quality + 0.2 * muep_metrics["final_score"])

    slam_metrics = {
        "ate_rmse_m": round(ate_m, 4),
        "rpe_rmse_m": round(float(diag_metrics["RPE"]), 4),
        "drift_rate": round(drift_rate, 6),
        "tracking_stability": round(stability, 4),
        "slam_score": round(slam_score, 4),
        "slam_score_v1": round(slam_score_v1, 4),
        "diagnostic_penalty_score": round(float(diag_metrics["diagnostic_penalty_score"]), 4),
        "path_length_m": round(path_len, 3),
        "tracked_frames": sum(
            1 for s in tracking_states if str(s).upper() in {"OK", "TRACKED", "TRACKING"}
        ) if tracking_states else None,
        "total_frames": len(tracking_states) if tracking_states else len(est_traj) or None,
        "structural": {
            "map_consistency_score": map_consistency,
            "trajectory_smoothness": round(traj_smooth, 4),
            "loop_closure_correctness": 1.0 if loop_closure_ok else 0.0,
        },
        "robustness": robustness,
        "scoring_weights": dict(SLAM_WEIGHTS_V2),
    }

    model_id = str(slam_run.get("backend", cfg.backend))
    dataset = str(slam_run.get("dataset", cfg.dataset))

    return {
        "envelope_id": envelope_id,
        "phase_ref": phase_ref,
        "test_case_id": f"slam_{dataset}_{model_id}_v1",
        "model_id": model_id,
        "model_category": "slam_vio",
        "model_version_or_registry_ref": "capabilities/midplatform/model_test_lens/standards/slam/slam_metric_spec_v1.json",
        "input_asset_refs": list(slam_run.get("input_asset_refs") or [
            f"capabilities/test_assets/p1/slam/{dataset}/sequence_manifest_v1.json",
        ]),
        "muep": {
            "protocol_version": "muep_v1",
            "input": {
                "model_type": "slam",
                "input": {
                    "data": "sequence",
                    "metadata": {
                        "dataset": dataset,
                        "imu": slam_run.get("imu", "optional"),
                        "camera_intrinsics_ref": slam_run.get("camera_intrinsics_ref", ""),
                    },
                },
                "task": {"prompt": "", "mode": "stream"},
            },
            "output": {
                "prediction": {
                    "trajectory": est_traj,
                    "map": slam_run.get("map") or {},
                    "keyframes": keyframes,
                    "tracking_state": tracking_state,
                },
                "intermediate": {
                    "aligned_trajectory_preview": aligned_traj[: min(5, len(aligned_traj))],
                    "covariance": slam_run.get("covariance") or [],
                },
                "metrics": muep_metrics,
                "failure_modes": failure_modes,
                "confidence": round(confidence, 4),
            },
        },
        "candidate_outputs": [
            {
                "artifact_type": "trajectory_candidate",
                "frame_count": len(est_traj),
                "candidate_only": True,
            }
        ],
        "visualization_layers": [
            {
                "layer_id": "trajectory_xy_overlay",
                "layer_type": "trajectory",
                "display_name": "estimated vs ground_truth (XY)",
                "model_id": model_id,
                "candidate_only": True,
                "trajectory_estimated": aligned_traj,
                "trajectory_ground_truth": gt_traj,
                "trajectory_raw_estimated": est_traj,
            },
            {
                "layer_id": "error_curve_panel",
                "layer_type": "error_curve",
                "display_name": "Frame-level error curve",
                "model_id": model_id,
                "candidate_only": True,
                "error_curve": diagnostics_block["diagnostics"]["error_curve"],
            },
            {
                "layer_id": "drift_heatmap_panel",
                "layer_type": "drift_heatmap",
                "display_name": "Drift heatmap by segment",
                "model_id": model_id,
                "candidate_only": True,
                "drift_heatmap": diagnostics_block["diagnostics"]["drift_heatmap"],
            },
            {
                "layer_id": "failure_timeline_panel",
                "layer_type": "failure_timeline",
                "display_name": "Failure timeline",
                "model_id": model_id,
                "candidate_only": True,
                "failure_timeline": diagnostics_block["diagnostics"]["failure_timeline"],
            },
            {
                "layer_id": "drift_metrics_panel",
                "layer_type": "drift_metrics",
                "display_name": "ATE / drift / stability",
                "model_id": model_id,
                "candidate_only": True,
                "metrics_ref": "metrics.slam",
            },
        ],
        "diagnostics": diagnostics_block,
        "metrics": {
            "muep_final_score": muep_metrics["final_score"],
            "slam": slam_metrics,
        },
        "failure_modes": failure_modes,
        "quality_summary": {
            "human_review_required": True,
            "suitable_for_runtime_admission": False,
            "not_semantic_fact": True,
            "aggregate_note": (
                f"SLAM Diagnostic V1 — ATE={ate_m:.3f}m RPE={diag_metrics['RPE']:.3f}m "
                f"drift={drift_rate:.4f} stability={stability:.2%} score_v2={slam_score:.3f}"
            ),
        },
        "test_board_refs": [],
        "protected_artifact_refs": [],
        "boundary_flags": {
            "candidate_only": True,
            "not_fact": True,
            "not_runtime_output": True,
            "not_output_adapter_output": True,
            "not_semantic_output": True,
            "not_navigation_action_speech": True,
        },
        "readiness_effect": {
            "runtime_ready": False,
            "output_adapter_ready": False,
            "semantic_layer_ready": False,
            "fact_write_ready": False,
            "navigation_action_speech_ready": False,
        },
        "testboard_protection": {
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
        },
    }


def _demo_street_scene_trajectories(frame_count: int = 120) -> tuple[List[List[float]], List[List[float]], List[str]]:
    """Synthetic Luna street scene — mild drift on estimated path."""
    gt: List[List[float]] = []
    est: List[List[float]] = []
    states: List[str] = []
    for i in range(frame_count):
        t = i * 0.1
        x = 0.35 * t
        y = 0.08 * math.sin(t * 0.4)
        z = 0.0
        gt.append([round(x, 4), round(y, 4), round(z, 4)])
        drift = 0.002 * i
        est.append([round(x + drift + 0.01 * math.sin(i * 0.15), 4), round(y + 0.005, 4), 0.0])
        states.append("OK" if i < 115 else "LOST")
    return est, gt, states


def build_demo_envelope(*, downsample: int = 1) -> Dict[str, Any]:
    est, gt, states = _demo_street_scene_trajectories()
    slam_run = {
        "backend": "orb_slam",
        "dataset": "luna_street_scene_v1",
        "trajectory": est,
        "ground_truth_trajectory": gt,
        "per_frame_tracking_state": states,
        "tracking_state": "OK",
        "keyframes": [0, 30, 60, 90, 115],
        "map": {"point_count_candidate": 18420, "loop_edges_candidate": 3},
        "map_consistency_score": 0.87,
        "loop_closure_correct": True,
        "loop_closure_stability": 0.91,
        "loop_closure_frames": [90],
        "motion_blur_sensitivity": 0.19,
        "low_light_degradation": 0.14,
        "input_asset_refs": [
            "capabilities/test_assets/p1/slam/luna_street_scene_v1/sequence_manifest_v1.json",
        ],
    }
    envelope = adapt_slam_run_to_envelope(
        slam_run,
        config=SlamAdapterConfig(backend="orb_slam", dataset="luna_street_scene_v1"),
        envelope_id="slam_orb_luna_street_scene_envelope_example_v1",
    )
    if downsample > 1:
        _downsample_envelope_trajectories(envelope, downsample)
    return envelope


def _downsample_envelope_trajectories(envelope: Dict[str, Any], step: int) -> None:
    pred = envelope.get("muep", {}).get("output", {}).get("prediction", {})
    if pred.get("trajectory"):
        pred["trajectory"] = pred["trajectory"][::step]
    diag = envelope.get("diagnostics") or {}
    if diag.get("diagnostics", {}).get("error_curve"):
        diag["diagnostics"]["error_curve"] = diag["diagnostics"]["error_curve"][::step]
    if diag.get("alignment", {}).get("aligned_trajectory"):
        diag["alignment"]["aligned_trajectory"] = diag["alignment"]["aligned_trajectory"][::step]
    for layer in envelope.get("visualization_layers") or []:
        lt = layer.get("layer_type")
        if lt == "trajectory":
            for key in ("trajectory_estimated", "trajectory_ground_truth", "trajectory_raw_estimated"):
                if layer.get(key):
                    layer[key] = layer[key][::step]
        elif lt == "error_curve" and layer.get("error_curve"):
            layer["error_curve"] = layer["error_curve"][::step]
        elif lt == "drift_heatmap":
            pass  # segments already aggregated


def write_demo_example(output_path: Optional[Path] = None, *, slim: bool = False) -> Path:
    default_name = (
        "slam_orb_luna_street_scene_envelope_example_slim_v1.json"
        if slim
        else "slam_orb_luna_street_scene_envelope_example_v1.json"
    )
    out = output_path or (
        Path(__file__).resolve().parents[2]
        / "examples"
        / default_name
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = build_demo_envelope(downsample=6 if slim else 1)
    if slim:
        payload["envelope_id"] = "slam_orb_luna_street_scene_envelope_example_slim_v1"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SLAM Evaluation Adapter V1 demo writer")
    parser.add_argument("--slim", action="store_true", help="Write downsampled envelope for static site")
    args = parser.parse_args()
    path = write_demo_example(slim=args.slim)
    print(f"Wrote SLAM example envelope: {path}")
