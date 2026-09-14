from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def _find_repo_root(start: Path) -> Path:
    """Walk upward to a stable repository sentinel; never depend on cwd."""
    for candidate in (start, *start.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("stable repository sentinel not found")


PHASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = _find_repo_root(PHASE_DIR)
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/personality_governance"
EVAL_DIR = REPO_ROOT / "_eval_out/personality_governance_controlled_implementation_v1"

CODE_FILES: Set[str] = {
    "__init__.py",
    "personality_governance_registry_v1.py",
    "personality_governance_error_types_v1.py",
    "personality_governance_core_types_v1.py",
    "personality_trait_types_v1.py",
    "personality_profile_types_v1.py",
    "personality_stability_types_v1.py",
    "personality_admission_types_v1.py",
    "personality_revision_types_v1.py",
    "personality_influence_types_v1.py",
    "personality_trace_types_v1.py",
    "personality_io_types_v1.py",
    "personality_governance_protocol_v1.py",
    "personality_governance_ownership_guard_v1.py",
    "personality_governance_static_validators_v1.py",
    "personality_governance_fixture_v1.py",
    "personality_governance_engine_v1.py",
    "run_personality_governance_controlled_implementation_v1.py",
}

DOC_FILES: Set[str] = {
    "personality_governance_controlled_implementation_overview_v1.md",
    "personality_governance_controlled_execution_contract_v1.json",
    "personality_governance_negative_guards_v1.json",
    "personality_governance_planning_to_code_mapping_v1.json",
    "personality_governance_controlled_change_manifest_v1.json",
    "personality_governance_implementation_summary_v1.md",
    "phase_contract.json",
    "verify_personality_governance_controlled_implementation_v1.py",
}

OUTPUT_FILES = {
    "personality_governance_result_v1.json",
    "personality_governance_case_results_v1.json",
    "personality_governance_trace_v1.json",
}
EXPECTED_SCENARIOS = {f"P{index:02d}" for index in range(1, 37)}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_verification() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    actual_code = {path.name for path in CODE_DIR.iterdir() if path.is_file()} if CODE_DIR.is_dir() else set()
    actual_docs = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    add("exact_code_file_set", actual_code == CODE_FILES, f"missing={sorted(CODE_FILES - actual_code)} extra={sorted(actual_code - CODE_FILES)}")
    add("exact_doc_file_set", actual_docs == DOC_FILES, f"missing={sorted(DOC_FILES - actual_docs)} extra={sorted(actual_docs - DOC_FILES)}")

    json_failures: List[str] = []
    docs: Dict[str, Any] = {}
    for name in sorted(name for name in DOC_FILES if name.endswith(".json")):
        try:
            docs[name] = _json(PHASE_DIR / name)
        except Exception as exc:
            json_failures.append(f"{name}:{exc}")
            docs[name] = {}
    add("implementation_json_parse", not json_failures, str(json_failures) if json_failures else "all implementation JSON parsed")

    ast_failures: List[str] = []
    for path in [*(CODE_DIR / name for name in CODE_FILES if name.endswith(".py")), PHASE_DIR / "verify_personality_governance_controlled_implementation_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            ast_failures.append(f"{path.name}:{exc}")
    add("python_ast_parse", not ast_failures, str(ast_failures) if ast_failures else "all new Python source AST parsed")

    registry = (CODE_DIR / "personality_governance_registry_v1.py").read_text(encoding="utf-8") if (CODE_DIR / "personality_governance_registry_v1.py").is_file() else ""
    runner_source = (CODE_DIR / "run_personality_governance_controlled_implementation_v1.py").read_text(encoding="utf-8") if (CODE_DIR / "run_personality_governance_controlled_implementation_v1.py").is_file() else ""
    required_dimensions = ["interaction_style", "expressiveness", "initiative_tendency", "social_openness", "caution_tendency", "exploration_tendency", "persistence_tendency", "adaptability", "empathy_expression_tendency", "humor_expression_tendency", "directness", "formality", "risk_tolerance_candidate", "uncertainty_tolerance_candidate", "attachment_expression_tendency", "conflict_style_candidate", "support_style_candidate", "reflection_tendency"]
    add("canonical_owner_and_taxonomy", 'CANONICAL_OWNER = "Personality Governance"' in registry and all(f'"{dimension}"' in registry for dimension in required_dimensions), "single owner and all 18 taxonomy dimensions are statically declared")
    add("runner_bootstrap", "Path(__file__).resolve()" in runner_source and "sys.path.insert(0, str(REPO_ROOT))" in runner_source and "capabilities" in runner_source and "docs" in runner_source, "direct-script runner has cwd-independent repo-root bootstrap")

    contract = docs.get("personality_governance_controlled_execution_contract_v1.json", {})
    contract_flags = contract.get("boundary_flags", {})
    add("execution_contract", contract.get("execution_mode") == "CONTROLLED_IMPLEMENTATION" and contract.get("canonical_owner") == "Personality Governance" and contract.get("synthetic_only") is True and contract.get("candidate_only") is True and all(value is False for value in contract_flags.values()), "controlled execution contract preserves synthetic candidate-only boundaries")

    negative = docs.get("personality_governance_negative_guards_v1.json", {}).get("guards", {})
    required_false = ["personality_can_mutate_self", "personality_can_mutate_memory", "personality_can_execute_learning", "personality_can_mutate_intent", "personality_can_mutate_pcn", "personality_can_mutate_emotion", "personality_can_mutate_regulation_parameters", "personality_can_activate_parameter_genome", "personality_can_create_task", "personality_can_control_device", "personality_can_run_scheduler", "personality_can_call_model", "database_write", "vector_store_write", "embedding_execution", "runtime_execution", "source_owner_mutation", "cross_user_transfer", "semantic_compression_execution", "affective_memory_compression", "emotion_memory_summary_generation", "personality_memory_semantic_fusion", "real_side_effect", "trait_activation"]
    add("negative_guards_contract", all(negative.get(name) is False for name in required_false) and negative.get("synthetic_only") is True and negative.get("candidate_only") is True, "all required controlled implementation negative guards are false")

    manifest = docs.get("personality_governance_controlled_change_manifest_v1.json", {})
    add("change_scope_preserved", manifest.get("existing_files_modified") == [] and manifest.get("planning_assets_modified") == [] and manifest.get("parallel_owner_directories_created") == [], "no existing owner, planning asset, or parallel owner modification recorded")

    phase_contract = docs.get("phase_contract.json", {})
    flags = phase_contract.get("boundary_flags", {})
    forbidden_phase_true = [name for name, value in flags.items() if name not in {"synthetic_only", "candidate_only"} and value is True]
    add("phase_boundary", phase_contract.get("Phase") == "Phase-Luna-Personality-Governance-Controlled-Implementation-v1-001" and phase_contract.get("Execution Mode") == "CONTROLLED_IMPLEMENTATION" and flags.get("synthetic_only") is True and flags.get("candidate_only") is True and not forbidden_phase_true, f"phase contract matches controlled synthetic candidate-only boundary; forbidden_true={forbidden_phase_true}")

    output_actual = {path.name for path in EVAL_DIR.iterdir() if path.is_file()} if EVAL_DIR.is_dir() else set()
    add("runner_artifact_existence", output_actual >= OUTPUT_FILES, f"missing={sorted(OUTPUT_FILES - output_actual)}")

    summary: Dict[str, Any] = {}
    case_results: List[Dict[str, Any]] = []
    trace_results: List[Dict[str, Any]] = []
    output_failures: List[str] = []
    if output_actual >= OUTPUT_FILES:
        try:
            summary = _json(EVAL_DIR / "personality_governance_result_v1.json")
            case_results = _json(EVAL_DIR / "personality_governance_case_results_v1.json")
            trace_results = _json(EVAL_DIR / "personality_governance_trace_v1.json")
        except Exception as exc:
            output_failures.append(str(exc))
    add("runner_output_parse", not output_failures, str(output_failures) if output_failures else "runner output artifacts parsed")

    case_ids = {item.get("scenario_id") for item in case_results if isinstance(item, dict)}
    trace_ids = {item.get("scenario_id") for item in trace_results if isinstance(item, dict)}
    add("runner_artifact_scenario_coverage", summary.get("scenario_count") == 36 and case_ids == EXPECTED_SCENARIOS and trace_ids == EXPECTED_SCENARIOS, f"summary={summary.get('scenario_count')} missing_cases={sorted(EXPECTED_SCENARIOS - case_ids)} missing_traces={sorted(EXPECTED_SCENARIOS - trace_ids)}")
    add("all_case_checks", len(case_results) == 36 and all(item.get("all_checks_passed") is True and all(item.get("checks", {}).values()) for item in case_results), "all P01-P36 case checks are true")
    add("candidate_flags_and_profile_boundary", all(item.get("actual", {}).get("candidate_only") is True and item.get("actual", {}).get("activated") is False and item.get("actual", {}).get("persisted") is False and item.get("actual", {}).get("truth_declared") is False for item in case_results), "runner cases preserve candidate-only flags and do not activate traits")
    add("semantic_compression_deferred", summary.get("semantic_compression_status") == "DEFERRED_TO_EMOTION_ENGINE" and summary.get("semantic_compression_execution") is False and summary.get("affective_memory_compression") is False and summary.get("emotion_memory_summary_generation") is False and summary.get("personality_memory_semantic_fusion") is False, "runner summary preserves deferred compression boundary")
    add("summary_negative_guards", summary.get("synthetic_only") is True and summary.get("candidate_only") is True and all(value is False for key, value in summary.get("negative_guards", {}).items() if key not in {"synthetic_only", "candidate_only"}), "runner summary exposes frozen negative guards")
    add("trace_reverse_lookup", len(trace_results) == 36 and all(item.get("reverse_locatable") is True and item.get("provenance_grants_authority") is False for item in trace_results), "all traces are reverse-locatable without authority transfer")
    add("contradiction_counterexample_retention", all(any(item.get("scenario_id") == sid and (item.get("contradiction_refs") or item.get("counterexample_refs")) for item in trace_results) for sid in {"P06", "P07", "P23"}), "counterexample and contradiction refs remain in trace output")
    add("lineage_retention", all(any(item.get("scenario_id") == sid and any(item.get("lineage", {}).get(key) for key in keys) for item in trace_results) for sid, keys in {"P24": ["revision_refs"], "P25": ["supersession_refs"], "P26": ["revocation_refs"], "P27": ["expiration_refs"]}.items()), "revision/supersession/revocation/expiration traces remain locatable")
    add("sensitivity_coverage", all(any(item.get("scenario_id") == sid and item.get("expected", {}).get("sensitivity") == sensitivity for item in case_results) for sid, sensitivity in {"P28": "HIGH_SENSITIVITY", "P29": "DO_NOT_TRANSFER", "P35": "DO_NOT_GENERALIZE"}.items()), "sensitivity boundary scenarios are represented")
    add("emotion_interface_coverage", all(any(item.get("scenario_id") == sid and item.get("expected", {}).get("emotion_bridge") is True for item in case_results) for sid in {"P17", "P18", "P19", "P34"}), "Emotion-to-Personality candidate interface scenarios are represented")

    failures = [item["name"] for item in checks if not item["passed"]]
    all_passed = not failures
    return {
        "CHECKS": {item["name"]: ("pass" if item["passed"] else "fail") for item in checks},
        "FAILED_CHECKS": failures,
        "PASSED_CHECK_COUNT": sum(1 for item in checks if item["passed"]),
        "FAILED_CHECK_COUNT": len(failures),
        "BLOCKER_COUNT": len(failures),
        "FINAL_DECISION": "PERSONALITY_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY_FOR_CHATGPT_AUDIT" if all_passed else "PERSONALITY_GOVERNANCE_CONTROLLED_IMPLEMENTATION_BLOCKED",
        "NEXT": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if all_passed else "LUNA_PERSONALITY_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION",
        "DETAILS": [{"name": item["name"], "detail": item["detail"]} for item in checks],
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
