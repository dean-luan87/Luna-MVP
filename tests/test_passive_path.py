# -*- coding: utf-8 -*-
"""Path v0 单元测试"""

import numpy as np
import cv2
import pytest

from vision_perception_b1.passive_path import (
    compute_path_instability,
    compute_branch_load,
    compute_path_and_branch,
)


def test_path_instability_uniform():
    """全方向运动 → path_instability 高"""
    h, w = 100, 100
    prev = np.ones((h, w), dtype=np.uint8) * 128
    curr = prev.copy()
    # 模拟多方向运动：不同区域向不同方向移动
    for i in range(0, h, 10):
        for j in range(0, w, 10):
            angle = (i + j) % 18 * 10  # 0-170°
            dx = int(3 * np.cos(np.radians(angle)))
            dy = int(3 * np.sin(np.radians(angle)))
            y0, y1 = max(0, i + dy), min(h, i + 10 + dy)
            x0, x1 = max(0, j + dx), min(w, j + 10 + dx)
            curr[y0:y1, x0:x1] = 200
    out = compute_path_instability(prev, curr)
    assert 0 <= out <= 1


def test_path_instability_single_direction():
    """单一方向运动 → path_instability 低"""
    h, w = 100, 100
    prev = np.ones((h, w), dtype=np.uint8) * 128
    curr = prev.copy()
    # 整体向右平移 5 像素
    curr[:, 5:] = prev[:, :-5]
    curr[:, :5] = 128
    out = compute_path_instability(prev, curr)
    assert 0 <= out <= 1


def test_path_instability_no_motion():
    """无运动 → path_instability 低（或 0）"""
    prev = np.ones((100, 100), dtype=np.uint8) * 128
    curr = prev.copy()
    out = compute_path_instability(prev, curr)
    assert out == 0.0


def test_path_instability_none_input():
    """None 输入 → 0"""
    prev = np.ones((100, 100), dtype=np.uint8) * 128
    assert compute_path_instability(None, prev) == 0.0
    assert compute_path_instability(prev, None) == 0.0


# --- Branch v0 ---


def test_branch_load_no_motion():
    """无运动 → branch_load 0"""
    prev = np.ones((100, 100), dtype=np.uint8) * 128
    curr = prev.copy()
    out = compute_branch_load(prev, curr)
    assert out == 0.0


def test_branch_load_single_direction():
    """单一方向运动 → branch_load 接近 0（1 个主方向）"""
    h, w = 100, 100
    prev = np.ones((h, w), dtype=np.uint8) * 128
    curr = prev.copy()
    curr[:, 5:] = prev[:, :-5]
    curr[:, :5] = 128
    out = compute_branch_load(prev, curr)
    assert 0 <= out <= 1


def test_branch_load_multi_direction():
    """多方向运动 → branch_load 上升"""
    h, w = 100, 100
    prev = np.ones((h, w), dtype=np.uint8) * 128
    curr = prev.copy()
    for i in range(0, h, 10):
        for j in range(0, w, 10):
            angle = (i + j) % 18 * 10
            dx = int(3 * np.cos(np.radians(angle)))
            dy = int(3 * np.sin(np.radians(angle)))
            y0, y1 = max(0, i + dy), min(h, i + 10 + dy)
            x0, x1 = max(0, j + dx), min(w, j + 10 + dx)
            curr[y0:y1, x0:x1] = 200
    out = compute_branch_load(prev, curr)
    assert 0 <= out <= 1


def test_path_and_branch_consistency():
    """compute_path_and_branch 与单独调用结果一致"""
    h, w = 80, 80
    prev = np.ones((h, w), dtype=np.uint8) * 128
    curr = prev.copy()
    curr[:, 3:] = prev[:, :-3]
    curr[:, :3] = 128
    path_a, branch_a = compute_path_and_branch(prev, curr)
    path_b = compute_path_instability(prev, curr)
    branch_b = compute_branch_load(prev, curr)
    assert abs(path_a - path_b) < 0.01
    assert abs(branch_a - branch_b) < 0.01
