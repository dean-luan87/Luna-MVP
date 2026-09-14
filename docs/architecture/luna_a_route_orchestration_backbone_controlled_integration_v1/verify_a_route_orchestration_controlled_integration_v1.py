from __future__ import annotations

import ast
import json
from pathlib import Path

PHASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PHASE_DIR.parents[2]
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/a_route_orchestration"
OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_orchestration_controlled_integration_v1"

REQUIRED_DOC_FILES = {
    "a_route_orchestration_controlled_integration_overview_v1.md",
    "a_route_orchestration_controlled_execution_contract_v1.json",
    "a_route_orchestration_negative_guards_v1.json",
    "a_route_orchestration_existing_asset_reuse_mapping_v1.json",
    "a_route_orchestration_controlled_change_manifest_v1.json",
    "a_route_orchestration_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_orchestration_controlled_integration_v1.py",
}
REQUIRED_CODE_FILES = {
    "__init__.py",
    "a_route_orchestration_error_types_v1.py",
    "a_route_orchestration_core_types_v1.py",
    "a_route_orchestration_trace_types_v1.py",
    "a_route_orchestration_protocol_v1.py",
    "a_route_orchestration_ownership_guard_v1.py",
    "a_route_orchestration_static_validators_v1.py",
    "a_route_orchestration_engine_v1.py",
    "a_route_orchestration_fixture_v1.py",
    "run_a_route_orchestration_controlled_integration_v1.py",
}
SCENARIOS = {f"A{i:02d}" for i in range(1, 40)}
FALSE_GUARDS = {
    "runtime_execution",
    "source_owner_mutation",
    "emotion_engine_execution",
    "b_route_execution",
    "semantic_compression_execution",
    "database_write",
    "vector_store_write",
    "embedding_execution",
    "model_call",
    "device_control",
    "real_side_effect",
}


