# -*- coding: utf-8 -*-
"""Reference-only projection types for Context Foundation skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple


class ProjectionKindV1(str, Enum):
    FIELD = "field"
    OBSERVATION = "observation"
    MEMORY = "memory"
    SELF = "self"
    ROLE = "role"
    RELATIONSHIP = "relationship"
    EMOTION = "emotion"


class UnknownStateV1(str, Enum):
    KNOWN = "known"
    UNKNOWN = "unknown"
    UNCERTAIN = "uncertain"
    MULTIPLE_CANDIDATES = "multiple_candidates"


@dataclass(frozen=True)
class ProjectionReferenceV1:
    """Metadata reference to a source-owned projection; never source payload."""

    source_owner: str
    projection_id: str
    projection_version: str
    timestamp: str
    validity: str
    confidence: Optional[float]
    unknown_state: str
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    projection_kind: str = ""
    trace_reference: str = ""
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False

