"""Immutable capability-inventory types for A3 Runtime Assessment v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple


RUNTIME_CAPABILITY_ASSESSMENT_PHASE_V1 = "Phase-A3-Cognitive-Analysis-Runtime-Capability-Assessment-v1-001"
RUNTIME_CAPABILITY_ASSESSMENT_RUN_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_CAPABILITY_ASSESSMENT_V1"
RUNTIME_CAPABILITY_ASSESSMENT_VERIFIER_ID_V1 = "A3_COGNITIVE_ANALYSIS_RUNTIME_CAPABILITY_ASSESSMENT_VERIFIER_V1"
CAPABILITY_IDS_V1 = (
    "context_interpretation_candidate",
    "evidence_relationship_candidate",
    "hypothesis_candidate",
    "uncertainty_assessment_candidate",
    "semantic_explanation_candidate",
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeCapabilityEntryV1:
    capability: str
    input_dependency: Tuple[str, ...]
    expected_output: str
    authority_boundary: str
    blocker_condition: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeCapabilityAssessmentReportV1:
    phase: str
    run_id: str
    capabilities: Tuple[CognitiveAnalysisRuntimeCapabilityEntryV1, ...]
    runtime_authorized: bool
    runtime_executed: bool
    model_invoked: bool
    evidence_inferred: bool
    hypothesis_generated: bool
    state_writeback: bool
    decision_generated: bool
    action_planned: bool
    memory_updated: bool
    deterministic_output: bool
    warning_codes: Tuple[str, ...]
    blocker_count: int
    final_candidate_decision: str
    determinism_status: str = "DETERMINISM_UNVERIFIED"
    determinism_evidence: Mapping[str, object] = field(default_factory=dict)
    side_effect_evidence: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeCapabilityAssessmentVerificationResultV1:
    verifier_id: str
    source_report_ref: str
    passed_checks: int
    failed_checks: int
    blocker_count: int
    warning_count: int
    capability_inventory_complete: bool
    authority_boundary_ok: bool
    forbidden_capability_absent: bool
    dependency_declaration_ok: bool
    deterministic_output_ok: bool
    verifier_invoked_runner: bool
    runtime_authorized: bool
    final_candidate_decision: str
    determinism_status: str = "DETERMINISM_UNVERIFIED"
    side_effect_evidence_status: str = "UNKNOWN"
