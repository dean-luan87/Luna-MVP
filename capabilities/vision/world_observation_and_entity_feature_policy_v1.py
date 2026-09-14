# -*- coding: utf-8 -*-
"""World Observation and Entity Feature Policy v1.

Phase-World-Observation-and-Entity-Feature-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-World-Observation-and-Entity-Feature-Policy-v1-001"
POLICY_ID = "woefp_v1_001"
POLICY_SCOPE = "world_observation_and_entity_feature_policy_only"
SOURCE_CHAIN = "world_observation_and_entity_feature_policy_v1"
FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
NEXT_PHASE = "Phase-Selective-Tracking-Adapter-Policy-v1-001"
VISUAL_FOCUS_FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "task_aware_visual_focus",
        "path_arg": "task_aware_visual_focus_root",
        "label": "Task-Aware Visual Focus Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "visual_observation_lifecycle_policy.json",
            "deferred_worldmodel_memory_library_boundary.json",
            "visual_focus_feedback_policy.json",
        ],
    },
    {
        "intake_id": "midplatform_perception_orchestration",
        "path_arg": "midplatform_perception_orchestration_root",
        "label": "MidPlatform Perception Orchestration Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "worldmodel_memory_library_handoff_boundary.json",
            "perception_feedback_candidate_policy.json",
        ],
    },
    {
        "intake_id": "return_to_vision_planning",
        "path_arg": "return_to_vision_planning_root",
        "label": "Return-To-Vision Mainline Planning v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "vision_mainline_roadmap.json",
            "deferred_worldmodel_memory_library_boundary.json",
        ],
    },
    {
        "intake_id": "preplan_input",
        "path_arg": "preplan_input_root",
        "label": "Return-To-Vision Mainline Preplan v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "proposed_vision_mainline_architecture.json",
            "deferred_worldmodel_memory_library_boundary.json",
        ],
    },
    {
        "intake_id": "ocr_final_closure",
        "path_arg": "ocr_final_closure_root",
        "label": "OCR Mainline Final Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "ocr_mainline_final_closure_report.json",
            "ocr_to_vision_handoff_plan.json",
        ],
    },
    {
        "intake_id": "minimal_runtime_integration_closure",
        "path_arg": "minimal_runtime_integration_closure_root",
        "label": "Minimal Runtime Integration Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "minimal_runtime_integration_closure_report.json",
            "vision_mainline_handoff_plan.json",
        ],
    },
]

REQUIRED_DOCS = {
    "task_aware_visual_focus_doc": "docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md",
    "midplatform_perception_orchestration_doc": "docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md",
    "vision_planning_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md",
    "vision_preplan_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "worldmodel_unresolved_observation_slot_contract": "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md",
    "worldmodel_lookup_for_reading_framework": "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    "confirmed_text_evidence_memory_governance_contract": "docs/architecture/evaluation/LUNA_EVALUATION_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
    "world_context_evidence_boundary_register": "docs/architecture/LUNA_WORLD_CONTEXT_EVIDENCE_BOUNDARY_REGISTER_V0.md",
    "map_anchor_evidence_schema": "docs/architecture/LUNA_MAP_ANCHOR_EVIDENCE_SCHEMA_V0.md",
    "map_anchor_trust_policy": "docs/architecture/LUNA_MAP_ANCHOR_TRUST_AND_WRITE_READINESS_POLICY_V0.md",
    "stc_sampling_guidance_policy": "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "ocr_activation_governance_policy": "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "vision_recognition_evidence_pack": "docs/architecture/vision/LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md",
    "vision_frame_input_governance": "docs/architecture/vision/LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md",
    "system_health_center_governance": "docs/architecture/system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    "hardware_profile_capability_registry": "docs/architecture/midplatform/LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md",
}

BOUNDARY_FALSE_FLAGS = {
    "no_runtime_executed": True,
    "no_new_runtime_enabled": True,
    "world_observation_runtime_enabled": False,
    "camera_invoked": False,
    "map_api_invoked": False,
    "ocr_provider_invoked": False,
    "ocrrequest_submitted": False,
    "tracking_runtime_invoked": False,
    "optical_flow_runtime_invoked": False,
    "supervision_invoked": False,
    "bytetrack_invoked": False,
    "ocsort_invoked": False,
    "entity_resolution_runtime_invoked": False,
    "fact_admission_runtime_invoked": False,
    "memory_consolidation_invoked": False,
    "library_experience_commit_invoked": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "speech_gate_invoked": False,
    "vop_invoked": False,
}

WORLD_OBSERVATION_TYPES = [
    "route_structure_candidate",
    "road_surface_candidate",
    "walkable_path_candidate",
    "entrance_or_exit_candidate",
    "public_facility_candidate",
    "shopfront_or_signage_candidate",
    "temporary_facility_candidate",
    "environmental_pattern_candidate",
    "scene_change_candidate",
    "safety_risk_point_candidate",
    "user_relevant_place_candidate",
    "recurring_observation_candidate",
]

WORLD_OBSERVATION_FIELD_SPECS = [
    {"name": "world_observation_id", "type": "string", "required": True},
    {"name": "source_visual_focus_slot_id", "type": "string", "required": True},
    {"name": "source_scene_sketch_id", "type": "string", "required": True},
    {"name": "source_visual_observation_ref", "type": "string", "required": False},
    {"name": "observation_type", "type": "enum", "required": True},
    {"name": "observed_entity_type", "type": "string", "required": True},
    {"name": "location_context_ref", "type": "string", "required": False},
    {"name": "pose_or_view_context_ref", "type": "string", "required": False},
    {"name": "task_context_ref", "type": "string", "required": True},
    {"name": "time_window_ref", "type": "string", "required": True},
    {"name": "freshness_status", "type": "string", "required": True},
    {"name": "ttl_policy_ref", "type": "string", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "uncertainty", "type": "number", "required": True},
    {"name": "privacy_tags", "type": "list", "required": True},
    {"name": "value_score_ref", "type": "string", "required": True},
    {"name": "conflict_refs", "type": "list", "required": True},
    {"name": "visual_refs", "type": "list", "required": True},
    {"name": "ocr_refs", "type": "list", "required": True},
    {"name": "map_refs", "type": "list", "required": True},
    {"name": "memory_refs", "type": "list", "required": True},
    {"name": "current_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

HIGH_VALUE_CANDIDATES = [
    "route_structure",
    "common_path",
    "entrance_or_exit",
    "public_facility",
    "shopfront_or_station",
    "temporary_facility",
    "scene_change",
    "safety_risk_point",
    "user_repeated_interaction_object",
    "user_confirmed_important_place_or_object",
    "OCR / map / memory conflict point",
]

LOW_VALUE_CANDIDATES = [
    "unrelated_background_pedestrian",
    "one-off_low_confidence_noise",
    "unlocalized_transient_background_object",
    "distant_unrelated_vehicle",
    "repeated_low_value_frame",
    "high_privacy_low_task_value_content",
]

ENTITY_TYPES = [
    "ObjectCandidate",
    "PlaceCandidate",
    "EventCandidate",
    "RelationCandidate",
    "FacilityCandidate",
    "SocialFacilityCandidate",
    "TemporaryFacilityCandidate",
    "RouteStructureCandidate",
    "EnvironmentalPatternCandidate",
]

ENTITY_FEATURE_FIELD_SPECS = [
    {"name": "entity_feature_candidate_id", "type": "string", "required": True},
    {"name": "source_world_observation_id", "type": "string", "required": True},
    {"name": "entity_type", "type": "enum", "required": True},
    {"name": "entity_category_candidate", "type": "string", "required": True},
    {"name": "name_candidate", "type": "string", "required": False},
    {"name": "visual_signature_refs", "type": "list", "required": True},
    {"name": "ocr_text_refs", "type": "list", "required": True},
    {"name": "location_anchor_candidate", "type": "string", "required": False},
    {"name": "universal_attributes", "type": "object", "required": True},
    {"name": "task_specific_attributes", "type": "object", "required": True},
    {"name": "user_profiled_attributes", "type": "object", "required": True},
    {"name": "social_context_attributes", "type": "object", "required": True},
    {"name": "emotional_attributes", "type": "object", "required": True},
    {"name": "operational_attributes", "type": "object", "required": True},
    {"name": "uncertainty_and_conflict", "type": "object", "required": True},
    {"name": "privacy_tags", "type": "list", "required": True},
    {"name": "requires_user_confirmation", "type": "boolean", "required": True},
    {"name": "requires_review", "type": "boolean", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

ATTRIBUTE_LAYERS = [
    "universal_attributes",
    "task_specific_attributes",
    "user_profiled_attributes",
    "social_context_attributes",
    "emotional_attributes",
    "operational_attributes",
    "uncertainty_and_conflict",
]

OBJECT_IDENTITY_FIELD_SPECS = [
    {"name": "object_identity_candidate_id", "type": "string", "required": True},
    {"name": "entity_feature_candidate_ref", "type": "string", "required": True},
    {"name": "entity_type", "type": "string", "required": True},
    {"name": "visual_signature_refs", "type": "list", "required": True},
    {"name": "location_context_refs", "type": "list", "required": True},
    {"name": "ocr_refs", "type": "list", "required": True},
    {"name": "user_alias_refs", "type": "list", "required": True},
    {"name": "historical_interaction_refs", "type": "list", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "conflict_refs", "type": "list", "required": True},
    {"name": "requires_review", "type": "boolean", "required": True},
    {"name": "requires_user_confirmation", "type": "boolean", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "identity_fact_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

TEMPORARY_FACILITY_TYPES = [
    "TemporaryFacilityCandidate",
    "MobileFacilityCandidate",
    "TransientSceneStructureCandidate",
    "RecurringTemporaryPatternCandidate",
]

TEMPORARY_MOBILE_EXAMPLES = [
    "临时摊位",
    "流动商贩",
    "临时施工围挡",
    "临时排队点",
    "临时服务台",
    "临时活动摊位",
    "临时交通管制",
    "临时路障",
    "临时公告",
    "临时公交/地铁改道提示",
    "临时市场/夜市",
    "临时人群聚集",
]

EMOTIONAL_ATTACHMENT_FIELD_SPECS = [
    {"name": "emotional_attachment_candidate_id", "type": "string", "required": True},
    {"name": "related_entity_feature_candidate_id", "type": "string", "required": True},
    {"name": "attachment_type_candidate", "type": "string", "required": True},
    {"name": "evidence_refs", "type": "list", "required": True},
    {"name": "user_feedback_refs", "type": "list", "required": True},
    {"name": "historical_interaction_refs", "type": "list", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "sensitivity_level", "type": "string", "required": True},
    {"name": "requires_user_confirmation", "type": "boolean", "required": True},
    {"name": "emotional_fact_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SCENARIO_ROWS = [
    {
        "scenario_id": "route_structure_observation",
        "focus": "观察道路结构 / 可走路径 / 入口出口",
        "outputs": ["WorldObservationCandidate"],
        "worldmodel_write_allowed": False,
    },
    {
        "scenario_id": "shopfront_entity_feature_candidate",
        "focus": "观察商铺门头 / 招牌 / 门口",
        "ocr_refs_placeholder": True,
        "outputs": ["PlaceCandidate", "FacilityCandidate"],
    },
    {
        "scenario_id": "home_familiar_object_candidate",
        "focus": "家庭熟悉物体",
        "object_identity_candidate_placeholder": True,
        "privacy_filtering_required": True,
        "identity_fact_allowed": False,
    },
    {
        "scenario_id": "temporary_mobile_vendor_candidate",
        "focus": "临时摊位 / 流动商贩",
        "ttl_short": True,
        "fixed_poi_commit_allowed": False,
    },
    {
        "scenario_id": "recurring_temporary_pattern_candidate",
        "focus": "多次出现的临时设施候选",
        "outputs": ["RecurringTemporaryPatternCandidate"],
        "long_term_promotion_allowed": False,
    },
    {
        "scenario_id": "emotional_attachment_candidate_placeholder",
        "focus": "用户相关物体 / 地点情感挂载候选",
        "requires_user_confirmation": True,
        "emotional_fact_allowed": False,
    },
    {
        "scenario_id": "scene_change_candidate",
        "focus": "施工 / 店铺变化 / 路线变化",
        "outputs": ["scene_change_candidate", "correction_handoff_candidate"],
        "auto_fact_correction_allowed": False,
    },
    {
        "scenario_id": "low_value_background_discard",
        "focus": "背景行人 / 远处车辆 / 低价值噪声",
        "discard_allowed": True,
        "enters_long_term_chain": False,
    },
]

GOVERNANCE_DEBT_TOPICS = [
    "world observation value filtering complexity",
    "entity feature attribute layering complexity",
    "temporary facility recurrence governance complexity",
    "object identity placeholder governance complexity",
    "emotional attachment placeholder governance complexity",
    "worldmodel memory library placeholder governance complexity",
    "duplicated schema risk",
    "future midplatform function governance required",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_root(path_str: Optional[str], summary_file: str) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir())
    summary_path = root / summary_file if loaded else None
    summary_loaded = bool(summary_path and summary_path.is_file())
    return {
        "root": root,
        "loaded": loaded and summary_loaded,
        "summary_path": summary_path if summary_loaded else None,
    }


def _doc_row(repo_root: Path, intake_id: str, rel_path: str, required: bool) -> Dict[str, Any]:
    abs_path = repo_root / rel_path
    loaded = abs_path.is_file()
    return {
        "intake_id": intake_id,
        "label": intake_id,
        "path": rel_path,
        "loaded": loaded,
        "required": required,
        "status": "loaded" if loaded else ("missing_required" if required else "optional_missing"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        **BOUNDARY_FALSE_FLAGS,
        "full_background_recording_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _load_optional_json(root_meta: Dict[str, Any], filename: str) -> Dict[str, Any]:
    root = root_meta.get("root")
    path = root / filename if root else None
    if path and path.is_file():
        return _read_json(path)
    return {}


def run_world_observation_and_entity_feature_policy_v1(
    *,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    return_to_vision_planning_root: str,
    preplan_input_root: str,
    ocr_final_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    workspace_root: str,
) -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    workspace = Path(workspace_root).expanduser().resolve()

    root_arg_values = {
        "task_aware_visual_focus_root": task_aware_visual_focus_root,
        "midplatform_perception_orchestration_root": midplatform_perception_orchestration_root,
        "return_to_vision_planning_root": return_to_vision_planning_root,
        "preplan_input_root": preplan_input_root,
        "ocr_final_closure_root": ocr_final_closure_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
    }
    root_meta = {
        spec["intake_id"]: _load_root(root_arg_values[spec["path_arg"]], spec["summary_file"])
        for spec in ROOT_INPUT_SPECS
    }

    input_root_rows: List[Dict[str, Any]] = []
    for spec in ROOT_INPUT_SPECS:
        meta = root_meta[spec["intake_id"]]
        input_root_rows.append(
            {
                "intake_id": spec["intake_id"],
                "label": spec["label"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "summary_file": spec["summary_file"],
                "extra_artifacts": spec["extra_artifacts"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    for intake_id, rel_path in REQUIRED_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, True))
    for intake_id, rel_path in OPTIONAL_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, False))

    visual_focus_summary = _read_json(root_meta["task_aware_visual_focus"]["summary_path"]) if root_meta["task_aware_visual_focus"]["summary_path"] else {}
    midplatform_summary = _read_json(root_meta["midplatform_perception_orchestration"]["summary_path"]) if root_meta["midplatform_perception_orchestration"]["summary_path"] else {}
    planning_summary = _read_json(root_meta["return_to_vision_planning"]["summary_path"]) if root_meta["return_to_vision_planning"]["summary_path"] else {}
    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    visual_focus_boundary = _load_optional_json(root_meta["task_aware_visual_focus"], "deferred_worldmodel_memory_library_boundary.json")
    midplatform_boundary = _load_optional_json(root_meta["midplatform_perception_orchestration"], "worldmodel_memory_library_handoff_boundary.json")
    planning_boundary = _load_optional_json(root_meta["return_to_vision_planning"], "deferred_worldmodel_memory_library_boundary.json")
    preplan_boundary = _load_optional_json(root_meta["preplan_input"], "deferred_worldmodel_memory_library_boundary.json")

    task_aware_visual_focus_input_loaded = (
        root_meta["task_aware_visual_focus"]["loaded"]
        and visual_focus_summary.get("final_decision") == VISUAL_FOCUS_FINAL_DECISION
        and visual_focus_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
    midplatform_perception_orchestration_input_loaded = (
        root_meta["midplatform_perception_orchestration"]["loaded"]
        and midplatform_summary.get("final_decision") == MIDPLATFORM_FINAL_DECISION
        and midplatform_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
    return_to_vision_planning_input_loaded = (
        root_meta["return_to_vision_planning"]["loaded"]
        and planning_summary.get("final_decision") == PLANNING_FINAL_DECISION
        and planning_summary.get("worldmodel_memory_library_boundary_deferred") is True
    )
    preplan_input_loaded = (
        root_meta["preplan_input"]["loaded"]
        and preplan_summary.get(PREPLAN_READY_FLAG) is True
        and preplan_summary.get("worldmodel_memory_library_boundary_deferred") is True
    )
    ocr_final_closure_loaded = root_meta["ocr_final_closure"]["loaded"] and ocr_summary.get("final_decision") == OCR_FINAL_DECISION
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and mri_summary.get("final_decision") == MRI_FINAL_DECISION
    )

    world_observation_layer_policy = {
        "policy_id": f"{POLICY_ID}_world_observation_layer",
        "scope": "background_low_frequency_candidate_layer",
        "allowed_observation_targets": [
            "route_structure",
            "road_surface",
            "walkable_path",
            "entrance_or_exit",
            "public_facility",
            "shopfront_or_signage",
            "temporary_facility",
            "environmental_pattern",
            "scene_change",
            "safety_risk_point",
            "user_relevant_place",
            "recurring_observation",
        ],
        "forbidden_observation_targets": [
            "full_background_recording",
            "unbounded_all_person_logging",
            "unbounded_all_vehicle_logging",
            "privacy_sensitive_low_value_background_capture",
            "navigation_action_authority",
            "worldmodel_write",
            "memory_write",
            "library_write",
        ],
        "background_budget_ref": "MidPlatformResourceBudgetPolicy.background_world_observation_budget",
        "privacy_policy_ref": "MidPlatformPrivacyFilteringPolicy",
        "freshness_policy_ref": "STC / freshness reuse family",
        "ttl_policy_ref": "reuse_existing_midplatform_ttl_policy",
        "worldmodel_handoff_boundary_ref": "worldmodel_memory_library_placeholder_policy.json",
        "value_filtering_policy_ref": "world_observation_value_filtering_policy.json",
        "background_low_frequency_only": True,
        "not_real_time_action_path": True,
        "not_navigation_authority": True,
        "not_speech_output_source": True,
        "not_worldmodel_writer": True,
        "not_memory_writer": True,
        "not_library_writer": True,
        "resource_budget_controlled_by_midplatform": True,
        "privacy_filtering_controlled_by_midplatform": True,
        "full_background_recording_allowed": False,
        "world_observation_runtime_enabled": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    world_observation_candidate_schema = {
        "schema_id": f"{POLICY_ID}_world_observation_candidate",
        "object_name": "WorldObservationCandidate",
        "observation_types": WORLD_OBSERVATION_TYPES,
        "fields": WORLD_OBSERVATION_FIELD_SPECS,
        "field_count": len(WORLD_OBSERVATION_FIELD_SPECS),
        "non_claims": [
            "WorldObservationCandidate 不等于 WorldModel 事实。",
            "WorldObservationCandidate 不等于导航 authority。",
            "WorldObservationCandidate 不直接进入 speech output。",
            "WorldObservationCandidate 只是未来 WorldModel / Memory / Library 的候选材料。",
        ],
        "current_action_allowed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "source_chain": SOURCE_CHAIN,
    }

    world_observation_value_filtering_policy = {
        "policy_id": f"{POLICY_ID}_world_observation_value_filtering",
        "high_value_candidates": HIGH_VALUE_CANDIDATES,
        "low_value_candidates": LOW_VALUE_CANDIDATES,
        "value_filter_fields": [
            "value_filter_id",
            "observation_value_score",
            "long_term_value_candidate",
            "current_task_value",
            "safety_value",
            "recurrence_value",
            "user_confirmed_value",
            "privacy_risk",
            "storage_policy",
            "discard_allowed",
            "archive_allowed",
            "worldmodel_handoff_allowed_candidate",
            "source_chain",
        ],
        "full_background_recording_allowed": False,
        "principles": [
            "后台世界观察不能退化成全量记录。",
            "高价值候选才允许进入 archive / handoff 链。",
            "低价值背景噪声应允许 discard。",
            "高隐私低任务价值内容优先丢弃或限制。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    world_entity_feature_candidate_schema = {
        "schema_id": f"{POLICY_ID}_world_entity_feature",
        "object_name": "WorldEntityFeatureCandidate",
        "entity_types": ENTITY_TYPES,
        "attribute_layers": ATTRIBUTE_LAYERS,
        "fields": ENTITY_FEATURE_FIELD_SPECS,
        "field_count": len(ENTITY_FEATURE_FIELD_SPECS),
        "principles": [
            "user_profiled_attributes 只能来自用户授权 / 配置 / 历史确认，不得由视觉默认推断敏感身份。",
            "emotional_attributes 只能是候选，不得写成情感事实。",
            "entity feature candidate 不等于实体事实。",
            "本阶段不做 entity resolution。",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
        "source_chain": SOURCE_CHAIN,
    }

    object_identity_candidate_schema = {
        "schema_id": f"{POLICY_ID}_object_identity",
        "object_name": "ObjectIdentityCandidate",
        "fields": OBJECT_IDENTITY_FIELD_SPECS,
        "field_count": len(OBJECT_IDENTITY_FIELD_SPECS),
        "identity_fact_allowed": False,
        "principles": [
            "单次观察不得生成 identity fact。",
            "当前阶段不做 Object Identity runtime。",
            "ObjectIdentityCandidate 只进入 future Memory / WorldModel 专项。",
            "家庭物品需要 privacy filtering。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    temporary_mobile_social_facility_policy = {
        "policy_id": f"{POLICY_ID}_temporary_mobile_social_facility",
        "candidate_types": TEMPORARY_FACILITY_TYPES,
        "covered_cases": TEMPORARY_MOBILE_EXAMPLES,
        "field_contract": [
            "facility_candidate_id",
            "facility_type",
            "observed_location_context",
            "observed_time_window",
            "mobility_status",
            "recurrence_hint",
            "visual_refs",
            "ocr_refs",
            "user_feedback_refs",
            "map_conflict_refs",
            "ttl_policy_ref",
            "current_action_relevance",
            "long_term_value_candidate",
            "expiration_condition",
            "review_required",
            "fixed_poi_commit_allowed",
            "fact_status",
            "source_chain",
        ],
        "fixed_poi_commit_allowed": False,
        "principles": [
            "临时设施默认 TTL 短。",
            "可用于当前任务 / 安全候选。",
            "不默认写长期 WorldModel。",
            "多次同地 / 同时间窗出现，只能升级为 recurring temporary pattern candidate。",
            "不能写成固定 POI。",
            "必须与 static POI 区分。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    emotional_attachment_candidate_policy = {
        "policy_id": f"{POLICY_ID}_emotional_attachment",
        "fields": EMOTIONAL_ATTACHMENT_FIELD_SPECS,
        "field_count": len(EMOTIONAL_ATTACHMENT_FIELD_SPECS),
        "emotional_fact_allowed": False,
        "principles": [
            "不根据单次视觉观察推断用户情感。",
            "不对陌生人做情感挂载。",
            "情感挂载不写事实。",
            "后续交给情感引擎 / 记忆治理处理。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    worldmodel_memory_library_placeholder_policy = {
        "policy_id": f"{POLICY_ID}_wml_placeholder",
        "allowed_now": [
            "WorldModelHandoffCandidate",
            "MemoryHandoffCandidate",
            "LibraryHandoffPlaceholder",
            "ExperienceCandidatePlaceholder",
        ],
        "forbidden_now": [
            "entity_resolution_runtime",
            "fact_admission",
            "worldmodel_write",
            "memory_write",
            "library_experience_commit",
            "memory_consolidation",
            "object_identity_fact_commit",
            "emotional_attachment_fact_commit",
            "temporary_facility_long_term_promotion",
            "route_experience_commit",
        ],
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "visual_focus_boundary_loaded": bool(visual_focus_boundary.get("boundary_id")),
        "midplatform_boundary_loaded": bool(midplatform_boundary.get("boundary_id")),
        "planning_boundary_loaded": bool(planning_boundary.get("boundary_scope")),
        "preplan_boundary_loaded": bool(preplan_boundary.get("boundary_scope")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    world_observation_feedback_policy = {
        "policy_id": f"{POLICY_ID}_world_observation_feedback",
        "output_candidates": [
            "WorldObservationFeedbackCandidate",
            "EntityFeatureFeedbackCandidate",
            "TemporaryFacilityFeedbackCandidate",
            "ObjectIdentityFeedbackCandidate",
            "WorldModelHandoffCandidate",
            "MemoryHandoffCandidate",
            "LibraryHandoffPlaceholder",
        ],
        "principles": [
            "feedback candidate 不直接播报。",
            "speech_allowed=false until Speech Gate。",
            "action_allowed=false。",
            "fact_status=not_fact。",
            "requires_arbitration_or_review=true。",
            "source_chain required。",
        ],
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "requires_arbitration_or_review": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    world_observation_entity_feature_scenario_matrix = {
        "matrix_id": f"{POLICY_ID}_scenario_matrix",
        "scenarios": [
            {
                **row,
                "requires_runtime_now": False,
                "fact_write_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for row in SCENARIO_ROWS
        ],
        "scenario_count": len(SCENARIO_ROWS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    world_observation_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_boundary_matrix",
        "full_background_recording_allowed": False,
        "world_observation_runtime_enabled": False,
        "camera_runtime_allowed": False,
        "map_api_allowed": False,
        "ocr_provider_runtime_allowed": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_allowed": False,
        "optical_flow_runtime_allowed": False,
        "supervision_runtime_allowed": False,
        "bytetrack_runtime_allowed": False,
        "ocsort_runtime_allowed": False,
        "entity_resolution_runtime_allowed": False,
        "fact_admission_runtime_allowed": False,
        "memory_consolidation_allowed": False,
        "library_experience_commit_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "scene_delta_allowed": False,
        "task_state_commit_allowed": False,
        "navigation_action_allowed": False,
        "speech_gate_allowed": False,
        "vop_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "register_id": f"{POLICY_ID}_governance_debt",
        "debts": [
            {
                "debt_id": f"debt_{idx:02d}",
                "topic": topic,
                "deferred_reason": "先完成世界观察与实体特征候选主链，再统一做 MidPlatform Function Governance / Consolidation。",
                "future_owner_phase": "MidPlatform Function Governance / Consolidation",
                "reuse_or_consolidation_required": True,
                "duplicate_governance_module_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for idx, topic in enumerate(GOVERNANCE_DEBT_TOPICS, start=1)
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{POLICY_ID}_next_phase",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "世界观察与实体特征候选层已定义完成，下一阶段应进入 Selective Tracking Adapter Policy 以定义候选追踪请求边界。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "world_observation_layer_policy_defined": True,
        "world_observation_candidate_schema_defined": True,
        "world_observation_value_filtering_policy_defined": True,
        "world_entity_feature_candidate_schema_defined": True,
        "object_identity_candidate_schema_defined": True,
        "temporary_mobile_social_facility_policy_defined": True,
        "emotional_attachment_candidate_policy_defined": True,
        "worldmodel_memory_library_placeholder_policy_defined": True,
        "world_observation_feedback_policy_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(SCENARIO_ROWS),
        "full_background_recording_allowed": False,
        "world_observation_runtime_enabled": False,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "object_identity_fact_allowed": False,
        "emotional_attachment_fact_allowed": False,
        "fixed_poi_commit_allowed": False,
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "governance_debt_register_generated": True,
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION,
        "recommended_next_phase": NEXT_PHASE,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": summary,
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "world_observation_layer_policy": world_observation_layer_policy,
        "world_observation_candidate_schema": world_observation_candidate_schema,
        "world_observation_value_filtering_policy": world_observation_value_filtering_policy,
        "world_entity_feature_candidate_schema": world_entity_feature_candidate_schema,
        "object_identity_candidate_schema": object_identity_candidate_schema,
        "temporary_mobile_social_facility_policy": temporary_mobile_social_facility_policy,
        "emotional_attachment_candidate_policy": emotional_attachment_candidate_policy,
        "worldmodel_memory_library_placeholder_policy": worldmodel_memory_library_placeholder_policy,
        "world_observation_feedback_policy": world_observation_feedback_policy,
        "world_observation_entity_feature_scenario_matrix": world_observation_entity_feature_scenario_matrix,
        "world_observation_boundary_matrix": world_observation_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "visual_focus_final_decision": visual_focus_summary.get("final_decision"),
            "midplatform_final_decision": midplatform_summary.get("final_decision"),
            "planning_final_decision": planning_summary.get("final_decision"),
            "preplan_ready_flag": preplan_summary.get(PREPLAN_READY_FLAG),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "scenario_count": len(SCENARIO_ROWS),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": NEXT_PHASE,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
    }
