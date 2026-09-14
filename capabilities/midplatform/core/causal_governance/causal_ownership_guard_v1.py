"""Ownership and boundary guards for Causal Governance."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.causal_governance.causal_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.causal_governance.causal_handoff_types_v1 import (
    CausalToDecisionHandoffCandidateV1,
)
from capabilities.midplatform.core.causal_governance.causal_registry_v1 import (
    CAUSAL_OWNER,
    DECISION_CONSUMER_OWNER,
    FORBIDDEN_AUTHORITY_TOKENS,
    LEGACY_CAUSAL_ALIAS,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CAUSAL_OWNER


def validate_legacy_alias_no_authority(owner: str) -> bool:
    return owner != LEGACY_CAUSAL_ALIAS


def validate_ref_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        item.read_only is True
        and item.reference_only is True
        and item.source_mutation_allowed is False
        for item in refs
    )


def validate_forbidden_authority_tokens(refs: Iterable[SourceRefV1]) -> bool:
    tokens = " ".join(f"{ref.owner} {ref.ref_type}" for ref in refs)
    return not any(token in tokens for token in FORBIDDEN_AUTHORITY_TOKENS)


def validate_candidate_only_handoff(
    handoff: CausalToDecisionHandoffCandidateV1,
) -> bool:
    return (
        handoff.producer_owner == CAUSAL_OWNER
        and handoff.consumer_owner == DECISION_CONSUMER_OWNER
        and handoff.candidate_only is True
        and handoff.decision_executed is False
        and handoff.action_triggered is False
        and handoff.task_created is False
    )
