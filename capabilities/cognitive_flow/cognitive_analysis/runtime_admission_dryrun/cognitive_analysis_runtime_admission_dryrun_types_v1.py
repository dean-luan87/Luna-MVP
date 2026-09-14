"""Types for the A3 Runtime Capability Admission DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


ADMISSION_DRYRUN_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.runtime_capability_admission_dryrun.v1"
)
ADMISSION_DRYRUN_PHASE_V1 = (
    "Phase-A3-Cognitive-Analysis-Runtime-Capability-Admission-DryRun-v1-001"
)
ADMISSION_DRYRUN_RUN_ID_V1 = "cognitive_analysis_runtime_capability_admission_dryrun_v1"
ADMISSION_DRYRUN_VERIFIER_ID_V1 = (
    "cognitive_analysis_runtime_capability_admission_dryrun_verifier_v1"
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeAdmissionAssessmentCandidateV1:
    phase: str
    run_id: str
    capability_id: str
    registry_ref: str
    registry_reference_exists: bool
    registry_record_exists: bool
    lifecycle_state: str
    checks: Mapping[str, bool]
    admission_status: str
    admission_applied: bool
    registry_write_applied: bool
    capability_activation_applied: bool
    permission_grant_applied: bool
    runtime_executed: bool
    runtime_authorized: bool
    blocker_codes: Tuple[str, ...]
    warning_codes: Tuple[str, ...]
    blocker_count: int
    warning_count: int
    deterministic_output: bool
    final_candidate_decision: str
    schema_version: str = ADMISSION_DRYRUN_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeAdmissionDryRunVerificationResultV1:
    verifier_id: str
    source_result_ref: str
    passed_checks: int
    failed_checks: int
    blocker_count: int
    warning_count: int
    registry_reference_ok: bool
    lifecycle_consistent: bool
    contract_complete: bool
    permission_reference_ok: bool
    boundary_consistent: bool
    deterministic_output_ok: bool
    verifier_invoked_runner: bool
    runtime_authorized: bool
    final_candidate_decision: str
    schema_version: str = ADMISSION_DRYRUN_SCHEMA_VERSION_V1
