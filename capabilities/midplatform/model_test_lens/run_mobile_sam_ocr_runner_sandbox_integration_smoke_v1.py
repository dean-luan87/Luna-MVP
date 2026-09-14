# -*- coding: utf-8 -*-
"""MobileSAM → OCR Runner Sandbox integration smoke — cases A-F."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/midplatform/model_test_lens").is_dir():
            return base
    return _REPO_ROOT


if str(_detect_repo_root()) not in sys.path:
    sys.path.insert(0, str(_detect_repo_root()))

from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_controlled_execution_runtime_v1 import (  # noqa: E402
    execute_controlled_ocr,
)

IMAGE_REF = (
    "local-file://capabilities/test_assets/p1/ocr/"
    "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png"
)
CEC_ID = "ocec_ocr_region_sign_001"


def _base_candidate(**overrides: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "ocr_execution_candidate_id": CEC_ID,
        "source_ocr_invocation_request_id": "oir_ocr_region_sign_001_001",
        "source_ocr_task_candidate_id": "T-ocr-region_sign_001",
        "source_region_id": "region_sign_001",
        "source_result_candidate_id": "rc_seg_region_sign_001",
        "source_analysis_record_id": "mpa_region_sign_001",
        "requested_runner_type": "OCR",
        "execution_mode": "manual_controlled",
        "execution_status": "ready_for_execution_review",
        "input_crop_ref": IMAGE_REF + "#crop/region_sign_001",
        "input_region_geometry_ref": "region://region_sign_001",
        "ocr_target_reason": "疑似文字区域，建议 OCR 候选复核（中台调度）",
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
        "trace_chain": [
            {"stage": "result_candidate", "ref": "rc_seg_region_sign_001"},
            {"stage": "midplatform_analysis", "ref": "mpa_region_sign_001"},
            {"stage": "ocr_task_candidate", "ref": "T-ocr-region_sign_001"},
            {"stage": "ocr_invocation_request", "ref": "oir_ocr_region_sign_001_001"},
            {"stage": "ocr_admission", "ref": "oiar_oir_001"},
            {"stage": "ocr_controlled_execution_candidate", "ref": CEC_ID},
        ],
    }
    base.update(overrides)
    return base


def _mock_bridge_ok(**kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": True,
        "job_id": "job_ocr_smoke_001",
        "runner_result": {
            "status": "completed",
            "model_name": "ocr_smoke_runner",
            "model_version": "ocr_smoke_v1",
            "smoke_runtime": True,
            "text_candidate_list": [
                {"text_candidate": "[smoke] line_1", "confidence": 0.8, "not_fact": True}
            ],
            "confidence": 0.8,
            "output_payload_ref": "ocr_output://smoke_001",
        },
    }


def _mock_bridge_invalid(**_kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": True,
        "job_id": "job_ocr_smoke_bad",
        "runner_result": {
            "status": "completed",
            "fact_text": "禁止",
            "text_candidate_list": [],
        },
    }


def _mock_bridge_invalid_crop(**_kwargs: Any) -> Dict[str, Any]:
    return {
        "ok": False,
        "error_type": "invalid_crop",
        "error_reason": "source_image_not_found",
    }


def run_smoke() -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []

    # Case A — Happy path
    happy = execute_controlled_ocr(_base_candidate(), bridge_fn=_mock_bridge_ok)
    cases.append({
        "case": "A_happy_path",
        "passed": happy.get("ok") is True
        and happy.get("ocr_execution_record", {}).get("status") == "completed"
        and happy.get("ocr_result_envelope") is not None
        and happy.get("completed_not_fact") is True
        and happy.get("ocr_result_envelope", {}).get("not_fact") is True
        and happy.get("ocr_result_envelope", {}).get("needs_fact_admission") is True,
    })

    # Case B — Cancelled
    cancelled = execute_controlled_ocr(
        _base_candidate(execution_status="cancelled"),
        bridge_fn=_mock_bridge_ok,
    )
    cases.append({
        "case": "B_cancelled_candidate",
        "passed": cancelled.get("ok") is False
        and cancelled.get("ocr_runner_error_candidate") is not None
        and cancelled.get("ocr_result_envelope") is None,
    })

    # Case C — Missing trace
    no_trace = execute_controlled_ocr(
        _base_candidate(trace_chain=[]),
        bridge_fn=_mock_bridge_ok,
    )
    cases.append({
        "case": "C_missing_trace",
        "passed": no_trace.get("ok") is False
        and no_trace.get("ocr_result_envelope") is None,
    })

    # Case D — Invalid crop
    bad_crop = execute_controlled_ocr(
        _base_candidate(
            input_crop_ref="local-file://capabilities/test_assets/p1/ocr/nonexistent_crop_v1.png#crop/x"
        ),
        bridge_fn=_mock_bridge_invalid_crop,
    )
    cases.append({
        "case": "D_invalid_crop",
        "passed": bad_crop.get("ok") is False
        and bad_crop.get("ocr_runner_error_candidate") is not None,
    })

    # Case E — Invalid output schema
    invalid_out = execute_controlled_ocr(_base_candidate(), bridge_fn=_mock_bridge_invalid)
    cases.append({
        "case": "E_invalid_output",
        "passed": invalid_out.get("ok") is False
        and invalid_out.get("ocr_runner_error_candidate") is not None
        and invalid_out.get("ocr_result_envelope") is None,
    })

    # Case F — Empty text
    empty = execute_controlled_ocr(
        _base_candidate(),
        smoke_mode="empty_text",
        bridge_fn=lambda **kw: {
            "ok": True,
            "runner_result": {
                "status": "completed",
                "text_candidate_list": [],
                "confidence": 0.0,
            },
        },
    )
    cases.append({
        "case": "F_empty_text",
        "passed": empty.get("ok") is False
        and empty.get("ocr_runner_error_candidate", {}).get("error_type") == "empty_text"
        and empty.get("empty_text_not_fact") is True,
    })

    passed = sum(1 for c in cases if c["passed"])
    return {
        "phase_ref": (
            "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
        ),
        "cases": cases,
        "case_count": len(cases),
        "passed_count": passed,
        "all_passed": passed == len(cases),
    }


def main() -> int:
    out_dir = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_v1_smoke_v0"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    result = run_smoke()
    out_path = out_dir / "mobile_sam_ocr_runner_sandbox_integration_smoke_v1.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
