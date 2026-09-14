from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = repo_root_from(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_engine_v1 import ARouteProductLoopIntegrationEngineV1  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_runtime_product_loop_controlled_integration_v1 import _check_case as _check_s0_case  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_s1_real_user_input_controlled_replacement_v1 import _check as _check_value  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_s1_real_user_input_controlled_replacement_v1 import _s1_case_result  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_fixture_v1 import build_fixture_cases  # noqa: E402
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_fixture_v1 import build_s1_fixture_cases  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_active_observation_control_engine_v1 import FieldPerceptionActiveObservationControlEngineV1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import build_vision_provider_admission_candidate_v1, deduplicate_visual_evidence_v1, run_authorized_vision_provider_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_binding_seam_v1 import CanonicalYOLO11nBindingContextV1, build_canonical_yolo11n_provider_admission_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_context_builder_v1 import CanonicalYOLO11nUpstreamRecordsV1, build_canonical_yolo11n_context_v1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_fixture_v1 import S3FixtureCaseV1, build_s3_fixture_cases  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_adapter_v1 import adapt_raw_camera_source  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_types_v1 import RawFrameRecordV1  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.run_a_route_s2_real_raw_camera_input_stream_controlled_replacement_v1 import _result_for_case as _s2_case_result  # noqa: E402
from capabilities.midplatform.field_perception_orchestrator.integration.raw_camera_stream_fixture_v1 import build_s2_fixture_cases  # noqa: E402


OUT_DIR = ROOT / "_eval_out/a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1"
FALSE_GUARDS = {
    "provider_autonomous_execution": False,
    "ocr_execution": False,
    "slam_execution": False,
    "vio_execution": False,
    "vlm_execution": False,
    "semantic_interpretation": False,
    "semantic_compression": False,
    "provider_semantic_authority": False,
    "automatic_fact_admission": False,
    "field_state_direct_mutation": False,
    "current_world_truth_declaration": False,
    "intent_mutation": False,
    "task_mutation": False,
    "decision_mutation": False,
    "real_action_execution": False,
    "real_runtime_execution": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "model_call": False,
    "scheduler_execution": False,
    "cross_user_transfer": False,
    "emotion_engine_execution": False,
    "b_route_execution": False,
}


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def _synthetic_frame(case_id: str, *, source_ref: Optional[str] = None, source_type: str = "IMAGE_FILE") -> Optional[RawFrameRecordV1]:
    source = source_ref or f"synthetic://s3/vision/{case_id}"
    mode = "REAL" if source_ref else "SYNTHETIC_REGRESSION"
    demand = f"demand:s3:{case_id}"
    adapted = adapt_raw_camera_source(
        source,
        source_type=source_type,
        observation_demand_ref=demand,
        source_mode=mode,
        session_id=f"s3-session:{case_id}",
        frame_id=f"s3-frame:{case_id}",
        width=640,
        height=480,
        captured_at=1700000000000,
    )
    return adapted.frames[0] if adapted.frames else None


def _control_payload(case: S3FixtureCaseV1) -> Dict[str, Any]:
    received = ("VISION_DETECTION",) if case.received_evidence else ()
    return {
        "case_id": case.case_id,
        "root_cycle_trace_id": f"trace:s3:cycle:{case.case_id}",
        "information_need": case.information_need,
        "task_ref": f"task:s3:{case.case_id}" if case.information_need else "",
        "intent_ref": f"intent:s3:{case.case_id}" if case.information_need else "",
        "target_semantic": "bounded visual target",
        "spatial_scope": "authorized observation region",
        "requested_capability_kinds": case.requested_capability_kinds,
        "expected_evidence_kinds": case.expected_evidence_kinds,
        "provider_admission_candidate": case.provider_admitted,
        "provider_candidate_ref": f"provider-candidate:s3:{case.case_id}",
        "selected_model_candidate_ref": f"model-candidate:s3:{case.case_id}",
        "received_evidence_kinds": received,
        "received_evidence_refs": (f"evidence:s3:{case.case_id}",) if case.received_evidence else (),
        "contradiction_refs": (f"contradiction:s3:{case.case_id}",) if case.contradiction else (),
        "cross_modal_contradiction": case.contradiction,
        "provider_failure": case.provider_failure,
        "budget_exhausted": case.budget_exhausted,
        "fallback_available": False,
        "target_coverage": case.received_evidence,
        "semantic_coverage": case.received_evidence,
        "temporal_validity": {"stale": False, "expired": False},
        "resource_budget": {"max_frames": 1, "max_duration_ms": 5000},
    }


def _admission_from_control(control: Any, case: S3FixtureCaseV1) -> Any:
    session = control.provider_session
    request = control.request
    requirement = control.capability_requirement
    return build_vision_provider_admission_candidate_v1(
        observation_demand_ref=control.demand.demand_id,
        observation_request_ref=request.request_id if request else "",
        capability_requirement_ref=requirement.requirement_id if requirement else "",
        provider_session_ref=session.session_id if session else "",
        provider_candidate_ref=f"provider-candidate:s3:{case.case_id}",
        model_candidate_ref=f"model-candidate:s3:{case.case_id}",
        model_admission_ref=f"model-admission:s3:{case.case_id}" if session else "",
        region_scope_candidate=request.target_region_candidate if request else "",
        expected_evidence=case.expected_evidence_kinds,
        bounded=bool(session),
        provider_admitted=case.provider_admitted,
        trace_ref=control.trace.control_trace_ref,
        provenance_refs=control.trace.provenance_refs,
    )


def _run_s3_case(case: S3FixtureCaseV1) -> Dict[str, Any]:
    control_engine = FieldPerceptionActiveObservationControlEngineV1()
    control = control_engine.run_case(_control_payload(case))
    frame = _synthetic_frame(case.case_id)
    admission = _admission_from_control(control, case)
    seen = ()
    if case.duplicate_inference and control.provider_session is not None and frame is not None:
        seen = (f"inference:{frame.frame_id}:{control.provider_session.session_id}",)
    provider = run_authorized_vision_provider_v1(
        frame,
        admission,
        execute_real_provider=False,
        provider_failure=case.provider_failure,
        budget_exhausted=case.budget_exhausted,
        seen_inference_ids=seen,
    )
    authorization_expected = bool(
        case.information_need and case.provider_admitted and case.requested_capability_kinds
    )
    checks = [
        _check_value("provider_admission_authorized", admission.provider_invocation_authorized, authorization_expected),
        _check_value("accepted", provider.accepted, case.expected_accept),
        _check_value("error_code", provider.error_code, case.expected_error),
        _check_value("candidate_only", provider.candidate_only, True),
        _check_value("provider_autonomous_execution", provider.provider_autonomous_execution, False),
        _check_value("semantic_interpretation", provider.semantic_interpretation, False),
        _check_value("semantic_compression", provider.semantic_compression, False),
        _check_value("provider_semantic_authority", provider.provider_semantic_authority, False),
    ]
    if case.expected_accept:
        evidence = provider.evidence[0] if provider.evidence else None
        checks.extend([
            _check_value("evidence_present", bool(provider.evidence), True),
            _check_value("gateway_handoff_candidate", bool(provider.gateway_handoff), True),
            _check_value("gateway_admission", provider.gateway_handoff.gateway_admission if provider.gateway_handoff else True, False),
            _check_value("truth_declared", evidence.truth_declared if evidence else True, False),
            _check_value("fact_admitted", evidence.fact_admitted if evidence else True, False),
            _check_value("field_mutation", evidence.field_mutation if evidence else True, False),
            _check_value("current_world_mutation", evidence.current_world_mutation if evidence else True, False),
            _check_value("intent_created", evidence.intent_created if evidence else True, False),
            _check_value("task_created", evidence.task_created if evidence else True, False),
            _check_value("natural_language_conclusion", evidence.natural_language_conclusion_ref if evidence else "unexpected", ""),
        ])
    if case.case_id in {"S3-06", "S3-07", "S3-08", "S3-09", "S3-10", "S3-11"}:
        evidence = provider.evidence[0] if provider.evidence else None
        checks.extend([
            _check_value("bbox_preserved", bool(evidence and len(evidence.bbox) == 4), True),
            _check_value("confidence_preserved", bool(evidence and 0.0 <= evidence.confidence <= 1.0), True),
            _check_value("provider_ref_preserved", bool(evidence and evidence.provider_ref), True),
            _check_value("model_ref_preserved", bool(evidence and evidence.model_ref), True),
            _check_value("frame_ref_preserved", evidence.frame_ref if evidence else "", frame.frame_id if frame else ""),
            _check_value("trace_reverse_lookup", bool(evidence and evidence.trace_ref and evidence.provenance_refs), True),
        ])
    if case.case_id in {"S3-13", "S3-14", "S3-15", "S3-16"}:
        evidence = provider.evidence[0] if provider.evidence else None
        field = {"S3-13": "field_mutation", "S3-14": "current_world_mutation", "S3-15": "intent_created", "S3-16": "task_created"}[case.case_id]
        checks.append(_check_value(field, getattr(evidence, field, True) if evidence else True, False))
    if case.case_id in {"S3-17", "S3-18", "S3-19", "S3-27"}:
        checks.extend([
            _check_value("ocr_invocation", provider.ocr_invocation, False),
            _check_value("slam_invocation", provider.slam_invocation, False),
            _check_value("vlm_invocation", provider.vlm_invocation, False),
            _check_value("semantic_compression", provider.semantic_compression, False),
        ])
    if case.case_id == "S3-05":
        checks.extend([
            _check_value("bounded_session", admission.bounded, True),
            _check_value("session_ref", bool(admission.provider_session_ref), True),
            _check_value("authorized_capability", admission.required_capability_kind, "VISION_DETECTION"),
            _check_value("region_scope_recorded", bool(provider.region_scope_candidate), True),
            _check_value("region_scope_enforced", provider.region_scope_enforced, False),
            _check_value("region_limitation_recorded", bool(provider.region_scope_limitation), True),
        ])
    if case.case_id == "S3-20":
        checks.append(_check_value("control_decision", control.control_decision.decision, "STOP"))
    if case.case_id == "S3-21":
        checks.append(_check_value("control_decision", control.control_decision.decision, "CONTINUE"))
    if case.case_id == "S3-22":
        checks.append(_check_value("control_decision", control.control_decision.decision, "RECONSIDER"))
    if case.case_id == "S3-26":
        unique, duplicate = deduplicate_visual_evidence_v1(provider.evidence, seen_evidence_ids=tuple(item.evidence_id for item in provider.evidence))
        checks.extend([
            _check_value("duplicate_evidence", duplicate, True),
            _check_value("duplicate_unique_count", len(unique), 0),
        ])
    actual = {
        "control": jsonable(control),
        "admission": jsonable(admission),
        "provider": jsonable(provider),
        "raw_frame_ref": frame.frame_id if frame else "",
    }
    return {"scenario_id": case.case_id, "title": case.title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": actual}


def _real_case(source_ref: str, source_type: str, model_path: str, canonical_binding: Optional[CanonicalYOLO11nBindingContextV1] = None) -> Dict[str, Any]:
    case = S3FixtureCaseV1("S3-REAL", "user-provided real YOLO evidence", received_evidence=True)
    control = FieldPerceptionActiveObservationControlEngineV1().run_case(_control_payload(case))
    frame = _synthetic_frame(case.case_id, source_ref=source_ref, source_type=source_type)
    session = control.provider_session
    request = control.request
    requirement = control.capability_requirement
    seam = build_canonical_yolo11n_provider_admission_v1(
        context=canonical_binding,
        observation_demand_ref=control.demand.demand_id,
        observation_request_ref=request.request_id if request else "",
        capability_requirement_ref=requirement.requirement_id if requirement else "",
        provider_session_ref=session.session_id if session else "",
        provider_candidate_ref=f"provider-candidate:s3:{case.case_id}",
        region_scope_candidate=request.target_region_candidate if request else "",
        expected_evidence=case.expected_evidence_kinds,
        bounded=bool(session),
        trace_ref=control.trace.control_trace_ref,
    )
    admission = seam.admission
    canonical_ready = seam.validation.valid
    provider = run_authorized_vision_provider_v1(frame, admission, execute_real_provider=True, model_path=model_path)
    checks = [
        _check_value("authorized", admission.provider_invocation_authorized, canonical_ready),
        _check_value("accepted", provider.accepted, canonical_ready),
        _check_value("provider_invocation", provider.invocation_performed, canonical_ready),
        _check_value("candidate_evidence", bool(provider.evidence), canonical_ready),
        _check_value("truth_declared", all(not item.truth_declared for item in provider.evidence), True),
        _check_value("field_mutation", provider.field_mutation, False),
        _check_value("ocr_execution", provider.ocr_invocation, False),
        _check_value("slam_execution", provider.slam_invocation, False),
        _check_value("vlm_execution", provider.vlm_invocation, False),
    ]
    return {"scenario_id": case.case_id, "title": case.title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": {"control": jsonable(control), "admission": jsonable(admission), "provider": jsonable(provider)}}


def run(*, source_ref: Optional[str] = None, source_type: str = "IMAGE_FILE", model_path: str = "", user_input: Optional[str] = None, canonical_upstream_records: Optional[CanonicalYOLO11nUpstreamRecordsV1] = None) -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = ARouteProductLoopIntegrationEngineV1()
    s0_cases = [_check_s0_case(engine, case) for case in build_fixture_cases()]
    s1_cases = [_s1_case_result(engine, case) for case in build_s1_fixture_cases()]
    s2_cases = [_s2_case_result(case) for case in build_s2_fixture_cases()]
    s3_cases = [_run_s3_case(case) for case in build_s3_fixture_cases()]
    if source_ref:
        constructed_context = build_canonical_yolo11n_context_v1(canonical_upstream_records)
        effective_binding = constructed_context.context if constructed_context.validation.valid else None
        s3_cases.append(_real_case(source_ref, source_type, model_path, effective_binding))
    failed_s0 = [item["scenario_id"] for item in s0_cases if not item["all_checks_passed"]]
    failed_s1 = [item["scenario_id"] for item in s1_cases if not item["all_checks_passed"]]
    failed_s2 = [item["scenario_id"] for item in s2_cases if not item["all_checks_passed"]]
    regression_case = next(item for item in s3_cases if item["scenario_id"] == "S3-28")
    regression_case["checks"].extend([
        _check_value("s0_regression", not failed_s0, True),
        _check_value("s1_regression", not failed_s1, True),
        _check_value("s2_regression", not failed_s2, True),
    ])
    regression_case["all_checks_passed"] = all(item["passed"] for item in regression_case["checks"])
    failed_s3 = [item["scenario_id"] for item in s3_cases if not item["all_checks_passed"]]
    real_executed = any(item.get("scenario_id") == "S3-REAL" and item.get("actual", {}).get("provider", {}).get("invocation_performed") for item in s3_cases)
    summary = {
        "mode": "HYBRID_S3_REAL_VISION_YOLO" if source_ref else "SYNTHETIC_REGRESSION",
        "real_components": (["USER_INPUT"] if user_input else []) + (["RAW_CAMERA_INPUT_STREAM", "VISION_YOLO_EVIDENCE"] if source_ref else []),
        "synthetic_components": ["OCR", "SLAM/VIO", "VLM", "Context/World", "Cognitive Chain", "Task/Action", "Runtime", "Outcome Feedback", "User Output"],
        "s3_scenario_count": len(s3_cases),
        "s0_scenario_count": len(s0_cases),
        "s1_scenario_count": len(s1_cases),
        "s2_scenario_count": len(s2_cases),
        "s0_all_cases_passed": not failed_s0,
        "s1_all_cases_passed": not failed_s1,
        "s2_all_cases_passed": not failed_s2,
        "s3_all_cases_passed": not failed_s3,
        "all_cases_passed": not (failed_s0 or failed_s1 or failed_s2 or failed_s3),
        "failed_case_ids": failed_s3 + failed_s2 + failed_s1 + failed_s0,
        "vision_yolo_execution": real_executed,
        "provider_autonomous_continuous_execution": False,
        "ocr_execution": False,
        "slam_execution": False,
        "vio_execution": False,
        "vlm_execution": False,
        "semantic_interpretation": False,
        "semantic_compression": False,
        "provider_semantic_authority": False,
        "automatic_fact_admission": False,
        "field_state_direct_mutation": False,
        "current_world_truth_declaration": False,
        "intent_mutation": False,
        "task_mutation": False,
        "decision_mutation": False,
        "real_action_execution": False,
        "real_runtime_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "model_call": real_executed,
        "scheduler_execution": False,
        "cross_user_transfer": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "do_not_persist_raw_content": True,
        "training_use": False,
        "user_input_adapter_accepted": bool(user_input),
    }
    (OUT_DIR / "a_route_s3_real_vision_yolo_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_real_vision_yolo_case_results_v1.json").write_text(json.dumps(s3_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_s0_regression_case_results_v1.json").write_text(json.dumps(s0_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_s1_regression_case_results_v1.json").write_text(json.dumps(s1_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s3_s2_regression_case_results_v1.json").write_text(json.dumps(s2_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    trace = {
        "provenance_grants_authority": False,
        "reverse_lookup": "S3 visual evidence -> provider output -> frame reference -> bounded session -> observation demand -> source",
        "s3_cases": [item.get("actual") for item in s3_cases if item.get("scenario_id") in {"S3-01", "S3-06", "S3-11", "S3-20"}],
    }
    (OUT_DIR / "a_route_s3_real_vision_yolo_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="S3 real vision/YOLO structured evidence controlled replacement")
    parser.add_argument("--source", default=None, help="external image/frame reference accepted from S2")
    parser.add_argument("--source-type", default="IMAGE_FILE", choices=("IMAGE_FILE", "FRAME_REFERENCE", "IMAGE_SEQUENCE"))
    parser.add_argument("--model-path", default="", help="existing local YOLO model file; no download")
    parser.add_argument("--user-input", default=None, help="optional S1 real-input marker")
    args = parser.parse_args()
    summary = run(source_ref=args.source, source_type=args.source_type, model_path=args.model_path, user_input=args.user_input)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
