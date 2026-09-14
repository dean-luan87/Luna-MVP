# -*- coding: utf-8 -*-
"""
Mid-Platform Dispatch Consumption Stub v0 (read-only).

Consumes only:
- need_navigation_routing_v0 (a read-only routing suggestion)

Hard boundaries:
- Not a decision maker; not an executor; does not switch chains.
- Does not fabricate routing results.
- Does not add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


def consume_mid_platform_dispatch_consumption_stub_v0(
    *,
    need_navigation_routing_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, observation_dict).

    relevant-only:
    - if need_navigation_routing_v0 missing/invalid => (False, None)
    """
    if not isinstance(need_navigation_routing_v0, dict) or not need_navigation_routing_v0:
        return False, None
    if str(need_navigation_routing_v0.get("routing_scope") or "") != "need_navigation_routing_v0":
        return False, None
    rd = str(need_navigation_routing_v0.get("routing_decision") or "").strip()
    if rd not in ("navigation_required", "navigation_not_required", "navigation_uncertain"):
        return False, None

    return True, {
        "consume_attempted": True,
        "consume_scope": "mid_platform_dispatch_consumption_stub_v0",
        "routing_decision_seen": rd,
        "consume_mode": "read_only",
    }

