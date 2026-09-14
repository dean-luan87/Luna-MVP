from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from .yolo11n_readiness_types_v1 import (
    YOLO11N_ASSET_ID,
    YOLO11N_EXPECTED_ASSET_PATH,
    resolve_yolo11n_readiness_v1,
    to_dict,
)


def build_yolo11n_readiness_cases_v1() -> List[Dict[str, Any]]:
    verified = {
        "registered_asset_id": YOLO11N_ASSET_ID,
        "physical_asset_status": "ASSET_PRESENT",
        "declared_checksum": "sha256:yolo11n-v1",
        "observed_checksum": "sha256:yolo11n-v1",
        "dependency_status": "PYTHON_DEPENDENCY_VERIFIED",
    }
    return [
        {"case_id": "Y11R-01", "title": "asset absent blocks", "candidate": {"registered_asset_id": YOLO11N_ASSET_ID}, "kind": "admission", "expected": "ADMISSION_BLOCKED_ASSET_MISSING"},
        {"case_id": "Y11R-02", "title": "expected asset path registered", "candidate": {"registered_asset_id": YOLO11N_ASSET_ID}, "kind": "registration", "expected": (YOLO11N_ASSET_ID, YOLO11N_EXPECTED_ASSET_PATH)},
        {"case_id": "Y11R-03", "title": "physical asset present candidate", "candidate": {**verified, "checksum_status": "CHECKSUM_UNAVAILABLE", "dependency_status": "PYTHON_DEPENDENCY_DECLARED"}, "kind": "physical", "expected": "ASSET_PRESENT"},
        {"case_id": "Y11R-04", "title": "checksum verified", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_DECLARED"}, "kind": "checksum", "expected": "CHECKSUM_VERIFIED"},
        {"case_id": "Y11R-05", "title": "checksum mismatch blocks", "candidate": {**verified, "observed_checksum": "sha256:other"}, "kind": "checksum_admission", "expected": ("CHECKSUM_MISMATCH", "ADMISSION_BLOCKED_CHECKSUM")},
        {"case_id": "Y11R-06", "title": "identity conflict blocks", "candidate": {**verified, "manifest_model_asset_id": "model-asset:yolo26n:weights-v1"}, "kind": "identity_admission", "expected": ("MODEL_ASSET_IDENTITY_CONFLICT", "ADMISSION_BLOCKED_IDENTITY")},
        {"case_id": "Y11R-07", "title": "dependency unresolved blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_UNRESOLVED", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11R-08", "title": "dependency missing blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_MISSING"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_MISSING", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11R-09", "title": "dependency version incompatible blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11R-10", "title": "dependency verified", "candidate": verified, "kind": "dependency", "expected": "PYTHON_DEPENDENCY_VERIFIED"},
        {"case_id": "Y11R-11", "title": "all prerequisites produce admission candidate", "candidate": verified, "kind": "ready", "expected": ("ASSET_READY_CANDIDATE", "ADMISSION_READY_CANDIDATE")},
        {"case_id": "Y11R-12", "title": "ready candidate does not execute inference", "candidate": verified, "kind": "execution_guards", "expected": (False, False)},
        {"case_id": "Y11R-13", "title": "no automatic download", "candidate": verified, "kind": "download_guards", "expected": (False, False, False)},
        {"case_id": "Y11R-14", "title": "no network", "candidate": verified, "kind": "network", "expected": False},
        {"case_id": "Y11R-15", "title": "no human contract selection", "candidate": verified, "kind": "human_selection", "expected": False},
        {"case_id": "Y11R-16", "title": "commercial license approval remains separate", "candidate": verified, "kind": "license", "expected": ("ADMISSION_READY_CANDIDATE", "REQUIRES_LICENSE_REVIEW")},
    ]


def evaluate_yolo11n_readiness_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    result = resolve_yolo11n_readiness_v1(case.get("candidate"))
    kind = case["kind"]
    expected = case["expected"]
    if kind == "admission":
        actual: Any = result.technical_admission_status
    elif kind == "registration":
        actual = (result.target_asset_id, result.expected_asset_path)
    elif kind == "physical":
        actual = result.physical_asset_status
    elif kind == "checksum":
        actual = result.checksum_status
    elif kind == "checksum_admission":
        actual = (result.checksum_status, result.technical_admission_status)
    elif kind == "identity_admission":
        actual = (result.model_identity_status, result.technical_admission_status)
    elif kind == "dependency_admission":
        actual = (result.dependency_status, result.technical_admission_status)
    elif kind == "dependency":
        actual = result.dependency_status
    elif kind == "ready":
        actual = (result.physical_asset_status, result.technical_admission_status)
    elif kind == "execution_guards":
        actual = (result.model_inference_executed, result.provider_invocation_executed)
    elif kind == "download_guards":
        actual = (result.automatic_model_download, result.automatic_package_download, result.automatic_dependency_install)
    elif kind == "network":
        actual = result.network_access
    elif kind == "human_selection":
        actual = result.human_contract_selection_required_normal_path
    else:
        actual = (result.technical_admission_status, result.commercial_license_status)
    return {
        "scenario_id": case["case_id"],
        "title": case["title"],
        "expectation_kind": kind,
        "expected": expected,
        "actual": actual,
        "passed": actual == expected,
        "readiness": to_dict(result),
    }
