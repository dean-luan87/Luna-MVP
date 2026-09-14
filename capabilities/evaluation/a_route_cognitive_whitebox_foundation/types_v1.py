from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Tuple


OBSERVABILITY_STATUSES = (
    "currently_observable",
    "partially_observable",
    "planned",
    "unavailable",
)

PROFILE_AVAILABILITY = (
    "observed",
    "planned",
    "unavailable",
    "not_observed",
    "not_applicable",
)

COGNITIVE_NODE_KINDS = (
    "GOAL",
    "INTENT",
    "CONCERN",
    "CONTEXT",
    "ROLE",
    "FIELD",
    "ATTENTION",
    "INFORMATION_NEED",
    "OBSERVATION_DEMAND",
    "OBSERVATION_REQUEST",
    "CAPABILITY_REQUIREMENT",
    "CAPABILITY_RESOLUTION",
    "EXTERNAL_CAPABILITY_INVOCATION",
    "OBSERVATION",
    "EVIDENCE",
    "EVIDENCE_RELEVANCE",
    "EVIDENCE_CONFLICT",
    "EVIDENCE_MISSING",
    "EVIDENCE_UNCERTAINTY",
    "CURRENT_WORLD_CANDIDATE",
    "HYPOTHESIS",
    "HYPOTHESIS_REVISION",
    "SUFFICIENCY",
    "INFORMATION_GAP",
    "REOBSERVATION",
    "STOP_REASON",
    "DECISION_GOVERNANCE_HANDOFF",
    "RESULT_CLOSURE",
)

COGNITIVE_GAP_TYPES = (
    "GOAL_GAP",
    "CONTEXT_GAP",
    "ROLE_GAP",
    "FIELD_REPRESENTATION_GAP",
    "ATTENTION_GAP",
    "INFORMATION_NEED_GAP",
    "OBSERVATION_PLANNING_GAP",
    "CAPABILITY_REQUIREMENT_GAP",
    "CAPABILITY_SELECTION_GAP",
    "EXTERNAL_EVIDENCE_GAP",
    "EVIDENCE_RELEVANCE_GAP",
    "EVIDENCE_CONFLICT_HANDLING_GAP",
    "EVIDENCE_UNCERTAINTY_HANDLING_GAP",
    "EVIDENCE_MISSING_HANDLING_GAP",
    "CURRENT_WORLD_FORMATION_GAP",
    "FIELD_COGNITION_GAP",
    "HYPOTHESIS_FORMATION_GAP",
    "HYPOTHESIS_REVISION_GAP",
    "PREMATURE_SUFFICIENCY",
    "DELAYED_SUFFICIENCY",
    "FALSE_INSUFFICIENCY",
    "INFORMATION_GAP_FORMATION_ERROR",
    "REOBSERVATION_TARGET_ERROR",
    "REOBSERVATION_LOOP_ERROR",
    "STOP_CONDITION_ERROR",
    "DECISION_HANDOFF_ERROR",
    "OWNER_BOUNDARY_ERROR",
    "TRACEABILITY_GAP",
    "EXTERNAL_CAPABILITY_FAILURE",
    "PROVIDER_FAILURE",
    "NORMALIZATION_FAILURE",
)

GAP_STATUSES = ("resolved", "unresolved", "deferred")


@dataclass(frozen=True)
class CognitiveWhiteBoxTraceNodeV1:
    trace_node_id: str
    node_kind: str
    observability_status: str
    owner_ref: str
    source_ref: str
    parent_refs: Tuple[str, ...]
    predecessor_refs: Tuple[str, ...]
    successor_refs: Tuple[str, ...]
    task_ref: str
    goal_ref: str
    concern_ref: str
    observation_cycle_index: int | None
    sequence_index: int
    timestamp_ref: str | None
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    candidate_only: bool = True
    authoritative: bool = False
    summary: str = ""
    bounded_metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveWhiteBoxTraceV1:
    trace_id: str
    test_case_ref: str
    task_ref: str
    goal_ref: str
    concern_ref: str
    nodes: Tuple[CognitiveWhiteBoxTraceNodeV1, ...]
    transition_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    test_board_refs: Tuple[str, ...]
    candidate_only: bool = True
    cognition_mutation: bool = False
    field_mutation: bool = False
    current_world_authoritative_write: bool = False
    world_truth_declared: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    observation_execution: bool = False
    action_execution: bool = False
    dataset_download: bool = False


