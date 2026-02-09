# -*- coding: utf-8 -*-
"""
ENGAGED 介入强度 v0：在 ENGAGED 内细化为 L1/L2/L3

目标：把介入从「开/关」细化为强度等级，输出给下游做参数调制。
不决定说什么，只决定介入强度等级和频率预算。

A1 v0 语义（时间累计版）：
- L2 进入条件：累计满足 PAL/复杂度/VC 条件的连续时长 >= L2_HOLD_SECONDS 秒（dt 按 obs.dt，与采样频率无关）。
- 补丁 v1：状态推进只能发生在 should_advance_state(obs)==True；禁止 time.time/行数/自管采样节奏。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.observation_frame import ObservationFrame

# A1 阈值：验收要求「每行 L2 的 PAL≥此值」，与 verify_a1_acceptance 一致
PAL_L2_THRESHOLD = 0.19
# 维持 L2：在 L2 内每 tick 需 PAL≥此值否则立即降回 L1，压低 L2 占比至 1%–10%
PAL_L2_MAINTAIN = 0.21
COMPLEXITY_L2_THRESHOLD = 0.5
VC_L2_THRESHOLD = 0.6
# L2 进入需累计满足条件 >= 此秒数（时间语义，与采样无关）
L2_HOLD_SECONDS = 3.0

# 兼容旧验收脚本（样本语义已由时间累计替代，仅导出供 verify 引用）
L2_HOLD_ENGAGED_SAMPLES = 3


# ----- A1 时间累计（方案 A） -----

@dataclass
class A1Thresholds:
    pal_l2_threshold: float = 0.19
    complexity_threshold: float = 0.50
    vc_threshold: float = 0.60
    l2_hold_seconds: float = 3.0
    dt_min: float = 0.0
    dt_max: float = 1.5


@dataclass
class A1LevelState:
    l2_acc_seconds: float = 0.0
    last_ts: Optional[float] = None
    level: int = 0  # 0=L0, 1=L1, 2=L2（仅 A1 输出，L3 由上层覆盖）


def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def _compute_dt(ts: Optional[float], last_ts: Optional[float], th: A1Thresholds) -> float:
    if ts is None or last_ts is None:
        return 0.0
    dt = ts - last_ts
    if dt < 0:
        return 0.0
    return _clamp(dt, th.dt_min, th.dt_max)


def _meet_l2_gate(engaged: bool, pal: float, complexity: float, vc: float, th: A1Thresholds) -> bool:
    if not engaged:
        return False
    if pal < th.pal_l2_threshold:
        return False
    if complexity < th.complexity_threshold:
        return False
    if vc < th.vc_threshold:
        return False
    return True


def a1_update_level_time_accum(
    st: A1LevelState,
    *,
    ts: Optional[float],
    engaged: bool,
    pal: float,
    complexity: float,
    vc: float,
    th: A1Thresholds,
) -> None:
    """每来一条样本调用一次；原地更新 st。"""
    dt = _compute_dt(ts, st.last_ts, th)
    if _meet_l2_gate(engaged, pal, complexity, vc, th):
        st.l2_acc_seconds += dt
    else:
        st.l2_acc_seconds = 0.0

    if st.l2_acc_seconds >= th.l2_hold_seconds:
        st.level = 2
    else:
        if st.level == 2:
            st.level = 1
    st.last_ts = ts


@dataclass
class EngagementOutput:
    level: str = "L0"
    advice_scale: float = 0.0
    pal_lookahead_m: float = 0.0
    speak_cooldown_s: float = 0.0


class EngagementV0:
    """
    介入强度 v0：仅在 rhythm.state==ENGAGED 时计算 L1/L2/L3。
    A1：L2 按时间累计（满足条件 >= L2_HOLD_SECONDS 秒）进入；降级仍为连续 2 窗口。
    """

    def __init__(self) -> None:
        self._level = "L0"
        self._down_counter = 0
        self._a1_state = A1LevelState()
        self._a1_th = A1Thresholds(
            pal_l2_threshold=PAL_L2_THRESHOLD,
            complexity_threshold=COMPLEXITY_L2_THRESHOLD,
            vc_threshold=VC_L2_THRESHOLD,
            l2_hold_seconds=L2_HOLD_SECONDS,
            dt_min=0.0,
            dt_max=1.5,
        )

    def _params(self, level: str) -> tuple[float, float, float]:
        return {
            "L1": (0.7, 8.0, 8.0),
            "L2": (0.85, 12.0, 6.0),
            "L3": (1.0, 18.0, 4.0),
        }.get(level, (0.0, 0.0, 0.0))

    def on_observation(
        self,
        obs: "ObservationFrame",
        *,
        rhythm_state: str,
    ) -> EngagementOutput:
        """
        补丁 v1 入口：仅当 should_advance_state(obs) 时推进 L2/TTL/冷却；否则只更新时间基准，不推进状态。
        禁止自行计算 dt，必须使用 obs.dt。
        """
        from runtime.gates import should_advance_state

        if not should_advance_state(obs):
            if self._a1_state.last_ts is not None:
                self._a1_state.last_ts = obs.ts
            return self._current_output()

        engaged = rhythm_state == "ENGAGED"
        if not engaged:
            self._level = "L0"
            self._down_counter = 0
            self._a1_state.l2_acc_seconds = 0.0
            self._a1_state.last_ts = None
            self._a1_state.level = 0
            return EngagementOutput()

        # 使用 obs.dt，禁止自己算 ts 差
        dt = _clamp(obs.dt, self._a1_th.dt_min, self._a1_th.dt_max)
        if _meet_l2_gate(
            True,
            obs.pal,
            obs.complexity,
            obs.vc,
            self._a1_th,
        ):
            self._a1_state.l2_acc_seconds += dt
        else:
            self._a1_state.l2_acc_seconds = 0.0

        if self._a1_state.l2_acc_seconds >= self._a1_th.l2_hold_seconds:
            self._a1_state.level = 2
        else:
            if self._a1_state.level == 2:
                self._a1_state.level = 1
        self._a1_state.last_ts = obs.ts

        target = "L2" if self._a1_state.level == 2 else "L1"
        if target == "L2" and obs.pal < PAL_L2_MAINTAIN:
            target = "L1"
            self._a1_state.l2_acc_seconds = 0.0
            self._a1_state.level = 1
        if (
            obs.pal >= 0.50
            and obs.complexity >= 0.75
            and obs.vc >= 0.75
            and obs.control_mode != "GUARDED"
        ):
            target = "L3"

        if target > self._level:
            self._level = target
            self._down_counter = 0
        elif target < self._level:
            self._down_counter += 1
            if self._down_counter >= 2:
                self._level = target
                self._down_counter = 0
        else:
            self._down_counter = 0

        return self._current_output()

    def _current_output(self) -> EngagementOutput:
        scale, look, cd = self._params(self._level)
        return EngagementOutput(
            level=self._level,
            advice_scale=scale,
            pal_lookahead_m=look,
            speak_cooldown_s=cd,
        )

    def tick(
        self,
        *,
        now: float,
        rhythm_state: str,
        pal: float,
        complexity: float,
        vc: float,
        control_mode: str,
    ) -> EngagementOutput:
        """Legacy：供未接 ObservationFrame 的路径或测试使用；生产路径请用 on_observation(obs, rhythm_state=...)。"""
        from runtime.observation_builders import build_observation_frame

        last_ts = self._a1_state.last_ts
        dt = _compute_dt(now, last_ts, self._a1_th) if rhythm_state == "ENGAGED" else 0.0
        obs = build_observation_frame(
            ts=now,
            dt=dt,
            seq=0,
            sampled=True,
            motion=0.0,
            path=0.0,
            branch=0.0,
            roi=0,
            pal=pal,
            complexity=complexity,
            vc=vc,
            frame_quality="GOOD",
            control_mode=control_mode,
        )
        return self.on_observation(obs, rhythm_state=rhythm_state)

    def reset(self) -> None:
        """重置状态（用于测试）"""
        self._level = "L0"
        self._down_counter = 0
        self._a1_state.l2_acc_seconds = 0.0
        self._a1_state.last_ts = None
        self._a1_state.level = 0


_ENGAGEMENT: Optional[EngagementV0] = None


def get_engagement_v0() -> EngagementV0:
    global _ENGAGEMENT
    if _ENGAGEMENT is None:
        _ENGAGEMENT = EngagementV0()
    return _ENGAGEMENT


def reset_engagement_state() -> None:
    """重置介入强度状态（用于测试）"""
    global _ENGAGEMENT
    if _ENGAGEMENT is not None:
        _ENGAGEMENT.reset()
