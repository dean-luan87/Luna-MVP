"""
Phase-Model-002 verifier

Validates Single Model Shadow Integration Implementation v0 against Model-001 constraints:
- Disabled by default
- Explicit enable required
- Input boundary applied (forbidden inputs blocked)
- Output contract applied (candidate schema v0; forbidden outputs blocked)
- Whitebox + replay records produced
- Disable + baseline fallback must work
- No execution authority / no side effects triggers
"""

from __future__ import annotations

import json
import os
import tempfile
import sys
from typing import Any, Dict, Mapping

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_integration.single_model_shadow_integration_v0 import (
    ShadowIntegrationInputV0,
    run_single_model_shadow_integration_v0,
)


def _fake_model_valid(_: Mapping[str, Any]) -> str:
    return json.dumps(
        {
            "output_kind": "candidate",
            "candidates": [
                {
                    "candidate_id": "c1",
                    "candidate_type": "nav_hint",
                    "summary": "keep straight",
                    "structured_fields": {"direction": "straight", "distance_m": 10},
                    "confidence": {"score": 0.7, "calibration_hint": "low"},
                    "reason_codes": ["OK"],
                    "evidence_pointers": ["p1"],
                    "safety_notes": [],
                }
            ],
        },
        ensure_ascii=False,
    )


def _fake_model_forbidden_execute(_: Mapping[str, Any]) -> str:
    return json.dumps({"output_kind": "execute_now", "command": "execute_now"}, ensure_ascii=False)


def _fake_model_forbidden_release(_: Mapping[str, Any]) -> str:
    return json.dumps({"output_kind": "open_release_window", "command": "open_release_window"}, ensure_ascii=False)


def _fake_model_malformed(_: Mapping[str, Any]) -> str:
    return "{not-json"


def _fake_model_timeout(_: Mapping[str, Any]) -> str:
    raise TimeoutError("simulated")


def _fake_model_exception(_: Mapping[str, Any]) -> str:
    raise RuntimeError("simulated")


def _mk_dirs() -> Dict[str, str]:
    d = tempfile.mkdtemp(prefix="m002_")
    return {"whitebox_dir": os.path.join(d, "whitebox"), "replay_dir": os.path.join(d, "replay")}


def _assert_common(out: Dict[str, Any]) -> None:
    assert out["model_name"] == "fake"
    assert out["model_disabled_fallback_available"] is True
    assert out["no_execution_side_effects"] is True or out.get("no_execution_side_effects") is True


def test_A_model_disabled_by_default() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=False,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["model_enabled_seen"] is False
    assert out["model_invoked"] is False
    assert out["baseline_fallback_used"] is True
    assert out["written_to_whitebox"] is True
    assert out["replay_record_ready"] is True


def test_B_explicit_enable_shadow_model() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["model_enabled_seen"] is True
    assert out["model_invoked"] is True
    assert out["candidate_generated"] is True
    assert out["candidate_schema_valid"] is True
    assert out["written_to_whitebox"] is True
    assert out["replay_record_ready"] is True


def test_C_forbidden_input_probe() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x", "side_effects_released": True, "grant_control": True},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["input_boundary_applied"] is True


def test_D_valid_candidate_output() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["candidate_schema_valid"] is True


def test_E_forbidden_output_probe_execute() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_forbidden_execute,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["forbidden_output_blocked"] is True
    assert out["baseline_fallback_used"] is True


def test_F_forbidden_output_probe_release() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_forbidden_release,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["forbidden_output_blocked"] is True
    assert out["baseline_fallback_used"] is True


def test_G_malformed_json_output() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_malformed,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["baseline_fallback_used"] is True
    assert out["candidate_schema_valid"] is False


def test_H_model_timeout() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_timeout,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["baseline_fallback_used"] is True
    assert out["model_invoked"] is True


def test_I_model_exception() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_exception,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["baseline_fallback_used"] is True
    assert out["model_invoked"] is True


def test_J_disable_switch_runtime() -> None:
    dirs = _mk_dirs()
    out_on = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out_on)
    assert out_on["model_enabled_seen"] is True
    out_off = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            disable_switch=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out_off)
    assert out_off["model_enabled_seen"] is False
    assert out_off["baseline_fallback_used"] is True


def test_K_replay_record_check() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["replay_record_ready"] is True
    assert os.path.exists(out["replay_path"])


def test_L_whitebox_trace_check() -> None:
    dirs = _mk_dirs()
    out = run_single_model_shadow_integration_v0(
        ShadowIntegrationInputV0(
            explicit_model_integration_enable_v0=True,
            model_name="fake",
            model_call=_fake_model_valid,
            restricted_context_summary={"scene": "x"},
            whitebox_dir=dirs["whitebox_dir"],
            replay_dir=dirs["replay_dir"],
        )
    )
    _assert_common(out)
    assert out["written_to_whitebox"] is True
    assert os.path.exists(out["whitebox_path"])


def main() -> None:
    tests = [
        test_A_model_disabled_by_default,
        test_B_explicit_enable_shadow_model,
        test_C_forbidden_input_probe,
        test_D_valid_candidate_output,
        test_E_forbidden_output_probe_execute,
        test_F_forbidden_output_probe_release,
        test_G_malformed_json_output,
        test_H_model_timeout,
        test_I_model_exception,
        test_J_disable_switch_runtime,
        test_K_replay_record_check,
        test_L_whitebox_trace_check,
    ]
    for t in tests:
        t()
    print("OK: Phase-Model-002 single model shadow integration verifier v0")


if __name__ == "__main__":
    main()

