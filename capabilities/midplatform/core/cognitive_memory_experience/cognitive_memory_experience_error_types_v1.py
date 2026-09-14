"""Error types for Cognitive Memory & Experience controlled implementation v1."""

from __future__ import annotations


class CognitiveMemoryExperienceErrorV1(Exception):
    """Base error."""


class CognitiveMemoryExperienceBoundaryViolationV1(CognitiveMemoryExperienceErrorV1):
    """Raised on boundary violation."""


class CognitiveMemoryExperienceValidationErrorV1(CognitiveMemoryExperienceErrorV1):
    """Raised on input/output validation failure."""
