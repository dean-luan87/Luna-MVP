#!/usr/bin/env python3
"""
基础验证脚本：测试 v1.4.2 新模块的基本导入和实例化
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_vision_modules():
    """测试 vision 模块"""
    print("测试 vision 模块...")
    from core.vision.camera_router import CameraRouter, CameraId
    from core.vision.vision_scheduler import VisionScheduler, SchedulerContext, SchedulerMode
    from core.vision.vision_fail_safe import VisionFailSafe, FailSafeConfig, FailSafeState
    
    router = CameraRouter()
    assert router.get_active_camera() == "front"
    
    scheduler = VisionScheduler()
    assert scheduler.get_mode() == "smart"
    
    failsafe = VisionFailSafe()
    assert failsafe.get_state() == "normal"
    print("✅ vision 模块测试通过")


def test_system_modules():
    """测试 system 模块"""
    print("测试 system 模块...")
    from core.system.system_recovery_center import RecoveryCenter, ModuleHeartbeat
    from core.system.safe_mode import SafeModeManager, SafeModeContext
    
    def dummy_get_cpu():
        return 0.5
    
    def dummy_safe_mode():
        pass
    
    center = RecoveryCenter(
        get_cpu_load=dummy_get_cpu,
        safe_mode_enter=dummy_safe_mode,
    )
    assert center is not None
    
    def dummy_tts(text):
        pass
    
    safe_mode = SafeModeManager(tts_say=dummy_tts)
    assert not safe_mode.is_active()
    print("✅ system 模块测试通过")


def test_task_modules():
    """测试 task 模块"""
    print("测试 task 模块...")
    from core.task.task_transition_manager import (
        TaskTransitionManager,
        TaskDecision,
        PositionState,
        UserIntentState,
        TaskContext,
    )
    from core.task.multi_target_buffer import MultiTargetBuffer, Target
    from core.task.query_bus import QueryBus, QueryStatus
    
    def dummy_ask():
        pass
    
    mgr = TaskTransitionManager(ask_end_callback=dummy_ask)
    assert mgr is not None
    
    buffer = MultiTargetBuffer()
    assert buffer.is_finished() is False
    
    def dummy_tts(text):
        pass
    
    bus = QueryBus(tts_say=dummy_tts)
    assert bus is not None
    print("✅ task 模块测试通过")


if __name__ == "__main__":
    try:
        test_vision_modules()
        test_system_modules()
        test_task_modules()
        print("\n🎉 所有 v1.4.2 模块基础测试通过！")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




