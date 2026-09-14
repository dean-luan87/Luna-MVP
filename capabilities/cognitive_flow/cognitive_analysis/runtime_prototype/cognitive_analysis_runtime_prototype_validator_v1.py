"""Pure validation for the A3 Runtime Prototype contract v1."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Tuple

from capabilities.cognitive_flow.cognitive_analysis.result_contract.cognitive_analysis_result_contract_validator_v1 import (
    validate_cognitive_analysis_result_candidate_v1,
)

from .cognitive_analysis_runtime_prototype_types_v1 import (
    RUNTIME_PROTOTYPE_PHASE_V1,
    RUNTIME_PROTOTYPE_SCHEMA_VERSION_V1,
    CognitiveAnalysisRuntimePrototypeRequestV1,
    CognitiveAnalysisRuntimePrototypeResultV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimePrototypeIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimePrototypeValidationResultV1:
    issues: Tuple[CognitiveAnalysisRuntimePrototypeIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def canonicalize_cognitive_analysis_runtime_prototype_result_v1(
    result: CognitiveAnalysisRuntimePrototypeResultV1,
) -> str:
    """Canonical serialization helper only; it performs no file write or execution."""
    return json.dumps(asdict(result), indent=2, sort_keys=True) + "\n"


def validate_cognitive_analysis_runtime_prototype_request_v1(
    request: CognitiveAnalysisRuntimePrototypeRequestV1,
) -> CognitiveAnalysisRuntimePrototypeValidationResultV1:
    """Validate prototype references without resolving, fetching, or executing them."""
    issues = []
    if request.schema_version != RUNTIME_PROTOTYPE_SCHEMA_VERSION_V1:
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "invalid_schema_version", "schema_version", "prototype request schema must match v1"
        ))
    for field_ref, value in {
        "analysis_id": request.analysis_id,
        "context_ref": request.context_ref,
        "analysis_question_ref": request.analysis_question_ref,
        "fixture_id": request.fixture_id,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
                "required_reference_missing", field_ref, f"{field_ref} must be non-empty"
            ))
    if not request.evidence_refs or not all(
        isinstance(reference, str) and reference.strip() for reference in request.evidence_refs
    ):
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "evidence_reference_missing", "evidence_refs", "at least one evidence reference is required"
        ))
    return CognitiveAnalysisRuntimePrototypeValidationResultV1(tuple(issues))


def validate_cognitive_analysis_runtime_prototype_result_v1(
    request: CognitiveAnalysisRuntimePrototypeRequestV1,
    result: CognitiveAnalysisRuntimePrototypeResultV1,
) -> CognitiveAnalysisRuntimePrototypeValidationResultV1:
    """Validate trace, output candidate, permissions, authority, and serialization determinism."""
    issues = list(validate_cognitive_analysis_runtime_prototype_request_v1(request).issues)
    if result.phase != RUNTIME_PROTOTYPE_PHASE_V1:
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "phase_mismatch", "phase", "prototype result must retain the declared phase"
        ))
    expected_trace = (request.context_ref, *request.evidence_refs, request.analysis_question_ref)
    if result.input_trace != expected_trace:
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "input_trace_inconsistent", "input_trace", "trace must preserve Context, Evidence, and Question references"
        ))
    result_contract_validation = validate_cognitive_analysis_result_candidate_v1(
        result.analysis_result_candidate
    )
    issues.extend(
        CognitiveAnalysisRuntimePrototypeIssueV1(issue.code, issue.field_ref, issue.message)
        for issue in result_contract_validation.issues
    )
    flags = result.execution_flags
    expected_false = (
        "model_invoked",
        "network_invoked",
        "database_written",
        "fact_write",
        "decision_execute",
        "action_execute",
        "state_writeback",
        "memory_update",
        "model_training",
        "runtime_authorized",
    )
    if flags.runtime_executed is not True or flags.fixture_only is not True or flags.simulation_only is not True:
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "prototype_execution_scope_invalid", "execution_flags", "prototype must be executed only against the fixed local fixture"
        ))
    for flag_name in expected_false:
        if getattr(flags, flag_name) is not False:
            issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
                "forbidden_operation_present", f"execution_flags.{flag_name}", f"{flag_name} must be false"
            ))
    if not result.deterministic_output or not canonicalize_cognitive_analysis_runtime_prototype_result_v1(result).endswith("\n"):
        issues.append(CognitiveAnalysisRuntimePrototypeIssueV1(
            "determinism_declaration_invalid", "deterministic_output", "prototype output must declare canonical deterministic serialization"
        ))
    return CognitiveAnalysisRuntimePrototypeValidationResultV1(tuple(issues))
