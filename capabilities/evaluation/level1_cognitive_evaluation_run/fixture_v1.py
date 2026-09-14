from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.evaluation.a_route_cognitive_whitebox_foundation.adapters_v1 import (
    build_luna_cognitive_execution_profile_v1,
)
from capabilities.evaluation.a_route_cognitive_whitebox_foundation.fixtures_v1 import (
    build_synthetic_cognitive_trace_cases_v1,
)
from capabilities.evaluation.a_route_cognitive_whitebox_foundation.types_v1 import (
    CognitiveWhiteBoxTraceV1,
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)
from capabilities.evaluation.dataset_registry.types_v1 import (
    DatasetRegistryEntryV1,
    DatasetRegistryV1,
    DatasetSampleManifestV1,
)
from capabilities.evaluation.level1_field_cognition_suite.composition_v1 import (
    compose_level1_cognitive_test_case_v1,
)
from capabilities.evaluation.level1_field_cognition_suite.types_v1 import (
    CognitiveEvaluationAssertionV1,
    ControlledPerturbationV1,
)

from .run_boundary_v1 import (
    assess_a_route_bridge_readiness_v1,
    attach_existing_whitebox_v1,
    new_evaluation_run_execution_id_v1,
    require_registered_case_inputs_v1,
)
from .types_v1 import (
    ARouteBridgeReadinessV1,
    EvaluationAvailabilityV1,
    EvaluationRunCandidateV1,
    EvaluationRunRecordV1,
    WhiteBoxAttachmentV1,
)


@dataclass(frozen=True)
class SyntheticEvaluationFixtureV1:
    registry: DatasetRegistryV1
    sample: DatasetSampleManifestV1
    case: object
    trace: CognitiveWhiteBoxTraceV1
    profile: object
    boundary: object
    bridge: ARouteBridgeReadinessV1
    whitebox: WhiteBoxAttachmentV1
    record: EvaluationRunRecordV1


def _registry_and_sample() -> Tuple[DatasetRegistryV1, DatasetSampleManifestV1]:
    dataset_id = "dataset:synthetic:level1:world"
    dataset_version = "v1"
    sample_id = "sample:synthetic:level1:decision-governance-handoff:v1"
    case_ref = "test-case:decision_governance_handoff:v1"
    loop_case_refs = (
        "test-case:minimum_sufficient_cognition:case-a:v1",
        "test-case:minimum_sufficient_cognition:case-b:v1",
    )
    entry = DatasetRegistryEntryV1(
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        dataset_class="LUNA_SCENARIO",
        lifecycle="candidate",
        modality_refs=("image",),
        task_refs=("field_cognition",),
        capability_refs=("capability:object_detection:v1",),
        source_ref="synthetic-fixture:level1-world",
        provenance_refs=("provenance:synthetic-fixture:v1",),
        source_version_refs=("synthetic-fixture-source:v1",),
        license_or_consent_refs=("synthetic-fixture-license:v1",),
        split_refs=("split:diagnostic",),
        annotation_schema_refs=("schema:world-ground-truth:v1",),
        declared_sample_count=1,
        allowed_evaluation_usage=("cognitive_evaluation",),
        environment_condition_refs=("condition:indoor:stable",),
        distribution_refs=("distribution:synthetic:diagnostic",),
        cognitive_difficulty_refs=("difficulty:obvious",),
        expected_observation_requirement_refs=("observation:single-cycle",),
        cognitive_test_case_refs=(case_ref, *loop_case_refs),
    )


    sample = DatasetSampleManifestV1(
        sample_id=sample_id,
        dataset_ref=f"{dataset_id}:{dataset_version}",
        dataset_version=dataset_version,
        media_refs=("synthetic-media:obvious-field:v1",),
        media_type="image",
        split_ref="split:diagnostic",
        source_ref="synthetic-fixture:level1-world/sample",
        provenance_refs=("provenance:synthetic-fixture:v1",),
        source_version_refs=("synthetic-fixture-source:v1",),
        content_hash="synthetic-hash:not-content-addressed",
        annotation_refs=("annotation:synthetic-world:v1",),
        environment_condition_refs=("condition:indoor:stable",),
        distribution_refs=("distribution:synthetic:diagnostic",),
        cognitive_difficulty_refs=("difficulty:obvious",),
        expected_observation_requirement_refs=("observation:single-cycle",),
        allowed_evaluation_usage=("cognitive_evaluation",),
        cognitive_test_case_refs=(case_ref, *loop_case_refs),
    )
    return (
        DatasetRegistryV1(
            registry_id="luna-evaluation-world-observation-corpus-registry",
            registry_version="v1",
            owner_ref="Evaluation Governance",
            entries=(entry,),
            sample_manifests=(sample,),
            source_of_truth="evaluation_governance",
        ),
        sample,
    )


