# -*- coding: utf-8 -*-
"""
Navigation destination confirmation fact v0 (read-only checker).

Hard boundaries:
- Does NOT write destination_bound.
- Does NOT change route/proposal/handoff/submit behavior.
- Does NOT parse places, does NOT call maps/search.
- Does NOT use memory/vision as confirmation evidence.
- Does NOT add any time/space anchors.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

from capabilities.voice.bridge.route_types import BridgeRouteType


_CONFIRM_PHRASES_NORM: tuple[str, ...] = ("对", "是", "是的", "没错", "对就是这个")
_NEGATIVE_PHRASES_NORM: tuple[str, ...] = ("不是", "不对", "不要")


def _norm_text(s: str) -> str:
    t = str(s or "").strip()
    if not t:
        return ""
    # remove whitespace and common punctuation to keep matching conservative
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[，,。.!！?？；;、】【()\[\]{}“”\"'`]", "", t)
    return t


def _text_from_event(event: Any) -> str:
    if event is None:
        return ""
    s = str(getattr(event, "wake_word_stripped", "") or "").strip()
    if not s:
        s = str(getattr(event, "normalized_text", "") or "").strip()
    if not s:
        s = str(getattr(event, "raw_text", "") or "").strip()
    return s


def _semantic_observation(event: Any) -> Tuple[str, bool, bool]:
    """
    Returns (intent, has_ambiguities, requires_followup) from semantic_v2 if present.
    Observation-only: cannot be used alone to pass confirmation.
    """
    try:
        md = getattr(event, "metadata", None) or {}
        payload = md.get("luna_voice_semantic_v2")
        if not isinstance(payload, dict):
            return "", False, False
        intent = str(payload.get("intent") or "").strip()
        amb = payload.get("ambiguities")
        has_amb = isinstance(amb, list) and len(amb) > 0
        rf = bool(payload.get("requires_followup") is True)
        return intent, has_amb, rf
    except Exception:
        return "", False, False


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


def evaluate_destination_confirmation_fact_check_v0(
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

    text = _text_from_event(event)
    t = _norm_text(text)
    if not t:
        return True, {
            "confirmation_ready": False,
            "check_scope": "navigation_destination_confirmation_fact_v0",
            "reason": "no_confirmation_signal",
        }

    # Negative / rejection signal wins (conservative).
    if t in _NEGATIVE_PHRASES_NORM:
        return True, {
            "confirmation_ready": False,
            "check_scope": "navigation_destination_confirmation_fact_v0",
            "reason": "negative_or_rejection_signal",
        }

    # Minimal confirmation phrase match (conservative, small set).
    if t not in _CONFIRM_PHRASES_NORM:
        return True, {
            "confirmation_ready": False,
            "check_scope": "navigation_destination_confirmation_fact_v0",
            "reason": "no_confirmation_signal",
        }

    _intent, has_amb, requires_followup = _semantic_observation(event)
    needs_confirmation = bool(has_amb or requires_followup)

    return True, {
        # NOTE: true here means "future confirmation fact candidate is possible",
        # not "confirmation is completed as a bound fact" and not "navigation may start".
        "confirmation_ready": True,
        "check_scope": "navigation_destination_confirmation_fact_v0",
        "confirmation_target": "current_destination_candidate",
        "needs_confirmation": bool(needs_confirmation) or True,
    }

