# -*- coding: utf-8 -*-
"""
Formal Decision Gate Inputs v0 (read-only wiring).

Reads (future) gate inputs from runtime_context.metadata without fabricating values:
- safety_gate_v0
- task_validity_v0

Hard boundaries:
- Does NOT decide; does NOT change behavior.
- Does NOT fabricate missing fields.
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def _is_safety_gate_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("safety_gate_present"), bool):
        return False
    st = x.get("safety_status")
    if st is not None and str(st) not in ("safe", "guarded", "blocked"):
        return False
    if "safety_preempt_active" in x and not isinstance(x.get("safety_preempt_active"), bool):
        return False
    return True


def _is_task_validity_v0(x: Any) -> bool:
    if not isinstance(x, dict) or not x:
        return False
    if not isinstance(x.get("task_validity_present"), bool):
        return False
    st = x.get("task_validity_status")
    if st is not None and str(st) not in ("active", "suspended", "expired", "overridden"):
        return False
    return True


def read_formal_decision_gate_inputs_v0(
    *,
    runtime_context_metadata: Optional[Dict[str, Any]],
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, observation_payload).

    relevant-only:
    - If neither gate input is present+valid => (False, None)
    """
    md = runtime_context_metadata or {}
    if not isinstance(md, dict) or not md:
        return False, None

    safety = md.get("safety_gate_v0")
    taskv = md.get("task_validity_v0")

    out: Dict[str, Any] = {
        "gate_inputs_scope": "mid_platform_formal_decision_gate_inputs_v0",
        "consume_mode": "read_only",
    }

    saw_any = False
    if _is_safety_gate_v0(safety):
        out["safety_gate_v0_present"] = True
        out["safety_status"] = str(safety.get("safety_status") or "")
        out["safety_preempt_active"] = bool(safety.get("safety_preempt_active", False))
        saw_any = True
    if _is_task_validity_v0(taskv):
        out["task_validity_v0_present"] = True
        out["task_validity_status"] = str(taskv.get("task_validity_status") or "")
        saw_any = True

    if not saw_any:
        return False, None
    return True, out

