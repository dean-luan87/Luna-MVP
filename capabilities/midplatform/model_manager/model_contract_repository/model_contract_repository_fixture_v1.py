from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .model_contract_repository_registry_v1 import build_model_contract_repository_v1
from .model_contract_repository_resolver_v1 import resolve_model_contract_v1


def build_model_contract_repository_cases_v1() -> List[Dict[str, Any]]:
    return [
        {"case_id": "MCR-01", "title": "exact unique model match", "descriptor": {"model_asset_id": "model-asset:yolov5n:weights-v1"}, "expected": "RESOLVED_UNIQUE"},
        {"case_id": "MCR-02", "title": "unknown model", "descriptor": {"model_asset_id": "model-asset:unknown"}, "expected": "NO_MATCH"},
        {"case_id": "MCR-03", "title": "same family different version", "descriptor": {"model_family": "yolo", "model_name": "yolo11n", "model_version": "v11"}, "expected": "RESOLVED_UNIQUE"},
        {"case_id": "MCR-04", "title": "same extension different loader", "descriptor": {"weights_path": "same/model.pt"}, "expected": "AMBIGUOUS_MATCH"},
        {"case_id": "MCR-05", "title": "ambiguous contract blocks", "descriptor": {"model_family": "yolo", "model_name": "yolov5n", "model_version": "v5"}, "expected": "AMBIGUOUS_MATCH"},
        {"case_id": "MCR-06", "title": "missing loader blocks", "descriptor": {"model_asset_id": "model-asset:missing-loader"}, "expected": "CONTRACT_CONFLICT"},
        {"case_id": "MCR-07", "title": "unsupported weight format", "descriptor": {"model_asset_id": "model-asset:unsupported-format"}, "expected": "UNSUPPORTED_WEIGHT_FORMAT"},
        {"case_id": "MCR-08", "title": "missing local source package", "descriptor": {"model_asset_id": "model-asset:yolov5n:weights-v1"}, "expected": "LOCAL_SOURCE_PACKAGE_REQUIRED"},
        {"case_id": "MCR-09", "title": "network required but forbidden", "descriptor": {"model_asset_id": "model-asset:network-required"}, "expected": "NETWORK_REQUIRED_BUT_FORBIDDEN"},
        {"case_id": "MCR-10", "title": "adapter loader mismatch", "descriptor": {"model_asset_id": "model-asset:adapter-mismatch"}, "expected": "ADAPTER_LOADER_MISMATCH"},
        {"case_id": "MCR-11", "title": "capability supported", "descriptor": {"model_asset_id": "model-asset:yolov5n:weights-v1"}, "expected": "OBJECT_DETECTION"},
        {"case_id": "MCR-12", "title": "capability unsupported", "descriptor": {"model_asset_id": "model-asset:unsupported-capability"}, "expected": "CAPABILITY_CONTRACT_MISSING"},
        {"case_id": "MCR-13", "title": "evidence contract compatible", "descriptor": {"model_asset_id": "model-asset:yolo11n:weights-v1"}, "expected": "evidence:visual-detection-candidate:v1"},
        {"case_id": "MCR-14", "title": "evidence contract incompatible", "descriptor": {"model_asset_id": "model-asset:evidence-conflict"}, "expected": "EVIDENCE_CONTRACT_INCOMPATIBLE"},
        {"case_id": "MCR-15", "title": "deprecated model", "descriptor": {"model_asset_id": "model-asset:deprecated"}, "expected": "CONTRACT_DEPRECATED"},
        {"case_id": "MCR-16", "title": "blocked model", "descriptor": {"model_asset_id": "model-asset:blocked"}, "expected": "CONTRACT_BLOCKED"},
        {"case_id": "MCR-17", "title": "multiple versions coexist", "descriptor": {"model_asset_id": "model-asset:yolov5n:weights-v2"}, "expected": "RESOLVED_UNIQUE"},
        {"case_id": "MCR-18", "title": "upgrade preserves evidence contract", "descriptor": {"model_asset_id": "model-asset:yolo11n:weights-v1"}, "expected": "evidence:visual-detection-candidate:v1"},
        {"case_id": "MCR-19", "title": "upgrade expands capability", "descriptor": {"model_asset_id": "model-asset:expanded-capability"}, "expected": "CAPABILITY_EVIDENCE_CONFLICT"},
        {"case_id": "MCR-20", "title": "current yolov5n blocker", "descriptor": {"model_asset_id": "model-asset:yolov5n:weights-v1"}, "expected": "BLOCKED"},
        {"case_id": "MCR-21", "title": "automatic resolution without human input", "descriptor": {"model_asset_id": "model-asset:yolo11n:weights-v1"}, "expected": False},
        {"case_id": "MCR-22", "title": "ambiguity blocks automatic execution", "descriptor": {"model_family": "yolo", "model_name": "yolov5n", "model_version": "v5"}, "expected": False},
        {"case_id": "MCR-23", "title": "availability is not execution admission", "descriptor": {"model_asset_id": "model-asset:yolo11n:weights-v1"}, "expected": False},
        {"case_id": "MCR-24", "title": "loader compatibility is not semantic authority", "descriptor": {"model_asset_id": "model-asset:yolo11n:weights-v1"}, "expected": False},
    ]


