"""User-terminal runner for controlled active observation preconditions.

This runner emits controlled candidate state only.  It intentionally does not
execute a provider; provider eligibility is the terminal output of this phase.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_engine_v1 import (
    EXECUTION_MODE,
    PHASE,
    evaluate,
    jsonable,
)

from .case_definitions_v1 import build_cases_v1


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/active_observation_precondition_dynamic_viewpoint_foundation_v1"


def _case_payload(request: Any, result: Any, canonical_chain: Dict[str, Any]) -> Dict[str, Any]:
    payload = jsonable(result)
    payload["canonical_observation_chain"] = jsonable(canonical_chain)
    payload["input"] = jsonable(request)
    return payload


def build_runner_summary_v1() -> Dict[str, Any]:
    results = []
    for request in build_cases_v1():
        result, canonical_chain = evaluate(request)
        results.append(_case_payload(request, result, canonical_chain))

    by_case: Dict[str, list] = {}
    for item in results:
        by_case.setdefault(item["case_id"], []).append(item)
    transitions = {}
    for case_id in ("DYNAMIC_STATE_REACHES_OBSERVABLE", "OBSERVATION_WINDOW_LOST"):
        states = sorted(by_case[case_id], key=lambda item: item["cycle_index"])
        transitions[case_id] = {
            "same_requirement_ref": len({item["request"]["observation_requirement"]["observation_requirement_ref"] for item in states}) == 1,
            "same_target_ref": len({item["request"]["observation_requirement"]["target_ref"] for item in states}) == 1,
            "same_field_ref": len({item["request"]["observation_requirement"]["field_ref"] for item in states}) == 1,
            "state_refs": [item["request"]["relative_state"]["relative_state_ref"] for item in states],
            "window_statuses": [item["window"]["status"] for item in states],
            "feasibility_statuses": [item["feasibility"]["status"] for item in states],
            "eligibility_statuses": [item["capability_eligibility"]["eligible_now"] for item in states],
            "temporal_refs": [item["request"]["temporal_ref"] for item in states],
        }

    return {
        "phase": PHASE,
        "execution_mode": EXECUTION_MODE,
        "controlled_only": True,
        "provider_invocation": False,
        "model_invocation": False,
        "real_dynamic_viewpoint_verified": False,
        "semantic_driver": "goal+information_need+continuation+minimum_conditions+self_state+relative_state+capability_availability",
        "scenario_id_semantic_driver": False,
        "cycle_index_semantic_driver": False,
        "cases": results,
        "transitions": transitions,
        "forbidden_behaviors": {
            "provider_invocation": False,
            "model_invocation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "device_control": False,
            "runtime_executor_invocation": False,
            "field_mutation": False,
            "field_truth_declared": False,
            "world_truth_declared": False,
            "self_owns_observation_decision": False,
        },
        "validation_errors": [],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled active observation precondition cases.")
    parser.parse_args()
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
