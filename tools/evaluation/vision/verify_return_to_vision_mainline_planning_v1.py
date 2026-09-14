#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Return To Vision Mainline Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "return_to_vision_mainline_planning_v1_smoke_v0"

FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
NEXT_PHASE = "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001"
PHASE_ID = "Phase-Return-To-Vision-Mainline-Planning-v1-001"
MIN_CHECKS = 120
BASELINE_REQUIREMENT = 90


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _contains_any(texts: List[str], needle: str) -> bool:
    lowered = needle.lower()
    return any(lowered in text.lower() for text in texts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Return-To-Vision Mainline Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def expect(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(output_root / "summary.json")
    input_root_matrix = _load_json(output_root / "input_root_matrix.json")
    planning_report = _load_json(output_root / "vision_mainline_planning_report.json")
    roadmap = _load_json(output_root / "vision_mainline_roadmap.json")
    adopted = _load_json(output_root / "adopted_preplan_principles.json")
    rejected = _load_json(output_root / "rejected_patterns_register.json")
    reuse = _load_json(output_root / "midplatform_reuse_commitment.json")
    bans = _load_json(output_root / "duplicate_module_ban_list.json")
    boundary = _load_json(output_root / "governance_boundary_matrix.json")
    first_batch = _load_json(output_root / "first_batch_phase_definitions.json")
    deferred = _load_json(output_root / "deferred_capability_register.json")
    wml_boundary = _load_json(output_root / "deferred_worldmodel_memory_library_boundary.json")
    wml_placeholder = _load_json(output_root / "worldmodel_memory_library_placeholder_plan.json")
    non_claims = _load_json(output_root / "vision_mainline_non_claims_register.json")
    readiness = _load_json(output_root / "formal_readiness_gate.json")
    next_phase = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write = _load_json(output_root / "no_write_boundary_report.json")

    # Input checks
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)
    expect("input.root_matrix_rows_present", isinstance(input_root_matrix.get("rows"), list))
    expect("input.root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_root_matrix.get("rows", [])))
    expect(
        "input.preplan_root_present",
        any(row.get("intake_id") == "preplan_input" and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
    )
    expect(
        "input.ocr_root_present",
        any(row.get("intake_id") == "ocr_final_closure" and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
    )
    expect(
        "input.mri_root_present",
        any(
            row.get("intake_id") == "minimal_runtime_integration_closure" and row.get("loaded") is True
            for row in input_root_matrix.get("rows", [])
        ),
    )
    for intake_id in (
        "preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ):
        expect(
            f"input.required_doc.{intake_id}",
            any(row.get("intake_id") == intake_id and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
        )

    # Planning checks
    expect("planning.formal_mainline_name", summary.get("formal_mainline_name") == "Task-Aware Perception Orchestration")
    expect("planning.planning_report_generated", summary.get("planning_report_generated") is True)
    expect("planning.roadmap_generated", summary.get("roadmap_generated") is True)
    expect("planning.adopted_preplan_principles_generated", summary.get("adopted_preplan_principles_generated") is True)
    expect("planning.rejected_patterns_register_generated", summary.get("rejected_patterns_register_generated") is True)
    expect("planning.midplatform_reuse_commitment_generated", summary.get("midplatform_reuse_commitment_generated") is True)
    expect("planning.duplicate_module_ban_list_generated", summary.get("duplicate_module_ban_list_generated") is True)
    expect("planning.governance_boundary_matrix_generated", summary.get("governance_boundary_matrix_generated") is True)
    expect("planning.first_batch_phase_definitions_generated", summary.get("first_batch_phase_definitions_generated") is True)
    expect("planning.deferred_capability_register_generated", summary.get("deferred_capability_register_generated") is True)
    expect(
        "planning.deferred_worldmodel_memory_library_boundary_generated",
        summary.get("deferred_worldmodel_memory_library_boundary_generated") is True,
    )
    expect(
        "planning.worldmodel_memory_library_placeholder_plan_generated",
        summary.get("worldmodel_memory_library_placeholder_plan_generated") is True,
    )
    expect("planning.non_claims_register_generated", summary.get("non_claims_register_generated") is True)
    expect("planning.formal_readiness_gate_generated", summary.get("formal_readiness_gate_generated") is True)
    expect("planning.report_scope", planning_report.get("planning_scope") == "return_to_vision_mainline_planning")
    expect("planning.report_final_name", planning_report.get("formal_mainline_name") == "Task-Aware Perception Orchestration")
    expect("planning.report_next_phase", planning_report.get("next_phase_recommendation") == NEXT_PHASE)
    expect("planning.report_reuse_ref", planning_report.get("reuse_commitment_ref") == "midplatform_reuse_commitment.json")
    expect("planning.report_boundary_ref", planning_report.get("governance_boundary_ref") == "governance_boundary_matrix.json")
    expect(
        "planning.report_first_batch_ref",
        planning_report.get("first_batch_phase_definitions_ref") == "first_batch_phase_definitions.json",
    )
    expect(
        "planning.report_wml_boundary_ref",
        planning_report.get("deferred_worldmodel_memory_library_boundary_ref")
        == "deferred_worldmodel_memory_library_boundary.json",
    )
    expect(
        "planning.report_wml_placeholder_ref",
        planning_report.get("worldmodel_memory_library_placeholder_plan_ref")
        == "worldmodel_memory_library_placeholder_plan.json",
    )
    expect(
        "planning.report_wml_boundary_deferred",
        planning_report.get("worldmodel_memory_library_boundary_deferred") is True,
    )
    expect("planning.report_p0_count", (planning_report.get("capability_priority_summary") or {}).get("p0_count") >= 8)
    expect("planning.report_p1_count", (planning_report.get("capability_priority_summary") or {}).get("p1_count") >= 6)
    expect("planning.report_p2_count", (planning_report.get("capability_priority_summary") or {}).get("p2_count") >= 6)

    # Principle checks
    principle_texts = [item.get("statement", "") for item in adopted.get("principles", [])]
    expect("principles.count_ge_18", len(principle_texts) >= 18, len(principle_texts))
    expect("principles.no_3x3_mainline", _contains_any(principle_texts, "3×3") or _contains_any(principle_texts, "3x3"))
    expect("principles.full_scene_tracking_forbidden", _contains_any(principle_texts, "full-scene tracking"))
    expect("principles.full_frame_ocr_forbidden", _contains_any(principle_texts, "full-frame OCR"))
    expect("principles.midplatform_owns_orchestration", _contains_any(principle_texts, "中台负责感知编排"))
    expect("principles.midplatform_owns_resource_budget", _contains_any(principle_texts, "Resource Budget 归中台"))
    expect("principles.midplatform_owns_privacy_filtering", _contains_any(principle_texts, "Privacy Filtering 归中台"))
    expect("principles.map_memory_context_hints_only", _contains_any(principle_texts, "context hint"))
    expect("principles.ocr_focus_triggered_only", _contains_any(principle_texts, "OCR only focus-triggered"))
    expect("principles.world_observation_candidate_only", _contains_any(principle_texts, "World Observation Layer"))
    expect("principles.world_entity_feature_candidate_only", _contains_any(principle_texts, "WorldEntityFeatureCandidate"))
    expect("principles.crossing_future_safety_governance", _contains_any(principle_texts, "Crossing Decision"))
    expect("principles.reuse_first_present", _contains_any(principle_texts, "Reuse First"))

    # Reuse checks
    reuse_assets = reuse.get("priority_reuse_assets", [])
    expect("reuse.count_ge_10", len(reuse_assets) >= 10, len(reuse_assets))
    expect("reuse.task_observation_request", any("Task Observation Request" in item for item in reuse_assets))
    expect("reuse.task_manager_state", any("Task Manager" in item or "Task State" in item for item in reuse_assets))
    expect("reuse.safety_task_arbitration", any("Safety-Task Arbitration" in item for item in reuse_assets))
    expect("reuse.stc", any("STC" in item for item in reuse_assets))
    expect("reuse.ocr_activation_ocrrequest", any("OCR Activation" in item or "OCRRequest" in item for item in reuse_assets))
    expect("reuse.worldmodel_slot_lookup", any("WorldModel unresolved observation slot" in item or "lookup" in item for item in reuse_assets))
    expect("reuse.memory_governance", any("Memory governance" in item for item in reuse_assets))
    expect("reuse.map_anchor", any("MapAnchor" in item for item in reuse_assets))
    expect("reuse.system_health_hardware", any("System Health" in item or "Hardware Profile" in item for item in reuse_assets))
    expect("reuse.speech_gate_vop", any("Speech Gate" in item or "VOP" in item for item in reuse_assets))
    expect("reuse.resource_budget_owner", reuse.get("resource_budget_owner") == "MidPlatform")
    expect("reuse.privacy_filtering_owner", reuse.get("privacy_filtering_owner") == "MidPlatform")

    # Duplicate bans
    ban_items = bans.get("forbidden_parallel_systems", [])
    expect("bans.count_ge_10", len(ban_items) >= 10, len(ban_items))
    for needle, check_id in (
        ("new STC", "bans.new_stc"),
        ("new TTL", "bans.new_ttl"),
        ("new source_chain", "bans.new_source_chain"),
        ("new Evidence Pack", "bans.new_evidence_pack"),
        ("new Memory write path", "bans.new_memory_write_path"),
        ("new WorldModel write path", "bans.new_worldmodel_write_path"),
        ("new Task State", "bans.new_task_state"),
        ("new Speech Gate / VOP", "bans.new_speech_gate_vop"),
        ("new Runtime Trial / Closure framework", "bans.new_runtime_framework"),
        ("new standalone resource budget outside MidPlatform", "bans.new_standalone_budget"),
        ("new standalone privacy filtering outside MidPlatform", "bans.new_standalone_privacy"),
    ):
        expect(check_id, any(needle in item for item in ban_items))

    # Boundary matrix checks
    expect("boundary.camera_runtime_allowed", boundary.get("camera_runtime_allowed") is False)
    expect("boundary.ocr_provider_runtime_allowed", boundary.get("ocr_provider_runtime_allowed") is False)
    expect("boundary.tracking_runtime_allowed", boundary.get("tracking_runtime_allowed") is False)
    expect("boundary.optical_flow_runtime_allowed", boundary.get("optical_flow_runtime_allowed") is False)
    expect("boundary.map_api_allowed", boundary.get("map_api_allowed") is False)
    expect("boundary.memory_write_allowed", boundary.get("memory_write_allowed") is False)
    expect("boundary.library_write_allowed", boundary.get("library_write_allowed") is False)
    expect("boundary.worldmodel_write_allowed", boundary.get("worldmodel_write_allowed") is False)
    expect("boundary.fact_write_allowed", boundary.get("fact_write_allowed") is False)
    expect("boundary.entity_fusion_runtime_allowed", boundary.get("entity_fusion_runtime_allowed") is False)
    expect("boundary.fact_admission_runtime_allowed", boundary.get("fact_admission_runtime_allowed") is False)
    expect("boundary.scene_delta_allowed", boundary.get("scene_delta_allowed") is False)
    expect("boundary.navigation_action_allowed", boundary.get("navigation_action_allowed") is False)
    expect("boundary.task_commit_allowed", boundary.get("task_commit_allowed") is False)
    expect("boundary.full_frame_ocr_allowed", boundary.get("full_frame_ocr_allowed") is False)
    expect("boundary.full_scene_tracking_allowed", boundary.get("full_scene_tracking_allowed") is False)

    # First batch phases
    phase_rows = first_batch.get("phases", [])
    phase_names = [row.get("phase") for row in phase_rows]
    expect("first_batch.count_ge_6", len(phase_rows) >= 6, len(phase_rows))
    expect("first_batch.midplatform_perception_policy", "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001" in phase_names)
    expect("first_batch.visual_focus_policy", "Phase-Task-Aware-Visual-Focus-Policy-v1-001" in phase_names)
    expect("first_batch.world_observation_entity_feature_policy", "Phase-World-Observation-and-Entity-Feature-Policy-v1-001" in phase_names)
    expect("first_batch.selective_tracking_policy", "Phase-Selective-Tracking-Adapter-Policy-v1-001" in phase_names)
    expect("first_batch.visual_ocr_map_feedback_dryrun", "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001" in phase_names)
    expect("first_batch.basic_navigation_loop_dryrun", "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001" in phase_names)
    for idx, row in enumerate(phase_rows):
        expect(f"first_batch.runtime_allowed_now_{idx}", row.get("runtime_allowed_now") is False)
        expect(f"first_batch.fact_write_allowed_{idx}", row.get("fact_write_allowed") is False)
        expect(f"first_batch.phase_kind_present_{idx}", row.get("phase_kind") in {"policy", "dryrun"})

    # Roadmap checks
    expect("roadmap.mainline_name", roadmap.get("formal_mainline_name") == "Task-Aware Perception Orchestration")
    expect("roadmap.p0_group_count", len(roadmap.get("p0_capability_group", [])) >= 8)
    expect("roadmap.p1_group_count", len(roadmap.get("p1_capability_group", [])) >= 6)
    expect("roadmap.p2_group_count", len(roadmap.get("p2_capability_group", [])) >= 6)
    expect("roadmap.first_batch_match", len(roadmap.get("first_batch_phases", [])) >= 6)
    expect("roadmap.deferred_capabilities_present", len(roadmap.get("deferred_capabilities", [])) >= 10)
    expect("roadmap.future_research_candidates_present", len(roadmap.get("future_research_candidates", [])) >= 3)
    expect(
        "roadmap.blocked_capabilities_present",
        any("runtime" in str(item).lower() or "write" in str(item).lower() for item in roadmap.get("blocked_capabilities", [])),
    )

    # Deferred register checks
    deferred_caps = [row.get("capability") for row in deferred.get("deferred_capabilities", [])]
    expect("deferred.real_camera_runtime", "real camera runtime" in deferred_caps)
    expect("deferred.real_ocr_provider", "real OCR provider" in deferred_caps)
    expect("deferred.real_tracking_runtime", "real tracking runtime" in deferred_caps)
    expect("deferred.supervision_runtime", "Supervision runtime integration" in deferred_caps)
    expect("deferred.bytetrack_runtime", "ByteTrack / OC-SORT runtime" in deferred_caps)
    expect("deferred.optical_flow_runtime", "optical flow runtime" in deferred_caps)
    expect("deferred.map_api", "map API / 高德 API" in deferred_caps)
    expect("deferred.entity_resolution_runtime", "Entity Resolution runtime" in deferred_caps)
    expect("deferred.object_identity_runtime_confirmation", "Object Identity Over Time runtime confirmation" in deferred_caps)
    expect("deferred.worldmodel_fact_admission", "WorldModel Fact Admission" in deferred_caps)
    expect("deferred.worldmodel_write", "WorldModel write" in deferred_caps)
    expect("deferred.worldmodel_query_runtime", "WorldModel Query Runtime" in deferred_caps)
    expect("deferred.memory_consolidation", "Memory Consolidation" in deferred_caps)
    expect("deferred.memory_write", "Memory write" in deferred_caps)
    expect("deferred.user_preference_fact_write", "User Preference Fact Write" in deferred_caps)
    expect("deferred.emotional_attachment_fact_write", "Emotional Attachment Fact Write" in deferred_caps)
    expect("deferred.library_experience_governance", "Library Experience Governance" in deferred_caps)
    expect("deferred.experience_reuse_admission", "Experience Reuse Admission" in deferred_caps)
    expect("deferred.long_term_route_experience_commit", "Long-term Route Experience Commit" in deferred_caps)
    expect("deferred.social_facility_fact_commit", "Social Facility Fact Commit" in deferred_caps)
    expect("deferred.temporary_facility_long_term_promotion", "Temporary Facility Long-term Promotion" in deferred_caps)
    expect("deferred.fact_write", "Fact write" in deferred_caps)
    expect("deferred.scene_delta_commit", "Scene Delta commit" in deferred_caps)
    expect("deferred.real_tts_audio", "real TTS / audio" in deferred_caps)
    expect("deferred.face_recognition", "face recognition" in deferred_caps)
    expect("deferred.voiceprint", "voiceprint" in deferred_caps)
    expect("deferred.facial_expression_audio_emotion", "facial expression / audio emotion" in deferred_caps)
    expect("deferred.full_background_recording", "full background recording" in deferred_caps)
    expect("deferred.crossing_action_instruction", "crossing action instruction" in deferred_caps)
    expect("deferred.future_research_count", len(deferred.get("future_research_candidates", [])) >= 3)

    # Non-claims checks
    non_claim_texts = non_claims.get("statements", [])
    expect("non_claims.count_ge_12", len(non_claim_texts) >= 12, len(non_claim_texts))
    expect("non_claims.planning_not_runtime", _contains_any(non_claim_texts, "planning 不等于 runtime"))
    expect("non_claims.orchestration_not_model_integrated", _contains_any(non_claim_texts, "不等于模型已接入"))
    expect("non_claims.work_order_not_executed", _contains_any(non_claim_texts, "Work Order 不等于真实视觉调度已执行"))
    expect("non_claims.scene_sketch_not_fact", _contains_any(non_claim_texts, "Scene Sketch 不等于环境事实"))
    expect("non_claims.visual_focus_plan_not_real_cutting", _contains_any(non_claim_texts, "VisualFocusPlan 不等于已经真实切割画面"))
    expect("non_claims.tracking_policy_not_runtime", _contains_any(non_claim_texts, "SelectiveTrackingPolicy 不等于追踪 runtime"))
    expect("non_claims.world_observation_not_write", _contains_any(non_claim_texts, "World Observation 不等于 WorldModel 写入"))
    expect("non_claims.world_entity_not_fact", _contains_any(non_claim_texts, "WorldEntityFeatureCandidate 不等于实体事实"))
    expect("non_claims.temporary_facility_not_poi", _contains_any(non_claim_texts, "TemporaryFacilityCandidate 不等于固定 POI"))
    expect("non_claims.crowd_flow_not_nav_instruction", _contains_any(non_claim_texts, "CrowdFlowFollowingCandidate 不等于导航指令"))
    expect("non_claims.crossing_not_cross_now", _contains_any(non_claim_texts, "CrossingCandidate 不等于允许过马路"))
    expect("non_claims.map_memory_not_reality", _contains_any(non_claim_texts, "Map / Memory hint 不等于现实事实"))
    expect("non_claims.ocr_focus_not_provider_runtime", _contains_any(non_claim_texts, "OCR focus-triggered 不等于 OCR provider runtime"))
    expect("non_claims.text_candidate_not_user_heard", _contains_any(non_claim_texts, "text-only / candidate 输出不等于真实用户听见"))
    expect("non_claims.worldmodel_handoff_not_write", _contains_any(non_claim_texts, "WorldModelHandoffCandidate 不等于已经写入 WorldModel"))
    expect("non_claims.memory_handoff_not_write", _contains_any(non_claim_texts, "MemoryHandoffCandidate 不等于已经写入 Memory"))
    expect("non_claims.library_handoff_not_live", _contains_any(non_claim_texts, "LibraryHandoffPlaceholder 不等于图书馆经验已生效"))
    expect("non_claims.object_identity_candidate_not_fact", _contains_any(non_claim_texts, "ObjectIdentityCandidate 不等于长期对象身份事实"))
    expect("non_claims.emotional_attachment_candidate_not_fact", _contains_any(non_claim_texts, "EmotionalAttachmentCandidate 不等于用户情感事实"))
    expect("non_claims.experience_candidate_not_admitted", _contains_any(non_claim_texts, "ExperienceCandidatePlaceholder 不等于经验已复用准入"))

    # Deferred WorldModel/Memory/Library boundary checks
    wml_allowed = wml_boundary.get("current_vision_mainline_allowed", [])
    wml_allowed_types = wml_boundary.get("current_vision_mainline_allowed_candidate_types", [])
    wml_forbidden = wml_boundary.get("current_vision_mainline_forbidden", [])
    wml_future = wml_boundary.get("deferred_to_future_phases", [])
    wml_risks = wml_boundary.get("misuse_risks", [])
    expect("wml_boundary.scope", wml_boundary.get("boundary_scope") == "deferred_worldmodel_memory_library_boundary")
    expect("wml_boundary.allowed_count_ge_9", len(wml_allowed) >= 9, len(wml_allowed))
    expect("wml_boundary.allowed_visual_observation", "generate_visual_observation_candidate" in wml_allowed)
    expect("wml_boundary.allowed_world_observation", "generate_world_observation_candidate" in wml_allowed)
    expect("wml_boundary.allowed_world_entity_feature", "generate_world_entity_feature_candidate" in wml_allowed)
    expect("wml_boundary.allowed_object_identity", "generate_object_identity_candidate" in wml_allowed)
    expect("wml_boundary.allowed_temporary_facility", "generate_temporary_facility_candidate" in wml_allowed)
    expect("wml_boundary.allowed_perception_correction", "generate_perception_correction_candidate" in wml_allowed)
    expect("wml_boundary.allowed_worldmodel_handoff", "generate_worldmodel_handoff_candidate" in wml_allowed)
    expect("wml_boundary.allowed_memory_handoff", "generate_memory_handoff_candidate" in wml_allowed)
    expect("wml_boundary.allowed_library_handoff", "generate_library_handoff_placeholder" in wml_allowed)
    expect("wml_boundary.allowed_types_count_ge_11", len(wml_allowed_types) >= 11, len(wml_allowed_types))
    expect("wml_boundary.allowed_type_worldmodel_handoff", "WorldModelHandoffCandidate" in wml_allowed_types)
    expect("wml_boundary.allowed_type_memory_handoff", "MemoryHandoffCandidate" in wml_allowed_types)
    expect("wml_boundary.allowed_type_library_handoff", "LibraryHandoffPlaceholder" in wml_allowed_types)
    expect("wml_boundary.allowed_type_experience_placeholder", "ExperienceCandidatePlaceholder" in wml_allowed_types)
    expect("wml_boundary.forbidden_entity_resolution", "entity_resolution_runtime" in wml_forbidden)
    expect("wml_boundary.forbidden_fact_admission", "worldmodel_fact_admission" in wml_forbidden)
    expect("wml_boundary.forbidden_worldmodel_write", "worldmodel_write" in wml_forbidden)
    expect("wml_boundary.forbidden_memory_write", "memory_write" in wml_forbidden)
    expect("wml_boundary.forbidden_library_commit", "library_experience_commit" in wml_forbidden)
    expect("wml_boundary.forbidden_object_identity_commit", "object_identity_fact_commit" in wml_forbidden)
    expect("wml_boundary.forbidden_emotional_attachment_commit", "emotional_attachment_fact_commit" in wml_forbidden)
    expect("wml_boundary.forbidden_user_preference_commit", "user_preference_fact_commit" in wml_forbidden)
    expect("wml_boundary.forbidden_temp_facility_promotion", "temporary_facility_long_term_promotion" in wml_forbidden)
    expect("wml_boundary.forbidden_route_experience_commit", "route_experience_commit" in wml_forbidden)
    expect("wml_boundary.future_memory_governance", "Memory Governance" in wml_future)
    expect("wml_boundary.future_entity_resolution", "Entity Resolution" in wml_future)
    expect("wml_boundary.future_library_governance", "Library Experience Governance" in wml_future)
    expect("wml_boundary.entity_resolution_deferred", wml_boundary.get("entity_resolution_deferred") is True)
    expect("wml_boundary.fact_admission_deferred", wml_boundary.get("fact_admission_deferred") is True)
    expect("wml_boundary.memory_consolidation_deferred", wml_boundary.get("memory_consolidation_deferred") is True)
    expect("wml_boundary.library_experience_governance_deferred", wml_boundary.get("library_experience_governance_deferred") is True)
    expect("wml_boundary.fact_write_allowed", wml_boundary.get("fact_write_allowed") is False)
    expect("wml_boundary.memory_write_allowed", wml_boundary.get("memory_write_allowed") is False)
    expect("wml_boundary.worldmodel_write_allowed", wml_boundary.get("worldmodel_write_allowed") is False)
    expect("wml_boundary.library_write_allowed", wml_boundary.get("library_write_allowed") is False)
    expect("wml_boundary.entity_fusion_runtime_allowed", wml_boundary.get("entity_fusion_runtime_allowed") is False)
    expect("wml_boundary.fact_admission_runtime_allowed", wml_boundary.get("fact_admission_runtime_allowed") is False)
    expect("wml_boundary.handoff_candidate_not_fact", wml_boundary.get("handoff_candidate_not_fact") is True)
    expect("wml_boundary.placeholder_not_runtime", wml_boundary.get("placeholder_not_runtime") is True)
    expect("wml_boundary.risks_count_ge_9", len(wml_risks) >= 9, len(wml_risks))

    # Placeholder plan checks
    placeholder_rows = wml_placeholder.get("handoff_candidates", [])
    placeholder_fields = wml_placeholder.get("required_fields_for_future_use", [])
    placeholder_non_claims = wml_placeholder.get("non_claims", [])
    expect("wml_placeholder.scope", wml_placeholder.get("placeholder_scope") == "worldmodel_memory_library_placeholder_plan")
    expect("wml_placeholder.count_ge_4", len(placeholder_rows) >= 4, len(placeholder_rows))
    expect(
        "wml_placeholder.worldmodel_handoff_candidate",
        any(row.get("candidate_type") == "WorldModelHandoffCandidate" and row.get("future_owner") == "WorldModel Governance" for row in placeholder_rows),
    )
    expect(
        "wml_placeholder.memory_handoff_candidate",
        any(row.get("candidate_type") == "MemoryHandoffCandidate" and row.get("future_owner") == "Memory Governance" for row in placeholder_rows),
    )
    expect(
        "wml_placeholder.library_handoff_placeholder",
        any(row.get("candidate_type") == "LibraryHandoffPlaceholder" and row.get("future_owner") == "Library System" for row in placeholder_rows),
    )
    expect(
        "wml_placeholder.experience_candidate_placeholder",
        any(
            row.get("candidate_type") == "ExperienceCandidatePlaceholder"
            and row.get("future_owner") == "Library / Experience Reuse Governance"
            for row in placeholder_rows
        ),
    )
    expect("wml_placeholder.required_source_chain", "source_chain" in placeholder_fields)
    expect("wml_placeholder.required_timestamp", "timestamp" in placeholder_fields)
    expect("wml_placeholder.required_location_context_ref", "location_context_ref" in placeholder_fields)
    expect("wml_placeholder.required_pose_context_ref", "pose_or_view_context_ref" in placeholder_fields)
    expect("wml_placeholder.required_task_context_ref", "task_context_ref" in placeholder_fields)
    expect("wml_placeholder.required_freshness", "freshness_status" in placeholder_fields)
    expect("wml_placeholder.required_ttl", "ttl_policy_ref" in placeholder_fields)
    expect("wml_placeholder.required_confidence", "confidence" in placeholder_fields)
    expect("wml_placeholder.required_uncertainty", "uncertainty" in placeholder_fields)
    expect("wml_placeholder.required_privacy_tags", "privacy_tags" in placeholder_fields)
    expect("wml_placeholder.required_conflict_refs", "conflict_refs" in placeholder_fields)
    expect("wml_placeholder.required_user_feedback_refs", "user_feedback_refs" in placeholder_fields)
    expect("wml_placeholder.required_ocr_refs", "ocr_refs" in placeholder_fields)
    expect("wml_placeholder.required_visual_refs", "visual_refs" in placeholder_fields)
    expect("wml_placeholder.required_map_refs", "map_refs" in placeholder_fields)
    expect("wml_placeholder.required_memory_refs", "memory_refs" in placeholder_fields)
    expect("wml_placeholder.non_claim_handoff_not_fact", "handoff_candidate_is_not_fact" in placeholder_non_claims)
    expect("wml_placeholder.non_claim_placeholder_not_runtime", "placeholder_is_not_runtime" in placeholder_non_claims)
    expect(
        "wml_placeholder.non_claim_identity_not_fact",
        "object_identity_candidate_is_not_identity_fact" in placeholder_non_claims,
    )
    expect(
        "wml_placeholder.non_claim_emotional_not_fact",
        "emotional_attachment_candidate_is_not_emotional_fact" in placeholder_non_claims,
    )
    expect("wml_placeholder.non_claim_temp_not_poi", "temporary_facility_candidate_is_not_fixed_poi" in placeholder_non_claims)
    expect(
        "wml_placeholder.non_claim_route_not_commit",
        "route_experience_candidate_is_not_route_memory_commit" in placeholder_non_claims,
    )

    # Rejected patterns checks
    rejected_patterns = [row.get("pattern") for row in rejected.get("patterns", [])]
    expect("rejected.3x3_grid", "3x3_grid_as_mainline" in rejected_patterns)
    expect("rejected.full_scene_tracking", "full_scene_tracking" in rejected_patterns)
    expect("rejected.full_frame_ocr", "full_frame_ocr" in rejected_patterns)
    expect("rejected.map_memory_authority", "map_or_memory_as_action_authority" in rejected_patterns)
    expect("rejected.direct_write", "direct_worldmodel_memory_fact_write" in rejected_patterns)
    expect("rejected.private_budget", "visual_private_resource_budget" in rejected_patterns)
    expect("rejected.private_privacy", "visual_private_privacy_filtering" in rejected_patterns)
    expect("rejected.parallel_stc", "new_parallel_stc_ttl_source_chain" in rejected_patterns)
    expect("rejected.parallel_evidence", "new_parallel_evidence_pack" in rejected_patterns)
    expect("rejected.parallel_task_state", "new_parallel_task_state" in rejected_patterns)
    expect("rejected.parallel_speech", "new_parallel_speech_gate_or_vop" in rejected_patterns)
    expect("rejected.parallel_runtime_framework", "new_parallel_runtime_trial_or_closure_framework" in rejected_patterns)
    expect("rejected.crossing_as_normal_task", "crossing_as_normal_navigation_visual_subtask" in rejected_patterns)
    expect("rejected.crowd_follow_as_direct_instruction", "crowd_flow_as_direct_navigation_instruction" in rejected_patterns)

    # Summary boundary checks
    expect("summary.no_runtime_executed", summary.get("no_runtime_executed") is True)
    expect("summary.no_new_capability_implemented", summary.get("no_new_capability_implemented") is True)
    expect("summary.camera_invoked", summary.get("camera_invoked") is False)
    expect("summary.map_api_invoked", summary.get("map_api_invoked") is False)
    expect("summary.ocr_provider_invoked", summary.get("ocr_provider_invoked") is False)
    expect("summary.tracking_runtime_invoked", summary.get("tracking_runtime_invoked") is False)
    expect("summary.optical_flow_runtime_invoked", summary.get("optical_flow_runtime_invoked") is False)
    expect("summary.world_model_written", summary.get("world_model_written") is False)
    expect("summary.memory_written", summary.get("memory_written") is False)
    expect("summary.fact_written", summary.get("fact_written") is False)
    expect("summary.scene_delta_generated", summary.get("scene_delta_generated") is False)
    expect("summary.task_state_committed_now", summary.get("task_state_committed_now") is False)
    expect("summary.navigation_action_triggered", summary.get("navigation_action_triggered") is False)
    expect("summary.full_scene_tracking_allowed", summary.get("full_scene_tracking_allowed") is False)
    expect("summary.full_frame_ocr_allowed", summary.get("full_frame_ocr_allowed") is False)
    expect("summary.worldmodel_write_allowed", summary.get("worldmodel_write_allowed") is False)
    expect("summary.memory_write_allowed", summary.get("memory_write_allowed") is False)
    expect("summary.library_write_allowed", summary.get("library_write_allowed") is False)
    expect("summary.fact_write_allowed", summary.get("fact_write_allowed") is False)
    expect("summary.worldmodel_memory_library_boundary_deferred", summary.get("worldmodel_memory_library_boundary_deferred") is True)
    expect("summary.entity_resolution_deferred", summary.get("entity_resolution_deferred") is True)
    expect("summary.fact_admission_deferred", summary.get("fact_admission_deferred") is True)
    expect("summary.memory_consolidation_deferred", summary.get("memory_consolidation_deferred") is True)
    expect("summary.library_experience_governance_deferred", summary.get("library_experience_governance_deferred") is True)
    expect("summary.worldmodel_handoff_candidate_allowed", summary.get("worldmodel_handoff_candidate_allowed") is True)
    expect("summary.memory_handoff_candidate_allowed", summary.get("memory_handoff_candidate_allowed") is True)
    expect("summary.library_handoff_placeholder_allowed", summary.get("library_handoff_placeholder_allowed") is True)
    expect("summary.entity_fusion_runtime_allowed", summary.get("entity_fusion_runtime_allowed") is False)
    expect("summary.fact_admission_runtime_allowed", summary.get("fact_admission_runtime_allowed") is False)
    expect("summary.handoff_candidate_not_fact", summary.get("handoff_candidate_not_fact") is True)
    expect("summary.placeholder_not_runtime", summary.get("placeholder_not_runtime") is True)
    expect("summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("summary.violations_empty", summary.get("violations") == [])

    # Boundary report checks
    for payload_name, payload in (("no_runtime", no_runtime), ("no_write", no_write)):
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])
        expect(f"{payload_name}.camera_invoked", payload.get("camera_invoked") is False)
        expect(f"{payload_name}.map_api_invoked", payload.get("map_api_invoked") is False)
        expect(f"{payload_name}.ocr_provider_invoked", payload.get("ocr_provider_invoked") is False)
        expect(f"{payload_name}.tracking_runtime_invoked", payload.get("tracking_runtime_invoked") is False)
        expect(f"{payload_name}.optical_flow_runtime_invoked", payload.get("optical_flow_runtime_invoked") is False)
        expect(f"{payload_name}.world_model_written", payload.get("world_model_written") is False)
        expect(f"{payload_name}.memory_written", payload.get("memory_written") is False)
        expect(f"{payload_name}.library_written", payload.get("library_written") is False)
        expect(f"{payload_name}.fact_written", payload.get("fact_written") is False)
        expect(f"{payload_name}.scene_delta_generated", payload.get("scene_delta_generated") is False)
        expect(f"{payload_name}.task_state_committed_now", payload.get("task_state_committed_now") is False)
        expect(f"{payload_name}.navigation_action_triggered", payload.get("navigation_action_triggered") is False)
        expect(f"{payload_name}.full_scene_tracking_allowed", payload.get("full_scene_tracking_allowed") is False)
        expect(f"{payload_name}.full_frame_ocr_allowed", payload.get("full_frame_ocr_allowed") is False)
        expect(f"{payload_name}.library_write_allowed", payload.get("library_write_allowed") is False)
        expect(f"{payload_name}.entity_fusion_runtime_allowed", payload.get("entity_fusion_runtime_allowed") is False)
        expect(f"{payload_name}.fact_admission_runtime_allowed", payload.get("fact_admission_runtime_allowed") is False)
        expect(f"{payload_name}.handoff_candidate_not_fact", payload.get("handoff_candidate_not_fact") is True)
        expect(f"{payload_name}.placeholder_not_runtime", payload.get("placeholder_not_runtime") is True)

    # Readiness and final decision checks
    expect("readiness.go", readiness.get("go") is True)
    expect("readiness.next_phase_fixed", readiness.get("next_phase_fixed") == NEXT_PHASE)
    readiness_hard_checks = readiness.get("hard_checks") or {}
    expect("readiness.entity_resolution_deferred", readiness_hard_checks.get("entity_resolution_deferred") is True)
    expect("readiness.fact_admission_deferred", readiness_hard_checks.get("fact_admission_deferred") is True)
    expect("readiness.memory_consolidation_deferred", readiness_hard_checks.get("memory_consolidation_deferred") is True)
    expect(
        "readiness.library_experience_governance_deferred",
        readiness_hard_checks.get("library_experience_governance_deferred") is True,
    )
    expect("readiness.worldmodel_write_allowed", readiness_hard_checks.get("worldmodel_write_allowed") is False)
    expect("readiness.memory_write_allowed", readiness_hard_checks.get("memory_write_allowed") is False)
    expect("readiness.library_write_allowed", readiness_hard_checks.get("library_write_allowed") is False)
    expect("readiness.entity_fusion_runtime_allowed", readiness_hard_checks.get("entity_fusion_runtime_allowed") is False)
    expect("readiness.fact_admission_runtime_allowed", readiness_hard_checks.get("fact_admission_runtime_allowed") is False)
    expect("readiness.handoff_candidate_not_fact", readiness_hard_checks.get("handoff_candidate_not_fact") is True)
    expect("readiness.placeholder_not_runtime", readiness_hard_checks.get("placeholder_not_runtime") is True)
    expect("readiness.final_assessment_next", next_phase.get("recommended_next_phase") == NEXT_PHASE)
    expect("readiness.final_decision_summary", summary.get("final_decision") == FINAL_DECISION)
    expect("readiness.final_decision_next_phase_file", next_phase.get("final_decision") == FINAL_DECISION)
    expect("readiness.recommended_next_phase_summary", summary.get("recommended_next_phase") == NEXT_PHASE)
    expect("readiness.recommended_next_phase_file", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "RETURN_TO_VISION_MAINLINE_PLANNING_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else "Phase-Return-To-Vision-Mainline-Planning-v1-001",
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
