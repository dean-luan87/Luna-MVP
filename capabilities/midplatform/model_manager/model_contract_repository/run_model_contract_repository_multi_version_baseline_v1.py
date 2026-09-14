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

from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_fixture_v1 import (  # noqa: E402
    build_model_contract_repository_cases_v1,
    evaluate_model_contract_case_v1,
)

OUT = ROOT / "_eval_out/model_contract_repository_multi_version_baseline_v1"


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def main() -> int:
    cases = [evaluate_model_contract_case_v1(case) for case in build_model_contract_repository_cases_v1()]
    results = [{key: jsonable(value) for key, value in item.items()} for item in cases]
    failed = [item["scenario_id"] for item in results if not item["passed"]]
    summary = {
        "owner": "Model Manager / Model Governance",
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "model_inference_executed": False,
        "provider_invocation_executed": False,
        "network_access": False,
        "automatic_download": False,
        "human_contract_selection_required_normal_path": False,
        "current_yolov5n_admission": "BLOCKED",
    }
    trace = {
        "reverse_trace": ["provider_invocation_candidate", "admission_decision", "compatibility_result", "resolved_contract_set", "model_asset_identity", "manifest_or_asset"],
        "provenance_grants_authority": False,
        "current_yolov5n": {"resolution": "RESOLVED_UNIQUE", "model_contract_resolution": "MODEL_CONTRACT_RESOLVED", "loader_contract_resolution": "LOADER_CONTRACT_RESOLVED", "loader": "loader:yolov5:torch-hub-local:v1", "local_source_package_resolution": "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "compatibility": ["LOCAL_SOURCE_PACKAGE_REQUIRED", "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "DEPENDENCY_NOT_SATISFIED"], "admission": "BLOCKED"},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "model_contract_repository_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "model_contract_repository_case_results_v1.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "model_contract_repository_trace_v1.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
