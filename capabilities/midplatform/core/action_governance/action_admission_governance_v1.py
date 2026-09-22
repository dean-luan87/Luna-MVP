"""Action Governance owner boundary for canonical Action Admission."""

from __future__ import annotations

from dataclasses import replace
from itertools import count
from threading import RLock
from typing import Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    _is_owner_formed_action_output_v1,
    query_current_runtime_safety_prerequisite_v1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceOutputV1,
)
from capabilities.midplatform.core.action_governance.action_permission_safety_types_v1 import (
    RuntimeSafetyPrerequisiteDecisionV1,
)
from capabilities.midplatform.core.action_governance.action_static_validators_v1 import (
    validate_action_candidate,
    validate_handoffs,
    validate_no_runtime_side_effects,
    validate_trace_completeness,
)
from capabilities.midplatform.core.action_governance.action_admission_types_v1 import (
    ACTION_ADMISSION_CANCELLED,
    ACTION_ADMISSION_CURRENT,
    ACTION_ADMISSION_OWNER,
    ACTION_ADMISSION_REVOKED,
    ACTION_ADMISSION_SUPERSEDED,
    CanonicalAdmittedActionRecordV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1,
    WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL,
    query_current_working_envelope_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.task_to_action_handoff_types_v1 import (
    TaskToActionHandoffCandidateV1,
)


ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL = (
    "action-admission-profile:production-canonical"
)
ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1 = (
    "action-admission-profile:controlled-evaluation-v1"
)
_PROFILE_TO_ENVELOPE_PROFILE = {
    ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL: (
        WORKING_ENVELOPE_PROFILE_PRODUCTION_CANONICAL
    ),
    ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1: (
        WORKING_ENVELOPE_PROFILE_CONTROLLED_EVALUATION_V1
    ),
}

_LOCK = RLock()
_CURRENT: Dict[str, Dict[str, CanonicalAdmittedActionRecordV1]] = {}
_HISTORY: Dict[str, Dict[str, Tuple[CanonicalAdmittedActionRecordV1, ...]]] = {}
_ACTION_REF_TO_PROFILE: Dict[str, str] = {}
_NEXT_ACTION_NUMBER = {
    profile_ref: count(1) for profile_ref in _PROFILE_TO_ENVELOPE_PROFILE
}


def resolve_action_admission_profile_v1(
    profile_ref: Optional[str] = None,
) -> Optional[str]:
    """Resolve an owner-defined profile; omitted means production."""

    resolved = (
        ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL
        if profile_ref is None
        else profile_ref
    )
    if not isinstance(resolved, str) or not resolved.strip():
        return None
    return resolved if resolved in _PROFILE_TO_ENVELOPE_PROFILE else None


def _refs(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            value for value in values if isinstance(value, str) and value.strip()
        )
    )


def _query_bound_envelope(
    *,
    envelope_ref: str,
    envelope_version_ref: str,
    profile_ref: str,
):
    envelope = query_current_working_envelope_v1(
        envelope_ref,
        profile_ref=_PROFILE_TO_ENVELOPE_PROFILE[profile_ref],
    )
    if envelope is None or envelope.envelope_version_ref != envelope_version_ref:
        return None
    return envelope


def _valid_action_output(action_output: object) -> bool:
    if not isinstance(action_output, ActionGovernanceOutputV1):
        return False
    if not _is_owner_formed_action_output_v1(action_output):
        return False
    if not validate_action_candidate(action_output.action_candidate):
        return False
    if not validate_handoffs(action_output):
        return False
    if not validate_trace_completeness(action_output):
        return False
    if not validate_no_runtime_side_effects(action_output):
        return False
    return (
        action_output.action_candidate.action_state == "READY_CANDIDATE"
        and action_output.action_candidate.execution_readiness == "candidate_ready"
    )


def _validate_task_lineage(
    *,
    action_output: ActionGovernanceOutputV1,
    task_handoff: object,
    envelope_ref: str,
    envelope_version_ref: str,
) -> Optional[Tuple[str, str]]:
    if not isinstance(task_handoff, TaskToActionHandoffCandidateV1):
        return None
    if task_handoff.candidate_only is not True:
        return None
    if task_handoff.working_envelope_ref != envelope_ref:
        return None
    if task_handoff.working_envelope_version_ref != envelope_version_ref:
        return None
    if not task_handoff.decision_candidate_ref or not task_handoff.task_state_ref:
        return None

    decision_refs = {
        ref.ref_id for ref in action_output.action_candidate.source_decision_refs
    }
    target_refs = {ref.ref_id for ref in action_output.action_candidate.target_refs}
    if task_handoff.decision_candidate_ref not in decision_refs:
        return None
    if task_handoff.option_ref not in target_refs:
        return None
    return task_handoff.decision_candidate_ref, task_handoff.task_state_ref


