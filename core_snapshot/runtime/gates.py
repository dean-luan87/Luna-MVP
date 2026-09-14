# -*- coding: utf-8 -*-
"""
推进门闩：只有 sampled=True 且 frame_quality==GOOD 才允许推进 L2/TTL/冷却等世界状态。
"""
from .observation_frame import ObservationFrame


def should_advance_state(obs: ObservationFrame) -> bool:
    return obs.sampled and obs.frame_quality == "GOOD"
