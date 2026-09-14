"""Fail-closed static verifier for the real visual situated-state projection."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict

from .real_visual_situated_state_source_runner_v1 import OUTPUT_DIR


PHASE = "Phase-P1-Luna-Real-Visual-Situated-State-Source-Integration-v1-001"
DEFAULT_SUMMARY = OUTPUT_DIR / "runner_summary_v1.json"
CONDITION_VISIBLE = "condition:target-visible:v1"
CONDITION_COMPLETE = "condition:target-complete:v1"
CONDITION_SCALE = "condition:target-scale-adequate:v1"
CONDITION_STABLE = "condition:stable-relation:v1"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _case(summary: Dict[str, Any], case_id: str) -> Dict[str, Any]:
    for item in summary.get("cases") or ():
        if item.get("case_id") == case_id:
            return item
    return {}


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    source = summary.get("visual_source") or {}
    binding = summary.get("target_binding") or {}
    perception = (_case(summary, "UNKNOWN_CONDITION_FAILS_CLOSED").get("perception") or {})
    precondition = (_case(summary, "UNKNOWN_CONDITION_FAILS_CLOSED").get("precondition_result") or {})
    candidates = perception.get("condition_candidates") or ()
    by_ref = {item.get("condition_ref"): item for item in candidates}
    feasibility = precondition.get("feasibility") or {}
    opportunity = precondition.get("opportunity") or {}
    eligibility = precondition.get("eligibility") or {}
    required = set((precondition.get("minimum_condition_requirement") or {}).get("required_condition_refs") or ())

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "real_execution_attempted", summary.get("provider_real_execution_attempted") is True)
    _check(checks, "real_execution_verified", summary.get("provider_real_execution_verified") is True)
    _check(checks, "real_visual_provider_invoked", summary.get("provider_invoked") is True)
    _check(checks, "real_model_invoked", summary.get("model_invoked") is True)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False)
    _check(checks, "canonical_provider_model", summary.get("selected_provider") == "provider:yolo:local:v1" and summary.get("model_ref") == "model-asset:yolo11n:weights-v1")
    _check(checks, "real_frame_dimensions_present", source.get("frame_width", 0) > 0 and source.get("frame_height", 0) > 0)
    _check(checks, "real_bbox_present", isinstance(source.get("bbox"), list) and len(source.get("bbox")) == 4)
    _check(checks, "target_binding_candidate_only", binding.get("candidate_only") is True and binding.get("semantic_target_resolved") is False)
    _check(checks, "target_visible_derived_from_real_detection", bool(summary.get("detection_ref")) and by_ref.get(CONDITION_VISIBLE, {}).get("status") == "SATISFIED")
    bbox = source.get("bbox") or []
    width = source.get("frame_width")
    height = source.get("frame_height")
    geometry_complete = (
        len(bbox) == 4
        and width
        and height
        and 0 <= bbox[0] < bbox[2] <= width
        and 0 <= bbox[1] < bbox[3] <= height
    )
    _check(checks, "completeness_derived_from_bbox_frame_geometry", source.get("target_completeness_candidate") == ("COMPLETE" if geometry_complete else "UNKNOWN"))
    metrics = source.get("target_scale_metrics") or {}
    expected_metrics = {
        "width_ratio": (bbox[2] - bbox[0]) / width if len(bbox) == 4 and width else None,
        "height_ratio": (bbox[3] - bbox[1]) / height if len(bbox) == 4 and height else None,
        "area_ratio": ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / (width * height) if len(bbox) == 4 and width and height else None,
    }
    _check(checks, "scale_metrics_derived_from_bbox_frame_geometry", set(metrics) == set(expected_metrics) and all(expected_metrics[key] is not None and math.isclose(float(metrics[key]), expected_metrics[key], rel_tol=1e-9, abs_tol=1e-12) for key in expected_metrics))
    _check(checks, "no_invented_scale_threshold", source.get("target_scale_condition_status") == "UNKNOWN" and by_ref.get(CONDITION_SCALE, {}).get("status") == "UNKNOWN")
    _check(checks, "single_frame_stable_relation_unknown", source.get("stable_relation_status") == "UNKNOWN" and by_ref.get(CONDITION_STABLE, {}).get("status") == "UNKNOWN")
    _check(checks, "unknown_condition_does_not_become_satisfied", CONDITION_STABLE in required and CONDITION_STABLE not in set(feasibility.get("satisfied_condition_refs") or ()))
    _check(checks, "unknown_required_condition_fails_feasibility", CONDITION_STABLE in set(feasibility.get("unknown_condition_refs") or ()) and feasibility.get("status") == "NOT_FEASIBLE")
    _check(checks, "unknown_required_condition_closes_opportunity", opportunity.get("status") == "CLOSED")
    _check(checks, "unknown_required_condition_blocks_eligibility", eligibility.get("eligible_now") is False)
    _check(checks, "absence_of_detection_not_world_absence", not any(item.get("status") == "UNSATISFIED" for item in candidates if item.get("condition_ref") == CONDITION_VISIBLE) or bool(summary.get("detection_ref")))
    signatures = {
        tuple((candidate.get("condition_ref"), candidate.get("status")) for candidate in (item.get("perception") or {}).get("condition_candidates") or ())
        for item in summary.get("cases") or ()
    }
    _check(checks, "condition_status_not_case_id_driven", len(signatures) == 1 and all((item.get("perception") or {}).get("case_id") == "REAL_VISUAL_SITUATED_STATE_SOURCE" for item in summary.get("cases") or ()))
    _check(checks, "condition_status_not_cycle_index_driven", len({(item.get("perception") or {}).get("cycle_index") for item in summary.get("cases") or ()}) == 1)
    _check(checks, "candidate_only", summary.get("target_binding", {}).get("candidate_only") is True and source.get("candidate_only") is True)
    forbidden = summary.get("forbidden_behaviors") or {}
    _check(checks, "no_world_truth", forbidden.get("world_truth_declared") is False)
    _check(checks, "no_field_mutation", forbidden.get("field_mutation") is False)
    _check(checks, "no_decision_execution", forbidden.get("decision_execution") is False)
    _check(checks, "no_task_execution", forbidden.get("task_execution") is False)
    _check(checks, "no_action_execution", forbidden.get("action_execution") is False)
    _check(checks, "no_device_control", forbidden.get("device_control") is False)
    _check(checks, "no_camera_control", forbidden.get("camera_control") is False)
    _check(checks, "no_movement_control", forbidden.get("movement_control") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    _check(checks, "traceability_complete", bool(summary.get("provider_request_ref")) and bool(summary.get("provider_result_ref")) and bool(summary.get("runtime_observation_ref")) and bool(summary.get("gateway_admission_ref")) and bool(summary.get("evidence_refs")) and bool(source.get("trace_refs")) and bool(source.get("provenance_refs")))

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "all_checks_passed": not failed,
        "check_count": len(checks),
        "checks": checks,
        "failed_checks": failed,
        "controlled_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "phase": PHASE,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify real visual situated-state source integration output.")
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    args = parser.parse_args()
    path = Path(args.summary)
    if not path.is_file():
        print(json.dumps({"all_checks_passed": False, "failed_checks": [f"summary_not_found:{path}"]}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
