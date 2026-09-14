"""Immutable types for the non-executing A3 Runtime Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


COGNITIVE_ANALYSIS_RUNTIME_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.runtime_skeleton.v1"


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeRequestV1:
    """Reference-only input; it contains no raw observations or mutation handles."""

    context_ref: str
    evidence_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    analysis_question_ref: str
    schema_version: str = COGNITIVE_ANALYSIS_RUNTIME_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeFlagsV1:
    """Frozen zero-side-effect flags for this controlled skeleton."""

    runtime_executed: bool = False
    simulation_only: bool = True
    model_invoked: bool = False
    network_invoked: bool = False
    database_invoked: bool = False
    state_writeback: bool = False
    decision_executed: bool = False


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeSkeletonResultV1:
    """A not-executed candidate envelope, never a real analysis result."""

    analysis_result_candidate: Mapping[str, str]
    evidence_trace: Mapping[str, Tuple[str, ...]]
    uncertainty: Mapping[str, str]
    warning_codes: Tuple[str, ...]
    runtime_flags: CognitiveAnalysisRuntimeFlagsV1
    validation_issue_codes: Tuple[str, ...]
    schema_version: str = COGNITIVE_ANALYSIS_RUNTIME_SCHEMA_VERSION_V1
