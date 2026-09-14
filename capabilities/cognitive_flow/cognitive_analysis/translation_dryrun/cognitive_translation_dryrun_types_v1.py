"""Types for the A3 Translation Layer Controlled DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.cognitive_flow.cognitive_analysis.translation_layer.cognitive_translation_types_v1 import (
    CognitiveTranslationCandidateEnvelopeV1,
    CognitiveTranslationRequestEnvelopeV1,
)


TRANSLATION_DRYRUN_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.translation_dryrun.v1"
TRANSLATION_DRYRUN_PHASE_V1 = "Phase-A3-Evidence-Context-Translation-Layer-Controlled-DryRun-v1-001"
TRANSLATION_DRYRUN_RUN_ID_V1 = "a3_translation_layer_controlled_dryrun_v1"
TRANSLATION_DRYRUN_VERIFIER_ID_V1 = "a3_translation_layer_controlled_dryrun_verifier_v1"


@dataclass(frozen=True)
class CognitiveTranslationDryRunFixtureCaseV1:
    case_id: str
    fixture_kind: str
    input_candidate_label: str
    expected_primitive_type: str
    expected_candidate_label: str
    forbidden_claims: Tuple[str, ...]
    request: CognitiveTranslationRequestEnvelopeV1


@dataclass(frozen=True)
class CognitiveTranslationDryRunCaseResultV1:
    case_id: str
    fixture_kind: str
    input_candidate_label: str
    expected_primitive_type: str
    expected_candidate_label: str
    forbidden_claims: Tuple[str, ...]
    semantic_label_generated: bool
    request: CognitiveTranslationRequestEnvelopeV1
    translation_candidate_envelope: CognitiveTranslationCandidateEnvelopeV1
    case_passed: bool


@dataclass(frozen=True)
class CognitiveTranslationDryRunRunResultV1:
    phase: str
    run_id: str
    case_results: Tuple[CognitiveTranslationDryRunCaseResultV1, ...]
    translation_executed: bool
    simulation_only: bool
    model_invoked: bool
    external_call: bool
    fact_created: bool
    decision_created: bool
    action_created: bool
    state_writeback: bool
    memory_updated: bool
    all_cases_passed: bool
    deterministic_output: bool
    blocker_count: int
    warning_count: int
    final_candidate_decision: str
    schema_version: str = TRANSLATION_DRYRUN_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveTranslationDryRunVerificationResultV1:
    verifier_id: str
    source_result_ref: str
    passed_checks: int
    failed_checks: int
    case_count: int
    negative_guards_passed: bool
    deterministic_output_ok: bool
    verifier_invoked_runner: bool
    verifier_invoked_skeleton: bool
    blocker_count: int
    warning_count: int
    final_candidate_decision: str
    schema_version: str = TRANSLATION_DRYRUN_SCHEMA_VERSION_V1
