# -*- coding: utf-8 -*-
"""Map Location Read-Only Context Policy v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Map-Location-ReadOnly-Context-Policy-v1-001"
POLICY_ID = "mlrocp_v1_001"
POLICY_SCOPE = "map_location_readonly_context_policy_only"
SOURCE_CHAIN = "map_location_readonly_context_policy_v1"
FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Planning-v1-001"

ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FEEDBACK_DRYRUN_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
TRACKING_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "post_vision_strengthening_roadmap_decision",
        "arg": "post_vision_strengthening_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json", "route_option_matrix.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "post_dryrun_review",
        "arg": "post_dryrun_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "closure_readiness_decision.json"],
    },
    {
        "id": "dryrun",
        "arg": "dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "navigation_loop_vision_strengthening_dryrun_results.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback",
        "arg": "visual_ocr_map_task_feedback_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "visual_ocr_map_task_feedback_dryrun_results.json"],
    },
    {
        "id": "selective_tracking",
        "arg": "selective_tracking_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "tracking_request_candidate_schema.json"],
    },
    {
        "id": "world_observation_entity_feature",
        "arg": "world_observation_entity_feature_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "worldmodel_memory_library_placeholder_policy.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "focus_to_ocr_activation_policy.json", "focus_to_tracking_request_policy.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_memory_context_hint_policy.json", "perception_work_order_schema.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "map_anchor_context_output",
        "arg": "map_anchor_context_output_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gps_route_context_output",
        "arg": "gps_route_context_output_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "route_context_preplan",
        "arg": "route_context_preplan_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "basic_navigation_guidance_loop_output",
        "arg": "basic_navigation_guidance_loop_output_root",
        "required": False,
        "summary": "basic_navigation_guidance_loop_dryrun_v1_summary.json",
        "artifacts": ["basic_navigation_guidance_loop_dryrun_v1_summary.json"],
    },
    {
        "id": "basic_navigation_loop_stabilization",
        "arg": "basic_navigation_loop_stabilization_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "safety_task_arbitration_policy",
        "arg": "safety_task_arbitration_policy_root",
        "required": False,
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "artifacts": ["safety_task_arbitration_policy_v1_summary.json"],
    },
]

ROUTE_STAGE_ENUM = [
    "route_not_started",
    "route_walking",
    "approaching_crossing",
    "crossing_area_candidate",
    "after_crossing_candidate",
    "approaching_destination",
    "target_search_area",
    "target_confirmation_area",
    "arrived_candidate",
    "off_route_candidate",
    "route_uncertain",
]

DISTANCE_BUCKET_ENUM = ["far", "nearby", "approaching", "very_close", "uncertain"]
SIDE_CANDIDATE_ENUM = ["left", "right", "front", "behind", "across_road", "same_side", "opposite_side", "unknown"]
SOURCE_TYPE_ENUM = [
    "simulated_map_hint",
    "cached_map_placeholder",
    "user_provided_location_hint",
    "memory_derived_location_hint",
    "route_plan_placeholder",
    "gps_placeholder",
    "poi_placeholder",
    "map_anchor_placeholder",
]

SCENARIO_MATRIX = [
    {
        "scenario_id": "route_walking_map_hint",
        "route_stage_candidate": "route_walking",
        "generated_candidates": ["route_stage_hint_candidate"],
        "visual_focus_effect": "no direct action; preserve normal route-following context",
        "ocr_activation_effect": "none",
        "tracking_effect": "none",
        "notes": "只生成 route_stage_hint，不触发行动",
    },
    {
        "scenario_id": "approaching_destination_nearby",
        "route_stage_candidate": "approaching_destination",
        "generated_candidates": ["target_proximity_hint_candidate", "route_stage_hint_candidate"],
        "visual_focus_effect": "increase destination_landmark_focus and signage_focus",
        "ocr_activation_effect": "allow signage OCR target candidate placeholder",
        "tracking_effect": "allow target-related tracking request candidate only after visual focus binding",
        "notes": "不说已到达，不构成 arrival fact",
    },
    {
        "scenario_id": "right_side_shop_search",
        "route_stage_candidate": "target_search_area",
        "generated_candidates": ["side_orientation_hint_candidate", "target_proximity_hint_candidate"],
        "visual_focus_effect": "trigger right-side shopfront focus candidate",
        "ocr_activation_effect": "allow shopfront or doorplate OCR target candidate placeholder",
        "tracking_effect": "allow storefront-related tracking request candidate only after visual confirmation",
        "notes": "右侧提示只是 hint，不是目标确认事实",
    },
    {
        "scenario_id": "intersection_approach_hint",
        "route_stage_candidate": "approaching_crossing",
        "generated_candidates": ["entrance_intersection_hint_candidate", "route_stage_hint_candidate"],
        "visual_focus_effect": "trigger crossing_focus and traffic_light_focus",
        "ocr_activation_effect": "allow traffic sign or countdown text OCR target candidate placeholder",
        "tracking_effect": "allow safety-relevant tracking request candidate only after visual focus binding",
        "notes": "crossing_action_allowed=false",
    },
    {
        "scenario_id": "entrance_hint_candidate",
        "route_stage_candidate": "target_search_area",
        "generated_candidates": ["entrance_intersection_hint_candidate", "side_orientation_hint_candidate"],
        "visual_focus_effect": "trigger doorway_or_entrance_focus",
        "ocr_activation_effect": "allow doorplate or entrance signage OCR target candidate placeholder",
        "tracking_effect": "none",
        "notes": "入口 hint 不是入口事实",
    },
    {
        "scenario_id": "off_route_uncertain_hint",
        "route_stage_candidate": "off_route_candidate",
        "generated_candidates": ["route_stage_hint_candidate", "map_location_feedback_candidate"],
        "visual_focus_effect": "trigger reobserve and active view adjustment candidate",
        "ocr_activation_effect": "none",
        "tracking_effect": "none",
        "notes": "需要视觉或用户确认",
    },
    {
        "scenario_id": "map_visual_conflict_shop_absent",
        "route_stage_candidate": "target_search_area",
        "generated_candidates": ["map_location_conflict_candidate", "reobserve_request_candidate", "correction_handoff_candidate"],
        "visual_focus_effect": "reobserve shopfront region",
        "ocr_activation_effect": "delay OCR until readable region candidate exists",
        "tracking_effect": "do not generate direct tracking order from conflict alone",
        "notes": "地图说有店，视觉没有看到，不更新事实",
    },
    {
        "scenario_id": "stale_map_or_old_poi",
        "route_stage_candidate": "route_uncertain",
        "generated_candidates": ["map_location_conflict_candidate", "correction_handoff_candidate"],
        "visual_focus_effect": "degrade map trust and request updated observation",
        "ocr_activation_effect": "optional signage OCR placeholder with stale warning",
        "tracking_effect": "none",
        "notes": "生成 stale_map conflict，不更新事实",
    },
    {
        "scenario_id": "indoor_floor_directory_hint",
        "route_stage_candidate": "target_search_area",
        "generated_candidates": ["entrance_intersection_hint_candidate", "target_proximity_hint_candidate"],
        "visual_focus_effect": "trigger directory sign focus or indoor landmark focus",
        "ocr_activation_effect": "allow directory sign OCR target candidate placeholder",
        "tracking_effect": "none",
        "notes": "不调用 OCR runtime",
    },
    {
        "scenario_id": "gps_low_confidence_location_uncertain",
        "route_stage_candidate": "route_uncertain",
        "generated_candidates": ["map_location_conflict_candidate", "reobserve_request_candidate", "user_confirmation_candidate"],
        "visual_focus_effect": "degrade to reobserve and user confirmation candidate",
        "ocr_activation_effect": "none",
        "tracking_effect": "none",
        "notes": "定位不稳定时降级为 route_uncertain",
    },
]

GOVERNANCE_DEBT_TOPICS = [
    "midplatform capability expansion debt",
    "map/location freshness and offset governance complexity",
    "route-stage candidate calibration debt",
    "side and orientation ambiguity debt",
    "entrance and intersection uncertainty debt",
    "map-visual-memory conflict escalation debt",
    "privacy filtering for map-guided OCR target debt",
    "controlled frame input dependency debt",
    "crossing governance dependency debt",
    "schema consolidation risk",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "policy_scope": POLICY_SCOPE,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "route_planning_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "arrival_fact_written": False,
        "crossing_action_instruction_allowed": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def run_map_location_readonly_context_policy_v1(
    *,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
    post_dryrun_review_root: str,
    dryrun_root: str,
    visual_ocr_map_task_feedback_root: str,
    selective_tracking_root: str,
    world_observation_entity_feature_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    map_anchor_context_output_root: Optional[str] = None,
    gps_route_context_output_root: Optional[str] = None,
    route_context_preplan_root: Optional[str] = None,
    basic_navigation_guidance_loop_output_root: Optional[str] = None,
    basic_navigation_loop_stabilization_root: Optional[str] = None,
    safety_task_arbitration_policy_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}

    post_vision_strengthening_roadmap_decision_input_loaded = (
        roots["post_vision_strengthening_roadmap_decision"]["loaded"]
        and summaries["post_vision_strengthening_roadmap_decision"].get("final_decision") == ROADMAP_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    post_dryrun_review_input_loaded = (
        roots["post_dryrun_review"]["loaded"]
        and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summaries["dryrun"].get("final_decision") == DRYRUN_DECISION
    visual_ocr_map_task_feedback_input_loaded = (
        roots["visual_ocr_map_task_feedback"]["loaded"]
        and summaries["visual_ocr_map_task_feedback"].get("final_decision") == FEEDBACK_DRYRUN_DECISION
    )
    selective_tracking_input_loaded = (
        roots["selective_tracking"]["loaded"]
        and summaries["selective_tracking"].get("final_decision") == TRACKING_DECISION
    )
    world_observation_entity_feature_input_loaded = (
        roots["world_observation_entity_feature"]["loaded"]
        and summaries["world_observation_entity_feature"].get("final_decision") == WORLDOBS_DECISION
    )
    task_aware_visual_focus_input_loaded = (
        roots["task_aware_visual_focus"]["loaded"]
        and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    )
    midplatform_perception_orchestration_input_loaded = (
        roots["midplatform_perception_orchestration"]["loaded"]
        and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    map_location_readonly_context_policy = {
        "policy_id": POLICY_ID,
        "policy_scope": POLICY_SCOPE,
        "map_context_role": "readonly_hint",
        "location_context_role": "readonly_hint",
        "route_context_role": "readonly_hint",
        "poi_context_role": "readonly_hint",
        "allowed_use_cases": [
            "task phase hinting",
            "route stage candidate generation",
            "target proximity hinting",
            "side and orientation hinting",
            "entrance and intersection hinting",
            "visual focus plan assistance",
            "OCR activation candidate assistance after visual focus binding",
            "tracking request candidate assistance after visual focus binding",
            "navigation guidance candidate assistance as readonly context",
            "conflict detection and correction handoff placeholder generation",
        ],
        "forbidden_use_cases": [
            "fact authority",
            "navigation authority",
            "safety authority",
            "action trigger",
            "arrival proof",
            "crossing permission",
            "WorldModel fact write",
            "Memory fact write",
            "direct OCR runtime invocation",
            "direct tracking runtime invocation",
            "direct Navigation Action",
            "direct Task State commit",
        ],
        "conflict_policy_ref": "map_visual_memory_conflict_policy.json",
        "freshness_policy_ref": "map_location_boundary_matrix.json",
        "privacy_policy_ref": "map_location_boundary_matrix.json",
        "safety_arbitration_required": True,
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_context_candidate_schema = {
        "schema_name": "MapLocationContextCandidate",
        "source_type_enum": SOURCE_TYPE_ENUM,
        "field_specs": [
            _field("map_location_context_id", "string", True),
            _field("source_type", "enum", True, allowed_values=SOURCE_TYPE_ENUM),
            _field("source_provider_placeholder", "string", True),
            _field("route_context_ref", "string", False),
            _field("location_context_ref", "string", False),
            _field("poi_context_ref", "string", False),
            _field("target_context_ref", "string", False),
            _field("route_stage_candidate", "string", False),
            _field("distance_to_target_candidate", "string", False),
            _field("side_hint_candidate", "string", False),
            _field("entrance_hint_candidate", "string", False),
            _field("intersection_hint_candidate", "string", False),
            _field("crossing_hint_candidate", "string", False),
            _field("floor_or_level_hint_candidate", "string", False),
            _field("indoor_outdoor_hint_candidate", "string", False),
            _field("confidence", "number", True),
            _field("uncertainty", "number", True),
            _field("freshness_status", "string", True),
            _field("ttl_policy_ref", "string", True),
            _field("provider_runtime_invoked", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("action_allowed", "boolean", True, default=False),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_stage_hint_candidate_schema = {
        "schema_name": "RouteStageHintCandidate",
        "route_stage_enum": ROUTE_STAGE_ENUM,
        "field_specs": [
            _field("route_stage_hint_id", "string", True),
            _field("related_task_id", "string", True),
            _field("route_stage", "enum", True, allowed_values=ROUTE_STAGE_ENUM),
            _field("stage_reason", "string", True),
            _field("map_location_refs", "list", True),
            _field("visual_refs_placeholder", "list", True),
            _field("memory_refs", "list", True),
            _field("confidence", "number", True),
            _field("uncertainty", "number", True),
            _field("current_action_allowed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "non_claims": [
            "arrived_candidate 不等于已到达事实",
            "crossing_area_candidate 不等于允许过马路",
            "off_route_candidate 不等于真实偏航事实",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    target_proximity_hint_candidate_schema = {
        "schema_name": "TargetProximityHintCandidate",
        "distance_bucket_candidate_enum": DISTANCE_BUCKET_ENUM,
        "field_specs": [
            _field("target_proximity_hint_id", "string", True),
            _field("related_task_id", "string", True),
            _field("target_ref", "string", True),
            _field("distance_bucket_candidate", "enum", True, allowed_values=DISTANCE_BUCKET_ENUM),
            _field("proximity_stage", "string", True),
            _field("side_hint", "string", False),
            _field("expected_visual_evidence", "list", True),
            _field("expected_ocr_targets", "list", True),
            _field("expected_tracking_targets", "list", True),
            _field("confidence", "number", True),
            _field("uncertainty", "number", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("action_allowed", "boolean", True, default=False),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    side_orientation_hint_candidate_schema = {
        "schema_name": "SideAndOrientationHintCandidate",
        "side_candidate_enum": SIDE_CANDIDATE_ENUM,
        "field_specs": [
            _field("side_orientation_hint_id", "string", True),
            _field("related_task_id", "string", True),
            _field("side_candidate", "enum", True, allowed_values=SIDE_CANDIDATE_ENUM),
            _field("orientation_candidate", "string", True),
            _field("expected_focus_direction", "string", True),
            _field("expected_visual_evidence", "list", True),
            _field("map_location_refs", "list", True),
            _field("confidence", "number", True),
            _field("uncertainty", "number", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("action_allowed", "boolean", True, default=False),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    entrance_intersection_hint_candidate_schema = {
        "schema_name": "EntranceIntersectionHintCandidate",
        "hint_type_enum": ["entrance_hint", "intersection_hint", "crossing_hint", "floor_hint"],
        "field_specs": [
            _field("entrance_intersection_hint_id", "string", True),
            _field("hint_type", "enum", True, allowed_values=["entrance_hint", "intersection_hint", "crossing_hint", "floor_hint"]),
            _field("related_task_id", "string", True),
            _field("expected_entrance_side", "string", False),
            _field("expected_intersection_type", "string", False),
            _field("expected_crossing_type", "string", False),
            _field("expected_visual_focus", "list", True),
            _field("expected_ocr_targets", "list", True),
            _field("expected_safety_focus", "list", True),
            _field("confidence", "number", True),
            _field("uncertainty", "number", True),
            _field("crossing_action_allowed", "boolean", True, default=False),
            _field("arrival_fact_allowed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_visual_memory_conflict_policy = {
        "policy_name": "MapVisualMemoryConflictPolicy",
        "conflict_types": [
            "map_vs_visual",
            "map_vs_ocr",
            "map_vs_memory",
            "location_vs_visual",
            "route_vs_visual",
            "poi_vs_signage",
            "side_hint_vs_scene_sketch",
            "arrival_hint_vs_visual_absence",
            "crossing_hint_vs_safety_uncertain",
            "stale_map_vs_current_observation",
        ],
        "outputs": [
            "MapLocationConflictCandidate",
            "ReobserveRequestCandidate",
            "UserConfirmationCandidate",
            "CorrectionHandoffCandidate",
        ],
        "principles": [
            "地图冲突不自动修正事实",
            "地图不能覆盖视觉安全",
            "地图不能覆盖用户反馈",
            "地图不能直接更新 WorldModel",
            "地图 conflict 可进入 correction candidate / handoff placeholder",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_to_visual_focus_binding_policy = {
        "policy_name": "MapLocationToVisualFocusBindingPolicy",
        "allowed_bindings": [
            "目标接近时提高 destination_landmark_focus",
            "右侧店铺 hint 触发 right-side shopfront focus",
            "路口 hint 触发 crossing_focus / traffic_light_focus",
            "入口 hint 触发 doorway_or_entrance_focus",
            "POI hint 触发 signage_focus / OCR activation candidate",
            "路线不确定时触发 active view adjustment / reobserve",
        ],
        "forbidden_bindings": [
            "地图直接触发 OCR runtime",
            "地图直接触发 tracking runtime",
            "地图直接生成导航动作",
            "地图直接判断已到达",
            "地图直接判断可过马路",
        ],
        "tracking_request_from_map_requires_visual_focus": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_to_ocr_activation_hint_policy = {
        "policy_name": "MapLocationToOCRActivationHintPolicy",
        "allowed_bindings": [
            "approaching_destination -> signage OCR target candidate",
            "shop_search_area -> shopfront / doorplate OCR target candidate",
            "intersection_area -> traffic sign / countdown text OCR target candidate placeholder",
            "indoor_floor_hint -> directory sign OCR target candidate",
            "temporary_notice_area -> notice OCR target candidate",
        ],
        "forbidden_bindings": [
            "full-frame OCR",
            "OCR provider invocation",
            "OCRRequest submission",
            "OCR from map alone without visual/readable region candidate",
            "OCR on privacy-sensitive text without filtering",
        ],
        "ocr_activation_from_map_requires_visual_focus": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_feedback_policy = {
        "policy_name": "MapLocationFeedbackPolicy",
        "output_candidates": [
            "MapLocationFeedbackCandidate",
            "RouteStageFeedbackCandidate",
            "TargetProximityFeedbackCandidate",
            "SideOrientationFeedbackCandidate",
            "EntranceIntersectionFeedbackCandidate",
            "MapVisualMemoryConflictFeedbackCandidate",
        ],
        "principles": {
            "feedback_candidate_only": True,
            "speech_allowed": False,
            "action_allowed": False,
            "navigation_action_allowed": False,
            "fact_status": "not_fact",
            "requires_arbitration": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_readonly_context_scenario_matrix = {
        "scenarios": [
            {
                **case,
                "expected_boundary_flags": {
                    "action_allowed": False,
                    "navigation_action_allowed": False,
                    "fact_status": "not_fact",
                    "crossing_action_allowed": False,
                    "arrival_fact_allowed": False,
                },
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for case in SCENARIO_MATRIX
        ],
        "scenario_count": len(SCENARIO_MATRIX),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_location_boundary_matrix = {
        "policy_scope": POLICY_SCOPE,
        "map_context_role": "readonly_hint",
        "location_context_role": "readonly_hint",
        "route_context_role": "readonly_hint",
        "poi_context_role": "readonly_hint",
        "map_is_fact_authority": False,
        "map_is_navigation_authority": False,
        "map_is_safety_authority": False,
        "map_can_trigger_action": False,
        "map_can_prove_arrival": False,
        "map_can_grant_crossing_permission": False,
        "map_can_write_worldmodel": False,
        "map_can_write_memory": False,
        "map_can_write_fact": False,
        "map_location_feedback_candidate_only": True,
        "map_visual_conflict_candidate_generated": True,
        "ocr_activation_from_map_requires_visual_focus": True,
        "tracking_request_from_map_requires_visual_focus": True,
        "freshness_policy": {
            "freshness_status_values": ["fresh", "stale", "uncertain", "expired"],
            "stale_or_offset_requires_degradation": True,
            "gps_low_confidence_degrades_to_route_uncertain": True,
        },
        "degradation_policy": {
            "stale_map_or_old_poi": "generate stale_map conflict and correction handoff",
            "gps_low_confidence": "request reobserve or user confirmation",
            "route_or_location_uncertain": "degrade to readonly hint only",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {
                "topic": topic,
                "impact": "must remain visible before controlled frame input and function governance",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in GOVERNANCE_DEBT_TOPICS
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "map/location readonly contract is defined; next step is controlled frame input planning without opening live camera",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    if not all(
        [
            post_vision_strengthening_roadmap_decision_input_loaded,
            vision_strengthening_closure_input_loaded,
            post_dryrun_review_input_loaded,
            dryrun_input_loaded,
            visual_ocr_map_task_feedback_input_loaded,
            selective_tracking_input_loaded,
            world_observation_entity_feature_input_loaded,
            task_aware_visual_focus_input_loaded,
            midplatform_perception_orchestration_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")

    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "visual_ocr_map_task_feedback_input_loaded": visual_ocr_map_task_feedback_input_loaded,
        "selective_tracking_input_loaded": selective_tracking_input_loaded,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "map_location_readonly_context_policy_defined": True,
        "map_location_context_candidate_schema_defined": True,
        "route_stage_hint_candidate_schema_defined": True,
        "target_proximity_hint_candidate_schema_defined": True,
        "side_orientation_hint_candidate_schema_defined": True,
        "entrance_intersection_hint_candidate_schema_defined": True,
        "map_visual_memory_conflict_policy_defined": True,
        "map_location_to_visual_focus_binding_policy_defined": True,
        "map_location_to_ocr_activation_hint_policy_defined": True,
        "map_location_feedback_policy_defined": True,
        "scenario_matrix_generated": True,
        "governance_debt_register_generated": True,
        "scenario_count": len(SCENARIO_MATRIX),
        "map_context_role": "readonly_hint",
        "location_context_role": "readonly_hint",
        "route_context_role": "readonly_hint",
        "poi_context_role": "readonly_hint",
        "map_is_fact_authority": False,
        "map_is_navigation_authority": False,
        "map_is_safety_authority": False,
        "map_can_trigger_action": False,
        "map_can_prove_arrival": False,
        "map_can_grant_crossing_permission": False,
        "map_can_write_worldmodel": False,
        "map_can_write_memory": False,
        "map_can_write_fact": False,
        "map_location_feedback_candidate_only": True,
        "map_visual_conflict_candidate_generated": True,
        "ocr_activation_from_map_requires_visual_focus": True,
        "tracking_request_from_map_requires_visual_focus": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "route_planning_runtime_invoked": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "arrival_fact_written": False,
        "crossing_action_instruction_allowed": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "MAP_LOCATION_READONLY_CONTEXT_POLICY_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "map_location_readonly_context_policy": map_location_readonly_context_policy,
        "map_location_context_candidate_schema": map_location_context_candidate_schema,
        "route_stage_hint_candidate_schema": route_stage_hint_candidate_schema,
        "target_proximity_hint_candidate_schema": target_proximity_hint_candidate_schema,
        "side_orientation_hint_candidate_schema": side_orientation_hint_candidate_schema,
        "entrance_intersection_hint_candidate_schema": entrance_intersection_hint_candidate_schema,
        "map_visual_memory_conflict_policy": map_visual_memory_conflict_policy,
        "map_location_to_visual_focus_binding_policy": map_location_to_visual_focus_binding_policy,
        "map_location_to_ocr_activation_hint_policy": map_location_to_ocr_activation_hint_policy,
        "map_location_feedback_policy": map_location_feedback_policy,
        "map_location_readonly_context_scenario_matrix": map_location_readonly_context_scenario_matrix,
        "map_location_boundary_matrix": map_location_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
