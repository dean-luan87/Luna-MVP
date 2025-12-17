"""Deterministic logical clock for replay mode (v1.4.9 P0-2-A).

Hard rules:
- 禁止使用系统时间 / wall clock
- 禁止隐式 sleep / now / monotonic

This module provides a logical clock driven by step index.
It can patch `time.time()` and `time.sleep()` ONLY within the replay runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional
import contextlib
import time as _time


@dataclass
class ReplayClock:
    t0_ms: int
    delta_ms: int
    steps: int

    step: int = 0

    def now_ms(self) -> int:
        return self.t0_ms + self.step * self.delta_ms

    def now_s(self) -> float:
        return self.now_ms() / 1000.0

    def advance(self, n: int = 1) -> None:
        self.step = min(self.steps, self.step + n)

    def sleep(self, seconds: float) -> None:
        # In replay, sleep is forbidden as wall-clock. We treat it as logical advance.
        if seconds <= 0:
            return
        steps = int(round((seconds * 1000.0) / float(self.delta_ms)))
        if steps <= 0:
            steps = 1
        self.advance(steps)


@contextlib.contextmanager
def patch_time(clock: ReplayClock):
    """Patch time.time and time.sleep for deterministic replay.

    This does NOT modify business logic; it only affects the replay process.
    """

    orig_time: Callable[[], float] = _time.time
    orig_sleep: Callable[[float], None] = _time.sleep
    orig_monotonic: Optional[Callable[[], float]] = getattr(_time, "monotonic", None)

    def _patched_time() -> float:
        return clock.now_s()

    def _patched_sleep(seconds: float) -> None:
        clock.sleep(seconds)

    def _patched_monotonic() -> float:
        return clock.now_s()

    _time.time = _patched_time
    _time.sleep = _patched_sleep
    if orig_monotonic is not None:
        _time.monotonic = _patched_monotonic  # type: ignore[attr-defined]

    try:
        yield
    finally:
        _time.time = orig_time
        _time.sleep = orig_sleep
        if orig_monotonic is not None:
            _time.monotonic = orig_monotonic  # type: ignore[attr-defined]
