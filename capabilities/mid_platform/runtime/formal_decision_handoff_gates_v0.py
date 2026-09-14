# -*- coding: utf-8 -*-
"""
Formal Decision Handoff Gates v0 (read-only gate-input wiring).

Builds a minimal gate input object from existing handoff-chain observations:
- destination_bound_v0
- navigation_handoff_consume_bound_v0
- navigation_handoff_post_bound_execution_stub_v0

Hard boundaries:
- Does NOT change formal decision behavior.
- Does NOT fabricate missing items; does NOT add time/space anchors.
- Does NOT infer allow_progress; only marks ready_candidate vs incomplete.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def _present_bound(x: Any) -> bool:
    return isinstance(x, dict) and bool(x) and (x.get("destination_bound") is True)


def _present_consume_bound(x: Any) -> bool:
    return isinstance(x, dict) and bool(x) and (x.get("bound_consumed") is True)


def _present_post_bound_stub(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if str(x.get("execution_scope") or "") != "navigation_handoff_post_bound_execution_stub_v0":
        return False
    st = str(x.get("execution_state") or "").strip()
    return st in ("execution_ready", "execution_blocked", "execution_pending")


def build_formal_decision_handoff_gates_v0(
    *,
    destination_bound_v0: Any,
    navigation_handoff_consume_bound_v0: Any,
    navigation_handoff_post_bound_execution_stub_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, gate_input_dict).

    relevant-only:
    - If none of the three inputs are present => (False, None)
    """
    bound_present = _present_bound(destination_bound_v0)
    consume_bound_present = _present_consume_bound(navigation_handoff_consume_bound_v0)
    post_stub_present = _present_post_bound_stub(navigation_handoff_post_bound_execution_stub_v0)

    if not (bound_present or consume_bound_present or post_stub_present):
        return False, None

    if bound_present and consume_bound_present and post_stub_present:
        status = "ready_candidate"
    else:
        status = "incomplete"

    return True, {
        "handoff_gate_present": True,
        "bound_present": bool(bound_present),
        "consume_bound_present": bool(consume_bound_present),
        "post_bound_stub_present": bool(post_stub_present),
        "handoff_gate_status": str(status),
        "consume_mode": "read_only",
    }

