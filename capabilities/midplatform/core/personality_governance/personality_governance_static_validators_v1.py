"""Static semantic validators for Personality Governance outputs."""

from __future__ import annotations

from typing import List

from .personality_governance_ownership_guard_v1 import validate_output_ownership
from .personality_governance_registry_v1 import (
    CANONICAL_OWNER,
    SEMANTIC_COMPRESSION_STATUS,
    SENSITIVITY_LEVELS,
    STABILITY_STATES,
    TRAIT_DIMENSIONS,
)
from .personality_io_types_v1 import PersonalityGovernanceOutputV1


def validate_output(output: PersonalityGovernanceOutputV1) -> List[str]:
    issues = [f"{item.code}:{item.message}" for item in validate_output_ownership(output)]
    trait = output.trait_candidate
    if trait.trait_dimension not in TRAIT_DIMENSIONS:
        issues.append("TRAIT_DIMENSION_NOT_REGISTERED")
    if trait.stability_candidate not in STABILITY_STATES:
        issues.append("STABILITY_NOT_REGISTERED")
    if trait.sensitivity not in SENSITIVITY_LEVELS:
        issues.append("SENSITIVITY_NOT_REGISTERED")
    if not trait.source_refs and not trait.evidence_refs:
        issues.append("SOURCE_EVIDENCE_MISSING")
    if not trait.trace_ref or not trait.provenance_refs:
        issues.append("TRACE_PROVENANCE_MISSING")
    if output.profile_candidate is not None:
        profile = output.profile_candidate
        if profile.single_personality_score is not None:
            issues.append("PROFILE_SINGLE_SCORE_FORBIDDEN")
        if profile.immutable_identity or profile.direct_action_control:
            issues.append("PROFILE_AUTHORITY_FORBIDDEN")
    if output.semantic_compression_status != SEMANTIC_COMPRESSION_STATUS:
        issues.append("SEMANTIC_COMPRESSION_STATUS_DRIFT")
    if not output.trace.reverse_locatable or not output.provenance.reverse_locatable:
        issues.append("REVERSE_LOOKUP_MISSING")
    if output.trait_candidate.contradiction_refs != output.trace.contradiction_refs:
        issues.append("CONTRADICTION_TRACE_LOSS")
    if output.trait_candidate.counterexample_refs != output.trace.counterexample_refs:
        issues.append("COUNTEREXAMPLE_TRACE_LOSS")
    return issues


def validate_candidate_flags(output: PersonalityGovernanceOutputV1) -> List[str]:
    issues = []
    for candidate in (output.trait_candidate, output.profile_candidate):
        if candidate is None:
            continue
        if not candidate.candidate_only or candidate.activated or candidate.persisted or candidate.truth_declared:
            issues.append(f"CANDIDATE_FLAG_DRIFT:{type(candidate).__name__}")
    return issues


def owner_name() -> str:
    return CANONICAL_OWNER
