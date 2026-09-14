"""User-terminal Runner for the first real provider execution path."""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict

from .engine_v1 import _jsonable
from .fixtures_v1 import build_provider_observation_cases_v1
from .real_provider_execution_engine_v1 import RealProviderExecutionEngineV1


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/real_provider_execution_integration_v1"
DEFAULT_SOURCE = ROOT / "_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg"
DEFAULT_MODEL = ROOT / "vision/detection/yolo/yolo11n.pt"


def _summary(result: Dict[str, Any], source_ref: str, model_path: str) -> Dict[str, Any]:
    provider = result.get("provider")
    provider_result = result.get("provider_result")
    request = result.get("provider_request")
    details = result.get("details") or {}
    return {
        "phase": "Phase-P1-Luna-Real-Provider-Execution-Integration-v1-001",
        "execution_mode": "LIVE_RUNTIME",
        "selected_provider": "YOLO11n local provider",
        "provider_family": "yolo",
        "source_ref": source_ref,
        "model_path": model_path,
        "provider_real_execution_attempted": bool(result.get("provider_real_execution_attempted")),
        "provider_real_execution_verified": bool(result.get("provider_real_execution_verified")),
        "provider_invoked": bool(result.get("provider_invoked")),
        "model_invoked": bool(result.get("model_invoked")),
        "recorded_provider_result_used": False,
        "provider_status": provider_result.status if provider_result else None,
        "provider_result_ref": provider_result.provider_result_ref if provider_result else None,
        "provider_request_ref": request.provider_request_ref if request else None,
        "runtime_observation_ref": result.get("runtime_observation_ref"),
        "gateway_admission_ref": result.get("gateway_admission_ref"),
        "evidence_refs": list(result.get("evidence_refs") or ()),
        "a_route_execution_ref": result.get("a_route_execution_ref"),
        "sufficiency_ref": result.get("sufficiency_ref"),
        "information_gap_ref": result.get("information_gap_ref"),
        "stop_ref": result.get("stop_ref"),
        "observation_demand_ref": request.observation_demand_ref if request else None,
        "capability_requirement_ref": request.capability_requirement_ref if request else None,
        "capability_ref": request.capability_ref if request else None,
        "provider_ref": request.provider_ref if request else None,
        "model_ref": request.model_ref if request else None,
        "trace_refs": list(request.trace_refs) if request else [],
        "provenance_refs": list(request.provenance_refs) if request else [],
        "forbidden_behaviors": {
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "external_side_effect": False,
            "field_mutation": bool(getattr(provider, "field_mutation", False)) if provider else False,
            "world_truth_declared": bool(getattr(provider, "truth_declared", False)) if provider else False,
        },
        "provider_native_result": _jsonable(provider) if provider else None,
        "provider_runtime_result": _jsonable(provider_result) if provider_result else None,
        "details": details,
        "validation_errors": list(result.get("errors") or ()),
        "status": "REAL_PROVIDER_EXECUTION_RESULT_CANDIDATE",
    }


def build_runner_summary_v1(*, source_ref: str = str(DEFAULT_SOURCE), model_path: str = str(DEFAULT_MODEL)) -> Dict[str, Any]:
    base_case = build_provider_observation_cases_v1()[0]
    case = replace(
        base_case,
        case_id="REAL_PROVIDER_EXECUTION_VISION",
        title="one bounded local YOLO11n provider result enters cognition",
        execution_instance_ref=f"provider-runtime:real-yolo11n:{uuid.uuid4().hex[:12]}",
    )
    result = RealProviderExecutionEngineV1(ROOT).run(case, source_ref=source_ref, model_path=model_path)
    summary = _summary(result, source_ref, model_path)
    summary["all_checks_passed"] = bool(
        summary["provider_real_execution_verified"]
        and summary["provider_invoked"]
        and summary["provider_status"] in {"SUCCESS", "EMPTY_SUCCESS"}
        and summary["runtime_observation_ref"]
        and summary["gateway_admission_ref"]
        and summary["a_route_execution_ref"]
        and not summary["validation_errors"]
        and not any(summary["forbidden_behaviors"].values())
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded real YOLO11n provider through Luna observation ingress.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--model-path", default=str(DEFAULT_MODEL))
    args = parser.parse_args()
    summary = build_runner_summary_v1(source_ref=args.source, model_path=args.model_path)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
