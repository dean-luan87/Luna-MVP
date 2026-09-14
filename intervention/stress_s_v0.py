# intervention/stress_s_v0.py
# S v0：System Stress / Disturbance Observer
# 从 R 的长期执行统计判断「执行压强是否异常」；只读、只解释，不反馈、不干预。

from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
import time


# -----------------------------
# 冻结枚举（S v0）
# -----------------------------

class SStressLevel(str, Enum):
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    SATURATED = "SATURATED"
    UNKNOWN = "UNKNOWN"


class SStressReason(str, Enum):
    EXECUTION_HEALTHY = "EXECUTION_HEALTHY"
    LONG_BLOCKED = "LONG_BLOCKED"
    BLOCKED_WITH_INTENT = "BLOCKED_WITH_INTENT"
    NO_EXECUTION_OBSERVED = "NO_EXECUTION_OBSERVED"


# -----------------------------
# S v0 数据结构
# -----------------------------

@dataclass
class SStressReport:
    ts: float
    stress_level: SStressLevel
    reason: SStressReason
    window_sec: int
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "stress_level": self.stress_level.value,
            "reason": self.reason.value,
            "window_sec": self.window_sec,
            "evidence": self.evidence,
        }


# -----------------------------
# S v0 核心推导器
# -----------------------------

class StressObserverSV0:
    """
    S v0：系统打扰压力观测器

    输入：RObservation（滚动窗口执行统计）
    输出：SStressReport（shadow-only）
    """

    def __init__(
        self,
        blocked_ratio_warn: float = 0.6,
        blocked_ratio_critical: float = 0.85,
        min_events: int = 5,
    ):
        self.blocked_ratio_warn = blocked_ratio_warn
        self.blocked_ratio_critical = blocked_ratio_critical
        self.min_events = min_events

    def observe(self, r_obs: Dict[str, Any]) -> Optional[SStressReport]:
        """
        基于一条 RObservation 生成 SStressReport
        """
        now = time.time()

        snapshot = r_obs.get("snapshot", {})
        total = snapshot.get("total_events", 0)
        executed = snapshot.get("executed", 0)
        blocked_ratio = snapshot.get("blocked_ratio", 0.0)

        # 防御：数据不足不判断
        if total < self.min_events:
            return None

        # ---------- 判定逻辑（v0 冻结） ----------

        if executed > 0:
            stress = SStressLevel.NORMAL
            reason = SStressReason.EXECUTION_HEALTHY

        elif blocked_ratio >= self.blocked_ratio_critical:
            stress = SStressLevel.SATURATED
            reason = SStressReason.LONG_BLOCKED

        elif blocked_ratio >= self.blocked_ratio_warn:
            stress = SStressLevel.ELEVATED
            reason = SStressReason.BLOCKED_WITH_INTENT

        else:
            stress = SStressLevel.UNKNOWN
            reason = SStressReason.NO_EXECUTION_OBSERVED

        evidence = {
            "total_events": total,
            "executed": executed,
            "blocked_ratio": blocked_ratio,
            "blocked_ratio_warn": self.blocked_ratio_warn,
            "blocked_ratio_critical": self.blocked_ratio_critical,
        }

        return SStressReport(
            ts=now,
            stress_level=stress,
            reason=reason,
            window_sec=r_obs.get("rolling_window_sec", 0),
            evidence=evidence,
        )
