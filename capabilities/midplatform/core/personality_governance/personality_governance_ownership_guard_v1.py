"""Ownership and mutation guards for Personality Governance."""

from __future__ import annotations

from typing import Iterable, Tuple

from .personality_governance_error_types_v1 import PersonalityGovernanceIssueV1
from .personality_governance_registry_v1 import CANONICAL_OWNER, NEGATIVE_GUARDS
from .personality_io_types_v1 import PersonalityGovernanceInputV1, PersonalityGovernanceOutputV1


def validate_input_ownership(request: PersonalityGovernanceInputV1) -> Tuple[PersonalityGovernanceIssueV1, ...]:
    issues = []
    if not request.candidate_only:
        issues.append(PersonalityGovernanceIssueV1("INPUT_NOT_CANDIDATE_ONLY", "Personality input must remain candidate-only."))
    if not request.synthetic_only:
        issues.append(PersonalityGovernanceIssueV1("INPUT_NOT_SYNTHETIC", "Controlled implementation input must be synthetic-only."))
    return tuple(issues)


def validate_output_ownership(output: PersonalityGovernanceOutputV1) -> Tuple[PersonalityGovernanceIssueV1, ...]:
    issues = []
    if output.source_owner_mutation or output.trace.provenance_grants_authority:
        issues.append(PersonalityGovernanceIssueV1("OWNER_MUTATION", "Personality output cannot mutate or acquire source-owner authority."))
    if not output.candidate_only or not output.synthetic_only:
        issues.append(PersonalityGovernanceIssueV1("OUTPUT_MODE", "Output must remain synthetic and candidate-only."))
    if output.trait_activation or output.trait_candidate.activated:
        issues.append(PersonalityGovernanceIssueV1("TRAIT_ACTIVATION", "Trait activation is forbidden."))
    for name, value in output.negative_guard_status.guards:
        expected = NEGATIVE_GUARDS.get(name)
        if expected is not None and value is not expected:
            issues.append(PersonalityGovernanceIssueV1("NEGATIVE_GUARD", f"Negative guard drift: {name}={value}."))
    return tuple(issues)


def source_owner_name() -> str:
    return CANONICAL_OWNER
