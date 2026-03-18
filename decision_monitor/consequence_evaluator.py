# -*- coding: utf-8 -*-
"""
后果层轻量真实化：根据当前决策与状态输出 expected_gain / cost / risk 等。

规则驱动，不做预测引擎。情况：floor_forced、b2_impact、sample_and_run、skip。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .schema import ConsequenceLayer, DecisionLayer, OutputsLayer


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def evaluate(
    ctx: Dict[str, Any],
    decision: DecisionLayer,
    outputs: Optional[OutputsLayer] = None,
) -> ConsequenceLayer:
    """
    根据当前决策与输出做轻量规则型后果评估。
    优先级：守底 > B2 介入 > 正常采样执行 > 节流跳过。
    """
    floor_forced = ctx.get("detector_floor_due") or ctx.get("ocr_floor_due") or ctx.get("floor_forced")
    policy_intent = ctx.get("policy_intent")
    b2_applied = bool(_get(policy_intent, "b2_impact_applied", False))
    policy_should_sample = ctx.get("policy_should_sample")
    decision_owner = _get(decision, "decision_owner")

    action_summary = None
    modules_run = None
    modules_skipped = None
    if outputs is not None:
        action_summary = _get(outputs, "action_summary")
        modules_run = _get(outputs, "modules_run")
        modules_skipped = _get(outputs, "modules_skipped")

    risk_score = ctx.get("risk_score")
    risk_str = f"risk={risk_score:.2f}" if risk_score is not None else "低"

    expected_gain = "维持观测与守底"
    expected_cost = "算力与延迟"
    expected_risk = risk_str
    consequence_confidence = 0.85
    evaluation_horizon_ms = 500.0
    rollback_hint = "下一周期重判"
    post_action_check_needed = True

    # A) 守底：floor_forced / floor_guard
    if floor_forced or decision_owner == "floor_guard":
        expected_gain = "避免突破最小观察底线，保证安全守底"
        expected_cost = "额外采样与执行成本"
        expected_risk = "低（安全收益大于代价）"
        consequence_confidence = 0.9
        rollback_hint = "下一周期重判；若仍 floor_due 继续强制采样"
        post_action_check_needed = True
        return ConsequenceLayer(
            expected_gain=expected_gain,
            expected_cost=expected_cost,
            expected_risk=expected_risk,
            consequence_confidence=consequence_confidence,
            evaluation_horizon_ms=evaluation_horizon_ms,
            rollback_hint=rollback_hint,
            post_action_check_needed=post_action_check_needed,
        )

    # B) B2 介入
    if b2_applied or decision_owner == "b2_impact":
        expected_gain = "提高对弱变化的确认能力"
        expected_cost = "采样/执行密度提高"
        expected_risk = "中低（功耗增加，非环境高危）"
        consequence_confidence = 0.8
        rollback_hint = "下一周期重判；B2 解除后恢复常规节奏"
        post_action_check_needed = True
        return ConsequenceLayer(
            expected_gain=expected_gain,
            expected_cost=expected_cost,
            expected_risk=expected_risk,
            consequence_confidence=consequence_confidence,
            evaluation_horizon_ms=evaluation_horizon_ms,
            rollback_hint=rollback_hint,
            post_action_check_needed=post_action_check_needed,
        )

    # C) 正常 sample_and_run（controller 且 policy_should_sample）
    if policy_should_sample is not False and decision_owner == "controller":
        expected_gain = "维持观察连续性，完成本轮检测/OCR"
        expected_cost = "一次完整执行成本"
        expected_risk = "低"
        consequence_confidence = 0.85
        rollback_hint = "下一周期重判"
        post_action_check_needed = True
        return ConsequenceLayer(
            expected_gain=expected_gain,
            expected_cost=expected_cost,
            expected_risk=expected_risk,
            consequence_confidence=consequence_confidence,
            evaluation_horizon_ms=evaluation_horizon_ms,
            rollback_hint=rollback_hint,
            post_action_check_needed=post_action_check_needed,
        )

    # D) 节流跳过：sampling_gate / detector 或 OCR 被跳过
    if policy_should_sample is False or decision_owner == "sampling_gate":
        expected_gain = "节省算力，保持节奏"
        expected_cost = "减少细节确认"
        expected_risk = "取决于当前目标和状态；若长时间跳过可能漏检"
        consequence_confidence = 0.75
        rollback_hint = "下一周期重判；floor_due 时会自动恢复采样"
        post_action_check_needed = True
        return ConsequenceLayer(
            expected_gain=expected_gain,
            expected_cost=expected_cost,
            expected_risk=expected_risk,
            consequence_confidence=consequence_confidence,
            evaluation_horizon_ms=evaluation_horizon_ms,
            rollback_hint=rollback_hint,
            post_action_check_needed=post_action_check_needed,
        )

    # 默认
    return ConsequenceLayer(
        expected_gain=expected_gain,
        expected_cost=expected_cost,
        expected_risk=expected_risk,
        consequence_confidence=consequence_confidence,
        evaluation_horizon_ms=evaluation_horizon_ms,
        rollback_hint=rollback_hint,
        post_action_check_needed=post_action_check_needed,
    )
