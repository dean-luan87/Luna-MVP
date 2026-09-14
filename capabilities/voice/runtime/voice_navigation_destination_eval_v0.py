# -*- coding: utf-8 -*-
"""
Navigation destination sufficiency eval v0 (read-only).

Hard boundaries:
- Only evaluates explicit destination binding fields on the proposal object.
- Does NOT parse text into destination.
- Does NOT use semantic/memory/vision hints.
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_BINDING_KEYS_V0: tuple[str, ...] = ("place_id", "destination_id", "target_id", "reference_id")


def evaluate_destination_sufficiency_v0(proposal: Any) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, eval_dict).

    Applicable only when proposal.task_action == "start_navigation".
    """
    if proposal is None:
        return False, None

    task_action = str(getattr(proposal, "task_action", "") or "").strip()
    if task_action != "start_navigation":
        return False, None

    for k in _BINDING_KEYS_V0:
        try:
            v = getattr(proposal, k, None)
        except Exception:
            v = None
        if v is not None and str(v).strip():
            return True, {
                "destination_sufficient": True,
                "eval_scope": "navigation_destination_sufficiency_v0",
                "binding_key_seen": str(k),
            }

    return True, {
        "destination_sufficient": False,
        "eval_scope": "navigation_destination_sufficiency_v0",
        "reason": "missing_destination",
    }

