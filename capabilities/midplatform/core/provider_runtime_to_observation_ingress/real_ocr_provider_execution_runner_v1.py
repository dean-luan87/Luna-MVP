"""User-terminal Runner for one real RapidOCR invocation through Luna cognition."""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any, Dict

from .engine_v1 import _jsonable
from .real_ocr_provider_execution_engine_v1 import RealOCRProviderExecutionEngineV1
from .types_v1 import ProviderObservationIngressCaseV1


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for candidate in (path, *path.parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "_eval_out/real_ocr_provider_execution_integration_v1"
DEFAULT_SOURCE = ROOT / "capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png"


def _case() -> ProviderObservationIngressCaseV1:
    return ProviderObservationIngressCaseV1(
        case_id="REAL_PROVIDER_EXECUTION_OCR",
        title="one bounded local RapidOCR result enters cognition",
        capability_kind="OCR_TEXT_EVIDENCE",
        capability_ref="text_recognition",
        modality="OCR",
        input_source_ref=str(DEFAULT_SOURCE),
        execution_instance_ref=f"provider-runtime:real-ocr:{uuid.uuid4().hex[:12]}",
        information_need_ref="need:read-visible-text",
        required_information_refs=("need:read-visible-text",),
        available_information_refs=(),
        context_ref="context:runtime:ocr-real",
        intent_ref="intent:runtime:read-visible-text",
        task_ref="task:observe-text",
        goal_ref="goal:read-visible-text",
        concern_ref="concern:visible-text",
        role_refs=("role:observer",),
        field_refs=("field:real-image:ocr-v1",),
        relation_refs=("relation:source-to-text-candidate",),
        source_ref=str(DEFAULT_SOURCE),
        raw_result_ref="provider-native-output:pending",
        expected_evidence_kinds=("text_candidate",),
        temporal_ref="time:runtime:ocr-real",
    )


def _summary(result: Dict[str, Any], source_ref: str) -> Dict[str, Any]:
    native = result.get("provider") or (result.get("details") or {}).get("provider_native_result") or {}
    provider_result = result.get("provider_result")
    request = result.get("provider_request")
    details = result.get("details") or {}
    native_candidates = native.get("raw_text_candidates") if isinstance(native, dict) else []
    return {
        "phase": "Phase-P1-Luna-Real-OCR-Provider-Execution-Integration-v1-001",
        "execution_mode": "LIVE_RUNTIME",
        "selected_provider": "ocr_v1",
        "selected_provider_ref": request.provider_ref if request else None,
        "provider_family": "ocr",
        "source_ref": source_ref,
        "observation_demand_ref": request.observation_demand_ref if request else None,
        "capability_requirement_ref": request.capability_requirement_ref if request else result.get("capability_requirement_ref"),
        "normalized_provider_requirement_ref": details.get("normalized_provider_requirement_ref"),
        "capability_ref": request.capability_ref if request else None,
        "provider_ref": request.provider_ref if request else None,
        "model_ref": request.model_ref if request else None,
        "native_provider_id": native.get("provider_id") if isinstance(native, dict) else None,
        "native_model_config_id": native.get("model_config_id") if isinstance(native, dict) else None,
        "provider_request_ref": request.provider_request_ref if request else None,
        "provider_result_ref": provider_result.provider_result_ref if provider_result else None,
        "execution_instance_ref": request.execution_instance_ref if request else None,
        "provider_runtime_request": _jsonable(request) if request else None,
        "provider_real_execution_attempted": bool(result.get("provider_real_execution_attempted")),
        "provider_real_execution_verified": bool(result.get("provider_real_execution_verified")),
        "provider_invoked": bool(result.get("provider_invoked")),
        "model_invoked": bool(result.get("model_invoked")),
        "provider_status": provider_result.status if provider_result else None,
        "empty_result": bool(provider_result.empty_result) if provider_result else False,
        "provider_native_result": _jsonable(native) if native else None,
        "provider_runtime_result": _jsonable(provider_result) if provider_result else None,
        "runtime_observation_ref": result.get("runtime_observation_ref"),
        "gateway_admission_ref": result.get("gateway_admission_ref"),
        "evidence_refs": list(result.get("evidence_refs") or ()),
        "recognized_text_candidates": native_candidates if isinstance(native_candidates, list) else [],
        "a_route_execution_ref": result.get("a_route_execution_ref"),
        "cognitive_state_reached": bool(
            any(
                item.get("stage_id") == "COGNITIVE_STATE"
                for item in (details.get("a_route") or {}).get("stage_results", ())
                if isinstance(item, dict)
            )
        ),
        "sufficiency_ref": result.get("sufficiency_ref"),
        "sufficiency_status": result.get("sufficiency_status"),
        "information_gap_ref": result.get("information_gap_ref"),
        "stop_ref": result.get("stop_ref"),
        "recorded_provider_result_used": False,
        "forbidden_behaviors": {
            "decision_execution": False,
            "task_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "device_control": False,
            "field_mutation": bool(native.get("field_mutation", False)) if isinstance(native, dict) else False,
            "world_truth_declared": bool(native.get("truth_declared", False)) if isinstance(native, dict) else False,
        },
        "trace_refs": list(request.trace_refs) if request else [],
        "provenance_refs": list(request.provenance_refs) if request else [],
        "details": details,
        "validation_errors": list(result.get("errors") or ()),
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def build_runner_summary_v1(*, source_ref: str = str(DEFAULT_SOURCE)) -> Dict[str, Any]:
    result = RealOCRProviderExecutionEngineV1().run(_case(), source_ref=source_ref)
    return _summary(result, source_ref)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded real RapidOCR provider through Luna observation ingress.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    args = parser.parse_args()
    summary = build_runner_summary_v1(source_ref=args.source)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
