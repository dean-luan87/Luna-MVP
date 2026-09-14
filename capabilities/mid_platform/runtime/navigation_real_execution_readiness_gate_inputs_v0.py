# -*- coding: utf-8 -*-
"""
Navigation Real Execution Readiness Gate Inputs v0 (read-only wiring).

Reads future readiness gate inputs from runtime_context.metadata without fabricating values.
Builds a minimal unified observation object for downstream readiness gate logic (future).

Hard boundaries:
- Does NOT decide readiness; does NOT trigger execution; does NOT add time/space anchors.
- Does NOT assume missing inputs are available.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_real_execution_readiness_gate_inputs_v0"


def _is_executor_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("executor_gate_present"), bool):
        return False
    if "executor_available" in x and not isinstance(x.get("executor_available"), bool):
        return False
    if "executor_takeover_allowed" in x and not isinstance(x.get("executor_takeover_allowed"), bool):
        return False
    st = x.get("executor_status")
    if st is not None and str(st) not in ("available", "unavailable", "blocked"):
        return False
    return True


def _is_path_support_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("path_support_gate_present"), bool):
        return False
    for k in ("map_support_available", "non_map_support_available"):
        if k in x and not isinstance(x.get(k), bool):
            return False
    st = x.get("path_support_status")
    if st is not None and str(st) not in ("available", "partial", "unavailable"):
        return False
    return True


def _is_execution_monitor_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("execution_monitor_gate_present"), bool):
        return False
    for k in ("monitor_feedback_available", "drift_detection_available"):
        if k in x and not isinstance(x.get(k), bool):
            return False
    st = x.get("execution_monitor_status")
    if st is not None and str(st) not in ("ready_candidate", "partial", "unavailable"):
        return False
    return True


def _is_start_policy_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("start_policy_gate_present"), bool):
        return False
    if "start_output_policy_available" in x and not isinstance(x.get("start_output_policy_available"), bool):
        return False
    st = x.get("start_policy_status")
    if st is not None and str(st) not in ("ready_candidate", "restricted", "unavailable"):
        return False
    return True


def _is_fallback_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("fallback_gate_present"), bool):
        return False
    for k in ("fallback_path_available", "interrupt_recovery_available"):
        if k in x and not isinstance(x.get(k), bool):
            return False
    st = x.get("fallback_status")
    if st is not None and str(st) not in ("ready_candidate", "partial", "unavailable"):
        return False
    return True


def read_navigation_real_execution_readiness_gate_inputs_v0(
    *,
    runtime_context_metadata: Optional[Dict[str, Any]],
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, observation_payload).

    relevant-only:
    - If none of the 5 gate inputs are present+valid => (False, None)
    """
    md = runtime_context_metadata or {}
    if not isinstance(md, dict) or not md:
        return False, None

    exec_gate = md.get("navigation_executor_gate_v0")
    path_gate = md.get("navigation_path_support_gate_v0")
    mon_gate = md.get("navigation_execution_monitor_gate_v0")
    start_gate = md.get("navigation_start_policy_gate_v0")
    fb_gate = md.get("navigation_fallback_gate_v0")

    out: Dict[str, Any] = {
        "readiness_gate_inputs_scope": _SCOPE,
        "consume_mode": "read_only",
        "readiness_gate_inputs_present": True,
        "executor_gate_present": False,
        "path_support_gate_present": False,
        "execution_monitor_gate_present": False,
        "start_policy_gate_present": False,
        "fallback_gate_present": False,
    }

    saw_any = False

    if _is_executor_gate_v0(exec_gate):
        out["executor_gate_present"] = bool(exec_gate.get("executor_gate_present"))
        if "executor_available" in exec_gate:
            out["executor_available"] = bool(exec_gate.get("executor_available"))
        if "executor_status" in exec_gate:
            out["executor_status"] = str(exec_gate.get("executor_status") or "")
        if "executor_takeover_allowed" in exec_gate:
            out["executor_takeover_allowed"] = bool(exec_gate.get("executor_takeover_allowed"))
        saw_any = True

    if _is_path_support_gate_v0(path_gate):
        out["path_support_gate_present"] = bool(path_gate.get("path_support_gate_present"))
        if "map_support_available" in path_gate:
            out["map_support_available"] = bool(path_gate.get("map_support_available"))
        if "non_map_support_available" in path_gate:
            out["non_map_support_available"] = bool(path_gate.get("non_map_support_available"))
        if "path_support_status" in path_gate:
            out["path_support_status"] = str(path_gate.get("path_support_status") or "")
        saw_any = True

    if _is_execution_monitor_gate_v0(mon_gate):
        out["execution_monitor_gate_present"] = bool(mon_gate.get("execution_monitor_gate_present"))
        if "monitor_feedback_available" in mon_gate:
            out["monitor_feedback_available"] = bool(mon_gate.get("monitor_feedback_available"))
        if "drift_detection_available" in mon_gate:
            out["drift_detection_available"] = bool(mon_gate.get("drift_detection_available"))
        if "execution_monitor_status" in mon_gate:
            out["execution_monitor_status"] = str(mon_gate.get("execution_monitor_status") or "")
        saw_any = True

    if _is_start_policy_gate_v0(start_gate):
        out["start_policy_gate_present"] = bool(start_gate.get("start_policy_gate_present"))
        if "start_output_policy_available" in start_gate:
            out["start_output_policy_available"] = bool(start_gate.get("start_output_policy_available"))
        if "start_policy_status" in start_gate:
            out["start_policy_status"] = str(start_gate.get("start_policy_status") or "")
        saw_any = True

    if _is_fallback_gate_v0(fb_gate):
        out["fallback_gate_present"] = bool(fb_gate.get("fallback_gate_present"))
        if "fallback_path_available" in fb_gate:
            out["fallback_path_available"] = bool(fb_gate.get("fallback_path_available"))
        if "interrupt_recovery_available" in fb_gate:
            out["interrupt_recovery_available"] = bool(fb_gate.get("interrupt_recovery_available"))
        if "fallback_status" in fb_gate:
            out["fallback_status"] = str(fb_gate.get("fallback_status") or "")
        saw_any = True

    if not saw_any:
        return False, None
    return True, out

