#!/usr/bin/env python3
"""Result verifier for PCN controlled dryrun validation v1.

User-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


DOC_DIR = Path(__file__).resolve().parent
REPO_ROOT = DOC_DIR.parents[2]
OUT_DIR = REPO_ROOT / "_eval_out/personal_cognitive_network_controlled_dryrun_v1"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(condition: bool, name: str, checks: List[str], failures: List[str]) -> None:
    checks.append(name)
    if not condition:
        failures.append(name)


def main() -> int:
    checks: List[str] = []
    failures: List[str] = []

    summary_path = OUT_DIR / "pcn_controlled_dryrun_result_v1.json"
    cases_path = OUT_DIR / "pcn_controlled_dryrun_case_results_v1.json"
    trace_path = OUT_DIR / "pcn_controlled_dryrun_trace_v1.json"

    _check(summary_path.is_file(), "output_result_exists", checks, failures)
    _check(cases_path.is_file(), "output_cases_exists", checks, failures)
    _check(trace_path.is_file(), "output_trace_exists", checks, failures)

    if failures:
        _emit(checks, failures)
        return 1

    summary = _load_json(summary_path)
    cases = _load_json(cases_path)
    trace = _load_json(trace_path)

    expected_registry = _load_json(
        DOC_DIR / "pcn_dryrun_scenario_expectation_registry_v1.json"
    )
    output_contract = _load_json(
        DOC_DIR / "pcn_controlled_dryrun_output_contract_v1.json"
    )
    nested_contract = _load_json(
        DOC_DIR / "pcn_nested_constraint_dryrun_contract_v1.json"
    )
    interaction_contract = _load_json(
        DOC_DIR / "pcn_interaction_dryrun_validation_contract_v1.json"
    )
    resource_contract = _load_json(
        DOC_DIR / "pcn_resource_degradation_dryrun_contract_v1.json"
    )
    subjective_contract = _load_json(
        DOC_DIR / "pcn_subjective_cognition_dryrun_contract_v1.json"
    )
    clar_inheritance = _load_json(
        DOC_DIR / "pcn_dryrun_clarification_inheritance_v1.json"
    )

    _check(summary.get("case_count") == 12, "12_scenarios_executed", checks, failures)
    _check(len(cases) == 12, "case_results_12", checks, failures)

    by_case = {item.get("case_id"): item for item in cases}

    c1 = by_case.get("CASE_01_WEATHER_QUERY", {})
    e1 = c1.get("evidence", {})
    _check(
        e1.get("minimal_activation") is True,
        "weather_minimal_activation",
        checks,
        failures,
    )
    _check(
        e1.get("has_historical_reactivation") is False,
        "weather_no_historical_reactivation",
        checks,
        failures,
    )

    c2 = by_case.get("CASE_02_HOME_TEMPORARY_WORK", {})
    _check(
        "ir-temp-occ-1" in c2.get("interaction_references", []),
        "temporary_occupation_detected",
        checks,
        failures,
    )
    _check(
        c2.get("boundary_flags", {}).get("source_mutation_executed") is False,
        "temporary_occupation_no_core_mutation",
        checks,
        failures,
    )

    c3 = by_case.get("CASE_03_REPEATED_HOME_WORK", {})
    _check(
        c3.get("growth_candidates", {}).get("strengthening_candidate") is not None,
        "repeated_occupation_candidate_exists",
        checks,
        failures,
    )
    _check(
        c3.get("boundary_flags", {}).get("source_mutation_executed") is False,
        "repeated_occupation_no_auto_structural_change",
        checks,
        failures,
    )

    c4 = by_case.get("CASE_04_COLLEAGUE_AND_SPOUSE", {})
    _check(c4.get("passed") is True, "multi_relationship_coexistence", checks, failures)

    c5 = by_case.get("CASE_05_DIVORCED_BUT_COLLEAGUES", {})
    _check(
        c5.get("evidence", {}).get("historical_relation_present") is True,
        "historical_relation_preserved",
        checks,
        failures,
    )

    c6 = by_case.get("CASE_06_MEETING_REACTIVATES_HISTORY", {})
    _check(
        c6.get("evidence", {}).get("has_historical_reactivation") is True,
        "historical_reactivation_exists",
        checks,
        failures,
    )

    c7 = by_case.get("CASE_07_WORK_FIELD_RESONANCE", {})
    _check(
        c7.get("evidence", {}).get("has_resonance") is True,
        "resonance_present",
        checks,
        failures,
    )
    _check(
        c7.get("evidence", {}).get("no_causal") is True,
        "resonance_not_causal",
        checks,
        failures,
    )

    c8 = by_case.get("CASE_08_FATHER_VS_EMPLOYEE", {})
    _check(
        c8.get("evidence", {}).get("has_competition") is True,
        "competition_present",
        checks,
        failures,
    )
    _check(
        c8.get("boundary_flags", {}).get("decision_executed") is False,
        "competition_not_arbitration",
        checks,
        failures,
    )

    c9 = by_case.get("CASE_09_COUPLE_BUSINESS", {})
    e9 = c9.get("evidence", {})
    _check(e9.get("has_overlap") is True, "overlap_supported", checks, failures)
    _check(
        any(item.get("evidence", {}).get("has_coexistence") is True for item in cases),
        "coexistence_supported",
        checks,
        failures,
    )
    _check(
        e9.get("has_fusion_candidate") is True,
        "fusion_candidate_supported",
        checks,
        failures,
    )

    c10 = by_case.get("CASE_10_DORMANT_FRIEND_REACTIVATION", {})
    _check(
        c10.get("evidence", {}).get("dormant_relation_present") is True,
        "dormant_relation_present",
        checks,
        failures,
    )
    _check(
        c10.get("boundary_flags", {}).get("source_mutation_executed") is False,
        "dormant_not_deleted",
        checks,
        failures,
    )

    c11 = by_case.get("CASE_11_SUBJECTIVE_FALSE_BELIEF", {})
    e11 = c11.get("evidence", {})
    _check(
        e11.get("subjective_true") is True, "subjective_link_allowed", checks, failures
    )
    _check(
        e11.get("truth_status_not_fact") is True, "strength_not_truth", checks, failures
    )

    c12 = by_case.get("CASE_12_RESOURCE_DEGRADATION", {})
    rc = c12.get("resource_comparison", {})
    _check(
        rc.get("low_less_than_high") is True,
        "resource_low_less_high_scope",
        checks,
        failures,
    )
    _check(
        rc.get("low_no_source_mutation") is True,
        "resource_no_source_mutation",
        checks,
        failures,
    )

    all_flags_false = all(
        item.get("boundary_flags", {}).get("source_mutation_executed") is False
        and item.get("boundary_flags", {}).get("persistence_executed") is False
        and item.get("boundary_flags", {}).get("runtime_integration_executed") is False
        and item.get("boundary_flags", {}).get("causal_reasoning_executed") is False
        and item.get("boundary_flags", {}).get("intent_generation_executed") is False
        and item.get("boundary_flags", {}).get("decision_executed") is False
        and item.get("boundary_flags", {}).get("action_executed") is False
        for item in cases
    )
    _check(
        all_flags_false,
        "no_source_mutation_no_persistence_no_runtime_no_intent_no_causal_no_decision_no_action",
        checks,
        failures,
    )

    _check(
        all(
            item.get("boundary_flags", {}).get("candidate_only") is True
            for item in cases
        ),
        "candidate_only_output",
        checks,
        failures,
    )

    _check(
        len(expected_registry.get("cases", [])) == 12,
        "expectation_registry_12_cases",
        checks,
        failures,
    )
    _check(
        len(clar_inheritance.get("clarifications", [])) == 5,
        "clarification_inherited_5",
        checks,
        failures,
    )
    _check(
        all(
            item.get("resolved") is False
            for item in clar_inheritance.get("clarifications", [])
        ),
        "clarification_unresolved",
        checks,
        failures,
    )

    _check(
        all(
            r.get("source_mutation") is False
            for r in nested_contract.get("relations", [])
        ),
        "nested_constraint_no_source_mutation",
        checks,
        failures,
    )
    _check(
        interaction_contract.get("pcn_interaction_boundary", {}).get(
            "interaction_kernel_executed"
        )
        is False,
        "interaction_kernel_not_executed",
        checks,
        failures,
    )
    _check(
        interaction_contract.get("pcn_interaction_boundary", {}).get(
            "interaction_kernel_owned_by_pcn"
        )
        is False,
        "interaction_kernel_not_owned_by_pcn",
        checks,
        failures,
    )

    _check(
        resource_contract.get("required_behavior", {}).get("resource_affects_truth")
        is False,
        "resource_not_affect_truth",
        checks,
        failures,
    )
    _check(
        subjective_contract.get("rules", {}).get("causal_fact_not_generated") is True,
        "subjective_no_causal_fact",
        checks,
        failures,
    )

    _check(len(trace.get("case_traces", [])) == 12, "trace_complete", checks, failures)

    _emit(checks, failures)
    return 0 if not failures else 1


def _emit(checks: List[str], failures: List[str]) -> None:
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
    print(
        "PCN_CONTROLLED_DRYRUN_VALIDATION_PASSED"
        if not failures
        else "BLOCKED_BY_VERIFIER_FAILURE"
    )

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


if __name__ == "__main__":
    sys.exit(main())
