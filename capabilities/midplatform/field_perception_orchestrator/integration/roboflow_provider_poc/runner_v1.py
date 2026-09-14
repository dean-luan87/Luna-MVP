from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

from .cognitive_loop_adapter_v1 import build_roboflow_cognitive_loop_candidates_v1
from .evidence_translator_v1 import (
    build_roboflow_observation_gateway_handoff_candidate_v1,
    translate_roboflow_result_to_luna_evidence_v1,
)
from .fixtures_v1 import rf_detr_normalization_cases_v1, structural_cases_v1
from .provider_client_v1 import (
    build_roboflow_provider_request_v1,
    invoke_roboflow_provider_v1,
)
from .types_v1 import PROVIDER_REF
from .rf_detr_declaration_validator_v1 import inspect_rf_detr_declarations_v1


REPO_PROVIDER_REGISTRY = Path("capabilities/midplatform/model_manager/registry/provider_registry_v1.json")


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    return value


def _provider_declaration_present() -> bool:
    if not REPO_PROVIDER_REGISTRY.is_file():
        return False
    try:
        registry = json.loads(REPO_PROVIDER_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return any(item.get("provider_id") == PROVIDER_REF for item in registry.get("providers") or ())


def _expected_evidence_kinds(request: Any) -> tuple[str, ...]:
    capability_to_kind = (
        ("object_detection", "VISION_DETECTION"),
        ("text_recognition", "OCR_TEXT_EVIDENCE"),
    )
    requested = set(request.requested_capabilities)
    return tuple(kind for capability, kind in capability_to_kind if capability in requested)


def _run_case(case: Mapping[str, Any], *, real_mode: bool) -> Dict[str, Any]:
    request_data = dict(case["request"])
    request = build_roboflow_provider_request_v1(real_mode=real_mode, **request_data)
    native = invoke_roboflow_provider_v1(
        request,
        native_payload=None if real_mode else case.get("native_payload"),
    )
    normalized = translate_roboflow_result_to_luna_evidence_v1(
        native,
        frame_ref=request.frame_ref,
        roi_ref=request.roi_ref,
    )
    gateway_handoff = build_roboflow_observation_gateway_handoff_candidate_v1(normalized)
    concern_ref = request.concern_ref or "concern:exit-poc"
    goal_refs = (request.goal_ref,) if request.goal_ref else ("goal:find-likely-exit",)
    semantic_assessment = None if real_mode else case.get("semantic_assessment")
    cognitive = build_roboflow_cognitive_loop_candidates_v1(
        normalized,
        concern_ref=concern_ref,
        goal_refs=goal_refs,
        requirement_ref=request.capability_requirement_ref,
        grant_refs=request.grant_refs,
        intent_refs=("intent:exit-poc",),
        context_refs=("context:room-environment-poc",),
        observation_refs=(request.observation_request_ref,),
        semantic_assessment=semantic_assessment,
        decision_candidate=case.get("decision_candidate"),
        expected_evidence_kinds=_expected_evidence_kinds(request),
    )
    output = {
        "case_id": case.get("case_id"),
        "mode": "real" if real_mode else "structural",
        "request_id": request.request_id,
        "goal_ref": request.goal_ref or "goal:find-likely-exit",
        "concern_ref": request.concern_ref or "concern:exit-poc",
        "provider_ref": request.provider_ref,
        "workflow_ref": request.workflow_ref,
        "model_refs": list(request.model_refs),
        "workflow_output_mapping": dict(request.workflow_output_mapping),
        "semantic_assessment_supplied": semantic_assessment is not None,
        "provider_declaration_present": _provider_declaration_present(),
        "actual_provider_response": native.actual_provider_response,
        "provider_invocation": native.actual_provider_response,
        "response_shape_diagnostics": dict(native.response_shape_diagnostics),
        "raw_roboflow_payload_not_canonical": normalized.raw_roboflow_payload_not_canonical,
        "provider_result_accepted": normalized.accepted,
        "normalization_error_class": normalized.error_class,
        "normalization_error_detail": normalized.error_detail,
        "detection_evidence_count": len(normalized.detection_evidence),
        "ocr_evidence_count": len(normalized.ocr_evidence),
        "evidence_refs": [
            item.evidence_id
            for item in (*normalized.detection_evidence, *normalized.ocr_evidence)
        ],
        "legal_empty_predictions": bool(
            normalized.accepted
            and not normalized.detection_evidence
            and not normalized.ocr_evidence
        ),
        "observation_gateway_handoff_present": gateway_handoff is not None,
        "observation_gateway_handoff_candidate_only": bool(
            gateway_handoff and gateway_handoff.candidate_only
        ),
        "observation_gateway_handoff_admission": bool(
            gateway_handoff and gateway_handoff.gateway_admission
        ),
        "observation_gateway_handoff_evidence_refs": list(
            gateway_handoff.evidence_refs if gateway_handoff else ()
        ),
        "current_world_candidate_present": cognitive.current_world_candidate is not None,
        "hypothesis_candidate_present": cognitive.hypothesis_candidate is not None,
        "sufficiency_candidate_present": cognitive.sufficiency_candidate is not None,
        "sufficiency_status": cognitive.sufficiency_candidate.status if cognitive.sufficiency_candidate else "",
        "next_observation_candidate_present": cognitive.next_observation_candidate is not None,
        "decision_candidate_present": cognitive.decision_candidate is not None,
        "decision_candidate_owner": getattr(cognitive.decision_candidate, "owner", ""),
        "next_target": (
            "Decision Governance"
            if cognitive.sufficiency_candidate and cognitive.sufficiency_candidate.status == "SUFFICIENT"
            else "Observation"
            if cognitive.next_observation_candidate is not None
            else ""
        ),
        "hypothesis_id": cognitive.hypothesis_candidate.hypothesis_id if cognitive.hypothesis_candidate else "",
        "hypothesis_revision_parent_ref": (
            cognitive.hypothesis_candidate.revision_parent_ref
            if cognitive.hypothesis_candidate and cognitive.hypothesis_candidate.revision_parent_ref
            else ""
        ),
        "information_gap": list(cognitive.information_gap),
        "requested_capabilities": list(request.requested_capabilities),
        "roi_ref": request.roi_ref,
        "next_observation_request_ref": (
            cognitive.next_observation_candidate.observation_request_ref
            if cognitive.next_observation_candidate
            else ""
        ),
        "next_observation_demand_ref": (
            cognitive.next_observation_candidate.observation_demand_ref
            if cognitive.next_observation_candidate
            else ""
        ),
        "next_observation_correction_refs": (
            list(cognitive.next_observation_candidate.correction_refs)
            if cognitive.next_observation_candidate
            else []
        ),
        "trace_refs": list(cognitive.trace_refs),
        "provenance_refs": list(cognitive.provenance_refs),
        "source_version_refs": list(cognitive.source_version_refs),
        "invalidation_refs": list(cognitive.invalidation_refs),
        "evidence_provider_ref": normalized.provider_ref,
        "evidence_workflow_ref": normalized.workflow_ref,
        "evidence_model_refs": list(normalized.model_refs),
        "cognitive_source_owner": cognitive.cognitive_source_owner,
        "candidate_only": cognitive.candidate_only,
        "world_truth_declared": cognitive.world_truth_declared,
        "field_mutation": cognitive.field_mutation,
        "task_created": cognitive.task_created,
        "action_executed": cognitive.action_executed,
        "provider_autonomous_reobservation": cognitive.provider_autonomous_reobservation,
        "failure_class": cognitive.failure_class,
        "failure_reason": cognitive.failure_reason,
    }
    output["passed"] = bool(
        output["provider_declaration_present"]
        and output["raw_roboflow_payload_not_canonical"]
        and output["provider_result_accepted"]
        and output["current_world_candidate_present"]
        and output["hypothesis_candidate_present"]
        and output["sufficiency_candidate_present"]
        and (
            output["next_observation_candidate_present"]
            or output["decision_candidate_present"]
            or output["next_target"] == "Decision Governance"
        )
        and output["candidate_only"]
        and not output["world_truth_declared"]
        and not output["field_mutation"]
        and not output["task_created"]
        and not output["action_executed"]
        and not output["provider_autonomous_reobservation"]
        and not output["failure_class"]
    )
    output["failure"] = None if output["passed"] else {
        "classification": output["failure_class"] or "COGNITIVE_LOOP_STRUCTURAL_CONDITION_FAILED",
        "reason": output["failure_reason"] or "required candidate boundary or guard was not satisfied",
    }
    return output


def _negative_checks() -> Dict[str, bool]:
    case = structural_cases_v1()[0]
    request = build_roboflow_provider_request_v1(real_mode=False, **case["request"])
    missing_provenance = False
    try:
        build_roboflow_provider_request_v1(
            **{**case["request"], "provenance_refs": ()},
            real_mode=False,
        )
    except ValueError:
        missing_provenance = True
    missing_frame_or_roi = False
    try:
        build_roboflow_provider_request_v1(
            **{**case["request"], "frame_ref": ""},
            real_mode=False,
        )
    except ValueError:
        missing_frame_or_roi = True
    stale_native = invoke_roboflow_provider_v1(
        replace(request, invalidation_refs=("invalidation:provider-result-stale",)),
    )
    stale_result_blocked = not translate_roboflow_result_to_luna_evidence_v1(
        stale_native,
        frame_ref=request.frame_ref,
        roi_ref=request.roi_ref,
    ).accepted
    conflict_native = invoke_roboflow_provider_v1(
        request,
        native_payload={
            "predictions": [{"id": "door-conflict", "class": "door", "confidence": 0.51, "bbox": [0, 0, 10, 10], "contradiction_refs": ["conflict:ocr-door"]}],
            "ocr": [{"id": "text-conflict", "text": "not-exit", "confidence": 0.52}],
        },
    )
    conflict_normalized = translate_roboflow_result_to_luna_evidence_v1(
        conflict_native,
        frame_ref=request.frame_ref,
        roi_ref=request.roi_ref,
    )
    conflict_preserved = bool(conflict_normalized.detection_evidence and conflict_normalized.detection_evidence[0].contradiction_refs)
    raw_isolated = "payload" not in _jsonable(conflict_normalized) and "raw_roboflow_payload" not in _jsonable(conflict_normalized)
    mutation_guard = not conflict_normalized.truth_declared and not conflict_normalized.field_mutation and not conflict_normalized.current_world_mutation
    autonomous_guard = not build_roboflow_cognitive_loop_candidates_v1(
        conflict_normalized,
        concern_ref="concern:exit-poc",
        goal_refs=("goal:find-likely-exit",),
        requirement_ref=request.capability_requirement_ref,
        grant_refs=request.grant_refs,
        semantic_assessment={**case["semantic_assessment"], "provider_autonomous_reobservation": True},
    ).accepted
    return {
        "missing_provenance_fail_closed": missing_provenance,
        "missing_frame_fail_closed": missing_frame_or_roi,
        "stale_provider_result_blocked": stale_result_blocked,
        "detection_ocr_conflict_preserved": conflict_preserved,
        "raw_schema_isolated": raw_isolated,
        "mutation_guards_hold": mutation_guard,
        "provider_autonomous_reobservation_blocked": autonomous_guard,
    }


def _run_rf_detr_normalization_case(case: Mapping[str, Any]) -> Dict[str, Any]:
    request = build_roboflow_provider_request_v1(real_mode=False, **dict(case["request"]))
    native = invoke_roboflow_provider_v1(request, native_payload=case.get("native_payload"))
    normalized = translate_roboflow_result_to_luna_evidence_v1(
        native,
        frame_ref=request.frame_ref,
        roi_ref=request.roi_ref,
    )
    gateway_handoff = build_roboflow_observation_gateway_handoff_candidate_v1(normalized)
    normalized_json = _jsonable(normalized)
    canonical_fields_only = "payload" not in normalized_json and "provider_extra" not in normalized_json
    evidence_identity_ok = all(
        item.provider_ref == request.provider_ref
        and item.model_ref == request.model_refs[0]
        and item.frame_ref == request.frame_ref
        and item.region_ref == request.roi_ref
        and item.trace_ref
        and item.provenance_refs
        for item in normalized.detection_evidence
    )
    handoff_boundary_ok = (
        gateway_handoff is None
        if not normalized.detection_evidence and not normalized.ocr_evidence
        else bool(
            gateway_handoff
            and gateway_handoff.candidate_only
            and not gateway_handoff.gateway_admission
            and not gateway_handoff.semantic_authority
            and gateway_handoff.provider_ref == request.provider_ref
            and gateway_handoff.source_frame_ref == request.frame_ref
            and gateway_handoff.evidence_refs
            and gateway_handoff.trace_ref
            and gateway_handoff.provenance_refs
            and gateway_handoff.raw_output_refs == (normalized.result_id,)
        )
    )
    passed = bool(
        normalized.accepted is bool(case.get("expected_accepted"))
        and len(normalized.detection_evidence) == int(case.get("expected_detection_count", 0))
        and normalized.raw_roboflow_payload_not_canonical
        and canonical_fields_only
        and evidence_identity_ok
        and handoff_boundary_ok
        and normalized.candidate_only
        and not normalized.truth_declared
        and not normalized.field_mutation
        and not normalized.current_world_mutation
    )
    return {
        "case_id": case.get("case_id"),
        "accepted": normalized.accepted,
        "expected_accepted": bool(case.get("expected_accepted")),
        "detection_evidence_count": len(normalized.detection_evidence),
        "expected_detection_count": int(case.get("expected_detection_count", 0)),
        "provider_ref": normalized.provider_ref,
        "workflow_ref": normalized.workflow_ref,
        "model_refs": list(normalized.model_refs),
        "trace_ref": normalized.trace_ref,
        "provenance_refs": list(normalized.provenance_refs),
        "error_class": normalized.error_class,
        "raw_roboflow_payload_not_canonical": normalized.raw_roboflow_payload_not_canonical,
        "canonical_fields_only": canonical_fields_only,
        "evidence_identity_ok": evidence_identity_ok,
        "observation_gateway_handoff_present": gateway_handoff is not None,
        "observation_gateway_handoff": _jsonable(gateway_handoff),
        "handoff_boundary_ok": handoff_boundary_ok,
        "candidate_only": normalized.candidate_only,
        "truth_declared": normalized.truth_declared,
        "field_mutation": normalized.field_mutation,
        "current_world_mutation": normalized.current_world_mutation,
        "passed": passed,
    }


def run_structural() -> Dict[str, Any]:
    cases = [_run_case(case, real_mode=False) for case in structural_cases_v1()]
    negative = _negative_checks()
    rf_detr_declarations = inspect_rf_detr_declarations_v1(Path("."))
    rf_detr_cases = [_run_rf_detr_normalization_case(case) for case in rf_detr_normalization_cases_v1()]
    return {
        "phase": "Phase-P1-Luna-Roboflow-Integrated-Vision-Provider-Cognitive-Loop-PoC-Controlled-Implementation-v1-001",
        "mode": "structural",
        "case_count": len(cases),
        "cases": cases,
        "rf_detr_declaration_checks": rf_detr_declarations["checks"],
        "rf_detr_normalization_cases": rf_detr_cases,
        "rf_detr_normalization_cases_passed": all(bool(case.get("passed")) for case in rf_detr_cases),
        "rf_detr_observation_gateway_handoff_cases_passed": bool(rf_detr_cases)
        and all(bool(case.get("handoff_boundary_ok")) for case in rf_detr_cases),
        "rf_detr_declarations_passed": bool(rf_detr_declarations.get("all_checks_passed")),
        "negative_cases": negative,
        "all_cases_passed": all(bool(case.get("passed")) for case in cases)
        and all(bool(case.get("passed")) for case in rf_detr_cases)
        and bool(rf_detr_declarations.get("all_checks_passed")),
        "all_negative_cases_passed": all(negative.values()),
        "actual_provider_response": False,
        "provider_invocation": False,
        "observation_execution": False,
        "task_execution": False,
        "action_execution": False,
        "source_mutation": False,
        "world_truth_declared": False,
        "raw_roboflow_payload_not_canonical": all(bool(case.get("raw_roboflow_payload_not_canonical")) for case in cases),
    }


def run_real(input_path: Path) -> Dict[str, Any]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    case = {
        "case_id": str(payload.get("case_id") or "real_roboflow_case"),
        "request": dict(payload["request"]),
    }
    result = _run_case(case, real_mode=True)
    return {
        "phase": "Phase-P1-Luna-Roboflow-Integrated-Vision-Provider-Cognitive-Loop-PoC-Controlled-Implementation-v1-001",
        "mode": "real",
        "case_count": 1,
        "cases": [result],
        "all_cases_passed": bool(result.get("passed")),
        "all_negative_cases_passed": None,
        "actual_provider_response": bool(result.get("actual_provider_response")),
        "provider_invocation": bool(result.get("actual_provider_response")),
        "observation_execution": False,
        "task_execution": False,
        "action_execution": False,
        "source_mutation": False,
        "world_truth_declared": False,
        "raw_roboflow_payload_not_canonical": bool(result.get("raw_roboflow_payload_not_canonical")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Controlled Roboflow Luna cognitive-loop PoC runner")
    parser.add_argument("--mode", choices=("structural", "real"), default="structural")
    parser.add_argument("--input", type=Path, help="real-mode governed request and A-assessment JSON")
    parser.add_argument("--output", type=Path, default=Path("_tmp_eval_out/roboflow_provider_poc/runner_summary_v1.json"))
    args = parser.parse_args()
    if args.mode == "real" and args.input is None:
        raise SystemExit("real mode requires --input; no implicit or fixture success is allowed")
    summary = run_structural() if args.mode == "structural" else run_real(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
