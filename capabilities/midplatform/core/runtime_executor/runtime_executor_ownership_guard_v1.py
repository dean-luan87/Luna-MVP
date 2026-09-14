"""Ownership and boundary guards for Runtime Executor."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.runtime_executor.runtime_executor_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_handoff_types_v1 import (
    ResultHandoffCandidateV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_registry_v1 import (
    ACTION_GOVERNANCE_OWNER,
    DECISION_GOVERNANCE_OWNER,
    DIAGNOSTICS_OWNER,
    LEGACY_ALIASES,
    RUNTIME_EXECUTOR_OWNER,
    SCHEDULER_OWNER,
    TASK_MANAGER_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == RUNTIME_EXECUTOR_OWNER


def validate_legacy_alias_no_authority(owner: str) -> bool:
    return owner not in LEGACY_ALIASES


def validate_no_parallel_runtime_executor_authority(
    refs: Iterable[SourceRefV1],
) -> bool:
    forbidden = {
        "Runtime Executor Authority 2",
        "Parallel Runtime Executor",
    }
    joined = " ".join(f"{item.owner}:{item.ref_type}" for item in refs)
    return not any(token in joined for token in forbidden)


def validate_source_refs_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.reference_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_forbidden_mutation_ownership(refs: Iterable[SourceRefV1]) -> bool:
    forbidden_owners = {
        "Intent Governance",
        "Causal Governance",
        DECISION_GOVERNANCE_OWNER,
        ACTION_GOVERNANCE_OWNER,
        TASK_MANAGER_OWNER,
        SCHEDULER_OWNER,
        "Permission Governance",
        "Safety Governance",
    }
    return all(ref.owner not in forbidden_owners or ref.reference_only for ref in refs)


def validate_result_handoff_reference_only(handoff: ResultHandoffCandidateV1) -> bool:
    allowed_consumers = {ACTION_GOVERNANCE_OWNER, TASK_MANAGER_OWNER, DIAGNOSTICS_OWNER}
    return (
        handoff.producer_owner == RUNTIME_EXECUTOR_OWNER
        and handoff.consumer_owner in allowed_consumers
        and handoff.handoff_kind == "RUNTIME_EXECUTOR_RESULT_CANDIDATE_HANDOFF"
        and handoff.reference_only is True
        and handoff.owner_mutation is False
    )
