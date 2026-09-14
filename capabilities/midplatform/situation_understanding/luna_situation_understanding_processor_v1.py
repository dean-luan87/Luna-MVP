# -*- coding: utf-8
"""Luna Situation Understanding Model — deterministic processor stub v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from capabilities.midplatform.situation_understanding.luna_situation_understanding_types_v1 import (
    POLICY_REF,
)

SHOPFRONT_FILES = (
    "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
    "shop_sign.png",
)
SUBWAY_FILES = ("subway_direction_sign_jiahuihu.png",)
STREET_HINTS = ("crosswalk_hint", "vehicle_hint", "person_hint", "open_road")
CORRIDOR_HINTS = ("corridor_lines", "indoor_path", "spatial_boundary")
SHOPFRONT_HINTS = ("large_text_density", "storefront_layout", "logo_region")
SUBWAY_HINTS = ("platform_screen_door", "direction_sign_text_density", "public_transport_hint")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _evidence_values(input_data: Dict[str, Any]) -> Set[str]:
    return {e.get("value", "") for e in input_data.get("visual_evidence_candidates", [])}


def _has_evidence(input_data: Dict[str, Any], *hints: str) -> bool:
    vals = _evidence_values(input_data)
    return any(h in vals for h in hints)


def _goal_type(input_data: Dict[str, Any]) -> str:
    return input_data.get("user_goal_candidate", {}).get("goal_type", "unknown")


def _case_types(input_data: Dict[str, Any]) -> List[str]:
    return [c.get("case_type", "") for c in input_data.get("situation_case_refs", [])]


def _runner_scene_hint(input_data: Dict[str, Any]) -> Optional[str]:
    for ev in input_data.get("visual_evidence_candidates", []):
        if ev.get("source") == "runner_scene_hint" and ev.get("evidence_type") == "scene_hint":
            return ev.get("value")
    return None


def infer_scene_profile_candidate(input_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Infer scene from evidence + case refs. Runner scene_hint is evidence only, not owner."""
    frame = input_data.get("frame_context", {})
    file_name = frame.get("file_name", "")
    case_types = _case_types(input_data)
    evidence_refs: List[str] = []
    case_refs: List[str] = []
    conflict_traces: List[Dict[str, Any]] = []

    runner_hint = _runner_scene_hint(input_data)
    if runner_hint:
        conflict_traces.append({
            "stage": "runner_scene_hint_received",
            "ref": runner_hint,
            "resolution": "runner_hint_is_evidence_only_not_owner",
        })

    scene_type = "unknown_scene"
    confidence = 0.35

    if file_name in SHOPFRONT_FILES or "shopfront_sign" in case_types or _has_evidence(input_data, *SHOPFRONT_HINTS):
        scene_type = "shopfront_sign"
        confidence = 0.88
    elif file_name in SUBWAY_FILES or "subway_platform" in case_types or _has_evidence(input_data, *SUBWAY_HINTS):
        scene_type = "subway_platform"
        confidence = 0.85
    elif _has_evidence(input_data, *STREET_HINTS):
        scene_type = "street_crossing"
        confidence = 0.82
    elif _has_evidence(input_data, *CORRIDOR_HINTS):
        scene_type = "corridor"
        confidence = 0.80

    for ev in input_data.get("visual_evidence_candidates", []):
        evidence_refs.append(ev.get("evidence_id", ev.get("value", "")))
    for cref in input_data.get("situation_case_refs", []):
        case_refs.append(cref.get("case_id", ""))

    if runner_hint and runner_hint != scene_type:
        conflict_traces.append({
            "stage": "runner_scene_hint_conflict",
            "runner_hint": runner_hint,
            "situation_layer_scene": scene_type,
            "resolution": "situation_layer_owns_scene_profile",
            "policy_ref": "scene_profile_owned_by_situation_layer",
        })

    profile = {
        "scene_type": scene_type,
        "confidence": confidence,
        "evidence_refs": evidence_refs,
        "case_refs": case_refs,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": conflict_traces,
        "policy_refs": [POLICY_REF, "scene_profile_owned_by_situation_layer"],
    }
    return profile, conflict_traces


