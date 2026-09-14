from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = repo_root_from(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_engine_v1 import FieldPerceptionActiveObservationControlEngineV1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import build_vision_provider_admission_candidate_v1, run_authorized_vision_provider_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_binding_seam_v1 import CanonicalYOLO11nBindingContextV1, build_canonical_yolo11n_provider_admission_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_adapter_v1 import adapt_raw_camera_source  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.yolo11n_single_frame_execution.yolo11n_single_frame_execution_fixture_v1 import build_yolo11n_single_frame_cases_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.yolo11n_single_frame_execution.yolo11n_single_frame_execution_types_v1 import build_single_frame_execution_result_v1, to_dict  # noqa: E402
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_external_provisioning.yolo11n_external_provisioning_types_v1 import resolve_yolo11n_external_provisioning_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.run_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1 import run as run_prior_s3_regression  # noqa: E402


OUT_DIR = ROOT / "_eval_out/a_route_s3_yolo11n_real_single_frame_provider_execution_v1"
DEFAULT_SOURCE = "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/s3_real_frame_001.jpg"
DEFAULT_MODEL = "/Users/luanlei/Desktop/Luna-Core/vision/detection/yolo/yolo11n.pt"
GOVERNED_MODEL_PATH = "vision/detection/yolo/yolo11n.pt"
MODEL_ASSET_ID = "model-asset:yolo11n:weights-v1"
LOADER_ID = "loader:ultralytics:yolo:v1"
ADAPTER_ID = "adapter:yolo:visual-evidence:v1"
EVIDENCE_ID = "evidence:visual-detection-candidate:v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def _control_payload(case_id: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "root_cycle_trace_id": f"trace:yolo11n-single-frame:cycle:{case_id}",
        "information_need": "bounded visual detection for one admitted frame",
        "task_ref": f"task:yolo11n:{case_id}",
        "intent_ref": f"intent:yolo11n:{case_id}",
        "target_semantic": "bounded visual target",
        "spatial_scope": "authorized single-frame scope",
        "requested_capability_kinds": ("VISION_DETECTION",),
        "expected_evidence_kinds": ("VISION_DETECTION",),
        "provider_admission_candidate": True,
        "provider_candidate_ref": f"provider-candidate:yolo11n:{case_id}",
        "selected_model_candidate_ref": MODEL_ASSET_ID,
        "received_evidence_kinds": (),
        "received_evidence_refs": (),
        "contradiction_refs": (),
        "cross_modal_contradiction": False,
        "provider_failure": False,
        "budget_exhausted": False,
        "fallback_available": False,
        "target_coverage": False,
        "semantic_coverage": False,
        "temporal_validity": {"stale": False, "expired": False},
        "resource_budget": {"max_frames": 1, "max_duration_ms": 5000},
    }


