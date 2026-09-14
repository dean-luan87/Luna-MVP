# -*- coding: utf-8 -*-
"""
从 VoiceLongInputParseResult 推导 VoiceLongVoiceFeedbackResult（规则版 v1）。

不接模型；仅映射主反馈模式与占位文案，供上层策略替换变量。
"""

from __future__ import annotations

from capabilities.voice.schemas.voice_long_input_feedback_kind import (
    MIXED_INPUT_ACKNOWLEDGED,
    NON_TASK_PRESERVED_FOR_FUTURE,
    TASK_UNDERSTOOD_AND_READY,
    TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION,
    TASK_UNDERSTOOD_BUT_NEED_CONFIRMATION,
    TEMPLATE_MIXED_ACK,
    TEMPLATE_NEED_CLARIFICATION,
    TEMPLATE_NEED_CONFIRMATION,
    TEMPLATE_NO_TASK_HEARD,
    TEMPLATE_TASK_READY,
    TEMPLATE_UNSUPPORTED,
    UNSUPPORTED_OR_REJECTED,
)
from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult
from capabilities.voice.schemas.voice_long_voice_feedback_result import VoiceLongVoiceFeedbackResult
from shared.schemas.task_plan import TaskPlan
from shared.schemas.task_domain_v1 import NON_TASK_DIALOGUE_FUTURE


def derive_long_voice_feedback_result(
    parse: VoiceLongInputParseResult,
    *,
    related_plan_version: str = "v1",
) -> VoiceLongVoiceFeedbackResult:
    """
    硬规则（当前阶段）：
    1. 任务反馈优先于情绪表达表述（文案仍克制）。
    2. 非任务不假装已被情感引擎处理；non_task_acknowledged 仅表示「已记录」语义位。
    3. V1 反馈反映当前 parse，不提前宣称 V2 优化已完成。
    """
    dr = parse.domain_result
    pc = parse.task_plan_v1

    if dr.primary_domain == NON_TASK_DIALOGUE_FUTURE:
        return VoiceLongVoiceFeedbackResult(
            feedback_mode=NON_TASK_PRESERVED_FOR_FUTURE,
            feedback_text_candidate=TEMPLATE_NO_TASK_HEARD,
            requires_user_response=False,
            related_plan_version="none",
            non_task_acknowledged=True,
            metadata={"handoff": "emotion_engine_future"},
        )

    is_mixed = parse.mixed_input_flag or (
        parse.input_mode_judgement is not None
        and parse.input_mode_judgement.mode == "mixed_task_and_non_task"
    )
    if is_mixed:
        extra = ""
        if pc is not None and pc.execution_order:
            extra = "现在我会按你的顺序准备任务步骤。"
        return VoiceLongVoiceFeedbackResult(
            feedback_mode=MIXED_INPUT_ACKNOWLEDGED,
            feedback_text_candidate=f"{TEMPLATE_MIXED_ACK}{extra}",
            requires_user_response=False,
            related_plan_version=related_plan_version,
            non_task_acknowledged=True,
            metadata={"has_task_plan": pc is not None},
        )

    if parse.rejection_needed:
        return VoiceLongVoiceFeedbackResult(
            feedback_mode=UNSUPPORTED_OR_REJECTED,
            feedback_text_candidate=TEMPLATE_UNSUPPORTED,
            requires_user_response=False,
            related_plan_version=related_plan_version,
            non_task_acknowledged=False,
            metadata={"rejection_reason": parse.rejection_reason or ""},
        )

    if parse.clarification_needed or dr.needs_clarification:
        return VoiceLongVoiceFeedbackResult(
            feedback_mode=TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION,
            feedback_text_candidate=TEMPLATE_NEED_CLARIFICATION.format(
                intent="这件事",
                missing="更多细节",
            ),
            requires_user_response=True,
            related_plan_version=related_plan_version,
            non_task_acknowledged=False,
            metadata={"domain": dr.primary_domain},
        )

    if pc is not None:
        if pc.confirmation_needed or dr.needs_confirmation:
            a, b = _two_plan_labels(pc)
            return VoiceLongVoiceFeedbackResult(
                feedback_mode=TASK_UNDERSTOOD_BUT_NEED_CONFIRMATION,
                feedback_text_candidate=TEMPLATE_NEED_CONFIRMATION.format(a=a, b=b),
                requires_user_response=True,
                related_plan_version=related_plan_version,
                non_task_acknowledged=False,
                metadata={"needs_confirmation": True},
            )
        labels = _summarize_plan_labels(pc)
        if len(labels) > 1:
            text = TEMPLATE_TASK_READY.format(a=labels[0], b=labels[1])
        elif labels:
            text = f"我明白了。接下来我会先处理：{labels[0]}。"
        else:
            text = TEMPLATE_TASK_READY.format(a="第一步", b="下一步")
        return VoiceLongVoiceFeedbackResult(
            feedback_mode=TASK_UNDERSTOOD_AND_READY,
            feedback_text_candidate=text,
            requires_user_response=False,
            related_plan_version=related_plan_version,
            non_task_acknowledged=False,
            metadata={"execution_order": list(pc.execution_order)},
        )

    return VoiceLongVoiceFeedbackResult(
        feedback_mode=TASK_UNDERSTOOD_BUT_NEED_CLARIFICATION,
        feedback_text_candidate=TEMPLATE_NEED_CLARIFICATION.format(intent="你的请求", missing="更多信息"),
        requires_user_response=True,
        related_plan_version=related_plan_version,
        non_task_acknowledged=False,
    )


def _summarize_plan_labels(pc: TaskPlan) -> list[str]:
    out: list[str] = []
    for tid in pc.execution_order[:3]:
        for t in pc.tasks:
            if t.task_id == tid:
                tgt = (t.target or {}).get("destination") or (t.metadata or {}).get("segment_text") or t.task_action
                out.append(str(tgt)[:24])
                break
    if not out and pc.tasks:
        out = [pc.tasks[0].task_action]
    return out if len(out) >= 2 else (out + ["下一步"]) if out else ["第一步", "第二步"]


def _two_plan_labels(pc: TaskPlan) -> tuple[str, str]:
    labels = _summarize_plan_labels(pc)
    if len(labels) >= 2:
        return labels[0], labels[1]
    if labels:
        return labels[0], "下一步"
    return "第一步", "第二步"


def attach_feedback_to_parse_dict(parse_dict: dict, feedback: VoiceLongVoiceFeedbackResult | None) -> dict:
    d = dict(parse_dict)
    d["voice_feedback"] = feedback.to_dict() if feedback else None
    return d


def attach_voice_feedback_to_parse_result(parse: VoiceLongInputParseResult) -> VoiceLongInputParseResult:
    """供规则链 / 模型链统一挂载 voice_feedback。"""
    parse.voice_feedback = derive_long_voice_feedback_result(parse)
    return parse
