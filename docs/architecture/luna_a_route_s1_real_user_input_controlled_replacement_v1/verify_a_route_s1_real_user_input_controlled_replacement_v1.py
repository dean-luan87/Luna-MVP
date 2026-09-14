from __future__ import annotations

import ast
import json
from pathlib import Path


S0_CODE_FILES = {
    "__init__.py",
    "a_route_product_loop_integration_core_types_v1.py",
    "a_route_product_loop_integration_error_types_v1.py",
    "a_route_product_loop_integration_ownership_guard_v1.py",
    "a_route_product_loop_integration_engine_v1.py",
    "a_route_product_loop_integration_fixture_v1.py",
    "run_a_route_runtime_product_loop_controlled_integration_v1.py",
}
S1_CODE_FILES = {
    "a_route_real_user_input_adapter_types_v1.py",
    "a_route_real_user_input_adapter_v1.py",
    "a_route_real_user_input_fixture_v1.py",
    "run_a_route_s1_real_user_input_controlled_replacement_v1.py",
}
DOC_FILES = {
    "s1_real_user_input_replacement_overview_v1.md",
    "s1_real_user_input_inventory_and_reuse_v1.json",
    "s1_real_user_input_controlled_execution_contract_v1.json",
    "s1_real_user_input_differential_validation_contract_v1.json",
    "s1_real_user_input_trace_provenance_contract_v1.json",
    "s1_real_user_input_negative_guards_v1.json",
    "s1_real_user_input_scenario_mapping_v1.json",
    "s1_real_user_input_change_manifest_v1.json",
    "s1_real_user_input_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_s1_real_user_input_controlled_replacement_v1.py",
}
PARALLEL_OWNER_NAMES = {
    "product_loop_governance",
    "a_route_runtime_governance",
    "runtime_brain",
    "cognitive_brain_governance",
    "product_orchestration_governance",
}


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    root = repo_root_from(Path(__file__).resolve())
    code_dir = root / "capabilities/midplatform/core/a_route_orchestration/integration"
    doc_dir = root / "docs/architecture/luna_a_route_s1_real_user_input_controlled_replacement_v1"
    eval_dir = root / "_eval_out/a_route_s1_real_user_input_controlled_replacement_v1"

    actual_code = {path.name for path in code_dir.iterdir() if path.is_file() and path.suffix == ".py"}
    require(actual_code == S0_CODE_FILES | S1_CODE_FILES, "S0/S1 code file set mismatch", failures)
    actual_docs = {path.name for path in doc_dir.iterdir() if path.is_file()}
    require(actual_docs == DOC_FILES, "S1 documentation file set mismatch", failures)
    for path in sorted(code_dir.glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            failures.append(f"AST parse failed: {path.name}: {exc}")
    for path in sorted(doc_dir.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed: {path.name}: {exc}")

    contract = json.loads((doc_dir / "phase_contract.json").read_text(encoding="utf-8"))
    require(contract.get("s0_baseline") == "S0_GOLDEN_SYNTHETIC_BASELINE:FROZEN_V1", "S0 baseline not frozen", failures)
    require(contract.get("new_semantic_owner") is False, "new semantic owner declared", failures)
    require(contract.get("s0_assets_modified") is False, "S0 assets modified", failures)
    require(contract.get("existing_owner_files_modified") is False, "existing owner files modified", failures)
    require(contract.get("real_components") == ["USER_INPUT"], "S1 real component scope mismatch", failures)
    false_guards = [key for key, value in contract.items() if key.endswith(("execution", "invocation", "call", "write", "control", "mutation", "side_effect")) and value is not False]
    require(not false_guards, f"S1 negative guard mismatch: {false_guards}", failures)
    require(contract.get("candidate_only") is True, "candidate boundary mismatch", failures)

    inventory = json.loads((doc_dir / "s1_real_user_input_inventory_and_reuse_v1.json").read_text(encoding="utf-8"))
    require(inventory.get("canonical_product_input_contract") == "ProductLoopInputV1", "ProductLoopInputV1 not canonical", failures)
    require(inventory.get("canonical_owner") == "A Route Orchestration Governance", "canonical owner mismatch", failures)
    require(inventory.get("new_semantic_owner") is False, "parallel input owner declared", failures)
    parallel_matches = tuple(
        path for base in (root / "capabilities/midplatform/core", root / "docs/architecture")
        for path in base.rglob("*")
        if path.is_dir() and path.name in PARALLEL_OWNER_NAMES
    )
    require(not parallel_matches, "parallel semantic owner created", failures)

    mapping = json.loads((doc_dir / "s1_real_user_input_scenario_mapping_v1.json").read_text(encoding="utf-8"))
    require(set(mapping.get("scenario_ids", [])) == {f"S1-{index:02d}" for index in range(1, 21)}, "S1 scenario mapping mismatch", failures)
    differential = json.loads((doc_dir / "s1_real_user_input_differential_validation_contract_v1.json").read_text(encoding="utf-8"))
    require(differential.get("synthetic_adapter_retained") is True, "synthetic adapter retention missing", failures)
    require(differential.get("one_component_at_a_time") is True, "single component replacement missing", failures)
    require(tuple(differential.get("comparison_dimensions", ())) == ("contract outputs", "trace/provenance", "state transitions", "negative guards", "unrelated module behavior"), "differential dimensions mismatch", failures)

    s0_manifest = json.loads((root / "docs/architecture/luna_a_route_golden_synthetic_product_loop_baseline_freeze_v1/a_route_golden_synthetic_baseline_manifest_v1.json").read_text(encoding="utf-8"))
    require(s0_manifest.get("freeze_status") == "FROZEN_V1", "S0 freeze evidence missing", failures)
    require(s0_manifest.get("freeze_id") == "S0_GOLDEN_SYNTHETIC_BASELINE", "S0 freeze identity mismatch", failures)

    artifacts = {
        "summary": eval_dir / "a_route_s1_real_user_input_result_v1.json",
        "cases": eval_dir / "a_route_s1_real_user_input_case_results_v1.json",
        "s0_cases": eval_dir / "a_route_s1_s0_regression_case_results_v1.json",
        "trace": eval_dir / "a_route_s1_real_user_input_trace_v1.json",
    }
    require(all(path.exists() for path in artifacts.values()), "S1 runner artifacts missing", failures)
    if all(path.exists() for path in artifacts.values()):
        summary = json.loads(artifacts["summary"].read_text(encoding="utf-8"))
        cases = json.loads(artifacts["cases"].read_text(encoding="utf-8"))
        s0_cases = json.loads(artifacts["s0_cases"].read_text(encoding="utf-8"))
        traces = json.loads(artifacts["trace"].read_text(encoding="utf-8"))
        require(summary.get("s1_scenario_count") == 20, "S1 scenario count mismatch", failures)
        require(summary.get("s0_scenario_count") == 40, "S0 scenario count mismatch", failures)
        require(summary.get("s0_all_cases_passed") is True, "S0 regression failed", failures)
        require(summary.get("all_cases_passed") is True, "S1 cases did not pass", failures)
        require(summary.get("failed_case_ids") == [], "S1 runner reports failed cases", failures)
        expected_s1_ids = {f"S1-{index:02d}" for index in range(1, 21)}
        require({item.get("scenario_id") for item in cases if item.get("scenario_id") in expected_s1_ids} == expected_s1_ids, "S1 case coverage mismatch", failures)
        require(all(item.get("all_checks_passed") is True for item in cases), "S1 case checks did not pass", failures)
        require({item.get("scenario_id") for item in s0_cases} == {f"L{index:02d}" for index in range(1, 41)}, "S0 regression coverage mismatch", failures)
        require(all(item.get("all_checks_passed") is True for item in s0_cases), "S0 case checks did not pass", failures)
        require(all(item.get("adapter_trace", {}).get("provenance_grants_authority") is False for item in traces), "S1 trace authority boundary violated", failures)
        s1_11 = next((item for item in cases if item.get("scenario_id") == "S1-11"), {})
        s1_11_trace = s1_11.get("actual", {}).get("trace", {}).get("adapter_trace", {})
        require(bool(s1_11_trace.get("input_id")) and bool(s1_11_trace.get("raw_input_ref")), "S1-11 trace reverse lookup missing", failures)
        if summary.get("mode") == "REAL_USER_INPUT_CONTROLLED":
            require(summary.get("real_components") == ["USER_INPUT"], "real mode activated extra components", failures)
            require(summary.get("synthetic_components") == ["all_remaining_s0_components"], "real mode downstream scope mismatch", failures)

    print(f"FAILED_CHECK_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL={failure}")
    print(f"BLOCKER_COUNT={len(failures)}")
    print(f"S1_STATUS={'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
