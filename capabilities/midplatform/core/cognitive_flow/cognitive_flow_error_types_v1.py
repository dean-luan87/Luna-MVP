"""Error types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations


class CognitiveFlowErrorV1(Exception):
    """Base error."""


class CognitiveFlowBoundaryViolationV1(CognitiveFlowErrorV1):
    """Raised when owner or boundary contracts are violated."""


class CognitiveFlowValidationErrorV1(CognitiveFlowErrorV1):
    """Raised when input or transition validation fails."""
