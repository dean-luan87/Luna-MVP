# -*- coding: utf-8 -*-
"""ATE / drift / trajectory utilities for SLAM evaluation adapter V1."""

from __future__ import annotations

import math
from typing import Iterable, List, Sequence


def _as_xyz(point: Sequence[float]) -> List[float]:
    if len(point) < 3:
        raise ValueError("trajectory point must have at least x,y,z")
    return [float(point[0]), float(point[1]), float(point[2])]


def _vec_add(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [a[i] + b[i] for i in range(3)]


def _vec_sub(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [a[i] - b[i] for i in range(3)]


def _vec_scale(a: Sequence[float], s: float) -> List[float]:
    return [a[i] * s for i in range(3)]


def _vec_norm(a: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def _centroid(points: Sequence[Sequence[float]]) -> List[float]:
    if not points:
        return [0.0, 0.0, 0.0]
    acc = [0.0, 0.0, 0.0]
    for p in points:
        xyz = _as_xyz(p)
        acc = _vec_add(acc, xyz)
    n = float(len(points))
    return [acc[i] / n for i in range(3)]


def align_trajectories_translation(
    estimated: Sequence[Sequence[float]],
    ground_truth: Sequence[Sequence[float]],
) -> List[List[float]]:
    """Translation-only alignment: shift estimate so centroids match GT."""
    est = [_as_xyz(p) for p in estimated]
    gt = [_as_xyz(p) for p in ground_truth]
    n = min(len(est), len(gt))
    if n == 0:
        return []
    est_n = est[:n]
    gt_n = gt[:n]
    c_est = _centroid(est_n)
    c_gt = _centroid(gt_n)
    delta = _vec_sub(c_gt, c_est)
    return [_vec_add(p, delta) for p in est_n]


def compute_ate_rmse_m(
    estimated: Sequence[Sequence[float]],
    ground_truth: Sequence[Sequence[float]],
    *,
    align: bool = True,
) -> float:
    """Absolute Trajectory Error as RMSE in meters after centroid alignment."""
    est = [_as_xyz(p) for p in estimated]
    gt = [_as_xyz(p) for p in ground_truth]
    n = min(len(est), len(gt))
    if n == 0:
        return float("nan")
    if align:
        est = align_trajectories_translation(est, gt)
        gt = gt[:n]
    else:
        est = est[:n]
        gt = gt[:n]
    sq = 0.0
    for e, g in zip(est, gt):
        d = _vec_sub(e, g)
        sq += _vec_norm(d) ** 2
    return math.sqrt(sq / n)


def compute_path_length_m(trajectory: Sequence[Sequence[float]]) -> float:
    pts = [_as_xyz(p) for p in trajectory]
    if len(pts) < 2:
        return 0.0
    total = 0.0
    for i in range(1, len(pts)):
        total += _vec_norm(_vec_sub(pts[i], pts[i - 1]))
    return total


def compute_drift_rate(ate_m: float, path_length_m: float) -> float:
    if path_length_m <= 1e-9:
        return float("inf") if ate_m > 0 else 0.0
    return ate_m / path_length_m


def compute_tracking_stability(tracking_states: Iterable[str]) -> float:
    states = list(tracking_states)
    if not states:
        return 0.0
    ok = sum(1 for s in states if str(s).upper() in {"OK", "TRACKED", "TRACKING"})
    return ok / len(states)


def compute_trajectory_smoothness(trajectory: Sequence[Sequence[float]]) -> float:
    """Higher is smoother. Based on inverse mean heading change (normalized)."""
    pts = [_as_xyz(p) for p in trajectory]
    if len(pts) < 3:
        return 1.0
    angles: List[float] = []
    for i in range(1, len(pts) - 1):
        v1 = _vec_sub(pts[i], pts[i - 1])
        v2 = _vec_sub(pts[i + 1], pts[i])
        n1 = _vec_norm(v1)
        n2 = _vec_norm(v2)
        if n1 < 1e-9 or n2 < 1e-9:
            continue
        cos_a = sum(v1[j] * v2[j] for j in range(3)) / (n1 * n2)
        cos_a = max(-1.0, min(1.0, cos_a))
        angles.append(math.acos(cos_a))
    if not angles:
        return 1.0
    mean_angle = sum(angles) / len(angles)
    # pi/2 -> 0 smoothness, 0 rad -> 1
    return max(0.0, 1.0 - (mean_angle / (math.pi / 2)))


def ate_to_score(ate_m: float, ate_ref_m: float = 0.5) -> float:
    if ate_ref_m <= 0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - ate_m / ate_ref_m))


def drift_to_penalty(drift_rate: float, drift_ref: float = 0.05) -> float:
    if drift_ref <= 0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - drift_rate / drift_ref))
