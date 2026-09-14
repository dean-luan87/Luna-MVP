# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _routing_required() -> Dict[str, Any]:
    return {"routing_scope": "need_navigation_routing_v0", "routing_suggestion": "navigation_required"}


def _routing_uncertain() -> Dict[str, Any]:
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

    # 场景 A：全部前提满足 => allow_progress
    app_a, p_a = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_required(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0={"destination_bound": True},
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
        navigation_handoff_post_bound_execution_stub_v0={
            "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
            "execution_state": "execution_pending",
        },
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "safety_gate_v0_present": True,
            "safety_status": "safe",
            "safety_preempt_active": False,
            "task_validity_v0_present": True,
            "task_validity_status": "active",
        },
        formal_decision_handoff_gates_v0={
            "handoff_gate_present": True,
            "handoff_gate_status": "ready_candidate",
            "consume_mode": "read_only",
        },
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "ready_candidate",
            "consume_mode": "read_only",
        },
    )
    assert app_a is True
    _assert(p_a, expected_result="allow_progress", expected_reason="all_minimum_preconditions_satisfied")

    # 场景 B：安全阻断 => block_execution / safety_gate_blocked（优先级最高）
    app_b, p_b = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_required(),
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
        formal_decision_handoff_gates_v0={
            "handoff_gate_present": True,
            "handoff_gate_status": "ready_candidate",
            "consume_mode": "read_only",
        },
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "ready_candidate",
            "consume_mode": "read_only",
        },
    )
    assert app_b is True
    _assert(p_b, expected_result="block_execution", expected_reason="safety_gate_blocked")

    # 场景 C：承接链不完整 => hold_pending / missing_handoff_gate_inputs
    app_c, p_c = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_required(),
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
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "ready_candidate",
            "consume_mode": "read_only",
        },
    )
    assert app_c is True
    _assert(p_c, expected_result="hold_pending", expected_reason="missing_handoff_gate_inputs")

    # 场景 D：信息不足 => hold_pending / insufficient_information
    app_d, p_d = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_required(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0=None,
        formal_decision_handoff_gates_v0={
            "handoff_gate_present": True,
            "handoff_gate_status": "ready_candidate",
            "consume_mode": "read_only",
        },
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "insufficient",
            "consume_mode": "read_only",
        },
    )
    assert app_d is True
    _assert(p_d, expected_result="hold_pending", expected_reason="insufficient_information")

    # Extra guard: branch consistency placeholder must be narrow (routing not required => no allow_progress)
    app_e, p_e = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=_routing_uncertain(),
        mid_platform_dispatch_consumption_stub_v0={},
        destination_bound_v0={"destination_bound": True},
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
        navigation_handoff_post_bound_execution_stub_v0={
            "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
            "execution_state": "execution_pending",
        },
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "safety_gate_v0_present": True,
            "safety_status": "safe",
            "safety_preempt_active": False,
            "task_validity_v0_present": True,
            "task_validity_status": "active",
        },
        formal_decision_handoff_gates_v0={
            "handoff_gate_present": True,
            "handoff_gate_status": "ready_candidate",
            "consume_mode": "read_only",
        },
        formal_decision_information_gates_v0={
            "info_gate_present": True,
            "info_sufficiency_status": "ready_candidate",
            "consume_mode": "read_only",
        },
    )
    assert app_e is True
    assert isinstance(p_e, dict)
    assert p_e.get("decision_result") != "allow_progress"

    print("VERIFY_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT: ALL_OK")


if __name__ == "__main__":
    main()

