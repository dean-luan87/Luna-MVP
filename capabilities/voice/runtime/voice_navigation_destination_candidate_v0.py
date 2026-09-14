# -*- coding: utf-8 -*-
"""
Navigation destination candidate v0 (read-only carrier + minimal evaluator).

Hard boundaries:
- Does NOT parse place names.
- Does NOT call maps/search.
- Does NOT use memory/vision to fill destination.
- Does NOT upgrade to destination_bound.
- Does NOT write any time/space anchors.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

from capabilities.voice.bridge.route_types import BridgeRouteType


_PURE_CONTINUE_PHRASES: tuple[str, ...] = (
    "继续",
    "接着",
    "接着做",
    "按我说的做",
    "照我说的做",
    "别停",
    "不要停",
)


def _norm_for_short_phrase(s: str) -> str:
    t = str(s or "").strip()
    if not t:
        return ""
    t = re.sub(r"\s+", "", t)
    return t


def _candidate_text_from_event(event: Any) -> str:
    if event is None:
        return ""
    s = str(getattr(event, "wake_word_stripped", "") or "").strip()
    if not s:
        s = str(getattr(event, "normalized_text", "") or "").strip()
    return s


def _in_missing_destination_nav_context(res: Any) -> bool:
    """
    Strict context:
    1) res.dispatch_type == "short_controlled_input"
    2) bridge_decision.route == TASK_LIFECYCLE
    3) proposal.task_action == "start_navigation"
    4) res.metadata["destination_sufficiency_eval_v0"].destination_sufficient == False
    5) reason == "missing_destination"
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


def capture_destination_candidate_v0(
    *,
    event: Any,
    navigation_context_result: Any,
) -> Optional[Dict[str, Any]]:
    """
    Returns:
    - dict: when candidate captured under strict navigation missing-destination context
    - None: otherwise (non-applicable or not worth capturing)
    """
    if not _in_missing_destination_nav_context(navigation_context_result):
        return None

    cand = _candidate_text_from_event(event)
    if not cand:
        return None
    cand_norm = _norm_for_short_phrase(cand)
    if len(cand_norm) < 2:
        return None
    if cand_norm in {_norm_for_short_phrase(x) for x in _PURE_CONTINUE_PHRASES}:
        return None

    return {
        "candidate_present": True,
        "candidate_text": cand,
        "candidate_scope": "navigation_destination_candidate_v0",
        "requires_confirmation": True,
        "binding_reason": "candidate_captured_but_not_bound",
    }

