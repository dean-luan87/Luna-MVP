"""Observational adapter from canonical A-Route replay evidence to White-box V1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.evaluation.level1_field_cognition_suite.types_v1 import Level1CognitiveTestCaseV1
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteCognitiveExecutionEvidenceV1,
)

from .adapters_v1 import build_luna_cognitive_execution_profile_v1
from .types_v1 import (
    CognitiveWhiteBoxTraceNodeV1,
    CognitiveWhiteBoxTraceV1,
    CognitiveFailureGapRefV1,
    LunaCognitiveExecutionProfileV1,
)


WHITEBOX_OWNER = "Cognitive Development Backend / White-box Observation"
CANONICAL_COGNITION_OWNER = "Cognitive State Formation Governance"


@dataclass(frozen=True)
class WhiteBoxRuntimeCollectionV1:
    evaluation_run_id: str
    trace: CognitiveWhiteBoxTraceV1
    profile: LunaCognitiveExecutionProfileV1
    gap_refs: Tuple[CognitiveFailureGapRefV1, ...]
    unavailable_metrics: Tuple[str, ...]
    observational_only: bool = True


def collect_runtime_whitebox_loop_v1(
    *,
    evaluation_run_id: str,
    case: Level1CognitiveTestCaseV1,
    replay_input_refs: Tuple[str, ...],
    gateway_admission_refs: Tuple[str, ...],
    proofs: Tuple[ARouteCognitiveExecutionEvidenceV1, ...],
) -> WhiteBoxRuntimeCollectionV1:
    """Collect a causally linked multi-cycle proof without inventing nodes."""
    if len(proofs) != 2 or len(replay_input_refs) != 2 or len(gateway_admission_refs) != 2:
        raise ValueError("whitebox_loop_collector_requires_exactly_two_cycles")
    if any(
        proof.execution_mode != "CONTROLLED_REPLAY_RUNTIME"
        or proof.owner_ref != CANONICAL_COGNITION_OWNER
        or not proof.runtime_executed
        or not proof.cognitive_transition_refs
        for proof in proofs
    ):
        raise ValueError("whitebox_loop_collector_requires_canonical_proofs")
    nodes = [
        _node(case, 0, "GOAL", case.goal_ref, "Level-1 Cognitive Test Case Registry", execution_identity_ref=evaluation_run_id, summary="registered case goal input"),
        _node(case, 1, "CONCERN", case.concern_ref, "Level-1 Cognitive Test Case Registry", execution_identity_ref=evaluation_run_id, predecessor_refs=(f"whitebox:{evaluation_run_id}:node:00",)),
    ]
    sequence = 2
    for cycle_index, proof in enumerate(proofs, start=1):
        previous = nodes[-1].trace_node_id
        for source_ref in proof.ingress_refs:
            nodes.append(
                _node(
                    case,
                    sequence,
                    "OBSERVATION" if "observation:" in source_ref else "EVIDENCE",
                    source_ref,
                    "Observation Gateway Governance",
                    execution_identity_ref=evaluation_run_id,
                    cycle=cycle_index - 1,
                    predecessor_refs=(previous,),
                    summary=f"canonical replay ingress reference cycle {cycle_index}",
                )
            )
            previous = nodes[-1].trace_node_id
            sequence += 1
        nodes.append(
            _node(
                case,
                sequence,
                "CURRENT_WORLD_CANDIDATE",
                proof.current_world_ref or f"unavailable:{proof.execution_ref}:current-world",
                CANONICAL_COGNITION_OWNER,
                execution_identity_ref=evaluation_run_id,
                cycle=cycle_index - 1,
                predecessor_refs=(previous,),
                summary=f"canonical Current World Candidate cycle {cycle_index}",
            )
        )
        previous = nodes[-1].trace_node_id
        sequence += 1
        for hypothesis_ref in proof.hypothesis_refs:
            nodes.append(
                _node(
                    case,
                    sequence,
                    "HYPOTHESIS",
                    hypothesis_ref,
                    CANONICAL_COGNITION_OWNER,
                    execution_identity_ref=evaluation_run_id,
                    cycle=cycle_index - 1,
                    predecessor_refs=(previous,),
                    summary=f"canonical Hypothesis candidate cycle {cycle_index}",
                )
            )
            previous = nodes[-1].trace_node_id
            sequence += 1
        loop_nodes = (
            ("SUFFICIENCY", proof.sufficiency_ref, proof.sufficiency_owner_ref),
            ("INFORMATION_GAP", proof.information_gap_ref, proof.information_gap_owner_ref),
            ("REOBSERVATION", proof.reobservation_ref, proof.reobservation_owner_ref),
            ("HYPOTHESIS_REVISION", proof.hypothesis_revision_ref, proof.hypothesis_revision_owner_ref),
            ("STOP_REASON", proof.stop_ref, proof.stop_owner_ref),
        )
        for kind, source_ref, owner_ref in loop_nodes:
            if source_ref is None:
                continue
            nodes.append(
                _node(
                    case,
                    sequence,
                    kind,
                    source_ref,
                    owner_ref or CANONICAL_COGNITION_OWNER,
                    execution_identity_ref=evaluation_run_id,
                    cycle=cycle_index - 1,
                    predecessor_refs=(previous,),
                    summary=proof.stop_reason if kind == "STOP_REASON" else f"canonical {kind} cycle {cycle_index}",
                )
            )
            previous = nodes[-1].trace_node_id
            sequence += 1
    transition_refs = tuple(ref for proof in proofs for ref in proof.cognitive_transition_refs)
    trace = CognitiveWhiteBoxTraceV1(
        trace_id=f"cognitive-trace:{evaluation_run_id}:v1",
        test_case_ref=case.cognitive_test_case_ref,
        task_ref=case.cognitive_task_ref,
        goal_ref=case.goal_ref,
        concern_ref=case.concern_ref,
        nodes=tuple(nodes),
        transition_refs=transition_refs,
        provenance_refs=(*replay_input_refs, *gateway_admission_refs, *(proof.execution_ref for proof in proofs)),
        source_version_refs=("whitebox-runtime-collector:v1",),
        invalidation_refs=(),
        test_board_refs=(f"test-board:level1-replay:{case.cognitive_test_case_ref}:v1",),
    )
    profile = build_luna_cognitive_execution_profile_v1(
        trace,
        role_ref=case.role_ref,
        environment_ref=case.environment_condition_refs[0] if case.environment_condition_refs else None,
        context_refs=(f"context:{evaluation_run_id}",),
        field_refs=(),
        execution_identity_ref=evaluation_run_id,
    )
    return WhiteBoxRuntimeCollectionV1(
        evaluation_run_id=evaluation_run_id,
        trace=trace,
        profile=profile,
        gap_refs=(),
        unavailable_metrics=("evidence_consumed_count", "latency", "resource_usage"),
    )


def _node(
    case: Level1CognitiveTestCaseV1,
    sequence: int,
    kind: str,
    source_ref: str,
    owner_ref: str,
    *,
    execution_identity_ref: str | None = None,
    cycle: int | None = 0,
    predecessor_refs: Tuple[str, ...] = (),
    summary: str = "",
) -> CognitiveWhiteBoxTraceNodeV1:
    return CognitiveWhiteBoxTraceNodeV1(
        trace_node_id=f"whitebox:{execution_identity_ref or case.cognitive_test_case_ref}:node:{sequence:02d}",
        node_kind=kind,
        observability_status="currently_observable",
        owner_ref=owner_ref,
        source_ref=source_ref,
        parent_refs=(),
        predecessor_refs=predecessor_refs,
        successor_refs=(),
        task_ref=case.cognitive_task_ref,
        goal_ref=case.goal_ref,
        concern_ref=case.concern_ref,
        observation_cycle_index=cycle,
        sequence_index=sequence,
        timestamp_ref=None,
        provenance_refs=(f"provenance:whitebox:{execution_identity_ref or case.cognitive_test_case_ref}",),
        source_version_refs=(f"whitebox-runtime-collector:v1",),
        invalidation_refs=(),
        candidate_only=True,
        authoritative=False,
        summary=summary,
    )


def collect_runtime_whitebox_v1(
    *,
    evaluation_run_id: str,
    case: Level1CognitiveTestCaseV1,
    replay_input_ref: str,
    gateway_admission_ref: str,
    ingress_refs: Tuple[str, ...],
    proof: ARouteCognitiveExecutionEvidenceV1,
) -> WhiteBoxRuntimeCollectionV1:
    """Observe only refs emitted by Gateway/A-Route/Cognitive State Formation."""
    if proof.execution_mode != "CONTROLLED_REPLAY_RUNTIME":
        raise ValueError("whitebox_runtime_collector_requires_controlled_replay")
    if proof.owner_ref != CANONICAL_COGNITION_OWNER:
        raise ValueError("whitebox_runtime_collector_owner_mismatch")
    if not proof.runtime_executed or not proof.cognitive_transition_refs:
        raise ValueError("whitebox_runtime_collector_requires_cognitive_proof")

    nodes = [
        _node(case, 0, "GOAL", case.goal_ref, "Level-1 Cognitive Test Case Registry", execution_identity_ref=evaluation_run_id, summary="registered case goal input"),
        _node(case, 1, "CONCERN", case.concern_ref, "Level-1 Cognitive Test Case Registry", execution_identity_ref=evaluation_run_id, predecessor_refs=(f"whitebox:{evaluation_run_id}:node:00",)),
    ]
    previous = nodes[-1].trace_node_id
    for offset, source_ref in enumerate(ingress_refs, start=2):
        kind = "OBSERVATION" if source_ref in proof.ingress_refs and "observation" in source_ref else "EVIDENCE"
        nodes.append(
            _node(
                case,
                offset,
                kind,
                source_ref,
                "Observation Gateway Governance",
                execution_identity_ref=evaluation_run_id,
                predecessor_refs=(previous,),
                summary="canonical replay ingress reference",
            )
        )
        previous = nodes[-1].trace_node_id
    sequence = len(nodes)
    nodes.append(
        _node(
            case,
            sequence,
            "CURRENT_WORLD_CANDIDATE",
            proof.current_world_ref or f"unavailable:{proof.execution_ref}:current-world",
            CANONICAL_COGNITION_OWNER,
            execution_identity_ref=evaluation_run_id,
            predecessor_refs=(previous,),
            summary="canonical candidate returned by Cognitive State Formation",
        )
    )
    previous = nodes[-1].trace_node_id
    for hypothesis_ref in proof.hypothesis_refs:
        nodes.append(
            _node(
                case,
                len(nodes),
                "HYPOTHESIS",
                hypothesis_ref,
                CANONICAL_COGNITION_OWNER,
                execution_identity_ref=evaluation_run_id,
                predecessor_refs=(previous,),
                summary="canonical hypothesis candidate",
            )
        )
        previous = nodes[-1].trace_node_id

    trace = CognitiveWhiteBoxTraceV1(
        trace_id=f"cognitive-trace:{evaluation_run_id}:v1",
        test_case_ref=case.cognitive_test_case_ref,
        task_ref=case.cognitive_task_ref,
        goal_ref=case.goal_ref,
        concern_ref=case.concern_ref,
        nodes=tuple(nodes),
        transition_refs=proof.cognitive_transition_refs,
        provenance_refs=(replay_input_ref, gateway_admission_ref, proof.execution_ref),
        source_version_refs=("whitebox-runtime-collector:v1",),
        invalidation_refs=(),
        test_board_refs=(f"test-board:level1-replay:{case.cognitive_test_case_ref}:v1",),
        candidate_only=True,
        cognition_mutation=False,
        field_mutation=False,
        current_world_authoritative_write=False,
        world_truth_declared=False,
        model_invocation=False,
        provider_invocation=False,
        observation_execution=False,
        action_execution=False,
        dataset_download=False,
    )
    profile = build_luna_cognitive_execution_profile_v1(
        trace,
        role_ref=case.role_ref,
        environment_ref=case.environment_condition_refs[0] if case.environment_condition_refs else None,
        context_refs=(f"context:{evaluation_run_id}",),
        field_refs=(),
        execution_identity_ref=evaluation_run_id,
    )
    unavailable_metrics = (
        "evidence_consumed_count",
        "reobservation_count",
        "latency",
        "resource_usage",
        "stop_reason",
        "decision_governance_handoff",
    )
    return WhiteBoxRuntimeCollectionV1(
        evaluation_run_id=evaluation_run_id,
        trace=trace,
        profile=profile,
        gap_refs=(),
        unavailable_metrics=unavailable_metrics,
    )
