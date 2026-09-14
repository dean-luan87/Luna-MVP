from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from ..model_contract_repository_registry_v1 import build_model_contract_repository_v1
from ..real_model_asset_admission.real_model_asset_admission_types_v1 import (
    resolve_real_model_asset_admission_v1,
)


YOLO11N_ASSET_ID = "model-asset:yolo11n:weights-v1"
YOLO11N_EXPECTED_ASSET_PATH = "vision/detection/yolo/yolo11n.pt"
YOLO11N_EXPECTED_ASSET_FILENAME = "yolo11n.pt"
YOLO11N_LOADER_ID = "loader:ultralytics:yolo:v1"
YOLO11N_PROVIDER_ADAPTER_ID = "adapter:yolo:visual-evidence:v1"
YOLO11N_CAPABILITY_ID = "capability:object-detection:v1"
YOLO11N_EVIDENCE_ID = "evidence:visual-detection-candidate:v1"

CHECKSUM_STATUSES = (
    "DECLARED_CHECKSUM",
    "OBSERVED_CHECKSUM",
    "CHECKSUM_VERIFIED",
    "CHECKSUM_MISMATCH",
    "CHECKSUM_UNAVAILABLE",
)
DEPENDENCY_STATUSES = (
    "PYTHON_DEPENDENCY_UNRESOLVED",
    "PYTHON_DEPENDENCY_DECLARED",
    "PYTHON_DEPENDENCY_VERIFIED",
    "PYTHON_DEPENDENCY_MISSING",
    "PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE",
)
TECHNICAL_ADMISSION_STATUSES = (
    "ADMISSION_READY_CANDIDATE",
    "ADMISSION_BLOCKED_ASSET_MISSING",
    "ADMISSION_BLOCKED_IDENTITY",
    "ADMISSION_BLOCKED_CHECKSUM",
    "ADMISSION_BLOCKED_CONTRACT",
    "ADMISSION_BLOCKED_DEPENDENCY",
    "ADMISSION_BLOCKED_LOADER",
    "ADMISSION_BLOCKED_PROVIDER",
)


@dataclass(frozen=True)
class YOLO11nReadinessCandidateV1:
    target_model: str
    target_route_role: str
    target_asset_id: str
    expected_asset_path: str
    expected_asset_filename: str
    physical_asset_status: str
    model_identity_status: str
    model_contract_status: str
    loader_contract_status: str
    provider_adapter_status: str
    capability_contract_status: str
    evidence_contract_status: str
    checksum_status: str
    declared_checksum: Optional[str]
    observed_checksum: Optional[str]
    dependency_status: str
    dependency_requirements: Tuple[str, ...]
    technical_admission_status: str
    commercial_license_status: str
    model_inference_executed: bool
    provider_invocation_executed: bool
    network_access: bool
    automatic_model_download: bool
    automatic_package_download: bool
    automatic_dependency_install: bool
    human_contract_selection_required_normal_path: bool
    loader_guessing: bool
    extension_based_loader_selection: bool
    provider_semantic_authority: bool
    truth_declared: bool
    fact_admitted: bool
    field_mutation: bool
    current_world_truth_declaration: bool
    intent_mutation: bool
    task_mutation: bool
    decision_mutation: bool
    route_reuse_owner: str
    identity_basis: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


