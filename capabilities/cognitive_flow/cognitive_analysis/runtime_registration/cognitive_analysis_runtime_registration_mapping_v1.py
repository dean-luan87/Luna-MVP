"""Reference-only mapping from A3 Runtime to the existing L1 Capability Registry."""

from __future__ import annotations

from .cognitive_analysis_runtime_registration_types_v1 import (
    CognitiveAnalysisRuntimeRegistrationCandidateV1,
)


CAPABILITY_REGISTRY_REF_V1 = (
    "capabilities/midplatform/model_manager/registries/capability_registry_v1.json"
)
MODEL_SKILL_ADMISSION_CONTRACT_REF_V1 = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1"
PERMISSION_ADMISSION_CONTRACT_REF_V1 = "Permission / Admission Contract"
RUNTIME_BOUNDARY_CONTRACT_REF_V1 = "Runtime Boundary Contract"
OUTPUT_CANDIDATE_CONTRACT_REF_V1 = "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1"
INPUT_CANDIDATE_CONTRACT_REF_V1 = "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1"
IO_SYMMETRY_CONTRACT_REF_V1 = "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1"
TRACEABILITY_CONTRACT_REF_V1 = "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1"
PROTOCOL_MANAGER_REGISTRY_INTERFACE_REF_V1 = (
    "capabilities/midplatform/protocol_manager/module/protocol_manager_registry_adapter_v1.py"
)
PROTOCOL_MANAGER_DIAGNOSTICS_REF_V1 = (
    "capabilities/midplatform/protocol_manager/module/protocol_manager_diagnostics_v1.py"
)
PERMISSION_DIAGNOSTICS_REF_V1 = (
    "capabilities/midplatform/permission_and_admission_manager/module/"
    "permission_and_admission_diagnostics_v1.py"
)


def build_cognitive_analysis_runtime_registration_candidate_v1(
) -> CognitiveAnalysisRuntimeRegistrationCandidateV1:
    """Build a static candidate without opening or mutating the L1 Registry."""
    return CognitiveAnalysisRuntimeRegistrationCandidateV1(
        capability_id="cognitive_analysis_runtime",
        capability_label="Cognitive Analysis Runtime (candidate)",
        capability_type="cognitive_analysis",
        capability_owner="L1 Protocol Governance / Cognitive Flow",
        lifecycle_state="candidate",
        required_contracts=(
            MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
            PERMISSION_ADMISSION_CONTRACT_REF_V1,
            RUNTIME_BOUNDARY_CONTRACT_REF_V1,
            INPUT_CANDIDATE_CONTRACT_REF_V1,
            OUTPUT_CANDIDATE_CONTRACT_REF_V1,
            IO_SYMMETRY_CONTRACT_REF_V1,
            TRACEABILITY_CONTRACT_REF_V1,
        ),
        protocol_dependencies=(
            PROTOCOL_MANAGER_REGISTRY_INTERFACE_REF_V1,
            "capabilities/midplatform/protocol_manager/module/protocol_manager_admission_v1.py",
            "capabilities/midplatform/permission_and_admission_manager/module/"
            "permission_and_admission_module_facade_v1.py",
        ),
        diagnostics_binding=(
            PROTOCOL_MANAGER_DIAGNOSTICS_REF_V1,
            PERMISSION_DIAGNOSTICS_REF_V1,
        ),
        registry_ref=CAPABILITY_REGISTRY_REF_V1,
        registry_entry_mapping={
            "capability_id": "cognitive_analysis_runtime",
            "capability_label": "Cognitive Analysis Runtime (candidate)",
            "need_triggers": ("cognitive_analysis_candidate",),
            "providers": (),
        },
        manifest_schema_status=(
            "no_standalone_capability_manifest_schema_located; "
            "existing_registry_entry_format_mapped_candidate_only"
        ),
        registry_write_applied=False,
        capability_activation_applied=False,
        permission_grant_applied=False,
        runtime_authorized=False,
    )
