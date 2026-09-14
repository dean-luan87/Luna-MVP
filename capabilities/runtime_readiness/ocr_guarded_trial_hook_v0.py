# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-004 — OCR guarded trial hook wrapper (default-off).

Safe wrapper for candidate OCR mainline paths:
- Evaluates gate with global kill precedence.
- Default behavior: no-op (enabled=false).
- Must NOT invoke OCR providers or downstream semantic consumers.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from typing import Any, Dict, Mapping, Optional

from capabilities.runtime_readiness.guarded_trial_gate_v0 import (
    evaluate_ocr_guarded_trial_gate_v0,
    read_guarded_trial_env_snapshot_v0,
)
from capabilities.runtime_readiness.guarded_trial_trw_validator_v0 import (
    validate_guarded_trial_trw_fields_v0,
)


def _gate_ref(trial_name: str, decision: str, trial_mode: str) -> str:
    raw = f"{trial_name}:{decision}:{trial_mode}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _reason_from_gate(decision: str) -> str:
    if decision == "disabled":
        return "trial_disabled"
    if decision == "forced_disabled_by_global_kill":
        return "global_kill_switch"
    if decision == "blocked_invalid_mode":
        return "invalid_mode"
    if decision == "blocked_missing_trw":
        return "missing_trw"
    if decision == "blocked_abort_condition":
        return "abort_condition"
    return "trial_disabled"


def evaluate_ocr_guarded_trial_hook_v0(
    *,
    request_id: Optional[str] = None,
    trw_payload: Optional[Mapping[str, Any]] = None,
    env_override: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """
    Returns HookResult schema (default-off).

    Never invokes OCR providers.
    """
    snap = read_guarded_trial_env_snapshot_v0(env_override)
    trw_ok: Optional[bool] = None
    if trw_payload is not None:
        trw_ok = bool(validate_guarded_trial_trw_fields_v0(trw_payload).get("valid"))

    gd = evaluate_ocr_guarded_trial_gate_v0(snap, trw_validation_ok=trw_ok)
    gate_ref = _gate_ref(gd.trial_name, gd.decision, gd.trial_mode)

    return {
        "hook_result_id": f"hook_ocr_{uuid.uuid4().hex[:12]}",
        "trial_name": gd.trial_name,
        "capability": "ocr",
        "gate_decision_ref": gate_ref,
        "enabled": False,
        "no_op": True,
        "reason": _reason_from_gate(gd.decision),
        "would_execute_if_enabled": False,
        "runtime_invoked": False,
        "provider_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "world_write_invoked": False,
        "navigation_action": None,
        "default_behavior_changed": False,
        "debug": {
            "ts": float(time.time()),
            "request_id": request_id,
            "gate_decision": gd.to_dict(),
        },
    }