def _fixture_repository() -> Dict[str, Any]:
    repo = build_model_contract_repository_v1()
    assets = repo["model_assets"]
    base = dict(assets["model-asset:yolov5n:weights-v1"])
    def add(asset_id: str, **updates: Any) -> None:
        item = dict(base)
        item.update(updates)
        item["model_asset_id"] = asset_id
        assets[asset_id] = item
    add("model-asset:missing-loader", declared_loader_contract_id="loader:missing", status="REGISTERED")
    add("model-asset:unsupported-format", weight_format="safetensors")
    add("model-asset:network-required", declared_loader_contract_id="loader:network", status="REGISTERED")
    add("model-asset:adapter-mismatch", declared_loader_contract_id="loader:unrelated")
    add("model-asset:unsupported-capability", declared_capability_contract_ids=("capability:missing",))
    add("model-asset:evidence-conflict", declared_evidence_contract_ids=("evidence:truth",))
    add("model-asset:deprecated", status="DEPRECATED")
    add("model-asset:blocked", status="BLOCKED")
    add("model-asset:expanded-capability", declared_capability_contract_ids=("capability:expanded",))
    add("model-asset:same-ext-a", model_name="same-ext-a", weights_path="same/model.pt", declared_loader_contract_id="loader:yolov5:torch-hub-local:v1")
    add("model-asset:same-ext-b", model_name="same-ext-b", weights_path="same/model.pt", declared_loader_contract_id="loader:ultralytics:yolo:v1")
    repo["loader_contracts"]["loader:network"] = dict(repo["loader_contracts"]["loader:yolov5:torch-hub-local:v1"], loader_contract_id="loader:network", network_allowed=True)
    repo["loader_contracts"]["loader:unrelated"] = dict(repo["loader_contracts"]["loader:yolov5:torch-hub-local:v1"], loader_contract_id="loader:unrelated")
    repo["evidence_contracts"]["evidence:truth"] = dict(repo["evidence_contracts"]["evidence:visual-detection-candidate:v1"], evidence_contract_id="evidence:truth", truth_declared=True)
    repo["capability_contracts"]["capability:expanded"] = dict(repo["capability_contracts"]["capability:object-detection:v1"], capability_contract_id="capability:expanded", canonical_evidence_contract_refs=("evidence:other:v1",))
    return repo


def evaluate_model_contract_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    repo = _fixture_repository()
    result = resolve_model_contract_v1(case["descriptor"], repository=repo, deployment_requirements={"network_forbidden": True, "dependencies_satisfied": False})
    expected = case["expected"]
    if case["case_id"] in {"MCR-07", "MCR-08", "MCR-09", "MCR-10", "MCR-12", "MCR-14", "MCR-19"}:
        actual = list(result.compatibility.reasons)
        passed = isinstance(expected, str) and expected in actual
        expectation_kind = "compatibility_reason_presence"
    elif case["case_id"] in {"MCR-11"}:
        actual = "OBJECT_DETECTION" if result.capability_contract_ids else ""
        passed = actual == expected
        expectation_kind = "capability_kind"
    elif case["case_id"] in {"MCR-13", "MCR-18"}:
        actual = result.evidence_contract_ids[0] if result.evidence_contract_ids else ""
        passed = actual == expected
        expectation_kind = "evidence_contract_id"
    elif case["case_id"] in {"MCR-20"}:
        actual = result.admission_status
        passed = actual == expected
        expectation_kind = "admission_status"
    elif case["case_id"] in {"MCR-21", "MCR-22", "MCR-23", "MCR-24"}:
        actual = result.human_contract_selection_required if case["case_id"] == "MCR-21" else result.execution_admitted
        passed = actual == expected
        expectation_kind = "boolean_guard"
    else:
        actual = result.resolution_status
        passed = actual == expected
        expectation_kind = "resolution_status"
    return {"scenario_id": case["case_id"], "title": case["title"], "expectation_kind": expectation_kind, "expected": expected, "actual": actual, "passed": passed, "resolution": result}
