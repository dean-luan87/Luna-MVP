# engaged_failure.py
# v0: signal-only
# 说明：
# - 不再输出 FAIL_* 枚举
# - 不再做「为什么失败」的解释
# - 只提供 ENGAGED 阶段的事实信号，供 N 层统一归因

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class EngagedSignal:
    """
    ENGAGED 阶段的事实信号（不含解释）
    """
    attempted: bool               # 本 tick 是否尝试过 ENGAGED 行为
    executed: bool                # 是否真正执行了行为（如 SPEAK）
    blocked: bool                 # 是否被阻断
    block_stage: Optional[str]    # 阻断发生在哪一层（如 RHYTHM / ARBITRATION / COOLDOWN）
    raw_context: Dict[str, Any]   # 原始上下文，供 N 层取证

    def to_trace_dict(self) -> Dict[str, Any]:
        """Trace 写入用；含 block_stage 与 raw_context 供 N 层取证。"""
        out = {
            "attempted": self.attempted,
            "executed": self.executed,
            "blocked": self.blocked,
            "block_stage": self.block_stage,
        }
        if self.raw_context:
            out["raw_context"] = dict(self.raw_context)
        return out


def compute_engaged_signal(
    *,
    engaged: bool,
    action_decided: bool,
    action_executed: bool,
    rhythm_state: Optional[str],
    arbitration_winner: Optional[str],
    cooldown_active: bool,
    extra_context: Optional[Dict[str, Any]] = None,
) -> Optional[EngagedSignal]:
    """
    生成 ENGAGED 信号（signal-only）

    返回：
    - None：本 tick 未处于 ENGAGED，不参与 N 层
    - EngagedSignal：仅描述「发生了什么」，不解释原因
    """

    if not engaged:
        return None

    attempted = True
    executed = bool(action_executed)

    blocked = not executed
    block_stage = None

    if blocked:
        if cooldown_active:
            block_stage = "COOLDOWN"
        elif rhythm_state not in ("ENGAGED",):
            block_stage = "RHYTHM"
        elif arbitration_winner is None:
            block_stage = "ARBITRATION"
        else:
            block_stage = "UNKNOWN"

    return EngagedSignal(
        attempted=attempted,
        executed=executed,
        blocked=blocked,
        block_stage=block_stage,
        raw_context={
            "action_decided": action_decided,
            "action_executed": action_executed,
            "rhythm_state": rhythm_state,
            "arbitration_winner": arbitration_winner,
            "cooldown_active": cooldown_active,
            **(extra_context or {}),
        },
    )
