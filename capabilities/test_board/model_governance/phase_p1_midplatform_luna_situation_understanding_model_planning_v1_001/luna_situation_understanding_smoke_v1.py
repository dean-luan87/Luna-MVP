# -*- coding: utf-8
"""Luna Situation Understanding Model — planning smoke v1 (deterministic stub)."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.situation_understanding.luna_situation_understanding_processor_v1 import (
    build_situation_understanding_candidate,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)

FINAL_SMOKE_GO = FINAL_GO.replace("_GO", "_SMOKE_GO")
FINAL_SMOKE_BLOCKED = FINAL_BLOCKED.replace("_BLOCKED", "_SMOKE_BLOCKED")


def _evidence(eid: str, source: str, etype: str, value: str, conf: float = 0.8) -> Dict[str, Any]:
    return {
        "evidence_id": eid,
        "source": source,
        "evidence_type": etype,
        "value": value,
        "confidence": conf,
        "source_trace_ref": eid,
        "candidate_only": True,
        "not_fact": True,
    }


def _base_input(
    file_name: str,
    *,
    goal_type: str = "unknown",
    evidence: List[Dict[str, Any]] | None = None,
    case_refs: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    return {
        "frame_context": {
            "frame_id": f"frame_{file_name}",
            "image_id": f"img_{file_name}",
            "file_name": file_name,
            "timestamp": "2026-06-30T00:00:00Z",
            "source": "test_fixture",
            "candidate_only": True,
            "not_fact": True,
        },
        "user_goal_candidate": {
            "goal_type": goal_type,
            "confidence": 0.7 if goal_type != "unknown" else 0.2,
            "source": "user_command" if goal_type != "unknown" else "unknown",
            "candidate_only": True,
            "not_fact": True,
        },
        "visual_evidence_candidates": evidence or [],
        "situation_case_refs": case_refs or [],
        "environment_memory_candidates": [],
        "human_correction_signals": [],
        "available_capabilities": [
            {"capability_id": "cap_ocr", "capability_type": "ocr", "availability": "available"},
            {"capability_id": "cap_slam", "capability_type": "slam", "availability": "available"},
            {"capability_id": "cap_depth", "capability_type": "depth", "availability": "available"},
            {"capability_id": "cap_detection", "capability_type": "detection", "availability": "available"},
            {"capability_id": "cap_tracking", "capability_type": "tracking", "availability": "available"},
        ],
        "candidate_only": True,
        "not_fact": True,
    }


def _caps(result: Dict[str, Any], bucket: str) -> List[str]:
    return [h["capability_type"] for h in result.get("model_need_hints", {}).get(bucket, [])]


def _task_types(result: Dict[str, Any]) -> List[str]:
    return [c["task_type"] for c in result.get("task_clue_candidates", [])]


def _info_types(result: Dict[str, Any]) -> List[str]:
    return [m["info_type"] for m in result.get("missing_information_candidates", [])]


def smoke_case_a_shopfront() -> Dict[str, Any]:
    case_id = "case_a_shopfront_sign"
    inp = _base_input(
        "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        goal_type="identify",
        evidence=[
            _evidence("ev1", "metadata", "text_density", "large_text_density"),
            _evidence("ev2", "sam", "scene_hint", "storefront_layout"),
            _evidence("ev3", "metadata", "region", "logo_region"),
        ],
        case_refs=[{
            "case_id": "shopfront_sign_case",
            "case_type": "shopfront_sign",
            "similarity_score": 0.91,
            "matched_clues": ["large_text_density", "storefront_layout"],
            "candidate_only": True,
            "not_fact": True,
        }],
    )
    result = build_situation_understanding_candidate(inp)
    scene = result["scene_profile_candidate"]
    survival = result["survival_context"]
    passed = (
        scene["scene_type"] == "shopfront_sign"
        and survival["environment_type"] == "commercial_entry"
        and survival["information_relevance"] == "high"
        and survival["mobility_relevance"] == "low"
        and "read_text" in _task_types(result)
        and "identify_place" in _task_types(result)
        and "text_content" in _info_types(result)
        and "place_identity" in _info_types(result)
        and "ocr" in _caps(result, "likely_needed")
        and "slam" in _caps(result, "not_needed")
        and "tracking" in _caps(result, "not_needed")
        and "depth" in _caps(result, "not_needed")
        and result["candidate_only"] is True
        and result["not_fact"] is True
        and result.get("no_runner_invocation") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_subway() -> Dict[str, Any]:
    case_id = "case_b_subway_platform"
    inp = _base_input(
        "subway_direction_sign_jiahuihu.png",
        goal_type="find",
        evidence=[
            _evidence("ev1", "metadata", "scene_hint", "platform_screen_door"),
            _evidence("ev2", "text_detector", "text_density", "direction_sign_text_density"),
            _evidence("ev3", "metadata", "scene_hint", "public_transport_hint"),
        ],
    )
    result = build_situation_understanding_candidate(inp)
    passed = (
        result["scene_profile_candidate"]["scene_type"] == "subway_platform"
        and "find_direction" in _task_types(result)
        and "read_text" in _task_types(result)
        and "ocr" in _caps(result, "likely_needed")
        and "slam" in _caps(result, "not_needed")
        and result["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_street() -> Dict[str, Any]:
    case_id = "case_c_street_crossing"
    inp = _base_input(
        "street_crossing_fixture.png",
        goal_type="navigate",
        evidence=[
            _evidence("ev1", "detection", "scene_hint", "crosswalk_hint"),
            _evidence("ev2", "detection", "object_hint", "vehicle_hint"),
            _evidence("ev3", "detection", "object_hint", "person_hint"),
            _evidence("ev4", "metadata", "spatial_hint", "open_road"),
        ],
    )
    result = build_situation_understanding_candidate(inp)
    likely = _caps(result, "likely_needed")
    passed = (
        result["scene_profile_candidate"]["scene_type"] == "street_crossing"
        and "assess_walkable" in _task_types(result)
        and "avoid_obstacle" in _task_types(result)
        and "detection" in likely
        and "depth" in likely
        and "tracking" in likely
        and "ocr" not in likely
        and result["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_corridor() -> Dict[str, Any]:
    case_id = "case_d_corridor"
    inp = _base_input(
        "corridor_fixture.png",
        goal_type="navigate",
        evidence=[
            _evidence("ev1", "metadata", "spatial_hint", "corridor_lines"),
            _evidence("ev2", "depth", "spatial_hint", "indoor_path"),
            _evidence("ev3", "sam", "spatial_hint", "spatial_boundary"),
        ],
    )
    result = build_situation_understanding_candidate(inp)
    likely = _caps(result, "likely_needed")
    not_needed = _caps(result, "not_needed")
    passed = (
        result["scene_profile_candidate"]["scene_type"] == "corridor"
        and result["survival_context"]["mobility_relevance"] == "high"
        and "depth" in likely
        and "slam" in likely
        and "ocr" in not_needed
        and result["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_unknown() -> Dict[str, Any]:
    case_id = "case_e_unknown_scene"
    inp = _base_input("ambiguous_fixture.png", goal_type="unknown", evidence=[
        _evidence("ev1", "metadata", "scene_hint", "weak_hint", 0.2),
    ])
    result = build_situation_understanding_candidate(inp)
    likely = _caps(result, "likely_needed")
    uncertainty = result["uncertainty"]
    passed = (
        result["scene_profile_candidate"]["scene_type"] == "unknown_scene"
        and (uncertainty["needs_manual_review"] is True or "ask_user" in uncertainty.get("fallback_suggestion", ""))
        and len(likely) == 0
        and result.get("no_runner_invocation") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_f_teacher_label() -> Dict[str, Any]:
    case_id = "case_f_teacher_label_input"
    inp = _base_input(
        "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        goal_type="identify",
        evidence=[
            _evidence("ev_teacher", "teacher_label", "scene_hint", "shopfront_sign", 0.75),
            _evidence("ev1", "metadata", "text_density", "large_text_density"),
        ],
        case_refs=[{
            "case_id": "teacher_derived_shopfront_case",
            "case_type": "shopfront_sign",
            "similarity_score": 0.88,
            "matched_clues": ["teacher_label_accepted"],
            "candidate_only": True,
            "not_fact": True,
        }],
    )
    result = build_situation_understanding_candidate(inp)
    scene = result["scene_profile_candidate"]
    passed = (
        scene["scene_type"] == "shopfront_sign"
        and scene["candidate_only"] is True
        and scene["not_fact"] is True
        and "teacher_derived_shopfront_case" in scene.get("case_refs", [])
        and result["candidate_only"] is True
    )
    return {"case_id": case_id, "passed": passed, "result": result, "teacher_not_direct_owner": True}


def smoke_case_g_runner_override() -> Dict[str, Any]:
    case_id = "case_g_runner_unknown_scene_override"
    inp = _base_input(
        "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
        goal_type="identify",
        evidence=[
            _evidence("ev_runner", "runner_scene_hint", "scene_hint", "unknown_scene", 0.6),
            _evidence("ev1", "metadata", "text_density", "large_text_density"),
            _evidence("ev2", "sam", "scene_hint", "storefront_layout"),
        ],
        case_refs=[{
            "case_id": "shopfront_sign_case",
            "case_type": "shopfront_sign",
            "similarity_score": 0.9,
            "matched_clues": ["storefront_layout"],
            "candidate_only": True,
            "not_fact": True,
        }],
    )
    result = build_situation_understanding_candidate(inp)
    scene = result["scene_profile_candidate"]
    conflict = any(
        t.get("stage") == "scene_conflict_resolution"
        for t in scene.get("trace_refs", [])
    )
    passed = (
        scene["scene_type"] == "shopfront_sign"
        and scene["scene_type"] != "unknown_scene"
        and conflict
        and result["candidate_only"] is True
    )
    return {"case_id": case_id, "passed": passed, "result": result, "runner_not_scene_owner": True}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront,
        smoke_case_b_subway,
        smoke_case_c_street,
        smoke_case_d_corridor,
        smoke_case_e_unknown,
        smoke_case_f_teacher_label,
        smoke_case_g_runner_override,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    passed_count = sum(1 for c in cases if c.get("passed"))
    decision = FINAL_SMOKE_GO if not failed else FINAL_SMOKE_BLOCKED
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001",
        "deterministic_smoke_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": passed_count,
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": decision,
    }
