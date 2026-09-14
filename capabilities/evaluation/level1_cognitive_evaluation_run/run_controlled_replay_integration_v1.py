"""User-terminal Runner for one complete Level-1 controlled replay integration."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict

from capabilities.evaluation.a_route_cognitive_whitebox_foundation.runtime_collector_v1 import (
    collect_runtime_whitebox_v1,
)
from capabilities.evaluation.a_route_cognitive_whitebox_foundation.types_v1 import (
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)
from capabilities.evaluation.level1_field_cognition_suite.types_v1 import PlaneAResultRefV1
from capabilities.evaluation.level1_cognitive_evaluation_run.archive_v1 import (
    archive_path_for_run_v1,
    write_evaluation_run_record_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.fixture_v1 import (
    build_registered_level1_case_inputs_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import (
    build_negative_replay_admission_case_v1,
    evaluate_plane_g_compliance_v1,
    validate_plane_g_compliance_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.run_boundary_v1 import (
    new_evaluation_run_execution_id_v1,
    require_registered_case_inputs_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.types_v1 import (
    EvaluationAvailabilityV1,
    EvaluationRunCandidateV1,
    EvaluationRunRecordV1,
    PlaneBResultV1,
    validate_evaluation_run_record_v1,
    validate_plane_b_result_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_controlled_replay_gateway_request_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (
    validate_negative_guards as validate_route_negative_guards,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    validate_execution_mode,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_negative_guards as validate_gateway_negative_guards,
)


PHASE = "Phase-P1-Luna-Level1-Replay-Evaluation-Whitebox-Archive-And-Governance-Integration-v1-001"
OUTPUT_DIR = Path("_eval_out/level1_replay_evaluation_whitebox_archive_governance_integration_v1")
ARCHIVE_ROOT = Path("evaluation_archive/level1_cognitive_runs")


def _evaluation_run_id(execution_instance_id: str) -> str:
    return (
        "evaluation-run:controlled-replay:level1:decision-governance-handoff:"
        + execution_instance_id
    )


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _availability(ref: str | None, note: str) -> Dict[str, Any]:
    return {"ref": ref, "availability": "observed" if ref else "not_observed", "notes": note}


def _negative_governance_check() -> Dict[str, Any]:
    negative = build_negative_replay_admission_case_v1()
    mode_errors = validate_execution_mode("LIVE_RUNTIME", synthetic_only=False)
    negative_gateway_request = dataclasses.replace(
        build_controlled_replay_gateway_request_v1(),
        execution_mode="LIVE_RUNTIME",
        synthetic_only=False,
    )
    negative_gateway = ObservationGatewayEngineV1().run_case(negative_gateway_request)
    gateway_rejected = (
        negative_gateway.admission_state == "REJECTED"
        and negative_gateway.replay_admission is None
        and bool(negative_gateway.errors)
    )
    result, violations = evaluate_plane_g_compliance_v1(
        run_ref="evaluation-run:negative:live-escalation:v1",
        execution_mode=str(negative["execution_mode"]),
        replay_input_ref=str(negative["replay_input_ref"]),
        gateway_admitted=False,
        cognition_owner_ref=None,
        transition_refs=(),
        model_invocation=False,
        provider_invocation=False,
        live_observation_execution=False,
        action_execution=False,
        field_mutation=False,
        world_truth_declared=False,
        memory_promotion=False,
        knowledge_promotion=False,
        experience_promotion=False,
        evaluation_constructed_cognition=False,
        whitebox_mutation=False,
        unavailable_metrics=("runtime_execution",),
    )
    return {
        "fixture": _jsonable(negative),
        "runtime_rejected": bool(mode_errors) and gateway_rejected,
        "runtime_rejection_errors": list(mode_errors),
        "gateway_rejection_errors": [item.code for item in negative_gateway.errors],
        "gateway_admission": negative_gateway.replay_admission is not None,
        "plane_g_status": result.compliance_status,
        "plane_g_violation_refs": [item.violation_id for item in violations],
        "expected": "canonical runtime fails closed and Plane G is NON_COMPLIANT",
        "passed": bool(mode_errors)
        and gateway_rejected
        and result.compliance_status == "NON_COMPLIANT"
        and bool(violations),
    }


def build_integration_summary_v1() -> Dict[str, Any]:
    execution_instance_id = new_evaluation_run_execution_id_v1()
    evaluation_run_id = _evaluation_run_id(execution_instance_id)
    registry, sample, case = build_registered_level1_case_inputs_v1()
    boundary = require_registered_case_inputs_v1(registry, sample, case)
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
        context_ref=f"context:{evaluation_run_id}",
        pcn_ref="pcn:controlled-replay:obvious-target",
        intent_ref=case.goal_ref,
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_admission=admission,
        synthetic_only=False,
        candidate_only=True,
    )
    route = ARouteOrchestrationEngineV1().run_case(route_request)
    proof = route.cognitive_execution
    validation_errors = list(boundary.errors)
    validation_errors.extend(f"gateway:{item.code}" for item in gateway.errors)
    if gateway.admission_state != "ADMITTED_OBSERVATION" or admission is None:
        validation_errors.append("gateway:replay_admission_missing")
    if not validate_gateway_negative_guards(gateway.negative_guards):
        validation_errors.append("gateway:negative_guards_invalid")
    if not validate_route_negative_guards(route.negative_guards):
        validation_errors.append("a_route:negative_guards_invalid")
    if route.errors:
        validation_errors.extend(f"a_route:{item.code}" for item in route.errors)
    if proof is None:
        validation_errors.append("a_route:cognitive_execution_proof_missing")

    collection = None
    if proof is not None and admission is not None:
        collection = collect_runtime_whitebox_v1(
            evaluation_run_id=evaluation_run_id,
            case=case,
            replay_input_ref=admission.replay_input_ref,
            gateway_admission_ref=admission.gateway_admission_ref,
            ingress_refs=proof.ingress_refs,
            proof=proof,
        )
        validation_errors.extend(validate_trace_contract_v1(collection.trace))
        validation_errors.extend(validate_profile_contract_v1(collection.profile))

    trace_ref = collection.trace.trace_id if collection else None
    profile_ref = collection.profile.execution_profile_id if collection else None
    proof_transition_refs = proof.cognitive_transition_refs if proof else ()
    plane_a = PlaneAResultRefV1(
        result_ref=f"plane-a-result:{evaluation_run_id}:v1",
        status="EXECUTION_OBSERVED" if proof and proof.runtime_executed else "INCOMPLETE",
        cognitive_trace_ref=trace_ref or "",
        execution_profile_ref=profile_ref or "",
        assertion_result_refs=case.cognitive_assertion_refs,
        completion_candidate_ref=None,
    )
    plane_b = PlaneBResultV1(
        result_ref=f"plane-b-result:{evaluation_run_id}:v1",
        status="NOT_EVALUATED",
        reason="No external model/provider executes in CONTROLLED_REPLAY_RUNTIME",
    )
    unavailable_metrics = collection.unavailable_metrics if collection else (
        "evidence_consumed_count",
        "reobservation_count",
        "latency",
        "resource_usage",
    )
    plane_g, violations = evaluate_plane_g_compliance_v1(
        run_ref=evaluation_run_id,
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_input_ref=admission.replay_input_ref if admission else None,
        gateway_admitted=gateway.admission_state == "ADMITTED_OBSERVATION" and admission is not None,
        cognition_owner_ref=proof.owner_ref if proof else None,
        transition_refs=proof_transition_refs,
        model_invocation=False,
        provider_invocation=False,
        live_observation_execution=False,
        action_execution=False,
        field_mutation=bool(proof and proof.field_mutation),
        world_truth_declared=bool(proof and proof.world_truth_declared),
        memory_promotion=False,
        knowledge_promotion=False,
        experience_promotion=False,
        evaluation_constructed_cognition=False,
        whitebox_mutation=bool(collection and not collection.observational_only),
        unavailable_metrics=unavailable_metrics,
        decision_handoff_ref=proof.decision_handoff_ref if proof else None,
    )
    validation_errors.extend(validate_plane_g_compliance_v1(plane_g))
    validation_errors.extend(validate_plane_b_result_v1(plane_b))
    negative = _negative_governance_check()
    if not negative["passed"]:
        validation_errors.append("negative_governance_fixture_failed")

    archive_path = archive_path_for_run_v1(evaluation_run_id, ARCHIVE_ROOT)
    run = EvaluationRunCandidateV1(
        evaluation_run_id=evaluation_run_id,
        evaluation_protocol_version="level1-cognitive-evaluation-run:v1",
        plane="PLANE_A_LUNA_COGNITIVE",
        cognitive_level="LEVEL_1_FIELD_COGNITION",
        dataset_ref=sample.dataset_ref,
        dataset_version=sample.dataset_version,
        sample_ref=sample.sample_id,
        sample_version="v1",
        cognitive_test_case_ref=case.cognitive_test_case_ref,
        cognitive_test_case_version=case.version,
        luna_code_version_ref=EvaluationAvailabilityV1(None, "unavailable", notes="build ref not instrumented"),
        luna_config_version_ref=EvaluationAvailabilityV1(None, "unavailable", notes="config ref not instrumented"),
        environment_condition_refs=case.environment_condition_refs,
        perturbation_refs=case.perturbation_refs,
        available_capability_refs=case.available_capability_refs,
        observation_budget_ref=case.observation_budget_ref,
        started_at=EvaluationAvailabilityV1(None, "not_observed", notes="timestamp instrumentation unavailable"),
        completed_at=EvaluationAvailabilityV1(None, "not_observed", notes="timestamp instrumentation unavailable"),
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        trace_ref=trace_ref,
        execution_profile_ref=profile_ref,
        gap_refs=tuple(gap.gap_id for gap in collection.gap_refs) if collection else (),
        result_status="EXECUTION_OBSERVED" if proof and proof.runtime_executed else "INCOMPLETE",
        failure_attribution_refs=tuple(item.violation_id for item in violations),
        invalidation_refs=(),
        provenance_refs=(
            *(admission.provenance_refs if admission else ()),
            f"provenance:{evaluation_run_id}:integration",
        ),
        source_version_refs=("level1-replay-evaluation-integration:v1",),
        a_route_bridge_status="READY" if admission else "BLOCKED",
        whitebox_attachment_status="ATTACHED" if collection else "UNAVAILABLE",
        comparison_eligibility=EvaluationAvailabilityV1(None, "planned", notes="baseline/comparison deferred"),
        runtime_metrics=EvaluationAvailabilityV1(None, "unavailable", notes="latency/resource instrumentation unavailable"),
        synthetic=False,
        cognition_execution=bool(proof and proof.runtime_executed),
        model_invocation=False,
        provider_invocation=False,
        observation_execution=False,
        action_execution=False,
        world_truth_declared=bool(proof and proof.world_truth_declared),
        field_mutation=bool(proof and proof.field_mutation),
        memory_promotion=False,
        experience_promotion=False,
        knowledge_promotion=False,
        runtime_executed=bool(proof and proof.runtime_executed),
        live_observation_execution=False,
        recorded_evidence_set_ref=admission.replay_input_ref if admission else None,
        replay_input_ref=admission.replay_input_ref if admission else None,
        replay_provenance_refs=admission.provenance_refs if admission else (),
        a_route_ingress_ref=(gateway.trace.a_route_ingress_ref if gateway.trace else None),
        a_route_execution_ref=proof.execution_ref if proof else None,
        cognition_execution_ref=proof.execution_ref if proof else None,
        task_ref=case.cognitive_task_ref,
        goal_ref=case.goal_ref,
        concern_ref=case.concern_ref,
        role_ref=case.role_ref,
        context_refs=(f"context:{evaluation_run_id}",),
        cognitive_result_ref=plane_a.result_ref,
        capability_fitness_result_status=plane_b.status,
        governance_compliance_result_ref=plane_g.result_ref,
        archive_ref=str(archive_path),
        availability_states={
            "current_world": proof.current_world_availability if proof else "not_observed",
            "hypothesis": proof.hypothesis_availability if proof else "not_observed",
            "sufficiency": proof.sufficiency_availability if proof else "not_observed",
            "information_gap": proof.information_gap_availability if proof else "not_observed",
            "stop": proof.stop_availability if proof else "not_observed",
            "decision_handoff": proof.decision_handoff_availability if proof else "not_observed",
        },
    )
    record = EvaluationRunRecordV1(
        record_id=f"evaluation-record:{evaluation_run_id}:v1",
        record_version="v1",
        evaluation_run=run,
        test_board_refs=(f"test-board:level1-replay:{case.cognitive_test_case_ref}:v1",),
        bounded_metadata={
            "fixture_kind": "CONTROLLED_RECORDED_FIXTURE",
            "plane_a_result": _jsonable(plane_a),
            "plane_b_result": _jsonable(plane_b),
            "plane_g_result": _jsonable(plane_g),
            "governance_violation_refs": [item.violation_id for item in violations],
            "canonical_cognition_proof": _jsonable(proof),
            "whitebox_refs": {
                "trace_ref": trace_ref,
                "profile_ref": profile_ref,
                "gap_refs": list(run.gap_refs),
            },
            "whitebox_trace": _jsonable(collection.trace) if collection else None,
            "whitebox_profile": _jsonable(collection.profile) if collection else None,
            "negative_governance_check": negative,
            "archive_role": "durable_evaluation_history",
        },
    )
    validation_errors.extend(validate_evaluation_run_record_v1(record))
    archive_created = False
    archive_immutable = record.immutable_by_identity
    if not validation_errors:
        _, archive_created = write_evaluation_run_record_v1(record, archive_root=ARCHIVE_ROOT)
        archive_created = archive_created or archive_path.is_file()

    return {
        "phase": PHASE,
        "execution_instance_id": execution_instance_id,
        "evaluation_run_id": evaluation_run_id,
        "dataset_registry_ref": boundary.dataset_registry_ref,
        "dataset_ref": sample.dataset_ref,
        "sample_ref": sample.sample_id,
        "case_ref": case.cognitive_test_case_ref,
        "execution_mode": CONTROLLED_REPLAY_RUNTIME,
        "replay_input_ref": run.recorded_evidence_set_ref,
        "replay_origin_class": "CONTROLLED_RECORDED_FIXTURE",
        "replay_provenance_refs": list(run.replay_provenance_refs),
        "run_boundary_valid": boundary.valid,
        "run_boundary_errors": list(boundary.errors),
        "observation_gateway_admitted": gateway.admission_state == "ADMITTED_OBSERVATION" and admission is not None,
        "observation_gateway_admission_ref": admission.gateway_admission_ref if admission else None,
        "a_route_ingress_ref": run.a_route_ingress_ref,
        "a_route_execution_ref": run.a_route_execution_ref,
        "cognition_execution": run.cognition_execution,
        "runtime_executed": run.runtime_executed,
        "cognitive_transition_count": len(proof_transition_refs),
        "cognitive_transition_refs": list(proof_transition_refs),
        "current_world": _availability(proof.current_world_ref if proof else None, "canonical Current World Candidate ref"),
        "hypothesis": {"refs": list(proof.hypothesis_refs) if proof else [], "availability": proof.hypothesis_availability if proof else "not_observed"},
        "sufficiency": _availability(proof.sufficiency_ref if proof else None, "canonical Sufficiency ref"),
        "information_gap": _availability(proof.information_gap_ref if proof else None, "canonical Information Gap ref"),
        "stop": _availability(proof.stop_ref if proof else None, "canonical Stop ref"),
        "decision_handoff": _availability(proof.decision_handoff_ref if proof else None, "canonical Decision Governance handoff ref"),
        "canonical_cognition_owner_ref": proof.owner_ref if proof else None,
        "canonical_execution_proof": _jsonable(proof),
        "whitebox_trace_ref": trace_ref,
        "whitebox_profile_ref": profile_ref,
        "failure_gap_refs": list(run.gap_refs),
        "plane_a_result": _jsonable(plane_a),
        "plane_b_result": _jsonable(plane_b),
        "plane_g_result": _jsonable(plane_g),
        "governance_assertion_summary": {item.assertion_id: item.status for item in plane_g.assertion_results},
        "governance_violation_refs": [item.violation_id for item in violations],
        "negative_governance_check": negative,
        "failure_attribution": list(run.failure_attribution_refs),
        "archive_location": str(archive_path),
        "archive_record_created": archive_created,
        "archive_record_immutable": archive_immutable,
        "model_invocation": run.model_invocation,
        "provider_invocation": run.provider_invocation,
        "live_observation_execution": run.live_observation_execution,
        "action_execution": run.action_execution,
        "field_mutation": run.field_mutation,
        "world_truth_declared": run.world_truth_declared,
        "memory_promotion": run.memory_promotion,
        "knowledge_promotion": run.knowledge_promotion,
        "experience_promotion": run.experience_promotion,
        "unavailable_metrics": list(unavailable_metrics),
        "boundary_errors": list(boundary.errors),
        "validation_errors": list(dict.fromkeys(validation_errors)),
        "archive_status": "CREATED" if archive_created else "NOT_CREATED",
    }


def main() -> None:
    summary = build_integration_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
