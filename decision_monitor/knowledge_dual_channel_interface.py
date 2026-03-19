# -*- coding: utf-8 -*-
"""
Knowledge Dual-Channel Interface M0（知识双通道接口预留层）

定位（写死）：
- 这是接口预留层，不是图书馆系统
- 只定义：沉淀候选通道、优化/查策略候选通道、策略注入口（slot）
- 不做：知识写入/检索/策略召回/自动注入/评分系统/对比与替换逻辑/反馈机制细化/历史统计

约束：
- 只读输入（optimization_feedback_loop / optimization_hint / reasoning_tree_metrics / structure_tree）
- 不反写任何主逻辑
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _b(x: Any) -> bool:
    return bool(x is True)


@dataclass
class KnowledgePersistCandidate:
    persist_candidate_type: Optional[str] = None
    persist_candidate_reason: Optional[str] = None
    persist_payload_summary: Optional[str] = None
    persist_priority: Optional[str] = None  # high/medium/low (占位)
    worth_persisting: bool = False
    persist_candidate_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "persist_candidate_type": self.persist_candidate_type,
            "persist_candidate_reason": self.persist_candidate_reason,
            "persist_payload_summary": self.persist_payload_summary,
            "persist_priority": self.persist_priority,
            "worth_persisting": bool(self.worth_persisting),
            "persist_candidate_applied": bool(self.persist_candidate_applied),
        }


@dataclass
class KnowledgeOptimizationCandidate:
    optimization_candidate_type: Optional[str] = None
    optimization_candidate_reason: Optional[str] = None
    needs_external_strategy_support: bool = False
    suggested_library_lookup_type: Optional[str] = None
    lookup_triggered_if_library_enabled: bool = False
    optimization_candidate_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "optimization_candidate_type": self.optimization_candidate_type,
            "optimization_candidate_reason": self.optimization_candidate_reason,
            "needs_external_strategy_support": bool(self.needs_external_strategy_support),
            "suggested_library_lookup_type": self.suggested_library_lookup_type,
            "lookup_triggered_if_library_enabled": bool(self.lookup_triggered_if_library_enabled),
            "optimization_candidate_applied": bool(self.optimization_candidate_applied),
        }


@dataclass
class KnowledgeInjectionSlot:
    injection_target_module: Optional[str] = None
    injection_target_stage: Optional[str] = None
    injection_payload_type: Optional[str] = None
    injection_mode: Optional[str] = None  # strategy_hint/rule_patch/weight_patch/validation_template (占位)
    injection_slot_reason: Optional[str] = None
    injection_slot_reserved: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "injection_target_module": self.injection_target_module,
            "injection_target_stage": self.injection_target_stage,
            "injection_payload_type": self.injection_payload_type,
            "injection_mode": self.injection_mode,
            "injection_slot_reason": self.injection_slot_reason,
            "injection_slot_reserved": bool(self.injection_slot_reserved),
        }


@dataclass
class KnowledgeDualChannelInterfaceResult:
    persist_candidate: Optional[KnowledgePersistCandidate] = None
    optimization_candidate: Optional[KnowledgeOptimizationCandidate] = None
    injection_slot: Optional[KnowledgeInjectionSlot] = None
    interface_summary: Optional[str] = None
    interface_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "persist_candidate": self.persist_candidate.to_dict() if self.persist_candidate else None,
            "optimization_candidate": self.optimization_candidate.to_dict() if self.optimization_candidate else None,
            "injection_slot": self.injection_slot.to_dict() if self.injection_slot else None,
            "interface_summary": self.interface_summary,
            "interface_applied": bool(self.interface_applied),
        }


def build_knowledge_dual_channel_interface(
    *,
    optimization_feedback_loop: Optional[Dict[str, Any]],
    optimization_hint: Optional[Dict[str, Any]],
    reasoning_tree_metrics: Optional[Dict[str, Any]],
) -> KnowledgeDualChannelInterfaceResult:
    """
    M0 最小生成规则（写死、简单）：
    - Persist candidate：优先依据 worth_persisting_to_library
    - Optimization candidate：issue 持续/建议无效/数据不足 => needs_external_strategy_support
    - Injection slot：按 issue/hint 粗映射到目标模块
    """
    ofl = optimization_feedback_loop or {}
    oh = optimization_hint or {}
    m = reasoning_tree_metrics or {}

    worth = _b(ofl.get("worth_persisting_to_library"))
    validation = _s(ofl.get("validation_result")) or "not_enough_data"
    issue = _s(m.get("possible_tree_issue_type")) or _s(ofl.get("current_issue_type")) or _s(oh.get("trigger_issue_type"))
    hint_type = _s(oh.get("optimization_hint_type"))

    # A) persist candidate
    persist = KnowledgePersistCandidate(
        persist_candidate_type="optimization_hint_validation" if hint_type else "tree_quality_snapshot",
        persist_candidate_reason="验证显示该建议带来改善，值得作为沉淀候选（仅预留接口，不写库）。" if worth else "当前不满足沉淀条件（仅预留接口）。",
        persist_payload_summary=f"hint={hint_type or '—'} validation={validation} issue={issue or '—'}",
        persist_priority="high" if worth else "low",
        worth_persisting=bool(worth),
        persist_candidate_applied=True,
    )

    # B) optimization / lookup candidate
    needs_ext = False
    if issue and validation in ("unchanged", "regressed", "not_enough_data"):
        needs_ext = True
    lookup_type = None
    if issue:
        lookup_type = f"issue:{issue}"
    elif hint_type:
        lookup_type = f"hint:{hint_type}"

    opt = KnowledgeOptimizationCandidate(
        optimization_candidate_type=issue or hint_type or "none",
        optimization_candidate_reason=(
            f"issue={issue or '—'} validation={validation}；建议未来可查策略/模板辅助（仅预留，不做 lookup）。"
            if needs_ext
            else "当前不需要外部策略支持（仅预留接口）。"
        ),
        needs_external_strategy_support=bool(needs_ext),
        suggested_library_lookup_type=lookup_type,
        lookup_triggered_if_library_enabled=False,
        optimization_candidate_applied=True,
    )

    # C) injection slot (single slot reserved)
    target_module = "hypothesis_layer"
    stage = "pre_hypothesis_generation"
    mode = "strategy_hint"
    payload_type = "library_strategy_stub"
    slot_reason = "默认注入口（M0 占位）：后续图书馆策略统一从此注入，不在模块内散落实现。"

    if issue in ("too_many_branches", "high_dead_branch_ratio"):
        target_module = "hypothesis_layer"
        stage = "hypothesis_branching"
        mode = "rule_patch"
        payload_type = "branch_pruning_hint"
        slot_reason = "分支发散/死分支偏高：预留向 hypothesis_layer 注入分支剪枝策略。"
    elif issue in ("feedback_not_effective",):
        target_module = "optimization_hint"
        stage = "post_metrics_hint_generation"
        mode = "validation_template"
        payload_type = "feedback_mapping_template"
        slot_reason = "反馈不生效：预留注入验证模板/映射策略（不执行）。"
    elif issue in ("blocked_without_resolution",):
        target_module = "recheck_planner"
        stage = "blocked_recovery"
        mode = "strategy_hint"
        payload_type = "fallback_recovery_hint"
        slot_reason = "阻断未收口：预留注入 fallback/恢复策略提示（不执行）。"

    inj = KnowledgeInjectionSlot(
        injection_target_module=target_module,
        injection_target_stage=stage,
        injection_payload_type=payload_type,
        injection_mode=mode,
        injection_slot_reason=slot_reason,
        injection_slot_reserved=True,
    )

    summary = f"persist={persist.worth_persisting} opt_needs_ext={opt.needs_external_strategy_support} inj={inj.injection_target_module}/{inj.injection_mode}"
    return KnowledgeDualChannelInterfaceResult(
        persist_candidate=persist,
        optimization_candidate=opt,
        injection_slot=inj,
        interface_summary=summary,
        interface_applied=True,
    )

