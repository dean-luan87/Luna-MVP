# -*- coding: utf-8 -*-
"""Qwen-VL Single Teacher Integration — dry-run fixtures v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_integration_dryrun.luna_qwen_vl_integration_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_qwen_vl_integration_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)

DRYRUN_CASE_IDS = (
    "case_a_teacher_admission_noop",
    "case_b_unknown_scene_request_teacher",
    "case_c_teacher_challenge_plan",
    "case_d_teacher_wrong_scene_rejected",
    "case_e_unsupported_claim_rejected",
)


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


def _generic_sam_regions() -> List[Dict[str, Any]]:
    return [
        {
            "prompt_id": f"generic_region_candidate_{i}",
            "prompt_target_label": f"generic_region_candidate_{i}",
            "ocr_route_candidate": False,
            "score": 0.85,
            "candidate_only": True,
        }
        for i in range(1, 6)
    ]


def fixture_job_unknown_scene() -> Dict[str, Any]:
    return {
        "job_id": "job_unknown_scene_dryrun",
        "created_at": "2026-07-09T01:00:00Z",
        "source": "replay",
        "asset_manifest": {
            "asset_id": "asset_unknown_scene",
            "file_name": "unknown_scene_sample_v1.png",
        },
        "runner_result": {
            "scene_profile_candidate": {
                "scene_type_candidate": "unknown_scene",
                "confidence": 0.35,
                "candidate_only": True,
                "not_fact": True,
            },
            "segmentation_prompt_policy": {
                "prompt_set_id": "scene_prompt_set_generic_v1",
                "scene_type_candidate": "unknown_scene",
            },
            "prompt_results": _generic_sam_regions(),
        },
        "runner_scene_hint_optional": "unknown_scene",
        "prompt_set_id_optional": "scene_prompt_set_generic_v1",
    }


def _plan_goal(result: Dict[str, Any]) -> str:
    plan = result.get("agent_plan_candidate") or {}
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "")


def _tools(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("active", [])


def _scene(result: Dict[str, Any]) -> str:
    sit = result.get("situation_understanding_candidate") or {}
    return (sit.get("scene_profile_candidate") or {}).get("scene_type", "")


def dryrun_case_a_teacher_admission_noop() -> Dict[str, Any]:
    """Case A: routine shopfront + OCR + high confidence → teacher noop."""
    case_id = "case_a_teacher_admission_noop"
    result = run_qwen_vl_integration_dryrun(fixture_job_564f1aa93983_shop_sign())
    admission = result.get("teacher_admission") or {}
    teacher_req = result.get("teacher_request") or {}
    validation = result.get("decision_validation_candidate") or {}
    passed = (
        admission.get("admission_status") == "noop"
        and admission.get("should_request_teacher") is False
        and "sufficient" in (admission.get("noop_reason") or teacher_req.get("noop_reason") or "").lower()
        and result.get("teacher_evidence_candidate") is None
        and validation.get("validation_status_candidate") == "validated_candidate"
        and _plan_goal(result) in ("identify_place", "read_text")
        and "ocr" in _tools(result)
        and result.get("no_tool_execution_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_unknown_scene_request_teacher() -> Dict[str, Any]:
    """Case B: unknown_scene + high uncertainty → request teacher, accepted evidence."""
    case_id = "case_b_unknown_scene_request_teacher"
    result = run_qwen_vl_integration_dryrun(
        fixture_job_unknown_scene(),
        qwen_mock_scenario="dryrun_case_b_unknown_indoor_hypothesis",
    )
    admission = result.get("teacher_admission") or {}
    review = result.get("teacher_validation_review") or {}
    evidence = result.get("teacher_evidence_candidate") or {}
    hypotheses = (
        (evidence.get("scene_hypothesis_candidate") or {}).get("scene_hypothesis_candidates")
        or (evidence.get("perception_output_optional") or {}).get("scene_hypothesis_candidates")
        or []
    )
    passed = (
        admission.get("should_request_teacher") is True
        and admission.get("admission_status") == "admitted"
        and admission.get("admission_reason") == "unknown_scene"
        and review.get("teacher_validation_status") == "accepted_as_evidence"
        and _scene(result) == "unknown_scene"
        and review.get("l1_scene_unchanged") is True
        and any(h.get("scene_type") == "indoor_public_space" for h in hypotheses)
        and float(evidence.get("uncertainty") or 1) <= 0.5
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_teacher_challenge_plan() -> Dict[str, Any]:
    """Case C: shopfront OCR plan + Qwen navigation context → alternative, plan unchanged."""
    case_id = "case_c_teacher_challenge_plan"
    result = run_qwen_vl_integration_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        qwen_mock_scenario="dryrun_case_c_navigation_context_challenge",
        admission_hints={"plan_challenge_requested": True},
    )
    review = result.get("teacher_validation_review") or {}
    evidence = result.get("teacher_evidence_candidate") or {}
    clue = evidence.get("task_clue_candidate") or {}
    passed = (
        review.get("teacher_validation_status") == "accepted_as_alternative"
        and review.get("selected_plan_unchanged") is True
        and review.get("keep_original_plan") is True
        and _plan_goal(result) in ("identify_place", "read_text")
        and "ocr" in _tools(result)
        and clue.get("clue_type") == "possible_navigation_context"
        and result.get("teacher_does_not_override_plan_assertion", {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_teacher_wrong_scene_rejected() -> Dict[str, Any]:
    """Case D: Qwen airport_terminal vs shopfront_sign → scene conflict reject."""
    case_id = "case_d_teacher_wrong_scene_rejected"
    result = run_qwen_vl_integration_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        qwen_mock_scenario="dryrun_case_d_wrong_scene_airport",
        admission_hints={"force_admission": True},
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and _scene(result) == "shopfront_sign"
        and any(
            c.get("conflict_type") == "l1_scene_override_attempt"
            for c in (review.get("conflict_candidates") or [])
        )
        and review.get("l1_scene_unchanged") is True
        and result.get("teacher_does_not_override_l1_assertion", {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_unsupported_claim_rejected() -> Dict[str, Any]:
    """Case E: Qwen Starbucks claim without OCR → unsupported_claim reject."""
    case_id = "case_e_unsupported_claim_rejected"
    result = run_qwen_vl_integration_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        qwen_mock_scenario="dryrun_case_e_unsupported_brand_claim",
        admission_hints={"force_admission": True},
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and any(
            c.get("conflict_type") == "unsupported_claim"
            for c in (review.get("conflict_candidates") or [])
        )
        and review.get("no_fact_write") is True
        and review.get("selected_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_teacher_admission_noop,
        dryrun_case_b_unknown_scene_request_teacher,
        dryrun_case_c_teacher_challenge_plan,
        dryrun_case_d_teacher_wrong_scene_rejected,
        dryrun_case_e_unsupported_claim_rejected,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    case_a = next((c for c in cases if c["case_id"] == "case_a_teacher_admission_noop"), {})
    a_res = case_a.get("result") or {}
    return {
        "phase_id": "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-DryRun-v1-001",
        "provider": "qwen_vl",
        "deterministic_dryrun_only": True,
        "no_real_qwen_api": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_cases_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "core_validations": {
            "luna_controls_admission": all(
                "teacher_admission" in (c.get("result") or {})
                for c in cases
            ),
            "no_plan_override_all": all(
                (c.get("result") or {}).get("teacher_does_not_override_plan_assertion", {}).get("passed")
                for c in cases
            ),
            "no_l1_override_all": all(
                (c.get("result") or {}).get("teacher_does_not_override_l1_assertion", {}).get("passed")
                for c in cases
            ),
        },
        "case_a_teacher_admission": (a_res.get("teacher_request") or {}),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
