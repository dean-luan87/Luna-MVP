from __future__ import annotations

from typing import Any, Dict


def build_read_projection_candidate_v1(
    *,
    reducer_run_id: str,
    field_id: str,
    state_type: str,
    state_candidate: Dict[str, Any] | None,
    reduction_summary: Dict[str, Any],
    conflict_status: str,
    overlay_status: str,
) -> Dict[str, Any] | None:
    if state_candidate is None:
        return None

    candidate_status = str(state_candidate.get("candidate_status", "candidate"))
    temporal_status = str(state_candidate.get("temporal_status", "unknown"))
    unresolved_reason = None
    if candidate_status in {"conflicted", "unresolved"}:
        unresolved_reason = candidate_status

    return {
        "projection_candidate_id": f"projection_{reducer_run_id}",
        "field_id": field_id,
        "state_type": state_type,
        "display_status": candidate_status,
        "candidate_value": dict(state_candidate.get("candidate_value", {})),
        "temporal_status": temporal_status,
        "confidence_band": "high"
        if float(state_candidate.get("confidence_snapshot", {}).get("confidence", 0.0))
        >= 0.75
        else "low",
        "conflict_status": conflict_status,
        "overlay_status": overlay_status,
        "freshness_status": "refresh_required"
        if reduction_summary.get("overlay_result", {}).get(
            "refresh_evidence_required", False
        )
        else "fresh",
        "source_summary": {
            "supporting_event_count": len(
                state_candidate.get("supporting_event_refs", [])
            ),
            "conflicting_event_count": len(
                state_candidate.get("conflicting_event_refs", [])
            ),
        },
        "provenance_summary": {
            "provenance_ref_count": len(state_candidate.get("provenance_refs", [])),
            "trace_ref": state_candidate.get("trace_ref", ""),
        },
        "unresolved_reason": unresolved_reason,
        "reducer_candidate_ref": state_candidate.get("state_candidate_id", ""),
        "projection_ready": candidate_status not in {"unresolved"},
        "persisted": False,
    }
