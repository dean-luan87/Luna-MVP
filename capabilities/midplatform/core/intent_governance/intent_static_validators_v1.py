"""Static validators for Intent Governance controlled implementation v1."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    IntentCandidateV1,
    PotentialIntentCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_handoff_types_v1 import (
    IntentToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_interaction_types_v1 import (
    IntentInteractionCandidateV1,
)
from capabilities.midplatform.core.intent_governance.intent_lifecycle_types_v1 import (
    STATE_CANDIDATES_V1,
)
from capabilities.midplatform.core.intent_governance.intent_ownership_guard_v1 import (
    validate_forbidden_owner_tokens,
    validate_handoff_boundary,
    validate_intent_candidate_boundary,
    validate_potential_candidate_boundary,
    validate_ref_read_only,
)
from capabilities.midplatform.core.intent_governance.intent_registry_v1 import (
    ALLOWED_FUTURE_RELATIONS,
    INTERACTION_SET,
)


def validate_input_refs_read_only(all_refs: Iterable[SourceRefV1]) -> bool:
    return validate_ref_read_only(all_refs) and validate_forbidden_owner_tokens(
        all_refs
    )


def validate_potential_intent(candidate: PotentialIntentCandidateV1) -> bool:
    return validate_potential_candidate_boundary(candidate)


def validate_intent_candidate(candidate: IntentCandidateV1) -> bool:
    return (
        validate_intent_candidate_boundary(candidate)
        and candidate.future_state_relation in ALLOWED_FUTURE_RELATIONS
        and candidate.state_candidate in STATE_CANDIDATES_V1
        and candidate.truth_status
        in {"UNKNOWN", "SUPPORTED_CANDIDATE", "CONTRADICTED_CANDIDATE"}
    )


def validate_interaction_candidate(candidate: IntentInteractionCandidateV1) -> bool:
    return (
        candidate.interaction_type in INTERACTION_SET
        and bool(candidate.participant_candidate_ids)
        and bool(candidate.source_refs)
        and bool(candidate.context_refs)
        and bool(candidate.resource_ref)
        and bool(candidate.provenance)
        and candidate.candidate_only is True
        and candidate.decision_authority is False
        and candidate.action_authority is False
    )


def validate_handoff_candidate(handoff: IntentToCausalHandoffCandidateV1) -> bool:
    return validate_handoff_boundary(handoff)


def validate_no_runtime_or_mutation(
    intent_candidates: Iterable[IntentCandidateV1],
) -> bool:
    return all(
        item.runtime_executed is False
        and item.source_mutation_executed is False
        and item.decision_output is False
        and item.action_output is False
        and item.task_output is False
        and item.causal_output is False
        for item in intent_candidates
    )