@dataclass(frozen=True)
class ProfileValueV1:
    value: Any
    availability: str
    source_refs: Tuple[str, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class LunaCognitiveExecutionProfileV1:
    execution_profile_id: str
    test_case_ref: str
    task_ref: str
    goal_ref: str
    concern_ref: str
    role_ref: str | None
    environment_ref: str | None
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    prior_cognition_refs: Tuple[str, ...]
    attention_node_refs: Tuple[str, ...]
    attention_transition_count: ProfileValueV1
    selected_target_refs: Tuple[str, ...]
    ignored_target_refs: ProfileValueV1
    information_need_refs: Tuple[str, ...]
    observation_demand_refs: Tuple[str, ...]
    observation_request_refs: Tuple[str, ...]
    capability_requirement_refs: Tuple[str, ...]
    observation_cycle_count: ProfileValueV1
    roi_refs: Tuple[str, ...]
    total_evidence_count: ProfileValueV1
    relevant_evidence_count: ProfileValueV1
    irrelevant_evidence_count: ProfileValueV1
    conflicting_evidence_count: ProfileValueV1
    uncertain_evidence_count: ProfileValueV1
    missing_evidence_refs: Tuple[str, ...]
    current_world_candidate_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    hypothesis_revision_count: ProfileValueV1
    sufficiency_refs: Tuple[str, ...]
    sufficiency_transition_history: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    reobservation_count: ProfileValueV1
    reobservation_reason_refs: Tuple[str, ...]
    reobservation_target_refs: Tuple[str, ...]
    capability_change_refs: ProfileValueV1
    roi_change_refs: ProfileValueV1
    stop_reason: ProfileValueV1
    decision_governance_handoff_ref: ProfileValueV1
    outcome_candidate: ProfileValueV1
    cognitive_transition_count: ProfileValueV1
    latency: ProfileValueV1
    resource_usage: ProfileValueV1
    cognitive_trace_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    test_board_refs: Tuple[str, ...]
    candidate_only: bool = True
    cognition_mutation: bool = False
    field_mutation: bool = False
    current_world_authoritative_write: bool = False
    world_truth_declared: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    observation_execution: bool = False
    action_execution: bool = False
    dataset_download: bool = False


@dataclass(frozen=True)
class CognitiveFailureGapRefV1:
    gap_id: str
    gap_type: str
    detector_ref: str
    responsible_owner_ref: str
    severity: str
    affected_refs: Tuple[str, ...]
    observation_cycle_index: int | None
    trace_node_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    status: str
    invalidation_refs: Tuple[str, ...] = ()


def validate_trace_contract_v1(trace: CognitiveWhiteBoxTraceV1) -> Tuple[str, ...]:
    errors = []
    if not trace.trace_id or not trace.nodes:
        errors.append("trace_identity_or_nodes_missing")
    node_ids = [node.trace_node_id for node in trace.nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("duplicate_trace_node_id")
    for node in trace.nodes:
        if node.node_kind not in COGNITIVE_NODE_KINDS:
            errors.append(f"invalid_node_kind:{node.node_kind}")
        if node.observability_status not in OBSERVABILITY_STATUSES:
            errors.append(f"invalid_observability_status:{node.trace_node_id}")
        if not node.owner_ref or not node.source_ref:
            errors.append(f"missing_owner_or_source:{node.trace_node_id}")
        if not node.candidate_only or node.authoritative:
            errors.append(f"node_authority_boundary:{node.trace_node_id}")
        if node.sequence_index < 0:
            errors.append(f"negative_sequence_index:{node.trace_node_id}")
        if node.observation_cycle_index is not None and node.observation_cycle_index < 0:
            errors.append(f"negative_cycle_index:{node.trace_node_id}")
        forbidden = {"raw_payload", "image_bytes", "base64", "api_key", "auth_header"}
        if forbidden.intersection(str(key) for key in node.bounded_metadata):
            errors.append(f"raw_or_secret_metadata:{node.trace_node_id}")
    if not trace.candidate_only:
        errors.append("trace_not_candidate_only")
    for flag in (
        trace.cognition_mutation,
        trace.field_mutation,
        trace.current_world_authoritative_write,
        trace.world_truth_declared,
        trace.model_invocation,
        trace.provider_invocation,
        trace.observation_execution,
        trace.action_execution,
        trace.dataset_download,
    ):
        if flag:
            errors.append("forbidden_execution_or_mutation_flag")
    return tuple(errors)


def validate_profile_contract_v1(profile: LunaCognitiveExecutionProfileV1) -> Tuple[str, ...]:
    errors = []
    if not profile.execution_profile_id or not profile.cognitive_trace_ref:
        errors.append("profile_identity_or_trace_missing")
    if not profile.candidate_only:
        errors.append("profile_not_candidate_only")
    for name, measure in (
        ("attention_transition_count", profile.attention_transition_count),
        ("observation_cycle_count", profile.observation_cycle_count),
        ("total_evidence_count", profile.total_evidence_count),
        ("relevant_evidence_count", profile.relevant_evidence_count),
        ("irrelevant_evidence_count", profile.irrelevant_evidence_count),
        ("conflicting_evidence_count", profile.conflicting_evidence_count),
        ("uncertain_evidence_count", profile.uncertain_evidence_count),
        ("hypothesis_revision_count", profile.hypothesis_revision_count),
        ("reobservation_count", profile.reobservation_count),
        ("cognitive_transition_count", profile.cognitive_transition_count),
        ("latency", profile.latency),
        ("resource_usage", profile.resource_usage),
    ):
        if measure.availability not in PROFILE_AVAILABILITY:
            errors.append(f"invalid_measure_availability:{name}")
        if measure.availability in {"planned", "unavailable", "not_observed", "not_applicable"} and measure.value is not None:
            errors.append(f"unavailable_measure_has_value:{name}")
        if measure.availability == "observed" and measure.value is None:
            errors.append(f"observed_measure_missing_value:{name}")
    for flag in (
        profile.cognition_mutation,
        profile.field_mutation,
        profile.current_world_authoritative_write,
        profile.world_truth_declared,
        profile.model_invocation,
        profile.provider_invocation,
        profile.observation_execution,
        profile.action_execution,
        profile.dataset_download,
    ):
        if flag:
            errors.append("profile_forbidden_execution_or_mutation_flag")
    return tuple(errors)


def validate_gap_ref_v1(gap: CognitiveFailureGapRefV1) -> Tuple[str, ...]:
    errors = []
    if gap.gap_type not in COGNITIVE_GAP_TYPES:
        errors.append(f"invalid_gap_type:{gap.gap_type}")
    if gap.status not in GAP_STATUSES:
        errors.append(f"invalid_gap_status:{gap.status}")
    if not gap.gap_id or not gap.detector_ref or not gap.responsible_owner_ref:
        errors.append("gap_identity_detector_owner_missing")
    if not gap.trace_node_refs:
        errors.append("gap_trace_nodes_missing")
    return tuple(errors)

