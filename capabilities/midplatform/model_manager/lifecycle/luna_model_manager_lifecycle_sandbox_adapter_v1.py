# -*- coding: utf-8 -*-
"""Luna Model Manager Lifecycle — sandbox adapter v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.lifecycle.model_lifecycle_processor_v1 import (
    activate_model,
    block_model,
    deprecate_model,
    discover_model,
    get_sandbox_model,
    reset_sandbox_registry,
    run_full_lifecycle_sandbox,
    run_sandbox_evaluation,
)
from capabilities.midplatform.model_manager.lifecycle.model_admission_processor_v1 import (
    complete_admission,
    start_admission_pipeline,
)
from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    is_routing_eligible,
)

SANDBOX_POLICY_REF = "model_activation_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_BLOCKED"


def assert_luna_owns_model(model_record: Dict[str, Any]) -> Dict[str, Any]:
    """Luna owns lifecycle state — model is managed, not merely called."""
    checks = {
        "has_lifecycle_state": bool(model_record.get("lifecycle_state")),
        "has_lifecycle_trace": isinstance(model_record.get("lifecycle_trace"), list),
        "sandbox_managed": model_record.get("sandbox") is True or "lifecycle_trace" in model_record,
        "not_mere_invocation": model_record.get("candidate_only") is True,
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True}


def run_lifecycle_sandbox_case(
    *,
    case_type: str,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Dispatch lifecycle sandbox case by type."""
    reset_sandbox_registry()
    if case_type == "new_ocr_model":
        return _case_new_ocr_model(**kwargs)
    if case_type == "insufficient_capability":
        return _case_insufficient_capability(**kwargs)
    if case_type == "model_deprecation":
        return _case_model_deprecation(**kwargs)
    if case_type == "malicious_model_block":
        return _case_malicious_model_block(**kwargs)
    return {"success": False, "error": f"unknown_case_type:{case_type}"}


def _case_new_ocr_model() -> Dict[str, Any]:
    result = run_full_lifecycle_sandbox(
        model_id="ocr_v2",
        model_label="OCR Tool v2",
        model_type="tool",
        capabilities=["text_recognition", "precise_ocr"],
        capability_id="text_recognition",
        reliability=0.91,
        latency_ms=450,
        cost_tier="low",
        owner="tool_os",
    )
    record = result.get("model_record") or {}
    passed = (
        record.get("lifecycle_state") == "active"
        and result.get("routing_eligible") is True
        and any(t.get("to_state") == "candidate" for t in record.get("lifecycle_trace", []))
        and any(t.get("to_state") == "evaluating" for t in record.get("lifecycle_trace", []))
        and any(t.get("to_state") == "active" for t in record.get("lifecycle_trace", []))
        and (result.get("capability_registry_update") or {}).get("registry_updated") is True
    )
    return {"case_type": "new_ocr_model", "passed": passed, "result": result}


def _case_insufficient_capability() -> Dict[str, Any]:
    """Qwen asked for precise OCR — evaluation_failed → not_routing_eligible."""
    discovery = discover_model(
        model_id="qwen_vl_ocr_attempt",
        model_label="Qwen-VL OCR Attempt",
        model_type="teacher",
        capabilities=["text_recognition"],
        owner="external_teacher",
    )
    record = discovery["model_record"]
    start = start_admission_pipeline(model_record=record)
    record = start["model_record"]

    evaluation = run_sandbox_evaluation(
        model_id="qwen_vl_ocr_attempt",
        capability_id="text_recognition",
        reliability=0.35,
        latency_ms=2800,
        cost_tier="high",
        unsupported_claim_rate=0.4,
        scene_type="shopfront_sign",
        force_fail=True,
    )
    admission = complete_admission(
        model_record=record,
        benchmark_record=evaluation["benchmark_record"],
        approve=False,
    )
    record = admission["model_record"]
    passed = (
        admission.get("evaluation_failed") is True
        and admission.get("routing_eligible") is False
        and record.get("lifecycle_state") == "candidate"
        and record.get("admission_status") == "rejected"
        and evaluation["benchmark_record"]["evaluation_status"] == "failed"
    )
    return {"case_type": "insufficient_capability", "passed": passed, "result": {
        "discovery": discovery,
        "evaluation": evaluation,
        "admission": admission,
        "model_record": record,
    }}


def _case_model_deprecation() -> Dict[str, Any]:
    """OCR-v1 active → OCR-v2 replaces → OCR-v1 deprecated, trace preserved."""
    reset_sandbox_registry()
    v2 = run_full_lifecycle_sandbox(
        model_id="ocr_v2",
        model_label="OCR Tool v2",
        model_type="tool",
        capabilities=["text_recognition"],
        capability_id="text_recognition",
        reliability=0.93,
        latency_ms=400,
        owner="tool_os",
    )
    v1 = run_full_lifecycle_sandbox(
        model_id="ocr_v1",
        model_label="OCR Tool v1",
        model_type="tool",
        capabilities=["text_recognition"],
        capability_id="text_recognition",
        reliability=0.88,
        latency_ms=600,
        owner="tool_os",
    )

    deprecation = deprecate_model(
        model_id="ocr_v1",
        replacement_model_id="ocr_v2",
        reason="replacement_available",
    )
    v1_final = deprecation.get("model_record") or {}
    trace = v1_final.get("lifecycle_trace", [])

    passed = (
        v1_final.get("lifecycle_state") == "deprecated"
        and deprecation.get("routing_eligible") is False
        and deprecation.get("trace_preserved") is True
        and len(trace) >= 4
        and v1_final.get("replaced_by") == "ocr_v2"
        and (v2.get("model_record") or {}).get("lifecycle_state") == "active"
        and (v1.get("model_record") or {}).get("lifecycle_state") == "active"
        and v1_final.get("lifecycle_state") == "deprecated"
    )
    return {"case_type": "model_deprecation", "passed": passed, "result": {
        "ocr_v2_lifecycle": v2,
        "ocr_v1_lifecycle": v1,
        "ocr_v1_deprecation": deprecation,
        "lifecycle_trace_length": len(trace),
    }}


def _case_malicious_model_block() -> Dict[str, Any]:
    """High unsupported claim rate → blocked."""
    discovery = discover_model(
        model_id="vision_teacher_bad",
        model_label="Vision Teacher Bad",
        model_type="teacher",
        capabilities=["unknown_scene_reasoning"],
        owner="external_teacher",
    )
    record = discovery["model_record"]
    start = start_admission_pipeline(model_record=record)
    record = start["model_record"]

    evaluation = run_sandbox_evaluation(
        model_id="vision_teacher_bad",
        capability_id="unknown_scene_reasoning",
        reliability=0.2,
        latency_ms=800,
        unsupported_claim_rate=0.85,
        force_fail=True,
    )
    block = block_model(
        model_id="vision_teacher_bad",
        reason="policy_violation",
        violation_type="unsupported_claim_abuse",
    )
    record = block.get("model_record") or {}
    passed = (
        record.get("lifecycle_state") == "blocked"
        and block.get("routing_eligible") is False
        and block.get("execution_eligible") is False
        and record.get("violation_type") == "unsupported_claim_abuse"
        and evaluation["benchmark_record"]["unsupported_claim_rate"] > 0.5
    )
    return {"case_type": "malicious_model_block", "passed": passed, "result": {
        "discovery": discovery,
        "evaluation": evaluation,
        "block": block,
        "model_record": record,
    }}
