# -*- coding: utf-8 -*-
"""
M2.2 备路注入式验证：主路 qwen-plus 三种失败形态 → 接入层切 qwen-turbo，不与规则链 fallback 混淆。

注入（仅主 Provider）：
1. timeout：`parse_long_input` 抛出 `TimeoutError`（模拟 HTTP/读超时等接入层异常）
2. exception：抛出 `RuntimeError`（模拟任意非超时异常）
3. returns None：主路返回 `None`（模拟无法产出结构化 JSON）

通过标准（写死）：
- 每次注入后必须发生 plus → turbo（`backup_provider_used`、`selected_provider_model_id`、reason）
- 接管后 json_rate / val_rate / fallback_rate 在本单测口径下为 1.0 / 1.0 / 0.0
- validator 失败后不得再调备路：沿用 M1 用例，不在此重复
"""

from __future__ import annotations

from typing import Any, Callable, Dict
from unittest.mock import MagicMock

import pytest

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


class _BundleJsonTrace:
    """记录 bundle 层 parse_long_input 是否返回非 None（与 smoke/benchmark 口径一致）。"""

    def __init__(self, inner: Any) -> None:
        self._inner = inner
        self.last_json_ok = False

    def parse_long_input(self, text: str, *, session_hint: str = "", request_id: str = ""):
        r = self._inner.parse_long_input(text, session_hint=session_hint, request_id=request_id)
        self.last_json_ok = r is not None
        return r

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)


def _run_one_injection(
    *,
    primary: Any,
    request_id: str,
) -> Dict[str, Any]:
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod

    backup = MagicMock()
    backup.parse_long_input.return_value = _minimal_ok_result()
    raw = QwenLongVoicePrimaryBackupLongInputProvider(primary, backup)
    provider = _BundleJsonTrace(raw)

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val: Callable[..., Any] = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]
    try:
        res = run_long_input_task_planning_v1(
            "带我去医院",
            parse_config=_cfg(),
            model_provider=provider,
            request_id=request_id,
        )
    finally:
        vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    vr = _last_vr["vr"]
    validator_ok = bool(vr is not None and vr.ok)
    json_ok = bool(provider.last_json_ok)
    fallback = not (json_ok and validator_ok)

    return {
        "res": res,
        "raw": raw,
        "backup": backup,
        "json_ok": json_ok,
        "validator_ok": validator_ok,
        "fallback": fallback,
    }


@pytest.mark.parametrize(
    "inject_name,primary_factory,expected_reason_substr",
    [
        (
            "timeout",
            lambda p: setattr(p, "parse_long_input", MagicMock(side_effect=TimeoutError("injected_http_read_timeout"))),
            "primary_exception:TimeoutError",
        ),
        (
            "exception",
            lambda p: setattr(p, "parse_long_input", MagicMock(side_effect=RuntimeError("injected_network"))),
            "primary_exception:RuntimeError",
        ),
        (
            "returns_none",
            lambda p: setattr(p, "parse_long_input", MagicMock(return_value=None)),
            "primary_returned_none",
        ),
    ],
)
def test_m2_2_injection_primary_failure_turbo_takes_over(
    inject_name: str,
    primary_factory: Callable[[MagicMock], None],
    expected_reason_substr: str,
) -> None:
    primary = MagicMock()
    primary_factory(primary)

    out = _run_one_injection(primary=primary, request_id=f"m22_{inject_name}")

    raw: QwenLongVoicePrimaryBackupLongInputProvider = out["raw"]
    backup: MagicMock = out["backup"]

    backup.parse_long_input.assert_called_once()
    assert raw.backup_provider_used is True
    assert raw.selected_provider_model_id == raw.backup_model_id
    assert expected_reason_substr in raw.provider_switch_reason

    assert out["json_ok"] is True
    assert out["validator_ok"] is True
    assert out["fallback"] is False

    res = out["res"]
    assert "model_chain" in (res.notes or ""), "应为模型链成功路径，不得误判为纯规则链兜底"


def test_m2_2_three_injections_aggregate_rates() -> None:
    """单轮三种注入各跑一次，聚合 json/val/fallback 均为理想值（M2.2 验收口径）。"""
    rows = []
    for name, factory, substr in [
        ("timeout", lambda p: setattr(p, "parse_long_input", MagicMock(side_effect=TimeoutError("t"))), "TimeoutError"),
        ("exception", lambda p: setattr(p, "parse_long_input", MagicMock(side_effect=ValueError("e"))), "ValueError"),
        ("none", lambda p: setattr(p, "parse_long_input", MagicMock(return_value=None)), "primary_returned_none"),
    ]:
        primary = MagicMock()
        factory(primary)
        out = _run_one_injection(primary=primary, request_id=f"m22_agg_{name}")
        raw = out["raw"]
        assert raw.backup_provider_used is True
        assert substr in raw.provider_switch_reason or "primary_exception" in raw.provider_switch_reason
        rows.append(out)

    assert all(r["json_ok"] for r in rows)
    assert all(r["validator_ok"] for r in rows)
    assert not any(r["fallback"] for r in rows)
    n = len(rows)
    assert sum(1 for r in rows if r["json_ok"]) / n == 1.0
    assert sum(1 for r in rows if r["validator_ok"]) / n == 1.0
    assert sum(1 for r in rows if r["fallback"]) / n == 0.0
