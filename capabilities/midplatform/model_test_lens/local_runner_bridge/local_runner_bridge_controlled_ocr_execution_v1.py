# -*- coding: utf-8 -*-
"""Local Runner Bridge — controlled OCR execution entry (governance-gated)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_job_store_v1 import (
    new_job_id,
    save_job,
    update_job_status,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    job_output_dir,
    resolve_path,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.runners.ocr_smoke_runner_v1 import (
    run_ocr_smoke_runner,
)
from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_runner_sandbox_v1 import (
    build_ocr_runner_error_candidate,
)

PHASE_REF = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_image_path(image_ref: str) -> Optional[Path]:
    if not image_ref:
        return None
    if image_ref.startswith("local-file://"):
        image_ref = image_ref[len("local-file://") :]
    for cand in (Path(image_ref).expanduser(), resolve_path(image_ref)):
        if cand.is_file():
            return cand
    return None


def run_controlled_ocr_job(
    *,
    execution_candidate: Dict[str, Any],
    adapter_input: Dict[str, Any],
    ocr_execution_id: str,
    smoke_mode: str = "normal",
) -> Dict[str, Any]:
    cec_id = execution_candidate.get("ocr_execution_candidate_id", "unknown")
    trace = execution_candidate.get("trace_chain") or []
    region_id = execution_candidate.get("source_region_id", "")
    image_ref = adapter_input.get("source_image_ref") or ""
    crop_ref = adapter_input.get("region_crop_ref", "")

    if not crop_ref and not image_ref:
        return {
            "ok": False,
            "error_type": "invalid_crop",
            "error_stage": "runner_bridge",
            "error_reason": "region_crop_ref_missing",
            "ocr_runner_error_candidate": build_ocr_runner_error_candidate(
                "invalid_crop",
                execution_candidate_id=cec_id,
                reason="region_crop_ref_missing",
                execution_id=ocr_execution_id,
                trace_chain=trace,
            ),
        }

    image_path = _resolve_image_path(image_ref)
    if not image_path:
        return {
            "ok": False,
            "error_type": "invalid_crop",
            "error_stage": "runner_bridge",
            "error_reason": "source_image_not_found",
            "ocr_runner_error_candidate": build_ocr_runner_error_candidate(
                "invalid_crop",
                execution_candidate_id=cec_id,
                reason="source_image_not_found",
                execution_id=ocr_execution_id,
                trace_chain=trace,
            ),
        }

    job_id = new_job_id()
    out_dir = job_output_dir(job_id)
    job = {
        "job_id": job_id,
        "status": "running",
        "status_reason": "controlled_ocr_execution_start",
        "created_at": _now(),
        "updated_at": _now(),
        "phase_ref": PHASE_REF,
        "controlled_execution": True,
        "ocr_runner_execution": True,
        "ocr_execution_id": ocr_execution_id,
        "source_ocr_execution_candidate_id": cec_id,
        "adapter_input": adapter_input,
        "trace_chain": trace,
        "requested_model_category": "ocr",
        "requested_model_id": "ocr_smoke_runner",
        "runner_type": "ocr_smoke",
        "candidate_output_only": True,
        "asset_manifest": {
            "local_path": str(image_path),
            "region_id": region_id,
            "crop_ref": crop_ref,
        },
    }
    save_job(job)

    runner_result = run_ocr_smoke_runner(
        image_path=image_path,
        output_dir=out_dir,
        region_id=region_id,
        smoke_mode=smoke_mode,
        crop_ref=crop_ref,
    )

    final_status = runner_result.get("status", "failed")
    update_job_status(
        job_id,
        "completed" if final_status == "completed" else "failed_no_boundary_violation",
        runner_result.get("status_reason", ""),
        runner_result=runner_result,
        controlled_execution_id=ocr_execution_id,
        source_execution_candidate_id=cec_id,
    )

    return {
        "ok": final_status == "completed",
        "job_id": job_id,
        "runner_result": runner_result,
        "ocr_execution_id": ocr_execution_id,
        "controlled_execution": True,
        "candidate_output_only": True,
        "ocr_runner_execution": True,
    }


def run_controlled_ocr_execution_api(body: Dict[str, Any]) -> tuple[int, Dict[str, Any]]:
    """HTTP API handler for POST /api/v1/controlled-execution/ocr/run."""
    from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_controlled_execution_runtime_v1 import (
        execute_controlled_ocr,
    )

    candidate = body.get("execution_candidate")
    if not candidate:
        return 400, {"error": "execution_candidate_required", "ok": False}
    if body.get("ui_direct_call"):
        return 403, {"error": "ui_direct_ocr_runner_call_forbidden", "ok": False}

    result = execute_controlled_ocr(
        candidate,
        smoke_mode=body.get("smoke_mode", "normal"),
        environment=body.get("environment", "localhost_8787"),
        bridge_fn=None,
    )
    code = 200 if result.get("ok") else 422
    return code, result
