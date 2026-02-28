#!/usr/bin/env python3
"""
直接测试 v1.4.2 新模块（绕过 __init__.py 的依赖问题）
"""
import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_vision_modules_direct():
    """直接测试 vision 模块文件"""
    print("测试 vision 模块（直接导入）...")
    
    # 直接导入文件，不通过 __init__.py
    from core.vision.camera_router import CameraRouter
    from core.vision.vision_scheduler import VisionScheduler, SchedulerContext
    from core.vision.vision_fail_safe import VisionFailSafe
    
    router = CameraRouter()
    assert router.get_active_camera() == "front"
    router.set_camera_available("down", True)
    router.select_camera({"need_down_view": True})
    assert router.get_active_camera() == "down"
    print("  ✅ camera_router")
    
    scheduler = VisionScheduler()
    ctx = SchedulerContext(
        cpu_load=0.5,
        motion_detected=True,
        task_priority=9,
        last_infer_ts=time.time() - 0.4,
        now_ts=time.time(),
    )
    assert scheduler.should_infer(ctx) is True
    print("  ✅ vision_scheduler")
    
    failsafe = VisionFailSafe()
    assert failsafe.get_state() == "normal"
    strategy = failsafe.get_current_strategy()
    assert strategy["model_type"] == "standard"
    print("  ✅ vision_fail_safe")


def test_system_modules_direct():
    """直接测试 system 模块文件"""
    print("测试 system 模块（直接导入）...")
    
    from core.system.system_recovery_center import RecoveryCenter
    from core.system.safe_mode import SafeModeManager, SafeModeContext
    
    def dummy_get_cpu():
        return 0.5
    
    def dummy_safe_mode():
        pass
    
    center = RecoveryCenter(
        get_cpu_load=dummy_get_cpu,
        safe_mode_enter=dummy_safe_mode,
    )
    center.register_module("test_module", timeout_seconds=5.0)
    center.update_heartbeat("test_module")
    status = center.get_health_status()
    assert "test_module" in status["modules"]
    print("  ✅ system_recovery_center")
    
    def dummy_tts(text):
        pass
    
    safe_mode = SafeModeManager(tts_say=dummy_tts)
    assert not safe_mode.is_active()
    safe_mode.enter()
    assert safe_mode.is_active()
    ctx = SafeModeContext(obstacle_distance=0.8)
    safe_mode.handle_frame(ctx)
    print("  ✅ safe_mode")


def test_task_modules_direct():
    """直接测试 task 模块文件"""
    print("测试 task 模块（直接导入）...")
    
    # 直接导入文件，不通过 __init__.py
    from core.task.task_transition_manager import (
        TaskTransitionManager,
        TaskDecision,
        PositionState,
        UserIntentState,
        TaskContext,
    )
    from core.task.multi_target_buffer import MultiTargetBuffer, Target
    from core.task.query_bus import QueryBus, QueryStatus
    
    called = {"ask": False}
    def dummy_ask():
        called["ask"] = True
    
    mgr = TaskTransitionManager(ask_end_callback=dummy_ask)
    ctx = TaskContext(
        position=PositionState(at_target=True, distance_to_target=0.5, stationary_seconds=0),
        intent=UserIntentState(want_stop=False, want_continue=False),
    )
    decision = mgr.decide(ctx)
    assert decision == TaskDecision.ASK_END
    assert called["ask"] is True
    print("  ✅ task_transition_manager")
    
    buffer = MultiTargetBuffer()
    target1 = Target(id="1", name="711", lat=39.9, lng=116.4)
    buffer.add_target(target1)
    current = buffer.start()
    assert current.id == "1"
    print("  ✅ multi_target_buffer")
    
    def dummy_tts(text):
        pass
    
    bus = QueryBus(tts_say=dummy_tts)
    query_id = bus.push_query("测试问询", priority=5)
    assert query_id is not None
    bus.tick()
    active = bus.get_active_query()
    assert active is not None
    assert active.status == QueryStatus.WAITING_USER
    print("  ✅ query_bus")


if __name__ == "__main__":
    try:
        test_vision_modules_direct()
        test_system_modules_direct()
        test_task_modules_direct()
        print("\n🎉 所有 v1.4.2 新模块测试通过！")
        print("\n📦 已创建以下模块：")
        print("  ✅ core/vision/camera_router.py")
        print("  ✅ core/vision/vision_scheduler.py")
        print("  ✅ core/vision/vision_fail_safe.py")
        print("  ✅ core/system/system_recovery_center.py")
        print("  ✅ core/system/safe_mode.py")
        print("  ✅ core/task/task_transition_manager.py")
        print("  ✅ core/task/multi_target_buffer.py")
        print("  ✅ core/task/query_bus.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




