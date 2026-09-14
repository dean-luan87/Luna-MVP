from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
    CAPABILITY_ID,
)


def resolve_observation_manager_module_status_v1(
    input_candidate: Mapping[str, Any],
    request_classification: Mapping[str, Any],
    task_context: Mapping[str, Any],
    temporal_snapshot: Mapping[str, Any],
    vision_adapter: Mapping[str, Any],
    ocr_adapter: Mapping[str, Any],
    evidence_intake: Mapping[str, Any],
    evidence_quality: Mapping[str, Any],
) -> str:
    if not input_candidate.get("observation_request_id"):
        return "invalid_input"
    if not request_classification.get("request_type_supported"):
        return "invalid_input"
    if input_candidate.get("source_constraints", {}).get("request_rejected", False):
        return "request_rejected"
    if not task_context.get("task_context_present"):
        return "context_incomplete"
    if not temporal_snapshot.get("temporal_snapshot_present"):
        return "context_incomplete"
    if request_classification.get("no_observation_required"):
        return "no_observation_required"
    if evidence_intake.get("evidence_conflicted"):
        return "evidence_conflicted"

    vision_req = bool(vision_adapter.get("vision_request_candidate_present"))
    ocr_req = bool(ocr_adapter.get("ocr_request_candidate_present"))
    vision_ev = bool(evidence_intake.get("vision_evidence_present"))
    ocr_ev = bool(evidence_intake.get("ocr_evidence_present"))

    if not evidence_intake.get("evidence_sufficient_hint", True):
        return "evidence_insufficient"
    if (vision_req or ocr_req) and not (vision_ev or ocr_ev):
        return "evidence_requested"
    if (vision_req and not vision_ev) or (ocr_req and not ocr_ev):
        return "evidence_partial"
    if evidence_quality.get("quality_level") == "low":
        return "degraded"
    return "observation_candidate_ready"


def build_observation_manager_module_output_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    task_context: Mapping[str, Any],
    scene_context: Mapping[str, Any],
    attention_plan: Mapping[str, Any],
    region_plan: Mapping[str, Any],
    vision_adapter: Mapping[str, Any],
    ocr_adapter: Mapping[str, Any],
    evidence_intake: Mapping[str, Any],
    crossmodal: Mapping[str, Any],
    temporal_snapshot: Mapping[str, Any],
    evidence_quality: Mapping[str, Any],
    observation_candidate: Mapping[str, Any] | None,
    admission_handoff: Mapping[str, Any] | None,
    diagnostics: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
    rejection_reasons: tuple[str, ...],
) -> Dict[str, Any]:
    output = {
        "capability_id": CAPABILITY_ID,
        "module_status": module_status,
        "observation_request_id": input_candidate.get("observation_request_id"),
        "request_type": input_candidate.get("request_type"),
        "task_context_ref": task_context.get("task_context_ref"),
        "scene_context_ref": scene_context.get("scene_context_ref"),
        "attention_plan": attention_plan.get("attention_plan"),
        "region_plan": region_plan.get("region_plan"),
        "vision_request_candidate": vision_adapter.get("vision_request_candidate"),
        "ocr_request_candidate": ocr_adapter.get("ocr_request_candidate"),
        "vision_evidence_refs": tuple(
            evidence_intake.get("vision_evidence_refs") or ()
        ),
        "ocr_evidence_refs": tuple(evidence_intake.get("ocr_evidence_refs") or ()),
        "crossmodal_associations": tuple(
            crossmodal.get("crossmodal_associations") or ()
        ),
        "temporal_snapshot": temporal_snapshot.get("temporal_snapshot"),
        "evidence_quality": {
            "quality_score": evidence_quality.get("quality_score"),
            "confidence_candidate": evidence_quality.get("confidence_candidate"),
            "quality_level": evidence_quality.get("quality_level"),
        },
        "observation_candidate": observation_candidate,
        "permission_admission_handoff_candidate": admission_handoff,
        "diagnostics": diagnostics,
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "rejection_reasons": tuple(rejection_reasons),
        "boundary_flags": {field: False for field in BOUNDARY_FALSE_FIELDS},
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
    for field in BOUNDARY_FALSE_FIELDS:
        output[field] = False
    return output
