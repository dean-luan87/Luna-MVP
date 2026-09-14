#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.task_manager.module import run_task_manager_module_v1


def _base_request(task_id: str) -> Dict[str, Any]:
    return {
        "task_request_id": task_id,
        "task_type": "sequential",
        "task_goal": "compose_task_plan",
        "requester_ref": "integration_test",
        "priority": "normal",
        "context_snapshot": {
            "request_direct_action_execution": False,
            "request_direct_model_call": False,
            "request_direct_field_state_write": False,
            "request_bypass_capability_module_api": False,
        },
        "dependency_refs": ("dep_a",),
        "dependency_snapshot": {"dep_a": "completed"},
        "dependency_graph": {"dep_a": []},
        "resource_constraints": {"budget": "candidate_only"},
        "permission_snapshot": {"governance_ref": "gov_tm_v1", "allowed": True},
        "capability_requirements": (
            "luna.field_state_reducer",
            "luna.model_controller",
        ),
        "deadline_or_timeout": "t+5m",
        "interruption_policy": {"required_revalidation": True},
        "recovery_policy": {
            "preferred_recovery": ("retry_candidate", "replan_candidate")
        },
        "version_snapshots": {
            "task_manager": "v1",
            "field_state_reducer": "v1",
        },
        "health_signal_refs": ("health_ok",),
        "decision_refs": ("decision_tm",),
        "context_refs": ("ctx_tm",),
        "observation_refs": ("obs_tm",),
        "module_adapter_refs": ("adapter_tm",),
        "output_gate_refs": ("gate_tm",),
        "worldmodel_memory_bridge_refs": ("wmb_tm",),
        "decision_center_refs": ("dc_tm",),
        "health_watchdog_refs": ("hw_tm",),
        "readiness_hint": "ready",
        "recovery_point": "rp_0",
        "failure_reason": "",
        "cancel_reason": "",
        "terminate_reason": "",
        "requested_control": "",
        "completion_status": "",
        "interruption_reason": "",
        "recovery_decision": "",
    }


def _cases() -> Tuple[Dict[str, Any], ...]:
    c1 = _base_request("tm_case_01_happy")

    c2 = _base_request("tm_case_02_invalid_input")
    c2["task_request_id"] = ""

    c3 = _base_request("tm_case_03_cycle_dependency")
    c3["dependency_graph"] = {"a": ["b"], "b": ["a"]}

    c4 = _base_request("tm_case_04_waiting_dependency")
    c4["dependency_snapshot"] = {"dep_a": "running"}

    c5 = _base_request("tm_case_05_pause")
    c5["requested_control"] = "pause"

    c6 = _base_request("tm_case_06_resume")
    c6["requested_control"] = "resume"
    c6["interruption_reason"] = "manual_pause"

    c7 = _base_request("tm_case_07_cancel")
    c7["requested_control"] = "cancel"

    c8 = _base_request("tm_case_08_terminate")
    c8["requested_control"] = "terminate"

    c9 = _base_request("tm_case_09_capability_unavailable")
    c9["capability_requirements"] = ("luna.non_existing_capability",)

    c10 = _base_request("tm_case_10_permission_denied")
    c10["permission_snapshot"] = {}

    c11 = _base_request("tm_case_11_completion")
    c11["completion_status"] = "completed"

    c12 = _base_request("tm_case_12_partial")
    c12["completion_status"] = "partially_completed"

    c13 = _base_request("tm_case_13_fail_recovery")
    c13["completion_status"] = "failed"
    c13["recovery_decision"] = "retry_candidate"

    c14 = _base_request("tm_case_14_direct_action_forbidden")
    c14["context_snapshot"]["request_direct_action_execution"] = True

    c15 = _base_request("tm_case_15_direct_model_forbidden")
    c15["context_snapshot"]["request_direct_model_call"] = True

    c16 = _base_request("tm_case_16_state_write_forbidden")
    c16["context_snapshot"]["request_direct_field_state_write"] = True

    c17 = _base_request("tm_case_17_bypass_api_forbidden")
    c17["context_snapshot"]["request_bypass_capability_module_api"] = True

    c18 = _base_request("tm_case_18_replay_deterministic")

    return (
        c1,
        c2,
        c3,
        c4,
        c5,
        c6,
        c7,
        c8,
        c9,
        c10,
        c11,
        c12,
        c13,
        c14,
        c15,
        c16,
        c17,
        c18,
    )


