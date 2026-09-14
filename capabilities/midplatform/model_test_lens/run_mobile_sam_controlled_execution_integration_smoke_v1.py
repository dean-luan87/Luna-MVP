# -*- coding: utf-8 -*-
"""MobileSAM controlled execution integration smoke tests — four validation chains."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.runner_sandbox.runner_sandbox_executor_v1 import (  # noqa: E402
    execute_controlled_mobilesam,
)


def _base_candidate(**overrides: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "execution_candidate_id": "crec_segmentation_entity_023_001",
        "source_invocation_request_id": "rir_detection_entity_023_001",
        "source_admission_result_id": "riar_rir_detection_entity_023_001_001",
        "source_runner_task_candidate_id": "rtc_entity_023_001",
        "source_region_id": "entity_023",
        "source_attention_record_id": "oar_entity_023",
        "requested_runner_type": "Segmentation",
        "model_id": "mobile_sam",
        "runner_config_ref": "runner_config/mobile_sam_manual_controlled_v1.json",
        "execution_status": "ready_for_execution_review",
        "admission_decision_at_create": "admitted",
        "input_payload_ref": "local-file://capabilities/test_assets/p1/mobile_sam/mobile_sam_real_local_image_street_scene_v1.png",
        "trace_chain": [
            {"stage": "segmentation_region", "ref": "entity_023"},
            {"stage": "observation_attention_record", "ref": "oar_entity_023"},
            {"stage": "followup_model_route_candidate", "ref": "fmrc_001"},
            {"stage": "runner_task_candidate", "ref": "rtc_entity_023_001"},
            {"stage": "runner_invocation_request", "ref": "rir_detection_entity_023_001"},
            {"stage": "runner_invocation_admission", "ref": "riar_rir_detection_entity_023_001_001"},
            {"stage": "controlled_runner_execution_candidate", "ref": "crec_segmentation_entity_023_001"},
        ],
    }
    base.update(overrides)
    return base


def _mock_runner_ok(**_kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": True,
        "job_id": "job_smoke_001",
        "runner_result": {
            "status": "completed",
            "candidate_outputs": [{"mask_ref": "artifact://mask_001.png", "score": 0.92}],
        },
    }


def _mock_runner_null_mask(**_kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": True,
        "job_id": "job_smoke_002",
        "runner_result": {
            "status": "completed",
            "candidate_outputs": [{"mask_ref": None, "score": 0.0}],
        },
    }


def _mock_runner_timeout(**_kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": False,
        "job_id": "job_smoke_003",
        "runner_result": {"status": "timeout", "status_reason": "inference_timeout"},
        "error_type": "timeout",
        "error_stage": "mobilesam_inference",
        "error_reason": "inference_timeout",
        "runner_error_candidate": {
            "envelope_type": "runner_error_candidate",
            "error_type": "timeout",
            "error_stage": "mobilesam_inference",
            "not_fact": True,
        },
    }


def run_smoke() -> Dict[str, Any]:
    image_ref = "local-file://capabilities/test_assets/p1/mobile_sam/mobile_sam_real_local_image_street_scene_v1.png"
    cases: List[Dict[str, Any]] = []

    # 1. Happy path (mock runner)
    happy = execute_controlled_mobilesam(
        _base_candidate(),
        image_ref=image_ref,
        runner_fn=_mock_runner_ok,
    )
    cases.append({
        "case": "happy_path",
        "passed": happy.get("ok") is True
        and happy.get("runner_execution_record", {}).get("status") == "completed"
        and happy.get("result_envelope_record") is not None
        and happy.get("segmentation_result_envelope") is not None
        and happy.get("completed_not_fact") is True,
    })

    # 2a. Cancelled candidate
    cancelled = execute_controlled_mobilesam(
        _base_candidate(execution_status="cancelled"),
        image_ref=image_ref,
        runner_fn=_mock_runner_ok,
    )
    cases.append({
        "case": "reject_cancelled_candidate",
        "passed": cancelled.get("ok") is False
        and cancelled.get("runner_execution_record", {}).get("status") == "rejected"
        and cancelled.get("runner_error_candidate") is not None,
    })

    # 2b. Missing admission
    no_admission = execute_controlled_mobilesam(
        _base_candidate(source_admission_result_id=""),
        image_ref=image_ref,
        runner_fn=_mock_runner_ok,
    )
    cases.append({
        "case": "reject_missing_admission",
        "passed": no_admission.get("ok") is False,
    })

    # 2c. Missing trace
    no_trace = execute_controlled_mobilesam(
        _base_candidate(trace_chain=[], source_attention_record_id=""),
        image_ref=image_ref,
        runner_fn=_mock_runner_ok,
    )
    cases.append({
        "case": "reject_missing_trace",
        "passed": no_trace.get("ok") is False,
    })

    # 3a. Timeout
    timeout = execute_controlled_mobilesam(
        _base_candidate(),
        image_ref=image_ref,
        runner_fn=_mock_runner_timeout,
    )
    cases.append({
        "case": "error_timeout",
        "passed": timeout.get("ok") is False
        and timeout.get("runner_error_candidate") is not None,
    })

    # 3b. Null mask
    null_mask = execute_controlled_mobilesam(
        _base_candidate(),
        image_ref=image_ref,
        runner_fn=_mock_runner_null_mask,
    )
    cases.append({
        "case": "error_null_mask",
        "passed": null_mask.get("ok") is False
        and null_mask.get("runner_error_candidate") is not None
        and null_mask.get("segmentation_result_envelope") is None,
    })

    passed = sum(1 for c in cases if c["passed"])
    result = {
        "phase_ref": "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002",
        "cases": cases,
        "passed": passed,
        "total": len(cases),
        "all_passed": passed == len(cases),
    }
    out = _REPO_ROOT / "_tmp_eval_out" / (
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)
    out_file = out / "mobile_sam_controlled_execution_integration_smoke_v1.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result["output_file"] = str(out_file)
    return result


def main() -> int:
    r = run_smoke()
    print(json.dumps({"all_passed": r["all_passed"], "passed": r["passed"], "total": r["total"]}, indent=2))
    return 0 if r["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
