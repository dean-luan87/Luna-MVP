from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from typing import Any, Dict, Mapping, Optional, Tuple

from ..model_contract_repository_registry_v1 import build_model_contract_repository_v1
from ..model_contract_repository_resolver_v1 import resolve_model_contract_v1


ROUTE_RESOLUTION_STATUSES = (
    "RESOLVED_UNIQUE",
    "ASSET_NOT_PRESENT",
    "NO_MATCH",
    "AMBIGUOUS_MATCH",
    "CONTRACT_CONFLICT",
    "CONTRACT_DEPRECATED",
    "CONTRACT_BLOCKED",
)


@dataclass(frozen=True)
class ProductionVisionRouteResolutionV1:
    model_asset_id: Optional[str]
    model_name: Optional[str]
    model_version: Optional[str]
    route_role: Optional[str]
    runtime_priority: Optional[str]
    benchmark_candidate: bool
    do_not_invest_further: bool
    route_resolution_status: str
    contract_resolution_status: str
    asset_presence_status: str
    loader_contract_id: Optional[str]
    provider_adapter_contract_id: Optional[str]
    capability_contract_ids: Tuple[str, ...]
    evidence_contract_ids: Tuple[str, ...]
    deployment_profile_refs: Tuple[str, ...]
    benchmark_profile_refs: Tuple[str, ...]
    license_metadata: Dict[str, Any]
    compatibility_status: str
    compatibility_reasons: Tuple[str, ...]
    contract_admission: str
    production_admission: str
    best_fit_status: str
    human_contract_selection_required: bool
    automatic_model_upgrade: bool = False
    automatic_model_download: bool = False
    network_access: bool = False
    model_inference_executed: bool = False
    provider_invocation_executed: bool = False
    cognitive_mutation: bool = False
    provider_semantic_authority: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)


def _trace(key: str) -> str:
    return "trace:production-vision-route:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def resolve_production_vision_model_route_v1(
    descriptor: Mapping[str, Any],
    *,
    repository: Optional[Mapping[str, Any]] = None,
    asset_presence: Optional[Mapping[str, str]] = None,
) -> ProductionVisionRouteResolutionV1:
    repo = repository or build_model_contract_repository_v1()
    presence = asset_presence or {}
    base = resolve_model_contract_v1(
        descriptor,
        repository=repo,
        deployment_requirements={"network_forbidden": True, "dependencies_satisfied": True},
    )
    if not base.model_asset_id:
        return ProductionVisionRouteResolutionV1(
            model_asset_id=None,
            model_name=None,
            model_version=None,
            route_role=None,
            runtime_priority=None,
            benchmark_candidate=False,
            do_not_invest_further=False,
            route_resolution_status=base.resolution_status,
            contract_resolution_status=base.resolution_status,
            asset_presence_status="UNKNOWN",
            loader_contract_id=base.loader_contract_id,
            provider_adapter_contract_id=base.provider_adapter_contract_id,
            capability_contract_ids=base.capability_contract_ids,
            evidence_contract_ids=base.evidence_contract_ids,
            deployment_profile_refs=(),
            benchmark_profile_refs=(),
            license_metadata={},
            compatibility_status=base.compatibility.status,
            compatibility_reasons=base.compatibility.reasons,
            contract_admission=base.admission_status,
            production_admission="NOT_YET_PROVEN",
            best_fit_status="NOT_EVALUATED",
            human_contract_selection_required=base.human_contract_selection_required,
            trace_ref=_trace(repr(dict(descriptor))),
            provenance_refs=(base.trace_ref,),
        )

    asset = (repo.get("model_assets") or {})[base.model_asset_id]
    route = (repo.get("production_vision_routes") or {}).get(base.model_asset_id, {})
    asset_presence_status = str(presence.get(base.model_asset_id, "ASSET_NOT_PRESENT"))
    route_status = base.resolution_status
    contract_admission = base.admission_status
    if asset_presence_status != "AVAILABLE_REFERENCE":
        route_status = "ASSET_NOT_PRESENT"
        contract_admission = "BLOCKED"
    elif base.admission_status != "ADMITTED":
        contract_admission = "BLOCKED"

    trace = _trace(base.trace_ref + ":" + base.model_asset_id)
    return ProductionVisionRouteResolutionV1(
        model_asset_id=base.model_asset_id,
        model_name=str(asset.get("model_name")),
        model_version=str(asset.get("model_version")),
        route_role=route.get("role"),
        runtime_priority=route.get("runtime_priority"),
        benchmark_candidate=bool(route.get("benchmark_candidate")),
        do_not_invest_further=bool(route.get("do_not_invest_further")),
        route_resolution_status=route_status,
        contract_resolution_status=base.resolution_status,
        asset_presence_status=asset_presence_status,
        loader_contract_id=base.loader_contract_id,
        provider_adapter_contract_id=base.provider_adapter_contract_id,
        capability_contract_ids=base.capability_contract_ids,
        evidence_contract_ids=base.evidence_contract_ids,
        deployment_profile_refs=tuple(asset.get("deployment_profile_refs") or ()),
        benchmark_profile_refs=tuple(asset.get("benchmark_profile_refs") or ()),
        license_metadata=dict((repo.get("license_profiles") or {}).get(base.model_asset_id, {})),
        compatibility_status=base.compatibility.status,
        compatibility_reasons=base.compatibility.reasons,
        contract_admission=contract_admission,
        production_admission=str(route.get("production_admission", "NOT_YET_PROVEN")),
        best_fit_status="NOT_EVALUATED" if route.get("best_fit") is False else "UNPROVEN",
        human_contract_selection_required=base.human_contract_selection_required,
        trace_ref=trace,
        provenance_refs=tuple(
            item
            for item in (
                trace,
                base.trace_ref,
                f"manifest:{asset.get('weights_path')}",
                f"route-role:{route.get('role')}",
            )
            if item
        ),
    )


def to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)
