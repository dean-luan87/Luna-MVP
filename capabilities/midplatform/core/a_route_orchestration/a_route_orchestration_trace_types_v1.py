from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ARouteTraceV1:
    root_cycle_trace_id: str
    cycle_id: str
    previous_cycle_id: str
    source_owner_trace_refs: Tuple[str, ...]
    stage_trace_refs: Tuple[str, ...]
    handoff_trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    error_refs: Tuple[str, ...]
    reconsideration_lineage: Tuple[str, ...]
    reverse_lookup_path: Tuple[str, ...]
    authority_granted: bool = False
    candidate_only: bool = True
