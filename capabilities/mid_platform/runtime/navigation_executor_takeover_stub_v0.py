# -*- coding: utf-8 -*-
"""
Navigation Executor Takeover Stub v0 (read-only).

Builds a unified, observable "takeover readiness" placeholder output from already-attached metadata.

Hard boundaries:
- NOT an executor; does NOT transfer control; does NOT trigger navigation execution; no maps.
- Does NOT fabricate missing inputs.
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_executor_takeover_stub_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _is_allow_progress(fd: Optional[Dict[str, Any]]) -> bool:
    if not fd:
        return False
    if str(fd.get("decision_scope") or "") != "mid_platform_formal_decision_stub_v0":
        return False
    return str(fd.get("decision_result") or "") == "allow_progress"


def _is_path_to_post_bound_stub(p: Optional[Dict[str, Any]]) -> bool:
    if not p:
        return False
    if p.get("allow_progress_path_present") is not True:
        return False
    if str(p.get("consume_mode") or "") != "read_only":
        return False
    return str(p.get("downstream_placeholder_interface") or "") == "navigation_handoff_post_bound_execution_stub_v0"


def _post_bound_consumption_equivalent_present(
    *,
    post_bound_stub: Optional[Dict[str, Any]],
    destination_bound_v0: Any,
    navigation_handoff_consume_bound_v0: Any,
    explicit_consumption_result: Optional[Dict[str, Any]],
) -> bool:
    # Preferred: explicit downstream consumption result (future hook).
    if explicit_consumption_result:
        if str(explicit_consumption_result.get("consumption_scope") or "") == "navigation_handoff_post_bound_execution_stub_consumption_v0":
            return str(explicit_consumption_result.get("consumption_result") or "") == "consumed_pending_execution"

    # Current repo fallback: treat presence of post-bound execution stub (pending) as the only safe equivalent.
    if not isinstance(post_bound_stub, dict) or not post_bound_stub:
        return False
    if str(post_bound_stub.get("execution_scope") or "") != "navigation_handoff_post_bound_execution_stub_v0":
        return False
    if str(post_bound_stub.get("execution_state") or "") != "execution_pending":
        return False

    # Must also have the upstream bound + consume-bound facts present (avoid taking stub alone as a signal).
    if not (isinstance(destination_bound_v0, dict) and destination_bound_v0.get("destination_bound") is True):
        return False
    if not (isinstance(navigation_handoff_consume_bound_v0, dict) and navigation_handoff_consume_bound_v0.get("bound_consumed") is True):
        return False
    return True


def evaluate_navigation_executor_takeover_stub_v0(
    *,
    mid_platform_formal_decision_stub_v0: Any,
    formal_decision_allow_progress_path_v0: Any,
    navigation_handoff_post_bound_execution_stub_v0: Any,
    navigation_real_execution_readiness_gate_stub_v0: Any,
    destination_bound_v0: Any = None,
    navigation_handoff_consume_bound_v0: Any = None,
    # Optional future explicit consumption result (not implemented in this repo yet).
    navigation_handoff_post_bound_execution_stub_consumption_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If none of the key inputs exist => (False, None)
    """
    fd = _as_dict(mid_platform_formal_decision_stub_v0)
    path = _as_dict(formal_decision_allow_progress_path_v0)
    post_stub = _as_dict(navigation_handoff_post_bound_execution_stub_v0)
    rg = _as_dict(navigation_real_execution_readiness_gate_stub_v0)
    cons = _as_dict(navigation_handoff_post_bound_execution_stub_consumption_v0)

    if not any([fd, path, post_stub, rg, cons]):
        return False, None

    # Rule 2: explicit blocked if readiness gate says blocked.
    if rg and str(rg.get("readiness_scope") or "") == "navigation_real_execution_readiness_gate_stub_v0":
        if str(rg.get("readiness_status") or "") == "blocked":
            return True, {
                "takeover_attempted": True,
                "takeover_scope": _SCOPE,
                "takeover_status": "blocked",
                "reason": "readiness_gate_blocked",
            }

    allow_ok = _is_allow_progress(fd)
    path_ok = _is_path_to_post_bound_stub(path)
    readiness_ok = bool(rg) and str(rg.get("readiness_scope") or "") == "navigation_real_execution_readiness_gate_stub_v0" and str(
        rg.get("readiness_status") or ""
    ) == "ready_candidate"
    downstream_ok = _post_bound_consumption_equivalent_present(
        post_bound_stub=post_stub,
        destination_bound_v0=destination_bound_v0,
        navigation_handoff_consume_bound_v0=navigation_handoff_consume_bound_v0,
        explicit_consumption_result=cons,
    )

    # Rule 1: all takeover entry preconditions satisfied.
    if allow_ok and path_ok and downstream_ok and readiness_ok:
        return True, {
            "takeover_attempted": True,
            "takeover_scope": _SCOPE,
            "takeover_status": "ready_to_takeover",
            "reason": "all_minimum_takeover_preconditions_satisfied",
        }

    # Rule 3: otherwise not_applicable (keep conservative; do not fabricate partial readiness).
    return True, {
        "takeover_attempted": True,
        "takeover_scope": _SCOPE,
        "takeover_status": "not_applicable",
        "reason": "missing_required_takeover_preconditions",
    }

