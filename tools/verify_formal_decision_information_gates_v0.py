# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _assert_gate(g: Dict[str, Any], expected_status: str) -> None:
    assert g.get("info_gate_present") is True
    assert g.get("consume_mode") == "read_only"
    assert g.get("info_sufficiency_status") == expected_status, g


def main() -> None:
    from capabilities.mid_platform.runtime.formal_decision_information_gates_v0 import (
        build_formal_decision_information_gates_v0,
    )

    # 1) task context missing => insufficient
    app1, g1 = build_formal_decision_information_gates_v0(
        task_action="",
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
    )
    assert app1 is False and g1 is None

    # 2) start_navigation but missing required action inputs (bound) => insufficient
    app2, g2 = build_formal_decision_information_gates_v0(
        task_action="start_navigation",
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
    )
    assert app2 is True and isinstance(g2, dict)
    _assert_gate(g2, "insufficient")
    assert g2.get("task_context_present") is True
    assert g2.get("required_action_inputs_present") is False

    # 3) start_navigation with bound + consume bound + post stub => ready_candidate
    app3, g3 = build_formal_decision_information_gates_v0(
        task_action="start_navigation",
        destination_bound_v0={"destination_bound": True},
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
        navigation_handoff_post_bound_execution_stub_v0={
            "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
            "execution_state": "execution_pending",
        },
    )
    assert app3 is True and isinstance(g3, dict)
    _assert_gate(g3, "ready_candidate")
    assert g3.get("required_action_inputs_present") is True
    assert g3.get("candidate_inputs_present") is True

    print("VERIFY_FORMAL_DECISION_INFORMATION_GATES_V0: ALL_OK")


if __name__ == "__main__":
    main()

