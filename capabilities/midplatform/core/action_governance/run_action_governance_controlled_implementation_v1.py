"""Controlled runner for Action Governance implementation v1.

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
        if (candidate / "capabilities/midplatform/core/action_governance").is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/action_governance").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.action_governance.action_governance_fixture_v1 import (
    get_action_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.action_governance.action_static_validators_v1 import (
    validate_action_candidate,
    validate_dependencies,
    validate_handoffs,
    validate_input_refs_read_only,
    validate_negative_guard_flags,
    validate_no_runtime_side_effects,
    validate_preconditions,
    validate_trace_completeness,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/action_governance_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = ActionGovernanceEngineV1()
    fixtures = get_action_synthetic_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        all_refs = (
            case.request.selected_decision_refs
            + case.request.intent_refs
            + case.request.causal_refs
            + case.request.target_refs
            + case.request.context_refs
            + case.request.field_refs
            + case.request.permission_refs
            + case.request.safety_refs
            + case.request.confirmation_refs
            + case.request.resource_refs
            + case.request.task_reference_context_refs
        )

        checks = {
            "input_refs_read_only": validate_input_refs_read_only(all_refs),
            "action_candidate_valid": validate_action_candidate(
                output.action_candidate
            ),
            "preconditions_valid": validate_preconditions(output.precondition_results),
            "dependencies_valid": validate_dependencies(output.dependency_results),
            "trace_complete": validate_trace_completeness(output),
            "handoffs_valid": validate_handoffs(output),
            "negative_guard_flags": validate_negative_guard_flags(),
            "no_runtime_side_effects": validate_no_runtime_side_effects(output),
            "state_expected": output.action_candidate.action_state
            == case.expected_state,
            "readiness_expected": output.readiness.state == case.expected_readiness,
            "runtime_handoff_expected": (
                output.runtime_handoff.execution_readiness == "candidate_ready"
            )
            is case.expected_runtime_handoff_eligible,
            "task_handoff_reference_only_expected": (
                output.task_handoff.reference_only
                is case.expected_task_handoff_reference_only
            ),
            "synthetic_only": case.synthetic_only is True
            and case.request.synthetic_only is True,
        }

        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "source_decision_refs": [
                    r.ref_id for r in case.request.selected_decision_refs
                ],
                "action_candidate_ref": output.action_candidate.action_candidate_id,
                "state": output.action_candidate.action_state,
                "preconditions": [
                    {"id": p.precondition_id, "status": p.status}
                    for p in output.precondition_results
                ],
                "dependencies": [
                    {"id": d.dependency_id, "status": d.status}
                    for d in output.dependency_results
                ],
                "permission_safety": {
                    "permission_valid": case.request.permission_valid,
                    "safety_valid": case.request.safety_valid,
                },
                "confirmation": {
                    "state": case.request.confirmation.state,
                    "stale": case.request.confirmation.is_stale,
                    "strong": case.request.confirmation.strong_confirmation,
                },
                "reversibility": case.request.reversibility,
                "resource": output.resource_status.state,
                "readiness": output.readiness.state,
                "provenance": list(output.trace_candidate.provenance),
                "expected_negative_guards": list(case.expected_negative_guards),
                "handoff_eligibility": {
                    "runtime_candidate_ready": output.runtime_handoff.execution_readiness
                    == "candidate_ready",
                    "task_reference_only": output.task_handoff.reference_only,
                },
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )

        traces.append(
            {
                "case_id": case.case_id,
                "trace_id": output.trace_candidate.trace_id,
                "action_candidate_ref": output.trace_candidate.action_candidate_ref,
                "decision_refs": list(output.trace_candidate.decision_refs),
                "precondition_refs": list(output.trace_candidate.precondition_refs),
                "dependency_refs": list(output.trace_candidate.dependency_refs),
                "runtime_handoff_id": output.runtime_handoff.handoff_id,
                "task_handoff_id": output.task_handoff.handoff_id,
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Action-Governance-Controlled-Implementation-v1-001",
        "case_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "candidate_only": True,
        "runtime_executed": False,
        "action_executed": False,
        "task_created": False,
        "scheduler_executed": False,
        "database_write_executed": False,
        "device_control_executed": False,
        "status": "ACTION_GOVERNANCE_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }

    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "action-governance-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    result_path = OUTPUT_DIR / "action_governance_result_v1.json"
    case_path = OUTPUT_DIR / "action_governance_case_results_v1.json"
    trace_path = OUTPUT_DIR / "action_governance_trace_v1.json"

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
