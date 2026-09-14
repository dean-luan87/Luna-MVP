from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT / "capabilities/midplatform/model_manager/model_contract_repository/yolo11n_external_provisioning"
OUT_ROOT = ROOT / "_eval_out/s3_yolo11n_external_asset_provisioning_and_admission_verification_v1"

EXPECTED_DOCS = {
    "overview_v1.md",
    "inventory_v1.json",
    "external_provisioning_record_v1.json",
    "physical_verification_v1.json",
    "checksum_fingerprint_v1.json",
    "dependency_probe_contract_v1.json",
    "admission_policy_v1.json",
    "license_boundary_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "phase_contract.json",
    "implementation_summary_v1.md",
    "verify_luna_s3_yolo11n_external_asset_provisioning_and_admission_verification_v1.py",
}
EXPECTED_CODE = {
    "__init__.py",
    "yolo11n_external_provisioning_types_v1.py",
    "yolo11n_external_provisioning_fixture_v1.py",
    "probe_yolo11n_python_dependencies_v1.py",
    "run_yolo11n_external_asset_provisioning_and_admission_verification_v1.py",
}


def regular_files(path: Path, suffixes: set[str]) -> set[str]:
    return {item.name for item in path.iterdir() if item.is_file() and item.suffix in suffixes}


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    require(regular_files(DOC_ROOT, {".json", ".md", ".py"}) == EXPECTED_DOCS, "exact documentation file set mismatch", failures)
    require(regular_files(CODE_ROOT, {".py"}) == EXPECTED_CODE, "exact implementation file set mismatch", failures)
    for path in sorted(DOC_ROOT.iterdir()):
        if path.is_file() and path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                failures.append(f"invalid JSON: {path.name}: {exc}")
        if path.is_file() and path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                failures.append(f"invalid verifier AST: {path.name}: {exc}")
    for path in sorted(CODE_ROOT.iterdir()):
        if path.is_file() and path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                failures.append(f"invalid implementation AST: {path.name}: {exc}")
    inventory = json.loads((DOC_ROOT / "inventory_v1.json").read_text(encoding="utf-8"))
    policy = json.loads((DOC_ROOT / "admission_policy_v1.json").read_text(encoding="utf-8"))
    guards = json.loads((DOC_ROOT / "negative_guards_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((DOC_ROOT / "phase_contract.json").read_text(encoding="utf-8"))
    require(inventory["canonical_owner"] == "Model Manager / Model Governance", "canonical owner changed", failures)
    require(inventory["current_physical_asset_status"] == "ASSET_NOT_PRESENT", "current physical asset state is not honest", failures)
    require(policy["acceptable_checksum_for_ready_candidate"] == "CHECKSUM_VERIFIED", "checksum admission policy missing", failures)
    require(contract["agent_may_copy_or_move"] is False, "copy guard missing", failures)
    require(contract["agent_may_compute_checksum"] is False, "checksum guard missing", failures)
    require(contract["agent_may_probe_dependencies"] is False, "probe execution guard missing", failures)
    require(contract["agent_may_infer"] is False, "inference guard missing", failures)
    for key in ("model_inference_executed", "provider_invocation_executed", "network_access", "automatic_dependency_install", "semantic_compression"):
        require(guards[key] is False, f"negative guard changed: {key}", failures)
    result_path = OUT_ROOT / "s3_yolo11n_external_asset_provisioning_result_v1.json"
    case_path = OUT_ROOT / "s3_yolo11n_external_asset_provisioning_case_results_v1.json"
    trace_path = OUT_ROOT / "s3_yolo11n_external_asset_provisioning_trace_v1.json"
    for path in (result_path, case_path, trace_path):
        require(path.is_file(), f"runner artifact missing: {path.name}", failures)
    if result_path.is_file():
        result = json.loads(result_path.read_text(encoding="utf-8"))
        require(result.get("target_model") == "YOLO11n", "runner target mismatch", failures)
        require(result.get("model_inference_executed") is False, "inference was executed", failures)
        require(result.get("provider_invocation_executed") is False, "provider was invoked", failures)
        require(result.get("automatic_model_download") is False, "model download guard changed", failures)
    if case_path.is_file():
        cases = json.loads(case_path.read_text(encoding="utf-8"))
        require(len(cases) == 16, "scenario count mismatch", failures)
        require(not [case for case in cases if not case.get("passed")], "controlled scenarios did not all pass", failures)
    if trace_path.is_file():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        require(trace.get("provenance_grants_authority") is False, "provenance authority guard changed", failures)
        require(trace.get("model_load_executed") is False, "model load was executed", failures)
    print(json.dumps({"failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
