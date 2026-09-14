# -*- coding: utf-8 -*-
"""
Navigation Real Executor Input Object v0 (implemented object; read-only builder).

Builds a minimal, standardized *implemented* object `navigation_real_executor_input_v0` from already-attached metadata.

Hard boundaries:
- NOT an executor; does NOT trigger navigation; no maps; no time/space anchors.
- Does NOT fabricate missing inputs; requires narrow, explicit upstream preconditions.
- Output is an implemented object (not placeholder), but still does not imply execution started.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_real_executor_input_v0"
_KIND = "implemented_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_real_executor_input_object_v0(
    *,
    mid_platform_formal_decision_stub_v0: Any,
    formal_decision_allow_progress_path_v0: Any,
    navigation_real_execution_readiness_gate_stub_v0: Any,
    navigation_executor_takeover_stub_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If ANY required upstream evidence missing or mismatched => (False, None)
    """
    fd = _as_dict(mid_platform_formal_decision_stub_v0)
    ap = _as_dict(formal_decision_allow_progress_path_v0)
    rg = _as_dict(navigation_real_execution_readiness_gate_stub_v0)
    tk = _as_dict(navigation_executor_takeover_stub_v0)

    if not (fd and ap and rg and tk):
        return False, None

    # 1) formal decision allow_progress
    if str(fd.get("decision_scope") or "") != "mid_platform_formal_decision_stub_v0":
        return False, None
    if str(fd.get("decision_result") or "") != "allow_progress":
        return False, None

    # 2) narrow allow-progress path points to our downstream placeholder interface
    if ap.get("allow_progress_path_present") is not True:
        return False, None
    if str(ap.get("consume_mode") or "") != "read_only":
        return False, None
    if str(ap.get("downstream_placeholder_interface") or "") != "navigation_handoff_post_bound_execution_stub_v0":
        return False, None

    # 3) readiness candidate
    if str(rg.get("readiness_scope") or "") != "navigation_real_execution_readiness_gate_stub_v0":
        return False, None
    if str(rg.get("readiness_status") or "") != "ready_candidate":
        return False, None

    # 4) takeover ready_to_takeover
    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(tk.get("takeover_status") or "") != "ready_to_takeover":
        return False, None

    # Implemented object: minimal categories (takeover auth / task context / constraints).
    # Keep it small; no time/space; no maps; no implicit execution signals.
    payload: Dict[str, Any] = {
        "executor_input_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        "takeover_authorization": {
            "authorized": True,
            "authorization_source_scope": "navigation_executor_takeover_stub_v0",
            "authorization_status": "ready_to_takeover",
        },
        "task_context": {
            "task_context_ready": True,
            "downstream_interface": "navigation_handoff_post_bound_execution_stub_v0",
            "decision_source_scope": "mid_platform_formal_decision_stub_v0",
            "decision_result": "allow_progress",
        },
        "execution_constraints": {
            "constraints_ready": False,
            "constraints_kind": "not_implemented_yet",
            "constraints_source_scope": "",
        },
        # allowed to remain minimal placeholder until maps/resources are integrated
        "path_support": {
            "mode": "unknown_placeholder",
            "reason": "maps_and_resources_not_integrated",
        },
        # allowed to remain minimal placeholder until monitoring routing is implemented
        "monitor_binding": {
            "binding_ready": False,
            "binding_kind": "not_implemented_yet",
        },
        # minimal upstream evidence echo for observability (no extra anchors)
        "upstream_evidence": {
            "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
            "readiness_status": "ready_candidate",
            "takeover_scope": "navigation_executor_takeover_stub_v0",
            "takeover_status": "ready_to_takeover",
        },
    }
    return True, payload

