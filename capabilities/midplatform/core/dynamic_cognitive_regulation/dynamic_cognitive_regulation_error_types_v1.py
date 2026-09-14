"""Explicit non-coercing error types for controlled regulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


class DynamicCognitiveRegulationErrorV1(ValueError):
    """Base error for invalid controlled implementation input."""


class OwnershipBoundaryErrorV1(DynamicCognitiveRegulationErrorV1):
    """Raised when owner or source-mutation boundaries are violated."""


class ParameterValidationErrorV1(DynamicCognitiveRegulationErrorV1):
    """Raised when a parameter cannot be evaluated without coercion."""


@dataclass(frozen=True)
class RegulationIssueV1:
    code: str
    message: str
    affected_ref: str
    classification: str
    remediation: str
    blocker: bool = False


@dataclass(frozen=True)
class RegulationIssueSetV1:
    issues: Tuple[RegulationIssueV1, ...]

    @property
    def has_blocker(self) -> bool:
        return any(item.blocker for item in self.issues)