def _validate_safety_prerequisite(
    *,
    action_output: ActionGovernanceOutputV1,
    task_handoff: TaskToActionHandoffCandidateV1,
    envelope_ref: str,
    envelope_version_ref: str,
    safety_prerequisite: object,
) -> Optional[RuntimeSafetyPrerequisiteDecisionV1]:
    if not isinstance(safety_prerequisite, RuntimeSafetyPrerequisiteDecisionV1):
        return None
    expected_prefix = (
        action_output.action_candidate.action_candidate_id,
        task_handoff.task_state_ref,
        task_handoff.decision_candidate_ref,
        envelope_ref,
        envelope_version_ref,
    )
    expected_binding_key = (*expected_prefix, safety_prerequisite.effect_class)
    if safety_prerequisite.binding_key != expected_binding_key:
        return None
    current = query_current_runtime_safety_prerequisite_v1(
        binding_key=expected_binding_key,
        result_ref=safety_prerequisite.result_ref,
    )
    if current is not safety_prerequisite:
        return None
    if (
        current.status != "ALLOWED"
        or current.authoritative is not True
        or current.candidate_only is not False
        or current.revoked is not False
    ):
        return None
    return current


def _store(record: CanonicalAdmittedActionRecordV1) -> None:
    _CURRENT.setdefault(record.profile_ref, {})[record.admitted_action_ref] = record
    _append_history(record)


def _append_history(record: CanonicalAdmittedActionRecordV1) -> None:
    history = _HISTORY.setdefault(record.profile_ref, {})
    history[record.admitted_action_ref] = history.get(record.admitted_action_ref, ()) + (
        record,
    )


def _register_admitted_action_namespace_v1(
    record: CanonicalAdmittedActionRecordV1,
) -> bool:
    """Register an owner-issued Action ref exactly once."""

    admitted_action_ref = record.admitted_action_ref
    if admitted_action_ref in _ACTION_REF_TO_PROFILE:
        return False
    _ACTION_REF_TO_PROFILE[admitted_action_ref] = record.profile_ref
    return True


