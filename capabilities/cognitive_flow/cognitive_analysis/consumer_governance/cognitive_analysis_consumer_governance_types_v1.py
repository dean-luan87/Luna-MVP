"""Types for A3 Cognitive Analysis Result Consumer Governance v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


CONSUMER_GOVERNANCE_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.consumer_governance.v1"

ALLOWED_CONSUMER_TYPES_V1 = (
    "observation_layer",
    "context_layer",
    "hypothesis_layer",
    "decision_support_layer",
    "learning_candidate_layer",
)

REQUIRED_READ_ACCESS_V1 = (
    "analysis_result_candidate",
    "evidence_reference",
    "uncertainty",
    "provenance",
)

FORBIDDEN_ACCESS_V1 = (
    "fact_creation",
    "fact_mutation",
    "decision_creation",
    "action_execution",
    "state_mutation",
    "memory_update",
)


@dataclass(frozen=True)
class CognitiveAnalysisConsumerGovernanceDeclarationV1:
    """A read-only consumer declaration, not a permission grant or handoff execution."""

    consumer_id: str
    consumer_type: str
    source_result_reference: str
    allowed_access: Tuple[str, ...]
    forbidden_access: Tuple[str, ...]
    required_evidence: bool
    required_trace: bool
    authority_flags: Mapping[str, bool]
    runtime_authorized: bool = False
    schema_version: str = CONSUMER_GOVERNANCE_SCHEMA_VERSION_V1
