# -*- coding: utf-8 -*-
"""
Optimization Feedback Loop M0（优化建议验证闭环）

定位：
- 不是自动优化器：只记录建议、对比前后指标、给出最小验证结论
- 验证对象：结构树质量（tree metrics / issue 变化）

约束：
- 只读 optimization_hint / metrics / tree / optional baseline
- 不反写主逻辑，不做自动调参/应用
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _i(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


@dataclass
class OptimizationBaselineSnapshot:
    tree_depth: int = 0
    branch_count: int = 0
    dead_branch_count: int = 0
    resolution_path_length: int = 0
    effective_feedback_count: int = 0
    prune_rate: float = 0.0
    issue_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tree_depth": int(self.tree_depth),
            "branch_count": int(self.branch_count),
            "dead_branch_count": int(self.dead_branch_count),
            "resolution_path_length": int(self.resolution_path_length),
            "effective_feedback_count": int(self.effective_feedback_count),
            "prune_rate": float(self.prune_rate),
            "issue_type": self.issue_type,
        }


@dataclass
class OptimizationFeedbackLoopResult:
    optimization_hint_type: Optional[str] = None
    suggested_optimization_module: Optional[str] = None
    suggested_optimization_action: Optional[str] = None

    baseline_metrics_summary: Optional[str] = None
    current_metrics_summary: Optional[str] = None

    baseline_issue_type: Optional[str] = None
    current_issue_type: Optional[str] = None

    delta_tree_depth: int = 0
    delta_branch_count: int = 0
    delta_dead_branch_count: int = 0
    delta_resolution_path_length: int = 0
    delta_effective_feedback_count: int = 0
    delta_prune_rate: float = 0.0

    validation_result: str = "not_applicable"  # improved/unchanged/regressed/not_enough_data/not_applicable
    validation_reason: Optional[str] = None
    improvement_detected: bool = False
    regression_detected: bool = False

    suggested_next_step: Optional[str] = None  # keep_observing/validate_with_more_samples/prioritize_module_tuning/reject_current_hint/persist_to_library_candidate
    worth_persisting_to_library: bool = False

    optimization_feedback_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "optimization_hint_type": self.optimization_hint_type,
            "suggested_optimization_module": self.suggested_optimization_module,
            "suggested_optimization_action": self.suggested_optimization_action,
            "baseline_metrics_summary": self.baseline_metrics_summary,
            "current_metrics_summary": self.current_metrics_summary,
            "baseline_issue_type": self.baseline_issue_type,
            "current_issue_type": self.current_issue_type,
            "delta_tree_depth": int(self.delta_tree_depth),
            "delta_branch_count": int(self.delta_branch_count),
            "delta_dead_branch_count": int(self.delta_dead_branch_count),
            "delta_resolution_path_length": int(self.delta_resolution_path_length),
            "delta_effective_feedback_count": int(self.delta_effective_feedback_count),
            "delta_prune_rate": float(self.delta_prune_rate),
            "validation_result": self.validation_result,
            "validation_reason": self.validation_reason,
            "improvement_detected": bool(self.improvement_detected),
            "regression_detected": bool(self.regression_detected),
            "suggested_next_step": self.suggested_next_step,
            "worth_persisting_to_library": bool(self.worth_persisting_to_library),
            "optimization_feedback_applied": bool(self.optimization_feedback_applied),
        }


def _extract_baseline_from_hint(hint: Dict[str, Any]) -> Optional[OptimizationBaselineSnapshot]:
    """
    M0：baseline 输入允许很简单。当前先支持：
    - hint['baseline_metrics']（dict）
    - hint['baseline_metrics_summary']（仅摘要，不够做 delta）
    """
    b = hint.get("baseline_metrics")
    if not isinstance(b, dict):
        return None
    return OptimizationBaselineSnapshot(
        tree_depth=_i(b.get("tree_depth")),
        branch_count=_i(b.get("branch_count")),
        dead_branch_count=_i(b.get("dead_branch_count")),
        resolution_path_length=_i(b.get("resolution_path_length")),
        effective_feedback_count=_i(b.get("effective_feedback_count")),
        prune_rate=_f(b.get("prune_rate")),
        issue_type=_s(b.get("issue_type")),
    )


def build_optimization_feedback_loop(
    *,
    optimization_hint: Optional[Dict[str, Any]],
    reasoning_tree_metrics: Optional[Dict[str, Any]],
    reasoning_structure_tree: Optional[Dict[str, Any]] = None,  # reserved
    baseline: Optional[Dict[str, Any]] = None,
) -> OptimizationFeedbackLoopResult:
    hint = optimization_hint or {}
    metrics = reasoning_tree_metrics or {}

    hint_type = _s(hint.get("optimization_hint_type"))
    if not hint or not hint_type or hint_type == "none" or not bool(hint.get("optimization_hint_applied")):
        return OptimizationFeedbackLoopResult(
            optimization_hint_type=hint_type or "none",
            suggested_optimization_module=_s(hint.get("suggested_optimization_module")),
            suggested_optimization_action=_s(hint.get("suggested_optimization_action")),
            baseline_metrics_summary=None,
            current_metrics_summary=_s(metrics.get("metrics_summary")),
            baseline_issue_type=None,
            current_issue_type=_s(metrics.get("possible_tree_issue_type")),
            validation_result="not_applicable",
            validation_reason="当前无有效优化建议，跳过验证。",
            improvement_detected=False,
            regression_detected=False,
            suggested_next_step="keep_observing",
            worth_persisting_to_library=False,
            optimization_feedback_applied=True,
        )

    current_issue = _s(metrics.get("possible_tree_issue_type"))
    current_summary = _s(metrics.get("metrics_summary"))

    # baseline source priority: explicit baseline arg > hint.baseline_metrics > not enough data
    base_obj: Optional[OptimizationBaselineSnapshot] = None
    if isinstance(baseline, dict):
        base_obj = OptimizationBaselineSnapshot(
            tree_depth=_i(baseline.get("tree_depth")),
            branch_count=_i(baseline.get("branch_count")),
            dead_branch_count=_i(baseline.get("dead_branch_count")),
            resolution_path_length=_i(baseline.get("resolution_path_length")),
            effective_feedback_count=_i(baseline.get("effective_feedback_count")),
            prune_rate=_f(baseline.get("prune_rate")),
            issue_type=_s(baseline.get("issue_type")),
        )
    if base_obj is None:
        base_obj = _extract_baseline_from_hint(hint)

    if base_obj is None:
        return OptimizationFeedbackLoopResult(
            optimization_hint_type=hint_type,
            suggested_optimization_module=_s(hint.get("suggested_optimization_module")),
            suggested_optimization_action=_s(hint.get("suggested_optimization_action")),
            baseline_metrics_summary=_s(hint.get("baseline_metrics_summary")),
            current_metrics_summary=current_summary,
            baseline_issue_type=_s(hint.get("trigger_issue_type")) or _s(hint.get("baseline_issue_type")),
            current_issue_type=current_issue,
            validation_result="not_enough_data",
            validation_reason="缺少 baseline 指标，无法做前后对照；建议继续采样并提供 baseline。",
            improvement_detected=False,
            regression_detected=False,
            suggested_next_step="validate_with_more_samples",
            worth_persisting_to_library=False,
            optimization_feedback_applied=True,
        )

    # compute deltas (current - baseline)
    d_depth = _i(metrics.get("tree_depth")) - base_obj.tree_depth
    d_branch = _i(metrics.get("branch_count")) - base_obj.branch_count
    d_dead = _i(metrics.get("dead_branch_count")) - base_obj.dead_branch_count
    d_res = _i(metrics.get("resolution_path_length")) - base_obj.resolution_path_length
    d_eff = _i(metrics.get("effective_feedback_count")) - base_obj.effective_feedback_count
    d_pr = _f(metrics.get("prune_rate")) - base_obj.prune_rate

    # core comparison rules (M0)
    improved = False
    regressed = False

    # improvements
    if d_depth < 0 or d_dead < 0 or d_res < 0 or d_pr < 0:
        improved = True
    if d_eff > 0:
        improved = True
    if base_obj.issue_type and (base_obj.issue_type != current_issue) and (not current_issue):
        improved = True

    # regressions
    if d_depth > 0 or d_dead > 0 or d_res > 0 or d_pr > 0:
        regressed = True
    if d_eff < 0:
        regressed = True

    # issue severity heuristic (very minimal): blocked_without_resolution / feedback_not_effective are "more severe"
    severe = {"blocked_without_resolution", "feedback_not_effective"}
    if current_issue in severe and base_obj.issue_type not in severe:
        regressed = True

    # decide validation_result
    if improved and not regressed:
        v = "improved"
    elif regressed and not improved:
        v = "regressed"
    else:
        v = "unchanged"

    # next step rules
    if v == "improved":
        next_step = "persist_to_library_candidate" if (base_obj.issue_type and not current_issue) else "keep_observing"
    elif v == "regressed":
        next_step = "reject_current_hint" if current_issue in severe else "prioritize_module_tuning"
    else:
        next_step = "validate_with_more_samples"

    worth = bool(v == "improved" and (base_obj.issue_type and not current_issue) and not regressed)

    reason = (
        f"baseline(issue={base_obj.issue_type}, depth={base_obj.tree_depth}, dead={base_obj.dead_branch_count}, prune={base_obj.prune_rate:.2f}) → "
        f"current(issue={current_issue or 'none'}, depth={_i(metrics.get('tree_depth'))}, dead={_i(metrics.get('dead_branch_count'))}, prune={_f(metrics.get('prune_rate')):.2f}); "
        f"Δdepth={d_depth} Δdead={d_dead} Δprune={d_pr:.2f} Δeff_fb={d_eff}"
    )

    return OptimizationFeedbackLoopResult(
        optimization_hint_type=hint_type,
        suggested_optimization_module=_s(hint.get("suggested_optimization_module")),
        suggested_optimization_action=_s(hint.get("suggested_optimization_action")),
        baseline_metrics_summary=_s(hint.get("baseline_metrics_summary")) or f"depth={base_obj.tree_depth} branch={base_obj.branch_count} dead={base_obj.dead_branch_count} prune_rate={base_obj.prune_rate:.2f}",
        current_metrics_summary=current_summary,
        baseline_issue_type=base_obj.issue_type,
        current_issue_type=current_issue,
        delta_tree_depth=d_depth,
        delta_branch_count=d_branch,
        delta_dead_branch_count=d_dead,
        delta_resolution_path_length=d_res,
        delta_effective_feedback_count=d_eff,
        delta_prune_rate=round(d_pr, 3),
        validation_result=v,
        validation_reason=reason,
        improvement_detected=improved,
        regression_detected=regressed,
        suggested_next_step=next_step,
        worth_persisting_to_library=worth,
        optimization_feedback_applied=True,
    )