def build_registered_level1_case_inputs_v1() -> Tuple[
    DatasetRegistryV1,
    DatasetSampleManifestV1,
    object,
]:
    """Return the registered sample/case without constructing a White-box fixture."""
    registry, sample = _registry_and_sample()
    assertion = CognitiveEvaluationAssertionV1(
        assertion_id="assertion:synthetic:minimum-sufficient:v1",
        assertion_kind="MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS",
        rationale_ref="rationale:synthetic:minimum-sufficient:v1",
        affected_node_kinds=("SUFFICIENCY", "STOP_REASON"),
        required_process_class="minimum_sufficient_cognition",
    )
    perturbation = ControlledPerturbationV1(
        perturbation_id="perturbation:synthetic:baseline:v1",
        perturbation_kind="baseline",
        source_ref="synthetic-fixture:baseline",
        version="v1",
        target_refs=(sample.sample_id,),
        expected_effect_refs=("effect:no_controlled_perturbation",),
        deterministic=True,
    )
    case = compose_level1_cognitive_test_case_v1(
        sample,
        cognitive_test_case_ref="test-case:decision_governance_handoff:v1",
        version="v1",
        cognitive_task_ref="task:decision_governance_handoff",
        goal_ref="goal:decision_governance_handoff",
        concern_ref="concern:decision_governance_handoff",
        role_ref="role:synthetic:observer",
        environment_condition_refs=("condition:indoor:stable",),
        cognitive_difficulty_refs=("difficulty:obvious",),
        perturbations=(perturbation,),
        available_capability_refs=("capability:object_detection:v1",),
        observation_budget_ref="budget:single-cycle",
        expected_observation_requirement_refs=("observation:single-cycle",),
        world_ground_truth_refs=("ground-truth:synthetic:world:v1",),
        observation_ground_truth_refs=("ground-truth:synthetic:observation:v1",),
        assertions=(assertion,),
    )
    return registry, sample, case


def build_minimum_sufficient_loop_case_inputs_v1() -> Tuple[
    DatasetRegistryV1,
    DatasetSampleManifestV1,
    Tuple[object, object],
]:
    """Return the two registered loop cases without constructing White-box data."""
    registry, sample = _registry_and_sample()

    def compose(case_ref: str, case_id: str, perturbation_kind: str):
        assertion = CognitiveEvaluationAssertionV1(
            assertion_id=f"assertion:{case_id}:minimum-sufficient:v1",
            assertion_kind="MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS",
            rationale_ref=f"rationale:{case_id}:minimum-sufficient:v1",
            affected_node_kinds=("SUFFICIENCY", "STOP_REASON", "INFORMATION_GAP", "REOBSERVATION", "HYPOTHESIS_REVISION"),
            required_process_class="minimum_sufficient_cognition",
        )
        perturbation = ControlledPerturbationV1(
            perturbation_id=f"perturbation:{case_id}:v1",
            perturbation_kind=perturbation_kind,
            source_ref="synthetic-fixture:minimum-sufficient-loop",
            version="v1",
            target_refs=(sample.sample_id,),
            expected_effect_refs=(f"effect:{case_id}:controlled-replay",),
            deterministic=True,
        )
        return compose_level1_cognitive_test_case_v1(
            sample,
            cognitive_test_case_ref=case_ref,
            version="v1",
            cognitive_task_ref=f"task:{case_id}",
            goal_ref=f"goal:{case_id}",
            concern_ref=f"concern:{case_id}",
            role_ref="role:synthetic:observer",
            environment_condition_refs=("condition:indoor:stable",),
            cognitive_difficulty_refs=("difficulty:obvious",),
            perturbations=(perturbation,),
            available_capability_refs=("capability:object_detection:v1",),
            observation_budget_ref="budget:single-cycle",
            expected_observation_requirement_refs=("observation:single-cycle",),
            world_ground_truth_refs=("ground-truth:synthetic:world:v1",),
            observation_ground_truth_refs=("ground-truth:synthetic:observation:v1",),
            assertions=(assertion,),
        )

    return (
        registry,
        sample,
        (
            compose("test-case:minimum_sufficient_cognition:case-a:v1", "case-a-sufficient-stop", "baseline"),
            compose("test-case:minimum_sufficient_cognition:case-b:v1", "case-b-gap-reobserve-revise-stop", "missing_evidence"),
        ),
    )


