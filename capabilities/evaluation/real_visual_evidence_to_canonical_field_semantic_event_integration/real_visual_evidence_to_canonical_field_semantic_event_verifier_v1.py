"""Fail-closed user-terminal verifier for canonical semantic-event integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "_eval_out/real_visual_evidence_to_canonical_field_semantic_event_integration_v1/runner_summary_v1.json"
)
PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Canonical-Field-Semantic-Event-Integration-v1-001"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(row.get("case_id")): row for row in summary.get("cases", [])}


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = _cases(summary)
    positive = cases.get(
        "REAL_VISUAL_EVIDENCE_TO_CANONICAL_FIELD_SEMANTIC_EVENT", {}
    )
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
            "REAL_VISUAL_EVIDENCE_TO_CANONICAL_FIELD_SEMANTIC_EVENT",
            "DETECTION_CLASS_NOT_FIELD_TRUTH",
            "UNRESOLVED_SUBJECT_NOT_FORCED_TO_PRESENCE_TRUE",
            "SAME_PROVIDER_DETECTIONS_NOT_SOURCE_DIVERSITY",
            "SEMANTIC_EVENT_ADMISSION_NOT_FACT_ADMISSION",
            "INSUFFICIENT_EVIDENCE_REMAINS_FAIL_CLOSED",
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
    dimensions = dict(summary.get("frame_dimensions") or {})
    _check(checks, "real_frame_dimensions_present", dimensions.get("width", 0) > 0 and dimensions.get("height", 0) > 0)
    _check(checks, "real_bbox_present", len(semantic.get("source_detection_refs") or ()) > 0)
    _check(checks, "canonical_event_type", event.get("event_type") == "field_definition_observed")
    _check(checks, "canonical_event_type_compatible", behavior.get("canonical_event_type_compatible") is True)
    _check(checks, "semantic_event_candidate_created", bool(semantic.get("projection_ref")))
    _check(checks, "semantic_event_traceable", bool(
        semantic.get("source_visual_projection_ref")
        and semantic.get("source_runtime_observation_ref")
        and semantic.get("source_evidence_refs")
        and semantic.get("source_detection_refs")
    ))
    _check(checks, "semantic_event_candidate_only", behavior.get("semantic_event_candidate_only") is True)
    _check(checks, "semantic_state_unresolved", behavior.get("semantic_state_unresolved") is True)
    _check(checks, "no_presence_true_for_unresolved_subject", behavior.get("no_presence_true_for_unresolved_subject") is True and payload.get("semantic_value_candidate") is None)
    _check(checks, "detection_class_not_field_truth", behavior.get("detection_class_not_field_truth") is True and summary.get("field_truth_declared") is False)
    _check(checks, "target_binding_remains_unresolved", summary.get("semantic_target_resolved") is False and behavior.get("target_binding_unresolved") is True)
    _check(checks, "semantic_event_admission_present", admission.get("admission_status") == "admitted_event" and admission.get("reducer_eligible") is True)
    _check(checks, "semantic_event_admission_not_fact_admission", behavior.get("semantic_event_admission_not_fact_admission") is True and admission.get("fact_admitted") is False)
    _check(checks, "evidence_sufficiency_contract_unchanged", summary.get("evidence_sufficiency_contract") == {"minimum_event_count": 2, "source_diversity_requirement": 2})
    _check(checks, "insufficient_evidence_remains_fail_closed", reducer.get("module_status") == "insufficient_evidence" and reducer.get("selection_summary", {}).get("selection_status") == "no_eligible_candidate")
    _check(checks, "same_provider_detections_not_source_diversity", behavior.get("same_provider_detections_not_source_diversity") is True)
    _check(checks, "confidence_lineage_complete", summary.get("confidence_lineage_complete") is True and summary.get("source_visual_confidence") == summary.get("field_projection_confidence") == summary.get("semantic_event_confidence") == summary.get("reducer_measured_confidence"))
    _check(checks, "policy_trace_gap_explicitly_reported", summary.get("policy_trace_compatibility_gap") is True)
    _check(checks, "real_evidence_not_field_truth", summary.get("field_truth_declared") is False)
    _check(checks, "real_evidence_not_world_truth", summary.get("world_truth_declared") is False)
    _check(checks, "candidate_only", summary.get("field_truth_declared") is False and semantic.get("candidate_only") is True)
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
        "ocr_invocation",
        "slam_invocation",
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
