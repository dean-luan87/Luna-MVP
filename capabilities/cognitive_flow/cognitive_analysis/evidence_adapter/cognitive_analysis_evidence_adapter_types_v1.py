"""Types for the reference-only A3 Evidence Context Adapter boundary v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


EVIDENCE_CONTEXT_ADAPTER_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.evidence_context_adapter_boundary.v1"
)

FORBIDDEN_ADAPTER_OPERATION_FLAGS_V1 = (
    "runtime_execution",
    "model_invocation",
    "fact_admission",
    "semantic_finalization",
    "decision_generation",
    "action_execution",
    "state_mutation",
    "memory_update",
)


@dataclass(frozen=True)
class CognitiveAnalysisEvidenceContextAdapterCandidateV1:
    """Normalized references only; it contains no raw payload, Fact, or mutation handle."""

    adapter_request_id: str
    input_reference: str
    evidence_references: Tuple[str, ...]
    context_reference: str
    provenance: Mapping[str, object]
    normalized_reference_mapping: Mapping[str, object]
    permission_flags: Mapping[str, bool]
    candidate_only: bool = True
    fact_status: str = "not_fact"
    runtime_authorized: bool = False
    schema_version: str = EVIDENCE_CONTEXT_ADAPTER_SCHEMA_VERSION_V1
