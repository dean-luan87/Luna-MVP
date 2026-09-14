from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from ..model_contract_repository_registry_v1 import build_model_contract_repository_v1
from ..model_contract_repository_resolver_v1 import identify_model_asset_v1, resolve_model_contract_v1


IDENTITY_STATUSES = (
    "MODEL_ASSET_IDENTIFIED_UNIQUE",
    "MODEL_ASSET_NOT_REGISTERED",
    "MODEL_ASSET_IDENTITY_AMBIGUOUS",
    "MODEL_ASSET_IDENTITY_CONFLICT",
    "MODEL_ASSET_PROVENANCE_UNRESOLVED",
)
PHYSICAL_ASSET_STATUSES = (
    "ASSET_PRESENT",
    "ASSET_NOT_PRESENT",
    "ASSET_NOT_REGISTERED",
    "ASSET_IDENTITY_UNRESOLVED",
    "ASSET_CONTRACT_MISMATCH",
    "ASSET_READY_CANDIDATE",
)
ADMISSION_STATUSES = (
    "ADMISSION_READY_CANDIDATE",
    "ADMISSION_BLOCKED_ASSET_MISSING",
    "ADMISSION_BLOCKED_IDENTITY",
    "ADMISSION_BLOCKED_CONTRACT",
    "ADMISSION_BLOCKED_DEPENDENCY",
    "ADMISSION_BLOCKED_LOADER",
    "ADMISSION_BLOCKED_PROVIDER",
)


@dataclass(frozen=True)
class RealModelAssetAdmissionV1:
    target_model: str
    target_route_role: str
    physical_asset_status: str
    model_identity_status: str
    model_contract_status: str
    loader_contract_status: str
    provider_adapter_status: str
    capability_contract_status: str
    evidence_contract_status: str
    dependency_status: str
    admission_status: str
    model_asset_id: Optional[str]
    loader_contract_id: Optional[str]
    provider_adapter_contract_id: Optional[str]
    capability_contract_ids: Tuple[str, ...]
    evidence_contract_ids: Tuple[str, ...]
    candidate_only: bool
    truth_declared: bool
    fact_admitted: bool
    provider_semantic_authority: bool
    human_contract_selection_required_normal_path: bool
    model_inference_executed: bool
    provider_invocation_executed: bool
    network_access: bool
    automatic_model_download: bool
    automatic_package_download: bool
    loader_guessing: bool
    extension_based_loader_selection: bool
    field_state_mutation: bool
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
    return "trace:model-asset-admission:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def physical_asset_status_v1(candidate: Mapping[str, Any]) -> str:
    explicit = _norm(candidate.get("physical_asset_status"))
    if explicit:
        return explicit
    path = _norm(candidate.get("physical_path"))
    if not path:
        return "ASSET_NOT_PRESENT"
    return "ASSET_PRESENT" if Path(path).is_file() else "ASSET_NOT_PRESENT"


