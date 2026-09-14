"""Caller-assembled Context Sufficiency Result v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .context_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1,
    ContextSufficiencyStatusV1,
)


@dataclass(frozen=True)
class ContextSufficiencyResultV1:
    sufficiency_status: str
    reason_codes: Tuple[str, ...]
    blocking_gap_refs: Tuple[str, ...]
    condition_refs: Tuple[str, ...]
    evaluated_context_ref: str
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        allowed = {status.value for status in ContextSufficiencyStatusV1}
        if self.sufficiency_status not in allowed:
            raise ValueError("unsupported Context Sufficiency status")
