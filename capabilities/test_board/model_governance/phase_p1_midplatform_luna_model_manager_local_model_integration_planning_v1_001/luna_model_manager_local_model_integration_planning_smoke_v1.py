# -*- coding: utf-8 -*-
"""Luna Model Manager Local Model — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_local_model_processor_v1 import (
    run_gpu_insufficient_with_fallback,
    run_local_model_integration_planning,
)
from capabilities.midplatform.model_manager.luna_model_manager_local_model_types_v1 import (
    EXTERNAL_MODEL_ID,
    FINAL_BLOCKED,
    FINAL_GO,
    LOCAL_MODEL_ID,
    SMOKE_CASE_IDS,
)


def smoke_case_a_local_normal_admission() -> Dict[str, Any]:
    """Case A: InternVL candidate → runtime check → benchmark → active → routing eligible."""
    case_id = "case_a_local_model_normal_admission"
    result = run_local_model_integration_planning(scenario="normal_admission", gpu_memory_available_gb=12)
    record = result.get("model_record") or {}
    passed = (
        result.get("admitted") is True
        and result.get("routing_eligible") is True
        and record.get("lifecycle_state") == "active"
        and record.get("execution_mode") == "local_runtime"
        and (result.get("environment_check") or {}).get("all_passed") is True
        and result.get("resource_profile") is not None
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_gpu_insufficient_fallback() -> Dict[str, Any]:
    """Case B: GPU insufficient → not_available → provider fallback candidate (Qwen API)."""
    case_id = "case_b_gpu_insufficient_fallback"
    result = run_gpu_insufficient_with_fallback()
    admission = result.get("admission_result") or {}
    fallback = result.get("provider_fallback_candidate") or {}
    passed = (
        admission.get("blocked") is True
        and result.get("not_available") is True
        and result.get("fallback_to_external_api") is True
        and fallback.get("fallback_model_id") == EXTERNAL_MODEL_ID
        and fallback.get("not_silent_switch") is True
        and fallback.get("fallback_type") == "provider_fallback_candidate"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_local_vs_external() -> Dict[str, Any]:
    """Case C: Local vs External — capability + resource aware selection."""
    case_id = "case_c_local_vs_external_routing"
    result = run_local_model_integration_planning(scenario="local_vs_external", internvl_busy=True)
    selected = result.get("selected_provider") or {}
    scores = result.get("provider_scores") or []
    internvl_score = next((s for s in scores if s["model_id"] == LOCAL_MODEL_ID), {})
    passed = (
        result.get("routing_considers_resource") is True
        and result.get("model_manager_location_agnostic") is True
        and internvl_score.get("routing_score", 1) == 0.0
        and selected.get("model_id") in ("qwen_vl", "gemini_vision")
        and selected.get("model_id") != LOCAL_MODEL_ID
        and result.get("provider_selection_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_version_upgrade() -> Dict[str, Any]:
    """Case D: InternVL v1 active → v2 upgrade → v1 deprecated."""
    case_id = "case_d_local_version_upgrade"
    result = run_local_model_integration_planning(scenario="version_upgrade", gpu_memory_available_gb=12)
    passed = (
        result.get("v2_active") is True
        and result.get("v1_deprecated") is True
        and result.get("trace_preserved") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_local_normal_admission,
        smoke_case_b_gpu_insufficient_fallback,
        smoke_case_c_local_vs_external,
        smoke_case_d_version_upgrade,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "unified_execution_mode_abstraction": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
