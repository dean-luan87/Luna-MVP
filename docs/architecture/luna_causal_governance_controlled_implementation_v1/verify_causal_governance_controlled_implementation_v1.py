#!/usr/bin/env python3
"""Final phase verifier for Causal Governance controlled implementation v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable


DOC_BASE = Path(__file__).resolve().parent
READY = "LUNA_CAUSAL_GOVERNANCE_CONTROLLED_IMPLEMENTATION_READY"
REMEDIATION = "LUNA_CAUSAL_GOVERNANCE_CONTROLLED_IMPLEMENTATION_REMEDIATION_REQUIRED"

CODE_FILES = {
    "__init__.py",
    "causal_error_types_v1.py",
    "causal_core_types_v1.py",
    "causal_state_types_v1.py",
    "causal_evidence_types_v1.py",
    "causal_confounder_types_v1.py",
    "causal_counterfactual_types_v1.py",
    "causal_trace_types_v1.py",
    "causal_handoff_types_v1.py",
    "causal_io_types_v1.py",
    "causal_registry_v1.py",
    "causal_ownership_guard_v1.py",
    "causal_governance_protocol_v1.py",
    "causal_static_validators_v1.py",
    "causal_governance_fixture_v1.py",
    "causal_governance_engine_v1.py",
    "run_causal_governance_controlled_implementation_v1.py",
}

DOC_FILES = {
    "causal_governance_controlled_implementation_overview_v1.md",
    "causal_governance_controlled_execution_contract_v1.json",
    "causal_governance_negative_guards_v1.json",
    "causal_governance_planning_to_code_mapping_v1.json",
    "causal_governance_implementation_summary_v1.md",
    "causal_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
    "verify_causal_governance_controlled_implementation_v1.py",
}

JSON_FILES = {
    "causal_governance_controlled_execution_contract_v1.json",
    "causal_governance_negative_guards_v1.json",
    "causal_governance_planning_to_code_mapping_v1.json",
    "causal_governance_controlled_change_manifest_v1.json",
    "phase_contract.json",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        target = candidate / "capabilities/midplatform/core/causal_governance"
        if target.is_dir():
            return candidate
    raise RuntimeError("repository_root_with_causal_governance_not_found")


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: list[str], failures: list[str]) -> None:
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


def _flatten_sources(case_result: Dict[str, Any]) -> bool:
    return (
        bool(case_result.get("supporting_evidence_refs"))
        and bool(case_result.get("state"))
        and bool(case_result.get("uncertainty"))
        and bool(case_result.get("provenance"))
    )


def _find_case(items: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    for item in items:
        if item.get("case_id") == case_id:
            return item
    return {}


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

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

    code_dir = repo_root / "capabilities/midplatform/core/causal_governance"
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

    contract = docs.get("causal_governance_controlled_execution_contract_v1.json", {})
    check(contract.get("canonical_owner") == "Causal Governance", "canonical_owner")
    aliases = contract.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_authority",
    )
    check(contract.get("candidate_only") is True, "candidate_only_contract")
    check(contract.get("runtime_execution") is False, "no_runtime_execution")
    check(contract.get("decision_output") is False, "no_decision_output")
    check(contract.get("action_output") is False, "no_action_output")
    check(contract.get("task_output") is False, "no_task_output")

    mapping = docs.get("causal_governance_planning_to_code_mapping_v1.json", {})
    mapped = {Path(item).name for item in mapping.get("all_code_assets", [])}
    check(mapped == CODE_FILES, "planning_to_code_completeness")
    check(
        mapping.get("planning_assets_modified") is False, "planning_assets_unmodified"
    )

    manifest = docs.get("causal_governance_controlled_change_manifest_v1.json", {})
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

    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

        from capabilities.midplatform.core.causal_governance.causal_governance_engine_v1 import (
            CausalGovernanceEngineV1,
        )
        from capabilities.midplatform.core.causal_governance.causal_governance_fixture_v1 import (
            get_causal_synthetic_fixtures_v1,
        )
        from capabilities.midplatform.core.causal_governance.causal_static_validators_v1 import (
            validate_handoff,
            validate_hypothesis_candidates,
            validate_no_runtime_side_effects,
            validate_trace_completeness,
        )

        engine = CausalGovernanceEngineV1()
        fixtures = get_causal_synthetic_fixtures_v1()
        check(len(fixtures) == 12, "scenario_fixture_count_12")

        case_results: list[Dict[str, Any]] = []
        for case in fixtures:
            output = engine.run_case(case.request)
            checks_for_case = {
                "state_expected": output.hypothesis_candidates[0].state_candidate
                == case.expected_state,
                "hypothesis_count_expected": len(output.hypothesis_candidates)
                == case.expected_hypothesis_count,
                "trace_complete": validate_trace_completeness(output),
                "handoff_valid": validate_handoff(output.handoff_candidate),
                "hypothesis_valid": validate_hypothesis_candidates(
                    output.hypothesis_candidates
                ),
                "no_runtime_effect": validate_no_runtime_side_effects(output),
                "evidence_present": bool(output.evidence_relations),
                "provenance_present": bool(output.trace_candidate.provenance),
                "uncertainty_present": bool(output.trace_candidate.uncertainty),
            }
            case_results.append(
                {
                    "case_id": case.case_id,
                    "state": output.hypothesis_candidates[0].state_candidate,
                    "hypothesis_count": len(output.hypothesis_candidates),
                    "supporting_evidence_refs": list(
                        output.handoff_candidate.supporting_evidence_refs
                    ),
                    "uncertainty": list(output.handoff_candidate.uncertainty),
                    "provenance": list(output.handoff_candidate.provenance),
                    "checks": checks_for_case,
                    "all_passed": all(checks_for_case.values()),
                    "counterfactual_count": len(output.counterfactual_candidates),
                    "confounder_count": len(output.confounder_candidates),
                }
            )

        check(
            all(item["all_passed"] for item in case_results), "scenario_checks_all_pass"
        )

        c01 = _find_case(case_results, "C01_TEMPORAL_PRECEDENCE_NO_CAUSALITY")
        check(c01.get("state") != "SUPPORTED", "temporal_guard_behavior")

        c02 = _find_case(case_results, "C02_STRONG_ASSOCIATION_UNRESOLVED_CAUSE")
        check(c02.get("state") == "CONTESTED", "correlation_guard_behavior")

        c03 = _find_case(case_results, "C03_TWO_COMPETING_HYPOTHESES")
        check(c03.get("hypothesis_count", 0) >= 2, "multi_hypothesis_behavior")

        c04 = _find_case(case_results, "C04_THIRD_VARIABLE_CONFOUNDER")
        check(c04.get("confounder_count", 0) >= 1, "confounder_behavior")

        c11 = _find_case(case_results, "C11_COUNTERFACTUAL_CANDIDATE")
        check(c11.get("counterfactual_count", 0) >= 1, "counterfactual_behavior")

        c06 = _find_case(case_results, "C06_OPPOSING_EVIDENCE")
        check(c06.get("state") == "CONTESTED", "evidence_opposition_behavior")

        c07 = _find_case(case_results, "C07_HYPOTHESIS_REVISION")
        c08 = _find_case(case_results, "C08_REVOKED_EVIDENCE")
        check(c07.get("state") == "REVISED", "revision_behavior")
        check(c08.get("state") == "REVOKED", "revocation_behavior")

        c12 = _find_case(case_results, "C12_CAUSAL_TO_DECISION_CANDIDATE_HANDOFF")
        check(_flatten_sources(c12), "candidate_handoff_payload_completeness")

    except Exception:
        check(False, "in_process_scenario_verification")

    # If runner outputs exist, verify key result fields too.
    eval_dir = repo_root / "_eval_out/causal_governance_controlled_implementation_v1"
    case_file = eval_dir / "causal_governance_case_results_v1.json"
    if case_file.is_file():
        try:
            payload = json.loads(case_file.read_text(encoding="utf-8"))
            check(
                isinstance(payload, list) and len(payload) == 12,
                "runner_case_file_coverage",
            )
            r_c01 = _find_case(payload, "C01_TEMPORAL_PRECEDENCE_NO_CAUSALITY")
            r_c12 = _find_case(payload, "C12_CAUSAL_TO_DECISION_CANDIDATE_HANDOFF")
            check(
                r_c01.get("state") == "INSUFFICIENT_EVIDENCE", "runner_case_c01_state"
            )
            check(bool(r_c12.get("provenance")), "runner_case_c12_provenance")
        except Exception:
            check(False, "runner_case_file_parse")
    else:
        check(False, "runner_case_file_exists")

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
