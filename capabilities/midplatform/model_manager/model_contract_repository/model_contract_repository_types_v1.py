from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

OWNER = "Model Manager / Model Governance"
REPOSITORY_VERSION = "model-contract-repository-v1"

MODEL_ASSET_STATUSES = ("REGISTERED", "SUPPORTED", "DEPRECATED", "BLOCKED", "QUARANTINED")
LOCAL_SOURCE_PACKAGE_STATUSES = ("REGISTERED", "SUPPORTED", "MISSING", "INCOMPATIBLE", "BLOCKED", "DEPRECATED")
CONTRACT_LIFECYCLE = ("DRAFT", "REGISTERED", "SUPPORTED", "DEPRECATED", "REVOKED", "BLOCKED")
RESOLUTION_STATUSES = (
    "RESOLVED_UNIQUE",
    "NO_MATCH",
    "AMBIGUOUS_MATCH",
    "CONTRACT_CONFLICT",
    "CONTRACT_DEPRECATED",
    "CONTRACT_BLOCKED",
)
COMPATIBILITY_STATUSES = ("COMPATIBLE", "BLOCKED")
ADMISSION_STATUSES = ("ADMITTED", "BLOCKED")


@dataclass(frozen=True)
class ModelAssetContractV1:
    model_asset_id: str
    model_family: str
    model_name: str
    model_version: str
    weights_version: str
    weight_format: str
    weights_path: str
    checksum: Optional[str]
    source: str
    license: Optional[str]
    provider_family: str
    declared_loader_contract_id: str
    declared_capability_contract_ids: Tuple[str, ...]
    declared_evidence_contract_ids: Tuple[str, ...]
    deployment_profile_refs: Tuple[str, ...]
    benchmark_profile_refs: Tuple[str, ...]
    status: str
    contract_lifecycle: str = "REGISTERED"


@dataclass(frozen=True)
class LoaderContractV1:
    loader_contract_id: str
    loader_kind: str
    loader_version: str
    runtime_framework: str
    framework_version_constraints: Tuple[str, ...]
    supported_weight_formats: Tuple[str, ...]
    local_source_package_required: bool
    local_source_package_ref: Optional[str]
    required_dependencies: Tuple[str, ...]
    supported_devices: Tuple[str, ...]
    network_allowed: bool
    automatic_download_allowed: bool
    loader_entrypoint_ref: str
    compatibility_constraints: Tuple[str, ...]
    status: str = "SUPPORTED"


@dataclass(frozen=True)
class LocalSourcePackageContractV1:
    local_source_package_id: str
    package_family: str
    package_version: str
    package_path: Optional[str]
    source_kind: str
    compatible_loader_contract_ids: Tuple[str, ...]
    required_files: Tuple[str, ...]
    validation_markers: Tuple[str, ...]
    network_allowed: bool
    automatic_download_allowed: bool
    checksum: Optional[str]
    provenance_ref: str
    status: str


@dataclass(frozen=True)
class ProviderAdapterContractV1:
    provider_adapter_id: str
    provider_family: str
    adapter_version: str
    input_contract: str
    native_output_contract: str
    canonical_output_contract_refs: Tuple[str, ...]
    supported_loader_contracts: Tuple[str, ...]
    error_namespace: str
    trace_requirements: Tuple[str, ...]
    candidate_only_output: bool
    status: str = "SUPPORTED"


@dataclass(frozen=True)
class CapabilityContractV1:
    capability_contract_id: str
    capability_kind: str
    capability_version: str
    execution_properties: Tuple[str, ...]
    required_input_contract: str
    canonical_evidence_contract_refs: Tuple[str, ...]
    status: str = "SUPPORTED"


@dataclass(frozen=True)
class EvidenceContractV1:
    evidence_contract_id: str
    evidence_kind: str
    evidence_version: str
    schema_ref: str
    candidate_only: bool
    truth_declared: bool
    fact_admitted: bool
    status: str = "SUPPORTED"


@dataclass(frozen=True)
class ModelIdentityCandidateV1:
    matched_model_asset_id: Optional[str]
    match_basis: Tuple[str, ...]
    confidence_status: str
    ambiguity_refs: Tuple[str, ...]
    candidate_contract_ids: Tuple[str, ...]


@dataclass(frozen=True)
class CompatibilityResultV1:
    status: str
    model_asset_id: Optional[str]
    loader_contract_id: Optional[str]
    provider_adapter_contract_id: Optional[str]
    capability_contract_ids: Tuple[str, ...]
    evidence_contract_ids: Tuple[str, ...]
    reasons: Tuple[str, ...]
    rejected_contracts: Tuple[str, ...]
    trace_ref: str
    local_source_package_id: Optional[str] = None
    local_source_package_status: str = "NOT_FOUND"
    dependency_status: str = "UNKNOWN"


@dataclass(frozen=True)
class ModelContractResolutionV1:
    resolution_status: str
    identity: ModelIdentityCandidateV1
    model_asset_id: Optional[str]
    loader_contract_id: Optional[str]
    provider_adapter_contract_id: Optional[str]
    capability_contract_ids: Tuple[str, ...]
    evidence_contract_ids: Tuple[str, ...]
    compatibility: CompatibilityResultV1
    admission_status: str
    local_source_package_id: Optional[str]
    local_source_package_status: str
    execution_admitted: bool = False
    human_contract_selection_required: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
