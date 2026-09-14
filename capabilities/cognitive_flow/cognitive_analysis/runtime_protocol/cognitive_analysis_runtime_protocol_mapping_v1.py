"""Reference-only A3 Runtime Capability to L1 Protocol Governance mapping v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


RUNTIME_PROTOCOL_MAPPING_SCHEMA_VERSION_V1 = "luna.cognitive_analysis.runtime_protocol_mapping.v1"
CAPABILITY_REGISTRY_REF_V1 = "capabilities/midplatform/model_manager/registries/capability_registry_v1.json"
MODEL_SKILL_ADMISSION_CONTRACT_REF_V1 = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1"
PERMISSION_ADMISSION_CONTRACT_REF_V1 = "Permission / Admission Contract"
RUNTIME_BOUNDARY_CONTRACT_REF_V1 = "Runtime Boundary Contract"
OUTPUT_CANDIDATE_CONTRACT_REF_V1 = "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1"
INPUT_CANDIDATE_CONTRACT_REF_V1 = "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1"
IO_SYMMETRY_CONTRACT_REF_V1 = "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1"
TRACEABILITY_CONTRACT_REF_V1 = "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1"
PROTOCOL_MANAGER_REF_V1 = "capabilities/midplatform/protocol_manager/module/protocol_manager_module_facade_v1.py"
PROTOCOL_DIAGNOSTICS_REF_V1 = "capabilities/midplatform/protocol_manager/module/protocol_manager_diagnostics_v1.py"
PERMISSION_DIAGNOSTICS_REF_V1 = "capabilities/midplatform/permission_and_admission_manager/module/permission_and_admission_diagnostics_v1.py"


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeProtocolMappingV1:
    capability_id: str
    capability_type: str
    owner: str
    lifecycle: str
    capability_registry_ref: str
    capability_registration_status: str
    capability_manifest_status: str
    required_contract_refs: Tuple[str, ...]
    input_schema_refs: Tuple[str, ...]
    output_schema_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    permission_governance_ref: str
    boundary_contract_ref: str
    diagnostics_refs: Tuple[str, ...]
    allowed_output_types: Tuple[str, ...]
    forbidden_operations: Tuple[str, ...]
    runtime_specific_permission_model: bool
    runtime_authorized: bool
    schema_version: str = RUNTIME_PROTOCOL_MAPPING_SCHEMA_VERSION_V1


def build_cognitive_analysis_runtime_protocol_mapping_v1() -> CognitiveAnalysisRuntimeProtocolMappingV1:
    """Return static references only; do not register, admit, or execute Runtime."""
    return CognitiveAnalysisRuntimeProtocolMappingV1(
        capability_id="cognitive_analysis_runtime",
        capability_type="cognitive_analysis",
        owner="L1 Protocol Governance / Cognitive Flow",
        lifecycle="candidate",
        capability_registry_ref=CAPABILITY_REGISTRY_REF_V1,
        capability_registration_status="registration_required_not_applied",
        capability_manifest_status="l1_registry_owned_record_required",
        required_contract_refs=(
            MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
            PERMISSION_ADMISSION_CONTRACT_REF_V1,
            RUNTIME_BOUNDARY_CONTRACT_REF_V1,
            INPUT_CANDIDATE_CONTRACT_REF_V1,
            OUTPUT_CANDIDATE_CONTRACT_REF_V1,
            IO_SYMMETRY_CONTRACT_REF_V1,
            TRACEABILITY_CONTRACT_REF_V1,
        ),
        input_schema_refs=("context_ref", "evidence_refs", "hypothesis_refs", "analysis_question_ref"),
        output_schema_refs=("analysis_result_candidate", "evidence_trace", "uncertainty", "warning_codes", "provenance", "runtime_flags"),
        dependency_refs=(
            "CurrentCognitiveContextV1",
            "governed_evidence_reference",
            "governed_hypothesis_reference",
            PROTOCOL_MANAGER_REF_V1,
            "capabilities/midplatform/permission_and_admission_manager/module/permission_and_admission_module_facade_v1.py",
        ),
        permission_governance_ref=PERMISSION_ADMISSION_CONTRACT_REF_V1,
        boundary_contract_ref=RUNTIME_BOUNDARY_CONTRACT_REF_V1,
        diagnostics_refs=(PROTOCOL_DIAGNOSTICS_REF_V1, PERMISSION_DIAGNOSTICS_REF_V1),
        allowed_output_types=("candidate_analysis_output",),
        forbidden_operations=(
            "fact_mutation",
            "decision_mutation",
            "action_execution",
            "state_writeback",
            "context_snapshot_event_evidence_mutation",
            "runtime_specific_permission_authority",
        ),
        runtime_specific_permission_model=False,
        runtime_authorized=False,
    )
