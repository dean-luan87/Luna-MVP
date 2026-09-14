# -*- coding: utf-8 -*-
"""Scene-Task Model Activation — deterministic executor v1 (no runner execution)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_types_v1 import (
    MODELS,
    PLANNING_ENDPOINT,
)

ALL_MODELS: tuple[str, ...] = MODELS


def _trace(stage: str, ref: str) -> Dict[str, str]:
    return {"stage": stage, "ref": ref}


def build_scene_profile_candidate(
    scene_type: str,
    confidence: float = 0.86,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    sid = f"spc_{uuid4().hex[:10]}"
    return {
        "scene_profile_id": sid,
        "scene_type_candidate": scene_type,
        "confidence": confidence,
        "evidence_refs": evidence_refs or [],
        "candidate_only": True,
        "not_fact": True,
        "scene_profile_candidate_not_fact": True,
        "trace_chain": [_trace("scene_profile_candidate", sid)],
    }


def build_task_intent_candidate(
    task_type: str,
    source: str = "scene_policy",
    confidence: float = 0.84,
) -> Dict[str, Any]:
    tid = f"tic_{uuid4().hex[:10]}"
    return {
        "task_intent_id": tid,
        "task_type_candidate": task_type,
        "source": source,
        "confidence": confidence,
        "candidate_only": True,
        "not_fact": True,
        "task_intent_candidate_not_fact": True,
        "trace_chain": [_trace("task_intent_candidate", tid)],
    }


def _noop(
    model_name: str,
    reason: str,
    scene_ref: str,
    task_ref: str,
    policy_ref: str = "scene_task_model_activation_policy_v1",
) -> Dict[str, Any]:
    return {
        "model_name": model_name,
        "noop_reason": reason,
        "scene_profile_ref": scene_ref,
        "task_intent_ref": task_ref,
        "policy_ref": policy_ref,
        "candidate_only": True,
        "not_fact": True,
    }


def _assignment(
    model_name: str,
    reason: str,
    region_ids: Optional[List[str]] = None,
    text_region_ids: Optional[List[str]] = None,
    runner_type: str = "controlled_runner_candidate",
) -> Dict[str, Any]:
    aid = f"mra_{uuid4().hex[:10]}"
    return {
        "assignment_id": aid,
        "model_name": model_name,
        "assigned_region_ids": region_ids or [],
        "assigned_text_region_ids": text_region_ids or [],
        "assignment_reason": reason,
        "input_constraints": {"execution_stub": True, "no_runner_execution": True},
        "allowed_runner_type": runner_type,
        "candidate_only": True,
        "not_fact": True,
        "trace_chain": [_trace("model_region_assignment", aid)],
    }


def _activated(model_name: str, reason: str, runner_type: str = "controlled_runner_candidate") -> Dict[str, Any]:
    return {
        "model_name": model_name,
        "activation_reason": reason,
        "allowed_runner_type": runner_type,
        "candidate_only": True,
        "not_fact": True,
    }


def _build_followup_tasks(active_names: Set[str], assignments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    for a in assignments:
        model = a["model_name"]
        if model not in active_names:
            continue
        runner = a.get("allowed_runner_type", "controlled_runner_candidate")
        if runner.endswith("_task_candidate"):
            tasks.append({
                "task_candidate_id": f"frtc_{uuid4().hex[:10]}",
                "model_name": model,
                "runner_task_type": runner,
                "assigned_region_ids": a.get("assigned_region_ids", []),
                "assigned_text_region_ids": a.get("assigned_text_region_ids", []),
                "candidate_only": True,
                "not_fact": True,
                "no_runner_execution": True,
            })
    return tasks


def build_model_activation_plan(
    image_ref: str,
    scene: Dict[str, Any],
    task: Dict[str, Any],
    *,
    text_region_ids: Optional[List[str]] = None,
    region_ids: Optional[List[str]] = None,
    spatial_continuity_requested: bool = False,
    navigation_context: bool = False,
    object_candidates: bool = False,
    dynamic_targets: bool = False,
    safety_context: bool = False,
) -> Dict[str, Any]:
    """Model Work Admission — deterministic stub. Does not execute runners."""
    scene_type = scene["scene_type_candidate"]
    task_type = task["task_type_candidate"]
    scene_ref = scene["scene_profile_id"]
    task_ref = task["task_intent_id"]
    text_region_ids = text_region_ids or []
    region_ids = region_ids or []

    activated: List[Dict[str, Any]] = []
    assignments: List[Dict[str, Any]] = []
    noop_reasons: Dict[str, str] = {}

    text_tasks = {"read_text", "find_direction", "locate_place"}
    spatial_tasks = {"assess_walkable_area", "track_dynamic_target", "identify_object"}
    text_scenes = {"text_signage_scene", "shopfront_sign", "subway_platform", "indoor_navigation"}

    def activate(model: str, reason: str, **assign_kw: Any) -> None:
        activated.append(_activated(model, reason, assign_kw.get("runner_type", "controlled_runner_candidate")))
        assignments.append(_assignment(model, reason, **assign_kw))

    def set_noop(model: str, reason: str) -> None:
        noop_reasons[model] = reason

    if scene_type == "outdoor_street_crossing" and text_region_ids:
        activate(
            "ocr_text_detector",
            "sign/text region only; not blanket OCR",
            text_region_ids=text_region_ids,
            runner_type="ocr_task_candidate",
        )
        activate(
            "ocr_recognizer",
            "sign/text region only",
            text_region_ids=text_region_ids,
            runner_type="ocr_task_candidate",
        )
    elif task_type in text_tasks and scene_type in text_scenes and text_region_ids:
        activate(
            "ocr_text_detector",
            f"task={task_type}; scene={scene_type}; text_likelihood_high",
            text_region_ids=text_region_ids,
            runner_type="ocr_task_candidate",
        )
        activate(
            "ocr_recognizer",
            f"task={task_type}; follows text_detector for sign reading",
            text_region_ids=text_region_ids,
            runner_type="ocr_task_candidate",
        )
    else:
        if task_type in spatial_tasks and scene_type not in ("unknown_scene", "outdoor_street_crossing"):
            set_noop("ocr_text_detector", "task is spatial/dynamic; no blanket OCR")
            set_noop("ocr_recognizer", "task is spatial/dynamic; no blanket OCR")
        elif scene_type in ("corridor",) and not text_region_ids:
            set_noop("ocr_text_detector", "pure spatial navigation; no text region")
            set_noop("ocr_recognizer", "pure spatial navigation; no text region")
        elif scene_type == "unknown_scene":
            set_noop("ocr_text_detector", "unknown scene; pending VLM route or manual_review")
            set_noop("ocr_recognizer", "unknown scene; pending VLM route or manual_review")
        elif scene_type == "outdoor_street_crossing" and not text_region_ids:
            set_noop("ocr_text_detector", "street crossing; no sign/text region candidate")
            set_noop("ocr_recognizer", "street crossing; no sign/text region candidate")
        else:
            set_noop("ocr_text_detector", "no text_likelihood or task not text-primary")
            set_noop("ocr_recognizer", "no text_likelihood or task not text-primary")

    slam_activate = False
    if spatial_continuity_requested or navigation_context:
        slam_activate = True
    elif scene_type == "corridor" and task_type in ("assess_walkable_area", "understand_scene"):
        slam_activate = True
    elif task_type in text_tasks and scene_type in ("shopfront_sign", "text_signage_scene"):
        slam_activate = False
    elif task_type in text_tasks and scene_type == "subway_platform" and not navigation_context:
        slam_activate = False

    if slam_activate:
        activate(
            "slam",
            f"spatial continuity; scene={scene_type}; task={task_type}",
            region_ids=region_ids or [],
            runner_type="slam_task_candidate",
        )
    else:
        if task_type in text_tasks:
            set_noop("slam", f"task_intent={task_type}; no spatial continuity required")
        else:
            set_noop("slam", f"scene={scene_type}; spatial continuity not requested")

    if task_type in ("identify_object", "track_dynamic_target", "assess_walkable_area") and (
        object_candidates or dynamic_targets or scene_type == "outdoor_street_crossing"
    ):
        activate(
            "detection",
            f"task={task_type}; object/dynamic candidate in {scene_type}",
            region_ids=region_ids or ["full_frame_candidate"],
            runner_type="detection_task_candidate",
        )
    elif safety_context and scene_type == "subway_platform":
        activate(
            "detection",
            "optional safety context for people/doors",
            region_ids=["platform_safety_zone_candidate"],
            runner_type="detection_task_candidate",
        )
    else:
        set_noop("detection", "task is text-only or no object-like target")

    if task_type in ("assess_walkable_area", "track_dynamic_target") or scene_type in (
        "outdoor_street_crossing",
        "corridor",
    ):
        if task_type == "read_text" and scene_type in ("shopfront_sign", "text_signage_scene"):
            set_noop("depth", "pure text reading; no distance/walkable risk")
        elif scene_type in ("corridor", "outdoor_street_crossing"):
            activate(
                "depth",
                f"spatial risk / walkable assessment; scene={scene_type}",
                region_ids=region_ids or ["walkable_area_candidate"],
                runner_type="depth_task_candidate",
            )
        else:
            set_noop("depth", "no spatial risk requirement")
    else:
        set_noop("depth", "no distance/walkable risk requirement")

    if dynamic_targets or task_type == "track_dynamic_target":
        activate(
            "tracking",
            "dynamic target / multi-frame review",
            region_ids=region_ids or ["dynamic_target_candidate"],
            runner_type="tracking_task_candidate",
        )
    else:
        set_noop("tracking", "static scene or text-only; no dynamic target tracking")

    if scene_type == "unknown_scene" or task_type == "manual_review":
        activate(
            "vlm_route_enhancer",
            "unknown scene or manual_review; high-level route candidate",
            runner_type="vlm_route_candidate",
        )
    else:
        set_noop("vlm_route_enhancer", "task clear and covered by specialized models")

    if scene_type in ("shopfront_sign", "text_signage_scene") and task_type == "read_text":
        set_noop("mobile_sam_region_proposal", "text-first scene; SAM not primary text detector")
    elif scene_type == "unknown_scene":
        set_noop("mobile_sam_region_proposal", "unknown scene; pending VLM route")
    else:
        set_noop("mobile_sam_region_proposal", "planning only; region refine deferred to execution")

    active_names: Set[str] = {a["model_name"] for a in activated}
    for m in ALL_MODELS:
        if m not in active_names and m not in noop_reasons:
            noop_reasons[m] = "not selected by activation policy"

    noop_set = [_noop(m, noop_reasons[m], scene_ref, task_ref) for m in ALL_MODELS if m not in active_names]
    followup_tasks = _build_followup_tasks(active_names, assignments)

    followup = "manual_review"
    if "ocr_text_detector" in active_names:
        followup = "ocr_task_candidate"
    if "vlm_route_enhancer" in active_names:
        followup = "vlm_route_candidate"
    elif "detection" in active_names and "ocr_text_detector" not in active_names:
        followup = "detection_task_candidate"
    elif "slam" in active_names and "ocr_text_detector" not in active_names:
        followup = "slam_task_candidate"

    plan_id = f"map_{uuid4().hex[:10]}"
    return {
        "plan_id": plan_id,
        "image_ref": image_ref,
        "scene_profile_ref": scene_ref,
        "task_intent_ref": task_ref,
        "scene_profile_candidate": scene,
        "task_intent_candidate": task,
        "model_activation_plan_candidate": True,
        "activated_model_set": activated,
        "model_noop_set": noop_set,
        "model_region_assignment": assignments,
        "followup_runner_task_candidates": followup_tasks,
        "activation_summary": f"scene={scene_type}; task={task_type}; activated={sorted(active_names)}",
        "recommended_followup_runner_task_candidate": followup,
        "candidate_only": True,
        "not_fact": True,
        "model_activation_candidate_not_fact": True,
        "no_fact_write": True,
        "no_runner_execution_in_activation_execution": True,
        "trace_chain": [
            _trace("input_image", image_ref),
            _trace("scene_profile_candidate", scene_ref),
            _trace("task_intent_candidate", task_ref),
            _trace(PLANNING_ENDPOINT, plan_id),
        ],
    }


def run_activation_from_inputs(
    *,
    image_ref: str,
    scene_profile_candidate: Dict[str, Any],
    task_intent_candidate: Dict[str, Any],
    text_region_ids: Optional[List[str]] = None,
    region_ids: Optional[List[str]] = None,
    spatial_continuity_requested: bool = False,
    navigation_context: bool = False,
    object_candidates: bool = False,
    dynamic_targets: bool = False,
    safety_context: bool = False,
) -> Dict[str, Any]:
    return build_model_activation_plan(
        image_ref,
        scene_profile_candidate,
        task_intent_candidate,
        text_region_ids=text_region_ids,
        region_ids=region_ids,
        spatial_continuity_requested=spatial_continuity_requested,
        navigation_context=navigation_context,
        object_candidates=object_candidates,
        dynamic_targets=dynamic_targets,
        safety_context=safety_context,
    )
