#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))

from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_api_v1 import (  # noqa: E402
    run_field_perception_orchestrator_module_v1,
)
from capabilities.midplatform.field_perception_orchestrator.module.field_perception_module_types_v1 import (  # noqa: E402
    BOUNDARY_FALSE_FIELDS,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "task_context": {
            "task_id": f"task_{case_id}",
            "goal": "navigate safely",
        },
        "current_field_state": {
            "field_snapshot_ref": f"field_snapshot_{case_id}",
            "known_entities": ["road", "pedestrian"],
            "known_regions": ["front_corridor", "left_side"],
            "temporary_overlays": [],
            "active_risks": [],
            "navigation_relevance": {"front_corridor": 0.9},
            "uncertainties": [],
            "conflicts": [],
            "stale_evidence": [],
            "missing_information": [],
        },
        "recent_observation_summary": {
            "sufficient_for_decision": False,
            "expired": False,
        },
        "available_visual_capabilities": [
            "detection",
            "segmentation",
            "depth",
            "ocr",
            "tracking",
            "region_intelligence",
            "roi_detection",
            "layout_analysis",
            "grounding",
            "spatial_relation",
        ],
        "available_model_assets": [
            {
                "model_id": "vision_general_v2",
                "supports": ["detection", "tracking"],
                "preferred": True,
            },
            {
                "model_id": "ocr_reader_v1",
                "supports": ["ocr", "layout_analysis"],
                "preferred": True,
            },
            {
                "model_id": "seg_depth_v1",
                "supports": ["segmentation", "depth"],
                "preferred": False,
            },
        ],
        "resource_budget": {
            "cpu_budget": 4,
            "memory_budget_mb": 4096,
            "latency_budget_ms": 2500,
        },
        "temporal_context": {
            "is_night": False,
            "low_light": False,
            "fast_changing_scene": False,
        },
        "uncertainty_state": {},
        "conflict_state": {},
        "previous_invocation_history": [],
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(field) is False for field in BOUNDARY_FALSE_FIELDS)


