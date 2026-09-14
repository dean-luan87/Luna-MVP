# -*- coding: utf-8 -*-
"""
Navigation Governance Action Executor Input Object v0 (implemented object; read-only builder).

Builds a standardized *implemented* input object `navigation_governance_action_executor_input_v0`
from legal upstream metadata (approval boundary + executor skeleton identity).

Hard boundaries:
- NOT a governance action command; NOT proof that governance actions executed.
- Does NOT trigger rollback/interrupt/release-control; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_executor_input_v0"
_KIND = "implemented_v0"
_APPROVAL_SCOPE = "navigation_governance_action_approval_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _executor_skeleton_ok() -> bool:
    try:
        from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
            get_governance_action_executor_identity,
        )

        ident = get_governance_action_executor_identity()
        if not isinstance(ident, dict):
            return False
        if ident.get("is_skeleton") is not True:
            return False
        if str(ident.get("governance_action_executor_identity") or "") != "navigation_governance_action_executor_v0":
            return False
        if ident.get("can_execute_real_actions") is not False:
            return False
        return True
    except Exception:
        return False


def _approval_status_to_action_type(approval_status: str) -> str:
    s = str(approval_status or "").strip()
    if s == "approved_interrupt":
        return "interrupt"
    if s == "approved_release_control":
        return "release_control"
    if s == "approved_rollback":
        return "rollback_request"
    if s == "approved_hold_executor_state":
        return "hold"
    return "hold"


def evaluate_navigation_governance_action_executor_input_v0(
    *,
    navigation_governance_action_approval_boundary_v0: Any,
    navigation_governance_action_boundary_v0: Any = None,
    navigation_rollback_and_interruption_governance_decision_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid approval boundary object AND approval status in approved_* (NOT approval_blocked).
    - Requires governance action executor skeleton identity ok.
    - Optional action boundary / governance decision are read-only consistency context only (must NOT expand authority).
    """
    ap = _as_dict(navigation_governance_action_approval_boundary_v0)
    if not ap:
        return False, None
    if str(ap.get("governance_action_approval_scope") or "") != _APPROVAL_SCOPE:
        return False, None
    if ap.get("governance_action_approval_attempted") is not True:
        return False, None

    approval_status = str(ap.get("governance_action_approval_status") or "").strip()
    if approval_status not in (
        "approved_hold_executor_state",
        "approved_interrupt",
        "approved_release_control",
        "approved_rollback",
    ):
        # approval_blocked or unknown => relevant-only (do not generate executor input object)
        return False, None

    if not _executor_skeleton_ok():
        return False, None

    approved_action_type = _approval_status_to_action_type(approval_status)

    # Optional: read-only context; no authority expansion, no blocking overrides.
    _ = navigation_governance_action_boundary_v0
    _ = navigation_rollback_and_interruption_governance_decision_v0

    payload: Dict[str, Any] = {
        "governance_action_executor_input_present": True,
        "governance_action_executor_input_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        # Category 1: approved action type
        "approved_action_type_class": {
            "approved_action_type": approved_action_type,
            "approval_scope": _APPROVAL_SCOPE,
            "approval_status": approval_status,
        },
        # Category 2: execution prerequisites (explicitly NOT ready; not a placeholder string)
        "execution_prerequisites_class": {
            "execution_prerequisites_ready": False,
            "prerequisites_fact": "not_ready_for_real_action_execution",
            "reason": "input_object_implementation_v0_does_not_imply_runtime_or_approval_chain_execution",
        },
        # Category 4: constraints (minimal, stable semantics)
        "execution_constraints_class": {
            "constraint_profile": "minimal_safe_constraints_v0",
            "hard_prohibitions": [
                "no_real_governance_action_execution",
                "no_route_change",
                "no_voice_or_memory_side_effects",
                "no_mid_platform_real_migration",
                "no_maps_or_coordinates",
            ],
        },
        # Category 3: target (semantic placeholder only)
        "action_target_class": {
            "target_kind": "navigation_executor_control_plane",
            "target_scope": "navigation_real_executor_v0",
            "notes": "semantic_placeholder_only",
        },
        # Category 5: return binding (placeholder; future wiring)
        "return_binding_class": {
            "return_binding_ready": False,
            "return_binding_kind": "not_bound_yet",
        },
        "upstream_evidence": {
            "governance_action_executor_identity": "navigation_governance_action_executor_v0",
            "approval_status": approval_status,
        },
    }
    return True, payload

