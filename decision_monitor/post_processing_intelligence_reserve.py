# -*- coding: utf-8 -*-
"""
Post-Processing Intelligence Reserve M0（后置信息处理板块占位层）

定位（写死）：
- 独立板块：位于运行主线之后、图书馆 / 记忆系统之前；**不是**记忆系统的一部分。
- 当前只做 reserve / placeholder：可归类、可分析、可筛选、可去向占位；**不**输出强结论、**不**写入图书馆或记忆。

约束：
- 不实现真实归类/归因/策略效果分析/记忆筛选/去噪压缩/自动知识提炼。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

RECORD_SOURCE_TYPES = (
    "reasoning_trace",
    "whitebox_summary",
    "optimization_feedback",
    "scenario_benchmark",
    "real_case_result",
    "user_feedback",
    "strategy_shadow",
    "unknown",
)

ANALYSIS_TYPES = (
    "classification",
    "root_cause_analysis",
    "pattern_extraction",
    "failure_mode_analysis",
    "strategy_effectiveness_analysis",
    "contamination_observation",
    "unknown",
)

ROUTING_TARGETS = (
    "library_candidate_pool",
    "memory_candidate_pool",
    "risk_observation_pool",
    "contamination_observation_pool",
    "discard_candidate",
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


def _any_whitebox_summary(frame: Dict[str, Any]) -> bool:
    for key in (
        "grid_search_whitebox_trace",
        "recheck_whitebox_trace",
        "action_hint_whitebox_trace",
        "confirmation_whitebox_trace",
        "evidence_hypothesis_whitebox_trace",
        "experience_governance_whitebox_trace",
    ):
        w = frame.get(key) if isinstance(frame.get(key), dict) else None
        if w and _s(w.get("whitebox_summary")):
            return True
    return False


def _trace_benchmark_hint(tid: Optional[str]) -> bool:
    if not tid:
        return False
    tl = tid.lower()
    return "benchmark" in tl or "bench" in tl or "scenario_pack" in tl or "triage" in tl


def _trace_real_case_hint(tid: Optional[str]) -> bool:
    if not tid:
        return False
    tl = tid.lower()
    if "real_case" in tl or "real_scenario" in tl:
        return True
    return bool(re.match(r"^r\d+[_-]", tl, re.I))


@dataclass
class PostProcessRecordCandidate:
    record_source_type: str = "unknown"
    record_summary: Optional[str] = None
    record_category_hint: Optional[str] = None
    record_quality_hint: Optional[str] = None
    record_candidate_ready: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_source_type": self.record_source_type,
            "record_summary": self.record_summary,
            "record_category_hint": self.record_category_hint,
            "record_quality_hint": self.record_quality_hint,
            "record_candidate_ready": bool(self.record_candidate_ready),
        }


@dataclass
class PostProcessAnalysisReserve:
    analysis_type: str = "unknown"
    analysis_summary: Optional[str] = None
    analysis_reserved_only: bool = True
    analysis_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analysis_type": self.analysis_type,
            "analysis_summary": self.analysis_summary,
            "analysis_reserved_only": bool(self.analysis_reserved_only),
            "analysis_note": self.analysis_note,
        }


@dataclass
class PostProcessRoutingReserve:
    routing_target: str = "unknown"
    routing_reason_summary: Optional[str] = None
    routing_requires_filtering: bool = True
    routing_reserved_only: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "routing_target": self.routing_target,
            "routing_reason_summary": self.routing_reason_summary,
            "routing_requires_filtering": bool(self.routing_requires_filtering),
            "routing_reserved_only": bool(self.routing_reserved_only),
        }


@dataclass
class PostProcessingIntelligenceReserveResult:
    record_candidates: List[PostProcessRecordCandidate] = field(default_factory=list)
    analysis_reserve: List[PostProcessAnalysisReserve] = field(default_factory=list)
    routing_reserve: List[PostProcessRoutingReserve] = field(default_factory=list)
    post_processing_summary: Optional[str] = None
    library_link_reserved: bool = False
    memory_write_reserved: bool = False
    post_processing_reserve_applied: bool = False
    # M0.5：与 Summary×后处理契约的交叉引用（在 run_summary 之后由 builder 回填）
    summary_post_processing_entry_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_candidates": [r.to_dict() for r in self.record_candidates],
            "analysis_reserve": [a.to_dict() for a in self.analysis_reserve],
            "routing_reserve": [r.to_dict() for r in self.routing_reserve],
            "post_processing_summary": self.post_processing_summary,
            "library_link_reserved": bool(self.library_link_reserved),
            "memory_write_reserved": bool(self.memory_write_reserved),
            "post_processing_reserve_applied": bool(self.post_processing_reserve_applied),
            "summary_post_processing_entry_id": self.summary_post_processing_entry_id,
        }


def build_post_processing_intelligence_reserve(frame: Dict[str, Any]) -> PostProcessingIntelligenceReserveResult:
    """
    M0 最小占位：从现有 frame 粗映射记录候选 / 分析占位 / 去向占位；不做真实后处理。
    """
    if not isinstance(frame, dict):
        return PostProcessingIntelligenceReserveResult()

    records: List[PostProcessRecordCandidate] = []
    analyses: List[PostProcessAnalysisReserve] = []
    routes: List[PostProcessRoutingReserve] = []

    tid = _s(frame.get("trace_anchor_id"))
    hints = frame.get("post_processing_hints") if isinstance(frame.get("post_processing_hints"), dict) else {}
    bench_hint = bool(hints.get("scenario_benchmark")) or _trace_benchmark_hint(tid)
    real_hint = bool(hints.get("real_case_result")) or _trace_real_case_hint(tid)

    rst = frame.get("reasoning_structure_tree") if isinstance(frame.get("reasoning_structure_tree"), dict) else None
    rtv = frame.get("reasoning_timeline_view") if isinstance(frame.get("reasoning_timeline_view"), dict) else None
    if rst and rst.get("tree_applied"):
        records.append(
            PostProcessRecordCandidate(
                record_source_type="reasoning_trace",
                record_summary=_s(rst.get("tree_summary")) or "reasoning_structure_tree present",
                record_category_hint="reasoning_backbone",
                record_quality_hint="tree_applied",
                record_candidate_ready=True,
            )
        )
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="classification",
                analysis_summary="reserve: structure tree snapshot for future classification",
                analysis_reserved_only=True,
                analysis_note="M0 stub",
            )
        )
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="pattern_extraction",
                analysis_summary="reserve: branch/path patterns (not extracted)",
                analysis_reserved_only=True,
                analysis_note="M0 stub",
            )
        )
    elif rtv and rtv.get("timeline_applied"):
        records.append(
            PostProcessRecordCandidate(
                record_source_type="reasoning_trace",
                record_summary=_s(rtv.get("key_transition_summary")) or "reasoning_timeline_view present",
                record_category_hint="temporal_flow",
                record_quality_hint="timeline_applied",
                record_candidate_ready=True,
            )
        )

    if _any_whitebox_summary(frame):
        records.append(
            PostProcessRecordCandidate(
                record_source_type="whitebox_summary",
                record_summary="whitebox trace layer present",
                record_category_hint="explainability",
                record_quality_hint="whitebox_summary",
                record_candidate_ready=True,
            )
        )

    ofb = frame.get("optimization_feedback_loop") if isinstance(frame.get("optimization_feedback_loop"), dict) else None
    if ofb:
        records.append(
            PostProcessRecordCandidate(
                record_source_type="optimization_feedback",
                record_summary=_s(ofb.get("validation_reason")) or _s(ofb.get("current_metrics_summary")) or "optimization_feedback_loop",
                record_category_hint="optimization",
                record_quality_hint="feedback_loop",
                record_candidate_ready=True,
            )
        )
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="strategy_effectiveness_analysis",
                analysis_summary=_s(ofb.get("suggested_next_step")) or "reserve: strategy / optimization effectiveness",
                analysis_reserved_only=True,
                analysis_note="M0 stub",
            )
        )
        routes.append(
            PostProcessRoutingReserve(
                routing_target="library_candidate_pool",
                routing_reason_summary="optimization / strategy-adjacent signals → library candidate pool (reserve)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    if bench_hint:
        records.append(
            PostProcessRecordCandidate(
                record_source_type="scenario_benchmark",
                record_summary=f"scenario_benchmark hint (trace={tid or '—'})",
                record_category_hint="evaluation",
                record_quality_hint="benchmark_context",
                record_candidate_ready=True,
            )
        )
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="failure_mode_analysis",
                analysis_summary="reserve: benchmark / harness failure-mode observation",
                analysis_reserved_only=True,
                analysis_note="M0 stub",
            )
        )

    if real_hint:
        records.append(
            PostProcessRecordCandidate(
                record_source_type="real_case_result",
                record_summary=f"real_case hint (trace={tid or '—'})",
                record_category_hint="real_scenario",
                record_quality_hint="pack_case",
                record_candidate_ready=True,
            )
        )
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="failure_mode_analysis",
                analysis_summary="reserve: real-case outcome observation",
                analysis_reserved_only=True,
                analysis_note="M0 stub",
            )
        )

    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else None
    raw = _s(_get(cib, "confirmation_input_raw_text")) if cib else None
    if raw:
        records.append(
            PostProcessRecordCandidate(
                record_source_type="user_feedback",
                record_summary=raw[:200],
                record_category_hint="user_channel",
                record_quality_hint="confirmation",
                record_candidate_ready=True,
            )
        )

    sis = frame.get("strategy_injection_shadow") if isinstance(frame.get("strategy_injection_shadow"), dict) else None
    if sis and (sis.get("shadow_reason") or sis.get("injection_target_module")):
        records.append(
            PostProcessRecordCandidate(
                record_source_type="strategy_shadow",
                record_summary=_s(sis.get("shadow_reason")) or "strategy_injection_shadow present",
                record_category_hint="strategy",
                record_quality_hint="shadow_only",
                record_candidate_ready=True,
            )
        )
        routes.append(
            PostProcessRoutingReserve(
                routing_target="library_candidate_pool",
                routing_reason_summary="strategy shadow → library strategy candidate pool (reserve, no inject)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    dcg = frame.get("decision_contamination_guard_reserve") if isinstance(frame.get("decision_contamination_guard_reserve"), dict) else None
    if dcg and dcg.get("contamination_guard_applied"):
        analyses.append(
            PostProcessAnalysisReserve(
                analysis_type="contamination_observation",
                analysis_summary=_s(dcg.get("contamination_observation_summary")) or "contamination guard reserve present",
                analysis_reserved_only=True,
                analysis_note="cross-link: contamination_guard_reserve",
            )
        )
        routes.append(
            PostProcessRoutingReserve(
                routing_target="contamination_observation_pool",
                routing_reason_summary="contamination observation chain → dedicated pool (reserve)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    # 粗去向：长期模式候选（结构 + 白盒齐全时偏 memory 池占位）
    if rst and rst.get("tree_applied") and _any_whitebox_summary(frame):
        routes.append(
            PostProcessRoutingReserve(
                routing_target="memory_candidate_pool",
                routing_reason_summary="stable reasoning + explainability signals → memory candidate pool (reserve)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    # 低信息量帧：丢弃候选占位（仍保留结构，便于观测空帧）
    if not records:
        records.append(
            PostProcessRecordCandidate(
                record_source_type="unknown",
                record_summary="minimal frame: no strong post-processing signals",
                record_category_hint="unknown",
                record_quality_hint="low",
                record_candidate_ready=False,
            )
        )
        routes.append(
            PostProcessRoutingReserve(
                routing_target="discard_candidate",
                routing_reason_summary="no extractable record signals → discard pool candidate (reserve)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    if not routes:
        routes.append(
            PostProcessRoutingReserve(
                routing_target="risk_observation_pool",
                routing_reason_summary="default observation pool placeholder (reserve)",
                routing_requires_filtering=True,
                routing_reserved_only=True,
            )
        )

    lib_ok = any(r.routing_target == "library_candidate_pool" for r in routes)
    mem_ok = any(r.routing_target == "memory_candidate_pool" for r in routes)

    parts: List[str] = []
    if records:
        parts.append(f"records={len(records)}")
    if analyses:
        parts.append(f"analysis_slots={len(analyses)}")
    if routes:
        parts.append(f"routing_slots={len(routes)}")
    summary = "；".join(parts) if parts else "post_processing_intelligence_reserve: empty"
    if not summary.strip():
        summary = "post_processing_intelligence_reserve: placeholder only"

    return PostProcessingIntelligenceReserveResult(
        record_candidates=records,
        analysis_reserve=analyses,
        routing_reserve=routes,
        post_processing_summary=summary,
        library_link_reserved=bool(lib_ok or bench_hint or bool(ofb)),
        memory_write_reserved=bool(mem_ok),
        post_processing_reserve_applied=True,
    )
