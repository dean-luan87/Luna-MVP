# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性测试摘要生成器单元测试

验证 summary 字段齐全且数值合理
"""

import sys
import os
import tempfile
import shutil

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.risk.robustness.summary_generator import (
    SummaryGenerator,
    ScenarioSummary,
    RunSummary,
)
from core.risk.risk_debug import RiskDebugSnapshot, RiskObjectSnapshot


def test_scenario_summary_fields():
    """测试场景摘要字段齐全"""
    # 创建模拟快照
    snapshots = [
        RiskDebugSnapshot(
            ts=1000.0,
            user_xy=(5.0, 3.0),
            objects=[
                RiskObjectSnapshot(
                    risk_id="test_001",
                    risk_type="WATER_EDGE",
                    dynamic_active=True,
                    hazard_level=0.8,
                    distance_m=3.0,
                    trend="APPROACHING",
                    risk_level=0.6,
                    delta_risk=0.1,
                    state="DORMANT"
                ),
                RiskObjectSnapshot(
                    risk_id="test_002",
                    risk_type="CROWD",
                    dynamic_active=False,
                    hazard_level=0.5,
                    distance_m=5.0,
                    trend="STABLE",
                    risk_level=0.3,
                    delta_risk=0.0,
                    state="DORMANT"
                ),
            ],
            advisory_triggered=False
        ),
        RiskDebugSnapshot(
            ts=1001.0,
            user_xy=(5.0, 2.5),
            objects=[
                RiskObjectSnapshot(
                    risk_id="test_001",
                    risk_type="WATER_EDGE",
                    dynamic_active=True,
                    hazard_level=0.8,
                    distance_m=2.5,
                    trend="APPROACHING",
                    risk_level=0.7,
                    delta_risk=0.15,
                    state="DORMANT"
                ),
            ],
            advisory_triggered=True
        ),
    ]
    
    # 生成摘要
    summary = SummaryGenerator.generate_scenario_summary(
        scenario_name="test_scenario",
        snapshots=snapshots
    )
    
    # 验证字段齐全
    assert summary.scenario == "test_scenario"
    assert summary.frames == 2
    assert summary.risk_objects == 2  # test_001 和 test_002
    assert summary.max_risk_level == 0.7
    assert summary.max_delta_risk == 0.15
    assert "APPROACHING" in summary.trend_distribution
    assert "STABLE" in summary.trend_distribution
    assert summary.dynamic_active_ratio > 0.0
    assert summary.triggered is True
    
    print("✅ 场景摘要字段齐全测试通过")


def test_scenario_summary_values():
    """测试场景摘要数值合理"""
    # 创建模拟快照（无触发）
    snapshots = [
        RiskDebugSnapshot(
            ts=1000.0,
            user_xy=(5.0, 3.0),
            objects=[
                RiskObjectSnapshot(
                    risk_id="test_001",
                    risk_type="WATER_EDGE",
                    dynamic_active=None,
                    hazard_level=0.8,
                    distance_m=3.0,
                    trend="STABLE",
                    risk_level=0.5,
                    delta_risk=0.05,
                    state="DORMANT"
                ),
            ],
            advisory_triggered=False
        ),
    ]
    
    # 生成摘要
    summary = SummaryGenerator.generate_scenario_summary(
        scenario_name="test_scenario",
        snapshots=snapshots
    )
    
    # 验证数值合理
    assert summary.frames > 0
    assert summary.risk_objects > 0
    assert 0.0 <= summary.max_risk_level <= 1.0
    assert summary.max_delta_risk >= 0.0
    assert len(summary.trend_distribution) > 0
    assert 0.0 <= summary.dynamic_active_ratio <= 1.0
    assert summary.triggered is False
    
    print("✅ 场景摘要数值合理测试通过")


def test_run_summary_fields():
    """测试运行汇总字段齐全"""
    scenario_summaries = [
        ScenarioSummary(
            scenario="scenario_1",
            frames=100,
            risk_objects=2,
            max_risk_level=0.6,
            max_delta_risk=0.1,
            trend_distribution={"APPROACHING": 10, "STABLE": 80, "LEAVING": 10},
            dynamic_active_ratio=0.5,
            triggered=False
        ),
        ScenarioSummary(
            scenario="scenario_2",
            frames=50,
            risk_objects=1,
            max_risk_level=0.8,
            max_delta_risk=0.2,
            trend_distribution={"APPROACHING": 20, "STABLE": 30},
            dynamic_active_ratio=0.0,
            triggered=True
        ),
    ]
    
    # 生成运行汇总
    run_summary = SummaryGenerator.generate_run_summary(scenario_summaries)
    
    # 验证字段齐全
    assert run_summary.scenarios == 2
    assert run_summary.total_frames == 150
    assert run_summary.any_triggered is True
    assert run_summary.global_max_risk_level == 0.8
    assert run_summary.global_max_delta_risk == 0.2
    
    print("✅ 运行汇总字段齐全测试通过")


def test_summary_save():
    """测试摘要保存功能"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 创建摘要
        summary = ScenarioSummary(
            scenario="test_scenario",
            frames=100,
            risk_objects=2,
            max_risk_level=0.6,
            max_delta_risk=0.1,
            trend_distribution={"APPROACHING": 10, "STABLE": 90},
            dynamic_active_ratio=0.5,
            triggered=False
        )
        
        # 保存摘要
        filepath = SummaryGenerator.save_summary(
            summary=summary,
            output_dir=temp_dir,
            filename="test_summary.json"
        )
        
        # 验证文件存在
        assert os.path.exists(filepath)
        
        # 验证文件内容
        import json
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data["scenario"] == "test_scenario"
        assert data["frames"] == 100
        assert data["risk_objects"] == 2
        
        print("✅ 摘要保存功能测试通过")
    
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)


def test_empty_snapshots():
    """测试空快照列表"""
    summary = SummaryGenerator.generate_scenario_summary(
        scenario_name="empty_scenario",
        snapshots=[]
    )
    
    assert summary.scenario == "empty_scenario"
    assert summary.frames == 0
    assert summary.risk_objects == 0
    assert summary.max_risk_level == 0.0
    assert summary.max_delta_risk == 0.0
    assert len(summary.trend_distribution) == 0
    assert summary.dynamic_active_ratio == 0.0
    assert summary.triggered is False
    
    print("✅ 空快照列表测试通过")


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Risk 鲁棒性测试摘要生成器单元测试")
    print("=" * 70)
    print()
    
    test_scenario_summary_fields()
    test_scenario_summary_values()
    test_run_summary_fields()
    test_summary_save()
    test_empty_snapshots()
    
    print()
    print("=" * 70)
    print("✅ 所有测试通过")
    print("=" * 70)


