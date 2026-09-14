# -*- coding: utf-8 -*-
"""Runner Sandbox v1 — controlled MobileSAM execution entry. Test environment only."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from capabilities.midplatform.model_test_lens.mobile_sam_single_model_execution_integration.mobile_sam_single_model_execution_integration_types_v1 import (
    ERROR_TYPES,
    EXECUTION_CANDIDATE_REQUIRED_STATUSES,
    FORBIDDEN_EXECUTION_CANDIDATE_STATUSES,
    MODEL_ID,
    RUNNER_EXECUTION_ENVIRONMENT_ALLOWLIST,
    RUNNER_EXECUTION_MODEL_ALLOWLIST,
    TASK_TYPE,
)

SANDBOX_POLICY_REF = (
    "schemas/mobile_sam_single_model_execution/runner_sandbox_policy_v1.json"
)
ADAPTER_INPUT_SCHEMA_REF = (
    "schemas/mobile_sam_single_model_execution/model_adapter_input_schema_v1.json"
)
OUTPUT_ENVELOPE_SCHEMA_REF = (
    "schemas/mobile_sam_single_model_execution/segmentation_result_envelope_schema_v1.json"
)
EXECUTION_CANDIDATE_CANCELLED_REASON = "execution_candidate_cancelled"


class RunnerSandboxPolicyViolation(Exception):
    """Raised when sandbox entry requirements are not met."""


def _error_candidate(
    error_type: str,
    *,
    execution_candidate_id: str,
    reason: str,
    trace_chain: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    if error_type not in ERROR_TYPES:
        error_type = "sandbox_policy_violation"
    return {
        "envelope_type": "runner_error_candidate",
        "error_type": error_type,
        "source_execution_candidate_id": execution_candidate_id,
        "error_reason": reason,
        "trace_chain": trace_chain or [],
        "candidate_only": True,
        "not_fact": True,
        "no_navigation_decision": True,
        "runner_error_does_not_write_fact": True,
    }


def validate_trace_chain(execution_candidate: Dict[str, Any]) -> Optional[str]:
    """Strict trace validation: region, attention, task candidate must be present."""
    chain = execution_candidate.get("trace_chain") or []
    if len(chain) < 5:
        return "trace_chain_incomplete"
    stages = {item.get("stage"): item.get("ref") for item in chain if item.get("stage")}
    required = (
        "segmentation_region",
        "observation_attention_record",
        "runner_task_candidate",
        "runner_invocation_request",
    )
    for stage in required:
        if not stages.get(stage):
            return f"trace_missing_{stage}"
    if not execution_candidate.get("source_region_id"):
        return "trace_missing_region_id"
    if not execution_candidate.get("source_attention_record_id"):
        return "trace_missing_attention_record_id"
    if not execution_candidate.get("source_runner_task_candidate_id"):
        return "trace_missing_task_candidate_id"
    if not execution_candidate.get("source_admission_result_id"):
        return "admission_result_missing"
    return None


def validate_execution_candidate(execution_candidate: Dict[str, Any]) -> Optional[str]:
    """Return rejection reason if candidate cannot enter sandbox."""
    if not execution_candidate:
        return "missing_execution_candidate"
    status = execution_candidate.get("execution_status")
    if status in FORBIDDEN_EXECUTION_CANDIDATE_STATUSES:
        if status == "cancelled":
            return EXECUTION_CANDIDATE_CANCELLED_REASON
        return f"execution_candidate_{status}"
    if status not in EXECUTION_CANDIDATE_REQUIRED_STATUSES:
        return "execution_candidate_status_not_allowed"
    if execution_candidate.get("admission_decision_at_create") != "admitted":
        return "admission_not_admitted_at_create"
    if not execution_candidate.get("source_invocation_request_id"):
        return "orphan_execution_candidate"
    trace_err = validate_trace_chain(execution_candidate)
    if trace_err:
        return trace_err
    model_ref = execution_candidate.get("runner_config_ref", "")
    runner_type = execution_candidate.get("requested_runner_type", "")
    if "mobile_sam" not in model_ref and runner_type not in ("Segmentation", "MobileSAM"):
        return "non_mobile_sam_execution_candidate"
    return None


def build_adapter_input(
    execution_candidate: Dict[str, Any],
    *,
    image_ref: str,
    region_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Normalize midplatform adapter input from execution candidate."""
    region = region_id or execution_candidate.get("source_region_id", "")
    return {
        "image_ref": image_ref,
        "region_ref": f"region://{region}",
        "task_type": TASK_TYPE,
        "model_id": MODEL_ID,
        "constraints": {
            "candidate_only": True,
            "no_fact_write": True,
            "no_navigation_decision": True,
            "crop_policy_ref": execution_candidate.get("crop_policy_ref"),
            "timeout_policy_ref": execution_candidate.get("timeout_policy_ref"),
        },
        "trace_chain": execution_candidate.get("trace_chain") or [],
        "source_execution_candidate_id": execution_candidate["execution_candidate_id"],
        "source_invocation_request_id": execution_candidate.get("source_invocation_request_id"),
        "source_admission_result_id": execution_candidate.get("source_admission_result_id"),
    }


