# -*- coding: utf-8 -*-
"""Luna Model Manager Local Model — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.local_runtime.dryrun.local_model_runtime_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_local_lifecycle_upgrade_dryrun,
    run_local_model_runtime_dryrun,
    run_local_vs_external_competition_dryrun,
)
from capabilities.midplatform.model_manager.luna_model_manager_local_model_types_v1 import (
    DRYRUN_CASE_IDS,
    EXTERNAL_MODEL_ID,
    LOCAL_MODEL_ID,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)


def dryrun_case_a_local_runtime_normal() -> Dict[str, Any]:
    """Case A: unknown_scene → InternVL selected → evidence → validation."""
    case_id = "case_a_local_runtime_normal"
    result = run_local_model_runtime_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        gpu_memory_available_gb=12,
        internvl_status="available",
        scoring_mode="cost_priority",
        mock_scenario="unknown_scene_hypothesis",
    )
    review = result.get("provider_validation_review") or {}
    selected = result.get("provider_selected_id")
    passed = (
        selected == LOCAL_MODEL_ID
        and result.get("capability_id") == "unknown_scene_reasoning"
        and "cost" in (result.get("selection_reason") or "")
        and review.get("validation_status") == "accepted_as_evidence"
        and result.get("evidence_bundle", {}).get("normalized") is not None
        and (result.get("model_evaluation_record") or {}).get("no_auto_policy_update") is True
        and result.get("runtime_not_task_decider") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_runtime_unavailable() -> Dict[str, Any]:
    """Case B: GPU insufficient → runtime_unavailable → fallback_provider_candidate."""
    case_id = "case_b_runtime_unavailable_fallback"
    result = run_local_model_runtime_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        force_internvl_unavailable=True,
        scoring_mode="cost_priority",
    )
    unavailable = result.get("runtime_unavailable_candidate") or {}
    fallback = result.get("fallback_provider_candidate") or {}
    passed = (
        unavailable.get("runtime_unavailable_candidate") is True
        and unavailable.get("not_silent_switch") is True
        and fallback.get("fallback_model_id") == EXTERNAL_MODEL_ID
        and fallback.get("fallback_type") == "provider_fallback_candidate"
        and result.get("provider_selected_id") != EXTERNAL_MODEL_ID
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_competition() -> Dict[str, Any]:
    """Case C: Local vs External multi-factor routing."""
    case_id = "case_c_local_vs_external_competition"
    result = run_local_vs_external_competition_dryrun()
    selection = result.get("runtime_selection") or {}
    scores = selection.get("provider_scores") or []
    passed = (
        result.get("multi_factor_scoring") is True
        and result.get("not_capability_only") is True
        and len(scores) >= 3
        and all(s.get("execution_mode") in ("local_runtime", "external_api") for s in scores)
        and selection.get("provider_selection_candidate") is True
        and result.get("selected_provider_id") is not None
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_output_pollution() -> Dict[str, Any]:
    """Case D: InternVL Starbucks claim → unsupported_claim → reject (same governance)."""
    case_id = "case_d_local_output_pollution"
    result = run_local_model_runtime_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        mock_scenario="unsupported_brand_claim",
        scoring_mode="cost_priority",
    )
    review = result.get("provider_validation_review") or {}
    bundle = result.get("evidence_bundle") or {}
    passed = (
        bundle.get("has_unsupported_claim") is True
        and review.get("validation_status") == "rejected_by_policy"
        and review.get("rejection_reason") == "unsupported_claim"
        and (result.get("provider_result") or {}).get("evidence_candidate") is None
        and result.get("upper_layer_transparent") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_lifecycle_upgrade() -> Dict[str, Any]:
    """Case E: InternVL v1→v2 upgrade, L1/L2 unchanged."""
    case_id = "case_e_runtime_lifecycle_upgrade"
    result = run_local_lifecycle_upgrade_dryrun()
    passed = (
        result.get("v2_active") is True
        and result.get("v1_deprecated") is True
        and result.get("trace_preserved") is True
        and result.get("l1_l2_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_local_runtime_normal,
        dryrun_case_b_runtime_unavailable,
        dryrun_case_c_competition,
        dryrun_case_d_output_pollution,
        dryrun_case_e_lifecycle_upgrade,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "execution_mode_transparent": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
