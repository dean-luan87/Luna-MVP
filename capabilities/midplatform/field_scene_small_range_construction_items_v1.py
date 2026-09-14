# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction — items, mock cases, policies v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SCOPE_DEFINITION: Dict[str, Any] = {
    "scope_id": "field_scene_small_range_scope_v1",
    "goal": "small_range_field_scene_construction_from_mock_observations",
    "field_origin": "self_centered",
    "field_radius_m": 20.0,
    "zones": {
        "inner_zone": {"range_m": "0-3", "required": True},
        "working_zone": {"range_m": "3-10", "required": True},
        "forecast_zone": {"range_m": "10-20", "required": False, "reserved": True},
        "unknown": {"required": True},
    },
    "not_in_scope": (
        "full_3d_reconstruction", "semantic_attachment", "tracking", "trajectory_simulation",
        "world_model_fact", "persistent_memory", "real_model_inference",
    ),
}

INPUT_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_scene_input_candidate_contract_v1",
    "supported_types": (
        "ObjectObservationCandidate",
        "DepthObservationCandidate",
        "CameraStateCandidate",
        "UserStateCandidate",
    ),
    "object_required_fields": (
        "observation_id", "timestamp", "source_ref", "label", "confidence", "bbox",
    ),
    "depth_fields": (
        "observation_id", "frame_ref", "timestamp", "depth_source", "depth_confidence",
        "object_depth_hints", "depth_map_ref",
    ),
    "camera_fields": ("camera_ref", "timestamp", "frame_width", "frame_height", "heading_hint", "motion_state"),
    "user_fields": ("user_ref", "timestamp", "user_motion_state", "location_hint", "speed_hint"),
    "mock_only": True,
}

OUTPUT_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_scene_output_candidate_contract_v1",
    "outputs": (
        "FieldSceneCandidate",
        "FieldEntityCandidate",
        "FieldSceneConstructionResultCandidate",
    ),
    "candidate_only": True,
    "fact_status": "candidate",
    "required_entity_fields": (
        "observation_refs", "label", "confidence", "bbox", "depth_source", "depth_confidence",
        "pseudo_3d_position", "field_zone", "fact_status",
    ),
}

PROCESSING_FLOW: Tuple[Dict[str, str], ...] = (
    {"step": "1", "id": "receive_observation_candidates", "desc": "Receive mock observation candidates"},
    {"step": "2", "id": "validate_observation_candidates", "desc": "Validate required fields"},
    {"step": "3", "id": "normalize_spatial_payload", "desc": "Normalize bbox, frame_ref, bbox center"},
    {"step": "4", "id": "attach_depth_hint", "desc": "Bind depth_hint with source and confidence"},
    {"step": "5", "id": "estimate_pseudo_3d_position", "desc": "bbox center + depth_hint → pseudo 3D"},
    {"step": "6", "id": "assign_field_zone", "desc": "inner / working / forecast / unknown"},
    {"step": "7", "id": "build_field_entity_candidate", "desc": "Build FieldEntityCandidate per object"},
    {"step": "8", "id": "assemble_field_scene_candidate", "desc": "Aggregate into FieldSceneCandidate"},
    {"step": "9", "id": "validate_field_scene_candidate", "desc": "candidate-only, traceability, depth uncertainty"},
    {"step": "10", "id": "emit_construction_result", "desc": "Emit FieldSceneConstructionResultCandidate"},
)

DEPTH_UNCERTAINTY_POLICY: Dict[str, Any] = {
    "policy_id": "depth_uncertainty_policy_v1",
    "depth_estimated_not_fact": True,
    "rules": (
        "estimated_depth_must_set_depth_error_expected_true",
        "hardware_depth_may_set_depth_error_expected_false",
        "unknown_depth_must_set_depth_unknown_true",
        "never_write_depth_estimated_as_hardware_fact",
        "pseudo_3d_unknown_allowed_when_depth_missing",
    ),
    "depth_sources": ("estimated", "hardware", "unknown"),
}

FIELD_ZONE_ASSIGNMENT_POLICY: Dict[str, Any] = {
    "policy_id": "field_zone_assignment_policy_v1",
    "inner_zone_supported": True,
    "working_zone_supported": True,
    "forecast_zone_reserved": True,
    "unknown_zone_supported": True,
    "thresholds_m": {"inner_zone": 3.0, "working_zone": 10.0, "forecast_zone": 20.0},
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "scope_id": "prohibited_scope_v1",
    "prohibited": (
        "model_download", "weight_download", "torch_cv2_paddle_transformers_import",
        "supervision_execution", "real_detection", "real_depth_estimation",
        "video_tracking", "track_id_continuity", "field_continuity_detection",
        "task_simulation", "semantic_event_graph", "relation_emotion_memory_attachment",
        "world_model_entry", "runtime", "integration_test", "module_handoff_contract",
        "candidate_lifecycle_manager",
    ),
}

