# -*- coding: utf-8 -*-
"""
ACTIVE × PAL 节律 v0：何时进入/退出介入态

目标：当「有资格介入」且「世界即将变复杂」时，
     系统什么时候开始介入？介入多久？什么时候退出？

v0 只决定「要不要进入介入态」，不决定「说什么」。
完全不影响 safety / eligibility。
"""

from __future__ import annotations

from typing import Optional, Union

from .eligibility import TaskState


# v0 固定参数
T_PREPARE_MIN = 2.0  # PREPARE 最少持续 2 秒才可进入 ENGAGED
T_ENGAGED_MIN = 5.0  # ENGAGED 最少持续 5 秒才可退出
T_COOLDOWN = 5.0  # ENGAGED→IDLE 后冷却 5 秒
PAL_ENTER_PREPARE = 0.15  # PAL ≥ 此值可进入 PREPARE
PAL_ENTER_ENGAGED = 0.20  # PAL ≥ 此值且 PREPARE 满 2 秒可进入 ENGAGED
PAL_EXIT = 0.08  # PAL < 此值可退出（降低退出阈值以延长 ENGAGED 段，便于 A1 占比验收）
VC_GATE = 0.6  # view_confidence 门禁


class ActivePalRhythmV0:
    """
    节律 v0 状态机：IDLE → PREPARE → ENGAGED

    宁愿慢 1–2 秒介入，也绝不来回抖动。
    """

    def __init__(self) -> None:
        self.state = "IDLE"
        self.t_enter_prepare: Optional[float] = None
        self.t_enter_engaged: Optional[float] = None
        self.t_last_exit: Optional[float] = None

    def tick(
        self,
        now: float,
        pal: float,
        eligible: bool,
        vc: float,
        task_state: Union[TaskState, str],
    ) -> str:
        """
        每 tick 调用，返回当前状态。

        Args:
            now: 当前时间戳
            pal: pal_horizon_difficulty
            eligible: 介入资格（来自 Eligibility Gate）
            vc: view_confidence
            task_state: ACTIVE / PASSIVE / NONE

        Returns:
            "IDLE" | "PREPARE" | "ENGAGED"
        """
        ts = self._normalize_task_state(task_state)

        if self.state == "IDLE":
            if (
                ts == "ACTIVE"
                and eligible
                and pal >= PAL_ENTER_PREPARE
                and vc >= VC_GATE
                and self._cooldown_passed(now)
            ):
                self.state = "PREPARE"
                self.t_enter_prepare = now

        elif self.state == "PREPARE":
            if pal < PAL_EXIT:
                self.state = "IDLE"
                self.t_enter_prepare = None
            elif (
                pal >= PAL_ENTER_ENGAGED
                and self.t_enter_prepare is not None
                and (now - self.t_enter_prepare) >= T_PREPARE_MIN
            ):
                self.state = "ENGAGED"
                self.t_enter_engaged = now
                self.t_enter_prepare = None

        elif self.state == "ENGAGED":
            if (
                (pal < PAL_EXIT or ts != "ACTIVE")
                and self.t_enter_engaged is not None
                and (now - self.t_enter_engaged) >= T_ENGAGED_MIN
            ):
                self.state = "IDLE"
                self.t_last_exit = now
                self.t_enter_engaged = None

        return self.state

    def _cooldown_passed(self, now: float) -> bool:
        if self.t_last_exit is None:
            return True
        return (now - self.t_last_exit) >= T_COOLDOWN

    def _normalize_task_state(self, ts: Union[TaskState, str]) -> str:
        if isinstance(ts, TaskState):
            return ts.value
        return str(ts)

    def reset(self) -> None:
        """重置状态（用于测试或新会话）"""
        self.state = "IDLE"
        self.t_enter_prepare = None
        self.t_enter_engaged = None
        self.t_last_exit = None


# 全局单例（跨 tick 持久化）
_RHYTHM: Optional[ActivePalRhythmV0] = None


def get_rhythm_v0() -> ActivePalRhythmV0:
    global _RHYTHM
    if _RHYTHM is None:
        _RHYTHM = ActivePalRhythmV0()
    return _RHYTHM


def reset_rhythm_state() -> None:
    """重置节律状态（用于测试）"""
    global _RHYTHM
    if _RHYTHM is not None:
        _RHYTHM.reset()
