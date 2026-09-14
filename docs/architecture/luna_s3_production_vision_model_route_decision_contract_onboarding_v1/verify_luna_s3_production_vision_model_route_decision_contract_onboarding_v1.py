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
DOC_DIR = ROOT / "docs/architecture/luna_s3_production_vision_model_route_decision_contract_onboarding_v1"
CODE_DIR = ROOT / "capabilities/midplatform/model_manager/model_contract_repository/production_vision_route_onboarding"
EVAL_DIR = ROOT / "_eval_out/s3_production_vision_model_route_decision_v1"
DOC_FILES = {
    "production_vision_model_route_overview_v1.md",
    "production_vision_model_route_inventory_v1.json",
    "production_vision_route_decision_v1.json",
    "production_vision_contract_mapping_v1.json",
    "production_vision_model_matrix_v1.json",
    "production_vision_loader_mapping_v1.json",
    "production_vision_capability_evidence_mapping_v1.json",
    "production_vision_deployment_profiles_v1.json",
    "production_vision_benchmark_profile_v1.json",
    "production_vision_license_metadata_v1.json",
    "production_vision_automatic_resolution_v1.json",
    "production_vision_differential_validation_v1.json",
    "production_vision_negative_guards_v1.json",
    "production_vision_scenario_mapping_v1.json",
    "production_vision_change_manifest_v1.json",
    "phase_contract.json",
    "implementation_summary_v1.md",
    "verify_luna_s3_production_vision_model_route_decision_contract_onboarding_v1.py",
}
CODE_FILES = {
    "__init__.py",
    "production_vision_route_types_v1.py",
    "production_vision_route_fixture_v1.py",
    "run_production_vision_model_route_decision_v1.py",
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require({p.name for p in DOC_DIR.iterdir()} == DOC_FILES, "exact documentation file set mismatch", failures)
    require({p.name for p in CODE_DIR.iterdir() if p.is_file()} == CODE_FILES, "exact integration file set mismatch", failures)
    parsed = {}
    for path in DOC_DIR.glob("*.json"):
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid json:{path.name}:{type(exc).__name__}")
    for path in list(CODE_DIR.glob("*.py")) + [DOC_DIR / "verify_luna_s3_production_vision_model_route_decision_contract_onboarding_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            failures.append(f"ast parse failed:{path.name}")

    inventory = parsed.get("production_vision_model_route_inventory_v1.json", {})
    require(inventory.get("canonical_owner") == "Model Manager / Model Governance", "canonical owner mismatch", failures)
    require(inventory.get("parallel_semantic_owner_created") is False, "parallel semantic owner created", failures)
    routes = parsed.get("production_vision_route_decision_v1.json", {}).get("route_roles", {})
    require(routes.get("model-asset:yolov5n:weights-v1", {}).get("role") == "LEGACY_REFERENCE", "YOLOv5 role mismatch", failures)
    require(routes.get("model-asset:yolo11n:weights-v1", {}).get("role") == "STABILITY_COMPARATOR", "YOLO11 role mismatch", failures)
    require(routes.get("model-asset:yolo26n:weights-v1", {}).get("role") == "PRIMARY_CANDIDATE", "YOLO26 role mismatch", failures)
    require(parsed.get("production_vision_route_decision_v1.json", {}).get("best_fit") is False, "BEST_FIT was declared", failures)
    mapping = parsed.get("production_vision_contract_mapping_v1.json", {})
    require(len(mapping.get("model_asset_contracts", [])) == 3, "three model assets not mapped", failures)
    require(mapping.get("canonical_evidence_contract") == "evidence:visual-detection-candidate:v1", "canonical evidence mismatch", failures)
    loader = parsed.get("production_vision_loader_mapping_v1.json", {}).get("loaders", {})
    require(loader.get("loader:yolov5:torch-hub-local:v1", {}).get("network_allowed") is False, "YOLOv5 network policy mismatch", failures)
    require(loader.get("loader:ultralytics:yolo:v1", {}).get("network_allowed") is False, "Ultralytics network policy mismatch", failures)
    require(parsed.get("production_vision_capability_evidence_mapping_v1.json", {}).get("evidence_fields", {}).get("truth_declared") is False, "evidence truth boundary mismatch", failures)
    require(parsed.get("production_vision_automatic_resolution_v1.json", {}).get("human_contract_selection_required_normal_path") is False, "human contract selection required", failures)
    require(parsed.get("production_vision_automatic_resolution_v1.json", {}).get("missing_asset_admission") == "BLOCKED", "missing asset does not block", failures)
    guards = parsed.get("production_vision_negative_guards_v1.json", {})
    require(all(value is False for value in guards.values()), "negative guard violated", failures)
    require(parsed.get("production_vision_scenario_mapping_v1.json", {}).get("scenario_count") == 18, "scenario count mismatch", failures)
    for path in (EVAL_DIR / "s3_production_vision_model_route_result_v1.json", EVAL_DIR / "s3_production_vision_model_route_case_results_v1.json", EVAL_DIR / "s3_production_vision_model_route_trace_v1.json"):
        require(path.is_file(), f"runner artifact missing:{path.name}", failures)
    summary_path = EVAL_DIR / "s3_production_vision_model_route_result_v1.json"
    cases_path = EVAL_DIR / "s3_production_vision_model_route_case_results_v1.json"
    if summary_path.is_file() and cases_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        require(summary.get("scenario_count") == 18, "runner scenario count mismatch", failures)
        require(summary.get("all_cases_passed") is True, "controlled scenarios did not pass", failures)
        require(summary.get("model_inference_executed") is False, "model inference executed", failures)
        require(summary.get("network_access") is False, "network access occurred", failures)
        require(summary.get("automatic_model_download") is False, "model download occurred", failures)
        require(len(cases) == 18 and all(item.get("passed") is True for item in cases), "case checks did not pass", failures)
    result = {"passed_check_count": 0 if failures else 16, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures, "status": "PASS" if not failures else "BLOCKED"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
