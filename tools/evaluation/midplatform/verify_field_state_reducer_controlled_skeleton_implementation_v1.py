# -*- coding: utf-8 -*-
"""Verify Field State Reducer controlled skeleton implementation v1."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
CORE_DIR = REPO_ROOT / "capabilities" / "midplatform" / "core" / "field_state_reducer"
DOC_DIR = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "luna_field_state_reducer_controlled_skeleton_implementation_v1"
)
RUNNER_FILE = (
    REPO_ROOT
    / "tools"
    / "evaluation"
    / "midplatform"
    / "run_field_state_reducer_controlled_skeleton_v1.py"
)

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

EXPECTED_FINAL_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION_GO"
)
EXPECTED_NEXT = "Phase-Luna-Field-State-Reducer-Controlled-DryRun-v1-001"

REQUIRED_FILES = [
    CORE_DIR / "field_state_reducer_types_v1.py",
    CORE_DIR / "field_state_reducer_trace_types_v1.py",
    CORE_DIR / "field_state_reducer_error_types_v1.py",
    CORE_DIR / "field_state_reducer_protocol_v1.py",
    CORE_DIR / "field_state_reducer_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_static_validators_v1.py",
    CORE_DIR / "field_state_reducer_policy_registry_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_transition_registry_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_fixture_v1.py",
    RUNNER_FILE,
    DOC_DIR / "field_state_reducer_controlled_skeleton_implementation_v1.md",
    DOC_DIR / "field_state_reducer_planning_to_code_mapping_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_contract_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_test_strategy_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_negative_guards_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_summary_v1.json",
    REPO_ROOT
    / "tools"
    / "evaluation"
    / "midplatform"
    / "verify_field_state_reducer_controlled_skeleton_implementation_v1.py",
]

JSON_FILES = [
    DOC_DIR / "field_state_reducer_planning_to_code_mapping_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_contract_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_test_strategy_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_negative_guards_v1.json",
    DOC_DIR / "field_state_reducer_skeleton_summary_v1.json",
]

PY_FILES = [
    CORE_DIR / "field_state_reducer_types_v1.py",
    CORE_DIR / "field_state_reducer_trace_types_v1.py",
    CORE_DIR / "field_state_reducer_error_types_v1.py",
    CORE_DIR / "field_state_reducer_protocol_v1.py",
    CORE_DIR / "field_state_reducer_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_static_validators_v1.py",
    CORE_DIR / "field_state_reducer_policy_registry_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_transition_registry_skeleton_v1.py",
    CORE_DIR / "field_state_reducer_fixture_v1.py",
    RUNNER_FILE,
]


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _importable(path: Path) -> Tuple[bool, str]:
    module_name = "luna_verify_dyn_" + "_".join(
        path.relative_to(REPO_ROOT).with_suffix("").parts
    )
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            return False, "spec_or_loader_none"
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return True, "ok"
    except Exception as exc:  # pragma: no cover
        sys.modules.pop(module_name, None)
        return False, str(exc)


def _load_module(path: Path) -> Tuple[Any, str]:
    module_name = "luna_verify_loaded_" + "_".join(
        path.relative_to(REPO_ROOT).with_suffix("").parts
    )
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None, "spec_or_loader_none"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module, "ok"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_all(container: List[str], expected: List[str]) -> bool:
    c = set(container)
    return all(i in c for i in expected)


def _fixture_field(event_obj: Any, field_name: str) -> Any:
    if isinstance(event_obj, dict):
        return event_obj.get(field_name)
    if hasattr(event_obj, field_name):
        return getattr(event_obj, field_name)
    return None


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [str(p) for p in REQUIRED_FILES if not p.exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        ",".join(missing) if missing else "ok",
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

    import_failures: List[str] = []
    loaded_modules: Dict[str, Any] = {}
    for p in PY_FILES:
        ok, msg = _importable(p)
        if not ok:
            import_failures.append(f"{p.name}:{msg}")
            continue
        module, load_msg = _load_module(p)
        if module is None:
            import_failures.append(f"{p.name}:{load_msg}")
            continue
        loaded_modules[p.name] = module
    add(
        "all_required_python_files_importable",
        len(import_failures) == 0,
        ";".join(import_failures) if import_failures else "ok",
    )

    if missing or invalid_json:
        failed = [c for c in checks if not c["passed"]]
        print("CHECKS")
        for c in checks:
            print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
        print("FAILED_CHECKS")
        for c in failed:
            print(f"- {c['name']}: {c['detail']}")
        print("PASSED_CHECK_COUNT")
        print(sum(1 for c in checks if c["passed"]))
        print("FAILED_CHECK_COUNT")
        print(len(failed))
        print("BLOCKER_COUNT")
        print(len(failed))
        print("FINAL_DECISION")
        print("LUNA_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED")
        print("NEXT")
        print("REMEDIATE_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION")
        return 1

    types_text = _read_text(CORE_DIR / "field_state_reducer_types_v1.py")
    trace_text = _read_text(CORE_DIR / "field_state_reducer_trace_types_v1.py")
    error_text = _read_text(CORE_DIR / "field_state_reducer_error_types_v1.py")
    protocol_text = _read_text(CORE_DIR / "field_state_reducer_protocol_v1.py")
    skeleton_text = _read_text(CORE_DIR / "field_state_reducer_skeleton_v1.py")
    validators_text = _read_text(
        CORE_DIR / "field_state_reducer_static_validators_v1.py"
    )
    policy_text = _read_text(
        CORE_DIR / "field_state_reducer_policy_registry_skeleton_v1.py"
    )
    transition_text = _read_text(
        CORE_DIR / "field_state_reducer_transition_registry_skeleton_v1.py"
    )
    fixture_text = _read_text(CORE_DIR / "field_state_reducer_fixture_v1.py")
    runner_text = _read_text(RUNNER_FILE)

    mapping = _load_json(
        DOC_DIR / "field_state_reducer_planning_to_code_mapping_v1.json"
    )
    contract = _load_json(DOC_DIR / "field_state_reducer_skeleton_contract_v1.json")
    test_strategy = _load_json(
        DOC_DIR / "field_state_reducer_skeleton_test_strategy_v1.json"
    )
    guards = _load_json(
        DOC_DIR / "field_state_reducer_skeleton_negative_guards_v1.json"
    )
    summary = _load_json(DOC_DIR / "field_state_reducer_skeleton_summary_v1.json")

    types_module = loaded_modules.get("field_state_reducer_types_v1.py")
    reducer_types_expected = [
        "FieldStateStatusV1",
        "FieldStateTypeV1",
        "TemporalValidityStatusV1",
        "ReductionPolicyTypeV1",
        "ReductionDecisionTypeV1",
        "StateChangeTypeV1",
        "FieldStateReducerInputV1",
        "FieldStateV1",
        "FieldStateReducerOutputV1",
        "FieldStateReducerConfigSnapshotV1",
        "FieldStateReducerVersionSnapshotV1",
    ]
    add(
        "reducer_types_complete",
        bool(types_module)
        and all(hasattr(types_module, name) for name in reducer_types_expected),
    )
    trace_module = loaded_modules.get("field_state_reducer_trace_types_v1.py")
    trace_types_expected = [
        "FieldStateReducerTraceV1",
        "FieldStateReducerDecisionStepV1",
        "FieldStateReducerConflictRefV1",
        "FieldStateReducerReplayKeyV1",
        "FieldStateReducerProvenanceRefV1",
    ]
    add(
        "trace_types_complete",
        bool(trace_module)
        and all(hasattr(trace_module, name) for name in trace_types_expected),
    )

    error_tokens = [
        "invalid_reducer_input",
        "raw_observation_not_allowed",
        "non_admitted_event_not_allowed",
        "missing_temporal_snapshot",
        "missing_version_snapshot",
        "unstable_event_order",
        "direct_state_mutation_forbidden",
        "provider_recall_forbidden",
        "external_lookup_forbidden",
        "action_trigger_forbidden",
        "event_mutation_forbidden",
        "runtime_execution_forbidden",
        "database_access_forbidden",
        "scheduler_access_forbidden",
        "unsupported_reduction_policy",
        "unresolved_conflict_preserved",
    ]
    add(
        "structured_error_namespace_complete",
        all(t in error_text for t in error_tokens)
        and "ERROR_NAMESPACE_V1" in error_text,
    )

    add(
        "reducer_protocol_methods_complete",
        all(
            k in protocol_text
            for k in [
                "validate_input",
                "order_events",
                "reduce",
                "build_trace",
                "build_replay_key",
            ]
        ),
    )
    add("skeleton_class_exists", "class FieldStateReducerSkeletonV1" in skeleton_text)
    add(
        "reducer_single_mutation_authority_true",
        "reducer_is_single_mutation_authority = True" in skeleton_text,
    )
    add("skeleton_only_true", "skeleton_only = True" in skeleton_text)
    add("runtime_implemented_false", "runtime_implemented = False" in skeleton_text)
    add("production_enabled_false", "production_enabled = False" in skeleton_text)
    add(
        "database_access_allowed_false",
        "database_access_allowed = False" in skeleton_text,
    )
    add(
        "scheduler_access_allowed_false",
        "scheduler_access_allowed = False" in skeleton_text,
    )
    add(
        "provider_recall_allowed_false",
        "provider_recall_allowed = False" in skeleton_text,
    )
    add(
        "external_lookup_allowed_false",
        "external_lookup_allowed = False" in skeleton_text,
    )
    add(
        "action_trigger_allowed_false",
        "action_trigger_allowed = False" in skeleton_text,
    )
    add(
        "direct_state_write_allowed_false",
        "direct_state_write_allowed = False" in skeleton_text,
    )
    add(
        "event_mutation_allowed_false",
        "event_mutation_allowed = False" in skeleton_text,
    )

    add(
        "admitted_event_validator_exists",
        "validate_admitted_events_only" in validators_text,
    )
    add(
        "raw_observation_rejection_exists",
        "validate_no_raw_observation" in validators_text,
    )
    add(
        "temporal_snapshot_validator_exists",
        "validate_temporal_snapshot_present" in validators_text,
    )
    add(
        "version_snapshot_validator_exists",
        "validate_version_snapshot_present" in validators_text,
    )
    add(
        "stable_event_order_validator_exists",
        "validate_stable_event_ids" in validators_text,
    )

    policies = [
        "latest_valid_event",
        "highest_confidence_valid_event",
        "multi_event_consensus",
        "negative_event_override",
        "revocation_override",
        "expiration_degrade",
        "temporary_overlay_separation",
        "conflict_preservation",
        "insufficient_evidence_unresolved",
        "explicit_owner_override_candidate",
        "no_state_change",
    ]
    add("policy_registry_complete", all(p in policy_text for p in policies))
    add(
        "all_policies_implemented_false",
        policy_text.count('"implemented": False') == 11,
    )
    add(
        "all_policies_runtime_callable_false",
        policy_text.count('"runtime_callable": False') == 11,
    )
    add(
        "fact_promotion_allowed_all_false",
        policy_text.count('"fact_promotion_allowed": False') == 11,
    )

    add(
        "revoked_to_active_false",
        '"revoked_to_active_allowed": False' in transition_text,
    )
    add(
        "expired_to_active_without_new_event_false",
        '"expired_to_active_without_new_event_allowed": False' in transition_text,
    )
    add(
        "suspended_to_active_without_refresh_false",
        '"suspended_to_active_without_refresh_allowed": False' in transition_text,
    )
    add(
        "superseded_to_active_false",
        '"superseded_to_active_allowed": False' in transition_text,
    )
    add(
        "conflicted_to_active_without_resolution_false",
        '"conflicted_to_active_without_resolution_allowed": False' in transition_text,
    )
    add(
        "unresolved_to_active_without_evidence_false",
        '"unresolved_to_active_without_sufficient_evidence_allowed": False'
        in transition_text,
    )

    fixture_events = [
        "road_accessible_event",
        "construction_notice_event",
        "barrier_visual_event",
        "road_blocked_event",
        "temporary_passage_event",
        "conflict_event",
        "overlay_expired_event",
        "refresh_evidence_event",
        "road_reopened_event",
    ]
    fixture_module = loaded_modules.get("field_state_reducer_fixture_v1.py")
    fixture_registry = (
        getattr(fixture_module, "FIELD_STATE_REDUCER_FIXTURES_V1", tuple())
        if fixture_module
        else tuple()
    )
    fixture_registry_list = (
        list(fixture_registry.values())
        if isinstance(fixture_registry, dict)
        else list(fixture_registry)
    )
    fixture_event_types = {
        str(_fixture_field(event_obj, "event_type") or "")
        for event_obj in fixture_registry_list
    }
    add(
        "xiaobeimen_fixture_complete",
        all(name in fixture_event_types for name in fixture_events),
    )
    add(
        "all_fixtures_synthetic_true",
        len(fixture_registry_list) >= 9
        and all(
            isinstance(_fixture_field(event_obj, "synthetic"), bool)
            and _fixture_field(event_obj, "synthetic") is True
            for event_obj in fixture_registry_list
        ),
    )
    add(
        "all_fixtures_admitted_true",
        len(fixture_registry_list) >= 9
        and all(
            isinstance(_fixture_field(event_obj, "admitted"), bool)
            and _fixture_field(event_obj, "admitted") is True
            for event_obj in fixture_registry_list
        ),
    )
    add(
        "production_data_all_false",
        len(fixture_registry_list) >= 9
        and all(
            isinstance(_fixture_field(event_obj, "production_data"), bool)
            and _fixture_field(event_obj, "production_data") is False
            for event_obj in fixture_registry_list
        ),
    )

    add(
        "controlled_runner_exists",
        "def run_field_state_reducer_controlled_skeleton_v1" in runner_text,
    )
    add(
        "controlled_runner_uses_static_fixture_only",
        "build_xiaobeimen_construction_closure_fixture_v1" in runner_text,
    )
    add("controlled_runner_no_database", "database" not in runner_text.lower())
    add(
        "controlled_runner_no_provider",
        "provider" not in runner_text.lower() or "provider_recall" in runner_text,
    )
    add("controlled_runner_no_model", "model" not in runner_text.lower())
    add(
        "controlled_runner_no_action",
        "action" not in runner_text.lower() or "no_action_trigger" in runner_text,
    )

    add(
        "skeleton_output_state_mutation_executed_false",
        "state_mutation_executed=False" in skeleton_text,
    )
    add(
        "skeleton_output_runtime_execution_false",
        "runtime_executed=False" in skeleton_text,
    )
    add("resulting_active_state_not_created", "resulting_state=None" in skeleton_text)
    add(
        "deterministic_placeholder_supported",
        "deterministic_placeholder_supported" in skeleton_text,
    )
    add(
        "provenance_trace_complete",
        all(
            k in trace_text
            for k in [
                "reducer_run_id",
                "ordered_event_ids",
                "resulting_state_hash",
                "replay_key",
            ]
        ),
    )

    add(
        "planning_to_code_mapping_complete",
        mapping.get("planning_to_code_mapping_complete") is True
        and len(mapping.get("mappings", [])) >= 15,
    )
    add(
        "planning_assets_modified_false",
        all(
            item.get("planning_asset_modified") is False
            for item in mapping.get("mappings", [])
        ),
    )
    contract_keys = [
        "skeleton_only",
        "controlled_execution_only",
        "real_reduction_allowed",
        "state_mutation_allowed",
        "resulting_active_state_allowed",
        "provider_recall_allowed",
        "external_lookup_allowed",
        "action_trigger_allowed",
        "database_access_allowed",
        "scheduler_access_allowed",
        "model_call_allowed",
        "production_data_allowed",
        "synthetic_fixture_only",
        "deterministic_placeholder_required",
    ]
    add("skeleton_contract_complete", all(k in contract for k in contract_keys))
    add("test_strategy_complete", test_strategy.get("test_strategy_complete") is True)
    add("negative_guards_complete", guards.get("negative_guards_complete") is True)

    guard_values = guards.get("guards", {})
    add("no_message_queue", guard_values.get("no_message_queue") is True)
    add("no_event_consumer", guard_values.get("no_event_consumer") is True)
    add("no_runtime_loop", guard_values.get("no_runtime_loop") is True)
    add("no_training", guard_values.get("no_training") is True)
    add("no_migration", guard_values.get("no_migration") is True)
    add("no_production_execution", guard_values.get("no_production_data") is True)

    add("candidate_only_true", summary.get("candidate_only") is True)
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
        "LUNA_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION_GO"
        if blocker_count == 0
        else "LUNA_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED"
    )
    next_value = (
        "Phase-Luna-Field-State-Reducer-Controlled-DryRun-v1-001"
        if blocker_count == 0
        else "REMEDIATE_FIELD_STATE_REDUCER_CONTROLLED_SKELETON_IMPLEMENTATION"
    )

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
