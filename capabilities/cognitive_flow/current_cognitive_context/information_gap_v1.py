"""Information Gap object for Current Cognitive Context v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .context_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1,
    InformationGapTypeV1,
)


@dataclass(frozen=True)
class InformationGapV1:
    gap_id: str
    gap_type: str
    target_ref: str
    missing_information: str
    blocking_level: str
    related_goal_ref: str
    related_task_ref: str
    recommended_observation_scope: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        allowed = {gap_type.value for gap_type in InformationGapTypeV1}
        if self.gap_type not in allowed:
            raise ValueError("unsupported Information Gap type")
