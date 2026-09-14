"""Trace candidates for controlled PCN skeleton assembly."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PCNTraceCandidate:
    trace_id: str
    context_ref: str
    activation_request_ref: str
    source_refs: Tuple[str, ...]
    link_refs: Tuple[str, ...]
    interaction_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    assembly_steps: Tuple[str, ...]
    projection_ref: str
    unknowns: Tuple[str, ...]
    status: str
    candidate_only: bool = True
