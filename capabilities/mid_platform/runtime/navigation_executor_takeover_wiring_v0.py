# -*- coding: utf-8 -*-
"""
Navigation Executor Takeover Wiring v0 (minimal implementation; non-action).

Builds a minimal wiring result object `navigation_executor_takeover_wiring_v0` from already-attached metadata.

Hard boundaries:
- NOT an executor; NOT an action runtime; does NOT trigger navigation; no maps; no voice/memory side effects.
- Does NOT fabricate missing evidence; enforces the 8 wiring preconditions (plus a conservative post-bound placeholder gate).
- Does NOT take mainline control; only materializes a wiring result and (optionally) calls executor skeleton wiring interface.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_executor_takeover_wiring_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _post_bound_placeholder_progress_ok(
    *,
    navigation_handoff_post_bound_execution_stub_v0: Any,
    navigation_handoff_post_bound_execution_stub_consumption_v0: Any = None,
) -> bool:
    """
    Conservative check for "post-bound consumption has entered can-continue placeholder stage".

    Current repo reality:
    - We have `navigation_handoff_post_bound_execution_stub_v0` (voice runtime) that emits execution_pending.
    - We do NOT yet have a dedicated consumption object, but we accept it if future code adds it.
    """
    stub = _as_dict(navigation_handoff_post_bound_execution_stub_v0)
    if stub:
        if str(stub.get("execution_scope") or "") != "navigation_handoff_post_bound_execution_stub_v0":
            return False
        if str(stub.get("execution_state") or "") != "execution_pending":
            return False
        return True

    cons = _as_dict(navigation_handoff_post_bound_execution_stub_consumption_v0)
    if cons:
        # Future-proof: if a consumption object exists, require it to explicitly claim "can_continue_placeholder".
        if str(cons.get("consume_scope") or "") != "navigation_handoff_post_bound_execution_stub_consumption_v0":
            return False
        return bool(cons.get("can_continue_placeholder") is True)

    return False


def evaluate_navigation_executor_takeover_wiring_v0(
    *,
    mid_platform_formal_decision_stub_v0: Any,
    formal_decision_allow_progress_path_v0: Any,
    navigation_handoff_post_bound_execution_stub_v0: Any,
    navigation_real_execution_readiness_gate_stub_v0: Any,
    navigation_executor_takeover_stub_v0: Any,
    navigation_real_executor_input_v0: Any,
    navigation_real_executor_status_v0: Any,
    navigation_execution_monitoring_status_v0: Any,
    navigation_handoff_post_bound_execution_stub_consumption_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    Semantics:
    - If all 8 preconditions are satisfied => wiring_status is "wired_ready_to_takeover".
    - Otherwise => wiring_status is "not_applicable" with a minimal reason (still non-action).

    relevant-only:
    - If none of the key upstream evidence exists => (False, None)
    """
    fd = _as_dict(mid_platform_formal_decision_stub_v0)
    ap = _as_dict(formal_decision_allow_progress_path_v0)
    pb = _as_dict(navigation_handoff_post_bound_execution_stub_v0)
    rg = _as_dict(navigation_real_execution_readiness_gate_stub_v0)
    tk = _as_dict(navigation_executor_takeover_stub_v0)
    inp = _as_dict(navigation_real_executor_input_v0)
    st = _as_dict(navigation_real_executor_status_v0)
    mon = _as_dict(navigation_execution_monitoring_status_v0)
    pb_cons = _as_dict(navigation_handoff_post_bound_execution_stub_consumption_v0)

    # relevant-only gate: if nothing is present, don't write.
    if not any([fd, ap, pb, rg, tk, inp, st, mon, pb_cons]):
        return False, None

    missing: list[str] = []

    # 1) formal decision allow_progress
    if not fd:
        missing.append("missing_mid_platform_formal_decision_stub_v0")
    else:
        if str(fd.get("decision_scope") or "") != "mid_platform_formal_decision_stub_v0":
            missing.append("bad_formal_decision_scope")
        if str(fd.get("decision_result") or "") != "allow_progress":
            missing.append("formal_decision_not_allow_progress")

    # 2) allow-progress path downstream interface
    if not ap:
        missing.append("missing_formal_decision_allow_progress_path_v0")
    else:
        if ap.get("allow_progress_path_present") is not True:
            missing.append("allow_progress_path_not_present")
        if str(ap.get("downstream_placeholder_interface") or "") != "navigation_handoff_post_bound_execution_stub_v0":
            missing.append("downstream_interface_mismatch")

    # 3) post-bound placeholder progress
    if not _post_bound_placeholder_progress_ok(
        navigation_handoff_post_bound_execution_stub_v0=pb,
        navigation_handoff_post_bound_execution_stub_consumption_v0=pb_cons,
    ):
        missing.append("post_bound_not_in_can_continue_placeholder_stage")

    # 4) readiness ready_candidate
    if not rg:
        missing.append("missing_navigation_real_execution_readiness_gate_stub_v0")
    else:
        if str(rg.get("readiness_scope") or "") != "navigation_real_execution_readiness_gate_stub_v0":
            missing.append("bad_readiness_scope")
        if str(rg.get("readiness_status") or "") != "ready_candidate":
            missing.append("readiness_not_ready_candidate")

    # 5) takeover ready_to_takeover
    if not tk:
        missing.append("missing_navigation_executor_takeover_stub_v0")
    else:
        if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
            missing.append("bad_takeover_scope")
        if str(tk.get("takeover_status") or "") != "ready_to_takeover":
            missing.append("takeover_not_ready_to_takeover")

    # 6) implemented input object exists
    if not inp:
        missing.append("missing_navigation_real_executor_input_v0")
    else:
        if str(inp.get("executor_input_scope") or "") != "navigation_real_executor_input_v0":
            missing.append("bad_executor_input_scope")
        if str(inp.get("object_kind") or "") != "implemented_v0":
            missing.append("executor_input_not_implemented")

    # 7) implemented status object exists
    if not st:
        missing.append("missing_navigation_real_executor_status_v0")
    else:
        if str(st.get("executor_status_scope") or "") != "navigation_real_executor_status_v0":
            missing.append("bad_executor_status_scope")
        if str(st.get("object_kind") or "") != "implemented_v0":
            missing.append("executor_status_not_implemented")

    # 8) implemented monitoring status exists
    if not mon:
        missing.append("missing_navigation_execution_monitoring_status_v0")
    else:
        if str(mon.get("monitoring_status_scope") or "") != "navigation_execution_monitoring_status_v0":
            missing.append("bad_monitoring_status_scope")
        if str(mon.get("object_kind") or "") != "implemented_v0":
            missing.append("monitoring_status_not_implemented")

    ok = len(missing) == 0
    wiring_status = "wired_ready_to_takeover" if ok else "not_applicable"

    payload: Dict[str, Any] = {
        "wiring_attempted": True,
        "wiring_scope": _SCOPE,
        "wiring_status": wiring_status,
        "reason": "all_preconditions_satisfied" if ok else (";".join(missing)[:240]),
    }

    # Safety note: even when wired_ready_to_takeover, this is NOT action execution.
    return True, payload

