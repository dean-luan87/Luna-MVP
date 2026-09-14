# -*- coding: utf-8 -*-
"""接入层主备 Provider（M1）：主 qwen-plus → 备 qwen-turbo，与 orchestrator/validator 边界。"""

from __future__ import annotations

from unittest.mock import MagicMock

from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.config.voice_long_input_parse_config import VoiceLongInputParseConfig
from capabilities.voice.providers.qwen_long_voice_primary_backup_provider import (
    QwenLongVoicePrimaryBackupLongInputProvider,
)
from capabilities.voice.schemas.voice_long_input_structured_parse_v1_1 import (
    GlobalJudgementStructuredV1_1,
    InputModeJudgementStructuredV1_1,
    TaskCandidateV1_1,
    VoiceLongInputStructuredParseResult,
)
from shared.schemas.task_domain_v1 import NAVIGATION


def _cfg() -> VoiceLongInputParseConfig:
    return VoiceLongInputParseConfig(
        parse_mode="model_preferred_with_rule_fallback",
        enable_model_adapter=True,
        model_timeout_ms=8000,
        fallback_to_rule_on_timeout=True,
        fallback_to_rule_on_validation_error=True,
        max_task_candidates=3,
        allow_non_task_payload=True,
    )


def _minimal_ok_result() -> VoiceLongInputStructuredParseResult:
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
                system_mapping_candidate="navigation.go_to_poi",
                execution_order=1,
            )
        ],
    )


def test_primary_success_backup_not_called() -> None:
    primary = MagicMock()
    primary.parse_long_input.return_value = _minimal_ok_result()
    backup = MagicMock()
    w = QwenLongVoicePrimaryBackupLongInputProvider(primary, backup)
    r = w.parse_long_input("带我去医院", session_hint="", request_id="t1")
    assert r is not None
    backup.parse_long_input.assert_not_called()
    assert w.backup_provider_used is False
    assert w.selected_provider_model_id == w.primary_model_id


def test_primary_none_invokes_backup() -> None:
    primary = MagicMock()
    primary.parse_long_input.return_value = None
    backup = MagicMock()
    backup.parse_long_input.return_value = _minimal_ok_result()
    w = QwenLongVoicePrimaryBackupLongInputProvider(primary, backup)
    r = w.parse_long_input("带我去医院", session_hint="", request_id="t2")
    assert r is not None
    backup.parse_long_input.assert_called_once()
    assert w.backup_provider_used is True
    assert w.selected_provider_model_id == w.backup_model_id
    assert "primary_returned_none" in w.provider_switch_reason


def test_primary_exception_invokes_backup() -> None:
    primary = MagicMock()
    primary.parse_long_input.side_effect = RuntimeError("network")

    backup = MagicMock()
    backup.parse_long_input.return_value = _minimal_ok_result()
    w = QwenLongVoicePrimaryBackupLongInputProvider(primary, backup)
    r = w.parse_long_input("带我去医院", session_hint="", request_id="t3")
    assert r is not None
    backup.parse_long_input.assert_called_once()
    assert w.backup_provider_used is True
    assert "primary_exception" in w.provider_switch_reason


def test_validator_failure_does_not_invoke_backup() -> None:
    """主选已返回结构化结果（非 None）；validator 失败走规则链，不得再调 turbo。"""

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

    backup = MagicMock()
    backup.parse_long_input = MagicMock(return_value=_minimal_ok_result())
    w = QwenLongVoicePrimaryBackupLongInputProvider(BadDomain(), backup)
    run_long_input_task_planning_v1(
        "带我去医院",
        parse_config=_cfg(),
        model_provider=w,
        request_id="t4",
    )
    backup.parse_long_input.assert_not_called()
    assert w.backup_provider_used is False
