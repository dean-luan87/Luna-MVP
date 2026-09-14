#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2/A3 Isolation：占位脚手架，作为 D0.1 准入门槛。
当前未做 D0.1（真实重算决策），无法在不动 runtime 的前提下验证 A3 隔离；
先 skip 并写明原因，待 D0.1 落地后改为正式测试。
"""
import sys


def test_a3_isolation_placeholder():
    """D0.1 未落地前：SimRunner 为 passthrough，无 A3 调用；无法验证隔离。"""
    import pytest
    pytest.skip(
        "D0.1 not implemented: no real A3 recompute in sim_runner, cannot assert A3 isolation without touching runtime. "
        "This test will be enabled when D0.1 provides deterministic replay that invokes decision logic in isolation."
    )


if __name__ == "__main__":
    print("test_a3_isolation: skipped (D0.1 not implemented)")
    sys.exit(0)
