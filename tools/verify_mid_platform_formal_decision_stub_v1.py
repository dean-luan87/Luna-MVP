# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_result(p: Dict[str, Any], expected: str, expected_reason: str) -> None:
    assert p.get("decision_attempted") is True
    assert p.get("decision_scope") == "mid_platform_formal_decision_stub_v0"
    assert p.get("decision_result") == expected, p
    assert p.get("reason") == expected_reason, p


def main() -> None:
    from capabilities.mid_platform.runtime.mid_platform_formal_decision_stub_v0 import (
        evaluate_mid_platform_formal_decision_stub_v0,
    )

    base_need = {"routing_decision": "navigation_required", "routing_scope": "need_navigation_routing_v0", "reason": "t"}

    # 场景 A：安全阻断
    app_a, p_a = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=base_need,
        mid_platform_dispatch_consumption_stub_v0=None,
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "safety_gate_v0_present": True,
            "safety_status": "blocked",
            "safety_preempt_active": True,
        },
    )
    assert app_a is True and isinstance(p_a, dict)
    _assert_result(p_a, "block_execution", "safety_gate_blocked")

    # 场景 B：任务无效阻断
    app_b, p_b = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=base_need,
        mid_platform_dispatch_consumption_stub_v0=None,
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "task_validity_v0_present": True,
            "task_validity_status": "expired",
        },
    )
    assert app_b is True and isinstance(p_b, dict)
    _assert_result(p_b, "block_execution", "task_validity_blocked")

    # 场景 C：门控输入存在但不够放行（guarded/active）
    app_c, p_c = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=base_need,
        mid_platform_dispatch_consumption_stub_v0=None,
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0={
            "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
            "consume_mode": "read_only",
            "safety_gate_v0_present": True,
            "safety_status": "guarded",
            "task_validity_v0_present": True,
            "task_validity_status": "active",
        },
    )
    assert app_c is True and isinstance(p_c, dict)
    _assert_result(p_c, "hold_pending", "missing_required_gate_inputs")

    # 场景 D：无门控输入
    app_d, p_d = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=base_need,
        mid_platform_dispatch_consumption_stub_v0=None,
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
        formal_decision_gate_inputs_v0=None,
    )
    assert app_d is True and isinstance(p_d, dict)
    _assert_result(p_d, "hold_pending", "missing_required_gate_inputs")

    print("VERIFY_MID_PLATFORM_FORMAL_DECISION_STUB_V1: ALL_OK")


if __name__ == "__main__":
    main()

