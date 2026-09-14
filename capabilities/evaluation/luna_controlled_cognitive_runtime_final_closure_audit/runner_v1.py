"""User-terminal runner for the final controlled-runtime closure audit.

The runner composes the already verified Full E2E runner and emits only a
transient audit report. It does not write a durable archive or invoke any
real runtime capability.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.runner_v1 import (
    build_runner_summary_v1,
)

from .contract_audit_v1 import run_static_contract_audit


PHASE = "Phase-P1-Luna-Controlled-Cognitive-Runtime-Final-Closure-Audit-v1-001"
OUTPUT_DIR = Path("_eval_out/luna_controlled_cognitive_runtime_final_closure_audit_v1")
OUTPUT_PATH = OUTPUT_DIR / "audit_report_v1.json"

NON_BLOCKING_DEBTS = (
    "Brain request semantic admission authority remains OWNER_UNRESOLVED",
    "Information Need formation/admission authority remains OWNER_UNRESOLVED",
    "Semantic Closure Acceptance authority remains OWNER_UNRESOLVED",
    "Generic Assimilation routing/consumption authority remains OWNER_UNRESOLVED",
    "Canonical Role ownership remains unresolved where not established by existing contracts",
    "Brain persistence and Emotion mutation ownership remain outside this controlled baseline",
)
DEFERRED_RUNTIME = (
    "real camera and live sensor stream",
    "real OCR/model/provider execution",
    "physical navigation and real Action execution",
    "Runtime Executor activation and external side effects",
)
HISTORICAL_ARTIFACTS = (
    "_eval_out/full_end_to_end_cognitive_logic_conformance_regression_v1/runner_summary_v1.json",
    "_eval_out/cognitive_end_to_end_controlled_integration_and_closure_v1/runner_summary_v1.json",
    "_eval_out/action_admission_safety_and_execution_boundary_closure_v1/runner_summary_v1.json",
    "_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1/synthetic_cognitive_whitebox_runner_v1.json",
    "evaluation_archive/level1_cognitive_runs",
)


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed}


def _all_false(values: Iterable[Any]) -> bool:
    return all(value is False for value in values)


def _governance_checks(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks = []
    for result in full.get("contrast_results") or ():
        proof = result.get("execution_proof") or {}
        checks.append(
            _check(
                f"cognition_owner:{result.get('contrast_id')}",
                proof.get("owner_ref") == "Cognitive State Formation Governance",
                proof.get("owner_ref"),
            )
        )
    for case in full.get("operational_source", {}).get("cases") or ():
        action = case.get("action_boundary") or {}
        candidate = action.get("action_candidate") or {}
        source_case = case.get("source_case") or {}
        task_case = source_case.get("task_case") or {}
        task = task_case.get("task_manager") or {}
        checks.extend(
            [
                _check(f"action_owner:{case.get('case_id')}", candidate.get("owner") == "Action Governance", candidate.get("owner")),
                _check(f"task_owner:{case.get('case_id')}", task.get("task_manager_owner_ref") == "Task Manager", task.get("task_manager_owner_ref")),
                _check(f"no_runtime_executor:{case.get('case_id')}", case.get("runtime_executor_invoked") is False, case.get("runtime_executor_invoked")),
            ]
        )
    return checks


def _traceability_checks(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks = []
    for result in full.get("contrast_results") or ():
        semantics = result.get("input_semantics") or {}
        proof = result.get("execution_proof") or {}
        required = (
            result.get("gateway_admission_ref"),
            result.get("a_route_execution_ref"),
            proof.get("execution_ref"),
            proof.get("owner_ref"),
            result.get("hypothesis_refs"),
            result.get("current_world_ref"),
            result.get("sufficiency_ref"),
            semantics.get("role_ref"),
            semantics.get("task_ref"),
            semantics.get("goal_ref"),
        )
        checks.append(_check(f"contrast_trace:{result.get('contrast_id')}", all(bool(item) for item in required), required))
    for case in full.get("operational_source", {}).get("cases") or ():
        traceability = case.get("traceability") or {}
        required = (
            traceability.get("final_cognition_execution_ref"),
            traceability.get("final_sufficiency_ref"),
            traceability.get("final_stop_ref"),
            traceability.get("decision_candidate_ref"),
            traceability.get("decision_trace_ref"),
            traceability.get("task_state_ref"),
            traceability.get("task_trace_ref"),
            traceability.get("action_candidate_ref"),
            traceability.get("action_trace_ref"),
            traceability.get("runtime_executor_handoff_ref"),
        )
        checks.append(_check(f"downstream_trace:{case.get('case_id')}", all(bool(item) for item in required), required))
    return checks


def _scenario_id_audit(full: Dict[str, Any]) -> Dict[str, Any]:
    by_id = {item.get("contrast_id"): item for item in full.get("contrast_results") or ()}
    pairs = (
        ("role-owner", "role-visitor"),
        ("task-document", "task-exit"),
        ("role-task-owner", "role-task-visitor"),
        ("goal-locate", "goal-operational-state"),
        ("task-document", "irrelevant-clutter"),
    )
    results = []
    for left, right in pairs:
        left_scenario_id = by_id.get(left, {}).get("scenario_id")
        right_scenario_id = by_id.get(right, {}).get("scenario_id")
        results.append(
            {
                "pair": [left, right],
                "same_scenario_id": bool(left_scenario_id and right_scenario_id and left_scenario_id == right_scenario_id),
                "left_scenario_id": left_scenario_id,
                "right_scenario_id": right_scenario_id,
            }
        )
    return {
        "controlled_contrast_pairs": results,
        "passed": all(item["same_scenario_id"] for item in results),
        "semantic_source": "Role/Task/Goal/Information Need and Evidence inputs; scenario_id is an identifier surface",
    }


def _historical_artifact_inventory(root: Path) -> list[Dict[str, Any]]:
    inventory = []
    for relative in HISTORICAL_ARTIFACTS:
        path = root / relative
        if path.is_dir():
            files = sorted(path.glob("*.json"))
            readable = 0
            for item in files:
                try:
                    json.loads(item.read_text(encoding="utf-8"))
                    readable += 1
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    pass
            inventory.append({
                "path": relative,
                "classification": "VALID_HISTORICAL_OR_SUPPORTING",
                "exists": True,
                "json_records": len(files),
                "json_records_readable": readable,
                "read_only": True,
            })
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            readable = True
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            readable = False
        inventory.append({
            "path": relative,
            "classification": "VALID_HISTORICAL_OR_SUPPORTING" if readable else "NOT_PRESENT_OR_UNREADABLE",
            "exists": path.exists(),
            "json_records": 1 if readable else 0,
            "json_records_readable": 1 if readable else 0,
            "read_only": True,
        })
    return inventory


def build_audit_report_v1() -> Dict[str, Any]:
    full = build_runner_summary_v1()
    root = Path(__file__).resolve().parents[3]
    static_contracts = run_static_contract_audit()
    governance_checks = _governance_checks(full)
    traceability_checks = _traceability_checks(full)
    forbidden = full.get("forbidden_behaviors") or {}
    operational_result = "PASS" if full.get("operational_result") == "PASS" else "FAIL"
    cognitive_result = "PASS" if full.get("cognitive_logic_result") == "PASS" else "FAIL"
    governance_result = "PASS" if governance_checks and all(item["passed"] for item in governance_checks) and _all_false(forbidden.values()) else "FAIL"
    traceability_result = "PASS" if traceability_checks and all(item["passed"] for item in traceability_checks) else "FAIL"
    scenario_audit = _scenario_id_audit(full)
    contract_result = "PASS" if static_contracts["passed"] and scenario_audit["passed"] and not full.get("capability_gaps") else "FAIL"
    failed_checks = [
        *(item["check_id"] for item in governance_checks if not item["passed"]),
        *(item["check_id"] for item in traceability_checks if not item["passed"]),
        *(item["check_id"] for item in static_contracts["checks"] if not item["passed"]),
        *([] if scenario_audit["passed"] else ["scenario_id_semantic_audit"]),
    ]
    if operational_result != "PASS":
        failed_checks.append("operational_result")
    if cognitive_result != "PASS":
        failed_checks.append("cognitive_logic_result")
    if governance_result != "PASS":
        failed_checks.append("governance_result")
    if traceability_result != "PASS":
        failed_checks.append("traceability_result")
    if contract_result != "PASS":
        failed_checks.append("contract_integrity_result")
    if not _all_false(forbidden.values()):
        failed_checks.append("negative_guard_result")
    return {
        "phase": PHASE,
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(root),
        "current_session_evidence": {
            "status": "PRODUCED_BY_FINAL_AUDIT_RUNNER",
            "source_runner": "capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.runner_v1",
            "source_summary_embedded": True,
            "transient_output": str(OUTPUT_PATH),
            "durable_archive_written": False,
        },
        "operational_result": operational_result,
        "cognitive_logic_result": cognitive_result,
        "governance_result": governance_result,
        "traceability_result": traceability_result,
        "contract_integrity_result": contract_result,
        "operational_evidence": full.get("operational"),
        "cognitive_evidence": {
            "source_phase": full.get("phase"),
            "assertion_result": cognitive_result,
            "failed_checks": [item["check_id"] for item in full.get("contrast_case_results") or () if item.get("changed_semantic_fields") is None],
        },
        "governance_checks": governance_checks,
        "traceability_checks": traceability_checks,
        "contract_checks": static_contracts,
        "historical_artifact_inventory": _historical_artifact_inventory(root),
        "scenario_id_audit": scenario_audit,
        "negative_guard_result": {
            "passed": _all_false(forbidden.values()) and all(
                case.get("runtime_executor_invoked") is False
                for case in full.get("operational_source", {}).get("cases") or ()
            ),
            "observed_forbidden_behaviors": forbidden,
        },
        "baseline_compatibility": [
            {"component": "CONTROLLED_REPLAY_RUNTIME", "classification": "CURRENT_BASELINE", "evidence": "Full E2E source"},
            {"component": "Minimum Sufficient Cognition Loop", "classification": "CURRENT_BASELINE", "evidence": "Full E2E source"},
            {"component": "Cognition → Decision → Task → Action Candidate", "classification": "CURRENT_BASELINE", "evidence": "operational evidence"},
            {"component": "Replay Evaluation / White-box / Archive / Governance", "classification": "COMPATIBILITY_REQUIRED", "evidence": "existing read-only artifacts and prior verified contracts"},
            {"component": "historical/deprecated phase harnesses", "classification": "SUPERSEDED", "evidence": "not rerun by final closure audit"},
        ],
        "owner_matrix_result": "PASS" if governance_result == "PASS" else "FAIL",
        "unresolved_items": [{"classification": "NON_BLOCKING_ARCHITECTURE_DEBT", "item": item} for item in NON_BLOCKING_DEBTS],
        "deferred_runtime_items": [{"classification": "DEFERRED_FUTURE_RUNTIME", "item": item} for item in DEFERRED_RUNTIME],
        "findings": [],
        "blocker_count": len(failed_checks),
        "non_blocking_debt_count": len(NON_BLOCKING_DEBTS),
        "deferred_runtime_count": len(DEFERRED_RUNTIME),
        "failed_checks": failed_checks,
        "full_e2e_summary": full,
        "final_decision": "PENDING_USER_VERIFIER",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    report = build_audit_report_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
