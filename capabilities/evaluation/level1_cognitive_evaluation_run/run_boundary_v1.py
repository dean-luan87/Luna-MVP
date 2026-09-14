from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import uuid4

from capabilities.evaluation.dataset_registry.types_v1 import (
    DatasetRegistryV1,
    DatasetSampleManifestV1,
    validate_dataset_registry_v1,
)
from capabilities.evaluation.level1_field_cognition_suite.types_v1 import (
    Level1CognitiveTestCaseV1,
    validate_level1_case_v1,
)
from capabilities.evaluation.a_route_cognitive_whitebox_foundation.types_v1 import (
    CognitiveFailureGapRefV1,
    CognitiveWhiteBoxTraceV1,
    LunaCognitiveExecutionProfileV1,
    validate_gap_ref_v1,
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)

from .types_v1 import ARouteBridgeReadinessV1, WhiteBoxAttachmentV1


@dataclass(frozen=True)
class RunBoundaryValidationV1:
    valid: bool
    errors: Tuple[str, ...]
    dataset_registry_ref: str
    sample_ref: str
    cognitive_test_case_ref: str
    evaluation_only: bool = True
    runtime_execution_started: bool = False


def new_evaluation_run_execution_id_v1() -> str:
    """Create a unique execution instance identity for one Runner invocation."""
    return f"evaluation-run-execution:{uuid4().hex}"


def _dataset_matches_sample(dataset_id: str, dataset_version: str, dataset_ref: str) -> bool:
    return dataset_ref in {dataset_id, f"{dataset_id}:{dataset_version}"}


def validate_registered_case_inputs_v1(
    registry: DatasetRegistryV1,
    sample: DatasetSampleManifestV1,
    case: Level1CognitiveTestCaseV1,
) -> RunBoundaryValidationV1:
    errors = list(validate_dataset_registry_v1(registry))
    errors.extend(validate_level1_case_v1(case))
    dataset_entry = next(
        (
            entry
            for entry in registry.entries
            if _dataset_matches_sample(entry.dataset_id, entry.dataset_version, sample.dataset_ref)
        ),
        None,
    )
    if dataset_entry is None:
        errors.append("dataset_registry_membership_missing")
    if not any(item.sample_id == sample.sample_id for item in registry.sample_manifests):
        errors.append("sample_registry_membership_missing")
    if not sample.evaluation_only or sample.runtime_allowed:
        errors.append("sample_runtime_boundary_invalid")
    if dataset_entry is not None and sample.dataset_version != dataset_entry.dataset_version:
        errors.append("sample_dataset_version_mismatch")
    if dataset_entry is not None and not _dataset_matches_sample(dataset_entry.dataset_id, dataset_entry.dataset_version, case.dataset_ref):
        errors.append("case_dataset_linkage_mismatch")
    if case.world_sample_ref != sample.sample_id:
        errors.append("case_sample_linkage_mismatch")
    if case.cognitive_test_case_ref not in sample.cognitive_test_case_refs:
        errors.append("case_not_declared_by_sample")
    if dataset_entry is not None and case.cognitive_test_case_ref not in dataset_entry.cognitive_test_case_refs:
        errors.append("case_not_declared_by_dataset")
    if not case.goal_ref or not case.concern_ref:
        errors.append("goal_or_concern_missing")
    if not case.environment_condition_refs:
        errors.append("environment_condition_missing")
    if not case.perturbation_refs:
        errors.append("perturbation_declaration_missing")
    if not case.available_capability_refs:
        errors.append("capability_availability_missing")
    if any(sample.invalidation_refs) or (dataset_entry is not None and dataset_entry.invalidation_refs):
        errors.append("input_invalidation_present")
    return RunBoundaryValidationV1(
        valid=not errors,
        errors=tuple(dict.fromkeys(errors)),
        dataset_registry_ref=registry.registry_id,
        sample_ref=sample.sample_id,
        cognitive_test_case_ref=case.cognitive_test_case_ref,
    )


def require_registered_case_inputs_v1(
    registry: DatasetRegistryV1,
    sample: DatasetSampleManifestV1,
    case: Level1CognitiveTestCaseV1,
) -> RunBoundaryValidationV1:
    """Fail closed before a caller may construct an evaluation run candidate."""
    result = validate_registered_case_inputs_v1(registry, sample, case)
    if not result.valid:
        raise ValueError("evaluation_run_input_boundary_failed:" + ",".join(result.errors))
    return result


def attach_existing_whitebox_v1(
    case: Level1CognitiveTestCaseV1,
    trace: CognitiveWhiteBoxTraceV1,
    profile: LunaCognitiveExecutionProfileV1,
    gaps: Tuple[CognitiveFailureGapRefV1, ...] = (),
) -> WhiteBoxAttachmentV1:
    """Attach existing V1 records without creating or mutating cognition."""
    errors = [*validate_trace_contract_v1(trace), *validate_profile_contract_v1(profile)]
    errors.extend(error for gap in gaps for error in validate_gap_ref_v1(gap))
    if trace.test_case_ref != case.cognitive_test_case_ref:
        errors.append("whitebox_trace_case_mismatch")
    if profile.test_case_ref != case.cognitive_test_case_ref:
        errors.append("whitebox_profile_case_mismatch")
    if errors:
        raise ValueError("whitebox_attachment_failed:" + ",".join(errors))
    return WhiteBoxAttachmentV1(
        status="ATTACHED",
        trace_ref=trace.trace_id,
        execution_profile_ref=profile.execution_profile_id,
        gap_refs=tuple(gap.gap_id for gap in gaps),
        source_refs=(trace.trace_id, profile.execution_profile_id),
    )


def assess_a_route_bridge_readiness_v1(
    case: Level1CognitiveTestCaseV1,
    *,
    supplied_input_refs: Tuple[str, ...],
) -> ARouteBridgeReadinessV1:
    missing = (
        "real_a_route_cognitive_ingress",
        "runtime_cognitive_event_stream",
    )
    return ARouteBridgeReadinessV1(
        status="PARTIAL",
        target_ingress_ref="a-route:field-cognition:level1:ingress",
        supplied_input_refs=supplied_input_refs,
        missing_refs=missing,
    )
