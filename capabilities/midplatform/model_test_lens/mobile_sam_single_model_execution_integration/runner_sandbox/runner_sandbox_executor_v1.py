# -*- coding: utf-8 -*-
"""Runner Sandbox Executor v1 — controlled MobileSAM execution through Local Runner Bridge."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.controlled_execution_records_v1 import (
    build_result_envelope_record,
    build_runner_error_candidate,
    build_runner_execution_record,
)
from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.runner_sandbox.runner_sandbox_v1 import (
    build_segmentation_result_envelope,
    prepare_execution,
)

PHASE_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002"
)
MODEL_VERSION = "mobile_sam_v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _reject(
    *,
    execution_candidate: Dict[str, Any],
    error_type: str,
    error_stage: str,
    reason: str,
    execution_id: str = "rex_mobile_sam_rejected",
) -> Dict[str, Any]:
    crec_id = execution_candidate.get("execution_candidate_id", "unknown")
    trace = execution_candidate.get("trace_chain") or []
    error = build_runner_error_candidate(
        execution_id=execution_id,
        error_type=error_type,
        error_stage=error_stage,
        error_reason=reason,
        source_execution_candidate_id=crec_id,
        trace_chain=trace,
        recoverable=False,
    )
    record = build_runner_execution_record(
        execution_id=execution_id,
        source_execution_candidate_id=crec_id,
        model_name="MobileSAM",
        model_version=MODEL_VERSION,
        status="rejected",
        input_ref=execution_candidate.get("input_payload_ref", ""),
        output_ref="",
        trace_chain=trace,
        start_time=_now(),
        end_time=_now(),
    )
    return {
        "ok": False,
        "phase_ref": PHASE_REF,
        "runner_execution_record": record,
        "runner_error_candidate": error,
        "result_envelope_record": None,
        "segmentation_result_envelope": None,
    }


def _parse_runner_output(
    runner_result: Dict[str, Any],
    *,
    execution_id: str,
    execution_candidate: Dict[str, Any],
    job_id: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Return (segmentation_envelope, error_candidate)."""
    crec_id = execution_candidate["execution_candidate_id"]
    region_id = execution_candidate.get("source_region_id", "")
    trace = execution_candidate.get("trace_chain") or []

    status = runner_result.get("status")
    if status == "timeout":
        return None, build_runner_error_candidate(
            execution_id=execution_id,
            error_type="timeout",
            error_stage="mobilesam_inference",
            error_reason=runner_result.get("status_reason", "timeout"),
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
            recoverable=True,
        )

    if status != "completed":
        return None, build_runner_error_candidate(
            execution_id=execution_id,
            error_type="model_output_invalid",
            error_stage="mobilesam_inference",
            error_reason=runner_result.get("status_reason", "runner_failed"),
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
        )

    outputs = runner_result.get("candidate_outputs") or []
    if not outputs:
        return None, build_runner_error_candidate(
            execution_id=execution_id,
            error_type="empty_mask_output",
            error_stage="output_envelope",
            error_reason="no_candidate_outputs",
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
        )

    best = outputs[0]
    mask_ref = best.get("mask_ref")
    if mask_ref is None:
        return None, build_runner_error_candidate(
            execution_id=execution_id,
            error_type="model_output_invalid",
            error_stage="output_envelope",
            error_reason="mask_null",
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
        )

    confidence = float(best.get("score", best.get("confidence", 0.0)) or 0.0)
    if mask_ref == "" or (confidence <= 0 and not best.get("mask_present")):
        return None, build_runner_error_candidate(
            execution_id=execution_id,
            error_type="empty_mask_output",
            error_stage="output_envelope",
            error_reason="valid_empty_result_distinct_from_failure",
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
            recoverable=True,
        )

    seg_env = build_segmentation_result_envelope(
        runner_execution_id=execution_id,
        execution_candidate_id=crec_id,
        region_id=region_id,
        mask_ref=str(mask_ref),
        confidence=confidence,
        trace_chain=trace,
        model_version=MODEL_VERSION,
    )
    seg_env["job_ref"] = job_id
    return seg_env, None


