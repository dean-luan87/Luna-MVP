"""Mechanical command/state bridging for the A semantic decision seam."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_engine_v1 import (
    apply_mechanical_command,
    validate_mechanical_command,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    LoopMechanicalReturnCandidateV1,
    LoopMechanicalStateCandidateV1,
    MechanicalCommandCandidateV1,
    MechanicalCommandValidationCandidateV1,
)

from .a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionBundleV1,
    ASemanticDecisionContextV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


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


__all__ = ["bridge_bundle_to_loop"]
