# -*- coding: utf-8 -*-
"""
Path v0（Passive Path Instability）

设计定位：运动方向一致性差的程度
只回答一个问题：当前运动是否沿稳定路径，还是多方向/不稳定？

约束：
- 只读，不控制
- 不抬 safety_level
- 不直接切 control_mode
- 仅入 complexity_raw
- 与 ROI、motion 解耦可观测

来源：optical flow 的方向一致性统计
"""

from __future__ import annotations

import numpy as np
import cv2
from typing import Optional, Tuple

# v0 参数
NUM_BINS = 18  # 0-180° 分 18 档，每档 10°
MIN_FLOW_MAG = 1.0  # 只统计幅度 > 1 像素的向量

# Branch v0 参数
BRANCH_NUM_BINS = 8  # 方向直方图 bin 数（建议 8 或 12）
BRANCH_BIN_RATIO_THRESH = 0.15  # bin 占比 >= 此值视为"有效方向"


def _compute_flow_angles(prev_gray: np.ndarray, curr_gray: np.ndarray) -> Optional[tuple]:
    """
    计算光流方向角度（0-180°），供 Path 和 Branch 复用。
    Returns:
        (angles_deg, total_count) 或 None（失败时）
    """
    if prev_gray is None or curr_gray is None:
        return None
    if prev_gray.shape != curr_gray.shape:
        return None

    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        pyr_scale=0.5, levels=2, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0,
    )
    fx, fy = flow[:, :, 0], flow[:, :, 1]
    mag = np.sqrt(fx * fx + fy * fy)
    mask = mag >= MIN_FLOW_MAG
    if not np.any(mask):
        return None

    fx_valid = fx[mask]
    fy_valid = fy[mask]
    angle_deg = np.degrees(np.arctan2(fy_valid, fx_valid))
    angle_deg = (angle_deg + 180) % 180
    return (angle_deg, len(angle_deg))


def compute_path_instability(
    prev_gray: np.ndarray,
    curr_gray: np.ndarray,
    *,
    num_bins: int = NUM_BINS,
    min_flow_mag: float = MIN_FLOW_MAG,
) -> float:
    """
    从光流计算 path_instability = 1 - dominant_ratio。

    Args:
        prev_gray: 上一帧灰度
        curr_gray: 当前帧灰度
        num_bins: 方向直方图 bin 数（0-180°）
        min_flow_mag: 最小流幅阈值，过滤静态/噪声

    Returns:
        path_instability: 0.0 ~ 1.0
    """
    res = _compute_flow_angles(prev_gray, curr_gray)
    if res is None:
        return 0.0
    angle_deg, total = res
    if total <= 0:
        return 0.0

    bin_edges = np.linspace(0, 180, num_bins + 1)
    hist, _ = np.histogram(angle_deg, bins=bin_edges)
    dominant_ratio = float(np.max(hist)) / total
    path_instability = 1.0 - dominant_ratio
    return float(np.clip(path_instability, 0.0, 1.0))


def compute_branch_load(
    prev_gray: np.ndarray,
    curr_gray: np.ndarray,
    *,
    num_bins: int = BRANCH_NUM_BINS,
    bin_ratio_thresh: float = BRANCH_BIN_RATIO_THRESH,
) -> float:
    """
    Branch v0：有效运动方向的数量密度。
    从方向直方图的多峰性计算 branch_load。

    Args:
        prev_gray: 上一帧灰度
        curr_gray: 当前帧灰度
        num_bins: 方向量化 bin 数（建议 8 或 12）
        bin_ratio_thresh: bin 占比 >= 此值视为有效方向

    Returns:
        branch_load: 0.0 ~ 1.0
        - 1 个主方向 → 0
        - 2–4 个方向 → 逐步上升
        - ≥4 个方向 → 饱和
    """
    res = _compute_flow_angles(prev_gray, curr_gray)
    if res is None:
        return 0.0
    angle_deg, total = res
    if total <= 0:
        return 0.0

    bin_edges = np.linspace(0, 180, num_bins + 1)
    hist, _ = np.histogram(angle_deg, bins=bin_edges)
    branch_count = int(np.sum(hist / total >= bin_ratio_thresh))
    branch_load = np.clip((branch_count - 1) / 3.0, 0.0, 1.0)
    return float(branch_load)


def compute_path_and_branch(
    prev_gray: np.ndarray,
    curr_gray: np.ndarray,
) -> Tuple[float, float]:
    """
    单次光流计算，同时返回 path_instability 和 branch_load。
    供 pipeline 复用，避免重复光流计算。
    """
    res = _compute_flow_angles(prev_gray, curr_gray)
    if res is None:
        return (0.0, 0.0)
    angle_deg, total = res
    if total <= 0:
        return (0.0, 0.0)

    # Path: 18 bins
    bin_edges_18 = np.linspace(0, 180, NUM_BINS + 1)
    hist_18, _ = np.histogram(angle_deg, bins=bin_edges_18)
    dominant_ratio = float(np.max(hist_18)) / total
    path_instability = float(np.clip(1.0 - dominant_ratio, 0.0, 1.0))

    # Branch: 8 bins
    bin_edges_8 = np.linspace(0, 180, BRANCH_NUM_BINS + 1)
    hist_8, _ = np.histogram(angle_deg, bins=bin_edges_8)
    branch_count = int(np.sum(hist_8 / total >= BRANCH_BIN_RATIO_THRESH))
    branch_load = float(np.clip((branch_count - 1) / 3.0, 0.0, 1.0))

    return (path_instability, branch_load)
