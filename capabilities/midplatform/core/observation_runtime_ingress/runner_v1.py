"""User-terminal runner for the real-runtime observation ingress contract.

Fixtures are provider-output-shaped inputs.  This runner never invokes a
provider; it verifies the adapter and the canonical Gateway/A-Route/CState
path once a result is available.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (
    validate_handoff,
    validate_negative_guards as validate_route_negative_guards,
    validate_stage_result,
    validate_trace as validate_route_trace,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_evidence,
    validate_ingress,
    validate_negative_guards as validate_gateway_negative_guards,
    validate_observation,
    validate_runtime_observation_admission,
    validate_runtime_observation_envelope,
    validate_trace as validate_gateway_trace,
)
from capabilities.midplatform.core.execution_mode_v1 import LIVE_RUNTIME

from .adapters_v1 import build_aroute_request, build_gateway_request
from .fixtures_v1 import (
    build_runtime_observation_cases_v1,
    malformed_runtime_observation_case_v1,
    missing_information_case_v1,
    unavailable_provider_case_v1,
)


OUTPUT_DIR = Path("_eval_out/real_observation_runtime_ingress_v1")


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _check(name: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": name, "passed": bool(passed), "observed": _jsonable(observed)}


def _positive_case(case: Any) -> Dict[str, Any]:
    gateway_request = build_gateway_request(case)
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    route = None
    if gateway.admission_state == "ADMITTED_OBSERVATION":
        route = ARouteOrchestrationEngineV1().run_case(build_aroute_request(case, gateway))
    proof = route.cognitive_execution if route else None
    errors = [f"gateway:{item.code}" for item in gateway.errors]
    if route:
        errors.extend(f"a_route:{item.code}" for item in route.errors)
    checks = [
        _check("live_runtime_mode", gateway.execution_mode == LIVE_RUNTIME and (route is None or route.execution_mode == LIVE_RUNTIME), gateway.execution_mode),
        _check("runtime_envelope_valid", validate_runtime_observation_envelope(case.observation)),
        _check("gateway_admitted", gateway.admission_state == "ADMITTED_OBSERVATION"),
        _check("gateway_contracts_valid", bool(gateway.ingress and validate_ingress(gateway.ingress)) and all(validate_evidence(item) for item in gateway.evidence) and bool(gateway.observation and validate_observation(gateway.observation)) and validate_gateway_trace(gateway.trace)),
        _check("gateway_runtime_admission_valid", bool(gateway.runtime_admission and validate_runtime_observation_admission(gateway.runtime_admission)), _jsonable(gateway.runtime_admission)),
        _check("provider_capability_provenance_retained", bool(gateway.evidence) and gateway.evidence[0].source_provider == case.observation.provider_ref and gateway.evidence[0].source_capability == case.observation.capability_ref and case.observation.provider_ref in gateway.trace.provider_trace_refs),
        _check("evidence_candidate_not_fact", all(item.candidate_only and item.fact_declared is False for item in gateway.evidence) and bool(gateway.observation and gateway.observation.truth_declared is False)),
        _check("gateway_negative_guards_closed", validate_gateway_negative_guards(gateway.negative_guards)),
        _check("a_route_consumes_admission", bool(route and route.cognitive_execution and gateway.runtime_admission and gateway.runtime_admission.gateway_admission_ref in route.cognitive_execution.ingress_refs)),
        _check("cstate_runtime_executed", bool(proof and proof.runtime_executed and proof.execution_mode == LIVE_RUNTIME and proof.owner_ref == "Cognitive State Formation Governance")),
        _check("conditioning_refs_preserved", bool(proof and tuple(case.role_refs) == proof.role_refs and tuple(case.task_refs) == proof.task_refs and tuple(case.goal_refs) == proof.goal_refs and tuple(case.information_need_refs) == proof.information_need_refs)),
        _check("sufficiency_or_gap_observed", bool(proof and (proof.sufficiency_ref or proof.information_gap_ref))),
        _check("route_contracts_valid", bool(route and not route.errors and all(validate_stage_result(item) for item in route.stage_results) and all(validate_handoff(item) for item in route.handoffs) and validate_route_trace(route.trace, route.stage_results) and validate_route_negative_guards(route.negative_guards))),
        _check("no_downstream_execution", bool(route and not any(item.stage_id in {"DECISION", "TASK", "ACTION", "EXECUTION"} for item in route.stage_results))),
    ]
    return {
        "case_id": case.case_id,
        "title": case.title,
        "execution_mode": LIVE_RUNTIME,
        "provider_ref": case.observation.provider_ref,
        "capability_ref": case.observation.capability_ref,
        "runtime_observation_ref": case.observation.observation_id,
        "gateway_admission_ref": gateway.runtime_admission.gateway_admission_ref if gateway.runtime_admission else None,
        "observation_ref": gateway.observation.observation_id if gateway.observation else None,
        "evidence_refs": [item.evidence_id for item in gateway.evidence],
        "a_route_execution_ref": proof.execution_ref if proof else None,
        "cognitive_transition_refs": list(proof.cognitive_transition_refs) if proof else [],
        "current_world_ref": proof.current_world_ref if proof else None,
        "hypothesis_refs": list(proof.hypothesis_refs) if proof else [],
        "sufficiency_ref": proof.sufficiency_ref if proof else None,
        "sufficiency_status": proof.sufficiency_status if proof else "not_observed",
        "information_gap_ref": proof.information_gap_ref if proof else None,
        "stop_ref": proof.stop_ref if proof else None,
        "required_information_refs": list(case.required_information_refs),
        "available_information_refs": list(case.available_information_refs),
        "information_need_refs": list(case.information_need_refs),
        "conditioned_evidence_relevance": list(proof.conditioned_evidence_relevance) if proof else [],
        "conditioned_missing_information_refs": list(proof.conditioned_missing_information_refs) if proof else [],
        "conditioning_refs": {
            "role_refs": list(case.role_refs),
            "task_refs": list(case.task_refs),
            "goal_refs": list(case.goal_refs),
            "information_need_refs": list(case.information_need_refs),
        },
        "provider_invocation": False,
        "model_invocation": False,
        "live_observation_execution": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "decision_execution": False,
        "task_execution": False,
        "action_execution": False,
        "validation_errors": list(dict.fromkeys(errors)),
        "checks": checks,
        "all_checks_passed": not errors and all(item["passed"] for item in checks),
        "gateway": _jsonable(gateway),
        "a_route": _jsonable(route),
    }


def _negative_case(case: Any, expected_code: str) -> Dict[str, Any]:
    gateway = ObservationGatewayEngineV1().run_case(build_gateway_request(case))
    error_codes = [item.code for item in gateway.errors]
    route_invoked = False
    if gateway.admission_state == "ADMITTED_OBSERVATION":
        route_invoked = True
    checks = [
        _check("gateway_rejected", gateway.admission_state == "REJECTED"),
        _check("expected_error", expected_code in error_codes, error_codes),
        _check("no_fake_evidence", not gateway.evidence and gateway.observation is None),
        _check("a_route_not_invoked", route_invoked is False),
    ]
    return {
        "case_id": case.case_id,
        "expected_error": expected_code,
        "admission_state": gateway.admission_state,
        "error_codes": error_codes,
        "a_route_invoked": route_invoked,
        "checks": checks,
        "all_checks_passed": all(item["passed"] for item in checks),
        "gateway": _jsonable(gateway),
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    positives = [_positive_case(case) for case in build_runtime_observation_cases_v1()]
    missing = _positive_case(missing_information_case_v1())
    missing["checks"].append(_check("missing_information_produces_gap", bool(missing["information_gap_ref"]) and missing["sufficiency_status"] == "INSUFFICIENT"))
    missing["all_checks_passed"] = not missing["validation_errors"] and all(item["passed"] for item in missing["checks"])
    negatives = [
        _negative_case(malformed_runtime_observation_case_v1(), "RUNTIME_OBSERVATION_INVALID"),
        _negative_case(unavailable_provider_case_v1(), "PROVIDER_UNAVAILABLE"),
    ]
    return {
        "phase": "Phase-P1-Luna-Real-Observation-Runtime-Ingress-Integration-v1-001",
        "execution_mode": LIVE_RUNTIME,
        "provider_invocation": False,
        "model_invocation": False,
        "live_observation_execution": False,
        "decision_execution": False,
        "task_execution": False,
        "action_execution": False,
        "runtime_executor_invocation": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "positive_cases": positives,
        "missing_information_case": missing,
        "negative_cases": negatives,
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "all_checks_passed": all(item["all_checks_passed"] for item in (*positives, missing, *negatives)),
        "status": "REAL_OBSERVATION_RUNTIME_INGRESS_RESULT_CANDIDATE_READY",
    }


def main() -> None:
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
