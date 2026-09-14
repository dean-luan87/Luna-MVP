# -*- coding: utf-8 -*-
"""Procrustes / Sim(3) GT alignment for SLAM diagnostic engine."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence


def _as_xyz(point: Sequence[float]) -> List[float]:
    if len(point) < 3:
        raise ValueError("trajectory point must have at least x,y,z")
    return [float(point[0]), float(point[1]), float(point[2])]


def _centroid(points: Sequence[Sequence[float]]) -> List[float]:
    if not points:
        return [0.0, 0.0, 0.0]
    acc = [0.0, 0.0, 0.0]
    for p in points:
        xyz = _as_xyz(p)
        for i in range(3):
            acc[i] += xyz[i]
    n = float(len(points))
    return [acc[i] / n for i in range(3)]


def _mat_mul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    rows, cols, inner = len(a), len(b[0]), len(b)
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            for j in range(cols):
                out[i][j] += a[i][k] * b[k][j]
    return out


def _mat_vec_mul(m: List[List[float]], v: List[float]) -> List[float]:
    return [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]


def _transpose(m: List[List[float]]) -> List[List[float]]:
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def _vec_sub(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [a[i] - b[i] for i in range(len(a))]


def _vec_add(a: Sequence[float], b: Sequence[float]) -> List[float]:
    return [a[i] + b[i] for i in range(len(a))]


def _vec_scale(a: Sequence[float], s: float) -> List[float]:
    return [a[i] * s for i in range(len(a))]


def _vec_norm(a: Sequence[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def _cross_covariance(
    pred_c: Sequence[Sequence[float]],
    gt_c: Sequence[Sequence[float]],
) -> List[List[float]]:
    n = len(pred_c)
    h = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    for p, g in zip(pred_c, gt_c):
        for i in range(3):
            for j in range(3):
                h[i][j] += p[i] * g[j]
    inv_n = 1.0 / max(n, 1)
    return [[h[i][j] * inv_n for j in range(3)] for i in range(3)]


def _svd_3x3(m: List[List[float]]) -> tuple[List[List[float]], List[float], List[List[float]]]:
    """3x3 SVD via numpy when available; otherwise symmetric eigen fallback for R only."""
    try:
        import numpy as np  # type: ignore

        a = np.array(m, dtype=float)
        u, s, vt = np.linalg.svd(a)
        return u.tolist(), s.tolist(), vt.tolist()
    except Exception:
        return _svd_3x3_jacobi(m)


def _svd_3x3_jacobi(m: List[List[float]]) -> tuple[List[List[float]], List[float], List[List[float]]]:
    """Jacobi SVD for 3x3 — sufficient for Procrustes."""
    a = [row[:] for row in m]
    u = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    v = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    for _ in range(30):
        p, q = 0, 1
        max_val = abs(a[p][q])
        for i in range(3):
            for j in range(i + 1, 3):
                if abs(a[i][j]) > max_val:
                    max_val = abs(a[i][j])
                    p, q = i, j
        if max_val < 1e-12:
            break
        phi = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(phi), math.sin(phi)
        for i in range(3):
            ap, aq = a[i][p], a[i][q]
            a[i][p] = c * ap - s * aq
            a[i][q] = s * ap + c * aq
        for i in range(3):
            ap, aq = a[p][i], a[q][i]
            a[p][i] = c * ap - s * aq
            a[q][i] = s * ap + c * aq
        for i in range(3):
            up, uq = u[i][p], u[i][q]
            u[i][p] = c * up - s * uq
            u[i][q] = s * up + c * uq
        for i in range(3):
            vp, vq = v[p][i], v[q][i]
            v[p][i] = c * vp - s * vq
            v[q][i] = s * vp + c * vq
    s = [abs(a[i][i]) for i in range(3)]
    vt = _transpose(v)
    return u, s, vt


@dataclass
class ProcrustesAlignmentResult:
    aligned_trajectory: List[List[float]]
    rotation_matrix: List[List[float]]
    translation: List[float]
    scale: float
    residual_rmse_m: float
    method: str


def align_procrustes(
    trajectory_pred: Sequence[Sequence[float]],
    trajectory_gt: Sequence[Sequence[float]],
    *,
    with_scale: bool = True,
) -> ProcrustesAlignmentResult:
    """
    Sim(3) alignment: minimize || s * R * P_pred + t - P_gt ||.
    Falls back to translation-only if trajectories are empty or degenerate.
    """
    pred = [_as_xyz(p) for p in trajectory_pred]
    gt = [_as_xyz(p) for p in trajectory_gt]
    n = min(len(pred), len(gt))
    if n < 2:
        return ProcrustesAlignmentResult(
            aligned_trajectory=pred[:n],
            rotation_matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            translation=[0.0, 0.0, 0.0],
            scale=1.0,
            residual_rmse_m=0.0,
            method="identity",
        )

    pred_n = pred[:n]
    gt_n = gt[:n]
    c_pred = _centroid(pred_n)
    c_gt = _centroid(gt_n)
    pred_c = [_vec_sub(p, c_pred) for p in pred_n]
    gt_c = [_vec_sub(g, c_gt) for g in gt_n]

    h = _cross_covariance(pred_c, gt_c)
    u, _s_vals, vt = _svd_3x3(h)
    # H = U S V^T  =>  R = U V^T (Kabsch / Umeyama)
    r = _mat_mul(u, vt)
    det = (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )
    if det < 0:
        u[2] = [-x for x in u[2]]
        r = _mat_mul(u, vt)

    scale = 1.0
    if with_scale:
        var_pred = sum(sum(p[i] * p[i] for i in range(3)) for p in pred_c) / n
        trace_s = sum(_s_vals)
        scale = trace_s / var_pred if var_pred > 1e-12 else 1.0

    aligned: List[List[float]] = []
    sq = 0.0
    t_vec = _vec_sub(c_gt, _vec_scale(_mat_vec_mul(r, c_pred), scale))
    for p, g in zip(pred_n, gt_n):
        rp = _mat_vec_mul(r, p)
        ap = _vec_add(_vec_scale(rp, scale), t_vec)
        aligned.append([round(ap[i], 6) for i in range(3)])
        d = _vec_sub(ap, g)
        sq += _vec_norm(d) ** 2
    rmse = math.sqrt(sq / n)
    t = t_vec

    return ProcrustesAlignmentResult(
        aligned_trajectory=aligned,
        rotation_matrix=r,
        translation=[round(t[i], 6) for i in range(3)],
        scale=round(scale, 6),
        residual_rmse_m=round(rmse, 6),
        method="procrustes_sim3" if with_scale else "procrustes_se3",
    )
