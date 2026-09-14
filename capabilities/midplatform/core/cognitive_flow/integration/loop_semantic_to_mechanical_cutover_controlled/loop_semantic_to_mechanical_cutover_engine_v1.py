"""Controlled semantic-to-mechanical cutover adapter.

This module intentionally does not infer semantic values.  It validates
supplied A/Brain decisions and delegates only mechanical command application
to the existing authority/mechanical-command engine.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_engine_v1 import (
    apply_mechanical_command,
    build_grant_status,
    validate_mechanical_command,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_registry_v1 import (
    A_AUTHORITIES,
    LOOP_AUTHORITIES,
    ROLE_A,
    ROLE_BRAIN,
    ROLE_LOOP,
)
from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_types_v1 import (
    AuthorityResponsibilityBindingCandidateV1,
    CognitiveAuthorityGrantCandidateV1,
    LoopMechanicalReturnCandidateV1,
    LoopMechanicalStateCandidateV1,
    MechanicalCommandCandidateV1,
)

from .loop_semantic_to_mechanical_cutover_registry_v1 import (
    CLOSURE_DISPOSITIONS,
    CLOSURE_SOURCE_OWNERS,
    CLOSURE_TO_COMMANDS,
    LOCAL_DISPOSITIONS,
    LOCAL_TO_COMMANDS,
    NEGATIVE_GUARDS,
    REQUIRED_A_AUTHORITIES,
    RESUME_DISPOSITIONS,
    RESUME_TO_COMMANDS,
)
from .loop_semantic_to_mechanical_cutover_types_v1 import (
    CutoverCommandResultV1,
    LoopClosureMechanicalInputV1,
    LoopLocalDispositionRecordV1,
    LoopResumeMechanicalInputV1,
)


def _trace(ref: str) -> str:
    return f"trace:{ref}"


def _provenance(ref: str) -> Tuple[str, ...]:
    return (f"provenance:{ref}",)


def _grant(
    grant_ref: str,
    receiver_ref: str,
    receiver_role: str,
    *,
    authorities: Iterable[str],
    concern_ref: str,
    work_ref: str,
    state_ref: str,
    issuer_ref: str,
    resource_ref: str = "resource:bounded",
    permission_ref: str = "permission:bounded",
) -> CognitiveAuthorityGrantCandidateV1:
    return CognitiveAuthorityGrantCandidateV1(
        grant_ref=grant_ref,
        issuer_ref=issuer_ref,
        receiver_ref=receiver_ref,
        receiver_role=receiver_role,
        concern_ref=concern_ref,
        work_ref=work_ref,
        granted_authority_refs=tuple(authorities),
        capability_boundary_ref=f"boundary:{receiver_role}",
        goal_refs=(f"goal:{work_ref}",),
        role_refs=(f"role:{work_ref}",),
        field_refs=(f"field:{work_ref}",),
        safety_refs=(f"safety:{work_ref}",),
        permission_refs=(permission_ref,),
        resource_envelope_refs=(resource_ref,),
        valid_from_state_ref=state_ref,
        valid_until_condition_refs=(f"condition:{work_ref}:state-advance",),
        revocation_condition_refs=(f"condition:{work_ref}:stop",),
        result_receiver_ref=f"result:{receiver_ref}",
        responsibility_owner_ref=f"responsibility:{receiver_ref}",
        trace_ref=_trace(grant_ref),
        provenance_refs=_provenance(grant_ref),
    )


def build_a_grant(
    case_id: str,
    *,
    concern_ref: Optional[str] = None,
    work_ref: Optional[str] = None,
    state_ref: str = "state:cutover:v1",
    authorities: Iterable[str] = A_AUTHORITIES,
    receiver_role: str = ROLE_A,
    issuer_ref: str = "brain:governance",
) -> CognitiveAuthorityGrantCandidateV1:
    concern = concern_ref or f"concern:{case_id}"
    work = work_ref or f"work:{case_id}"
    return _grant(
        f"grant:a:{case_id}",
        f"a:{case_id}",
        receiver_role,
        authorities=authorities,
        concern_ref=concern,
        work_ref=work,
        state_ref=state_ref,
        issuer_ref=issuer_ref,
    )


def build_brain_closure_grant(
    case_id: str,
    *,
    concern_ref: str,
    work_ref: str,
    state_ref: str = "state:cutover:v1",
) -> CognitiveAuthorityGrantCandidateV1:
    return _grant(
        f"grant:brain:{case_id}",
        "brain:governance",
        ROLE_BRAIN,
        authorities=("ASSIMILATE_RESULT",),
        concern_ref=concern_ref,
        work_ref=work_ref,
        state_ref=state_ref,
        issuer_ref="brain:governance",
    )


def build_loop_grant(
    case_id: str,
    *,
    concern_ref: str,
    work_ref: str,
    state_ref: str = "state:cutover:v1",
) -> CognitiveAuthorityGrantCandidateV1:
    return _grant(
        f"grant:loop:{case_id}",
        f"loop:{case_id}",
        ROLE_LOOP,
        authorities=LOOP_AUTHORITIES,
        concern_ref=concern_ref,
        work_ref=work_ref,
        state_ref=state_ref,
        issuer_ref="brain:governance",
    )


def build_binding(ref: str, authority_ref: str, *, valid: bool = True) -> AuthorityResponsibilityBindingCandidateV1:
    return AuthorityResponsibilityBindingCandidateV1(
        binding_ref=f"binding:{ref}",
        authority_ref=authority_ref,
        decision_authority_ref=f"decision:{authority_ref}" if authority_ref else "",
        responsibility_owner_ref=f"responsibility:{ref}" if valid else "",
        result_receiver_ref=f"result:{ref}" if valid else "",
        error_owner_ref=f"error:{ref}" if valid else "",
        expiry_ref=f"expiry:{ref}" if valid else "",
        revocation_authority_ref=f"revoke:{ref}" if valid else "",
        valid=valid,
        reason_refs=("binding:explicit",) if valid else ("binding:invalid",),
        trace_ref=_trace(f"binding:{ref}"),
        provenance_refs=_provenance(f"binding:{ref}"),
    )


def build_loop_state(
    case_id: str,
    *,
    concern_ref: Optional[str] = None,
    work_ref: Optional[str] = None,
    state_ref: str = "state:cutover:v1",
) -> LoopMechanicalStateCandidateV1:
    concern = concern_ref or f"concern:{case_id}"
    work = work_ref or f"work:{case_id}"
    return LoopMechanicalStateCandidateV1(
        loop_ref=f"loop:{case_id}",
        concern_ref=concern,
        work_ref=work,
        current_mechanical_state="ACTIVE",
        state_version_ref=state_ref,
        trace_refs=(_trace(f"loop:{case_id}"),),
        provenance_refs=_provenance(f"loop:{case_id}"),
    )


def _semantic_grant_status(
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    required_authority: Optional[str],
    owner_role: str,
    checked_state_ref: str,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[bool, Tuple[str, ...]]:
    binding_authority = required_authority or (grant.granted_authority_refs[0] if grant.granted_authority_refs else "semantic:closure")
    binding = build_binding(grant.grant_ref, binding_authority)
    status = build_grant_status(
        grant,
        checked_state_version_ref=checked_state_ref,
        revoked=revoked,
        expired=expired,
        binding=binding,
    )
    reasons = list(status.reason_refs)
    if grant.receiver_role != owner_role:
        reasons.append("issuer_role_mismatch")
    if required_authority and required_authority not in grant.granted_authority_refs:
        reasons.append("required_semantic_authority_missing")
    if owner_role == ROLE_BRAIN and "ASSIMILATE_RESULT" not in grant.granted_authority_refs:
        reasons.append("brain_adjudication_authority_missing")
    return status.valid and grant.receiver_role == owner_role and not (
        required_authority and required_authority not in grant.granted_authority_refs
    ) and not (owner_role == ROLE_BRAIN and "ASSIMILATE_RESULT" not in grant.granted_authority_refs), tuple(reasons)


def _command(
    case_id: str,
    kind: str,
    issuer_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    *,
    target_refs: Tuple[str, ...] = (),
    reason_refs: Tuple[str, ...] = (),
    source_state_ref: Optional[str] = None,
    concern_ref: Optional[str] = None,
    work_ref: Optional[str] = None,
) -> MechanicalCommandCandidateV1:
    return MechanicalCommandCandidateV1(
        command_ref=f"command:{case_id}:{kind.lower()}",
        command_kind=kind,
        issuer_ref=issuer_grant.receiver_ref,
        issuer_role=issuer_grant.receiver_role,
        receiver_ref=loop_grant.receiver_ref,
        grant_ref=issuer_grant.grant_ref,
        loop_grant_ref=loop_grant.grant_ref,
        concern_ref=concern_ref or issuer_grant.concern_ref,
        work_ref=work_ref or issuer_grant.work_ref,
        source_state_version_ref=source_state_ref or issuer_grant.valid_from_state_ref,
        target_refs=target_refs,
        reason_refs=reason_refs,
        trace_ref=_trace(f"command:{case_id}:{kind.lower()}"),
        provenance_refs=_provenance(f"command:{case_id}:{kind.lower()}"),
    )


def _mechanical_commands(
    case_id: str,
    command_kinds: Tuple[str, ...],
    *,
    issuer_grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    state: LoopMechanicalStateCandidateV1,
    target_refs: Tuple[str, ...],
    reason_refs: Tuple[str, ...],
    revoked: bool = False,
    expired: bool = False,
) -> CutoverCommandResultV1:
    commands = tuple(
        _command(
            f"{case_id}:{index}",
            kind,
            issuer_grant,
            loop_grant,
            target_refs=(
                target_refs[-1:]
                if kind in {"RECORD_NEED_REF", "RECORD_PENDING_CANDIDATE"} and len(target_refs) > 1
                else target_refs[1:2]
                if kind == "FREEZE_FINAL_STATE" and len(target_refs) > 1
                else target_refs[2:3]
                if kind == "ARCHIVE_HISTORY_BOUNDARY" and len(target_refs) > 2
                else target_refs
            ),
            reason_refs=reason_refs,
        )
        for index, kind in enumerate(command_kinds, 1)
    )
    issuer_binding = build_binding(issuer_grant.grant_ref, "supplied:semantic-decision")
    loop_binding = build_binding(loop_grant.grant_ref, "mechanical:persistence")
    validations = tuple(
        validate_mechanical_command(
            command,
            issuer_grant=issuer_grant,
            loop_grant=loop_grant,
            issuer_binding=issuer_binding,
            loop_binding=loop_binding,
            current_state_version_ref=state.state_version_ref,
            revoked_grant_refs=(issuer_grant.grant_ref,) if revoked else (),
            expired_grant_refs=(issuer_grant.grant_ref,) if expired else (),
        )
        for command in commands
    )
    next_state = state
    for command, validation in zip(commands, validations):
        next_state, _ = apply_mechanical_command(next_state, command, validation)
    failures = tuple(item.failure_class for item in validations if item.failure_class)
    return CutoverCommandResultV1(
        source_ref=f"cutover:{case_id}",
        supplied_semantic_kind="SUPPLIED",
        command_refs=tuple(command.command_ref for command in commands),
        command_kinds=command_kinds,
        accepted=bool(validations) and all(item.accepted for item in validations),
        semantic_authority_supplied=True,
        mechanical_only=True,
        validation_failure_refs=failures,
        state_version_ref=next_state.state_version_ref,
        trace_refs=tuple(command.trace_ref for command in commands),
        provenance_refs=tuple(ref for command in commands for ref in command.provenance_refs),
    )


def validate_resume_input(
    value: LoopResumeMechanicalInputV1,
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[bool, Tuple[str, ...]]:
    valid, reasons = _semantic_grant_status(
        grant,
        required_authority=REQUIRED_A_AUTHORITIES["RESUME"],
        owner_role=ROLE_A,
        checked_state_ref=value.source_state_version_ref,
        revoked=revoked,
        expired=expired,
    )
    extra = list(reasons)
    if value.issuing_owner_ref != ROLE_A:
        valid = False
        extra.append("resume_issuer_not_a")
    if value.grant_ref != grant.grant_ref:
        valid = False
        extra.append("grant_ref_mismatch")
    if value.concern_ref != grant.concern_ref or value.work_ref != grant.work_ref:
        valid = False
        extra.append("scope_mismatch")
    if value.source_state_version_ref != grant.valid_from_state_ref:
        valid = False
        extra.append("stale_state_version")
    if value.supplied_resume_disposition not in RESUME_DISPOSITIONS:
        valid = False
        extra.append("unsupported_resume_disposition")
    return valid and value.candidate_only and value.synthetic_only, tuple(extra)


def build_resume_mechanical_cutover(
    value: LoopResumeMechanicalInputV1,
    grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    state: LoopMechanicalStateCandidateV1,
    *,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[CutoverCommandResultV1, Tuple[str, ...]]:
    valid, reasons = validate_resume_input(value, grant, revoked=revoked, expired=expired)
    if not valid:
        return (
            CutoverCommandResultV1(
                source_ref=value.supplied_resume_decision_ref,
                supplied_semantic_kind=value.supplied_resume_disposition,
                command_refs=(),
                command_kinds=(),
                accepted=False,
                semantic_authority_supplied=True,
                mechanical_only=True,
                validation_failure_refs=reasons,
                state_version_ref=state.state_version_ref,
                trace_refs=value.trace_refs,
                provenance_refs=value.provenance_refs,
            ),
            reasons,
        )
    targets = {
        "KEEP": (value.target_state_version_ref,),
        "REPLAN": (value.target_state_version_ref, f"need:{value.loop_ref}:replacement"),
        "SUPERSEDE": (f"requirement:{value.loop_ref}:prior",),
        "COMPLETE": (f"final-state:{value.loop_ref}",),
        "WAITING": (),
    }[value.supplied_resume_disposition]
    reasons_for_command = value.reason_refs or (value.supplied_resume_decision_ref,)
    result = _mechanical_commands(
        value.loop_ref,
        RESUME_TO_COMMANDS[value.supplied_resume_disposition],
        issuer_grant=grant,
        loop_grant=loop_grant,
        state=state,
        target_refs=targets,
        reason_refs=reasons_for_command,
        revoked=revoked,
        expired=expired,
    )
    return result, reasons


def build_local_disposition_record(
    value: LoopLocalDispositionRecordV1,
    grant: Optional[CognitiveAuthorityGrantCandidateV1] = None,
) -> Tuple[bool, Tuple[str, ...]]:
    if value.compatibility_source_only:
        return (
            value.candidate_only and value.synthetic_only and value.supplied_local_disposition in LOCAL_DISPOSITIONS,
            () if value.supplied_local_disposition in LOCAL_DISPOSITIONS else ("unsupported_local_disposition",),
        )
    if grant is None:
        return False, ("grant_missing",)
    valid, reasons = _semantic_grant_status(
        grant,
        required_authority=REQUIRED_A_AUTHORITIES["LOCAL_DISPOSITION"],
        owner_role=ROLE_A,
        checked_state_ref=value.source_state_version_ref,
    )
    extra = list(reasons)
    if value.source_owner_ref != ROLE_A:
        valid = False
        extra.append("local_disposition_owner_not_a")
    if value.loop_ref != f"loop:{value.loop_ref.split(':', 1)[-1]}" and not value.loop_ref:
        valid = False
        extra.append("loop_ref_missing")
    if value.supplied_local_disposition not in LOCAL_DISPOSITIONS:
        valid = False
        extra.append("unsupported_local_disposition")
    return valid and value.candidate_only and value.synthetic_only, tuple(extra)


def build_local_disposition_mechanical_cutover(
    value: LoopLocalDispositionRecordV1,
    grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    state: LoopMechanicalStateCandidateV1,
) -> Tuple[CutoverCommandResultV1, Tuple[str, ...]]:
    valid, reasons = build_local_disposition_record(value, grant)
    if not valid:
        return (
            CutoverCommandResultV1(
                source_ref=value.source_semantic_decision_ref,
                supplied_semantic_kind=value.supplied_local_disposition,
                command_refs=(),
                command_kinds=(),
                accepted=False,
                semantic_authority_supplied=True,
                mechanical_only=True,
                validation_failure_refs=reasons,
                state_version_ref=state.state_version_ref,
                trace_refs=value.trace_refs,
                provenance_refs=value.provenance_refs,
            ),
            reasons,
        )
    command_result = _mechanical_commands(
        value.loop_ref,
        LOCAL_TO_COMMANDS[value.supplied_local_disposition],
        issuer_grant=grant,
        loop_grant=loop_grant,
        state=state,
        target_refs=(value.source_semantic_decision_ref,),
        reason_refs=value.trace_refs,
    )
    return command_result, reasons


def validate_closure_input(
    value: LoopClosureMechanicalInputV1,
    grant: CognitiveAuthorityGrantCandidateV1,
    *,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[bool, Tuple[str, ...]]:
    owner = value.issuing_owner_ref
    required = REQUIRED_A_AUTHORITIES["CLOSURE"] if owner == ROLE_A else None
    valid, reasons = _semantic_grant_status(
        grant,
        required_authority=required,
        owner_role=owner,
        checked_state_ref=value.source_state_version_ref,
        revoked=revoked,
        expired=expired,
    )
    extra = list(reasons)
    if owner not in CLOSURE_SOURCE_OWNERS:
        valid = False
        extra.append("closure_source_owner_not_allowed")
    if value.grant_ref != grant.grant_ref:
        valid = False
        extra.append("grant_ref_mismatch")
    if value.concern_ref != grant.concern_ref or value.work_ref != grant.work_ref:
        valid = False
        extra.append("scope_mismatch")
    if value.source_state_version_ref != grant.valid_from_state_ref:
        valid = False
        extra.append("stale_state_version")
    if not value.supplied_closure_reason_ref:
        valid = False
        extra.append("closure_reason_missing")
    if value.supplied_closure_disposition not in CLOSURE_DISPOSITIONS:
        valid = False
        extra.append("unsupported_closure_disposition")
    return valid and value.candidate_only and value.synthetic_only, tuple(extra)


def build_closure_mechanical_cutover(
    value: LoopClosureMechanicalInputV1,
    grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    state: LoopMechanicalStateCandidateV1,
    *,
    revoked: bool = False,
    expired: bool = False,
) -> Tuple[CutoverCommandResultV1, Tuple[str, ...]]:
    valid, reasons = validate_closure_input(value, grant, revoked=revoked, expired=expired)
    if not valid:
        return (
            CutoverCommandResultV1(
                source_ref=value.closure_request_ref,
                supplied_semantic_kind=value.supplied_closure_disposition,
                command_refs=(),
                command_kinds=(),
                accepted=False,
                semantic_authority_supplied=True,
                mechanical_only=True,
                validation_failure_refs=reasons,
                state_version_ref=state.state_version_ref,
                trace_refs=value.trace_refs,
                provenance_refs=value.provenance_refs,
            ),
            reasons,
        )
    command_result = _mechanical_commands(
        value.loop_ref,
        CLOSURE_TO_COMMANDS[value.supplied_closure_disposition],
        issuer_grant=grant,
        loop_grant=loop_grant,
        state=state,
        target_refs=(value.supplied_closure_reason_ref, f"final-state:{value.loop_ref}", f"history:{value.loop_ref}"),
        reason_refs=(value.closure_request_ref,),
        revoked=revoked,
        expired=expired,
    )
    return command_result, reasons


def build_compatibility_record_set(
    case_id: str,
    *,
    loop_ref: str,
    concern_ref: str,
    work_ref: str,
    state_ref: str,
    resume_disposition: str = "REPLAN",
    local_disposition: str = "RECONSIDER",
    closure_reason: str = "COGNITIVE_CONCERN_RESOLVED",
    closure_disposition: str = "COMPLETED",
) -> Tuple[LoopResumeMechanicalInputV1, LoopLocalDispositionRecordV1, LoopClosureMechanicalInputV1]:
    # These values model legacy helper output only.  They are explicitly not
    # treated as semantic authority at this boundary.
    return (
        LoopResumeMechanicalInputV1(
            loop_ref=loop_ref,
            work_ref=work_ref,
            concern_ref=concern_ref,
            source_state_version_ref=state_ref,
            target_state_version_ref=f"{state_ref}:next",
            supplied_resume_decision_ref=f"legacy-resume:{case_id}",
            supplied_resume_disposition=resume_disposition,
            issuing_owner_ref=ROLE_A,
            grant_ref=f"grant:a:{case_id}",
            reason_refs=(f"legacy-reason:{case_id}",),
            trace_refs=(_trace(f"legacy:{case_id}"),),
            provenance_refs=_provenance(f"legacy:{case_id}"),
            compatibility_source_only=True,
        ),
        LoopLocalDispositionRecordV1(
            loop_ref=loop_ref,
            source_semantic_decision_ref=f"legacy-local:{case_id}",
            supplied_local_disposition=local_disposition,
            source_owner_ref="LEGACY_LOOP_COMPATIBILITY",
            source_state_version_ref=state_ref,
            trace_refs=(_trace(f"legacy-local:{case_id}"),),
            provenance_refs=_provenance(f"legacy-local:{case_id}"),
            compatibility_source_only=True,
        ),
        LoopClosureMechanicalInputV1(
            loop_ref=loop_ref,
            concern_ref=concern_ref,
            work_ref=work_ref,
            source_state_version_ref=state_ref,
            closure_request_ref=f"legacy-closure:{case_id}",
            supplied_closure_reason_ref=closure_reason,
            supplied_closure_disposition=closure_disposition,
            issuing_owner_ref=ROLE_A,
            grant_ref=f"grant:a:{case_id}",
            trace_refs=(_trace(f"legacy-closure:{case_id}"),),
            provenance_refs=_provenance(f"legacy-closure:{case_id}"),
            compatibility_source_only=True,
        ),
    )


def build_forbidden_semantic_command(
    case_id: str,
    *,
    grant: CognitiveAuthorityGrantCandidateV1,
    loop_grant: CognitiveAuthorityGrantCandidateV1,
    state: LoopMechanicalStateCandidateV1,
) -> CutoverCommandResultV1:
    result = _mechanical_commands(
        case_id,
        ("JUDGE_SUFFICIENCY",),
        issuer_grant=grant,
        loop_grant=loop_grant,
        state=state,
        target_refs=("semantic:forbidden",),
        reason_refs=("loop-must-not-judge",),
    )
    return result


def return_is_mechanical_only(value: LoopMechanicalReturnCandidateV1) -> bool:
    return bool(
        value.loop_ref
        and value.state_version_ref
        and value.candidate_only
        and value.synthetic_only
        and not hasattr(value, "sufficiency")
        and not hasattr(value, "selected_need")
        and not hasattr(value, "reconsideration")
    )


def negative_guards() -> Dict[str, bool]:
    return dict(NEGATIVE_GUARDS)


__all__ = [
    "build_a_grant",
    "build_brain_closure_grant",
    "build_loop_grant",
    "build_binding",
    "build_loop_state",
    "validate_resume_input",
    "build_resume_mechanical_cutover",
    "build_local_disposition_record",
    "build_local_disposition_mechanical_cutover",
    "validate_closure_input",
    "build_closure_mechanical_cutover",
    "build_compatibility_record_set",
    "build_forbidden_semantic_command",
    "return_is_mechanical_only",
    "negative_guards",
]
