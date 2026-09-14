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

# P 层 v0 回写 N 的 reason（冻结）
REASON_SAY_OK = "SAY_OK"
REASON_APPLY_NOW_FALSE = "APPLY_NOW_FALSE"
REASON_ACTION_NOT_ALLOWED_IN_V0 = "ACTION_NOT_ALLOWED_IN_V0"
REASON_EMPTY_TEXT = "EMPTY_TEXT"
REASON_TTS_ERROR_PREFIX = "TTS_ERROR:"


# ===== Data Structure =====

@dataclass
class Outcome:
    """
    N 层输出：一次 ENGAGED tick 的最终结果归因
    outcome_type: ACTION | NO_ACTION | ACTION_EXECUTED | ACTION_FAILED（P v0 扩展）
    """
    outcome_type: str        # ACTION / NO_ACTION / ACTION_EXECUTED / ACTION_FAILED
    reason: str              # WHY（稳定枚举）
    confidence: float         # 0.0–1.0（v0 固定规则）
    evidence: Dict[str, Any]  # 原始证据（供分析，不参与决策）
    apply_now: bool = False   # 是否本 tick 实际执行（P 执行时为 True）

    def to_trace_dict(self) -> Dict[str, Any]:
        return {
            "outcome_type": self.outcome_type,
            "reason": self.reason,
            "confidence": self.confidence,
            "apply_now": self.apply_now,
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


# ===== P 层 v0：执行结果 → N Outcome（冻结映射）=====

def outcome_from_p_result(p_result: Dict[str, Any], m_apply_now: bool = False) -> Outcome:
    """
    P 执行结果 → N Outcome，满足「每次执行都有 N.outcome」。
    映射（冻结）：
    - EXECUTED → outcome_type=ACTION_EXECUTED, reason=SAY_OK
    - BLOCKED  → outcome_type=NO_ACTION, reason=APPLY_NOW_FALSE / ACTION_NOT_ALLOWED_IN_V0
    - FAILED   → outcome_type=ACTION_FAILED, reason=EMPTY_TEXT / TTS_ERROR:...
    """
    result_enum = p_result.get("result")
    reason = p_result.get("reason", "UNKNOWN")
    executed = p_result.get("executed", False)

    if result_enum is not None:
        result_name = getattr(result_enum, "value", str(result_enum))
    else:
        result_name = str(p_result.get("result", ""))

    if result_name == "EXECUTED":
        return Outcome(
            outcome_type="ACTION_EXECUTED",
            reason=REASON_SAY_OK,
            confidence=1.0,
            evidence={"p_result": dict(p_result)},
            apply_now=True,
        )
    if result_name == "BLOCKED":
        return Outcome(
            outcome_type="NO_ACTION",
            reason=reason if reason in (REASON_APPLY_NOW_FALSE, REASON_ACTION_NOT_ALLOWED_IN_V0) else reason,
            confidence=0.7,
            evidence={"p_result": dict(p_result)},
            apply_now=False,
        )
    # FAILED
    if reason.startswith(REASON_TTS_ERROR_PREFIX):
        out_reason = reason  # 保留 TTS_ERROR:...
    else:
        out_reason = REASON_EMPTY_TEXT if reason == "EMPTY_TEXT" else reason
    return Outcome(
        outcome_type="ACTION_FAILED",
        reason=out_reason,
        confidence=0.5,
        evidence={"p_result": dict(p_result)},
        apply_now=False,
    )
