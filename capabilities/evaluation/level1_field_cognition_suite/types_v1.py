from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple


COGNITIVE_ASSERTION_KINDS = (
    "MUST_NOT_DECLARE_SUFFICIENT_WITH_REQUIRED_INFORMATION_MISSING",
    "MUST_PRESERVE_UNCERTAINTY",
    "MUST_NOT_PROMOTE_PROVIDER_OUTPUT_TO_WORLD_TRUTH",
    "MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED",
    "MUST_REOBSERVE_WHEN_REQUIRED",
    "MUST_NOT_REOBSERVE_WITHOUT_JUSTIFICATION",
    "MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS",
    "MUST_PRESERVE_OWNER_BOUNDARIES",
)

PERTURBATION_KINDS = (
    "baseline",
    "irrelevant_clutter",
    "missing_evidence",
    "partial_occlusion",
    "false_evidence",
    "conflicting_evidence",
    "stale_evidence",
    "duplicate_evidence",
    "delayed_evidence",
    "viewpoint_variation",
    "lighting_variation",
    "target_count_variation",
    "distractor_similarity",
    "wrong_attention",
    "capability_unavailable",
    "observation_budget_restriction",
)

FAILURE_ATTRIBUTIONS = (
    "LUNA_COGNITIVE",
    "EXTERNAL_CAPABILITY",
    "PROVIDER",
    "NORMALIZATION",
    "DATASET_OR_GT",
    "EVALUATION_INFRASTRUCTURE",
    "GOVERNANCE_COMPLIANCE",
    "UNRESOLVED",
)


@dataclass(frozen=True)
class WorldGroundTruthRefV1:
    ground_truth_id: str
    version: str
    sample_ref: str
    fact_schema_ref: str
    fact_refs: Tuple[str, ...]
    source_ref: str
    provenance_refs: Tuple[str, ...]
    review_status: str
    evaluation_only: bool = True
    world_truth_forbidden: bool = True


@dataclass(frozen=True)
class ObservationGroundTruthRefV1:
    observation_ground_truth_id: str
    version: str
    sample_ref: str
    observation_ref: str
    visible_fact_refs: Tuple[str, ...]
    occluded_fact_refs: Tuple[str, ...]
    outside_roi_refs: Tuple[str, ...]
    ambiguous_fact_refs: Tuple[str, ...]
    source_ref: str
    provenance_refs: Tuple[str, ...]
    evaluation_only: bool = True


@dataclass(frozen=True)
class CognitiveEvaluationAssertionV1:
    assertion_id: str
    assertion_kind: str
    rationale_ref: str
    affected_node_kinds: Tuple[str, ...]
    required_process_class: str
    forbidden_semantic_answer: bool = True
    evaluation_only: bool = True


@dataclass(frozen=True)
class ControlledPerturbationV1:
    perturbation_id: str
    perturbation_kind: str
    source_ref: str
    version: str
    target_refs: Tuple[str, ...]
    expected_effect_refs: Tuple[str, ...]
    deterministic: bool
    applied_by_runtime: bool = False


@dataclass(frozen=True)
class Level1CognitiveTestCaseV1:
    cognitive_test_case_ref: str
    version: str
    world_sample_ref: str
    dataset_ref: str
    cognitive_task_ref: str
    goal_ref: str
    concern_ref: str
    role_ref: str | None
    environment_condition_refs: Tuple[str, ...]
    cognitive_difficulty_refs: Tuple[str, ...]
    perturbation_refs: Tuple[str, ...]
    available_capability_refs: Tuple[str, ...]
    observation_budget_ref: str
    expected_observation_requirement_refs: Tuple[str, ...]
    world_ground_truth_refs: Tuple[str, ...]
    observation_ground_truth_refs: Tuple[str, ...]
    cognitive_assertion_refs: Tuple[str, ...]
    cognitive_trace_ref: str | None
    execution_profile_ref: str | None
    evaluation_only: bool = True
    runtime_execution_allowed: bool = False


@dataclass(frozen=True)
class PlaneAResultRefV1:
    result_ref: str
    status: str
    cognitive_trace_ref: str
    execution_profile_ref: str
    assertion_result_refs: Tuple[str, ...]
    completion_candidate_ref: str | None
    evaluation_only: bool = True


@dataclass(frozen=True)
class PlaneBObservationRefV1:
    result_ref: str
    capability_ref: str
    implementation_ref: str
    provider_ref: str
    evidence_refs: Tuple[str, ...]
    fitness_metric_refs: Tuple[str, ...]
    failure_refs: Tuple[str, ...]
    evaluation_only: bool = True


@dataclass(frozen=True)
class DualPlaneEvaluationResultV1:
    evaluation_id: str
    cognitive_test_case_ref: str
    plane_a_result_ref: str
    plane_b_observation_ref: str
    failure_attribution: str
    attribution_evidence_refs: Tuple[str, ...]
    unresolved_reason: str | None
    evaluation_only: bool = True


def validate_dual_plane_result_v1(result: DualPlaneEvaluationResultV1) -> Tuple[str, ...]:
    errors = []
    if result.failure_attribution not in FAILURE_ATTRIBUTIONS:
        errors.append(f"invalid_failure_attribution:{result.failure_attribution}")
    if not result.evaluation_only:
        errors.append("dual_plane_result_not_evaluation_only")
    if not result.plane_a_result_ref or not result.plane_b_observation_ref:
        errors.append("dual_plane_result_ref_missing")
    if result.failure_attribution == "UNRESOLVED" and not result.unresolved_reason:
        errors.append("unresolved_attribution_reason_missing")
    return tuple(errors)


def validate_level1_case_v1(case: Level1CognitiveTestCaseV1) -> Tuple[str, ...]:
    errors = []
    required = (
        case.cognitive_test_case_ref,
        case.version,
        case.world_sample_ref,
        case.dataset_ref,
        case.cognitive_task_ref,
        case.goal_ref,
        case.concern_ref,
        case.observation_budget_ref,
    )
    if any(not str(value).strip() for value in required):
        errors.append("case_required_ref_missing")
    if not case.cognitive_assertion_refs:
        errors.append("cognitive_assertions_missing")
    if not case.available_capability_refs:
        errors.append("available_capabilities_missing")
    if not case.evaluation_only or case.runtime_execution_allowed:
        errors.append("case_runtime_boundary_invalid")
    return tuple(errors)


def validate_assertion_v1(assertion: CognitiveEvaluationAssertionV1) -> Tuple[str, ...]:
    errors = []
    if assertion.assertion_kind not in COGNITIVE_ASSERTION_KINDS:
        errors.append(f"invalid_assertion_kind:{assertion.assertion_kind}")
    if not assertion.forbidden_semantic_answer or not assertion.evaluation_only:
        errors.append(f"assertion_semantic_boundary_invalid:{assertion.assertion_id}")
    return tuple(errors)
