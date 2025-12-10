from dataclasses import dataclass
from typing import Literal
import time
from infra.logging_manager import get_logger

logger = get_logger("vision_fail_safe")

FailSafeState = Literal["normal", "degraded"]


@dataclass
class VisionErrorCounters:
    infer_timeout_count: int = 0
    model_error_count: int = 0
    camera_error_count: int = 0

    def reset(self) -> None:
        self.infer_timeout_count = 0
        self.model_error_count = 0
        self.camera_error_count = 0


@dataclass
class FailSafeConfig:
    timeout_threshold: int = 3
    model_error_threshold: int = 2
    camera_error_threshold: int = 2
    cooldown_seconds: int = 10


class VisionFailSafe:
    def __init__(self, config: FailSafeConfig) -> None:
        self.config = config
        self.counters = VisionErrorCounters()
        self.state: FailSafeState = "normal"
        self._last_trigger_ts: float = 0.0

    def report_infer_timeout(self) -> None:
        self.counters.infer_timeout_count += 1
        logger.error("[FAIL_SAFE] infer timeout reported")
        self._evaluate_state()

    def report_model_error(self) -> None:
        self.counters.model_error_count += 1
        logger.error("[FAIL_SAFE] model error reported")
        self._evaluate_state()

    def report_camera_error(self) -> None:
        self.counters.camera_error_count += 1
        logger.error("[FAIL_SAFE] camera error reported")
        self._evaluate_state()

    def reset(self) -> None:
        self.counters.reset()
        self.state = "normal"

    def _evaluate_state(self) -> None:
        now = time.time()
        if now - self._last_trigger_ts < self.config.cooldown_seconds:
            return

        if (
            self.counters.infer_timeout_count >= self.config.timeout_threshold
            or self.counters.model_error_count >= self.config.model_error_threshold
            or self.counters.camera_error_count >= self.config.camera_error_threshold
        ):
            if self.state != "degraded":
                logger.error("[FAIL_SAFE] enter degraded mode, use tiny model.")
            self.state = "degraded"
            self._last_trigger_ts = now
            self.counters.reset()

    def get_state(self) -> FailSafeState:
        return self.state
