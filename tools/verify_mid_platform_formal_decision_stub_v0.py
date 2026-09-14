# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_payload(p: Dict[str, Any]) -> None:
    assert p.get("decision_attempted") is True, f"attempted_not_true:{p}"
    assert p.get("decision_scope") == "mid_platform_formal_decision_stub_v0", f"bad_scope:{p}"
    assert p.get("decision_result") == "hold_pending", f"bad_result:{p}"
    assert p.get("reason") == "missing_required_gate_inputs", f"bad_reason:{p}"


def main() -> None:
    from capabilities.mid_platform.runtime.mid_platform_formal_decision_stub_v0 import (
        evaluate_mid_platform_formal_decision_stub_v0,
    )

    # 场景 A：存在导航建议链与执行前承接 stub 相关输入（但仍应保守 hold_pending）
    applicable_a, p_a = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0={
            "routing_decision": "navigation_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "test",
        },
        mid_platform_dispatch_consumption_stub_v0={
            "consume_attempted": True,
            "consume_scope": "mid_platform_dispatch_consumption_stub_v0",
            "routing_decision_seen": "navigation_required",
            "consume_mode": "read_only",
        },
        destination_bound_v0={"destination_bound": True, "binding_key": "destination_id", "binding_value": "d1"},
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
        navigation_handoff_post_bound_execution_stub_v0={
            "execution_stub_attempted": True,
            "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
            "execution_state": "execution_pending",
            "reason": "missing_formal_mid_platform_dispatch",
        },
    )
    assert applicable_a is True and isinstance(p_a, dict)
    _assert_payload(p_a)

    # 场景 B：缺少关键输入（need_navigation_routing_v0 不存在 => relevant-only）
    applicable_b, p_b = evaluate_mid_platform_formal_decision_stub_v0(
        need_navigation_routing_v0=None,
        mid_platform_dispatch_consumption_stub_v0=None,
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
    )
    assert applicable_b is False and p_b is None

    print("VERIFY_MID_PLATFORM_FORMAL_DECISION_STUB_V0: ALL_OK")


if __name__ == "__main__":
    main()

