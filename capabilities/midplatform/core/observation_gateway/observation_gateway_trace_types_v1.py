from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ObservationGatewayTraceV1:
    root_trace_id: str
    a_route_ingress_ref: str
    observation_trace_ref: str
    evidence_trace_refs: Tuple[str, ...]
    provider_trace_refs: Tuple[str, ...]
    source_input_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    correction_lineage: Tuple[str, ...]
    contradiction_lineage: Tuple[str, ...]
    temporal_lineage: Tuple[str, ...]
    reverse_lookup_path: Tuple[str, ...]
    authority_granted: bool = False
    candidate_only: bool = True
