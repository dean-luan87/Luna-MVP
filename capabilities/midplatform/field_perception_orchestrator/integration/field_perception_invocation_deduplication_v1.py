from __future__ import annotations

from typing import Any, Dict, Mapping


def build_invocation_deduplication_v1(
    history_resolution: Mapping[str, Any],
) -> Dict[str, Any]:
    if history_resolution.get("active_match"):
        return {
            "deduplication_status": "duplicate_active_request",
            "duplicate_of": (history_resolution.get("active_match") or {}).get(
                "handoff_id"
            ),
            "deduplication_reason": "active_or_recent_invocation",
            "reuse_existing_result": False,
        }
    if history_resolution.get("fresh_match"):
        return {
            "deduplication_status": "fresh_evidence_reuse",
            "duplicate_of": (history_resolution.get("fresh_match") or {}).get(
                "handoff_id"
            ),
            "deduplication_reason": "fresh_evidence_available",
            "reuse_existing_result": True,
        }
    if history_resolution.get("recent_match"):
        return {
            "deduplication_status": "duplicate_recent_request",
            "duplicate_of": (history_resolution.get("recent_match") or {}).get(
                "handoff_id"
            ),
            "deduplication_reason": "recent_invocation_found",
            "reuse_existing_result": False,
        }
    return {
        "deduplication_status": "not_duplicate",
        "duplicate_of": None,
        "deduplication_reason": "no_matching_history",
        "reuse_existing_result": False,
    }
