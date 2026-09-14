# -*- coding: utf-8 -*-
"""OCR controlled execution runtime — sandbox → bridge → envelope or error."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_controlled_execution_records_v1 import (
    build_ocr_execution_record,
    build_ocr_result_layer_record,
)
from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_runner_sandbox_v1 import (
    RUNNER_NAME,
    RUNNER_VERSION,
    build_ocr_result_envelope,
    build_ocr_runner_error_candidate,
    prepare_ocr_execution,
    validate_ocr_runner_output,
)

PHASE_REF = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cec_id(candidate: Dict[str, Any]) -> str:
    return candidate.get("ocr_execution_candidate_id", "unknown")


def _reject(
    candidate: Dict[str, Any],
    error_type: str,
    reason: str,
    *,
    execution_id: str = "rex_ocr_rejected",
) -> Dict[str, Any]:
    cec = _cec_id(candidate)
    trace = candidate.get("trace_chain") or []
    error = build_ocr_runner_error_candidate(
        error_type,
        execution_candidate_id=cec,
        reason=reason,
        execution_id=execution_id,
        trace_chain=trace,
    )
    record = build_ocr_execution_record(
        ocr_execution_id=execution_id,
        source_ocr_execution_candidate_id=cec,
        runner_name=RUNNER_NAME,
        runner_version=RUNNER_VERSION,
        status="rejected",
        input_ref=candidate.get("input_crop_ref", ""),
        error_ref=error.get("error_candidate_id", ""),
        trace_chain=trace,
        start_time=_now(),
        end_time=_now(),
    )
    return {
        "ok": False,
        "phase_ref": PHASE_REF,
        "ocr_execution_record": record,
        "ocr_runner_error_candidate": error,
        "ocr_result_envelope": None,
        "result_envelope_record": None,
        "ocr_runner_execution": False,
    }


def execute_controlled_ocr(
    execution_candidate: Dict[str, Any],
    *,
    smoke_mode: str = "normal",
    environment: str = "localhost_8787",
    bridge_fn: Optional[Callable[..., Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    start = _now()
    prepared = prepare_ocr_execution(execution_candidate, environment=environment)
    if not prepared.get("ok"):
        err = prepared.get("error") or {}
        etype = err.get("error_type", "route_mismatch")
        return _reject(
            execution_candidate,
            etype,
            err.get("error_reason", "sandbox_rejected"),
            execution_id=prepared.get("ocr_execution_id", "rex_ocr_rejected"),
        )

    oexec_id = prepared["ocr_execution_id"]
    cec = _cec_id(execution_candidate)
    adapter = prepared["adapter_input"]
    trace = prepared.get("trace_chain") or []
    region_id = execution_candidate.get("source_region_id", "")
    image_ref = adapter.get("source_image_ref", "")

    if bridge_fn is None:
        from capabilities.midplatform.model_test_lens.local_runner_bridge import (
            local_runner_bridge_controlled_ocr_execution_v1 as bridge_ocr,
        )

        bridge_result = bridge_ocr.run_controlled_ocr_job(
            execution_candidate=execution_candidate,
            adapter_input=adapter,
            ocr_execution_id=oexec_id,
            smoke_mode=smoke_mode,
        )
    else:
        bridge_result = bridge_fn(
            execution_candidate=execution_candidate,
            adapter_input=adapter,
            ocr_execution_id=oexec_id,
            smoke_mode=smoke_mode,
        )

    if not bridge_result.get("ok"):
        runner_result = bridge_result.get("runner_result") or {}
        if runner_result.get("status") == "timeout":
            etype = "timeout"
        elif bridge_result.get("error_type") == "invalid_crop":
            etype = "invalid_crop"
        else:
            etype = bridge_result.get("error_type", "runner_unavailable")
        error = bridge_result.get("ocr_runner_error_candidate") or build_ocr_runner_error_candidate(
            etype,
            execution_candidate_id=cec,
            reason=bridge_result.get("error_reason", "bridge_failed"),
            execution_id=oexec_id,
            trace_chain=trace,
            recoverable=etype == "timeout",
        )
        record = build_ocr_execution_record(
            ocr_execution_id=oexec_id,
            source_ocr_execution_candidate_id=cec,
            runner_name=RUNNER_NAME,
            runner_version=RUNNER_VERSION,
            status="failed",
            input_ref=adapter.get("region_crop_ref", image_ref),
            error_ref=error.get("error_candidate_id", ""),
            trace_chain=trace,
            start_time=start,
            end_time=_now(),
        )
        return {
            "ok": False,
            "phase_ref": PHASE_REF,
            "ocr_execution_record": record,
            "ocr_runner_error_candidate": error,
            "ocr_result_envelope": None,
            "result_envelope_record": None,
            "ocr_runner_execution": True,
        }

    runner_output = bridge_result.get("runner_result") or {}
    schema_err = validate_ocr_runner_output(runner_output)
    if schema_err:
        error = build_ocr_runner_error_candidate(
            "invalid_output_schema",
            execution_candidate_id=cec,
            reason=schema_err,
            execution_id=oexec_id,
            trace_chain=trace,
        )
        record = build_ocr_execution_record(
            ocr_execution_id=oexec_id,
            source_ocr_execution_candidate_id=cec,
            runner_name=RUNNER_NAME,
            runner_version=RUNNER_VERSION,
            status="failed",
            input_ref=adapter.get("region_crop_ref", image_ref),
            error_ref=error.get("error_candidate_id", ""),
            trace_chain=trace,
            start_time=start,
            end_time=_now(),
        )
        return {
            "ok": False,
            "phase_ref": PHASE_REF,
            "ocr_execution_record": record,
            "ocr_runner_error_candidate": error,
            "ocr_result_envelope": None,
            "result_envelope_record": None,
            "ocr_runner_execution": True,
        }

    text_list = runner_output.get("text_candidate_list") or []
    if not text_list and smoke_mode == "empty_text":
        error = build_ocr_runner_error_candidate(
            "empty_text",
            execution_candidate_id=cec,
            reason="empty_text_policy",
            execution_id=oexec_id,
            trace_chain=trace,
            recoverable=True,
        )
        record = build_ocr_execution_record(
            ocr_execution_id=oexec_id,
            source_ocr_execution_candidate_id=cec,
            runner_name=RUNNER_NAME,
            runner_version=RUNNER_VERSION,
            status="failed",
            input_ref=adapter.get("region_crop_ref", image_ref),
            error_ref=error.get("error_candidate_id", ""),
            trace_chain=trace,
            start_time=start,
            end_time=_now(),
        )
        return {
            "ok": False,
            "phase_ref": PHASE_REF,
            "ocr_execution_record": record,
            "ocr_runner_error_candidate": error,
            "ocr_result_envelope": None,
            "result_envelope_record": None,
            "ocr_runner_execution": True,
            "empty_text_not_fact": True,
        }

    ocr_env = build_ocr_result_envelope(
        {"ocr_execution_id": oexec_id, "source_ocr_execution_candidate_id": cec, "trace_chain": trace},
        runner_output,
        region_id=region_id,
        image_ref=image_ref,
        trace_chain=trace,
    )
    result_record = build_ocr_result_layer_record(ocr_result_envelope=ocr_env)
    exec_record = build_ocr_execution_record(
        ocr_execution_id=oexec_id,
        source_ocr_execution_candidate_id=cec,
        runner_name=runner_output.get("model_name", RUNNER_NAME),
        runner_version=runner_output.get("model_version", RUNNER_VERSION),
        status="completed",
        input_ref=adapter.get("region_crop_ref", image_ref),
        output_ref=ocr_env.get("output_payload_ref", ""),
        trace_chain=ocr_env.get("trace_chain", trace),
        start_time=start,
        end_time=_now(),
    )
    return {
        "ok": True,
        "phase_ref": PHASE_REF,
        "ocr_runner_execution": True,
        "ocr_execution_record": exec_record,
        "ocr_result_envelope": ocr_env,
        "result_envelope_record": result_record,
        "ocr_runner_error_candidate": None,
        "completed_not_fact": True,
        "job_id": bridge_result.get("job_id"),
    }
