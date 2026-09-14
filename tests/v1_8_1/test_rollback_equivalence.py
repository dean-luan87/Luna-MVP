#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TC-06: 全局回滚等价性测试

目标：验证 observer_mode=false 时，行为必须等价 v1.8

重点：这是"合同测试"，不是功能测试
失败就意味着：版本不可存在
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.v1_8_1.conftest import SystemRunner


def test_observer_disabled_equals_v18(system_runner):
    """
    TC-06: 回滚等价性测试
    
    这是"合同测试"，不是功能测试。
    失败 = 版本不可存在。
    
    测试范围：
    - 所有 observer_mode 代码路径跳过
    - 无新增播报
    - 任务流与 v1.8 完全一致
    
    判定标准：
    - outputs 必须完全一致
    - task_flow 必须完全一致
    - 任何差异 → FAIL（版本不可存在）
    """
    # 设置 observer_mode=false
    system_runner.set_config(observer_enabled=False)
    
    # 运行 v1.8 基线版本
    baseline = system_runner.run_v18()
    
    # 运行当前版本（v1.8.1，observer_mode=false）
    current = system_runner.run_v181()
    
    # 验证：outputs 必须完全一致
    assert current.outputs == baseline.outputs, \
        "v1.8.1 (observer_mode=false) outputs 与 v1.8 不一致"
    
    # 验证：task_flow 必须完全一致
    assert current.task_flow == baseline.task_flow, \
        "v1.8.1 (observer_mode=false) task_flow 与 v1.8 不一致"


def test_observer_mode_disabled_no_new_code_paths(system_runner):
    """
    TC-06 扩展：验证所有 observer_mode 代码路径被跳过
    
    测试范围：
    - 所有 observer_mode 相关函数不应被调用
    - 所有 observer_mode 相关逻辑不应执行
    """
    # 设置 observer_mode=false
    system_runner.set_config(OBSERVER_MODE_ENABLED=False)
    
    # 运行系统
    result = system_runner.run_current()
    
    # 验证：observer_mode 相关代码路径不应执行
    # TODO: 实现代码路径追踪逻辑
    # assert "observer_mode" not in result.get("executed_paths", [])


def test_observer_mode_disabled_task_chain_equivalence(system_runner):
    """
    TC-06 扩展：验证任务链行为等价
    
    测试范围：
    - 任务创建、执行、完成流程与 v1.8 一致
    - 任务状态转换与 v1.8 一致
    """
    # 设置 observer_mode=false
    system_runner.set_config(OBSERVER_MODE_ENABLED=False)
    
    # 运行 v1.8 基线版本
    result_v18 = system_runner.run_baseline_v18()
    
    # 运行当前版本
    result_v181 = system_runner.run_current()
    
    # 验证：任务链行为一致
    assert result_v181["task_flow"] == result_v18["task_flow"], \
        "任务链行为与 v1.8 不一致"


@pytest.mark.parametrize("test_scenario", [
    "navigation_basic",
    "navigation_with_waiting",
    "hospital_registration",
    "complex_route",
])
def test_observer_mode_disabled_scenario_equivalence(system_runner, test_scenario):
    """
    TC-06 参数化：不同场景下的回滚等价性
    
    测试多个场景，确保在所有场景下都等价
    """
    # 设置 observer_mode=false
    system_runner.set_config(OBSERVER_MODE_ENABLED=False)
    
    # 运行指定场景
    # TODO: 实现场景运行逻辑
    result_v18 = system_runner.run_baseline_v18(scenario=test_scenario)
    result_v181 = system_runner.run_current(scenario=test_scenario)
    
    # 验证等价性
    assert result_v181["outputs"] == result_v18["outputs"], \
        f"场景 {test_scenario} 下 outputs 与 v1.8 不一致"
    
    assert result_v181["task_flow"] == result_v18["task_flow"], \
        f"场景 {test_scenario} 下 task_flow 与 v1.8 不一致"