def validate_environment(environment: str) -> bool:
    return environment in RUNNER_EXECUTION_ENVIRONMENT_ALLOWLIST


def validate_model(model_id: str) -> bool:
    return model_id in RUNNER_EXECUTION_MODEL_ALLOWLIST


def prepare_execution(
    execution_candidate: Dict[str, Any],
    *,
    image_ref: str,
    environment: str = "test_environment",
) -> Dict[str, Any]:
    """
    Validate sandbox entry and return execution package (not yet invoked).
    Does NOT call MobileSAM inference — caller invokes runner separately.
    """
    rejection = validate_execution_candidate(execution_candidate)
    if rejection:
        return {
            "ok": False,
            "error": _error_candidate(
                "execution_cancelled" if "cancelled" in rejection else "sandbox_policy_violation",
                execution_candidate_id=execution_candidate.get("execution_candidate_id", "unknown"),
                reason=rejection,
                trace_chain=execution_candidate.get("trace_chain"),
            ),
        }
    if not validate_environment(environment):
        return {
            "ok": False,
            "error": _error_candidate(
                "sandbox_policy_violation",
                execution_candidate_id=execution_candidate["execution_candidate_id"],
                reason="non_test_environment",
            ),
        }
    adapter_input = build_adapter_input(execution_candidate, image_ref=image_ref)
    if adapter_input["model_id"] not in RUNNER_EXECUTION_MODEL_ALLOWLIST:
        return {
            "ok": False,
            "error": _error_candidate(
                "sandbox_policy_violation",
                execution_candidate_id=execution_candidate["execution_candidate_id"],
                reason="non_mobile_sam_model",
            ),
        }

    rex_id = f"rex_mobile_sam_{execution_candidate['execution_candidate_id']}_{uuid4().hex[:8]}"
    return {
        "ok": True,
        "runner_execution_id": rex_id,
        "runner_execution": True,
        "model_id": MODEL_ID,
        "environment": environment,
        "adapter_input": adapter_input,
        "sandbox_policy_ref": SANDBOX_POLICY_REF,
        "adapter_input_schema_ref": ADAPTER_INPUT_SCHEMA_REF,
        "output_envelope_schema_ref": OUTPUT_ENVELOPE_SCHEMA_REF,
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
        "trace_chain": adapter_input["trace_chain"],
    }


def build_segmentation_result_envelope(
    *,
    runner_execution_id: str,
    execution_candidate_id: str,
    region_id: str,
    mask_ref: str,
    confidence: float,
    trace_chain: List[Dict[str, str]],
    model_version: str = "mobile_sam_v1",
) -> Dict[str, Any]:
    """Wrap MobileSAM output as segmentation result envelope (result candidate)."""
    return {
        "envelope_type": "segmentation_result_envelope",
        "source_model": "MobileSAM",
        "model_version": model_version,
        "source_runner_execution_id": runner_execution_id,
        "source_execution_candidate_id": execution_candidate_id,
        "region_id": region_id,
        "mask_ref": mask_ref,
        "confidence": confidence,
        "result_candidate_type": "segmentation_mask_candidate",
        "candidate_only": True,
        "not_fact": True,
        "needs_fact_admission": True,
        "trace_chain": trace_chain,
    }


__all__ = [
    "RunnerSandboxPolicyViolation",
    "build_adapter_input",
    "build_segmentation_result_envelope",
    "prepare_execution",
    "validate_execution_candidate",
    "validate_trace_chain",
    "validate_environment",
    "validate_model",
]
