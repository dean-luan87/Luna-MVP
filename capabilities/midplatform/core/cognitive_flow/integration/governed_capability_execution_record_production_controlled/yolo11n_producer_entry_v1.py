"""YOLO11n repository-backed entrypoint for the generic producer seam."""

from __future__ import annotations

from pathlib import Path

from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_readiness.yolo11n_readiness_types_v1 import (
    YOLO11N_ASSET_ID,
    YOLO11N_CAPABILITY_ID,
)
from capabilities.midplatform.field_perception_orchestrator.integration.canonical_yolo11n_context_builder_v1 import (
    CanonicalYOLO11nUpstreamRecordsV1,
)

from .producer_v1 import produce_governed_execution_records_v1
from .types_v1 import GovernedExecutionRecordBundleV1, GovernedRecordProductionResultV1


YOLO11N_PROVIDER_FAMILY = "yolo"


def produce_yolo11n_governed_execution_records_v1(repo_root: Path) -> GovernedRecordProductionResultV1:
    result = produce_governed_execution_records_v1(
        repo_root,
        target_model_asset_id=YOLO11N_ASSET_ID,
        target_capability_contract_id=YOLO11N_CAPABILITY_ID,
        target_provider_family=YOLO11N_PROVIDER_FAMILY,
    )
    if result.bundle is not None or result.inventory.missing_declarations:
        return result
    from capabilities.midplatform.core.cognitive_flow.integration.runtime_admission_production_controlled.yolo11n_source_v1 import (
        produce_repository_backed_yolo11n_bundle_v1,
    )

    bundle, failure, source_refs = produce_repository_backed_yolo11n_bundle_v1(repo_root)
    if bundle is None:
        return GovernedRecordProductionResultV1(
            status="BLOCKED_BY_RUNTIME_ADMISSION_PRODUCTION_SOURCE",
            inventory=result.inventory,
            bundle=None,
            missing_declarations=(failure or "OWNER_ISSUED_GOVERNED_RECORD_BUNDLE",),
            responsible_owners=("Runtime Admission", "Capability Governance", "Provider Governance"),
            trace_refs=("trace:governed-record-production:runtime-admission-blocked",),
            provenance_refs=source_refs or result.provenance_refs,
        )
    return GovernedRecordProductionResultV1(
        status="REPOSITORY_BACKED_VALIDATION_BUNDLE_PRODUCED",
        inventory=result.inventory,
        bundle=bundle,
        missing_declarations=(),
        responsible_owners=("Capability Governance", "Model Governance", "Runtime Admission", "Provider Governance"),
        trace_refs=bundle.trace_refs,
        provenance_refs=bundle.provenance_refs,
    )


def adapt_governed_bundle_to_canonical_yolo11n_records_v1(
    bundle: GovernedExecutionRecordBundleV1,
) -> CanonicalYOLO11nUpstreamRecordsV1 | None:
    """Translate only a complete owner-issued bundle; never fill missing refs."""

    required = (
        bundle.capability_resolution,
        bundle.capability_model_binding,
        bundle.runtime_admission_assessment,
        bundle.executable_capability,
        bundle.model_provider_binding,
        bundle.runtime_admission_ref,
        bundle.runtime_admission_version,
        bundle.source_version_refs,
        bundle.trace_refs,
        bundle.provenance_refs,
    )
    if any(value in (None, "", ()) for value in required) or bundle.invalidation_refs:
        return None
    return CanonicalYOLO11nUpstreamRecordsV1(
        capability_resolution=bundle.capability_resolution,
        capability_model_binding=bundle.capability_model_binding,
        runtime_admission_assessment=bundle.runtime_admission_assessment,
        executable_capability=bundle.executable_capability,
        model_provider_binding=bundle.model_provider_binding,
        runtime_admission_ref=bundle.runtime_admission_ref,
        runtime_admission_version=bundle.runtime_admission_version,
        grant_refs=bundle.grant_refs,
        constraint_refs=bundle.constraint_refs,
        source_version_refs=bundle.source_version_refs,
        trace_refs=bundle.trace_refs,
        provenance_refs=bundle.provenance_refs,
        invalidation_refs=bundle.invalidation_refs,
    )


__all__ = [
    "YOLO11N_PROVIDER_FAMILY",
    "adapt_governed_bundle_to_canonical_yolo11n_records_v1",
    "produce_yolo11n_governed_execution_records_v1",
]
