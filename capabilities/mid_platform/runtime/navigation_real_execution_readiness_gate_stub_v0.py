# -*- coding: utf-8 -*-
"""
Navigation Real Execution Readiness Gate Stub v0 (read-only).

Consumes the unified readiness gate inputs object and emits a conservative readiness result.

Hard boundaries:
- NOT an executor; does NOT trigger navigation execution; does NOT depend on maps.
- Does NOT fabricate missing gate inputs; missing => not_ready (or relevant-only no write).
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_real_execution_readiness_gate_stub_v0"
_INPUT_SCOPE = "navigation_real_execution_readiness_gate_inputs_v0"


def _is_inputs_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if str(x.get("readiness_gate_inputs_scope") or "") != _INPUT_SCOPE:
        return False
    if x.get("readiness_gate_inputs_present") is not True:
        return False
    if str(x.get("consume_mode") or "") != "read_only":
        return False
    return True


def _status_str(x: Any) -> str:
    return str(x or "").strip()


def evaluate_navigation_real_execution_readiness_gate_stub_v0(
    *,
    navigation_real_execution_readiness_gate_inputs_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If inputs missing/invalid => (False, None)
    """
    inp = navigation_real_execution_readiness_gate_inputs_v0
    if not _is_inputs_v0(inp):
        return False, None

    # Rule 1: hard block if any explicit blocked/unavailable appears in known status fields.
    # Extremely conservative: treat "unavailable" as hard-block for now (per Phase-Next-12 request).
    hard_block_reasons = []
    exec_status = _status_str(inp.get("executor_status"))
    if exec_status in ("blocked", "unavailable"):
        hard_block_reasons.append(f"executor_status:{exec_status}")

    path_status = _status_str(inp.get("path_support_status"))
    if path_status == "unavailable":
        hard_block_reasons.append("path_support_status:unavailable")

    mon_status = _status_str(inp.get("execution_monitor_status"))
    if mon_status == "unavailable":
        hard_block_reasons.append("execution_monitor_status:unavailable")

    start_status = _status_str(inp.get("start_policy_status"))
    if start_status == "unavailable":
        hard_block_reasons.append("start_policy_status:unavailable")

    fb_status = _status_str(inp.get("fallback_status"))
    if fb_status == "unavailable":
        hard_block_reasons.append("fallback_status:unavailable")

    if hard_block_reasons:
        return True, {
            "readiness_attempted": True,
            "readiness_scope": _SCOPE,
            "readiness_status": "blocked",
            "reason": "hard_blocked:" + ",".join(hard_block_reasons),
        }

    # Rule 2: ready_candidate only when ALL 5 gates are present and satisfy minimal thresholds.
    all_present = all(
        inp.get(k) is True
        for k in (
            "executor_gate_present",
            "path_support_gate_present",
            "execution_monitor_gate_present",
            "start_policy_gate_present",
            "fallback_gate_present",
        )
    )
    if all_present:
        ok_exec = exec_status == "available" and inp.get("executor_takeover_allowed") is True
        ok_path = path_status in ("available", "partial")
        ok_mon = mon_status == "ready_candidate"
        ok_start = start_status == "ready_candidate"
        ok_fb = fb_status == "ready_candidate"

        if ok_exec and ok_path and ok_mon and ok_start and ok_fb:
            return True, {
                "readiness_attempted": True,
                "readiness_scope": _SCOPE,
                "readiness_status": "ready_candidate",
                "reason": "all_minimum_readiness_preconditions_satisfied",
            }

    # Rule 3: otherwise not_ready.
    return True, {
        "readiness_attempted": True,
        "readiness_scope": _SCOPE,
        "readiness_status": "not_ready",
        "reason": "missing_or_insufficient_readiness_gate_inputs",
    }

