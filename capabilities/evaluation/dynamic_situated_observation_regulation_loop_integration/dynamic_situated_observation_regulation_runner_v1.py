"""User-terminal Runner for bounded Dynamic Situated Observation regulation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .engine_v1 import (
    EXECUTION_MODE,
    PHASE,
    PROVIDER_EXECUTION_MODE,
    SITUATED_STATE_MODE,
    DynamicSituatedObservationRegulationLoopEngineV1,
    jsonable,
)


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/dynamic_situated_observation_regulation_loop_integration_v1"


def build_runner_summary_v1() -> Dict[str, Any]:
    cases = DynamicSituatedObservationRegulationLoopEngineV1(
        repository_root=ROOT,
    ).run_cases()
    states = [state for case in cases for state in case.states]
    total_provider_invocations = sum(case.real_provider_invocation_count for case in cases)
    return {
        "phase": PHASE,
        "execution_mode": EXECUTION_MODE,
        "situated_state_mode": SITUATED_STATE_MODE,
        "provider_execution_mode": PROVIDER_EXECUTION_MODE,
        "provider_family": "ocr",
        "capability_ref": "text_recognition",
        "selected_provider": "RapidOCR / ONNXRuntime",
        "provider_ref": "provider:ocr_v1",
        "model_ref": "model:ocr_v1",
        "native_model_ref": "rapidocr_onnxruntime_v0",
        "case_count": len(cases),
        "cases": cases,
        "regulation_states": states,
        "per_state_provider_invocation_count": {
            f"{state.case_id}:{state.state_id}": state.provider_invocation_count
            for state in states
        },
        "per_case_provider_invocation_count": {
            case.case_id: case.real_provider_invocation_count
            for case in cases
        },
        "real_provider_invocation_count": total_provider_invocations,
        "recorded_provider_result_used": False,
        "forbidden_behaviors": {
            "provider_invocation_before_current_eligibility": False,
            "model_invocation_before_current_eligibility": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "camera_control": False,
            "movement_control": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "memory_mutation": False,
            "autonomous_background_loop": False,
        },
        "scenario_id_semantic_driver": False,
        "cycle_index_semantic_driver": False,
        "validation_errors": [
            error
            for case in cases
            for error in case.validation_errors
        ],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run bounded Situated Observation regulation with gated real OCR.")
    parser.parse_args()
    summary = jsonable(build_runner_summary_v1())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["build_runner_summary_v1"]