def _plan_contract_present(result: Mapping[str, Any]) -> bool:
    plan = dict(result.get("field_perception_plan") or {})
    required = (
        "plan_id",
        "task_id",
        "field_snapshot_ref",
        "observation_goal",
        "information_gap",
        "target_region",
        "target_entity_types",
        "requested_visual_capabilities",
        "preferred_model_candidates",
        "fallback_model_candidates",
        "resolution_level",
        "temporal_window",
        "observation_priority",
        "confidence_requirement",
        "stop_condition",
        "reobserve_condition",
        "expected_evidence_types",
        "reasoning_summary",
        "trace_ref",
        "replay_key",
    )
    return all(key in plan for key in required)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    c1 = _base_payload("road_known")
    c1["recent_observation_summary"] = {
        "sufficient_for_decision": True,
        "expired": False,
    }
    scenarios["1_road_known_no_visual_needed"] = c1

    c2 = _base_payload("obstacle_stale")
    c2["current_field_state"]["stale_evidence"] = ["front_obstacle"]
    scenarios["2_obstacle_stale_need_redetect"] = c2

    c3 = _base_payload("find_exit")
    c3["task_context"]["goal"] = "find nearest exit"
    scenarios["3_find_exit"] = c3

    c4 = _base_payload("find_entrance")
    c4["task_context"]["goal"] = "find shopping mall entrance"
    scenarios["4_find_entrance"] = c4

    c5 = _base_payload("read_notice")
    c5["task_context"]["goal"] = "read notice board"
    scenarios["5_read_notice"] = c5

    c6 = _base_payload("traffic_unknown")
    c6["task_context"]["goal"] = "check traffic light state"
    c6["current_field_state"]["missing_information"] = ["traffic_light_state"]
    scenarios["6_traffic_light_unknown"] = c6

    c7 = _base_payload("traffic_recent")
    c7["task_context"]["goal"] = "check traffic light state"
    c7["recent_observation_summary"] = {
        "sufficient_for_decision": True,
        "expired": False,
    }
    c7["previous_invocation_history"] = [
        {
            "observation_goal": "confirm_traffic_light_state",
            "success": True,
            "fresh": True,
        }
    ]
    scenarios["7_traffic_recent_no_repeat"] = c7

    c8 = _base_payload("construction_conflict")
    c8["current_field_state"]["conflicts"] = ["construction_zone_inconsistent"]
    c8["conflict_state"] = {"conflicting_claims": ["construction_boundary_conflict"]}
    scenarios["8_construction_conflict"] = c8

    c9 = _base_payload("target_uncertain")
    c9["task_context"]["goal"] = "locate target object"
    c9["uncertainty_state"] = {"information_gap": ["target_location_uncertain"]}
    scenarios["9_target_uncertain"] = c9

    c10 = _base_payload("person_lost")
    c10["task_context"]["goal"] = "track target person"
    c10["current_field_state"]["missing_information"] = ["target_person_presence"]
    scenarios["10_person_lost"] = c10

    c11 = _base_payload("night_low_light")
    c11["temporal_context"] = {
        "is_night": True,
        "low_light": True,
        "fast_changing_scene": False,
    }
    c11["current_field_state"]["missing_information"] = ["front_space_visibility"]
    scenarios["11_night_low_light"] = c11

    c12 = _base_payload("ocr_ambiguous")
    c12["task_context"]["goal"] = "read notice board"
    c12["current_field_state"]["conflicts"] = ["text_ownership_ambiguous"]
    scenarios["12_ocr_ambiguous_ownership"] = c12

    c13 = _base_payload("evidence_sufficient")
    c13["recent_observation_summary"] = {
        "sufficient_for_decision": True,
        "expired": False,
    }
    c13["current_field_state"]["missing_information"] = []
    scenarios["13_sufficient_evidence_no_call"] = c13

    c14 = _base_payload("resource_low")
    c14["resource_budget"] = {
        "cpu_budget": 1,
        "memory_budget_mb": 512,
        "latency_budget_ms": 800,
    }
    c14["task_context"]["goal"] = "check passable path"
    c14["current_field_state"]["missing_information"] = ["front_passability"]
    scenarios["14_resource_low_degrade"] = c14

    c15 = _base_payload("multi_models")
    c15["task_context"]["goal"] = "find entrance and read sign"
    c15["current_field_state"]["missing_information"] = [
        "entrance_location",
        "entry_sign_text",
    ]
    c15["available_model_assets"].append(
        {
            "model_id": "multi_scene_v3",
            "supports": ["detection", "ocr", "region_intelligence"],
            "preferred": False,
        }
    )
    scenarios["15_multi_model_candidates"] = c15

    c16 = _base_payload("no_explicit_task")
    c16["task_context"]["goal"] = ""
    c16["recent_observation_summary"] = {
        "sufficient_for_decision": False,
        "expired": False,
    }
    c16["current_field_state"]["missing_information"] = ["minimum_safety_scan"]
    scenarios["16_no_explicit_task_min_safety"] = c16

    expected_need_handoff = {
        "1_road_known_no_visual_needed": False,
        "2_obstacle_stale_need_redetect": True,
        "3_find_exit": True,
        "4_find_entrance": True,
        "5_read_notice": True,
        "6_traffic_light_unknown": True,
        "7_traffic_recent_no_repeat": False,
        "8_construction_conflict": True,
        "9_target_uncertain": True,
        "10_person_lost": True,
        "11_night_low_light": True,
        "12_ocr_ambiguous_ownership": True,
        "13_sufficient_evidence_no_call": False,
        "14_resource_low_degrade": True,
        "15_multi_model_candidates": True,
        "16_no_explicit_task_min_safety": True,
    }

    failed_cases = []
    rows = []
    diagnostics_present_all = True
    trace_present_all = True
    replay_present_all = True
    information_gap_correct = True
    observation_goal_present = True
    need_visual_invocation_judgement_correct = True
    capability_plan_generated = True
    model_requirement_generated = True
    stop_condition_present = True
    reobserve_condition_present = True
    vision_handoff_present = True
    boundary_preserved = True
    unhandled_exceptions = 0

    for case_id, payload in scenarios.items():
        result = run_field_perception_orchestrator_module_v1(payload)
        if bool(result.get("unhandled_exception", False)):
            unhandled_exceptions += 1

        diagnostics = dict(result.get("diagnostics") or {})
        plan = dict(result.get("field_perception_plan") or {})
        handoff = dict(result.get("vision_handoff_candidate") or {})
        info_gap = dict(result.get("information_gap") or {})

        if not diagnostics:
            diagnostics_present_all = False
        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        if not isinstance(info_gap.get("information_gap"), tuple):
            information_gap_correct = False
        if not str(plan.get("observation_goal") or ""):
            observation_goal_present = False
        if not bool(
            result.get("capability_plan", {}).get("capability_plan_generated", False)
        ):
            capability_plan_generated = False
        if not isinstance(
            result.get("model_requirements", {}).get("model_requirements"), dict
        ):
            model_requirement_generated = False
        if not isinstance(plan.get("stop_condition"), dict):
            stop_condition_present = False
        if not isinstance(plan.get("reobserve_condition"), dict):
            reobserve_condition_present = False
        if not isinstance(handoff, dict):
            vision_handoff_present = False

        expected_handoff = expected_need_handoff[case_id]
        actual_handoff = bool(handoff.get("handoff_required", False))
        if expected_handoff != actual_handoff:
            need_visual_invocation_judgement_correct = False

        case_pass = _plan_contract_present(result)
        case_pass = case_pass and isinstance(diagnostics, dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)
        case_pass = case_pass and expected_handoff == actual_handoff

        if case_id == "11_night_low_light":
            fallback = tuple(plan.get("fallback_model_candidates") or ())
            case_pass = case_pass and ("low_light_enhancer_v1" in fallback)
        if case_id == "14_resource_low_degrade":
            case_pass = (
                case_pass
                and str(result.get("module_status") or "") == "degraded_resource_plan"
            )
            case_pass = case_pass and str(plan.get("resolution_level") or "") == "low"
        if case_id in {
            "1_road_known_no_visual_needed",
            "7_traffic_recent_no_repeat",
            "13_sufficient_evidence_no_call",
        }:
            case_pass = (
                case_pass
                and str(result.get("module_status") or "")
                == "no_visual_invocation_required"
            )

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "module_status": result.get("module_status"),
                "handoff_required": actual_handoff,
                "expected_handoff_required": expected_handoff,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    report = {
        "phase": "Phase-Luna-Field-Perception-Orchestrator-Functional-Module-Planning-And-Build-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "information_gap_correct": information_gap_correct,
        "observation_goal_present": observation_goal_present,
        "need_visual_invocation_judgement_correct": need_visual_invocation_judgement_correct,
        "capability_plan_generated": capability_plan_generated,
        "model_requirement_generated": model_requirement_generated,
        "stop_condition_present": stop_condition_present,
        "reobserve_condition_present": reobserve_condition_present,
        "vision_handoff_present": vision_handoff_present,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
    }
    report["integration_pass"] = (
        passed_cases == total_cases
        and not failed_cases
        and information_gap_correct
        and observation_goal_present
        and need_visual_invocation_judgement_correct
        and capability_plan_generated
        and model_requirement_generated
        and stop_condition_present
        and reobserve_condition_present
        and vision_handoff_present
        and diagnostics_present_all
        and trace_present_all
        and replay_present_all
        and boundary_preserved
        and unhandled_exceptions == 0
    )
    return report


def main() -> int:
    report = run_integration()
    out_dir = Path(
        "_tmp_eval_out/field_perception_orchestrator_module_integration_v1_smoke_v0"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "field_perception_orchestrator_module_integration_v1.json"
    out_file.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "information_gap_correct": report["information_gap_correct"],
                "observation_goal_present": report["observation_goal_present"],
                "need_visual_invocation_judgement_correct": report[
                    "need_visual_invocation_judgement_correct"
                ],
                "capability_plan_generated": report["capability_plan_generated"],
                "model_requirement_generated": report["model_requirement_generated"],
                "stop_condition_present": report["stop_condition_present"],
                "reobserve_condition_present": report["reobserve_condition_present"],
                "vision_handoff_present": report["vision_handoff_present"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "boundary_preserved": report["boundary_preserved"],
                "output": str(out_file.resolve()),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
