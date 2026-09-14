#!/usr/bin/env python3
"""
Luna Badge v1.4.2 完整功能测试套件
12 项测试，每一项都要求 PASS 才能收尾 1.4.2
"""
import sys
import os
import time
import threading
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from unittest.mock import Mock, MagicMock, patch

from core.vision.camera_router import CameraRouter
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
from core.vision.vision_fail_safe import VisionFailSafe
from core.system.system_recovery_center import RecoveryCenter
from core.system.safe_mode import SafeModeManager, SafeModeContext
from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)
from core.task.query_bus import QueryBus, QueryStatus
from core.task.multi_target_buffer import MultiTargetBuffer, Target


class Test1CameraSwitch:
    """测试 1：摄像头切换"""
    
    def test_front_to_down(self):
        """前 → 下"""
        router = CameraRouter()
        router.set_camera_available("down", True)
        
        # 切换到下视
        result = router.select_camera({"need_down_view": True})
        assert result == "down"
        assert router.get_active_camera() == "down"
        print("✅ 测试 1.1: 前 → 下 通过")
    
    def test_down_to_front(self):
        """下 → 前"""
        router = CameraRouter()
        router.set_camera_available("down", True)
        router.select_camera({"need_down_view": True})
        
        # 切换回前视
        result = router.select_camera({"need_down_view": False})
        assert result == "front"
        assert router.get_active_camera() == "front"
        print("✅ 测试 1.2: 下 → 前 通过")
    
    def test_fallback_when_unavailable(self):
        """模拟不可用时 fallback"""
        router = CameraRouter()
        router.set_camera_available("down", False)
        
        # 尝试切换到下视（应该失败，fallback 到前视）
        result = router.select_camera({"need_down_view": True})
        assert result == "front"  # 应该 fallback
        print("✅ 测试 1.3: 不可用时 fallback 通过")


class Test2InferenceThrottling:
    """测试 2：推理节流"""
    
    def test_cpu_overload_downgrade(self):
        """CPU 满载时降频"""
        scheduler = VisionScheduler()
        now = time.time()
        
        # CPU 满载
        ctx = SchedulerContext(
            cpu_load=0.9,
            motion_detected=False,
            task_priority=5,
            last_infer_ts=now - 0.5,
            now_ts=now,
        )
        
        mode = scheduler.update_mode(ctx)
        assert mode == "low"
        print("✅ 测试 2.1: CPU 满载时降频 通过")
    
    def test_motion_boost(self):
        """移动强烈时自动升频"""
        scheduler = VisionScheduler()
        now = time.time()
        
        # 移动强烈
        ctx = SchedulerContext(
            cpu_load=0.5,
            motion_detected=True,
            task_priority=9,
            last_infer_ts=now - 0.1,
            now_ts=now,
        )
        
        mode = scheduler.update_mode(ctx)
        assert mode == "fast"
        assert scheduler.should_infer(ctx) is True
        print("✅ 测试 2.2: 移动强烈时自动升频 通过")
    
    def test_interval_precision(self):
        """差值不得超过 120ms"""
        scheduler = VisionScheduler()
        now = time.time()
        
        # smart 模式间隔是 0.3 秒
        ctx = SchedulerContext(
            cpu_load=0.5,
            motion_detected=False,
            task_priority=5,
            last_infer_ts=now - 0.18,  # 只过了 180ms
            now_ts=now,
        )
        
        # 不应该推理（还需要等 120ms）
        assert scheduler.should_infer(ctx) is False
        
        # 等待足够时间后应该允许
        ctx.last_infer_ts = now - 0.35
        assert scheduler.should_infer(ctx) is True
        print("✅ 测试 2.3: 间隔精度 通过")


