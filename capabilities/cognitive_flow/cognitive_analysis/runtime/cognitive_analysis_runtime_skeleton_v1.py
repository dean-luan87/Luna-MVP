"""Non-executing candidate-envelope builder for A3 Runtime Skeleton v1."""

from __future__ import annotations

from .cognitive_analysis_runtime_interface_v1 import CognitiveAnalysisRuntimeInterfaceV1
from .cognitive_analysis_runtime_types_v1 import (
    CognitiveAnalysisRuntimeFlagsV1,
    CognitiveAnalysisRuntimeRequestV1,
    CognitiveAnalysisRuntimeSkeletonResultV1,
)
from .cognitive_analysis_runtime_validator_v1 import (
    validate_runtime_flags_v1,
    validate_runtime_request_v1,
)


class CognitiveAnalysisRuntimeSkeletonV1(CognitiveAnalysisRuntimeInterfaceV1):
    """Build a fixed skeleton envelope; it performs no cognitive analysis."""

    def execute(
        self,
        request: CognitiveAnalysisRuntimeRequestV1,
    ) -> CognitiveAnalysisRuntimeSkeletonResultV1:
        """Return a not-executed result without resolving any supplied reference."""
        flags = CognitiveAnalysisRuntimeFlagsV1()
        request_validation = validate_runtime_request_v1(request)
        flag_validation = validate_runtime_flags_v1(flags)
        issue_codes = tuple(issue.code for issue in request_validation.issues + flag_validation.issues)
        warnings = ("runtime_not_authorized", "runtime_skeleton_not_executed") + issue_codes
        return CognitiveAnalysisRuntimeSkeletonResultV1(
            analysis_result_candidate={
                "kind": "cognitive_analysis_result_candidate",
                "status": "not_executed",
                "context_ref": request.context_ref,
                "analysis_question_ref": request.analysis_question_ref,
            },
            evidence_trace={
                "context_refs": (request.context_ref,),
                "evidence_refs": request.evidence_refs,
                "hypothesis_refs": request.hypothesis_refs,
                "analysis_question_refs": (request.analysis_question_ref,),
            },
            uncertainty={
                "status": "not_evaluated",
                "reason": "runtime_skeleton_only",
            },
            warning_codes=warnings,
            runtime_flags=flags,
            validation_issue_codes=issue_codes,
        )
