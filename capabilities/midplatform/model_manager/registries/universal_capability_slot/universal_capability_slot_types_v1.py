"""Candidate-only Universal Capability Slot and Official Module contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


OWNER = "Capability Registry / Capability Governance"
ADMISSION_OWNER = "Capability Admission Governance"
MODEL_PROVIDER_BOUNDARY = "Model Manager / Provider Governance"

ORIGIN_VALUES = ("OFFICIAL", "MARKET")
REQUIREMENT_CLASSES = ("MANDATORY_SAFETY", "SYSTEM_REQUIRED", "OPTIONAL")
SLOT_LIFECYCLE_STATES = (
    "EMPTY",
    "BOUND",
    "UNBOUND",
    "SUSPENDED",
    "DEGRADED",
    "RECOVERABLE",
)
MODULE_LIFECYCLE_STATES = (
    "AVAILABLE",
    "ADMITTED",
    "BOUND",
    "INSTALLED",
    "ACTIVE",
    "SUSPENDED",
    "DEGRADED",
    "INCOMPATIBLE",
    "UNAVAILABLE",
    "RECOVERABLE",
    "RETIRED",
)
SLOT_BINDING_STATES = ("EMPTY", "BINDING_CANDIDATE", "BOUND", "UNBINDING_CANDIDATE")
RESOLUTION_STATUSES = ("READY_CANDIDATE", "UNAVAILABLE_CANDIDATE", "DEGRADED_CANDIDATE")
REGULATION_ACTIONS = (
    "ACQUIRE",
    "DOWNLOAD",
    "INSTALL",
    "BIND",
    "ACTIVATE",
    "SUSPEND",
    "RESUME",
    "RELEASE",
    "UNLOAD",
    "UNINSTALL_IMPLEMENTATION",
    "RESTORE",
    "REBIND",
    "REPLACE",
    "UPGRADE",
    "DEGRADE",
    "ROLLBACK",
)


@dataclass(frozen=True)
class SlotModuleBindingV1:
    slot_id: str
    module_id: str
    module_version: str
    binding_state: str
    admission_ref: str
    compatibility_assessment_ref: str
    implementation_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class UniversalCapabilitySlotV1:
    slot_id: str
    slot_version: str
    lifecycle_state: str
    current_module_binding: Optional[SlotModuleBindingV1]
    compatibility_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    health_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    history_refs: Tuple[str, ...]
    recovery_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    self_visibility: str
    candidate_only: bool = True
    slot_semantic_authority: bool = False
    slot_world_truth_authority: bool = False


@dataclass(frozen=True)
class CapabilityModuleV1:
    module_id: str
    capability_purpose: str
    problem_classes: Tuple[str, ...]
    origin: str
    requirement_class: str
    module_version: str
    lifecycle_state: str
    implementation_refs: Tuple[str, ...]
    input_contract_refs: Tuple[str, ...]
    output_contract_refs: Tuple[str, ...]
    provider_contract_refs: Tuple[str, ...]
    model_asset_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    compatibility_refs: Tuple[str, ...]
    integrity_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    degradation_policy_refs: Tuple[str, ...]
    rollback_refs: Tuple[str, ...]
    self_visibility: str
    knowledge_dependency_refs: Tuple[str, ...] = ()
    capability_semantic_annotation_ref: Optional[str] = None
    accepted_requirement_types: Tuple[str, ...] = ()
    accepted_input_contract_refs: Tuple[str, ...] = ()
    produced_output_contract_refs: Tuple[str, ...] = ()
    supported_operation_refs: Tuple[str, ...] = ()
    explicit_boundary_refs: Tuple[str, ...] = ()
    known_non_capability_refs: Tuple[str, ...] = ()
    authority_boundary_refs: Tuple[str, ...] = ()
    execution_boundary_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    module_world_truth_authority: bool = False


@dataclass(frozen=True)
class OfficialCapabilityModuleV1(CapabilityModuleV1):
    """Official is an origin value, not a Slot specialization."""

    def __post_init__(self) -> None:
        if self.origin != "OFFICIAL":
            raise ValueError("OfficialCapabilityModuleV1 requires origin=OFFICIAL")


@dataclass(frozen=True)
class ModuleAdmissionCandidateV1:
    module_id: str
    origin: str
    definition_admission_ref: str
    implementation_admission_ref: str
    model_provider_admission_ref: str
    integrity_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ModuleAdmissionOutcomeV1:
    module_id: str
    accepted: bool
    definition_admitted: bool
    implementation_admitted: bool
    model_provider_admitted: bool
    reason: str
    lifecycle_state: str
    candidate_only: bool = True
    installation_executed: bool = False
    activation_executed: bool = False
    provider_invocation: bool = False


@dataclass(frozen=True)
class SlotCompatibilityAssessmentV1:
    slot_id: str
    module_id: str
    compatible: bool
    reason: str
    compatibility_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityBindingCandidateV1:
    slot_id: str
    module_id: str
    admission_ref: str
    compatibility_assessment_ref: str
    binding_state: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityBindingOutcomeV1:
    slot_id: str
    module_id: str
    accepted: bool
    reason: str
    binding_state: str
    projected_slot: UniversalCapabilitySlotV1
    candidate_only: bool = True
    state_mutation_executed: bool = False
    installation_executed: bool = False
    activation_executed: bool = False


@dataclass(frozen=True)
class SlotLifecycleCandidateV1:
    slot_id: str
    requested_state: str
    accepted: bool
    actor: str
    reason: str
    projected_slot: UniversalCapabilitySlotV1
    candidate_only: bool = True
    state_mutation_executed: bool = False


@dataclass(frozen=True)
class CapabilityRequirementV1:
    requirement_id: str
    requested_module_id: Optional[str]
    purpose: str
    task_context: str
    required_semantic_depth: str
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    execution_boundary_ref: str
    candidate_only: bool = True
    requester_ref: Optional[str] = None
    requirement_type: str = "CAPABILITY_REQUEST"
    problem_class: Optional[str] = None
    requested_operation: Optional[str] = None
    input_contract_ref: Optional[str] = None
    expected_output_contract_ref: Optional[str] = None
    required_authority: str = "EVIDENCE_ONLY"
    task_context_refs: Tuple[str, ...] = ()
    trace_ref: Optional[str] = None
    technical_hints: Tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilityScopeAssessmentV1:
    requirement_ref: str
    module_ref: Optional[str]
    scope_result: str
    in_scope: bool
    problem_class_supported: bool
    operation_supported: bool
    input_contract_supported: bool
    output_contract_supported: bool
    authority_supported: bool
    boundary_violation_refs: Tuple[str, ...]
    unmet_requirement_refs: Tuple[str, ...]
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityGapCandidateV1:
    gap_id: str
    originating_requirement_ref: str
    rejected_module_refs: Tuple[str, ...]
    unmet_problem_class: Optional[str]
    unmet_operation: Optional[str]
    unmet_contract_refs: Tuple[str, ...]
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityResolutionCandidateV1:
    requirement_id: str
    status: str
    module_ref: Optional[str]
    slot_ref: Optional[str]
    implementation_refs: Tuple[str, ...]
    model_asset_refs: Tuple[str, ...]
    provider_contract_refs: Tuple[str, ...]
    reason: str
    recovery_available: bool
    candidate_only: bool = True
    provider_invocation: bool = False
    model_inference: bool = False
    scope_assessment_ref: Optional[str] = None
    capability_gap_ref: Optional[str] = None


@dataclass(frozen=True)
class CapabilityRuntimeAdmissionResultV1:
    """Owner-derived capability admission prerequisite for one runtime scope."""

    result_ref: str
    binding_key: Tuple[str, ...]
    capability_candidate_ref: str
    provider_candidate_ref: str
    execution_instance_preparation_candidate_ref: str
    status: str
    reason: str
    catalog_ref: str
    catalog_version: str
    evaluation_profile_ref: str = ""
    owner_ref: str = ADMISSION_OWNER
    authoritative: bool = True
    candidate_only: bool = False
    read_only: bool = True


@dataclass(frozen=True)
class CapabilityRuntimeEvaluationProfileV1:
    """Owner-defined catalog view for one runtime admission evaluation mode."""

    profile_ref: str
    owner_ref: str
    catalog_ref: str
    catalog_version: str
    capability_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...] = ()
    production_canonical: bool = False


@dataclass(frozen=True)
class CapabilityInvocationCandidateV1:
    invocation_id: str
    requirement_ref: str
    module_ref: Optional[str]
    slot_ref: Optional[str]
    execution_boundary_ref: str
    accepted: bool
    reason: str
    candidate_only: bool = True
    real_provider_invocation: bool = False
    model_inference: bool = False
    runtime_execution: bool = False
    observation_gateway_bypass: bool = False
    scope_assessment_ref: Optional[str] = None
    implementation_refs: Tuple[str, ...] = ()
    model_asset_refs: Tuple[str, ...] = ()
    provider_contract_refs: Tuple[str, ...] = ()
    gateway_refs: Tuple[str, ...] = ()
    trace_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class CapabilitySelfViewV1:
    current_refs: Tuple[str, ...]
    unavailable_refs: Tuple[str, ...]
    degraded_refs: Tuple[str, ...]
    suspended_refs: Tuple[str, ...]
    recoverable_refs: Tuple[str, ...]
    historical_refs: Tuple[str, ...]
    potential_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    semantic_annotation_refs: Tuple[str, ...] = ()
    scope_problem_class_refs: Tuple[str, ...] = ()
    scope_operation_refs: Tuple[str, ...] = ()
    scope_boundary_refs: Tuple[str, ...] = ()
    usage_profile_refs: Tuple[str, ...] = ()
    weakness_candidate_refs: Tuple[str, ...] = ()
    feedback_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    self_is_lifecycle_owner: bool = False


@dataclass(frozen=True)
class CapabilityRegulationCandidateV1:
    candidate_id: str
    action: str
    module_ref: str
    slot_ref: Optional[str]
    source: str
    reason: str
    governance_handoff_ref: str
    candidate_only: bool = True
    direct_capability_mutation: bool = False
    automatic_optimization: bool = False
    automatic_acquisition: bool = False
    automatic_uninstall: bool = False


@dataclass(frozen=True)
class CapabilityUsageRecordV1:
    """One candidate-only observation of a capability use."""

    usage_id: str
    module_ref: str
    module_version_ref: Optional[str]
    slot_ref: Optional[str]
    invocation_ref: str
    requirement_ref: str
    problem_class: str
    operation: str
    context_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    execution_result_ref: Optional[str]
    execution_outcome: str
    requirement_satisfaction: str
    task_contribution: str
    failure_refs: Tuple[str, ...]
    degradation_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    candidate_only: bool = True
    raw_personal_data_included: bool = False


@dataclass(frozen=True)
class CapabilityOutcomeAssessmentV1:
    """Separate execution, requirement, and task dimensions."""

    assessment_id: str
    usage_ref: str
    execution_outcome: str
    requirement_satisfaction: str
    task_contribution: str
    evidence_refs: Tuple[str, ...]
    failure_pattern_refs: Tuple[str, ...]
    reason: str
    candidate_only: bool = True
    world_truth_declared: bool = False
    lifecycle_mutation: bool = False


@dataclass(frozen=True)
class IndividualCapabilityExperienceProfileV1:
    """Bounded aggregate projection for one Luna and one capability."""

    profile_id: str
    module_ref: str
    aggregation_window_ref: str
    usage_count: int
    execution_success_count: int
    execution_failure_count: int
    execution_degraded_count: int
    requirement_satisfied_count: int
    requirement_partial_count: int
    requirement_unsatisfied_count: int
    task_resolved_count: int
    task_contributed_count: int
    task_no_contribution_count: int
    problem_class_distribution: Tuple[str, ...]
    operation_distribution: Tuple[str, ...]
    failure_pattern_distribution: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    candidate_only: bool = True
    scalar_value_score: bool = False
    lifecycle_mutation: bool = False


@dataclass(frozen=True)
class CapabilityWeaknessCandidateV1:
    """Evidence of insufficiency in an existing admitted capability."""

    weakness_id: str
    module_ref: str
    problem_class: str
    operation: str
    context_refs: Tuple[str, ...]
    source_profile_ref: str
    evidence_refs: Tuple[str, ...]
    reason: str
    candidate_only: bool = True
    scope_mutation: bool = False
    lifecycle_mutation: bool = False
    model_replacement: bool = False
    provider_replacement: bool = False
    learning_trigger: bool = False
    improvement_execution: bool = False


@dataclass(frozen=True)
class HiveCapabilityFeedbackCandidateV1:
    """Privacy-conscious aggregate candidate; never a raw telemetry packet."""

    feedback_id: str
    module_ref: str
    aggregation_window_ref: str
    sample_count: int
    problem_class_buckets: Tuple[str, ...]
    operation_buckets: Tuple[str, ...]
    execution_outcome_buckets: Tuple[str, ...]
    requirement_satisfaction_buckets: Tuple[str, ...]
    task_contribution_buckets: Tuple[str, ...]
    weakness_refs: Tuple[str, ...]
    gap_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    privacy_policy_ref: str
    raw_conversations_included: bool = False
    raw_images_included: bool = False
    raw_audio_included: bool = False
    identity_records_included: bool = False
    memory_contents_included: bool = False
    full_personal_task_histories_included: bool = False
    candidate_only: bool = True
    direct_individual_mutation: bool = False


@dataclass(frozen=True)
class HiveCapabilityDemandCandidateV1:
    """Aggregate demand candidate, distinct between weakness and capability gap."""

    demand_id: str
    demand_kind: str
    problem_class: str
    operation: str
    source_feedback_ref: str
    source_profile_refs: Tuple[str, ...]
    existing_module_refs: Tuple[str, ...]
    unmet_requirement_refs: Tuple[str, ...]
    aggregate_count: int
    reason: str
    candidate_only: bool = True
    executes_acquisition: bool = False
    executes_learning: bool = False
    executes_model_replacement: bool = False
    executes_provider_replacement: bool = False