def admit_action_v1(
    action_output: ActionGovernanceOutputV1,
    *,
    task_handoff: TaskToActionHandoffCandidateV1,
    working_envelope_ref: str,
    working_envelope_version_ref: str,
    safety_prerequisite: RuntimeSafetyPrerequisiteDecisionV1,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    """Admit one owner-formed Action candidate into Action Governance."""

    resolved = resolve_action_admission_profile_v1(profile_ref)
    if resolved is None:
        return None
    if not all(
        isinstance(value, str) and value.strip()
        for value in (working_envelope_ref, working_envelope_version_ref)
    ):
        return None
    if not _valid_action_output(action_output):
        return None
    if not isinstance(task_handoff, TaskToActionHandoffCandidateV1):
        return None
    with _LOCK:
        envelope = _query_bound_envelope(
            envelope_ref=working_envelope_ref,
            envelope_version_ref=working_envelope_version_ref,
            profile_ref=resolved,
        )
        if envelope is None:
            return None
        lineage = _validate_task_lineage(
            action_output=action_output,
            task_handoff=task_handoff,
            envelope_ref=envelope.envelope_ref,
            envelope_version_ref=envelope.envelope_version_ref,
        )
        if lineage is None:
            return None
        safety = _validate_safety_prerequisite(
            action_output=action_output,
            task_handoff=task_handoff,
            envelope_ref=envelope.envelope_ref,
            envelope_version_ref=envelope.envelope_version_ref,
            safety_prerequisite=safety_prerequisite,
        )
        if safety is None:
            return None

        action_number = next(_NEXT_ACTION_NUMBER[resolved])
        admitted_action_ref = f"admitted-action:{resolved.rsplit(':', 1)[-1]}:{action_number}"
        selected_decision_ref, selected_task_ref = lineage
        record = CanonicalAdmittedActionRecordV1(
            admitted_action_ref=admitted_action_ref,
            action_candidate_ref=action_output.action_candidate.action_candidate_id,
            action_candidate=action_output.action_candidate,
            working_envelope_ref=envelope.envelope_ref,
            working_envelope_version_ref=envelope.envelope_version_ref,
            selected_decision_ref=selected_decision_ref,
            selected_task_ref=selected_task_ref,
            safety_prerequisite_ref=safety.result_ref,
            safety_effect_class=safety.effect_class,
            admission_basis_refs=(
                f"current-working-envelope:{envelope.envelope_ref}:{envelope.envelope_version_ref}",
                f"selected-decision:{selected_decision_ref}",
                f"selected-task:{selected_task_ref}",
                f"current-safety-prerequisite:{safety.result_ref}",
            ),
            applicable_policy_refs=("action-admission-policy:v1",),
            provenance_refs=_refs(
                (
                    f"owner:{ACTION_ADMISSION_OWNER}",
                    f"candidate:{action_output.action_candidate.action_candidate_id}",
                    f"envelope:{envelope.envelope_ref}:{envelope.envelope_version_ref}",
                    f"decision:{selected_decision_ref}",
                    f"task:{selected_task_ref}",
                    f"safety:{safety.result_ref}",
                    *tuple(ref.ref_id for ref in action_output.action_candidate.provenance),
                )
            ),
            profile_ref=resolved,
            lifecycle_status=ACTION_ADMISSION_CURRENT,
        )
        if not _register_admitted_action_namespace_v1(record):
            return None
        _store(record)
        return record


def query_current_admitted_action_v1(
    admitted_action_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    """Return a current Action admission only while prerequisites remain current."""

    if not isinstance(admitted_action_ref, str) or not admitted_action_ref.strip():
        return None
    with _LOCK:
        resolved = _ACTION_REF_TO_PROFILE.get(admitted_action_ref)
        if resolved is None:
            return None
        if profile_ref is not None:
            explicit_profile = resolve_action_admission_profile_v1(profile_ref)
            if explicit_profile is None or explicit_profile != resolved:
                return None
        record = _CURRENT.get(resolved, {}).get(admitted_action_ref)
        if record is None or record.lifecycle_status != ACTION_ADMISSION_CURRENT:
            return None
        envelope = _query_bound_envelope(
            envelope_ref=record.working_envelope_ref,
            envelope_version_ref=record.working_envelope_version_ref,
            profile_ref=resolved,
        )
        if envelope is None:
            return None
        safety = query_current_runtime_safety_prerequisite_v1(
            binding_key=(
                record.action_candidate_ref,
                record.selected_task_ref,
                record.selected_decision_ref,
                record.working_envelope_ref,
                record.working_envelope_version_ref,
                record.safety_effect_class,
            ),
            result_ref=record.safety_prerequisite_ref,
        )
        if (
            safety is None
            or safety.status != "ALLOWED"
            or safety.authoritative is not True
            or safety.candidate_only is not False
            or safety.revoked
        ):
            return None
        return record


def query_historical_admitted_action_v1(
    admitted_action_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    """Return the latest immutable historical record without current authority."""

    resolved = resolve_action_admission_profile_v1(profile_ref)
    if resolved is None or not isinstance(admitted_action_ref, str) or not admitted_action_ref.strip():
        return None
    with _LOCK:
        history = _HISTORY.get(resolved, {}).get(admitted_action_ref, ())
        return history[-1] if history else None


def _transition(
    admitted_action_ref: str,
    *,
    next_status: str,
    profile_ref: Optional[str],
    reason_ref: str,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    resolved = resolve_action_admission_profile_v1(profile_ref)
    if resolved is None or not isinstance(reason_ref, str) or not reason_ref.strip():
        return None
    with _LOCK:
        current = _CURRENT.get(resolved, {}).get(admitted_action_ref)
        if current is None or current.lifecycle_status != ACTION_ADMISSION_CURRENT:
            return None
        if next_status == ACTION_ADMISSION_REVOKED:
            transitioned = replace(current, lifecycle_status=next_status, revocation_ref=reason_ref)
        else:
            transitioned = replace(current, lifecycle_status=next_status, cancellation_ref=reason_ref)
        _CURRENT[resolved].pop(admitted_action_ref, None)
        _append_history(transitioned)
        return transitioned


def supersede_admitted_action_v1(
    admitted_action_ref: str,
    *,
    replacement_admitted_action_ref: str,
    reason_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    """Supersede an old record only in favor of an owner-issued current record."""

    resolved = resolve_action_admission_profile_v1(profile_ref)
    if resolved is None or admitted_action_ref == replacement_admitted_action_ref:
        return None
    with _LOCK:
        current = _CURRENT.get(resolved, {}).get(admitted_action_ref)
        replacement = _CURRENT.get(resolved, {}).get(replacement_admitted_action_ref)
        if (
            current is None
            or replacement is None
            or current.lifecycle_status != ACTION_ADMISSION_CURRENT
            or replacement.lifecycle_status != ACTION_ADMISSION_CURRENT
            or not isinstance(reason_ref, str)
            or not reason_ref.strip()
        ):
            return None
        transitioned = replace(
            current,
            lifecycle_status=ACTION_ADMISSION_SUPERSEDED,
            superseded_by_admitted_action_ref=replacement_admitted_action_ref,
            supersession_reason_ref=reason_ref,
        )
        _CURRENT[resolved].pop(admitted_action_ref, None)
        _append_history(transitioned)
        return transitioned


def revoke_admitted_action_v1(
    admitted_action_ref: str,
    *,
    reason_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    return _transition(
        admitted_action_ref,
        next_status=ACTION_ADMISSION_REVOKED,
        profile_ref=profile_ref,
        reason_ref=reason_ref,
    )


def cancel_admitted_action_v1(
    admitted_action_ref: str,
    *,
    reason_ref: str,
    profile_ref: Optional[str] = None,
) -> Optional[CanonicalAdmittedActionRecordV1]:
    return _transition(
        admitted_action_ref,
        next_status=ACTION_ADMISSION_CANCELLED,
        profile_ref=profile_ref,
        reason_ref=reason_ref,
    )


__all__ = [
    "ACTION_ADMISSION_PROFILE_CONTROLLED_EVALUATION_V1",
    "ACTION_ADMISSION_PROFILE_PRODUCTION_CANONICAL",
    "admit_action_v1",
    "cancel_admitted_action_v1",
    "query_current_admitted_action_v1",
    "query_historical_admitted_action_v1",
    "resolve_action_admission_profile_v1",
    "revoke_admitted_action_v1",
    "supersede_admitted_action_v1",
]
