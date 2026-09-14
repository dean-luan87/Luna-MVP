"""Deterministic types for A3 Runtime Validation Closure v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


RUNTIME_VALIDATION_CLOSURE_PHASE_V1 = "Phase-A3-Cognitive-Analysis-Runtime-Validation-Closure-v1-001"
RUNTIME_VALIDATION_RUN_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_VALIDATION_CLOSURE_V1"
RUNTIME_VALIDATION_VERIFIER_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_VALIDATION_CLOSURE_VERIFIER_V1"


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeValidationRunResultV1:
    phase: str
    run_id: str
    source_runtime_dryrun_ref: str
    checks: Mapping[str, bool]
    input_validation_ok: bool
    output_validation_ok: bool
    boundary_validation_ok: bool
    permission_validation_ok: bool
    forbidden_capability_absent: bool
    deterministic_validation_result: bool
    blocker_codes: Tuple[str, ...]
    warning_count: int
    blocker_count: int
    runtime_authorized: bool
    final_candidate_decision: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeValidationVerificationResultV1:
    verifier_id: str
    source_runtime_dryrun_ref: str
    source_validation_ref: str
    passed_checks: int
    failed_checks: int
    blocker_count: int
    warning_count: int
    runtime_flag_consistency_ok: bool
    permission_boundary_ok: bool
    output_contract_ok: bool
    forbidden_capability_absent: bool
    deterministic_validation_result_ok: bool
    verifier_invoked_runner: bool
    runtime_authorized: bool
    final_candidate_decision: str
