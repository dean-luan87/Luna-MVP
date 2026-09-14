from core.vision.vision_scheduler import VisionScheduler, SchedulerContext


def test_scheduler_mode_switch():
    sched = VisionScheduler()

    ctx = SchedulerContext(
        cpu_load=0.2,
        motion_detected=False,
        task_priority=3,
        last_infer_ts=0.0,
        now_ts=1.0,
    )
    assert sched.should_infer(ctx) is True
    assert sched.mode == "smart"

    ctx.cpu_load = 0.9
    ctx.last_infer_ts = 1.0
    ctx.now_ts = 1.9  # low 模式需要 0.8 秒间隔
    assert sched.should_infer(ctx) is True
    assert sched.mode == "low"

    ctx.cpu_load = 0.3
    ctx.motion_detected = True
    ctx.last_infer_ts = 1.5
    ctx.now_ts = 1.6
    assert sched.should_infer(ctx) is True
    assert sched.mode == "fast"

