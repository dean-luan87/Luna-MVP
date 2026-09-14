# -*- coding: utf-8 -*-
"""长语音模型接入适配层 v1：双通道与规则兜底。"""

from __future__ import annotations

from capabilities.voice.bridge.voice_long_input_model_adapter import (
    DualChannelParseOutcome,
    RuleFallbackLongVoiceModelAdapter,
    VoiceLongInputModelIntegrationConfig,
    enrich_structured_parse_system_b_group,
    run_structured_long_input_parse_v1_1_dual_channel,
)
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1,
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    VoiceLongInputStructuredParseResult,
)


def test_default_rule_only_channel() -> None:
    cfg = VoiceLongInputModelIntegrationConfig(use_model_for_structured_parse=False)
    out = run_structured_long_input_parse_v1_1_dual_channel(
        "先去商场，再找便利店买点吃的",
        config=cfg,
        adapter=RuleFallbackLongVoiceModelAdapter(),
    )
    assert isinstance(out, DualChannelParseOutcome)
    assert out.used_model is False
    assert out.fallback_reason == "rule_only"
    assert out.structured.schema_version == SCHEMA_VERSION_VOICE_TASK_PARSE_V1_1
    assert len(out.structured.task_candidates) >= 1


def test_use_model_false_behaves_like_rule() -> None:
    cfg = VoiceLongInputModelIntegrationConfig(use_model_for_structured_parse=False)
    out = run_structured_long_input_parse_v1_1_dual_channel(
        "带我去医院",
        config=cfg,
        adapter=RuleFallbackLongVoiceModelAdapter(),
    )
    assert out.used_model is False
    assert out.fallback_reason == "rule_only"


def test_use_model_true_but_adapter_returns_none() -> None:
    cfg = VoiceLongInputModelIntegrationConfig(use_model_for_structured_parse=True)
    out = run_structured_long_input_parse_v1_1_dual_channel(
        "带我去医院",
        config=cfg,
        adapter=RuleFallbackLongVoiceModelAdapter(),
    )
    assert out.used_model is False
    assert out.fallback_reason == "model_unavailable"


def test_invalid_model_output_falls_back_to_rules() -> None:
    class BadAdapter:
        def parse_to_structured(self, text: str, **kwargs):
            # 缺关键字段 → 校验失败 → 规则链
            return VoiceLongInputStructuredParseResult()

    cfg = VoiceLongInputModelIntegrationConfig(use_model_for_structured_parse=True)
    out = run_structured_long_input_parse_v1_1_dual_channel(
        "带我去医院",
        config=cfg,
        adapter=BadAdapter(),
    )
    assert out.used_model is False
    assert "model_invalid" in out.fallback_reason


def test_enrich_system_b_sets_input_meta() -> None:
    s = VoiceLongInputStructuredParseResult(
        input_mode_judgement=InputModeJudgementStructuredV1_1(mode="task_only", confidence=0.9),
        global_judgement=GlobalJudgementStructuredV1_1(primary_domain="navigation", confidence=0.9),
    )
    s = enrich_structured_parse_system_b_group(
        s,
        raw_text="测试",
        context_resume_hint="hint",
    )
    assert s.input_meta.raw_text == "测试"
    assert s.input_meta.context_resume_hint == "hint"
    assert s.knowledge_collaboration.history_used is False


def test_illegal_mapping_filtered() -> None:
    from capabilities.voice.bridge.voice_long_input_model_validation import filter_task_candidates_by_mapping
    from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import TaskCandidateV1_1

    cands = [
        TaskCandidateV1_1(
            candidate_id="tc_001",
            task_domain="navigation",
            task_action="start",
            system_mapping_candidate="navigation.start",
            execution_order=1,
        ),
        TaskCandidateV1_1(
            candidate_id="tc_002",
            task_domain="x",
            task_action="x",
            system_mapping_candidate="malicious.arbitrary",
            execution_order=2,
        ),
    ]
    kept, rep = filter_task_candidates_by_mapping(cands)
    assert len(kept) == 1
    assert rep.dropped_candidates
