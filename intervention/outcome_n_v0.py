# outcome_n_v0.py
# N 层 v0：系统里唯一「敢下结论」的地方
# 只做三件事：把 J 的事实信号 → 归因为 Outcome；不改历史、不学习；给 trace 稳定可统计结构

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from intervention.engaged_failure import EngagedSignal


# ===== v0 冻结 reason 枚举（无 FAIL / ERROR / SHOULD_HAVE_DONE）=====
REASON_ACTION_EXECUTED = "ACTION_EXECUTED"
REASON_BLOCKED_COOLDOWN = "BLOCKED_COOLDOWN"
REASON_BLOCKED_RHYTHM = "BLOCKED_RHYTHM"
REASON_BLOCKED_ARBITRATION = "BLOCKED_ARBITRATION"
REASON_BLOCKED_UNKNOWN = "BLOCKED_UNKNOWN"
REASON_NOT_ATTEMPTED = "NOT_ATTEMPTED"


# ===== Data Structure =====

@dataclass
class Outcome:
    """
    N 层输出：一次 ENGAGED tick 的最终结果归因
    """
    outcome_type: str        # ACTION / NO_ACTION
    reason: str              # WHY（稳定枚举）
    confidence: float         # 0.0–1.0（v0 固定规则）
    evidence: Dict[str, Any]  # 原始证据（供分析，不参与决策）

    def to_trace_dict(self) -> Dict[str, Any]:
        return {
            "outcome_type": self.outcome_type,
            "reason": self.reason,
            "confidence": self.confidence,
            "apply_now": False,  # v0 shadow-only，不干预行为
            "evidence": dict(self.evidence),
        }


# ===== Core: J 信号 → Outcome =====

def compute_outcome_v0(
    *,
    engaged_signal: Optional[EngagedSignal],
) -> Optional[Outcome]:
    """
    N 层 v0：Outcome 归因（只在 ENGAGED 时产出）

    返回：
    - None：本 tick 未进入 ENGAGED
    - Outcome：一次 ENGAGED tick 的最终归因
    """
    if engaged_signal is None:
        return None

    # 情况 1：成功执行行为
    if engaged_signal.executed:
        return Outcome(
            outcome_type="ACTION",
            reason=REASON_ACTION_EXECUTED,
            confidence=1.0,
            evidence={
                "engaged_signal": asdict(engaged_signal),
            },
        )

    # 情况 2：尝试过，但被阻断
    if engaged_signal.attempted and engaged_signal.blocked:
        stage = engaged_signal.block_stage or "UNKNOWN"
        reason_map = {
            "COOLDOWN": REASON_BLOCKED_COOLDOWN,
            "RHYTHM": REASON_BLOCKED_RHYTHM,
            "ARBITRATION": REASON_BLOCKED_ARBITRATION,
        }
        return Outcome(
            outcome_type="NO_ACTION",
            reason=reason_map.get(stage, REASON_BLOCKED_UNKNOWN),
            confidence=0.7,
            evidence={
                "engaged_signal": asdict(engaged_signal),
            },
        )

    # 情况 3：理论兜底（不应频繁发生）
    return Outcome(
        outcome_type="NO_ACTION",
        reason=REASON_NOT_ATTEMPTED,
        confidence=0.3,
        evidence={
            "engaged_signal": asdict(engaged_signal),
        },
    )
