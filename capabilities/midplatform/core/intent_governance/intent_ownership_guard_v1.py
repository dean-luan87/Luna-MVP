"""Ownership and boundary guards for Intent Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import fields
from typing import Iterable, Tuple

from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    IntentCandidateV1,
    PotentialIntentCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_handoff_types_v1 import (
    IntentToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_registry_v1 import (
    INTENT_OWNER,
)


FORBIDDEN_OWNER_TOKENS: Tuple[str, ...] = (
    "Causal Governance",
    "Decision",
    "Action",
    "Task",
    "Runtime",
)


def validate_ref_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.reference_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_intent_owner(owner: str) -> bool:
    return owner == INTENT_OWNER


def validate_forbidden_owner_tokens(refs: Iterable[SourceRefV1]) -> bool:
    joined = " ".join(f"{ref.owner} {ref.ref_type}" for ref in refs)
    return not any(token in joined for token in FORBIDDEN_OWNER_TOKENS)


def validate_potential_candidate_boundary(
    candidate: PotentialIntentCandidateV1,
) -> bool:
    return (
        candidate.candidate_only is True
        and validate_intent_owner(candidate.owner)
        and candidate.candidate_kind == "POTENTIAL_INTENT_CANDIDATE"
        and bool(candidate.source_refs)
        and bool(candidate.context_refs)
        and bool(candidate.why_candidate)
        and bool(candidate.provenance)
        and bool(candidate.formation_trace)
    )


def validate_intent_candidate_boundary(candidate: IntentCandidateV1) -> bool:
    field_names = {item.name for item in fields(candidate)}
    forbidden = {"decision_output", "action_output", "task_output", "causal_output"}
    return (
        candidate.candidate_only is True
        and candidate.reference_only is True
        and validate_intent_owner(candidate.owner)
        and candidate.candidate_kind == "INTENT_CANDIDATE"
        and bool(candidate.source_refs)
        and bool(candidate.context_refs)
        and bool(candidate.provenance)
        and bool(candidate.formation_trace)
        and forbidden <= field_names
        and candidate.decision_output is False
        and candidate.action_output is False
        and candidate.task_output is False
        and candidate.causal_output is False
        and candidate.runtime_executed is False
        and candidate.source_mutation_executed is False
    )


def validate_handoff_boundary(handoff: IntentToCausalHandoffCandidateV1) -> bool:
    return (
        handoff.candidate_only is True
        and handoff.producer_owner == INTENT_OWNER
        and bool(handoff.consumer_owner)
        and bool(handoff.intent_candidate_refs or handoff.potential_intent_refs)
        and bool(handoff.provenance)
        and handoff.causal_explanation is False
        and handoff.decision_output is False
        and handoff.action_output is False
        and handoff.task_output is False
    )
