"""Static validation for an A3 Runtime registration candidate; no Registry write."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from .cognitive_analysis_runtime_registration_mapping_v1 import (
    CAPABILITY_REGISTRY_REF_V1,
    MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
    OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    PERMISSION_ADMISSION_CONTRACT_REF_V1,
    RUNTIME_BOUNDARY_CONTRACT_REF_V1,
)
from .cognitive_analysis_runtime_registration_types_v1 import (
    CognitiveAnalysisRuntimeRegistrationCandidateV1,
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeRegistrationIssueV1:
    code: str
    field_ref: str
    message: str


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeRegistrationValidationResultV1:
    issues: Tuple[CognitiveAnalysisRuntimeRegistrationIssueV1, ...]
    duplicate_capability_detected: bool

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_cognitive_analysis_runtime_registration_candidate_v1(
    candidate: CognitiveAnalysisRuntimeRegistrationCandidateV1,
    project_root: Path,
) -> CognitiveAnalysisRuntimeRegistrationValidationResultV1:
    """Read the existing Registry solely to validate references and duplicates."""
    issues = []
    for field_ref, value in {
        "capability_id": candidate.capability_id,
        "capability_label": candidate.capability_label,
        "capability_type": candidate.capability_type,
        "capability_owner": candidate.capability_owner,
        "lifecycle_state": candidate.lifecycle_state,
        "registry_ref": candidate.registry_ref,
    }.items():
        if not isinstance(value, str) or not value.strip():
            issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
                "missing_required_declaration", field_ref, f"{field_ref} must be non-empty"
            ))

    registry_path = project_root / candidate.registry_ref
    registry_data = {}
    if candidate.registry_ref != CAPABILITY_REGISTRY_REF_V1 or not registry_path.is_file():
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "registry_reference_missing", "registry_ref", "existing L1 Capability Registry is required"
        ))
    else:
        try:
            registry_data = json.loads(registry_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
                "registry_unreadable", "registry_ref", str(exc)
            ))

    capabilities = registry_data.get("capabilities", []) if isinstance(registry_data, dict) else []
    if not isinstance(capabilities, list):
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "registry_format_incompatible", "capabilities", "capabilities must be a list"
        ))
        capabilities = []
    duplicate_detected = any(
        isinstance(record, dict) and record.get("capability_id") == candidate.capability_id
        for record in capabilities
    )
    if duplicate_detected:
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "duplicate_capability_id", "capability_id", "candidate already exists in the L1 Capability Registry"
        ))

    entry_mapping = dict(candidate.registry_entry_mapping)
    for field_ref in ("capability_id", "capability_label", "need_triggers", "providers"):
        if field_ref not in entry_mapping:
            issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
                "manifest_mapping_incomplete", "registry_entry_mapping", f"missing {field_ref} mapping"
            ))
    if entry_mapping.get("capability_id") != candidate.capability_id:
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "capability_id_inconsistent", "registry_entry_mapping.capability_id", "must equal candidate capability_id"
        ))
    if "existing_registry_entry_format_mapped_candidate_only" not in candidate.manifest_schema_status:
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "manifest_schema_status_inconsistent", "manifest_schema_status", "must record the existing Registry entry format"
        ))

    for contract_ref in (
        MODEL_SKILL_ADMISSION_CONTRACT_REF_V1,
        PERMISSION_ADMISSION_CONTRACT_REF_V1,
        RUNTIME_BOUNDARY_CONTRACT_REF_V1,
        OUTPUT_CANDIDATE_CONTRACT_REF_V1,
    ):
        if contract_ref not in candidate.required_contracts:
            issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
                "required_contract_missing", "required_contracts", contract_ref
            ))
    if candidate.lifecycle_state != "candidate":
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "lifecycle_declaration_invalid", "lifecycle_state", "registration candidate must remain candidate"
        ))
    if not candidate.protocol_dependencies or not candidate.diagnostics_binding:
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "governance_reference_missing", "protocol_dependencies", "Protocol and diagnostics references are required"
        ))
    if any((
        candidate.registry_write_applied,
        candidate.capability_activation_applied,
        candidate.permission_grant_applied,
        candidate.runtime_authorized,
    )):
        issues.append(CognitiveAnalysisRuntimeRegistrationIssueV1(
            "registration_boundary_violated", "registry_write_applied", "this phase cannot write, activate, grant, or authorize"
        ))
    return CognitiveAnalysisRuntimeRegistrationValidationResultV1(
        issues=tuple(issues), duplicate_capability_detected=duplicate_detected
    )
