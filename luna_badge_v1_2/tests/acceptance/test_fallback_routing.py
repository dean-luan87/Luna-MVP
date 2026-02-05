#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fallback 路由验收测试

验收点：
- 按 fallback_policy.yaml 路由
- attempts 累积
- exhausted → abort
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from governance.fallback.fallback_executor import FallbackExecutor
from metrics.metrics_collector import MetricsCollector


def test_fallback_policy_routing():
    """测试 1: 按 fallback_policy.yaml 路由"""
    print("\n=== 测试 1: Fallback 策略路由 ===")
    
    collector = MetricsCollector()
    executor = FallbackExecutor(metrics_collector=collector)
    
    # 测试不同 trigger 的路由
    triggers = ["low_confidence", "conflict", "timeout"]
    for trigger in triggers:
        executor.reset("navigation")
        result = executor.execute("navigation", trigger)
        assert result["action"] in ["switch_model", "degrade_capability", "cross_domain", "abort"], \
            f"Trigger '{trigger}' 应该路由到有效 action"
        print(f"✓ Trigger '{trigger}' → action={result['action']}, plan={result['plan']}")


def test_attempts_accumulation():
    """测试 2: attempts 累积"""
    print("\n=== 测试 2: Attempts 累积 ===")
    
    collector = MetricsCollector()
    executor = FallbackExecutor(metrics_collector=collector)
    executor.reset("navigation")
    
    # 连续执行多次 fallback
    import time
    for i in range(3):
        if i > 0:
            time.sleep(2.1)  # 等待冷却期
        result = executor.execute("navigation", "low_confidence")
        assert result["attempt"] == i + 1, f"第 {i+1} 次 attempt 应该是 {i+1}"
        print(f"✓ Attempt {result['attempt']}: action={result['action']}")


def test_exhausted_abort():
    """测试 3: exhausted → abort"""
    print("\n=== 测试 3: Exhausted → Abort ===")
    
    collector = MetricsCollector()
    executor = FallbackExecutor(metrics_collector=collector)
    executor.reset("navigation")
    
    # navigation 的 max_attempts 是 3
    import time
    for i in range(3):
        if i > 0:
            time.sleep(2.1)
        executor.execute("navigation", "low_confidence")
    
    # 第 4 次应该触发 exhausted
    time.sleep(2.1)
    result = executor.execute("navigation", "low_confidence")
    assert result["action"] == "abort", "应该触发 abort"
    assert result["reason"] == "exhausted", "原因应该是 exhausted"
    print(f"✓ Exhausted 触发: {result['action']}, reason={result['reason']}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Fallback 路由验收测试")
    print("=" * 60)
    
    try:
        test_fallback_policy_routing()
        test_attempts_accumulation()
        test_exhausted_abort()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
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




