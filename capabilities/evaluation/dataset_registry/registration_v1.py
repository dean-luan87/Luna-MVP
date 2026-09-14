from __future__ import annotations

from dataclasses import replace
from pathlib import PurePosixPath
from typing import Iterable, Tuple

from .types_v1 import (
    AnnotationGroundTruthRefV1,
    BenchmarkSpecV1,
    DatasetRegistryEntryV1,
    DatasetRegistryV1,
    DatasetSampleManifestV1,
    validate_dataset_registry_v1,
)


FORBIDDEN_AUTO_PROMOTION_ROOTS = (
    "_tmp_eval_inputs",
    "_tmp_eval_out",
    "_eval_out",
)


def _is_forbidden_generated_ref(ref: str) -> bool:
    parts = PurePosixPath(str(ref)).parts
    return any(root in parts for root in FORBIDDEN_AUTO_PROMOTION_ROOTS)


def register_explicit_dataset_v1(
    registry: DatasetRegistryV1,
    entry: DatasetRegistryEntryV1,
    *,
    samples: Iterable[DatasetSampleManifestV1] = (),
    annotations: Iterable[AnnotationGroundTruthRefV1] = (),
    benchmarks: Iterable[BenchmarkSpecV1] = (),
    explicit_registration: bool = False,
    directory_scan_used: bool = False,
) -> DatasetRegistryV1:
    """Pure explicit-registration bridge; never scans or loads media.

    The caller supplies owner-controlled declarations. Generated evaluation
    roots are rejected so temporary output cannot become corpus source-of-truth.
    """
    if not explicit_registration:
        raise ValueError("explicit_registration_required")
    if directory_scan_used:
        raise ValueError("directory_scan_cannot_promote_dataset")
    if _is_forbidden_generated_ref(entry.source_ref):
        raise ValueError("generated_artifact_cannot_be_dataset_source")
    sample_items: Tuple[DatasetSampleManifestV1, ...] = tuple(samples)
    annotation_items: Tuple[AnnotationGroundTruthRefV1, ...] = tuple(annotations)
    benchmark_items: Tuple[BenchmarkSpecV1, ...] = tuple(benchmarks)
    if any(_is_forbidden_generated_ref(ref) for sample in sample_items for ref in (sample.source_ref, *sample.media_refs)):
        raise ValueError("generated_artifact_cannot_be_sample_source")
    candidate = replace(
        registry,
        entries=(*registry.entries, entry),
        sample_manifests=(*registry.sample_manifests, *sample_items),
        annotation_refs=(*registry.annotation_refs, *annotation_items),
        benchmark_specs=(*registry.benchmark_specs, *benchmark_items),
    )
    errors = validate_dataset_registry_v1(candidate)
    if errors:
        raise ValueError("dataset_registry_validation_failed:" + ",".join(errors))
    return candidate

