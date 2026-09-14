from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Tuple

from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
)


EVALUATION_AVAILABILITY = (
    "observed",
    "planned",
    "unavailable",
    "not_observed",
    "not_applicable",
)
RUN_EXECUTION_MODES = (
    "synthetic_candidate",
    "real_evaluation",
    SYNTHETIC_CONTROLLED,
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
)
RUN_PLANES = ("PLANE_A_LUNA_COGNITIVE", "PLANE_B_EXTERNAL_CAPABILITY")
BRIDGE_STATUSES = ("READY", "PARTIAL", "BLOCKED")
WHITEBOX_ATTACHMENT_STATUSES = ("ATTACHED", "PARTIAL", "UNAVAILABLE")
RUN_RESULT_STATUSES = (
    "NOT_EXECUTED_CANDIDATE_ONLY",
    "EXECUTION_OBSERVED",
    "BLOCKED",
    "INCOMPLETE",
)


@dataclass(frozen=True)
class EvaluationAvailabilityV1:
    """A value plus an explicit observation state; missing is never zero-filled."""

    value: Any
    availability: str
    source_refs: Tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class ARouteBridgeReadinessV1:
    status: str
    target_ingress_ref: str
    supplied_input_refs: Tuple[str, ...]
    missing_refs: Tuple[str, ...]
    owner_ref: str = "A-Route / Cognitive Governance"
    evaluation_only: bool = True
    cognition_owned_by_bridge: bool = False


@dataclass(frozen=True)
class WhiteBoxAttachmentV1:
    status: str
    trace_ref: str | None
    execution_profile_ref: str | None
    gap_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    reused_trace_profile_v1: bool = True
    evaluation_only: bool = True
    authoritative_runtime_write: bool = False


@dataclass(frozen=True)
class EvaluationRunCandidateV1:
    evaluation_run_id: str
    evaluation_protocol_version: str
    plane: str
    cognitive_level: str
    dataset_ref: str
    dataset_version: str
    sample_ref: str
    sample_version: str
    cognitive_test_case_ref: str
    cognitive_test_case_version: str
    luna_code_version_ref: EvaluationAvailabilityV1
    luna_config_version_ref: EvaluationAvailabilityV1
    environment_condition_refs: Tuple[str, ...]
    perturbation_refs: Tuple[str, ...]
    available_capability_refs: Tuple[str, ...]
    observation_budget_ref: str
    started_at: EvaluationAvailabilityV1
    completed_at: EvaluationAvailabilityV1
    execution_mode: str
    trace_ref: str | None
    execution_profile_ref: str | None
    gap_refs: Tuple[str, ...]
    result_status: str
    failure_attribution_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    a_route_bridge_status: str
    whitebox_attachment_status: str
    comparison_eligibility: EvaluationAvailabilityV1
    runtime_metrics: EvaluationAvailabilityV1
    synthetic: bool = True
    evaluation_only: bool = True
    cognition_execution: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    observation_execution: bool = False
    action_execution: bool = False
    world_truth_declared: bool = False
    field_mutation: bool = False
    memory_promotion: bool = False
    experience_promotion: bool = False
    knowledge_promotion: bool = False
    runtime_executed: bool = False
    live_observation_execution: bool = False
    recorded_evidence_set_ref: str | None = None
    replay_input_ref: str | None = None
    replay_provenance_refs: Tuple[str, ...] = ()
    a_route_ingress_ref: str | None = None
    a_route_execution_ref: str | None = None
    cognition_execution_ref: str | None = None
    task_ref: str | None = None
    goal_ref: str | None = None
    concern_ref: str | None = None
    role_ref: str | None = None
    context_refs: Tuple[str, ...] = ()
    cognitive_result_ref: str | None = None
    capability_fitness_result_status: str = "NOT_EVALUATED"
    governance_compliance_result_ref: str | None = None
    archive_ref: str | None = None
    availability_states: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationRunRecordV1:
    """Immutable historical evaluation evidence, not runtime cognition state."""

    record_id: str
    record_version: str
    evaluation_run: EvaluationRunCandidateV1
    archive_owner_ref: str = "Evaluation Governance"
    immutable_by_identity: bool = True
    append_or_supersede_only: bool = True
    world_truth: bool = False
    runtime_state: bool = False
    memory: bool = False
    experience: bool = False
    knowledge: bool = False
    test_board_refs: Tuple[str, ...] = ()
    bounded_metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlaneBResultV1:
    """Explicit Plane B status; no external capability executes in replay."""

    result_ref: str
    status: str
    reason: str
    evaluation_only: bool = True


