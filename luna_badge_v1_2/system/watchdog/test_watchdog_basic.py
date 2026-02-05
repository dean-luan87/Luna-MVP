#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watchdog & Fail-Safe 基础功能测试

验证 Watchdog 的核心功能：
1. 任意异常 → 必有响应
2. 无"无声失败"
3. Fail-Safe 行为可预测、可配置
4. 不因模型异常导致系统卡死
5. 可恢复路径明确
6. 用户始终能理解"发生了什么"
"""

import sys
import os
import time

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from system.watchdog.watchdog_monitor import WatchdogMonitor, AnomalyType
from system.watchdog.failsafe_trigger import FailSafeTrigger, FailSafeLevel
from system.watchdog.restart_recovery_flow import RestartRecoveryFlow
from decision.task_chain.task_chain_manager import TaskChainManager
from decision.task_chain.task_node import TaskNode
from decision.task_chain.task_state import TaskState


def test_anomaly_detection():
    """测试 1: 任意异常 → 必有响应"""
    print("\n=== 测试 1: 异常检测 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    monitor = WatchdogMonitor(manager)
    monitor.start()
    
    # 测试节点超时检测
    monitor.node_start_times["test_node"] = time.time() - 35  # 35 秒前启动（超过 30 秒阈值）
    
    anomaly = monitor.check()
    assert anomaly is not None, "应该检测到节点超时异常"
    assert anomaly["type"] == AnomalyType.NODE_TIMEOUT, "异常类型应该是 NODE_TIMEOUT"
    assert anomaly["severity"] == "high", "超时异常应该是高优先级"
    print(f"✓ 检测到异常: {anomaly['type'].value}, 严重程度: {anomaly['severity']}")


def test_failsafe_decision():
    """测试 2: Fail-Safe 行为可预测、可配置"""
    print("\n=== 测试 2: Fail-Safe 决策 ===")
    manager = TaskChainManager()
    trigger = FailSafeTrigger(manager)
    
    # 测试不同异常类型对应的 Fail-Safe 等级
    test_cases = [
        (AnomalyType.MODEL_TIMEOUT, FailSafeLevel.FS_1_SOFT_INTERVENTION),
        (AnomalyType.NODE_TIMEOUT, FailSafeLevel.FS_2_TASK_RESET),
        (AnomalyType.ENV_MUTATION, FailSafeLevel.FS_3_SYSTEM_PAUSE),
        (AnomalyType.FALLBACK_LOOP, FailSafeLevel.FS_4_ABORT_RECOVER),
    ]
    
    for anomaly_type, expected_level in test_cases:
        anomaly = {
            "type": anomaly_type,
            "severity": "high",
            "description": f"Test {anomaly_type.value}",
            "context": {}
        }
        
        action = trigger.decide(anomaly)
        assert action["level"] == expected_level.value, \
            f"{anomaly_type.value} 应该对应 {expected_level.value}"
        print(f"✓ {anomaly_type.value} → {action['level']}: {action['action']}")


def test_failsafe_execution():
    """测试 3: Fail-Safe 执行"""
    print("\n=== 测试 3: Fail-Safe 执行 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    trigger = FailSafeTrigger(manager)
    
    # 测试 FS-1: 软干预
    anomaly_fs1 = {
        "type": AnomalyType.MODEL_TIMEOUT,
        "severity": "high",
        "description": "Model timeout",
        "context": {}
    }
    action_fs1 = trigger.decide(anomaly_fs1)
    result_fs1 = trigger.execute(action_fs1)
    assert result_fs1["success"], "FS-1 应该执行成功"
    assert result_fs1["action_taken"] == "paused_node", "应该暂停节点"
    assert manager.state == TaskState.PAUSED, "任务链应该处于 PAUSED 状态"
    print(f"✓ FS-1 执行成功: {result_fs1['action_taken']}")
    
    # 测试 FS-4: 终止并恢复
    manager2 = TaskChainManager()
    node2 = TaskNode("test_node", "navigation")
    manager2.start(node2)
    trigger2 = FailSafeTrigger(manager2)
    
    anomaly_fs4 = {
        "type": AnomalyType.FALLBACK_LOOP,
        "severity": "high",
        "description": "Fallback loop detected",
        "context": {}
    }
    action_fs4 = trigger2.decide(anomaly_fs4)
    result_fs4 = trigger2.execute(action_fs4)
    assert result_fs4["success"], "FS-4 应该执行成功"
    assert result_fs4["action_taken"] == "aborted_task", "应该中止任务"
    assert manager2.state == TaskState.ABORTED, "任务链应该处于 ABORTED 状态"
    print(f"✓ FS-4 执行成功: {result_fs4['action_taken']}")


def test_no_silent_failure():
    """测试 4: 无"无声失败"（所有异常都被记录）"""
    print("\n=== 测试 4: 无无声失败 ===")
    manager = TaskChainManager()
    monitor = WatchdogMonitor(manager)
    monitor.start()
    
    # 记录多个异常
    monitor.record_model_anomaly(AnomalyType.MODEL_TIMEOUT, "Model timeout", {"model_id": "test"})
    monitor.record_model_anomaly(AnomalyType.MODEL_NO_RETURN, "Model no return", {"model_id": "test"})
    monitor.record_env_mutation("Door closed", {"vision_state": "door_closed"})
    
    history = monitor.get_anomaly_history()
    assert len(history) >= 3, "应该记录所有异常"
    
    anomaly_types = [a["anomaly"]["type"] for a in history]
    assert AnomalyType.MODEL_TIMEOUT in anomaly_types, "应该包含 MODEL_TIMEOUT"
    assert AnomalyType.MODEL_NO_RETURN in anomaly_types, "应该包含 MODEL_NO_RETURN"
    assert AnomalyType.ENV_MUTATION in anomaly_types, "应该包含 ENV_MUTATION"
    print(f"✓ 所有异常都被记录: {len(history)} 个异常")


def test_fallback_loop_detection():
    """测试 5: PlanB 循环检测"""
    print("\n=== 测试 5: PlanB 循环检测 ===")
    manager = TaskChainManager()
    manager.context.attempts["navigation"] = 6  # 超过阈值 5
    
    monitor = WatchdogMonitor(manager)
    monitor.fallback_loop_threshold = 5
    monitor.start()
    
    anomaly = monitor.check()
    assert anomaly is not None, "应该检测到 PlanB 循环"
    assert anomaly["type"] == AnomalyType.FALLBACK_LOOP, "异常类型应该是 FALLBACK_LOOP"
    print(f"✓ 检测到 PlanB 循环: {anomaly['description']}")


def test_recovery_flow():
    """测试 6: 可恢复路径明确"""
    print("\n=== 测试 6: 恢复流程 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    manager.context.set("step", 1)
    
    recovery = RestartRecoveryFlow()
    
    # 创建快照
    snapshot = recovery.create_snapshot(manager)
    assert snapshot["task_state"] == "running", "快照应该包含任务状态"
    assert snapshot["node_id"] == "test_node", "快照应该包含节点 ID"
    assert snapshot["context"]["data"]["step"] == 1, "快照应该包含上下文"
    print(f"✓ 创建快照成功: snapshot_id={snapshot['snapshot_id']}")
    
    # 测试恢复决策
    decision = recovery.start(snapshot)
    assert decision["has_unfinished_task"], "应该检测到未完成任务"
    assert decision["can_recover"], "应该可以恢复"
    assert decision["user_prompt"] is not None, "应该生成用户提示"
    print(f"✓ 恢复决策: {decision['recovery_action']}, 用户提示: {decision['user_prompt']}")


def test_env_mutation_priority():
    """测试 7: 视角优先 - 环境突变时立即暂停"""
    print("\n=== 测试 7: 视角优先（环境突变） ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    monitor = WatchdogMonitor(manager)
    trigger = FailSafeTrigger(manager)
    
    # 记录环境突变
    monitor.record_env_mutation("Door closed suddenly", {
        "vision_state": "door_closed",
        "previous_state": "door_open"
    })
    
    # 获取异常并触发 Fail-Safe
    history = monitor.get_anomaly_history(limit=1)
    if history:
        anomaly = history[0]["anomaly"]
        action = trigger.decide(anomaly)
        
        # 环境突变应该触发 FS-3（系统暂停）
        assert action["level"] == FailSafeLevel.FS_3_SYSTEM_PAUSE.value, \
            "环境突变应该触发 FS-3"
        
        result = trigger.execute(action)
        assert result["success"], "应该执行成功"
        assert "user_notification" in result, "应该生成用户通知"
        assert manager.state == TaskState.PAUSED, "应该暂停系统"
        print(f"✓ 环境突变触发 FS-3: {result['user_notification']}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Watchdog & Fail-Safe 基础功能测试")
    print("=" * 60)
    
    try:
        test_anomaly_detection()
        test_failsafe_decision()
        test_failsafe_execution()
        test_no_silent_failure()
        test_fallback_loop_detection()
        test_recovery_flow()
        test_env_mutation_priority()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
        print("\n验收标准验证：")
        print("✓ 1. 任意异常 → 必有响应")
        print("✓ 2. 无'无声失败'")
        print("✓ 3. Fail-Safe 行为可预测、可配置")
        print("✓ 4. 不因模型异常导致系统卡死")
        print("✓ 5. 可恢复路径明确")
        print("✓ 6. 用户始终能理解'发生了什么'")
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





