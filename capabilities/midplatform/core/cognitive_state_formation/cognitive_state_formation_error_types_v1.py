"""Error types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations


class CognitiveStateFormationErrorV1(Exception):
    """Base error for controlled implementation failures."""


class OwnershipBoundaryViolationV1(CognitiveStateFormationErrorV1):
    """Raised when owner boundary checks fail."""


class ContractValidationErrorV1(CognitiveStateFormationErrorV1):
    """Raised when input or output contract checks fail."""
