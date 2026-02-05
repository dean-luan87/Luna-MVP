# tests/test_vision_performance.py
"""
测试视觉性能调度模块
"""
import time
from capabilities.vision.vision_scheduler import VisionScheduler, SchedulerContext


def test_scheduler_mode_fast():
    """测试快速模式"""
    scheduler = VisionScheduler()
    ctx = SchedulerContext(
        cpu_load=0.5,
        motion_detected=True,
        task_priority=9,
        last_infer_ts=time.time() - 0.1,
        now_ts=time.time(),
    )
    mode = scheduler.update_mode(ctx)
    assert mode == "fast"
    assert scheduler.should_infer(ctx) is True


def test_scheduler_mode_low():
    """测试低功耗模式"""
    scheduler = VisionScheduler()
    ctx = SchedulerContext(
        cpu_load=0.9,
        motion_detected=False,
        task_priority=3,
        last_infer_ts=time.time() - 0.1,
        now_ts=time.time(),
    )
    mode = scheduler.update_mode(ctx)
    assert mode == "low"
    # 即使时间间隔短，低功耗模式也需要等待更长时间
    assert scheduler.should_infer(ctx) is False


def test_scheduler_mode_smart():
    """测试智能模式"""
    scheduler = VisionScheduler()
    ctx = SchedulerContext(
        cpu_load=0.6,
        motion_detected=False,
        task_priority=5,
        last_infer_ts=time.time() - 0.4,
        now_ts=time.time(),
    )
    mode = scheduler.update_mode(ctx)
    assert mode == "smart"
    assert scheduler.should_infer(ctx) is True


def test_scheduler_interval_enforcement():
    """测试间隔强制执行"""
    scheduler = VisionScheduler()
    now = time.time()
    ctx = SchedulerContext(
        cpu_load=0.5,
        motion_detected=False,
        task_priority=5,
        last_infer_ts=now - 0.2,  # 只过了 0.2 秒
        now_ts=now,
    )
    # smart 模式需要 0.3 秒间隔
    assert scheduler.should_infer(ctx) is False

    # 等待足够时间后应该允许推理
    ctx.last_infer_ts = now - 0.4
    assert scheduler.should_infer(ctx) is True


if __name__ == "__main__":
    test_scheduler_mode_fast()
    test_scheduler_mode_low()
    test_scheduler_mode_smart()
    test_scheduler_interval_enforcement()
    print("所有测试通过！")















