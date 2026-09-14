"""User-terminal Runner for the two-case minimum sufficient cognition loop."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from capabilities.evaluation.a_route_cognitive_whitebox_foundation.runtime_collector_v1 import (
    WhiteBoxRuntimeCollectionV1,
    collect_runtime_whitebox_loop_v1,
    collect_runtime_whitebox_v1,
)
from capabilities.evaluation.a_route_cognitive_whitebox_foundation.types_v1 import (
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.archive_v1 import (
    archive_path_for_run_v1,
    write_evaluation_run_record_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.fixture_v1 import (
    build_minimum_sufficient_loop_case_inputs_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import (
    evaluate_plane_g_compliance_v1,
    validate_plane_g_compliance_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.plane_a_loop_v1 import (
    PlaneALoopResultV1,
    evaluate_plane_a_loop_case_v1,
    validate_plane_a_loop_result_v1,
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
    ARouteCognitiveExecutionEvidenceV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (
    validate_negative_guards as validate_route_negative_guards,
)
from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_minimum_sufficient_loop_gateway_request_v1,
    build_minimum_sufficient_loop_replay_input_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import (
    validate_output_contract as validate_cognitive_output_contract,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_negative_guards as validate_gateway_negative_guards,
)


PHASE = "Phase-P1-Luna-Level1-Minimum-Sufficient-Cognition-Loop-Controlled-Replay-v1-001"
OUTPUT_DIR = Path("_eval_out/level1_minimum_sufficient_cognition_loop_controlled_replay_v1")
ARCHIVE_ROOT = Path("evaluation_archive/level1_cognitive_runs")


def _evaluation_run_id(execution_instance_id: str, case_id: str) -> str:
    return f"evaluation-run:controlled-replay:minimum-sufficient:{case_id}:{execution_instance_id}"


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


def _route_for_replay(case: Any, replay: Any, scenario_id: str, evaluation_run_id: str):
    gateway_request = build_minimum_sufficient_loop_gateway_request_v1(
        scenario_id=scenario_id,
        replay=replay,
        execution_identity_ref=f"{evaluation_run_id}:{scenario_id}",
    )
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    observation = gateway.observation
    admission = gateway.replay_admission
    ingress = ARouteIngressRefsV1(
        observation_refs=(observation.observation_id,) if observation else (),
        perception_refs=tuple(item.evidence_id for item in gateway.evidence),
    )
    route = ARouteOrchestrationEngineV1().run_case(
        ARouteOrchestrationRequestV1(
            scenario_id=scenario_id,
            ingress=ingress,
            context_ref=f"context:{evaluation_run_id}",
            pcn_ref=f"pcn:{evaluation_run_id}",
            intent_ref=case.goal_ref,
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            execution_identity_ref=f"{evaluation_run_id}:{scenario_id}",
            replay_admission=admission,
            synthetic_only=False,
            candidate_only=True,
        )
    )
    return gateway, admission, route


def _assert_case_b_cycle_2_causal_contract(proof_a: Any, replay_b: Any) -> None:
    values = {
        "cycle_1_sufficiency_ref": proof_a.sufficiency_ref if proof_a else None,
        "cycle_1_information_gap_ref": proof_a.information_gap_ref if proof_a else None,
        "cycle_1_reobservation_ref": proof_a.reobservation_ref if proof_a else None,
        "cycle_1_next_cycle_ingress_ref": proof_a.next_cycle_ingress_ref if proof_a else None,
        "cycle_2_prior_information_gap_ref": replay_b.prior_information_gap_ref,
        "cycle_2_prior_reobservation_ref": replay_b.prior_reobservation_ref,
        "cycle_2_prior_next_cycle_ingress_ref": replay_b.prior_next_cycle_ingress_ref,
        "revision_gap_ref": replay_b.prior_information_gap_ref,
        "revision_reobservation_ref": replay_b.prior_reobservation_ref,
    }
    mismatches = []
    if proof_a is None:
        mismatches.append("cycle_1_proof_missing")
    else:
        if replay_b.prior_information_gap_ref != proof_a.information_gap_ref:
            mismatches.append("information_gap_ref")
        if replay_b.prior_reobservation_ref != proof_a.reobservation_ref:
            mismatches.append("reobservation_ref")
        if replay_b.prior_next_cycle_ingress_ref != proof_a.next_cycle_ingress_ref:
            mismatches.append("next_cycle_ingress_ref")
        if replay_b.prior_sufficiency_candidate != proof_a.sufficiency_candidate:
            mismatches.append("sufficiency_candidate")
        if replay_b.prior_information_gap_candidate != proof_a.information_gap_candidate:
            mismatches.append("information_gap_candidate")
        if replay_b.prior_reobservation_candidate != proof_a.reobservation_candidate:
            mismatches.append("reobservation_candidate")
    if mismatches:
        raise ValueError(
            "case_b_cycle_2_causal_contract_invalid:"
            + ",".join(mismatches)
            + ":"
            + ";".join(f"{key}={value!r}" for key, value in values.items())
        )


def _case_a(case: Any, registry: Any, sample: Any, execution_instance_id: str) -> Dict[str, Any]:
    run_id = _evaluation_run_id(execution_instance_id, "case-a")
    replay = build_minimum_sufficient_loop_replay_input_v1(
        case_id="case-a-sufficient-stop",
        cycle_index=1,
        evidence_refs=("evidence:minimum-sufficient:case-a:target-identity",),
        available_information_refs=("information:target-identity", "information:target-location"),
    )
    gateway, admission, route = _route_for_replay(case, replay, "S01", run_id)
    proof = route.cognitive_execution
    errors = []
    if gateway.errors:
        errors.extend(f"gateway:{item.code}" for item in gateway.errors)
    if not gateway.replay_admission or gateway.admission_state != "ADMITTED_OBSERVATION":
        errors.append("gateway:replay_not_admitted")
    if not validate_gateway_negative_guards(gateway.negative_guards):
        errors.append("gateway:negative_guard_invalid")
    if route.errors:
        errors.extend(f"a_route:{item.code}" for item in route.errors)
    if not validate_route_negative_guards(route.negative_guards):
        errors.append("a_route:negative_guard_invalid")
    if proof is None:
        errors.append("a_route:cognitive_proof_missing")
    collection = None
    if proof and admission:
        collection = collect_runtime_whitebox_v1(
            evaluation_run_id=run_id,
            case=case,
            replay_input_ref=admission.replay_input_ref,
            gateway_admission_ref=admission.gateway_admission_ref,
            ingress_refs=proof.ingress_refs,
            proof=proof,
        )
        errors.extend(validate_trace_contract_v1(collection.trace))
        errors.extend(validate_profile_contract_v1(collection.profile))
    if proof:
        if proof.sufficiency_status != "SUFFICIENT" or not proof.stop_ref:
            errors.append("case_a:sufficient_stop_proof_missing")
        if proof.information_gap_ref or proof.reobservation_ref or proof.next_cycle_ingress_ref:
            errors.append("case_a:unexpected_gap_or_reobservation")
    plane_a = evaluate_plane_a_loop_case_v1(
        result_ref=f"plane-a-result:{run_id}:v1",
        case_ref=case.cognitive_test_case_ref,
        expected_behavior="sufficient-and-stop",
        proofs=(proof,) if proof else (),
        unnecessary_observation=False,
    )
    if validate_plane_a_loop_result_v1(plane_a):
        errors.extend(validate_plane_a_loop_result_v1(plane_a))
    plane_b = PlaneBResultV1(f"plane-b-result:{run_id}:v1", "NOT_EVALUATED", "No model/provider executes in replay")
    if validate_plane_b_result_v1(plane_b):
        errors.extend(validate_plane_b_result_v1(plane_b))
    plane_g, violations = evaluate_plane_g_compliance_v1(
        run_ref=run_id,
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_input_ref=admission.replay_input_ref if admission else None,
        gateway_admitted=bool(admission and gateway.admission_state == "ADMITTED_OBSERVATION"),
        cognition_owner_ref=proof.owner_ref if proof else None,
        transition_refs=proof.cognitive_transition_refs if proof else (),
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
        unavailable_metrics=collection.unavailable_metrics if collection else ("latency", "resource_usage"),
        sufficiency_ref=proof.sufficiency_ref if proof else None,
        sufficiency_owner_ref=proof.sufficiency_owner_ref if proof else None,
        stop_ref=proof.stop_ref if proof else None,
        stop_owner_ref=proof.stop_owner_ref if proof else None,
        unnecessary_observation=False,
    )
    errors.extend(validate_plane_g_compliance_v1(plane_g))
    return _archive_case(
        run_id=run_id,
        case=case,
        registry=registry,
        sample=sample,
        replays=(replay,),
        gateways=(gateway,),
        admissions=(admission,),
        routes=(route,),
        proofs=(proof,) if proof else (),
        collection=collection,
        plane_a=plane_a,
        plane_b=plane_b,
        plane_g=plane_g,
        violations=violations,
        errors=errors,
        expected="sufficient-and-stop",
    )


def _case_b(case: Any, registry: Any, sample: Any, execution_instance_id: str) -> Dict[str, Any]:
    run_id = _evaluation_run_id(execution_instance_id, "case-b")
    replay_a = build_minimum_sufficient_loop_replay_input_v1(
        case_id="case-b-gap-reobserve-revise-stop",
        cycle_index=1,
        evidence_refs=("evidence:minimum-sufficient:case-b:target-identity",),
        available_information_refs=("information:target-identity",),
    )
    gateway_a, admission_a, route_a = _route_for_replay(case, replay_a, "S04", f"{run_id}:cycle-1")
    proof_a = route_a.cognitive_execution
    errors = []
    if not proof_a or proof_a.sufficiency_status != "INSUFFICIENT" or not proof_a.information_gap_ref or not proof_a.reobservation_ref or not proof_a.next_cycle_ingress_ref:
        errors.append("case_b:cycle_1_gap_reobservation_proof_missing")
    replay_b = build_minimum_sufficient_loop_replay_input_v1(
        case_id="case-b-gap-reobserve-revise-stop",
        cycle_index=2,
        evidence_refs=("evidence:minimum-sufficient:case-b:target-location",),
        available_information_refs=("information:target-identity", "information:target-location"),
        prior_current_world_ref=proof_a.current_world_ref if proof_a else None,
        prior_hypothesis_refs=proof_a.hypothesis_refs if proof_a else (),
        prior_information_gap_ref=proof_a.information_gap_ref if proof_a else None,
        prior_reobservation_ref=proof_a.reobservation_ref if proof_a else None,
        prior_next_cycle_ingress_ref=proof_a.next_cycle_ingress_ref if proof_a else None,
        prior_sufficiency_candidate=proof_a.sufficiency_candidate if proof_a else None,
        prior_information_gap_candidate=proof_a.information_gap_candidate if proof_a else None,
        prior_reobservation_candidate=proof_a.reobservation_candidate if proof_a else None,
    )
    _assert_case_b_cycle_2_causal_contract(proof_a, replay_b)
    gateway_b, admission_b, route_b = _route_for_replay(case, replay_b, "S10", f"{run_id}:cycle-2")
    proof_b = route_b.cognitive_execution
    if not proof_b or proof_b.sufficiency_status != "SUFFICIENT" or not proof_b.hypothesis_revision_ref or not proof_b.stop_ref:
        errors.append("case_b:cycle_2_revision_sufficient_stop_proof_missing")
    if (
        not admission_b
        or admission_b.prior_information_gap_ref != (proof_a.information_gap_ref if proof_a else None)
        or admission_b.prior_reobservation_ref != (proof_a.reobservation_ref if proof_a else None)
        or admission_b.prior_next_cycle_ingress_ref != (proof_a.next_cycle_ingress_ref if proof_a else None)
        or admission_b.prior_sufficiency_candidate != (proof_a.sufficiency_candidate if proof_a else None)
        or admission_b.prior_information_gap_candidate != (proof_a.information_gap_candidate if proof_a else None)
        or admission_b.prior_reobservation_candidate != (proof_a.reobservation_candidate if proof_a else None)
    ):
        errors.append("case_b:cycle_linkage_invalid")
    for label, gateway, route in (("cycle_1", gateway_a, route_a), ("cycle_2", gateway_b, route_b)):
        if gateway.errors:
            errors.extend(f"{label}:gateway:{item.code}" for item in gateway.errors)
        if gateway.admission_state != "ADMITTED_OBSERVATION" or gateway.replay_admission is None:
            errors.append(f"{label}:gateway:replay_not_admitted")
        if route.errors:
            errors.extend(f"{label}:a_route:{item.code}" for item in route.errors)
        if not validate_gateway_negative_guards(gateway.negative_guards):
            errors.append(f"{label}:gateway:negative_guard_invalid")
        if not validate_route_negative_guards(route.negative_guards):
            errors.append(f"{label}:a_route:negative_guard_invalid")
    collection = None
    if proof_a and proof_b and admission_a and admission_b:
        collection = collect_runtime_whitebox_loop_v1(
            evaluation_run_id=run_id,
            case=case,
            replay_input_refs=(admission_a.replay_input_ref, admission_b.replay_input_ref),
            gateway_admission_refs=(admission_a.gateway_admission_ref, admission_b.gateway_admission_ref),
            proofs=(proof_a, proof_b),
        )
        errors.extend(validate_trace_contract_v1(collection.trace))
        errors.extend(validate_profile_contract_v1(collection.profile))
    proofs = tuple(proof for proof in (proof_a, proof_b) if proof is not None)
    plane_a = evaluate_plane_a_loop_case_v1(
        result_ref=f"plane-a-result:{run_id}:v1",
        case_ref=case.cognitive_test_case_ref,
        expected_behavior="identify-gap-reobserve-revise-sufficient-and-stop",
        proofs=proofs,
        unnecessary_observation=False,
    )
    errors.extend(validate_plane_a_loop_result_v1(plane_a))
    plane_b = PlaneBResultV1(f"plane-b-result:{run_id}:v1", "NOT_EVALUATED", "No model/provider executes in replay")
    errors.extend(validate_plane_b_result_v1(plane_b))
    plane_g, violations = evaluate_plane_g_compliance_v1(
        run_ref=run_id,
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_input_ref=admission_b.replay_input_ref if admission_b else None,
        gateway_admitted=bool(admission_a and admission_b and gateway_a.admission_state == "ADMITTED_OBSERVATION" and gateway_b.admission_state == "ADMITTED_OBSERVATION"),
        cognition_owner_ref=proof_b.owner_ref if proof_b else None,
        transition_refs=tuple(ref for proof in proofs for ref in proof.cognitive_transition_refs),
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
        unavailable_metrics=collection.unavailable_metrics if collection else ("latency", "resource_usage"),
        sufficiency_ref=proof_b.sufficiency_ref if proof_b else None,
        sufficiency_owner_ref=proof_b.sufficiency_owner_ref if proof_b else None,
        information_gap_ref=proof_a.information_gap_ref if proof_a else None,
        information_gap_owner_ref=proof_a.information_gap_owner_ref if proof_a else None,
        reobservation_ref=proof_a.reobservation_ref if proof_a else None,
        reobservation_owner_ref=proof_a.reobservation_owner_ref if proof_a else None,
        next_cycle_ingress_ref=proof_a.next_cycle_ingress_ref if proof_a else None,
        hypothesis_revision_ref=proof_b.hypothesis_revision_ref if proof_b else None,
        hypothesis_revision_owner_ref=proof_b.hypothesis_revision_owner_ref if proof_b else None,
        stop_ref=proof_b.stop_ref if proof_b else None,
        stop_owner_ref=proof_b.stop_owner_ref if proof_b else None,
        unnecessary_observation=False,
    )
    errors.extend(validate_plane_g_compliance_v1(plane_g))
    return _archive_case(
        run_id=run_id,
        case=case,
        registry=registry,
        sample=sample,
        replays=(replay_a, replay_b),
        gateways=(gateway_a, gateway_b),
        admissions=(admission_a, admission_b),
        routes=(route_a, route_b),
        proofs=proofs,
        collection=collection,
        plane_a=plane_a,
        plane_b=plane_b,
        plane_g=plane_g,
        violations=violations,
        errors=errors,
        expected="identify-gap-reobserve-revise-sufficient-and-stop",
    )


def _archive_case(
    *,
    run_id: str,
    case: Any,
    registry: Any,
    sample: Any,
    replays: Tuple[Any, ...],
    gateways: Tuple[Any, ...],
    admissions: Tuple[Any, ...],
    routes: Tuple[Any, ...],
    proofs: Tuple[ARouteCognitiveExecutionEvidenceV1, ...],
    collection: WhiteBoxRuntimeCollectionV1 | None,
    plane_a: PlaneALoopResultV1,
    plane_b: PlaneBResultV1,
    plane_g: Any,
    violations: Tuple[Any, ...],
    errors: list[str],
    expected: str,
) -> Dict[str, Any]:
    boundary = require_registered_case_inputs_v1(registry, sample, case)
    errors.extend(boundary.errors)
    first_admission = admissions[0] if admissions else None
    final_proof = proofs[-1] if proofs else None
    archive_path = archive_path_for_run_v1(run_id, ARCHIVE_ROOT)
    run = EvaluationRunCandidateV1(
        evaluation_run_id=run_id,
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
        trace_ref=collection.trace.trace_id if collection else None,
        execution_profile_ref=collection.profile.execution_profile_id if collection else None,
        gap_refs=(),
        result_status="EXECUTION_OBSERVED" if final_proof and final_proof.runtime_executed else "INCOMPLETE",
        failure_attribution_refs=tuple(item.violation_id for item in violations),
        invalidation_refs=(),
        provenance_refs=(
            f"evaluation-execution:{run_id}",
            *(ref for admission in admissions for ref in (admission.provenance_refs if admission else ())),
        ),
        source_version_refs=("minimum-sufficient-cognition-loop:v1",),
        a_route_bridge_status="READY" if all(admissions) else "BLOCKED",
        whitebox_attachment_status="ATTACHED" if collection else "UNAVAILABLE",
        comparison_eligibility=EvaluationAvailabilityV1(None, "planned", notes="baseline/comparison deferred"),
        runtime_metrics=EvaluationAvailabilityV1(None, "unavailable", notes="latency/resource instrumentation unavailable"),
        synthetic=False,
        cognition_execution=bool(final_proof and final_proof.runtime_executed),
        model_invocation=False,
        provider_invocation=False,
        observation_execution=False,
        action_execution=False,
        world_truth_declared=False,
        field_mutation=False,
        memory_promotion=False,
        experience_promotion=False,
        knowledge_promotion=False,
        runtime_executed=bool(final_proof and final_proof.runtime_executed),
        live_observation_execution=False,
        recorded_evidence_set_ref=first_admission.replay_input_ref if first_admission else None,
        replay_input_ref=first_admission.replay_input_ref if first_admission else None,
        replay_provenance_refs=tuple(ref for admission in admissions for ref in (admission.provenance_refs if admission else ())),
        a_route_ingress_ref=gateways[0].trace.a_route_ingress_ref if gateways and gateways[0].trace else None,
        a_route_execution_ref=final_proof.execution_ref if final_proof else None,
        cognition_execution_ref=final_proof.execution_ref if final_proof else None,
        task_ref=case.cognitive_task_ref,
        goal_ref=case.goal_ref,
        concern_ref=case.concern_ref,
        role_ref=case.role_ref,
        context_refs=(f"context:{run_id}",),
        cognitive_result_ref=plane_a.result_ref,
        capability_fitness_result_status=plane_b.status,
        governance_compliance_result_ref=plane_g.result_ref,
        archive_ref=str(archive_path),
        availability_states={
            "current_world": final_proof.current_world_availability if final_proof else "not_observed",
            "hypothesis": final_proof.hypothesis_availability if final_proof else "not_observed",
            "sufficiency": final_proof.sufficiency_availability if final_proof else "not_observed",
            "information_gap": final_proof.information_gap_availability if final_proof else "not_observed",
            "reobservation": "observed" if final_proof and final_proof.reobservation_ref else "not_observed",
            "hypothesis_revision": "observed" if final_proof and final_proof.hypothesis_revision_ref else "not_observed",
            "stop": final_proof.stop_availability if final_proof else "not_observed",
        },
    )
    record = EvaluationRunRecordV1(
        record_id=f"evaluation-record:{run_id}:v1",
        record_version="v1",
        evaluation_run=run,
        test_board_refs=(f"test-board:level1-minimum-sufficient-loop:{case.cognitive_test_case_ref}:v1",),
        bounded_metadata={
            "fixture_kind": "CONTROLLED_RECORDED_FIXTURE",
            "expected_behavior": expected,
            "cycle_count": len(proofs),
            "replay_inputs": [_jsonable(item) for item in replays],
            "gateway_admission_refs": [item.gateway_admission_ref if item else None for item in admissions],
            "a_route_execution_refs": [item.execution_ref for item in proofs],
            "canonical_cognition_proofs": [_jsonable(item) for item in proofs],
            "cycle_routes": [_jsonable(item) for item in routes],
            "plane_a_result": _jsonable(plane_a),
            "plane_b_result": _jsonable(plane_b),
            "plane_g_result": _jsonable(plane_g),
            "governance_violation_refs": [item.violation_id for item in violations],
            "whitebox_trace": _jsonable(collection.trace) if collection else None,
            "whitebox_profile": _jsonable(collection.profile) if collection else None,
            "whitebox_refs": {
                "trace_ref": collection.trace.trace_id if collection else None,
                "profile_ref": collection.profile.execution_profile_id if collection else None,
                "gap_refs": [],
            },
            "archive_role": "durable_evaluation_history",
        },
    )
    errors.extend(validate_evaluation_run_record_v1(record))
    archive_created = False
    if not errors:
        _, archive_created = write_evaluation_run_record_v1(record, archive_root=ARCHIVE_ROOT)
        archive_created = archive_created or archive_path.is_file()
    return {
        "case_ref": case.cognitive_test_case_ref,
        "case_id": expected,
        "evaluation_run_id": run_id,
        "execution_mode": CONTROLLED_REPLAY_RUNTIME,
        "replay_input_refs": [item.replay_input_ref for item in replays],
        "replay_provenance_refs": list(run.replay_provenance_refs),
        "cognition_execution": run.cognition_execution,
        "runtime_executed": run.runtime_executed,
        "cognitive_cycle_count": len(proofs),
        "cognitive_transition_count": sum(len(item.cognitive_transition_refs) for item in proofs),
        "cognitive_transition_refs": [ref for item in proofs for ref in item.cognitive_transition_refs],
        "current_world_refs": [_availability(item.current_world_ref, "canonical Current World Candidate") for item in proofs],
        "hypothesis_refs": [list(item.hypothesis_refs) for item in proofs],
        "hypothesis_revision_refs": [item.hypothesis_revision_ref for item in proofs if item.hypothesis_revision_ref],
        "sufficiency": [{"ref": item.sufficiency_ref, "status": item.sufficiency_status} for item in proofs],
        "information_gap_refs": [item.information_gap_ref for item in proofs if item.information_gap_ref],
        "reobservation_refs": [item.reobservation_ref for item in proofs if item.reobservation_ref],
        "next_cycle_ingress_refs": [item.next_cycle_ingress_ref for item in proofs if item.next_cycle_ingress_ref],
        "stop_refs": [item.stop_ref for item in proofs if item.stop_ref],
        "stop_reasons": [item.stop_reason for item in proofs if item.stop_reason],
        "observation_count": _availability(str(len(gateways)), "one Gateway observation per replay cycle"),
        "unnecessary_observation": False,
        "whitebox_trace_ref": run.trace_ref,
        "whitebox_profile_ref": run.execution_profile_ref,
        "failure_gap_refs": list(run.gap_refs),
        "plane_a_result": _jsonable(plane_a),
        "plane_b_result": _jsonable(plane_b),
        "plane_g_result": _jsonable(plane_g),
        "governance_assertion_summary": {item.assertion_id: item.status for item in plane_g.assertion_results},
        "governance_violation_refs": [item.violation_id for item in violations],
        "archive_location": str(archive_path),
        "archive_record_created": archive_created,
        "archive_record_immutable": record.immutable_by_identity,
        "model_invocation": False,
        "provider_invocation": False,
        "live_observation_execution": False,
        "action_execution": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "memory_promotion": False,
        "knowledge_promotion": False,
        "experience_promotion": False,
        "unavailable_metrics": list(collection.unavailable_metrics if collection else ("latency", "resource_usage")),
        "validation_errors": list(dict.fromkeys(errors)),
        "boundary_errors": list(boundary.errors),
        "archive_status": "CREATED" if archive_created else "NOT_CREATED",
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    registry, sample, cases = build_minimum_sufficient_loop_case_inputs_v1()
    execution_instance_id = new_evaluation_run_execution_id_v1()
    case_a = _case_a(cases[0], registry, sample, execution_instance_id)
    case_b = _case_b(cases[1], registry, sample, execution_instance_id)
    case_results = (case_a, case_b)
    return {
        "phase": PHASE,
        "execution_instance_id": execution_instance_id,
        "case_count": len(case_results),
        "case_results": list(case_results),
        "all_cases_archived": all(item["archive_record_created"] for item in case_results),
        "all_cases_validation_clean": all(not item["validation_errors"] for item in case_results),
        "all_cases_governance_compliant": all(item["plane_g_result"]["compliance_status"] == "COMPLIANT" for item in case_results),
        "model_invocation": False,
        "provider_invocation": False,
        "live_observation_execution": False,
        "action_execution": False,
        "field_mutation": False,
        "world_truth_declared": False,
        "memory_promotion": False,
        "knowledge_promotion": False,
        "experience_promotion": False,
        "phase_validation_errors": [error for item in case_results for error in item["validation_errors"]],
    }


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
