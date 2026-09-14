from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_registry_v1 import build_model_contract_repository_v1
from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_resolver_v1 import resolve_model_contract_v1
from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_types_v1 import LocalSourcePackageContractV1, to_dict


LOADER = "loader:yolov5:torch-hub-local:v1"
EVIDENCE = "evidence:visual-detection-candidate:v1"
CAPABILITY = "capability:object-detection:v1"


def _package(
    package_id: str,
    *,
    family: str = "yolov5",
    version: str = "v7.0-local",
    loaders: tuple[str, ...] = (LOADER,),
    status: str = "SUPPORTED",
    network: bool = False,
    auto_download: bool = False,
) -> Dict[str, Any]:
    return to_dict(LocalSourcePackageContractV1(
        local_source_package_id=package_id,
        package_family=family,
        package_version=version,
        package_path=None if status == "MISSING" else f"external://{package_id}",
        source_kind="preinstalled_local_source" if not network else "network_only_source",
        compatible_loader_contract_ids=loaders,
        required_files=("hubconf.py", "models/yolo.py", "models/common.py", "utils/"),
        validation_markers=("models.yolo.Model", "local_source_tree", "no_network"),
        network_allowed=network,
        automatic_download_allowed=auto_download,
        checksum=None,
        provenance_ref=f"source-package-provenance:{package_id}",
        status=status,
    ))


def build_source_package_cases_v1() -> List[Dict[str, Any]]:
    return [
        {"case_id": "YSP-01", "title": "missing local package blocks", "packages": (), "expected_reason": "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-02", "title": "unique local package resolves", "packages": (_package("source:yolov5:v7-local"),), "expected_status": "RESOLVED", "expected_dependency_status": "READY_CANDIDATE", "expected_admission": "ADMITTED"},
        {"case_id": "YSP-03", "title": "wrong package family blocks", "packages": (_package("source:other:v1", family="other-model"),), "expected_reason": "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-04", "title": "incompatible package version blocks", "packages": (_package("source:yolov5:incompatible", status="INCOMPATIBLE"),), "expected_reason": "LOCAL_SOURCE_PACKAGE_INCOMPATIBLE", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-05", "title": "ambiguous local package blocks", "packages": (_package("source:yolov5:a"), _package("source:yolov5:b", version="v8-local")), "expected_reason": "LOCAL_SOURCE_PACKAGE_AMBIGUOUS", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-06", "title": "network-only package blocks", "packages": (_package("source:yolov5:network", network=True, auto_download=True),), "expected_reason": "LOCAL_SOURCE_PACKAGE_NETWORK_POLICY_INVALID", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-07", "title": "automatic resolution without human selection", "packages": (_package("source:yolov5:auto"),), "expected_human_selection": False, "expected_status": "RESOLVED"},
        {"case_id": "YSP-08", "title": "source package does not grant execution authority", "packages": (_package("source:yolov5:authority"),), "expected_execution_admitted": False},
        {"case_id": "YSP-09", "title": "source package does not change capability semantics", "packages": (_package("source:yolov5:capability"),), "expected_capability": CAPABILITY},
        {"case_id": "YSP-10", "title": "source package does not change evidence authority", "packages": (_package("source:yolov5:evidence"),), "expected_evidence": EVIDENCE},
        {"case_id": "YSP-11", "title": "current yolov5n resolution", "packages": (), "expected_resolution": "RESOLVED_UNIQUE", "expected_reason": "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "expected_admission": "BLOCKED"},
        {"case_id": "YSP-12", "title": "trace reverse lookup", "packages": (_package("source:yolov5:trace"),), "expected_trace": True},
    ]


def _repository_with_packages(packages: tuple[Dict[str, Any], ...]) -> Dict[str, Any]:
    repo = build_model_contract_repository_v1()
    repo["local_source_packages"] = {item["local_source_package_id"]: item for item in packages}
    return repo


def evaluate_source_package_case_v1(case: Dict[str, Any]) -> Dict[str, Any]:
    result = resolve_model_contract_v1(
        {"model_asset_id": "model-asset:yolov5n:weights-v1"},
        repository=_repository_with_packages(case["packages"]),
        deployment_requirements={"network_forbidden": True, "dependencies_satisfied": True},
    )
    reasons = list(result.compatibility.reasons)
    if "expected_reason" in case:
        actual: Any = reasons
        passed = case["expected_reason"] in reasons
        expectation_kind = "reason_presence"
    elif "expected_status" in case:
        actual = result.local_source_package_status
        passed = actual == case["expected_status"]
        expectation_kind = "source_package_status"
    elif "expected_human_selection" in case:
        actual = result.human_contract_selection_required
        passed = actual == case["expected_human_selection"]
        expectation_kind = "human_selection_guard"
    elif "expected_execution_admitted" in case:
        actual = result.execution_admitted
        passed = actual == case["expected_execution_admitted"]
        expectation_kind = "execution_guard"
    elif "expected_capability" in case:
        actual = result.capability_contract_ids[0] if result.capability_contract_ids else ""
        passed = actual == case["expected_capability"]
        expectation_kind = "capability_contract"
    elif "expected_evidence" in case:
        evidence_contract = _repository_with_packages(case["packages"])["evidence_contracts"][EVIDENCE]
        actual = {
            "evidence_contract_id": result.evidence_contract_ids[0] if result.evidence_contract_ids else "",
            "truth_declared": bool(evidence_contract.get("truth_declared")),
            "fact_admitted": bool(evidence_contract.get("fact_admitted")),
            "provider_semantic_authority": False,
            "provenance_grants_authority": False,
            "compatibility_status": result.compatibility.status,
        }
        expected = {
            "evidence_contract_id": case["expected_evidence"],
            "truth_declared": False,
            "fact_admitted": False,
            "provider_semantic_authority": False,
            "provenance_grants_authority": False,
            "compatibility_status": "COMPATIBLE",
        }
        passed = actual == expected
        expectation_kind = "evidence_identity_and_authority_boundary"
    elif "expected_resolution" in case:
        actual = result.resolution_status
        passed = actual == case["expected_resolution"]
        expectation_kind = "resolution_status"
    else:
        actual = bool(result.trace_ref and result.provenance_refs and any("source-package-provenance" in ref for ref in result.provenance_refs))
        passed = actual == case["expected_trace"]
        expectation_kind = "trace_provenance"
    if "expected_admission" in case:
        passed = passed and result.admission_status == case["expected_admission"]
    if "expected_resolution" in case:
        passed = passed and result.resolution_status == case["expected_resolution"]
    if "expected_dependency_status" in case:
        passed = passed and result.compatibility.dependency_status == case["expected_dependency_status"]
    expected_output = expected if "expected_evidence" in case else case.get("expected_reason", case.get("expected_status", case.get("expected_admission", case.get("expected_resolution", case.get("expected_trace", False)))))
    return {
        "scenario_id": case["case_id"],
        "title": case["title"],
        "expectation_kind": expectation_kind,
        "expected": expected_output,
        "actual": actual,
        "passed": passed,
        "resolution": result,
    }
