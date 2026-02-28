# -*- coding: utf-8 -*-
"""Stage 2: 定点舍入策略稳定——round half away from zero，± 与 0.5 边界一致。"""
import os
import pytest

# 确保使用定点模块
os.environ["A3_FIXEDPOINT"] = "1"

from runtime.a3_fixedpoint import SCORE_SCALE, q, dq


def test_round_half_away_from_zero_positive():
    """0.5 -> 500 (half away from zero)；epsilon 消除边界抖动后 0.5005 -> 501。"""
    assert q(0.5) == 500
    assert q(0.501) == 501
    assert q(0.499) == 499
    assert q(0.5005) == 501


def test_round_half_away_from_zero_negative():
    """-0.5 -> -500 (away from zero)；epsilon 消除正半轴边界抖动。"""
    assert q(-0.5) == -500
    assert q(-0.501) == -501
    assert q(-0.499) == -499
    # -0.5001 更接近 -0.5，round-half-away-from-zero 得 -500
    assert q(-0.5001) == -500


def test_stable_boundary_3795_3800_3805():
    """阈值边界附近舍入稳定，不因浮点尾差在 0.38 两侧抖动。"""
    # 0.3795 -> 380 (half up)
    assert q(0.3795) == 380
    assert q(0.3800) == 380
    assert q(0.3805) == 381
    assert q(0.3794) == 379
    assert q(0.3806) == 381


def test_dq_roundtrip():
    """q(dq(i)) == i 对 [0, SCORE_SCALE] 内整数成立。"""
    for i in [0, 1, 500, 999, SCORE_SCALE]:
        assert q(dq(i)) == i


def test_zero_and_one():
    assert q(0.0) == 0
    assert q(1.0) == SCORE_SCALE
    assert dq(0) == 0.0
    assert dq(SCORE_SCALE) == 1.0


def test_non_finite():
    assert q(float("nan")) == 0
    assert q(float("inf")) == 0
    assert q(float("-inf")) == 0
