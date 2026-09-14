"""Fail-closed user-terminal verifier for the Field projection integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "_eval_out/real_visual_evidence_to_field_state_candidate_projection_v1/runner_summary_v1.json"
PHASE = "Phase-P1-Luna-Real-Visual-Evidence-To-Field-State-Candidate-Projection-Integration-v1-001"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(row.get("case_id")): row for row in summary.get("cases", [])}


def _projection(row: Dict[str, Any]) -> Dict[str, Any]:
    return dict(row.get("projection") or {})


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = _cases(summary)
    positive = cases.get("REAL_VISUAL_EVIDENCE_TO_FIELD_CANDIDATE", {})
    unresolved = cases.get("UNRESOLVED_FIELD_REF_REMAINS_UNRESOLVED", {})
    unadmitted = cases.get("UNADMITTED_EVENT_CANNOT_MUTATE_REDUCER_STATE", {})
    absence = cases.get("DETECTION_ABSENCE_NOT_FIELD_ABSENCE", {})
    positive_projection = _projection(positive)
    unresolved_projection = _projection(unresolved)
    positive_admission = dict(positive.get("admission") or {})
    positive_reducer = dict(positive.get("reducer_result") or {})
    positive_state = dict(positive.get("field_state_candidate") or {})
    positive_behavior = dict(positive.get("behavior") or {})
    unadmitted_behavior = dict(unadmitted.get("behavior") or {})

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "required_cases", set(cases) >= {
        "REAL_VISUAL_EVIDENCE_TO_FIELD_CANDIDATE",
        "REAL_EVIDENCE_DOES_NOT_BECOME_FIELD_TRUTH",
        "UNRESOLVED_FIELD_REF_REMAINS_UNRESOLVED",
        "UNADMITTED_EVENT_CANNOT_MUTATE_REDUCER_STATE",
        "DETECTION_ABSENCE_NOT_FIELD_ABSENCE",
    })
    _check(checks, "real_provider_invoked", summary.get("provider_invoked") is True)
    _check(checks, "real_model_invoked", summary.get("model_invoked") is True)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False)
    _check(checks, "real_runtime_observation_present", bool(summary.get("runtime_observation_ref")))
    _check(checks, "real_visual_evidence_present", int(summary.get("real_visual_evidence_count", 0)) > 0)
    _check(checks, "real_bbox_present", len(positive_projection.get("bbox_candidate") or ()) == 4)
    dimensions = dict(summary.get("frame_dimensions") or {})
    _check(checks, "real_frame_dimensions_present", dimensions.get("width", 0) > 0 and dimensions.get("height", 0) > 0)
    _check(checks, "field_projection_candidate_created", bool(positive_projection.get("projection_ref")))
    _check(checks, "field_projection_traceable_to_real_evidence", bool(
        positive_projection.get("source_runtime_observation_ref")
        and positive_projection.get("source_evidence_refs")
        and positive_projection.get("source_detection_refs")
    ))
    _check(checks, "field_projection_candidate_only", positive_projection.get("candidate_only") is True)
    _check(checks, "field_ref_not_case_id_driven", positive_projection.get("field_ref_candidate") == "field:visual-frame:v1")
    _check(checks, "field_ref_not_detection_class_driven_without_contract", positive_projection.get("field_ref_candidate") != positive_projection.get("object_class_candidate"))
    _check(checks, "image_region_not_physical_field_region", positive_projection.get("region_semantics") == "DETECTION_REGION_CANDIDATE")
    _check(checks, "canonical_field_admission_respected", positive_admission.get("admission_status") == "admitted_event" and positive_admission.get("reducer_eligible") is True)
    _check(checks, "field_reducer_candidate_present", bool(positive_state) or positive_reducer.get("module_status") in {"no_state_change", "insufficient_evidence"})
    _check(checks, "unadmitted_event_not_reduced", unadmitted.get("reducer_result") is None and unadmitted_behavior.get("unadmitted_event_reduced") is False)
    _check(checks, "unresolved_field_ref_remains_unresolved", unresolved_projection.get("field_ref_resolution_status") == "UNRESOLVED" and not unresolved_projection.get("field_ref_candidate"))
    _check(checks, "absence_of_detection_not_field_absence", absence.get("projection", {}).get("field_ref_resolution_status") == "UNRESOLVED" and summary.get("field_truth_declared") is False)
    _check(checks, "field_reducer_authority_unchanged", positive_behavior.get("field_reducer_authority_unchanged") is True)
    _check(checks, "real_evidence_not_field_truth", summary.get("field_truth_declared") is False and positive_projection.get("truth_declared") is False)
    _check(checks, "real_evidence_not_world_truth", summary.get("world_truth_declared") is False)
    _check(checks, "no_target_semantic_resolution", summary.get("semantic_target_resolved") is False)
    forbidden = dict(summary.get("forbidden_behaviors") or {})
    for name in (
        "field_truth_promotion", "world_truth_declared", "field_mutation", "decision_execution",
        "task_execution", "action_execution", "device_control", "camera_control", "movement_control",
        "ocr_invocation", "slam_invocation",
    ):
        _check(checks, f"no_{name}", forbidden.get(name) is False)
    _check(checks, "candidate_only", summary.get("field_truth_declared") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    return {
        "phase": PHASE,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "operational_result": "PASS" if all(checks.values()) else "FAIL",
        "controlled_logic_result": "PASS" if all(checks.values()) else "FAIL",
        "final_decision": "GO" if all(checks.values()) else "NO-GO",
    }


def main() -> None:
    if not OUTPUT.exists():
        raise FileNotFoundError(f"Runner summary not found: {OUTPUT}")
    summary = json.loads(OUTPUT.read_text(encoding="utf-8"))
    result = _verify(summary)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
