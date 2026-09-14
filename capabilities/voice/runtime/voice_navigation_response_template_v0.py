# -*- coding: utf-8 -*-
"""
Navigation response templates v0 (minimal helpers).

Scope:
- Only a fixed response template for missing destination when start_navigation is requested.
- No map, no parsing, no memory/vision/semantic supplementation.
"""

from __future__ import annotations

from typing import Any

from capabilities.voice.bridge.route_types import BridgeRouteType


NAVIGATION_MISSING_DESTINATION_CONFIRM_TEMPLATE_V0: str = (
    "我现在还不能开始导航，因为你还没有告诉我目的地。请先告诉我你要去哪里。"
)


def should_trigger_navigation_missing_destination_confirm_v0(res: Any) -> bool:
    """
    Trigger iff ALL conditions are met (write-locked):
    1) dispatch_type == "short_controlled_input"
    2) bridge_decision.route == TASK_LIFECYCLE
    3) proposal.task_action == "start_navigation"
    4) result.metadata["destination_sufficiency_eval_v0"] exists
    5) destination_sufficient == False
    6) reason == "missing_destination"
    """
    if res is None:
        return False

    if str(getattr(res, "dispatch_type", "") or "") != "short_controlled_input":
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
    ev = md.get("destination_sufficiency_eval_v0")
    if not isinstance(ev, dict):
        return False

    if ev.get("destination_sufficient") is not False:
        return False
    if str(ev.get("reason") or "").strip() != "missing_destination":
        return False
    return True

