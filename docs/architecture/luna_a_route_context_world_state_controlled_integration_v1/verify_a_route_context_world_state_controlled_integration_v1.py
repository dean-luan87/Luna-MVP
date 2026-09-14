from __future__ import annotations

import ast
import json
from pathlib import Path

VERIFIER_PATH = Path(__file__).resolve()
PHASE_DIR = VERIFIER_PATH.parent


def _resolve_repo_root() -> Path:
    for candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/context_foundation/integration"
OUTPUT_DIR = REPO_ROOT / "_eval_out/context_world_state_controlled_integration_v1"
SCENARIOS = {f"C{i:02d}" for i in range(1, 37)}

REQUIRED_DOC_FILES = {
    "context_world_state_controlled_integration_overview_v1.md",
    "context_world_state_controlled_execution_contract_v1.json",
    "context_world_owner_reuse_matrix_v1.json",
    "observation_context_handoff_contract_v1.json",
    "observation_field_event_handoff_contract_v1.json",
    "field_state_current_world_boundary_v1.json",
    "temporal_validity_integration_contract_v1.json",
    "contradiction_correction_integration_contract_v1.json",
    "trace_provenance_integration_contract_v1.json",
    "a_route_context_world_handoff_mapping_v1.json",
    "context_world_negative_guards_v1.json",
    "context_world_scenario_mapping_v1.json",
    "context_world_change_manifest_v1.json",
    "context_world_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_context_world_state_controlled_integration_v1.py",
}
REQUIRED_CODE_FILES = {
    "__init__.py",
    "context_world_state_controlled_integration_types_v1.py",
    "context_world_state_controlled_integration_error_types_v1.py",
    "context_world_state_controlled_integration_engine_v1.py",
    "context_world_state_controlled_integration_fixture_v1.py",
    "run_context_world_state_controlled_integration_v1.py",
}
FALSE_GUARDS = {
    "provider_can_mutate_context", "provider_can_mutate_field", "observation_can_mutate_field",
    "context_can_mutate_field", "current_world_can_mutate_field", "observation_declares_truth",
    "context_declares_truth", "current_world_is_field_truth", "second_field_writer",
    "runtime_execution", "provider_invocation", "model_call", "database_write", "vector_store_write",
    "scheduler_execution", "device_control", "emotion_engine_execution", "b_route_execution",
    "semantic_compression_execution", "real_side_effect",
}


