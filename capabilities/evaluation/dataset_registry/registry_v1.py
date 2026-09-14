from __future__ import annotations

from .types_v1 import DatasetRegistryV1


REGISTRY_ID = "luna-evaluation-world-observation-corpus-registry"
REGISTRY_VERSION = "v1"
REGISTRY_OWNER = "Evaluation Governance"


def build_empty_dataset_registry_v1() -> DatasetRegistryV1:
    """Return the unregistered foundation baseline; no data is discovered or loaded."""
    return DatasetRegistryV1(
        registry_id=REGISTRY_ID,
        registry_version=REGISTRY_VERSION,
        owner_ref=REGISTRY_OWNER,
        entries=(),
        sample_manifests=(),
        annotation_refs=(),
        benchmark_specs=(),
        evaluation_only=True,
        runtime_allowed=False,
        source_of_truth="evaluation_governance",
    )

