"""User-terminal runner for provider-result to observation ingress."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict

from .engine_v1 import ProviderRuntimeObservationIngressEngineV1
from .fixtures_v1 import (
    build_provider_observation_cases_v1,
    malformed_provider_result_case_v1,
    provider_unavailable_case_v1,
    reobservation_case_v1,
    unresolved_capability_case_v1,
)


OUTPUT_DIR = Path("_eval_out/provider_runtime_to_observation_ingress_v1")
ENGINE = ProviderRuntimeObservationIngressEngineV1()


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": _jsonable(observed)}


def _no_downstream_execution(result: Any) -> bool:
    stages = result.details.get("a_route", {}).get("stage_results", [])
    return not any(item.get("stage_id") in {"DECISION", "TASK", "ACTION", "EXECUTION"} for item in stages)


def _positive(case: Any) -> Dict[str, Any]:
    result = ENGINE.run_case(case)
    request = result.provider_request
    provider_result = result.provider_result
    runtime_observation = result.details.get("runtime_observation", {})
    gateway = result.details.get("gateway", {})
    route = result.details.get("a_route", {})
    proof = route.get("cognitive_execution", {}) if isinstance(route, dict) else {}
    gateway_evidence = gateway.get("evidence", []) if isinstance(gateway, dict) else []
    checks = [
        _check("demand_present", bool(result.demand_ref)),
        _check("capability_requirement_present", bool(result.capability_requirement_ref)),
        _check("capability_resolved", result.capability_resolution_status == "READY_CANDIDATE"),
        _check("provider_request_present", request is not None),
        _check("provider_result_present", provider_result is not None and provider_result.status == "SUCCESS"),
        _check("provider_provenance_retained", bool(request and request.provenance_refs and provider_result and provider_result.provenance_refs and set(request.provenance_refs).issubset(set(provider_result.provenance_refs)))),
        _check("provider_result_maps_to_observation", bool(provider_result and runtime_observation and runtime_observation.get("provider_ref") == provider_result.provider_ref and runtime_observation.get("capability_ref") == provider_result.capability_ref and runtime_observation.get("raw_result_ref") == provider_result.raw_result_ref)),
        _check(
            "observation_provenance_retained",
            bool(
                request
                and runtime_observation
                and set(request.provenance_refs).issubset(
                    set(runtime_observation.get("provenance_refs", ()))
                )
                and set(request.trace_refs).issubset(
                    set(runtime_observation.get("trace_refs", ()))
                )
            ),
        ),
        _check("provider_result_not_world_truth", provider_result is not None and provider_result.truth_declared is False and runtime_observation.get("truth_declared") is False),
        _check("runtime_observation_present", bool(result.runtime_observation_ref)),
        _check("gateway_admitted", bool(result.gateway_admission_ref)),
        _check("evidence_present", bool(result.evidence_refs)),
        _check("evidence_candidate_not_fact", bool(gateway_evidence) and all(item.get("candidate_only") is True and item.get("fact_declared") is False for item in gateway_evidence)),
        _check("cognition_reached", bool(result.a_route_execution_ref and result.sufficiency_ref)),
        _check("conditioning_refs_preserved", bool(proof and tuple(proof.get("role_refs", ())) == tuple(case.role_refs) and tuple(proof.get("task_refs", ())) == (case.task_ref,) and tuple(proof.get("goal_refs", ())) == (case.goal_ref,) and tuple(proof.get("information_need_refs", ())) == (case.information_need_ref,))),
        _check("no_live_observation_execution", proof.get("live_observation_execution") is False),
        _check("no_provider_or_model_invocation", result.provider_invocation is False and result.model_invocation is False),
        _check("no_downstream_execution", _no_downstream_execution(result), result.details.get("a_route", {}).get("stage_results", [])),
    ]
    return {
        "case_id": case.case_id,
        "title": case.title,
        "capability_kind": case.capability_kind,
        "capability_ref": case.capability_ref,
        "modality": case.modality,
        "observation_demand_ref": result.demand_ref,
        "capability_requirement_ref": result.capability_requirement_ref,
        "capability_resolution_status": result.capability_resolution_status,
        "observation_request_ref": result.observation_request_ref,
        "reobservation_request_ref": result.reobservation_request_ref,
        "provider_request_ref": request.provider_request_ref if request else None,
        "provider_ref": request.provider_ref if request else None,
        "model_ref": request.model_ref if request else None,
        "provider_request_trace_refs": list(request.trace_refs) if request else [],
        "provider_request_provenance_refs": list(request.provenance_refs) if request else [],
        "provider_result_ref": provider_result.provider_result_ref if provider_result else None,
        "provider_result_status": provider_result.status if provider_result else None,
        "provider_result_truth_declared": provider_result.truth_declared if provider_result else None,
        "runtime_observation_ref": result.runtime_observation_ref,
        "runtime_observation_trace_refs": list(runtime_observation.get("trace_refs", ())),
        "runtime_observation_provenance_refs": list(runtime_observation.get("provenance_refs", ())),
        "gateway_admission_ref": result.gateway_admission_ref,
        "evidence_refs": list(result.evidence_refs),
        "a_route_execution_ref": result.a_route_execution_ref,
        "sufficiency_ref": result.sufficiency_ref,
        "information_gap_ref": result.information_gap_ref,
        "stop_ref": result.stop_ref,
        "provider_runtime_contract_verified": result.provider_runtime_contract_verified,
        "provider_real_execution_verified": result.provider_real_execution_verified,
        "provider_invocation": result.provider_invocation,
        "model_invocation": result.model_invocation,
        "live_observation_execution": False,
        "checks": checks,
        "validation_errors": list(result.errors),
        "all_checks_passed": not result.errors and all(item["passed"] for item in checks),
        "details": result.details,
    }


def _negative(case: Any, expected_error: str) -> Dict[str, Any]:
    result = ENGINE.run_case(case)
    checks = [
        _check("expected_failure", expected_error in result.errors, result.errors),
        _check("no_provider_call", result.provider_invocation is False and result.model_invocation is False),
        _check("no_fake_observation", result.runtime_observation_ref is None and result.evidence_refs == ()),
    ]
    return {
        "case_id": case.case_id,
        "expected_error": expected_error,
        "validation_errors": list(result.errors),
        "provider_request_ref": result.provider_request.provider_request_ref if result.provider_request else None,
        "runtime_observation_ref": result.runtime_observation_ref,
        "evidence_refs": list(result.evidence_refs),
        "provider_invocation": result.provider_invocation,
        "model_invocation": result.model_invocation,
        "live_observation_execution": False,
        "checks": checks,
        "all_checks_passed": all(item["passed"] for item in checks),
        "details": result.details,
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    positives = [_positive(case) for case in build_provider_observation_cases_v1()]
    reobservation_result = ENGINE.build_reobservation_provider_request(reobservation_case_v1())
    reobservation_request = reobservation_result.provider_request
    reobservation = {
        "case_id": "REOBSERVATION_TO_PROVIDER_REQUEST",
        "observation_demand_ref": reobservation_result.demand_ref,
        "observation_request_ref": reobservation_result.observation_request_ref,
        "reobservation_request_ref": reobservation_result.reobservation_request_ref,
        "next_cycle_ingress_ref": reobservation_result.next_cycle_ingress_ref,
        "provider_request_ref": reobservation_request.provider_request_ref if reobservation_request else None,
        "provider_ref": reobservation_request.provider_ref if reobservation_request else None,
        "capability_ref": reobservation_request.capability_ref if reobservation_request else None,
        "trace_refs": list(reobservation_request.trace_refs) if reobservation_request else [],
        "provider_invocation": reobservation_result.provider_invocation,
        "model_invocation": reobservation_result.model_invocation,
        "validation_errors": list(reobservation_result.errors),
        "checks": [
            _check("reobservation_demand_present", bool(reobservation_result.demand_ref)),
            _check("reobservation_next_cycle_present", bool(reobservation_result.next_cycle_ingress_ref)),
            _check("reobservation_provider_request_candidate", bool(reobservation_request and reobservation_result.reobservation_request_ref)),
            _check("reobservation_trace_carries_next_cycle", bool(reobservation_request and reobservation_result.next_cycle_ingress_ref in reobservation_request.trace_refs)),
            _check("reobservation_no_provider_call", reobservation_result.provider_invocation is False and reobservation_result.model_invocation is False),
        ],
        "details": reobservation_result.details,
    }
    reobservation["all_checks_passed"] = not reobservation["validation_errors"] and all(item["passed"] for item in reobservation["checks"])
    negatives = [
        _negative(provider_unavailable_case_v1(), "provider_result_unavailable"),
        _negative(malformed_provider_result_case_v1(), "provider_result_raw_result_ref_missing"),
        _negative(unresolved_capability_case_v1(), "capability_unresolved"),
    ]
    return {
        "phase": "Phase-P1-Luna-Real-Provider-Runtime-To-Observation-Ingress-Integration-v1-001",
        "execution_mode": "LIVE_RUNTIME",
        "provider_runtime_contract_verified": True,
        "provider_real_execution_verified": False,
        "provider_invocation": False,
        "model_invocation": False,
        "live_observation_execution": False,
        "decision_execution": False,
        "task_execution": False,
        "action_execution": False,
        "runtime_executor_invocation": False,
        "device_control": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "positive_cases": positives,
        "reobservation_case": reobservation,
        "negative_cases": negatives,
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "all_checks_passed": all(item["all_checks_passed"] for item in (*positives, reobservation, *negatives)),
        "status": "PROVIDER_RUNTIME_TO_OBSERVATION_INGRESS_RESULT_CANDIDATE_READY",
    }


def main() -> None:
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
