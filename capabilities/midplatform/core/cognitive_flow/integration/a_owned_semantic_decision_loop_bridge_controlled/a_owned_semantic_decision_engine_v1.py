"""Candidate-only A semantic decisions."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    DynamicCognitiveLoopOutputV1,
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

from .a_owned_semantic_decision_registry_v1 import (
    COMPATIBILITY_SOURCE_OWNER,
    DECISION_OWNER,
    NEXT_STEP_DISPOSITIONS,
    REQUIRED_AUTHORITIES,
    SUFFICIENCY_STATUSES,
)
from .a_owned_semantic_decision_types_v1 import (
    ACognitiveHypothesisDecisionCandidateV1,
    ACognitiveSemanticJudgmentV1,
    ACurrentNeedDecisionCandidateV1,
    ALocalSufficiencyDecisionCandidateV1,
    ANextStepDecisionCandidateV1,
    AReconsiderationDecisionCandidateV1,
    ASemanticDecisionBundleV1,
    ASemanticDecisionContextV1,
    ASemanticDecisionValidationCandidateV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _strict_ref_tuple(value: Any, field: str) -> Tuple[str, ...]:
    if type(value) is not tuple:
        raise ValueError(f"A_CONTRACT_REJECTION:{field}_must_be_tuple")
    if any(type(item) is not str or not item.strip() for item in value):
        raise ValueError(f"A_CONTRACT_REJECTION:{field}_member_invalid")
    return value


def _strict_optional_ref(value: Any, field: str) -> str | None:
    if value is not None and (type(value) is not str or not value.strip()):
        raise ValueError(f"A_CONTRACT_REJECTION:{field}_invalid")
    return value


def validate_a_semantic_judgment_input(
    *,
    context: ASemanticDecisionContextV1,
    source_snapshot_ref: str,
    current_world_ref: str,
    attention_refs: Tuple[str, ...],
    evidence_refs: Tuple[str, ...],
    required_information_refs: Tuple[str, ...],
    available_information_refs: Tuple[str, ...],
    requirement_establishment_status: str,
    prior_hypothesis_refs: Tuple[str, ...],
    prior_information_gap_ref: str | None,
    prior_reobservation_ref: str | None,
    conflict_refs: Tuple[str, ...] = (),
) -> None:
    """Validate the A entry contract before any semantic computation."""
    if not isinstance(context, ASemanticDecisionContextV1):
        raise ValueError("A_CONTRACT_REJECTION:context_type_invalid")
    if (
        type(context.candidate_only) is not bool
        or type(context.synthetic_only) is not bool
        or context.candidate_only is not True
    ):
        raise ValueError("A_CONTRACT_REJECTION:context_control_flags_invalid")
    for field in (
        "work_ref", "concern_ref", "a_grant_ref", "source_state_version_ref",
    ):
        value = getattr(context, field)
        if type(value) is not str or not value.strip():
            raise ValueError(f"A_CONTRACT_REJECTION:context_{field}_invalid")
    for field in (
        "goal_refs", "intent_refs", "role_refs", "perspective_refs", "field_refs",
        "context_refs", "current_world_refs", "task_behavior_refs",
        "emotion_modulation_refs", "experience_refs", "safety_refs", "permission_refs",
        "resource_envelope_refs", "evidence_refs", "prior_need_refs",
        "prior_hypothesis_refs", "prior_requirement_refs", "trace_refs",
        "provenance_refs", "contradiction_refs",
    ):
        _strict_ref_tuple(getattr(context, field), f"context.{field}")
    for field, value in (
        ("source_snapshot_ref", source_snapshot_ref),
        ("current_world_ref", current_world_ref),
    ):
        if type(value) is not str or not value.strip():
            raise ValueError(f"A_CONTRACT_REJECTION:{field}_invalid")
    for field, value in (
        ("attention_refs", attention_refs),
        ("evidence_refs", evidence_refs),
        ("required_information_refs", required_information_refs),
        ("available_information_refs", available_information_refs),
        ("prior_hypothesis_refs", prior_hypothesis_refs),
        ("conflict_refs", conflict_refs),
    ):
        _strict_ref_tuple(value, field)
    if type(requirement_establishment_status) is not str or not requirement_establishment_status.strip():
        raise ValueError("A_CONTRACT_REJECTION:requirement_establishment_status_invalid")
    _strict_optional_ref(prior_information_gap_ref, "prior_information_gap_ref")
    _strict_optional_ref(prior_reobservation_ref, "prior_reobservation_ref")
    if (prior_information_gap_ref is None) != (prior_reobservation_ref is None):
        raise ValueError("A_CONTRACT_REJECTION:prior_revision_refs_incomplete")
    if context.contradiction_refs != conflict_refs:
        raise ValueError("A_CONTRACT_REJECTION:conflict_refs_context_mismatch")


def _judgment_ref_tuple(value: Any, field: str) -> bool:
    return type(value) is tuple and all(
        type(item) is str and bool(item.strip()) for item in value
    )


def validate_a_semantic_judgment_projection(
    judgment: Any,
    *,
    semantic_owner_ref: Any,
    semantic_judgment_ref: Any,
    hypothesis_refs: Any,
    sufficiency_ref: Any,
    sufficiency_status: Any,
    information_gap_ref: Any,
    reobservation_ref: Any,
    hypothesis_revision_ref: Any,
    hypothesis_revision_information_gap_ref: Any,
    hypothesis_revision_reobservation_ref: Any,
    stop_ref: Any,
    semantic_provenance_refs: Any,
    conflict_refs: Any = (),
) -> Tuple[str, ...]:
    """Check that a proof is an exact projection of the A judgment."""
    errors = []
    if not isinstance(judgment, ACognitiveSemanticJudgmentV1):
        return ("a_judgment_type_invalid",)
    if judgment.candidate_only is not True:
        errors.append("a_judgment_candidate_boundary_invalid")
    for hypothesis in judgment.hypothesis_candidates:
        if (
            not isinstance(hypothesis, ACognitiveHypothesisDecisionCandidateV1)
            or hypothesis.semantic_owner_ref != "A_REASONING_ROLE"
            or hypothesis.candidate_only is not True
            or hypothesis.truth_declared is not False
            or hypothesis.world_truth_declared is not False
            or not _judgment_ref_tuple(hypothesis.conflict_refs, "hypothesis.conflict_refs")
        ):
            errors.append("a_judgment_hypothesis_boundary_invalid")
            break
    if not _judgment_ref_tuple(conflict_refs, "conflict_refs"):
        errors.append("a_judgment_conflict_refs_invalid")
    else:
        judgment_conflict_refs = tuple(
            ref
            for hypothesis in judgment.hypothesis_candidates
            for ref in hypothesis.conflict_refs
        )
        if conflict_refs != judgment_conflict_refs:
            errors.append("a_judgment_conflict_refs_mismatch")
    if judgment.semantic_owner_ref != "A_REASONING_ROLE" or semantic_owner_ref != judgment.semantic_owner_ref:
        errors.append("a_judgment_owner_unbound")
    if not judgment.judgment_ref or not isinstance(judgment.judgment_ref, str):
        errors.append("a_judgment_ref_invalid")
    elif semantic_judgment_ref != judgment.judgment_ref:
        errors.append("a_judgment_ref_mismatch")
    if not _judgment_ref_tuple(hypothesis_refs, "hypothesis_refs"):
        errors.append("a_judgment_hypothesis_refs_invalid")
    elif hypothesis_refs != tuple(item.hypothesis_ref for item in judgment.hypothesis_candidates):
        errors.append("a_judgment_hypothesis_refs_mismatch")
    if sufficiency_ref != judgment.sufficiency_ref:
        errors.append("a_judgment_sufficiency_ref_mismatch")
    if sufficiency_status != judgment.sufficiency_status:
        errors.append("a_judgment_sufficiency_status_mismatch")
    if information_gap_ref != judgment.information_gap_ref:
        errors.append("a_judgment_information_gap_mismatch")
    if reobservation_ref != judgment.reobservation_ref:
        errors.append("a_judgment_reobservation_mismatch")
    if hypothesis_revision_ref != judgment.reconsideration_ref:
        errors.append("a_judgment_revision_mismatch")
    if hypothesis_revision_information_gap_ref != judgment.prior_information_gap_ref:
        errors.append("a_judgment_revision_gap_mismatch")
    if hypothesis_revision_reobservation_ref != judgment.prior_reobservation_ref:
        errors.append("a_judgment_revision_reobservation_mismatch")
    if stop_ref != judgment.local_disposition_ref:
        errors.append("a_judgment_stop_mismatch")
    if not _judgment_ref_tuple(semantic_provenance_refs, "semantic_provenance_refs"):
        errors.append("a_judgment_provenance_invalid")
    elif semantic_provenance_refs != judgment.provenance_refs:
        errors.append("a_judgment_provenance_mismatch")
    if judgment.relationship_truth_mutation or judgment.field_truth_declared or judgment.current_world_truth_declared:
        errors.append("a_judgment_negative_boundary_violation")
    return tuple(errors)


def form_cognitive_semantic_judgment(
    *,
    context: ASemanticDecisionContextV1,
    source_snapshot_ref: str,
    current_world_ref: str,
    attention_refs: Tuple[str, ...],
    evidence_refs: Tuple[str, ...],
    required_information_refs: Tuple[str, ...],
    available_information_refs: Tuple[str, ...],
    requirement_establishment_status: str,
    prior_hypothesis_refs: Tuple[str, ...] = (),
    prior_information_gap_ref: str | None = None,
    prior_reobservation_ref: str | None = None,
    conflict_refs: Tuple[str, ...] = (),
) -> ACognitiveSemanticJudgmentV1:
    """Form concern-local semantics from a pre-semantic CState snapshot.

    CState supplies aligned references and a candidate Current World view.  A
    owns the interpretation and disposition derived from those inputs.  This
    function deliberately does not mutate Field/relationship state or declare
    world truth.
    """

    validate_a_semantic_judgment_input(
        context=context,
        source_snapshot_ref=source_snapshot_ref,
        current_world_ref=current_world_ref,
        attention_refs=attention_refs,
        evidence_refs=evidence_refs,
        required_information_refs=required_information_refs,
        available_information_refs=available_information_refs,
        requirement_establishment_status=requirement_establishment_status,
        prior_hypothesis_refs=prior_hypothesis_refs,
        prior_information_gap_ref=prior_information_gap_ref,
        prior_reobservation_ref=prior_reobservation_ref,
        conflict_refs=conflict_refs,
    )
    required = required_information_refs
    available = set(available_information_refs)
    missing = tuple(ref for ref in required if ref not in available)
    established = requirement_establishment_status == "ESTABLISHED"
    if established and not missing:
        sufficiency_status = "SUFFICIENT"
    elif established:
        sufficiency_status = "INSUFFICIENT"
    elif requirement_establishment_status == "WITHHELD":
        sufficiency_status = "WITHHELD"
    else:
        sufficiency_status = "UNKNOWN"

    if prior_information_gap_ref and prior_reobservation_ref:
        hypothesis_state = "REVISED"
    elif conflict_refs:
        hypothesis_state = "CONTESTED"
    elif missing:
        hypothesis_state = "INSUFFICIENT_EVIDENCE"
    else:
        hypothesis_state = "SUPPORTED"
    hypothesis_ref = f"a-hypothesis:{context.work_ref}:{context.source_state_version_ref}:v1"
    hypothesis = ACognitiveHypothesisDecisionCandidateV1(
        hypothesis_ref=hypothesis_ref,
        hypothesis_statement=(
            f"A concern-local interpretation for {context.concern_ref} over "
            f"snapshot {source_snapshot_ref}"
        ),
        supporting_evidence_refs=tuple(evidence_refs),
        unknown_refs=missing,
        source_snapshot_ref=source_snapshot_ref,
        state=hypothesis_state,
        trace_ref=_trace(f"a-semantic:{context.work_ref}:hypothesis"),
        provenance_refs=(
            *context.provenance_refs,
            *tuple(evidence_refs),
            source_snapshot_ref,
        ),
        conflict_refs=conflict_refs,
    )

    if sufficiency_status == "SUFFICIENT":
        local_disposition = "STOP_SUFFICIENT"
        disposition_reasons = ("a:cognitive_information_sufficient",)
        information_gap_ref = None
        reobservation_ref = None
        next_cycle_ingress_ref = None
        reobservation_owner_ref = None
    elif prior_information_gap_ref and prior_reobservation_ref:
        local_disposition = "RECONSIDER"
        disposition_reasons = (prior_information_gap_ref, prior_reobservation_ref)
        information_gap_ref = prior_information_gap_ref
        reobservation_ref = None
        next_cycle_ingress_ref = None
        reobservation_owner_ref = None
    elif sufficiency_status == "INSUFFICIENT":
        local_disposition = "ACQUIRE_INFORMATION"
        information_gap_ref = f"information-gap:{context.source_state_version_ref}:v1"
        reobservation_ref = f"reobservation:{context.source_state_version_ref}:v1"
        next_cycle_ingress_ref = f"next-cycle-ingress:{context.source_state_version_ref}:v1"
        reobservation_owner_ref = "Field Perception Orchestrator"
        disposition_reasons = tuple(missing) or ("a:required-information-missing",)
    else:
        local_disposition = "CONTINUE"
        information_gap_ref = None
        reobservation_ref = None
        next_cycle_ingress_ref = None
        reobservation_owner_ref = None
        disposition_reasons = ("a:cognitive-sufficiency-undetermined",)

    reconsideration_ref = (
        f"hypothesis-revision:{context.source_state_version_ref}:v1"
        if prior_information_gap_ref and prior_reobservation_ref
        else None
    )
    judgment_ref = f"a-semantic-judgment:{context.work_ref}:{context.source_state_version_ref}:v1"
    return ACognitiveSemanticJudgmentV1(
        judgment_ref=judgment_ref,
        source_snapshot_ref=source_snapshot_ref,
        current_world_ref=current_world_ref,
        hypothesis_candidates=(hypothesis,),
        sufficiency_ref=f"sufficiency:{context.source_state_version_ref}:v1",
        sufficiency_status=sufficiency_status,
        missing_information_refs=missing,
        information_gap_ref=information_gap_ref,
        reobservation_ref=reobservation_ref,
        next_cycle_ingress_ref=next_cycle_ingress_ref,
        reobservation_owner_ref=reobservation_owner_ref,
        reconsideration_ref=reconsideration_ref,
        local_disposition=local_disposition,
        local_disposition_ref=(
            f"stop:{context.source_state_version_ref}:v1"
            if local_disposition == "STOP_SUFFICIENT"
            else None
        ),
        disposition_reason_refs=disposition_reasons,
        trace_ref=_trace(judgment_ref),
        provenance_refs=(
            *context.provenance_refs,
            source_snapshot_ref,
            current_world_ref,
            *attention_refs,
        ),
        prior_information_gap_ref=prior_information_gap_ref,
        prior_reobservation_ref=prior_reobservation_ref,
    )


def _validation(
    context: ASemanticDecisionContextV1,
    decision_kind: str,
    required_authority_ref: str,
    *,
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> ASemanticDecisionValidationCandidateV1:
    scope_ok = bool(
        grant
        and grant.receiver_role == ROLE_A
        and grant.concern_ref == context.concern_ref
        and grant.work_ref == context.work_ref
        and grant.grant_ref == context.a_grant_ref
    )
    state_ok = bool(grant and grant.valid_from_state_ref == context.source_state_version_ref)
    authority_ok = bool(grant and required_authority_ref in grant.granted_authority_refs)
    grant_active = False
    failure_class: Optional[str] = None

    if grant is None:
        failure_class = "AUTHORITY_NOT_GRANTED"
    elif grant.receiver_role != ROLE_A:
        failure_class = "AUTHORITY_NOT_GRANTED"
    elif not authority_ok:
        failure_class = "AUTHORITY_NOT_GRANTED"
    elif not scope_ok:
        failure_class = "SCOPE_MISMATCH"
    elif not state_ok:
        failure_class = "STALE_STATE_VERSION"
    elif revoked:
        failure_class = "GRANT_REVOKED"
    elif expired:
        failure_class = "GRANT_EXPIRED"
    elif binding is None:
        failure_class = "RESPONSIBILITY_BINDING_INVALID"
    else:
        status = build_grant_status(
            grant,
            checked_state_version_ref=context.source_state_version_ref,
            revoked=revoked,
            expired=expired,
            binding=binding,
        )
        grant_active = status.valid
        if not status.valid:
            if status.status == "REVOKED":
                failure_class = "GRANT_REVOKED"
            elif status.status == "EXPIRED":
                failure_class = "GRANT_EXPIRED"
            elif status.status == "STALE":
                failure_class = "STALE_STATE_VERSION"
            elif "authority" in " ".join(status.reason_refs):
                failure_class = "CAPABILITY_BOUNDARY_VIOLATION"
            elif "responsibility" in " ".join(status.reason_refs):
                failure_class = "RESPONSIBILITY_BINDING_INVALID"
            else:
                failure_class = "AUTHORITY_NOT_GRANTED"

    return ASemanticDecisionValidationCandidateV1(
        validation_ref=f"validation:{decision_kind}:{context.work_ref}:{context.source_state_version_ref}",
        decision_kind=decision_kind,
        grant_ref=grant.grant_ref if grant else context.a_grant_ref,
        required_authority_ref=required_authority_ref,
        concern_ref=context.concern_ref,
        work_ref=context.work_ref,
        source_state_version_ref=context.source_state_version_ref,
        accepted=failure_class is None,
        failure_class=failure_class,
        grant_active=grant_active,
        scope_ok=scope_ok,
        state_version_ok=state_ok,
        authority_ok=authority_ok,
        decision_owner_ref=DECISION_OWNER,
        trace_ref=_trace(f"validation:{decision_kind}:{context.work_ref}"),
        provenance_refs=_provenance(f"validation:{decision_kind}:{context.work_ref}"),
    )


def build_need_decision(
    context: ASemanticDecisionContextV1,
    *,
    selected_need_ref: Optional[str],
    alternative_need_refs: Tuple[str, ...],
    selection_reason_refs: Tuple[str, ...],
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[ACurrentNeedDecisionCandidateV1, ASemanticDecisionValidationCandidateV1]:
    validation = _validation(
        context,
        "NEED",
        REQUIRED_AUTHORITIES["NEED"],
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    decision = ACurrentNeedDecisionCandidateV1(
        decision_ref=f"a-need:{context.work_ref}:{context.source_state_version_ref}",
        work_ref=context.work_ref,
        concern_ref=context.concern_ref,
        source_state_version_ref=context.source_state_version_ref,
        selected_need_ref=selected_need_ref,
        alternative_need_refs=alternative_need_refs,
        selection_reason_refs=selection_reason_refs,
        evidence_basis_refs=context.evidence_refs,
        hypothesis_basis_refs=context.prior_hypothesis_refs,
        grant_ref=context.a_grant_ref,
    )
    return decision, validation


def build_sufficiency_decision(
    context: ASemanticDecisionContextV1,
    *,
    sufficiency_status: str,
    sufficiency_reason_refs: Tuple[str, ...],
    current_need_ref: Optional[str],
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[ALocalSufficiencyDecisionCandidateV1, ASemanticDecisionValidationCandidateV1]:
    validation = _validation(
        context,
        "SUFFICIENCY",
        REQUIRED_AUTHORITIES["SUFFICIENCY"],
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    if sufficiency_status not in SUFFICIENCY_STATUSES and validation.accepted:
        validation = ASemanticDecisionValidationCandidateV1(
            **{
                **validation.__dict__,
                "accepted": False,
                "failure_class": "INVALID_DECISION_VALUE",
            }
        )
    decision = ALocalSufficiencyDecisionCandidateV1(
        decision_ref=f"a-sufficiency:{context.work_ref}:{context.source_state_version_ref}",
        work_ref=context.work_ref,
        concern_ref=context.concern_ref,
        source_state_version_ref=context.source_state_version_ref,
        sufficiency_status=sufficiency_status,
        sufficiency_reason_refs=sufficiency_reason_refs,
        evidence_basis_refs=context.evidence_refs,
        current_need_ref=current_need_ref,
        grant_ref=context.a_grant_ref,
    )
    return decision, validation


def build_reconsideration_decision(
    context: ASemanticDecisionContextV1,
    *,
    reconsideration_required: bool,
    reconsideration_reason_refs: Tuple[str, ...],
    invalidated_hypothesis_refs: Tuple[str, ...],
    stale_requirement_refs: Tuple[str, ...],
    replacement_need_ref: Optional[str],
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[AReconsiderationDecisionCandidateV1, ASemanticDecisionValidationCandidateV1]:
    validation = _validation(
        context,
        "RECONSIDERATION",
        REQUIRED_AUTHORITIES["RECONSIDERATION"],
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    decision = AReconsiderationDecisionCandidateV1(
        decision_ref=f"a-reconsideration:{context.work_ref}:{context.source_state_version_ref}",
        work_ref=context.work_ref,
        concern_ref=context.concern_ref,
        source_state_version_ref=context.source_state_version_ref,
        reconsideration_required=reconsideration_required,
        reconsideration_reason_refs=reconsideration_reason_refs,
        invalidated_hypothesis_refs=invalidated_hypothesis_refs,
        stale_requirement_refs=stale_requirement_refs,
        replacement_need_ref=replacement_need_ref,
        grant_ref=context.a_grant_ref,
    )
    return decision, validation


def build_next_step_decision(
    context: ASemanticDecisionContextV1,
    *,
    source_need_decision_ref: str,
    source_sufficiency_decision_ref: str,
    source_reconsideration_decision_ref: str,
    next_step_disposition: str,
    selected_next_need_ref: Optional[str],
    reason_refs: Tuple[str, ...],
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[ANextStepDecisionCandidateV1, ASemanticDecisionValidationCandidateV1]:
    validation = _validation(
        context,
        "NEXT_STEP",
        REQUIRED_AUTHORITIES["NEXT_STEP"],
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    if next_step_disposition not in NEXT_STEP_DISPOSITIONS and validation.accepted:
        validation = ASemanticDecisionValidationCandidateV1(
            **{
                **validation.__dict__,
                "accepted": False,
                "failure_class": "INVALID_DECISION_VALUE",
            }
        )
    decision = ANextStepDecisionCandidateV1(
        decision_ref=f"a-next-step:{context.work_ref}:{context.source_state_version_ref}",
        source_need_decision_ref=source_need_decision_ref,
        source_sufficiency_decision_ref=source_sufficiency_decision_ref,
        source_reconsideration_decision_ref=source_reconsideration_decision_ref,
        next_step_disposition=next_step_disposition,
        selected_next_need_ref=selected_next_need_ref,
        reason_refs=reason_refs,
        grant_ref=context.a_grant_ref,
    )
    return decision, validation


def wrap_dynamic_flow_output(
    context: ASemanticDecisionContextV1,
    output: DynamicCognitiveLoopOutputV1,
    *,
    grant: Optional[CognitiveAuthorityGrantCandidateV1],
    binding: Optional[AuthorityResponsibilityBindingCandidateV1],
    revoked: bool = False,
    expired: bool = False,
) -> ASemanticDecisionBundleV1:
    """Treat existing Dynamic Flow output as computational source only."""
    sufficiency_candidate = output.sufficiency_candidates[-1] if output.sufficiency_candidates else None
    if sufficiency_candidate is None:
        sufficiency_status = "INSUFFICIENT"
        sufficiency_reasons = ("compatibility_output_without_sufficiency_candidate",)
    elif sufficiency_candidate.status == "SUFFICIENT":
        sufficiency_status = "SUFFICIENT"
        sufficiency_reasons = (sufficiency_candidate.reason,)
    elif output.reconsiderations or output.final_disposition == "RECONSIDER":
        sufficiency_status = "REQUIRES_RECONSIDERATION"
        sufficiency_reasons = (sufficiency_candidate.reason, "dynamic_output_reconsideration")
    else:
        sufficiency_status = "INSUFFICIENT"
        sufficiency_reasons = (sufficiency_candidate.reason,)

    need, need_validation = build_need_decision(
        context,
        selected_need_ref=output.current_minimum_need_ref,
        alternative_need_refs=output.non_materialized_plan_refs,
        selection_reason_refs=("compatibility_dynamic_output_current_need",),
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    sufficiency, sufficiency_validation = build_sufficiency_decision(
        context,
        sufficiency_status=sufficiency_status,
        sufficiency_reason_refs=sufficiency_reasons,
        current_need_ref=output.current_minimum_need_ref,
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    reconsideration, reconsideration_validation = build_reconsideration_decision(
        context,
        reconsideration_required=bool(output.reconsiderations),
        reconsideration_reason_refs=(
            tuple(item.reconsideration_reason for item in output.reconsiderations)
            or ("no_reconsideration_from_compatibility_output",)
        ),
        invalidated_hypothesis_refs=tuple(
            ref
            for state in output.state_versions
            for ref in state.invalidated_hypothesis_refs
        ),
        stale_requirement_refs=output.stale_requirement_refs,
        replacement_need_ref=output.current_minimum_need_ref if output.reconsiderations else None,
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    next_step, next_step_validation = build_next_step_decision(
        context,
        source_need_decision_ref=need.decision_ref,
        source_sufficiency_decision_ref=sufficiency.decision_ref,
        source_reconsideration_decision_ref=reconsideration.decision_ref,
        next_step_disposition=output.next_step_disposition,
        selected_next_need_ref=output.current_minimum_need_ref,
        reason_refs=(f"compatibility_dynamic_output:{output.scenario_id}",),
        grant=grant,
        binding=binding,
        revoked=revoked,
        expired=expired,
    )
    return ASemanticDecisionBundleV1(
        context=context,
        need_decision=need,
        sufficiency_decision=sufficiency,
        reconsideration_decision=reconsideration,
        next_step_decision=next_step,
        validations=(need_validation, sufficiency_validation, reconsideration_validation, next_step_validation),
        compatibility_source_owner_ref=COMPATIBILITY_SOURCE_OWNER,
        compatibility_wrapper_only=True,
    )


__all__ = [
    "form_cognitive_semantic_judgment",
    "validate_a_semantic_judgment_input",
    "validate_a_semantic_judgment_projection",
    "build_need_decision",
    "build_next_step_decision",
    "build_reconsideration_decision",
    "build_sufficiency_decision",
    "wrap_dynamic_flow_output",
]
