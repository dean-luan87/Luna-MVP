# -*- coding: utf-8 -*-
"""
ObservationFrame v1：统一观测帧，带 seq/dt/sampled，消灭隐性状态。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ObservationFrame:
    ts: float  # seconds, CLOCK.now()
    dt: float  # seconds, ts - last_tick_ts
    seq: int  # monotonic increasing
    sampled: bool  # True if real sampling happened

    motion: float
    path: float
    branch: float
    roi: int

    pal: float
    complexity: float
    vc: float

    frame_quality: str  # GOOD/DEGRADED/INVALID/NONE
    control_mode: str  # ASSISTED/GUARDED/SHARED/NONE
