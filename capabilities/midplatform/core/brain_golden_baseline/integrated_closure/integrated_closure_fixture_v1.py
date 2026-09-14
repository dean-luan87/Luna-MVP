"""Governance-only closure scenarios."""

from __future__ import annotations

from typing import Callable, Dict

from .integrated_closure_governance_v1 import (
    REQUIRED_SUITE_IDS,
    ROUTE_MATRIX,
    _continuity_checks,
    _empty_evidence,
    evaluate_freeze_candidate,
    load_baseline_snapshot,
)
from .integrated_closure_types_v1 import RegressionEvidenceRecordV1


def _verified_records() -> Dict[str, RegressionEvidenceRecordV1]:
    snapshot = load_baseline_snapshot()
    records = _empty_evidence(snapshot)
    for suite_id, record in records.items():
        expected = record.expected_scenario_count
        observed = None if isinstance(expected, str) else expected
        records[suite_id] = RegressionEvidenceRecordV1(
            suite_id=record.suite_id,
            runner_ref=record.runner_ref,
            verifier_ref=record.verifier_ref,
            expected_scenario_count=expected,
            observed_scenario_count=observed,
            all_cases_passed=True,
            failed_case_ids=(),
            blocker_count=0,
            verification_status="VERIFIED",
            artifact_ref=f"user-terminal-artifact:{suite_id}",
            verified_by_user_terminal=True,
            evidence_basis="explicit_fixture_for_freeze_rule_case",
            runner_stdout_observed=None if isinstance(expected, str) else True,
            coverage_mode="B3_SUBSCOPE" if isinstance(expected, str) else "FULL_SUITE",
            subscope_refs=("B3-16", "B3-17", "B3-18", "B3-19", "B3-20", "B3-26") if isinstance(expected, str) else (),
        )
    return records


def build_cases() -> Dict[str, Callable[[], bool]]:
    snapshot = load_baseline_snapshot()
    continuity = _continuity_checks(snapshot)
    return {
        "CL-01": lambda: continuity["phase_membership_complete"],
        "CL-02": lambda: continuity["required_regression_suites_indexed"],
        "CL-03": lambda: ROUTE_MATRIX[0]["edge_id"] == "S3_TO_B1" and ROUTE_MATRIX[0]["direct_owner_bypass"] is False,
        "CL-04": lambda: ROUTE_MATRIX[1]["edge_id"] == "B1_TO_B2" and ROUTE_MATRIX[1]["direct_owner_bypass"] is False,
        "CL-05": lambda: ROUTE_MATRIX[2]["edge_id"] == "B2_TO_B3" and ROUTE_MATRIX[2]["direct_owner_bypass"] is False,
        "CL-06": lambda: ROUTE_MATRIX[3]["edge_id"] == "B3_TO_B4" and ROUTE_MATRIX[3]["direct_owner_bypass"] is False,
        "CL-07": lambda: ROUTE_MATRIX[4]["edge_id"] == "B4_TO_BASELINE_FEEDBACK" and ROUTE_MATRIX[4]["direct_owner_bypass"] is False and continuity["feedback_loop_continuity"],
        "CL-08": lambda: continuity["owner_continuity"],
        "CL-09": lambda: continuity["mutation_continuity"],
        "CL-10": lambda: continuity["candidate_truth_continuity"],
        "CL-11": lambda: continuity["trace_provenance_continuity"],
        "CL-12": lambda: continuity["real_synthetic_continuity"],
        "CL-13": lambda: continuity["negative_guard_continuity"],
        "CL-14": lambda: snapshot.regression_index.get("execution_policy") == "B5 indexes suites; it does not execute them",
        "CL-15": lambda: evaluate_freeze_candidate(_empty_evidence(snapshot), snapshot=snapshot).state == "NOT_READY",
        "CL-16": lambda: _failed_suite_blocks_freeze(snapshot),
        "CL-17": lambda: _blocker_blocks_freeze(snapshot),
        "CL-18": lambda: evaluate_freeze_candidate(_verified_records(), snapshot=snapshot).state == "READY_TO_FREEZE",
        "CL-19": lambda: evaluate_freeze_candidate(_verified_records(), snapshot=snapshot).manifest_state_mutated is False,
        "CL-20": lambda: snapshot.manifest.get("manifest_does_not_duplicate_contracts") is True and continuity["cross_phase_contract_continuity"],
    }


def _failed_suite_blocks_freeze(snapshot: object) -> bool:
    records = _verified_records()
    first = records[REQUIRED_SUITE_IDS[0]]
    records[REQUIRED_SUITE_IDS[0]] = RegressionEvidenceRecordV1(
        suite_id=first.suite_id,
        runner_ref=first.runner_ref,
        verifier_ref=first.verifier_ref,
        expected_scenario_count=first.expected_scenario_count,
        observed_scenario_count=first.observed_scenario_count,
        all_cases_passed=False,
        failed_case_ids=("CONTROLLED_FAILURE",),
        blocker_count=0,
        verification_status="VERIFIED",
        artifact_ref=first.artifact_ref,
        verified_by_user_terminal=True,
    )
    return evaluate_freeze_candidate(records, snapshot=snapshot).state == "NOT_READY"


def _blocker_blocks_freeze(snapshot: object) -> bool:
    records = _verified_records()
    first = records[REQUIRED_SUITE_IDS[0]]
    records[REQUIRED_SUITE_IDS[0]] = RegressionEvidenceRecordV1(
        suite_id=first.suite_id,
        runner_ref=first.runner_ref,
        verifier_ref=first.verifier_ref,
        expected_scenario_count=first.expected_scenario_count,
        observed_scenario_count=first.observed_scenario_count,
        all_cases_passed=True,
        failed_case_ids=(),
        blocker_count=1,
        verification_status="VERIFIED",
        artifact_ref=first.artifact_ref,
        verified_by_user_terminal=True,
    )
    return evaluate_freeze_candidate(records, snapshot=snapshot).state == "NOT_READY"
