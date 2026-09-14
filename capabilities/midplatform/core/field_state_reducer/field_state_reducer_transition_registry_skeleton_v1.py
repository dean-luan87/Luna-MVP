# -*- coding: utf-8 -*-
"""Field State Reducer transition registry skeleton v1."""

from __future__ import annotations

TRANSITION_GUARDS_SKELETON_V1 = {
    "revoked_to_active_allowed": False,
    "expired_to_active_without_new_event_allowed": False,
    "suspended_to_active_without_refresh_allowed": False,
    "superseded_to_active_allowed": False,
    "conflicted_to_active_without_resolution_allowed": False,
    "unresolved_to_active_without_sufficient_evidence_allowed": False,
    "transition_engine_implemented": False,
}
