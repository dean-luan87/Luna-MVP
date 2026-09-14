# -*- coding: utf-8 -*-
"""
Mid-Platform Formal Decision Stub v0 (read-only).

Hard boundaries:
- Not a real decision maker; does NOT switch branches or trigger execution.
- Does NOT fabricate missing gate inputs (safety/task validity/formal dispatch).
- Does NOT add time/space anchors; does NOT depend on maps.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "mid_platform_formal_decision_stub_v0"


def evaluate_mid_platform_formal_decision_stub_v0(
    *,
    need_navigation_routing_v0: Any,
    mid_platform_dispatch_consumption_stub_v0: Any,
    destination_bound_v0: Any,
    navigation_handoff_consume_bound_v0: Any,
    navigation_handoff_post_bound_execution_stub_v0: Any,
    formal_decision_gate_inputs_v0: Any = None,
    formal_decision_handoff_gates_v0: Any = None,
    formal_decision_information_gates_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - requires need_navigation_routing_v0 to exist (as the minimal stable input signal)
    """
    if not isinstance(need_navigation_routing_v0, dict) or not need_navigation_routing_v0:
        return False, None
    if str(need_navigation_routing_v0.get("routing_scope") or "") != "need_navigation_routing_v0":
        return False, None

    # vNext narrow allow-progress path (still within v0 file):
    # - Still read-only; still no execution; allow_progress only in an extremely narrow, fully-satisfied precondition case.
    # - Otherwise, fall back to v2 structured pending/block reasons.
    gi = formal_decision_gate_inputs_v0 if isinstance(formal_decision_gate_inputs_v0, dict) else None
    if gi is not None and str(gi.get("gate_inputs_scope") or "") == "mid_platform_formal_decision_gate_inputs_v0":
        # Rule 1: safety blocked => block_execution
        if gi.get("safety_gate_v0_present") is True and str(gi.get("safety_status") or "") == "blocked":
            return True, {
                "decision_attempted": True,
                "decision_scope": _SCOPE,
                "decision_result": "block_execution",
                "reason": "safety_gate_blocked",
            }
        # Rule 2: task validity blocked => block_execution
        if gi.get("task_validity_v0_present") is True and str(gi.get("task_validity_status") or "") in (
            "expired",
            "overridden",
        ):
            return True, {
                "decision_attempted": True,
                "decision_scope": _SCOPE,
                "decision_result": "block_execution",
                "reason": "task_validity_blocked",
            }

    # Narrow allow_progress preconditions (ALL must be satisfied):
    # - branch consistency (minimal placeholder): routing_suggestion == "navigation_required"
    # - safety gate present + not blocked + no preempt
    # - task validity present + active
    # - handoff gates present + ready_candidate
    # - information gates present + ready_candidate
    hg = formal_decision_handoff_gates_v0 if isinstance(formal_decision_handoff_gates_v0, dict) else None
    ig = formal_decision_information_gates_v0 if isinstance(formal_decision_information_gates_v0, dict) else None
    suggestion = str(need_navigation_routing_v0.get("routing_suggestion") or "").strip()

    if (
        suggestion == "navigation_required"
        and isinstance(gi, dict)
        and gi.get("safety_gate_v0_present") is True
        and str(gi.get("safety_status") or "") in ("safe", "guarded")
        and (gi.get("safety_preempt_active") in (False, None))
        and gi.get("task_validity_v0_present") is True
        and str(gi.get("task_validity_status") or "") == "active"
        and isinstance(hg, dict)
        and hg.get("handoff_gate_present") is True
        and str(hg.get("handoff_gate_status") or "") == "ready_candidate"
        and isinstance(ig, dict)
        and ig.get("info_gate_present") is True
        and str(ig.get("info_sufficiency_status") or "") == "ready_candidate"
    ):
        return True, {
            "decision_attempted": True,
            "decision_scope": _SCOPE,
            "decision_result": "allow_progress",
            "reason": "all_minimum_preconditions_satisfied",
        }

    # Pending reason classification (priority order):
    # 1) missing_handoff_gate_inputs
    # 2) insufficient_information
    # 3) missing_required_gate_inputs (fallback)
    if hg is not None and hg.get("handoff_gate_present") is True:
        if str(hg.get("handoff_gate_status") or "") == "incomplete":
            return True, {
                "decision_attempted": True,
                "decision_scope": _SCOPE,
                "decision_result": "hold_pending",
                "reason": "missing_handoff_gate_inputs",
            }

    if ig is not None and ig.get("info_gate_present") is True:
        if str(ig.get("info_sufficiency_status") or "") == "insufficient":
            return True, {
                "decision_attempted": True,
                "decision_scope": _SCOPE,
                "decision_result": "hold_pending",
                "reason": "insufficient_information",
            }

    # Missing gate inputs (safety/task validity/handoff/info) or insufficient signals => conservative hold.
    # We MAY observe presence of other inputs, but must not infer execution readiness.
    _ = mid_platform_dispatch_consumption_stub_v0
    _ = destination_bound_v0
    _ = navigation_handoff_consume_bound_v0
    _ = navigation_handoff_post_bound_execution_stub_v0

    return True, {
        "decision_attempted": True,
        "decision_scope": _SCOPE,
        "decision_result": "hold_pending",
        "reason": "missing_required_gate_inputs",
    }

