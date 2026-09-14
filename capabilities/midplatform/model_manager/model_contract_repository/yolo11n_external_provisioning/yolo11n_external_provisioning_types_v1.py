from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from ..yolo11n_readiness.yolo11n_readiness_types_v1 import (
    CHECKSUM_STATUSES,
    DEPENDENCY_STATUSES,
    YOLO11N_ASSET_ID,
    YOLO11N_EXPECTED_ASSET_FILENAME,
    YOLO11N_EXPECTED_ASSET_PATH,
    resolve_yolo11n_readiness_v1,
)


PROVISIONING_STATUSES = (
    "PROVISIONING_CANDIDATE_ACCEPTED",
    "PROVISIONING_READY_FOR_CONTROLLED_COPY",
    "PROVISIONING_COPY_RECORDED",
    "PROVISIONING_COPY_NOT_EXECUTED",
    "PROVISIONING_REJECTED",
)
PHYSICAL_ASSET_STATUSES = (
    "ASSET_NOT_PRESENT",
    "ASSET_PRESENT_UNVERIFIED",
    "ASSET_PRESENT_VERIFIED_CANDIDATE",
    "ASSET_INVALID_FILE",
    "ASSET_PATH_MISMATCH",
)
EXTENDED_CHECKSUM_STATUSES = CHECKSUM_STATUSES + ("CHECKSUM_REGISTRATION_CANDIDATE",)
IDENTITY_STATUSES = (
    "MODEL_ASSET_IDENTIFIED_UNIQUE",
    "MODEL_ASSET_IDENTITY_CONFLICT",
    "MODEL_ASSET_PROVENANCE_UNRESOLVED",
    "MODEL_ASSET_FINGERPRINT_MISMATCH",
)
TECHNICAL_ADMISSION_STATUSES = (
    "ADMISSION_READY_CANDIDATE",
    "ADMISSION_BLOCKED_ASSET_MISSING",
    "ADMISSION_BLOCKED_PHYSICAL_ASSET",
    "ADMISSION_BLOCKED_IDENTITY",
    "ADMISSION_BLOCKED_CHECKSUM",
    "ADMISSION_BLOCKED_DEPENDENCY",
    "ADMISSION_BLOCKED_CONTRACT",
)


@dataclass(frozen=True)
class ExternalModelProvisioningRecordV1:
    source_file_ref: Optional[str]
    target_model_asset_id: str
    target_governed_path: str
    provisioning_source_type: str
    expected_filename: str
    expected_family: str
    expected_model_name: str
    provenance_ref: str
    copy_required: bool
    copy_executed: bool
    registration_required: bool
    candidate_only: bool
    provisioning_status: str
    trace_ref: str


@dataclass(frozen=True)
class PhysicalAssetVerificationV1:
    file_exists: bool
    is_regular_file: bool
    file_size: Optional[int]
    observed_filename: Optional[str]
    observed_extension: Optional[str]
    observed_path: Optional[str]
    governed_path_match: bool
    physical_asset_status: str
    trace_ref: str


@dataclass(frozen=True)
class DependencyProbeResultV1:
    dependency_name: str
    required_or_conditional: str
    declared_constraint: Optional[str]
    observed_version: Optional[str]
    import_available: Optional[bool]
    version_compatible: Optional[bool]
    verification_status: str
    error_ref: Optional[str]


@dataclass(frozen=True)
class YOLO11nExternalProvisioningAdmissionV1:
    target_model: str
    target_asset_id: str
    expected_governed_path: str
    provisioning: ExternalModelProvisioningRecordV1
    physical: PhysicalAssetVerificationV1
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
    loader_guessing: bool
    filename_only_identity: bool
    extension_only_identity: bool
    human_contract_selection_required_normal_path: bool
    provider_semantic_authority: bool
    truth_declared: bool
    fact_admitted: bool
    field_mutation: bool
    current_world_truth_declaration: bool
    ocr_execution: bool
    slam_execution: bool
    vlm_execution: bool
    semantic_compression: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


