"""Boundary classification without promotion to identity truth."""

from __future__ import annotations

from typing import Tuple

from .self_governance_registry_v1 import BOUNDARY_CLASSES


def classify_self_boundary(statement: str, explicit_class: str | None = None) -> str:
    if explicit_class in BOUNDARY_CLASSES:
        return explicit_class
    text = statement.lower()
    if "someone told me" in text or "contested" in text or "dispute" in text:
        return "CONTESTED"
    if "user" in text or "other" in text or "someone else" in text:
        return "OTHER"
    if "battery" in text or "resource" in text or "platform" in text:
        return "SYSTEM"
    if "shared" in text or "joint" in text:
        return "SHARED"
    if "environment" in text or "weather" in text or "world" in text:
        return "ENVIRONMENT"
    if "my " in text or "own " in text or "self" in text:
        return "SELF"
    return "UNKNOWN"


def boundary_classification_is_candidate_only(boundary_class: str) -> bool:
    return boundary_class in BOUNDARY_CLASSES


BOUNDARY_CLASS_SET: Tuple[str, ...] = BOUNDARY_CLASSES
