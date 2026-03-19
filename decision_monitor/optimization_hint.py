# -*- coding: utf-8 -*-
"""
Optimization Hint / Tree Improvement Suggestion M0（决策树优化建议层）

定位：
- 不是自动优化器：只输出“哪里效率低、为什么、最该先改哪个模块、建议怎么改”
- 从诊断走向优化的第一步：基于结构树 + 指标 + issue + 白盒摘要做规则版建议
- 建议必须可审计：必须包含触发问题、支撑指标摘要、树摘要与排除备选模块理由

约束：
- 只读输入（tree / metrics / whiteboxes）
- 不反写任何主逻辑
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


@dataclass
class OptimizationHintResult:
    optimization_hint_type: Optional[str] = None
    optimization_hint_reason: Optional[str] = None
    suggested_optimization_module: Optional[str] = None
    suggested_optimization_action: Optional[str] = None
    priority_level: Optional[str] = None  # high / medium / low
    trigger_issue_type: Optional[str] = None
    trigger_issue_reason: Optional[str] = None
    supporting_metrics_summary: Optional[str] = None
    supporting_tree_summary: Optional[str] = None
    suggested_followup_measure: Optional[str] = None
    suggested_validation_path: Optional[str] = None
    excluded_alternative_modules: List[str] = field(default_factory=list)
    optimization_hint_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "optimization_hint_type": self.optimization_hint_type,
            "optimization_hint_reason": self.optimization_hint_reason,
            "suggested_optimization_module": self.suggested_optimization_module,
            "suggested_optimization_action": self.suggested_optimization_action,
            "priority_level": self.priority_level,
            "trigger_issue_type": self.trigger_issue_type,
            "trigger_issue_reason": self.trigger_issue_reason,
            "supporting_metrics_summary": self.supporting_metrics_summary,
            "supporting_tree_summary": self.supporting_tree_summary,
            "suggested_followup_measure": self.suggested_followup_measure,
            "suggested_validation_path": self.suggested_validation_path,
            "excluded_alternative_modules": list(self.excluded_alternative_modules),
            "optimization_hint_applied": bool(self.optimization_hint_applied),
        }


def _priority_from_context(issue_type: Optional[str], metrics: Dict[str, Any]) -> str:
    prune_rate = _f(metrics.get("prune_rate"), 0.0)
    depth = int(metrics.get("tree_depth") or 0)
    eff_fb = int(metrics.get("effective_feedback_count") or 0)
    fb_n = int(metrics.get("feedback_node_count") or 0)

    if issue_type in ("feedback_not_effective", "blocked_without_resolution"):
        return "high"
    if issue_type == "high_dead_branch_ratio":
        return "high" if prune_rate > 0.75 else "medium"
    if issue_type in ("tree_too_deep", "long_resolution_path"):
        return "medium" if depth > 6 else "low"
    if issue_type == "too_many_branches":
        return "medium"
    # no issue: if feedback exists but weak effect, still medium
    if fb_n > 0 and eff_fb == 0:
        return "medium"
    return "low"


def build_optimization_hint(
    *,
    reasoning_tree_metrics: Optional[Dict[str, Any]],
    reasoning_structure_tree: Optional[Dict[str, Any]],
    whiteboxes: Optional[Dict[str, Any]] = None,
) -> OptimizationHintResult:
    """
    规则版建议生成：
    1) 优先基于 metrics.possible_tree_issue_type
    2) 结合 prune/depth/feedback/resolved/blocked 细化模块与动作
    3) 输出排除备选模块（为什么不是别的模块）
    """
    metrics = reasoning_tree_metrics or {}
    tree = reasoning_structure_tree or {}
    issue_type = _s(metrics.get("possible_tree_issue_type"))
    issue_reason = _s(metrics.get("possible_tree_issue_reason"))
    metrics_summary = _s(metrics.get("metrics_summary"))
    tree_summary = _s(tree.get("tree_summary"))

    if not issue_type:
        # no obvious issue: still return a stable none result
        return OptimizationHintResult(
            optimization_hint_type="none",
            optimization_hint_reason="暂无明显优化建议（未命中结构树 issue 规则）。",
            suggested_optimization_module=None,
            suggested_optimization_action=None,
            priority_level="low",
            trigger_issue_type=None,
            trigger_issue_reason=None,
            supporting_metrics_summary=metrics_summary,
            supporting_tree_summary=tree_summary,
            excluded_alternative_modules=[],
            optimization_hint_applied=False,
        )

    pr = _priority_from_context(issue_type, metrics)
    prune_rate = _f(metrics.get("prune_rate"), 0.0)
    dead = int(metrics.get("dead_branch_count") or 0)
    branch = int(metrics.get("branch_count") or 0)
    depth = int(metrics.get("tree_depth") or 0)
    resolved = bool(metrics.get("resolved") is True)
    blocked = bool(metrics.get("blocked") is True)
    fb_n = int(metrics.get("feedback_node_count") or 0)
    eff_fb = int(metrics.get("effective_feedback_count") or 0)

    # rule mapping table (M0)
    hint_type = None
    module = None
    action = None
    excluded: List[str] = []
    reason = None
    followup = None
    validate = None

    if issue_type == "high_dead_branch_ratio":
        hint_type = "reduce_dead_branches"
        module = "hypothesis_layer"
        action = "tighten weak-hypothesis entry threshold (reduce low-confidence alternatives)"
        excluded = ["grid_search_expansion", "action_hint_copy"]
        reason = (
            f"当前分支={branch}，死分支={dead}，prune_rate={prune_rate:.2f}；"
            "浪费主要发生在假设/备选分支扩张，建议先收紧 hypothesis 入口与弱分支创建。"
        )
        followup = "track prune_rate and dead_branch_count after threshold tightening"
        validate = "use smoke_reasoning_tree_metrics on same context; expect prune_rate下降"

    elif issue_type == "too_many_branches":
        hint_type = "reduce_over_branching"
        module = "hypothesis_layer"
        action = "reduce low-confidence alternative branch creation; cap hypothesis types per frame"
        excluded = ["grid_search_expansion"]
        reason = f"branch_count={branch} 偏高，说明候选/分支发散；优先在 hypothesis_layer 做分支约束。"
        followup = "compare branch_count before/after; keep recall stable"
        validate = "unit test: branch_count decreases while active_path_length stable"

    elif issue_type in ("tree_too_deep", "long_resolution_path"):
        hint_type = "shorten_resolution_path"
        module = "action_hint_copy"
        action = "prefer earlier direct confirmation under strong evidence; reduce redundant followups"
        excluded = ["recheck_planner", "grid_search_expansion"]
        reason = (
            f"tree_depth={depth} 且收敛链偏长；优先让 action_hint_copy 在强证据时更早进入确认/收口，减少绕远。"
        )
        followup = "track tree_depth and resolution_path_length on resolved frames"
        validate = "smoke with resolved terminal; expect resolution_path_length下降"

    elif issue_type == "feedback_not_effective":
        hint_type = "improve_feedback_convergence"
        module = "confirmation_input_bridge"
        action = "raise feedback-driven path switching priority; ensure next_effect advances when feedback is clear"
        excluded = ["action_hint_copy", "hypothesis_layer"]
        reason = (
            f"feedback_node_count={fb_n} 但 effective_feedback_count={eff_fb}；"
            "说明用户反馈未真正推动推进/收敛，优先检查 confirmation_input_bridge 的映射与 next_effect。"
        )
        followup = "track effective_feedback_count and next_effect distribution"
        validate = "smoke with clear feedback; expect next_effect != none and effective_feedback_count>0"

    elif issue_type == "blocked_without_resolution":
        hint_type = "resolve_blocked_state"
        module = "recheck_planner"
        action = "add fallback for blocked recheck path (human_check or alternative recheck) and ensure terminal/resolution update"
        excluded = ["task_arbitration", "confirmation_input_bridge"]
        reason = (
            f"blocked={blocked} 且 resolved={resolved}；"
            "系统处于阻断但未收口，优先在 recheck_planner/阻断恢复路径上给出明确 fallback 与收口策略。"
        )
        followup = "track blocked_without_resolution occurrences"
        validate = "unit test: blocked frames yield explicit resolution or next_effect"

    else:
        # default fallback mapping
        hint_type = "reduce_dead_branches"
        module = "hypothesis_layer"
        action = "tighten weak-branch entry threshold"
        excluded = ["grid_search_expansion"]
        reason = f"命中 issue={issue_type}；优先从分支收敛角度减少无效扩张（规则版默认建议）。"

    # strengthen governance stability hint when governance appears problematic (M0 light)
    # only as low-priority secondary when no direct mapping above
    if issue_type not in ("blocked_without_resolution", "feedback_not_effective") and whiteboxes:
        eg = whiteboxes.get("experience_governance_whitebox_trace") if isinstance(whiteboxes, dict) else None
        if isinstance(eg, dict) and _s(eg.get("whitebox_summary")) and ("rejected" in str(eg.get("whitebox_summary")) or "blocked" in str(eg.get("whitebox_summary"))):
            # keep as excluded alternative for now
            if "experience_evolution" not in excluded:
                excluded.append("experience_evolution")

    return OptimizationHintResult(
        optimization_hint_type=hint_type,
        optimization_hint_reason=f"{reason}（trigger={issue_type}: {issue_reason or '—'}）",
        suggested_optimization_module=module,
        suggested_optimization_action=action,
        priority_level=pr,
        trigger_issue_type=issue_type,
        trigger_issue_reason=issue_reason,
        supporting_metrics_summary=metrics_summary,
        supporting_tree_summary=tree_summary,
        suggested_followup_measure=followup,
        suggested_validation_path=validate,
        excluded_alternative_modules=excluded,
        optimization_hint_applied=True,
    )

