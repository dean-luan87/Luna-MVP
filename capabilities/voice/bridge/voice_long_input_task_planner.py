# -*- coding: utf-8 -*-
"""
长输入拆解 v1。

- `run_long_input_task_planning_v1`：总入口，经 `voice_long_input_parse_orchestrator` 路由规则链或模型链（可配置）。
- `run_long_input_task_planning_v1_rule_chain`：纯规则链（classifier → mapper → builder），供模型降级与测试复用。

顺序固定：先长语音类型判定，再域分类，再指令候选，再任务计划（规格写死）。
不生成 V2/Final；非任务内容写入 non_task_payload，供情感引擎预留。
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any, List, Optional

from capabilities.voice.bridge.voice_long_input_domain_classifier import classify_long_input_text
from capabilities.voice.bridge.voice_long_input_instruction_mapper import map_long_input_instructions
from capabilities.voice.bridge.voice_long_input_mode_judgement import (
    LongVoiceModeAnalysis,
    analyze_long_voice_input_mode,
    merge_notes,
)
from capabilities.voice.bridge.voice_long_input_task_plan_builder import (
    build_task_plan_v1_from_candidates,
    new_plan_id,
)
from capabilities.voice.bridge.voice_long_voice_feedback_deriver import attach_voice_feedback_to_parse_result
from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult


def split_segments(text: str) -> List[str]:
    """按「然后/然后/再/，」切分；单句则整段为一段。"""
    t = (text or "").strip()
    if not t:
        return []
    parts = re.split(r"(?:然后|接着|之后)|[，,]", t)
    segs = [p.strip() for p in parts if p.strip()]
    return segs if segs else [t]


def run_long_input_task_planning_v1_rule_chain(
    text: str,
    *,
    request_id: str = "",
    session_hint: str = "",
) -> VoiceLongInputParseResult:
    """
    纯规则链：输入模式判定 → 规则 classifier → 规则 mapper → builder → task_plan_v1。

    非任务型长语音：不 reject 为无效，primary_domain=non_task_dialogue_future，保留 non_task_payload。
    """
    rid = request_id or str(uuid.uuid4())
    raw = (text or "").strip()
    mode = analyze_long_voice_input_mode(raw)

    if not raw:
        from shared.schemas.domain_classification import DomainClassificationResult
        from shared.schemas.task_domain_v1 import UNSUPPORTED_OR_REJECT

        dr = DomainClassificationResult(
            primary_domain=UNSUPPORTED_OR_REJECT,
            needs_clarification=True,
            can_map_to_system_tasks=False,
            confidence=0.0,
        )
        return _attach_mode(
            VoiceLongInputParseResult(
                request_id=rid,
                raw_text=raw,
                domain_result=dr,
                instruction_candidates=[],
                task_plan_v1=None,
                clarification_needed=True,
                rejection_needed=False,
                notes="empty_input",
                session_hint=session_hint,
            ),
            mode,
        )

    # 纯非任务长对话：预留出口，不生成任务计划
    if mode.judgement.mode == "non_task_only" and not (mode.task_text_for_planner or "").strip():
        return _non_task_dialogue_reserved(rid, raw, mode, session_hint)

    task_body = (mode.task_text_for_planner or "").strip() or raw

    segments = split_segments(task_body)
    if len(segments) > 3:
        dr = classify_long_input_text(task_body)
        return _attach_mode(
            VoiceLongInputParseResult(
                request_id=rid,
                raw_text=raw,
                domain_result=dr,
                instruction_candidates=[],
                task_plan_v1=None,
                clarification_needed=True,
                rejection_needed=False,
                notes=merge_notes("too_many_segments_v1_limit_3", mode),
                session_hint=session_hint,
            ),
            mode,
        )

    dr = classify_long_input_text(task_body)
    if dr.should_reject:
        return _attach_mode(
            VoiceLongInputParseResult(
                request_id=rid,
                raw_text=raw,
                domain_result=dr,
                instruction_candidates=[],
                task_plan_v1=None,
                clarification_needed=False,
                rejection_needed=True,
                rejection_reason=dr.rejection_reason_candidate,
                notes=merge_notes("unsupported_or_reject", mode),
                session_hint=session_hint,
            ),
            mode,
        )

    cands = map_long_input_instructions(dr, task_body, segments)
    if not cands and not dr.needs_clarification:
        return _attach_mode(
            VoiceLongInputParseResult(
                request_id=rid,
                raw_text=raw,
                domain_result=dr,
                instruction_candidates=[],
                task_plan_v1=None,
                clarification_needed=True,
                rejection_needed=False,
                notes=merge_notes("no_instruction_candidates", mode),
                session_hint=session_hint,
            ),
            mode,
        )

    if not cands:
        return _attach_mode(
            VoiceLongInputParseResult(
                request_id=rid,
                raw_text=raw,
                domain_result=dr,
                instruction_candidates=[],
                task_plan_v1=None,
                clarification_needed=True,
                rejection_needed=False,
                notes=merge_notes(dr.metadata.get("reason", "ambiguous"), mode),
                session_hint=session_hint,
            ),
            mode,
        )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan = build_task_plan_v1_from_candidates(
        plan_id=new_plan_id(),
        domain=dr,
        candidates=cands,
        clarification_needed=dr.needs_clarification,
        rejection_needed=False,
        generated_at=ts,
    )

    return _attach_mode(
        VoiceLongInputParseResult(
            request_id=rid,
            raw_text=raw,
            domain_result=dr,
            instruction_candidates=cands,
            task_plan_v1=plan,
            clarification_needed=dr.needs_clarification,
            rejection_needed=False,
            notes=merge_notes("ok_v1", mode),
            session_hint=session_hint,
        ),
        mode,
    )


def _attach_mode(res: VoiceLongInputParseResult, mode: LongVoiceModeAnalysis) -> VoiceLongInputParseResult:
    res.input_mode_judgement = mode.judgement
    res.non_task_payload = mode.non_task_payload
    res.mixed_input_flag = mode.judgement.mode == "mixed_task_and_non_task"
    return _with_feedback(res)


def _with_feedback(res: VoiceLongInputParseResult) -> VoiceLongInputParseResult:
    return attach_voice_feedback_to_parse_result(res)


def run_long_input_task_planning_v1(
    text: str,
    *,
    request_id: str = "",
    session_hint: str = "",
    parse_config: Optional[Any] = None,
    model_provider: Optional[Any] = None,
) -> VoiceLongInputParseResult:
    """
    长输入解析总入口：默认规则链；可配置 model_preferred + Provider（见 orchestrator）。

    外部签名保持兼容；新增参数均为可选。
    """
    from capabilities.voice.bridge.voice_long_input_parse_orchestrator import orchestrate_long_input_task_planning

    return orchestrate_long_input_task_planning(
        text,
        request_id=request_id,
        session_hint=session_hint,
        parse_config=parse_config,
        model_provider=model_provider,
    )


def _non_task_dialogue_reserved(
    rid: str,
    raw: str,
    mode: LongVoiceModeAnalysis,
    session_hint: str,
) -> VoiceLongInputParseResult:
    from shared.schemas.domain_classification import DomainClassificationResult
    from shared.schemas.task_domain_v1 import NON_TASK_DIALOGUE_FUTURE

    dr = DomainClassificationResult(
        primary_domain=NON_TASK_DIALOGUE_FUTURE,
        secondary_domains=[],
        intent_complexity="single_step",
        can_map_to_system_tasks=False,
        needs_clarification=False,
        should_reject=False,
        confidence=0.55,
        metadata={
            "should_execute_task_plan": False,
            "handoff_candidate": "emotion_engine_future",
            "no_task_plan_generated": True,
        },
    )
    payload = mode.non_task_payload
    res = VoiceLongInputParseResult(
        request_id=rid,
        raw_text=raw,
        domain_result=dr,
        instruction_candidates=[],
        task_plan_v1=None,
        clarification_needed=False,
        rejection_needed=False,
        notes=merge_notes("non_task_dialogue_reserved", mode),
        session_hint=session_hint,
        input_mode_judgement=mode.judgement,
        non_task_payload=payload,
        mixed_input_flag=False,
    )
    return _with_feedback(res)
