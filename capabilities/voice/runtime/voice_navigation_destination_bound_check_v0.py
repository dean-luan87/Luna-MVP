# -*- coding: utf-8 -*-
"""
Navigation destination bound check v0 (read-only evaluator).

Hard boundaries:
- Does NOT write destination_bound.
- Does NOT change route/proposal/handoff/submit behavior.
- Does NOT parse places, does NOT call maps/search.
- Does NOT use memory/vision as upgrade evidence.
- Does NOT add any time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.voice.bridge.route_types import BridgeRouteType


_BINDING_KEYS_V0: tuple[str, ...] = ("place_id", "destination_id", "target_id", "reference_id")


def _is_applicable(res: Any) -> bool:
    if res is None:
        return False
    bd = getattr(res, "bridge_decision", None)
    if bd is None:
        return False
    try:
        if getattr(bd, "route", None) != BridgeRouteType.TASK_LIFECYCLE:
            return False
    except Exception:
        return False
    prop = getattr(bd, "proposal", None)
    if prop is None:
        return False
    if str(getattr(prop, "task_action", "") or "").strip() != "start_navigation":
        return False
    md = getattr(res, "metadata", None) or {}
    if not isinstance(md, dict):
        return False
    cand = md.get("destination_candidate_v0")
    if not isinstance(cand, dict) or cand.get("candidate_present") is not True:
        return False
    return True


def _binding_key_seen_from_proposal(prop: Any) -> str:
    for k in _BINDING_KEYS_V0:
        try:
            v = getattr(prop, k, None)
        except Exception:
            v = None
        if v is not None and str(v).strip():
            return str(k)
    return ""


def _semantic_ambiguity_observation(event: Any) -> Tuple[bool, bool]:
    """
    Returns (has_ambiguities, requires_followup) from semantic_v2 if present.
    Observation-only: must not be used as binding evidence.
    """
    try:
        md = getattr(event, "metadata", None) or {}
        payload = md.get("luna_voice_semantic_v2")
        if not isinstance(payload, dict):
            return False, False
        amb = payload.get("ambiguities")
        has_amb = isinstance(amb, list) and len(amb) > 0
        rf = bool(payload.get("requires_followup") is True)
        return has_amb, rf
    except Exception:
        return False, False


def evaluate_destination_bound_check_v0(
    *,
    res: Any,
    event: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, check_dict).

    Applicable only when:
    - proposal.task_action == "start_navigation"
    - destination_candidate_v0.candidate_present == True
    """
    if not _is_applicable(res):
        return False, None

    bd = getattr(res, "bridge_decision", None)
    prop = getattr(bd, "proposal", None) if bd is not None else None
    binding_key_seen = _binding_key_seen_from_proposal(prop)

    has_amb, requires_followup = _semantic_ambiguity_observation(event)
    needs_confirmation = bool(has_amb or requires_followup)

    if not binding_key_seen:
        return True, {
            "bound_ready": False,
            "check_scope": "navigation_destination_bound_check_v0",
            "reason": "missing_binding_evidence",
        }

    return True, {
        # NOTE: true here means "future bound upgrade candidate is possible",
        # not "destination is already bound" and not "navigation may start".
        "bound_ready": True,
        "check_scope": "navigation_destination_bound_check_v0",
        "binding_key_seen": binding_key_seen,
        "needs_confirmation": bool(needs_confirmation),
    }

