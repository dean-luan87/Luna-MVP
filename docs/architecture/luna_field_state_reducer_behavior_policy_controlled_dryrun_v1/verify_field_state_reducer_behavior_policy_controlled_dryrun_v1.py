from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = Path(__file__).resolve().parent
CODE_DIR = (
    REPO_ROOT / "capabilities/midplatform/core/field_state_reducer/behavior_policy"
)
TOOLS_DIR = REPO_ROOT / "tools/evaluation/midplatform"

EXPECTED_FINAL_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_GO"
)
EXPECTED_NEXT = "Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Policy-Evaluation-Technical-Planning-v1-001"
EXPECTED_FAILURE_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN_BLOCKED"
)
EXPECTED_FAILURE_NEXT = (
    "REMEDIATE_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_DRYRUN"
)

REQUIRED_FILES = [
    CODE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_types_v1.py",
    CODE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_cases_v1.py",
    TOOLS_DIR / "run_field_state_reducer_behavior_policy_controlled_dryrun_v1.py",
    TOOLS_DIR
    / "verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1.py",
    BASE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_v1.md",
    BASE_DIR
    / "field_state_reducer_behavior_policy_controlled_dryrun_case_registry_v1.json",
    BASE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_contract_v1.json",
    BASE_DIR
    / "field_state_reducer_behavior_policy_controlled_dryrun_expected_results_v1.json",
    BASE_DIR
    / "field_state_reducer_behavior_policy_controlled_dryrun_determinism_contract_v1.json",
    BASE_DIR
    / "field_state_reducer_behavior_policy_controlled_dryrun_negative_guards_v1.json",
    BASE_DIR
    / "field_state_reducer_behavior_policy_controlled_dryrun_test_strategy_v1.json",
    BASE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_summary_v1.json",
    BASE_DIR / "verify_field_state_reducer_behavior_policy_controlled_dryrun_v1.py",
]

JSON_FILES = [p for p in REQUIRED_FILES if p.suffix == ".json"]

PY_FILES = [
    CODE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_types_v1.py",
    CODE_DIR / "field_state_reducer_behavior_policy_controlled_dryrun_cases_v1.py",
    TOOLS_DIR / "run_field_state_reducer_behavior_policy_controlled_dryrun_v1.py",
    TOOLS_DIR
    / "verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1.py",
]

PY_MODULES = [
    "capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_controlled_dryrun_types_v1",
    "capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_controlled_dryrun_cases_v1",
    "tools.evaluation.midplatform.run_field_state_reducer_behavior_policy_controlled_dryrun_v1",
    "tools.evaluation.midplatform.verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1",
]

REQUIRED_CASE_IDS = {
    "registry_loading_case",
    "baseline_placeholder_chain_case",
    "repeated_identical_input_case",
    "reversed_candidate_order_case",
    "conflict_preservation_candidate_case",
    "temporary_overlay_candidate_case",
    "owner_correction_candidate_case",
    "insufficient_evidence_no_state_change_case",
    "unknown_policy_id_rejection_case",
    "unknown_state_type_rejection_case",
    "missing_policy_registry_snapshot_case",
    "missing_eligibility_snapshot_case",
    "missing_precedence_snapshot_case",
    "missing_composition_snapshot_case",
    "runtime_request_rejection_case",
    "direct_state_write_rejection_case",
    "fact_promotion_rejection_case",
    "action_trigger_rejection_case",
    "provider_recall_rejection_case",
    "external_lookup_rejection_case",
}

NEGATIVE_ERROR_CODES = {
    "unknown_policy_id",
    "unknown_state_type",
    "missing_policy_registry_snapshot",
    "missing_eligibility_matrix_snapshot",
    "missing_precedence_snapshot",
    "missing_composition_snapshot",
    "runtime_execution_forbidden",
    "direct_state_write_forbidden",
    "fact_promotion_forbidden",
    "action_trigger_forbidden",
    "provider_recall_forbidden",
    "external_lookup_forbidden",
}


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _ensure_repo_root_on_syspath() -> None:
    root = str(REPO_ROOT)
    sys.path[:] = [p for p in sys.path if p != root]
    sys.path.insert(0, root)


