"""Mechanical projection from current Action admission into Runtime handoff.

This module owns sequencing/transport only.  Action Governance remains the
source of admitted-action authority and Runtime/Permission Governance remains
the source of runtime authorization authority.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Optional, Tuple

from capabilities.midplatform.core.action_governance.action_admission_governance_v1 import (
    query_current_admitted_action_v1,
)
from capabilities.midplatform.core.action_governance.action_handoff_types_v1 import (
    ActionToRuntimeExecutorHandoffCandidateV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_target_preparation_v1 import (
    ProviderRuntimeTargetPreparationCandidateV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
)


def project_current_admitted_action_to_runtime_handoff_v1(
    admitted_action_ref: str,
    *,
    profile_ref: Optional[str] = None,
) -> Optional[ActionToRuntimeExecutorHandoffCandidateV1]:
    """Project one owner-current Action admission without creating authority."""

    record = query_current_admitted_action_v1(
        admitted_action_ref,
        profile_ref=profile_ref,
    )
    if record is None:
        return None

    candidate = record.action_candidate
    return ActionToRuntimeExecutorHandoffCandidateV1(
        handoff_id=f"runtime-handoff:admitted-action:{record.admitted_action_ref}",
        producer_owner="Action Governance",
        consumer_owner="Runtime Executor",
        handoff_kind="ACTION_TO_RUNTIME_EXECUTOR_CANDIDATE_HANDOFF",
        action_candidate_ref=record.action_candidate_ref,
        target_refs=tuple(ref.ref_id for ref in candidate.target_refs),
        precondition_refs=candidate.precondition_refs,
        dependency_refs=candidate.dependency_refs,
        permission_refs=tuple(ref.ref_id for ref in candidate.permission_refs),
        safety_refs=tuple(ref.ref_id for ref in candidate.safety_refs),
        confirmation_state=(
            candidate.confirmation_refs[0].ref_id
            if candidate.confirmation_refs
            else "UNSPECIFIED"
        ),
        resource_refs=tuple(ref.ref_id for ref in candidate.resource_refs),
        reversibility=candidate.reversibility,
        rollback_context_ref="",
        provenance=tuple(
            dict.fromkeys(
                (
                    *record.provenance_refs,
                    f"admitted-action:{record.admitted_action_ref}",
                    f"working-envelope:{record.working_envelope_ref}:{record.working_envelope_version_ref}",
                    "projection:action-admission-to-runtime:v1",
                )
            )
        ),
        execution_readiness=candidate.execution_readiness,
        candidate_only=True,
        action_executed=False,
        scheduler_executed=False,
        device_control_executed=False,
        admitted_action_ref=record.admitted_action_ref,
        working_envelope_ref=record.working_envelope_ref,
        working_envelope_version_ref=record.working_envelope_version_ref,
    )


def project_runtime_handoff_to_provider_preparation_request_v1(
    handoff: ActionToRuntimeExecutorHandoffCandidateV1,
    *,
    preparation_ref: str,
    parent_cognitive_problem_ref: str,
    source_state_ref: str,
    provider_target_candidates: Tuple[
        ProviderRuntimeTargetPreparationCandidateV1, ...
    ],
    context_refs: Tuple[str, ...] = (),
    trace_ref: str = "",
    provenance_refs: Tuple[str, ...] = (),
) -> Optional[ProviderBindingRuntimePreparationInputV1]:
    """Project a verified handoff into the first reusable prep input."""

    if not isinstance(handoff, ActionToRuntimeExecutorHandoffCandidateV1):
        return None
    if (
        handoff.candidate_only is not True
        or not handoff.admitted_action_ref
        or not handoff.working_envelope_ref
        or not handoff.working_envelope_version_ref
        or not preparation_ref
        or not parent_cognitive_problem_ref
        or not source_state_ref
        or not isinstance(provider_target_candidates, tuple)
    ):
        return None
    record = query_current_admitted_action_v1(handoff.admitted_action_ref)
    if record is None:
        return None
    if (
        record.admitted_action_ref != handoff.admitted_action_ref
        or record.working_envelope_ref != handoff.working_envelope_ref
        or record.working_envelope_version_ref
        != handoff.working_envelope_version_ref
    ):
        return None
    scoped_candidates = tuple(
        replace(
            candidate,
            admitted_action_ref=record.admitted_action_ref,
            working_envelope_ref=record.working_envelope_ref,
            working_envelope_version_ref=record.working_envelope_version_ref,
        )
        for candidate in provider_target_candidates
    )
    return ProviderBindingRuntimePreparationInputV1(
        preparation_ref=preparation_ref,
        parent_cognitive_problem_ref=parent_cognitive_problem_ref,
        source_state_ref=source_state_ref,
        provider_target_candidates=scoped_candidates,
        context_refs=context_refs,
        trace_ref=trace_ref,
        provenance_refs=provenance_refs,
        candidate_only=True,
        admitted_action_ref=record.admitted_action_ref,
        working_envelope_ref=record.working_envelope_ref,
        working_envelope_version_ref=record.working_envelope_version_ref,
    )


__all__ = [
    "project_current_admitted_action_to_runtime_handoff_v1",
    "project_runtime_handoff_to_provider_preparation_request_v1",
]
