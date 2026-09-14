"""Controlled runner for Cognitive Flow implementation v1.

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
        sentinel = candidate / "capabilities/midplatform/core/cognitive_flow"
        if sentinel.is_dir():
            return candidate

    cwd = Path.cwd().resolve()
    if (cwd / "capabilities/midplatform/core/cognitive_flow").is_dir():
        return cwd

    return Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

if __package__ in {None, ""}:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.cognitive_flow_engine_v1 import (  # noqa: E402
    CognitiveFlowEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_fixture_v1 import (  # noqa: E402
    get_cognitive_flow_fixtures_v1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_static_validators_v1 import (  # noqa: E402
    validate_output_contract,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/cognitive_flow_controlled_implementation_v1"


def run_controlled() -> Dict[str, Any]:
    engine = CognitiveFlowEngineV1()
    fixtures = get_cognitive_flow_fixtures_v1()

    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []

    for case in fixtures:
        output = engine.run_case(case.request)
        all_refs = (
            case.request.context_refs
            + case.request.pcn_refs
            + case.request.intent_refs
            + case.request.state_formation_refs
            + case.request.attention_refs
            + case.request.hypothesis_refs
            + case.request.field_refs
            + case.request.causal_refs
            + (
                ()
                if case.request.current_world_ref is None
                else (case.request.current_world_ref,)
            )
            + (
                ()
                if case.request.cognitive_state_vector_ref is None
                else (case.request.cognitive_state_vector_ref,)
            )
            + (
                ()
                if case.request.regulation_candidate_ref is None
                else (case.request.regulation_candidate_ref,)
            )
        )
        checks = {
            "output_contract": validate_output_contract(output, all_refs),
            "final_state_expected": output.final_state.current_state
            == case.expected_final_state,
            "transition_kind_expected": bool(output.transition_candidates)
            and output.transition_candidates[0].relationship_kind
            == case.expected_transition_kind,
            "reconsideration_expected": bool(output.reconsideration_candidates)
            == case.expected_reconsideration,
            "suspended_expected": (output.suspend_candidate is not None)
            == case.expected_suspended,
            "aborted_expected": (output.abort_candidate is not None)
            == case.expected_aborted,
            "inheritance_expected": (output.inheritance_candidate is not None)
            == case.expected_inheritance,
            "memory_candidate_expected": (
                output.memory_observation_candidate is not None
            )
            == case.expected_memory_candidate,
            "learning_candidate_expected": (
                output.learning_handoff_candidate is not None
            )
            == case.expected_learning_candidate,
            "negative_guards_expected": {
                "runtime_execution": output.negative_guard_status.runtime_execution,
                "database_write": output.negative_guard_status.database_write,
                "device_control": output.negative_guard_status.device_control,
                "scheduler_execution": output.negative_guard_status.scheduler_execution,
                "task_mutation": output.negative_guard_status.task_mutation,
                "model_call": output.negative_guard_status.model_call,
                "source_owner_mutation": output.negative_guard_status.source_owner_mutation,
                "real_side_effect": output.negative_guard_status.real_side_effect,
                "synthetic_only": output.negative_guard_status.synthetic_only,
            }
            == case.expected_negative_guards,
        }
        case_results.append(
            {
                "case_id": case.case_id,
                "description": case.description,
                "final_state": output.final_state.current_state,
                "transition_kind": output.transition_candidates[0].relationship_kind
                if output.transition_candidates
                else "NONE",
                "reconsideration": bool(output.reconsideration_candidates),
                "suspended": output.suspend_candidate is not None,
                "aborted": output.abort_candidate is not None,
                "inheritance": output.inheritance_candidate is not None,
                "memory_candidate": output.memory_observation_candidate is not None,
                "learning_candidate": output.learning_handoff_candidate is not None,
                "checks": checks,
                "all_checks_passed": all(checks.values()),
            }
        )
        traces.append(
            {
                "case_id": case.case_id,
                "root_cycle_trace_id": output.trace.root_cycle_trace_id,
                "transition_trace": list(output.trace.transition_trace),
                "reconsideration_trace": list(output.trace.reconsideration_trace),
                "inheritance_trace": list(output.trace.inheritance_trace),
            }
        )

    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-Cognitive-Flow-And-State-Machine-Controlled-Implementation-v1-001",
        "scenario_count": len(case_results),
        "runtime_execution": False,
        "database_write": False,
        "device_control": False,
        "scheduler_execution": False,
        "task_mutation": False,
        "model_call": False,
        "source_owner_mutation": False,
        "synthetic_only": True,
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "status": "COGNITIVE_FLOW_CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }
    return {
        "summary": summary,
        "case_results": case_results,
        "trace": {
            "trace_id": "cognitive-flow-controlled-implementation-trace-v1",
            "case_traces": traces,
            "candidate_only": True,
        },
    }


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "cognitive_flow_result_v1.json"
    case_path = OUTPUT_DIR / "cognitive_flow_case_results_v1.json"
    trace_path = OUTPUT_DIR / "cognitive_flow_trace_v1.json"
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