def _identity_input(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    keys = ("model_family", "model_name", "model_version", "weights_version", "weights_path", "checksum")
    return {key: candidate[key] for key in keys if candidate.get(key) not in (None, "")}


def _identify(candidate: Mapping[str, Any], repository: Mapping[str, Any]) -> Tuple[str, Optional[str], Tuple[str, ...], Tuple[str, ...]]:
    registered_id = _norm(candidate.get("registered_asset_id"))
    manifest_id = _norm(candidate.get("manifest_model_asset_id"))
    conflicts = []
    if registered_id and manifest_id and registered_id != manifest_id:
        return "MODEL_ASSET_IDENTITY_CONFLICT", None, (), (registered_id, manifest_id)
    selected_id = registered_id or manifest_id
    if selected_id:
        asset = (repository.get("model_assets") or {}).get(selected_id)
        if not asset:
            return "MODEL_ASSET_NOT_REGISTERED", None, ("registered_asset_id",), (selected_id,)
        for key in ("model_family", "model_name", "model_version", "weights_version"):
            supplied = _norm(candidate.get(key))
            if supplied and supplied != _norm(asset.get(key)):
                conflicts.append(f"{key}:{supplied}!={asset.get(key)}")
        if conflicts:
            return "MODEL_ASSET_IDENTITY_CONFLICT", None, ("explicit_identity",), tuple(conflicts)
        return "MODEL_ASSET_IDENTIFIED_UNIQUE", selected_id, ("registered_asset_id" if registered_id else "manifest_model_asset_id",), ()
    descriptor = _identity_input(candidate)
    if set(descriptor) == {"weights_path"}:
        return "MODEL_ASSET_PROVENANCE_UNRESOLVED", None, ("weights_path_only",), ()
    if not descriptor:
        return "MODEL_ASSET_PROVENANCE_UNRESOLVED", None, (), ()
    identity = identify_model_asset_v1(descriptor, repository)
    if identity.confidence_status == "AMBIGUOUS":
        return "MODEL_ASSET_IDENTITY_AMBIGUOUS", None, identity.match_basis, identity.ambiguity_refs
    if identity.matched_model_asset_id:
        return "MODEL_ASSET_IDENTIFIED_UNIQUE", identity.matched_model_asset_id, identity.match_basis, ()
    return "MODEL_ASSET_NOT_REGISTERED", None, identity.match_basis, ()


def resolve_real_model_asset_admission_v1(
    candidate: Mapping[str, Any],
    *,
    repository: Optional[Mapping[str, Any]] = None,
) -> RealModelAssetAdmissionV1:
    repo = repository or build_model_contract_repository_v1()
    physical_status = physical_asset_status_v1(candidate)
    identity_status, asset_id, identity_basis, conflict_refs = _identify(candidate, repo)
    target_model = _norm(candidate.get("target_model")) or _norm(candidate.get("model_name")) or "YOLO11n"
    route = (repo.get("production_vision_routes") or {}).get(asset_id or "", {})
    target_role = str(route.get("role") or ("STABILITY_COMPARATOR" if target_model.lower() == "yolo11n" else "UNKNOWN"))
    defaults = {
        "target_model": target_model,
        "target_route_role": target_role,
        "physical_asset_status": physical_status,
        "model_identity_status": identity_status,
        "model_contract_status": "UNRESOLVED",
        "loader_contract_status": "UNRESOLVED",
        "provider_adapter_status": "UNRESOLVED",
        "capability_contract_status": "UNRESOLVED",
        "evidence_contract_status": "UNRESOLVED",
        "dependency_status": _norm(candidate.get("dependency_status")) or "UNRESOLVED",
        "admission_status": "ADMISSION_BLOCKED_IDENTITY",
        "model_asset_id": asset_id,
        "loader_contract_id": None,
        "provider_adapter_contract_id": None,
        "capability_contract_ids": (),
        "evidence_contract_ids": (),
        "candidate_only": True,
        "truth_declared": False,
        "fact_admitted": False,
        "provider_semantic_authority": False,
        "human_contract_selection_required_normal_path": False,
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "loader_guessing": False,
        "extension_based_loader_selection": False,
        "field_state_mutation": False,
        "current_world_truth_declaration": False,
        "intent_mutation": False,
        "task_mutation": False,
        "decision_mutation": False,
        "route_reuse_owner": "Model Manager / Model Governance",
        "identity_basis": identity_basis,
        "conflict_refs": conflict_refs,
        "trace_ref": _trace(repr(dict(candidate))),
        "provenance_refs": (),
    }
    if identity_status != "MODEL_ASSET_IDENTIFIED_UNIQUE":
        defaults["physical_asset_status"] = "ASSET_IDENTITY_UNRESOLVED" if identity_status == "MODEL_ASSET_PROVENANCE_UNRESOLVED" else physical_status
        return RealModelAssetAdmissionV1(**defaults)

    dependency = _norm(candidate.get("dependency_status")) or "UNRESOLVED"
    dependency_satisfied = dependency == "PYTHON_DEPENDENCY_READY"
    dependency_input = True if dependency_satisfied else False if dependency == "PYTHON_DEPENDENCY_NOT_READY" else None
    base = resolve_model_contract_v1(
        {"model_asset_id": asset_id},
        repository=repo,
        deployment_requirements={"network_forbidden": True, "dependencies_satisfied": dependency_input},
    )
    asset = (repo.get("model_assets") or {})[asset_id]
    reasons = set(base.compatibility.reasons)
    defaults.update(
        {
            "model_contract_status": "RESOLVED" if base.model_asset_id else "BLOCKED",
            "loader_contract_status": "RESOLVED" if base.loader_contract_id and base.loader_contract_id in (repo.get("loader_contracts") or {}) else "MISSING",
            "provider_adapter_status": "MISMATCH" if "ADAPTER_LOADER_MISMATCH" in reasons else "RESOLVED" if base.provider_adapter_contract_id else "MISSING",
            "capability_contract_status": "RESOLVED" if base.capability_contract_ids else "MISSING",
            "evidence_contract_status": "RESOLVED" if base.evidence_contract_ids else "MISSING",
            "dependency_status": "PYTHON_DEPENDENCY_READY" if dependency_satisfied else "PYTHON_DEPENDENCY_NOT_READY" if dependency == "PYTHON_DEPENDENCY_NOT_READY" else "PYTHON_DEPENDENCY_UNRESOLVED",
            "loader_contract_id": base.loader_contract_id,
            "provider_adapter_contract_id": base.provider_adapter_contract_id,
            "capability_contract_ids": base.capability_contract_ids,
            "evidence_contract_ids": base.evidence_contract_ids,
            "identity_basis": identity_basis,
            "provenance_refs": (base.trace_ref, f"manifest:{asset.get('weights_path')}", f"model-asset:{asset_id}"),
        }
    )
    evidence = next(iter((repo.get("evidence_contracts") or {}).values()), {})
    defaults["candidate_only"] = bool(evidence.get("candidate_only", True))
    defaults["truth_declared"] = bool(evidence.get("truth_declared", False))
    defaults["fact_admitted"] = bool(evidence.get("fact_admitted", False))
    if defaults["physical_asset_status"] == "ASSET_PRESENT":
        defaults["physical_asset_status"] = "ASSET_READY_CANDIDATE" if dependency_satisfied and not reasons else "ASSET_PRESENT"
    if defaults["physical_asset_status"] != "ASSET_READY_CANDIDATE" and physical_status != "ASSET_PRESENT":
        defaults["admission_status"] = "ADMISSION_BLOCKED_ASSET_MISSING"
    elif defaults["loader_contract_status"] == "MISSING":
        defaults["admission_status"] = "ADMISSION_BLOCKED_LOADER"
    elif defaults["provider_adapter_status"] in ("MISSING", "MISMATCH"):
        defaults["admission_status"] = "ADMISSION_BLOCKED_PROVIDER"
    elif defaults["capability_contract_status"] != "RESOLVED" or defaults["evidence_contract_status"] != "RESOLVED" or base.compatibility.status != "COMPATIBLE":
        defaults["admission_status"] = "ADMISSION_BLOCKED_CONTRACT"
    elif not dependency_satisfied:
        defaults["admission_status"] = "ADMISSION_BLOCKED_DEPENDENCY"
    else:
        defaults["admission_status"] = "ADMISSION_READY_CANDIDATE"
    return RealModelAssetAdmissionV1(**defaults)


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
