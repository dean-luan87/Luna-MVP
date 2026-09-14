"""Immutable deterministic result types for A3 Controlled DryRun v1."""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, Mapping, Tuple


DRYRUN_PHASE_V1 = "Phase-A3-Cognitive-Analysis-Controlled-DryRun-Implementation-v1-001"
DRYRUN_RUN_ID_V1 = "A3_COGNITIVE_ANALYSIS_CONTROLLED_DRYRUN_V1_SMOKE_V0"
DRYRUN_VERIFIER_ID_V1 = "A3_COGNITIVE_ANALYSIS_CONTROLLED_DRYRUN_VERIFIER_V1"
FIXTURE_BASELINE_V1 = "A3_COGNITIVE_ANALYSIS_FIXTURE_BASELINE_V1"
CONTRACT_REF_V1 = "capabilities/cognitive_flow/cognitive_analysis/contracts/cognitive_analysis_object_contract_v1.json"


@dataclass(frozen=True)
class CognitiveAnalysisDryRunCheckResultV1:
    check_id: str; check_level: str; check_name: str; expected: Any; observed: Any; passed: bool
    warning_codes: Tuple[str, ...]; failure_codes: Tuple[str, ...]; blocker_codes: Tuple[str, ...]; evidence_refs: Tuple[str, ...]


@dataclass(frozen=True)
class CognitiveAnalysisDryRunCaseResultV1:
    case_id: str; case_name: str; fixture_ref: str; expected_status: str; observed_status: str
    object_checks: Tuple[CognitiveAnalysisDryRunCheckResultV1, ...]; reference_checks: Tuple[CognitiveAnalysisDryRunCheckResultV1, ...]
    semantic_checks: Tuple[CognitiveAnalysisDryRunCheckResultV1, ...]; permission_checks: Tuple[CognitiveAnalysisDryRunCheckResultV1, ...]
    negative_guard_checks: Tuple[CognitiveAnalysisDryRunCheckResultV1, ...]; warning_codes: Tuple[str, ...]
    failure_codes: Tuple[str, ...]; blocker_codes: Tuple[str, ...]; passed: bool


@dataclass(frozen=True)
class CognitiveAnalysisDryRunRunResultV1:
    phase: str; run_id: str; contract_ref: str; fixture_baseline_ref: str; fixture_assembled: bool; real_analysis_executed: bool
    runtime_executed: bool; simulation_only: bool; model_invoked: bool; network_invoked: bool; database_invoked: bool
    observation_executed: bool; decision_executed: bool; state_writeback: bool; case_count: int; passed_case_count: int
    failed_case_count: int; blocker_count: int; warning_count: int; case_results: Tuple[CognitiveAnalysisDryRunCaseResultV1, ...]
    negative_guard_summary: Mapping[str, bool]; final_candidate_decision: str


@dataclass(frozen=True)
class CognitiveAnalysisDryRunVerificationResultV1:
    verifier_id: str; source_run_ref: str; expected_case_count: int; observed_case_count: int; passed_checks: int; failed_checks: int
    blocker_count: int; warning_count: int; dangling_reference_count: int; cross_case_reference_count: int; boundary_ok: bool
    fixture_only: bool; runtime_executed: bool; simulation_only: bool; final_candidate_decision: str


def to_jsonable_v1(value: Any) -> Any:
    if isinstance(value, Enum): return value.value
    if is_dataclass(value): return to_jsonable_v1(asdict(value))
    if isinstance(value, Mapping): return {str(k): to_jsonable_v1(v) for k, v in value.items()}
    if isinstance(value, tuple): return [to_jsonable_v1(v) for v in value]
    return value
