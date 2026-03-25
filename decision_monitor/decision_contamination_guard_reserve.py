# -*- coding: utf-8 -*-
"""
Decision Contamination Guard Reserve M0（污染抵抗 / 决策污染观察占位层）

定位（写死）：
- 为未来「污染判断 / 溯源 / 成因 / 扩散 / 抵抗 / 消化 / 多模型议会式复核」预留结构与观察位
- 当前**不**输出强结论（不判定「已被污染」）；只输出潜在入口、潜在传播链、潜在阻断位点（reserve）

约束：
- 不反写主逻辑；不实现污染识别算法、评分、溯源图谱、清洗策略
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

ENTRY_POINT_TYPES = (
    "user_input",
    "environment_observation",
    "memory_recall",
    "novel_information",
    "strategy_injection",
    "task_context",
    "unknown",
)
RISK_LEVELS = ("low", "medium", "high", "unknown")

FLOW_STAGES = (
    "input",
    "hypothesis",
    "recheck",
    "task_stage",
    "memory_candidate",
    "action_output",
    "unknown",
)

MITIGATION_TYPES = (
    "axiom_guard",
    "fact_cross_check",
    "confidence_decay",
    "shadow_validation",
    "watchlist_only",
    "multi_model_review",
    "vote_council_reserved",
    "unknown",
)


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


@dataclass
class ContaminationEntryPointReserve:
    entry_point_type: str = "unknown"
    entry_point_summary: Optional[str] = None
    entry_point_risk_level: str = "unknown"
    entry_point_observed: bool = False
    entry_point_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_point_type": self.entry_point_type,
            "entry_point_summary": self.entry_point_summary,
            "entry_point_risk_level": self.entry_point_risk_level,
            "entry_point_observed": bool(self.entry_point_observed),
            "entry_point_note": self.entry_point_note,
        }


@dataclass
class ContaminationFlowReserve:
    flow_stage: str = "unknown"
    flow_summary: Optional[str] = None
    flow_spread_possible: bool = False
    flow_block_point_possible: bool = False
    flow_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "flow_stage": self.flow_stage,
            "flow_summary": self.flow_summary,
            "flow_spread_possible": bool(self.flow_spread_possible),
            "flow_block_point_possible": bool(self.flow_block_point_possible),
            "flow_note": self.flow_note,
        }


@dataclass
class ContaminationMitigationReserve:
    mitigation_type: str = "unknown"
    mitigation_summary: Optional[str] = None
    mitigation_ready: bool = False
    mitigation_reserved_only: bool = True
    mitigation_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mitigation_type": self.mitigation_type,
            "mitigation_summary": self.mitigation_summary,
            "mitigation_ready": bool(self.mitigation_ready),
            "mitigation_reserved_only": bool(self.mitigation_reserved_only),
            "mitigation_note": self.mitigation_note,
        }


@dataclass
class DecisionContaminationGuardReserveResult:
    potential_entry_points: List[ContaminationEntryPointReserve] = field(default_factory=list)
    potential_flow_chain: List[ContaminationFlowReserve] = field(default_factory=list)
    potential_mitigation_points: List[ContaminationMitigationReserve] = field(default_factory=list)
    contamination_observation_summary: Optional[str] = None
    multi_model_review_reserved: bool = True
    vote_council_reserved: bool = True
    contamination_guard_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "potential_entry_points": [e.to_dict() for e in self.potential_entry_points],
            "potential_flow_chain": [f.to_dict() for f in self.potential_flow_chain],
            "potential_mitigation_points": [m.to_dict() for m in self.potential_mitigation_points],
            "contamination_observation_summary": self.contamination_observation_summary,
            "multi_model_review_reserved": bool(self.multi_model_review_reserved),
            "vote_council_reserved": bool(self.vote_council_reserved),
            "contamination_guard_applied": bool(self.contamination_guard_applied),
        }


def build_decision_contamination_guard_reserve(frame: Dict[str, Any]) -> DecisionContaminationGuardReserveResult:
    """
    M0 最小占位：从现有 frame 轻量推断潜在入口/链/位点；不做污染判定。
    """
    if not isinstance(frame, dict):
        return DecisionContaminationGuardReserveResult()

    entries: List[ContaminationEntryPointReserve] = []
    flows: List[ContaminationFlowReserve] = []
    mitigations: List[ContaminationMitigationReserve] = []

    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else None
    raw = _s(_get(cib, "confirmation_input_raw_text")) if cib else None
    cit = (_s(_get(cib, "confirmation_input_type")) or "").strip().lower() if cib else ""
    if cib and (raw or cit):
        risk = "medium" if cit and cit != "unknown" else "low"
        entries.append(
            ContaminationEntryPointReserve(
                entry_point_type="user_input",
                entry_point_summary=(raw or f"confirmation_type={cit}")[:200],
                entry_point_risk_level=risk,
                entry_point_observed=True,
                entry_point_note="reserve: user-facing feedback channel",
            )
        )

    mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
    if mn:
        dom = _s(mn.get("dominant_reasoning_channel"))
        if dom == "memory_derived":
            entries.append(
                ContaminationEntryPointReserve(
                    entry_point_type="memory_recall",
                    entry_point_summary="memory_derived channel active",
                    entry_point_risk_level="low",
                    entry_point_observed=True,
                    entry_point_note="reserve: memory vs novel channel",
                )
            )
        if int(mn.get("novel_channel_count") or 0) > 0 or dom in ("newly_observed", "inferred_from_exclusion"):
            entries.append(
                ContaminationEntryPointReserve(
                    entry_point_type="novel_information",
                    entry_point_summary=dom or "novel/inferred signal present",
                    entry_point_risk_level="medium",
                    entry_point_observed=True,
                    entry_point_note="reserve: novel or exclusion-inferred path",
                )
            )

    kdc = frame.get("knowledge_dual_channel_interface") if isinstance(frame.get("knowledge_dual_channel_interface"), dict) else None
    shadow = frame.get("strategy_injection_shadow") if isinstance(frame.get("strategy_injection_shadow"), dict) else None
    if kdc or shadow:
        entries.append(
            ContaminationEntryPointReserve(
                entry_point_type="strategy_injection",
                entry_point_summary="knowledge slot / strategy shadow present (no execution)",
                entry_point_risk_level="medium",
                entry_point_observed=True,
                entry_point_note="reserve: external strategy or library path",
            )
        )

    etc = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
    if etc:
        ec = etc.get("environment_context") if isinstance(etc.get("environment_context"), dict) else {}
        tc = etc.get("task_chain_context") if isinstance(etc.get("task_chain_context"), dict) else {}
        env_snip = _s(ec.get("environment_context_summary")) or _s(ec.get("environment_scene_type"))
        task_snip = _s(tc.get("task_chain_context_summary")) or _s(tc.get("task_chain_stage"))
        if env_snip or task_snip:
            entries.append(
                ContaminationEntryPointReserve(
                    entry_point_type="environment_observation",
                    entry_point_summary=(env_snip or "env")[:120],
                    entry_point_risk_level="low",
                    entry_point_observed=True,
                    entry_point_note="reserve: environment premise",
                )
            )
            entries.append(
                ContaminationEntryPointReserve(
                    entry_point_type="task_context",
                    entry_point_summary=(task_snip or "task_chain")[:120],
                    entry_point_risk_level="low",
                    entry_point_observed=True,
                    entry_point_note="reserve: task chain stage",
                )
            )

    # 粗粒度「链」占位（非真实图谱）
    if entries:
        flows.append(
            ContaminationFlowReserve(
                flow_stage="input",
                flow_summary="inputs → confirmation/memory/env hooks (reserve chain stub)",
                flow_spread_possible=True,
                flow_block_point_possible=True,
                flow_note="M0: not a real diffusion graph",
            )
        )
    hyp = frame.get("hypothesis_layer") if isinstance(frame.get("hypothesis_layer"), dict) else None
    if hyp and (hyp.get("hypotheses") or []):
        flows.append(
            ContaminationFlowReserve(
                flow_stage="hypothesis",
                flow_summary="hypothesis candidates present",
                flow_spread_possible=True,
                flow_block_point_possible=True,
                flow_note="reserve: hypothesis as spread stage",
            )
        )
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else None
    if rp:
        flows.append(
            ContaminationFlowReserve(
                flow_stage="recheck",
                flow_summary=_s(rp.get("recheck_reason")) or "recheck planner active",
                flow_spread_possible=True,
                flow_block_point_possible=bool(rp.get("recheck_blocked")),
                flow_note="reserve: recheck as potential block point",
            )
        )
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else None
    if osi:
        flows.append(
            ContaminationFlowReserve(
                flow_stage="task_stage",
                flow_summary=_s(osi.get("search_subtask_state")) or "object search interaction",
                flow_spread_possible=True,
                flow_block_point_possible=False,
                flow_note="reserve: task-stage surface",
            )
        )

    mitigations.append(
        ContaminationMitigationReserve(
            mitigation_type="shadow_validation",
            mitigation_summary="strategy_injection_shadow validates before real inject (reserved)",
            mitigation_ready=False,
            mitigation_reserved_only=True,
            mitigation_note="M0 placeholder",
        )
    )
    mitigations.append(
        ContaminationMitigationReserve(
            mitigation_type="watchlist_only",
            mitigation_summary="experience governance may hold promotable to watchlist (reserved)",
            mitigation_ready=False,
            mitigation_reserved_only=True,
            mitigation_note="M0 placeholder",
        )
    )
    mitigations.append(
        ContaminationMitigationReserve(
            mitigation_type="multi_model_review",
            mitigation_summary="multi-model / council review not implemented; slot reserved",
            mitigation_ready=False,
            mitigation_reserved_only=True,
            mitigation_note="future governance",
        )
    )
    mitigations.append(
        ContaminationMitigationReserve(
            mitigation_type="vote_council_reserved",
            mitigation_summary="vote or council quorum not implemented; slot reserved",
            mitigation_ready=False,
            mitigation_reserved_only=True,
            mitigation_note="future governance",
        )
    )
    exp = frame.get("experience_evolution") if isinstance(frame.get("experience_evolution"), dict) else None
    if exp:
        mitigations.append(
            ContaminationMitigationReserve(
                mitigation_type="confidence_decay",
                mitigation_summary="experience evolution audits promotion (reserved)",
                mitigation_ready=False,
                mitigation_reserved_only=True,
                mitigation_note="reserve: slow confidence / watchlist",
            )
        )

    parts = []
    if entries:
        parts.append(f"entry_points={len(entries)}")
    if flows:
        parts.append(f"flow_stages={len(flows)}")
    if mitigations:
        parts.append(f"mitigation_slots={len(mitigations)}")
    summary = "；".join(parts) if parts else "contamination_guard_reserve: no signals (minimal frame)"
    if not summary.strip():
        summary = "contamination_guard_reserve: observation placeholder only"

    return DecisionContaminationGuardReserveResult(
        potential_entry_points=entries,
        potential_flow_chain=flows,
        potential_mitigation_points=mitigations,
        contamination_observation_summary=summary,
        multi_model_review_reserved=True,
        vote_council_reserved=True,
        contamination_guard_applied=True,
    )
