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

from capabilities.midplatform.model_manager.model_contract_repository.production_vision_route_onboarding.production_vision_route_fixture_v1 import (  # noqa: E402
    build_production_vision_route_cases_v1,
    evaluate_production_vision_route_case_v1,
)


OUT = ROOT / "_eval_out/s3_production_vision_model_route_decision_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    cases = [evaluate_production_vision_route_case_v1(case) for case in build_production_vision_route_cases_v1()]
    results = [{key: jsonable(value) for key, value in case.items()} for case in cases]
    failed = [case["scenario_id"] for case in results if not case["passed"]]
    summary = {
        "owner": "Model Manager / Model Governance",
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "route_status": "CONTRACT_ONBOARDED_NOT_RUNTIME_ADMITTED",
        "real_components": [],
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_model_download": False,
        "automatic_package_download": False,
        "latest_model_auto_upgrade": False,
        "best_fit_declared_without_benchmark": False,
        "production_approved_without_real_validation": False,
        "model_change_mutates_cognition": False,
        "provider_semantic_authority": False,
        "current_roles": {"yolov5n": "LEGACY_REFERENCE", "yolo11n": "STABILITY_COMPARATOR", "yolo26n": "PRIMARY_CANDIDATE"},
        "current_assets": {"yolov5n": "AVAILABLE_REFERENCE", "yolo11n": "ASSET_NOT_PRESENT", "yolo26n": "ASSET_NOT_PRESENT"},
    }
    trace = {
        "reverse_trace": ["provider_invocation_candidate", "admission", "deployment_compatibility", "evidence_contract", "capability_contract", "provider_adapter_contract", "loader_contract", "model_asset_identity", "original_manifest_or_asset"],
        "provenance_grants_authority": False,
        "route_decisions": [item["resolution"] for item in results],
        "future_reference_asset": "/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/phone_local_001_clear_path.mp4",
        "future_reference_executed": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s3_production_vision_model_route_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_production_vision_model_route_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_production_vision_model_route_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