def _import_module(module_name: str) -> Tuple[bool, str]:
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        return False, str(exc)
    return True, "ok"


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [str(p) for p in REQUIRED_FILES if not p.exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        ";".join(missing) if missing else "ok",
    )

    invalid_json: List[str] = []
    for p in JSON_FILES:
        try:
            _load_json(p)
        except Exception as exc:
            invalid_json.append(f"{p.name}:{exc}")
    add(
        "all_json_valid",
        len(invalid_json) == 0,
        ";".join(invalid_json) if invalid_json else "ok",
    )

    _ensure_repo_root_on_syspath()

    import_failures: List[str] = []
    for module_name in PY_MODULES:
        ok, msg = _import_module(module_name)
        if not ok:
            import_failures.append(f"{module_name}:{msg}")
    add(
        "all_python_files_importable",
        len(import_failures) == 0,
        ";".join(import_failures) if import_failures else "ok",
    )

    cases_json = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_case_registry_v1.json"
    )
    contract = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_contract_v1.json"
    )
    expected = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_expected_results_v1.json"
    )
    determinism = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_determinism_contract_v1.json"
    )
    guards = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_negative_guards_v1.json"
    )
    strategy = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_test_strategy_v1.json"
    )
    summary = _load_json(
        BASE_DIR
        / "field_state_reducer_behavior_policy_controlled_dryrun_summary_v1.json"
    )

    case_rows = list(cases_json.get("cases", []))
    case_ids = {str(r.get("case_id", "")) for r in case_rows}
    positive_rows = [r for r in case_rows if r.get("category") == "positive"]
    negative_rows = [r for r in case_rows if r.get("category") == "negative"]

    add(
        "dryrun_types_complete",
        (
            CODE_DIR
            / "field_state_reducer_behavior_policy_controlled_dryrun_types_v1.py"
        ).exists(),
    )
    add("case_registry_complete_20", len(case_rows) == 20)
    add("positive_case_count_exact_8", len(positive_rows) == 8)
    add("negative_case_count_exact_12", len(negative_rows) == 12)
    add("all_required_case_ids_exist", case_ids == REQUIRED_CASE_IDS)
    add(
        "runner_exists",
        (
            TOOLS_DIR
            / "run_field_state_reducer_behavior_policy_controlled_dryrun_v1.py"
        ).exists(),
    )
    add(
        "result_verifier_exists",
        (
            TOOLS_DIR
            / "verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1.py"
        ).exists(),
    )

    add("dryrun_only_true", contract.get("dryrun_only") is True)
    add("synthetic_fixture_only_true", contract.get("synthetic_fixture_only") is True)
    add("deep_copy_required_true", contract.get("deep_copy_required") is True)
    add(
        "fixture_mutation_allowed_false",
        contract.get("fixture_mutation_allowed") is False,
    )
    add(
        "registry_mutation_allowed_false",
        contract.get("registry_mutation_allowed") is False,
    )
    add(
        "real_policy_selection_allowed_false",
        contract.get("real_policy_selection_allowed") is False,
    )
    add(
        "real_policy_execution_allowed_false",
        contract.get("real_policy_execution_allowed") is False,
    )
    add(
        "real_precedence_execution_allowed_false",
        contract.get("real_precedence_execution_allowed") is False,
    )
    add(
        "real_composition_execution_allowed_false",
        contract.get("real_composition_execution_allowed") is False,
    )
    add(
        "confidence_aggregation_allowed_false",
        contract.get("confidence_aggregation_allowed") is False,
    )
    add(
        "conflict_resolution_allowed_false",
        contract.get("conflict_resolution_allowed") is False,
    )
    add(
        "active_state_creation_allowed_false",
        contract.get("active_state_creation_allowed") is False,
    )
    add("state_mutation_allowed_false", contract.get("state_mutation_allowed") is False)
    add("fact_promotion_allowed_false", contract.get("fact_promotion_allowed") is False)
    add("action_trigger_allowed_false", contract.get("action_trigger_allowed") is False)
    add(
        "provider_recall_allowed_false",
        contract.get("provider_recall_allowed") is False,
    )
    add(
        "external_lookup_allowed_false",
        contract.get("external_lookup_allowed") is False,
    )
    add("model_call_allowed_false", contract.get("model_call_allowed") is False)
    add(
        "database_access_allowed_false",
        contract.get("database_access_allowed") is False,
    )
    add(
        "runtime_execution_allowed_false",
        contract.get("runtime_execution_allowed") is False,
    )
    add(
        "deterministic_replay_required_true",
        contract.get("deterministic_replay_required") is True,
    )
    add(
        "placeholder_decision_required_true",
        contract.get("placeholder_decision_required") is True,
    )

    expected_rows = list(expected.get("cases", []))
    expected_positive = [r for r in expected_rows if r.get("category") == "positive"]
    expected_negative = [r for r in expected_rows if r.get("category") == "negative"]

    add("expected_results_complete_20", len(expected_rows) == 20)
    add("positive_expected_results_complete", len(expected_positive) == 8)
    add("negative_expected_errors_complete", len(expected_negative) == 12)
    add(
        "structured_error_codes_exact",
        {str(r.get("structured_error_code", "")) for r in expected_negative}
        == NEGATIVE_ERROR_CODES,
    )

    add("determinism_contract_complete", bool(determinism))
    add(
        "same_input_same_snapshot_same_result_true",
        determinism.get("same_input_same_snapshot_same_result") is True,
    )
    add(
        "candidate_order_not_authoritative_true",
        determinism.get("input_candidate_order_not_final_authority") is True,
    )
    add(
        "stable_policy_id_tie_breaker_true",
        determinism.get("stable_policy_id_tie_breaker_required") is True,
    )
    add("deterministic_fields_complete", len(determinism.get("core_fields", [])) >= 14)
    add(
        "nondeterministic_fields_excluded",
        len(determinism.get("excluded_or_fixed_fields", [])) >= 5,
    )

    add(
        "fixture_immutability_required",
        guards.get("guards", {}).get("no_fixture_mutation") is True,
    )
    add(
        "registry_immutability_required",
        guards.get("guards", {}).get("no_registry_mutation") is True,
    )
    add(
        "trace_validation_required",
        "Trace completeness" in set(strategy.get("checks", [])),
    )
    add(
        "replay_key_stability_required",
        "Replay key stability" in set(strategy.get("checks", [])),
    )

    add("negative_guards_complete", len(guards.get("guards", {})) >= 25)
    add("test_strategy_complete", len(strategy.get("checks", [])) >= 30)

    add(
        "summary_counts_exact",
        summary.get("total_case_count") == 20
        and summary.get("positive_case_count") == 8
        and summary.get("negative_case_count") == 12,
    )
    add("summary_dryrun_only_true", summary.get("dryrun_only") is True)
    add(
        "summary_controlled_skeleton_reused_true",
        summary.get("controlled_skeleton_reused") is True,
    )
    add(
        "summary_synthetic_fixture_only_true",
        summary.get("synthetic_fixture_only") is True,
    )
    add(
        "summary_real_policy_selection_false",
        summary.get("real_policy_selection_executed") is False,
    )
    add(
        "summary_real_policy_execution_false",
        summary.get("real_policy_execution_executed") is False,
    )
    add(
        "summary_real_precedence_false",
        summary.get("real_precedence_execution") is False,
    )
    add(
        "summary_real_composition_false",
        summary.get("real_composition_execution") is False,
    )
    add(
        "summary_confidence_aggregation_false",
        summary.get("confidence_aggregation_executed") is False,
    )
    add(
        "summary_conflict_resolution_false",
        summary.get("conflict_resolution_executed") is False,
    )
    add(
        "summary_active_state_created_false",
        summary.get("active_state_created") is False,
    )
    add("summary_state_mutation_false", summary.get("state_mutation_executed") is False)
    add("summary_fact_promotion_false", summary.get("fact_promotion_executed") is False)
    add("summary_action_trigger_false", summary.get("action_trigger_executed") is False)
    add(
        "summary_fixture_mutation_false",
        summary.get("fixture_mutation_executed") is False,
    )
    add(
        "summary_registry_mutation_false",
        summary.get("registry_mutation_executed") is False,
    )
    add(
        "summary_runtime_implemented_false", summary.get("runtime_implemented") is False
    )
    add("summary_runtime_executed_false", summary.get("runtime_executed") is False)
    add("no_database", summary.get("database_created") is False)
    add("no_scheduler", summary.get("scheduler_created") is False)
    add("no_message_queue", summary.get("message_queue_created") is False)
    add("no_event_consumer", summary.get("event_consumer_created") is False)
    add("no_provider_recall", summary.get("provider_recall_executed") is False)
    add("no_external_lookup", summary.get("external_lookup_executed") is False)
    add("no_model_call", summary.get("model_call_executed") is False)
    add("no_training", summary.get("training_executed") is False)
    add("no_migration", summary.get("migration_executed") is False)
    add("no_production_execution", summary.get("production_execution") is False)
    add("blocker_count_zero", summary.get("blocker_count") == 0)
    add(
        "final_decision_exact_match",
        summary.get("final_decision") == EXPECTED_FINAL_DECISION,
    )
    add("next_exact_match", summary.get("recommended_next_phase") == EXPECTED_NEXT)

    failed = [c for c in checks if not c["passed"]]
    print("CHECKS")
    for c in checks:
        print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
    print("FAILED_CHECKS")
    if failed:
        for c in failed:
            print(
                f"- {c['name']}: {c['detail'] if c['detail'] else 'condition_not_met'}"
            )
    else:
        print("- NONE")
    print("PASSED_CHECK_COUNT")
    print(sum(1 for c in checks if c["passed"]))
    print("FAILED_CHECK_COUNT")
    print(len(failed))
    print("BLOCKER_COUNT")
    print(len(failed))

    if failed:
        print("FINAL_DECISION")
        print(EXPECTED_FAILURE_DECISION)
        print("NEXT")
        print(EXPECTED_FAILURE_NEXT)
        return 1

    print("FINAL_DECISION")
    print(EXPECTED_FINAL_DECISION)
    print("NEXT")
    print(EXPECTED_NEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