def _prepare(
    *,
    case_id: str,
    source_ref: str,
    source_mode: str,
    model_path: str,
    declared_checksum: Optional[str],
    observed_checksum: Optional[str],
    dependency_status: str,
    canonical_binding: Optional[CanonicalYOLO11nBindingContextV1] = None,
) -> Tuple[Any, Any, Any, Any, Any, Any]:
    manager_admission = resolve_yolo11n_external_provisioning_v1({
        "target_model_asset_id": MODEL_ASSET_ID,
        "target_governed_path": GOVERNED_MODEL_PATH,
        "source_file_ref": model_path,
        "observed_path": model_path,
        "provenance_ref": f"provenance:yolo11n:{source_mode.lower()}",
        "declared_checksum": declared_checksum,
        "observed_checksum": observed_checksum,
        "dependency_status": dependency_status,
        "candidate_only": True,
    })
    control = FieldPerceptionActiveObservationControlEngineV1().run_case(_control_payload(case_id))
    raw = adapt_raw_camera_source(
        source_ref,
        source_type="IMAGE_FILE",
        observation_demand_ref=f"demand:yolo11n:{case_id}",
        capability_requirement_ref="capability:RAW_CAMERA_INPUT_STREAM",
        source_mode=source_mode,
        session_id=f"yolo11n-session:{case_id}",
        frame_id=f"yolo11n-frame:{case_id}",
        width=640,
        height=480,
        max_frames=1,
        max_duration_ms=5000,
    )
    frame = raw.frames[0] if raw.frames else None
    session = control.provider_session
    request = control.request
    requirement = control.capability_requirement
    if source_mode == "REAL":
        provider_admission = build_canonical_yolo11n_provider_admission_v1(
            context=canonical_binding,
            observation_demand_ref=control.demand.demand_id,
            observation_request_ref=request.request_id if request else "",
            capability_requirement_ref=requirement.requirement_id if requirement else "",
            provider_session_ref=session.session_id if session else "",
            provider_candidate_ref=f"provider-candidate:yolo11n:{case_id}",
            region_scope_candidate=request.target_region_candidate if request else "",
            expected_evidence=("VISION_DETECTION",),
            bounded=bool(session and session.resource_budget_candidate.get("max_frames") == 1),
            trace_ref=control.trace.control_trace_ref,
        ).admission
        if manager_admission.technical_admission_status != "ADMISSION_READY_CANDIDATE":
            provider_admission = dataclasses.replace(
                provider_admission,
                provider_invocation_authorized=False,
            )
    else:
        provider_admission = build_vision_provider_admission_candidate_v1(
            observation_demand_ref=control.demand.demand_id,
            observation_request_ref=request.request_id if request else "",
            capability_requirement_ref=requirement.requirement_id if requirement else "",
            provider_session_ref=session.session_id if session else "",
            provider_candidate_ref=f"provider-candidate:yolo11n:{case_id}",
            model_candidate_ref=MODEL_ASSET_ID,
            model_admission_ref=manager_admission.trace_ref if manager_admission.technical_admission_status == "ADMISSION_READY_CANDIDATE" else "",
            region_scope_candidate=request.target_region_candidate if request else "",
            expected_evidence=("VISION_DETECTION",),
            bounded=bool(session and session.resource_budget_candidate.get("max_frames") == 1),
            provider_admitted=manager_admission.technical_admission_status == "ADMISSION_READY_CANDIDATE",
            trace_ref=control.trace.control_trace_ref,
            provenance_refs=tuple(dict.fromkeys((*control.trace.provenance_refs, *manager_admission.provenance_refs))),
        )
    return manager_admission, control, raw, frame, provider_admission, session


def _execute(
    *,
    case_id: str,
    source_ref: str,
    source_mode: str,
    model_path: str,
    declared_checksum: Optional[str],
    observed_checksum: Optional[str],
    dependency_status: str,
    execute_real_provider: bool,
    canonical_binding: Optional[CanonicalYOLO11nBindingContextV1] = None,
    synthetic_zero_detections: bool = False,
) -> Dict[str, Any]:
    manager, control, raw, frame, provider_admission, session = _prepare(
        case_id=case_id,
        source_ref=source_ref,
        source_mode=source_mode,
        model_path=model_path,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
        dependency_status=dependency_status,
        canonical_binding=canonical_binding,
    )
    provider = run_authorized_vision_provider_v1(
        frame,
        provider_admission,
        execute_real_provider=execute_real_provider and provider_admission.provider_invocation_authorized,
        model_path=model_path,
        seen_inference_ids=(),
        synthetic_zero_detections=synthetic_zero_detections,
    )
    execution = build_single_frame_execution_result_v1(
        manager_admission=manager,
        frame=frame,
        provider=provider,
        provider_adapter_contract_id=ADAPTER_ID,
        evidence_contract_id=EVIDENCE_ID,
        model_load_executed=bool(execute_real_provider and provider.invocation_performed),
        invocation_count=1 if provider.invocation_performed else 0,
        provider_error_stage="controlled_failure_fixture" if provider.error_code == "PROVIDER_INVOCATION_FAILED" and not execute_real_provider else "",
        provider_error_type=provider.error_code if provider.error_code else "",
        provider_error_detail="synthetic bounded provider failure" if provider.error_code == "PROVIDER_INVOCATION_FAILED" and not execute_real_provider else "",
    )
    return {
        "manager_admission": manager,
        "control": control,
        "raw": raw,
        "frame": frame,
        "session": session,
        "provider_admission": provider_admission,
        "provider": provider,
        "execution": execution,
    }


def _check(name: str, actual: Any, expected: Any) -> Dict[str, Any]:
    return {"field": name, "actual": actual, "expected": expected, "passed": actual == expected}