def infer_survival_context(
    input_data: Dict[str, Any],
    scene: Dict[str, Any],
) -> Dict[str, Any]:
    scene_type = scene.get("scene_type", "unknown_scene")
    goal = _goal_type(input_data)

    env_map = {
        "shopfront_sign": "commercial_entry",
        "subway_platform": "public_transport",
        "street_crossing": "street_mobility",
        "corridor": "indoor_navigation",
        "indoor_store": "retail_consumption",
    }
    environment_type = env_map.get(scene_type, "unknown")

    mobility = "low"
    information = "medium"
    risk = "low"
    task_pressure = "low"
    uncertainty_level = "medium"

    if scene_type == "shopfront_sign":
        information = "high"
        mobility = "low"
    elif scene_type == "subway_platform":
        information = "high"
        mobility = "medium" if goal == "navigate" else "low"
    elif scene_type == "street_crossing":
        mobility = "high"
        risk = "medium"
        information = "low"
        task_pressure = "medium" if goal in ("navigate", "avoid") else "low"
    elif scene_type == "corridor":
        mobility = "high"
        information = "low"
    elif scene_type == "unknown_scene":
        uncertainty_level = "high"
        risk = "unknown"
        mobility = "unknown"
        information = "unknown"

    return {
        "environment_type": environment_type,
        "risk_level": risk,
        "mobility_relevance": mobility,
        "information_relevance": information,
        "social_relevance": "low",
        "task_pressure": task_pressure,
        "uncertainty_level": uncertainty_level,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "infer_survival_context", "scene_type": scene_type}],
        "policy_refs": [POLICY_REF],
    }


def infer_task_clues(
    input_data: Dict[str, Any],
    scene: Dict[str, Any],
    survival_context: Dict[str, Any],
) -> List[Dict[str, Any]]:
    scene_type = scene.get("scene_type", "unknown_scene")
    goal = _goal_type(input_data)
    clues: List[Dict[str, Any]] = []

    def _clue(task_type: str, priority: str, reason: str, refs: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            "task_type": task_type,
            "priority": priority,
            "reason": reason,
            "evidence_refs": refs or scene.get("evidence_refs", []),
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "infer_task_clues", "task_type": task_type}],
        }

    if scene_type == "shopfront_sign":
        clues.extend([
            _clue("read_text", "P0", "店招场景默认需要读取文字"),
            _clue("identify_place", "P1", "店招场景需要识别地点/店名"),
        ])
    elif scene_type == "subway_platform":
        clues.append(_clue("find_direction", "P0", "地铁站场景默认需要找方向"))
        clues.append(_clue("read_text", "P0", "方向牌/站台信息需要读文字"))
    elif scene_type == "street_crossing":
        clues.append(_clue("assess_walkable", "P0", "街道路口需要评估可通行性"))
        clues.append(_clue("avoid_obstacle", "P1", "街道路口需要避让车辆/行人"))
    elif scene_type == "corridor":
        clues.append(_clue("assess_walkable", "P0", "走廊导航需要评估可通行路径"))
        if goal == "navigate":
            clues.append(_clue("find_direction", "P1", "走廊导航需要方向/路径线索"))
    elif scene_type == "unknown_scene":
        clues.append(_clue("ask_user", "P0", "未知场景需要用户目标澄清"))
        clues.append(_clue("manual_review", "P1", "未知场景建议人工复核"))

    if goal == "identify" and scene_type == "shopfront_sign":
        pass  # already covered
    elif goal == "find" and scene_type == "subway_platform":
        pass

    return clues


