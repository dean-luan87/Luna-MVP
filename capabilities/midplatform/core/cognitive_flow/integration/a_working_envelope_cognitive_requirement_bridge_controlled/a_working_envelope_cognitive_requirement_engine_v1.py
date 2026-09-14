"""Deterministic candidate-only construction for the A working-context seam."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionContextV1,
    ACurrentNeedDecisionCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_engine_v1 import (
    build_grant_status,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    ROLE_A,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_governance_v1 import (
    form_capability_requirement,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CapabilityRequirementFormationCandidateV1,
    CognitiveNeedCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    resolve_scoped_capability_requirement,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityModuleV1,
    CapabilityScopeAssessmentV1,
    CapabilityResolutionCandidateV1,
    UniversalCapabilitySlotV1,
)

from .a_working_envelope_cognitive_requirement_registry_v1 import (
    CAPABILITY_RESOLUTION_OWNER,
    CAPABILITY_SCOPE_OWNER,
    IMPACT_DISPOSITIONS,
    OBSERVATION_OWNER,
    ROLE_A,
    SUPPORTED_REQUESTS,
)
from .a_working_envelope_cognitive_requirement_types_v1 import (
    AEnvironmentImpactAssessmentCandidateV1,
    ACognitiveRequirementCandidateV1,
    AEvidenceReturnCandidateV1,
    AWorkingEnvelopeCandidateV1,
    WorkingEnvelopeInvalidationCandidateV1,
    WorkingEnvelopeVersionCandidateV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def build_working_envelope(
    *,
    work_ref: str,
    concern_ref: str,
    authority_grant_ref: str,
    source_state_version_ref: str,
    goal_refs: Iterable[str] = (),
    role_refs: Iterable[str] = (),
    perspective_refs: Iterable[str] = (),
    field_refs: Iterable[str] = (),
    context_refs: Iterable[str] = (),
    current_world_refs: Iterable[str] = (),
    task_refs: Iterable[str] = (),
    behavior_refs: Iterable[str] = (),
    emotion_modulation_refs: Iterable[str] = (),
    experience_prior_refs: Iterable[str] = (),
    attention_refs: Iterable[str] = (),
    safety_refs: Iterable[str] = (),
    permission_refs: Iterable[str] = (),
    resource_envelope_refs: Iterable[str] = (),
) -> AWorkingEnvelopeCandidateV1:
    return AWorkingEnvelopeCandidateV1(
        work_ref=work_ref,
        concern_ref=concern_ref,
        goal_refs=tuple(goal_refs),
        authority_grant_ref=authority_grant_ref,
        role_refs=tuple(role_refs),
        perspective_refs=tuple(perspective_refs),
        field_refs=tuple(field_refs),
        context_refs=tuple(context_refs),
        current_world_refs=tuple(current_world_refs),
        task_refs=tuple(task_refs),
        behavior_refs=tuple(behavior_refs),
        emotion_modulation_refs=tuple(emotion_modulation_refs),
        experience_prior_refs=tuple(experience_prior_refs),
        attention_refs=tuple(attention_refs),
        safety_refs=tuple(safety_refs),
        permission_refs=tuple(permission_refs),
        resource_envelope_refs=tuple(resource_envelope_refs),
        source_cognitive_state_version_ref=source_state_version_ref,
        trace_refs=(_trace(work_ref),),
        provenance_refs=_provenance(work_ref),
    )


def build_envelope_version(
    envelope: AWorkingEnvelopeCandidateV1,
    *,
    version_ref: str,
    parent_version_ref: Optional[str],
    changed_source_refs: Iterable[str],
    unchanged_source_refs: Iterable[str],
    change_reason_refs: Iterable[str],
) -> WorkingEnvelopeVersionCandidateV1:
    return WorkingEnvelopeVersionCandidateV1(
        envelope_ref=f"envelope:{envelope.work_ref}",
        version_ref=version_ref,
        parent_version_ref=parent_version_ref,
        source_state_version_ref=envelope.source_cognitive_state_version_ref,
        changed_source_refs=tuple(changed_source_refs),
        unchanged_source_refs=tuple(unchanged_source_refs),
        change_reason_refs=tuple(change_reason_refs),
        trace_refs=(_trace(version_ref),),
        provenance_refs=_provenance(version_ref),
    )


def validate_a_grant(
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    *,
    required_authority: str,
    work_ref: str,
    concern_ref: str,
    state_version_ref: str,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[bool, Optional[str]]:
    if grant is None or binding is None:
        return False, "AUTHORITY_NOT_GRANTED"
    if grant.receiver_role != ROLE_A or grant.work_ref != work_ref or grant.concern_ref != concern_ref:
        return False, "SCOPE_MISMATCH"
    if required_authority not in grant.granted_authority_refs:
        return False, "AUTHORITY_NOT_GRANTED"
    status = build_grant_status(
        grant,
        checked_state_version_ref=state_version_ref,
        revoked=revoked,
        expired=expired,
        binding=binding,
    )
    if status.valid:
        return True, None
    if status.status == "STALE":
        return False, "STALE_STATE_VERSION"
    if status.status == "REVOKED":
        return False, "GRANT_REVOKED"
    if status.status == "EXPIRED":
        return False, "GRANT_EXPIRED"
    if "responsibility" in " ".join(status.reason_refs):
        return False, "RESPONSIBILITY_BINDING_INVALID"
    return False, "AUTHORITY_NOT_GRANTED"


def assess_environment_impact(
    envelope: AWorkingEnvelopeCandidateV1,
    version: WorkingEnvelopeVersionCandidateV1,
    *,
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    disposition: str,
    reason_refs: Iterable[str],
    revoked: bool = False,
    expired: bool = False,
) -> AEnvironmentImpactAssessmentCandidateV1:
    if disposition not in IMPACT_DISPOSITIONS:
        raise ValueError(f"unsupported environment impact disposition: {disposition}")
    accepted, failure = validate_a_grant(
        grant,
        binding,
        required_authority="JUDGE_EVIDENCE_RELEVANCE",
        work_ref=envelope.work_ref,
        concern_ref=envelope.concern_ref,
        state_version_ref=envelope.source_cognitive_state_version_ref,
        revoked=revoked,
        expired=expired,
    )
    return AEnvironmentImpactAssessmentCandidateV1(
        assessment_ref=f"impact:{envelope.work_ref}:{version.version_ref}",
        work_ref=envelope.work_ref,
        concern_ref=envelope.concern_ref,
        source_envelope_ref=f"envelope:{envelope.work_ref}",
        source_envelope_version_ref=version.version_ref,
        source_state_version_ref=envelope.source_cognitive_state_version_ref,
        changed_source_refs=version.changed_source_refs,
        impact_disposition=disposition,
        reason_refs=tuple(reason_refs),
        grant_ref=grant.grant_ref if grant else envelope.authority_grant_ref,
        accepted=accepted,
        failure_class=failure,
    )


def build_a_cognitive_requirement(
    *,
    need_decision: ACurrentNeedDecisionCandidateV1,
    need: CognitiveNeedCandidateV1,
    work_ref: str,
    concern_ref: str,
    source_state_version_ref: str,
    requested_information_type: str,
    information_gap_ref: str,
    priority_ref: str,
    required_evidence_characteristics_refs: Iterable[str],
    resource_constraint_refs: Iterable[str],
    safety_refs: Iterable[str],
    permission_refs: Iterable[str],
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> ACognitiveRequirementCandidateV1:
    accepted, failure = validate_a_grant(
        grant,
        binding,
        required_authority="REQUEST_CAPABILITY",
        work_ref=work_ref,
        concern_ref=concern_ref,
        state_version_ref=source_state_version_ref,
        revoked=revoked,
        expired=expired,
    )
    if not accepted:
        raise ValueError(f"A cognitive requirement rejected: {failure}")
    if need_decision.decision_owner_ref != ROLE_A or need_decision.selected_need_ref != need.need_id:
        raise ValueError("A cognitive requirement requires an accepted A Need decision")
    spec = SUPPORTED_REQUESTS[requested_information_type]
    return ACognitiveRequirementCandidateV1(
        requirement_ref=f"cognitive-requirement:{work_ref}:{need.need_id}",
        work_ref=work_ref,
        concern_ref=concern_ref,
        source_need_decision_ref=need_decision.decision_ref,
        source_need_ref=need.need_id,
        source_state_version_ref=source_state_version_ref,
        information_gap_ref=information_gap_ref,
        requested_information_type=requested_information_type,
        requested_operation=spec["operation"],
        required_evidence_characteristics_refs=tuple(required_evidence_characteristics_refs),
        priority_ref=priority_ref,
        resource_constraint_refs=tuple(resource_constraint_refs),
        safety_refs=tuple(safety_refs),
        permission_refs=tuple(permission_refs),
        trace_refs=(_trace(need.need_id),),
        provenance_refs=_provenance(need.need_id),
    )


def bridge_to_existing_capability_requirement(
    cognitive_requirement: ACognitiveRequirementCandidateV1,
    need: CognitiveNeedCandidateV1,
    *,
    task_context: str,
) -> CapabilityRequirementFormationCandidateV1:
    spec = SUPPORTED_REQUESTS[cognitive_requirement.requested_information_type]
    return form_capability_requirement(
        need,
        formation_id=cognitive_requirement.requirement_ref,
        problem_class=spec["problem_class"],
        requested_operation=spec["operation"],
        input_contract_ref=spec["input_contract"],
        output_contract_ref=spec["output_contract"],
        requirement_type=spec["requirement_type"],
        task_context=task_context,
        permission_refs=cognitive_requirement.permission_refs,
        resource_refs=cognitive_requirement.resource_constraint_refs,
        execution_boundary_ref="Observation Gateway / FPO",
    )


def resolve_existing_capability_requirement(
    formation: CapabilityRequirementFormationCandidateV1,
    modules: Iterable[CapabilityModuleV1],
    slots: Iterable[UniversalCapabilitySlotV1],
    *,
    resource_ready: bool = True,
    permission_granted: bool = True,
) -> Tuple[CapabilityScopeAssessmentV1, CapabilityResolutionCandidateV1, object]:
    return resolve_scoped_capability_requirement(
        formation.requirement,
        modules,
        slots,
        resource_ready=resource_ready,
        permission_granted=permission_granted,
    )


def build_observation_candidate(
    *,
    observation_ref: str,
    evidence_refs: Iterable[str],
    admitted: bool,
    trace_ref: str,
) -> object:
    from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import ObservationCandidateV1

    return ObservationCandidateV1(
        observation_id=observation_ref,
        observation_type="CONTROLLED_REQUIREMENT_ADMISSION",
        evidence_refs=tuple(evidence_refs),
        subject_candidate="synthetic_subject",
        attribute_candidate=None,
        relation_candidate=None,
        spatial_refs=(),
        temporal_refs=(f"temporal:{observation_ref}",),
        uncertainty_refs=(),
        contradiction_refs=(),
        correction_refs=(),
        admission_state="ADMITTED_OBSERVATION" if admitted else "REJECTED",
        routing_targets=("A Route Orchestration",),
        trace_ref=trace_ref,
        provenance_refs=_provenance(observation_ref),
        sensitivity="NORMAL",
        truth_declared=False,
    )


def build_evidence_return(
    *,
    work_ref: str,
    concern_ref: str,
    cognitive_requirement: ACognitiveRequirementCandidateV1,
    formation: CapabilityRequirementFormationCandidateV1,
    scope_ref: str,
    resolution_ref: str,
    observation_ref: str,
    admission_ref: str,
    evidence_refs: Iterable[str],
    state_version_ref: str,
) -> AEvidenceReturnCandidateV1:
    return AEvidenceReturnCandidateV1(
        return_ref=f"evidence-return:{work_ref}:{state_version_ref}",
        work_ref=work_ref,
        concern_ref=concern_ref,
        source_requirement_ref=cognitive_requirement.requirement_ref,
        capability_requirement_ref=formation.requirement_ref,
        scope_ref=scope_ref,
        resolution_ref=resolution_ref,
        observation_candidate_ref=observation_ref,
        observation_admission_ref=admission_ref,
        evidence_refs=tuple(evidence_refs),
        source_state_version_ref=state_version_ref,
        trace_refs=(_trace(work_ref),),
        provenance_refs=_provenance(work_ref),
    )


def build_invalidation(
    *,
    invalidation_ref: str,
    source_change_refs: Iterable[str],
    envelope_ref: str,
    affected_state_version_ref: str,
    affected_grant_refs: Iterable[str],
) -> WorkingEnvelopeInvalidationCandidateV1:
    return WorkingEnvelopeInvalidationCandidateV1(
        invalidation_ref=invalidation_ref,
        source_change_refs=tuple(source_change_refs),
        affected_envelope_ref=envelope_ref,
        affected_state_version_ref=affected_state_version_ref,
        affected_grant_refs=tuple(affected_grant_refs),
    )


__all__ = [
    "build_working_envelope",
    "build_envelope_version",
    "validate_a_grant",
    "assess_environment_impact",
    "build_a_cognitive_requirement",
    "bridge_to_existing_capability_requirement",
    "resolve_existing_capability_requirement",
    "build_observation_candidate",
    "build_evidence_return",
    "build_invalidation",
    "CAPABILITY_SCOPE_OWNER",
    "CAPABILITY_RESOLUTION_OWNER",
    "OBSERVATION_OWNER",
]
