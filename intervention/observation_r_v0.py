# intervention/observation_r_v0.py
# R v0：Post-Execution Observation（执行后观测层）
# 只读 / 只统计 / 只解释；不改决策、不触发行为、不写回系统状态。

from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
import time


# -----------------------------
# 冻结枚举（R v0）
# -----------------------------

class RHealthSignal(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    STALLED = "STALLED"
    UNKNOWN = "UNKNOWN"


class RObservationType(str, Enum):
    EXECUTION_OK = "EXECUTION_OK"
    EXECUTION_BLOCKED = "EXECUTION_BLOCKED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


# -----------------------------
# R v0 数据结构
# -----------------------------

@dataclass
class RObservation:
    ts: float
    observation_type: RObservationType
    reason: str
    rolling_window_sec: int
    snapshot: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "observation_type": self.observation_type.value,
            "reason": self.reason,
            "rolling_window_sec": self.rolling_window_sec,
            "snapshot": self.snapshot,
        }


# -----------------------------
# R v0 核心聚合器
# -----------------------------

class ObservationRCollectorV0:
    """
    R v0：执行后观测聚合器

    - 输入：Q 层 outcome（一次一次喂）
    - 输出：只读观测（RObservation）
    """

    def __init__(self, rolling_window_sec: int = 300):
        self.rolling_window_sec = rolling_window_sec
        self.events = []  # [(ts, outcome_dict)]

    # ---------- public API ----------

    def feed(self, outcome_q: Dict[str, Any]) -> Optional[RObservation]:
        """
        喂入一次 Q outcome
        可能返回一条 RObservation，也可能返回 None
        """
        now = time.time()
        self.events.append((now, outcome_q))
        self._evict_old(now)

        return self._build_observation(now)

    # ---------- internal ----------

    def _evict_old(self, now: float) -> None:
        cutoff = now - self.rolling_window_sec
        self.events = [(ts, e) for ts, e in self.events if ts >= cutoff]

    def _reason_and_executed(self, e: Dict[str, Any]) -> tuple:
        """从 Q outcome 中取 reason / executed（兼容 meta 或顶层）。"""
        meta = e.get("meta") or {}
        reason = meta.get("reason", e.get("reason", ""))
        executed = meta.get("executed", e.get("executed", False))
        return reason, executed

    def _build_observation(self, now: float) -> Optional[RObservation]:
        if not self.events:
            return None

        total = len(self.events)
        executed = 0
        blocked = 0
        failed = 0

        for _, e in self.events:
            reason, executed_flag = self._reason_and_executed(e)
            if executed_flag:
                executed += 1
            elif reason.startswith("BLOCKED") or reason == "APPLY_NOW_FALSE" or reason == "ACTION_NOT_ALLOWED_IN_V0":
                blocked += 1
            elif reason.startswith("FAILED") or reason == "EMPTY_TEXT" or (reason and "TTS_ERROR" in reason):
                failed += 1

        # v0 观测规则（冻结）
        if executed > 0:
            obs_type = RObservationType.EXECUTION_OK
            main_reason = "EXECUTED_PRESENT"
        elif blocked > 0 and failed == 0:
            obs_type = RObservationType.EXECUTION_BLOCKED
            main_reason = "ONLY_BLOCKED"
        elif failed > 0:
            obs_type = RObservationType.EXECUTION_FAILED
            main_reason = "FAILED_PRESENT"
        else:
            return None

        snapshot = {
            "total_events": total,
            "executed": executed,
            "blocked": blocked,
            "failed": failed,
            "executed_ratio": executed / total if total else 0.0,
            "blocked_ratio": blocked / total if total else 0.0,
            "failed_ratio": failed / total if total else 0.0,
        }

        return RObservation(
            ts=now,
            observation_type=obs_type,
            reason=main_reason,
            rolling_window_sec=self.rolling_window_sec,
            snapshot=snapshot,
        )
