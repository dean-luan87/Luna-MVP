from __future__ import annotations

from typing import Any, Mapping, Sequence


def decide_ocr_manager_module_status_v1(
    *,
    input_valid: bool,
    governance_admitted: bool,
    engine_ready: bool,
    raw_evidence_count: int,
    reading_order_ambiguous: bool,
    layout_available: bool,
    enhancement_count: int,
    correction_count: int,
    crossmodal_conflict: bool,
    envelope_ready: bool,
) -> str:
    if not input_valid:
        return "invalid_input"
    if not governance_admitted:
        return "request_rejected"
    if not engine_ready:
        return "engine_unavailable"
    if raw_evidence_count == 0:
        return "no_text_detected"
    if crossmodal_conflict:
        return "crossmodal_conflict"
    if reading_order_ambiguous:
        return "reading_order_ambiguous"
    if layout_available and not envelope_ready:
        return "degraded"
    if correction_count > 0:
        return "correction_candidate_ready"
    if enhancement_count > 0:
        return "enhancement_candidate_ready"
    if envelope_ready:
        return "structured_evidence_ready"
    return "raw_evidence_ready"


def build_ocr_manager_result_summary_v1(
    *,
    request_id: str,
    module_status: str,
    raw_evidence: Sequence[Mapping[str, Any]],
    envelope: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "request_id": request_id,
        "module_status": module_status,
        "raw_evidence_count": len(raw_evidence),
        "engine_refs": tuple(envelope.get("engine_refs") or ()),
        "ambiguity_flags": tuple(envelope.get("ambiguity_flags") or ()),
        "conflict_flags": tuple(envelope.get("conflict_flags") or ()),
    }
