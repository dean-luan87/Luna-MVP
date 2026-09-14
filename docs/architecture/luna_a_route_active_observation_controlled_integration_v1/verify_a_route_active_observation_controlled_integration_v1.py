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
CODE_DIR = REPO_ROOT / "capabilities/midplatform/field_perception_orchestrator/integration"
OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_active_observation_controlled_integration_v1"

REQUIRED_DOC_FILES = {
    "a_route_active_observation_controlled_integration_overview_v1.md",
    "a_route_active_observation_controlled_execution_contract_v1.json",
    "provider_autonomy_contract_v1.json",
    "evidence_sufficiency_contract_v1.json",
    "control_decision_contract_v1.json",
    "existing_asset_reuse_mapping_v1.json",
    "a_route_handoff_mapping_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "controlled_change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_a_route_active_observation_controlled_integration_v1.py",
}
NEW_CODE_FILES = {
    "field_perception_active_observation_control_types_v1.py",
    "field_perception_active_observation_control_error_types_v1.py",
    "field_perception_active_observation_control_engine_v1.py",
    "field_perception_active_observation_control_fixture_v1.py",
    "run_field_perception_active_observation_controlled_integration_v1.py",
}
SCENARIOS = {f"R{i:02d}" for i in range(1, 37)}
CONTROL_DECISIONS = {"STOP", "CONTINUE", "REDIRECT", "SWITCH_PROVIDER", "ADD_CAPABILITY", "RECONSIDER", "DEFER", "FAIL"}
FALSE_GUARDS = {
    "provider_autonomous_continuous_execution", "provider_invocation", "runtime_execution",
    "provider_can_mutate_context", "provider_can_mutate_field", "provider_can_mutate_intent",
    "provider_can_mutate_task", "provider_can_mutate_decision", "observation_control_can_mutate_context",
    "observation_control_can_mutate_field", "observation_control_can_mutate_intent",
    "observation_control_can_mutate_task", "observation_control_can_mutate_decision",
    "observation_gateway_admission_is_execution", "model_confidence_is_sufficiency", "database_write",
    "vector_store_write", "embedding_execution", "model_call", "scheduler_execution", "device_control",
    "emotion_engine_execution", "b_route_execution", "semantic_compression_execution",
}


