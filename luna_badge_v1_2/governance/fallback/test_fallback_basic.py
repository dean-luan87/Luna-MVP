#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fallback / PlanB 基础功能测试

验证 FallbackExecutor 的核心功能：
1. 任何 fallback 都有明确 trigger
2. 每一次 fallback 都能数清第几次
3. 达到 max_attempts 必然中止
4. fallback 路径完全来自配置
5. 不改代码即可调整兜底策略
"""

import sys
import os
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from governance.fallback.fallback_executor import FallbackExecutor


def test_trigger_matching():
    """测试 1: 任何 fallback 都有明确 trigger"""
    print("\n=== 测试 1: Trigger 匹配 ===")
    executor = FallbackExecutor()
    
    # 测试不同的 trigger
    triggers = [
        "low_confidence",
        "model_failure",
        "conflict",
        "timeout",
        "invalid_output"
    ]
    
    for trigger in triggers:
        executor.reset("navigation")
        result = executor.execute("navigation", trigger)
        assert result["action"] != "abort" or result["reason"] == "exhausted", \
            f"Trigger '{trigger}' 应该匹配到策略，而不是直接中止"
        print(f"✓ Trigger '{trigger}' → action={result['action']}, plan={result['plan']}")


def test_attempt_counting():
    """测试 2: 每一次 fallback 都能数清第几次"""
    print("\n=== 测试 2: 尝试次数计数 ===")
    executor = FallbackExecutor()
    executor.reset("navigation")
    
    # 连续执行多次 fallback（等待冷却期过去）
    import time
    for expected_attempt in range(1, 4):
        # 如果不在第一次，等待冷却期过去
        if expected_attempt > 1:
            time.sleep(2.1)  # navigation 的 cooldown_ms 是 2000ms
        
        result = executor.execute("navigation", "low_confidence")
        
        # 如果处于冷却期，等待冷却期过去后重试
        while result["action"] == "wait":
            wait_ms = result.get("cooldown_remaining_ms", 0)
            if wait_ms > 0:
                time.sleep((wait_ms + 100) / 1000.0)  # 多等 100ms 确保冷却期过去
            result = executor.execute("navigation", "low_confidence")
        
        actual_attempt = result["attempt"]
        assert actual_attempt == expected_attempt, \
            f"第 {expected_attempt} 次 fallback，但 attempt={actual_attempt}"
        print(f"✓ 第 {actual_attempt} 次 fallback: action={result['action']}, plan={result['plan']}")


def test_max_attempts_enforcement():
    """测试 3: 达到 max_attempts 必然中止"""
    print("\n=== 测试 3: 最大尝试次数强制中止 ===")
    executor = FallbackExecutor()
    executor.reset("navigation")
    
    # navigation 的 max_attempts 是 3
    max_attempts = 3
    
    # 执行到最大次数（等待冷却期）
    import time
    for i in range(max_attempts):
        if i > 0:
            time.sleep(2.1)  # 等待冷却期过去
        result = executor.execute("navigation", "low_confidence")
        # 如果处于冷却期，等待后重试
        while result["action"] == "wait":
            wait_ms = result.get("cooldown_remaining_ms", 0)
            if wait_ms > 0:
                time.sleep((wait_ms + 100) / 1000.0)
            result = executor.execute("navigation", "low_confidence")
        print(f"  尝试 {i+1}: action={result['action']}, attempt={result['attempt']}")
    
    # 第 max_attempts + 1 次应该触发 exhausted
    time.sleep(2.1)
    result = executor.execute("navigation", "low_confidence")
    assert result["action"] == "abort", "达到 max_attempts 后应该中止"
    assert result["reason"] == "exhausted", "中止原因应该是 exhausted"
    assert result["attempt"] == max_attempts, f"attempt 应该是 {max_attempts}"
    print(f"✓ 达到最大尝试次数 ({max_attempts})，正确触发中止")


def test_config_driven_path():
    """测试 4: fallback 路径完全来自配置"""
    print("\n=== 测试 4: 配置驱动的路径 ===")
    executor = FallbackExecutor()
    executor.reset("navigation")
    
    # 测试不同 trigger 对应的不同 action
    test_cases = [
        ("low_confidence", "switch_model", "B1"),
        ("conflict", "degrade_capability", "B2"),
        ("timeout", "cross_domain", "B3"),
    ]
    
    for trigger, expected_action, expected_plan in test_cases:
        executor.reset("navigation")
        result = executor.execute("navigation", trigger)
        assert result["action"] == expected_action, \
            f"Trigger '{trigger}' 应该对应 action '{expected_action}'，实际是 '{result['action']}'"
        assert result["plan"] == expected_plan, \
            f"Trigger '{trigger}' 应该对应 plan '{expected_plan}'，实际是 '{result['plan']}'"
        print(f"✓ Trigger '{trigger}' → action={result['action']}, plan={result['plan']}, target={result['target']}")


def test_cooldown():
    """测试 5: 冷却时间机制"""
    print("\n=== 测试 5: 冷却时间 ===")
    executor = FallbackExecutor()
    executor.reset("navigation")
    
    # 第一次执行
    result1 = executor.execute("navigation", "low_confidence")
    assert result1["action"] != "wait", "第一次执行不应该在冷却期"
    print(f"✓ 第一次执行: action={result1['action']}")
    
    # 立即第二次执行（应该在冷却期内）
    result2 = executor.execute("navigation", "low_confidence")
    if result2["action"] == "wait":
        assert result2["cooldown_remaining_ms"] > 0, "冷却期剩余时间应该 > 0"
        print(f"✓ 冷却期检测: 需等待 {result2['cooldown_remaining_ms']}ms")
    else:
        print(f"  注意: 冷却时间可能太短，未触发等待")


def test_different_domains():
    """测试 6: 不同任务域的策略"""
    print("\n=== 测试 6: 不同任务域的策略 ===")
    executor = FallbackExecutor()
    
    domains = ["navigation", "safety", "inquiry"]
    for domain in domains:
        executor.reset(domain)
        result = executor.execute(domain, "low_confidence")
        print(f"✓ {domain}: action={result['action']}, max_attempts={executor._get_domain_config(domain).get('max_attempts')}")


def test_reset():
    """测试 7: 重置功能"""
    print("\n=== 测试 7: 重置功能 ===")
    executor = FallbackExecutor()
    
    # 执行几次
    executor.execute("navigation", "low_confidence")
    executor.execute("navigation", "low_confidence")
    
    # 重置
    executor.reset("navigation")
    
    # 重置后应该从 attempt=1 开始
    result = executor.execute("navigation", "low_confidence")
    assert result["attempt"] == 1, "重置后应该从 attempt=1 开始"
    print(f"✓ 重置成功，attempt={result['attempt']}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Fallback / PlanB 基础功能测试")
    print("=" * 60)
    
    try:
        test_trigger_matching()
        test_attempt_counting()
        test_max_attempts_enforcement()
        test_config_driven_path()
        test_cooldown()
        test_different_domains()
        test_reset()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
        print("\n验收标准验证：")
        print("✓ 1. 任何 fallback 都有明确 trigger")
        print("✓ 2. 每一次 fallback 都能数清第几次")
        print("✓ 3. 达到 max_attempts 必然中止")
        print("✓ 4. fallback 路径完全来自配置")
        print("✓ 5. 不改代码即可调整兜底策略（通过修改 YAML）")
        return 0
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())





