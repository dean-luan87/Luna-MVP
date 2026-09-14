"""User-terminal Runner for Situated Eligibility gated real RapidOCR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .engine_v1 import (
    EXECUTION_MODE,
    PHASE,
    SituatedEligibilityGatedRealOCRExecutionEngineV1,
    jsonable,
)


def _repo_root() -> Path:
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/situated_eligibility_gated_real_ocr_execution_integration_v1"


def build_runner_summary_v1() -> Dict[str, Any]:
    records = SituatedEligibilityGatedRealOCRExecutionEngineV1(
        repository_root=ROOT,
    ).run_controlled_bindings()
    attempted = sum(record.provider_real_execution_attempted for record in records)
    provider_invocations = sum(record.provider_invoked for record in records)
    model_invocations = sum(record.model_invoked for record in records)
    return {
        "phase": PHASE,
        "execution_mode": EXECUTION_MODE,
        "records": records,
        "case_count": len(records),
        "real_provider_execution_attempt_count": attempted,
        "real_provider_invocation_count": provider_invocations,
        "real_model_invocation_count": model_invocations,
        "recorded_provider_result_used": False,
        "forbidden_behaviors": {
            "provider_invocation_before_eligibility": False,
            "model_invocation_before_eligibility": False,
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "camera_control": False,
            "movement_control": False,
            "field_mutation": False,
            "world_truth_declared": False,
        },
        "validation_errors": [
            error
            for record in records
            for error in record.validation_errors
        ],
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real RapidOCR only after Situated Eligibility admission.")
    parser.parse_args()
    summary = jsonable(build_runner_summary_v1())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["build_runner_summary_v1"]
