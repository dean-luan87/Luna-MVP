#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaskChain 暂停/恢复验收测试

验收点：
- running → paused → resumed 状态一致
- 恢复后仍能继续 handle_result
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from decision.task_chain.task_chain_manager import TaskChainManager
from decision.task_chain.task_node import TaskNode
from decision.task_chain.task_state import TaskState
from metrics.metrics_collector import MetricsCollector


def test_pause_resume_state_consistency():
    """测试 1: running → paused → resumed 状态一致"""
    print("\n=== 测试 1: 暂停/恢复状态一致性 ===")
    
    collector = MetricsCollector()
    manager = TaskChainManager(metrics_collector=collector)
    node = TaskNode("test_node", "navigation")
    
    # 启动
    manager.start(node)
    assert manager.state == TaskState.RUNNING, "启动后应该是 RUNNING"
    
    # 暂停
    manager.pause()
    assert manager.state == TaskState.PAUSED, "暂停后应该是 PAUSED"
    assert manager.current_node.state == TaskState.PAUSED, "节点状态也应该是 PAUSED"
    
    # 恢复
    manager.resume()
    assert manager.state == TaskState.RUNNING, "恢复后应该是 RUNNING"
    assert manager.current_node.state == TaskState.RUNNING, "节点状态也应该是 RUNNING"
    
    print("✓ 状态转换一致: RUNNING → PAUSED → RUNNING")


def test_resume_can_handle_result():
    """测试 2: 恢复后仍能继续 handle_result"""
    print("\n=== 测试 2: 恢复后处理结果 ===")
    
    collector = MetricsCollector()
    manager = TaskChainManager(metrics_collector=collector)
    node = TaskNode("test_node", "navigation")
    
    manager.start(node)
    manager.pause()
    manager.resume()
    
    # 恢复后应该能处理结果
    moc_result = {
        "decision": "commit",
        "selected_result": {"action": "turn_left"},
        "reason": "Test",
        "used_model": {"model_id": "test_model", "version": "1.0"}
    }
    
    manager.handle_result(moc_result)
    assert manager.state == TaskState.COMPLETED, "应该能完成"
    print("✓ 恢复后能正常处理结果")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("TaskChain 暂停/恢复验收测试")
    print("=" * 60)
    
    try:
        test_pause_resume_state_consistency()
        test_resume_can_handle_result()
        
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




