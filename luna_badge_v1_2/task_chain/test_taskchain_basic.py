#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaskChain 基础功能测试

验证 TaskChain 的核心功能：
1. 任何时刻系统都知道当前 state
2. 任何失败都有明确归类（FAILED / ABORTED）
3. PlanB 不破坏任务上下文
4. 中断后可恢复到一致状态
5. TaskChain 不依赖模型具体实现
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from task_chain.task_state import TaskState
from task_chain.task_node import TaskNode
from task_chain.task_context import TaskContext
from task_chain.task_chain_manager import TaskChainManager


def test_state_management():
    """测试 1: 任何时刻系统都知道当前 state"""
    print("\n=== 测试 1: 状态管理 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    
    # 初始状态
    assert manager.state == TaskState.PENDING, "初始状态应该是 PENDING"
    print(f"✓ 初始状态: {manager.state.value}")
    
    # 启动
    manager.start(node)
    assert manager.state == TaskState.RUNNING, "启动后应该是 RUNNING"
    print(f"✓ 启动后状态: {manager.state.value}")
    
    # 暂停
    manager.pause()
    assert manager.state == TaskState.PAUSED, "暂停后应该是 PAUSED"
    print(f"✓ 暂停后状态: {manager.state.value}")
    
    # 恢复
    manager.resume()
    assert manager.state == TaskState.RUNNING, "恢复后应该是 RUNNING"
    print(f"✓ 恢复后状态: {manager.state.value}")


def test_failure_classification():
    """测试 2: 任何失败都有明确归类（FAILED / ABORTED）"""
    print("\n=== 测试 2: 失败分类 ===")
    
    # 测试 FAILED（有 PlanB，可恢复）
    manager1 = TaskChainManager()
    node1 = TaskNode("test_node", "navigation")
    manager1.start(node1)
    
    # 模拟 fallback 导致的失败
    manager1._mark_node_failed("Model output conflict")
    assert manager1.state == TaskState.FAILED, "失败后应该是 FAILED"
    assert manager1.current_node.state == TaskState.FAILED, "节点状态也应该是 FAILED"
    assert manager1.current_node.failure_reason == "Model output conflict", "失败原因应该被记录"
    print(f"✓ FAILED 状态: {manager1.state.value}, 原因: {manager1.current_node.failure_reason}")
    
    # 测试 ABORTED（系统/策略禁止继续，不可恢复）
    manager2 = TaskChainManager()
    node2 = TaskNode("test_node", "navigation")
    manager2.start(node2)
    
    manager2.abort("Max attempts exceeded")
    assert manager2.state == TaskState.ABORTED, "中止后应该是 ABORTED"
    assert manager2.current_node.state == TaskState.ABORTED, "节点状态也应该是 ABORTED"
    assert manager2.current_node.failure_reason == "Max attempts exceeded", "中止原因应该被记录"
    print(f"✓ ABORTED 状态: {manager2.state.value}, 原因: {manager2.current_node.failure_reason}")
    
    # 验证 FAILED ≠ ABORTED
    assert TaskState.FAILED != TaskState.ABORTED, "FAILED 和 ABORTED 应该不同"
    assert TaskState.FAILED.can_resume(), "FAILED 应该可以恢复"
    assert not TaskState.ABORTED.can_resume(), "ABORTED 不应该可以恢复"
    print("✓ FAILED ≠ ABORTED，且 FAILED 可恢复，ABORTED 不可恢复")


def test_moc_integration():
    """测试 3: TaskChain × MOC 集成"""
    print("\n=== 测试 3: MOC 集成 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    # 测试 commit 决策
    moc_result_commit = {
        "decision": "commit",
        "selected_result": {"action": "turn_left"},
        "reason": "Primary model selected",
        "used_model": {"model_id": "vision_model_v1", "version": "1.0"}
    }
    manager.handle_result(moc_result_commit)
    assert manager.state == TaskState.COMPLETED, "commit 后应该是 COMPLETED"
    print(f"✓ MOC commit 决策: 状态变为 {manager.state.value}")
    
    # 测试 abort 决策
    manager2 = TaskChainManager()
    node2 = TaskNode("test_node", "navigation")
    manager2.start(node2)
    
    moc_result_abort = {
        "decision": "abort",
        "reason": "Critical error"
    }
    manager2.handle_result(moc_result_abort)
    assert manager2.state == TaskState.ABORTED, "abort 后应该是 ABORTED"
    print(f"✓ MOC abort 决策: 状态变为 {manager2.state.value}")


def test_fallback_integration():
    """测试 4: PlanB 不破坏任务上下文"""
    print("\n=== 测试 4: Fallback 集成 ===")
    
    # 创建 FallbackExecutor mock
    class MockFallbackExecutor:
        def execute(self, task_domain, reason, context):
            return {
                "action": "switch_model",
                "target": "backup_vision_model",
                "reason": reason,
                "attempt": context.get("attempt", 0) + 1,
                "plan": "B1"
            }
    
    manager = TaskChainManager(fallback_executor=MockFallbackExecutor())
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    # 保存上下文快照
    context_before = manager.context.to_dict()
    
    # 触发 fallback
    moc_result_fallback = {
        "decision": "fallback",
        "reason": "low_confidence"
    }
    manager.handle_result(moc_result_fallback)
    
    # 验证上下文未被破坏
    assert manager.context.get_attempt_count("navigation") == 1, "attempts 应该增加"
    assert len(manager.context.history) > len(context_before["history"]), "history 应该增加"
    assert manager.state == TaskState.FAILED, "fallback 后应该是 FAILED（可恢复）"
    print(f"✓ Fallback 后状态: {manager.state.value}")
    print(f"✓ 上下文保持完整: attempts={manager.context.get_attempt_count('navigation')}, history_count={len(manager.context.history)}")


def test_pause_resume():
    """测试 5: 中断后可恢复到一致状态"""
    print("\n=== 测试 5: 暂停/恢复 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    # 先执行节点，使其进入 RUNNING 状态
    node.execute(manager.context.to_dict())
    assert node.state == TaskState.RUNNING, "节点执行后应该是 RUNNING"
    
    # 设置一些上下文
    manager.context.set("step", 1)
    manager.context.set("data", {"key": "value"})
    
    # 暂停
    manager.pause()
    assert manager.state == TaskState.PAUSED, "暂停后应该是 PAUSED"
    assert manager.current_node.state == TaskState.PAUSED, "节点状态也应该是 PAUSED"
    
    # 验证上下文保持
    assert manager.context.get("step") == 1, "上下文应该保持"
    assert manager.context.get("data") == {"key": "value"}, "上下文应该保持"
    
    # 恢复
    manager.resume()
    assert manager.state == TaskState.RUNNING, "恢复后应该是 RUNNING"
    assert manager.current_node.state == TaskState.RUNNING, "节点状态也应该是 RUNNING"
    
    # 验证上下文仍然保持
    assert manager.context.get("step") == 1, "恢复后上下文应该保持"
    assert manager.context.get("data") == {"key": "value"}, "恢复后上下文应该保持"
    print("✓ 暂停/恢复后状态和上下文保持一致")


def test_context_history():
    """测试 6: 上下文历史记录"""
    print("\n=== 测试 6: 上下文历史 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    
    # 启动
    manager.start(node)
    assert len(manager.context.history) >= 1, "启动应该记录历史"
    
    # 暂停
    manager.pause()
    assert len(manager.context.history) >= 2, "暂停应该记录历史"
    
    # 恢复
    manager.resume()
    assert len(manager.context.history) >= 3, "恢复应该记录历史"
    
    # 验证历史记录包含关键事件
    event_types = [e["type"] for e in manager.context.history]
    assert "task_chain_started" in event_types, "应该包含启动事件"
    assert "task_chain_paused" in event_types, "应该包含暂停事件"
    assert "task_chain_resumed" in event_types, "应该包含恢复事件"
    print(f"✓ 历史记录完整: {len(manager.context.history)} 个事件")


def test_no_model_dependency():
    """测试 7: TaskChain 不依赖模型具体实现"""
    print("\n=== 测试 7: 无模型依赖 ===")
    manager = TaskChainManager()
    node = TaskNode("test_node", "navigation")
    manager.start(node)
    
    # 使用假输出测试完整流程
    fake_moc_result = {
        "decision": "commit",
        "selected_result": {"fake": "data"},
        "reason": "Fake model output",
        "used_model": {"model_id": "fake_model", "version": "1.0"}
    }
    
    # 应该能正常处理，不依赖真实模型
    manager.handle_result(fake_moc_result)
    assert manager.state == TaskState.COMPLETED, "应该能完成"
    print("✓ TaskChain 不依赖模型具体实现，可以用假输出跑完整流程")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("TaskChain 基础功能测试")
    print("=" * 60)
    
    try:
        test_state_management()
        test_failure_classification()
        test_moc_integration()
        test_fallback_integration()
        test_pause_resume()
        test_context_history()
        test_no_model_dependency()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)
        print("\n验收标准验证：")
        print("✓ 1. 任何时刻系统都知道当前 state")
        print("✓ 2. 任何失败都有明确归类（FAILED / ABORTED）")
        print("✓ 3. PlanB 不破坏任务上下文")
        print("✓ 4. 中断后可恢复到一致状态")
        print("✓ 5. TaskChain 不依赖模型具体实现")
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





