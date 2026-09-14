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

from capabilities.midplatform.model_manager.model_contract_repository.local_source_package_integration.local_source_package_fixture_v1 import (  # noqa: E402
    build_source_package_cases_v1,
    evaluate_source_package_case_v1,
)

OUT = ROOT / "_eval_out/s3_yolov5_local_source_package_compatibility_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    cases = [evaluate_source_package_case_v1(case) for case in build_source_package_cases_v1()]
    results = [{key: jsonable(value) for key, value in case.items()} for case in cases]
    failed = [case["scenario_id"] for case in results if not case["passed"]]
    summary = {
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_download": False,
        "human_contract_selection_required_normal_path": False,
        "current_yolov5n": {
            "model_contract_resolution": "MODEL_CONTRACT_RESOLVED",
            "loader_contract_resolution": "LOADER_CONTRACT_RESOLVED",
            "local_source_package_resolution": "LOCAL_SOURCE_PACKAGE_NOT_FOUND",
            "dependency_status": "NOT_SATISFIED",
            "admission": "BLOCKED",
        },
    }
    trace = {
        "reverse_trace": ["provider_invocation_candidate", "admission", "compatibility", "local_source_package_contract", "loader_contract", "model_asset", "original_manifest"],
        "provenance_grants_authority": False,
        "source_package_grants_execution_authority": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s3_yolov5_local_source_package_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolov5_local_source_package_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "s3_yolov5_local_source_package_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
