"""Fixture-only A3 Runtime Prototype executor v1; no model, I/O, or writes."""

from __future__ import annotations

from capabilities.cognitive_flow.cognitive_analysis.result_contract.cognitive_analysis_result_contract_types_v1 import (
    FORBIDDEN_AUTHORITY_FLAGS_V1,
    CognitiveAnalysisResultCandidateV1,
)

from .cognitive_analysis_runtime_prototype_types_v1 import (
    RUNTIME_PROTOTYPE_PHASE_V1,
    CognitiveAnalysisRuntimePrototypeExecutionFlagsV1,
    CognitiveAnalysisRuntimePrototypeRequestV1,
    CognitiveAnalysisRuntimePrototypeResultV1,
)


FIXED_PROTOTYPE_FIXTURE_ID_V1 = "a3_runtime_prototype_fixed_reference_fixture_v1"


def build_fixed_runtime_prototype_fixture_v1() -> CognitiveAnalysisRuntimePrototypeRequestV1:
    """Return the immutable local fixture; no external reference is resolved or fetched."""
    return CognitiveAnalysisRuntimePrototypeRequestV1(
        analysis_id="a3-runtime-prototype-analysis-candidate-001",
        context_ref="current_cognitive_context:fixture:shopping_mall:v1",
        evidence_refs=("evidence:fixture:mall:entrance-status:v1",),
        analysis_question_ref="analysis_question:fixture:entrance-status:v1",
        fixture_id=FIXED_PROTOTYPE_FIXTURE_ID_V1,
    )


def execute_cognitive_analysis_runtime_prototype_v1(
    request: CognitiveAnalysisRuntimePrototypeRequestV1,
) -> CognitiveAnalysisRuntimePrototypeResultV1:
    """Build a deterministic candidate from supplied references without semantic inference."""
    authority_flags = {flag: False for flag in FORBIDDEN_AUTHORITY_FLAGS_V1}
    candidate = CognitiveAnalysisResultCandidateV1(
        analysis_id=request.analysis_id,
        input_reference=request.context_ref,
        evidence_reference=request.evidence_refs,
        analysis_type="uncertainty_assessment_candidate",
        candidate_output={
            "status": "prototype_reference_bound",
            "analysis_question_ref": request.analysis_question_ref,
            "meaning": "no_semantic_inference_performed",
        },
        uncertainty={
            "status": "unresolved",
            "reason_code": "prototype_fixture_no_semantic_inference",
        },
        provenance={
            "source_analysis_question_ref": request.analysis_question_ref,
            "context_ref": request.context_ref,
            "fixture_id": request.fixture_id,
            "trace_ref": "trace:a3-runtime-prototype:fixed-fixture:v1",
        },
        confidence=None,
        warning=("prototype_fixture_only", "semantic_inference_not_performed"),
        authority_flags=authority_flags,
    )
    return CognitiveAnalysisRuntimePrototypeResultV1(
        phase=RUNTIME_PROTOTYPE_PHASE_V1,
        fixture_id=request.fixture_id,
        input_trace=(
            request.context_ref,
            *request.evidence_refs,
            request.analysis_question_ref,
        ),
        analysis_result_candidate=candidate,
        execution_flags=CognitiveAnalysisRuntimePrototypeExecutionFlagsV1(),
        deterministic_output=True,
    )
