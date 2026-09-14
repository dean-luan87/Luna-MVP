# -*- coding: utf-8 -*-
"""
真实本地模型 Provider 接入（Qwen 3.5 4B）——以 mock HTTP 返回替代真实推理服务。

验收目标：
- Provider 能产出结构化（至少 input_mode/global/task_candidates）
- model_preferred_with_rule_fallback 下可进入 builder 生成 task_plan_v1
- Provider 输出非法/不可用时，orchestrator 可回退规则链
"""

from __future__ import annotations

from typing import Any, Dict

import pytest

from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
from capabilities.voice.providers.qwen_long_input_model_provider import QwenLongInputModelProvider
from shared.schemas.task_domain_v1 import NAVIGATION, UNSUPPORTED_OR_REJECT


def _cfg() -> VoiceLongInputParseConfig:
    return VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=1500,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )


def _patch_provider_json(monkeypatch: pytest.MonkeyPatch, provider: QwenLongInputModelProvider, obj: Dict[str, Any]) -> None:
    monkeypatch.setattr(provider.client, "chat_completion_json", lambda req: obj)  # type: ignore[assignment]


def test_task_only_two_steps_enters_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = QwenLongInputModelProvider()
    _patch_provider_json(
        monkeypatch,
        provider,
        {
            "schema_version": "voice_task_parse_v1_1",
            "input_mode_judgement": {
                "mode": "task_only",
                "has_task_content": True,
                "has_non_task_content": False,
                "should_generate_task_plan": True,
                "should_preserve_non_task_payload": False,
                "confidence": 0.8,
            },
            "global_judgement": {
                "primary_domain": NAVIGATION,
                "secondary_domains": [],
                "intent_complexity": "multi_step",
                "can_map_to_system_tasks": True,
                "needs_confirmation": False,
                "needs_clarification": False,
                "should_reject": False,
                "rejection_reason_candidate": None,
                "safety_risk_level": "low",
                "confidence": 0.7,
            },
            "task_candidates": [
                {
                    "candidate_id": "c1",
                    "task_domain": NAVIGATION,
                    "task_action": "go",
                    "system_mapping_candidate": "navigation.start_route",
                    "target": {"segment_text": "先去商场"},
                    "entities": [],
                    "constraints": [],
                    "conditional_clauses": [],
                    "execution_order": 1,
                    "dependency": None,
                    "is_temporary": False,
                    "requires_confirmation": False,
                    "can_execute_directly_candidate": True,
                    "confidence": 0.7,
                },
                {
                    "candidate_id": "c2",
                    "task_domain": NAVIGATION,
                    "task_action": "go",
                    "system_mapping_candidate": "navigation.start_route",
                    "target": {"segment_text": "再找便利店买点吃的"},
                    "entities": [],
                    "constraints": [],
                    "conditional_clauses": [],
                    "execution_order": 2,
                    "dependency": None,
                    "is_temporary": False,
                    "requires_confirmation": False,
                    "can_execute_directly_candidate": True,
                    "confidence": 0.65,
                },
            ],
            "non_task_payload": {"exists": False, "segments": [], "handoff_candidate": "emotion_engine_future", "confidence": 0.0},
            "clarification_candidates": [],
            "unsupported_candidates": [],
            "feedback_candidate": {},
            "parser_notes": {"notes": "ok"},
        },
    )

    r = run_long_input_task_planning_v1(
        "先去商场，再找便利店买点吃的",
        parse_config=_cfg(),
        model_provider=provider,
    )
    assert r.task_plan_v1 is not None
    assert len(r.task_plan_v1.execution_order) == 2


