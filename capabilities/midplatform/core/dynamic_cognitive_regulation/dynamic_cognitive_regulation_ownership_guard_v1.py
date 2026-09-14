"""Ownership and reference-only guards for controlled regulation."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_genome_types_v1 import (
    CognitiveParameterGenomeCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_core_types_v1 import (
    RegulationPolicyRefV1,
    SourceRefV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_registry_v1 import (
    CANONICAL_OWNER,
    FORBIDDEN_PARALLEL_OWNERS,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER


def validate_no_parallel_owner(owner: str) -> bool:
    return owner not in FORBIDDEN_PARALLEL_OWNERS


def validate_source_refs_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.reference_only is True
        and ref.candidate_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_policy_refs_read_only(refs: Iterable[RegulationPolicyRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.candidate_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_genome_boundary(
    genome: CognitiveParameterGenomeCandidateV1 | None,
) -> bool:
    if genome is None:
        return True
    return (
        genome.candidate_only is True
        and genome.active is False
        and genome.persisted is False
        and genome.model_weights_rewritten is False
        and genome.user_identity_modified is False
        and genome.cross_user_propagated is False
        and genome.learned_truth is False
        and bool(genome.rollback_ref)
        and bool(genome.trace_ref)
        and bool(genome.provenance_refs)
    )
