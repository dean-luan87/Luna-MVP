"""Deterministic result types for A3 Runtime Skeleton DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple

from ..runtime.cognitive_analysis_runtime_types_v1 import (
    CognitiveAnalysisRuntimeSkeletonResultV1,
)


RUNTIME_SKELETON_DRYRUN_PHASE_V1 = "Phase-A3-Cognitive-Analysis-Runtime-Skeleton-DryRun-v1-001"
RUNTIME_SKELETON_DRYRUN_RUN_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_SKELETON_DRYRUN_V1"
RUNTIME_SKELETON_DRYRUN_VERIFIER_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_SKELETON_DRYRUN_VERIFIER_V1"
RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1 = "runtime_skeleton_request_fixture_v1"


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeDryRunResultV1:
    phase: str
    run_id: str
    request_fixture_ref: str
    runtime_authorization_status: str
    skeleton_result: CognitiveAnalysisRuntimeSkeletonResultV1
    runtime_executed: bool
    simulation_only: bool
    model_invoked: bool
    network_invoked: bool
    database_invoked: bool
    state_writeback: bool
    decision_executed: bool
    external_invocation_observed: bool
    deterministic_serialization: bool
    warning_count: int
    blocker_count: int
    final_candidate_decision: str
    determinism_status: str = "DETERMINISM_UNVERIFIED"
    determinism_evidence: Mapping[str, object] = field(default_factory=dict)
    side_effect_evidence: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeDryRunVerificationResultV1:
    verifier_id: str
    source_run_ref: str
    passed_checks: int
    failed_checks: int
    blocker_count: int
    warning_count: int
    runtime_boundary_ok: bool
    permission_boundary_ok: bool
    flag_consistency_ok: bool
    deterministic_serialization_ok: bool
    external_invocation_absent: bool
    verifier_invoked_runner: bool
    final_candidate_decision: str
    determinism_status: str = "DETERMINISM_UNVERIFIED"
    side_effect_evidence_status: str = "UNKNOWN"
