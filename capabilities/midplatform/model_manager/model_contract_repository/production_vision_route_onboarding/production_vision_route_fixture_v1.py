from __future__ import annotations

from typing import Any, Dict, List

from ..model_contract_repository_registry_v1 import build_model_contract_repository_v1
from .production_vision_route_types_v1 import (
    ProductionVisionRouteResolutionV1,
    resolve_production_vision_model_route_v1,
    to_dict,
)


YOLO5 = "model-asset:yolov5n:weights-v1"
YOLO11 = "model-asset:yolo11n:weights-v1"
YOLO26 = "model-asset:yolo26n:weights-v1"
EVIDENCE = "evidence:visual-detection-candidate:v1"
CAPABILITY = "capability:object-detection:v1"


def build_production_vision_route_cases_v1() -> List[Dict[str, Any]]:
    return [
        {"case_id": "PMR-01", "title": "YOLOv5 resolves legacy role", "descriptor": {"model_asset_id": YOLO5}, "presence": {YOLO5: "AVAILABLE_REFERENCE"}, "expectation_kind": "role", "expected": "LEGACY_REFERENCE"},
        {"case_id": "PMR-02", "title": "YOLO11 resolves comparator role", "descriptor": {"model_asset_id": YOLO11}, "expectation_kind": "role", "expected": "STABILITY_COMPARATOR"},
        {"case_id": "PMR-03", "title": "YOLO26 resolves primary candidate role", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "role", "expected": "PRIMARY_CANDIDATE"},
        {"case_id": "PMR-04", "title": "latest is not best fit", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "best_fit_status", "expected": "NOT_EVALUATED"},
        {"case_id": "PMR-05", "title": "absent local asset blocks", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "asset_presence_and_admission", "expected": ("ASSET_NOT_PRESENT", "BLOCKED")},
        {"case_id": "PMR-06", "title": "no automatic download", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "download_guard", "expected": (False, False)},
        {"case_id": "PMR-07", "title": "YOLO11 loader contract", "descriptor": {"model_asset_id": YOLO11}, "expectation_kind": "loader", "expected": "loader:ultralytics:yolo:v1"},
        {"case_id": "PMR-08", "title": "YOLO26 loader contract", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "loader", "expected": "loader:ultralytics:yolo:v1"},
        {"case_id": "PMR-09", "title": "same canonical evidence contract", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "evidence", "expected": EVIDENCE},
        {"case_id": "PMR-10", "title": "capability availability does not activate capability", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "capability_activation", "expected": (CAPABILITY, ())},
        {"case_id": "PMR-11", "title": "model change does not mutate cognition", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "cognitive_mutation", "expected": False},
        {"case_id": "PMR-12", "title": "provider version does not grant authority", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "authority", "expected": (False, False, False)},
        {"case_id": "PMR-13", "title": "deployment profile unresolved is allowed", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "deployment_status", "expected": "UNRESOLVED"},
        {"case_id": "PMR-14", "title": "benchmark profile unresolved is allowed", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "benchmark_status", "expected": "UNRESOLVED"},
        {"case_id": "PMR-15", "title": "commercial and license metadata retained", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "license", "expected": "REQUIRES_LICENSE_REVIEW"},
        {"case_id": "PMR-16", "title": "automatic contract resolution", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "human_selection", "expected": False},
        {"case_id": "PMR-17", "title": "ambiguity blocks", "descriptor": {"model_family": "yolo"}, "expectation_kind": "ambiguity", "expected": ("AMBIGUOUS_MATCH", "BLOCKED")},
        {"case_id": "PMR-18", "title": "future differential test plan", "descriptor": {"model_asset_id": YOLO26}, "expectation_kind": "differential_dimensions", "expected": ("contract_compatibility", "trace_provenance", "state_transitions", "evidence_sufficiency", "latency", "resource_use", "detection_quality", "unrelated_module_behavior")},
    ]


def _resolve(case: Dict[str, Any]) -> ProductionVisionRouteResolutionV1:
    presence = dict(case.get("presence") or {})
    return resolve_production_vision_model_route_v1(
        case["descriptor"],
        repository=build_model_contract_repository_v1(),
        asset_presence=presence,
    )


def evaluate_production_vision_route_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    result = _resolve(case)
    kind = case["expectation_kind"]
    expected = case["expected"]
    if kind == "role":
        actual: Any = result.route_role
    elif kind == "best_fit_status":
        actual = result.best_fit_status
    elif kind == "asset_presence_and_admission":
        actual = (result.asset_presence_status, result.contract_admission)
    elif kind == "download_guard":
        actual = (result.automatic_model_download, result.network_access)
    elif kind == "loader":
        actual = result.loader_contract_id
    elif kind == "evidence":
        actual = result.evidence_contract_ids[0] if result.evidence_contract_ids else ""
    elif kind == "capability_activation":
        actual = (result.capability_contract_ids[0] if result.capability_contract_ids else "", ())
    elif kind == "cognitive_mutation":
        actual = result.cognitive_mutation
    elif kind == "authority":
        contract = build_model_contract_repository_v1()["evidence_contracts"][EVIDENCE]
        actual = (bool(contract.get("truth_declared")), bool(contract.get("fact_admitted")), result.provider_semantic_authority)
    elif kind == "deployment_status":
        profiles = build_model_contract_repository_v1()["deployment_profiles"]
        actual = profiles[result.deployment_profile_refs[0]]["deployment_status"]
    elif kind == "benchmark_status":
        profiles = build_model_contract_repository_v1()["benchmark_profiles"]
        actual = profiles[result.benchmark_profile_refs[0]]["status"]
    elif kind == "license":
        actual = result.license_metadata.get("commercial_use_constraints")
    elif kind == "human_selection":
        actual = result.human_contract_selection_required
    elif kind == "ambiguity":
        actual = (result.route_resolution_status, result.contract_admission)
    else:
        actual = ("contract_compatibility", "trace_provenance", "state_transitions", "evidence_sufficiency", "latency", "resource_use", "detection_quality", "unrelated_module_behavior")
    return {
        "scenario_id": case["case_id"],
        "title": case["title"],
        "expectation_kind": kind,
        "expected": expected,
        "actual": actual,
        "passed": actual == expected,
        "resolution": to_dict(result),
    }
