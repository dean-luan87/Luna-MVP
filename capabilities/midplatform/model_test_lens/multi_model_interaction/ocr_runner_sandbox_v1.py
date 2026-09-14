# -*- coding: utf-8 -*-
"""OCR Runner Sandbox v1 — controlled OCR execution entry. Test environment only."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_controlled_execution_records_v1 import (
    new_ocr_execution_id,
)
from capabilities.midplatform.model_test_lens.multi_model_interaction.ocr_runner_sandbox_types_v1 import (
    OCR_ADAPTER_FORBIDDEN_INPUTS,
    OCR_ERROR_TYPES,
    SCHEMA_REFS,
)

PHASE_REF = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)
RUNNER_NAME = "ocr_smoke_runner"
RUNNER_VERSION = "ocr_smoke_v1"
BRIDGE_ENDPOINT = "/api/v1/controlled-execution/ocr/run"
ALLOWED_CANDIDATE_STATUSES = ("planned_only", "not_executed", "ready_for_execution_review")
FORBIDDEN_CANDIDATE_STATUSES = ("cancelled", "blocked", "running", "executed", "completed")


def _candidate_id(candidate: Dict[str, Any]) -> str:
    return candidate.get("ocr_execution_candidate_id") or candidate.get("execution_candidate_id", "unknown")


def _forbidden_in_blob(candidate: Dict[str, Any]) -> Optional[str]:
    blob = json.dumps(candidate, ensure_ascii=False).lower()
    patterns = (
        ("confirmed_text", r"confirmed_text|confirmed text"),
        ("fact_label", r"fact_label|fact label"),
        ("confirmed_object_type", r"confirmed_object_type"),
        ("confirmed_sign_type", r"confirmed_sign_type|这是路牌"),
        ("human_correction_as_truth", r"human_correction_as_truth"),
        ("navigation_decision", r"navigation_decision|navigation_instruction"),
        ("mobilesam_prompt_label_as_fact", r"prompt_label_as_fact"),
    )
    for name, pat in patterns:
        if re.search(pat, blob):
            return name
    return None


def validate_trace_chain(candidate: Dict[str, Any]) -> Optional[str]:
    chain = candidate.get("trace_chain") or []
    if len(chain) < 4:
        return "trace_chain_incomplete"
    stages = {item.get("stage"): item.get("ref") for item in chain if item.get("stage")}
    if not stages.get("ocr_task_candidate") and not candidate.get("source_ocr_task_candidate_id"):
        return "trace_missing_ocr_task_candidate"
    if not stages.get("ocr_invocation_request") and not candidate.get("source_ocr_invocation_request_id"):
        return "trace_missing_ocr_invocation_request"
    cec_id = _candidate_id(candidate)
    ocec_ref = stages.get("ocr_controlled_execution_candidate")
    if not ocec_ref or ocec_ref != cec_id:
        return "trace_missing_ocr_controlled_execution_candidate"
    return None


def validate_ocr_execution_candidate(candidate: Dict[str, Any]) -> Optional[str]:
    if not candidate:
        return "orphan_candidate"
    status = candidate.get("execution_status")
    if status in FORBIDDEN_CANDIDATE_STATUSES:
        return f"candidate_{status}"
    if status not in ALLOWED_CANDIDATE_STATUSES:
        return "invalid_execution_status"
    if not candidate.get("source_ocr_invocation_request_id"):
        return "missing_source_ocr_invocation_request_id"
    if not candidate.get("source_ocr_task_candidate_id"):
        return "missing_source_ocr_task_candidate_id"
    if not candidate.get("source_region_id"):
        return "missing_source_region_id"
    if not candidate.get("source_result_candidate_id"):
        return "missing_source_result_candidate_id"
    if not candidate.get("source_analysis_record_id"):
        return "missing_source_analysis_record_id"
    if candidate.get("requested_runner_type") != "OCR":
        return "route_not_ocr"
    if not candidate.get("candidate_only") or not candidate.get("not_fact"):
        return "missing_boundary_flags"
    if candidate.get("needs_fact_admission") is False:
        return "needs_fact_admission_required"
    forbidden = _forbidden_in_blob(candidate)
    if forbidden:
        return f"forbidden_input_{forbidden}"
    trace_err = validate_trace_chain(candidate)
    if trace_err:
        return trace_err
    return None


def build_ocr_adapter_input(candidate: Dict[str, Any]) -> Dict[str, Any]:
    rejection = validate_ocr_execution_candidate(candidate)
    if rejection:
        raise ValueError(rejection)
    crop_ref = candidate.get("input_crop_ref") or candidate.get("region_crop_ref", "")
    image_ref = crop_ref.split("#")[0] if crop_ref else ""
    return {
        "adapter_type": "ocr_adapter_input",
        "source_image_ref": image_ref,
        "source_region_id": candidate.get("source_region_id"),
        "region_crop_ref": crop_ref,
        "region_geometry_ref": candidate.get("input_region_geometry_ref")
        or candidate.get("region_geometry_ref"),
        "source_ocr_execution_candidate_id": _candidate_id(candidate),
        "source_ocr_task_candidate_id": candidate.get("source_ocr_task_candidate_id"),
        "source_analysis_record_id": candidate.get("source_analysis_record_id"),
        "ocr_target_reason": candidate.get("ocr_target_reason", "text_observation_candidate"),
        "trace_chain": candidate.get("trace_chain") or [],
        "candidate_only": True,
        "not_fact": True,
    }


def prepare_ocr_execution(
    candidate: Dict[str, Any],
    *,
    environment: str = "localhost_8787",
) -> Dict[str, Any]:
    rejection = validate_ocr_execution_candidate(candidate)
    cec_id = _candidate_id(candidate)
    if rejection:
        return {
            "ok": False,
            "error": build_ocr_runner_error_candidate(
                "cancelled" if "cancelled" in rejection else "route_mismatch",
                execution_candidate_id=cec_id,
                reason=rejection,
                trace_chain=candidate.get("trace_chain"),
            ),
        }
    adapter_input = build_ocr_adapter_input(candidate)
    oexec_id = new_ocr_execution_id(cec_id)
    trace = list(adapter_input.get("trace_chain") or [])
    trace.append({"stage": "ocr_runner_sandbox", "ref": oexec_id})
    return {
        "ok": True,
        "ocr_execution_id": oexec_id,
        "runner_name": RUNNER_NAME,
        "runner_version": RUNNER_VERSION,
        "adapter_input": adapter_input,
        "bridge_endpoint": BRIDGE_ENDPOINT,
        "timeout_policy_ref": candidate.get("timeout_policy_ref", SCHEMA_REFS["error_candidate"]),
        "environment": environment,
        "trace_chain": trace,
        "candidate_only": True,
        "not_fact": True,
        "ocr_runner_execution": True,
    }


def validate_ocr_runner_output(output: Dict[str, Any]) -> Optional[str]:
    if not output or not isinstance(output, dict):
        return "invalid_output_schema"
    blob = json.dumps(output, ensure_ascii=False).lower()
    if re.search(r"fact_text|confirmed_text|navigation_instruction|confirmed_sign", blob):
        return "forbidden_fact_fields_in_output"
    if "text_candidate_list" not in output and "candidate_outputs" not in output:
        return "missing_text_candidate_list"
    if output.get("fact_text") or output.get("confirmed_text"):
        return "forbidden_fact_fields_in_output"
    return None


def build_ocr_result_envelope(
    execution_record: Dict[str, Any],
    output: Dict[str, Any],
    *,
    region_id: str,
    image_ref: str,
    trace_chain: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    oexec_id = execution_record.get("ocr_execution_id", "")
    cec_id = execution_record.get("source_ocr_execution_candidate_id", "")
    text_list = output.get("text_candidate_list")
    if text_list is None and output.get("candidate_outputs"):
        text_list = [
            {"text_candidate": item.get("text", ""), "confidence": item.get("confidence", 0.0)}
            for item in output.get("candidate_outputs", [])
        ]
    text_list = text_list or []
    confidence = float(output.get("confidence", 0.0) or 0.0)
    if not confidence and text_list:
        confidence = float(text_list[0].get("confidence", 0.5) or 0.5)
    env_id = f"orenv_ocr_{region_id}_{uuid4().hex[:8]}"
    chain = list(trace_chain or execution_record.get("trace_chain") or [])
    chain.append({"stage": "ocr_result_envelope", "ref": env_id})
    return {
        "envelope_type": "ocr_result_envelope",
        "ocr_result_envelope_id": env_id,
        "source_ocr_execution_id": oexec_id,
        "source_ocr_execution_candidate_id": cec_id,
        "source_region_id": region_id,
        "source_image_ref": image_ref,
        "text_candidate_list": text_list,
        "text_region_candidate": output.get("text_region_candidate", {"region_id": region_id}),
        "reading_order_candidate": output.get("reading_order_candidate", []),
        "confidence": confidence,
        "model_name": output.get("model_name", RUNNER_NAME),
        "model_version": output.get("model_version", RUNNER_VERSION),
        "output_payload_ref": output.get("output_payload_ref", f"ocr_output://{env_id}"),
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
        "trace_chain": chain,
        "smoke_runtime": output.get("smoke_runtime", False),
    }


def build_ocr_runner_error_candidate(
    error_type: str,
    *,
    execution_candidate_id: str,
    reason: str,
    execution_id: str = "",
    recoverable: bool = False,
    trace_chain: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    if error_type not in OCR_ERROR_TYPES:
        error_type = "invalid_output_schema"
    err_id = f"oerr_ocr_{execution_candidate_id}_{uuid4().hex[:6]}"
    return {
        "envelope_type": "ocr_runner_error_candidate",
        "error_candidate_id": err_id,
        "error_type": error_type,
        "error_stage": "ocr_runner_sandbox",
        "error_reason": reason,
        "source_ocr_execution_candidate_id": execution_candidate_id,
        "source_ocr_execution_id": execution_id or None,
        "recoverable": recoverable,
        "not_fact": True,
        "not_navigation_decision": True,
        "traceable_to_ocr_execution_candidate": True,
        "trace_chain": trace_chain or [],
    }


__all__ = [
    "validate_ocr_execution_candidate",
    "validate_trace_chain",
    "build_ocr_adapter_input",
    "prepare_ocr_execution",
    "validate_ocr_runner_output",
    "build_ocr_result_envelope",
    "build_ocr_runner_error_candidate",
    "BRIDGE_ENDPOINT",
    "RUNNER_NAME",
    "RUNNER_VERSION",
]
