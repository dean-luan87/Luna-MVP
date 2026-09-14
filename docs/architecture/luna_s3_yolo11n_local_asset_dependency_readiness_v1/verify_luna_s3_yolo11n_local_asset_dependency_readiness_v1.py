from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT / "capabilities/midplatform/model_manager/model_contract_repository/yolo11n_readiness"
OUT_ROOT = ROOT / "_eval_out/s3_yolo11n_local_asset_dependency_readiness_v1"

EXPECTED_DOCS = {
    "inventory_v1.json",
    "asset_location_policy_v1.json",
    "fingerprint_checksum_v1.json",
    "dependency_readiness_v1.json",
    "admission_readiness_v1.json",
    "license_separation_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "overview_v1.md",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_luna_s3_yolo11n_local_asset_dependency_readiness_v1.py",
}
EXPECTED_CODE = {
    "__init__.py",
    "yolo11n_readiness_types_v1.py",
    "yolo11n_readiness_fixture_v1.py",
    "run_yolo11n_local_asset_dependency_readiness_v1.py",
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
    for item in sorted(EXPECTED_DOCS):
        path = DOC_ROOT / item
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                failures.append(f"invalid JSON: {item}: {exc}")
        elif path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                failures.append(f"invalid verifier AST: {exc}")
    for item in sorted(EXPECTED_CODE):
        try:
            ast.parse((CODE_ROOT / item).read_text(encoding="utf-8"), filename=str(CODE_ROOT / item))
        except SyntaxError as exc:
            failures.append(f"invalid implementation AST: {item}: {exc}")
    manifest = json.loads((DOC_ROOT / "inventory_v1.json").read_text(encoding="utf-8"))
    guards = json.loads((DOC_ROOT / "negative_guards_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((DOC_ROOT / "phase_contract.json").read_text(encoding="utf-8"))
    require(manifest["canonical_owner"] == "Model Manager / Model Governance", "canonical owner changed", failures)
    require(manifest["physical_asset_status"] == "ASSET_NOT_PRESENT", "current physical asset state is not honest", failures)
    require(contract["agent_download_allowed"] is False, "agent download guard missing", failures)
    require(contract["agent_install_allowed"] is False, "agent install guard missing", failures)
    require(contract["inference_allowed"] is False, "inference guard missing", failures)
    require(guards["model_inference_executed"] is False, "inference negative guard changed", failures)
    require(guards["network_access"] is False, "network negative guard changed", failures)
    require(guards["automatic_dependency_install"] is False, "dependency install guard changed", failures)
    require(guards["semantic_compression"] is False, "semantic compression guard changed", failures)
    require((DOC_ROOT / "scenario_mapping_v1.json").exists(), "scenario mapping missing", failures)
    result_path = OUT_ROOT / "s3_yolo11n_local_asset_dependency_readiness_result_v1.json"
    case_path = OUT_ROOT / "s3_yolo11n_local_asset_dependency_readiness_case_results_v1.json"
    trace_path = OUT_ROOT / "s3_yolo11n_local_asset_dependency_readiness_trace_v1.json"
    for path in (result_path, case_path, trace_path):
        require(path.is_file(), f"runner artifact missing: {path.name}", failures)
    if result_path.is_file():
        result = json.loads(result_path.read_text(encoding="utf-8"))
        require(result.get("target_model") == "YOLO11n", "runner target mismatch", failures)
        require(result.get("model_inference_executed") is False, "runner inference guard changed", failures)
        require(result.get("automatic_model_download") is False, "runner download guard changed", failures)
    if case_path.is_file():
        cases = json.loads(case_path.read_text(encoding="utf-8"))
        require(len(cases) == 16, "scenario count mismatch", failures)
        require(not [item for item in cases if not item.get("passed")], "controlled scenarios did not all pass", failures)
    if trace_path.is_file():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        require(trace.get("provenance_grants_authority") is False, "provenance authority guard changed", failures)
    print(json.dumps({"failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
