#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TC-05: 等待态安全行为测试（半自动 / 模拟）

目标：验证 waiting_state 下只允许 INTERVENE

优先级：第二优先级（半自动 / 模拟）
"""

import pytest
from tests.v1_8_1.conftest import SystemRunner


def test_waiting_state_no_background_output(system_runner):
    """
    TC-05: 等待态安全行为
    
    测试范围：
    - waiting_state=true 时，不输出 BACKGROUND
    - waiting_state=true 时，不输出 CONFIRM
    - 只允许 INTERVENE
    """
    # 设置 observer_mode=true
    system_runner.set_config(OBSERVER_MODE_ENABLED=True)
    
    # 模拟等待态场景
    # TODO: 实现等待态场景模拟
    # result = system_runner.run_scenario(waiting_state=True)
    
    # 验证：不输出 BACKGROUND
    # assert "background" not in result.get("outputs", [])
    
    # 验证：不输出 CONFIRM
    # assert "confirm" not in result.get("outputs", [])
    
    # 验证：只允许 INTERVENE（如果有危险）
    # if result.get("has_danger"):
    #     assert result["vision_output_state"] == "intervene"


def test_waiting_state_equivalence_when_disabled(system_runner):
    """
    TC-05 扩展：observer_mode=false 时，等待态与 v1.8 一致
    
    测试范围：
    - observer_mode=false 时，等待态行为与 v1.8 完全一致
    """
    # 设置 observer_mode=false
    system_runner.set_config(OBSERVER_MODE_ENABLED=False)
    
    # 运行 v1.8 基线版本
    result_v18 = system_runner.run_baseline_v18()
    
    # 运行当前版本
    result_v181 = system_runner.run_current()
    
    # 验证：等待态行为一致
    # TODO: 实现等待态行为对比逻辑
    # assert result_v181["waiting_behavior"] == result_v18["waiting_behavior"]