NEXT_STAGE_SPLIT_PLAN: Dict[str, Any] = {
    "plan_id": "next_stage_split_plan_v1",
    "current_stage": "Phase-Midplatform-Field-Scene-Small-Range-Construction-Core-Definition-v1-001",
    "recommended_next": "Phase-Midplatform-Field-Continuity-Detection-Planning-v1-001",
    "deferred": (
        "static_target_lock", "dynamic_target_tracking", "trajectory_analysis",
        "task_impact_extraction", "continuous_field_world_model",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "small_range_construction_not_full_3d_reconstruction",
    "mock_construction_not_real_inference",
    "field_scene_candidate_not_world_model_fact",
    "core_definition_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Continuity-Detection-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Field Continuity Detection Planning"

_DEFAULT_CAM = {"camera_ref": "cam_mock_0", "timestamp": "2026-06-11T10:00:00Z", "frame_width": 640, "frame_height": 480, "heading_hint": 0.0, "motion_state": "stationary"}
_DEFAULT_USER = {"user_ref": "user_self_ref", "timestamp": "2026-06-11T10:00:00Z", "user_motion_state": "stationary"}


def _obj(oid: str, label: str, bbox: Dict[str, float], conf: float = 0.85, **kw: Any) -> Dict[str, Any]:
    return {
        "observation_id": oid, "source_type": "object", "source_ref": "mock_frontend",
        "frame_ref": "frame_0", "timestamp": "2026-06-11T10:00:00Z",
        "label": label, "confidence": conf, "bbox": bbox, **kw,
    }


MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "simple_indoor_objects",
        "description": "chair, table, cup with estimated depth",
        "observations": (
            _obj("obs_chair", "chair", {"x1": 100, "y1": 200, "x2": 200, "y2": 400}, depth_hint=2.5, depth_source="estimated", depth_confidence=0.6, depth_error_expected=True),
            _obj("obs_table", "table", {"x1": 250, "y1": 300, "x2": 450, "y2": 450}, depth_hint=3.5, depth_source="estimated", depth_confidence=0.55, depth_error_expected=True),
            _obj("obs_cup", "cup", {"x1": 300, "y1": 280, "x2": 330, "y2": 320}, depth_hint=3.2, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "expected_zones": ("inner_zone", "working_zone"),
        "expect_pass": True,
    },
    {
        "case_id": "near_obstacle_inner_zone",
        "description": "near obstacle in inner zone",
        "observations": (
            _obj("obs_obstacle", "obstacle", {"x1": 280, "y1": 350, "x2": 360, "y2": 470}, depth_hint=1.2, depth_source="estimated", depth_confidence=0.7, depth_error_expected=True, risk_hint="near_collision"),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "expected_zones": ("inner_zone",),
        "expect_pass": True,
    },
    {
        "case_id": "working_zone_door_and_sign",
        "description": "door and sign in working zone",
        "observations": (
            _obj("obs_door", "door", {"x1": 50, "y1": 50, "x2": 150, "y2": 450}, depth_hint=6.0, depth_source="estimated", depth_confidence=0.65, depth_error_expected=True),
            _obj("obs_sign", "sign", {"x1": 400, "y1": 100, "x2": 500, "y2": 200}, depth_hint=7.5, depth_source="estimated", depth_confidence=0.6, depth_error_expected=True),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "expected_zones": ("working_zone",),
        "expect_pass": True,
    },
    {
        "case_id": "missing_depth_hint",
        "description": "no depth — entity still built with unknown zone",
        "observations": (
            _obj("obs_unknown", "box", {"x1": 200, "y1": 200, "x2": 300, "y2": 300}),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "expected_zones": ("unknown",),
        "expect_pass": True,
    },
    {
        "case_id": "low_confidence_object",
        "description": "low confidence retained with warning",
        "observations": (
            _obj("obs_low", "unknown_object", {"x1": 100, "y1": 100, "x2": 140, "y2": 140}, conf=0.25, depth_hint=4.0, depth_source="estimated", depth_confidence=0.3, depth_error_expected=True),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "expected_warnings_contain": "low_confidence",
        "expect_pass": True,
    },
    {
        "case_id": "multiple_objects_same_frame",
        "description": "multiple entities from one frame",
        "observations": (
            _obj("obs_a", "person", {"x1": 10, "y1": 10, "x2": 80, "y2": 200}, depth_hint=5.0, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
            _obj("obs_b", "bag", {"x1": 90, "y1": 150, "x2": 160, "y2": 220}, depth_hint=4.5, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
            _obj("obs_c", "pole", {"x1": 500, "y1": 50, "x2": 530, "y2": 400}, depth_hint=8.0, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
            _obj("obs_d", "bench", {"x1": 200, "y1": 300, "x2": 400, "y2": 380}, depth_hint=2.0, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
            _obj("obs_e", "tree", {"x1": 550, "y1": 20, "x2": 620, "y2": 300}, depth_hint=12.0, depth_source="estimated", depth_confidence=0.4, depth_error_expected=True),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "min_entities": 5,
        "expect_pass": True,
    },
    {
        "case_id": "camera_state_missing_heading",
        "description": "field builds but records missing heading",
        "observations": (
            _obj("obs_item", "shelf", {"x1": 150, "y1": 100, "x2": 350, "y2": 400}, depth_hint=3.0, depth_source="estimated", depth_confidence=0.5, depth_error_expected=True),
        ),
        "camera_state": {**_DEFAULT_CAM, "heading_hint": None},
        "user_state": dict(_DEFAULT_USER),
        "expect_missing": "camera_heading_hint_missing",
        "expect_pass": True,
    },
    {
        "case_id": "depth_estimated_error_expected",
        "description": "software estimated depth must mark error expected",
        "observations": (
            _obj("obs_est", "cabinet", {"x1": 220, "y1": 180, "x2": 320, "y2": 420}, depth_hint=2.8, depth_source="estimated", depth_confidence=0.45, depth_error_expected=True),
        ),
        "camera_state": dict(_DEFAULT_CAM),
        "user_state": dict(_DEFAULT_USER),
        "require_depth_error_expected": True,
        "expect_pass": True,
    },
)
