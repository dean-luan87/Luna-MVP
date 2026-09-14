from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = find_repo_root(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_readiness.yolo11n_readiness_fixture_v1 import (  # noqa: E402
    build_yolo11n_readiness_cases_v1,
    evaluate_yolo11n_readiness_case_v1,
)


OUT = ROOT / "_eval_out/s3_yolo11n_local_asset_dependency_readiness_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    cases = [evaluate_yolo11n_readiness_case_v1(case) for case in build_yolo11n_readiness_cases_v1()]
    results = [jsonable(item) for item in cases]
    failed = [item["scenario_id"] for item in results if not item["passed"]]
    current = results[0].get("readiness", {}) if results else {}
    summary = {
        "owner": "Model Manager / Model Governance",
        "target_model": "YOLO11n",
        "target_asset_id": current.get("target_asset_id"),
        "expected_asset_path": current.get("expected_asset_path"),
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "physical_asset_status": current.get("physical_asset_status"),
        "checksum_status": current.get("checksum_status"),
        "identity_status": current.get("model_identity_status"),
        "contract_statuses": {
            "model": current.get("model_contract_status"),
            "loader": current.get("loader_contract_status"),
            "provider_adapter": current.get("provider_adapter_status"),
            "capability": current.get("capability_contract_status"),
            "evidence": current.get("evidence_contract_status"),
        },
        "dependency_status": current.get("dependency_status"),
        "technical_admission_status": current.get("technical_admission_status"),
        "commercial_license_status": current.get("commercial_license_status"),
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "automatic_dependency_install": False,
        "human_contract_selection_required_normal_path": False,
        "provider_semantic_authority": False,
        "truth_declared": False,
        "fact_admitted": False,
    }
    trace = {
        "reverse_trace": [
            "technical_admission",
            "dependency_readiness",
            "evidence_contract",
            "capability_contract",
            "provider_adapter_contract",
            "loader_contract",
            "model_asset_contract",
            "physical_asset_or_expected_manifest",
        ],
        "provenance_grants_authority": False,
        "target_model": "YOLO11n",
        "current_case_trace": current.get("trace_ref"),
        "execution_started": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s3_yolo11n_local_asset_dependency_readiness_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolo11n_local_asset_dependency_readiness_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolo11n_local_asset_dependency_readiness_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
