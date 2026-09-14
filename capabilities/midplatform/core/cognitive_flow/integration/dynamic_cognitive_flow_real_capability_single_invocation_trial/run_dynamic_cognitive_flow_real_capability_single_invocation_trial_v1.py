"""Runner: one real YOLO11n invocation, then controlled cognitive cases."""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict


RUNNER_PATH = Path(__file__).resolve()
PHASE = "Phase-Luna-Dynamic-Cognitive-Flow-Real-Capability-Single-Invocation-Trial-v1-001"
OUT_DIR_NAME = "luna_dynamic_cognitive_flow_real_capability_single_invocation_trial_v1"


def _resolve_repo_root() -> Path:
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.integration.dynamic_cognitive_flow_real_capability_single_invocation_trial.dynamic_cognitive_flow_real_capability_trial_adapter_v1 import (  # noqa: E402
    build_real_capability_requirement_ref,
    build_scenario_context,
    execute_real_trial_once,
)
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_cognitive_flow_real_capability_single_invocation_trial.dynamic_cognitive_flow_real_capability_trial_fixture_v1 import (  # noqa: E402
    RealCapabilityTrialScenarioV1,
    build_real_capability_trial_scenarios_v1,
)


OUT_DIR = REPO_ROOT / "_eval_out" / OUT_DIR_NAME


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _check(field: str, actual: Any, expected: Any) -> Dict[str, Any]:
    return {"field": field, "actual": _jsonable(actual), "expected": _jsonable(expected), "passed": actual == expected}


