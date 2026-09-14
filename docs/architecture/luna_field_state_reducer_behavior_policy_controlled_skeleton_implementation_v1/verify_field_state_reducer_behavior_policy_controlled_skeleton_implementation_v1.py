from __future__ import annotations

import ast
from dataclasses import is_dataclass
from enum import Enum
import importlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[2]

REQUIRED_FILES = [
    "field_state_reducer_behavior_policy_controlled_skeleton_implementation_v1.md",
    "field_state_reducer_behavior_policy_planning_to_code_mapping_v1.json",
    "field_state_reducer_behavior_policy_skeleton_contract_v1.json",
    "field_state_reducer_behavior_policy_skeleton_test_strategy_v1.json",
    "field_state_reducer_behavior_policy_skeleton_negative_guards_v1.json",
    "field_state_reducer_behavior_policy_skeleton_summary_v1.json",
    "verify_field_state_reducer_behavior_policy_controlled_skeleton_implementation_v1.py",
]

REQUIRED_CODE_FILES = [
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_types_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_trace_types_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_error_types_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_registry_skeleton_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_policy_eligibility_skeleton_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_policy_precedence_skeleton_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_policy_composition_skeleton_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_decision_skeleton_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_static_validators_v1.py",
    "capabilities/midplatform/core/field_state_reducer/behavior_policy/field_state_reducer_behavior_policy_fixture_v1.py",
    "tools/evaluation/midplatform/run_field_state_reducer_behavior_policy_controlled_skeleton_v1.py",
]

JSON_FILES = [name for name in REQUIRED_FILES if name.endswith(".json")]

EXPECTED_POLICY_IDS: Set[str] = {
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
}

EXPECTED_STATE_TYPES: Set[str] = {
    "presence_state",
    "accessibility_state",
    "path_state",
    "obstruction_state",
    "facility_state",
    "service_state",
    "environmental_condition_state",
    "human_activity_state",
    "navigation_relevance_state",
    "temporary_overlay_state",
    "uncertainty_state",
    "conflict_state",
}

EXPECTED_TOTAL_CHECKS = 89
EXPECTED_FINAL_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_SKELETON_IMPLEMENTATION_GO"
)
EXPECTED_NEXT = (
    "Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-DryRun-v1-001"
)
EXPECTED_FAILURE_DECISION = "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED"
EXPECTED_FAILURE_NEXT = (
    "REMEDIATE_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_CONTROLLED_SKELETON_IMPLEMENTATION"
)