def build_synthetic_evaluation_fixture_v1(
    *, evaluation_run_id: str | None = None,
) -> SyntheticEvaluationFixtureV1:
    registry, sample = _registry_and_sample()
    assertion = CognitiveEvaluationAssertionV1(
        assertion_id="assertion:synthetic:minimum-sufficient:v1",
        assertion_kind="MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS",
        rationale_ref="rationale:synthetic:minimum-sufficient:v1",
        affected_node_kinds=("SUFFICIENCY", "STOP_REASON"),
        required_process_class="minimum_sufficient_cognition",
    )
    perturbation = ControlledPerturbationV1(
        perturbation_id="perturbation:synthetic:baseline:v1",
        perturbation_kind="baseline",
        source_ref="synthetic-fixture:baseline",
        version="v1",
        target_refs=(sample.sample_id,),
        expected_effect_refs=("effect:no_controlled_perturbation",),
        deterministic=True,
    )
    case = compose_level1_cognitive_test_case_v1(
        sample,
        cognitive_test_case_ref="test-case:decision_governance_handoff:v1",
        version="v1",
        cognitive_task_ref="task:decision_governance_handoff",
        goal_ref="goal:decision_governance_handoff",
        concern_ref="concern:decision_governance_handoff",
        role_ref="role:synthetic:observer",
        environment_condition_refs=("condition:indoor:stable",),
        cognitive_difficulty_refs=("difficulty:obvious",),
        perturbations=(perturbation,),
        available_capability_refs=("capability:object_detection:v1",),
        observation_budget_ref="budget:single-cycle",
        expected_observation_requirement_refs=("observation:single-cycle",),
        world_ground_truth_refs=("ground-truth:synthetic:world:v1",),
        observation_ground_truth_refs=("ground-truth:synthetic:observation:v1",),
        assertions=(assertion,),
    )
    trace_case = next(
        item for item in build_synthetic_cognitive_trace_cases_v1()
        if item.scenario_id == "decision_governance_handoff"
    )
    trace = trace_case.trace
    profile = build_luna_cognitive_execution_profile_v1(trace)
    trace_errors = validate_trace_contract_v1(trace)
    profile_errors = validate_profile_contract_v1(profile)
    if trace_errors or profile_errors:
        raise ValueError("synthetic_whitebox_fixture_invalid:" + ",".join((*trace_errors, *profile_errors)))
    boundary = require_registered_case_inputs_v1(registry, sample, case)
    bridge = assess_a_route_bridge_readiness_v1(
        case,
        supplied_input_refs=(sample.sample_id, case.cognitive_test_case_ref, trace.trace_id),
    )
    whitebox = attach_existing_whitebox_v1(case, trace, profile)
    run_id = evaluation_run_id or (
        "evaluation-run:synthetic:level1:decision-governance-handoff:"
        + new_evaluation_run_execution_id_v1()
    )
    run = EvaluationRunCandidateV1(
        evaluation_run_id=run_id,
        evaluation_protocol_version="level1-cognitive-evaluation-run:v1",
        plane="PLANE_A_LUNA_COGNITIVE",
        cognitive_level="LEVEL_1_FIELD_COGNITION",
        dataset_ref=sample.dataset_ref,
        dataset_version=sample.dataset_version,
        sample_ref=sample.sample_id,
        sample_version="v1",
        cognitive_test_case_ref=case.cognitive_test_case_ref,
        cognitive_test_case_version=case.version,
        luna_code_version_ref=EvaluationAvailabilityV1(None, "unavailable", notes="synthetic fixture does not assert a Luna code version"),
        luna_config_version_ref=EvaluationAvailabilityV1(None, "unavailable", notes="synthetic fixture does not assert a Luna config version"),
        environment_condition_refs=case.environment_condition_refs,
        perturbation_refs=case.perturbation_refs,
        available_capability_refs=case.available_capability_refs,
        observation_budget_ref=case.observation_budget_ref,
        started_at=EvaluationAvailabilityV1(None, "not_observed", notes="no runtime execution"),
        completed_at=EvaluationAvailabilityV1(None, "not_observed", notes="no runtime execution"),
        execution_mode="synthetic_candidate",
        trace_ref=whitebox.trace_ref,
        execution_profile_ref=whitebox.execution_profile_ref,
        gap_refs=whitebox.gap_refs,
        result_status="NOT_EXECUTED_CANDIDATE_ONLY",
        failure_attribution_refs=(),
        invalidation_refs=(),
        provenance_refs=("provenance:synthetic-fixture:v1", trace.trace_id),
        source_version_refs=("synthetic-fixture-source:v1",),
        a_route_bridge_status=bridge.status,
        whitebox_attachment_status=whitebox.status,
        comparison_eligibility=EvaluationAvailabilityV1(None, "planned", notes="comparison requires a later real run and stable Luna version refs"),
        runtime_metrics=EvaluationAvailabilityV1(None, "not_observed", notes="runtime metrics are not collected by this synthetic fixture"),
    )
    record = EvaluationRunRecordV1(
        record_id=f"evaluation-record:{run_id}:v1",
        record_version="v1",
        evaluation_run=run,
        test_board_refs=("test-board-ref:synthetic-evaluation-run:v1",),
        bounded_metadata={
            "fixture_kind": "synthetic_registered_sample_case",
            "cognition_result_is_not_claimed": True,
            "archive_role": "durable_evaluation_history_candidate",
        },
    )
    return SyntheticEvaluationFixtureV1(registry, sample, case, trace, profile, boundary, bridge, whitebox, record)
