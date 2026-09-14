"""Pure validation of the A3 Runtime to L1 Protocol reference mapping v1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from .cognitive_analysis_runtime_protocol_mapping_v1 import (
    CAPABILITY_REGISTRY_REF_V1,
    MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
    OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    PERMISSION_ADMISSION_CONTRACT_REF_V1,
    RUNTIME_BOUNDARY_CONTRACT_REF_V1,
    CognitiveAnalysisRuntimeProtocolMappingV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeProtocolMappingIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeProtocolMappingValidationResultV1:
    issues: Tuple[CognitiveAnalysisRuntimeProtocolMappingIssueV1, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_runtime_protocol_mapping_v1(
    mapping: CognitiveAnalysisRuntimeProtocolMappingV1,
    project_root: Path,
) -> CognitiveAnalysisRuntimeProtocolMappingValidationResultV1:
    """Validate references and boundaries only; never register or execute Runtime."""
    issues = []
    required_text = {
        "capability_id": mapping.capability_id,
        "capability_type": mapping.capability_type,
        "owner": mapping.owner,
        "lifecycle": mapping.lifecycle,
        "capability_registry_ref": mapping.capability_registry_ref,
        "permission_governance_ref": mapping.permission_governance_ref,
        "boundary_contract_ref": mapping.boundary_contract_ref,
    }
    for field_ref, value in required_text.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("missing_reference", field_ref, f"{field_ref} must be non-empty"))
    if mapping.capability_registry_ref != CAPABILITY_REGISTRY_REF_V1 or not (project_root / mapping.capability_registry_ref).is_file():
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("capability_registry_reference_missing", "capability_registry_ref", "existing L1 Capability Registry reference is required"))
    for contract_ref in (MODEL_SKILL_ADMISSION_CONTRACT_REF_V1, PERMISSION_ADMISSION_CONTRACT_REF_V1, RUNTIME_BOUNDARY_CONTRACT_REF_V1, OUTPUT_CANDIDATE_CONTRACT_REF_V1):
        if contract_ref not in mapping.required_contract_refs:
            issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("required_contract_reference_missing", "required_contract_refs", contract_ref))
    if mapping.permission_governance_ref != PERMISSION_ADMISSION_CONTRACT_REF_V1:
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("permission_reference_missing", "permission_governance_ref", "existing Permission / Admission Contract must be referenced"))
    if mapping.boundary_contract_ref != RUNTIME_BOUNDARY_CONTRACT_REF_V1 or mapping.allowed_output_types != ("candidate_analysis_output",):
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("boundary_mapping_inconsistent", "boundary_contract_ref", "candidate-only boundary mapping is required"))
    forbidden = {"fact_mutation", "decision_mutation", "action_execution", "state_writeback"}
    if not forbidden.issubset(mapping.forbidden_operations):
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("forbidden_operation_missing", "forbidden_operations", "Fact, Decision, Action, and State boundaries must be declared"))
    if mapping.runtime_specific_permission_model or mapping.runtime_authorized:
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("duplicated_authorization_model", "runtime_specific_permission_model", "A3 must not own a Runtime-specific authorization model"))
    if mapping.capability_registration_status != "registration_required_not_applied":
        issues.append(CognitiveAnalysisRuntimeProtocolMappingIssueV1("registration_status_drift", "capability_registration_status", "this mapping must not claim Registry registration"))
    return CognitiveAnalysisRuntimeProtocolMappingValidationResultV1(tuple(issues))
