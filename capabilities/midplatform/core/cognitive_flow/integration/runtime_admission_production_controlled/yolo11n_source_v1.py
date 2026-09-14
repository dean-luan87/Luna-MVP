"""First repository-backed consumer of the generic Runtime Admission source."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.types_v1 import (
    GovernedExecutionRecordBundleV1,
)
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_readiness.yolo11n_readiness_types_v1 import (
    YOLO11N_ASSET_ID,
    YOLO11N_CAPABILITY_ID,
)

from .bundle_adapter_v1 import build_governed_execution_record_bundle_v1
from .producer_v1 import assess_runtime_admission_production_v1
from .repository_source_v1 import build_repository_runtime_admission_input_v1


YOLO11N_PROVIDER_FAMILY = "yolo"


def produce_repository_backed_yolo11n_bundle_v1(
    repo_root: Path,
) -> Tuple[Optional[GovernedExecutionRecordBundleV1], Optional[str], Tuple[str, ...]]:
    data = build_repository_runtime_admission_input_v1(
        repo_root,
        model_asset_id=YOLO11N_ASSET_ID,
        capability_id="object_detection",
        provider_family=YOLO11N_PROVIDER_FAMILY,
    )
    if data is None:
        return None, "RUNTIME_ADMISSION_REPOSITORY_INPUT_MISSING", ()
    result = assess_runtime_admission_production_v1(data)
    bundle = build_governed_execution_record_bundle_v1(data, result)
    if bundle is None:
        failure = result.failure.classification if result.failure else "GOVERNED_BUNDLE_NOT_FORMED"
        return None, failure, result.source_refs
    return bundle, None, result.source_refs


__all__ = ["produce_repository_backed_yolo11n_bundle_v1"]
