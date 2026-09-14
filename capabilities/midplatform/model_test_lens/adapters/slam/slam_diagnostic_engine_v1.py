# -*- coding: utf-8 -*-
"""SLAM Diagnostic Engine V1 — alignment, error curve, heatmap, failure timeline."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, Optional, Sequence

from capabilities.midplatform.model_test_lens.adapters.slam.ate_calculator_v1 import (
    compute_drift_rate,
    compute_path_length_m,
    compute_tracking_stability,
    drift_to_penalty,
)
from capabilities.midplatform.model_test_lens.adapters.slam.procrustes_alignment_v1 import (
    ProcrustesAlignmentResult,
    align_procrustes,
    _vec_norm,
    _vec_sub,
)
from capabilities.midplatform.model_test_lens.standards.muep.muep_scoring_v1 import clamp01

SLAM_DIAGNOSTIC_WEIGHTS_V2 = {
    "ate_score": 0.4,
    "stability": 0.2,
    "drift_penalty": 0.2,
    "diagnostic_penalty": 0.2,
}


def _as_xyz(point: Sequence[float]) -> List[float]:
    return [float(point[0]), float(point[1]), float(point[2]) if len(point) > 2 else 0.0]


def compute_frame_errors(
    aligned_pred: Sequence[Sequence[float]],
    trajectory_gt: Sequence[Sequence[float]],
) -> List[float]:
    n = min(len(aligned_pred), len(trajectory_gt))
    errors: List[float] = []
    for i in range(n):
        d = _vec_sub(_as_xyz(aligned_pred[i]), _as_xyz(trajectory_gt[i]))
        errors.append(_vec_norm(d))
    return errors


def compute_error_curve(
    aligned_pred: Sequence[Sequence[float]],
    trajectory_gt: Sequence[Sequence[float]],
    timestamps: Optional[Sequence[float]] = None,
) -> List[Dict[str, float]]:
    errors = compute_frame_errors(aligned_pred, trajectory_gt)
    curve: List[Dict[str, float]] = []
    for i, err in enumerate(errors):
        t = float(timestamps[i]) if timestamps and i < len(timestamps) else float(i)
        curve.append({"frame": i, "t": round(t, 4), "error": round(err, 6)})
    return curve


def compute_rpe_rmse_m(
    aligned_pred: Sequence[Sequence[float]],
    trajectory_gt: Sequence[Sequence[float]],
    delta: int = 1,
) -> float:
    """Relative Pose Error — mean translation delta error over delta frames."""
    n = min(len(aligned_pred), len(trajectory_gt))
    if n <= delta:
        return 0.0
    sq = 0.0
    count = 0
    for i in range(n - delta):
        dp = _vec_sub(_as_xyz(aligned_pred[i + delta]), _as_xyz(aligned_pred[i]))
        dg = _vec_sub(_as_xyz(trajectory_gt[i + delta]), _as_xyz(trajectory_gt[i]))
        d = _vec_sub(dp, dg)
        sq += _vec_norm(d) ** 2
        count += 1
    return math.sqrt(sq / count) if count else 0.0


def _error_to_color_class(error: float, low: float, high: float) -> str:
    if error <= low:
        return "low"
    if error >= high:
        return "high"
    return "mid"


def compute_drift_heatmap(
    error_curve: Sequence[Mapping[str, float]],
    trajectory_gt: Sequence[Sequence[float]],
    *,
    segment_count: int = 20,
) -> List[Dict[str, Any]]:
    """Trajectory segments colored by mean frame error (green/yellow/red)."""
    if not error_curve:
        return []
    n = len(error_curve)
    seg_n = min(segment_count, n)
    seg_size = max(1, n // seg_n)
    errors = [float(p["error"]) for p in error_curve]
    low = sorted(errors)[max(0, int(0.33 * len(errors)) - 1)]
    high = sorted(errors)[min(len(errors) - 1, int(0.66 * len(errors)))]

    heatmap: List[Dict[str, Any]] = []
    for s in range(seg_n):
        start = s * seg_size
        end = min(n, (s + 1) * seg_size) if s < seg_n - 1 else n
        if start >= end:
            continue
        seg_errors = errors[start:end]
        mean_err = sum(seg_errors) / len(seg_errors)
        traj_slice = trajectory_gt[start:end] if start < len(trajectory_gt) else []
        heatmap.append({
            "segment_index": s,
            "frame_start": start,
            "frame_end": end - 1,
            "t_start": error_curve[start].get("t", start),
            "t_end": error_curve[end - 1].get("t", end - 1),
            "mean_error": round(mean_err, 6),
            "max_error": round(max(seg_errors), 6),
            "color_class": _error_to_color_class(mean_err, low, high),
            "trajectory_segment": [[round(p[0], 4), round(p[1], 4)] for p in traj_slice],
        })
    return heatmap


def _slope(values: Sequence[float], window: int = 5) -> List[float]:
    slopes: List[float] = []
    for i in range(len(values)):
        if i < window:
            slopes.append(0.0)
            continue
        dy = values[i] - values[i - window]
        slopes.append(dy / window)
    return slopes


def build_failure_timeline(
    error_curve: Sequence[Mapping[str, float]],
    *,
    tracking_states: Optional[Sequence[str]] = None,
    keyframes: Optional[Sequence[int]] = None,
    loop_closure_frames: Optional[Sequence[int]] = None,
    error_spike_threshold: float = 0.05,
    slope_threshold: float = 0.008,
) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    errors = [float(p["error"]) for p in error_curve]
    slopes = _slope(errors)

    for i, pt in enumerate(error_curve):
        t = pt.get("t", i)
        frame = int(pt.get("frame", i))
        if i > 0 and errors[i] - errors[i - 1] > error_spike_threshold:
            events.append({
                "t": t,
                "frame": frame,
                "event_type": "error_spike",
                "label": "tracking degradation",
                "severity": "medium",
                "error": errors[i],
            })
        if slopes[i] > slope_threshold:
            events.append({
                "t": t,
                "frame": frame,
                "event_type": "localization_break",
                "label": "localization break (error slope rise)",
                "severity": "high",
                "slope": round(slopes[i], 6),
            })

    if tracking_states:
        prev_ok = True
        for i, st in enumerate(tracking_states):
            ok = str(st).upper() in {"OK", "TRACKED", "TRACKING"}
            if prev_ok and not ok:
                t = error_curve[i].get("t", i) if i < len(error_curve) else float(i)
                events.append({
                    "t": t,
                    "frame": i,
                    "event_type": "tracking_lost",
                    "label": "tracking lost",
                    "severity": "critical",
                })
            if not prev_ok and ok:
                t = error_curve[i].get("t", i) if i < len(error_curve) else float(i)
                events.append({
                    "t": t,
                    "frame": i,
                    "event_type": "relocalization",
                    "label": "re-localization attempt",
                    "severity": "medium",
                })
            prev_ok = ok

    for kf in keyframes or []:
        if kf < len(error_curve):
            events.append({
                "t": error_curve[kf].get("t", kf),
                "frame": kf,
                "event_type": "keyframe",
                "label": "keyframe",
                "severity": "info",
            })

    for lf in loop_closure_frames or []:
        if lf < len(error_curve):
            before = errors[max(0, lf - 3):lf]
            after = errors[lf:min(len(errors), lf + 3)]
            reduced = after and before and (sum(after) / len(after)) < (sum(before) / len(before)) - 0.01
            events.append({
                "t": error_curve[lf].get("t", lf),
                "frame": lf,
                "event_type": "loop_closure_failure" if not reduced else "loop_closure_success",
                "label": "loop closure failure" if not reduced else "loop closure correction",
                "severity": "high" if not reduced else "low",
            })

    events.sort(key=lambda e: (e.get("t", 0), e.get("frame", 0)))
    return events


def classify_failure_modes_diagnostic(
    *,
    drift_rate: float,
    tracking_stability: float,
    error_curve: Sequence[Mapping[str, float]],
    timeline: Sequence[Mapping[str, Any]],
    loop_closure_ok: bool,
    drift_threshold: float = 0.03,
    stability_threshold: float = 0.7,
) -> List[str]:
    modes: List[str] = []
    if drift_rate > drift_threshold:
        modes.append("short_term_drift" if drift_rate < drift_threshold * 2 else "drift_failure")
    if tracking_stability < stability_threshold:
        modes.append("tracking_lost")
    loc_breaks = [e for e in timeline if e.get("event_type") == "localization_break"]
    if loc_breaks:
        modes.append("localization_break")
    loop_fail = [e for e in timeline if e.get("event_type") == "loop_closure_failure"]
    if loop_fail or not loop_closure_ok:
        modes.append("loop_closure_failure")
    spikes = [e for e in timeline if e.get("event_type") == "error_spike"]
    if len(spikes) >= 3:
        modes.append("boundary_instability")
    if error_curve:
        tail = [float(p["error"]) for p in error_curve[-max(1, len(error_curve) // 5):]]
        head = [float(p["error"]) for p in error_curve[:max(1, len(error_curve) // 5)]]
        if tail and head and (sum(tail) / len(tail)) > (sum(head) / len(head)) * 1.5:
            if "short_term_drift" not in modes:
                modes.append("short_term_drift")
    return list(dict.fromkeys(modes))


def compute_diagnostic_penalty(
    error_curve: Sequence[Mapping[str, float]],
    timeline: Sequence[Mapping[str, Any]],
    *,
    loop_closure_ok: bool,
) -> float:
    """Higher is better (penalty inverted to score). 1.0 = clean, 0.0 = severe."""
    if not error_curve:
        return 1.0
    errors = [float(p["error"]) for p in error_curve]
    mean_e = sum(errors) / len(errors)
    spike_count = sum(1 for e in timeline if e.get("event_type") == "error_spike")
    failure_count = sum(
        1 for e in timeline
        if e.get("event_type") in {"tracking_lost", "localization_break", "loop_closure_failure"}
    )
    loop_severity = 0.0 if loop_closure_ok else 0.35
    spike_pen = min(0.4, spike_count * 0.08)
    fail_pen = min(0.4, failure_count * 0.12)
    err_pen = min(0.3, mean_e / 0.5)
    penalty = clamp01(spike_pen + fail_pen + loop_severity + err_pen)
    return clamp01(1.0 - penalty)


def compute_slam_score_v2(
    ate_m: float,
    stability: float,
    drift_rate: float,
    diagnostic_penalty_score: float,
    *,
    ate_ref_m: float = 0.5,
    drift_ref: float = 0.05,
) -> float:
    from capabilities.midplatform.model_test_lens.adapters.slam.ate_calculator_v1 import ate_to_score

    ate_score = ate_to_score(ate_m, ate_ref_m)
    drift_pen = drift_to_penalty(drift_rate, drift_ref)
    w = SLAM_DIAGNOSTIC_WEIGHTS_V2
    return clamp01(
        w["ate_score"] * ate_score
        + w["stability"] * clamp01(stability)
        + w["drift_penalty"] * drift_pen
        + w["diagnostic_penalty"] * clamp01(diagnostic_penalty_score)
    )


def run_slam_diagnostics(
    slam_input: Mapping[str, Any],
    *,
    segment_count: int = 20,
    ate_ref_m: float = 0.5,
    drift_ref: float = 0.05,
) -> Dict[str, Any]:
    """
    Full diagnostic pass from SLAM envelope-style input.

    Expected keys: trajectory_pred / trajectory, trajectory_gt / ground_truth_trajectory,
    timestamps, per_frame_tracking_state, keyframes, loop_closure_frames, metadata.
    """
    pred = slam_input.get("trajectory_pred") or slam_input.get("trajectory") or []
    gt = slam_input.get("trajectory_gt") or slam_input.get("ground_truth_trajectory") or []
    timestamps = slam_input.get("timestamps")
    tracking_states = slam_input.get("per_frame_tracking_state") or []
    keyframes = slam_input.get("keyframes") or []
    loop_closure_frames = slam_input.get("loop_closure_frames") or []
    loop_closure_ok = bool(slam_input.get("loop_closure_correct", True))
    metadata = dict(slam_input.get("metadata") or {})

    alignment: ProcrustesAlignmentResult = align_procrustes(pred, gt, with_scale=True)
    error_curve = compute_error_curve(alignment.aligned_trajectory, gt, timestamps)
    ate_m = alignment.residual_rmse_m
    rpe_m = compute_rpe_rmse_m(alignment.aligned_trajectory, gt)
    path_len = compute_path_length_m(gt or pred)
    drift_rate = compute_drift_rate(ate_m, path_len)
    stability = compute_tracking_stability(tracking_states) if tracking_states else 1.0
    heatmap = compute_drift_heatmap(error_curve, gt, segment_count=segment_count)
    timeline = build_failure_timeline(
        error_curve,
        tracking_states=tracking_states,
        keyframes=keyframes,
        loop_closure_frames=loop_closure_frames,
    )
    diag_penalty_score = compute_diagnostic_penalty(error_curve, timeline, loop_closure_ok=loop_closure_ok)
    failure_modes = classify_failure_modes_diagnostic(
        drift_rate=drift_rate,
        tracking_stability=stability,
        error_curve=error_curve,
        timeline=timeline,
        loop_closure_ok=loop_closure_ok,
    )
    slam_score = compute_slam_score_v2(
        ate_m, stability, drift_rate, diag_penalty_score,
        ate_ref_m=ate_ref_m, drift_ref=drift_ref,
    )

    return {
        "engine_version": "slam_diagnostic_engine_v1",
        "alignment": {
            "method": alignment.method,
            "scale": alignment.scale,
            "translation": alignment.translation,
            "rotation_matrix": alignment.rotation_matrix,
            "residual_rmse_m": alignment.residual_rmse_m,
            "aligned_trajectory": alignment.aligned_trajectory,
        },
        "metrics": {
            "ATE": round(ate_m, 6),
            "RPE": round(rpe_m, 6),
            "drift_rate": round(drift_rate, 6),
            "tracking_stability": round(stability, 4),
            "slam_score_v2": round(slam_score, 4),
            "diagnostic_penalty_score": round(diag_penalty_score, 4),
        },
        "diagnostics": {
            "error_curve": error_curve,
            "drift_heatmap": heatmap,
            "failure_timeline": timeline,
        },
        "failure_modes": failure_modes,
        "metadata": metadata,
        "scoring_weights": dict(SLAM_DIAGNOSTIC_WEIGHTS_V2),
    }
