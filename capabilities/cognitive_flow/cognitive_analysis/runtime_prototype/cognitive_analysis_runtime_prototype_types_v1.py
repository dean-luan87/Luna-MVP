"""Types for the fixture-only A3 Cognitive Analysis Runtime Prototype v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.cognitive_flow.cognitive_analysis.result_contract.cognitive_analysis_result_contract_types_v1 import (
    CognitiveAnalysisResultCandidateV1,
)


RUNTIME_PROTOTYPE_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.runtime_prototype.v1"
RUNTIME_PROTOTYPE_PHASE_V1 = "Phase-A3-Cognitive-Analysis-Runtime-Prototype-v1-001"


@dataclass(frozen=True)
class CognitiveAnalysisRuntimePrototypeRequestV1:
    """Reference-only prototype input; it has no state or external capability handle."""

    analysis_id: str
    context_ref: str
    evidence_refs: Tuple[str, ...]
    analysis_question_ref: str
    fixture_id: str
    schema_version: str = RUNTIME_PROTOTYPE_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisRuntimePrototypeExecutionFlagsV1:
    """Execution is local and fixture-only; every external or write capability remains false."""

    runtime_executed: bool = True
    fixture_only: bool = True
    simulation_only: bool = True
    model_invoked: bool = False
    network_invoked: bool = False
    database_written: bool = False
    fact_write: bool = False
    decision_execute: bool = False
    action_execute: bool = False
    state_writeback: bool = False
    memory_update: bool = False
    model_training: bool = False
    runtime_authorized: bool = False


@dataclass(frozen=True)
class CognitiveAnalysisRuntimePrototypeResultV1:
    """A controlled execution envelope containing a candidate-only Analysis Result."""

    phase: str
    fixture_id: str
    input_trace: Tuple[str, ...]
    analysis_result_candidate: CognitiveAnalysisResultCandidateV1
    execution_flags: CognitiveAnalysisRuntimePrototypeExecutionFlagsV1
    deterministic_output: bool
    schema_version: str = RUNTIME_PROTOTYPE_SCHEMA_VERSION_V1