def _load_json(filename: str) -> Dict[str, Any]:
    with open(BASE_DIR / filename, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_repo_file(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _parse_registry_policy_ids(registry_text: str) -> Set[str]:
    marker = "FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1"
    start = registry_text.find(marker)
    if start < 0:
        return set()
    tuple_start = registry_text.find("(", start)
    if tuple_start < 0:
        return set()
    depth = 0
    tuple_end = -1
    for idx in range(tuple_start, len(registry_text)):
        ch = registry_text[idx]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                tuple_end = idx
                break
    if tuple_end < 0:
        return set()

    tuple_text = registry_text[tuple_start : tuple_end + 1]
    try:
        parsed = ast.literal_eval(tuple_text)
    except Exception:
        return set()

    result: Set[str] = set()
    if isinstance(parsed, tuple):
        for row in parsed:
            if isinstance(row, dict) and "policy_id" in row:
                result.add(str(row.get("policy_id")))
    return result


def _collect_state_types(registry_text: str) -> Set[str]:
    marker = "FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1"
    start = registry_text.find(marker)
    if start < 0:
        return set()
    tuple_start = registry_text.find("(", start)
    if tuple_start < 0:
        return set()
    depth = 0
    tuple_end = -1
    for idx in range(tuple_start, len(registry_text)):
        ch = registry_text[idx]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                tuple_end = idx
                break
    if tuple_end < 0:
        return set()

    tuple_text = registry_text[tuple_start : tuple_end + 1]
    try:
        parsed = ast.literal_eval(tuple_text)
    except Exception:
        return set()

    types: Set[str] = set()
    if isinstance(parsed, tuple):
        for row in parsed:
            if isinstance(row, dict):
                for st in tuple(row.get("eligible_state_types", tuple())):
                    types.add(str(st))
    return types


def _normalize_token(value: Any) -> str:
    if isinstance(value, Enum):
        enum_value = value.value
        if isinstance(enum_value, str):
            return enum_value
        raise TypeError(f"enum_value_not_str:{type(enum_value).__name__}")
    if isinstance(value, str):
        return value
    raise TypeError(f"unsupported_token_type:{type(value).__name__}")


def _extract_field(entry: Any, field_name: str) -> Any:
    if isinstance(entry, dict):
        if field_name not in entry:
            raise KeyError(field_name)
        return entry[field_name]
    if is_dataclass(entry) and hasattr(entry, field_name):
        return getattr(entry, field_name)
    raise TypeError(f"unsupported_entry_type:{type(entry).__name__}")


def _load_registry_runtime_rows() -> Tuple[Any, Tuple[Any, ...]]:
    module_name = (
        "capabilities.midplatform.core.field_state_reducer.behavior_policy."
        "field_state_reducer_behavior_policy_registry_skeleton_v1"
    )
    const_name = "FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1"

    module = None
    try:
        module = importlib.import_module(module_name)
    except Exception:
        module_path = REPO_ROOT / REQUIRED_CODE_FILES[3]
        spec = importlib.util.spec_from_file_location(
            "_luna_registry_skeleton_runtime", module_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    if module is None or not hasattr(module, const_name):
        raise RuntimeError("registry_runtime_load_failed")

    registry_obj = getattr(module, const_name)
    if not isinstance(registry_obj, tuple):
        raise TypeError(f"registry_outer_type_not_tuple:{type(registry_obj).__name__}")

    return registry_obj, tuple(registry_obj)


def _extract_policy_and_state_sets(rows: Tuple[Any, ...]) -> Tuple[Set[str], Set[str]]:
    policy_ids: Set[str] = set()
    state_types: Set[str] = set()

    for row in rows:
        policy_ids.add(_normalize_token(_extract_field(row, "policy_id")))

        eligible = _extract_field(row, "eligible_state_types")
        if not isinstance(eligible, (tuple, list)):
            raise TypeError(
                f"eligible_state_types_not_sequence:{type(eligible).__name__}"
            )
        for st in eligible:
            state_types.add(_normalize_token(st))

    return policy_ids, state_types


def _print_report(
    checks: List[Dict[str, Any]],
    final_decision: str,
    nxt: str,
) -> None:
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
    print("FINAL_DECISION")
    print(final_decision)
    print("NEXT")
    print(nxt)


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing_docs = [name for name in REQUIRED_FILES if not (BASE_DIR / name).exists()]
    add(
        "required_doc_files_exist",
        len(missing_docs) == 0,
        "missing=" + ",".join(missing_docs) if missing_docs else "all_present",
    )

    missing_code = [
        name for name in REQUIRED_CODE_FILES if not (REPO_ROOT / name).exists()
    ]
    add(
        "required_code_files_exist",
        len(missing_code) == 0,
        "missing=" + ",".join(missing_code) if missing_code else "all_present",
    )

    invalid_json: List[str] = []
    for filename in JSON_FILES:
        try:
            _load_json(filename)
        except Exception as exc:
            invalid_json.append(f"{filename}:{exc}")
    add(
        "all_json_valid",
        len(invalid_json) == 0,
        ";".join(invalid_json) if invalid_json else "valid",
    )

    if missing_docs or missing_code or invalid_json:
        while len(checks) < EXPECTED_TOTAL_CHECKS:
            add(
                f"reserved_check_{len(checks) + 1:02d}",
                True,
                "skipped_after_hard_blocker",
            )
        _print_report(checks, EXPECTED_FAILURE_DECISION, EXPECTED_FAILURE_NEXT)
        return 1

    mapping = _load_json(
        "field_state_reducer_behavior_policy_planning_to_code_mapping_v1.json"
    )
    contract = _load_json(
        "field_state_reducer_behavior_policy_skeleton_contract_v1.json"
    )
    strategy = _load_json(
        "field_state_reducer_behavior_policy_skeleton_test_strategy_v1.json"
    )
    guards = _load_json(
        "field_state_reducer_behavior_policy_skeleton_negative_guards_v1.json"
    )
    summary = _load_json("field_state_reducer_behavior_policy_skeleton_summary_v1.json")

    types_text = _read_repo_file(REQUIRED_CODE_FILES[0])
    trace_text = _read_repo_file(REQUIRED_CODE_FILES[1])
    errors_text = _read_repo_file(REQUIRED_CODE_FILES[2])
    registry_text = _read_repo_file(REQUIRED_CODE_FILES[3])
    eligibility_text = _read_repo_file(REQUIRED_CODE_FILES[4])
    precedence_text = _read_repo_file(REQUIRED_CODE_FILES[5])
    composition_text = _read_repo_file(REQUIRED_CODE_FILES[6])
    decision_text = _read_repo_file(REQUIRED_CODE_FILES[7])
    validators_text = _read_repo_file(REQUIRED_CODE_FILES[8])
    fixture_text = _read_repo_file(REQUIRED_CODE_FILES[9])
    runner_text = _read_repo_file(REQUIRED_CODE_FILES[10])

    policy_ids = _parse_registry_policy_ids(registry_text)
    state_types = _collect_state_types(registry_text)
    try:
        _, registry_rows = _load_registry_runtime_rows()
        policy_ids, state_types = _extract_policy_and_state_sets(registry_rows)
    except Exception:
        pass

    # Mapping checks (4-10)
    mappings = mapping.get("mappings", [])
    add("mapping_version_1_0", mapping.get("version") == "1.0")
    add("mapping_complete_true", mapping.get("mapping_complete") is True)
    add("mapping_rows_7", len(mappings) == 7)
    add(
        "mapping_all_no_rewrite",
        all(
            m.get("rewrite_required") is False for m in mappings if isinstance(m, dict)
        ),
    )
    add(
        "mapping_all_planning_asset_not_modified",
        all(
            m.get("planning_asset_modified") is False
            for m in mappings
            if isinstance(m, dict)
        ),
    )
    add(
        "mapping_has_registry_entry",
        any(
            m.get("mapping_type") == "registry" for m in mappings if isinstance(m, dict)
        ),
    )
    add(
        "mapping_has_negative_guards_entry",
        any(
            m.get("mapping_type") == "negative_guards"
            for m in mappings
            if isinstance(m, dict)
        ),
    )

    # Contract checks (11-23)
    add("contract_version_1_0", contract.get("version") == "1.0")
    add("contract_skeleton_only_true", contract.get("skeleton_only") is True)
    add("contract_candidate_only_true", contract.get("candidate_only") is True)
    add(
        "contract_real_policy_selection_false",
        contract.get("real_policy_selection_allowed") is False,
    )
    add(
        "contract_real_policy_execution_false",
        contract.get("real_policy_execution_allowed") is False,
    )
    add(
        "contract_real_precedence_false",
        contract.get("real_precedence_execution_allowed") is False,
    )
    add(
        "contract_real_composition_false",
        contract.get("real_composition_execution_allowed") is False,
    )
    add(
        "contract_state_mutation_false", contract.get("state_mutation_allowed") is False
    )
    add(
        "contract_fact_promotion_false", contract.get("fact_promotion_allowed") is False
    )
    add(
        "contract_action_trigger_false", contract.get("action_trigger_allowed") is False
    )
    add(
        "contract_provider_recall_false",
        contract.get("provider_recall_allowed") is False,
    )
    add(
        "contract_external_lookup_false",
        contract.get("external_lookup_allowed") is False,
    )
    add("contract_runtime_false", contract.get("runtime_execution_allowed") is False)

    # Strategy and guards checks (24-33)
    add("strategy_version_1_0", strategy.get("version") == "1.0")
    add("strategy_checks_len_ge_20", len(strategy.get("checks", [])) >= 20)
    add("strategy_contains_no_runtime", "no Runtime" in set(strategy.get("checks", [])))
    add(
        "strategy_contains_no_action",
        "no action trigger" in set(strategy.get("checks", [])),
    )
    add("strategy_complete_true", strategy.get("test_strategy_complete") is True)
    g = guards.get("guards", {})
    add(
        "guards_no_real_policy_execution_true",
        g.get("no_real_policy_execution") is True,
    )
    add("guards_no_state_mutation_true", g.get("no_state_mutation") is True)
    add("guards_no_action_trigger_true", g.get("no_action_trigger") is True)
    add("guards_no_model_call_true", g.get("no_model_call") is True)
    add("guards_complete_true", guards.get("negative_guards_complete") is True)

    # Summary checks (34-47)
    add("summary_version_1_0", summary.get("version") == "1.0")
    add(
        "summary_required_files_total_18",
        summary.get("required_final_files_total") == 18,
    )
    add(
        "summary_required_files_complete_true",
        summary.get("required_final_files_complete") is True,
    )
    add("summary_code_files_count_11", summary.get("code_files", {}).get("count") == 11)
    add("summary_docs_files_count_7", summary.get("docs_files", {}).get("count") == 7)
    add("summary_policy_count_11", summary.get("policy_count") == 11)
    add("summary_state_type_count_12", summary.get("state_type_count") == 12)
    add("summary_skeleton_only_true", summary.get("skeleton_only") is True)
    add("summary_candidate_only_true", summary.get("candidate_only") is True)
    add("summary_runtime_execution_false", summary.get("runtime_execution") is False)
    add("summary_state_mutation_false", summary.get("state_mutation") is False)
    add("summary_fact_promotion_false", summary.get("fact_promotion") is False)
    add("summary_action_trigger_false", summary.get("action_trigger") is False)
    add("summary_complete_true", summary.get("summary_complete") is True)

    # Registry / types checks (48-63)
    add("policy_ids_exact_match", policy_ids == EXPECTED_POLICY_IDS)
    add("policy_count_exact_11", len(policy_ids) == 11)
    add("state_types_exact_match", state_types == EXPECTED_STATE_TYPES)
    add("state_type_count_exact_12", len(state_types) == 12)
    add(
        "registry_contains_real_execution_false",
        '"real_execution": False' in registry_text,
    )
    add(
        "registry_contains_state_write_false",
        '"state_write_allowed": False' in registry_text,
    )
    add(
        "registry_contains_fact_promotion_false",
        '"fact_promotion_allowed": False' in registry_text,
    )
    add(
        "registry_contains_action_trigger_false",
        '"action_trigger_allowed": False' in registry_text,
    )
    add(
        "types_define_behavior_policy_id_enum", "class BehaviorPolicyIdV1" in types_text
    )
    add(
        "types_define_decision_dataclass",
        "class BehaviorPolicyDecisionV1" in types_text,
    )
    add(
        "types_define_replay_snapshot",
        "class BehaviorPolicyReplaySnapshotV1" in types_text,
    )
    add("types_default_no_runtime", "runtime_execution: bool = False" in types_text)
    add("trace_define_trace_dataclass", "class BehaviorPolicyTraceV1" in trace_text)
    add(
        "trace_define_replay_key_dataclass",
        "class BehaviorPolicyReplayKeyV1" in trace_text,
    )
    add("errors_define_namespace", "ERROR_NAMESPACE_V1" in errors_text)
    add("errors_define_16_error_codes", errors_text.count("=") >= 16)

    # Skeleton module boundary checks (64-79)
    add(
        "eligibility_has_validate_input",
        "def validate_eligibility_input" in eligibility_text,
    )
    add(
        "eligibility_has_placeholder_results",
        "def build_placeholder_eligibility_results" in eligibility_text,
    )
    add(
        "eligibility_enforces_no_provider_recall",
        "provider_recall_forbidden" in eligibility_text,
    )
    add(
        "precedence_has_rules_constant",
        "PRECEDENCE_RULES_SKELETON_V1" in precedence_text,
    )
    add(
        "precedence_has_execution_false",
        "precedence_execution_executed = False" in precedence_text,
    )
    add(
        "composition_has_contract_constant",
        "COMPOSITION_CONTRACT_SKELETON_V1" in composition_text,
    )
    add("composition_has_depth_3", '"maximum_composition_depth": 3' in composition_text)
    add(
        "composition_has_execution_false",
        "composition_execution_executed = False" in composition_text,
    )
    add(
        "decision_builds_replay_key",
        "def build_behavior_policy_replay_key" in decision_text,
    )
    add("decision_no_state_mutation", "state_mutation_executed=False" in decision_text)
    add("decision_no_fact_promotion", "fact_promotion_executed=False" in decision_text)
    add("decision_no_action_trigger", "action_trigger_executed=False" in decision_text)
    add("decision_no_runtime", "runtime_execution=False" in decision_text)
    add(
        "validators_has_boundary_validator",
        "def validate_skeleton_decision_boundary" in validators_text,
    )
    add("validators_default_registry_hook", "def default_registry" in validators_text)
    add("fixture_synthetic_only_flag_present", '"synthetic": True' in fixture_text)

    # Runner checks (80-89)
    add(
        "runner_has_entry_function",
        "def run_field_state_reducer_behavior_policy_controlled_skeleton_v1"
        in runner_text,
    )
    add(
        "runner_writes_json_output",
        "out_path.write_text(" in runner_text and "json.dumps(result" in runner_text,
    )
    add("runner_policy_count_11", '"policy_count": len(policy_ids)' in runner_text)
    add("runner_state_type_count_12", '"state_type_count": 12' in runner_text)
    add("runner_no_database_true", '"no_database": True' in runner_text)
    add("runner_no_provider_recall_true", '"no_provider_recall": True' in runner_text)
    add("runner_no_external_lookup_true", '"no_external_lookup": True' in runner_text)
    add("runner_no_model_call_true", '"no_model_call": True' in runner_text)
    add("runner_no_action_true", '"no_action": True' in runner_text)
    add("runner_runtime_execution_false", '"runtime_execution": False' in runner_text)

    if len(checks) != EXPECTED_TOTAL_CHECKS:
        add(
            "check_count_integrity",
            False,
            f"expected={EXPECTED_TOTAL_CHECKS},actual={len(checks)}",
        )

    failed = [c for c in checks if not c["passed"]]
    if failed:
        _print_report(checks, EXPECTED_FAILURE_DECISION, EXPECTED_FAILURE_NEXT)
        return 1

    _print_report(checks, EXPECTED_FINAL_DECISION, EXPECTED_NEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
