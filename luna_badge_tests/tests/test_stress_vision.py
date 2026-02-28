import time
from core.vision.vision_scheduler import VisionScheduler, SchedulerContext


def test_stress_scheduler_runs_without_error():
    sched = VisionScheduler()
    last_ts = 0.0

    for i in range(1000):
        now = last_ts + 0.02
        ctx = SchedulerContext(
            cpu_load=0.3,
            motion_detected=True,
            task_priority=5,
            last_infer_ts=last_ts,
            now_ts=now,
        )
        _ = sched.should_infer(ctx)
        last_ts = now

    # 能跑完就算 PASS
    assert True
