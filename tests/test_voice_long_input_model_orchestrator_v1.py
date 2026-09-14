# -*- coding: utf-8 -*-
"""
长语音解析 orchestrator：规则链 / 模型链双通道与降级（v1 验收场景）。
"""

from __future__ import annotations

import time

from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
from capabilities.voice.interfaces.voice_long_input_model_provider import MockVoiceLongInputModelProvider
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    TaskCandidateV1_1,
    VoiceLongInputStructuredParseResult,
)
from shared.schemas.task_domain_v1 import NAVIGATION


def _cfg(**kwargs: object) -> VoiceLongInputParseConfig:
    d: dict[str, object] = {
        "parse_mode": "model_preferred_with_rule_fallback",
        "enable_model_adapter": True,
        "model_timeout_ms": 8000,
        "fallback_to_rule_on_timeout": True,
        "fallback_to_rule_on_validation_error": True,
        "max_task_candidates": 3,
        "allow_non_task_payload": True,
    }
    d.update(kwargs)
    return VoiceLongInputParseConfig(**d)  # type: ignore[arg-type]


def test_scenario_rule_only_still_emits_task_plan() -> None:
    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=VoiceLongInputParseConfig(parse_mode="rule_only"),
    )
    assert r.task_plan_v1 is not None
    assert r.domain_result.primary_domain == NAVIGATION


def test_scenario_model_preferred_mock_produces_task_plan() -> None:
    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=MockVoiceLongInputModelProvider(),
    )
    assert r.task_plan_v1 is not None
    assert r.task_plan_v1.plan_version == "v1"


def test_scenario_illegal_primary_domain_fallback_rule() -> None:
    class BadDomain:
        def parse_long_input(self, text: str, **kwargs: object) -> VoiceLongInputStructuredParseResult:
            return VoiceLongInputStructuredParseResult(
                input_mode_judgement=InputModeJudgementStructuredV1_1(
                    mode="task_only",
                    has_task_content=True,
                    has_non_task_content=False,
                    should_generate_task_plan=True,
                    should_preserve_non_task_payload=False,
                    confidence=0.9,
                ),
                global_judgement=GlobalJudgementStructuredV1_1(
                    primary_domain="not_a_valid_v1_domain",
                    secondary_domains=[],
                    can_map_to_system_tasks=True,
                    needs_clarification=False,
                    should_reject=False,
                    confidence=0.8,
                ),
                task_candidates=[
                    TaskCandidateV1_1(
                        candidate_id="c1",
                        task_domain=NAVIGATION,
                        task_action="go",
                        system_mapping_candidate="navigation.start_route",
                        execution_order=1,
                    )
                ],
            )

    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=BadDomain(),
    )
    assert r.task_plan_v1 is not None
    assert r.domain_result.primary_domain == NAVIGATION


def test_scenario_illegal_system_mapping_dropped_before_validate() -> None:
    """M3.2：非法 system_mapping 在 validator 前被丢弃；不再整表退回规则链。"""

    class BadMapping:
        def parse_long_input(self, text: str, **kwargs: object) -> VoiceLongInputStructuredParseResult:
            return VoiceLongInputStructuredParseResult(
                input_mode_judgement=InputModeJudgementStructuredV1_1(
                    mode="task_only",
                    has_task_content=True,
                    has_non_task_content=False,
                    should_generate_task_plan=True,
                    should_preserve_non_task_payload=False,
                    confidence=0.9,
                ),
                global_judgement=GlobalJudgementStructuredV1_1(
                    primary_domain=NAVIGATION,
                    secondary_domains=[],
                    can_map_to_system_tasks=True,
                    needs_clarification=False,
                    should_reject=False,
                    confidence=0.8,
                ),
                task_candidates=[
                    TaskCandidateV1_1(
                        candidate_id="c1",
                        task_domain=NAVIGATION,
                        task_action="go",
                        system_mapping_candidate="invalid_prefix.not_allowed",
                        execution_order=1,
                    )
                ],
            )

    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=BadMapping(),
    )
    assert r.domain_result.primary_domain == NAVIGATION
    # 候选被丢光 → 模型链收口为「无候选」：无 task_plan、需澄清（见 structured_to_voice_long_input_parse_result）
    assert r.task_plan_v1 is None
    assert r.clarification_needed is True
    assert "no_candidates" in (r.notes or "")


def test_scenario_model_timeout_fallback_rule() -> None:
    class Slow:
        def parse_long_input(self, text: str, **kwargs: object) -> VoiceLongInputStructuredParseResult:
            time.sleep(1.0)
            return VoiceLongInputStructuredParseResult()

    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(model_timeout_ms=80),
        model_provider=Slow(),
    )
    assert r.task_plan_v1 is not None
    assert r.domain_result.primary_domain == NAVIGATION


def test_scenario_missing_input_mode_judgement_fallback_rule() -> None:
    class MissingMode:
        def parse_long_input(self, text: str, **kwargs: object) -> VoiceLongInputStructuredParseResult:
            # 关键字段缺失（mode 为空）→ validator 应判定缺失并回退规则链
            return VoiceLongInputStructuredParseResult(
                input_mode_judgement=InputModeJudgementStructuredV1_1(mode=""),
                global_judgement=GlobalJudgementStructuredV1_1(
                    primary_domain=NAVIGATION,
                    secondary_domains=[],
                    can_map_to_system_tasks=True,
                    needs_clarification=False,
                    should_reject=False,
                    confidence=0.8,
                ),
                task_candidates=[
                    TaskCandidateV1_1(
                        candidate_id="c1",
                        task_domain=NAVIGATION,
                        task_action="go",
                        system_mapping_candidate="navigation.start_route",
                        execution_order=1,
                    )
                ],
            )

    r = run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=MissingMode(),
    )
    assert r.task_plan_v1 is not None
    assert r.domain_result.primary_domain == NAVIGATION


def test_scenario_mixed_input_non_task_preserved_with_mock_chain() -> None:
    text = "我今天有点不舒服，你先带我去最近的医院吧"
    r = run_long_input_task_planning_v1(
        text,
        parse_config=_cfg(),
        model_provider=MockVoiceLongInputModelProvider(),
    )
    assert r.input_mode_judgement is not None
    assert r.input_mode_judgement.mode == "mixed_task_and_non_task"
    assert r.non_task_payload is not None
    assert r.non_task_payload.exists is True
    assert r.task_plan_v1 is not None
