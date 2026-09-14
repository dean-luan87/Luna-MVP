from __future__ import annotations

from typing import Any, Dict, Mapping


def build_observation_manager_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    evidence_intake: Mapping[str, Any],
    crossmodal: Mapping[str, Any],
    evidence_quality: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "observation_manager_diagnostics_v1",
        "observation_request_id": input_candidate.get("observation_request_id"),
        "request_type": input_candidate.get("request_type"),
        "module_status": module_status,
        "vision_evidence_count": len(evidence_intake.get("vision_evidence_refs") or ()),
        "ocr_evidence_count": len(evidence_intake.get("ocr_evidence_refs") or ()),
        "crossmodal_count": len(crossmodal.get("crossmodal_associations") or ()),
        "quality_score": evidence_quality.get("quality_score"),
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
