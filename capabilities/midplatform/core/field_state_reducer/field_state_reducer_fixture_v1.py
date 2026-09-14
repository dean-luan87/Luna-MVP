# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton synthetic fixture v1."""

from __future__ import annotations

from typing import Dict, Tuple


def _event(
    event_id: str, event_type: str, payload: Dict[str, object]
) -> Dict[str, object]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "admitted": True,
        "synthetic": True,
        "production_data": False,
        "external_lookup_required": False,
        "provider_recall_required": False,
        "payload": payload,
    }


FIELD_STATE_REDUCER_FIXTURES_V1 = (
    _event("e01", "road_accessible_event", {"state": "road_accessible"}),
    _event("e02", "construction_notice_event", {"state": "construction_notice"}),
    _event("e03", "barrier_visual_event", {"state": "barrier_visual_detected"}),
    _event("e04", "road_blocked_event", {"state": "road_blocked"}),
    _event("e05", "temporary_passage_event", {"state": "temporary_passage"}),
    _event("e06", "conflict_event", {"state": "conflicting_signal"}),
    _event("e07", "overlay_expired_event", {"state": "overlay_expired"}),
    _event("e08", "refresh_evidence_event", {"state": "refresh_evidence_requested"}),
    _event("e09", "road_reopened_event", {"state": "road_reopened"}),
)


def build_xiaobeimen_construction_closure_fixture_v1() -> Tuple[Dict[str, object], ...]:
    return tuple(FIELD_STATE_REDUCER_FIXTURES_V1)