def _validate_common(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for k in (
        "task_status",
        "task_plan",
        "subtasks",
        "execution_request_candidates",
        "dependency_status",
        "progress",
        "interruption_state",
        "recovery_candidates",
        "result_summary",
        "unresolved_items",
        "diagnostics",
        "trace_ref",
        "replay_key",
    ):
        if k not in result:
            issues.append(f"missing_key:{k}")

    for f in (
        "action_execution_executed",
        "model_call_executed",
        "state_mutation_executed",
        "fact_promotion_executed",
        "runtime_dispatch_executed",
    ):
        if result.get(f) is not False:
            issues.append(f"forbidden_side_effect:{f}")

    return len(issues) == 0, issues


def run() -> Dict[str, Any]:
    rows = []
    pass_count = 0

    all_cases = _cases()
    deterministic_payload = all_cases[-1]
    deterministic_a = run_task_manager_module_v1(deterministic_payload)
    deterministic_b = run_task_manager_module_v1(deterministic_payload)
    deterministic_ok = (
        deterministic_a.get("task_status") == deterministic_b.get("task_status")
        and deterministic_a.get("replay_key") == deterministic_b.get("replay_key")
        and deterministic_a.get("progress") == deterministic_b.get("progress")
    )

    for payload in all_cases:
        result = run_task_manager_module_v1(payload)
        ok_common, issues = _validate_common(result)

        cid = payload["task_request_id"] or "missing_id_case"
        expected_checks: List[Tuple[str, bool]] = []

        if "invalid_input" in cid or cid == "missing_id_case":
            expected_checks.append(
                ("blocked_on_invalid", result["task_status"] in {"blocked", "failed"})
            )
        if "waiting_dependency" in cid:
            expected_checks.append(
                (
                    "waiting_dependency",
                    result["task_status"] in {"waiting_dependency", "blocked"},
                )
            )
        if "pause" in cid:
            expected_checks.append(
                ("pause_state", result["task_status"] in {"paused", "blocked"})
            )
        if "resume" in cid:
            expected_checks.append(
                (
                    "resume_state",
                    result["task_status"] in {"resuming", "paused", "blocked"},
                )
            )
        if "cancel" in cid:
            expected_checks.append(
                ("cancel_state", result["task_status"] == "cancelled")
            )
        if "terminate" in cid:
            expected_checks.append(
                ("terminate_state", result["task_status"] == "terminated")
            )
        if "capability_unavailable" in cid:
            expected_checks.append(
                ("blocked_capability", len(result["unresolved_items"]) > 0)
            )
        if "permission_denied" in cid:
            expected_checks.append(
                ("permission_denied", len(result["unresolved_items"]) > 0)
            )
        if "completion" in cid:
            expected_checks.append(("completed", result["task_status"] == "completed"))
        if "partial" in cid:
            expected_checks.append(
                ("partial", result["task_status"] == "partially_completed")
            )
        if "replay_deterministic" in cid:
            expected_checks.append(("deterministic", deterministic_ok))

        expect_ok = all(v for _, v in expected_checks)
        passed = ok_common and expect_ok
        if passed:
            pass_count += 1

        rows.append(
            {
                "case_id": cid,
                "passed": passed,
                "issues": issues,
                "expected_checks": [
                    {"check": k, "passed": v} for k, v in expected_checks
                ],
                "task_status": result.get("task_status"),
            }
        )

    return {
        "summary": {
            "total": len(all_cases),
            "passed": pass_count,
            "failed": len(all_cases) - pass_count,
            "all_passed": pass_count == len(all_cases),
        },
        "rows": rows,
    }


def main() -> int:
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["summary"]["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
