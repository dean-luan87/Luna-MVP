"""User-terminal Runner for one controlled replay through canonical A-Route."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (
    validate_handoff,
    validate_negative_guards,
    validate_stage_result,
    validate_trace,
)
from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_controlled_replay_gateway_request_v1,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_evidence,
    validate_ingress,
    validate_negative_guards as validate_gateway_negative_guards,
    validate_observation,
    validate_trace as validate_gateway_trace,
)


OUTPUT_DIR = Path("_eval_out/a_route_controlled_replay_runtime_enablement_v1")


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _availability(ref: str | None, *, observed_note: str, unavailable_note: str) -> Dict[str, Any]:
    return {
        "ref": ref,
        "availability": "observed" if ref else "not_observed",
        "notes": observed_note if ref else unavailable_note,
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    gateway_request = build_controlled_replay_gateway_request_v1()
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    observation = gateway.observation
    admission = gateway.replay_admission
    ingress = ARouteIngressRefsV1(
        observation_refs=(observation.observation_id,) if observation else (),
        perception_refs=tuple(item.evidence_id for item in gateway.evidence),
    )
    route_request = ARouteOrchestrationRequestV1(
        scenario_id=gateway_request.scenario_id,
        ingress=ingress,
        context_ref="context:controlled-replay:obvious-target",
        pcn_ref="pcn:controlled-replay:obvious-target",
        intent_ref="intent:controlled-replay:obvious-target",
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_admission=admission,
        synthetic_only=False,
        candidate_only=True,
    )
    route = ARouteOrchestrationEngineV1().run_case(route_request)
    proof = route.cognitive_execution
    validation_errors = []
    if gateway.errors:
        validation_errors.extend(f"gateway:{item.code}" for item in gateway.errors)
    if not gateway.ingress or not validate_ingress(gateway.ingress):
        validation_errors.append("gateway:ingress_contract_invalid")
    if not all(validate_evidence(item) for item in gateway.evidence):
        validation_errors.append("gateway:evidence_contract_invalid")
    if not observation or not validate_observation(observation):
        validation_errors.append("gateway:observation_contract_invalid")
    if not validate_gateway_trace(gateway.trace):
        validation_errors.append("gateway:trace_contract_invalid")
    if not validate_gateway_negative_guards(gateway.negative_guards):
        validation_errors.append("gateway:negative_guards_invalid")
    if route.errors:
        validation_errors.extend(f"a_route:{item.code}" for item in route.errors)
    if not all(validate_stage_result(item) for item in route.stage_results):
        validation_errors.append("a_route:stage_contract_invalid")
    if not all(validate_handoff(item) for item in route.handoffs):
        validation_errors.append("a_route:handoff_contract_invalid")
    if not validate_trace(route.trace, route.stage_results):
        validation_errors.append("a_route:trace_contract_invalid")
    if not validate_negative_guards(route.negative_guards):
        validation_errors.append("a_route:negative_guards_invalid")

    transition_refs = proof.cognitive_transition_refs if proof else ()
    summary: Dict[str, Any] = {
        "phase": "Phase-P1-Luna-A-Route-Controlled-Replay-Runtime-Enablement-v1-001",
        "execution_mode": CONTROLLED_REPLAY_RUNTIME,
        "replay_input_ref": gateway.replay_input_ref,
        "replay_origin_class": gateway_request.replay_input.origin_class if gateway_request.replay_input else None,
        "observation_gateway_admitted": gateway.admission_state == "ADMITTED_OBSERVATION" and admission is not None,
        "observation_gateway_admission_ref": admission.gateway_admission_ref if admission else None,
        "a_route_ingress_ref": gateway.trace.a_route_ingress_ref,
        "a_route_execution_ref": proof.execution_ref if proof else None,
        "cognition_execution": bool(proof and proof.runtime_executed),
        "runtime_executed": bool(proof and proof.runtime_executed),
        "cognitive_transition_count": len(transition_refs),
        "cognitive_transition_refs": list(transition_refs),
        "cognitive_transition_owner_ref": proof.owner_ref if proof else None,
        "current_world": _availability(
            proof.current_world_ref if proof else None,
            observed_note="Current World Candidate returned by canonical Cognitive State Formation",
            unavailable_note="Current World Candidate was not observed",
        ),
        "hypothesis": {
            "refs": list(proof.hypothesis_refs) if proof else [],
            "availability": proof.hypothesis_availability if proof else "not_observed",
            "notes": "Hypothesis candidates returned by canonical Cognitive State Formation" if proof else "Hypothesis candidates were not observed",
        },
        "sufficiency": _availability(
            proof.sufficiency_ref if proof else None,
            observed_note="Sufficiency was returned by canonical cognition",
            unavailable_note="Sufficiency is outside this minimum replay depth",
        ),
        "information_gap": _availability(
            proof.information_gap_ref if proof else None,
            observed_note="Information Gap was returned by canonical cognition",
            unavailable_note="Information Gap was not observed at this replay depth",
        ),
        "stop": _availability(
            proof.stop_ref if proof else None,
            observed_note="Stop reference was returned by canonical cognition",
            unavailable_note="Stop reference was not instrumented at this replay depth",
        ),
        "decision_handoff": _availability(
            proof.decision_handoff_ref if proof else None,
            observed_note="Decision Governance handoff was returned",
            unavailable_note="Decision Governance handoff was deferred",
        ),
        "canonical_execution_proof": _jsonable(proof),
        "model_invocation": False,
        "provider_invocation": False,
        "live_observation_execution": False,
        "action_execution": False,
        "field_mutation": bool(proof and proof.field_mutation),
        "world_truth_declared": bool(proof and proof.world_truth_declared),
        "validation_errors": list(dict.fromkeys(validation_errors)),
        "blocker_status": "NONE" if not validation_errors else "CONTROLLED_REPLAY_RUNTIME_VALIDATION_FAILED",
        "synthetic_compatibility_preserved": True,
        "route_lifecycle_state": route.lifecycle_state,
        "route_control_state": route.control_state,
        "route_deferred_refs": list(route.deferred_refs),
    }
    return summary


def main() -> None:
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

