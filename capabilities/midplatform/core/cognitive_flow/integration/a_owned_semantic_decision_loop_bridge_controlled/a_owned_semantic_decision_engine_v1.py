"""Candidate-only A semantic decisions and Loop mechanical bridge."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_types_v1 import (
    DynamicCognitiveLoopOutputV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_engine_v1 import (
    apply_mechanical_command,
    build_grant_status,
    validate_mechanical_command,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    ROLE_A,
    ROLE_LOOP,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    LoopMechanicalReturnCandidateV1,
    LoopMechanicalStateCandidateV1,
    MechanicalCommandCandidateV1,
    MechanicalCommandValidationCandidateV1,
)

from .a_owned_semantic_decision_registry_v1 import (
    COMPATIBILITY_SOURCE_OWNER,
    DECISION_OWNER,
    NEXT_STEP_DISPOSITIONS,
    REQUIRED_AUTHORITIES,
    SUFFICIENCY_STATUSES,
)
from .a_owned_semantic_decision_types_v1 import (
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


def _command(
    command_ref: str,
    command_kind: str,
    context: ASemanticDecisionContextV1,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    target_refs: Tuple[str, ...],
    reason_refs: Tuple[str, ...],
) -> MechanicalCommandCandidateV1:
    return MechanicalCommandCandidateV1(
        command_ref=command_ref,
        command_kind=command_kind,
        issuer_ref=a_grant.receiver_ref,
        issuer_role=a_grant.receiver_role,
        receiver_ref=loop_grant.receiver_ref,
        grant_ref=a_grant.grant_ref,
        loop_grant_ref=loop_grant.grant_ref,
        concern_ref=context.concern_ref,
        work_ref=context.work_ref,
        source_state_version_ref=context.source_state_version_ref,
        target_refs=target_refs,
        reason_refs=reason_refs,
        trace_ref=_trace(command_ref),
        provenance_refs=_provenance(command_ref),
    )


def bridge_bundle_to_loop(
    bundle: ASemanticDecisionBundleV1,
    *,
    a_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    a_binding: AuthorityResponsibilityBindingCandidateV1,
    loop_binding: AuthorityResponsibilityBindingCandidateV1,
    state: LoopMechanicalStateCandidateV1,
) -> Tuple[
    Tuple[MechanicalCommandCandidateV1, ...],
    Tuple[MechanicalCommandValidationCandidateV1, ...],
    LoopMechanicalStateCandidateV1,
    LoopMechanicalReturnCandidateV1,
]:
    if not all(validation.accepted for validation in bundle.validations):
        return (), (), state, _return_state(state)

    specs = []
    need = bundle.need_decision
    sufficiency = bundle.sufficiency_decision
    reconsideration = bundle.reconsideration_decision
    next_step = bundle.next_step_decision
    if need and need.selected_need_ref:
        specs.append(("RECORD_NEED_REF", (need.selected_need_ref,), (need.decision_ref,)))
    if sufficiency:
        if sufficiency.sufficiency_status == "SUFFICIENT":
            specs.extend(
                (
                    ("CLOSE", (), (sufficiency.decision_ref,)),
                    ("FREEZE_FINAL_STATE", (sufficiency.source_state_version_ref,), (sufficiency.decision_ref,)),
                )
            )
        else:
            specs.append(("RECORD_PENDING_CANDIDATE", (sufficiency.decision_ref,), sufficiency.sufficiency_reason_refs))
    if reconsideration and reconsideration.reconsideration_required:
        for requirement_ref in reconsideration.stale_requirement_refs:
            specs.append(("SUPERSEDE_REQUIREMENT", (requirement_ref,), reconsideration.reconsideration_reason_refs))
        if reconsideration.replacement_need_ref:
            specs.append(("RECORD_NEED_REF", (reconsideration.replacement_need_ref,), reconsideration.reconsideration_reason_refs))
    if next_step:
        if next_step.next_step_disposition == "CONTINUE":
            specs.append(("RECORD_PENDING_CANDIDATE", (next_step.decision_ref,), next_step.reason_refs))
        elif next_step.next_step_disposition == "REQUEST_MORE_EVIDENCE":
            specs.append(("RECORD_PENDING_CANDIDATE", (next_step.decision_ref,), next_step.reason_refs))
        elif next_step.next_step_disposition == "REPLAN":
            specs.extend(
                (
                    ("RECORD_STATE_VERSION", (bundle.context.source_state_version_ref,), next_step.reason_refs),
                    ("RECORD_NEED_REF", (next_step.selected_next_need_ref,) if next_step.selected_next_need_ref else (), next_step.reason_refs),
                )
            )
        elif next_step.next_step_disposition == "STOP_SUFFICIENT":
            specs.extend(
                (
                    ("CLOSE", (), next_step.reason_refs),
                    ("FREEZE_FINAL_STATE", (bundle.context.source_state_version_ref,), next_step.reason_refs),
                )
            )
        elif next_step.next_step_disposition in {"WAIT", "DEFER"}:
            specs.append(("WAIT", (), next_step.reason_refs))
        elif next_step.next_step_disposition == "PAUSE":
            specs.append(("PAUSE", (), next_step.reason_refs))

    commands = tuple(
        _command(
            f"a-loop-command:{bundle.context.work_ref}:{index}",
            kind,
            bundle.context,
            a_grant,
            loop_grant,
            targets,
            reasons,
        )
        for index, (kind, targets, reasons) in enumerate(specs, start=1)
    )
    validations = tuple(
        validate_mechanical_command(
            command,
            issuer_grant=a_grant,
            loop_grant=loop_grant,
            issuer_binding=a_binding,
            loop_binding=loop_binding,
            current_state_version_ref=state.state_version_ref,
        )
        for command in commands
    )
    next_state = state
    returned = _return_state(state)
    for command, validation in zip(commands, validations):
        next_state, returned = apply_mechanical_command(next_state, command, validation)
    return commands, validations, next_state, returned


def _return_state(state: LoopMechanicalStateCandidateV1) -> LoopMechanicalReturnCandidateV1:
    return LoopMechanicalReturnCandidateV1(
        loop_ref=state.loop_ref,
        current_mechanical_state=state.current_mechanical_state,
        state_version_ref=state.state_version_ref,
        pending_refs=state.pending_refs,
        pause_reason_ref=state.pause_reason_ref,
        wait_reason_ref=state.wait_reason_ref,
        requirement_refs=state.requirement_refs,
        b_branch_refs=state.b_branch_refs,
        closure_state=state.closure_state,
        final_freeze_ref=state.final_freeze_ref,
        history_boundary_ref=state.history_boundary_ref,
        trace_refs=state.trace_refs,
        provenance_refs=state.provenance_refs,
    )


__all__ = [
    "bridge_bundle_to_loop",
    "build_need_decision",
    "build_next_step_decision",
    "build_reconsideration_decision",
    "build_sufficiency_decision",
    "wrap_dynamic_flow_output",
]
