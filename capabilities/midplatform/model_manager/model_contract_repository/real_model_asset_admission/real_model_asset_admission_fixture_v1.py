from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..model_contract_repository_registry_v1 import build_model_contract_repository_v1
from .real_model_asset_admission_types_v1 import RealModelAssetAdmissionV1, resolve_real_model_asset_admission_v1, to_dict


YOLO11 = "model-asset:yolo11n:weights-v1"
YOLO26 = "model-asset:yolo26n:weights-v1"
EVIDENCE = "evidence:visual-detection-candidate:v1"


def build_real_model_asset_admission_cases_v1() -> List[Dict[str, Any]]:
    return [
        {"case_id": "RMA-01", "title": "YOLO11 manifest exists but physical asset absent", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_NOT_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "expected_kind": "admission", "expected": "ADMISSION_BLOCKED_ASSET_MISSING"},
        {"case_id": "RMA-02", "title": "physical file exists but asset is not registered", "candidate": {"target_model": "YOLO11n", "model_name": "unregistered11n", "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "identity_admission", "expected": ("MODEL_ASSET_NOT_REGISTERED", "ADMISSION_BLOCKED_IDENTITY")},
        {"case_id": "RMA-03", "title": "registered asset and unique contract binding", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "identity", "expected": "MODEL_ASSET_IDENTIFIED_UNIQUE"},
        {"case_id": "RMA-04", "title": "two matching asset identities are ambiguous", "candidate": {"target_model": "YOLO11n", "model_family": "yolo", "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "identity_admission", "expected": ("MODEL_ASSET_IDENTITY_AMBIGUOUS", "ADMISSION_BLOCKED_IDENTITY")},
        {"case_id": "RMA-05", "title": "manifest and registered identity conflict", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "manifest_model_asset_id": YOLO26, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "identity_admission", "expected": ("MODEL_ASSET_IDENTITY_CONFLICT", "ADMISSION_BLOCKED_IDENTITY")},
        {"case_id": "RMA-06", "title": "extension does not select loader", "candidate": {"target_model": "YOLO11n", "physical_path": "/external/yolo11n.pt", "physical_asset_status": "ASSET_PRESENT"}, "expected_kind": "extension_guard", "expected": ("MODEL_ASSET_PROVENANCE_UNRESOLVED", False)},
        {"case_id": "RMA-07", "title": "valid identity with missing loader contract", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "repository_variant": "missing_loader", "expected_kind": "admission", "expected": "ADMISSION_BLOCKED_LOADER"},
        {"case_id": "RMA-08", "title": "valid loader with provider adapter mismatch", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "repository_variant": "provider_mismatch", "expected_kind": "admission", "expected": "ADMISSION_BLOCKED_PROVIDER"},
        {"case_id": "RMA-09", "title": "valid contracts with unresolved dependency", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "expected_kind": "admission", "expected": "ADMISSION_BLOCKED_DEPENDENCY"},
        {"case_id": "RMA-10", "title": "all static prerequisites satisfied", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "ready", "expected": ("ASSET_READY_CANDIDATE", "ADMISSION_READY_CANDIDATE", False)},
        {"case_id": "RMA-11", "title": "ready candidate preserves candidate-only evidence", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "evidence_boundary", "expected": (True, False, False, False)},
        {"case_id": "RMA-12", "title": "ready candidate does not mutate cognition or world", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "mutation_boundary", "expected": (False, False, False, False, False)},
        {"case_id": "RMA-13", "title": "network requirement cannot be introduced", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "network_guard", "expected": False},
        {"case_id": "RMA-14", "title": "automatic download cannot be introduced", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "download_guard", "expected": (False, False)},
        {"case_id": "RMA-15", "title": "normal path does not require human contract selection", "candidate": {"target_model": "YOLO11n", "registered_asset_id": YOLO11, "physical_asset_status": "ASSET_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_READY"}, "expected_kind": "human_selection", "expected": False},
        {"case_id": "RMA-16", "title": "YOLO26 reuses admission architecture without execution", "candidate": {"target_model": "YOLO26n", "registered_asset_id": YOLO26, "physical_asset_status": "ASSET_NOT_PRESENT", "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "expected_kind": "generic_reuse", "expected": ("Model Manager / Model Governance", "PRIMARY_CANDIDATE", False)},
    ]


def _repository_variant(name: str) -> Dict[str, Any]:
    repo = build_model_contract_repository_v1()
    assets = repo["model_assets"]
    if name == "missing_loader":
        assets[YOLO11]["declared_loader_contract_id"] = "loader:missing-modern"
    elif name == "provider_mismatch":
        assets[YOLO11]["declared_loader_contract_id"] = "loader:modern-unrelated"
        repo["loader_contracts"]["loader:modern-unrelated"] = dict(repo["loader_contracts"]["loader:ultralytics:yolo:v1"], loader_contract_id="loader:modern-unrelated")
    return repo


def _resolve(case: Dict[str, Any]) -> RealModelAssetAdmissionV1:
    return resolve_real_model_asset_admission_v1(
        case["candidate"],
        repository=_repository_variant(str(case.get("repository_variant") or "")),
    )


def evaluate_real_model_asset_admission_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    result = _resolve(case)
    kind = case["expected_kind"]
    expected = case["expected"]
    if kind == "admission":
        actual: Any = result.admission_status
    elif kind == "identity_admission":
        actual = (result.model_identity_status, result.admission_status)
    elif kind == "identity":
        actual = result.model_identity_status
    elif kind == "extension_guard":
        actual = (result.model_identity_status, result.extension_based_loader_selection)
    elif kind == "ready":
        actual = (result.physical_asset_status, result.admission_status, result.model_inference_executed)
    elif kind == "evidence_boundary":
        actual = (result.candidate_only, result.truth_declared, result.fact_admitted, result.provider_semantic_authority)
    elif kind == "mutation_boundary":
        actual = (result.field_state_mutation, result.current_world_truth_declaration, result.intent_mutation, result.task_mutation, result.decision_mutation)
    elif kind == "network_guard":
        actual = result.network_access
    elif kind == "download_guard":
        actual = (result.automatic_model_download, result.automatic_package_download)
    elif kind == "human_selection":
        actual = result.human_contract_selection_required_normal_path
    else:
        actual = (result.route_reuse_owner, result.target_route_role, result.provider_invocation_executed)
    return {"scenario_id": case["case_id"], "title": case["title"], "expectation_kind": kind, "expected": expected, "actual": actual, "passed": actual == expected, "admission": to_dict(result)}
