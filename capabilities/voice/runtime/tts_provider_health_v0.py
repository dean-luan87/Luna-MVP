# -*- coding: utf-8 -*-
"""
Provider health + circuit breaker state (v0).

Scope: runtime-only memory; never writes to disk by default.
Hard boundary: does not change navigation semantics; does not generate speech text.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class CircuitBreakerConfig:
    failure_count_threshold: int = 3
    failure_window_ms: int = 300_000  # 5 min window
    open_duration_ms: int = 300_000  # 5 min open
    half_open_probe_count: int = 1


@dataclass
class CircuitState:
    state: str = "closed"  # closed | open | half_open
    consecutive_failures: int = 0
    open_until_s: float = 0.0
    half_open_remaining: int = 0
    last_failure_reason: Optional[str] = None
    last_failure_at_s: float = 0.0
    last_success_at_s: float = 0.0


class ProviderHealthStoreV0:
    def __init__(self) -> None:
        self.qwen = CircuitState()

    @staticmethod
    def _now() -> float:
        return time.time()

    def should_skip_qwen(self, *, cfg: CircuitBreakerConfig, now_s: Optional[float] = None) -> bool:
        now = float(now_s if now_s is not None else self._now())
        st = self.qwen
        if st.state == "open":
            if now < st.open_until_s:
                return True
            # transition to half-open
            st.state = "half_open"
            st.half_open_remaining = max(1, int(cfg.half_open_probe_count or 1))
            return False
        if st.state == "half_open":
            # allow limited probes
            return st.half_open_remaining <= 0
        return False

    def note_qwen_probe_attempt(self) -> None:
        st = self.qwen
        if st.state == "half_open" and st.half_open_remaining > 0:
            st.half_open_remaining -= 1

    def note_qwen_success(self, *, now_s: Optional[float] = None) -> None:
        now = float(now_s if now_s is not None else self._now())
        st = self.qwen
        st.last_success_at_s = now
        st.consecutive_failures = 0
        st.last_failure_reason = None
        st.state = "closed"
        st.open_until_s = 0.0
        st.half_open_remaining = 0

    def note_qwen_failure(self, *, cfg: CircuitBreakerConfig, reason: str, now_s: Optional[float] = None) -> None:
        now = float(now_s if now_s is not None else self._now())
        st = self.qwen
        st.last_failure_at_s = now
        st.last_failure_reason = str(reason or "unknown")
        st.consecutive_failures += 1
        if st.consecutive_failures >= int(cfg.failure_count_threshold or 3):
            st.state = "open"
            st.open_until_s = now + (int(cfg.open_duration_ms or 300_000) / 1000.0)


# process-global store (mainline runtime)
PROVIDER_HEALTH_V0 = ProviderHealthStoreV0()

