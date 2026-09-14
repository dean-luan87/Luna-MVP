"""Fail-closed user-terminal Verifier for real cognitive conditioning."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import GOVERNANCE_ASSERTION_IDS


ROOT = next(
    candidate for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents)
    if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md"))
)
DEFAULT_SUMMARY = ROOT / "_eval_out/real_role_task_goal_cognitive_conditioning_integration_v1/runner_summary_v1.json"
EXPECTED = {
    "SAME_EVIDENCE_DIFFERENT_GOAL": "GOAL",
    "SAME_EVIDENCE_DIFFERENT_TASK": "TASK",
    "SAME_EVIDENCE_DIFFERENT_ROLE": "ROLE",
}


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _no_downstream(side: Dict[str, Any]) -> bool:
    return not any(
        item.get("stage_id") in {"DECISION", "TASK", "ACTION", "EXECUTION"}
        for item in (side.get("route") or {}).get("stage_results", ())
        if isinstance(item, dict)
    )


def _side_checks(side: Dict[str, Any], prefix: str, checks: Dict[str, bool]) -> None:
    _check(checks, f"{prefix}:live_runtime", side.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, f"{prefix}:real_provider_attempted", side.get("provider_real_execution_attempted") is True)
    _check(checks, f"{prefix}:real_provider_verified", side.get("provider_real_execution_verified") is True)
    _check(checks, f"{prefix}:provider_invoked", side.get("provider_invoked") is True)
    _check(checks, f"{prefix}:model_invoked", side.get("model_invoked") is True)
    _check(checks, f"{prefix}:recorded_result_unused", side.get("recorded_result_used") is False)
    _check(checks, f"{prefix}:canonical_identity", (
        side.get("capability_ref") == "text_recognition"
        and side.get("provider_ref") == "provider:ocr_v1"
        and side.get("model_ref") == "model:ocr_v1"
    ))
    _check(checks, f"{prefix}:runtime_gateway_evidence", bool(
        side.get("runtime_observation_ref") and side.get("gateway_admission_ref") and side.get("evidence_refs")
    ))
    _check(checks, f"{prefix}:real_text_evidence", side.get("provider_status") == "SUCCESS" and side.get("empty_result") is False and bool(side.get("recognized_text_candidates")))
    runtime = side.get("provider_runtime_result") or {}
    _check(checks, f"{prefix}:request_result_identity", runtime.get("provider_request_ref") == side.get("provider_request_ref") and runtime.get("provider_result_ref") == side.get("provider_result_ref") and runtime.get("execution_instance_ref") == side.get("execution_instance_ref"))
    _check(checks, f"{prefix}:trace_provenance", bool((runtime.get("trace_refs") or ()) and (runtime.get("provenance_refs") or ())))
    _check(checks, f"{prefix}:cstate_reached", side.get("cognitive_state_reached") is True)
    _check(checks, f"{prefix}:candidate_only", (
        (side.get("cognitive_material_snapshot") or {}).get("candidate_only") is True
        and (side.get("cognitive_material_snapshot") or {}).get("world_truth_declared") is False
    ))
    forbidden = side.get("forbidden_behaviors") or {}
    _check(checks, f"{prefix}:forbidden_boundaries", all(
        forbidden.get(name) is False for name in (
            "scenario_id_driven_cognition", "world_truth_declared", "fact_admitted", "field_mutation",
            "decision_execution", "task_execution", "action_execution", "runtime_executor_invocation", "device_control",
        )
    ))
    _check(checks, f"{prefix}:no_downstream_execution", _no_downstream(side))
    plane = (side.get("plane_g") or {}).get("result") or {}
    assertions = plane.get("assertion_results") or ()
    _check(checks, f"{prefix}:plane_g", plane.get("compliance_status") == "COMPLIANT" and {item.get("assertion_id") for item in assertions} == set(GOVERNANCE_ASSERTION_IDS) and all(item.get("status") == "PASS" and item.get("passed") is True for item in assertions))
    _check(checks, f"{prefix}:validation_errors_empty", not side.get("validation_errors"))


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    contrasts = {item.get("contrast_id"): item for item in summary.get("contrasts", ())}
    _check(checks, "phase", summary.get("phase") == "Phase-P1-Luna-Real-Role-Task-Goal-Cognitive-Conditioning-Integration-v1-001")
    _check(checks, "live_runtime", summary.get("execution_mode") == "LIVE_RUNTIME")
    _check(checks, "canonical_capability", summary.get("capability_ref") == "text_recognition")
    _check(checks, "canonical_provider", summary.get("provider_ref") == "provider:ocr_v1")
    _check(checks, "canonical_model", summary.get("model_ref") == "model:ocr_v1")
    _check(checks, "three_contrast_families", set(contrasts) == set(EXPECTED))
    _check(checks, "conditioning_not_scenario_driven", summary.get("semantic_driver") == "role+task+goal+information_need+admitted_evidence")
    _check(checks, "role_canonical_input_available", summary.get("role_conditioning_canonical_input_gap") is False)
    _check(checks, "global_recorded_result_unused", summary.get("recorded_result_used") is False)
    _check(checks, "global_validation_errors_empty", not summary.get("validation_errors"))
    _check(checks, "global_forbidden_boundaries", all(value is False for value in (summary.get("forbidden_behaviors") or {}).values()))

    for contrast_id, category in EXPECTED.items():
        contrast = contrasts.get(contrast_id) or {}
        prefix = contrast_id
        _check(checks, f"{prefix}:category", contrast.get("category") == category)
        left = contrast.get("left") or {}
        right = contrast.get("right") or {}
        _side_checks(left, f"{prefix}:left", checks)
        _side_checks(right, f"{prefix}:right", checks)
        comparison = contrast.get("comparison") or {}
        _check(checks, f"{prefix}:same_source", left.get("source_ref") == right.get("source_ref"))
        _check(checks, f"{prefix}:same_provider_model", left.get("provider_ref") == right.get("provider_ref") == "provider:ocr_v1" and left.get("model_ref") == right.get("model_ref") == "model:ocr_v1")
        _check(checks, f"{prefix}:same_native_observation", comparison.get("physical_evidence_equivalent") is True)
        _check(checks, f"{prefix}:no_physical_mutation", comparison.get("unexpected_physical_mutation") is False)
        _check(checks, f"{prefix}:conditioning_changed", comparison.get("expected_difference_dimension") in comparison.get("conditioning_dimensions_changed", ()))
        _check(checks, f"{prefix}:material_cognition_difference", bool(comparison.get("cognitive_material_differences")))
        _check(checks, f"{prefix}:not_identity_only", comparison.get("identity_only_difference") is False)
        _check(checks, f"{prefix}:expected_difference_observed", comparison.get("expected_difference_observed") is True)

    goal = contrasts.get("SAME_EVIDENCE_DIFFERENT_GOAL") or {}
    _check(checks, "goal:information_need_causality", (goal.get("left") or {}).get("information_need_ref") != (goal.get("right") or {}).get("information_need_ref") and (goal.get("left") or {}).get("required_information_refs") != (goal.get("right") or {}).get("required_information_refs"))
    _check(checks, "goal:sufficiency_causality", (goal.get("left") or {}).get("sufficiency") != (goal.get("right") or {}).get("sufficiency"))
    task = contrasts.get("SAME_EVIDENCE_DIFFERENT_TASK") or {}
    _check(checks, "task:no_task_execution", all(
        (side.get("forbidden_behaviors") or {}).get("task_execution") is False
        for side in (task.get("left") or {}, task.get("right") or {})
    ))
    role = contrasts.get("SAME_EVIDENCE_DIFFERENT_ROLE") or {}
    _check(checks, "role:existing_vocabulary", {(role.get("left") or {}).get("role_ref"), (role.get("right") or {}).get("role_ref")} == {"role:workspace-owner", "role:visitor"})

    # Relevance is a coverage guard, not merely a descriptive projection.
    # The real OCR contrast must contain both a negative and a positive probe:
    # an explicitly IRRELEVANT candidate cannot satisfy the active need, while
    # a RELEVANT candidate can satisfy it when its declared information refs
    # cover the required refs.
    sides = [side for contrast in contrasts.values() for side in (contrast.get("left") or {}, contrast.get("right") or {})]
    irrelevant_sides = [
        side for side in sides
        if any(":IRRELEVANT:" in item for item in (side.get("evidence_relevance") or ()))
    ]
    relevant_sufficient_sides = [
        side for side in sides
        if any(":RELEVANT:" in item for item in (side.get("evidence_relevance") or ()))
        and set(side.get("required_information_refs") or ()) <= set(side.get("supported_information_refs") or ())
    ]
    _check(checks, "irrelevant_evidence_does_not_cover_required_information", bool(irrelevant_sides) and all(side.get("sufficiency") != "SUFFICIENT" for side in irrelevant_sides))
    _check(checks, "relevant_evidence_can_cover_required_information", bool(relevant_sufficient_sides) and any(side.get("sufficiency") == "SUFFICIENT" for side in relevant_sufficient_sides))

    failed = [name for name, passed in checks.items() if not passed]
    operational = (
        summary.get("execution_mode") == "LIVE_RUNTIME"
        and summary.get("real_provider_invocation_count", 0) == summary.get("side_count", -1)
        and summary.get("real_model_invocation_count", 0) == summary.get("side_count", -1)
        and summary.get("recorded_result_used") is False
        and not summary.get("validation_errors")
        and all(
            side.get("provider_real_execution_verified") is True
            and side.get("runtime_observation_ref")
            and side.get("gateway_admission_ref")
            and side.get("evidence_refs")
            and side.get("provider_status") == "SUCCESS"
            and side.get("empty_result") is False
            and not side.get("validation_errors")
            for side in sides
        )
    )
    global_forbidden = summary.get("forbidden_behaviors") or {}
    cognitive = (
        summary.get("semantic_driver") == "role+task+goal+information_need+admitted_evidence"
        and summary.get("role_conditioning_canonical_input_gap") is False
        and all(value is False for value in global_forbidden.values())
        and all(
        (contrast.get("comparison") or {}).get("physical_evidence_equivalent") is True
        and (contrast.get("comparison") or {}).get("expected_difference_observed") is True
        for contrast in contrasts.values()
        )
        and (goal.get("left") or {}).get("information_need_ref") != (goal.get("right") or {}).get("information_need_ref")
        and (goal.get("left") or {}).get("required_information_refs") != (goal.get("right") or {}).get("required_information_refs")
        and (goal.get("left") or {}).get("sufficiency") != (goal.get("right") or {}).get("sufficiency")
    )
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "operational_result": "PASS" if operational else "FAIL",
        "cognitive_logic_result": "PASS" if cognitive else "FAIL",
        "final_decision": "GO" if operational and cognitive else "NOT_GO",
        "checks": checks,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
