#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna v1.4 → v1.5 迁移后功能测试

测试迁移后模块的基本功能是否正常
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

test_results: Dict[str, List[Tuple[str, bool, str]]] = {}


def test_function(category: str, test_name: str, test_func):
    """执行功能测试"""
    if category not in test_results:
        test_results[category] = []
    
    try:
        test_func()
        test_results[category].append((test_name, True, ""))
        print(f"  ✅ {test_name}")
        return True
    except Exception as e:
        error_msg = str(e)
        test_results[category].append((test_name, False, error_msg))
        print(f"  ❌ {test_name}: {error_msg}")
        import traceback
        traceback.print_exc()
        return False


def test_task_chain_functional():
    """测试任务链功能"""
    print("\n" + "=" * 60)
    print("测试任务链功能")
    print("=" * 60)
    
    def test_task_state():
        from decision.task_chain.task_state import TaskState
        assert TaskState.PENDING.value == "pending"
        assert TaskState.RUNNING.value == "running"
        assert TaskState.PENDING.is_terminal() == False
        assert TaskState.COMPLETED.is_terminal() == True
    
    def test_task_context():
        from decision.task_chain.task_context import TaskContext
        ctx = TaskContext()
        ctx.set("key1", "value1")
        assert ctx.get("key1") == "value1"
        assert ctx.get("key2", "default") == "default"
        ctx.increment_attempt("domain1")
        assert ctx.get_attempt_count("domain1") == 1
    
    def test_task_node():
        from decision.task_chain.task_node import TaskNode
        from decision.task_chain.task_state import TaskState
        node = TaskNode("node1", "test_domain")
        assert node.node_id == "node1"
        assert node.domain == "test_domain"
        assert node.state == TaskState.PENDING
        node.mark_completed()
        assert node.state == TaskState.COMPLETED
    
    def test_task_chain_manager():
        from decision.task_chain.task_chain_manager import TaskChainManager
        from decision.task_chain.task_node import TaskNode
        from decision.task_chain.task_state import TaskState
        manager = TaskChainManager()
        assert manager.state == TaskState.PENDING
        node = TaskNode("test_node", "test_domain")
        manager.start(node)
        assert manager.state == TaskState.RUNNING
        manager.pause()
        assert manager.state == TaskState.PAUSED
    
    def test_multi_target_buffer():
        from decision.task_chain.multi_target_buffer import MultiTargetBuffer, Target
        buffer = MultiTargetBuffer(max_targets=3)
        target1 = Target(id="t1", name="目标1", lat=0.0, lng=0.0, extra={})
        target2 = Target(id="t2", name="目标2", lat=1.0, lng=1.0, extra={})
        assert buffer.add_target(target1) == True
        assert buffer.add_target(target2) == True
        current = buffer.start()
        assert current.name == "目标1"
        next_target = buffer.complete_current()
        assert next_target.name == "目标2"
    
    test_function("任务链功能", "TaskState 枚举", test_task_state)
    test_function("任务链功能", "TaskContext 基本操作", test_task_context)
    test_function("任务链功能", "TaskNode 创建和状态", test_task_node)
    test_function("任务链功能", "TaskChainManager 基本操作", test_task_chain_manager)
    test_function("任务链功能", "MultiTargetBuffer 基本操作", test_multi_target_buffer)


def test_vision_functional():
    """测试视觉功能"""
    print("\n" + "=" * 60)
    print("测试视觉功能")
    print("=" * 60)
    
    def test_camera_router():
        from capabilities.vision.camera_router import CameraRouter, CameraId
        router = CameraRouter()
        assert router.get_active_camera() == CameraId.FRONT
        router.set_camera_available("down", True)
        router.select_camera({"need_down_view": True})
        assert router.get_active_camera() == CameraId.DOWN
    
    def test_vision_scheduler():
        from capabilities.vision.vision_scheduler import VisionScheduler, SchedulerContext
        scheduler = VisionScheduler()
        ctx = SchedulerContext(
            cpu_load=0.5,
            motion_detected=True,
            task_priority=5,
            last_infer_ts=0.0,
            now_ts=1.0
        )
        result = scheduler.should_infer(ctx)
        assert isinstance(result, bool)
    
    test_function("视觉功能", "CameraRouter 基本操作", test_camera_router)
    test_function("视觉功能", "VisionScheduler 基本操作", test_vision_scheduler)


def test_decision_functional():
    """测试决策功能"""
    print("\n" + "=" * 60)
    print("测试决策功能")
    print("=" * 60)
    
    def test_decision_request():
        from core.framework.decision.decision_core import DecisionRequest
        req = DecisionRequest(
            user_id="test_user",
            utterance="测试",
            extra={"test": "data"}
        )
        assert req.user_id == "test_user"
        assert req.utterance == "测试"
    
    test_function("决策功能", "DecisionRequest 创建", test_decision_request)


def test_tts_policy_functional():
    """测试 TTS 策略功能"""
    print("\n" + "=" * 60)
    print("测试 TTS 策略功能")
    print("=" * 60)
    
    def test_broadcast_policy():
        from core.framework.runtime.tts_policy.broadcast_policy import BroadcastPolicy, BroadcastPriority
        policy = BroadcastPolicy()
        message = {"type": "safety", "text": "注意安全"}
        priority = policy.get_priority(message)
        assert priority == BroadcastPriority.CRITICAL
    
    test_function("TTS策略功能", "BroadcastPolicy 基本操作", test_broadcast_policy)


def generate_report():
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("功能测试报告")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for category, results in test_results.items():
        print(f"\n{category}:")
        for test_name, success, error in results:
            total_tests += 1
            if success:
                passed_tests += 1
                print(f"  ✅ {test_name}")
            else:
                failed_tests += 1
                print(f"  ❌ {test_name}: {error}")
    
    print("\n" + "=" * 60)
    print("测试统计")
    print("=" * 60)
    if total_tests > 0:
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"失败: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
    print("=" * 60)
    
    if failed_tests == 0:
        print("\n✅ 所有功能测试通过！")
        return True
    else:
        print(f"\n⚠️  有 {failed_tests} 个功能测试失败")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("Luna v1.4 → v1.5 迁移后功能测试")
    print("=" * 60)
    
    test_task_chain_functional()
    test_vision_functional()
    test_decision_functional()
    test_tts_policy_functional()
    
    success = generate_report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
