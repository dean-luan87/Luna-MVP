# -*- coding: utf-8 -*-
"""
从规则引擎产物组装 VoiceLongInputStructuredParseResult（v1.1）。

当前不接模型：由 VoiceLongInputParseResult + 元数据填充总 Schema；
后续模型可直接产出同结构或覆写字段。
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    ClarificationCandidateV1_1,
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    KnowledgeCollaborationV1_1,
    NonTaskPayloadStructuredV1_1,
    NonTaskSegmentStructuredV1_1,
    ParserNotesV1_1,
    TaskCandidateConstraintV1_1,
    TaskCandidateEntityV1_1,
    TaskCandidateV1_1,
    TaskOptimizationV1_1,
    UnsupportedCandidateV1_1,
    VoiceInputMetaV1_1,
    VoiceLongInputStructuredParseResult,
)


def build_voice_long_input_structured_parse_v1_1(
    parse: VoiceLongInputParseResult,
    *,
    raw_text: Optional[str] = None,
    normalized_text: Optional[str] = None,
    normalized_text_override: Optional[str] = None,
    is_continuation: bool = False,
    context_resume_hint: str = "",
    parse_timestamp_iso: Optional[str] = None,
    input_mode_confidence: float = 0.0,
    global_confidence_override: Optional[float] = None,
) -> VoiceLongInputStructuredParseResult:
    """
    将管线内 `VoiceLongInputParseResult` 升为总 Schema v1.1。

    - task_plan_v1 仅反映原始理解；协同/优化块占位。
    - feedback_candidate 来自 parse.voice_feedback（若已挂载）。
    """
    raw = raw_text if raw_text is not None else parse.raw_text
    norm = normalized_text_override or normalized_text or (raw or "").strip()
    ts = parse_timestamp_iso or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    dr = parse.domain_result
    im_conf = input_mode_confidence or 0.88
    if parse.input_mode_judgement is not None:
        im_conf = max(im_conf, 0.75)
        im = parse.input_mode_judgement
        input_mode = InputModeJudgementStructuredV1_1(
            mode=im.mode,
            has_task_content=im.has_task_content,
            has_non_task_content=im.has_non_task_content,
            should_generate_task_plan=im.should_generate_task_plan,
            should_preserve_non_task_payload=im.should_preserve_non_task_payload,
            confidence=im_conf,
        )
    else:
        input_mode = InputModeJudgementStructuredV1_1(
            mode="task_only",
            has_task_content=True,
            has_non_task_content=False,
            should_generate_task_plan=True,
            should_preserve_non_task_payload=False,
            confidence=0.75,
        )

    gj_conf = global_confidence_override if global_confidence_override is not None else dr.confidence
    global_j = GlobalJudgementStructuredV1_1(
        primary_domain=dr.primary_domain,
        secondary_domains=list(dr.secondary_domains),
        intent_complexity=dr.intent_complexity,
        can_map_to_system_tasks=dr.can_map_to_system_tasks,
        needs_confirmation=dr.needs_confirmation,
        needs_clarification=dr.needs_clarification,
        should_reject=dr.should_reject,
        rejection_reason_candidate=dr.rejection_reason_candidate,
        safety_risk_level="high" if dr.should_reject else "low",
        confidence=gj_conf,
    )

    task_cands = _build_task_candidates(parse)
    non_task = _build_non_task_payload_structured(parse)

    kc = KnowledgeCollaborationV1_1(
        history_used=False,
        history_confirmation_recommended=False,
        matched_history_tasks=[],
        matched_memory_entities=[],
        auto_filled_fields=[],
        reused_experience_candidates=[],
        history_conflict_flags=[],
        confidence=0.0,
    )

    topt = TaskOptimizationV1_1(
        optimization_applied=False,
        optimization_candidates=[],
        recommended_reordering=[],
        requires_user_confirmation=False,
        optimization_reasoning_summary="",
    )

    clar: List[ClarificationCandidateV1_1] = []
    if parse.clarification_needed or dr.needs_clarification:
        rid = task_cands[0].candidate_id if task_cands else None
        clar.append(
            ClarificationCandidateV1_1(
                clarification_id="cq_001",
                reason="needs_clarification",
                question_candidate="需要更多信息才能继续编排。",
                related_task_candidate_id=rid,
                priority="high",
            )
        )

    unsup: List[UnsupportedCandidateV1_1] = []
    if parse.rejection_needed:
        unsup.append(
            UnsupportedCandidateV1_1(
                item_id="uc_001",
                unsupported_type="out_of_scope_action",
                content=raw or "",
                reason_candidate=parse.rejection_reason or dr.rejection_reason_candidate or "",
                suggested_fallback="",
            )
        )

    fb: Dict[str, Any] = {}
    if parse.voice_feedback is not None:
        fb = parse.voice_feedback.to_dict()

    parser_notes = ParserNotesV1_1(
        contains_multiple_intents=len(parse.instruction_candidates) > 1,
        contains_conditional_logic=bool(re.search(r"如果|要是|除非", raw or "")),
        contains_context_reference=bool(context_resume_hint or parse.session_hint),
        possible_conflict_with_current_task=False,
        notes=parse.notes,
    )

    meta = VoiceInputMetaV1_1(
        input_type="voice_long_text",
        source_language="zh",
        raw_text=raw or "",
        normalized_text=norm,
        is_continuation=is_continuation,
        context_resume_hint=context_resume_hint or parse.session_hint or "",
        parse_timestamp=ts,
    )

    return VoiceLongInputStructuredParseResult(
        schema_version=SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
        input_meta=meta,
        input_mode_judgement=input_mode,
        global_judgement=global_j,
        task_candidates=task_cands,
        non_task_payload=non_task,
        knowledge_collaboration=kc,
        task_optimization=topt,
        clarification_candidates=clar,
        unsupported_candidates=unsup,
        feedback_candidate=fb,
        parser_notes=parser_notes,
    )


def _build_task_candidates(parse: VoiceLongInputParseResult) -> List[TaskCandidateV1_1]:
    out: List[TaskCandidateV1_1] = []
    plan = parse.task_plan_v1
    if plan and plan.tasks:
        for i, t in enumerate(plan.tasks):
            try:
                order_idx = list(plan.execution_order).index(t.task_id) + 1
            except ValueError:
                order_idx = i + 1
            tgt = dict(t.target) if t.target else {}
            if not tgt and t.metadata.get("segment_text"):
                tgt = {"type": "segment", "value": t.metadata.get("segment_text", "")}
            ents = _entities_from_target(tgt)
            conds: List[Any] = []
            if "conditional_clauses" in tgt:
                conds = tgt.get("conditional_clauses") or []
            out.append(
                TaskCandidateV1_1(
                    candidate_id=f"tc_{i + 1:03d}",
                    task_domain=t.task_domain,
                    task_action=t.task_action,
                    system_mapping_candidate=t.system_mapping_candidate,
                    target=tgt,
                    entities=ents,
                    constraints=[TaskCandidateConstraintV1_1(constraint_type="priority", value=str(t.priority))],
                    conditional_clauses=conds if isinstance(conds, list) else [],
                    execution_order=order_idx,
                    dependency=t.dependency,
                    is_temporary=t.is_temporary,
                    requires_confirmation=t.requires_confirmation,
                    can_execute_directly_candidate=not t.requires_confirmation,
                    confidence=t.confidence,
                )
            )
        return out

    for i, c in enumerate(parse.instruction_candidates):
        out.append(
            TaskCandidateV1_1(
                candidate_id=f"tc_{i + 1:03d}",
                task_domain=parse.domain_result.primary_domain,
                task_action=_infer_task_action(c.system_mapping_candidate),
                system_mapping_candidate=c.system_mapping_candidate,
                target=_target_from_params(c.param_candidates),
                entities=_entities_from_target(_target_from_params(c.param_candidates)),
                constraints=[],
                conditional_clauses=[],
                execution_order=c.ordering_index + 1 if c.ordering_index else i + 1,
                dependency=None,
                is_temporary=False,
                requires_confirmation=c.requires_confirmation_candidate,
                can_execute_directly_candidate=not c.requires_confirmation_candidate,
                confidence=c.confidence,
            )
        )
    return out


def _infer_task_action(mapping: str) -> str:
    m = (mapping or "").lower()
    if "navigation" in m:
        return "start_navigation"
    if "observation" in m:
        return "observe"
    return "unknown"


def _target_from_params(params: Dict[str, Any]) -> Dict[str, Any]:
    if not params:
        return {}
    if "destination" in params:
        return {"type": "poi_category", "value": params.get("destination"), "qualifier": params.get("qualifier", "")}
    return dict(params)


def _entities_from_target(target: Dict[str, Any]) -> List[TaskCandidateEntityV1_1]:
    if not target:
        return []
    val = target.get("value") or target.get("destination") or ""
    et = str(target.get("type") or "poi_category")
    if val:
        return [TaskCandidateEntityV1_1(entity_type=et, entity_value=str(val))]
    return []


def _map_segment_type(st: str) -> str:
    if st == "narrative":
        return "background_explanation"
    if st == "other":
        return "non_task_dialogue"
    return st


def _build_non_task_payload_structured(parse: VoiceLongInputParseResult) -> NonTaskPayloadStructuredV1_1:
    p = parse.non_task_payload
    if not p or not p.exists:
        return NonTaskPayloadStructuredV1_1(exists=False, confidence=0.0)
    segs: List[NonTaskSegmentStructuredV1_1] = []
    for i, s in enumerate(p.segments):
        segs.append(
            NonTaskSegmentStructuredV1_1(
                segment_id=f"nt_{i + 1:03d}",
                segment_type=_map_segment_type(s.segment_type),
                content=s.content,
            )
        )
    return NonTaskPayloadStructuredV1_1(
        exists=True,
        segments=segs,
        handoff_candidate=p.handoff_candidate,
        confidence=0.84,
    )
