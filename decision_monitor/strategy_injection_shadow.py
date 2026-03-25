# -*- coding: utf-8 -*-
"""
Strategy Injection Shadow M0（策略注入影子验证）

定位（写死）：
- 影子验证层，不是注入执行层：只输出“如果注入，会怎样”的轻量预估
- 不真正注入，不改主逻辑，不做复杂模拟器/多轮评估/图书馆接入
- 主要服务后续图书馆/策略库接入前的“先过 shadow 再决定是否真注入”
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class StrategyInjectionShadowResult:
    injection_target_module: Optional[str] = None
    injection_mode: Optional[str] = None
    shadow_applied: bool = False

    expected_tree_change: Optional[str] = None
    expected_metric_change: Optional[str] = None
    expected_issue_relief: Optional[str] = None

    expected_risk_level: str = "unknown"  # low/medium/high/unknown
    shadow_reason: Optional[str] = None
    recommended_next_step: Optional[str] = None

    library_integration_ready: bool = False
    shadow_reserved_for_library: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "injection_target_module": self.injection_target_module,
            "injection_mode": self.injection_mode,
            "shadow_applied": bool(self.shadow_applied),
            "expected_tree_change": self.expected_tree_change,
            "expected_metric_change": self.expected_metric_change,
            "expected_issue_relief": self.expected_issue_relief,
            "expected_risk_level": self.expected_risk_level,
            "shadow_reason": self.shadow_reason,
            "recommended_next_step": self.recommended_next_step,
            "library_integration_ready": bool(self.library_integration_ready),
            "shadow_reserved_for_library": bool(self.shadow_reserved_for_library),
        }


def _risk_from_mode(mode: Optional[str]) -> str:
    m = (mode or "").strip().lower()
    if m == "weight_patch":
        return "high"
    if m == "rule_patch":
        return "medium"
    if m in ("strategy_hint", "validation_template"):
        return "low"
    return "unknown"


def _expected_tree_change(target: Optional[str]) -> str:
    t = (target or "").strip()
    if t == "hypothesis_layer":
        return "may reduce branch expansion"
    if t == "optimization_hint":
        return "may improve hint-to-action alignment"
    if t == "recheck_planner":
        return "may shorten blocked or fallback path"
    if t == "experience_evolution":
        return "may stabilize governance decision path"
    return "may affect decision path"


def _expected_metric_change(target: Optional[str]) -> str:
    t = (target or "").strip()
    if t == "hypothesis_layer":
        return "dead_branch_count↓, prune_rate↓, branch_count↓"
    if t == "optimization_hint":
        return "resolution_path_length↓, tree_depth↓"
    if t == "confirmation_input_bridge":
        return "effective_feedback_count↑, feedback_not_effective缓解"
    if t == "recheck_planner":
        return "blocked_without_resolution缓解, resolution_path_length↓"
    if t == "experience_evolution":
        return "governance path更稳（watchlist/blocked摇摆减少，占位）"
    return "unknown metric impact"


def _expected_issue_relief(issue_type: Optional[str]) -> str:
    it = (issue_type or "").strip()
    if not it:
        return "no strong issue-targeted relief expected"
    if it == "high_dead_branch_ratio":
        return "may relieve dead-branch issue"
    if it == "tree_too_deep":
        return "may relieve deep-tree issue"
    if it == "feedback_not_effective":
        return "may improve feedback convergence"
    if it == "blocked_without_resolution":
        return "may relieve blocked-state issue"
    if it == "too_many_branches":
        return "may reduce over-branching issue"
    return f"may relieve issue: {it}"


def build_strategy_injection_shadow(
    *,
    injection_slot: Optional[Dict[str, Any]],
    optimization_hint: Optional[Dict[str, Any]],
    optimization_feedback_loop: Optional[Dict[str, Any]],
    reasoning_tree_metrics: Optional[Dict[str, Any]],
    reasoning_structure_tree: Optional[Dict[str, Any]],
) -> StrategyInjectionShadowResult:
    """
    M0 最小生成规则：
    - 若 injection_slot_reserved=true 则生成 shadow；否则 shadow_applied=false
    - target/mode 直接来自 slot
    - expected_* 按 target 与 issue_type 粗映射
    - risk_level 仅由 mode 推断
    """
    slot = injection_slot or {}
    reserved = bool(slot.get("injection_slot_reserved") is True)
    if not reserved:
        return StrategyInjectionShadowResult(
            injection_target_module=_s(slot.get("injection_target_module")),
            injection_mode=_s(slot.get("injection_mode")),
            shadow_applied=False,
            expected_risk_level="unknown",
            shadow_reason="无注入口预留，跳过影子验证。",
            recommended_next_step="do_not_execute_now",
            library_integration_ready=False,
            shadow_reserved_for_library=True,
        )

    target = _s(slot.get("injection_target_module"))
    mode = _s(slot.get("injection_mode"))
    issue_type = _s((reasoning_tree_metrics or {}).get("possible_tree_issue_type")) or _s((optimization_hint or {}).get("trigger_issue_type")) or _s((optimization_feedback_loop or {}).get("current_issue_type"))

    risk = _risk_from_mode(mode)
    tree_change = _expected_tree_change(target)
    metric_change = _expected_metric_change(target)
    issue_relief = _expected_issue_relief(issue_type)

    # next step (M0 default)
    next_step = "keep_reserved_only" if risk in ("medium", "high") else "validate_with_library_when_enabled"

    reason = f"slot_reserved=true target={target or '—'} mode={mode or '—'} issue={issue_type or '—'}; no real injection executed"
    return StrategyInjectionShadowResult(
        injection_target_module=target,
        injection_mode=mode,
        shadow_applied=True,
        expected_tree_change=tree_change,
        expected_metric_change=metric_change,
        expected_issue_relief=issue_relief,
        expected_risk_level=risk,
        shadow_reason=reason,
        recommended_next_step=next_step,
        library_integration_ready=False,
        shadow_reserved_for_library=True,
    )

