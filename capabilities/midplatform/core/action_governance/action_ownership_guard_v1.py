"""Ownership and boundary guards for Action Governance controlled implementation v1."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_handoff_types_v1 import (
    ActionToRuntimeExecutorHandoffCandidateV1,
    ActionToTaskManagerHandoffCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_registry_v1 import (
    ACTION_OWNER,
    LEGACY_ALIASES,
    RUNTIME_EXECUTOR_OWNER,
    TASK_MANAGER_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == ACTION_OWNER


def validate_legacy_alias_no_authority(owner: str) -> bool:
    return owner not in LEGACY_ALIASES


def validate_ref_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.reference_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_no_parallel_owner_token(refs: Iterable[SourceRefV1]) -> bool:
    joined = " ".join(f"{ref.owner} {ref.ref_type}" for ref in refs)
    forbidden = (
        "Action Runtime Authority",
        "Action Task Creator",
        "Action Scheduler",
        "Action Executor Authority",
    )
    return not any(token in joined for token in forbidden)


def validate_runtime_handoff_candidate_only(
    handoff: ActionToRuntimeExecutorHandoffCandidateV1,
) -> bool:
    return (
        handoff.producer_owner == ACTION_OWNER
        and handoff.consumer_owner == RUNTIME_EXECUTOR_OWNER
        and handoff.handoff_kind == "ACTION_TO_RUNTIME_EXECUTOR_CANDIDATE_HANDOFF"
        and handoff.candidate_only is True
        and handoff.action_executed is False
        and handoff.scheduler_executed is False
        and handoff.device_control_executed is False
    )


def validate_task_handoff_reference_only(
    handoff: ActionToTaskManagerHandoffCandidateV1,
) -> bool:
    return (
        handoff.producer_owner == ACTION_OWNER
        and handoff.consumer_owner == TASK_MANAGER_OWNER
        and handoff.handoff_kind == "ACTION_TO_TASK_MANAGER_REFERENCE_HANDOFF"
        and handoff.reference_only is True
        and handoff.task_created is False
    )
