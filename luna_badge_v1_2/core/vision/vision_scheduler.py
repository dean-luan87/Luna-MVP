from dataclasses import dataclass
from typing import Literal
from infra.logging_manager import get_logger

logger = get_logger("vision_scheduler")

SchedulerMode = Literal["fast", "smart", "low"]


@dataclass
class SchedulerContext:
    cpu_load: float
    motion_detected: bool
    task_priority: int
    last_infer_ts: float
    now_ts: float


class VisionScheduler:
    def __init__(self) -> None:
        self.mode: SchedulerMode = "smart"
        self._intervals = {
            "fast": 0.0,
            "smart": 0.3,
            "low": 0.8,
        }

    def update_mode(self, ctx: SchedulerContext) -> SchedulerMode:
        if ctx.cpu_load > 0.8:
            self.mode = "low"
        elif ctx.motion_detected or ctx.task_priority >= 8:
            self.mode = "fast"
        else:
            self.mode = "smart"
        logger.debug(f"[SCHED] mode={self.mode}, cpu={ctx.cpu_load:.2f}")
        return self.mode

    def should_infer(self, ctx: SchedulerContext) -> bool:
        mode = self.update_mode(ctx)
        min_interval = self._intervals[mode]
        if ctx.now_ts - ctx.last_infer_ts >= min_interval:
            return True
        return False
