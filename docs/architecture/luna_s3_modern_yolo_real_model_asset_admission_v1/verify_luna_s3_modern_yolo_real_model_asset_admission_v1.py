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
DOC_DIR = ROOT / "docs/architecture/luna_s3_modern_yolo_real_model_asset_admission_v1"
CODE_DIR = ROOT / "capabilities/midplatform/model_manager/model_contract_repository/real_model_asset_admission"
EVAL_DIR = ROOT / "_eval_out/s3_modern_yolo_real_model_asset_admission_v1"
DOC_FILES = {
    "modern_yolo_real_model_asset_admission_overview_v1.md",
    "asset_inventory_v1.json",
    "physical_asset_identity_model_v1.json",
    "automatic_model_identification_v1.json",
    "contract_binding_v1.json",
    "dependency_readiness_v1.json",
    "admission_policy_v1.json",
    "current_yolo11n_case_v1.json",
    "yolo26_reuse_boundary_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_luna_s3_modern_yolo_real_model_asset_admission_v1.py",
}
CODE_FILES = {
    "__init__.py",
    "real_model_asset_admission_types_v1.py",
    "real_model_asset_admission_fixture_v1.py",
    "run_real_model_asset_admission_v1.py",
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    doc_entries = {p.name for p in DOC_DIR.iterdir() if p.is_file() and p.suffix in {".json", ".md", ".py"}}
    code_entries = {p.name for p in CODE_DIR.iterdir() if p.is_file() and p.suffix == ".py"}
    require(doc_entries == DOC_FILES, "exact documentation file set mismatch", failures)
    require(code_entries == CODE_FILES, "exact implementation file set mismatch", failures)
    parsed = {}
    for path in DOC_DIR.glob("*.json"):
        try:
            parsed[path.name] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid json:{path.name}:{type(exc).__name__}")
    for path in list(CODE_DIR.glob("*.py")) + [DOC_DIR / "verify_luna_s3_modern_yolo_real_model_asset_admission_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            failures.append(f"ast parse failed:{path.name}")

    inventory = parsed.get("asset_inventory_v1.json", {})
    require(inventory.get("canonical_owner") == "Model Manager / Model Governance", "canonical owner mismatch", failures)
    require(inventory.get("physical_asset_inventory", {}).get("real_file_present") is False, "YOLO11 asset presence overstated", failures)
    current = parsed.get("current_yolo11n_case_v1.json", {})
    require(current.get("physical_asset_status") == "ASSET_NOT_PRESENT", "current physical status mismatch", failures)
    require(current.get("model_identity_status") == "MODEL_ASSET_IDENTIFIED_UNIQUE", "current identity status mismatch", failures)
    require(current.get("admission_status") == "ADMISSION_BLOCKED_ASSET_MISSING", "current admission is not fail-closed", failures)
    binding = parsed.get("contract_binding_v1.json", {})
    require(binding.get("loader_contract") == "loader:ultralytics:yolo:v1", "YOLO11 loader binding mismatch", failures)
    require(binding.get("evidence_contract") == "evidence:visual-detection-candidate:v1", "evidence binding mismatch", failures)
    require(binding.get("truth_declared") is False and binding.get("fact_admitted") is False, "evidence authority boundary mismatch", failures)
    identification = parsed.get("automatic_model_identification_v1.json", {})
    require(identification.get("filename_is_authority") is None or identification.get("filename_is_authority") is False, "filename identity authority enabled", failures)
    require(identification.get("loader_selected_from_extension") is False, "extension loader selection enabled", failures)
    phase = parsed.get("phase_contract.json", {})
    for key in ("model_inference_executed", "provider_invocation_executed", "network_access", "automatic_model_download", "automatic_package_download", "best_fit_declared", "production_approved"):
        require(phase.get(key) is False, f"phase guard violated:{key}", failures)
    guards = parsed.get("negative_guards_v1.json", {})
    require(all(value is False for value in guards.values()), "negative guard violated", failures)
    require(parsed.get("scenario_mapping_v1.json", {}).get("scenario_count") == 16, "scenario count mismatch", failures)
    for path in (EVAL_DIR / "s3_modern_yolo_real_model_asset_admission_result_v1.json", EVAL_DIR / "s3_modern_yolo_real_model_asset_admission_case_results_v1.json", EVAL_DIR / "s3_modern_yolo_real_model_asset_admission_trace_v1.json"):
        require(path.is_file(), f"runner artifact missing:{path.name}", failures)
    summary_path = EVAL_DIR / "s3_modern_yolo_real_model_asset_admission_result_v1.json"
    cases_path = EVAL_DIR / "s3_modern_yolo_real_model_asset_admission_case_results_v1.json"
    if summary_path.is_file() and cases_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        require(summary.get("target_model") == "YOLO11n", "target model mismatch", failures)
        require(summary.get("scenario_count") == 16, "runner scenario count mismatch", failures)
        require(summary.get("all_cases_passed") is True, "controlled cases did not pass", failures)
        for key in ("model_inference_executed", "provider_invocation_executed", "network_access", "automatic_model_download", "automatic_package_download", "human_contract_selection_required_normal_path", "provider_semantic_authority", "truth_declared", "fact_admitted"):
            require(summary.get(key) is False, f"runner guard violated:{key}", failures)
        require(len(cases) == 16 and all(item.get("passed") is True for item in cases), "case checks did not pass", failures)
    result = {"passed_check_count": 0 if failures else 16, "failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures, "status": "PASS" if not failures else "BLOCKED"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