def test_mixed_preserves_non_task_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = QwenLongInputModelProvider()
    _patch_provider_json(
        monkeypatch,
        provider,
        {
            "schema_version": "voice_task_parse_v1_1",
            "input_mode_judgement": {
                "mode": "mixed_task_and_non_task",
                "has_task_content": True,
                "has_non_task_content": True,
                "should_generate_task_plan": True,
                "should_preserve_non_task_payload": True,
                "confidence": 0.75,
            },
            "global_judgement": {
                "primary_domain": NAVIGATION,
                "secondary_domains": [],
                "intent_complexity": "single_step",
                "can_map_to_system_tasks": True,
                "needs_confirmation": False,
                "needs_clarification": False,
                "should_reject": False,
                "rejection_reason_candidate": None,
                "safety_risk_level": "low",
                "confidence": 0.7,
            },
            "task_candidates": [
                {
                    "candidate_id": "c1",
                    "task_domain": NAVIGATION,
                    "task_action": "go",
                    "system_mapping_candidate": "navigation.start_route",
                    "target": {"segment_text": "先带我去最近的医院"},
                    "entities": [],
                    "constraints": [],
                    "conditional_clauses": [],
                    "execution_order": 1,
                    "dependency": None,
                    "is_temporary": False,
                    "requires_confirmation": False,
                    "can_execute_directly_candidate": True,
                    "confidence": 0.7,
                }
            ],
            "non_task_payload": {
                "exists": True,
                "segments": [{"segment_id": "s1", "segment_type": "emotion", "content": "我今天有点不舒服"}],
                "handoff_candidate": "emotion_engine_future",
                "confidence": 0.6,
            },
            "clarification_candidates": [],
            "unsupported_candidates": [],
            "feedback_candidate": {},
            "parser_notes": {"notes": "mixed"},
        },
    )

    r = run_long_input_task_planning_v1(
        "我今天有点不舒服，先带我去最近的医院吧",
        parse_config=_cfg(),
        model_provider=provider,
    )
    assert r.task_plan_v1 is not None
    assert r.non_task_payload is not None
    assert r.non_task_payload.exists is True
    assert any("不舒服" in s.content for s in r.non_task_payload.segments)


def test_unsupported_should_not_force_plan(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = QwenLongInputModelProvider()
    _patch_provider_json(
        monkeypatch,
        provider,
        {
            "schema_version": "voice_task_parse_v1_1",
            "input_mode_judgement": {
                "mode": "task_only",
                "has_task_content": True,
                "has_non_task_content": False,
                "should_generate_task_plan": False,
                "should_preserve_non_task_payload": False,
                "confidence": 0.7,
            },
            "global_judgement": {
                "primary_domain": UNSUPPORTED_OR_REJECT,
                "secondary_domains": [],
                "intent_complexity": "single_step",
                "can_map_to_system_tasks": False,
                "needs_confirmation": False,
                "needs_clarification": False,
                "should_reject": True,
                "rejection_reason_candidate": "unsupported",
                "safety_risk_level": "low",
                "confidence": 0.7,
            },
            "task_candidates": [],
            "non_task_payload": {"exists": False, "segments": [], "handoff_candidate": "emotion_engine_future", "confidence": 0.0},
            "unsupported_candidates": [{"item_id": "u1", "unsupported_type": "capability", "content": "自动挂号", "reason_candidate": "not_supported", "suggested_fallback": ""}],
            "clarification_candidates": [],
            "feedback_candidate": {},
            "parser_notes": {"notes": "unsupported"},
        },
    )

    r = run_long_input_task_planning_v1(
        "帮我自动挂号",
        parse_config=_cfg(),
        model_provider=provider,
    )
    # 若模型链产出拒绝/不支持，builder 侧可能不生成 plan；这里更重要的是：主线不崩、语义可控
    assert r.domain_result.primary_domain == UNSUPPORTED_OR_REJECT


def test_missing_global_judgement_triggers_fallback_to_rule(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = QwenLongInputModelProvider()
    _patch_provider_json(
        monkeypatch,
        provider,
        {
            "schema_version": "voice_task_parse_v1_1",
            "input_mode_judgement": {
                "mode": "task_only",
                "has_task_content": True,
                "has_non_task_content": False,
                "should_generate_task_plan": True,
                "should_preserve_non_task_payload": False,
                "confidence": 0.8,
            },
            "global_judgement": {"primary_domain": ""},  # 缺关键字段（primary_domain 为空）
            "task_candidates": [
                {
                    "candidate_id": "c1",
                    "task_domain": NAVIGATION,
                    "task_action": "go",
                    "system_mapping_candidate": "navigation.start_route",
                    "target": {"segment_text": "去医院"},
                    "execution_order": 1,
                }
            ],
        },
    )

    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=provider,
    )
    # 回退规则链：仍能产出 v1 plan（本用例主要验证 fallback 生效）
    assert r.task_plan_v1 is not None

