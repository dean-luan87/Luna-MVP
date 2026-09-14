# -*- coding: utf-8
"""Luna Agent Planning Layer — dry-run fixtures & cases v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.agent_planning.luna_agent_planning_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_agent_planning_dryrun,
)

DRYRUN_CASE_IDS = (
    "case_a_job_564f1aa93983_shop_sign",
    "case_b_subway_find_direction",
    "case_c_street_cross_safely",
    "case_d_user_goal_overrides_scene",
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


def _runner_unknown_generic() -> Dict[str, Any]:
    return {
        "scene_profile_candidate": {
            "scene_type_candidate": "unknown_scene",
            "confidence": 0.55,
            "candidate_only": True,
            "not_fact": True,
        },
        "segmentation_prompt_policy": {
            "prompt_set_id": "scene_prompt_set_generic_v1",
            "scene_type_candidate": "unknown_scene",
        },
        "prompt_results": _generic_sam_regions(),
    }


def fixture_job_564f1aa93983_shop_sign() -> Dict[str, Any]:
    job_path = (
        _repo_root()
        / "capabilities/midplatform/model_test_lens/local_runner_bridge/jobs/job_564f1aa93983.json"
    )
    if job_path.is_file():
        envelope = json.loads(job_path.read_text(encoding="utf-8"))
    else:
        envelope = {
            "job_id": "job_564f1aa93983",
            "created_at": "2026-07-08T02:30:08Z",
            "source": "replay",
            "asset_manifest": {
                "asset_id": "asset_d19f5fe2972f",
                "file_name": "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
            },
            "runner_result": _runner_unknown_generic(),
            "runner_scene_hint_optional": "unknown_scene",
            "prompt_set_id_optional": "scene_prompt_set_generic_v1",
        }
    envelope.setdefault("job_id", "job_564f1aa93983")
    envelope.setdefault("dryrun_case_ref_key", "shopfront_sign_case")
    return envelope


def fixture_subway_find_direction() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_l2_subway",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {
            "asset_id": "asset_subway",
            "file_name": "subway_direction_sign_jiahuihu.png",
        },
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": _runner_unknown_generic(),
        "dryrun_case_ref_key": "subway_platform_case",
        "user_goal_candidate_optional": {
            "goal_type": "find",
            "goal_text_optional": "find_direction",
            "confidence": 0.85,
            "source": "user_command",
            "explicitness": "explicit",
            "candidate_only": True,
            "not_fact": True,
        },
    }


def fixture_street_cross_safely() -> Dict[str, Any]:
    return {
        "job_id": "job_dryrun_l2_street",
        "source": "test_fixture",
        "created_at": "2026-07-08T00:00:00Z",
        "asset_manifest": {
            "asset_id": "asset_street",
            "file_name": "street_crossing_fixture.png",
        },
        "runner_scene_hint_optional": "unknown_scene",
        "runner_result": _runner_unknown_generic(),
        "dryrun_case_ref_key": "street_crossing_case",
        "dryrun_extra_evidence": [
            {
                "evidence_id": "ev_st1",
                "source": "detection",
                "evidence_type": "scene_hint",
                "value": "crosswalk_hint",
                "confidence": 0.83,
                "source_trace_ref": "ev_st1",
                "candidate_only": True,
                "not_fact": True,
            },
            {
                "evidence_id": "ev_st2",
                "source": "detection",
                "evidence_type": "object_hint",
                "value": "vehicle_hint",
                "confidence": 0.8,
                "source_trace_ref": "ev_st2",
                "candidate_only": True,
                "not_fact": True,
            },
            {
                "evidence_id": "ev_st3",
                "source": "detection",
                "evidence_type": "object_hint",
                "value": "person_hint",
                "confidence": 0.78,
                "source_trace_ref": "ev_st3",
                "candidate_only": True,
                "not_fact": True,
            },
            {
                "evidence_id": "ev_st4",
                "source": "metadata",
                "evidence_type": "spatial_hint",
                "value": "open_road",
                "confidence": 0.76,
                "source_trace_ref": "ev_st4",
                "candidate_only": True,
                "not_fact": True,
            },
        ],
        "user_goal_candidate_optional": {
            "goal_type": "navigate",
            "goal_text_optional": "cross_safely",
            "confidence": 0.88,
            "source": "user_command",
            "explicitness": "explicit",
            "candidate_only": True,
            "not_fact": True,
        },
    }


def fixture_user_goal_overrides_shopfront() -> Dict[str, Any]:
    """Visual: shopfront_sign; User: find entrance — goal > scene default."""
    env = fixture_job_564f1aa93983_shop_sign()
    env = dict(env)
    env["job_id"] = "job_dryrun_l2_goal_override"
    env["user_goal_candidate_optional"] = {
        "goal_type": "navigate",
        "goal_text_optional": "我要去找入口 / navigate_to_entrance",
        "confidence": 0.9,
        "source": "user_command",
        "explicitness": "explicit",
        "candidate_only": True,
        "not_fact": True,
    }
    env["dryrun_extra_evidence"] = list(env.get("dryrun_extra_evidence") or []) + [
        {
            "evidence_id": "ev_entrance",
            "source": "metadata",
            "evidence_type": "region",
            "value": "entrance_exit",
            "confidence": 0.8,
            "source_trace_ref": "ev_entrance",
            "candidate_only": True,
            "not_fact": True,
        }
    ]
    return env


def _tools(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("active", [])


def _noops(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("noop", [])


def _goal(result: Dict[str, Any]) -> str:
    plan = result.get("selected_plan_candidate") or {}
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "")


def _steps(result: Dict[str, Any]) -> List[str]:
    plan = result.get("selected_plan_candidate") or {}
    return [s.get("step_type", "") for s in plan.get("plan_steps", [])]


def dryrun_case_a_shopfront() -> Dict[str, Any]:
    case_id = "case_a_job_564f1aa93983_shop_sign"
    result = run_agent_planning_dryrun(fixture_job_564f1aa93983_shop_sign())
    scene = (
        result.get("situation_understanding_candidate", {})
        .get("scene_profile_candidate", {})
        .get("scene_type")
    )
    tools = _tools(result)
    noops = _noops(result)
    goal = _goal(result)
    passed = (
        result.get("job_id") == "job_564f1aa93983"
        and scene == "shopfront_sign"
        and goal in ("identify_place", "read_text")
        and "ocr" in tools
        and "slam" in noops
        and "depth" in noops
        and "tracking" in noops
        and "request_tool" in _steps(result)
        and "evaluate_result" in _steps(result)
        and result.get("l1_drives_l2_assertion", {}).get("passed") is True
        and result.get("l2_constrains_tools_assertion", {}).get("passed") is True
        and result.get("no_tool_execution_assertion") is True
        and result.get("no_runner_invocation_assertion") is True
        # spatial structure visible but SLAM not activated
        and "slam" not in tools
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "result": result,
        "assertions": {
            "l1_scene_shopfront": scene == "shopfront_sign",
            "ocr_active": "ocr" in tools,
            "slam_not_started_despite_spatial_regions": "slam" not in tools and "slam" in noops,
        },
    }


def dryrun_case_b_subway() -> Dict[str, Any]:
    case_id = "case_b_subway_find_direction"
    result = run_agent_planning_dryrun(fixture_subway_find_direction())
    scene = (
        result.get("situation_understanding_candidate", {})
        .get("scene_profile_candidate", {})
        .get("scene_type")
    )
    tools = _tools(result)
    noops = _noops(result)
    goal = _goal(result)
    passed = (
        scene == "subway_platform"
        and goal == "find_direction"
        and "ocr" in tools
        and "slam" in noops
        and "slam" not in tools
        and result.get("no_fact_write_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_street() -> Dict[str, Any]:
    case_id = "case_c_street_cross_safely"
    result = run_agent_planning_dryrun(fixture_street_cross_safely())
    scene = (
        result.get("situation_understanding_candidate", {})
        .get("scene_profile_candidate", {})
        .get("scene_type")
    )
    tools = _tools(result)
    passed = (
        scene == "street_crossing"
        and "detection" in tools
        and "depth" in tools
        and "tracking" in tools
        and "ocr" not in tools  # no sign/text evidence → OCR not full-image
        and result.get("l2_constrains_tools_assertion", {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_user_goal_override() -> Dict[str, Any]:
    case_id = "case_d_user_goal_overrides_scene"
    result = run_agent_planning_dryrun(fixture_user_goal_overrides_shopfront())
    scene = (
        result.get("situation_understanding_candidate", {})
        .get("scene_profile_candidate", {})
        .get("scene_type")
    )
    plan = result.get("selected_plan_candidate") or {}
    goal = _goal(result)
    tools = _tools(result)
    competition = result.get("plan_competition") or {}
    selection = competition.get("selection_trace") or {}
    goal_traces = (plan.get("plan_goal_candidate") or {}).get("trace_refs") or []
    override_traced = any(t.get("stage") == "user_goal_overrides_task_clue" for t in goal_traces)
    # Selected plan must NOT be OCR-first identify/read when user wants entrance
    ocr_first = goal in ("read_text", "identify_place") and tools == ["ocr"]
    passed = (
        scene == "shopfront_sign"
        and goal == "navigate"
        and (plan.get("plan_strategy") or {}).get("strategy_type") == "navigation_support"
        and ("detection" in tools or "depth" in tools)
        and not ocr_first
        and (override_traced or selection.get("reason") == "user_goal_dominates_scene_default")
        and result.get("l1_drives_l2_assertion", {}).get("passed") is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "result": result,
        "assertions": {
            "goal_over_scene_default": goal == "navigate" and scene == "shopfront_sign",
            "not_ocr_first": not ocr_first,
            "competition_present": bool(competition.get("competing_plans")),
        },
    }


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_shopfront,
        dryrun_case_b_subway,
        dryrun_case_c_street,
        dryrun_case_d_user_goal_override,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    case_a = next((c for c in cases if c["case_id"] == "case_a_job_564f1aa93983_shop_sign"), {})
    a_res = case_a.get("result") or {}
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-DryRun-v1-001",
        "deterministic_dryrun_only": True,
        "no_real_model_execution": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_cases_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "core_validations": {
            "l1_drives_l2": all(
                (c.get("result") or {}).get("l1_drives_l2_assertion", {}).get("passed")
                for c in cases
            ),
            "l2_constrains_tools": all(
                (c.get("result") or {}).get("l2_constrains_tools_assertion", {}).get("passed")
                for c in cases
            ),
            "plan_competition_present": all(
                bool((c.get("result") or {}).get("plan_competition")) for c in cases
            ),
        },
        "job_564f1aa93983_l2_result": {
            "job_id": "job_564f1aa93983",
            "l1_scene": (a_res.get("situation_understanding_candidate") or {})
            .get("scene_profile_candidate", {})
            .get("scene_type"),
            "l2_goal": _goal(a_res),
            "active_tools": _tools(a_res),
            "noop_tools": _noops(a_res),
            "slam_not_activated": "slam" not in _tools(a_res),
        },
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