def _load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def _check(check_id: str, passed: bool, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def run_verification() -> dict:
    checks = []
    actual_docs = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    checks.append(_check("CWI01_exact_document_files", actual_docs == REQUIRED_DOC_FILES, "Required Context / World documentation set is exact."))
    actual_code = {name for name in REQUIRED_CODE_FILES if (CODE_DIR / name).is_file()}
    checks.append(_check("CWI02_exact_code_files", actual_code == REQUIRED_CODE_FILES, "Integration code set exists under existing Context Foundation owner."))

    docs = {}
    json_ok = True
    for name in sorted(REQUIRED_DOC_FILES):
        if name.endswith(".json"):
            try:
                docs[name] = _load(name)
            except Exception:
                json_ok = False
    checks.append(_check("CWI03_json_parse", json_ok, "All integration JSON assets parse."))

    ast_ok = True
    for path in [PHASE_DIR / "verify_a_route_context_world_state_controlled_integration_v1.py", *(CODE_DIR / name for name in REQUIRED_CODE_FILES if name.endswith(".py"))]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            ast_ok = False
    checks.append(_check("CWI04_ast_parse", ast_ok, "Verifier and integration code parse as AST."))

    contract = docs.get("context_world_state_controlled_execution_contract_v1.json", {})
    required_owners = {
        "observation_admission": "Observation Gateway",
        "context_assembly": "Context Foundation",
        "field_event_admission": "Field Event Admission",
        "field_mutation": "Field State Reducer",
        "current_world_representation": "Cognitive State Formation",
        "orchestration": "A Route Orchestration",
    }
    checks.append(_check("CWI05_owner_reuse", contract.get("owners") == required_owners and contract.get("runtime_execution") is False and contract.get("mutation_authority") is False, "Canonical owners are reused without a semantic super-owner."))
    inequalities = contract.get("semantic_inequalities", [])
    checks.append(_check("CWI06_inequalities", all(item in inequalities for item in ("Observation != Context", "Observation != Field State", "Current World != Field State", "Admitted Observation != Fact", "Field Event != Field State", "Trace / Provenance != semantic authority")), "Context, Field, World, Fact, and authority boundaries are explicit."))

    types_source = (CODE_DIR / "context_world_state_controlled_integration_types_v1.py").read_text(encoding="utf-8")
    checks.append(_check("CWI07_candidate_types", all(token in types_source for token in ("ObservationContextHandoffCandidateV1", "FieldEventHandoffCandidateV1", "ContextWorldAssemblyCandidateV1", "CurrentWorldCandidateV1", "candidate_only")), "Required candidate handoff types exist."))
    engine_source = (CODE_DIR / "context_world_state_controlled_integration_engine_v1.py").read_text(encoding="utf-8")
    checks.append(_check("CWI08_owner_adapters", all(token in engine_source for token in ("ContextFoundationSkeletonV1", "admit_field_event", "Field State Reducer", "CurrentWorldCandidateV1", "field_state_reducer_is_single_mutation_authority")), "Existing Context, Field Event, Reducer and Current World assets are reused."))

    handoff = docs.get("observation_context_handoff_contract_v1.json", {})
    field_handoff = docs.get("observation_field_event_handoff_contract_v1.json", {})
    checks.append(_check("CWI09_observation_handoffs", handoff.get("context_mutation") is False and handoff.get("admitted_observation_is_fact") is False and field_handoff.get("field_event_admission_required") is True and field_handoff.get("observation_can_mutate_field") is False, "Observation handoffs remain candidate-only and admission-gated."))

    boundary = docs.get("field_state_current_world_boundary_v1.json", {})
    checks.append(_check("CWI10_field_world_boundary", boundary.get("field_state_reducer_is_single_mutation_authority") is True and boundary.get("current_world_cannot") and boundary.get("current_world_may_reference"), "Field State and Current World authority boundaries are preserved."))
    temporal = docs.get("temporal_validity_integration_contract_v1.json", {})
    checks.append(_check("CWI11_temporal", set(temporal.get("statuses", [])) >= {"ACTIVE", "STALE", "EXPIRED", "REFRESHED", "SUPERSEDED", "REVOKED"} and temporal.get("scheduler_driven_mutation") is False and temporal.get("silent_expiration") is False, "Temporal validity and non-scheduler boundary exist."))
    contradiction = docs.get("contradiction_correction_integration_contract_v1.json", {})
    checks.append(_check("CWI12_contradiction_correction", contradiction.get("silent_overwrite") is False and contradiction.get("correction_precedence") and contradiction.get("contradiction_state"), "Contradiction and correction lineage are preserved."))
    trace_contract = docs.get("trace_provenance_integration_contract_v1.json", {})
    checks.append(_check("CWI13_trace", len(trace_contract.get("reverse_route", [])) >= 6 and trace_contract.get("authority_granted_by_provenance") is False and trace_contract.get("source_owner_trace_preserved") is True, "Reverse trace and provenance are complete without authority transfer."))
    route = docs.get("a_route_context_world_handoff_mapping_v1.json", {})
    checks.append(_check("CWI14_a_route_handoff", route.get("current_world_to_a_route", {}).get("runtime_handoff_ready") is False and route.get("current_world_to_a_route", {}).get("mutation_authority") is False, "Current World to A Route handoff is candidate-only."))

    guards = docs.get("context_world_negative_guards_v1.json", {}).get("guards", {})
    checks.append(_check("CWI15_negative_guards", all(guards.get(name) is False for name in FALSE_GUARDS) and guards.get("candidate_only") is True and guards.get("synthetic_only") is True, "Mutation, runtime, deferred-workstream and side-effect guards are frozen."))
    scenario = docs.get("context_world_scenario_mapping_v1.json", {})
    checks.append(_check("CWI16_scenario_mapping", set(scenario.get("scenario_ids", [])) == SCENARIOS, "C01-C36 scenario mapping is complete."))
    fixture_source = (CODE_DIR / "context_world_state_controlled_integration_fixture_v1.py").read_text(encoding="utf-8")
    checks.append(_check("CWI17_fixture_ids", all(f'"C{i:02d}"' in fixture_source for i in range(1, 37)), "Fixture source retains one-to-one C01-C36 IDs."))

    manifest = docs.get("context_world_change_manifest_v1.json", {})
    checks.append(_check("CWI18_existing_owner_protection", manifest.get("existing_files_modified") == [] and manifest.get("existing_owner_files_modified") == [] and manifest.get("new_top_level_semantic_owner_created") is False, "No existing owner files or parallel semantic owner are changed."))
    phase = docs.get("phase_contract.json", {})
    checks.append(_check("CWI19_phase_contract", phase.get("execution_mode") == "CONTROLLED_INTEGRATION" and phase.get("runtime_execution") is False and phase.get("field_state_mutation") is False and phase.get("new_top_level_semantic_owner") is False and phase.get("agent_stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "Phase contract preserves controlled integration boundaries."))

    artifacts = [OUTPUT_DIR / name for name in ("context_world_state_result_v1.json", "context_world_state_case_results_v1.json", "context_world_state_trace_v1.json")]
    artifacts_exist = all(path.is_file() for path in artifacts)
    checks.append(_check("CWI20_runner_artifacts", artifacts_exist, "Runner artifacts exist."))
    cases = []
    summary = {}
    trace = {}
    if artifacts_exist:
        try:
            summary = json.loads(artifacts[0].read_text(encoding="utf-8"))
            cases = json.loads(artifacts[1].read_text(encoding="utf-8"))
            trace = json.loads(artifacts[2].read_text(encoding="utf-8"))
        except Exception:
            cases = []
    checks.append(_check("CWI21_runner_coverage", {item.get("case_id") for item in cases} == SCENARIOS and summary.get("scenario_count") == 36, "Runner artifacts cover C01-C36."))
    checks.append(_check("CWI22_controlled_behaviors", bool(cases) and all(item.get("all_checks_passed") is True for item in cases), "All C01-C36 controlled behavior checks pass."))
    checks.append(_check("CWI23_trace_artifact", bool(trace.get("case_traces")) and all(item.get("root_trace_id") and item.get("reverse_lookup_path") and item.get("authority_granted") is False for item in trace.get("case_traces", [])), "Runner trace artifact preserves reverse lookup and no authority."))
    checks.append(_check("CWI24_side_effect_summary", summary.get("runtime_execution") is False and summary.get("provider_invocation") is False and summary.get("model_call") is False and summary.get("database_write") is False and summary.get("field_state_mutation") is False and summary.get("emotion_engine_execution") is False and summary.get("b_route_execution") is False and summary.get("semantic_compression_execution") is False and summary.get("runtime_handoff_ready") is False, "Runner summary confirms no runtime, mutation or deferred workstream activation."))

    passed = sum(1 for item in checks if item["passed"])
    return {
        "phase": "Phase-Luna-A-Route-Context-World-State-Controlled-Integration-v1-001",
        "checks": checks,
        "passed_check_count": passed,
        "failed_check_count": len(checks) - passed,
        "blocker_count": sum(1 for item in checks if not item["passed"]),
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
