"""Structured error namespace for Intent Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


ERROR_NAMESPACES = (
    "INTENT_BOUNDARY_",
    "INTENT_INPUT_",
    "INTENT_LIFECYCLE_",
    "INTENT_INTERACTION_",
    "INTENT_RESOURCE_",
    "INTENT_HANDOFF_",
    "INTENT_TRACE_",
)


@dataclass(frozen=True)
class IntentErrorV1:
    code: str
    message: str
    details: Dict[str, str]


def build_error(
    namespace: str, suffix: str, message: str, **details: str
) -> IntentErrorV1:
    if namespace not in ERROR_NAMESPACES:
        namespace = "INTENT_BOUNDARY_"
    return IntentErrorV1(code=f"{namespace}{suffix}", message=message, details=details)