def validate_plane_b_result_v1(result: PlaneBResultV1) -> Tuple[str, ...]:
    errors = []
    if not result.result_ref or result.status not in {"PASS", "FAIL", "INCOMPLETE", "NOT_EVALUATED"}:
        errors.append("plane_b_result_invalid")
    if not result.evaluation_only:
        errors.append("plane_b_result_not_evaluation_only")
    if result.status == "NOT_EVALUATED" and not result.reason:
        errors.append("plane_b_not_evaluated_reason_missing")
    return tuple(errors)


def _availability_errors(value: EvaluationAvailabilityV1, field_name: str) -> Tuple[str, ...]:
    errors = []
    if value.availability not in EVALUATION_AVAILABILITY:
        errors.append(f"invalid_availability:{field_name}")
    if value.availability in {"unavailable", "not_observed", "not_applicable"} and value.value is not None:
        errors.append(f"fabricated_unavailable_value:{field_name}")
    if value.availability == "observed" and value.value is None:
        errors.append(f"observed_value_missing:{field_name}")
    return tuple(errors)


def validate_evaluation_run_candidate_v1(run: EvaluationRunCandidateV1) -> Tuple[str, ...]:
    errors = []
    required = (
        run.evaluation_run_id,
        run.evaluation_protocol_version,
        run.plane,
        run.cognitive_level,
        run.dataset_ref,
        run.dataset_version,
        run.sample_ref,
        run.sample_version,
        run.cognitive_test_case_ref,
        run.cognitive_test_case_version,
        run.observation_budget_ref,
    )
    if any(not str(value).strip() for value in required):
        errors.append("run_identity_or_linkage_missing")
    if run.plane not in RUN_PLANES:
        errors.append("invalid_plane")
    if run.execution_mode not in RUN_EXECUTION_MODES:
        errors.append("invalid_execution_mode")
    if run.result_status not in RUN_RESULT_STATUSES:
        errors.append("invalid_run_result_status")
    if run.a_route_bridge_status not in BRIDGE_STATUSES:
        errors.append("invalid_a_route_bridge_status")
    if run.whitebox_attachment_status not in WHITEBOX_ATTACHMENT_STATUSES:
        errors.append("invalid_whitebox_attachment_status")
    for field_name, value in (
        ("luna_code_version_ref", run.luna_code_version_ref),
        ("luna_config_version_ref", run.luna_config_version_ref),
        ("started_at", run.started_at),
        ("completed_at", run.completed_at),
        ("comparison_eligibility", run.comparison_eligibility),
        ("runtime_metrics", run.runtime_metrics),
    ):
        errors.extend(_availability_errors(value, field_name))
    if not run.evaluation_only:
        errors.append("run_not_evaluation_only")
    if not run.synthetic and run.execution_mode == "synthetic_candidate":
        errors.append("synthetic_mode_flag_invalid")
    if run.synthetic and run.cognition_execution:
        errors.append("synthetic_run_claims_cognition_execution")
    if any((run.model_invocation, run.provider_invocation, run.observation_execution, run.live_observation_execution, run.action_execution)):
        errors.append("forbidden_execution_claimed")
    if any((run.world_truth_declared, run.field_mutation, run.memory_promotion, run.experience_promotion, run.knowledge_promotion)):
        errors.append("forbidden_promotion_or_mutation_claimed")
    if run.whitebox_attachment_status == "ATTACHED" and not run.trace_ref:
        errors.append("attached_whitebox_trace_missing")
    if run.capability_fitness_result_status not in {"NOT_EVALUATED", "PASS", "FAIL", "INCOMPLETE"}:
        errors.append("invalid_capability_fitness_result_status")
    if run.execution_mode == CONTROLLED_REPLAY_RUNTIME:
        if run.synthetic:
            errors.append("controlled_replay_marked_synthetic")
        if not run.runtime_executed or not run.cognition_execution:
            errors.append("controlled_replay_cognition_execution_missing")
        if not run.recorded_evidence_set_ref or not run.replay_input_ref or not run.a_route_ingress_ref or not run.a_route_execution_ref:
            errors.append("controlled_replay_runtime_refs_missing")
        if not run.cognitive_result_ref or not run.governance_compliance_result_ref:
            errors.append("controlled_replay_result_refs_missing")
    if run.execution_mode == LIVE_RUNTIME:
        errors.append("live_runtime_not_enabled_for_level1_evaluation")
    return tuple(errors)


def validate_evaluation_run_record_v1(record: EvaluationRunRecordV1) -> Tuple[str, ...]:
    errors = list(validate_evaluation_run_candidate_v1(record.evaluation_run))
    if not record.record_id or not record.record_version:
        errors.append("record_identity_missing")
    if record.archive_owner_ref != "Evaluation Governance":
        errors.append("archive_owner_invalid")
    if not record.immutable_by_identity or not record.append_or_supersede_only:
        errors.append("archive_immutability_invalid")
    if any((record.world_truth, record.runtime_state, record.memory, record.experience, record.knowledge)):
        errors.append("record_boundary_invalid")
    return tuple(errors)
