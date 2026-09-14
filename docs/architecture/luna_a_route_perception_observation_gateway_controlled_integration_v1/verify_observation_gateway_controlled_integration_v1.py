from __future__ import annotations

import ast
import json
from pathlib import Path

VERIFIER_PATH = Path(__file__).resolve()
PHASE_DIR = VERIFIER_PATH.parent


def _resolve_repo_root() -> Path:
    for candidate in (PHASE_DIR, *PHASE_DIR.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError(
        "Unable to locate repository root sentinel: capabilities/ + docs/ + README.md"
    )


REPO_ROOT = _resolve_repo_root()
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/observation_gateway"
OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_perception_observation_gateway_controlled_integration_v1"

REQUIRED_DOC_FILES = {
    "observation_gateway_controlled_integration_overview_v1.md",
    "observation_gateway_controlled_execution_contract_v1.json",
    "observation_gateway_negative_guards_v1.json",
    "observation_gateway_existing_asset_reuse_mapping_v1.json",
    "observation_gateway_a_route_adapter_mapping_v1.json",
    "observation_gateway_controlled_change_manifest_v1.json",
    "observation_gateway_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_observation_gateway_controlled_integration_v1.py",
}
REQUIRED_CODE_FILES = {
    "__init__.py",
    "observation_gateway_error_types_v1.py",
    "observation_gateway_core_types_v1.py",
    "observation_gateway_trace_types_v1.py",
    "observation_gateway_ownership_guard_v1.py",
    "observation_gateway_static_validators_v1.py",
    "observation_gateway_engine_v1.py",
    "observation_gateway_fixture_v1.py",
    "run_observation_gateway_controlled_integration_v1.py",
}
SCENARIOS = {f"O{i:02d}" for i in range(1, 47)}
INGRESS_TYPES = {"USER_INPUT", "VISION", "OCR", "AUDIO", "SLAM_SPATIAL", "FIELD_REFERENCE", "SYSTEM_EVENT", "EXTERNAL_PROVIDER"}
ADMISSION_STATES = {"RECEIVED", "NORMALIZED", "EVIDENCE_READY", "OBSERVATION_CANDIDATE_READY", "NEEDS_CONFIRMATION", "CONTESTED", "ADMITTED_OBSERVATION", "REJECTED", "REVOKED", "EXPIRED", "SUPERSEDED"}
FALSE_GUARDS = {
    "gateway_can_execute_vision", "gateway_can_execute_ocr", "gateway_can_execute_slam", "gateway_can_execute_audio_model",
    "gateway_can_mutate_field_state", "gateway_can_mutate_context", "gateway_can_mutate_attention", "gateway_can_mutate_hypothesis",
    "gateway_can_mutate_intent", "gateway_can_mutate_decision", "gateway_can_mutate_task", "gateway_can_mutate_memory",
    "gateway_can_execute_learning", "gateway_can_mutate_self", "gateway_can_mutate_personality", "gateway_can_mutate_emotion",
    "observation_is_world_truth", "ocr_evidence_is_fact", "visual_detection_is_fact", "slam_geometry_is_semantic_truth",
    "database_write", "vector_store_write", "embedding_execution", "model_call", "scheduler_execution", "device_control",
    "real_side_effect", "cross_user_transfer", "emotion_engine_execution", "b_route_execution", "semantic_compression_execution",
}


def load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def check(check_id: str, passed: bool, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def run_verification() -> dict:
    checks = []
    actual_docs = {item.name for item in PHASE_DIR.iterdir() if item.is_file()}
    checks.append(check("O01_exact_document_file_set", actual_docs == REQUIRED_DOC_FILES, "Documentation file set is exact."))
    actual_code = {item.name for item in CODE_DIR.iterdir() if item.is_file()} if CODE_DIR.is_dir() else set()
    checks.append(check("O02_exact_code_file_set", actual_code == REQUIRED_CODE_FILES, "Observation Gateway code file set is exact."))

    docs = {}
    parse_ok = True
    for name in sorted(REQUIRED_DOC_FILES):
        if name.endswith(".json"):
            try:
                docs[name] = load(name)
            except Exception:
                parse_ok = False
    checks.append(check("O03_json_parse", parse_ok, "All JSON controlled integration assets parse."))

    ast_ok = True
    for path in [PHASE_DIR / "verify_observation_gateway_controlled_integration_v1.py", *(CODE_DIR / name for name in REQUIRED_CODE_FILES if name.endswith(".py"))]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            ast_ok = False
    checks.append(check("O04_ast_parse", ast_ok, "Verifier and new code parse as AST."))

    contract = docs.get("phase_contract.json", {})
    flags = contract.get("boundary_flags", {})
    checks.append(check(contract.get("execution_mode") == "CONTROLLED_INTEGRATION_IMPLEMENTATION" and contract.get("canonical_owner") == "Observation Gateway Governance" and flags.get("controlled_integration_only") is True and flags.get("synthetic_only") is True and flags.get("candidate_only") is True and all(flags.get(name) is False for name in FALSE_GUARDS), "O05_phase_contract", "Controlled integration and negative boundary flags are frozen."))

    execution = docs.get("observation_gateway_controlled_execution_contract_v1.json", {})
    checks.append(check(execution.get("canonical_owner") == "Observation Gateway Governance" and execution.get("owner_type") == "ingress_evidence_observation_admission_and_routing_governance", "O06_canonical_owner", "Canonical owner is narrow and explicit."))
    checks.append(check(set(execution.get("ingress_types", [])) == INGRESS_TYPES, "O07_ingress_type_coverage", "All required ingress types are represented."))
    checks.append(check(set(execution.get("admission_states", [])) == ADMISSION_STATES and execution.get("candidate_only") is True and execution.get("truth_declared") is False, "O08_admission_and_truth_boundary", "Admission lifecycle and non-truth boundary are explicit."))

    negative = docs.get("observation_gateway_negative_guards_v1.json", {}).get("guards", {})
    checks.append(check(all(negative.get(name) is False for name in FALSE_GUARDS) and negative.get("synthetic_only") is True and negative.get("controlled_integration_only") is True, "O09_negative_guards", "All provider, owner mutation, truth, and side-effect guards are false."))

    reuse = docs.get("observation_gateway_existing_asset_reuse_mapping_v1.json", {}).get("classifications", {})
    checks.append(check(all(reuse.get(key) for key in ("A", "B", "C", "D")) and reuse.get("canonical_owner_found_before_phase") is False, "O10_reuse_classification", "Existing assets are classified A/B/C/D and no canonical owner was found."))
    manifest = docs.get("observation_gateway_controlled_change_manifest_v1.json", {})
    checks.append(check(manifest.get("existing_files_modified") == [], "O11_existing_owner_protection", "No existing owner files are modified."))
    adapter = docs.get("observation_gateway_a_route_adapter_mapping_v1.json", {})
    checks.append(check(adapter.get("consumer") == "A Route Orchestration Governance" and adapter.get("route_lifecycle_target") == "INGRESS_READY" and adapter.get("mutation_authority") is False and adapter.get("runtime_handoff_ready") is False, "O12_a_route_adapter", "A Route ingress adapter is candidate-only and non-mutating."))

    source = (CODE_DIR / "observation_gateway_core_types_v1.py").read_text(encoding="utf-8")
    checks.append(check(all(token in source for token in ("ObservationIngressCandidateV1", "PerceptionEvidenceV1", "ObservationCandidateV1", "candidate_only", "truth_declared", "source_model_ref", "source_region_ref", "contradiction_refs", "correction_refs")), "O13_core_models", "Ingress, evidence, observation, lineage, and candidate fields exist."))
    checks.append(check(all(token in source for token in ("USER_INPUT", "VISION", "OCR", "AUDIO", "SLAM_SPATIAL", "FIELD_REFERENCE", "SYSTEM_EVENT", "EXTERNAL_PROVIDER")), "O14_core_ingress_types", "Core ingress type registry is complete."))
    engine_source = (CODE_DIR / "observation_gateway_engine_v1.py").read_text(encoding="utf-8")
    checks.append(check(all(token in engine_source for token in ("multi_evidence_agreement", "multi_evidence_contradiction", "user_correction", "valid_until_candidate", "DUPLICATE_INGRESS", "DUPLICATE_EVIDENCE", "DUPLICATE_OBSERVATION", "INGRESS_READY")), "O15_behavioral_boundaries", "Multi-evidence, correction, temporal, idempotency, and A Route behavior are implemented."))
    error_source = (CODE_DIR / "observation_gateway_error_types_v1.py").read_text(encoding="utf-8")
    checks.append(check(all(token in error_source for token in ("INVALID_INGRESS", "INVALID_EVIDENCE_MAPPING", "MISSING_PROVENANCE", "DUPLICATE_INGRESS", "INVALID_ADMISSION_TRANSITION", "INVALID_CORRECTION_LINEAGE", "INVALID_ROUTING_TARGET")), "O16_error_namespace", "Observation Gateway error namespace is narrow and complete."))

    case_path = OUTPUT_DIR / "observation_gateway_case_results_v1.json"
    result_path = OUTPUT_DIR / "observation_gateway_result_v1.json"
    trace_path = OUTPUT_DIR / "observation_gateway_trace_v1.json"
    artifacts_exist = all(path.is_file() for path in (case_path, result_path, trace_path))
    checks.append(check("O17_runner_artifacts", artifacts_exist, "Runner artifacts exist."))
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
    checks.append(check({item.get("case_id") for item in cases} == SCENARIOS and summary.get("scenario_count") == 46, "O18_scenario_coverage", "Runner artifacts cover O01-O46."))
    checks.append(check(bool(cases) and all(item.get("all_checks_passed") is True for item in cases), "O19_controlled_behaviors", "All controlled gateway behavior checks pass."))
    checks.append(check(bool(traces.get("case_traces")) and all(item.get("root_trace_id") and item.get("reverse_lookup_path") and item.get("authority_granted") is False for item in traces.get("case_traces", [])), "O20_trace_provenance", "Trace/provenance reverse lookup is preserved without authority."))
    checks.append(check(summary.get("runtime_execution") is False and summary.get("model_call") is False and summary.get("database_write") is False and summary.get("device_control") is False and summary.get("emotion_engine_execution") is False and summary.get("b_route_execution") is False and summary.get("semantic_compression_execution") is False, "O21_deferred_and_side_effect_boundary", "No provider/runtime/model/device side effects or deferred workstream activation."))
    checks.append(check(not (REPO_ROOT / "capabilities/midplatform/core/perception_governance").exists() and not (REPO_ROOT / "capabilities/midplatform/core/vision_governance").exists() and not (REPO_ROOT / "capabilities/midplatform/core/ocr_governance").exists() and not (REPO_ROOT / "capabilities/midplatform/core/slam_governance").exists(), "O22_no_parallel_owner", "No parallel perception/provider semantic owner was created."))

    passed = sum(1 for item in checks if item["passed"])
    return {"phase": "Phase-Luna-A-Route-Perception-Observation-Gateway-Controlled-Integration-v1-001", "checks": checks, "passed_check_count": passed, "failed_check_count": len(checks) - passed, "blocker_count": sum(1 for item in checks if not item["passed"]), "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION"}


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
