# -*- coding: utf-8 -*-
"""
Navigation destination bound v0 (minimal materialization; metadata-only).

Hard boundaries:
- Writes ONLY result.metadata["destination_bound_v0"].
- Does NOT start navigation; does NOT modify handoff/proposal/route/submit.
- Does NOT fabricate any binding id; only consumes existing proposal binding fields.
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.voice.bridge.route_types import BridgeRouteType


_BINDING_KEYS_V0: tuple[str, ...] = ("place_id", "destination_id", "target_id", "reference_id")


def _get_binding_from_proposal(prop: Any, preferred_key: str) -> Tuple[str, str]:
    keys = [str(preferred_key or "").strip()] if str(preferred_key or "").strip() else []
    for k in _BINDING_KEYS_V0:
        if k not in keys:
            keys.append(k)
    for k in keys:
        try:
            v = getattr(prop, k, None)
        except Exception:
            v = None
        if v is not None and str(v).strip():
            return str(k), str(v).strip()
    return "", ""


def _all_hard_prereqs_met(res: Any) -> bool:
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
    if not (isinstance(cand, dict) and cand.get("candidate_present") is True):
        return False

    conf = md.get("destination_confirmation_fact_v0")
    if not (isinstance(conf, dict) and conf.get("confirmation_ready") is True):
        return False

    bchk = md.get("destination_bound_check_v0")
    if not (isinstance(bchk, dict) and bchk.get("bound_ready") is True):
        return False

    uev = md.get("destination_bound_upgrade_eval_v0")
    if not (isinstance(uev, dict) and uev.get("eligible") is True):
        return False

    mev = md.get("destination_bound_materialization_eval_v0")
    if not (isinstance(mev, dict) and mev.get("materialize_ready") is True):
        return False

    # Extra safety: require actual binding value present on proposal.
    preferred_key = ""
    if isinstance(bchk, dict) and isinstance(bchk.get("binding_key_seen"), str):
        preferred_key = str(bchk.get("binding_key_seen") or "").strip()
    k, v = _get_binding_from_proposal(prop, preferred_key)
    if not k or not v:
        return False

    return True


def materialize_destination_bound_v0_if_allowed(
    *,
    res: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable_and_written, destination_bound_dict).

    Writes NOTHING unless all hard prerequisites are met.
    """
    if res is None:
        return False, None

    if not _all_hard_prereqs_met(res):
        return False, None

    bd = getattr(res, "bridge_decision", None)
    prop = getattr(bd, "proposal", None) if bd is not None else None
    md = getattr(res, "metadata", None) or {}
    bchk = md.get("destination_bound_check_v0") if isinstance(md, dict) else None
    preferred_key = ""
    if isinstance(bchk, dict) and isinstance(bchk.get("binding_key_seen"), str):
        preferred_key = str(bchk.get("binding_key_seen") or "").strip()
    binding_key, binding_value = _get_binding_from_proposal(prop, preferred_key)
    if not binding_key or not binding_value:
        return False, None

    return True, {
        "destination_bound": True,
        "binding_key": str(binding_key),
        "binding_value": str(binding_value),
        "binding_reason": "candidate_confirmed_and_materialization_ready",
        "bound_scope": "navigation_start_v0",
    }

