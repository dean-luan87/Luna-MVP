from __future__ import annotations

from typing import Any, Optional

from a3.engine import A3Engine
from a3.config import A3Config
from a3.providers.default import DefaultA3SignalProvider


class A3Runtime:
    """
    Runtime wiring for A3.
    - Read-only: collects signals and updates runtime context.
    - Safe default: A3Config(enabled=False)
    """

    def __init__(self, config: A3Config, managers: Any):
        self.engine = A3Engine(config)
        self.provider = DefaultA3SignalProvider(
            risk_mgr=managers.risk,
            nav_mgr=managers.nav,
            vision_mgr=managers.vision,
            advice_mgr=managers.advice,
            task_mgr=managers.task,
        )
        self.last_mode = None
        self.last_signals = None

    def tick(self, runtime_ctx: Any, now_ms: Optional[int] = None):
        signals = self.provider.collect()
        mode = self.engine.tick(signals, now_ms)
        setattr(runtime_ctx, "env_mode", mode)
        self.last_signals = signals
        self.last_mode = mode
        return mode
