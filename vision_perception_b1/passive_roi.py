# -*- coding: utf-8 -*-
"""
被动 ROI v0（Passive ROI v0）

设计定位：基于运动/变化的「候选区域计数器」
只回答一个问题：当前画面里，有多少个「可能值得关注的区域」？

约束：
- 不分类（人/车/物）
- 不学习
- 不进 C1/C2
- 不抬 safety
- 不产生行为
- 不生成真正 ROI 对象（只生成 count）

来源：motion / frame diff 的空间分布
"""

from __future__ import annotations

import numpy as np
import cv2
# v0 参数（写死）
MIN_AREA_RATIO = 0.01  # 占画面 ≥1%
MAX_ROI_COUNT = 5
DIFF_THRESHOLD = 20  # 帧差二值化阈值（0-255）


def compute_passive_roi_count(
    diff_map: np.ndarray,
    frame_area: int,
    *,
    min_area_ratio: float = MIN_AREA_RATIO,
    max_roi_count: int = MAX_ROI_COUNT,
    diff_threshold: int = DIFF_THRESHOLD,
) -> int:
    """
    从 diff_map 计算被动 ROI 数量。

    Args:
        diff_map: 帧差图（灰度，0-255），来自 cv2.absdiff
        frame_area: 画面面积 H * W
        min_area_ratio: 最小区域占比（默认 0.01）
        max_roi_count: 最大计数（默认 5）
        diff_threshold: 二值化阈值（默认 20）

    Returns:
        roi_count: 0 ~ max_roi_count
    """
    if frame_area <= 0:
        return 0
    if diff_map is None or diff_map.size == 0:
        return 0

    # 1. 阈值 → binary mask
    _, binary = cv2.threshold(diff_map, diff_threshold, 255, cv2.THRESH_BINARY)

    # 2. 连通域分析
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary, connectivity=8
    )
    # num_labels 包含背景(0)，有效区域从 1 开始
    # stats: [x, y, w, h, area]

    # 3. 过滤过小区域
    valid = 0
    for i in range(1, num_labels):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area / frame_area >= min_area_ratio:
            valid += 1

    # 4. clamp
    return min(valid, max_roi_count)
