# -*- coding: utf-8 -*-
"""
Formal Decision Information Sufficiency Gates v0 (read-only gate-input wiring).

Builds a minimal info sufficiency gate input from existing stable context:
- proposal.task_action (or equivalent context) (passed in)
- handoff-chain observations in result.metadata:
  - destination_bound_v0
  - navigation_handoff_consume_bound_v0
  - navigation_handoff_post_bound_execution_stub_v0

Hard boundaries:
- Does NOT change formal decision behavior.
- Does NOT add time/space anchors; does NOT depend on maps.
- Does NOT infer allow_progress; only marks ready_candidate vs insufficient.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def _as_str(x: Any) -> str:
    return str(x or "").strip()


def _present_bound(x: Any) -> bool:
    return isinstance(x, dict) and bool(x) and (x.get("destination_bound") is True)


def _present_consume_bound(x: Any) -> bool:
    return isinstance(x, dict) and bool(x) and (x.get("bound_consumed") is True)


def _present_post_bound_stub(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if str(x.get("execution_scope") or "") != "navigation_handoff_post_bound_execution_stub_v0":
        return False
    st = _as_str(x.get("execution_state"))
    return st in ("execution_ready", "execution_blocked", "execution_pending")


def build_formal_decision_information_gates_v0(
    *,
    task_action: str,
    destination_bound_v0: Any,
    navigation_handoff_consume_bound_v0: Any,
    navigation_handoff_post_bound_execution_stub_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, gate_input_dict).

    relevant-only:
    - If task_action empty and none of the inputs exist => (False, None)
    """
    ta = _as_str(task_action)

    bound_present = _present_bound(destination_bound_v0)
    consume_bound_present = _present_consume_bound(navigation_handoff_consume_bound_v0)
    post_stub_present = _present_post_bound_stub(navigation_handoff_post_bound_execution_stub_v0)

    task_context_present = bool(ta)

    # Minimal placeholder for "required_action_inputs_present":
    # - for start_navigation, require a bound destination fact to exist (still not execution-ready).
    # - for all other/unknown actions, keep conservative false unless explicitly present (not available v0).
    if ta == "start_navigation":
        required_action_inputs_present = bool(bound_present)
    else:
        required_action_inputs_present = False

    # Minimal placeholder for "candidate_inputs_present":
    # - true when any of the handoff-related observations exist, indicating some supporting context exists.
    candidate_inputs_present = bool(bound_present or consume_bound_present or post_stub_present)

    if (not task_context_present) and (not candidate_inputs_present):
        return False, None

    if task_context_present and required_action_inputs_present and candidate_inputs_present:
        status = "ready_candidate"
    else:
        status = "insufficient"

    return True, {
        "info_gate_present": True,
        "task_context_present": bool(task_context_present),
        "required_action_inputs_present": bool(required_action_inputs_present),
        "candidate_inputs_present": bool(candidate_inputs_present),
        "info_sufficiency_status": str(status),
        "consume_mode": "read_only",
    }

