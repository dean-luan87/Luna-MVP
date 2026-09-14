#!/usr/bin/env python3
"""Final phase verifier for Decision Governance controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


DOC_BASE = Path(__file__).resolve().parent
READY = "LUNA_DECISION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = "LUNA_DECISION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"

CODE_FILES = {
    "__init__.py",
    "decision_registry_v1.py",
    "decision_error_types_v1.py",
    "decision_state_types_v1.py",
    "decision_core_types_v1.py",
    "decision_trace_types_v1.py",
    "decision_handoff_types_v1.py",
    "decision_io_types_v1.py",
    "decision_governance_protocol_v1.py",
    "decision_ownership_guard_v1.py",
    "decision_static_validators_v1.py",
    "decision_governance_fixture_v1.py",
    "decision_governance_engine_v1.py",
    "run_decision_governance_controlled_implementation_v1.py",
}

DOC_FILES = {
    "decision_governance_controlled_implementation_overview_v1.md",
    "decision_governance_controlled_execution_contract_v1.json",
    "decision_governance_negative_guards_v1.json",
    "decision_governance_planning_to_code_mapping_v1.json",
    "decision_governance_implementation_summary_v1.md",
    "decision_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
    "verify_decision_governance_controlled_implementation_v1.py",
}

JSON_FILES = {
    "decision_governance_controlled_execution_contract_v1.json",
    "decision_governance_negative_guards_v1.json",
    "decision_governance_planning_to_code_mapping_v1.json",
    "decision_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
}

REQUIRED_SCENARIO_IDS = {
    "D01_LOW_RISK_SINGLE_CANDIDATE",
    "D02_TWO_CANDIDATE_COEXISTENCE",
    "D03_HIGH_UTILITY_PERMISSION_DENIED",
    "D04_HIGH_UTILITY_SAFETY_VETO",
    "D05_CAUSAL_UNCERTAINTY_DEFER",
    "D06_EVIDENCE_GAP_REQUEST_MORE",
    "D07_NO_ACCEPTABLE_OPTION_ABSTAIN",
    "D08_REVERSIBLE_CANDIDATE",
    "D09_IRREVERSIBLE_CONFIRMATION_REQUIRED",
    "D10_RESOURCE_CONSTRAINT_LOWER_COST",
    "D11_ROLE_CONSTRAINT_ELIGIBILITY_SHIFT",
    "D12_INTENT_PREFERENCE_NO_OVERRULE",
    "D13_COMPETING_CAUSAL_HYPOTHESES",
    "D14_DECISION_TO_ACTION_TASK_CANDIDATE_ONLY",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (candidate / "capabilities/midplatform/core/decision_governance").is_dir():
            return candidate
    raise RuntimeError("repository_root_with_decision_governance_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: List[str], failures: List[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(READY if not failures else "BLOCKED_BY_VERIFIER_FAILURE")

    print("READINESS")
    print(READY if not failures else REMEDIATION)

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


def _find_case(items: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    for item in items:
        if item.get("case_id") == case_id:
            return item
    return {}


def main() -> int:
    checks: List[str] = []
    failures: List[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    try:
        repo_root = find_repo_root()
        check(True, "repo_root_resolved")
    except RuntimeError:
        repo_root = Path.cwd().resolve()
        check(False, "repo_root_resolved")

    code_dir = repo_root / "capabilities/midplatform/core/decision_governance"
    actual_code = {item.name for item in code_dir.iterdir() if item.is_file()}
    actual_doc = {item.name for item in DOC_BASE.iterdir() if item.is_file()}
    check(actual_code == CODE_FILES, "exact_code_file_set")
    check(actual_doc == DOC_FILES, "exact_doc_file_set")

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            docs[name] = load_json(DOC_BASE / name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    for name in sorted(CODE_FILES):
        try:
            ast.parse((code_dir / name).read_text(encoding="utf-8"))
            check(True, f"ast_parse:{name}")
        except (OSError, SyntaxError):
            check(False, f"ast_parse:{name}")

    contract = docs.get("decision_governance_controlled_execution_contract_v1.json", {})
    check(contract.get("canonical_owner") == "Decision Governance", "canonical_owner")
    aliases = contract.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_authority",
    )
    check(
        all(item.get("authority") is False for item in aliases),
        "legacy_alias_no_parallel_authority",
    )
    check(contract.get("candidate_only") is True, "candidate_only_contract")
    check(contract.get("runtime_execution") is False, "no_runtime_execution")
    check(contract.get("database_write") is False, "no_database_write")
    check(contract.get("decision_output") is False, "no_decision_execution")
    check(contract.get("action_output") is False, "no_action_execution")
    check(contract.get("task_output") is False, "no_task_creation")

    mapping = docs.get("decision_governance_planning_to_code_mapping_v1.json", {})
    mapped = {Path(item).name for item in mapping.get("all_code_assets", [])}
    check(mapped == CODE_FILES, "planning_to_code_completeness")
    check(
        mapping.get("planning_assets_modified") is False,
        "planning_assets_unmodified",
    )
    check(
        mapping.get("parallel_implementation_created") is False,
        "no_parallel_decision_owner",
    )

    manifest = docs.get("decision_governance_controlled_change_manifest_v1.json", {})
    created_code = {Path(item).name for item in manifest.get("created_code_files", [])}
    created_doc = {
        Path(item).name for item in manifest.get("created_documentation_files", [])
    }
    check(created_code == CODE_FILES, "manifest_code_set")
    check(created_doc == DOC_FILES, "manifest_doc_set")
    check(
        manifest.get("modified_existing_files") == [], "no_existing_asset_modification"
    )
    check(manifest.get("runtime_executed") is False, "manifest_runtime_false")
    check(manifest.get("database_accessed") is False, "manifest_database_false")

    guards = docs.get("decision_governance_negative_guards_v1.json", {})
    guard_set = set(guards.get("negative_guards", []))
    required_guards = {
        "intent != decision",
        "causal != decision",
        "correlation != decision authority",
        "model suggestion != decision authority",
        "memory preference != decision authority",
        "emotion != decision authority",
        "utility != permission",
        "risk != safety authority",
        "preferred candidate != executable action",
        "selected candidate != task",
        "decision layer != action executor",
        "decision layer != task creator",
        "no permission bypass",
        "no safety bypass",
        "no fabricated confirmation",
        "no runtime side effect",
        "no database write",
        "no source mutation",
    }
    check(required_guards <= guard_set, "negative_guard_completeness")

    phase = docs.get("phase_contract.json", {})
    check(
        phase.get("phase")
        == "Phase-Luna-Decision-Governance-Controlled-Implementation-v1-001",
        "phase_id",
    )
    check(
        phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_waiting",
    )

    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

        from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
            DecisionGovernanceEngineV1,
        )
        from capabilities.midplatform.core.decision_governance.decision_governance_fixture_v1 import (
            get_decision_synthetic_fixtures_v1,
        )
        from capabilities.midplatform.core.decision_governance.decision_static_validators_v1 import (
            validate_handoff,
            validate_negative_guard_flags,
            validate_no_runtime_side_effects,
            validate_trace_completeness,
        )

        engine = DecisionGovernanceEngineV1()
        fixtures = get_decision_synthetic_fixtures_v1()
        check(len(fixtures) == 14, "scenario_fixture_count_14")
        check(
            REQUIRED_SCENARIO_IDS == {item.case_id for item in fixtures},
            "scenario_id_coverage_14",
        )

        case_results: List[Dict[str, Any]] = []
        for case in fixtures:
            output = engine.run_case(case.request)
            checks_for_case = {
                "state_expected": output.state == case.expected_state,
                "outcome_expected": output.outcome_kind == case.expected_outcome_kind,
                "trace_complete": validate_trace_completeness(output),
                "handoff_valid": validate_handoff(output.handoff_candidate),
                "no_runtime": validate_no_runtime_side_effects(output),
                "negative_guards": validate_negative_guard_flags(),
            }
            selected_option = None
            for candidate in output.decision_candidates:
                if (
                    candidate.decision_candidate_id
                    == output.selection_candidate.selected_candidate_ref
                ):
                    selected_option = candidate.option_id
                    break

            case_results.append(
                {
                    "case_id": case.case_id,
                    "state": output.state,
                    "outcome_kind": output.outcome_kind,
                    "selected_option_id": selected_option,
                    "handoff_eligible": output.handoff_candidate.execution_eligibility_candidate,
                    "confirmation_requirement": output.selection_candidate.confirmation_requirement,
                    "checks": checks_for_case,
                    "all_passed": all(checks_for_case.values()),
                }
            )

        check(
            all(item["all_passed"] for item in case_results),
            "all_fixture_expectations_pass",
        )

        d02 = _find_case(case_results, "D02_TWO_CANDIDATE_COEXISTENCE")
        check(d02.get("state") == "CONTESTED", "multi_candidate_behavior")

        d03 = _find_case(case_results, "D03_HIGH_UTILITY_PERMISSION_DENIED")
        check(d03.get("state") == "CONSTRAINED", "permission_veto_behavior")

        d04 = _find_case(case_results, "D04_HIGH_UTILITY_SAFETY_VETO")
        check(d04.get("state") == "CONSTRAINED", "safety_veto_behavior")

        d05 = _find_case(case_results, "D05_CAUSAL_UNCERTAINTY_DEFER")
        check(d05.get("outcome_kind") == "DEFER", "defer_behavior")

        d06 = _find_case(case_results, "D06_EVIDENCE_GAP_REQUEST_MORE")
        check(
            d06.get("outcome_kind") == "REQUEST_MORE_EVIDENCE",
            "request_more_evidence_behavior",
        )

        d07 = _find_case(case_results, "D07_NO_ACCEPTABLE_OPTION_ABSTAIN")
        check(d07.get("outcome_kind") == "ABSTAIN", "abstain_behavior")

        d09 = _find_case(case_results, "D09_IRREVERSIBLE_CONFIRMATION_REQUIRED")
        check(
            d09.get("state") == "NEEDS_CONFIRMATION"
            and d09.get("confirmation_requirement") == "CONFIRMATION_REQUIRED",
            "irreversible_confirmation_behavior",
        )

        d10 = _find_case(case_results, "D10_RESOURCE_CONSTRAINT_LOWER_COST")
        check(
            d10.get("selected_option_id") == "opt_d10_low",
            "resource_degradation_behavior",
        )

        d11 = _find_case(case_results, "D11_ROLE_CONSTRAINT_ELIGIBILITY_SHIFT")
        check(d11.get("state") == "CONSTRAINED", "role_eligibility_behavior")

        d12 = _find_case(case_results, "D12_INTENT_PREFERENCE_NO_OVERRULE")
        check(
            d12.get("selected_option_id") == "opt_d12_safe",
            "intent_influence_only_behavior",
        )

        d13 = _find_case(case_results, "D13_COMPETING_CAUSAL_HYPOTHESES")
        check(d13.get("state") == "CONTESTED", "causal_contested_behavior")

        d14 = _find_case(case_results, "D14_DECISION_TO_ACTION_TASK_CANDIDATE_ONLY")
        check(d14.get("handoff_eligible") is True, "candidate_only_handoff_behavior")

    except Exception:
        check(False, "in_process_behavior_verification")

    eval_dir = repo_root / "_eval_out/decision_governance_controlled_implementation_v1"
    case_file = eval_dir / "decision_governance_case_results_v1.json"
    if case_file.is_file():
        try:
            payload = json.loads(case_file.read_text(encoding="utf-8"))
            check(
                isinstance(payload, list) and len(payload) == 14,
                "runner_case_file_coverage",
            )
            r_d03 = _find_case(payload, "D03_HIGH_UTILITY_PERMISSION_DENIED")
            r_d04 = _find_case(payload, "D04_HIGH_UTILITY_SAFETY_VETO")
            r_d14 = _find_case(payload, "D14_DECISION_TO_ACTION_TASK_CANDIDATE_ONLY")
            check(r_d03.get("state") == "CONSTRAINED", "runner_case_d03_permission")
            check(r_d04.get("state") == "CONSTRAINED", "runner_case_d04_safety")
            check(
                r_d14.get("handoff_eligibility") is True,
                "runner_case_d14_handoff",
            )
            check(bool(r_d14.get("provenance")), "runner_case_provenance")
        except Exception:
            check(False, "runner_case_file_parse")
    else:
        check(False, "runner_case_file_exists")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
