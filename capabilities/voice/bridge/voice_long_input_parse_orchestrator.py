# -*- coding: utf-8 -*-
"""
长语音解析协调器：规则链 / 模型链双通道，统一收口到 VoiceLongInputParseResult + task_plan_v1（经 builder）。

不接执行层；不替换 task_plan_builder。
"""

from __future__ import annotations

import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from capabilities.voice.interfaces.voice_long_input_model_provider import VoiceLongInputModelProvider

from capabilities.voice.config.voice_long_input_parse_config import (
    VoiceLongInputParseConfig,
    get_default_voice_long_input_parse_config,
)
from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult

logger = logging.getLogger(__name__)


def orchestrate_long_input_task_planning(
    text: str,
    *,
    request_id: str = "",
    session_hint: str = "",
    parse_config: Optional[VoiceLongInputParseConfig] = None,
    model_provider: Optional["VoiceLongInputModelProvider"] = None,
) -> VoiceLongInputParseResult:
    """
    对外入口（由 run_long_input_task_planning_v1 调用）。

    1) 路由：rule_only → 规则链
    2) model_preferred：Provider → 校验 → structured → builder（经 structured_to_voice_long_input_parse_result）
    3) 失败：fallback 规则链（可配置）
    """
    from capabilities.voice.bridge.voice_long_input_parse_route_selector import (
        should_attempt_model_chain,
        should_use_rule_chain_only,
    )
    from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1_rule_chain

    cfg = parse_config or get_default_voice_long_input_parse_config()
    rid = request_id or str(uuid.uuid4())

    if should_use_rule_chain_only(cfg):
        return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)

    if not should_attempt_model_chain(cfg, model_provider is not None):
        return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)

    raw = (text or "").strip()

    def _call() -> Optional[object]:
        assert model_provider is not None
        return model_provider.parse_long_input(
            raw,
            session_hint=session_hint,
            request_id=rid,
        )

    try:
        timeout_sec = max(0.05, cfg.model_timeout_ms / 1000.0)
        with ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(_call)
            structured = fut.result(timeout=timeout_sec)
    except FuturesTimeout:
        logger.warning("long_voice_model_timeout_ms=%s", cfg.model_timeout_ms)
        if cfg.fallback_to_rule_on_timeout:
            return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)
        raise
    except Exception as e:
        logger.warning("long_voice_model_provider_exception: %s", e)
        if cfg.fallback_to_rule_on_validation_error:
            return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)
        raise

    if structured is None:
        return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)

    # 延迟导入，避免与 model_adapter 的环依赖
    from capabilities.voice.bridge.voice_long_input_model_adapter import enrich_structured_parse_system_b_group
    from capabilities.voice.bridge.voice_long_input_model_output_validator import validate_model_structured_output
    from capabilities.voice.bridge.voice_long_input_model_validation import sanitize_structured_parse_mappings
    from capabilities.voice.bridge.voice_long_input_structured_parse_builder import (
        build_voice_long_input_structured_parse_v1_1,
    )
    from capabilities.voice.bridge.voice_long_input_structured_to_parse_result import (
        structured_to_voice_long_input_parse_result,
    )

    # 先补 B 组（schema_version / input_meta 等）。
    structured = enrich_structured_parse_system_b_group(
        structured,
        raw_text=raw,
        context_resume_hint=session_hint,
    )

    # M3.2：在 validator 之前先做 mapping 白名单过滤（丢弃非法 system_mapping_candidate，不改写语义）。
    # 否则非法前缀（如 task_control.*）会先触发整表校验失败并整条回退规则链，sanitize 永远执行不到。
    structured = sanitize_structured_parse_mappings(structured)

    vr = validate_model_structured_output(structured, cfg=cfg)
    if not vr.ok:
        logger.warning("model_output_validation_failed: %s", vr.errors)
        return run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)

    rule_parse = run_long_input_task_planning_v1_rule_chain(text, request_id=rid, session_hint=session_hint)
    rule_struct = build_voice_long_input_structured_parse_v1_1(
        rule_parse,
        raw_text=raw,
        context_resume_hint=session_hint,
    )
    if rule_struct.feedback_candidate:
        structured.feedback_candidate = dict(rule_struct.feedback_candidate)

    return structured_to_voice_long_input_parse_result(
        structured,
        raw_text=raw,
        request_id=rid,
        session_hint=session_hint,
    )
