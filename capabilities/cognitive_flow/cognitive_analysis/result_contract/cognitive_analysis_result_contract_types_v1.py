"""Types for A3 Cognitive Analysis Result Candidate Contract v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


COGNITIVE_ANALYSIS_RESULT_CONTRACT_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.result_candidate_contract.v1"
)

ALLOWED_ANALYSIS_TYPES_V1 = (
    "context_interpretation_candidate",
    "evidence_relationship_candidate",
    "hypothesis_candidate",
    "uncertainty_assessment_candidate",
    "semantic_explanation_candidate",
)

FORBIDDEN_AUTHORITY_FLAGS_V1 = (
    "fact_created",
    "fact_mutated",
    "decision_created",
    "action_executed",
    "state_mutated",
    "memory_updated",
    "runtime_executed",
    "model_invoked",
    "inference_executed",
)


@dataclass(frozen=True)
class CognitiveAnalysisResultCandidateV1:
    """A structured cognitive signal; never a Fact, Decision, Action, State, or Memory write."""

    analysis_id: str
    input_reference: str
    evidence_reference: Tuple[str, ...]
    analysis_type: str
    candidate_output: Mapping[str, object]
    uncertainty: Mapping[str, object]
    provenance: Mapping[str, object]
    confidence: float | None
    warning: Tuple[str, ...]
    authority_flags: Mapping[str, bool]
    candidate_only: bool = True
    fact_status: str = "not_fact"
    schema_version: str = COGNITIVE_ANALYSIS_RESULT_CONTRACT_SCHEMA_VERSION_V1
