"""Ownership and boundary guards for Decision Governance controlled implementation v1."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.decision_governance.decision_handoff_types_v1 import (
    DecisionToActionTaskHandoffCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_registry_v1 import (
    ACTION_CONSUMER_OWNER,
    DECISION_OWNER,
    LEGACY_ALIASES,
    TASK_CONSUMER_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == DECISION_OWNER


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
        "Decision Authority",
        "Decision Executor",
        "Action Executor",
        "Task Creator",
    )
    return not any(token in joined for token in forbidden)


def validate_candidate_only_handoff(
    handoff: DecisionToActionTaskHandoffCandidateV1,
) -> bool:
    consumers = set(handoff.consumer_owners)
    return (
        handoff.producer_owner == DECISION_OWNER
        and ACTION_CONSUMER_OWNER in consumers
        and TASK_CONSUMER_OWNER in consumers
        and handoff.candidate_only is True
        and handoff.decision_executed is False
        and handoff.action_triggered is False
        and handoff.task_created is False
    )
