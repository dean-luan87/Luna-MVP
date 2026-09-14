# -*- coding: utf-8 -*-
"""长语音结构化总 Schema v1.1 与规则 builder。"""

from __future__ import annotations

from capabilities.voice.bridge.voice_long_input_structured_parse_builder import (
    build_voice_long_input_structured_parse_v1_1,
)
from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
)


def test_schema_keys_and_version() -> None:
    r = run_long_input_task_planning_v1("先去商场，再找便利店买点吃的")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert d["schema_version"] == SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1
    keys = set(d.keys())
    assert keys == {
        "schema_version",
        "input_meta",
        "input_mode_judgement",
        "global_judgement",
        "task_candidates",
        "non_task_payload",
        "knowledge_collaboration",
        "task_optimization",
        "clarification_candidates",
        "unsupported_candidates",
        "feedback_candidate",
        "parser_notes",
    }


def test_task_only_has_candidates_and_feedback() -> None:
    r = run_long_input_task_planning_v1("先去商场，再找便利店买点吃的")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert d["input_mode_judgement"]["mode"] == "task_only"
    assert len(d["task_candidates"]) >= 1
    assert d["non_task_payload"]["exists"] is False
    assert d["feedback_candidate"].get("feedback_mode") == "task_understood_and_ready"


def test_mixed_non_task_and_feedback() -> None:
    r = run_long_input_task_planning_v1("我今天有点不舒服，你先带我去最近的医院吧")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert d["input_mode_judgement"]["mode"] == "mixed_task_and_non_task"
    assert d["non_task_payload"]["exists"] is True
    assert d["non_task_payload"]["segments"][0]["segment_id"] == "nt_001"
    assert d["feedback_candidate"].get("feedback_mode") == "mixed_input_acknowledged"


def test_non_task_only_empty_task_candidates() -> None:
    r = run_long_input_task_planning_v1("我今天真的很烦，感觉什么都不顺。")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert d["input_mode_judgement"]["mode"] == "non_task_only"
    assert d["task_candidates"] == []
    assert d["feedback_candidate"].get("feedback_mode") == "non_task_preserved_for_future"


def test_unsupported_populates_unsupported_candidates() -> None:
    r = run_long_input_task_planning_v1("替我给别人发消息")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert len(d["unsupported_candidates"]) == 1
    assert d["unsupported_candidates"][0]["item_id"] == "uc_001"


def test_knowledge_and_optimization_placeholders() -> None:
    r = run_long_input_task_planning_v1("带我去医院")
    s = build_voice_long_input_structured_parse_v1_1(r)
    d = s.to_dict()
    assert d["knowledge_collaboration"]["history_used"] is False
    assert d["task_optimization"]["optimization_applied"] is False


def test_dict_to_structured_parse_unwraps_qwen36_style_nested_root() -> None:
    """qwen3.6-plus 等模型偶发将整表包在 voice_task_parse_v1_1 键下，应解包后再解析。"""
    from capabilities.voice.bridge.voice_long_input_model_output_validator import validate_model_structured_output
    from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
    from capabilities.voice.providers.qwen_long_input_model_provider import dict_to_structured_parse

    cfg = VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=120_000,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )
    wrapped = {
        SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1: {
            "input_mode_judgement": {
                "mode": "task_only",
                "has_task_content": True,
                "has_non_task_content": False,
            },
            "global_judgement": {
                "primary_domain": "navigation",
                "should_generate_task_plan": True,
                "needs_clarification": False,
            },
            "task_candidates": [
                {
                    "candidate_id": "c1",
                    "system_mapping_candidate": "navigation.go_to_poi",
                    "target": {"segment_text": "回家"},
                    "entities": [],
                    "constraints": [],
                    "conditional_clauses": [],
                }
            ],
            "non_task_payload": {"exists": False, "segments": []},
            "clarification_candidates": [],
            "unsupported_candidates": [],
            "parser_notes": {"notes": ""},
        }
    }
    s = dict_to_structured_parse(wrapped)
    vr = validate_model_structured_output(s, cfg=cfg)
    assert vr.ok is True
