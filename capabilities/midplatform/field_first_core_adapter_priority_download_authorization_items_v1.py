# -*- coding: utf-8 -*-
"""Field-First Adapter Priority and Download Authorization Planning items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

PLANNING_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "adapter_priority_planning_principles_v1",
    "rules": (
        "adapter_before_download",
        "lightweight_chain_before_heavy_models",
        "observation_candidate_before_field_simulation",
        "download_authorization_not_auto_opened",
        "self_developed_skeleton_first",
    ),
}

DOWNLOAD_AUTH_STATUS_OPTIONS: Tuple[str, ...] = (
    "keep_false", "eligible_for_owner_review", "conditional_future_review",
    "reference_only_no_download", "deferred_no_download", "no_download_required",
)

P0_SELF_DEVELOPED: Tuple[Dict[str, Any], ...] = (
    {"priority": "P0", "adapter_id": "luna_frontend_sensing_adapter", "model_project_id": "Luna_frontend_sensing_adapter", "purpose": "unify_frontend_source_input", "outputs": ("ObservationCandidate",), "download_auth": "no_download_required", "reason": "all_model_intake_entry"},
    {"priority": "P0", "adapter_id": "luna_ecs_dataclass_skeleton", "model_project_id": "Luna_dataclass_ECS_skeleton", "purpose": "field_model_ecs_layer", "outputs": ("WorldEntityCandidate", "EntityComponentCandidate", "AttributeStateCandidate"), "download_auth": "no_download_required", "reason": "entity_attribute_foundation"},
    {"priority": "P0", "adapter_id": "luna_event_graph_skeleton", "model_project_id": "Luna_lightweight_event_graph_skeleton", "purpose": "semantic_event_graph_layer", "outputs": ("SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate"), "download_auth": "no_download_required", "reason": "event_semantics_phase1"},
    {"priority": "P0", "adapter_id": "luna_geometry_trajectory_simulator", "model_project_id": "Luna_geometry_simulator", "purpose": "field_simulation", "outputs": ("FieldSimulationResultCandidate", "RiskProjectionCandidate"), "download_auth": "no_download_required", "reason": "simulation_not_external_llm"},
    {"priority": "P0", "adapter_id": "luna_drive_layer_skeleton", "model_project_id": "Luna_drive_layer_self_work", "purpose": "survival_task_reflection_drive", "outputs": ("PerceptionRequestCandidate", "TaskControlCandidate"), "download_auth": "no_download_required", "reason": "active_perception_loop"},
)

P1_NEAR_TERM: Tuple[Dict[str, Any], ...] = (
    {"priority": "P1", "adapter_id": "paddleocr_adapter", "model_project_id": "PaddleOCR", "purpose": "ocr_text_perception", "outputs": ("TextObservationCandidate", "TextRegionCandidate", "ReadabilityCandidate"), "download_auth": "eligible_for_owner_review", "reason": "det_rec_region_confidence_confirmed"},
    {"priority": "P1", "adapter_id": "rapidocr_adapter", "model_project_id": "RapidOCR", "purpose": "lightweight_ocr", "outputs": ("TextObservationCandidate",), "download_auth": "eligible_for_owner_review", "reason": "paddleocr_backup_path"},
    {"priority": "P1", "adapter_id": "bytetrack_adapter", "model_project_id": "ByteTrack", "purpose": "visual_track_continuity", "outputs": ("TrackObservationCandidate",), "download_auth": "eligible_for_owner_review", "reason": "field_continuity_track_id"},
    {"priority": "P1", "adapter_id": "yolo_lightweight_detector_adapter", "model_project_id": "YOLO_lightweight", "purpose": "lightweight_object_detection", "outputs": ("ObjectObservationCandidate",), "download_auth": "eligible_for_owner_review", "reason": "phase1_basic_object_candidate_after_variant_selection"},
    {"priority": "P1", "adapter_id": "whisper_adapter", "model_project_id": "Whisper", "purpose": "asr", "outputs": ("SpeechObservationCandidate", "IntentHintCandidate"), "download_auth": "eligible_for_owner_review", "reason": "speech_input_interrupt"},
    {"priority": "P1", "adapter_id": "faster_whisper_adapter", "model_project_id": "faster_whisper", "purpose": "edge_asr", "outputs": ("SpeechObservationCandidate",), "download_auth": "eligible_for_owner_review", "reason": "edge_asr_candidate"},
    {"priority": "P1", "adapter_id": "rule_llm_hybrid_reasoning_adapter", "model_project_id": "rule_LLM_hybrid", "purpose": "midplatform_field_reasoning", "outputs": ("MidplatformReasoningCandidate",), "download_auth": "keep_false", "reason": "model_selection_not_complete"},
)

P2_FUTURE: Tuple[Dict[str, Any], ...] = (
    {"priority": "P2", "adapter_id": "grounded_sam2_adapter", "model_project_id": "Grounded_SAM2", "purpose": "open_vocab_grounding_segmentation_tracking", "outputs": ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate"), "download_auth": "conditional_future_review", "reason": "high_hardware_risk"},
    {"priority": "P2", "adapter_id": "sam2_adapter", "model_project_id": "SAM2", "purpose": "segmentation_mask_tracking", "outputs": ("MaskObservationCandidate",), "download_auth": "conditional_future_review", "reason": "needs_grounding_companion"},
    {"priority": "P2", "adapter_id": "sensevoice_adapter", "model_project_id": "SenseVoice", "purpose": "asr_speech_understanding", "outputs": ("SpeechObservationCandidate", "IntentHintCandidate"), "download_auth": "conditional_future_review", "reason": "intent_hint_schema_pending"},
    {"priority": "P2", "adapter_id": "pyannote_audio_adapter", "model_project_id": "pyannote_audio", "purpose": "speaker_diarization", "outputs": ("SpeakerObservationCandidate",), "download_auth": "conditional_future_review", "reason": "privacy_realtime_cost"},
    {"priority": "P2", "adapter_id": "groundingdino_adapter", "model_project_id": "GroundingDINO", "purpose": "open_vocab_detection", "outputs": ("ObjectObservationCandidate",), "download_auth": "conditional_future_review", "reason": "grounded_sam_component_not_batch1"},
    {"priority": "P2", "adapter_id": "structured_llm_local_adapter", "model_project_id": "local_small_model", "purpose": "structured_reasoning", "outputs": ("MidplatformReasoningCandidate",), "download_auth": "keep_false", "reason": "model_not_selected"},
    {"priority": "P2", "adapter_id": "networkx_event_graph_reference", "model_project_id": "NetworkX", "purpose": "optional_graph_reference", "outputs": ("SemanticEventCandidate",), "download_auth": "no_download_required", "reason": "python_lib_not_weight"},
)

P3_REFERENCE_DEFERRED: Tuple[Dict[str, Any], ...] = (
    {"priority": "P3", "model_project_id": "Kimera", "download_auth": "reference_only_no_download", "reason": "slam_structure_reference"},
    {"priority": "P3", "model_project_id": "Hydra", "download_auth": "reference_only_no_download", "reason": "scene_graph_structure_reference"},
    {"priority": "P3", "model_project_id": "HOV_SG", "download_auth": "reference_only_no_download", "reason": "open_vocab_3d_sg_reference"},
    {"priority": "P3", "model_project_id": "Open3DSG", "download_auth": "reference_only_no_download", "reason": "3d_sg_reference"},
    {"priority": "P3", "model_project_id": "Esper", "download_auth": "reference_only_no_download", "reason": "ecs_reference_dataclass_first"},
    {"priority": "P3", "model_project_id": "Flecs", "download_auth": "reference_only_no_download", "reason": "ecs_performance_reference"},
    {"priority": "P3", "model_project_id": "RDFLib", "download_auth": "reference_only_no_download", "reason": "kg_standard_reference"},
    {"priority": "P3", "model_project_id": "Neo4j", "download_auth": "deferred_no_download", "reason": "database_too_heavy"},
    {"priority": "P3", "model_project_id": "Florence2", "download_auth": "deferred_no_download", "reason": "runtime_cost"},
    {"priority": "P3", "model_project_id": "DINO_X", "download_auth": "deferred_no_download", "reason": "missing_outputs"},
    {"priority": "P3", "model_project_id": "RTG_SLAM_placeholder", "download_auth": "deferred_no_download", "reason": "project_not_selected"},
    {"priority": "P3", "model_project_id": "Splatt3R_SLAM_placeholder", "download_auth": "deferred_no_download", "reason": "project_not_selected"},
    {"priority": "P3", "model_project_id": "VAD_placeholder", "download_auth": "deferred_no_download", "reason": "project_not_selected"},
    {"priority": "P3", "model_project_id": "voiceprint_placeholder", "download_auth": "deferred_no_download", "reason": "governance_risk"},
    {"priority": "P3", "model_project_id": "cloud_LLM", "download_auth": "conditional_future_review", "reason": "governance_latency_risk"},
)

ADAPTER_BATCH_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "batch_id": "batch_a_self_developed_skeleton",
        "items": ("field_first_source_adapter_skeleton", "field_model_ecs_layer_skeleton", "field_model_event_graph_skeleton", "field_simulation_geometry_skeleton", "drive_layer_candidate_skeleton"),
        "requires_download": False,
        "goal": "field_first_main_chain_without_weights",
    },
    {
        "batch_id": "batch_b_lightweight_observation",
        "items": ("paddleocr_adapter_skeleton", "rapidocr_adapter_skeleton", "bytetrack_adapter_skeleton", "yolo_detector_adapter_skeleton", "whisper_adapter_skeleton"),
        "requires_download": False,
        "goal": "define_adapter_io_no_real_model_load",
    },
    {
        "batch_id": "batch_c_future_heavy",
        "items": ("grounded_sam2_adapter_skeleton", "sam2_adapter_skeleton", "sensevoice_adapter_skeleton", "pyannote_adapter_skeleton", "rule_llm_reasoning_adapter_skeleton"),
        "requires_download": False,
        "goal": "placeholder_only_no_download_no_run",
    },
)

SKELETON_BATCH_RECOMMENDATION: Tuple[str, ...] = (
    "batch_a_first_self_developed_no_weights",
    "batch_b_second_lightweight_observation_skeleton_only",
    "batch_c_third_future_placeholder_only",
)

RISK_CONTROL_RULES: Tuple[str, ...] = (
    "owner_review_required_before_any_download",
    "download_authorized_remains_false_until_owner_approval_phase",
    "no_heavy_slam_in_phase1_download_plan",
    "no_database_in_phase1_download_plan",
    "self_developed_skeleton_before_model_weights",
    "adapter_contract_before_weight_download",
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_download_execution",
    "eligible_for_owner_review_not_download_authorized",
    "conditional_future_review_not_near_term_download",
    "adapter_priority_not_model_selection",
    "planning_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Self-Developed-Skeleton-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Self-Developed Field-First Skeleton Implementation"

def _all_priority_items() -> Tuple[Dict[str, Any], ...]:
    return P0_SELF_DEVELOPED + P1_NEAR_TERM + P2_FUTURE
