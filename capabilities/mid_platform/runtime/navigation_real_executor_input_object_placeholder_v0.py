# -*- coding: utf-8 -*-
"""
Navigation Real Executor Input Object Placeholder v0 (read-only).

Builds a minimal, observable placeholder object `navigation_real_executor_input_v0` from already-attached metadata.

Hard boundaries:
- NOT an executor; does NOT trigger navigation; no maps; no time/space anchors.
- Does NOT fabricate missing inputs; requires narrow, explicit upstream preconditions.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_real_executor_input_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_real_executor_input_object_placeholder_v0(
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

    if str(fd.get("decision_scope") or "") != "mid_platform_formal_decision_stub_v0":
        return False, None
    if str(fd.get("decision_result") or "") != "allow_progress":
        return False, None

    if ap.get("allow_progress_path_present") is not True:
        return False, None
    if str(ap.get("consume_mode") or "") != "read_only":
        return False, None
    # Current narrow wiring: allow-progress path targets post-bound placeholder interface.
    if str(ap.get("downstream_placeholder_interface") or "") != "navigation_handoff_post_bound_execution_stub_v0":
        return False, None

    if str(rg.get("readiness_scope") or "") != "navigation_real_execution_readiness_gate_stub_v0":
        return False, None
    if str(rg.get("readiness_status") or "") != "ready_candidate":
        return False, None

    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(tk.get("takeover_status") or "") != "ready_to_takeover":
        return False, None

    # Minimal placeholder object (do NOT add time/space anchors; keep flat and small).
    return True, {
        "executor_input_present": True,
        "executor_input_scope": _SCOPE,
        "takeover_authorized": True,
        "task_context_ready": True,
        "path_support_mode": "unknown_placeholder",
        "execution_constraints_ready": False,
        "monitor_binding_ready": False,
        "consume_mode": "read_only",
    }

