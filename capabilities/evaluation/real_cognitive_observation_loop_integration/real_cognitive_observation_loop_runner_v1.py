"""User-terminal Runner for two bounded real OCR cognitive-loop cases.

This module intentionally performs real work only when the user invokes it.
The Agent does not import or execute this Runner during implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .case_definitions_v1 import build_real_cognitive_observation_cases_v1
from .engine_v1 import PHASE, RealCognitiveObservationLoopEngineV1, _jsonable


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/real_cognitive_observation_loop_integration_v1"


def build_runner_summary_v1() -> Dict[str, Any]:
    engine = RealCognitiveObservationLoopEngineV1(repository_root=ROOT)
    cases = [engine.run_case(case) for case in build_real_cognitive_observation_cases_v1(ROOT)]
    cycles = [cycle for case in cases for cycle in case.get("observation_cycles", ())]
    return {
        "phase": PHASE,
        "execution_mode": "LIVE_RUNTIME",
        "selected_provider": "ocr_v1",
        "provider_family": "ocr",
        "capability_ref": "text_recognition",
        "provider_ref": "provider:ocr_v1",
        "model_ref": "model:ocr_v1",
        "cases": cases,
        "case_count": len(cases),
        "real_provider_invocation_count": sum(1 for item in cycles if item.get("provider_invoked")),
        "real_model_invocation_count": sum(1 for item in cycles if item.get("model_invoked")),
        "recorded_result_used": False,
        "operational_result": "PENDING_USER_TERMINAL_VERIFICATION",
        "cognitive_logic_result": "PENDING_USER_TERMINAL_VERIFICATION",
        "forbidden_behaviors": {
            "scenario_id_driven_cognition": False,
            "world_truth_declared": False,
            "fact_admitted": False,
            "field_mutation": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "cycle_three": False,
        },
        "validation_errors": [
            error
            for case in cases
            for error in case.get("validation_errors", ())
        ],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(_jsonable(summary), indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(_jsonable(summary), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