def _scenario_result(case: RealCapabilityTrialScenarioV1, trial) -> Dict[str, Any]:
    context = build_scenario_context(case, trial)
    checks = []
    if context is None:
        checks.append(_check("current_world_available", False, True))
        return {"scenario_id": case.scenario_id, "title": case.title, "passed": False, "checks": checks}
    formation = context["formation"]
    scope = context["scope"]
    resolution = context["resolution"]
    invocation = context["invocation"]
    dynamic = context["dynamic_output"]
    b2 = context["b2"]
    requirement = formation.requirement

    if case.scenario_id == "RCT-01":
        checks.extend(
            [
                _check("requirement_type", requirement.requirement_type, "OBJECT_DETECTION"),
                _check("requested_operation", requirement.requested_operation, "DETECT_OBJECT"),
                _check("requested_module_id", requirement.requested_module_id, "object_detection"),
                _check("source_need_is_minimum", formation.source_need_ref, f"need:{case.scenario_id}:1"),
            ]
        )
    elif case.scenario_id == "RCT-02":
        checks.extend([_check("scope_in_scope", scope.in_scope, True), _check("scope_result", scope.scope_result, "IN_SCOPE")])
    elif case.scenario_id == "RCT-03":
        checks.extend(
            [
                _check("model_asset_id", trial.model_contract_resolution.model_asset_id, "model-asset:yolo11n:weights-v1"),
                _check("loader_contract", trial.model_contract_resolution.loader_contract_id, "loader:ultralytics:yolo:v1"),
                _check("provider_adapter_contract", trial.model_contract_resolution.provider_adapter_contract_id, "adapter:yolo:visual-evidence:v1"),
                _check("capability_contract", "capability:object-detection:v1" in trial.model_contract_resolution.capability_contract_ids, True),
            ]
        )
    elif case.scenario_id == "RCT-04":
        checks.extend(
            [
                _check("provider_requirement_mapping", trial.provider_admission.capability_requirement_ref, trial.provider_capability_requirement_ref),
                _check("provider_admission_authorized", trial.provider_admission.provider_invocation_authorized, True),
                _check("provider_candidate_only", trial.provider_admission.candidate_only, True),
            ]
        )
    elif case.scenario_id == "RCT-05":
        checks.extend([_check("real_provider_invocation_count", trial.real_provider_invocation_count, 1), _check("provider_invocation_executed", trial.execution_result.provider_invocation_executed, True)])
    elif case.scenario_id == "RCT-06":
        checks.extend([_check("single_frame", trial.single_frame, True), _check("frame_ref_present", bool(trial.execution_result.frame_ref), True), _check("frame_id_matches", trial.frame.frame_id, trial.execution_result.frame_ref)])
    elif case.scenario_id == "RCT-07":
        checks.extend([_check("provider_accepted", trial.provider_result.accepted, True), _check("real_evidence_returned", bool(trial.evidence_refs), True), _check("provider_status", trial.execution_result.provider_status in {"SUCCESS_WITH_DETECTIONS", "SUCCESS_ZERO_DETECTIONS"}, True)])
    elif case.scenario_id == "RCT-08":
        checks.extend([_check("gateway_admission", bool(trial.gateway_admission and trial.gateway_admission.gateway_admission), True), _check("gateway_candidate_only", trial.gateway_admission.candidate_only if trial.gateway_admission else False, True), _check("gateway_truth_authority", trial.gateway_admission.semantic_authority if trial.gateway_admission else True, False)])
    elif case.scenario_id == "RCT-09":
        checks.extend([_check("current_world_created", trial.current_world is not None, True), _check("current_world_observation_refs", bool(trial.current_world.observation_refs) if trial.current_world else False, True), _check("current_world_candidate_only", trial.current_world.candidate_only if trial.current_world else False, True)])
    elif case.scenario_id == "RCT-10":
        checks.extend([_check("b2_state_current_world_ref", bool(b2.state_output.current_world_candidate.current_world_id), True), _check("b2_state_observation_ref", bool(b2.state_output.current_world_candidate.observation_refs), True), _check("b2_candidate_only", b2.candidate_only, True)])
    elif case.scenario_id == "RCT-11":
        checks.extend([_check("final_disposition", dynamic.final_disposition, "RECONSIDER"), _check("next_step", dynamic.next_step_disposition, "REQUEST_MORE_EVIDENCE"), _check("reconsideration_count", len(dynamic.reconsiderations), 1), _check("state_count", len(dynamic.state_versions), 2)])
    elif case.scenario_id == "RCT-12":
        checks.extend([_check("final_disposition", dynamic.final_disposition, "SUFFICIENT"), _check("next_step", dynamic.next_step_disposition, "STOP_SUFFICIENT"), _check("stop_not_failure", dynamic.stop_sufficient_not_failure, True), _check("remaining_non_binding", dynamic.provisional_plan.binding, False)])
    elif case.scenario_id == "RCT-13":
        checks.extend([_check("final_disposition", dynamic.final_disposition, "RECONSIDER"), _check("next_step", dynamic.next_step_disposition, "REPLAN"), _check("reconsideration_count", len(dynamic.reconsiderations), 1), _check("alternative_need", dynamic.current_minimum_need_ref, f"need:{case.scenario_id}:alternative")])
    elif case.scenario_id == "RCT-14":
        checks.extend([_check("final_disposition", dynamic.final_disposition, "RECONSIDER"), _check("insufficient_next_step", dynamic.next_step_disposition, "REQUEST_MORE_EVIDENCE"), _check("reconsideration_count", len(dynamic.reconsiderations), 1), _check("no_additional_real_provider_call", trial.real_provider_invocation_count, 1), _check("real_invocation_cap", trial.real_provider_invocation_count <= 1, True)])
    elif case.scenario_id == "RCT-15":
        checks.extend([_check("sufficient_next_step", dynamic.next_step_disposition, "STOP_SUFFICIENT"), _check("post_sufficiency_evidence_ignored", bool(dynamic.ignored_evidence_update_refs), True), _check("no_additional_real_provider_call", trial.real_provider_invocation_count, 1)])
    elif case.scenario_id == "RCT-16":
        checks.extend([_check("plan_binding", dynamic.provisional_plan.binding, False), _check("remaining_candidates_are_non_binding", bool(dynamic.transitions and dynamic.transitions[-1].non_materialized_plan_refs), True)])
    elif case.scenario_id == "RCT-17":
        checks.extend([_check("provider_truth_authority", trial.execution_result.provider_semantic_authority, False), _check("evidence_truth_declared", trial.execution_result.truth_declared, False), _check("world_truth_declared", trial.execution_result.current_world_truth_declaration, False)])
    elif case.scenario_id == "RCT-18":
        checks.extend([_check("brain_requirement_module_only", requirement.requested_module_id, "object_detection"), _check("brain_requirement_has_no_model_identity", not requirement.technical_hints and not requirement.requested_module_id.startswith("model-asset:"), True), _check("provider_identity_from_resolution", trial.provider_admission.model_candidate_ref, trial.model_contract_resolution.model_asset_id)])
    elif case.scenario_id == "RCT-19":
        checks.append(_check("action_execution", trial.action_execution, False))
    elif case.scenario_id == "RCT-20":
        checks.extend([_check("learning_execution", trial.learning_execution, False), _check("memory_mutation", trial.memory_mutation, False)])
    elif case.scenario_id == "RCT-21":
        checks.extend([_check("trace_refs", bool(trial.trace_refs), True), _check("provenance_refs", bool(trial.provenance_refs), True), _check("dynamic_trace_refs", bool(dynamic.trace_refs), True), _check("b2_provenance_chain", bool(b2.provenance_chain), True)])
    elif case.scenario_id == "RCT-22":
        checks.extend([_check("one_real_invocation", trial.real_provider_invocation_count, 1), _check("second_invocation_not_allowed", trial.second_real_invocation_allowed, False), _check("continuous_camera_not_allowed", trial.continuous_camera_allowed, False), _check("download_not_allowed", trial.model_download_allowed, False), _check("candidate_only", trial.candidate_only, True)])
    passed = all(item["passed"] for item in checks)
    return {
        "scenario_id": case.scenario_id,
        "title": case.title,
        "passed": passed,
        "checks": checks,
        "final_disposition": dynamic.final_disposition,
        "next_step_disposition": dynamic.next_step_disposition,
        "state_version_refs": [item.state_version_ref for item in dynamic.state_versions],
    }


