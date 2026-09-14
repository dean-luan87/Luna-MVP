# -*- coding: utf-8 -*-
"""Verify Field State Reducer controlled dryrun v1 (phase verifier)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_DIR = REPO_ROOT / "capabilities" / "midplatform" / "core" / "field_state_reducer"
TOOLS_DIR = REPO_ROOT / "tools" / "evaluation" / "midplatform"
DOC_DIR = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "luna_field_state_reducer_controlled_dryrun_v1"
)

EXPECTED_FINAL_DECISION = "LUNA_FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_GO"
EXPECTED_NEXT = (
    "Phase-Luna-Field-State-Reducer-Behavior-Policy-Technical-Planning-v1-001"
)
EXPECTED_FAILURE_DECISION = "LUNA_FIELD_STATE_REDUCER_CONTROLLED_DRYRUN_BLOCKED"
EXPECTED_FAILURE_NEXT = "REMEDIATE_FIELD_STATE_REDUCER_CONTROLLED_DRYRUN"

REQUIRED_FILES = [
    CORE_DIR / "field_state_reducer_controlled_dryrun_cases_v1.py",
    CORE_DIR / "field_state_reducer_controlled_dryrun_types_v1.py",
    TOOLS_DIR / "run_field_state_reducer_controlled_dryrun_v1.py",
    TOOLS_DIR / "verify_field_state_reducer_controlled_dryrun_result_v1.py",
    DOC_DIR / "field_state_reducer_controlled_dryrun_v1.md",
    DOC_DIR / "field_state_reducer_controlled_dryrun_case_registry_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_contract_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_expected_results_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_determinism_contract_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_negative_guards_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_test_strategy_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_summary_v1.json",
    DOC_DIR / "verify_field_state_reducer_controlled_dryrun_v1.py",
]

JSON_FILES = [
    DOC_DIR / "field_state_reducer_controlled_dryrun_case_registry_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_contract_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_expected_results_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_determinism_contract_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_negative_guards_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_test_strategy_v1.json",
    DOC_DIR / "field_state_reducer_controlled_dryrun_summary_v1.json",
]

PY_FILES = [
    CORE_DIR / "field_state_reducer_controlled_dryrun_cases_v1.py",
    CORE_DIR / "field_state_reducer_controlled_dryrun_types_v1.py",
    TOOLS_DIR / "run_field_state_reducer_controlled_dryrun_v1.py",
    TOOLS_DIR / "verify_field_state_reducer_controlled_dryrun_result_v1.py",
]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _import_module(path: Path) -> Tuple[Any, str]:
    module_name = "luna_dryrun_verify_" + "_".join(
        path.relative_to(REPO_ROOT).with_suffix("").parts
    )
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None, "spec_or_loader_none"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover
        sys.modules.pop(module_name, None)
        return None, str(exc)
    return module, "ok"


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

    loaded_modules: Dict[str, Any] = {}
    import_failures: List[str] = []
    for p in PY_FILES:
        m, msg = _import_module(p)
        if m is None:
            import_failures.append(f"{p.name}:{msg}")
        else:
            loaded_modules[p.name] = m
    add(
        "all_python_files_importable",
        len(import_failures) == 0,
        ";".join(import_failures) if import_failures else "ok",
    )

    dryrun_types = loaded_modules.get(
        "field_state_reducer_controlled_dryrun_types_v1.py"
    )
    dryrun_cases = loaded_modules.get(
        "field_state_reducer_controlled_dryrun_cases_v1.py"
    )
    add(
        "dryrun_types_complete",
        bool(dryrun_types)
        and all(
            hasattr(dryrun_types, n)
            for n in (
                "FieldStateReducerDryRunCaseV1",
                "FieldStateReducerDryRunCaseResultV1",
                "FieldStateReducerDryRunReportV1",
                "FieldStateReducerDeterminismComparisonV1",
                "FieldStateReducerBoundaryObservationV1",
            )
        ),
    )

    case_registry = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_case_registry_v1.json"
    )
    contract = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_contract_v1.json"
    )
    expected = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_expected_results_v1.json"
    )
    determinism = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_determinism_contract_v1.json"
    )
    guards = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_negative_guards_v1.json"
    )
    strategy = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_test_strategy_v1.json"
    )
    summary = _load_json(
        DOC_DIR / "field_state_reducer_controlled_dryrun_summary_v1.json"
    )

    cases = case_registry.get("cases", [])
    expected_cases = expected.get("cases", [])
    case_ids = {c.get("case_id") for c in cases}
    positive_cases = [c for c in cases if c.get("category") == "positive"]
    negative_cases = [c for c in cases if c.get("category") == "negative"]

    add("case_registry_complete_16", len(cases) == 16)
    add("positive_case_count_exact_6", len(positive_cases) == 6)
    add("negative_case_count_exact_10", len(negative_cases) == 10)
    add("baseline_case_exists", "baseline_all_fixtures_case" in case_ids)
    add(
        "repeated_identical_input_case_exists",
        "repeated_identical_input_case" in case_ids,
    )
    add("reversed_input_order_case_exists", "reversed_input_order_case" in case_ids)
    add("single_event_case_exists", "single_event_case" in case_ids)
    add("conflict_fixture_case_exists", "conflict_fixture_case" in case_ids)
    add("overlay_fixture_case_exists", "overlay_fixture_case" in case_ids)
    add(
        "non_admitted_rejection_case_exists",
        "non_admitted_event_rejection_case" in case_ids,
    )
    add(
        "raw_observation_rejection_case_exists",
        "raw_observation_rejection_case" in case_ids,
    )
    add(
        "missing_temporal_snapshot_case_exists",
        "missing_temporal_snapshot_case" in case_ids,
    )
    add(
        "missing_version_snapshot_case_exists",
        "missing_version_snapshot_case" in case_ids,
    )
    add("unstable_event_id_case_exists", "unstable_event_id_case" in case_ids)
    add(
        "direct_mutation_request_case_exists",
        "direct_mutation_request_case" in case_ids,
    )
    add(
        "provider_recall_request_case_exists",
        "provider_recall_request_case" in case_ids,
    )
    add(
        "external_lookup_request_case_exists",
        "external_lookup_request_case" in case_ids,
    )
    add("action_trigger_request_case_exists", "action_trigger_request_case" in case_ids)
    add("event_mutation_guard_case_exists", "event_mutation_guard_case" in case_ids)

    add(
        "dryrun_runner_exists",
        (TOOLS_DIR / "run_field_state_reducer_controlled_dryrun_v1.py").exists(),
    )
    add(
        "result_verifier_exists",
        (
            TOOLS_DIR / "verify_field_state_reducer_controlled_dryrun_result_v1.py"
        ).exists(),
    )

    add("synthetic_fixture_only_true", contract.get("synthetic_fixture_only") is True)

    fixture_module = _import_module(CORE_DIR / "field_state_reducer_fixture_v1.py")[0]
    fixture_registry = (
        getattr(fixture_module, "FIELD_STATE_REDUCER_FIXTURES_V1", tuple())
        if fixture_module
        else tuple()
    )
    fixture_map = {
        str(e.get("event_type", "")): e for e in fixture_registry if isinstance(e, dict)
    }
    add(
        "positive_cases_admitted_only",
        all(
            all(
                fixture_map.get(ref, {}).get("admitted") is True
                for ref in case.get("fixture_refs", [])
            )
            for case in positive_cases
        ),
    )
    add(
        "negative_cases_use_copy_only",
        contract.get("negative_case_mutation_uses_copy_only") is True,
    )
    add(
        "real_event_allowed_all_false",
        all(c.get("real_event_allowed") is False for c in cases),
    )

    add("real_reduction_allowed_false", contract.get("real_reduction_allowed") is False)
    add(
        "active_state_creation_allowed_false",
        contract.get("active_state_creation_allowed") is False,
    )
    add("state_mutation_allowed_false", contract.get("state_mutation_allowed") is False)
    add(
        "fixture_mutation_allowed_false",
        contract.get("input_fixture_mutation_allowed") is False,
    )
    add(
        "deterministic_replay_required_true",
        contract.get("deterministic_replay_required") is True,
    )

    add(
        "same_input_same_snapshot_same_result_true",
        determinism.get("same_input_same_snapshot_same_result") is True,
    )
    add(
        "reversed_input_order_not_authoritative_true",
        determinism.get("input_list_order_not_final_order_authority") is True,
    )
    add(
        "stable_event_id_tie_breaker_required_true",
        determinism.get("stable_event_id_tie_breaker_required") is True,
    )

    required_compare_fields = {
        "ordered_event_ids",
        "reduction_decision",
        "resulting_state",
        "state_change_type",
        "replay_key",
        "accepted_event_ids",
        "rejected_event_ids",
        "ignored_event_ids",
        "conflict_ids",
        "state_mutation_executed",
        "runtime_execution",
    }
    add(
        "deterministic_comparison_fields_complete",
        required_compare_fields.issubset(set(determinism.get("comparison_fields", []))),
    )
    excluded_required = {
        "created_at",
        "reducer_run_id",
        "process_id",
        "memory_address",
        "wall_clock_duration",
    }
    add(
        "nondeterministic_fields_excluded_or_fixed",
        excluded_required.issubset(
            set(determinism.get("excluded_or_fixed_fields", []))
        ),
    )

    add("expected_results_complete_16", len(expected_cases) == 16)

    positive_expected_ok = True
    negative_expected_ok = True
    negative_error_codes = set()
    for row in expected_cases:
        cid = row.get("case_id")
        if cid in {c.get("case_id") for c in positive_cases}:
            if not (
                row.get("validation_passed") is True
                and row.get("reduction_decision") == "skeleton_no_state_change"
                and row.get("resulting_state") is None
                and row.get("state_mutation_executed") is False
                and row.get("runtime_execution") is False
            ):
                positive_expected_ok = False
        if cid in {c.get("case_id") for c in negative_cases}:
            if not (
                row.get("validation_passed") is False
                and row.get("skeleton_called") is False
                and isinstance(row.get("structured_error_code"), str)
                and row.get("state_mutation_executed") is False
                and row.get("runtime_execution") is False
            ):
                negative_expected_ok = False
            if isinstance(row.get("structured_error_code"), str):
                negative_error_codes.add(row.get("structured_error_code"))
    add("positive_expected_placeholder_complete", positive_expected_ok)
    add("negative_expected_errors_complete", negative_expected_ok)
    required_negative_codes = {
        "non_admitted_event_not_allowed",
        "raw_observation_not_allowed",
        "missing_temporal_snapshot",
        "missing_version_snapshot",
        "unstable_event_order",
        "direct_state_mutation_forbidden",
        "provider_recall_forbidden",
        "external_lookup_forbidden",
        "action_trigger_forbidden",
    }
    add(
        "structured_error_codes_exact",
        required_negative_codes.issubset(negative_error_codes),
    )

    add("trace_validation_required", strategy.get("trace_validation_required") is True)
    add(
        "replay_key_stability_required",
        strategy.get("replay_key_stability_required") is True,
    )
    add(
        "fixture_immutability_required",
        strategy.get("fixture_immutability_required") is True,
    )

    gv = guards.get("guards", {})
    add("no_database", gv.get("no_database") is True)
    add("no_scheduler", gv.get("no_scheduler") is True)
    add("no_message_queue", gv.get("no_message_queue") is True)
    add("no_event_consumer", gv.get("no_event_consumer") is True)
    add("no_runtime_loop", gv.get("no_runtime_loop") is True)
    add("no_provider_recall", gv.get("no_provider_recall") is True)
    add("no_external_lookup", gv.get("no_external_lookup") is True)
    add("no_model_call", gv.get("no_model_call") is True)
    add("no_action_trigger", gv.get("no_action_trigger") is True)
    add("no_training", gv.get("no_training") is True)
    add("no_migration", gv.get("no_migration") is True)
    add("no_production_execution", gv.get("no_production_execution") is True)
    add(
        "no_previous_phase_semantic_rewrite",
        gv.get("no_previous_phase_semantic_rewrite") is True,
    )

    add("negative_guards_complete", guards.get("negative_guards_complete") is True)
    add("test_strategy_complete", strategy.get("test_strategy_complete") is True)

    add(
        "summary_counts_exact",
        summary.get("positive_case_count") == 6
        and summary.get("negative_case_count") == 10
        and summary.get("total_case_count") == 16,
    )
    add("dryrun_only_true", summary.get("dryrun_only") is True)
    add(
        "controlled_skeleton_reused_true",
        summary.get("controlled_skeleton_reused") is True,
    )
    add(
        "synthetic_fixture_only_summary_true",
        summary.get("synthetic_fixture_only") is True,
    )
    add(
        "real_reduction_implemented_false",
        summary.get("real_reduction_implemented") is False,
    )
    add(
        "real_reduction_executed_false", summary.get("real_reduction_executed") is False
    )
    add("active_state_created_false", summary.get("active_state_created") is False)
    add(
        "state_mutation_executed_false", summary.get("state_mutation_executed") is False
    )
    add(
        "fixture_mutation_executed_false",
        summary.get("fixture_mutation_executed") is False,
    )
    add("runtime_implemented_false", summary.get("runtime_implemented") is False)
    add("runtime_executed_false", summary.get("runtime_executed") is False)
    add("blocker_count_zero", summary.get("blocker_count") == 0)
    add(
        "final_decision_exact_match",
        summary.get("final_decision") == EXPECTED_FINAL_DECISION,
    )
    add("next_exact_match", summary.get("recommended_next_phase") == EXPECTED_NEXT)

    failed = [c for c in checks if not c["passed"]]
    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(failed)
    blocker_count = failed_count

    final_decision = (
        EXPECTED_FINAL_DECISION if blocker_count == 0 else EXPECTED_FAILURE_DECISION
    )
    next_value = EXPECTED_NEXT if blocker_count == 0 else EXPECTED_FAILURE_NEXT

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
    print(passed_count)
    print("FAILED_CHECK_COUNT")
    print(failed_count)
    print("BLOCKER_COUNT")
    print(blocker_count)
    print("FINAL_DECISION")
    print(final_decision)
    print("NEXT")
    print(next_value)

    return 0 if blocker_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
