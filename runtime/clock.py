# -*- coding: utf-8 -*-
"""
单一时间源：所有时间都来自 SystemClock.now()（单调秒）。
硬约束：后续任何模块都不许再自己 time.time() / 自己维护 last_ts。
"""
import time


class SystemClock:
    def __init__(self):
        self._t0 = time.monotonic()

    def now(self) -> float:
        return time.monotonic() - self._t0  # seconds, monotonic


CLOCK = SystemClock()
