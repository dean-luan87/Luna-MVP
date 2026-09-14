# -*- coding: utf-8 -*-
"""Local Runner Bridge — controlled MobileSAM execution entry (governance-gated)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_job_store_v1 import (
    new_job_id,
    save_job,
    update_job_status,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    job_output_dir,
    resolve_path,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.runners.mobilesam_image_runner_v1 import (
    run_mobilesam_image_runner,
)
from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.controlled_execution_records_v1 import (
    build_runner_error_candidate,
)

PHASE_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_image_path(image_ref: str) -> Optional[Path]:
    if not image_ref:
        return None
    if image_ref.startswith("local-file://"):
        image_ref = image_ref[len("local-file://") :]
    candidates = [Path(image_ref).expanduser(), resolve_path(image_ref)]
    for cand in candidates:
        if cand.is_file():
            return cand
    return None


def run_controlled_mobilesam_job(
    *,
    execution_candidate: Dict[str, Any],
    adapter_input: Dict[str, Any],
    execution_id: str,
    image_ref: str,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    """Run MobileSAM via bridge with controlled execution metadata attached to job."""
    crec_id = execution_candidate.get("execution_candidate_id", "unknown")
    trace = execution_candidate.get("trace_chain") or []
    image_path = _resolve_image_path(image_ref)
    if not image_path:
        return {
            "ok": False,
            "error_type": "invalid_crop",
            "error_stage": "runner_bridge",
            "error_reason": "image_ref_not_found",
            "runner_error_candidate": build_runner_error_candidate(
                execution_id=execution_id,
                error_type="invalid_crop",
                error_stage="runner_bridge",
                error_reason="image_ref_not_found",
                source_execution_candidate_id=crec_id,
                trace_chain=trace,
            ),
        }

    job_id = new_job_id()
    out_dir = job_output_dir(job_id)
    job = {
        "job_id": job_id,
        "status": "running",
        "status_reason": "controlled_execution_start",
        "created_at": _now(),
        "updated_at": _now(),
        "phase_ref": PHASE_REF,
        "controlled_execution": True,
        "runner_execution_id": execution_id,
        "source_execution_candidate_id": crec_id,
        "adapter_input": adapter_input,
        "trace_chain": trace,
        "requested_model_category": "segmentation",
        "requested_model_id": "mobile_sam",
        "runner_type": "segmentation_mobile_sam",
        "candidate_output_only": True,
        "asset_manifest": {
            "local_path": str(image_path),
            "requested_model_id": "mobile_sam",
            "intended_test_type": "segmentation",
        },
    }
    save_job(job)

    try:
        runner_result = run_mobilesam_image_runner(
            image_path=image_path,
            output_dir=out_dir,
            job_id=job_id,
            file_name=str(image_path.name),
        )
    except Exception as exc:  # noqa: BLE001 — record as runner_error_candidate
        runner_result = {
            "status": "failed_no_boundary_violation",
            "status_reason": f"runner_exception:{exc}",
            "candidate_outputs": [],
        }

    # timeout_ms reserved for future watchdog; documented in sandbox policy
    runner_path = out_dir / "runner_result.json"
    runner_path.write_text(json.dumps(runner_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    final_status = runner_result.get("status", "failed_no_boundary_violation")
    update_job_status(
        job_id,
        "completed" if final_status == "completed" else "failed_no_boundary_violation",
        runner_result.get("status_reason", ""),
        runner_result=runner_result,
        controlled_execution_id=execution_id,
        source_execution_candidate_id=crec_id,
    )

    return {
        "ok": final_status == "completed",
        "job_id": job_id,
        "runner_result": runner_result,
        "runner_execution_id": execution_id,
        "controlled_execution": True,
        "candidate_output_only": True,
    }


def run_controlled_execution_api(body: Dict[str, Any]) -> tuple[int, Dict[str, Any]]:
    """HTTP API handler body for POST /api/v1/controlled-execution/run."""
    from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.runner_sandbox.runner_sandbox_executor_v1 import (
        execute_controlled_mobilesam,
    )

    candidate = body.get("execution_candidate")
    image_ref = body.get("image_ref") or (candidate or {}).get("input_payload_ref", "")
    if not candidate:
        return 400, {"error": "execution_candidate_required", "ok": False}
    if not image_ref:
        return 400, {"error": "image_ref_required", "ok": False}

    result = execute_controlled_mobilesam(
        candidate,
        image_ref=image_ref,
        environment=body.get("environment", "test_environment"),
        timeout_ms=body.get("timeout_ms"),
    )
    code = 200 if result.get("ok") else 422
    return code, result
