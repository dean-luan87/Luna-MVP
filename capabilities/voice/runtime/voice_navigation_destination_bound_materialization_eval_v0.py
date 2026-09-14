# -*- coding: utf-8 -*-
"""
Navigation destination bound materialization eval v0 (read-only evaluator).

Hard boundaries:
- Does NOT write destination_bound (no materialization).
- Does NOT change route/proposal/handoff/submit behavior.
- Does NOT parse places, does NOT call maps/search.
- Does NOT use memory/vision as binding evidence.
- Does NOT add any time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.voice.bridge.route_types import BridgeRouteType


_BINDING_KEYS_V0: tuple[str, ...] = ("place_id", "destination_id", "target_id", "reference_id")


def _semantic_blocker_observation(event: Any) -> Tuple[bool, bool]:
    """
    Returns (has_ambiguities, requires_followup) from semantic_v2 if present.
    Blocker-only: can veto materialization, must not be used to allow it.
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


def _binding_value_present(prop: Any) -> bool:
    if prop is None:
        return False
    for k in _BINDING_KEYS_V0:
        try:
            v = getattr(prop, k, None)
        except Exception:
            v = None
        if v is not None and str(v).strip():
            return True
    return False


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


def evaluate_destination_bound_materialization_eval_v0(
    *,
    res: Any,
    event: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, eval_dict).

    Applicable only when:
    - proposal.task_action == "start_navigation"
    - destination_candidate_v0.candidate_present == True
    """
    if not _is_applicable(res):
        return False, None

    bd = getattr(res, "bridge_decision", None)
    prop = getattr(bd, "proposal", None) if bd is not None else None
    md = getattr(res, "metadata", None) or {}

    cand = md.get("destination_candidate_v0")
    if not isinstance(cand, dict) or cand.get("candidate_present") is not True:
        # Shouldn't happen due to applicability, but keep defensive.
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "missing_candidate",
        }

    conf = md.get("destination_confirmation_fact_v0")
    conf_ready = isinstance(conf, dict) and (conf.get("confirmation_ready") is True)
    if not conf_ready:
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "missing_confirmation_fact",
        }

    bchk = md.get("destination_bound_check_v0")
    bound_ready = isinstance(bchk, dict) and (bchk.get("bound_ready") is True)
    if not bound_ready:
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "missing_binding_evidence",
        }

    uev = md.get("destination_bound_upgrade_eval_v0")
    upgrade_eligible = isinstance(uev, dict) and (uev.get("eligible") is True)
    if not upgrade_eligible:
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "missing_upgrade_eligibility",
        }

    # Extra sanity: require proposal explicit binding field to be present (No Fabrication).
    if not _binding_value_present(prop):
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "missing_binding_evidence",
        }

    # Hard blockers: needs_confirmation or semantic ambiguity/followup.
    needs_confirmation = False
    for key in (
        "destination_confirmation_fact_v0",
        "destination_bound_check_v0",
        "destination_bound_upgrade_eval_v0",
    ):
        v = md.get(key)
        if isinstance(v, dict) and v.get("needs_confirmation") is True:
            needs_confirmation = True
            break
    has_amb, requires_followup = _semantic_blocker_observation(event)
    if needs_confirmation or has_amb or requires_followup:
        return True, {
            "materialize_ready": False,
            "eval_scope": "navigation_destination_bound_materialization_v0",
            "reason": "confirmation_or_ambiguity_blocker",
        }

    return True, {
        "materialize_ready": True,
        "eval_scope": "navigation_destination_bound_materialization_v0",
        "materialization_scope": "future_bound_materialization_candidate_only",
    }

