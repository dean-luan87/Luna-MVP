"""Fail-closed user-terminal verifier for L1 subject-candidate binding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "_eval_out/real_visual_evidence_to_cognitive_entity_subject_binding_integration_v1/runner_summary_v1.json"
)
PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Cognitive-Entity-Subject-Binding-Integration-v1-001"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(row.get("case_id")): row for row in summary.get("cases", [])}


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = _cases(summary)
    positive = cases.get("REAL_VISUAL_EVIDENCE_TO_ENTITY_SUBJECT_CANDIDATE", {})
    entity = dict(positive.get("entity_candidate") or {})
    binding = dict(positive.get("subject_binding") or {})
    semantic = dict(positive.get("semantic_projection") or {})
    event = dict(positive.get("semantic_event_candidate") or {})
    payload = dict(event.get("payload") or {})
    admission = dict(positive.get("admission") or {})
    reducer = dict(positive.get("reducer_result") or {})
    behavior = dict(positive.get("behavior") or {})

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(
        checks,
        "required_cases",
        set(cases)
        >= {
            "REAL_VISUAL_EVIDENCE_TO_ENTITY_SUBJECT_CANDIDATE",
            "DETECTION_CLASS_NOT_ENTITY_IDENTITY",
            "SAME_CLASS_DETECTIONS_NOT_SAME_ENTITY",
            "ENTITY_CANDIDATE_NOT_PHYSICAL_IDENTITY",
            "ENTITY_CANDIDATE_NOT_TARGET_BINDING",
            "SUBJECT_CANDIDATE_NOT_PRESENCE_TRUE",
            "SUBJECT_BINDING_NOT_FACT_ADMISSION",
            "ENTITY_CANDIDATE_NOT_SOURCE_DIVERSITY",
            "ENTITY_CANDIDATE_NOT_MEMORY_IDENTITY",
        },
    )
    _check(checks, "real_provider_invoked", summary.get("provider_invoked") is True)
    _check(checks, "real_model_invoked", summary.get("model_invoked") is True)
    _check(
        checks,
        "recorded_provider_result_not_used",
        summary.get("recorded_provider_result_used") is False,
    )
    _check(checks, "real_runtime_observation_present", bool(summary.get("runtime_observation_ref")))
    _check(checks, "real_visual_evidence_present", int(summary.get("real_visual_evidence_count", 0)) > 0)
    _check(checks, "real_bbox_present", bool(entity.get("attributes", {}).get("bbox_observation_geometry")))
    dimensions = dict(summary.get("frame_dimensions") or {})
    _check(
        checks,
        "real_frame_dimensions_present",
        _positive_number(dimensions.get("width"))
        and _positive_number(dimensions.get("height")),
    )
    _check(checks, "entity_candidate_created", bool(entity.get("entity_id")))
    _check(checks, "entity_candidate_contract_reused", entity.get("candidate_only") is True and entity.get("fact_admitted") is False)
    _check(checks, "entity_candidate_has_evidence_provenance", bool(entity.get("evidence_refs") and entity.get("observation_refs") and entity.get("provenance_refs")))
    _check(checks, "subject_binding_candidate_created", binding.get("binding_status") == "CANDIDATE_BOUND")
    _check(checks, "subject_binding_traceable", bool(binding.get("source_runtime_observation_ref") and binding.get("source_evidence_refs") and binding.get("source_detection_refs") and binding.get("provenance_refs")))
    _check(checks, "subject_binding_candidate_only", binding.get("candidate_only") is True and binding.get("fact_admitted") is False)
    _check(checks, "subject_ref_candidate_populated", payload.get("subject_ref_candidate") == entity.get("entity_id"))
    _check(checks, "subject_reference_layer_l1", summary.get("subject_reference_layer") == "L1" and payload.get("subject_reference_layer") == "L1")
    _check(checks, "resolved_subject_layer_not_entered", summary.get("resolved_subject_layer_entered") is False)
    _check(checks, "persistent_identity_layer_not_entered", summary.get("persistent_identity_layer_entered") is False)
    _check(checks, "identity_resolution_unresolved", behavior.get("identity_resolution_unresolved") is True and binding.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "semantic_state_remains_unresolved", summary.get("semantic_state_resolution_status") == "UNRESOLVED" and payload.get("semantic_value_candidate") is None)
    _check(checks, "subject_candidate_not_presence_true", behavior.get("subject_candidate_not_presence_true") is True and payload.get("semantic_value_candidate") is None)
    _check(checks, "target_binding_remains_unresolved", summary.get("semantic_target_resolved") is False and summary.get("target_binding_status") == "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE")
    _check(checks, "semantic_event_admission_present", admission.get("admission_status") == "admitted_event" and admission.get("reducer_eligible") is True)
    _check(checks, "semantic_event_admission_not_fact_admission", behavior.get("semantic_event_admission_not_fact_admission") is True and admission.get("fact_admitted") is False)
    _check(checks, "evidence_sufficiency_contract_unchanged", summary.get("evidence_sufficiency_contract") == {"minimum_event_count": 2, "source_diversity_requirement": 2})
    _check(checks, "insufficient_evidence_remains_fail_closed", reducer.get("module_status") == "insufficient_evidence" and reducer.get("selection_summary", {}).get("selection_status") == "no_eligible_candidate")
    _check(checks, "entity_candidate_not_source_diversity", behavior.get("entity_candidate_not_source_diversity") is True)
    _check(checks, "same_class_detections_not_same_entity", cases.get("SAME_CLASS_DETECTIONS_NOT_SAME_ENTITY", {}).get("behavior", {}).get("same_class_detections_not_same_entity") is True)
    _check(checks, "detection_class_not_entity_identity", behavior.get("detection_class_not_entity_identity") is True)
    _check(checks, "entity_candidate_not_target_binding", behavior.get("entity_candidate_not_target_binding") is True)
    _check(checks, "subject_binding_not_fact_admission", behavior.get("subject_binding_not_fact_admission") is True)
    _check(checks, "entity_candidate_not_memory_identity", behavior.get("entity_candidate_not_memory_identity") is True)
    _check(checks, "confidence_lineage_complete", summary.get("confidence_lineage_complete") is True and summary.get("source_visual_confidence") == summary.get("field_projection_confidence") == summary.get("semantic_event_confidence") == summary.get("reducer_measured_confidence"))
    _check(checks, "visual_confidence_not_identity_confidence", entity.get("attributes", {}).get("identity_resolution_status") == "UNRESOLVED" and "identity_resolution_confidence" not in entity.get("attributes", {}))
    _check(checks, "policy_trace_gap_preserved", summary.get("policy_trace_compatibility_gap") is True)
    _check(checks, "candidate_only", summary.get("field_truth_declared") is False and summary.get("world_truth_declared") is False and summary.get("resolved_subject_layer_entered") is False)
    forbidden = dict(summary.get("forbidden_behaviors") or {})
    for name in (
        "field_truth_promotion",
        "world_truth_declared",
        "field_mutation",
        "decision_execution",
        "task_execution",
        "action_execution",
        "device_control",
        "camera_control",
        "movement_control",
        "memory_mutation",
        "pcn_mutation",
    ):
        _check(checks, f"no_{name}", forbidden.get(name) is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    return {
        "phase": PHASE,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "operational_result": "PASS" if all(checks.values()) else "FAIL",
        "cognitive_logic_result": "PASS" if all(checks.values()) else "FAIL",
        "final_decision": "GO" if all(checks.values()) else "NO-GO",
    }


def main() -> None:
    if not OUTPUT.exists():
        raise FileNotFoundError(f"Runner summary not found: {OUTPUT}")
    summary = json.loads(OUTPUT.read_text(encoding="utf-8"))
    print(json.dumps(_verify(summary), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
