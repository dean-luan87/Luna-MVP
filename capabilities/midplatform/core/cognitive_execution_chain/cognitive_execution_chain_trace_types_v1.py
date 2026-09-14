from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class EndToEndTraceV1:
    root_trace_id: str
    intent_trace_ref: str
    causal_trace_ref: str
    decision_trace_ref: str
    action_trace_ref: str
    execution_trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class ProvenanceReversePathV1:
    execution_result_ref: str
    action_candidate_ref: str
    decision_candidate_ref: str | None
    causal_hypothesis_refs: Tuple[str, ...]
    intent_candidate_refs: Tuple[str, ...]
    source_evidence_or_context_refs: Tuple[str, ...]
    reverse_locatable: bool