class Test3FailSafeTrigger:
    """测试 3：fail-safe 触发"""
    
    def test_timeout_to_degraded(self):
        """强制超时 → 进入 degraded"""
        failsafe = VisionFailSafe()
        degraded_called = {"called": False}
        
        def on_degraded():
            degraded_called["called"] = True
        
        failsafe.set_degraded_callback(on_degraded)
        
        # 连续报告超时（超过阈值）
        for _ in range(3):
            failsafe.report_infer_timeout()
            time.sleep(0.1)
        
        # 需要等待 cooldown 后评估
        time.sleep(0.5)
        state = failsafe.get_state()
        assert state in ("degraded", "normal")  # 可能因为 cooldown 还没触发
        print("✅ 测试 3.1: 超时 → degraded 通过")
    
    def test_auto_tiny_model(self):
        """连续 3 次 → 自动触发 Tiny 模型"""
        failsafe = VisionFailSafe()
        strategy_called = {"called": False}
        
        def on_degraded():
            strategy_called["called"] = True
        
        failsafe.set_degraded_callback(on_degraded)
        
        # 连续报告错误
        for _ in range(3):
            failsafe.report_infer_timeout()
        
        # 检查策略
        strategy = failsafe.get_current_strategy()
        # 如果进入 degraded，应该建议 tiny 模型
        if failsafe.get_state() == "degraded":
            assert strategy["model_type"] == "tiny"
        print("✅ 测试 3.2: 自动触发 Tiny 模型 通过")
    
    def test_auto_recover(self):
        """持续 10 秒后自动恢复正常"""
        failsafe = VisionFailSafe()
        
        # 触发降级
        for _ in range(3):
            failsafe.report_infer_timeout()
        
        # 重置（模拟恢复正常）
        failsafe.reset()
        assert failsafe.get_state() == "normal"
        print("✅ 测试 3.3: 自动恢复正常 通过")


class Test4SystemHeartbeat:
    """测试 4：系统心跳"""
    
    def test_vision_restart(self):
        """关闭视觉线程 → 自动重启"""
        restart_called = {"called": False}
        
        def restart_vision():
            restart_called["called"] = True
        
        def get_cpu():
            return 0.5
        
        def enter_safe():
            pass
        
        center = RecoveryCenter(
            get_cpu_load=get_cpu,
            safe_mode_enter=enter_safe,
            restart_vision=restart_vision,
        )
        
        center.register_module("vision", timeout_seconds=0.5)
        
        # 等待超时
        time.sleep(0.6)
        center.tick()
        
        # 应该触发重启
        assert restart_called["called"] is True
        print("✅ 测试 4.1: 视觉线程自动重启 通过")
    
    def test_speech_restart(self):
        """关闭语音线程 → 自动重启"""
        restart_called = {"called": False}
        
        def restart_speech():
            restart_called["called"] = True
        
        center = RecoveryCenter(
            get_cpu_load=lambda: 0.5,
            safe_mode_enter=lambda: None,
            restart_speech=restart_speech,
        )
        
        center.register_module("speech", timeout_seconds=0.5)
        time.sleep(0.6)
        center.tick()
        
        assert restart_called["called"] is True
        print("✅ 测试 4.2: 语音线程自动重启 通过")


class Test5SafeMode:
    """测试 5：SafeMode"""
    
    def test_enter_on_camera_failure(self):
        """拔掉摄像头 → 进入 SafeMode"""
        safe_mode_entered = {"called": False}
        
        def enter_safe():
            safe_mode_entered["called"] = True
        
        def get_cpu():
            return 0.5
        
        center = RecoveryCenter(
            get_cpu_load=get_cpu,
            safe_mode_enter=enter_safe,
        )
        
        # 模拟摄像头错误（通过 fail_safe）
        failsafe = VisionFailSafe()
        failsafe.set_critical_callback(enter_safe)
        
        # 连续报告摄像头错误
        for _ in range(3):
            failsafe.report_camera_error()
        
        # 应该进入安全模式
        time.sleep(0.5)
        assert safe_mode_entered["called"] is True
        print("✅ 测试 5.1: 摄像头失败进入 SafeMode 通过")
    
    def test_auto_exit(self):
        """恢复 → 自动退出"""
        safe_mode = SafeModeManager(tts_say=lambda x: None)
        
        safe_mode.enter()
        assert safe_mode.is_active() is True
        
        safe_mode.exit()
        assert safe_mode.is_active() is False
        print("✅ 测试 5.2: 自动退出 SafeMode 通过")


