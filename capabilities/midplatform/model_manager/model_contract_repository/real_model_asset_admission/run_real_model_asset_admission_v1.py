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

from capabilities.midplatform.model_manager.model_contract_repository.real_model_asset_admission.real_model_asset_admission_fixture_v1 import (  # noqa: E402
    build_real_model_asset_admission_cases_v1,
    evaluate_real_model_asset_admission_case_v1,
)


OUT = ROOT / "_eval_out/s3_modern_yolo_real_model_asset_admission_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    cases = [evaluate_real_model_asset_admission_case_v1(case) for case in build_real_model_asset_admission_cases_v1()]
    results = [{key: jsonable(value) for key, value in case.items()} for case in cases]
    failed = [item["scenario_id"] for item in results if not item["passed"]]
    current = results[0]["admission"] if results else {}
    summary = {
        "owner": "Model Manager / Model Governance",
        "target_model": "YOLO11n",
        "target_route_role": "STABILITY_COMPARATOR",
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "physical_asset_status": current.get("physical_asset_status"),
        "model_identity_status": current.get("model_identity_status"),
        "model_contract_status": current.get("model_contract_status"),
        "loader_contract_status": current.get("loader_contract_status"),
        "provider_adapter_status": current.get("provider_adapter_status"),
        "capability_contract_status": current.get("capability_contract_status"),
        "evidence_contract_status": current.get("evidence_contract_status"),
        "dependency_status": current.get("dependency_status"),
        "admission_status": current.get("admission_status"),
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "human_contract_selection_required_normal_path": False,
        "provider_semantic_authority": False,
        "truth_declared": False,
        "fact_admitted": False,
    }
    trace = {
        "reverse_trace": ["admission_decision", "dependency_readiness", "evidence_contract", "capability_contract", "provider_adapter_contract", "loader_contract", "model_asset_contract", "physical_asset_or_manifest"],
        "provenance_grants_authority": False,
        "target_model": "YOLO11n",
        "current_case_trace": current.get("trace_ref"),
        "execution_started": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s3_modern_yolo_real_model_asset_admission_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_modern_yolo_real_model_asset_admission_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_modern_yolo_real_model_asset_admission_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
