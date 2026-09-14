from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOC_ROOT = Path(__file__).resolve().parent
CODE_ROOT = ROOT / "capabilities/midplatform/field_perception_orchestrator/integration/yolo11n_single_frame_execution"
OUT_ROOT = ROOT / "_eval_out/a_route_s3_yolo11n_real_single_frame_provider_execution_v1"

EXPECTED_DOCS = {
    "overview_v1.md",
    "inventory_v1.json",
    "execution_path_v1.json",
    "model_manager_admission_v1.json",
    "provider_execution_contract_v1.json",
    "evidence_mapping_v1.json",
    "zero_detection_and_error_policy_v1.json",
    "regression_and_differential_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "trace_provenance_v1.json",
    "change_manifest_v1.json",
    "phase_contract.json",
    "implementation_summary_v1.md",
    "verify_luna_a_route_s3_yolo11n_real_single_frame_provider_execution_v1.py",
}
EXPECTED_CODE = {
    "__init__.py",
    "yolo11n_single_frame_execution_types_v1.py",
    "yolo11n_single_frame_execution_fixture_v1.py",
    "run_yolo11n_real_single_frame_provider_execution_v1.py",
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
    contract = json.loads((DOC_ROOT / "phase_contract.json").read_text(encoding="utf-8"))
    evidence = json.loads((DOC_ROOT / "evidence_mapping_v1.json").read_text(encoding="utf-8"))
    guards = json.loads((DOC_ROOT / "negative_guards_v1.json").read_text(encoding="utf-8"))
    require(contract["real_component_scope"] == ["VISION_YOLO11N_PROVIDER"], "real scope changed", failures)
    require(contract["single_frame_only"] is True and contract["max_invocations"] == 1, "single-frame bound missing", failures)
    require(evidence["candidate_only"] is True and evidence["truth_declared"] is False and evidence["fact_admitted"] is False, "evidence authority boundary changed", failures)
    for key, value in guards.items():
        require(value is False, f"negative guard changed: {key}", failures)
    result_path = OUT_ROOT / "a_route_s3_yolo11n_real_single_frame_result_v1.json"
    cases_path = OUT_ROOT / "a_route_s3_yolo11n_real_single_frame_case_results_v1.json"
    trace_path = OUT_ROOT / "a_route_s3_yolo11n_real_single_frame_trace_v1.json"
    for path in (result_path, cases_path, trace_path):
        require(path.is_file(), f"runner artifact missing: {path.name}", failures)
    if result_path.is_file():
        result = json.loads(result_path.read_text(encoding="utf-8"))
        require(result.get("s0_all_cases_passed") is True, "S0 regression failed", failures)
        require(result.get("s1_all_cases_passed") is True, "S1 regression failed", failures)
        require(result.get("s2_all_cases_passed") is True, "S2 regression failed", failures)
        require(result.get("s3_synthetic_all_cases_passed") is True, "S3 synthetic regression failed", failures)
        require(result.get("s3_y11_real_case_present") is True, "real case missing", failures)
        require(result.get("s3_y11_real_case_passed") is True, "real single-frame case failed", failures)
        require(result.get("provider_status") in {"SUCCESS_WITH_DETECTIONS", "SUCCESS_ZERO_DETECTIONS"}, "provider did not succeed", failures)
        require(result.get("model_inference_executed") is True and result.get("provider_invocation_executed") is True, "real execution flags missing", failures)
        require(result.get("network_access") is False and result.get("automatic_model_download") is False, "network/download guard changed", failures)
    if cases_path.is_file():
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        require({item.get("scenario_id") for item in cases if item.get("scenario_id", "").startswith("Y11E-")} == {f"Y11E-{index:02d}" for index in range(1, 19)}, "Y11E coverage missing", failures)
        require(all(item.get("all_checks_passed") is True for item in cases), "single-frame case checks failed", failures)
    if trace_path.is_file():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        require(trace.get("provenance_grants_authority") is False, "provenance authority changed", failures)
        require(trace.get("raw_content_persisted") is False, "raw content persisted", failures)
    print(json.dumps({"failed_check_count": len(failures), "blocker_count": len(failures), "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