def _norm(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def _optional_norm(value: Any) -> Optional[str]:
    normalized = _norm(value)
    return normalized or None


def _trace(key: str) -> str:
    return "trace:yolo11n-provisioning:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def _path_matches_governed(observed_path: Optional[str], target_path: str) -> bool:
    if not observed_path:
        return False
    observed = _norm(observed_path).rstrip("/")
    target = _norm(target_path).lstrip("/")
    return observed == target or observed.endswith("/" + target)


def _physical_verification(candidate: Mapping[str, Any], target_path: str, trace: str) -> PhysicalAssetVerificationV1:
    observed_path = _optional_norm(candidate.get("observed_path") or candidate.get("physical_path"))
    file_exists_value = candidate.get("file_exists")
    regular_value = candidate.get("is_regular_file")
    if file_exists_value is None:
        file_exists_value = bool(observed_path and Path(observed_path).exists())
    if regular_value is None:
        regular_value = bool(observed_path and Path(observed_path).is_file())
    file_exists = bool(file_exists_value)
    is_regular_file = bool(regular_value)
    file_size = candidate.get("file_size")
    if file_size is None and is_regular_file and observed_path:
        file_size = Path(observed_path).stat().st_size
    observed_filename = _optional_norm(candidate.get("observed_filename")) or (Path(observed_path).name if observed_path else None)
    observed_extension = _optional_norm(candidate.get("observed_extension")) or (Path(observed_filename).suffix.lower().lstrip(".") if observed_filename else None)
    governed_match = _path_matches_governed(observed_path, target_path)
    explicit = _norm(candidate.get("physical_asset_status"))
    if explicit in PHYSICAL_ASSET_STATUSES:
        status = explicit
    elif not file_exists:
        status = "ASSET_NOT_PRESENT"
    elif not is_regular_file:
        status = "ASSET_INVALID_FILE"
    elif not governed_match:
        status = "ASSET_PATH_MISMATCH"
    else:
        status = "ASSET_PRESENT_UNVERIFIED"
    return PhysicalAssetVerificationV1(
        file_exists=file_exists,
        is_regular_file=is_regular_file,
        file_size=int(file_size) if file_size is not None else None,
        observed_filename=observed_filename,
        observed_extension=observed_extension,
        observed_path=observed_path,
        governed_path_match=governed_match,
        physical_asset_status=status,
        trace_ref=trace,
    )


def _checksum_status(candidate: Mapping[str, Any]) -> Tuple[str, Optional[str], Optional[str]]:
    declared = _optional_norm(candidate.get("declared_checksum"))
    observed = _optional_norm(candidate.get("observed_checksum"))
    if declared and observed:
        return ("CHECKSUM_VERIFIED" if declared == observed else "CHECKSUM_MISMATCH", declared, observed)
    if declared:
        return "DECLARED_CHECKSUM", declared, observed
    if observed:
        return "CHECKSUM_REGISTRATION_CANDIDATE", declared, observed
    return "CHECKSUM_UNAVAILABLE", declared, observed


def _provisioning_record(candidate: Mapping[str, Any], target_path: str, trace: str) -> ExternalModelProvisioningRecordV1:
    source = _optional_norm(candidate.get("source_file_ref"))
    target_id = _norm(candidate.get("target_model_asset_id")) or YOLO11N_ASSET_ID
    copy_required = bool(candidate.get("copy_required", bool(source and not _path_matches_governed(source, target_path))))
    copy_executed = bool(candidate.get("copy_executed", False))
    valid = target_id == YOLO11N_ASSET_ID and bool(target_path) and bool(candidate.get("candidate_only", True))
    return ExternalModelProvisioningRecordV1(
        source_file_ref=source,
        target_model_asset_id=target_id,
        target_governed_path=target_path,
        provisioning_source_type=_norm(candidate.get("provisioning_source_type")) or "EXTERNAL_LOCAL_FILE",
        expected_filename=_norm(candidate.get("expected_filename")) or YOLO11N_EXPECTED_ASSET_FILENAME,
        expected_family=_norm(candidate.get("expected_family")) or "yolo",
        expected_model_name=_norm(candidate.get("expected_model_name")) or "yolo11n",
        provenance_ref=_norm(candidate.get("provenance_ref")) or "provenance:external-provisioning-unresolved",
        copy_required=copy_required,
        copy_executed=copy_executed,
        registration_required=bool(candidate.get("registration_required", True)),
        candidate_only=bool(candidate.get("candidate_only", True)),
        provisioning_status=(
            "PROVISIONING_READY_FOR_CONTROLLED_COPY" if valid and copy_required and not copy_executed else
            "PROVISIONING_CANDIDATE_ACCEPTED" if valid and not copy_required and not copy_executed else
            "PROVISIONING_COPY_RECORDED" if valid and copy_executed else
            "PROVISIONING_REJECTED"
        ),
        trace_ref=trace,
    )


def resolve_yolo11n_external_provisioning_v1(
    candidate: Optional[Mapping[str, Any]] = None,
) -> YOLO11nExternalProvisioningAdmissionV1:
    supplied = dict(candidate or {})
    target_path = _norm(supplied.get("target_governed_path")) or YOLO11N_EXPECTED_ASSET_PATH
    trace = _trace(repr(supplied))
    provisioning = _provisioning_record(supplied, target_path, trace)
    physical = _physical_verification(supplied, target_path, trace)
    checksum, declared, observed = _checksum_status(supplied)
    dependency = _norm(supplied.get("dependency_status")) or "PYTHON_DEPENDENCY_UNRESOLVED"
    if dependency not in DEPENDENCY_STATUSES:
        dependency = "PYTHON_DEPENDENCY_UNRESOLVED"
    identity = _norm(supplied.get("identity_status")) or "MODEL_ASSET_IDENTIFIED_UNIQUE"
    if provisioning.target_model_asset_id != YOLO11N_ASSET_ID:
        identity = "MODEL_ASSET_IDENTITY_CONFLICT"
    if bool(supplied.get("filename_only_identity")) or (not supplied.get("target_model_asset_id") and not supplied.get("provenance_ref")):
        identity = "MODEL_ASSET_PROVENANCE_UNRESOLVED"
    if checksum == "CHECKSUM_MISMATCH":
        identity = "MODEL_ASSET_FINGERPRINT_MISMATCH"
    readiness_candidate = {
        "registered_asset_id": YOLO11N_ASSET_ID,
        "physical_asset_status": "ASSET_PRESENT" if physical.governed_path_match and physical.is_regular_file else "ASSET_NOT_PRESENT",
        "declared_checksum": declared,
        "observed_checksum": observed,
        "dependency_status": "PYTHON_DEPENDENCY_READY" if dependency == "PYTHON_DEPENDENCY_VERIFIED" else "PYTHON_DEPENDENCY_UNRESOLVED",
    }
    readiness = resolve_yolo11n_readiness_v1(readiness_candidate)
    technical = "ADMISSION_BLOCKED_ASSET_MISSING"
    if physical.physical_asset_status == "ASSET_NOT_PRESENT":
        technical = "ADMISSION_BLOCKED_ASSET_MISSING"
    elif physical.physical_asset_status in ("ASSET_INVALID_FILE", "ASSET_PATH_MISMATCH"):
        technical = "ADMISSION_BLOCKED_PHYSICAL_ASSET"
    elif checksum == "CHECKSUM_MISMATCH":
        technical = "ADMISSION_BLOCKED_CHECKSUM"
    elif provisioning.provisioning_status == "PROVISIONING_REJECTED":
        technical = "ADMISSION_BLOCKED_IDENTITY"
    elif identity != "MODEL_ASSET_IDENTIFIED_UNIQUE":
        technical = "ADMISSION_BLOCKED_IDENTITY"
    elif checksum in ("CHECKSUM_MISMATCH", "CHECKSUM_UNAVAILABLE", "CHECKSUM_REGISTRATION_CANDIDATE", "DECLARED_CHECKSUM"):
        technical = "ADMISSION_BLOCKED_CHECKSUM"
    elif readiness.model_contract_status != "RESOLVED" or readiness.loader_contract_status != "RESOLVED" or readiness.provider_adapter_status != "RESOLVED" or readiness.capability_contract_status != "RESOLVED" or readiness.evidence_contract_status != "RESOLVED":
        technical = "ADMISSION_BLOCKED_CONTRACT"
    elif dependency != "PYTHON_DEPENDENCY_VERIFIED":
        technical = "ADMISSION_BLOCKED_DEPENDENCY"
    else:
        technical = "ADMISSION_READY_CANDIDATE"
    physical_status = physical.physical_asset_status
    if technical == "ADMISSION_READY_CANDIDATE":
        physical_status = "ASSET_PRESENT_VERIFIED_CANDIDATE"
    physical = PhysicalAssetVerificationV1(
        file_exists=physical.file_exists,
        is_regular_file=physical.is_regular_file,
        file_size=physical.file_size,
        observed_filename=physical.observed_filename,
        observed_extension=physical.observed_extension,
        observed_path=physical.observed_path,
        governed_path_match=physical.governed_path_match,
        physical_asset_status=physical_status,
        trace_ref=physical.trace_ref,
    )
    return YOLO11nExternalProvisioningAdmissionV1(
        target_model="YOLO11n",
        target_asset_id=YOLO11N_ASSET_ID,
        expected_governed_path=target_path,
        provisioning=provisioning,
        physical=physical,
        model_identity_status=identity,
        model_contract_status=readiness.model_contract_status,
        loader_contract_status=readiness.loader_contract_status,
        provider_adapter_status=readiness.provider_adapter_status,
        capability_contract_status=readiness.capability_contract_status,
        evidence_contract_status=readiness.evidence_contract_status,
        checksum_status=checksum,
        declared_checksum=declared,
        observed_checksum=observed,
        dependency_status=dependency,
        dependency_requirements=readiness.dependency_requirements,
        technical_admission_status=technical,
        commercial_license_status=readiness.commercial_license_status,
        model_inference_executed=False,
        provider_invocation_executed=False,
        network_access=False,
        automatic_model_download=False,
        automatic_package_download=False,
        automatic_dependency_install=False,
        loader_guessing=False,
        filename_only_identity=bool(supplied.get("filename_only_identity", False)),
        extension_only_identity=bool(supplied.get("extension_only_identity", False)),
        human_contract_selection_required_normal_path=False,
        provider_semantic_authority=False,
        truth_declared=False,
        fact_admitted=False,
        field_mutation=False,
        current_world_truth_declaration=False,
        ocr_execution=False,
        slam_execution=False,
        vlm_execution=False,
        semantic_compression=False,
        trace_ref=trace,
        provenance_refs=(trace, provisioning.provenance_ref, f"model-asset:{YOLO11N_ASSET_ID}", f"manifest:{target_path}"),
    )


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