def load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def result(check_id: str, passed: bool, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def run_verification() -> dict:
    checks = []
    actual_docs = {item.name for item in PHASE_DIR.iterdir() if item.is_file()}
    checks.append(result("A01_exact_document_file_set", actual_docs == REQUIRED_DOC_FILES, "Documentation file set is exact."))
    actual_code = {item.name for item in CODE_DIR.iterdir() if item.is_file()} if CODE_DIR.is_dir() else set()
    checks.append(result("A02_exact_code_file_set", actual_code == REQUIRED_CODE_FILES, "New orchestration code file set is exact."))

    json_names = sorted(name for name in REQUIRED_DOC_FILES if name.endswith(".json"))
    docs = {}
    parse_ok = True
    for name in json_names:
        try:
            docs[name] = load(name)
        except Exception:
            parse_ok = False
    checks.append(result("A03_json_parse", parse_ok, "All controlled integration JSON assets parse."))

    ast_ok = True
    for path in [PHASE_DIR / "verify_a_route_orchestration_controlled_integration_v1.py", *(CODE_DIR / name for name in REQUIRED_CODE_FILES if name.endswith(".py"))]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            ast_ok = False
    checks.append(result("A04_ast_parse", ast_ok, "Verifier and new code assets parse as AST."))

    contract = docs.get("phase_contract.json", {})
    flags = contract.get("boundary_flags", {})
    checks.append(result("A05_phase_contract", contract.get("execution_mode") == "CONTROLLED_INTEGRATION_IMPLEMENTATION" and flags.get("controlled_integration_only") is True and flags.get("synthetic_only") is True and flags.get("candidate_only") is True and all(flags.get(name) is False for name in FALSE_GUARDS), "Controlled integration boundary flags are frozen."))

    execution = docs.get("a_route_orchestration_controlled_execution_contract_v1.json", {})
    checks.append(result("A06_canonical_owner", execution.get("canonical_owner") == "A Route Orchestration Governance" and "Context Orchestrator" not in execution.get("owned_concepts", []), "Canonical owner is narrow and non-semantic."))
    checks.append(result("A07_lifecycle", len(execution.get("lifecycle_stages", [])) == 18 and "CYCLE_COMPLETE" in execution.get("lifecycle_stages", []) and set(execution.get("control_states", [])) == {"STOPPED", "DEFERRED", "RECONSIDERING", "FAILED", "SUSPENDED"}, "Lifecycle and control states are explicit."))
    checks.append(result("A08_handoff_statuses", set(execution.get("handoff_statuses", [])) == {"CONTRACT_AVAILABLE", "ADAPTER_AVAILABLE", "CONTROLLED_HANDOFF_READY", "RUNTIME_HANDOFF_READY", "BLOCKED", "DEFERRED"} and execution.get("runtime_handoff_ready") is False, "Handoff statuses preserve controlled versus runtime readiness."))
    checks.append(result("A09_feedback_linkage", execution.get("result_feedback", {}).get("flow") == ["Execution / Result", "Result Observation Candidate", "Result Comparison Candidate", "Experience / Learning / Self refs", "next-cycle ingress refs"] and execution.get("result_feedback", {}).get("comparison_logic_implemented") is False, "Result feedback and deferred comparison boundary are explicit."))
    checks.append(result("A10_reconsideration_guards", execution.get("reconsideration", {}).get("maximum_depth_candidate") == 2 and execution.get("reconsideration", {}).get("automatic_retry") is False and execution.get("reconsideration", {}).get("duplicate_request_guard") is True, "Reconsideration depth and loop guards are present."))

    negative = docs.get("a_route_orchestration_negative_guards_v1.json", {}).get("guards", {})
    checks.append(result("A11_negative_guards", all(value is False for key, value in negative.items() if key not in {"synthetic_only", "controlled_integration_only"}) and negative.get("synthetic_only") is True and negative.get("controlled_integration_only") is True, "Negative guards preserve owner and side-effect boundaries."))
    manifest = docs.get("a_route_orchestration_controlled_change_manifest_v1.json", {})
    checks.append(result("A12_existing_owner_protection", manifest.get("existing_files_modified") == [], "No existing owner files are listed as modified."))
    checks.append(result("A13_scenario_manifest", set(manifest.get("scenario_ids", [])) == SCENARIOS, "A01-A39 are mapped one-to-one."))

    reuse = docs.get("a_route_orchestration_existing_asset_reuse_mapping_v1.json", {}).get("classifications", {})
    checks.append(result("A14_reuse_classification", all(reuse.get(key) for key in ("A", "B", "C", "D")), "Existing assets are classified A/B/C/D."))
    checks.append(result("A15_deferred_workstream_boundary", any(item.get("asset") == "Emotion Engine, B Route, semantic compression" for item in reuse.get("D", [])), "Emotion, B Route, and semantic compression remain deferred."))

    case_path = OUTPUT_DIR / "a_route_orchestration_case_results_v1.json"
    result_path = OUTPUT_DIR / "a_route_orchestration_result_v1.json"
    trace_path = OUTPUT_DIR / "a_route_orchestration_trace_v1.json"
    artifacts_exist = all(path.is_file() for path in (case_path, result_path, trace_path))
    checks.append(result("A16_runner_artifacts", artifacts_exist, "Runner artifacts exist."))
    cases = []
    summary = {}
    traces = {}
    if artifacts_exist:
        try:
            cases = json.loads(case_path.read_text(encoding="utf-8"))
            summary = json.loads(result_path.read_text(encoding="utf-8"))
            traces = json.loads(trace_path.read_text(encoding="utf-8"))
        except Exception:
            cases = []
    checks.append(result("A17_scenario_coverage", {item.get("case_id") for item in cases} == SCENARIOS and summary.get("scenario_count") == 39, "Runner artifacts cover all 39 scenarios."))
    checks.append(result("A18_controlled_behaviors", bool(cases) and all(item.get("all_checks_passed") is True for item in cases) and summary.get("runtime_execution") is False and summary.get("candidate_only") is True, "All controlled case behavior checks pass without runtime execution."))
    checks.append(result("A19_trace_provenance", bool(traces.get("case_traces")) and all(item.get("root_cycle_trace_id") and item.get("reverse_lookup_path") and item.get("authority_granted") is False for item in traces.get("case_traces", [])), "Trace continuity and provenance reverse lookup are present."))
    checks.append(result("A20_no_emotion_or_b_route_implementation", not (REPO_ROOT / "capabilities/midplatform/core/emotion_governance").exists() and not (REPO_ROOT / "capabilities/midplatform/core/b_route").exists(), "No Emotion Engine or B Route implementation directory exists."))

    passed = sum(1 for item in checks if item["passed"])
    return {"phase": "Phase-Luna-A-Route-Orchestration-Backbone-Controlled-Integration-v1-001", "checks": checks, "passed_check_count": passed, "failed_check_count": len(checks) - passed, "blocker_count": sum(1 for item in checks if not item["passed"]), "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION"}


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
