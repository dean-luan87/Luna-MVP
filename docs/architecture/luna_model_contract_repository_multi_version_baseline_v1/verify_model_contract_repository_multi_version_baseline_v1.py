from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = find_repo_root(Path(__file__))
DOC_DIR = ROOT / "docs/architecture/luna_model_contract_repository_multi_version_baseline_v1"
CODE_DIR = ROOT / "capabilities/midplatform/model_manager/model_contract_repository"
EVAL_DIR = ROOT / "_eval_out/model_contract_repository_multi_version_baseline_v1"

DOC_FILES = {
    "model_contract_repository_architecture_overview_v1.md",
    "existing_asset_inventory_v1.json",
    "version_model_v1.json",
    "automatic_identity_resolution_v1.json",
    "loader_contract_baseline_v1.json",
    "provider_adapter_contract_baseline_v1.json",
    "capability_evidence_contract_baseline_v1.json",
    "compatibility_validation_v1.json",
    "current_yolov5n_resolution_v1.json",
    "lifecycle_change_control_v1.json",
    "future_recommendation_interface_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_model_contract_repository_multi_version_baseline_v1.py",
}
CODE_FILES = {
    "__init__.py",
    "model_contract_repository_types_v1.py",
    "model_contract_repository_registry_v1.py",
    "model_contract_repository_resolver_v1.py",
    "model_contract_repository_fixture_v1.py",
    "run_model_contract_repository_multi_version_baseline_v1.py",
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require({p.name for p in DOC_DIR.iterdir()} == DOC_FILES, "exact documentation file set mismatch", failures)
    actual_code_files = {p.name for p in CODE_DIR.iterdir() if p.is_file() and p.suffix == ".py"}
    require(actual_code_files == CODE_FILES, "exact implementation file set mismatch", failures)
    json_docs = [p for p in DOC_DIR.glob("*.json")]
    parsed = {}
    for path in json_docs:
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid json:{path.name}:{type(exc).__name__}")
    for path in list(CODE_DIR.glob("*.py")) + [DOC_DIR / "verify_model_contract_repository_multi_version_baseline_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            failures.append(f"ast parse failed:{path.name}")
    inventory = parsed.get("existing_asset_inventory_v1.json", {})
    require(inventory.get("canonical_owner") == "capabilities/midplatform/model_manager/", "canonical Model Manager owner missing", failures)
    require(inventory.get("parallel_owner_created") is False, "parallel semantic owner created", failures)
    version = parsed.get("version_model_v1.json", {})
    require(len(version.get("version_dimensions", [])) >= 5, "version dimensions incomplete", failures)
    identity = parsed.get("automatic_identity_resolution_v1.json", {})
    require(identity.get("extension_only_is_sufficient") is False, "extension-only loader selection allowed", failures)
    require(identity.get("human_contract_selection_required_normal_path") is False, "human selection required", failures)
    loader = parsed.get("loader_contract_baseline_v1.json", {})
    require(loader.get("yolov5_loader_kind") == "torch_hub_yolov5_custom_local_weights", "YOLOv5 loader kind mismatch", failures)
    require(loader.get("yolov5_local_source_package_ref") is None, "missing source package was fabricated", failures)
    current = parsed.get("current_yolov5n_resolution_v1.json", {})
    require(current.get("identity") == "RESOLVED_UNIQUE", "current YOLOv5 identity not unique", failures)
    require(current.get("model_contract_resolution") == "MODEL_CONTRACT_RESOLVED", "model contract resolution missing", failures)
    require(current.get("loader_contract_resolution") == "LOADER_CONTRACT_RESOLVED", "loader contract resolution missing", failures)
    require(current.get("loader_contract") == "loader:yolov5:torch-hub-local:v1", "current YOLOv5 loader not resolved", failures)
    require(current.get("final_admission") == "BLOCKED", "current YOLOv5 blocker not preserved", failures)
    require("LOCAL_SOURCE_PACKAGE_REQUIRED" in current.get("blocking_reasons", []), "current YOLOv5 missing-source blocker absent", failures)
    guards = parsed.get("negative_guards_v1.json", {})
    require(all(value is False for value in guards.values()), "negative guard is not false", failures)
    phase = parsed.get("phase_contract.json", {})
    require(phase.get("inference_execution") is False and phase.get("network_access") is False, "execution boundary violated", failures)
    require(parsed.get("scenario_mapping_v1.json", {}).get("scenario_count") == 24, "scenario count mismatch", failures)
    summary_path = EVAL_DIR / "model_contract_repository_result_v1.json"
    cases_path = EVAL_DIR / "model_contract_repository_case_results_v1.json"
    trace_path = EVAL_DIR / "model_contract_repository_trace_v1.json"
    require(summary_path.is_file() and cases_path.is_file() and trace_path.is_file(), "runner artifacts missing", failures)
    if summary_path.is_file() and cases_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        require(summary.get("scenario_count") == 24, "runner scenario count mismatch", failures)
        require(summary.get("all_cases_passed") is True, "controlled scenarios did not all pass", failures)
        require(summary.get("model_inference_executed") is False, "model inference executed", failures)
        require(summary.get("network_access") is False, "network access occurred", failures)
        require(len(cases) == 24 and all(item.get("passed") is True for item in cases), "case checks did not all pass", failures)
    result = {"passed_check_count": 0 if failures else 16, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures, "status": "PASS" if not failures else "BLOCKED"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
