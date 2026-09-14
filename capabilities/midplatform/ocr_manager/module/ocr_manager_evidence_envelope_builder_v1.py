from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence


def build_ocr_manager_evidence_envelope_v1(
    *,
    request_id: str,
    source_ref: str,
    raw_evidence: Sequence[Mapping[str, Any]],
    layout_candidates: Sequence[Mapping[str, Any]],
    reading_order_candidates: Sequence[Mapping[str, Any]],
    region_attribution_candidates: Sequence[Mapping[str, Any]],
    enhancement_candidates: Sequence[Mapping[str, Any]],
    correction_candidates: Sequence[Mapping[str, Any]],
    crossmodal_consistency_candidates: Sequence[Mapping[str, Any]],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    ambiguity_flags = []
    conflict_flags = []

    if any(bool(item.get("ambiguous_order")) for item in reading_order_candidates):
        ambiguity_flags.append("reading_order_ambiguous")
    if any(
        str(item.get("status") or "").startswith("unresolved")
        for item in crossmodal_consistency_candidates
    ):
        ambiguity_flags.append("crossmodal_unresolved")
    if any(
        str(item.get("status") or "") == "conflict_candidate"
        for item in crossmodal_consistency_candidates
    ):
        conflict_flags.append("crossmodal_conflict")
    if any(
        bool(item.get("unresolved_attribution"))
        for item in region_attribution_candidates
    ):
        ambiguity_flags.append("region_attribution_unresolved")

    return {
        "request_id": request_id,
        "evidence_envelope_id": f"ocr_envelope_{request_id}",
        "source_refs": (source_ref,),
        "engine_refs": tuple(
            sorted(
                {
                    str(item.get("engine_ref") or "")
                    for item in raw_evidence
                    if str(item.get("engine_ref") or "")
                }
            )
        ),
        "raw_evidence": tuple(raw_evidence),
        "layout_candidates": tuple(layout_candidates),
        "reading_order_candidates": tuple(reading_order_candidates),
        "region_attribution_candidates": tuple(region_attribution_candidates),
        "enhancement_candidates": tuple(enhancement_candidates),
        "correction_candidates": tuple(correction_candidates),
        "crossmodal_consistency_candidates": tuple(crossmodal_consistency_candidates),
        "ambiguity_flags": tuple(ambiguity_flags),
        "conflict_flags": tuple(conflict_flags),
        "provenance_refs": (source_ref, trace_ref, replay_key),
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "candidate_only": True,
        "not_fact": True,
    }
