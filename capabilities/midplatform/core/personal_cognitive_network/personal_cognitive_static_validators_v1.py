"""Pure static validators for PCN controlled skeleton boundaries."""

from __future__ import annotations

from typing import Iterable

from .personal_cognitive_interaction_types_v1 import InteractionReferenceCandidate
from .personal_cognitive_link_types_v1 import (
    CognitiveLinkCandidate,
    strength_not_equal_truth,
)
from .personal_cognitive_projection_types_v1 import ActiveCognitiveProjectionCandidate


def validate_source_owner_exists(owner: str) -> bool:
    return bool(owner.strip())


def validate_no_source_payload_copied(source_payload_copied: bool) -> bool:
    return source_payload_copied is False


def validate_no_source_mutation_authority(source_mutation_allowed: bool) -> bool:
    return source_mutation_allowed is False


def validate_strength_not_truth(link: CognitiveLinkCandidate) -> bool:
    return strength_not_equal_truth(link)


def validate_dormant_not_deleted(dormant_not_deleted: bool) -> bool:
    return dormant_not_deleted is True


def validate_resonance_not_causal(interaction: InteractionReferenceCandidate) -> bool:
    return not (
        interaction.interaction_type == "RESONANCE"
        and interaction.status.upper() == "CAUSAL_FACT"
    )


def validate_competition_not_arbitration(
    interaction: InteractionReferenceCandidate,
) -> bool:
    return not (
        interaction.interaction_type == "COMPETITION"
        and "WINNER" in interaction.status.upper()
    )


def validate_kernel_not_owned_by_pcn(
    interaction: InteractionReferenceCandidate,
) -> bool:
    return interaction.pcn_owns_interaction_kernel is False


def validate_unknown_preserved(unknowns: Iterable[str]) -> bool:
    return len(tuple(unknowns)) >= 1


def validate_resource_reference_exists(resource_ref: str) -> bool:
    return bool(resource_ref.strip())


def validate_no_fixed_propagation_depth(fixed_depth: bool) -> bool:
    return fixed_depth is False


def validate_no_fixed_graph_size(fixed_max_nodes: bool, fixed_max_links: bool) -> bool:
    return fixed_max_nodes is False and fixed_max_links is False


def validate_no_fixed_retention_duration(fixed_retention_days: bool) -> bool:
    return fixed_retention_days is False


def validate_projection_candidate_only(
    projection: ActiveCognitiveProjectionCandidate,
) -> bool:
    return projection.candidate_only is True


def validate_no_decision_output(projection: ActiveCognitiveProjectionCandidate) -> bool:
    return projection.decision_output is False


def validate_no_causal_output(projection: ActiveCognitiveProjectionCandidate) -> bool:
    return projection.causal_output is False


def validate_no_intent_output(projection: ActiveCognitiveProjectionCandidate) -> bool:
    return projection.intent_output is False


def validate_no_runtime_execution(runtime_executed: bool) -> bool:
    return runtime_executed is False