def execute_controlled_mobilesam(
    execution_candidate: Dict[str, Any],
    *,
    image_ref: str,
    environment: str = "test_environment",
    runner_fn: Optional[Callable[..., Dict[str, Any]]] = None,
    timeout_ms: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Full controlled execution: sandbox validate → bridge run → envelope or error.
    runner_fn(image_path, output_dir, job_id) injectable for tests.
    """
    start = _now()
    prepared = prepare_execution(execution_candidate, image_ref=image_ref, environment=environment)
    if not prepared.get("ok"):
        err = prepared.get("error") or {}
        return _reject(
            execution_candidate=execution_candidate,
            error_type=err.get("error_type", "sandbox_policy_violation"),
            error_stage="sandbox_validation",
            reason=err.get("error_reason", "sandbox_rejected"),
            execution_id=prepared.get("runner_execution_id", "rex_mobile_sam_rejected"),
        )

    execution_id = prepared["runner_execution_id"]
    crec_id = execution_candidate["execution_candidate_id"]
    trace = prepared.get("trace_chain") or []

    if runner_fn is None:
        from capabilities.midplatform.model_test_lens.local_runner_bridge import (
            local_runner_bridge_controlled_execution_v1 as bridge_ctrl,
        )

        bridge_result = bridge_ctrl.run_controlled_mobilesam_job(
            execution_candidate=execution_candidate,
            adapter_input=prepared["adapter_input"],
            execution_id=execution_id,
            image_ref=image_ref,
            timeout_ms=timeout_ms,
        )
    else:
        bridge_result = runner_fn(
            execution_candidate=execution_candidate,
            adapter_input=prepared["adapter_input"],
            execution_id=execution_id,
            image_ref=image_ref,
        )

    if not bridge_result.get("ok"):
        error = bridge_result.get("runner_error_candidate") or build_runner_error_candidate(
            execution_id=execution_id,
            error_type=bridge_result.get("error_type", "runner_unavailable"),
            error_stage=bridge_result.get("error_stage", "runner_bridge"),
            error_reason=bridge_result.get("error_reason", "bridge_failed"),
            source_execution_candidate_id=crec_id,
            trace_chain=trace,
        )
        record = build_runner_execution_record(
            execution_id=execution_id,
            source_execution_candidate_id=crec_id,
            model_name="MobileSAM",
            model_version=MODEL_VERSION,
            status="failed",
            input_ref=image_ref,
            output_ref="",
            trace_chain=trace,
            start_time=start,
            end_time=_now(),
        )
        return {
            "ok": False,
            "phase_ref": PHASE_REF,
            "runner_execution_record": record,
            "runner_error_candidate": error,
            "result_envelope_record": None,
            "segmentation_result_envelope": None,
        }

    runner_result = bridge_result.get("runner_result") or {}
    job_id = bridge_result.get("job_id", "")
    seg_env, error = _parse_runner_output(
        runner_result,
        execution_id=execution_id,
        execution_candidate=execution_candidate,
        job_id=job_id,
    )

    if error:
        record = build_runner_execution_record(
            execution_id=execution_id,
            source_execution_candidate_id=crec_id,
            model_name="MobileSAM",
            model_version=MODEL_VERSION,
            status="failed",
            input_ref=image_ref,
            output_ref="",
            trace_chain=trace,
            start_time=start,
            end_time=_now(),
        )
        return {
            "ok": False,
            "phase_ref": PHASE_REF,
            "runner_execution_record": record,
            "runner_error_candidate": error,
            "result_envelope_record": None,
            "segmentation_result_envelope": None,
        }

    payload_ref = seg_env.get("mask_ref", "")
    result_record = build_result_envelope_record(
        source_execution_id=execution_id,
        source_execution_candidate_id=crec_id,
        result_type="segmentation_result_envelope",
        payload_ref=payload_ref,
        confidence=float(seg_env.get("confidence", 0.0)),
        trace_chain=trace,
        mask_ref=payload_ref,
    )
    exec_record = build_runner_execution_record(
        execution_id=execution_id,
        source_execution_candidate_id=crec_id,
        model_name="MobileSAM",
        model_version=MODEL_VERSION,
        status="completed",
        input_ref=image_ref,
        output_ref=payload_ref,
        trace_chain=trace,
        start_time=start,
        end_time=_now(),
    )
    return {
        "ok": True,
        "phase_ref": PHASE_REF,
        "runner_execution": True,
        "runner_execution_record": exec_record,
        "result_envelope_record": result_record,
        "segmentation_result_envelope": seg_env,
        "runner_error_candidate": None,
        "job_id": job_id,
        "completed_not_fact": True,
    }


def write_execution_artifacts(
    result: Dict[str, Any],
    output_dir: Path,
) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    refs: Dict[str, str] = {}
    for key in (
        "runner_execution_record",
        "runner_error_candidate",
        "result_envelope_record",
        "segmentation_result_envelope",
    ):
        payload = result.get(key)
        if payload:
            path = output_dir / f"{key}.json"
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            refs[key] = str(path)
    return refs
