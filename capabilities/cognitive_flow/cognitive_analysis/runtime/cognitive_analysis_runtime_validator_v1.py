"""Pure static input and boundary validation for the A3 Runtime Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .cognitive_analysis_runtime_types_v1 import (
    COGNITIVE_ANALYSIS_RUNTIME_SCHEMA_VERSION_V1,
    CognitiveAnalysisRuntimeFlagsV1,
    CognitiveAnalysisRuntimeRequestV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeValidationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeValidationResultV1:
    issues: Tuple[CognitiveAnalysisRuntimeValidationIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def _missing_reference_issues_v1(
    field_ref: str,
    references: Tuple[str, ...],
) -> Tuple[CognitiveAnalysisRuntimeValidationIssueV1, ...]:
    return tuple(
        CognitiveAnalysisRuntimeValidationIssueV1(
            "missing_reference",
            field_ref,
            f"{field_ref}[{index}] must be a non-empty reference",
        )
        for index, reference in enumerate(references)
        if not isinstance(reference, str) or not reference.strip()
    )


def validate_runtime_request_v1(
    request: CognitiveAnalysisRuntimeRequestV1,
) -> CognitiveAnalysisRuntimeValidationResultV1:
    """Validate references only; never fetch, resolve, or execute them."""
    issues = []
    if request.schema_version != COGNITIVE_ANALYSIS_RUNTIME_SCHEMA_VERSION_V1:
        issues.append(CognitiveAnalysisRuntimeValidationIssueV1(
            "invalid_schema_version",
            "schema_version",
            "request must use the controlled runtime skeleton schema version",
        ))
    for field_ref, reference in (
        ("context_ref", request.context_ref),
        ("analysis_question_ref", request.analysis_question_ref),
    ):
        if not isinstance(reference, str) or not reference.strip():
            issues.append(CognitiveAnalysisRuntimeValidationIssueV1(
                "missing_reference",
                field_ref,
                f"{field_ref} must be a non-empty reference",
            ))
    issues.extend(_missing_reference_issues_v1("evidence_refs", request.evidence_refs))
    issues.extend(_missing_reference_issues_v1("hypothesis_refs", request.hypothesis_refs))
    return CognitiveAnalysisRuntimeValidationResultV1(tuple(issues))


def validate_runtime_flags_v1(
    flags: CognitiveAnalysisRuntimeFlagsV1,
) -> CognitiveAnalysisRuntimeValidationResultV1:
    """Reject any flag that would turn the controlled skeleton into Runtime work."""
    expected = {
        "runtime_executed": False,
        "simulation_only": True,
        "model_invoked": False,
        "network_invoked": False,
        "database_invoked": False,
        "state_writeback": False,
        "decision_executed": False,
    }
    issues = tuple(
        CognitiveAnalysisRuntimeValidationIssueV1(
            "runtime_boundary_flag_violation",
            name,
            f"{name} must remain {required!r} for the controlled skeleton",
        )
        for name, required in expected.items()
        if getattr(flags, name) is not required
    )
    return CognitiveAnalysisRuntimeValidationResultV1(issues)
