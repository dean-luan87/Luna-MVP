# -*- coding: utf-8
"""Luna Decision Validation Layer — dry-run fixtures & cases v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.decision_validation.luna_decision_validation_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_decision_validation_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
    fixture_street_cross_safely,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_situation_understanding_model_dryrun_v1_001.luna_situation_understanding_dryrun_fixtures_v1 import (
    fixture_unknown_scene_low_evidence,
)

DRYRUN_CASE_IDS = (
    "case_a_shopfront_ocr_validated",
    "case_b_shopfront_slam_blocked",
    "case_c_user_goal_needs_review",
    "case_d_unknown_blanket_blocked",
    "case_e_street_crossing_high_risk_review",
)


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[4]


def _tools(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("active", [])


def _noops(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("noop", [])


def _validation(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("decision_validation_candidate") or {}


def _status(result: Dict[str, Any]) -> str:
    return _validation(result).get("validation_status_candidate", "")


def _plan_override_slam_mapping(plan_id: str = "plan_override_slam") -> Dict[str, Any]:
    return {
        "plan_id": plan_id,
        "plan_goal_candidate": {
            "goal_type": "navigate",
            "interpreted_goal": "SLAM spatial mapping",
            "candidate_only": True,
            "not_fact": True,
        },
        "plan_strategy": {"strategy_type": "navigation_support", "candidate_only": True, "not_fact": True},
        "plan_steps": [
            {
                "step_order": 1,
                "step_type": "request_tool",
                "step_goal": "spatial mapping via SLAM",
                "candidate_only": True,
            }
        ],
        "tool_plan_candidates": [{
            "capability_type": "slam",
            "tool_purpose": "spatial mapping",
            "execution_mode": "request_tool_os_admission",
            "candidate_only": True,
            "not_fact": True,
        }],
        "noop_tool_plan_candidates": [
            {"capability_type": "ocr", "noop_reason": "not used in override", "candidate_only": True},
        ],
        "handoff_to_tool_os_candidate": {
            "should_handoff": True,
            "runner_admission_required": True,
            "fact_admission_required_after_result": True,
            "required_tool_os_checks": ["permission check", "resource check", "runner admission"],
            "candidate_only": True,
            "not_fact": True,
        },
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
        "no_tool_execution": True,
    }


def _plan_override_ocr(plan_id: str = "plan_override_ocr") -> Dict[str, Any]:
    return {
        "plan_id": plan_id,
        "plan_goal_candidate": {"goal_type": "read_text", "candidate_only": True, "not_fact": True},
        "plan_strategy": {"strategy_type": "information_gathering", "candidate_only": True, "not_fact": True},
        "plan_steps": [{"step_type": "request_tool", "step_goal": "read sign text", "candidate_only": True}],
        "tool_plan_candidates": [{
            "capability_type": "ocr",
            "tool_purpose": "extract text",
            "execution_mode": "request_tool_os_admission",
            "candidate_only": True,
        }],
        "noop_tool_plan_candidates": [
            {"capability_type": "slam", "noop_reason": "no navigation", "candidate_only": True},
            {"capability_type": "depth", "noop_reason": "no spatial risk", "candidate_only": True},
            {"capability_type": "tracking", "noop_reason": "no dynamic target", "candidate_only": True},
        ],
        "handoff_to_tool_os_candidate": {
            "should_handoff": True,
            "runner_admission_required": True,
            "fact_admission_required_after_result": True,
            "required_tool_os_checks": ["permission check", "resource check", "runner admission"],
            "candidate_only": True,
        },
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
    }


def _plan_override_blanket(plan_id: str = "plan_blanket") -> Dict[str, Any]:
    caps = ["ocr", "slam", "detection", "depth", "tracking"]
    return {
        "plan_id": plan_id,
        "plan_goal_candidate": {"goal_type": "understand_environment", "candidate_only": True, "not_fact": True},
        "plan_strategy": {"strategy_type": "environment_understanding", "candidate_only": True, "not_fact": True},
        "tool_plan_candidates": [
            {"capability_type": c, "execution_mode": "request_tool_os_admission", "candidate_only": True}
            for c in caps
        ],
        "noop_tool_plan_candidates": [],
        "handoff_to_tool_os_candidate": {"should_handoff": True, "candidate_only": True},
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
    }


def _plan_override_cross_road(plan_id: str = "plan_cross_road") -> Dict[str, Any]:
    return {
        "plan_id": plan_id,
        "plan_goal_candidate": {"goal_type": "navigate", "candidate_only": True, "not_fact": True},
        "plan_strategy": {"strategy_type": "navigation_support", "candidate_only": True, "not_fact": True},
        "plan_steps": [
            {"step_type": "request_tool", "step_goal": "cross road immediately", "candidate_only": True},
        ],
        "tool_plan_candidates": [{
            "capability_type": "slam",
            "tool_purpose": "cross road",
            "execution_mode": "request_tool_os_admission",
            "candidate_only": True,
        }],
        "noop_tool_plan_candidates": [],
        "handoff_to_tool_os_candidate": {"should_handoff": True, "candidate_only": True},
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
    }


def _user_goal_find_entrance() -> Dict[str, Any]:
    return {
        "goal_type": "navigate",
        "goal_text_optional": "find entrance / navigate_to_entrance",
        "confidence": 0.9,
        "source": "user_command",
        "explicitness": "explicit",
        "candidate_only": True,
        "not_fact": True,
    }


def dryrun_case_a_shopfront_ocr_validated() -> Dict[str, Any]:
    case_id = "case_a_shopfront_ocr_validated"
    result = run_decision_validation_dryrun(fixture_job_564f1aa93983_shop_sign())
    v = _validation(result)
    readiness = v.get("tool_execution_readiness_candidate") or {}
    handoff = result.get("tool_os_handoff_candidate") or {}
    reason_codes = [r.get("reason_code") for r in v.get("validation_reason_candidates", [])]
    passed = (
        result.get("job_id") == "job_564f1aa93983"
        and _status(result) == "validated_candidate"
        and "ocr" in _tools(result)
        and "slam" in _noops(result)
        and "depth" in _noops(result)
        and "tracking" in _noops(result)
        and readiness.get("should_handoff_to_tool_os") is True
        and handoff.get("validation_cleared") is True
        and result.get("validation_gates_handoff_assertion", {}).get("passed") is True
        and result.get("no_teacher_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_shopfront_slam_blocked() -> Dict[str, Any]:
    case_id = "case_b_shopfront_slam_blocked"
    result = run_decision_validation_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        plan_override=_plan_override_slam_mapping(),
    )
    v = _validation(result)
    conflicts = v.get("validation_result", {}).get("policy_conflict_detected") or []
    handoff = result.get("tool_os_handoff_candidate") or {}
    passed = (
        _status(result) == "blocked_candidate"
        and (
            "text_objective_slam_mapping_conflict" in conflicts
            or "text_goal_slam_tool_conflict" in conflicts
        )
        and handoff.get("gated_by_validation") is True
        and handoff.get("should_handoff") is False
        and v.get("no_plan_override") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_user_goal_needs_review() -> Dict[str, Any]:
    case_id = "case_c_user_goal_needs_review"
    result = run_decision_validation_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        user_goal_candidate=_user_goal_find_entrance(),
        plan_override=_plan_override_ocr(),
    )
    v = _validation(result)
    alts = v.get("alternative_plan_candidates") or []
    plan = result.get("agent_plan_candidate") or {}
    passed = (
        _status(result) == "needs_review"
        and len(alts) >= 1
        and alts[0].get("plan_goal_type") == "navigate"
        and alts[0].get("does_not_override_selected_plan") is True
        and (plan.get("plan_goal_candidate") or {}).get("goal_type") == "read_text"
        and (result.get("tool_os_handoff_candidate") or {}).get("gated_by_validation") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_unknown_blanket_blocked() -> Dict[str, Any]:
    case_id = "case_d_unknown_blanket_blocked"
    try:
        envelope = fixture_unknown_scene_low_evidence()
    except Exception:
        envelope = {
            "job_id": "job_dryrun_unknown",
            "runner_scene_hint_optional": "unknown_scene",
            "runner_result": {
                "scene_profile_candidate": {"scene_type_candidate": "unknown_scene", "confidence": 0.3},
                "prompt_results": [],
            },
            "dryrun_case_ref_key": "unknown_scene_case",
        }
    result = run_decision_validation_dryrun(
        envelope,
        plan_override=_plan_override_blanket(),
    )
    v = _validation(result)
    conflicts = v.get("validation_result", {}).get("policy_conflict_detected") or []
    passed = (
        _status(result) == "blocked_candidate"
        and ("blanket_tool_activation" in conflicts or "unknown_scene_blanket_activation" in conflicts)
        and (result.get("tool_os_handoff_candidate") or {}).get("should_handoff") is False
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_street_crossing_high_risk_review() -> Dict[str, Any]:
    case_id = "case_e_street_crossing_high_risk_review"
    result = run_decision_validation_dryrun(
        fixture_street_cross_safely(),
        plan_override=_plan_override_cross_road(),
    )
    v = _validation(result)
    readiness = v.get("tool_execution_readiness_candidate") or {}
    checks = readiness.get("required_checks") or []
    passed = (
        _status(result) == "needs_review"
        and v.get("validation_result", {}).get("risk_level_candidate") == "high"
        and "additional_evidence_required" in checks
        and (result.get("tool_os_handoff_candidate") or {}).get("gated_by_validation") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_shopfront_ocr_validated,
        dryrun_case_b_shopfront_slam_blocked,
        dryrun_case_c_user_goal_needs_review,
        dryrun_case_d_unknown_blanket_blocked,
        dryrun_case_e_street_crossing_high_risk_review,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    case_a = next((c for c in cases if c["case_id"] == "case_a_shopfront_ocr_validated"), {})
    a_res = case_a.get("result") or {}
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-DryRun-v1-001",
        "deterministic_dryrun_only": True,
        "no_teacher": True,
        "no_real_model_execution": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_cases_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "core_validations": {
            "l2_feeds_validation": all(
                (c.get("result") or {}).get("l2_feeds_validation_assertion", {}).get("passed")
                for c in cases
            ),
            "validation_gates_handoff": all(
                (c.get("result") or {}).get("validation_gates_handoff_assertion", {}).get("passed")
                for c in cases
            ),
            "no_teacher_all_cases": all((c.get("result") or {}).get("no_teacher_assertion") for c in cases),
        },
        "job_564f1aa93983_validation_result": {
            "job_id": "job_564f1aa93983",
            "validation_status": a_res.get("validation_status"),
            "active_tools": _tools(a_res),
            "noop_tools": _noops(a_res),
            "handoff_cleared": (a_res.get("tool_os_handoff_candidate") or {}).get("validation_cleared"),
        },
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
