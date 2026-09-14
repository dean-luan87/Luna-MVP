# intervention/p3_policy_v0.py
"""
P3 v0：说话节律控制器（Temporal / Rhythmic Gate）
不决定「说不说」内容，只决定「现在是不是合适的说话时机」。
P2 之后、真正执行 SAY 之前的最后一道节律闸门。
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class P3Config:
    min_gap_s: float = 8.0          # 两次说话的最小间隔
    min_engaged_s: float = 2.0      # 进入 ENGAGED 后的最小稳定时间
    max_rhythm_flips: int = 2       # 短时间内节律翻转阈值
    rhythm_window_s: float = 5.0    # 节律翻转观察窗口


@dataclass
class P3Decision:
    allow: bool
    reason: str
    checks: Dict[str, bool]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allow": self.allow,
            "reason": self.reason,
            "checks": self.checks,
        }


class RhythmHistory:
    def __init__(self):
        self.records = []  # list of (ts, state)

    def add(self, ts: float, state: str):
        self.records.append((ts, state))

    def prune(self, now: float, window_s: float):
        self.records = [(t, s) for (t, s) in self.records if now - t <= window_s]

    def flip_count(self) -> int:
        if len(self.records) < 2:
            return 0
        flips = 0
        for i in range(1, len(self.records)):
            if self.records[i][1] != self.records[i - 1][1]:
                flips += 1
        return flips


class P3State:
    def __init__(self):
        self.last_say_ts: float = 0.0
        self.engaged_enter_ts: float = 0.0
        self.rhythm_history = RhythmHistory()


def decide_p3_allow(
    *,
    cfg: P3Config,
    state: P3State,
    now_ts: float,
    rhythm_state: str,
) -> P3Decision:
    checks = {
        "gap_ok": True,
        "engaged_stable": True,
        "rhythm_stable": True,
    }

    # 记录节律
    state.rhythm_history.add(now_ts, rhythm_state)
    state.rhythm_history.prune(now_ts, cfg.rhythm_window_s)

    # 规则 1：说话间隔
    if state.last_say_ts > 0 and (now_ts - state.last_say_ts) < cfg.min_gap_s:
        checks["gap_ok"] = False

    # 规则 2：ENGAGED 稳定时间
    if rhythm_state == "ENGAGED":
        if state.engaged_enter_ts == 0:
            state.engaged_enter_ts = now_ts
        elif (now_ts - state.engaged_enter_ts) < cfg.min_engaged_s:
            checks["engaged_stable"] = False
    else:
        state.engaged_enter_ts = 0.0

    # 规则 3：节律抖动
    if state.rhythm_history.flip_count() > cfg.max_rhythm_flips:
        checks["rhythm_stable"] = False

    allow = all(checks.values())
    if not allow:
        return P3Decision(
            allow=False,
            reason="BLOCKED_BAD_RHYTHM",
            checks=checks,
        )

    return P3Decision(
        allow=True,
        reason="OK_RHYTHM",
        checks=checks,
    )
