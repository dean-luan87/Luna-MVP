# -*- coding: utf-8 -*-
"""
Navigation start handoff v0 (minimal, observable).

Goal:
- Move beyond core_placeholder_v1 no-op by producing a structured handoff result.
- Does NOT execute real navigation unless required inputs are present.
- Does NOT fabricate destination/time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.voice.bridge.bridge_decision import BridgeDecision
from capabilities.voice.bridge.route_types import BridgeRouteType


def _as_nonempty_str(v: Any) -> str:
    s = str(v or "").strip()
    return s


def consume_destination_bound_v0_in_handoff_v0(
    decision: BridgeDecision,
    *,
    destination_bound_v0: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Consume a bound fact (read-only) for start_navigation.

    Hard boundaries:
    - Does NOT start real navigation.
    - Does NOT read candidate/confirmation/upgrade evals.
    - Does NOT fabricate any binding id.
    - Only acknowledges the already-materialized destination_bound_v0 fact.
    """
    if decision is None:
        return None
    if getattr(decision, "route", None) != BridgeRouteType.TASK_LIFECYCLE:
        return None
    prop = getattr(decision, "proposal", None)
    task_action = _as_nonempty_str(getattr(prop, "task_action", ""))
    if task_action != "start_navigation":
        return None
    if not isinstance(destination_bound_v0, dict) or not destination_bound_v0:
        return None
    if destination_bound_v0.get("destination_bound") is not True:
        return None
    bk = str(destination_bound_v0.get("binding_key") or "").strip()
    bv = str(destination_bound_v0.get("binding_value") or "").strip()
    if not bk or not bv:
        return None
    return {
        "bound_consumed": True,
        "consume_scope": "navigation_handoff_consume_bound_v0",
        "binding_key": bk,
        "binding_value": bv,
        "executor": "voice_navigation_handoff_v0",
    }


def attempt_navigation_start_handoff_v0(
    decision: BridgeDecision,
) -> Optional[Dict[str, Any]]:
    """
    Returns:
    - dict: when handoff_attempted (for start_navigation only)
    - None: when not applicable
    """
    if decision is None:
        return None
    if getattr(decision, "route", None) != BridgeRouteType.TASK_LIFECYCLE:
        return None

    prop = getattr(decision, "proposal", None)
    task_action = _as_nonempty_str(getattr(prop, "task_action", ""))
    if task_action != "start_navigation":
        return None

    # v0 minimal: we only attempt a real call when a destination is explicitly provided.
    # Current Stage-1 shortcut "开始导航" carries no destination -> must not fabricate.
    md = getattr(prop, "metadata", None) if prop is not None else None
    dest = ""
    if isinstance(md, dict):
        dest = _as_nonempty_str(md.get("destination") or md.get("end") or md.get("target") or "")

    if not dest:
        return {
            "handoff_attempted": True,
            "task_action": "start_navigation",
            "handoff_status": "not_ready",
            "executor": "voice_navigation_handoff_v0_stub",
            "reason": "missing_destination",
        }

    # If in the future an explicit destination is present, this is the narrowest safe place
    # to call a real navigation entrypoint. For v0, keep it conservative.
    return {
        "handoff_attempted": True,
        "task_action": "start_navigation",
        "handoff_status": "not_implemented",
        "executor": "voice_navigation_handoff_v0_stub",
        "reason": "destination_present_but_real_executor_not_wired",
    }