def infer_missing_information(
    input_data: Dict[str, Any],
    task_clues: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    missing: List[Dict[str, Any]] = []
    task_types = {c["task_type"] for c in task_clues}

    mapping = {
        "read_text": ("text_content", "ocr", "需要读取可见文字内容"),
        "identify_place": ("place_identity", "ocr", "需要识别地点/店名"),
        "find_direction": ("direction_info", "ocr", "需要方向/指引信息"),
        "assess_walkable": ("walkable_area", "depth", "需要可通行区域信息"),
        "avoid_obstacle": ("dynamic_motion", "tracking", "需要动态障碍信息"),
        "ask_user": ("user_goal", "speech", "需要用户目标澄清"),
    }
    for tt in task_types:
        if tt in mapping:
            info_type, cap, reason = mapping[tt]
            missing.append({
                "info_type": info_type,
                "required_for": tt,
                "suggested_capability": cap,
                "reason": reason,
                "candidate_only": True,
                "not_fact": True,
                "trace_refs": [{"stage": "infer_missing_information", "info_type": info_type}],
            })
    return missing


def infer_attention_target_hints(
    input_data: Dict[str, Any],
    scene: Dict[str, Any],
    task_clues: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    scene_type = scene.get("scene_type", "unknown_scene")
    hints: List[Dict[str, Any]] = []

    def _hint(target_type: str, priority: str, reason: str) -> Dict[str, Any]:
        return {
            "target_hint_id": _uid("ath"),
            "target_type": target_type,
            "priority": priority,
            "reason": reason,
            "region_ref_optional": "",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "infer_attention_target_hints"}],
        }

    if scene_type == "shopfront_sign":
        hints.append(_hint("primary_text_block", "P0", "店招主文字区域"))
        hints.append(_hint("unknown_region", "P2", "店招周边次要区域"))
    elif scene_type == "subway_platform":
        hints.append(_hint("direction_sign", "P0", "方向指示牌"))
    elif scene_type == "street_crossing":
        hints.append(_hint("walkable_path", "P0", "可通行路径"))
        hints.append(_hint("obstacle_candidate", "P1", "车辆/行人障碍"))
    elif scene_type == "corridor":
        hints.append(_hint("spatial_boundary", "P0", "走廊空间边界"))
        hints.append(_hint("walkable_path", "P0", "走廊可通行路径"))
    else:
        hints.append(_hint("unknown_region", "P0", "未知场景全图需审慎关注"))

    return hints


def infer_model_need_hints(
    input_data: Dict[str, Any],
    task_clues: List[Dict[str, Any]],
    missing_information: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    scene_type = input_data.get("_inferred_scene_type", "unknown_scene")
    goal = _goal_type(input_data)
    has_text_evidence = _has_evidence(
        input_data, "large_text_density", "direction_sign_text_density", "sign_text",
    )

    likely: List[Dict[str, Any]] = []
    optional: List[Dict[str, Any]] = []
    not_needed: List[Dict[str, Any]] = []

    def _need(cap: str, reason: str, policy: str, bucket: str) -> None:
        item = {
            "capability_type": cap,
            "reason": reason,
            "policy_ref": policy,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "infer_model_need_hints", "capability": cap}],
        }
        if bucket == "likely":
            likely.append(item)
        elif bucket == "optional":
            optional.append(item)
        else:
            not_needed.append(item)

    if scene_type == "shopfront_sign":
        _need("ocr", "shopfront_sign 默认需要 OCR 读取文字", "shopfront_sign_prefers_ocr", "likely")
        for cap in ("slam", "tracking", "depth"):
            _need(cap, "文字识别场景默认不需要空间/动态模型", "text_task_no_default_slam", "not_needed")
    elif scene_type == "subway_platform":
        _need("ocr", "地铁站方向/站台信息读取", "subway_direction_prefers_ocr", "likely")
        _need("detection", "站台门/行人检测可选", "subway_direction_prefers_ocr", "optional")
        if goal != "navigate":
            _need("slam", "非导航目标不需要 SLAM", "subway_direction_prefers_ocr", "not_needed")
        else:
            _need("slam", "导航目标下 SLAM 可选", "subway_direction_prefers_ocr", "optional")
    elif scene_type == "street_crossing":
        for cap in ("detection", "depth", "tracking"):
            _need(cap, "街道路口通行评估需要感知动态与深度", "street_crossing_prefers_detection_depth_tracking", "likely")
        if has_text_evidence:
            _need("ocr", "仅在有文字/标识证据时可选 OCR", "street_crossing_prefers_detection_depth_tracking", "optional")
        else:
            _need("ocr", "无文字证据时不应全图默认 OCR", "street_crossing_prefers_detection_depth_tracking", "not_needed")
    elif scene_type == "corridor":
        _need("depth", "走廊空间理解需要深度", "corridor_prefers_spatial_tools", "likely")
        _need("slam", "走廊导航需要空间连续性", "corridor_prefers_spatial_tools", "likely")
        if has_text_evidence:
            _need("ocr", "有文字证据时 OCR 可选", "corridor_prefers_spatial_tools", "optional")
        else:
            _need("ocr", "走廊默认不需要 OCR", "corridor_prefers_spatial_tools", "not_needed")
    elif scene_type == "unknown_scene":
        _need("vlm", "未知场景可用 VLM advisor 辅助理解", "unknown_scene_requires_uncertainty", "optional")
        for cap in ("slam", "detection", "ocr", "tracking", "depth"):
            _need(cap, "未知场景禁止 blanket activate", "no_blanket_model_activation", "not_needed")

    return {"likely_needed": likely, "optional": optional, "not_needed": not_needed}


