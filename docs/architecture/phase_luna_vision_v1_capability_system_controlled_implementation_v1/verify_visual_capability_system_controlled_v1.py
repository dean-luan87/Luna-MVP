"""Deterministic verifier for the controlled V1 Visual Capability System."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

VERIFIER_PATH = Path(__file__).resolve()
PHASE_DIR = VERIFIER_PATH.parent


def _repo_root() -> Path:
    for candidate in VERIFIER_PATH.parents:
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir():
            return candidate
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
CODE_DIR = REPO_ROOT / "capabilities/vision/registry/visual_capability_system_controlled"
CODE_FILES = {"__init__.py", "visual_capability_system_types_v1.py", "visual_capability_system_governance_v1.py", "visual_capability_system_fixture_v1.py", "run_visual_capability_system_controlled_v1.py"}
DOC_FILES = {"overview.md", "inventory_reuse.md", "safety_capability_domain.md", "warehouse_contract.md", "lifecycle_contract.md", "registration_contract.md", "safety_registration_policy.md", "dual_channel_contract.md", "routing_contract.md", "user_control_degradation_boundary.md", "snsp_srsk_boundary.md", "owner_mutation_matrix.md", "negative_guards_v1.json", "scenario_mapping_v1.json", "contract_shape_reconciliation_v1.json", "change_manifest.md", "phase_contract.json", "implementation_summary.md", "verify_visual_capability_system_controlled_v1.py"}
FORBIDDEN_SOURCE_TOKENS = ("ultralytics", "torch", "cv2", "subprocess", "requests", "socket")


def _check(checks: list[dict], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def run_verification() -> dict:
    checks: list[dict] = []
    actual_code = {path.name for path in CODE_DIR.iterdir() if path.is_file()} if CODE_DIR.is_dir() else set()
    actual_docs = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    _check(checks, "VCSV-01_code_file_set", actual_code == CODE_FILES, "Controlled code set is exact and generated directories are ignored.")
    _check(checks, "VCSV-02_document_file_set", actual_docs == DOC_FILES, "Controlled documentation set is exact and generated directories are ignored.")
    parsed = True
    for name in ("negative_guards_v1.json", "scenario_mapping_v1.json", "contract_shape_reconciliation_v1.json", "phase_contract.json"):
        try:
            json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            parsed = False
    _check(checks, "VCSV-03_json_assets", parsed, "Structured governance assets parse.")
    ast_ok = True
    source_text = ""
    for path in [CODE_DIR / name for name in CODE_FILES if name.endswith(".py")]:
        try:
            text = path.read_text(encoding="utf-8")
            source_text += text
            ast.parse(text, filename=str(path))
        except (OSError, SyntaxError):
            ast_ok = False
    _check(checks, "VCSV-04_ast_assets", ast_ok, "Controlled code assets are statically parseable.")
    _check(checks, "VCSV-05_no_runtime_imports", not any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS), "No model/provider/runtime/network imports are present.")
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from capabilities.vision.registry.visual_capability_system_controlled.visual_capability_system_fixture_v1 import build_runner_result
        result = build_runner_result()
    except Exception as exc:  # deterministic verifier reports import/fixture failure
        result = {"scenario_count": 0, "all_cases_passed": False, "failed_case_ids": [f"verifier:{type(exc).__name__}"]}
    mapping = json.loads((PHASE_DIR / "scenario_mapping_v1.json").read_text(encoding="utf-8"))
    reconciliation = json.loads((PHASE_DIR / "contract_shape_reconciliation_v1.json").read_text(encoding="utf-8"))
    _check(checks, "VCSV-06_scenario_count", result.get("scenario_count") == 24 and mapping.get("scenario_count") == 24, "The controlled suite declares 24 scenarios.")
    _check(checks, "VCSV-06b_reconciliation_matrix", len(reconciliation.get("scenarios", [])) == 24 and all(item.get("field_exists") is True and item.get("shape_correct") is True and item.get("semantic_layer_correct") is True for item in reconciliation.get("scenarios", [])), "All VCS scenarios have an explicit reconciled contract-shape record.")
    _check(checks, "VCSV-07_scenario_pass", result.get("all_cases_passed") is True and result.get("failed_case_ids") == [], "Synthetic candidate scenarios pass when user executes the Runner.")
    _check(checks, "VCSV-08_owner_boundary", result.get("owner") == "Capability Registry; Model Manager admission retained", "Capability Registry owns capability metadata and Model Manager remains admission owner.")
    _check(checks, "VCSV-09_negative_guards", all(result.get(name) is False for name in ("provider_invocation", "model_inference", "camera_activation", "automatic_download", "automatic_install", "learning_execution", "field_mutation", "current_world_mutation", "intent_mutation", "decision_mutation", "task_mutation", "provider_to_brain_shortcut")), "Execution and mutation guards remain false.")
    _check(checks, "VCSV-10_candidate_gateway", result.get("candidate_only") is True, "All outputs remain candidate-only and Gateway-bound.")
    _check(checks, "VCSV-11_safety_protection", result.get("user_uninstalls_mandatory_safety") is False and result.get("user_bypasses_safety_baseline") is False and result.get("unapproved_safety_provider_activation") is False, "Mandatory Safety controls remain protected.")
    _check(checks, "VCSV-12_snsps_srsk_boundary", result.get("vision_owns_semantic_sufficiency") is False and result.get("snsp_effective_rule_authority") is False and result.get("srsk_truth_authority") is False, "SNSP and SRSK remain reference-only boundaries.")
    passed = sum(1 for item in checks if item["passed"])
    return {"phase": "Phase-Luna-Vision-V1-Capability-System-Controlled-Implementation-v1-001", "checks": checks, "passed_check_count": passed, "failed_check_count": len(checks) - passed, "blocker_count": sum(1 for item in checks if not item["passed"]), "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION"}


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
