"""
P5 v0：表达裁剪与说话形态规划（Pre-Execution）。
不决定「说不说」，只决定「如果要说，说成什么样子」。
Shadow-only、无生成、只读上游、可完全验收。
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExpressionLength(str, Enum):
    SHORT = "SHORT"        # ≤ 1 句
    MEDIUM = "MEDIUM"      # 2–3 句
    LONG = "LONG"          # ≥ 4 句（v0 基本不会用）


class ExpressionForm(str, Enum):
    STATEMENT = "STATEMENT"      # 陈述
    QUESTION = "QUESTION"        # 询问
    SUGGESTION = "SUGGESTION"    # 建议
    WARNING = "WARNING"          # 警告（只给 SAFETY）


class ExpressionDensity(str, Enum):
    LOW = "LOW"      # 信息压缩
    NORMAL = "NORMAL"
    HIGH = "HIGH"    # 信息密集（v0 很少）


@dataclass
class ExpressionPlanV0:
    length: ExpressionLength
    form: ExpressionForm
    density: ExpressionDensity
    reason: str               # 可解释原因
    shadow_only: bool = True

    def to_dict(self):
        return {
            "length": self.length.value,
            "form": self.form.value,
            "density": self.density.value,
            "reason": self.reason,
            "shadow_only": self.shadow_only,
        }


def build_expression_plan_v0(
    p1_apply_now: bool,
    p2_allowed: bool,
    p4_style: Optional[str] = None,
    p4_reason: Optional[str] = None,
    winner_type: Optional[str] = None,
) -> ExpressionPlanV0:
    """
    P5 v0：只在 P1 + P2 允许的前提下规划表达形态。
    不改变执行结果（shadow-only）。
    入参为上游结果的可读视图，避免强依赖具体类型。
    """
    length = ExpressionLength.SHORT
    form = ExpressionForm.STATEMENT
    density = ExpressionDensity.LOW
    reason = "DEFAULT_MINIMAL"

    if not p1_apply_now or not p2_allowed:
        return ExpressionPlanV0(
            length=length,
            form=form,
            density=density,
            reason="BLOCKED_UPSTREAM",
        )

    # 根据 P4 风格微调（只读）
    if p4_style is not None or p4_reason is not None:
        if p4_style == "ASK_CONFIRM":
            form = ExpressionForm.QUESTION
            reason = "STYLE_ASK_CONFIRM"
        elif (p4_reason or "").strip().upper() == "SAFETY_SHORT" or (winner_type or "").upper() == "SAFETY":
            form = ExpressionForm.WARNING
            density = ExpressionDensity.HIGH
            reason = "STYLE_WARN"
        elif p4_style == "TWO_STEP":
            form = ExpressionForm.SUGGESTION
            density = ExpressionDensity.NORMAL
            reason = "STYLE_GUIDE"

    return ExpressionPlanV0(
        length=length,
        form=form,
        density=density,
        reason=reason,
    )