def build_uncertainty(
    input_data: Dict[str, Any],
    scene: Dict[str, Any],
    task_clues: List[Dict[str, Any]],
) -> Dict[str, Any]:
    scene_type = scene.get("scene_type", "unknown_scene")
    goal = _goal_type(input_data)
    confidence = scene.get("confidence", 0.0)

    needs_user_goal = goal == "unknown" and scene_type == "unknown_scene"
    needs_manual_review = scene_type == "unknown_scene" or confidence < 0.5
    fallback = ""
    if needs_manual_review:
        fallback = "ask_user"
    if scene_type == "unknown_scene":
        fallback = "ask_user / vlm_advisor"

    return {
        "needs_user_goal": needs_user_goal,
        "needs_manual_review": needs_manual_review,
        "ambiguity_reason_optional": "weak_evidence" if scene_type == "unknown_scene" else "",
        "confidence_gap_optional": f"{1.0 - confidence:.2f}" if confidence < 0.7 else "",
        "fallback_suggestion": fallback,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "build_uncertainty", "scene_type": scene_type}],
        "policy_refs": [POLICY_REF, "unknown_scene_requires_uncertainty"],
    }


def build_situation_understanding_candidate(
    input_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Main entry: build full situation_understanding_candidate from input."""
    scene, conflict_traces = infer_scene_profile_candidate(input_data)
    input_data = {**input_data, "_inferred_scene_type": scene["scene_type"]}

    survival = infer_survival_context(input_data, scene)
    task_clues = infer_task_clues(input_data, scene, survival)
    missing = infer_missing_information(input_data, task_clues)
    attention = infer_attention_target_hints(input_data, scene, task_clues)
    model_needs = infer_model_need_hints(input_data, task_clues, missing)
    uncertainty = build_uncertainty(input_data, scene, task_clues)

    all_traces: List[Dict[str, Any]] = list(conflict_traces)
    frame_id = input_data.get("frame_context", {}).get("frame_id", "")
    all_traces.append({"stage": "input_frame", "ref": frame_id})
    for ev in input_data.get("visual_evidence_candidates", []):
        all_traces.append({"stage": "evidence", "ref": ev.get("evidence_id", "")})
    for cref in input_data.get("situation_case_refs", []):
        all_traces.append({"stage": "case_ref", "ref": cref.get("case_id", "")})

    situation_id = _uid("sit")
    return {
        "situation_id": situation_id,
        "scene_profile_candidate": scene,
        "survival_context": survival,
        "task_clue_candidates": task_clues,
        "missing_information_candidates": missing,
        "attention_target_hints": attention,
        "model_need_hints": model_needs,
        "uncertainty": uncertainty,
        "trace_refs": all_traces,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
        "no_runner_invocation": True,
        "no_fact_write": True,
        "no_navigation_decision": True,
    }
