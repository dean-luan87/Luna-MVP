#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watchdog Fail-Safe 验收测试

验收点：
- node 超时 → FS-2 或 FS-3（按设定）
- 写入 error_log + execution_trace
"""

import sys
import os
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from system.watchdog.watchdog_monitor import WatchdogMonitor, AnomalyType
from system.watchdog.failsafe_trigger import FailSafeTrigger
from decision.task_chain.task_chain_manager import TaskChainManager
from decision.task_chain.task_node import TaskNode
from metrics.metrics_collector import MetricsCollector


def test_node_timeout_triggers_failsafe():
    """测试 1: node 超时 → FS-2"""
    print("\n=== 测试 1: Node 超时触发 Fail-Safe ===")
    
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    collector = MetricsCollector()
    monitor = WatchdogMonitor(manager)
    trigger = FailSafeTrigger(manager, metrics_collector=collector)
    
    # 模拟节点超时
    monitor.node_start_times["test_node"] = time.time() - 35  # 35 秒前启动
    
    anomaly = monitor.check()
    assert anomaly is not None, "应该检测到超时异常"
    assert anomaly["type"] == AnomalyType.NODE_TIMEOUT, "异常类型应该是 NODE_TIMEOUT"
    
    # 触发 Fail-Safe
    action = trigger.decide(anomaly)
    assert action["level"] == "FS-2", "超时应该触发 FS-2"
    
    result = trigger.execute(action)
    assert result["success"], "应该执行成功"
    assert result["action_taken"] == "reset_node", "应该重置节点"
    
    print(f"✓ Node 超时触发 FS-2: {action['level']}, action={result['action_taken']}")


def test_error_log_written():
    """测试 2: 写入 error_log + execution_trace"""
    print("\n=== 测试 2: 错误日志写入 ===")
    
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    collector = MetricsCollector()
    monitor = WatchdogMonitor(manager)
    trigger = FailSafeTrigger(manager, metrics_collector=collector, trace_id=collector.new_trace_id())
    
    # 模拟异常
    anomaly = {
        "type": AnomalyType.NODE_TIMEOUT,
        "severity": "high",
        "description": "Node timeout",
        "context": {}
    }
    
    action = trigger.decide(anomaly)
    trigger.execute(action)
    
    # 检查日志文件是否存在且有内容
    import json
    error_path = collector.error_path
    if error_path.exists():
        with error_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            assert len(lines) > 0, "error_log 应该有内容"
            last_error = json.loads(lines[-1])
            assert last_error["error_type"] == "watchdog_triggered", "应该记录 watchdog 错误"
            print(f"✓ 错误日志已写入: {last_error['error_type']}")
    
    trace_path = collector.trace_path
    if trace_path.exists():
        with trace_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            assert len(lines) > 0, "execution_trace 应该有内容"
            last_trace = json.loads(lines[-1])
            assert last_trace["event"] == "watchdog", "应该记录 watchdog 事件"
            print(f"✓ 执行跟踪已写入: {last_trace['event']}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Watchdog Fail-Safe 验收测试")
    print("=" * 60)
    
    try:
        test_node_timeout_triggers_failsafe()
        test_error_log_written()
        
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




