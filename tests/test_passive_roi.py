# -*- coding: utf-8 -*-
"""
被动 ROI v0 单元测试
"""

import numpy as np
import cv2
import pytest

from vision_perception_b1.passive_roi import compute_passive_roi_count


def test_passive_roi_empty():
    """无 diff 时返回 0"""
    diff = np.zeros((100, 100), dtype=np.uint8)
    assert compute_passive_roi_count(diff, 10000) == 0


def test_passive_roi_single_region():
    """单个运动区域（≥1%）"""
    diff = np.zeros((100, 100), dtype=np.uint8)
    # 10x10 = 100 像素 = 1%
    diff[10:20, 10:20] = 50
    assert compute_passive_roi_count(diff, 10000) == 1


def test_passive_roi_two_regions():
    """两个运动区域"""
    diff = np.zeros((100, 100), dtype=np.uint8)
    diff[10:20, 10:20] = 50  # 1%
    diff[50:60, 50:60] = 50  # 1%
    assert compute_passive_roi_count(diff, 10000) == 2


def test_passive_roi_small_region_filtered():
    """过小区域被过滤"""
    diff = np.zeros((100, 100), dtype=np.uint8)
    # 5x5 = 25 像素 < 1%
    diff[10:15, 10:15] = 50
    assert compute_passive_roi_count(diff, 10000) == 0


def test_passive_roi_clamp_max():
    """超过 5 个区域时 clamp 到 5"""
    diff = np.zeros((200, 200), dtype=np.uint8)
    # 6 个 20x20 区域 = 各 4%
    for i in range(6):
        y, x = (i // 3) * 60, (i % 3) * 60
        diff[y : y + 20, x : x + 20] = 50
    assert compute_passive_roi_count(diff, 40000) == 5


def test_passive_roi_zero_area():
    """frame_area=0 时返回 0"""
    diff = np.zeros((100, 100), dtype=np.uint8)
    diff[10:20, 10:20] = 50
    assert compute_passive_roi_count(diff, 0) == 0