def build_trial_result(
    *,
    source_ref: str,
    model_path: str,
    declared_checksum: str | None,
    observed_checksum: str | None,
    dependency_status: str,
) -> Dict[str, Any]:
    """Run one real provider call and all remaining cases as controlled projections."""
    requirement_ref = "requirement:RCT-REAL-01:object-detection"
    trial = execute_real_trial_once(
        requirement_ref=requirement_ref,
        source_ref=source_ref,
        model_path=model_path,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
        dependency_status=dependency_status,
    )
    cases = [_scenario_result(case, trial) for case in build_real_capability_trial_scenarios_v1()]
    failed = [item["scenario_id"] for item in cases if not item["passed"]]
    summary = {
        "phase": PHASE,
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "real_provider_invocation_count": trial.real_provider_invocation_count,
        "logical_resolution_status": trial.logical_resolution_status,
        "runtime_admission_status": trial.runtime_admission_status,
        "executable_capability_created": trial.executable_capability_created,
        "provider_admission_reached": trial.provider_admission_reached,
        "provider_invocation_executed": trial.execution_result.provider_invocation_executed,
        "second_provider_invocation": trial.second_provider_invocation,
        "a_interpretation_reached": bool(trial.current_world is not None),
        "terminal_readiness_owner": trial.terminal_readiness_owner,
        "runtime_admission_bypassed": trial.runtime_admission_bypassed,
        "executable_candidate_bypassed": trial.executable_candidate_bypassed,
        "dynamic_flow_semantic_authority": trial.dynamic_flow_semantic_authority,
        "max_real_provider_invocation": 1,
        "single_frame": trial.single_frame,
        "real_provider_status": trial.execution_result.provider_status,
        "real_evidence_count": len(trial.evidence_refs),
        "gateway_admitted": bool(trial.gateway_admission and trial.gateway_admission.gateway_admission),
        "current_world_created": trial.current_world is not None,
        "candidate_only": trial.candidate_only,
        "provider_semantic_authority": trial.execution_result.provider_semantic_authority,
        "world_truth_authority": trial.world_truth_authority,
        "second_real_invocation_allowed": trial.second_real_invocation_allowed,
        "continuous_camera_allowed": trial.continuous_camera_allowed,
        "model_download_allowed": trial.model_download_allowed,
        "action_execution": trial.action_execution,
        "learning_execution": trial.learning_execution,
        "memory_mutation": trial.memory_mutation,
        "model_asset_id": trial.model_contract_resolution.model_asset_id,
        "loader_contract_id": trial.model_contract_resolution.loader_contract_id,
        "provider_adapter_contract_id": trial.model_contract_resolution.provider_adapter_contract_id,
        "provider_capability_requirement_ref": trial.provider_capability_requirement_ref,
        "trace_refs": trial.trace_refs,
        "provenance_refs": trial.provenance_refs,
        "cases": cases,
    }
    return {"summary": summary, "trial": trial}


def write_trial_artifacts(payload: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = payload["summary"]
    (OUT_DIR / "trial_summary_v1.json").write_text(json.dumps(_jsonable(summary), ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "trial_snapshot_v1.json").write_text(json.dumps(_jsonable(payload["trial"]), ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="One governed real YOLO11n single-frame Cognitive Flow trial")
    parser.add_argument("--source", default="/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/s3_real_frame_001.jpg")
    parser.add_argument("--model-path", default="/Users/luanlei/Desktop/Luna-Core/vision/detection/yolo/yolo11n.pt")
    parser.add_argument("--declared-checksum")
    parser.add_argument("--observed-checksum")
    parser.add_argument("--dependency-status", default="PYTHON_DEPENDENCY_UNRESOLVED")
    args = parser.parse_args()
    payload = build_trial_result(
        source_ref=args.source,
        model_path=args.model_path,
        declared_checksum=args.declared_checksum,
        observed_checksum=args.observed_checksum,
        dependency_status=args.dependency_status,
    )
    write_trial_artifacts(payload)
    print(json.dumps(_jsonable(payload["summary"]), ensure_ascii=False, sort_keys=True))
    return 0 if payload["summary"]["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_trial_result", "main"]
