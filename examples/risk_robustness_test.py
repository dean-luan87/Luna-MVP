#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性测试（Robustness Test）

目标：
在真实模型接入前，确认 risk 系统在"烂数据 + 极端行为"下不会乱说话。

测试内容：
1. 噪声/抖动注入（Noise）
2. 极端行为脚本（Scenario）
3. Shadow Mode（默认只输出日志，不触发播报）
"""

import sys
import os
import time
import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.risk.risk_registry import RiskRegistry
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService
from core.risk.robustness_test_harness import (
    RiskRobustnessTestHarness,
    TestScenario,
)
from core.risk.robustness import (
    NoisePositionProvider,
    ScenarioLibrary,
)
from core.risk.risk_object import DynamicProfile


def main():
    """运行 Risk 鲁棒性测试"""
    print("=" * 70)
    print("v1.8.4 Risk 鲁棒性测试框架")
    print("=" * 70)
    print()
    
    # 初始化组件
    reg = RiskRegistry()
    factory = RiskObjectFactory()
    service = RiskAdvisoryService(reg, enable_debug=True)
    
    # 创建测试风险对象
    # 1. 湖边（静态）
    lake = factory.make_line(
        risk_id="test_lake",
        risk_type="WATER_EDGE",
        polyline=[(0.0, 0.0), (30.0, 0.0)],
        confidence=0.95,
    )
    reg.upsert(lake)
    
    # 2. 人群拥堵区域（动态，TIME_WINDOW）
    crowd = factory.make_area(
        risk_id="test_crowd",
        risk_type="CROWD",
        polygon=[(10, 0), (20, 0), (20, 5), (10, 5)],
        confidence=0.9,
    )
    crowd.dynamic_profile = DynamicProfile(
        mode="TIME_WINDOW",
        active_windows=[(8, 9)],  # 只在 8-9 点激活
        hazard_multiplier=1.3,
        ignore_when_inactive=True
    )
    reg.upsert(crowd)
    
    print("✅ 创建测试风险对象")
    print(f"   - {lake.risk_id} ({lake.risk_type})")
    print(f"   - {crowd.risk_id} ({crowd.risk_type}, TIME_WINDOW)")
    print()
    
    # 初始化测试框架（Shadow Mode = True，只打日志，不播报）
    # 使用默认 seed 确保可复现
    harness = RiskRobustnessTestHarness(service, shadow_mode=True, seed=None)
    
    # 定义测试场景（使用 ScenarioLibrary）
    scenarios = []
    
    # === 场景 1：噪声/抖动注入 ===
    noisy_provider = NoisePositionProvider(
        base_xy=(5.0, 3.0),
        jitter_radius=0.3,
        jump_prob=0.05,
        jump_radius=2.0
    )
    scenarios.append(TestScenario(
        name="噪声/抖动注入",
        description="模拟模型识别抖动，验证系统是否稳定",
        position_generator=noisy_provider.sample,
        duration_seconds=10.0,
        expected_behavior="噪声存在，但系统基本不说话"
    ))
    
    # === 场景 2：阈值附近来回晃 ===
    threshold_scenario = ScenarioLibrary.hover_near_threshold()
    scenarios.append(TestScenario(
        name=threshold_scenario.name,
        description=threshold_scenario.description,
        position_generator=threshold_scenario.create_generator(),
        duration_seconds=sum(step.duration_s for step in threshold_scenario.steps),
        expected_behavior=threshold_scenario.expected_behavior
    ))
    
    # === 场景 3：快速靠近又立刻离开 ===
    approach_scenario = ScenarioLibrary.approach_and_leave_fast()
    scenarios.append(TestScenario(
        name=approach_scenario.name,
        description=approach_scenario.description,
        position_generator=approach_scenario.create_generator(),
        duration_seconds=sum(step.duration_s for step in approach_scenario.steps),
        expected_behavior=approach_scenario.expected_behavior
    ))
    
    # === 场景 4：静态停留（最重要） ===
    static_scenario = ScenarioLibrary.static_stay()
    scenarios.append(TestScenario(
        name=static_scenario.name,
        description=static_scenario.description,
        position_generator=static_scenario.create_generator(),
        duration_seconds=sum(step.duration_s for step in static_scenario.steps),
        expected_behavior=static_scenario.expected_behavior
    ))
    
    # === 场景 5：多风险叠加 ===
    multi_risk_scenario = ScenarioLibrary.multi_risk_overlap()
    scenarios.append(TestScenario(
        name=multi_risk_scenario.name,
        description=multi_risk_scenario.description,
        position_generator=multi_risk_scenario.create_generator(),
        duration_seconds=sum(step.duration_s for step in multi_risk_scenario.steps),
        expected_behavior=multi_risk_scenario.expected_behavior
    ))
    
    # 运行所有场景
    summary = harness.run_all_scenarios(scenarios, verbose=True)
    
    # 验收标准检查
    print("=" * 70)
    print("✅ 验收标准检查")
    print("=" * 70)
    
    # 检查 1：噪声场景
    noise_result = next((r for r in summary['results'] if '噪声' in r['scenario_name']), None)
    if noise_result:
        if noise_result['advisory_count'] <= 2:
            print("✅ 噪声场景：系统基本不说话（通过）")
        else:
            print(f"⚠️  噪声场景：触发 {noise_result['advisory_count']} 次（可能太敏感）")
    
    # 检查 2：静态停留
    static_result = next((r for r in summary['results'] if '静态停留' in r['scenario_name']), None)
    if static_result:
        if static_result['advisory_count'] <= 1:
            print("✅ 静态停留：只说一次或不说（通过）")
        else:
            print(f"⚠️  静态停留：触发 {static_result['advisory_count']} 次（可能重复触发）")
    
    # 检查 3：总体触发率
    if summary['advisory_rate'] < 0.1:  # 触发率 < 10%
        print(f"✅ 总体触发率：{summary['advisory_rate']:.2%}（系统保持克制）")
    else:
        print(f"⚠️  总体触发率：{summary['advisory_rate']:.2%}（可能太敏感）")
    
    print()
    print("=" * 70)
    print("✅ 鲁棒性测试完成")
    print("=" * 70)
    print()
    print("💡 提示")
    print("-" * 70)
    print("  • 所有测试在 Shadow Mode 下运行（不触发播报）")
    print("  • 可以通过 RiskDebugSnapshot 日志查看详细状态")
    print("  • 如果触发率过高，建议调整 delta_warn 或 cooldown 参数")
    print()


if __name__ == "__main__":
    main()

