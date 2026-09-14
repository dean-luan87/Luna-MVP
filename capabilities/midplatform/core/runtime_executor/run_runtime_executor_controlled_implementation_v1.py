"""Controlled runner for Runtime Executor implementation v1.

This runner is intended for user-terminal execution only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "capabilities/midplatform/core/runtime_executor").is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/runtime_executor").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.runtime_executor.runtime_executor_engine_v1 import (  # noqa: E402
    RuntimeExecutorEngineV1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_fixture_v1 import (  # noqa: E402
    get_runtime_executor_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.runtime_executor.runtime_executor_static_validators_v1 import (  # noqa: E402
    validate_final_gate,
    validate_idempotency_behavior,
    validate_negative_guards,
    validate_no_side_effects,
    validate_partial_not_success,
    validate_result_handoffs,
    validate_retry_boundary,
    validate_state,
    validate_timeout_cancel,
    validate_trace,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/runtime_executor_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = RuntimeExecutorEngineV1()
    fixtures = get_runtime_executor_synthetic_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        checks = {
            "state_valid": validate_state(output),
            "final_gate_valid": validate_final_gate(output),
            "idempotency_valid": validate_idempotency_behavior(output),
            "retry_boundary_valid": validate_retry_boundary(output),
            "timeout_cancel_valid": validate_timeout_cancel(output),
            "partial_not_success_valid": validate_partial_not_success(output),
            "handoffs_valid": validate_result_handoffs(output),
            "trace_valid": validate_trace(output),
            "negative_guards_valid": validate_negative_guards(),
            "no_side_effects": validate_no_side_effects(output),
            "expected_status": output.result.status == case.expected_status,
            "expected_state": output.state.state == case.expected_state,
            "expected_admitted": output.admission.admitted is case.expected_admitted,
            "expected_retry_blocked": (
                output.retry.blocked_reason == "retry_without_authority"
            )
            is case.expected_retry_blocked,
            "expected_duplicate": output.idempotency_duplicate
            is case.expected_idempotency_duplicate,
            "expected_scope_mismatch": output.idempotency_scope_mismatch
            is case.expected_idempotency_scope_mismatch,
            "expected_partial_present": (output.partial_result is not None)
            is case.expected_partial_present,
            "expected_failure_present": (output.failure is not None)
            is case.expected_failure_present,
            "expected_rollback_required": output.rollback.rollback_required
            is case.expected_rollback_required,
            "synthetic_only": case.synthetic_only
            and case.request.request.candidate_only
            and case.request.request.planning_only,
        }

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "execution_id": output.execution_id,
                "status": output.result.status,
                "state": output.state.state,
                "admission": {
                    "admitted": output.admission.admitted,
                    "reason": output.admission.reason,
                },
                "final_gate": {
                    "passed": output.final_gate.passed,
                    "scope_valid": output.final_gate.scope_valid,
                    "time_window_valid": output.final_gate.time_window_valid,
                },
                "idempotency": {
                    "duplicate": output.idempotency_duplicate,
                    "scope_mismatch": output.idempotency_scope_mismatch,
                    "duplicate_attempt_created": output.duplicate_attempt_created,
                },
                "retry": {
                    "requested": output.retry.retry_requested,
                    "authorized": output.retry.retry_authorized,
                    "blocked_reason": output.retry.blocked_reason,
                },
                "timeout": {
                    "timed_out": output.timeout.timed_out,
                    "timeout_stage": output.timeout.timeout_stage,
                },
                "cancellation": {
                    "cancel_requested": output.cancellation.cancel_requested,
                    "cancelled": output.cancellation.cancelled,
                },
                "partial_result_ref": output.result.partial_result_ref,
                "failure_ref": output.result.failure_ref,
                "rollback_required": output.rollback.rollback_required,
                "handoff_consumers": [
                    output.action_handoff.consumer_owner,
                    output.task_handoff.consumer_owner,
                    output.diagnostics_result_handoff.consumer_owner,
                ],
                "expected_negative_guards": list(case.expected_negative_guards),
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "trace_id": output.trace.trace_id,
                "execution_request_ref": output.trace.execution_request_ref,
                "attempt_refs": list(output.trace.attempt_refs),
                "result_ref": output.trace.result_ref,
                "failure_refs": list(output.trace.failure_refs),
                "diagnostics_refs": list(output.trace.diagnostics_refs),
                "provenance": list(output.trace.provenance),
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Runtime-Executor-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "device_control_executed": False,
        "provider_call_executed": False,
        "adapter_call_executed": False,
        "scheduler_runtime_executed": False,
        "task_mutation_executed": False,
        "database_write_executed": False,
        "status": "RUNTIME_EXECUTOR_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "runtime-executor-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_path = OUTPUT_DIR / "runtime_executor_result_v1.json"
    case_path = OUTPUT_DIR / "runtime_executor_case_results_v1.json"
    trace_path = OUTPUT_DIR / "runtime_executor_trace_v1.json"

    result_path.write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    case_path.write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    trace_path.write_text(
        json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "result": str(result_path),
        "cases": str(case_path),
        "trace": str(trace_path),
    }


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
