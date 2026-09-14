"""Error types for Cognitive Learning controlled implementation v1."""

from __future__ import annotations


class CognitiveLearningErrorV1(Exception):
    """Base error."""


class CognitiveLearningBoundaryViolationV1(CognitiveLearningErrorV1):
    """Raised on owner/boundary violation."""


class CognitiveLearningValidationErrorV1(CognitiveLearningErrorV1):
    """Raised on input/output validation failure."""
