"""Structured error namespace for PCN controlled skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


ERROR_NAMESPACES = (
    "PCN_BOUNDARY_",
    "PCN_REFERENCE_",
    "PCN_ACTIVATION_",
    "PCN_PROJECTION_",
    "PCN_INTERACTION_",
    "PCN_RESOURCE_",
    "PCN_TRACE_",
)


@dataclass(frozen=True)
class PCNError:
    code: str
    message: str
    details: Dict[str, str]


def build_error(namespace: str, suffix: str, message: str, **details: str) -> PCNError:
    if namespace not in ERROR_NAMESPACES:
        namespace = "PCN_BOUNDARY_"
    return PCNError(code=f"{namespace}{suffix}", message=message, details=details)
