# -*- coding: utf-8 -*-
"""Luna Model Manager Multi-Model Collaboration — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.collaboration.dryrun.multi_model_collaboration_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_challenge_mode_dryrun,
    run_collaboration_degradation_dryrun,
    run_evidence_conflict_dryrun,
    run_parallel_evidence_dryrun,
    run_pipeline_collaboration_dryrun,
)
from capabilities.midplatform.model_manager.luna_model_manager_collaboration_types_v1 import (
    DRYRUN_CASE_IDS,
)


def dryrun_case_a_pipeline() -> Dict[str, Any]:
    """Case A: shopfront pipeline — slots, OCR primary, VLM context only."""
    case_id = "case_a_pipeline_collaboration_shopfront"
    result = run_pipeline_collaboration_dryrun()
    handoff = result.get("tool_os_handoff") or {}
    passed = (
        result.get("collaboration_type") == "pipeline"
        and result.get("uses_collaboration_slots") is True
        and result.get("direct_vlm_skipped") is True
        and result.get("ocr_is_primary") is True
        and result.get("vlm_context_only") is True
        and result.get("fusion_candidate") is True
        and result.get("not_executed") is True
        and handoff.get("tool_os_handoff_candidate") is True
        and result.get("sequence") == ["text_detector", "ocr", "vlm_context"]
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_parallel() -> Dict[str, Any]:
    """Case B: parallel evidence set, not single answer."""
    case_id = "case_b_parallel_evidence_unknown_scene"
    result = run_parallel_evidence_dryrun()
    fusion = result.get("evidence_fusion") or {}
    passed = (
        fusion.get("produces_single_answer") is False
        and fusion.get("not_merged_hypothesis") is True
        and len(result.get("evidence_set") or []) >= 3
        and fusion.get("not_voting") is True
        and fusion.get("fusion_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_challenge() -> Dict[str, Any]:
    """Case C: challenge mode — alternative hypothesis, plan unchanged."""
    case_id = "case_c_challenge_mode_teacher"
    result = run_challenge_mode_dryrun()
    challenge = result.get("challenge") or {}
    passed = (
        result.get("plan_not_overridden") is True
        and result.get("alternative_hypothesis_present") is True
        and challenge.get("challenge_does_not_override_plan") is True
        and challenge.get("override_plan") is False
        and result.get("selected_plan_still_ocr") is True
        and challenge.get("alternative_hypothesis_candidate") is not None
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_conflict() -> Dict[str, Any]:
    """Case D: semantic conflict — no confidence voting."""
    case_id = "case_d_evidence_conflict_semantic"
    result = run_evidence_conflict_dryrun()
    conflict = result.get("model_conflict_candidate") or {}
    passed = (
        result.get("conflict_detected") is True
        and result.get("not_auto_resolved") is True
        and result.get("not_confidence_voting") is True
        and result.get("conflict_type_semantic") is True
        and result.get("resolution_request_more_evidence") is True
        and conflict.get("not_score_voting") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_degradation() -> Dict[str, Any]:
    """Case E: resource degradation — lost_capability recorded."""
    case_id = "case_e_resource_collaboration_degradation"
    result = run_collaboration_degradation_dryrun()
    degradation = result.get("collaboration_degradation") or {}
    passed = (
        result.get("had_internvl_in_original") is True
        and result.get("degraded_to_qwen_only") is True
        and result.get("lost_capability_recorded") is True
        and result.get("not_silent_degradation") is True
        and degradation.get("collaboration_degradation_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_pipeline,
        dryrun_case_b_parallel,
        dryrun_case_c_challenge,
        dryrun_case_d_conflict,
        dryrun_case_e_degradation,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "model_os_collaboration_loop": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
