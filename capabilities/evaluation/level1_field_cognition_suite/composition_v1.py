from __future__ import annotations

from typing import Iterable, Tuple

from capabilities.evaluation.dataset_registry.types_v1 import DatasetSampleManifestV1

from .types_v1 import (
    CognitiveEvaluationAssertionV1,
    ControlledPerturbationV1,
    Level1CognitiveTestCaseV1,
    validate_assertion_v1,
    validate_level1_case_v1,
)


def compose_level1_cognitive_test_case_v1(
    sample: DatasetSampleManifestV1,
    *,
    cognitive_test_case_ref: str,
    version: str,
    cognitive_task_ref: str,
    goal_ref: str,
    concern_ref: str,
    role_ref: str | None,
    environment_condition_refs: Tuple[str, ...],
    cognitive_difficulty_refs: Tuple[str, ...],
    perturbations: Iterable[ControlledPerturbationV1],
    available_capability_refs: Tuple[str, ...],
    observation_budget_ref: str,
    expected_observation_requirement_refs: Tuple[str, ...],
    world_ground_truth_refs: Tuple[str, ...],
    observation_ground_truth_refs: Tuple[str, ...],
    assertions: Iterable[CognitiveEvaluationAssertionV1],
    cognitive_trace_ref: str | None = None,
    execution_profile_ref: str | None = None,
) -> Level1CognitiveTestCaseV1:
    """Compose refs from an explicitly registered sample; never loads media."""
    if not sample.evaluation_only or sample.runtime_allowed:
        raise ValueError("sample_not_evaluation_only")
    perturbation_items = tuple(perturbations)
    assertion_items = tuple(assertions)
    if any(item.applied_by_runtime for item in perturbation_items):
        raise ValueError("runtime_perturbation_execution_forbidden")
    assertion_errors = tuple(error for item in assertion_items for error in validate_assertion_v1(item))
    if assertion_errors:
        raise ValueError("assertion_validation_failed:" + ",".join(assertion_errors))
    case = Level1CognitiveTestCaseV1(
        cognitive_test_case_ref=cognitive_test_case_ref,
        version=version,
        world_sample_ref=sample.sample_id,
        dataset_ref=sample.dataset_ref,
        cognitive_task_ref=cognitive_task_ref,
        goal_ref=goal_ref,
        concern_ref=concern_ref,
        role_ref=role_ref,
        environment_condition_refs=environment_condition_refs,
        cognitive_difficulty_refs=cognitive_difficulty_refs,
        perturbation_refs=tuple(item.perturbation_id for item in perturbation_items),
        available_capability_refs=available_capability_refs,
        observation_budget_ref=observation_budget_ref,
        expected_observation_requirement_refs=expected_observation_requirement_refs,
        world_ground_truth_refs=world_ground_truth_refs,
        observation_ground_truth_refs=observation_ground_truth_refs,
        cognitive_assertion_refs=tuple(item.assertion_id for item in assertion_items),
        cognitive_trace_ref=cognitive_trace_ref,
        execution_profile_ref=execution_profile_ref,
    )
    errors = validate_level1_case_v1(case)
    if errors:
        raise ValueError("cognitive_case_validation_failed:" + ",".join(errors))
    return case

