"""Compatibility seam for the existing real single-invocation trial.

This module only maps already-supplied trial candidates into the verified
logical-resolution/runtime-admission candidate seam. It performs no probe,
checksum computation, model loading, or Provider invocation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_scope_resolution_fixture_v1 import (
    _bind,
    _slot,
    build_scope_modules,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_resolution_v1 import (
    resolve_scoped_capability_requirement,
)
from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_adapter_v1 import (
    assess_runtime_admission_v1,
    build_executable_capability_candidate_v1,
    build_provider_admission_input_v1,
    build_runtime_admission_input_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_types_v1 import (
    ExecutableCapabilityCandidateV1,
    ProviderAdmissionInputCandidateV1,
    RuntimeAdmissionAssessmentCandidateV1,
    RuntimeAdmissionInputCandidateV1,
)


@dataclass(frozen=True)
class TerminalReadinessEvidenceCandidateV1:
    source_ref: str
    model_path_ref: Optional[str]
    dependency_status_ref: str
    declared_checksum_ref: Optional[str]
    observed_integrity_evidence_ref: Optional[str]
    ownership_source_ref: str = "TERMINAL_CONTROLLED_TRIAL_INPUT"
    candidate_only: bool = True
    synthetic_only: bool = False


@dataclass(frozen=True)
class RuntimeAdmissionCompatibilityRecordV1:
    terminal_evidence: TerminalReadinessEvidenceCandidateV1
    logical_resolution: Any
    assessment: RuntimeAdmissionAssessmentCandidateV1
    executable: Optional[ExecutableCapabilityCandidateV1]
    provider_input: Optional[ProviderAdmissionInputCandidateV1]
    candidate_only: bool = True
    synthetic_only: bool = False


def _ref(prefix: str, value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return f"{prefix}:{value}"


def build_terminal_readiness_evidence_candidate_v1(
    *,
    source_ref: str,
    model_path: str,
    dependency_status: str,
    declared_checksum: Optional[str],
    observed_checksum: Optional[str],
) -> TerminalReadinessEvidenceCandidateV1:
    return TerminalReadinessEvidenceCandidateV1(
        source_ref=source_ref,
        model_path_ref=_ref("terminal-model-path", model_path),
        dependency_status_ref=dependency_status,
        declared_checksum_ref=_ref("terminal-declared-checksum", declared_checksum),
        observed_integrity_evidence_ref=_ref("terminal-observed-integrity", observed_checksum),
    )


def build_runtime_admission_compatibility_v1(
    *,
    case_id: str,
    formation: Any,
    source_ref: str,
    model_path: str,
    declared_checksum: Optional[str],
    observed_checksum: Optional[str],
    dependency_status: str,
    model_admission: Any,
    model_contract_resolution: Any,
) -> RuntimeAdmissionCompatibilityRecordV1:
    terminal = build_terminal_readiness_evidence_candidate_v1(
        source_ref=source_ref,
        model_path=model_path,
        dependency_status=dependency_status,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
    )

    modules = build_scope_modules()
    object_module = next(item for item in modules if item.module_id == "object_detection")
    object_slot = _bind(object_module, _slot(f"slot:runtime-admission:{case_id}"))
    _scope, logical_resolution, _gap = resolve_scoped_capability_requirement(
        formation.requirement,
        (object_module,),
        (object_slot,),
    )

    technical_status = str(getattr(model_admission, "technical_admission_status", ""))
    model_contract_admitted = str(getattr(model_contract_resolution, "admission_status", "")) == "ADMITTED"
    asset_blocked = technical_status in {
        "ADMISSION_BLOCKED_ASSET_MISSING",
        "ADMISSION_BLOCKED_PHYSICAL_ASSET",
    }
    identity_blocked = technical_status == "ADMISSION_BLOCKED_IDENTITY"
    contract_blocked = technical_status == "ADMISSION_BLOCKED_CONTRACT" or not model_contract_admitted
    asset_ref = None if asset_blocked else (getattr(model_contract_resolution, "model_asset_id", None) or object_module.model_asset_refs[0])
    path_ref = None if asset_blocked else terminal.model_path_ref
    version_status = "MODEL_VERSION_MISMATCH" if identity_blocked else "MODEL_VERSION_MATCH"
    integrity_status = str(getattr(model_admission, "checksum_status", "CHECKSUM_UNAVAILABLE"))
    provider_refs: Tuple[str, ...] = () if contract_blocked else (f"provider-compatibility:trial:{case_id}",)

    # The existing trial provides a candidate admission result but no new
    # runtime probe. This is evidence projection, not a runtime fact.
    runtime_status = (
        "RUNTIME_HEALTH_VERIFIED"
        if technical_status == "ADMISSION_READY_CANDIDATE" and model_contract_admitted
        else "RUNTIME_HEALTH_UNRESOLVED"
    )
    runtime_input: RuntimeAdmissionInputCandidateV1 = build_runtime_admission_input_v1(
        logical_resolution_ref=f"resolution:real-trial:{case_id}",
        logical_resolution=logical_resolution,
        logical_capability_ref=logical_resolution.module_ref or "capability:object_detection",
        capability_slot_ref=logical_resolution.slot_ref or f"slot:runtime-admission:{case_id}",
        model_asset_ref=asset_ref,
        model_version_ref=f"model-version:yolo11n:trial:{case_id}",
        governed_model_path_ref=path_ref,
        declared_checksum_ref=terminal.declared_checksum_ref,
        observed_integrity_evidence_ref=terminal.observed_integrity_evidence_ref,
        dependency_health_refs=(f"terminal-dependency-health:{case_id}",),
        dependency_status_ref=terminal.dependency_status_ref,
        device_runtime_health_refs=(f"existing-trial-runtime-health-candidate:{case_id}",),
        runtime_health_status_ref=runtime_status,
        provider_compatibility_refs=provider_refs,
        permission_refs=("permission:capability-governance",),
        permission_status_ref="PERMISSION_GRANTED",
        resource_refs=("resource:controlled-real-trial",),
        resource_status_ref="RESOURCE_AVAILABLE",
        safety_refs=("safety:controlled-real-trial",),
        safety_status_ref="SAFETY_ALLOWED",
        integrity_status_ref=integrity_status,
        model_version_status_ref=version_status,
        source_acquisition_context_ref=f"source-context:terminal-trial:{case_id}",
        source_state_version_ref=f"state:real-trial:{case_id}:v1",
        valid_source_state_version_ref=f"state:real-trial:{case_id}:v1",
        staleness_refs=(),
        trace_refs=(f"trace:runtime-admission:real-trial:{case_id}",),
        provenance_refs=(
            f"provenance:terminal-readiness:{case_id}",
            "ownership:terminal-input-not-canonical",
        ),
    )
    assessment = assess_runtime_admission_v1(runtime_input)
    executable = build_executable_capability_candidate_v1(assessment)
    provider_input = build_provider_admission_input_v1(executable)
    return RuntimeAdmissionCompatibilityRecordV1(
        terminal_evidence=terminal,
        logical_resolution=logical_resolution,
        assessment=assessment,
        executable=executable,
        provider_input=provider_input,
    )


__all__ = [
    "RuntimeAdmissionCompatibilityRecordV1",
    "TerminalReadinessEvidenceCandidateV1",
    "build_runtime_admission_compatibility_v1",
    "build_terminal_readiness_evidence_candidate_v1",
]