def _load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def _check(check_id: str, passed: bool, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def run_verification() -> dict:
    checks = []
    actual_docs = {p.name for p in PHASE_DIR.iterdir() if p.is_file()}
    checks.append(_check("AOC01_exact_document_files", actual_docs == REQUIRED_DOC_FILES, "Controlled integration documentation set is exact."))
    actual_new_code = {name for name in NEW_CODE_FILES if (CODE_DIR / name).is_file()}
    checks.append(_check("AOC02_new_code_files", actual_new_code == NEW_CODE_FILES, "New controlled integration code assets exist in the existing owner directory."))

    docs = {}
    parse_ok = True
    for name in sorted(REQUIRED_DOC_FILES):
        if name.endswith(".json"):
            try:
                docs[name] = _load(name)
            except Exception:
                parse_ok = False
    checks.append(_check("AOC03_json_parse", parse_ok, "All controlled integration JSON assets parse."))

    ast_ok = True
    for path in [PHASE_DIR / "verify_a_route_active_observation_controlled_integration_v1.py", *(CODE_DIR / name for name in NEW_CODE_FILES if name.endswith(".py"))]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            ast_ok = False
    checks.append(_check("AOC04_ast_parse", ast_ok, "Verifier and new controlled integration code parse as AST."))

    contract = docs.get("a_route_active_observation_controlled_execution_contract_v1.json", {})
    checks.append(_check("AOC05_owner_reuse", contract.get("canonical_owner") == "Field Perception Orchestrator" and contract.get("owner_decision") == "B_EXISTING_OWNER_REQUIRES_CONTROLLED_INTEGRATION" and contract.get("runtime_execution") is False and contract.get("provider_invocation") is False and contract.get("mutation_authority") is False, "Existing Field Perception Orchestrator owner and controlled boundary are frozen."))
    checks.append(_check("AOC06_inequalities", all(item in contract.get("semantic_inequalities", []) for item in ("Observation Demand != Observation Request", "Observation Request != Capability Requirement", "Capability Requirement != Model Selection", "Model Selection != Provider Invocation", "Provider Session Candidate != Provider Runtime Execution", "Evidence Sufficiency != Model Confidence")), "Core semantic inequalities are explicit."))

    types_source = (CODE_DIR / "field_perception_active_observation_control_types_v1.py").read_text(encoding="utf-8")
    checks.append(_check("AOC07_candidate_types", all(token in types_source for token in ("ObservationDemandCandidateV1", "ObservationRequestCandidateV1", "CapabilityRequirementCandidateV1", "BoundedProviderSessionCandidateV1", "EvidenceSufficiencyCandidateV1", "ObservationControlDecisionV1", "NextCycleIngressCandidateV1", "candidate_only", "runtime_execution", "provider_invocation")), "Required candidate type layers exist."))
    engine_source = (CODE_DIR / "field_perception_active_observation_control_engine_v1.py").read_text(encoding="utf-8")
    checks.append(_check("AOC08_engine_guards", all(token in engine_source for token in ("provider_autonomous_continuous_execution = False", "runtime_execution = False", "provider_invocation = False", "gateway_admission_is_continuation_authority", "MAX_RECONSIDERATION_DEPTH", "observation_gateway_handoff_candidate_present", "a_route_ingress_candidate_present")), "Engine-level autonomy, handoff and loop guards exist."))

    autonomy = docs.get("provider_autonomy_contract_v1.json", {})
    checks.append(_check("AOC09_provider_autonomy", autonomy.get("provider_autonomous_continuous_execution") is False and len(autonomy.get("forbidden_authorization_triggers", [])) >= 9 and autonomy.get("general_provider_autonomy") is False and set(autonomy.get("safety_exception_required_fields", [])) >= {"explicit_policy_ref", "reason", "target_scope", "capability_scope", "bounded_budget", "temporal_validity", "revoke_condition", "trace_ref", "provenance_refs"}, "Provider autonomy and bounded safety exception are frozen."))

    sufficiency = docs.get("evidence_sufficiency_contract_v1.json", {})
    checks.append(_check("AOC10_sufficiency", sufficiency.get("inequality") == "Evidence Sufficiency != Model Confidence" and sufficiency.get("model_confidence_role") == "quality_input_only" and len(sufficiency.get("required_inputs", [])) >= 14 and set(sufficiency.get("allowed_statuses", [])) >= {"SUFFICIENT", "INSUFFICIENT", "CONTESTED", "STALE", "NEEDS_CONFIRMATION", "NEEDS_ADDITIONAL_MODALITY", "NEEDS_REDIRECT", "NEEDS_PROVIDER_SWITCH"}, "Evidence Sufficiency is task-relative and not a confidence shortcut."))

    decisions = docs.get("control_decision_contract_v1.json", {})
    checks.append(_check("AOC11_control_decisions", set(decisions.get("decisions", [])) == CONTROL_DECISIONS and decisions.get("authority_boundary", {}).get("runtime_execution") is False and decisions.get("no_hidden_retry") is True, "All deterministic candidate control decisions and no-hidden-retry guard exist."))

    scenario = docs.get("scenario_mapping_v1.json", {})
    checks.append(_check("AOC12_scenario_mapping", set(scenario.get("scenario_ids", [])) == SCENARIOS, "R01-R36 scenario mapping is complete."))
    fixture_source = (CODE_DIR / "field_perception_active_observation_control_fixture_v1.py").read_text(encoding="utf-8")
    checks.append(_check("AOC13_fixture_ids", all(f'"R{i:02d}"' in fixture_source for i in range(1, 37)), "Fixture source retains one-to-one R01-R36 IDs."))

    guards = docs.get("negative_guards_v1.json", {}).get("guards", {})
    checks.append(_check("AOC14_negative_guards", all(guards.get(name) is False for name in FALSE_GUARDS) and guards.get("candidate_only") is True and guards.get("synthetic_only") is True and guards.get("controlled_integration_only") is True, "Runtime, provider, mutation, Emotion, B Route and semantic compression guards are frozen."))

    handoff = docs.get("a_route_handoff_mapping_v1.json", {})
    checks.append(_check("AOC15_a_route_handoff", handoff.get("a_route_ingress", {}).get("route_lifecycle_target") == "INGRESS_READY" and handoff.get("a_route_ingress", {}).get("runtime_handoff_ready") is False and handoff.get("a_route_ingress", {}).get("mutation_authority") is False and handoff.get("observation_gateway_handoff", {}).get("admission_is_continuation_authority") is False, "Observation Gateway and A Route handoffs remain candidate-only."))

    manifest = docs.get("controlled_change_manifest_v1.json", {})
    checks.append(_check("AOC16_existing_owner_protection", manifest.get("existing_files_modified") == [] and manifest.get("existing_owner_files_modified") == [] and manifest.get("new_top_level_owner_created") is False, "No existing owner files or parallel owner are modified/created."))

    phase = docs.get("phase_contract.json", {})
    checks.append(_check("AOC17_phase_contract", phase.get("execution_mode") == "CONTROLLED_INTEGRATION" and phase.get("controlled_integration_only") is True and phase.get("runtime_execution") is False and phase.get("provider_invocation") is False and phase.get("database_write") is False and phase.get("model_call") is False and phase.get("emotion_engine_execution") is False and phase.get("b_route_execution") is False and phase.get("semantic_compression_execution") is False and phase.get("existing_owner_files_modified") == [], "Phase contract preserves controlled integration boundaries."))

    artifacts = [OUTPUT_DIR / name for name in ("active_observation_control_result_v1.json", "active_observation_control_case_results_v1.json", "active_observation_control_trace_v1.json")]
    artifacts_exist = all(path.is_file() for path in artifacts)
    checks.append(_check("AOC18_runner_artifacts", artifacts_exist, "Runner artifacts exist."))
    cases = []
    summary = {}
    trace = {}
    if artifacts_exist:
        try:
            cases = json.loads(artifacts[1].read_text(encoding="utf-8"))
            summary = json.loads(artifacts[0].read_text(encoding="utf-8"))
            trace = json.loads(artifacts[2].read_text(encoding="utf-8"))
        except Exception:
            cases = []
    checks.append(_check("AOC19_runner_scenario_coverage", {item.get("case_id") for item in cases} == SCENARIOS and summary.get("scenario_count") == 36, "Runner artifacts cover R01-R36."))
    checks.append(_check("AOC20_controlled_behaviors", bool(cases) and all(item.get("all_checks_passed") is True for item in cases), "All controlled R01-R36 behavior checks pass."))
    checks.append(_check("AOC21_trace_provenance", bool(trace.get("case_traces")) and all(item.get("root_cycle_trace_id") and item.get("reverse_lookup_path") and item.get("authority_granted") is False for item in trace.get("case_traces", [])), "Trace reverse lookup and no-authority provenance are preserved."))
    checks.append(_check("AOC22_side_effect_boundary", summary.get("runtime_execution") is False and summary.get("provider_invocation") is False and summary.get("model_call") is False and summary.get("database_write") is False and summary.get("device_control") is False and summary.get("emotion_engine_execution") is False and summary.get("b_route_execution") is False and summary.get("semantic_compression_execution") is False and summary.get("runtime_handoff_ready") is False, "Runner summary confirms no runtime or deferred workstream activation."))
    checks.append(_check("AOC23_no_parallel_owner", not (REPO_ROOT / "capabilities/midplatform/core/active_observation_control").exists() and not (REPO_ROOT / "capabilities/midplatform/core/observation_control_governance").exists() and not (REPO_ROOT / "capabilities/midplatform/core/perception_governance").exists(), "No parallel semantic owner directory exists."))

    passed = sum(1 for item in checks if item["passed"])
    return {"phase":"Phase-Luna-A-Route-Active-Observation-Controlled-Integration-v1-001","checks":checks,"passed_check_count":passed,"failed_check_count":len(checks)-passed,"blocker_count":sum(1 for item in checks if not item["passed"]),"status":"WAITING_FOR_USER_TERMINAL_VERIFICATION"}


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
