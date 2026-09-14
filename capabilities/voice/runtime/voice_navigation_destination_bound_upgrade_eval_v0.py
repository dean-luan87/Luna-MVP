# -*- coding: utf-8 -*-
"""
Navigation destination bound upgrade eval v0 (read-only evaluator).

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


def _semantic_ambiguity_observation(event: Any) -> Tuple[bool, bool]:
    """
    Returns (has_ambiguities, requires_followup) from semantic_v2 if present.
    Observation-only: cannot be used alone to pass eligibility.
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


def evaluate_destination_bound_upgrade_eval_v0(
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

    md = getattr(res, "metadata", None) or {}
    conf = md.get("destination_confirmation_fact_v0")
    bchk = md.get("destination_bound_check_v0")

    conf_ready = isinstance(conf, dict) and (conf.get("confirmation_ready") is True)
    bound_ready = isinstance(bchk, dict) and (bchk.get("bound_ready") is True)

    if not conf_ready:
        return True, {
            "eligible": False,
            "eval_scope": "navigation_destination_bound_upgrade_v0",
            "reason": "missing_confirmation_fact",
        }

    if not bound_ready:
        return True, {
            "eligible": False,
            "eval_scope": "navigation_destination_bound_upgrade_v0",
            "reason": "missing_binding_evidence",
        }

    # Optional observation field (must not gate eligibility alone).
    has_amb, requires_followup = _semantic_ambiguity_observation(event)
    needs_confirmation = False
    if isinstance(conf, dict) and isinstance(conf.get("needs_confirmation"), bool):
        needs_confirmation = needs_confirmation or bool(conf.get("needs_confirmation"))
    if isinstance(bchk, dict) and isinstance(bchk.get("needs_confirmation"), bool):
        needs_confirmation = needs_confirmation or bool(bchk.get("needs_confirmation"))
    needs_confirmation = needs_confirmation or bool(has_amb or requires_followup)

    out: Dict[str, Any] = {
        "eligible": True,
        "eval_scope": "navigation_destination_bound_upgrade_v0",
        "upgrade_scope": "future_bound_candidate_only",
    }
    # Keep minimal; attach only if we observed anything.
    if needs_confirmation:
        out["needs_confirmation"] = True
    return True, out

