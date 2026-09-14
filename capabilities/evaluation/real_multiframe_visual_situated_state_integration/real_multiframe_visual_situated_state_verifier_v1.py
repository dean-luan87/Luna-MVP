"""Fail-closed verifier for real multi-frame visual candidate integration."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict

from .real_multiframe_visual_situated_state_runner_v1 import DEFAULT_SOURCE, OUTPUT_DIR


PHASE = "Phase-P1-Luna-Real-MultiFrame-Visual-Situated-State-Integration-v1-001"
DEFAULT_SUMMARY = OUTPUT_DIR / "runner_summary_v1.json"
STABLE = "condition:stable-relation:v1"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _geometry(frame: Dict[str, Any]) -> Dict[str, Any] | None:
    bbox = frame.get("bbox") or []
    width = frame.get("frame_width")
    height = frame.get("frame_height")
    if len(bbox) != 4 or not width or not height:
        return None
    x1, y1, x2, y2 = bbox
    return {
        "center": ((x1 + x2) / 2.0 / width, (y1 + y2) / 2.0 / height),
        "size": ((x2 - x1) / width, (y2 - y1) / height),
        "area": ((x2 - x1) * (y2 - y1)) / (width * height),
    }


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    observations = summary.get("observations") or []
    association = summary.get("association") or {}
    metrics = summary.get("temporal_metrics") or {}
    stability = summary.get("stability") or {}
    preconditions = summary.get("precondition_results") or []
    forbidden = summary.get("forbidden_behaviors") or {}
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "required_cases", len(observations) == 2 and bool(association) and bool(stability))
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "real_provider_invocation_count", summary.get("provider_invocation_count", 0) >= 2)
    _check(checks, "real_model_invocation_count", summary.get("model_invocation_count", 0) >= 2)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False)
    _check(checks, "multiple_runtime_observations_present", len({item.get("runtime_observation_ref") for item in observations}) == 2 and all(item.get("runtime_observation_ref") for item in observations))
    _check(checks, "multiple_temporal_refs_present", len({item.get("temporal_ref") for item in observations}) == 2 and all(item.get("temporal_ref") for item in observations))
    _check(checks, "real_bbox_per_observation", all(item.get("detection_ref") and item.get("frame_width", 0) > 0 and item.get("frame_height", 0) > 0 and isinstance(item.get("bbox"), list) and len(item.get("bbox")) == 4 for item in observations))
    frame_geometry = [_geometry(item) for item in observations]
    _check(checks, "normalized_geometry_present", all(item is not None and len(item["center"]) == 2 and len(item["size"]) == 2 for item in frame_geometry))
    delta = metrics.get("delta_center") or []
    expected = None
    if all(item is not None for item in frame_geometry):
        expected = {
            "delta_center": [frame_geometry[1]["center"][i] - frame_geometry[0]["center"][i] for i in (0, 1)],
            "delta_size": [frame_geometry[1]["size"][i] - frame_geometry[0]["size"][i] for i in (0, 1)],
            "delta_area": frame_geometry[1]["area"] - frame_geometry[0]["area"],
        }
    _check(checks, "temporal_metrics_derived_from_geometry", expected is not None and all(math.isclose(float(metrics["delta_center"][i]), expected["delta_center"][i], rel_tol=1e-9, abs_tol=1e-12) for i in (0, 1)) and all(math.isclose(float(metrics["delta_size"][i]), expected["delta_size"][i], rel_tol=1e-9, abs_tol=1e-12) for i in (0, 1)) and math.isclose(float(metrics["delta_area"]), expected["delta_area"], rel_tol=1e-9, abs_tol=1e-12))
    _check(checks, "cross_frame_association_candidate_only", association.get("candidate_only") is True)
    _check(checks, "semantic_identity_not_resolved", association.get("semantic_identity_resolved") is False)
    _check(checks, "physical_identity_not_declared", association.get("physical_identity_declared") is False)
    _check(checks, "same_class_not_equal_physical_identity", association.get("semantic_identity_resolved") is False and association.get("physical_identity_declared") is False)
    _check(checks, "stable_relation_not_case_id_driven", stability.get("status") == "UNKNOWN" and stability.get("metrics_ref") == metrics.get("metrics_ref"))
    _check(checks, "stable_relation_not_cycle_index_driven", stability.get("status") == "UNKNOWN" and all(item.get("frame_ref") in {"frame:real-multiframe:source-a:v1", "frame:real-multiframe:controlled-transform-b:v1"} for item in observations))
    _check(checks, "no_invented_stability_threshold", summary.get("stability_threshold_defined") is False and summary.get("stability_threshold_ref") is None and stability.get("threshold_ref") is None)
    _check(checks, "no_threshold_means_unknown", stability.get("status") == "UNKNOWN")
    stable_candidates = [candidate for result in preconditions for candidate in (result.get("request", {}).get("situated_state", {}).get("condition_state_candidates") or []) if candidate.get("condition_ref") == STABLE]
    feasibility = [result.get("feasibility") or {} for result in preconditions]
    _check(checks, "unknown_stability_not_satisfied", all(candidate.get("status") == "UNKNOWN" for candidate in stable_candidates))
    _check(checks, "unknown_stability_fails_feasibility", all(STABLE in set(item.get("unknown_condition_refs") or ()) and item.get("status") == "NOT_FEASIBLE" for item in feasibility))
    _check(checks, "unknown_stability_closes_opportunity", all((result.get("opportunity") or {}).get("status") == "CLOSED" for result in preconditions))
    _check(checks, "unknown_stability_blocks_eligibility", all((result.get("eligibility") or {}).get("eligible_now") is False for result in preconditions))
    _check(checks, "candidate_only", summary.get("association", {}).get("candidate_only") is True and summary.get("stability", {}).get("candidate_only") is True and all(item.get("candidate_only") is True for item in observations))
    _check(checks, "no_world_truth", forbidden.get("world_truth_declared") is False)
    _check(checks, "no_field_mutation", forbidden.get("field_mutation") is False)
    _check(checks, "no_decision_execution", forbidden.get("decision_execution") is False)
    _check(checks, "no_task_execution", forbidden.get("task_execution") is False)
    _check(checks, "no_action_execution", forbidden.get("action_execution") is False)
    _check(checks, "no_device_control", forbidden.get("device_control") is False)
    _check(checks, "no_camera_control", forbidden.get("camera_control") is False)
    _check(checks, "no_movement_control", forbidden.get("movement_control") is False)
    _check(checks, "no_ocr_invocation", forbidden.get("ocr_invocation") is False)
    _check(checks, "no_slam_invocation", forbidden.get("slam_invocation") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors") and not summary.get("runtime_validation_errors"))
    _check(checks, "traceability_complete", all(item.get("provider_request_ref") and item.get("provider_result_ref") and item.get("runtime_observation_ref") and item.get("temporal_ref") and item.get("trace_refs") and item.get("provenance_refs") for item in observations) and bool(association.get("trace_refs")) and bool(metrics.get("trace_refs")) and bool(stability.get("trace_refs")))

    failed = [name for name, value in checks.items() if not value]
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
    parser = argparse.ArgumentParser(description="Verify real multi-frame visual situated-state output.")
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

