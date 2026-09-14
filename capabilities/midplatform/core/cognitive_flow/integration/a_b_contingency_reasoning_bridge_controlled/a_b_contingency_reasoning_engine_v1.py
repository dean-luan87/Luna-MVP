"""Candidate-only mechanics for the A -> B-CR -> A bridge."""

from __future__ import annotations

from typing import Iterable, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_engine_v1 import (
    build_grant_status,
    derive_b_grant,
    validate_responsibility_binding,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    DerivedAuthorityGrantCandidateV1,
)

from .a_b_contingency_reasoning_registry_v1 import (
    B_CR_AUTHORITIES,
    B_RESULT_STATUSES,
    EVALUATION_DISPOSITIONS,
    FAILURE_CLASSES,
    REQUIRED_A_TRIGGER_AUTHORITY,
    RESULT_EVALUATION_AUTHORITY,
    ROLE_A,
    ROLE_B,
)
from .a_b_contingency_reasoning_types_v1 import (
    ABConcurrentStateCandidateV1,
    ABContingencyTriggerCandidateV1,
    ABContingencyValidationCandidateV1,
    ABReasoningHandoffCandidateV1,
    ABResultEvaluationCandidateV1,
    BContingencyRequestCandidateV1,
    BContingencyResultCandidateV1,
    BReasoningEnvelopeCandidateV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _validation(
    ref: str,
    kind: str,
    accepted: bool,
    failure: Optional[str],
    *,
    source_owner: str,
    result_receiver: str,
    concern_ok: bool = True,
    work_ok: bool = True,
    state_ok: bool = True,
    authority_ok: bool = True,
    grant_active: bool = True,
    b_loop_control: bool = False,
    b_recursive_delegation: bool = False,
    b_concern_creation: bool = False,
) -> ABContingencyValidationCandidateV1:
    return ABContingencyValidationCandidateV1(
        validation_ref=f"validation:{ref}",
        validation_kind=kind,
        accepted=accepted,
        failure_class=failure,
        source_owner_ref=source_owner,
        result_receiver_ref=result_receiver,
        concern_scope_ok=concern_ok,
        work_scope_ok=work_ok,
        state_version_ok=state_ok,
        authority_scope_ok=authority_ok,
        grant_active=grant_active,
        b_loop_control=b_loop_control,
        b_recursive_delegation=b_recursive_delegation,
        b_concern_creation=b_concern_creation,
        trace_refs=(_trace(ref),),
        provenance_refs=_provenance(ref),
    )


def build_contingency_trigger(
    *,
    trigger_ref: str,
    work_ref: str,
    concern_ref: str,
    source_state_ref: str,
    source_need_ref: str,
    source_hypothesis_refs: Iterable[str],
    uncertainty_ref: str,
    uncertainty_type: str,
    reason_refs: Iterable[str],
    expected_information_value_ref: str,
    a_grant_ref: str,
) -> ABContingencyTriggerCandidateV1:
    return ABContingencyTriggerCandidateV1(
        trigger_ref=trigger_ref,
        work_ref=work_ref,
        concern_ref=concern_ref,
        source_a_state_version_ref=source_state_ref,
        source_need_ref=source_need_ref,
        source_hypothesis_refs=tuple(source_hypothesis_refs),
        uncertainty_ref=uncertainty_ref,
        uncertainty_type=uncertainty_type,
        reason_refs=tuple(reason_refs),
        expected_information_value_ref=expected_information_value_ref,
        a_grant_ref=a_grant_ref,
    )


def validate_a_trigger(
    trigger: ABContingencyTriggerCandidateV1,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    binding: AuthorityResponsibilityBindingCandidateV1,
    *,
    current_state_ref: str,
    revoked: bool = False,
    expired: bool = False,
) -> ABContingencyValidationCandidateV1:
    status = build_grant_status(
        a_grant,
        checked_state_version_ref=current_state_ref,
        revoked=revoked,
        expired=expired,
        binding=binding,
    )
    concern_ok = trigger.concern_ref == a_grant.concern_ref
    work_ok = trigger.work_ref == a_grant.work_ref
    state_ok = trigger.source_a_state_version_ref == a_grant.valid_from_state_ref == current_state_ref
    authority_ok = REQUIRED_A_TRIGGER_AUTHORITY in a_grant.granted_authority_refs
    active = status.valid and not revoked and not expired
    failure = None
    if not authority_ok:
        failure = "AUTHORITY_NOT_GRANTED"
    elif not concern_ok or not work_ok:
        failure = "SCOPE_MISMATCH"
    elif not state_ok:
        failure = "STALE_STATE_VERSION"
    elif revoked:
        failure = "GRANT_REVOKED"
    elif expired:
        failure = "GRANT_EXPIRED"
    elif not validate_responsibility_binding(binding) or not active:
        failure = "AUTHORITY_NOT_GRANTED"
    return _validation(
        trigger.trigger_ref,
        "A_TRIGGER",
        failure is None,
        failure,
        source_owner=trigger.issuing_owner_ref,
        result_receiver=ROLE_A,
        concern_ok=concern_ok,
        work_ok=work_ok,
        state_ok=state_ok,
        authority_ok=authority_ok,
        grant_active=active,
    )


def build_contingency_request(
    *,
    request_ref: str,
    work_ref: str,
    concern_ref: str,
    source_state_ref: str,
    trigger_ref: str,
    a_grant_ref: str,
    derived_b_grant_ref: str,
    scenario_scope_refs: Iterable[str] = (),
    assumption_refs: Iterable[str] = (),
    uncertainty_refs: Iterable[str] = (),
    resource_refs: Iterable[str] = (),
    safety_refs: Iterable[str] = (),
    permission_refs: Iterable[str] = (),
    depth_limit: int = 1,
    branch_limit: int = 1,
    required_result_refs: Iterable[str] = (),
    termination_condition_refs: Iterable[str] = (),
) -> BContingencyRequestCandidateV1:
    return BContingencyRequestCandidateV1(
        request_ref=request_ref,
        work_ref=work_ref,
        concern_ref=concern_ref,
        source_a_state_version_ref=source_state_ref,
        trigger_ref=trigger_ref,
        contingency_question_ref=f"question:{request_ref}",
        scenario_scope_refs=tuple(scenario_scope_refs),
        assumption_refs=tuple(assumption_refs),
        uncertainty_refs=tuple(uncertainty_refs),
        depth_limit=depth_limit,
        branch_limit=branch_limit,
        resource_envelope_refs=tuple(resource_refs),
        safety_refs=tuple(safety_refs),
        permission_refs=tuple(permission_refs),
        required_result_refs=tuple(required_result_refs),
        termination_condition_refs=tuple(termination_condition_refs),
        a_grant_ref=a_grant_ref,
        derived_b_grant_ref=derived_b_grant_ref,
        trace_refs=(_trace(request_ref),),
        provenance_refs=_provenance(request_ref),
    )


def derive_b_contingency_grant(
    a_grant: CognitiveAuthorityGrantCandidateV1,
    request: BContingencyRequestCandidateV1,
    *,
    requested_authorities: Iterable[str] = B_CR_AUTHORITIES,
    a_binding: Optional[AuthorityResponsibilityBindingCandidateV1] = None,
    revoked: bool = False,
    expired: bool = False,
) -> DerivedAuthorityGrantCandidateV1:
    requested = tuple(requested_authorities)
    active = build_grant_status(
        a_grant,
        checked_state_version_ref=request.source_a_state_version_ref,
        revoked=revoked,
        expired=expired,
        binding=a_binding,
    ).valid if a_binding is not None else False
    failure: Optional[str] = None
    if not active:
        failure = "GRANT_REVOKED" if revoked else "GRANT_EXPIRED" if expired else "AUTHORITY_NOT_GRANTED"
    elif request.a_grant_ref != a_grant.grant_ref or request.concern_ref != a_grant.concern_ref or request.work_ref != a_grant.work_ref:
        failure = "SCOPE_MISMATCH"
    elif request.source_a_state_version_ref != a_grant.valid_from_state_ref:
        failure = "STALE_STATE_VERSION"
    elif not request.resource_envelope_refs or not set(request.resource_envelope_refs).issubset(set(a_grant.resource_envelope_refs)):
        failure = "RESOURCE_SCOPE_MISMATCH"
    elif not request.safety_refs or not set(request.safety_refs).issubset(set(a_grant.safety_refs)):
        failure = "SAFETY_SCOPE_MISMATCH"
    elif not request.permission_refs or not set(request.permission_refs).issubset(set(a_grant.permission_refs)):
        failure = "PERMISSION_SCOPE_MISMATCH"
    elif request.depth_limit < 1 or request.branch_limit < 1:
        failure = "SCOPE_MISMATCH"
    elif any(item not in B_CR_AUTHORITIES for item in requested):
        failure = "CAPABILITY_BOUNDARY_VIOLATION"
    if failure:
        rejected = tuple(item for item in requested if item not in B_CR_AUTHORITIES)
        return DerivedAuthorityGrantCandidateV1(
            derived_grant_ref=f"derived:{request.request_ref}",
            source_grant_ref=a_grant.grant_ref,
            request_ref=request.request_ref,
            grant=None,
            inherited_authority_refs=tuple(a_grant.granted_authority_refs),
            derived_authority_refs=(),
            rejected_authority_refs=rejected,
            bounded_by_refs=(a_grant.grant_ref, a_grant.capability_boundary_ref, "boundary:B_CONTINGENCY_ROLE"),
            accepted=False,
            failure_class=failure,
            trace_ref=_trace(f"derived:{request.request_ref}"),
            provenance_refs=_provenance(f"derived:{request.request_ref}"),
        )
    return derive_b_grant(
        a_grant,
        {
            "request_ref": request.request_ref,
            "requester_role": ROLE_A,
            "concern_ref": request.concern_ref,
            "work_ref": request.work_ref,
            "source_state_version_ref": request.source_a_state_version_ref,
            "requested_authorities": requested,
            "resource_ref": request.resource_envelope_refs[0],
            "requested_depth": request.depth_limit,
            "max_depth": request.depth_limit,
            "stop_condition_refs": request.termination_condition_refs,
        },
    )


def build_b_reasoning_envelope(
    request: BContingencyRequestCandidateV1,
    derived_grant_ref: str,
    *,
    goal_refs: Iterable[str] = (),
    intent_refs: Iterable[str] = (),
    role_refs: Iterable[str] = (),
    perspective_refs: Iterable[str] = (),
    field_refs: Iterable[str] = (),
    context_refs: Iterable[str] = (),
    current_world_refs: Iterable[str] = (),
    task_behavior_refs: Iterable[str] = (),
    emotion_modulation_refs: Iterable[str] = (),
    experience_refs: Iterable[str] = (),
    source_a_need_ref: str = "need:current",
    source_a_hypothesis_refs: Iterable[str] = (),
    source_a_expectation_refs: Iterable[str] = (),
    source_a_evidence_refs: Iterable[str] = (),
) -> BReasoningEnvelopeCandidateV1:
    return BReasoningEnvelopeCandidateV1(
        work_ref=request.work_ref,
        concern_ref=request.concern_ref,
        goal_refs=tuple(goal_refs), intent_refs=tuple(intent_refs), role_refs=tuple(role_refs),
        perspective_refs=tuple(perspective_refs), field_refs=tuple(field_refs), context_refs=tuple(context_refs),
        current_world_refs=tuple(current_world_refs), task_behavior_refs=tuple(task_behavior_refs),
        emotion_modulation_refs=tuple(emotion_modulation_refs), experience_refs=tuple(experience_refs),
        source_a_need_ref=source_a_need_ref, source_a_hypothesis_refs=tuple(source_a_hypothesis_refs),
        source_a_expectation_refs=tuple(source_a_expectation_refs), source_a_evidence_refs=tuple(source_a_evidence_refs),
        uncertainty_refs=request.uncertainty_refs, scenario_scope_refs=request.scenario_scope_refs,
        assumption_refs=request.assumption_refs, depth_limit=request.depth_limit, branch_limit=request.branch_limit,
        safety_refs=request.safety_refs, permission_refs=request.permission_refs,
        resource_envelope_refs=request.resource_envelope_refs, source_a_state_version_ref=request.source_a_state_version_ref,
        derived_b_grant_ref=derived_grant_ref, trace_refs=request.trace_refs, provenance_refs=request.provenance_refs,
    )


def build_b_result(
    request: BContingencyRequestCandidateV1,
    *,
    status: str = "COMPLETED_WITH_CANDIDATES",
    derived_b_grant_ref: Optional[str] = None,
    scenario_candidate_refs: Iterable[str] = ("scenario:candidate",),
    conditional_response_candidate_refs: Iterable[str] = ("response:candidate",),
    additional_contingency_need_ref: Optional[str] = None,
    new_concern_suggestion_ref: Optional[str] = None,
) -> BContingencyResultCandidateV1:
    if status not in B_RESULT_STATUSES:
        raise ValueError(f"unsupported B result status: {status}")
    return BContingencyResultCandidateV1(
        result_ref=f"result:{request.request_ref}", request_ref=request.request_ref,
        work_ref=request.work_ref, concern_ref=request.concern_ref,
        source_a_state_version_ref=request.source_a_state_version_ref,
        scenario_candidate_refs=tuple(scenario_candidate_refs),
        conditional_response_candidate_refs=tuple(conditional_response_candidate_refs),
        assumption_refs=request.assumption_refs, uncertainty_boundary_refs=request.uncertainty_refs,
        result_confidence_ref=f"confidence:{request.request_ref}",
        result_limit_refs=request.termination_condition_refs,
        termination_reason_ref=status,
        derived_b_grant_ref=derived_b_grant_ref or request.derived_b_grant_ref,
        additional_contingency_need_ref=additional_contingency_need_ref,
        new_concern_suggestion_ref=new_concern_suggestion_ref,
        trace_refs=(_trace(f"result:{request.request_ref}"),),
        provenance_refs=_provenance(f"result:{request.request_ref}"),
    )


def build_b_handoff(request: BContingencyRequestCandidateV1, result: BContingencyResultCandidateV1) -> ABReasoningHandoffCandidateV1:
    return ABReasoningHandoffCandidateV1(
        handoff_ref=f"handoff:{request.request_ref}", request_ref=request.request_ref,
        result_ref=result.result_ref, source_a_state_version_ref=result.source_a_state_version_ref,
        b_completion_status=result.termination_reason_ref,
        scenario_refs=result.scenario_candidate_refs,
        conditional_refs=result.conditional_response_candidate_refs,
        uncertainty_refs=result.uncertainty_boundary_refs,
        trace_refs=result.trace_refs, provenance_refs=result.provenance_refs,
    )


def evaluate_b_result(
    result: BContingencyResultCandidateV1,
    *,
    current_a_state_version_ref: str,
    current_world_refs: Iterable[str],
    current_need_ref: str,
    current_hypothesis_refs: Iterable[str],
    disposition: str,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    binding: AuthorityResponsibilityBindingCandidateV1,
) -> ABResultEvaluationCandidateV1:
    if disposition not in EVALUATION_DISPOSITIONS:
        raise ValueError(f"unsupported A evaluation disposition: {disposition}")
    status = build_grant_status(
        a_grant,
        checked_state_version_ref=current_a_state_version_ref,
        binding=binding,
    )
    authority_ok = RESULT_EVALUATION_AUTHORITY in a_grant.granted_authority_refs
    if not status.valid or not authority_ok:
        raise ValueError("A result evaluation requires an active evidence-relevance grant")
    stale = result.source_a_state_version_ref != current_a_state_version_ref
    stale_refs = (result.result_ref,) if stale else ()
    discarded = (result.result_ref,) if disposition in {"SUPERSEDE", "DISCARD"} else ()
    adopted = result.scenario_candidate_refs if disposition in {"USE", "PARTIAL_USE"} and not stale else ()
    return ABResultEvaluationCandidateV1(
        evaluation_ref=f"evaluation:{result.result_ref}:{current_a_state_version_ref}",
        b_result_ref=result.result_ref, current_a_state_version_ref=current_a_state_version_ref,
        current_world_refs=tuple(current_world_refs), current_need_ref=current_need_ref,
        current_hypothesis_refs=tuple(current_hypothesis_refs), evaluation_disposition=disposition,
        adopted_candidate_refs=tuple(adopted), discarded_candidate_refs=tuple(discarded),
        stale_b_result_refs=stale_refs,
        reason_refs=("a:current-reality-evaluation", "a:stale-b-result") if stale else ("a:current-reality-evaluation",),
        a_grant_ref=a_grant.grant_ref, trace_refs=(_trace(f"evaluation:{result.result_ref}"),),
        provenance_refs=_provenance(f"evaluation:{result.result_ref}"),
    )


def build_concurrent_state(
    *, work_ref: str, concern_ref: str, a_state_ref: str, b_request_ref: str,
    b_state_ref: str, a_active: bool, b_active: bool,
    shared_read_only_refs: Iterable[str] = (), isolated_local_refs: Iterable[str] = (),
) -> ABConcurrentStateCandidateV1:
    return ABConcurrentStateCandidateV1(
        work_ref=work_ref, concern_ref=concern_ref, a_state_ref=a_state_ref,
        b_request_ref=b_request_ref, b_state_ref=b_state_ref, a_active=a_active, b_active=b_active,
        shared_read_only_refs=tuple(shared_read_only_refs), isolated_local_refs=tuple(isolated_local_refs),
    )


def reject_b_escalation(ref: str, kind: str) -> ABContingencyValidationCandidateV1:
    failure = {
        "LOOP": "B_LOOP_CONTROL_FORBIDDEN",
        "RECURSIVE": "B_RECURSIVE_DELEGATION_FORBIDDEN",
        "CONCERN": "B_CONCERN_CREATION_FORBIDDEN",
    }[kind]
    return _validation(
        ref, f"B_{kind}", False, failure, source_owner=ROLE_B, result_receiver=ROLE_A,
        authority_ok=False, b_loop_control=kind == "LOOP",
        b_recursive_delegation=kind == "RECURSIVE", b_concern_creation=kind == "CONCERN",
    )


__all__ = [
    "build_contingency_trigger", "validate_a_trigger", "build_contingency_request",
    "derive_b_contingency_grant", "build_b_reasoning_envelope", "build_b_result",
    "build_b_handoff", "evaluate_b_result", "build_concurrent_state", "reject_b_escalation",
]
