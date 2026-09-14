from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_candidate_v1(
    input_candidate: Mapping[str, Any],
    scene_context: Mapping[str, Any],
    region_plan: Mapping[str, Any],
    evidence_intake: Mapping[str, Any],
    crossmodal: Mapping[str, Any],
    temporal_snapshot: Mapping[str, Any],
    evidence_quality: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    request_id = str(input_candidate.get("observation_request_id") or "")
    candidate_id = f"obs_cand_{request_id or 'unknown'}"
    conflict_reasons = []
    if evidence_intake.get("evidence_conflicted"):
        conflict_reasons.append("cross_source_conflict")
    uncertainty_reasons = []
    if evidence_quality.get("quality_level") == "low":
        uncertainty_reasons.append("low_evidence_quality")

    return {
        "schema_version": "observation_manager_candidate_v1",
        "candidate_id": candidate_id,
        "observation_request_id": request_id,
        "task_id": input_candidate.get("task_id"),
        "scene_id": (scene_context.get("scene_context") or {}).get("scene_id")
        or (scene_context.get("scene_context") or {}).get("scene_context_ref"),
        "observation_type": input_candidate.get("request_type"),
        "subject_refs": tuple(
            (input_candidate.get("task_context") or {}).get("subject_refs") or ()
        ),
        "region_refs": tuple(
            (region_plan.get("region_plan") or {}).get("region_refs") or ()
        ),
        "vision_evidence_refs": tuple(
            evidence_intake.get("vision_evidence_refs") or ()
        ),
        "ocr_evidence_refs": tuple(evidence_intake.get("ocr_evidence_refs") or ()),
        "crossmodal_association_refs": tuple(
            assoc.get("association_id")
            for assoc in (crossmodal.get("crossmodal_associations") or ())
        ),
        "temporal_snapshot_ref": temporal_snapshot.get("temporal_snapshot_ref"),
        "quality_score": evidence_quality.get("quality_score"),
        "confidence_candidate": evidence_quality.get("confidence_candidate"),
        "uncertainty_reasons": tuple(uncertainty_reasons),
        "conflict_reasons": tuple(conflict_reasons),
        "human_correction_refs": tuple(
            input_candidate.get("human_correction_refs") or ()
        ),
        "source_chain": "observation_manager_module_v1",
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "candidate_only": True,
        **not_fact(),
    }