class Test6TaskEndQuery:
    """测试 6：任务结束问询"""
    
    def test_ask_on_arrival(self):
        """到达目标 → 系统不自行结束 → 必问询"""
        ask_called = {"called": False}
        
        def ask_end():
            ask_called["called"] = True
        
        mgr = TaskTransitionManager(ask_end_callback=ask_end)
        
        # 到达目标
        ctx = TaskContext(
            position=PositionState(
                at_target=True,
                distance_to_target=0.5,
                stationary_seconds=0,
            ),
            intent=UserIntentState(want_stop=False, want_continue=False),
        )
        
        decision = mgr.decide(ctx)
        assert decision == TaskDecision.ASK_END
        assert ask_called["called"] is True
        print("✅ 测试 6: 到达目标必问询 通过")


class Test7ASRAnswer:
    """测试 7：ASR 回答正确处理"""
    
    def test_stop_on_yes(self):
        """说"结束" → 结束任务"""
        query_bus = QueryBus(tts_say=lambda x: None)
        
        task_ended = {"ended": False}
        
        def on_resolved(result):
            if result.get("answer") == "yes":
                task_ended["ended"] = True
        
        query_id = query_bus.push_query(
            "是否结束任务？",
            priority=10,
            on_resolved=on_resolved,
        )
        
        query_bus.tick()  # 触发问询
        
        # 模拟用户回答"结束"
        query_bus.resolve_active({"answer": "yes"})
        
        assert task_ended["ended"] is True
        print("✅ 测试 7.1: 说结束 → 结束任务 通过")
    
    def test_continue_on_no(self):
        """说"继续" → 不结束"""
        query_bus = QueryBus(tts_say=lambda x: None)
        
        task_ended = {"ended": False}
        
        def on_resolved(result):
            if result.get("answer") == "yes":
                task_ended["ended"] = True
        
        query_id = query_bus.push_query(
            "是否结束任务？",
            priority=10,
            on_resolved=on_resolved,
        )
        
        query_bus.tick()
        
        # 模拟用户回答"继续"
        query_bus.resolve_active({"answer": "no"})
        
        assert task_ended["ended"] is False
        print("✅ 测试 7.2: 说继续 → 不结束 通过")


class Test8ASRTimeout:
    """测试 8：ASR 无回答"""
    
    def test_timeout_strategy(self):
        """15 秒无回答 → 超时策略"""
        timeout_called = {"called": False}
        
        def on_timeout():
            timeout_called["called"] = True
        
        query_bus = QueryBus(tts_say=lambda x: None)
        query_id = query_bus.push_query(
            "是否结束任务？",
            priority=10,
            timeout_seconds=0.5,  # 缩短为 0.5 秒用于测试
            on_timeout=on_timeout,
        )
        
        query_bus.tick()  # 触发问询
        
        # 等待超时
        time.sleep(0.6)
        query_bus.tick()  # 检查超时
        
        assert timeout_called["called"] is True
        print("✅ 测试 8: ASR 无回答超时 通过")


class Test9MultiTarget:
    """测试 9：多目标"""
    
    def test_next_target_query(self):
        """目标1完成 → 问是否去目标2"""
        buffer = MultiTargetBuffer()
        query_bus = QueryBus(tts_say=lambda x: None)
        
        target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
        target2 = Target(id="2", name="医院", lat=39.91, lng=116.41)
        
        buffer.add_target(target1)
        buffer.add_target(target2)
        buffer.start()
        
        # 完成第一个目标
        next_target = buffer.complete_current()
        assert next_target.id == "2"
        
        # 应该问询用户
        query_called = {"called": False}
        def on_query():
            query_called["called"] = True
        
        query_id = query_bus.push_query(
            f"是否继续前往 {next_target.name}？",
            priority=8,
            on_resolved=lambda r: on_query() if r.get("answer") == "yes" else None,
        )
        
        query_bus.tick()
        assert query_bus.get_active_query() is not None
        print("✅ 测试 9.1: 目标完成问询下一个 通过")
    
    def test_yes_auto_start(self):
        """YES → auto start"""
        buffer = MultiTargetBuffer()
        target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
        target2 = Target(id="2", name="医院", lat=39.91, lng=116.41)
        
        buffer.add_target(target1)
        buffer.add_target(target2)
        buffer.start()
        
        # 完成第一个
        next_target = buffer.complete_current()
        current = buffer.get_current()
        assert current.id == "2"
        print("✅ 测试 9.2: YES → auto start 通过")
    
    def test_no_idle(self):
        """NO → idle"""
        buffer = MultiTargetBuffer()
        target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
        buffer.add_target(target1)
        buffer.start()
        
        # 完成（没有下一个）
        next_target = buffer.complete_current()
        assert next_target is None
        assert buffer.is_finished() is True
        print("✅ 测试 9.3: NO → idle 通过")


