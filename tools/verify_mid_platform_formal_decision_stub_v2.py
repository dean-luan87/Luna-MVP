# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _routing_stub() -> Dict[str, Any]:
    return {"routing_scope": "need_navigation_routing_v0", "routing_suggestion": "navigation_uncertain"}


def _assert(
    payload: Optional[Dict[str, Any]],
    *,
    expected_result: str,
    expected_reason: str,
) -> None:
    assert isinstance(payload, dict), payload
    assert payload.get("decision_attempted") is True
    assert payload.get("decision_scope") == "mid_platform_formal_decision_stub_v0"
    assert payload.get("decision_result") == expected_result, payload
    assert payload.get("reason") == expected_reason, payload


def main() -> None:
    from capabilities.mid_platform.runtime.mid_platform_formal_decision_stub_v0 import (
        evaluate_mid_platform_formal_decision_stub_v0,
    )

    # 场景 A：安全阻断
    app_a, p_a = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_stub(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "safety_gate_v0_present": True,
            "safety_status": "blocked",
        },
        formal_decision_handoff_gates_v0=None,
        formal_decision_information_gates_v0=None,
    )
    assert app_a is True
    _assert(p_a, expected_result="block_execution", expected_reason="safety_gate_blocked")

    # 场景 B：任务无效阻断
    app_b, p_b = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_stub(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "task_validity_v0_present": True,
            "task_validity_status": "expired",
        },
        formal_decision_handoff_gates_v0=None,
        formal_decision_information_gates_v0=None,
    )
    assert app_b is True
    _assert(p_b, expected_result="block_execution", expected_reason="task_validity_blocked")

    # 场景 C：承接链不完整
    app_c, p_c = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_stub(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0=None,
        formal_decision_handoff_gates_v0={
            "handoff_gate_present": True,
            "handoff_gate_status": "incomplete",
            "consume_mode": "read_only",
        },
        formal_decision_information_gates_v0=None,
    )
    assert app_c is True
    _assert(p_c, expected_result="hold_pending", expected_reason="missing_handoff_gate_inputs")

    # 场景 D：信息不足
    app_d, p_d = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_stub(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0=None,
        formal_decision_handoff_gates_v0=None,
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "insufficient",
            "consume_mode": "read_only",
        },
    )
    assert app_d is True
    _assert(p_d, expected_result="hold_pending", expected_reason="insufficient_information")

    # 场景 E：其他缺输入（fallback）
    app_e, p_e = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_stub(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0=None,
        formal_decision_handoff_gates_v0=None,
        formal_decision_information_gates_v0=None,
    )
    assert app_e is True
    _assert(p_e, expected_result="hold_pending", expected_reason="missing_required_gate_inputs")

    print("VERIFY_MID_PLATFORM_FORMAL_DECISION_STUB_V2: ALL_OK")


if __name__ == "__main__":
    main()

