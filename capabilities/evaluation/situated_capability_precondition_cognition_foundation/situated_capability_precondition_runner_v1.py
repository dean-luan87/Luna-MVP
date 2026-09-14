"""User-terminal runner for controlled situated capability preconditions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_engine_v1 import (
    EXECUTION_MODE,
    evaluate,
    jsonable,
)
from .case_definitions_v1 import build_cases_v1


PHASE = "Phase-P1-Luna-Situated-Capability-Precondition-Cognition-Foundation-v1-001"


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/situated_capability_precondition_cognition_foundation_v1"


def _payload(result: Any) -> Dict[str, Any]:
    return jsonable(result)


def build_runner_summary_v1() -> Dict[str, Any]:
    results = [_payload(evaluate(request)) for request in build_cases_v1()]

    return {
        "phase": PHASE,
        "execution_mode": EXECUTION_MODE,
        "controlled_only": True,
        "provider_invocation": False,
        "model_invocation": False,
        "semantic_driver": "capability_need+precondition_definition+situated_state+capability_availability",
        "scenario_id_semantic_driver": False,
        "cycle_index_semantic_driver": False,
        "cases": results,
        "resolution_policy": "information_need+goal+capability_supported_dimensions",
        "forbidden_behaviors": {
            "provider_invocation": False,
            "model_invocation": False,
            "runtime_execution": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "device_control": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "self_owns_capability_decision": False,
        },
        "validation_errors": [],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled situated capability precondition cases.")
    parser.parse_args()
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
