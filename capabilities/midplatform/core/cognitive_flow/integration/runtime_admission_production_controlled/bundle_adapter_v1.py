"""Compose Runtime Admission output into the existing generic bundle."""

from __future__ import annotations

from typing import Optional

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.types_v1 import (
    GovernedExecutionRecordBundleV1,
)

from .types_v1 import RuntimeAdmissionProductionInputV1, RuntimeAdmissionProductionResultV1


def build_governed_execution_record_bundle_v1(
    data: RuntimeAdmissionProductionInputV1,
    result: RuntimeAdmissionProductionResultV1,
) -> Optional[GovernedExecutionRecordBundleV1]:
    if result.failure is not None or result.assessment is None or result.executable is None:
        return None
    if result.invalidation_refs or not result.candidate_only:
        return None
    required = (
        data.capability_resolution,
        data.capability_model_binding,
        data.model_provider_binding,
        result.assessment,
        result.executable,
    )
    if any(value is None for value in required):
        return None
    return GovernedExecutionRecordBundleV1(
        capability_resolution=data.capability_resolution,
        capability_model_binding=data.capability_model_binding,
        runtime_admission_assessment=result.assessment,
        executable_capability=result.executable,
        model_provider_binding=data.model_provider_binding,
        runtime_admission_ref=result.assessment.admission_candidate_ref,
        runtime_admission_version="runtime-admission-production-source:v1",
        grant_refs=data.grant_refs,
        constraint_refs=data.permission_refs + data.safety_refs + data.resource_refs + data.working_envelope_refs,
        source_version_refs=data.source_version_refs,
        trace_refs=result.trace_refs,
        provenance_refs=result.provenance_refs,
        invalidation_refs=result.invalidation_refs,
        source_refs=data.repository_source_refs,
    )


__all__ = ["build_governed_execution_record_bundle_v1"]