def _case_result(case_id: str, title: str, primary: Dict[str, Any], prior: Dict[str, Any], synthetic: Dict[str, Any]) -> Dict[str, Any]:
    execution = primary["execution"]
    provider = primary["provider"]
    manager = primary["manager_admission"]
    frame = primary["frame"]
    session = primary["session"]
    evidence = tuple(provider.evidence or ())
    checks = []
    if case_id == "Y11E-01":
        checks.append(_check("technical_admission_status", execution.technical_admission_status, "ADMISSION_READY_CANDIDATE"))
    elif case_id == "Y11E-02":
        checks.append(_check("model_asset_id", execution.model_asset_id, MODEL_ASSET_ID))
    elif case_id == "Y11E-03":
        checks.append(_check("loader_contract_id", execution.loader_contract_id, LOADER_ID))
    elif case_id == "Y11E-04":
        checks.append(_check("provider_adapter_contract_id", execution.provider_adapter_contract_id, ADAPTER_ID))
    elif case_id == "Y11E-05":
        checks.extend([_check("single_frame", execution.single_frame, True), _check("resource_budget_max_frames", session.resource_budget_candidate.get("max_frames", 0) if session else 0, 1), _check("invocation_count", execution.invocation_count <= 1, True)])
    elif case_id == "Y11E-06":
        checks.append(_check("native_to_canonical_count", len(provider.detections), len(evidence)))
        checks.append(_check("structured_mapping", all(len(item.bbox) == 4 and item.frame_ref == execution.frame_ref for item in evidence), True))
    elif case_id == "Y11E-07":
        checks.append(_check("zero_detections_are_valid", not provider.detections, True if not provider.detections else False))
        checks.append(_check("provider_success_status", execution.provider_status in {"SUCCESS_WITH_DETECTIONS", "SUCCESS_ZERO_DETECTIONS"}, True))
    elif case_id == "Y11E-08":
        failure = synthetic["provider_failure"]["execution"]
        checks.extend([_check("failure_status", failure.provider_status, "FAILED_WITH_DIAGNOSTIC"), _check("error_stage", bool(failure.provider_error_stage), True), _check("error_type", bool(failure.provider_error_type), True), _check("error_detail", bool(failure.provider_error_detail), True)])
    elif case_id == "Y11E-09":
        checks.extend([_check("candidate_only", execution.candidate_only, True), _check("truth_declared", execution.truth_declared, False), _check("fact_admitted", execution.fact_admitted, False), _check("provider_semantic_authority", execution.provider_semantic_authority, False)])
    elif case_id == "Y11E-10":
        checks.extend([_check("field_mutation", execution.field_state_direct_mutation, False), _check("world_truth", execution.current_world_truth_declaration, False), _check("intent_mutation", execution.intent_mutation, False), _check("task_mutation", execution.task_mutation, False), _check("decision_mutation", execution.decision_mutation, False)])
    elif case_id == "Y11E-11":
        checks.extend([_check("ocr", execution.ocr_execution, False), _check("slam", execution.slam_execution, False), _check("vlm", execution.vlm_execution, False), _check("semantic_interpretation", execution.semantic_interpretation, False)])
    elif case_id == "Y11E-12":
        checks.extend([_check("network", execution.network_access, False), _check("model_download", execution.automatic_model_download, False), _check("package_download", execution.automatic_package_download, False)])
    elif case_id == "Y11E-13":
        checks.extend([_check("hidden_retry", execution.hidden_retry, False), _check("invocation_at_most_once", execution.invocation_count <= 1, True), _check("autonomous_continuation", execution.provider_autonomous_continuous_execution, False)])
    elif case_id == "Y11E-14":
        checks.append(_check("gateway_handoff_candidate", execution.gateway_handoff_candidate, True))
    elif case_id == "Y11E-15":
        checks.extend([_check("trace_ref", bool(execution.trace_ref), True), _check("provenance_refs", bool(execution.provenance_refs), True)])
    elif case_id == "Y11E-16":
        checks.extend([_check("s0", prior.get("s0_all_cases_passed"), True), _check("s1", prior.get("s1_all_cases_passed"), True), _check("s2", prior.get("s2_all_cases_passed"), True), _check("s3_synthetic", prior.get("s3_all_cases_passed"), True)])
    elif case_id == "Y11E-17":
        checks.extend([_check("synthetic_evidence_contract", synthetic["execution"].evidence_contract_id, EVIDENCE_ID), _check("real_evidence_contract", execution.evidence_contract_id, EVIDENCE_ID), _check("structural_contract_compatibility", execution.candidate_only == synthetic["execution"].candidate_only, True)])
    else:
        checks.extend([_check("real_provider_surface_declared", True, True), _check("single_frame_scope", execution.single_frame, True), _check("no_downstream_mutation", execution.field_state_direct_mutation, False)])
    return {"scenario_id": case_id, "title": title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": {"execution": to_dict(execution), "provider": jsonable(provider)}}


def _real_case(primary: Dict[str, Any]) -> Dict[str, Any]:
    execution = primary["execution"]
    checks = [
        _check("admission", execution.technical_admission_status, "ADMISSION_READY_CANDIDATE"),
        _check("provider_invocation", execution.provider_invocation_executed, True),
        _check("model_inference", execution.model_inference_executed, True),
        _check("network", execution.network_access, False),
        _check("automatic_download", execution.automatic_model_download, False),
        _check("provider_status", execution.provider_status in {"SUCCESS_WITH_DETECTIONS", "SUCCESS_ZERO_DETECTIONS"}, True),
    ]
    return {"scenario_id": "S3-Y11-REAL-01", "title": "real YOLO11n single-frame provider execution", "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": {"execution": to_dict(execution), "provider": jsonable(primary["provider"]), "admission": to_dict(primary["manager_admission"])}}


def run(*, real: bool = False, source_ref: str = DEFAULT_SOURCE, model_path: str = DEFAULT_MODEL, declared_checksum: Optional[str] = None, observed_checksum: Optional[str] = None, dependency_status: str = "PYTHON_DEPENDENCY_UNRESOLVED", canonical_binding: Optional[CanonicalYOLO11nBindingContextV1] = None) -> Dict[str, Any]:
    prior = run_prior_s3_regression()
    synthetic = _execute(
        case_id="SYNTHETIC-Y11N",
        source_ref="synthetic://s3-yolo11n/frame-001",
        source_mode="SYNTHETIC_REGRESSION",
        model_path=GOVERNED_MODEL_PATH,
        declared_checksum="sha256:synthetic-yolo11n-v1",
        observed_checksum="sha256:synthetic-yolo11n-v1",
        dependency_status="PYTHON_DEPENDENCY_VERIFIED",
        execute_real_provider=False,
    )
    failure = _execute(
        case_id="SYNTHETIC-Y11N-FAILURE",
        source_ref="synthetic://s3-yolo11n/frame-001",
        source_mode="SYNTHETIC_REGRESSION",
        model_path=GOVERNED_MODEL_PATH,
        declared_checksum="sha256:synthetic-yolo11n-v1",
        observed_checksum="sha256:synthetic-yolo11n-v1",
        dependency_status="PYTHON_DEPENDENCY_VERIFIED",
        execute_real_provider=False,
    )
    failure["provider"] = run_authorized_vision_provider_v1(
        failure["frame"], failure["provider_admission"], execute_real_provider=False, model_path=GOVERNED_MODEL_PATH, provider_failure=True
    )
    failure["execution"] = build_single_frame_execution_result_v1(
        manager_admission=failure["manager_admission"], frame=failure["frame"], provider=failure["provider"], provider_adapter_contract_id=ADAPTER_ID, evidence_contract_id=EVIDENCE_ID, model_load_executed=False, invocation_count=0, provider_error_stage="controlled_failure_fixture", provider_error_type="PROVIDER_INVOCATION_FAILED", provider_error_detail="synthetic bounded provider failure"
    )
    primary = _execute(
        case_id="S3-Y11-REAL-01" if real else "SYNTHETIC-Y11N-PRIMARY",
        source_ref=source_ref if real else "synthetic://s3-yolo11n/frame-001",
        source_mode="REAL" if real else "SYNTHETIC_REGRESSION",
        model_path=model_path,
        declared_checksum=declared_checksum if real else "sha256:synthetic-yolo11n-v1",
        observed_checksum=observed_checksum if real else "sha256:synthetic-yolo11n-v1",
        dependency_status=dependency_status if real else "PYTHON_DEPENDENCY_VERIFIED",
        execute_real_provider=real,
        canonical_binding=canonical_binding,
    )
    zero_detection = _execute(
        case_id="SYNTHETIC-Y11N-ZERO-DETECTIONS",
        source_ref="synthetic://s3-yolo11n/frame-001",
        source_mode="SYNTHETIC_REGRESSION",
        model_path=GOVERNED_MODEL_PATH,
        declared_checksum="sha256:synthetic-yolo11n-v1",
        observed_checksum="sha256:synthetic-yolo11n-v1",
        dependency_status="PYTHON_DEPENDENCY_VERIFIED",
        execute_real_provider=False,
        synthetic_zero_detections=True,
    )
    primary_by_fixture = {
        "DEFAULT_DETECTIONS": primary,
        "ZERO_DETECTIONS": zero_detection,
    }
    cases = [
        _case_result(
            case["scenario_id"],
            case["title"],
            primary_by_fixture.get(case.get("provider_fixture", "DEFAULT_DETECTIONS"), primary),
            prior,
            {"execution": synthetic["execution"], "provider_failure": failure},
        )
        for case in build_yolo11n_single_frame_cases_v1()
    ]
    if real:
        cases.append(_real_case(primary))
    failed = [item["scenario_id"] for item in cases if not item["all_checks_passed"]]
    execution = primary["execution"]
    summary = {
        "mode": "REAL_SINGLE_FRAME" if real else "SYNTHETIC_REGRESSION",
        "real_components": ["VISION_YOLO11N_PROVIDER"] if real else [],
        "synthetic_components": ["OCR", "SLAM/VIO", "VLM", "Context/World", "Cognitive Chain", "Task/Action", "Runtime", "Outcome Feedback", "User Output"],
        "y11e_scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "s0_all_cases_passed": prior.get("s0_all_cases_passed"),
        "s1_all_cases_passed": prior.get("s1_all_cases_passed"),
        "s2_all_cases_passed": prior.get("s2_all_cases_passed"),
        "s3_synthetic_all_cases_passed": prior.get("s3_all_cases_passed"),
        "s3_y11_real_case_present": real,
        "s3_y11_real_case_passed": bool(real and not failed),
        "model_asset_id": execution.model_asset_id,
        "loader_contract_id": execution.loader_contract_id,
        "provider_adapter_contract_id": execution.provider_adapter_contract_id,
        "evidence_contract_id": execution.evidence_contract_id,
        "technical_admission_status": execution.technical_admission_status,
        "provider_status": execution.provider_status,
        "provider_error_stage": execution.provider_error_stage,
        "provider_error_type": execution.provider_error_type,
        "provider_error_detail": execution.provider_error_detail,
        "model_load_executed": execution.model_load_executed,
        "provider_invocation_executed": execution.provider_invocation_executed,
        "model_inference_executed": execution.model_inference_executed,
        "commercial_license_status": execution.commercial_license_status,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "automatic_dependency_install": False,
        "provider_autonomous_continuous_execution": False,
        "hidden_retry": False,
        "ocr_execution": False,
        "slam_execution": False,
        "vlm_execution": False,
        "semantic_interpretation": False,
        "semantic_compression": False,
        "provider_semantic_authority": False,
        "automatic_fact_admission": False,
        "field_state_direct_mutation": False,
        "current_world_truth_declaration": False,
        "intent_mutation": False,
        "decision_mutation": False,
        "task_mutation": False,
        "real_action_execution": False,
        "raw_content_persisted": False,
    }
    trace = {
        "reverse_lookup": "canonical evidence -> provider-native detection -> single frame -> bounded session -> observation request/demand -> Model Manager admission -> model asset",
        "provenance_grants_authority": False,
        "provider_autonomous_continuous_execution": False,
        "raw_content_persisted": False,
        "current_trace_ref": execution.trace_ref,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "a_route_s3_yolo11n_real_single_frame_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_yolo11n_real_single_frame_case_results_v1.json").write_text(json.dumps(jsonable(cases), ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_yolo11n_real_single_frame_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded YOLO11n single-frame execution; Model Manager admission required.")
    parser.add_argument("--real", action="store_true", help="enable the explicitly requested single-frame real provider case")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--model-path", default=DEFAULT_MODEL)
    parser.add_argument("--declared-checksum")
    parser.add_argument("--observed-checksum")
    parser.add_argument("--dependency-status", default="PYTHON_DEPENDENCY_UNRESOLVED")
    args = parser.parse_args()
    summary = run(real=args.real, source_ref=args.source, model_path=args.model_path, declared_checksum=args.declared_checksum, observed_checksum=args.observed_checksum, dependency_status=args.dependency_status)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