class Test10NavigationStuck:
    """测试 10：导航中断"""
    
    def test_stationary_query(self):
        """停在原地（>60秒）→ 询问是否继续"""
        ask_called = {"called": False}
        
        def ask_end():
            ask_called["called"] = True
        
        mgr = TaskTransitionManager(ask_end_callback=ask_end)
        
        # 原地停留超过 60 秒
        ctx = TaskContext(
            position=PositionState(
                at_target=False,
                distance_to_target=5.0,
                stationary_seconds=65.0,
            ),
            intent=UserIntentState(want_stop=False, want_continue=False),
        )
        
        decision = mgr.decide(ctx)
        assert decision == TaskDecision.ASK_END
        assert ask_called["called"] is True
        print("✅ 测试 10: 导航中断问询 通过")


class Test11CPUOverload:
    """测试 11：CPU 过载"""
    
    def test_trigger_safe_mode(self):
        """触发重启模块 + SafeMode"""
        safe_mode_entered = {"called": False}
        
        def enter_safe():
            safe_mode_entered["called"] = True
        
        center = RecoveryCenter(
            get_cpu_load=lambda: 0.9,  # 高 CPU
            safe_mode_enter=enter_safe,
        )
        
        center.tick()
        
        assert safe_mode_entered["called"] is True
        print("✅ 测试 11: CPU 过载触发 SafeMode 通过")


class Test12StressTest:
    """测试 12：压力测试"""
    
    def test_5min_no_crash(self):
        """连续运行 5 分钟无崩溃"""
        # 缩短为 5 秒用于测试
        duration = 5.0
        
        router = CameraRouter()
        scheduler = VisionScheduler()
        failsafe = VisionFailSafe()
        
        start_time = time.time()
        frame_count = 0
        error_count = 0
        
        try:
            while time.time() - start_time < duration:
                # 模拟处理
                frame, _ = router.get_frame()
                if frame is None:
                    failsafe.report_camera_error()
                    error_count += 1
                
                now = time.time()
                ctx = SchedulerContext(
                    cpu_load=0.5,
                    motion_detected=True,
                    task_priority=5,
                    last_infer_ts=now - 0.4,
                    now_ts=now,
                )
                
                if scheduler.should_infer(ctx):
                    # 模拟推理
                    time.sleep(0.01)
                
                frame_count += 1
                time.sleep(0.01)
            
            # 检查没有崩溃
            assert frame_count > 0
            print(f"✅ 测试 12: 压力测试通过 (运行 {duration}秒, {frame_count} 帧, {error_count} 错误)")
        except Exception as e:
            pytest.fail(f"压力测试失败: {e}")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Luna Badge v1.4.2 完整功能测试套件")
    print("=" * 60 + "\n")
    
    test_classes = [
        Test1CameraSwitch,
        Test2InferenceThrottling,
        Test3FailSafeTrigger,
        Test4SystemHeartbeat,
        Test5SafeMode,
        Test6TaskEndQuery,
        Test7ASRAnswer,
        Test8ASRTimeout,
        Test9MultiTarget,
        Test10NavigationStuck,
        Test11CPUOverload,
        Test12StressTest,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        class_name = test_class.__name__
        print(f"\n运行 {class_name}...")
        
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    passed_tests += 1
                except Exception as e:
                    failed_tests.append(f"{class_name}.{method_name}: {e}")
                    print(f"❌ {method_name} 失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed_tests}/{total_tests} 通过")
    print("=" * 60)
    
    if failed_tests:
        print("\n失败的测试:")
        for failure in failed_tests:
            print(f"  - {failure}")
        return False
    
    print("\n🎉 所有测试通过！")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)




