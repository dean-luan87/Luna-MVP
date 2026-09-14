# -*- coding: utf-8 -*-
"""Field Continuity Detection — state machine v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Set, Tuple

ALLOWED_TRANSITIONS: Set[Tuple[str, str]] = {
    ("active", "shifted"), ("active", "occluded"), ("active", "lost"), ("active", "closed"),
    ("shifted", "active"), ("occluded", "active"), ("occluded", "lost"),
    ("lost", "recovering"), ("lost", "replaced"),
    ("recovering", "active"), ("recovering", "replaced"),
}


def validate_field_session_state_transition(from_state: str, to_state: str) -> Dict[str, Any]:
    allowed = (from_state, to_state) in ALLOWED_TRANSITIONS
    return {
        "transition_id": f"fst_{uuid.uuid4().hex[:12]}",
        "from_state": from_state,
        "to_state": to_state,
        "transition_allowed": allowed,
        "reason_codes": ["allowed_transition"] if allowed else ["invalid_transition_blocked"],
        "candidate_only": True,
    }
