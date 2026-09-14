from __future__ import annotations

import ast
import json
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = find_repo_root(Path(__file__))
DOC_DIR = ROOT / "docs/architecture/phase_luna_a_route_s3_yolov5_local_source_package_compatibility_v1_001"
CODE_DIR = ROOT / "capabilities/midplatform/model_manager/model_contract_repository/local_source_package_integration"
EVAL_DIR = ROOT / "_eval_out/s3_yolov5_local_source_package_compatibility_v1"
DOC_FILES = {
    "s3_yolov5_local_source_package_compatibility_overview_v1.md",
    "existing_source_inventory_v1.json",
    "local_source_package_contract_v1.json",
    "automatic_source_package_resolution_v1.json",
    "current_yolov5n_case_v1.json",
    "dependency_layer_separation_v1.json",
    "trace_provenance_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_s3_yolov5_local_source_package_compatibility_v1.py",
}
CODE_FILES = {"__init__.py", "local_source_package_fixture_v1.py", "run_local_source_package_compatibility_v1.py"}


def require(value: bool, message: str, failures: list[str]) -> None:
    if not value:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require({p.name for p in DOC_DIR.iterdir()} == DOC_FILES, "exact documentation file set mismatch", failures)
    require({p.name for p in CODE_DIR.iterdir() if p.is_file() and p.suffix == ".py"} == CODE_FILES, "exact integration file set mismatch", failures)
    parsed = {}
    for path in DOC_DIR.glob("*.json"):
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            failures.append(f"invalid json:{path.name}")
    for path in list(CODE_DIR.glob("*.py")) + [DOC_DIR / "verify_s3_yolov5_local_source_package_compatibility_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            failures.append(f"ast parse failed:{path.name}")
    inventory = parsed.get("existing_source_inventory_v1.json", {})
    require(inventory.get("complete_local_yolov5_source_package_exists") is False, "source inventory incorrectly claims package exists", failures)
    contract = parsed.get("local_source_package_contract_v1.json", {})
    require("models.yolo.Model" in contract.get("yolov5_required_markers", []), "YOLOv5 source marker missing", failures)
    current = parsed.get("current_yolov5n_case_v1.json", {})
    require(current.get("model_contract_resolution") == "MODEL_CONTRACT_RESOLVED", "model contract not resolved", failures)
    require(current.get("loader_contract_resolution") == "LOADER_CONTRACT_RESOLVED", "loader contract not resolved", failures)
    require(current.get("local_source_package_resolution") == "LOCAL_SOURCE_PACKAGE_NOT_FOUND", "missing package result incorrect", failures)
    require(current.get("admission") == "BLOCKED", "missing package did not block", failures)
    guards = parsed.get("negative_guards_v1.json", {})
    require(all(value is False for value in guards.values()), "negative guard violated", failures)
    require(parsed.get("scenario_mapping_v1.json", {}).get("scenario_count") == 12, "scenario count mismatch", failures)
    for name in ("s3_yolov5_local_source_package_result_v1.json", "s3_yolov5_local_source_package_case_results_v1.json", "s3_yolov5_local_source_package_trace_v1.json"):
        require((EVAL_DIR / name).is_file(), f"runner artifact missing:{name}", failures)
    summary_path = EVAL_DIR / "s3_yolov5_local_source_package_result_v1.json"
    cases_path = EVAL_DIR / "s3_yolov5_local_source_package_case_results_v1.json"
    if summary_path.is_file() and cases_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        require(summary.get("scenario_count") == 12, "runner scenario count mismatch", failures)
        require(summary.get("all_cases_passed") is True, "controlled cases did not pass", failures)
        require(summary.get("model_inference_executed") is False, "inference executed", failures)
        require(summary.get("network_access") is False, "network access occurred", failures)
        require(summary.get("automatic_download") is False, "automatic download occurred", failures)
        require(len(cases) == 12 and all(item.get("passed") is True for item in cases), "case checks did not pass", failures)
    result = {"passed_check_count": 0 if failures else 14, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures, "status": "PASS" if not failures else "BLOCKED"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
