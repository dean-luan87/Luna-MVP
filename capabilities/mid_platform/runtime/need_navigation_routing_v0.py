# -*- coding: utf-8 -*-
"""
Need-Navigation Routing v0 (read-only suggestion layer).

Hard boundaries:
- Only emits a routing suggestion; does NOT change route/proposal/behavior.
- Does NOT trigger navigation execution.
- Does NOT add time/space anchors; does NOT depend on maps.
- Conservative: insufficient info => navigation_uncertain.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


_NON_NAV_TASK_ACTIONS_V0: Tuple[str, ...] = (
    "end_task",
    "switch_task",
    "pause_task",
    "resume_task",
)


def _as_str(x: Any) -> str:
    return str(x or "").strip()


def _slice_types(md: Dict[str, Any]) -> List[str]:
    s = md.get("vision_consumable_slices_v0")
    if isinstance(s, dict):
        st = _as_str(s.get("slice_type"))
        return [st] if st else []
    if isinstance(s, list):
        out: List[str] = []
        for it in s:
            if isinstance(it, dict):
                st = _as_str(it.get("slice_type"))
                if st:
                    out.append(st)
        # de-dup keep order
        seen = set()
        out2: List[str] = []
        for t in out:
            if t in seen:
                continue
            seen.add(t)
            out2.append(t)
        return out2
    return []


def _candidate_types(md: Dict[str, Any]) -> List[str]:
    c = md.get("vision_interpretation_candidates_v0")
    if isinstance(c, dict):
        ct = _as_str(c.get("candidate_type"))
        return [ct] if ct else []
    if isinstance(c, list):
        out: List[str] = []
        for it in c:
            if isinstance(it, dict):
                ct = _as_str(it.get("candidate_type"))
                if ct:
                    out.append(ct)
        seen = set()
        out2: List[str] = []
        for t in out:
            if t in seen:
                continue
            seen.add(t)
            out2.append(t)
        return out2
    return []


def evaluate_need_navigation_routing_v0(
    *,
    proposal: Any,
    route: Any,
    raw_text: str,
    runtime_context_metadata: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Returns a minimal suggestion dict (always).
    """
    md = runtime_context_metadata or {}

    task_action = _as_str(getattr(proposal, "task_action", ""))
    route_s = _as_str(getattr(route, "value", route))
    _ = route_s  # reserved for future observation use without changing behavior
    _ = _as_str(raw_text)  # reserved; do not parse semantics here

    # 1) Explicit task action takes priority.
    if task_action == "start_navigation":
        return {
            "routing_decision": "navigation_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "explicit_navigation_task_action",
        }
    if task_action in _NON_NAV_TASK_ACTIONS_V0:
        return {
            "routing_decision": "navigation_not_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "explicit_non_navigation_task_action",
        }

    # 2) Vision hints (conservative; only accept an explicit nav-related slice type).
    st = _slice_types(md)
    if "navigation_need_candidate" in st:
        return {
            "routing_decision": "navigation_required",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "vision_navigation_need_slice",
        }

    # 3) Otherwise, keep conservative.
    ct = _candidate_types(md)
    if ct:
        return {
            "routing_decision": "navigation_uncertain",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "vision_candidates_present_but_not_navigation_specific",
        }
    if st:
        return {
            "routing_decision": "navigation_uncertain",
            "routing_scope": "need_navigation_routing_v0",
            "reason": "vision_slices_present_but_not_navigation_specific",
        }
    return {
        "routing_decision": "navigation_uncertain",
        "routing_scope": "need_navigation_routing_v0",
        "reason": "insufficient_task_and_vision_signals",
    }

