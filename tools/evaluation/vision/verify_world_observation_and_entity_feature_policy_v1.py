#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify World Observation and Entity Feature Policy v1."""

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
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "world_observation_and_entity_feature_policy_v1_smoke_v0"
PHASE_ID = "Phase-World-Observation-and-Entity-Feature-Policy-v1-001"
FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
NEXT_PHASE = "Phase-Selective-Tracking-Adapter-Policy-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify World Observation and Entity Feature Policy v1")
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
    layer_policy = _load_json(output_root / "world_observation_layer_policy.json")
    observation_schema = _load_json(output_root / "world_observation_candidate_schema.json")
    value_filtering = _load_json(output_root / "world_observation_value_filtering_policy.json")
    entity_feature = _load_json(output_root / "world_entity_feature_candidate_schema.json")
    object_identity = _load_json(output_root / "object_identity_candidate_schema.json")
    temporary_facility = _load_json(output_root / "temporary_mobile_social_facility_policy.json")
    emotional_attachment = _load_json(output_root / "emotional_attachment_candidate_policy.json")
    wml_placeholder = _load_json(output_root / "worldmodel_memory_library_placeholder_policy.json")
    feedback = _load_json(output_root / "world_observation_feedback_policy.json")
    scenario_matrix = _load_json(output_root / "world_observation_entity_feature_scenario_matrix.json")
    boundary_matrix = _load_json(output_root / "world_observation_boundary_matrix.json")
    governance_debt = _load_json(output_root / "governance_debt_register.json")
    next_phase = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write = _load_json(output_root / "no_write_boundary_report.json")

    # Input checks
    expect("input.task_aware_visual_focus_input_loaded", summary.get("task_aware_visual_focus_input_loaded") is True)
    expect("input.midplatform_perception_orchestration_input_loaded", summary.get("midplatform_perception_orchestration_input_loaded") is True)
    expect("input.return_to_vision_planning_input_loaded", summary.get("return_to_vision_planning_input_loaded") is True)
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)
    expect("input.root_matrix_rows_present", isinstance(input_root_matrix.get("rows"), list))
    expect("input.root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_root_matrix.get("rows", [])))
    for intake_id in (
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "preplan_input",
        "ocr_final_closure",
        "minimal_runtime_integration_closure",
        "task_aware_visual_focus_doc",
        "midplatform_perception_orchestration_doc",
        "vision_planning_doc",
        "vision_preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ):
        expect(
            f"input.required.{intake_id}",
            any(row.get("intake_id") == intake_id and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
        )

    # Summary / readiness checks
    expect("summary.policy_scope", summary.get("policy_scope") == "world_observation_and_entity_feature_policy_only")
    expect("summary.world_observation_layer_policy_defined", summary.get("world_observation_layer_policy_defined") is True)
    expect("summary.world_observation_candidate_schema_defined", summary.get("world_observation_candidate_schema_defined") is True)
    expect("summary.world_observation_value_filtering_policy_defined", summary.get("world_observation_value_filtering_policy_defined") is True)
    expect("summary.world_entity_feature_candidate_schema_defined", summary.get("world_entity_feature_candidate_schema_defined") is True)
    expect("summary.object_identity_candidate_schema_defined", summary.get("object_identity_candidate_schema_defined") is True)
    expect("summary.temporary_mobile_social_facility_policy_defined", summary.get("temporary_mobile_social_facility_policy_defined") is True)
    expect("summary.emotional_attachment_candidate_policy_defined", summary.get("emotional_attachment_candidate_policy_defined") is True)
    expect("summary.worldmodel_memory_library_placeholder_policy_defined", summary.get("worldmodel_memory_library_placeholder_policy_defined") is True)
    expect("summary.world_observation_feedback_policy_defined", summary.get("world_observation_feedback_policy_defined") is True)
    expect("summary.scenario_matrix_generated", summary.get("scenario_matrix_generated") is True)
    expect("summary.scenario_count", summary.get("scenario_count", 0) >= 8, summary.get("scenario_count"))
    expect("summary.full_background_recording_allowed", summary.get("full_background_recording_allowed") is False)
    expect("summary.world_observation_runtime_enabled", summary.get("world_observation_runtime_enabled") is False)
    expect("summary.worldmodel_handoff_candidate_allowed", summary.get("worldmodel_handoff_candidate_allowed") is True)
    expect("summary.memory_handoff_candidate_allowed", summary.get("memory_handoff_candidate_allowed") is True)
    expect("summary.library_handoff_placeholder_allowed", summary.get("library_handoff_placeholder_allowed") is True)
    expect("summary.object_identity_fact_allowed", summary.get("object_identity_fact_allowed") is False)
    expect("summary.emotional_attachment_fact_allowed", summary.get("emotional_attachment_fact_allowed") is False)
    expect("summary.fixed_poi_commit_allowed", summary.get("fixed_poi_commit_allowed") is False)

    # Layer policy checks
    expect("layer_policy.scope", layer_policy.get("scope") == "background_low_frequency_candidate_layer")
    expect("layer_policy.background_low_frequency_only", layer_policy.get("background_low_frequency_only") is True)
    expect("layer_policy.not_real_time_action_path", layer_policy.get("not_real_time_action_path") is True)
    expect("layer_policy.not_navigation_authority", layer_policy.get("not_navigation_authority") is True)
    expect("layer_policy.not_speech_output_source", layer_policy.get("not_speech_output_source") is True)
    expect("layer_policy.not_worldmodel_writer", layer_policy.get("not_worldmodel_writer") is True)
    expect("layer_policy.not_memory_writer", layer_policy.get("not_memory_writer") is True)
    expect("layer_policy.not_library_writer", layer_policy.get("not_library_writer") is True)
    expect("layer_policy.resource_budget_controlled_by_midplatform", layer_policy.get("resource_budget_controlled_by_midplatform") is True)
    expect("layer_policy.privacy_filtering_controlled_by_midplatform", layer_policy.get("privacy_filtering_controlled_by_midplatform") is True)
    expect("layer_policy.full_background_recording_allowed", layer_policy.get("full_background_recording_allowed") is False)
    expect("layer_policy.world_observation_runtime_enabled", layer_policy.get("world_observation_runtime_enabled") is False)
    for target in (
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
    ):
        expect(f"layer_policy.allowed_target.{target}", target in layer_policy.get("allowed_observation_targets", []))
    for target in (
        "full_background_recording",
        "unbounded_all_person_logging",
        "unbounded_all_vehicle_logging",
        "privacy_sensitive_low_value_background_capture",
        "navigation_action_authority",
        "worldmodel_write",
        "memory_write",
        "library_write",
    ):
        expect(f"layer_policy.forbidden_target.{target}", target in layer_policy.get("forbidden_observation_targets", []))

    # WorldObservationCandidate checks
    obs_fields = [item.get("name") for item in observation_schema.get("fields", [])]
    expect("world_observation.object_name", observation_schema.get("object_name") == "WorldObservationCandidate")
    expect("world_observation.field_count_match", observation_schema.get("field_count") == len(observation_schema.get("fields", [])))
    for field_name in (
        "world_observation_id",
        "source_visual_focus_slot_id",
        "source_scene_sketch_id",
        "source_visual_observation_ref",
        "observation_type",
        "observed_entity_type",
        "location_context_ref",
        "pose_or_view_context_ref",
        "task_context_ref",
        "time_window_ref",
        "freshness_status",
        "ttl_policy_ref",
        "confidence",
        "uncertainty",
        "privacy_tags",
        "value_score_ref",
        "conflict_refs",
        "visual_refs",
        "ocr_refs",
        "map_refs",
        "memory_refs",
        "current_action_allowed",
        "fact_status",
        "write_allowed",
        "source_chain",
    ):
        expect(f"world_observation.field.{field_name}", field_name in obs_fields)
    for obs_type in (
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
    ):
        expect(f"world_observation.type.{obs_type}", obs_type in observation_schema.get("observation_types", []))
    expect("world_observation.current_action_allowed", observation_schema.get("current_action_allowed") is False)
    expect("world_observation.not_fact", observation_schema.get("fact_status") == "not_fact")
    expect("world_observation.write_allowed", observation_schema.get("write_allowed") is False)
    expect("world_observation.non_claims_count", len(observation_schema.get("non_claims", [])) >= 4)

    # Value filtering checks
    expect("value_filtering.full_background_recording_allowed", value_filtering.get("full_background_recording_allowed") is False)
    high_value_candidates = [
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
    for candidate in high_value_candidates:
        expect(f"value_filtering.high_value.{candidate}", candidate in value_filtering.get("high_value_candidates", []))
    low_value_candidates = [
        "unrelated_background_pedestrian",
        "one-off_low_confidence_noise",
        "unlocalized_transient_background_object",
        "distant_unrelated_vehicle",
        "repeated_low_value_frame",
        "high_privacy_low_task_value_content",
    ]
    for candidate in low_value_candidates:
        expect(f"value_filtering.low_value.{candidate}", candidate in value_filtering.get("low_value_candidates", []))
    for field_name in (
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
    ):
        expect(f"value_filtering.field.{field_name}", field_name in value_filtering.get("value_filter_fields", []))
    expect("value_filtering.principles_count", len(value_filtering.get("principles", [])) >= 4)

    # Entity feature checks
    entity_fields = [item.get("name") for item in entity_feature.get("fields", [])]
    expect("entity_feature.object_name", entity_feature.get("object_name") == "WorldEntityFeatureCandidate")
    expect("entity_feature.field_count_match", entity_feature.get("field_count") == len(entity_feature.get("fields", [])))
    for entity_type in (
        "ObjectCandidate",
        "PlaceCandidate",
        "EventCandidate",
        "RelationCandidate",
        "FacilityCandidate",
        "SocialFacilityCandidate",
        "TemporaryFacilityCandidate",
        "RouteStructureCandidate",
        "EnvironmentalPatternCandidate",
    ):
        expect(f"entity_feature.entity_type.{entity_type}", entity_type in entity_feature.get("entity_types", []))
    for layer_name in (
        "universal_attributes",
        "task_specific_attributes",
        "user_profiled_attributes",
        "social_context_attributes",
        "emotional_attributes",
        "operational_attributes",
        "uncertainty_and_conflict",
    ):
        expect(f"entity_feature.attribute_layer.{layer_name}", layer_name in entity_feature.get("attribute_layers", []))
        expect(f"entity_feature.field.{layer_name}", layer_name in entity_fields)
    for field_name in (
        "entity_feature_candidate_id",
        "source_world_observation_id",
        "entity_type",
        "entity_category_candidate",
        "name_candidate",
        "visual_signature_refs",
        "ocr_text_refs",
        "location_anchor_candidate",
        "privacy_tags",
        "requires_user_confirmation",
        "requires_review",
        "fact_status",
        "write_allowed",
        "source_chain",
    ):
        expect(f"entity_feature.field.{field_name}", field_name in entity_fields)
    expect("entity_feature.not_fact", entity_feature.get("fact_status") == "not_fact")
    expect("entity_feature.write_allowed", entity_feature.get("write_allowed") is False)
    expect("entity_feature.principles_count", len(entity_feature.get("principles", [])) >= 4)

    # Object identity checks
    object_identity_fields = [item.get("name") for item in object_identity.get("fields", [])]
    expect("object_identity.object_name", object_identity.get("object_name") == "ObjectIdentityCandidate")
    expect("object_identity.field_count_match", object_identity.get("field_count") == len(object_identity.get("fields", [])))
    for field_name in (
        "object_identity_candidate_id",
        "entity_feature_candidate_ref",
        "entity_type",
        "visual_signature_refs",
        "location_context_refs",
        "ocr_refs",
        "user_alias_refs",
        "historical_interaction_refs",
        "confidence",
        "conflict_refs",
        "requires_review",
        "requires_user_confirmation",
        "fact_status",
        "identity_fact_allowed",
        "source_chain",
    ):
        expect(f"object_identity.field.{field_name}", field_name in object_identity_fields)
    expect("object_identity.identity_fact_allowed", object_identity.get("identity_fact_allowed") is False)
    expect("object_identity.not_fact", object_identity.get("fact_status") == "not_fact")
    expect("object_identity.principles_count", len(object_identity.get("principles", [])) >= 4)

    # Temporary facility checks
    expect("temporary_facility.fixed_poi_commit_allowed", temporary_facility.get("fixed_poi_commit_allowed") is False)
    for candidate_type in (
        "TemporaryFacilityCandidate",
        "MobileFacilityCandidate",
        "TransientSceneStructureCandidate",
        "RecurringTemporaryPatternCandidate",
    ):
        expect(f"temporary_facility.candidate_type.{candidate_type}", candidate_type in temporary_facility.get("candidate_types", []))
    for covered in (
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
    ):
        expect(f"temporary_facility.covered.{covered}", covered in temporary_facility.get("covered_cases", []))
    for field_name in (
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
    ):
        expect(f"temporary_facility.field.{field_name}", field_name in temporary_facility.get("field_contract", []))
    expect("temporary_facility.principles_count", len(temporary_facility.get("principles", [])) >= 6)

    # Emotional attachment checks
    emotional_fields = [item.get("name") for item in emotional_attachment.get("fields", [])]
    expect("emotional_attachment.emotional_fact_allowed", emotional_attachment.get("emotional_fact_allowed") is False)
    for field_name in (
        "emotional_attachment_candidate_id",
        "related_entity_feature_candidate_id",
        "attachment_type_candidate",
        "evidence_refs",
        "user_feedback_refs",
        "historical_interaction_refs",
        "confidence",
        "sensitivity_level",
        "requires_user_confirmation",
        "emotional_fact_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"emotional_attachment.field.{field_name}", field_name in emotional_fields)
    expect("emotional_attachment.not_fact", emotional_attachment.get("fact_status") == "not_fact")
    expect("emotional_attachment.principles_count", len(emotional_attachment.get("principles", [])) >= 4)

    # Placeholder policy checks
    expect("wml_placeholder.entity_resolution_deferred", wml_placeholder.get("entity_resolution_deferred") is True)
    expect("wml_placeholder.fact_admission_deferred", wml_placeholder.get("fact_admission_deferred") is True)
    expect("wml_placeholder.memory_consolidation_deferred", wml_placeholder.get("memory_consolidation_deferred") is True)
    expect("wml_placeholder.library_experience_governance_deferred", wml_placeholder.get("library_experience_governance_deferred") is True)
    expect("wml_placeholder.worldmodel_write_allowed", wml_placeholder.get("worldmodel_write_allowed") is False)
    expect("wml_placeholder.memory_write_allowed", wml_placeholder.get("memory_write_allowed") is False)
    expect("wml_placeholder.library_write_allowed", wml_placeholder.get("library_write_allowed") is False)
    expect("wml_placeholder.handoff_candidate_not_fact", wml_placeholder.get("handoff_candidate_not_fact") is True)
    expect("wml_placeholder.placeholder_not_runtime", wml_placeholder.get("placeholder_not_runtime") is True)
    expect("wml_placeholder.worldmodel_handoff_candidate_allowed", wml_placeholder.get("worldmodel_handoff_candidate_allowed") is True)
    expect("wml_placeholder.memory_handoff_candidate_allowed", wml_placeholder.get("memory_handoff_candidate_allowed") is True)
    expect("wml_placeholder.library_handoff_placeholder_allowed", wml_placeholder.get("library_handoff_placeholder_allowed") is True)
    for allowed in (
        "WorldModelHandoffCandidate",
        "MemoryHandoffCandidate",
        "LibraryHandoffPlaceholder",
        "ExperienceCandidatePlaceholder",
    ):
        expect(f"wml_placeholder.allowed.{allowed}", allowed in wml_placeholder.get("allowed_now", []))
    for forbidden in (
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
    ):
        expect(f"wml_placeholder.forbidden.{forbidden}", forbidden in wml_placeholder.get("forbidden_now", []))
    expect("wml_placeholder.visual_focus_boundary_loaded", wml_placeholder.get("visual_focus_boundary_loaded") is True)
    expect("wml_placeholder.midplatform_boundary_loaded", wml_placeholder.get("midplatform_boundary_loaded") is True)
    expect("wml_placeholder.planning_boundary_loaded", wml_placeholder.get("planning_boundary_loaded") is True)
    expect("wml_placeholder.preplan_boundary_loaded", wml_placeholder.get("preplan_boundary_loaded") is True)

    # Feedback policy checks
    expect("feedback.speech_allowed_false_until_gate", feedback.get("speech_allowed_false_until_gate") is True)
    expect("feedback.action_allowed_false", feedback.get("action_allowed_false") is True)
    expect("feedback.fact_status_not_fact", feedback.get("fact_status_not_fact") is True)
    expect("feedback.requires_arbitration_or_review", feedback.get("requires_arbitration_or_review") is True)
    for output_name in (
        "WorldObservationFeedbackCandidate",
        "EntityFeatureFeedbackCandidate",
        "TemporaryFacilityFeedbackCandidate",
        "ObjectIdentityFeedbackCandidate",
        "WorldModelHandoffCandidate",
        "MemoryHandoffCandidate",
        "LibraryHandoffPlaceholder",
    ):
        expect(f"feedback.output.{output_name}", output_name in feedback.get("output_candidates", []))

    # Scenario checks
    scenarios = scenario_matrix.get("scenarios", [])
    scenario_ids = [row.get("scenario_id") for row in scenarios]
    expect("scenario_matrix.count_match", scenario_matrix.get("scenario_count") == len(scenarios))
    expect("scenario_matrix.count_ge_8", len(scenarios) >= 8, len(scenarios))
    for scenario_id in (
        "route_structure_observation",
        "shopfront_entity_feature_candidate",
        "home_familiar_object_candidate",
        "temporary_mobile_vendor_candidate",
        "recurring_temporary_pattern_candidate",
        "emotional_attachment_candidate_placeholder",
        "scene_change_candidate",
        "low_value_background_discard",
    ):
        expect(f"scenario_matrix.id.{scenario_id}", scenario_id in scenario_ids)
    shopfront = next((row for row in scenarios if row.get("scenario_id") == "shopfront_entity_feature_candidate"), {})
    home = next((row for row in scenarios if row.get("scenario_id") == "home_familiar_object_candidate"), {})
    temporary_vendor = next((row for row in scenarios if row.get("scenario_id") == "temporary_mobile_vendor_candidate"), {})
    recurring = next((row for row in scenarios if row.get("scenario_id") == "recurring_temporary_pattern_candidate"), {})
    emotional = next((row for row in scenarios if row.get("scenario_id") == "emotional_attachment_candidate_placeholder"), {})
    scene_change = next((row for row in scenarios if row.get("scenario_id") == "scene_change_candidate"), {})
    discard = next((row for row in scenarios if row.get("scenario_id") == "low_value_background_discard"), {})
    expect("scenario.shopfront_ocr_refs_placeholder", shopfront.get("ocr_refs_placeholder") is True)
    expect("scenario.shopfront_outputs_place", "PlaceCandidate" in shopfront.get("outputs", []))
    expect("scenario.shopfront_outputs_facility", "FacilityCandidate" in shopfront.get("outputs", []))
    expect("scenario.home_identity_placeholder", home.get("object_identity_candidate_placeholder") is True)
    expect("scenario.home_privacy_filtering_required", home.get("privacy_filtering_required") is True)
    expect("scenario.home_identity_fact_allowed", home.get("identity_fact_allowed") is False)
    expect("scenario.temporary_ttl_short", temporary_vendor.get("ttl_short") is True)
    expect("scenario.temporary_fixed_poi_commit_allowed", temporary_vendor.get("fixed_poi_commit_allowed") is False)
    expect("scenario.recurring_output", "RecurringTemporaryPatternCandidate" in recurring.get("outputs", []))
    expect("scenario.recurring_long_term_promotion_allowed", recurring.get("long_term_promotion_allowed") is False)
    expect("scenario.emotional_requires_user_confirmation", emotional.get("requires_user_confirmation") is True)
    expect("scenario.emotional_fact_allowed", emotional.get("emotional_fact_allowed") is False)
    expect("scenario.scene_change_auto_fact_correction_allowed", scene_change.get("auto_fact_correction_allowed") is False)
    expect("scenario.discard_allowed", discard.get("discard_allowed") is True)
    expect("scenario.enters_long_term_chain", discard.get("enters_long_term_chain") is False)
    for idx, row in enumerate(scenarios):
        expect(f"scenario.requires_runtime_now_{idx}", row.get("requires_runtime_now") is False)
        expect(f"scenario.fact_write_allowed_{idx}", row.get("fact_write_allowed") is False)

    # Boundary matrix checks
    expect("boundary.full_background_recording_allowed", boundary_matrix.get("full_background_recording_allowed") is False)
    expect("boundary.world_observation_runtime_enabled", boundary_matrix.get("world_observation_runtime_enabled") is False)
    expect("boundary.camera_runtime_allowed", boundary_matrix.get("camera_runtime_allowed") is False)
    expect("boundary.map_api_allowed", boundary_matrix.get("map_api_allowed") is False)
    expect("boundary.ocr_provider_runtime_allowed", boundary_matrix.get("ocr_provider_runtime_allowed") is False)
    expect("boundary.ocrrequest_submitted", boundary_matrix.get("ocrrequest_submitted") is False)
    expect("boundary.tracking_runtime_allowed", boundary_matrix.get("tracking_runtime_allowed") is False)
    expect("boundary.optical_flow_runtime_allowed", boundary_matrix.get("optical_flow_runtime_allowed") is False)
    expect("boundary.supervision_runtime_allowed", boundary_matrix.get("supervision_runtime_allowed") is False)
    expect("boundary.bytetrack_runtime_allowed", boundary_matrix.get("bytetrack_runtime_allowed") is False)
    expect("boundary.ocsort_runtime_allowed", boundary_matrix.get("ocsort_runtime_allowed") is False)
    expect("boundary.entity_resolution_runtime_allowed", boundary_matrix.get("entity_resolution_runtime_allowed") is False)
    expect("boundary.fact_admission_runtime_allowed", boundary_matrix.get("fact_admission_runtime_allowed") is False)
    expect("boundary.memory_consolidation_allowed", boundary_matrix.get("memory_consolidation_allowed") is False)
    expect("boundary.library_experience_commit_allowed", boundary_matrix.get("library_experience_commit_allowed") is False)
    expect("boundary.worldmodel_write_allowed", boundary_matrix.get("worldmodel_write_allowed") is False)
    expect("boundary.memory_write_allowed", boundary_matrix.get("memory_write_allowed") is False)
    expect("boundary.library_write_allowed", boundary_matrix.get("library_write_allowed") is False)
    expect("boundary.fact_write_allowed", boundary_matrix.get("fact_write_allowed") is False)
    expect("boundary.scene_delta_allowed", boundary_matrix.get("scene_delta_allowed") is False)
    expect("boundary.task_state_commit_allowed", boundary_matrix.get("task_state_commit_allowed") is False)
    expect("boundary.navigation_action_allowed", boundary_matrix.get("navigation_action_allowed") is False)
    expect("boundary.speech_gate_allowed", boundary_matrix.get("speech_gate_allowed") is False)
    expect("boundary.vop_allowed", boundary_matrix.get("vop_allowed") is False)

    # Governance debt checks
    debt_rows = governance_debt.get("debts", [])
    expect("governance_debt.generated", summary.get("governance_debt_register_generated") is True)
    expect("governance_debt.count_ge_8", len(debt_rows) >= 8, len(debt_rows))
    expect("governance_debt.future_midplatform_function_governance_required", governance_debt.get("future_midplatform_function_governance_required") is True)
    expect("governance_debt.no_duplicate_governance_module_allowed", governance_debt.get("no_duplicate_governance_module_allowed") is True)
    for topic in (
        "world observation value filtering complexity",
        "entity feature attribute layering complexity",
        "temporary facility recurrence governance complexity",
        "object identity placeholder governance complexity",
        "emotional attachment placeholder governance complexity",
        "worldmodel memory library placeholder governance complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(f"governance_debt.topic.{topic}", any(row.get("topic") == topic for row in debt_rows))
    for idx, row in enumerate(debt_rows):
        expect(f"governance_debt.future_owner_phase_{idx}", row.get("future_owner_phase") == "MidPlatform Function Governance / Consolidation")
        expect(f"governance_debt.reuse_or_consolidation_required_{idx}", row.get("reuse_or_consolidation_required") is True)
        expect(f"governance_debt.duplicate_governance_module_allowed_{idx}", row.get("duplicate_governance_module_allowed") is False)

    # Runtime / write checks
    for check_name, expected in (
        ("no_runtime_executed", True),
        ("no_new_runtime_enabled", True),
        ("world_observation_runtime_enabled", False),
        ("camera_invoked", False),
        ("map_api_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocrrequest_submitted", False),
        ("tracking_runtime_invoked", False),
        ("optical_flow_runtime_invoked", False),
        ("supervision_invoked", False),
        ("bytetrack_invoked", False),
        ("ocsort_invoked", False),
        ("entity_resolution_runtime_invoked", False),
        ("fact_admission_runtime_invoked", False),
        ("memory_consolidation_invoked", False),
        ("library_experience_commit_invoked", False),
        ("world_model_written", False),
        ("memory_written", False),
        ("library_written", False),
        ("fact_written", False),
        ("scene_delta_generated", False),
        ("task_state_committed_now", False),
        ("navigation_action_triggered", False),
        ("speech_gate_invoked", False),
        ("vop_invoked", False),
    ):
        expect(f"runtime.summary.{check_name}", summary.get(check_name) is expected)
    expect("runtime.summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("runtime.summary.violations_empty", summary.get("violations") == [])
    for payload_name, payload in (("no_runtime", no_runtime), ("no_write", no_write)):
        for check_name, expected in (
            ("no_runtime_executed", True),
            ("no_new_runtime_enabled", True),
            ("world_observation_runtime_enabled", False),
            ("camera_invoked", False),
            ("map_api_invoked", False),
            ("ocr_provider_invoked", False),
            ("ocrrequest_submitted", False),
            ("tracking_runtime_invoked", False),
            ("optical_flow_runtime_invoked", False),
            ("supervision_invoked", False),
            ("bytetrack_invoked", False),
            ("ocsort_invoked", False),
            ("entity_resolution_runtime_invoked", False),
            ("fact_admission_runtime_invoked", False),
            ("memory_consolidation_invoked", False),
            ("library_experience_commit_invoked", False),
            ("world_model_written", False),
            ("memory_written", False),
            ("library_written", False),
            ("fact_written", False),
            ("scene_delta_generated", False),
            ("task_state_committed_now", False),
            ("navigation_action_triggered", False),
            ("speech_gate_invoked", False),
            ("vop_invoked", False),
        ):
            expect(f"{payload_name}.{check_name}", payload.get(check_name) is expected)
        expect(f"{payload_name}.full_background_recording_allowed", payload.get("full_background_recording_allowed") is False)
        expect(f"{payload_name}.worldmodel_write_allowed", payload.get("worldmodel_write_allowed") is False)
        expect(f"{payload_name}.memory_write_allowed", payload.get("memory_write_allowed") is False)
        expect(f"{payload_name}.library_write_allowed", payload.get("library_write_allowed") is False)
        expect(f"{payload_name}.handoff_candidate_not_fact", payload.get("handoff_candidate_not_fact") is True)
        expect(f"{payload_name}.placeholder_not_runtime", payload.get("placeholder_not_runtime") is True)
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])

    # Final checks
    expect("final.summary_final_decision", summary.get("final_decision") == FINAL_DECISION)
    expect("final.summary_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    expect("final.next_phase_final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    expect("final.next_phase_recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
