# -*- coding: utf-8 -*-
"""
将 VoiceLongInputStructuredParseResult（模型/适配产物）转为 VoiceLongInputParseResult，
并调用既有 builder 生成 task_plan_v1。

模型链不得绕过 builder。
"""

from __future__ import annotations

from datetime import datetime, timezone

from shared.schemas.domain_classification import DomainClassificationResult

from capabilities.voice.bridge.voice_long_input_task_plan_builder import build_task_plan_v1_from_candidates, new_plan_id
from capabilities.voice.bridge.voice_long_voice_feedback_deriver import attach_voice_feedback_to_parse_result
from capabilities.voice.schemas.voice_long_input_input_mode import InputModeJudgement, NonTaskPayload, NonTaskSegment
from capabilities.voice.schemas.voice_long_input_instruction_candidate import VoiceLongInputInstructionCandidate
from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    NonTaskPayloadStructuredV1_1,
    TaskCandidateV1_1,
    VoiceLongInputStructuredParseResult,
)


def global_judgement_to_domain_result(gj: GlobalJudgementStructuredV1_1) -> DomainClassificationResult:
    return DomainClassificationResult(
        primary_domain=gj.primary_domain,
        secondary_domains=list(gj.secondary_domains),
        intent_complexity=gj.intent_complexity,
        can_map_to_system_tasks=gj.can_map_to_system_tasks,
        needs_confirmation=gj.needs_confirmation,
        needs_clarification=gj.needs_clarification,
        should_reject=gj.should_reject,
        rejection_reason_candidate=gj.rejection_reason_candidate,
        confidence=gj.confidence,
    )


def task_candidate_to_instruction(tc: TaskCandidateV1_1) -> VoiceLongInputInstructionCandidate:
    params = dict(tc.target) if isinstance(tc.target, dict) else {}
    return VoiceLongInputInstructionCandidate(
        system_mapping_candidate=tc.system_mapping_candidate,
        param_candidates=params,
        requires_confirmation_candidate=tc.requires_confirmation,
        confidence=tc.confidence,
        segment_text=str(params.get("segment_text", "") or ""),
        ordering_index=max(0, int(tc.execution_order or 1) - 1),
        relation_hint="",
    )


def input_mode_structured_to_dataclass(im: InputModeJudgementStructuredV1_1) -> InputModeJudgement:
    return InputModeJudgement(
        mode=im.mode,
        has_task_content=im.has_task_content,
        has_non_task_content=im.has_non_task_content,
        should_generate_task_plan=im.should_generate_task_plan,
        should_preserve_non_task_payload=im.should_preserve_non_task_payload,
        reason_notes="",
    )


def structured_non_task_to_payload(sp: NonTaskPayloadStructuredV1_1) -> NonTaskPayload:
    if not sp.exists:
        return NonTaskPayload(exists=False)
    segs = [NonTaskSegment(segment_type=s.segment_type, content=s.content) for s in sp.segments]
    return NonTaskPayload(exists=True, segments=segs, handoff_candidate=sp.handoff_candidate)


def structured_to_voice_long_input_parse_result(
    structured: VoiceLongInputStructuredParseResult,
    *,
    raw_text: str,
    request_id: str,
    session_hint: str,
    notes_prefix: str = "model_chain",
) -> VoiceLongInputParseResult:
    """模型链收口：统一 VoiceLongInputParseResult + task_plan_v1（经 builder）。"""
    raw = raw_text or ""
    dr = global_judgement_to_domain_result(structured.global_judgement)
    cands = [task_candidate_to_instruction(tc) for tc in structured.task_candidates]
    im_j = input_mode_structured_to_dataclass(structured.input_mode_judgement)
    ntp = structured_non_task_to_payload(structured.non_task_payload)

    mixed = structured.input_mode_judgement.mode == "mixed_task_and_non_task"

    if structured.input_mode_judgement.mode == "non_task_only" and not cands:
        res = VoiceLongInputParseResult(
            request_id=request_id,
            raw_text=raw,
            domain_result=dr,
            instruction_candidates=[],
            task_plan_v1=None,
            clarification_needed=False,
            rejection_needed=False,
            notes=f"{notes_prefix}_non_task_only",
            session_hint=session_hint,
            input_mode_judgement=im_j,
            non_task_payload=ntp,
            mixed_input_flag=False,
        )
        return attach_voice_feedback_to_parse_result(res)

    if dr.should_reject:
        res = VoiceLongInputParseResult(
            request_id=request_id,
            raw_text=raw,
            domain_result=dr,
            instruction_candidates=cands,
            task_plan_v1=None,
            clarification_needed=False,
            rejection_needed=True,
            rejection_reason=dr.rejection_reason_candidate,
            notes=f"{notes_prefix}_rejected",
            session_hint=session_hint,
            input_mode_judgement=im_j,
            non_task_payload=ntp,
            mixed_input_flag=mixed,
        )
        return attach_voice_feedback_to_parse_result(res)

    if not cands:
        res = VoiceLongInputParseResult(
            request_id=request_id,
            raw_text=raw,
            domain_result=dr,
            instruction_candidates=[],
            task_plan_v1=None,
            clarification_needed=True,
            rejection_needed=False,
            notes=f"{notes_prefix}_no_candidates",
            session_hint=session_hint,
            input_mode_judgement=im_j,
            non_task_payload=ntp,
            mixed_input_flag=mixed,
        )
        return attach_voice_feedback_to_parse_result(res)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan = build_task_plan_v1_from_candidates(
        plan_id=new_plan_id(),
        domain=dr,
        candidates=cands,
        clarification_needed=dr.needs_clarification,
        rejection_needed=False,
        generated_at=ts,
    )
    res = VoiceLongInputParseResult(
        request_id=request_id,
        raw_text=raw,
        domain_result=dr,
        instruction_candidates=cands,
        task_plan_v1=plan,
        clarification_needed=dr.needs_clarification,
        rejection_needed=False,
        notes=f"{notes_prefix}_ok",
        session_hint=session_hint,
        input_mode_judgement=im_j,
        non_task_payload=ntp,
        mixed_input_flag=mixed,
    )
    return attach_voice_feedback_to_parse_result(res)