def _norm(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def _trace(key: str) -> str:
    return "trace:yolo11n-readiness:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def checksum_status_v1(candidate: Mapping[str, Any]) -> str:
    explicit = _norm(candidate.get("checksum_status"))
    if explicit in CHECKSUM_STATUSES:
        return explicit
    declared = _norm(candidate.get("declared_checksum"))
    observed = _norm(candidate.get("observed_checksum"))
    if declared and observed:
        return "CHECKSUM_VERIFIED" if declared == observed else "CHECKSUM_MISMATCH"
    if declared:
        return "DECLARED_CHECKSUM"
    if observed:
        return "OBSERVED_CHECKSUM"
    return "CHECKSUM_UNAVAILABLE"


def dependency_status_v1(candidate: Mapping[str, Any]) -> str:
    value = _norm(candidate.get("dependency_status"))
    aliases = {
        "UNRESOLVED": "PYTHON_DEPENDENCY_UNRESOLVED",
        "PYTHON_DEPENDENCY_NOT_READY": "PYTHON_DEPENDENCY_UNRESOLVED",
        "PYTHON_DEPENDENCY_READY": "PYTHON_DEPENDENCY_VERIFIED",
        "READY": "PYTHON_DEPENDENCY_VERIFIED",
        "DECLARED": "PYTHON_DEPENDENCY_DECLARED",
        "VERIFIED": "PYTHON_DEPENDENCY_VERIFIED",
        "MISSING": "PYTHON_DEPENDENCY_MISSING",
        "VERSION_INCOMPATIBLE": "PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE",
    }
    return aliases.get(value, value if value in DEPENDENCY_STATUSES else "PYTHON_DEPENDENCY_UNRESOLVED")


def physical_asset_status_v1(candidate: Mapping[str, Any]) -> str:
    explicit = _norm(candidate.get("physical_asset_status"))
    if explicit:
        return explicit
    path = _norm(candidate.get("physical_path")) or _norm(candidate.get("expected_asset_path"))
    return "ASSET_PRESENT" if path and Path(path).is_file() else "ASSET_NOT_PRESENT"


def _contract_readiness(candidate: Mapping[str, Any], dependency: str, repo: Mapping[str, Any]) -> Any:
    prior_candidate = dict(candidate)
    prior_candidate["registered_asset_id"] = _norm(candidate.get("registered_asset_id")) or YOLO11N_ASSET_ID
    prior_candidate["physical_asset_status"] = physical_asset_status_v1(candidate)
    prior_candidate["dependency_status"] = (
        "PYTHON_DEPENDENCY_READY" if dependency == "PYTHON_DEPENDENCY_VERIFIED" else
        "PYTHON_DEPENDENCY_NOT_READY" if dependency != "PYTHON_DEPENDENCY_UNRESOLVED" else
        "PYTHON_DEPENDENCY_UNRESOLVED"
    )
    return resolve_real_model_asset_admission_v1(prior_candidate, repository=repo)


def resolve_yolo11n_readiness_v1(
    candidate: Optional[Mapping[str, Any]] = None,
    *,
    repository: Optional[Mapping[str, Any]] = None,
) -> YOLO11nReadinessCandidateV1:
    supplied = dict(candidate or {})
    repo = repository or build_model_contract_repository_v1()
    asset = (repo.get("model_assets") or {}).get(YOLO11N_ASSET_ID, {})
    dependency = dependency_status_v1(supplied)
    physical = physical_asset_status_v1(supplied)
    checksum = checksum_status_v1(supplied)
    declared_checksum = _norm(supplied.get("declared_checksum")) or asset.get("checksum") or None
    observed_checksum = _norm(supplied.get("observed_checksum")) or None
    if not supplied.get("checksum_status") and declared_checksum and observed_checksum:
        checksum = "CHECKSUM_VERIFIED" if declared_checksum == observed_checksum else "CHECKSUM_MISMATCH"
    contract = _contract_readiness(supplied, dependency, repo)
    contract_dict = asdict(contract)
    loader = (repo.get("loader_contracts") or {}).get(YOLO11N_LOADER_ID, {})
    dependency_requirements = tuple(str(item) for item in loader.get("required_dependencies") or ())
    expected_path = _norm(supplied.get("expected_asset_path")) or _norm(asset.get("weights_path")) or YOLO11N_EXPECTED_ASSET_PATH
    expected_filename = Path(expected_path).name or YOLO11N_EXPECTED_ASSET_FILENAME
    technical = contract.admission_status
    if contract.model_identity_status != "MODEL_ASSET_IDENTIFIED_UNIQUE":
        technical = "ADMISSION_BLOCKED_IDENTITY"
    elif physical != "ASSET_PRESENT":
        technical = "ADMISSION_BLOCKED_ASSET_MISSING"
    elif checksum == "CHECKSUM_MISMATCH":
        technical = "ADMISSION_BLOCKED_CHECKSUM"
    elif checksum != "CHECKSUM_VERIFIED":
        technical = "ADMISSION_BLOCKED_CHECKSUM"
    elif contract.loader_contract_status == "MISSING":
        technical = "ADMISSION_BLOCKED_LOADER"
    elif contract.provider_adapter_status in ("MISSING", "MISMATCH"):
        technical = "ADMISSION_BLOCKED_PROVIDER"
    elif any(
        status != "RESOLVED"
        for status in (
            contract.model_contract_status,
            contract.capability_contract_status,
            contract.evidence_contract_status,
        )
    ):
        technical = "ADMISSION_BLOCKED_CONTRACT"
    elif dependency != "PYTHON_DEPENDENCY_VERIFIED":
        technical = "ADMISSION_BLOCKED_DEPENDENCY"
    else:
        technical = "ADMISSION_READY_CANDIDATE"
    readiness_physical = "ASSET_READY_CANDIDATE" if technical == "ADMISSION_READY_CANDIDATE" else physical
    license_profile = (repo.get("license_profiles") or {}).get(YOLO11N_ASSET_ID, {})
    result = YOLO11nReadinessCandidateV1(
        target_model="YOLO11n",
        target_route_role="STABILITY_COMPARATOR",
        target_asset_id=YOLO11N_ASSET_ID,
        expected_asset_path=expected_path,
        expected_asset_filename=expected_filename,
        physical_asset_status=readiness_physical,
        model_identity_status=contract.model_identity_status,
        model_contract_status=contract.model_contract_status,
        loader_contract_status=contract.loader_contract_status,
        provider_adapter_status=contract.provider_adapter_status,
        capability_contract_status=contract.capability_contract_status,
        evidence_contract_status=contract.evidence_contract_status,
        checksum_status=checksum,
        declared_checksum=declared_checksum,
        observed_checksum=observed_checksum,
        dependency_status=dependency,
        dependency_requirements=dependency_requirements,
        technical_admission_status=technical,
        commercial_license_status=str(license_profile.get("commercial_use_constraints") or "REQUIRES_LICENSE_REVIEW"),
        model_inference_executed=False,
        provider_invocation_executed=False,
        network_access=False,
        automatic_model_download=False,
        automatic_package_download=False,
        automatic_dependency_install=False,
        human_contract_selection_required_normal_path=False,
        loader_guessing=False,
        extension_based_loader_selection=False,
        provider_semantic_authority=False,
        truth_declared=False,
        fact_admitted=False,
        field_mutation=False,
        current_world_truth_declaration=False,
        intent_mutation=False,
        task_mutation=False,
        decision_mutation=False,
        route_reuse_owner="Model Manager / Model Governance",
        identity_basis=tuple(contract.identity_basis),
        conflict_refs=tuple(contract.conflict_refs),
        trace_ref=_trace(repr(supplied)),
        provenance_refs=(contract.trace_ref, f"manifest:{expected_path}", f"model-asset:{YOLO11N_ASSET_ID}"),
    )
    return result


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
