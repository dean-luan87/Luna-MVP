#!/usr/bin/env python3
"""B2 view_conf gate：k=1,floor=0.5 与旧逻辑 0.5+0.5*view_conf 在 0/0.6/1.0 三点对齐（允许 1e-6）。"""
import pytest

from a3.engine import _view_conf_gate


def test_view_conf_gate_regression():
    """k=1, floor=0.5 等价于旧逻辑 0.5 + 0.5*view_conf"""
    floor, k = 0.5, 1.0
    for vc in (0.0, 0.6, 1.0):
        legacy = 0.5 + 0.5 * vc
        gate = _view_conf_gate(vc, floor, k)
        assert abs(gate - legacy) < 1e-6, "vc=%s legacy=%s gate=%s" % (vc, legacy, gate)
