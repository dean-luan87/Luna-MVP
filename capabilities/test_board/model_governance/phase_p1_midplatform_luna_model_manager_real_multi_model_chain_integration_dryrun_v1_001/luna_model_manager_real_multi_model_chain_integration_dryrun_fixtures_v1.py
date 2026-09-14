# -*- coding: utf-8 -*-
"""Luna Model Manager Real Multi-Model Chain — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.collaboration.real_chain.dryrun.real_chain_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_context_challenge_dryrun,
    run_evidence_conflict_dryrun,
    run_full_trace_dryrun,
    run_ocr_failure_chain_dryrun,
    run_slot_provider_upgrade_dryrun,
    run_standard_shopfront_dryrun,
)
from capabilities.midplatform.model_manager.luna_model_manager_real_chain_types_v1 import (
    DRYRUN_CASE_IDS,
)


def dryrun_case_a_standard_shopfront() -> Dict[str, Any]:
    case_id = "case_a_standard_shopfront_chain"
    result = run_standard_shopfront_dryrun()
    fusion_pkg = result.get("fusion_evidence_package") or {}
    passed = (
        result.get("slot_driven_not_model_pipeline") is True
        and result.get("three_slots_executed") is True
        and result.get("not_merged_fact") is True
        and fusion_pkg.get("not_merged_fact") is True
        and (result.get("fusion_candidate") or {}).get("fusion_candidate") is True
        and (result.get("validation_review") or {}).get("validation_id") is not None
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_provider_upgrade() -> Dict[str, Any]:
    case_id = "case_b_slot_provider_upgrade"
    result = run_slot_provider_upgrade_dryrun()
    passed = (
        result.get("slot_2_provider_changed") is True
        and result.get("l1_unchanged") is True
        and result.get("l2_unchanged") is True
        and result.get("collaboration_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_ocr_failure() -> Dict[str, Any]:
    case_id = "case_c_ocr_failure_chain"
    result = run_ocr_failure_chain_dryrun()
    passed = (
        result.get("detection_succeeded") is True
        and result.get("ocr_failed") is True
        and result.get("qwen_not_invoked_for_guess") is True
        and result.get("not_qwen_guess") is True
        and result.get("l2_replan_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_context_challenge() -> Dict[str, Any]:
    case_id = "case_d_context_challenge"
    result = run_context_challenge_dryrun()
    passed = (
        result.get("context_allowed") is True
        and result.get("restaurant_fact_forbidden") is True
        and result.get("ocr_text") == "阿叔阿姨的店"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_evidence_conflict() -> Dict[str, Any]:
    case_id = "case_e_evidence_conflict"
    result = run_evidence_conflict_dryrun()
    conflict = result.get("evidence_conflict") or {}
    passed = (
        result.get("ocr_text") == "嘉会湖"
        and conflict.get("evidence_conflict_candidate") is True
        and result.get("not_confidence_override") is True
        and (result.get("validation_review") or {}).get("not_confidence_based") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_f_full_trace() -> Dict[str, Any]:
    case_id = "case_f_full_execution_trace"
    result = run_full_trace_dryrun()
    ids = result.get("ids_present") or {}
    passed = (
        result.get("trace_complete") is True
        and result.get("self_explainable") is True
        and all(ids.get(k) for k in ("goal_id", "collaboration_plan_id", "validation_id", "slot_ids", "provider_execution_ids", "evidence_ids"))
        and result.get("why_has_situation_goal_capability") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_standard_shopfront,
        dryrun_case_b_provider_upgrade,
        dryrun_case_c_ocr_failure,
        dryrun_case_d_context_challenge,
        dryrun_case_e_evidence_conflict,
        dryrun_case_f_full_trace,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "slot_driven_orchestration": True,
        "execution_trace_graph": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
