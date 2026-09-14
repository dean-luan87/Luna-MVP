# intervention/p4_planner_v0.py
"""
P4 v0：表达结构控制。
不决定「说不说」，只决定「说成什么形态」；只读、可解释、不引入学习/情绪/生成。
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class SpeechPlan:
    style: str                 # ONE_LINER / TWO_STEP / ASK_CONFIRM
    prefix: str = ""
    suffix: str = ""
    max_tokens_hint: int = 48   # 仅提示，不硬控
    reason: str = "OK"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "style": self.style,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "max_tokens_hint": self.max_tokens_hint,
            "reason": self.reason,
        }


@dataclass
class P4Config:
    # 阈值（v0 固化）
    vc_low: float = 0.55
    complexity_high: float = 0.65
    pal_high: float = 0.22

    # token hint（v0 固化）
    tokens_one_liner: int = 32
    tokens_two_step: int = 64
    tokens_confirm: int = 28


def plan_speech_p4_v0(
    *,
    cfg: P4Config,
    winner_type: str,
    engagement_level: str,
    control_mode: str,
    view_confidence: float,
    complexity_effective: float,
    pal_horizon_difficulty: float,
    speak_budget_scale: Optional[float] = None,
) -> SpeechPlan:
    """
    P4 不决定「说不说」，只决定「怎么说」。
    输出必须可解释。
    """
    winner_type = (winner_type or "NONE").upper()
    engagement_level = (engagement_level or "L0").upper()
    control_mode = (control_mode or "ASSISTED").upper()
    vc = float(view_confidence or 0.0)
    ce = float(complexity_effective or 0.0)
    pal = float(pal_horizon_difficulty or 0.0)

    # SAFETY 永远短句
    if winner_type == "SAFETY":
        return SpeechPlan(
            style="ONE_LINER",
            prefix="注意：",
            suffix="",
            max_tokens_hint=cfg.tokens_one_liner,
            reason="SAFETY_SHORT",
        )

    # GUARDED：只允许短句或确认（不允许 two-step）
    guarded = control_mode == "GUARDED"

    # 低 VC / 高复杂度 / PAL 高：倾向确认
    risky_to_overstate = (vc < cfg.vc_low) or (ce >= cfg.complexity_high) or (pal >= cfg.pal_high)

    # 预算紧张也更克制（可选）
    if speak_budget_scale is not None and speak_budget_scale < 0.7:
        risky_to_overstate = True

    # engagement 低（L1/L0）也更克制
    if engagement_level in ("L0", "L1"):
        risky_to_overstate = True

    if risky_to_overstate:
        return SpeechPlan(
            style="ASK_CONFIRM",
            prefix="我先确认一下：",
            suffix="需要我继续提醒吗？",
            max_tokens_hint=cfg.tokens_confirm,
            reason="LOW_CONF_OR_HIGH_COMPLEXITY",
        )

    # 非风险：可 two-step（先提醒，再补一句）
    if not guarded:
        return SpeechPlan(
            style="TWO_STEP",
            prefix="提醒一下：",
            suffix="我会继续留意。",
            max_tokens_hint=cfg.tokens_two_step,
            reason="OK_TWO_STEP",
        )

    # GUARDED 兜底
    return SpeechPlan(
        style="ONE_LINER",
        prefix="提醒：",
        suffix="",
        max_tokens_hint=cfg.tokens_one_liner,
        reason="GUARDED_ONE_LINER",
    )
