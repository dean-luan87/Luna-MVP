# -*- coding: utf-8 -*-
"""
Reasoning Tree Quality Overlay M0（推理树质量叠加层）

定位（写死）：
- 评分不是独立系统，而是结构树上的质量叠加层
- 树表达“怎么想的”，质量层表达“想得好不好”
- 扣分/加分来源回挂到树和分支上
- 不做复杂总分系统/历史趋势/图书馆对照/多维权重学习
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


QUALITY_FLAGS = (
    "healthy",
    "costly",
    "weak_support",
    "pruned",
    "feedback_effective",
    "feedback_ineffective",
    "blocked",
)


@dataclass
class ReasoningTreeQualityOverlayResult:
    structure_score: float = 0.0  # 0–100
    convergence_score: float = 0.0  # 0–100
    quality_grade: str = "acceptable"  # good / acceptable / poor

    quality_summary: Optional[str] = None
    score_reason_summary: Optional[str] = None
    score_penalty_sources: List[str] = field(default_factory=list)
    score_bonus_sources: List[str] = field(default_factory=list)

    active_path_quality: Optional[str] = None
    active_path_cost: Optional[str] = None

    node_quality_annotations: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # node_id -> {quality_flag, quality_note}
    quality_overlay_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "structure_score": float(self.structure_score),
            "convergence_score": float(self.convergence_score),
            "quality_grade": self.quality_grade,
            "quality_summary": self.quality_summary,
            "score_reason_summary": self.score_reason_summary,
            "score_penalty_sources": list(self.score_penalty_sources),
            "score_bonus_sources": list(self.score_bonus_sources),
            "active_path_quality": self.active_path_quality,
            "active_path_cost": self.active_path_cost,
            "node_quality_annotations": dict(self.node_quality_annotations),
            "quality_overlay_applied": bool(self.quality_overlay_applied),
        }


def _structure_score(metrics: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
    """规则版结构分 0–100；返回 (score, penalties, bonuses)。"""
    depth = _as_int(metrics.get("tree_depth"), 0)
    branch = _as_int(metrics.get("branch_count"), 0)
    dead = _as_int(metrics.get("dead_branch_count"), 0)
    prune_rate = _as_float(metrics.get("prune_rate"), 0.0)
    res_path = _as_int(metrics.get("resolution_path_length"), 0)
    active_len = _as_int(metrics.get("active_path_length"), 0)

    penalties: List[str] = []
    bonuses: List[str] = []

    score = 80.0
    if depth > 6:
        score -= 20
        penalties.append("tree_too_deep")
    elif depth > 4:
        score -= 10
        penalties.append("moderate_tree_depth")
    if depth <= 3 and active_len <= 4:
        bonuses.append("short_active_path")

    if dead > 2 or (branch > 0 and dead / max(1, branch) >= 0.6):
        score -= 15
        penalties.append("high_dead_branch_ratio")
    if prune_rate > 0.7:
        score -= 10
        penalties.append("high_prune_rate")
    elif prune_rate <= 0.3 and branch > 0:
        bonuses.append("low_prune_rate")

    if res_path > 5:
        score -= 10
        penalties.append("long_unresolved_path")
    elif res_path > 0 and depth <= 4:
        bonuses.append("resolution_path_present")

    score = max(0.0, min(100.0, score))
    return score, penalties, bonuses


def _convergence_score(
    metrics: Dict[str, Any],
    feedback_loop: Optional[Dict[str, Any]],
) -> Tuple[float, List[str], List[str]]:
    """规则版收敛分 0–100。"""
    resolved = bool(metrics.get("resolved") is True)
    blocked = bool(metrics.get("blocked") is True)
    eff_fb = _as_int(metrics.get("effective_feedback_count"), 0)
    issue_type = _s(metrics.get("possible_tree_issue_type"))
    feedback_node_count = _as_int(metrics.get("feedback_node_count"), 0)

    penalties: List[str] = []
    bonuses: List[str] = []

    score = 70.0
    if resolved:
        score += 15
        bonuses.append("resolved")
    if blocked:
        score -= 25
        penalties.append("blocked_state")
    if eff_fb >= 2:
        score += 10
        bonuses.append("effective_feedback_on_active_path")
    elif feedback_node_count > 0 and eff_fb == 0:
        score -= 15
        penalties.append("feedback_ineffective")

    if issue_type in ("feedback_not_effective", "blocked_without_resolution"):
        score -= 10
        penalties.append(f"issue_{issue_type}")
    if issue_type is None or issue_type == "":
        bonuses.append("no_tree_issue")

    val = (feedback_loop or {}).get("validation_result")
    if _s(val) == "improved":
        score += 5
        bonuses.append("optimization_validation_improved")
    elif _s(val) == "regressed":
        score -= 10
        penalties.append("optimization_validation_regressed")

    score = max(0.0, min(100.0, score))
    return score, penalties, bonuses


def _quality_grade(
    structure_score: float,
    convergence_score: float,
    penalties: List[str],
    metrics: Dict[str, Any],
) -> str:
    blocked = bool(metrics.get("blocked") is True)
    resolved = bool(metrics.get("resolved") is True)
    depth = _as_int(metrics.get("tree_depth"), 0)
    dead = _as_int(metrics.get("dead_branch_count"), 0)

    if blocked or (depth >= 6 and dead >= 2):
        return "poor"
    if structure_score >= 70 and convergence_score >= 70 and not penalties:
        return "good"
    if structure_score >= 50 and convergence_score >= 50:
        return "acceptable"
    if structure_score < 40 or convergence_score < 40:
        return "poor"
    return "acceptable"


def _node_annotations(
    tree: Dict[str, Any],
    metrics: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """按节点打轻量 quality_flag。"""
    nodes = tree.get("nodes") or []
    active_ids = set(str(x) for x in (tree.get("active_path_node_ids") or []) if x is not None)
    pruned_ids = set(str(x) for x in (tree.get("pruned_node_ids") or []) if x is not None)
    resolved_id = _s(tree.get("resolved_node_id"))

    out: Dict[str, Dict[str, Any]] = {}
    for n in nodes:
        if not isinstance(n, dict) or not n.get("node_id"):
            continue
        nid = str(n["node_id"])
        st = (n.get("status") or "").strip().lower()
        is_feedback = bool(n.get("is_user_feedback_driven"))

        flag = "healthy"
        note = ""

        if st == "blocked":
            flag = "blocked"
            note = "node blocked"
        elif nid in pruned_ids or st in ("pruned", "rejected"):
            flag = "pruned"
            note = n.get("exclusion_reason") or "pruned"
        elif is_feedback:
            eff_fb = _as_int(metrics.get("effective_feedback_count"), 0)
            flag = "feedback_effective" if eff_fb > 0 else "feedback_ineffective"
            note = "user feedback driven"
        elif nid in active_ids:
            depth = _as_int(metrics.get("tree_depth"), 0)
            if depth > 5:
                flag = "costly"
                note = "long path"
            else:
                flag = "healthy"
                note = "on active path"
        elif st == "resolved" or nid == resolved_id:
            flag = "healthy"
            note = "resolved"
        else:
            conf = n.get("confidence_score")
            if conf is not None and isinstance(conf, (int, float)) and float(conf) < 0.4:
                flag = "weak_support"
                note = "low confidence"
            else:
                flag = "healthy"
                note = ""

        out[nid] = {"quality_flag": flag, "quality_note": note or None}
    return out


def build_reasoning_tree_quality_overlay(
    tree: Dict[str, Any],
    metrics: Dict[str, Any],
    optimization_feedback_loop: Optional[Dict[str, Any]] = None,
) -> ReasoningTreeQualityOverlayResult:
    """
    M0 最小质量叠加：只读 tree + metrics（+ 可选 feedback_loop），
    输出树级评分、解释、节点级 quality 标记。
    """
    if not tree or not isinstance(tree, dict):
        return ReasoningTreeQualityOverlayResult(
            quality_summary="无结构树，跳过质量叠加。",
            quality_overlay_applied=False,
        )
    metrics = metrics or {}
    if not isinstance(metrics, dict):
        metrics = {}

    struct_score, struct_pen, struct_bonus = _structure_score(metrics)
    conv_score, conv_pen, conv_bonus = _convergence_score(metrics, optimization_feedback_loop)

    all_penalties = list(dict.fromkeys(struct_pen + conv_pen))
    all_bonuses = list(dict.fromkeys(struct_bonus + conv_bonus))

    grade = _quality_grade(struct_score, conv_score, all_penalties, metrics)
    node_ann = _node_annotations(tree, metrics)

    # 一句话总结
    if grade == "good":
        quality_summary = "树结构良好，收敛顺畅，无明显问题。"
    elif grade == "poor":
        quality_summary = "树较深或阻断明显，质量较差，建议关注死分支与收敛。"
    else:
        quality_summary = "树结构中等，存在可改进点，但整体可接受。"
    if all_penalties:
        quality_summary += " 主要扣分：" + "；".join(all_penalties[:3])
    if all_bonuses:
        quality_summary += " 加分项：" + "；".join(all_bonuses[:3])

    reason_parts = []
    if struct_pen or struct_bonus:
        reason_parts.append(f"structure: {struct_score:.0f} (penalties: {struct_pen}, bonuses: {struct_bonus})")
    if conv_pen or conv_bonus:
        reason_parts.append(f"convergence: {conv_score:.0f} (penalties: {conv_pen}, bonuses: {conv_bonus})")
    score_reason_summary = "; ".join(reason_parts) if reason_parts else f"structure={struct_score:.0f} convergence={conv_score:.0f}"

    active_path_len = _as_int(metrics.get("active_path_length"), 0)
    active_path_quality = "short and clear" if active_path_len <= 4 else ("moderate" if active_path_len <= 6 else "long")
    active_path_cost = "low" if active_path_len <= 4 else ("medium" if active_path_len <= 6 else "high")

    return ReasoningTreeQualityOverlayResult(
        structure_score=struct_score,
        convergence_score=conv_score,
        quality_grade=grade,
        quality_summary=quality_summary,
        score_reason_summary=score_reason_summary,
        score_penalty_sources=all_penalties,
        score_bonus_sources=all_bonuses,
        active_path_quality=active_path_quality,
        active_path_cost=active_path_cost,
        node_quality_annotations=node_ann,
        quality_overlay_applied=True,
    )
