"""Explicit errors for candidate-only Personality Governance validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalityGovernanceIssueV1:
    code: str
    message: str


class PersonalityGovernanceErrorV1(ValueError):
    """Base error for invalid candidate input or owner boundary requests."""


class PersonalityOwnershipBoundaryErrorV1(PersonalityGovernanceErrorV1):
    """Raised when Personality attempts to mutate another owner."""


class PersonalityCandidateValidationErrorV1(PersonalityGovernanceErrorV1):
    """Raised for malformed or unsafe candidate input."""


class DuplicatePersonalityCandidateErrorV1(PersonalityGovernanceErrorV1):
    """Raised only by explicit duplicate admission requests."""


@dataclass(frozen=True)
class PersonalityValidationResultV1:
    issues: Tuple[PersonalityGovernanceIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues
