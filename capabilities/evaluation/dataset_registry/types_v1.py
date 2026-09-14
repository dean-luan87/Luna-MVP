from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Tuple


DATASET_CLASSES = (
    "PUBLIC_BENCHMARK",
    "LUNA_SCENARIO",
    "FUTURE_REAL_OBSERVATION",
)
DATASET_LIFECYCLES = ("draft", "candidate", "active", "deprecated", "invalidated")
ANNOTATION_REVIEW_STATUSES = ("missing", "candidate", "in_review", "accepted", "rejected", "stale")
EVALUATION_USAGE = ("cognitive_evaluation", "capability_fitness", "regression", "benchmark", "quality_review")


@dataclass(frozen=True)
class DatasetRegistryEntryV1:
    dataset_id: str
    dataset_version: str
    dataset_class: str
    lifecycle: str
    modality_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    capability_refs: Tuple[str, ...]
    source_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    license_or_consent_refs: Tuple[str, ...]
    split_refs: Tuple[str, ...]
    annotation_schema_refs: Tuple[str, ...]
    declared_sample_count: int | None
    allowed_evaluation_usage: Tuple[str, ...]
    environment_condition_refs: Tuple[str, ...] = ()
    distribution_refs: Tuple[str, ...] = ()
    cognitive_difficulty_refs: Tuple[str, ...] = ()
    expected_observation_requirement_refs: Tuple[str, ...] = ()
    cognitive_test_case_refs: Tuple[str, ...] = ()
    invalidation_refs: Tuple[str, ...] = ()
    supersession_refs: Tuple[str, ...] = ()
    evaluation_only: bool = True
    runtime_allowed: bool = False


@dataclass(frozen=True)
class DatasetSampleManifestV1:
    sample_id: str
    dataset_ref: str
    dataset_version: str
    media_refs: Tuple[str, ...]
    media_type: str
    split_ref: str
    source_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    content_hash: str | None
    annotation_refs: Tuple[str, ...]
    environment_condition_refs: Tuple[str, ...]
    distribution_refs: Tuple[str, ...]
    cognitive_difficulty_refs: Tuple[str, ...]
    expected_observation_requirement_refs: Tuple[str, ...]
    allowed_evaluation_usage: Tuple[str, ...]
    cognitive_test_case_refs: Tuple[str, ...] = ()
    invalidation_refs: Tuple[str, ...] = ()
    evaluation_only: bool = True
    runtime_allowed: bool = False


@dataclass(frozen=True)
class AnnotationGroundTruthRefV1:
    annotation_id: str
    annotation_version: str
    sample_ref: str
    task_ref: str
    schema_ref: str
    payload_ref: str
    source_ref: str
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    review_status: str
    quality_ref: str | None
    completeness_ref: str | None
    invalidation_refs: Tuple[str, ...] = ()
    supersession_refs: Tuple[str, ...] = ()
    evaluation_ground_truth_only: bool = True
    world_truth: bool = False


@dataclass(frozen=True)
class BenchmarkSpecV1:
    benchmark_id: str
    benchmark_version: str
    dataset_refs: Tuple[str, ...]
    split_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    capability_refs: Tuple[str, ...]
    model_refs: Tuple[str, ...]
    provider_refs: Tuple[str, ...]
    metric_refs: Tuple[str, ...]
    ground_truth_required: bool
    reproducibility_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    evaluation_only: bool = True
    runtime_allowed: bool = False


@dataclass(frozen=True)
class DatasetRegistryV1:
    registry_id: str
    registry_version: str
    owner_ref: str
    entries: Tuple[DatasetRegistryEntryV1, ...] = ()
    sample_manifests: Tuple[DatasetSampleManifestV1, ...] = ()
    annotation_refs: Tuple[AnnotationGroundTruthRefV1, ...] = ()
    benchmark_specs: Tuple[BenchmarkSpecV1, ...] = ()
    evaluation_only: bool = True
    runtime_allowed: bool = False
    source_of_truth: str = "evaluation_governance"


def _missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip()) or value == () or value == []


def validate_dataset_registry_v1(registry: DatasetRegistryV1) -> Tuple[str, ...]:
    errors = []
    if registry.owner_ref != "Evaluation Governance":
        errors.append("owner_must_be_evaluation_governance")
    if not registry.evaluation_only or registry.runtime_allowed:
        errors.append("registry_runtime_boundary_invalid")
    if not registry.registry_id or not registry.registry_version:
        errors.append("registry_identity_or_version_missing")

    dataset_keys = [(entry.dataset_id, entry.dataset_version) for entry in registry.entries]
    if len(dataset_keys) != len(set(dataset_keys)):
        errors.append("duplicate_dataset_identity_version")
    sample_keys = [sample.sample_id for sample in registry.sample_manifests]
    if len(sample_keys) != len(set(sample_keys)):
        errors.append("duplicate_sample_id")

    for entry in registry.entries:
        required = (entry.dataset_id, entry.dataset_version, entry.source_ref, entry.provenance_refs, entry.source_version_refs)
        if any(_missing(value) for value in required):
            errors.append(f"dataset_required_field_missing:{entry.dataset_id}")
        if entry.dataset_class not in DATASET_CLASSES:
            errors.append(f"invalid_dataset_class:{entry.dataset_id}")
        if entry.lifecycle not in DATASET_LIFECYCLES:
            errors.append(f"invalid_dataset_lifecycle:{entry.dataset_id}")
        if entry.declared_sample_count is not None and entry.declared_sample_count < 0:
            errors.append(f"negative_sample_count:{entry.dataset_id}")
        if not entry.evaluation_only or entry.runtime_allowed:
            errors.append(f"dataset_runtime_boundary_invalid:{entry.dataset_id}")
        if any(usage not in EVALUATION_USAGE for usage in entry.allowed_evaluation_usage):
            errors.append(f"invalid_evaluation_usage:{entry.dataset_id}")

    for sample in registry.sample_manifests:
        required = (sample.sample_id, sample.dataset_ref, sample.dataset_version, sample.media_refs, sample.source_ref, sample.provenance_refs, sample.source_version_refs)
        if any(_missing(value) for value in required):
            errors.append(f"sample_required_field_missing:{sample.sample_id}")
        if not sample.evaluation_only or sample.runtime_allowed:
            errors.append(f"sample_runtime_boundary_invalid:{sample.sample_id}")

    for annotation in registry.annotation_refs:
        required = (annotation.annotation_id, annotation.annotation_version, annotation.sample_ref, annotation.schema_ref, annotation.payload_ref, annotation.provenance_refs, annotation.source_version_refs)
        if any(_missing(value) for value in required):
            errors.append(f"annotation_required_field_missing:{annotation.annotation_id}")
        if not annotation.evaluation_ground_truth_only or annotation.world_truth:
            errors.append(f"annotation_truth_boundary_invalid:{annotation.annotation_id}")
        if annotation.review_status not in ANNOTATION_REVIEW_STATUSES:
            errors.append(f"invalid_annotation_review_status:{annotation.annotation_id}")

    for benchmark in registry.benchmark_specs:
        required = (benchmark.benchmark_id, benchmark.benchmark_version, benchmark.dataset_refs, benchmark.task_refs, benchmark.metric_refs, benchmark.provenance_refs, benchmark.source_version_refs)
        if any(_missing(value) for value in required):
            errors.append(f"benchmark_required_field_missing:{benchmark.benchmark_id}")
        if not benchmark.evaluation_only or benchmark.runtime_allowed:
            errors.append(f"benchmark_runtime_boundary_invalid:{benchmark.benchmark_id}")
    return tuple(errors)

