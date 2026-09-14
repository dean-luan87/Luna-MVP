from __future__ import annotations

from typing import Any, Dict, List

from .yolo11n_external_provisioning_types_v1 import (
    YOLO11N_ASSET_ID,
    YOLO11N_EXPECTED_ASSET_PATH,
    resolve_yolo11n_external_provisioning_v1,
    to_dict,
)


def build_yolo11n_external_provisioning_cases_v1() -> List[Dict[str, Any]]:
    governed = "/workspace/Luna-Core/vision/detection/yolo/yolo11n.pt"
    verified = {
        "target_model_asset_id": YOLO11N_ASSET_ID,
        "target_governed_path": YOLO11N_EXPECTED_ASSET_PATH,
        "source_file_ref": governed,
        "provenance_ref": "provenance:controlled-local-asset",
        "file_exists": True,
        "is_regular_file": True,
        "file_size": 1000000,
        "observed_path": governed,
        "observed_filename": "yolo11n.pt",
        "observed_extension": "pt",
        "declared_checksum": "sha256:yolo11n-v1",
        "observed_checksum": "sha256:yolo11n-v1",
        "dependency_status": "PYTHON_DEPENDENCY_VERIFIED",
    }
    return [
        {"case_id": "Y11P-01", "title": "asset absent", "candidate": {"target_model_asset_id": YOLO11N_ASSET_ID}, "kind": "admission", "expected": "ADMISSION_BLOCKED_ASSET_MISSING"},
        {"case_id": "Y11P-02", "title": "external file reference accepted as provisioning candidate", "candidate": {"target_model_asset_id": YOLO11N_ASSET_ID, "source_file_ref": "/external/provisioned/yolo11n.pt", "provenance_ref": "provenance:external-file-ref"}, "kind": "provisioning", "expected": "PROVISIONING_READY_FOR_CONTROLLED_COPY"},
        {"case_id": "Y11P-03", "title": "governed path match", "candidate": {**verified, "checksum_status": "CHECKSUM_UNAVAILABLE", "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "kind": "physical", "expected": ("ASSET_PRESENT_UNVERIFIED", True)},
        {"case_id": "Y11P-04", "title": "path mismatch", "candidate": {**verified, "observed_path": "/external/provisioned/yolo11n.pt", "source_file_ref": "/external/provisioned/yolo11n.pt"}, "kind": "physical_status", "expected": "ASSET_PATH_MISMATCH"},
        {"case_id": "Y11P-05", "title": "checksum registration candidate", "candidate": {**verified, "declared_checksum": None, "observed_checksum": "sha256:first-local-fingerprint", "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "kind": "checksum_admission", "expected": ("CHECKSUM_REGISTRATION_CANDIDATE", "ADMISSION_BLOCKED_CHECKSUM")},
        {"case_id": "Y11P-06", "title": "checksum verified", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "kind": "checksum", "expected": "CHECKSUM_VERIFIED"},
        {"case_id": "Y11P-07", "title": "checksum mismatch blocks", "candidate": {**verified, "observed_checksum": "sha256:wrong"}, "kind": "checksum_admission", "expected": ("CHECKSUM_MISMATCH", "ADMISSION_BLOCKED_CHECKSUM")},
        {"case_id": "Y11P-08", "title": "provenance unresolved blocks", "candidate": {**verified, "provenance_ref": None, "target_model_asset_id": None}, "kind": "identity_admission", "expected": ("MODEL_ASSET_PROVENANCE_UNRESOLVED", "ADMISSION_BLOCKED_IDENTITY")},
        {"case_id": "Y11P-09", "title": "dependency unresolved blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_UNRESOLVED"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_UNRESOLVED", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11P-10", "title": "dependency missing blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_MISSING"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_MISSING", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11P-11", "title": "dependency incompatible blocks", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE"}, "kind": "dependency_admission", "expected": ("PYTHON_DEPENDENCY_VERSION_INCOMPATIBLE", "ADMISSION_BLOCKED_DEPENDENCY")},
        {"case_id": "Y11P-12", "title": "dependencies verified", "candidate": {**verified, "dependency_status": "PYTHON_DEPENDENCY_VERIFIED"}, "kind": "dependency", "expected": "PYTHON_DEPENDENCY_VERIFIED"},
        {"case_id": "Y11P-13", "title": "all prerequisites produce admission candidate", "candidate": verified, "kind": "ready", "expected": ("ASSET_PRESENT_VERIFIED_CANDIDATE", "ADMISSION_READY_CANDIDATE")},
        {"case_id": "Y11P-14", "title": "admission ready does not invoke model", "candidate": verified, "kind": "execution", "expected": (False, False)},
        {"case_id": "Y11P-15", "title": "no automatic install download or network", "candidate": verified, "kind": "negative_guards", "expected": (False, False, False)},
        {"case_id": "Y11P-16", "title": "commercial license remains separate", "candidate": verified, "kind": "license", "expected": ("ADMISSION_READY_CANDIDATE", "REQUIRES_LICENSE_REVIEW")},
    ]


def evaluate_yolo11n_external_provisioning_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    result = resolve_yolo11n_external_provisioning_v1(case.get("candidate"))
    kind = case["kind"]
    expected = case["expected"]
    if kind == "admission":
        actual: Any = result.technical_admission_status
    elif kind == "provisioning":
        actual = result.provisioning.provisioning_status
    elif kind == "physical":
        actual = (result.physical.physical_asset_status, result.physical.governed_path_match)
    elif kind == "physical_status":
        actual = result.physical.physical_asset_status
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
        actual = (result.physical.physical_asset_status, result.technical_admission_status)
    elif kind == "execution":
        actual = (result.model_inference_executed, result.provider_invocation_executed)
    elif kind == "negative_guards":
        actual = (result.network_access, result.automatic_model_download, result.automatic_dependency_install)
    else:
        actual = (result.technical_admission_status, result.commercial_license_status)
    return {
        "scenario_id": case["case_id"],
        "title": case["title"],
        "expectation_kind": kind,
        "expected": expected,
        "actual": actual,
        "passed": actual == expected,
        "admission": to_dict(result),
    }
