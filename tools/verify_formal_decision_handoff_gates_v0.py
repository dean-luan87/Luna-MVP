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
    assert g.get("handoff_gate_present") is True
    assert g.get("consume_mode") == "read_only"
    assert g.get("handoff_gate_status") == expected_status, g


def main() -> None:
    from capabilities.mid_platform.runtime.formal_decision_handoff_gates_v0 import (
        build_formal_decision_handoff_gates_v0,
    )

    # incomplete when only one present
    app1, g1 = build_formal_decision_handoff_gates_v0(
        destination_bound_v0={"destination_bound": True},
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
    )
    assert app1 is True and isinstance(g1, dict)
    _assert_gate(g1, "incomplete")
    assert g1.get("bound_present") is True
    assert g1.get("consume_bound_present") is False
    assert g1.get("post_bound_stub_present") is False

    # ready_candidate when all three present
    app2, g2 = build_formal_decision_handoff_gates_v0(
        destination_bound_v0={"destination_bound": True, "binding_key": "k", "binding_value": "v"},
        navigation_handoff_consume_bound_v0={"bound_consumed": True},
        navigation_handoff_post_bound_execution_stub_v0={
            "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
            "execution_state": "execution_pending",
        },
    )
    assert app2 is True and isinstance(g2, dict)
    _assert_gate(g2, "ready_candidate")
    assert g2.get("bound_present") is True
    assert g2.get("consume_bound_present") is True
    assert g2.get("post_bound_stub_present") is True

    # relevant-only when none present
    app3, g3 = build_formal_decision_handoff_gates_v0(
        destination_bound_v0=None,
        navigation_handoff_consume_bound_v0=None,
        navigation_handoff_post_bound_execution_stub_v0=None,
    )
    assert app3 is False and g3 is None

    print("VERIFY_FORMAL_DECISION_HANDOFF_GATES_V0: ALL_OK")


if __name__ == "__main__":
    main()

