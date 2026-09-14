# -*- coding: utf-8 -*-
"""
Abort / rollback hook placeholders for guarded trials (Phase-003).

No side effects; returns structured plans only.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional


def evaluate_guarded_trial_abort_conditions_v0(
    *,
    gate_decision: str,
    trial_capability: str,
    signals: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Placeholder abort evaluation. Extend with real predicates in later phases.

    signals may include: detector_error, schema_invalid, governance_leakage, etc.
    """
    sig = dict(signals or {})
    reasons: List[str] = []
    abort_required = False

    if sig.get("detector_exception"):
        abort_required = True
        reasons.append("detector_exception")
    if sig.get("schema_invalid"):
        abort_required = True
        reasons.append("schema_invalid")
    if sig.get("governance_leakage"):
        abort_required = True
        reasons.append("governance_leakage")
    if sig.get("downstream_invocation_detected"):
        abort_required = True
        reasons.append("downstream_invocation_detected")

    return {
        "abort_required": abort_required,
        "abort_reason": ",".join(reasons) if reasons else None,
        "gate_decision_snapshot": gate_decision,
        "trial_capability": trial_capability,
    }


def build_guarded_trial_rollback_plan_v0(
    *,
    trial_capability: str,
    gate_decision: str,
    abort_payload: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Default rollback plan — conservative; does not mutate env at runtime."""
    ap = abort_payload or {}
    rollback_action = "none"
    safe_default = "trial_disabled"

    if ap.get("abort_required"):
        rollback_action = "disable_trial"
        safe_default = "shadow_only_or_offline"

    if trial_capability == "ocr":
        safe_default = "force_not_available_when_abort"
    elif trial_capability == "qwen_voice":
        safe_default = "force_offline_only_selected_provider_none"

    return {
        "rollback_action": rollback_action,
        "safe_default": safe_default,
        "shadow_evidence_retained": True,
        "trial_capability": trial_capability,
        "related_gate_decision": gate_decision,
    }
