# -*- coding: utf-8 -*-
"""
长语音模型接入适配层（v1）。

原则：模型只产出「理解候选」，输出必须可落到 VoiceLongInputStructuredParseResult；
系统负责结构、治理、协同占位与裁决；规则链始终可兜底。

不接执行层；不替换 task_plan_builder；本地 Qwen 等模型在实现 LongVoiceModelAdapter 后接入。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Protocol, runtime_checkable

from capabilities.voice.bridge.voice_long_input_model_validation import (
    sanitize_structured_parse_mappings,
    validate_structured_parse_minimal,
)
from capabilities.voice.bridge.voice_long_input_structured_parse_builder import (
    build_voice_long_input_structured_parse_v1_1,
)
from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1_rule_chain
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    KnowledgeCollaborationV1_1,
    ParserNotesV1_1,
    TaskOptimizationV1_1,
    VoiceInputMetaV1_1,
    VoiceLongInputStructuredParseResult,
)

logger = logging.getLogger(__name__)


@dataclass
class VoiceLongInputModelIntegrationConfig:
    """双通道开关；默认规则链。"""

    use_model_for_structured_parse: bool = False
    model_timeout_sec: float = 2.0
    """若 True，用规则管线生成的 feedback 覆盖 feedback_candidate 中的文案候选。"""
    template_feedback_text_from_rules: bool = True


@dataclass
class DualChannelParseOutcome:
    """双通道解析结果 + 可追溯元数据。"""

    structured: VoiceLongInputStructuredParseResult
    used_model: bool
    fallback_reason: str = ""
    """空=模型成功 | rule_only | model_unavailable | model_invalid:* | model_exception"""


@runtime_checkable
class LongVoiceModelAdapter(Protocol):
    """
    模型实现：输出必须符合 VoiceLongInputStructuredParseResult（可仅填 A 组理解字段）。

    返回 None 表示本适配器不参与，走规则降级。
    """

    def parse_to_structured(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        ...


class RuleFallbackLongVoiceModelAdapter:
    """占位：不调用模型，始终返回 None → 触发规则链。"""

    def parse_to_structured(
        self,
        text: str,
        *,
        session_hint: str = "",
        request_id: str = "",
    ) -> Optional[VoiceLongInputStructuredParseResult]:
        return None


def enrich_structured_parse_system_b_group(
    structured: VoiceLongInputStructuredParseResult,
    *,
    raw_text: str,
    normalized_text: Optional[str] = None,
    is_continuation: bool = False,
    context_resume_hint: str = "",
    parse_timestamp_iso: Optional[str] = None,
) -> VoiceLongInputStructuredParseResult:
    """
    B 组系统字段覆盖：schema_version、input_meta、knowledge_collaboration、
    task_optimization、parser_notes 治理位（不覆盖 A 组理解字段）。

    knowledge / task_optimization 始终为占位，待图书馆与环境协同写入。
    """
    norm = (normalized_text or raw_text or "").strip()
    ts = parse_timestamp_iso or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    structured.schema_version = SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1
    structured.input_meta = VoiceInputMetaV1_1(
        input_type="voice_long_text",
        source_language="zh",
        raw_text=raw_text or "",
        normalized_text=norm,
        is_continuation=is_continuation,
        context_resume_hint=context_resume_hint or "",
        parse_timestamp=ts,
    )
    structured.knowledge_collaboration = KnowledgeCollaborationV1_1()
    structured.task_optimization = TaskOptimizationV1_1()

    pn = structured.parser_notes or ParserNotesV1_1()
    prev_notes = pn.notes or ""
    structured.parser_notes = ParserNotesV1_1(
        contains_multiple_intents=pn.contains_multiple_intents,
        contains_conditional_logic=pn.contains_conditional_logic,
        contains_context_reference=pn.contains_context_reference,
        possible_conflict_with_current_task=pn.possible_conflict_with_current_task,
        notes=(prev_notes + ";system_b_group_enriched").strip(";"),
    )
    return structured


def run_structured_long_input_parse_v1_1_dual_channel(
    text: str,
    *,
    config: VoiceLongInputModelIntegrationConfig,
    adapter: LongVoiceModelAdapter,
    session_hint: str = "",
    request_id: str = "",
    is_continuation: bool = False,
    context_resume_hint: str = "",
) -> DualChannelParseOutcome:
    """
    双通道：可选模型 → 校验 + B 组系统补位 + mapping 清洗；失败则规则链全量。

    不接执行；不替换 task_plan_builder（规则路径内仍用 builder 生成 task_plan_v1）。
    """
    raw = (text or "").strip()

    if not config.use_model_for_structured_parse:
        return _rule_only(
            raw,
            session_hint=session_hint,
            request_id=request_id,
            is_continuation=is_continuation,
            context_resume_hint=context_resume_hint,
            reason="rule_only",
        )

    try:
        model_out = adapter.parse_to_structured(
            raw,
            session_hint=session_hint,
            request_id=request_id,
        )
    except Exception as e:
        logger.warning("long_voice_model_adapter_exception: %s", e)
        return _rule_only(
            raw,
            session_hint=session_hint,
            request_id=request_id,
            is_continuation=is_continuation,
            context_resume_hint=context_resume_hint,
            reason="model_exception",
        )

    if model_out is None:
        return _rule_only(
            raw,
            session_hint=session_hint,
            request_id=request_id,
            is_continuation=is_continuation,
            context_resume_hint=context_resume_hint,
            reason="model_unavailable",
        )

    ok, inv_reason = validate_structured_parse_minimal(model_out)
    if not ok:
        return _rule_only(
            raw,
            session_hint=session_hint,
            request_id=request_id,
            is_continuation=is_continuation,
            context_resume_hint=context_resume_hint,
            reason=f"model_invalid:{inv_reason}",
        )

    model_out = sanitize_structured_parse_mappings(model_out)
    model_out = enrich_structured_parse_system_b_group(
        model_out,
        raw_text=raw,
        is_continuation=is_continuation,
        context_resume_hint=context_resume_hint,
    )
    if config.template_feedback_text_from_rules:
        rule_parse = run_long_input_task_planning_v1_rule_chain(
            raw,
            request_id=request_id or "",
            session_hint=session_hint,
        )
        rule_struct = build_voice_long_input_structured_parse_v1_1(
            rule_parse,
            raw_text=raw,
            is_continuation=is_continuation,
            context_resume_hint=context_resume_hint,
        )
        if rule_struct.feedback_candidate:
            model_out.feedback_candidate = dict(rule_struct.feedback_candidate)
    return DualChannelParseOutcome(structured=model_out, used_model=True, fallback_reason="")


def _rule_only(
    raw: str,
    *,
    session_hint: str,
    request_id: str,
    is_continuation: bool,
    context_resume_hint: str,
    reason: str,
) -> DualChannelParseOutcome:
    parse = run_long_input_task_planning_v1_rule_chain(raw, request_id=request_id, session_hint=session_hint)
    structured = build_voice_long_input_structured_parse_v1_1(
        parse,
        raw_text=raw,
        is_continuation=is_continuation,
        context_resume_hint=context_resume_hint,
    )
    return DualChannelParseOutcome(structured=structured, used_model=False, fallback_reason=reason)
