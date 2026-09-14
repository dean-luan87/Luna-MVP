from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class MainlineTraceLinkV1:
    root_trace_id: str
    context_trace_ref: str
    pcn_trace_ref: str
    intent_trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class MainlineProvenanceReversePathV1:
    intent_candidate_ref: str
    pcn_projection_ref: str
    context_candidate_ref: str
    source_context_refs: Tuple[str, ...]
    reverse_locatable: bool
    provenance_chain: Tuple[str, ...] = field(default_factory=tuple)
