from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .model_contract_repository_registry_v1 import build_model_contract_repository_v1
from .model_contract_repository_types_v1 import (
    CompatibilityResultV1,
    ModelContractResolutionV1,
    ModelIdentityCandidateV1,
)


def _norm(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def _extension(path: str) -> str:
    return PurePosixPath(_norm(path)).suffix.lower().lstrip(".")


def _trace(identity_key: str) -> str:
    return "trace:model-contract:" + hashlib.sha256(identity_key.encode("utf-8")).hexdigest()[:20]


def resolve_local_source_package_v1(
    *, asset: Mapping[str, Any], loader: Optional[Mapping[str, Any]], repository: Mapping[str, Any]
) -> Tuple[Optional[Mapping[str, Any]], str, Tuple[str, ...]]:
    if not loader or not bool(loader.get("local_source_package_required")):
        return None, "NOT_REQUIRED", ()
    package_records = list((repository.get("local_source_packages") or {}).values())
    model_name = _norm(asset.get("model_name")).lower()
    model_family = _norm(asset.get("model_family")).lower()
    candidates = [
        item
        for item in package_records
        if loader.get("loader_contract_id") in tuple(item.get("compatible_loader_contract_ids") or ())
        and _norm(item.get("package_family")).lower() in {model_family, model_name, model_name.rstrip("n")}
    ]
    if len(candidates) == 0:
        return None, "NOT_FOUND", ()
    if len(candidates) > 1:
        return None, "AMBIGUOUS", tuple(str(item.get("local_source_package_id")) for item in candidates)
    package = candidates[0]
    status = str(package.get("status") or "MISSING")
    if status == "SUPPORTED":
        return package, "RESOLVED", (str(package.get("local_source_package_id")),)
    if status == "MISSING":
        return package, "NOT_FOUND", (str(package.get("local_source_package_id")),)
    return package, status, (str(package.get("local_source_package_id")),)


def identify_model_asset_v1(
    descriptor: Mapping[str, Any],
    repository: Mapping[str, Any],
) -> ModelIdentityCandidateV1:
    assets = list((repository.get("model_assets") or {}).values())
    explicit_id = _norm(descriptor.get("model_asset_id"))
    if explicit_id:
        item = (repository.get("model_assets") or {}).get(explicit_id)
        if item:
            return ModelIdentityCandidateV1(explicit_id, ("explicit_model_asset_id",), "EXACT", (), (explicit_id,))
        return ModelIdentityCandidateV1(None, ("explicit_model_asset_id",), "NO_MATCH", (), ())

    fields = ("model_family", "model_name", "model_version", "weights_version", "weights_path", "checksum")
    supplied = {key: _norm(descriptor.get(key)) for key in fields if _norm(descriptor.get(key))}
    if not supplied:
        return ModelIdentityCandidateV1(None, (), "NO_MATCH", (), ())

    candidates: List[Dict[str, Any]] = []
    for asset in assets:
        matched = 0
        for key, value in supplied.items():
            asset_value = _norm(asset.get(key))
            if key == "weights_path" and asset_value and value:
                if asset_value == value or PurePosixPath(asset_value).name == PurePosixPath(value).name:
                    matched += 1
            elif asset_value and asset_value == value:
                matched += 1
        if matched == len(supplied):
            candidates.append(asset)

    if not candidates and set(supplied) == {"weights_path"} and _extension(supplied["weights_path"]):
        return ModelIdentityCandidateV1(None, ("weight_extension_only",), "INSUFFICIENT", (), ())
    if len(candidates) == 1:
        item = candidates[0]
        return ModelIdentityCandidateV1(item["model_asset_id"], tuple(supplied), "EXACT", (), (item["model_asset_id"],))
    ambiguity = tuple(str(item.get("model_asset_id")) for item in candidates)
    return ModelIdentityCandidateV1(None, tuple(supplied), "AMBIGUOUS" if candidates else "NO_MATCH", ambiguity, ambiguity)


def validate_contract_compatibility_v1(
    *,
    asset: Mapping[str, Any],
    loader: Optional[Mapping[str, Any]],
    adapter: Optional[Mapping[str, Any]],
    capabilities: Sequence[Mapping[str, Any]],
    evidences: Sequence[Mapping[str, Any]],
    local_source_package: Optional[Mapping[str, Any]] = None,
    local_source_package_status: str = "NOT_FOUND",
    deployment_requirements: Optional[Mapping[str, Any]] = None,
) -> CompatibilityResultV1:
    reasons: List[str] = []
    rejected: List[str] = []
    dependency_status = "UNKNOWN"
    if not loader:
        reasons.append("MISSING_LOADER_CONTRACT")
    else:
        if str(asset.get("weight_format")) not in tuple(loader.get("supported_weight_formats") or ()):
            reasons.append("UNSUPPORTED_WEIGHT_FORMAT")
        if bool(loader.get("local_source_package_required")):
            if local_source_package_status in ("NOT_FOUND", "MISSING"):
                reasons.append("LOCAL_SOURCE_PACKAGE_REQUIRED")
                reasons.append("LOCAL_SOURCE_PACKAGE_NOT_FOUND")
            elif local_source_package_status == "AMBIGUOUS":
                reasons.append("LOCAL_SOURCE_PACKAGE_AMBIGUOUS")
            elif local_source_package_status in ("INCOMPATIBLE", "BLOCKED", "DEPRECATED"):
                reasons.append("LOCAL_SOURCE_PACKAGE_INCOMPATIBLE")
            elif local_source_package_status == "RESOLVED":
                if not tuple(local_source_package.get("required_files") or ()) or not tuple(local_source_package.get("validation_markers") or ()):
                    reasons.append("LOCAL_SOURCE_PACKAGE_INCOMPATIBLE")
                if local_source_package.get("network_allowed") is True or local_source_package.get("automatic_download_allowed") is True:
                    reasons.append("LOCAL_SOURCE_PACKAGE_NETWORK_POLICY_INVALID")
        if not tuple(loader.get("required_dependencies") or ()):
            dependency_status = "NOT_SATISFIED"
            reasons.append("DEPENDENCY_NOT_SATISFIED")
        elif deployment_requirements and deployment_requirements.get("dependencies_satisfied") is False:
            dependency_status = "NOT_SATISFIED"
            reasons.append("DEPENDENCY_NOT_SATISFIED")
        elif deployment_requirements and deployment_requirements.get("dependencies_satisfied") is True:
            dependency_status = "READY_CANDIDATE"
        if bool(loader.get("network_allowed")) and deployment_requirements and deployment_requirements.get("network_forbidden"):
            reasons.append("NETWORK_REQUIRED_BUT_FORBIDDEN")
        if str(loader.get("status")) in ("DEPRECATED", "REVOKED", "BLOCKED"):
            rejected.append(str(loader.get("loader_contract_id")))
            reasons.append("LOADER_CONTRACT_BLOCKED")
    if not adapter:
        reasons.append("MISSING_PROVIDER_ADAPTER_CONTRACT")
    else:
        if loader and loader.get("loader_contract_id") not in tuple(adapter.get("supported_loader_contracts") or ()):
            reasons.append("ADAPTER_LOADER_MISMATCH")
        if adapter.get("candidate_only_output") is not True:
            reasons.append("CANDIDATE_ONLY_OUTPUT_REQUIRED")
    if not capabilities:
        reasons.append("CAPABILITY_CONTRACT_MISSING")
    if not evidences:
        reasons.append("EVIDENCE_CONTRACT_MISSING")
    for capability in capabilities:
        if not set(capability.get("canonical_evidence_contract_refs") or ()).intersection(
            set(asset.get("declared_evidence_contract_ids") or ())
        ):
            reasons.append("CAPABILITY_EVIDENCE_CONFLICT")
    for evidence in evidences:
        if evidence.get("candidate_only") is not True or evidence.get("truth_declared") is True:
            reasons.append("EVIDENCE_CONTRACT_INCOMPATIBLE")
    status = "COMPATIBLE" if not reasons else "BLOCKED"
    return CompatibilityResultV1(
        status=status,
        model_asset_id=str(asset.get("model_asset_id")),
        loader_contract_id=str(loader.get("loader_contract_id")) if loader else None,
        provider_adapter_contract_id=str(adapter.get("provider_adapter_id")) if adapter else None,
        capability_contract_ids=tuple(str(x.get("capability_contract_id")) for x in capabilities),
        evidence_contract_ids=tuple(str(x.get("evidence_contract_id")) for x in evidences),
        reasons=tuple(dict.fromkeys(reasons)),
        rejected_contracts=tuple(dict.fromkeys(rejected)),
        trace_ref=_trace(str(asset.get("model_asset_id")) + ":compatibility"),
        local_source_package_id=(str(local_source_package.get("local_source_package_id")) if local_source_package else None),
        local_source_package_status=local_source_package_status,
        dependency_status=dependency_status,
    )


def resolve_model_contract_v1(
    descriptor: Mapping[str, Any],
    *,
    repository: Optional[Mapping[str, Any]] = None,
    deployment_requirements: Optional[Mapping[str, Any]] = None,
) -> ModelContractResolutionV1:
    repo = repository or build_model_contract_repository_v1()
    identity = identify_model_asset_v1(descriptor, repo)
    trace = _trace(repr(dict(descriptor)))
    if identity.confidence_status == "AMBIGUOUS":
        compatibility = CompatibilityResultV1("BLOCKED", None, None, None, (), (), ("AMBIGUOUS_MATCH",), identity.ambiguity_refs, trace)
        return ModelContractResolutionV1("AMBIGUOUS_MATCH", identity, None, None, None, (), (), compatibility, "BLOCKED", None, "NOT_FOUND", trace_ref=trace, provenance_refs=identity.ambiguity_refs)
    if not identity.matched_model_asset_id:
        compatibility = CompatibilityResultV1("BLOCKED", None, None, None, (), (), ("NO_MATCH",), (), trace)
        return ModelContractResolutionV1("NO_MATCH", identity, None, None, None, (), (), compatibility, "BLOCKED", None, "NOT_FOUND", trace_ref=trace)

    assets = repo["model_assets"]
    asset = assets[identity.matched_model_asset_id]
    loader_id = asset.get("declared_loader_contract_id")
    loader = (repo.get("loader_contracts") or {}).get(loader_id)
    local_source_package, local_source_package_status, local_source_package_refs = resolve_local_source_package_v1(
        asset=asset, loader=loader, repository=repo
    )
    adapter = next(
        (item for item in (repo.get("provider_adapter_contracts") or {}).values() if item.get("provider_family") == asset.get("provider_family")),
        None,
    )
    capabilities = [
        (repo.get("capability_contracts") or {})[item]
        for item in asset.get("declared_capability_contract_ids") or ()
        if item in (repo.get("capability_contracts") or {})
    ]
    evidences = [
        (repo.get("evidence_contracts") or {})[item]
        for item in asset.get("declared_evidence_contract_ids") or ()
        if item in (repo.get("evidence_contracts") or {})
    ]
    compatibility = validate_contract_compatibility_v1(
        asset=asset,
        loader=loader,
        adapter=adapter,
        capabilities=capabilities,
        evidences=evidences,
        local_source_package=local_source_package,
        local_source_package_status=local_source_package_status,
        deployment_requirements=deployment_requirements,
    )
    resolution_status = "RESOLVED_UNIQUE"
    if not loader or not adapter:
        resolution_status = "CONTRACT_CONFLICT"
    elif asset.get("status") == "DEPRECATED" or loader.get("status") == "DEPRECATED":
        resolution_status = "CONTRACT_DEPRECATED"
    elif asset.get("status") in ("BLOCKED", "QUARANTINED") or loader.get("status") in ("BLOCKED", "REVOKED"):
        resolution_status = "CONTRACT_BLOCKED"
    return ModelContractResolutionV1(
        resolution_status=resolution_status,
        identity=identity,
        model_asset_id=asset.get("model_asset_id"),
        loader_contract_id=loader_id,
        provider_adapter_contract_id=adapter.get("provider_adapter_id") if adapter else None,
        capability_contract_ids=tuple(item.get("capability_contract_id") for item in capabilities),
        evidence_contract_ids=tuple(item.get("evidence_contract_id") for item in evidences),
        compatibility=compatibility,
        admission_status="ADMITTED" if resolution_status == "RESOLVED_UNIQUE" and compatibility.status == "COMPATIBLE" else "BLOCKED",
        local_source_package_id=local_source_package_refs[0] if local_source_package_refs and local_source_package_status == "RESOLVED" else None,
        local_source_package_status=local_source_package_status,
        execution_admitted=False,
        trace_ref=trace,
        provenance_refs=tuple(
            item
            for item in (
                trace,
                f"manifest:{asset.get('weights_path')}",
                local_source_package.get("provenance_ref") if local_source_package else None,
            )
            if item
        ),
    )
