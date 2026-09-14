# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性测试指纹单元测试

验证：
- fingerprint 在参数不变时稳定
- seed 相同时 summary 可复现
"""

import sys
import os
import tempfile
import shutil
import random

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.risk.robustness.fingerprint import calculate_risk_params_fingerprint
from core.risk.robustness.summary_generator import SummaryGenerator, ScenarioSummary


def test_fingerprint_stability():
    """测试 fingerprint 在参数不变时稳定"""
    # 计算两次 fingerprint
    fp1 = calculate_risk_params_fingerprint()
    fp2 = calculate_risk_params_fingerprint()
    
    # 应该相同
    assert fp1 == fp2, f"Fingerprint 不稳定: {fp1} != {fp2}"
    assert fp1.startswith("sha256:"), f"Fingerprint 格式错误: {fp1}"
    
    print("✅ Fingerprint 稳定性测试通过")


def test_fingerprint_format():
    """测试 fingerprint 格式"""
    fp = calculate_risk_params_fingerprint()
    
    # 检查格式
    assert fp.startswith("sha256:"), f"Fingerprint 应该以 'sha256:' 开头: {fp}"
    assert len(fp) > 70, f"Fingerprint 长度应该 > 70: {len(fp)}"
    
    # 提取哈希部分
    hash_part = fp[7:]  # 跳过 "sha256:"
    assert len(hash_part) == 64, f"哈希部分长度应该为 64: {len(hash_part)}"
    assert all(c in '0123456789abcdef' for c in hash_part), f"哈希部分应该只包含十六进制字符: {hash_part}"
    
    print("✅ Fingerprint 格式测试通过")


def test_seed_reproducibility():
    """测试 seed 相同时 summary 可复现"""
    # 创建两个相同的场景摘要（模拟相同 seed 下的结果）
    summary1 = ScenarioSummary(
        scenario="test_scenario",
        frames=100,
        risk_objects=2,
        max_risk_level=0.6,
        max_delta_risk=0.1,
        trend_distribution={"APPROACHING": 10, "STABLE": 90},
        dynamic_active_ratio=0.5,
        triggered=False
    )
    
    summary2 = ScenarioSummary(
        scenario="test_scenario",
        frames=100,
        risk_objects=2,
        max_risk_level=0.6,
        max_delta_risk=0.1,
        trend_distribution={"APPROACHING": 10, "STABLE": 90},
        dynamic_active_ratio=0.5,
        triggered=False
    )
    
    # 使用相同 seed 生成运行汇总
    run_summary1 = SummaryGenerator.generate_run_summary(
        scenario_summaries=[summary1],
        seed=123456,
        shadow_mode=True
    )
    
    run_summary2 = SummaryGenerator.generate_run_summary(
        scenario_summaries=[summary2],
        seed=123456,
        shadow_mode=True
    )
    
    # 关键字段应该相同（除了 run_id）
    assert run_summary1.seed == run_summary2.seed
    assert run_summary1.shadow_mode == run_summary2.shadow_mode
    assert run_summary1.scenarios == run_summary2.scenarios
    assert run_summary1.total_frames == run_summary2.total_frames
    assert run_summary1.risk_params_fingerprint == run_summary2.risk_params_fingerprint
    
    print("✅ Seed 可复现性测试通过")


def test_run_summary_fields():
    """测试运行汇总字段齐全"""
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
    
    run_summary = SummaryGenerator.generate_run_summary(
        scenario_summaries=[summary],
        seed=123456,
        shadow_mode=True
    )
    
    # 验证所有新字段存在
    assert run_summary.summary_schema_version == "1.0"
    assert run_summary.run_id is not None
    assert run_summary.build is not None
    assert "git_commit" in run_summary.build
    assert "build_id" in run_summary.build
    assert run_summary.risk_params_fingerprint is not None
    assert run_summary.risk_params_fingerprint.startswith("sha256:")
    assert run_summary.seed == 123456
    assert run_summary.shadow_mode is True
    
    print("✅ 运行汇总字段齐全测试通过")


def test_build_info():
    """测试构建信息获取"""
    from core.risk.robustness.fingerprint import get_build_info
    
    build_info = get_build_info()
    
    # 验证字段存在
    assert "git_commit" in build_info
    assert "build_id" in build_info
    
    # git_commit 应该是字符串（可能是 "unknown"）
    assert isinstance(build_info["git_commit"], str)
    
    # build_id 应该是字符串
    assert isinstance(build_info["build_id"], str)
    
    print("✅ 构建信息获取测试通过")


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Risk 鲁棒性测试指纹单元测试")
    print("=" * 70)
    print()
    
    test_fingerprint_stability()
    test_fingerprint_format()
    test_seed_reproducibility()
    test_run_summary_fields()
    test_build_info()
    
    print()
    print("=" * 70)
    print("✅ 所有测试通过")
    print("=" * 70)


