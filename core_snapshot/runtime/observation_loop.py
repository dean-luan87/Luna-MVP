# -*- coding: utf-8 -*-
"""
唯一采样节拍入口：只允许这里决定 sampled，其他任何模块不许节流/判断采样。
v1.1 Phase-Locked Sampling：采样相位锁定到虚拟时间轴 t0 + n*interval，与运行耗时解耦。
"""
from .clock import CLOCK
from .observation_builders import build_empty_observation_frame

OBS_INTERVAL_SEC = 1.0  # v1 固定，后续再参数化


class ObservationLoop:
    def __init__(self):
        self._last_tick_ts = CLOCK.now()
        self.t0 = CLOCK.now()
        self.sample_index = 0
        self.next_sample_ts = self.t0 + OBS_INTERVAL_SEC

    def step(self, build_real_fn, now=None):
        """
        build_real_fn(now, dt, seq) -> ObservationFrame，仅在采样时刻被调用。
        seq = sample_index（相位锁定，与调用时机无关）。
        now: 若提供则用此时间（视频回放时用 frame_ts 保证确定性），否则用 CLOCK.now()。
        """
        if now is None:
            now = CLOCK.now()
        dt = now - self._last_tick_ts
        self._last_tick_ts = now

        if now >= self.next_sample_ts:
            seq = self.sample_index
            obs = build_real_fn(now, dt, seq)
            self.sample_index += 1
            self.next_sample_ts = self.t0 + self.sample_index * OBS_INTERVAL_SEC
            return obs
        return build_empty_observation_frame(now, dt, 0)
