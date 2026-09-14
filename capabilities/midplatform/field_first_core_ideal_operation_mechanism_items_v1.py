# -*- coding: utf-8 -*-
"""Field-First Ideal Operation Mechanism and Model Requirement Mapping items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

IDEAL_OPERATION_MECHANISM: Dict[str, Any] = {
    "mechanism_id": "ideal_operation_mechanism_v1",
    "principle": "define_ideal_operation_before_model_selection",
    "chain": (
        "frontend_sensing", "source_adapter", "source_basket",
        "observation_candidate_normalization", "field_model_construction",
        "field_state_continuity", "field_boundary_control", "field_simulation",
        "task_field_view_generation", "midplatform_field_reasoning",
        "drive_layer_evaluation", "perception_request_generation", "field_update_loop",
    ),
}

OPERATION_NODES: Tuple[Dict[str, Any], ...] = (
    {
        "operation_node_id": "frontend_sensing",
        "node_role": "source_intake_normalization_operator",
        "step_index": 1,
        "reference_models": ("camera", "vision_model", "tof_depth", "microphone_asr", "ocr", "imu", "location_map", "health_signal", "user_input"),
        "required_capabilities": ("timestamped_raw_perception", "source_confidence_score", "source_ref", "streaming_or_quasi_realtime", "failure_mode_exposure"),
        "expected_outputs": ("raw_perception_with_metadata",),
        "cannot_assume": ("field_construction", "reasoning", "final_judgment"),
        "luna_self_work": "adapter_metadata_normalization",
        "model_dependency": "high_for_sensing_low_for_core",
    },
    {
        "operation_node_id": "visual_object_segmentation_tracking",
        "node_role": "source_intake_normalization_operator",
        "reference_models": ("SAM2", "Grounded_SAM2", "Grounding_DINO", "Florence2", "DINO_X", "YOLO_series", "ByteTrack"),
        "operation_position": "frontend_sensing_source_adapter_visual_observation_candidate",
        "required_capabilities": (
            "object_detection", "open_vocabulary_detection", "segmentation_mask", "video_tracking",
            "track_id_continuity", "bbox_mask_label_confidence", "object_level_observation_candidate",
            "failure_mode_occlusion_lowlight_misdetect_miss",
        ),
        "expected_outputs": ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate", "VisualRelationHintCandidate"),
        "cannot_assume": ("direct_field_entity", "world_model_write", "task_complete", "action_suggestion"),
        "doc_review_focus": ("video_continuous_frames", "tracking_support", "open_vocab", "confidence_output", "edge_runtime", "license", "hardware"),
        "can_be_reference_only": True,
    },
    {
        "operation_node_id": "ocr_text_perception",
        "node_role": "source_intake_normalization_operator",
        "reference_models": ("PaddleOCR", "RapidOCR"),
        "operation_position": "frontend_sensing_ocr_adapter_text_observation_candidate",
        "required_capabilities": (
            "text_region_detection", "text_recognition", "text_confidence", "reading_order",
            "text_region_position", "multilingual", "readability_from_distance_angle_occlusion",
        ),
        "expected_outputs": ("TextObservationCandidate", "TextRegionCandidate", "ReadabilityCandidate"),
        "cannot_assume": ("reading_task_complete", "long_term_knowledge", "replace_task_field_view"),
        "doc_review_focus": ("det_rec_separation", "mobile_edge", "region_coords_confidence", "chinese_english", "direction_correction", "visual_entity_binding"),
        "can_be_reference_only": False,
    },
    {
        "operation_node_id": "audio_speech_speaker",
        "node_role": "source_intake_normalization_operator",
        "reference_models": ("SenseVoice", "Whisper", "faster_whisper", "pyannote_audio", "VAD", "voiceprint"),
        "operation_position": "frontend_sensing_speech_adapter_speech_observation_candidate",
        "required_capabilities": (
            "asr", "vad", "speaker_diarization", "speaker_identity_candidate",
            "interruption_detection", "intent_hint_extraction", "confidence_timestamp_segment",
        ),
        "expected_outputs": ("SpeechObservationCandidate", "SpeakerObservationCandidate", "IntentHintCandidate", "InterruptSignalCandidate"),
        "cannot_assume": ("authorization", "user_preference_fact", "task_execution", "long_term_emotion_fact"),
        "doc_review_focus": ("streaming", "speaker_separation", "time_segments", "confidence", "chinese", "offline", "noisy_environment"),
        "can_be_reference_only": False,
    },
    {
        "operation_node_id": "spatial_slam_dynamic_scene_graph",
        "node_role": "field_model_builder",
        "reference_models": ("Kimera", "Hydra", "HOV_SG", "Open3DSG", "RTG_SLAM", "Splatt3R_SLAM"),
        "operation_position": "observation_candidate_field_model_construction_dynamic_scene_graph_layer",
        "required_capabilities": (
            "pose_estimation", "spatial_mapping", "object_spatial_relation", "room_area_place_hierarchy",
            "scene_object_relation", "reachability_occlusion_blocking", "dynamic_update", "scene_graph_output_or_mappable",
        ),
        "expected_outputs": ("PoseObservationCandidate", "SpatialObservationCandidate", "SceneRelationCandidate", "SceneGraphReferenceCandidate", "AccessibilityRelationCandidate"),
        "cannot_assume": ("task_action_decision", "replace_midplatform_reasoning", "long_term_world_model_fact", "runtime_required_now"),
        "doc_review_focus": ("realtime", "dynamic_scene", "semantic_labels", "scene_graph_output", "rgbd_imu_lidar", "hardware_complexity", "first_person_device", "structure_reference_vs_dependency"),
        "can_be_reference_only": True,
    },
    {
        "operation_node_id": "ecs_entity_component",
        "node_role": "field_model_builder",
        "reference_models": ("Esper", "Flecs", "luna_dataclass_ecs_skeleton"),
        "operation_position": "field_model_construction_ecs_layer",
        "required_capabilities": (
            "entity_id", "component_attach_detach", "attribute_component_extension",
            "state_component_high_freq_update", "update_policy", "ttl",
            "attribute_tier_stable_semi_dynamic_relational_emotional", "entity_merge_split_lost_restored",
        ),
        "expected_outputs": ("WorldEntityCandidate", "EntityComponentCandidate", "AttributeStateCandidate", "EntityStateUpdateCandidate"),
        "cannot_assume": ("full_spatial_relation", "full_semantic_event", "long_term_kg", "replace_dynamic_scene_graph"),
        "doc_review_focus": ("lightweight", "python_usable", "serializable", "dynamic_components", "skeleton_first", "no_heavy_runtime"),
        "luna_self_work": "primary_dataclass_skeleton",
        "model_dependency": "low_reference_only",
    },
    {
        "operation_node_id": "lightweight_semantic_event_graph",
        "node_role": "field_model_builder",
        "reference_models": ("NetworkX", "RDFLib", "Neo4j", "luna_event_graph_skeleton"),
        "operation_position": "field_model_construction_semantic_event_graph_layer",
        "required_capabilities": (
            "event_node", "risk_zone", "rule_zone", "place_function", "task_affordance",
            "supports_conflicts_blocks_causes_or_enables", "event_entity_binding", "risk_task_binding", "scene_semantic_interpretation",
        ),
        "expected_outputs": ("SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate", "PlaceFunctionCandidate", "EventRelationCandidate"),
        "cannot_assume": ("full_long_term_kg", "emotional_graph", "replace_ecs", "replace_scene_graph", "direct_action"),
        "doc_review_focus": ("lightweight_graph", "property_graph", "relation_access", "offline", "json_serializable", "field_candidate_alignment"),
        "luna_self_work": "primary_lightweight_skeleton",
        "model_dependency": "low_networkx_reference",
    },
    {
        "operation_node_id": "field_boundary_continuity",
        "node_role": "field_state_continuity_manager_field_boundary_controller",
        "reference_capabilities": ("tracking", "slam_pose_continuity", "entity_state_history", "speed_radius_control", "ttl_state_machine"),
        "operation_position": "field_state_continuity_manager_field_boundary_controller",
        "required_capabilities": (
            "user_position_speed_input", "default_20m_field", "inner_working_forecast_zones",
            "speed_radius_refresh", "task_direction_weight", "risk_expand_field", "overload_shrink_view",
            "visible_occluded_lost_forgotten_state_machine",
        ),
        "expected_outputs": ("FieldBoundaryCandidate", "FieldSessionStateCandidate", "EntityContinuityCandidate", "FieldRefreshPolicyCandidate"),
        "luna_self_work": "primary_self_developed",
        "model_dependency": "low_external_support_only",
        "external_support": ("tracking", "pose", "speed", "spatial_relation"),
    },
    {
        "operation_node_id": "field_simulation",
        "node_role": "field_simulation_operator",
        "reference_capabilities": ("geometry_projection", "trajectory_prediction", "collision_path_intersection", "occlusion_update", "task_simulator", "rules_state_machine"),
        "operation_position": "field_model_field_simulation_operator",
        "required_capabilities": (
            "past_reconstruction", "current_state_estimation", "future_projection",
            "dynamic_trajectory", "path_intersection", "collision_risk", "visibility_occlusion_prediction",
            "accessibility_prediction", "task_specific_simulation",
        ),
        "task_branches": ("navigation", "find_object", "reading", "road_crossing", "obstacle_avoidance"),
        "expected_outputs": ("FieldSimulationResultCandidate", "TrajectoryProjectionCandidate", "RiskProjectionCandidate", "MissingInformationCandidate", "SafeWindowCandidate"),
        "cannot_assume": ("execute_action", "final_conclusion", "world_model_fact", "replace_field_reasoning"),
        "luna_self_work": "primary_rules_geometry_state_machine",
        "model_dependency": "low_input_only",
    },
    {
        "operation_node_id": "task_field_view",
        "node_role": "task_field_view_builder",
        "reference_capabilities": ("task_goal_parsing", "context_selection", "relevance_ranking", "field_view_summarization"),
        "operation_position": "field_model_field_simulation_task_field_view_candidate",
        "required_capabilities": (
            "extract_task_entities_relations_events", "summarize_risk_conflict_missing",
            "control_context_size", "structured_model_input",
        ),
        "expected_outputs": ("TaskFieldViewCandidate", "ReasoningContextCandidate"),
        "cannot_assume": ("final_reasoning", "modify_field", "replace_simulation"),
        "luna_self_work": "primary_self_developed",
        "model_dependency": "low_llm_compress_optional",
    },
    {
        "operation_node_id": "midplatform_reasoning",
        "node_role": "midplatform_field_reasoning_operator",
        "reference_models": ("local_small_model", "cloud_llm", "vlm_future", "rules_plus_llm_hybrid"),
        "operation_position": "task_field_view_field_simulation_midplatform_reasoning_candidate",
        "required_capabilities": (
            "understand_structured_field_view", "understand_simulation_result",
            "generate_candidate_conclusion", "mark_risk_gap_conflict", "output_reason_codes",
            "output_need_more_info", "output_perception_request_need",
            "output_route_risk_defer_block_candidate",
        ),
        "expected_outputs": ("MidplatformReasoningCandidate", "NeedMoreInfoCandidate", "RiskCandidate", "RouteCandidate", "PerceptionNeedCandidate", "TaskBlockedCandidate"),
        "cannot_assume": ("read_all_raw_sources", "direct_field_write", "execute_action", "create_facts", "replace_field_simulation"),
        "doc_review_focus": ("structured_io", "json_schema_function_calling", "local_runtime", "low_latency", "reason_codes", "non_execution_guard"),
        "can_be_reference_only": False,
    },
    {
        "operation_node_id": "drive_layer",
        "node_role": "survival_task_reflection_drive_controllers",
        "reference_capabilities": ("survival_drive", "task_drive", "reflection_drive"),
        "operation_position": "reasoning_candidate_drive_evaluation_perception_request",
        "required_capabilities": (
            "survival_interrupt_task", "task_maintain_goal", "reflection_correction_candidate",
            "active_perception_request", "no_world_model_fact_write",
        ),
        "expected_outputs": ("PerceptionRequestCandidate", "TaskControlCandidate", "ReflectionCorrectionCandidate", "SafetyInterruptCandidate"),
        "luna_self_work": "primary_self_developed",
        "model_dependency": "low_llm_reflection_optional",
    },
)

REQUIREMENT_MATRIX_FIELDS: Tuple[str, ...] = (
    "operation_node_id", "node_role", "required_capability", "acceptable_model_type",
    "expected_input", "expected_output_candidate", "latency_requirement", "update_frequency",
    "confidence_required", "traceability_required", "failure_modes_required",
    "edge_runtime_importance", "safety_critical", "can_be_reference_only", "must_have_now", "can_defer",
)

MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS: Tuple[str, ...] = (
    "project_name", "open_source_status", "license", "model_weights_available",
    "runtime_requirements", "input_supported", "output_supported", "confidence_output",
    "streaming_or_realtime", "tracking_or_temporal_support", "structured_output_support",
    "known_failure_modes", "hardware_requirement", "edge_deployment_possible",
    "adapter_feasibility", "maps_to_operation_node", "satisfies_required_capabilities",
    "missing_capabilities", "integration_risk", "recommended_status",
)

RECOMMENDED_STATUS_OPTIONS: Tuple[str, ...] = (
    "reference_only", "candidate_for_future_adapter", "candidate_for_near_term_adapter",
    "unsuitable_for_phase_1", "deferred_due_to_runtime_cost", "deferred_due_to_missing_outputs",
)

MODEL_ROOM_ALIGNMENT: Tuple[Dict[str, str], ...] = (
    {"operation_node_id": "frontend_sensing", "model_room_id": "source_intake_room", "alignment": "sensing_maps_to_source_room"},
    {"operation_node_id": "visual_object_segmentation_tracking", "model_room_id": "visual_perception_room", "alignment": "visual_node_maps_to_visual_room"},
    {"operation_node_id": "ocr_text_perception", "model_room_id": "ocr_text_perception_room", "alignment": "ocr_node_maps_to_ocr_room"},
    {"operation_node_id": "audio_speech_speaker", "model_room_id": "audio_speech_perception_room", "alignment": "speech_node_maps_to_audio_room"},
    {"operation_node_id": "spatial_slam_dynamic_scene_graph", "model_room_id": "spatial_slam_scene_graph_room", "alignment": "spatial_node_maps_to_slam_room"},
    {"operation_node_id": "ecs_entity_component", "model_room_id": "ecs_entity_component_room", "alignment": "ecs_node_maps_to_ecs_room"},
    {"operation_node_id": "lightweight_semantic_event_graph", "model_room_id": "semantic_event_graph_room", "alignment": "semantic_node_maps_to_semantic_room"},
    {"operation_node_id": "field_boundary_continuity", "model_room_id": "field_boundary_continuity_self_work", "alignment": "boundary_continuity_primarily_self_work"},
    {"operation_node_id": "field_simulation", "model_room_id": "field_simulation_room", "alignment": "simulation_node_maps_to_simulation_room"},
    {"operation_node_id": "task_field_view", "model_room_id": "task_field_view_self_work", "alignment": "task_view_primarily_self_work"},
    {"operation_node_id": "midplatform_reasoning", "model_room_id": "midplatform_reasoning_room", "alignment": "reasoning_node_maps_to_reasoning_room"},
    {"operation_node_id": "drive_layer", "model_room_id": "drive_layer_self_work", "alignment": "drive_primarily_self_work"},
)

SELF_WORK_VS_MODEL_DEPENDENCY: Tuple[Dict[str, Any], ...] = (
    {"domain": "source_adapter_normalization", "primary": "luna_self_work", "model_support": "frontend_sensing_models"},
    {"domain": "field_model_ecs_layer", "primary": "luna_self_work_dataclass", "model_support": "esper_flecs_reference"},
    {"domain": "field_model_scene_graph", "primary": "luna_self_work", "model_support": "kimera_hydra_reference"},
    {"domain": "field_model_semantic_graph", "primary": "luna_self_work_lightweight", "model_support": "networkx_reference"},
    {"domain": "field_boundary_continuity", "primary": "luna_self_work", "model_support": "tracking_pose_speed"},
    {"domain": "field_simulation", "primary": "luna_self_work_rules_geometry", "model_support": "model_input_only"},
    {"domain": "task_field_view", "primary": "luna_self_work", "model_support": "optional_llm_compress"},
    {"domain": "midplatform_reasoning", "primary": "luna_self_work_structure", "model_support": "llm_interpretation"},
    {"domain": "drive_layer", "primary": "luna_self_work", "model_support": "optional_llm_reflection"},
)

NEXT_RESEARCH_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"target_id": "sam2_capability_review", "operation_node": "visual_object_segmentation_tracking", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "grounded_sam2_capability_review", "operation_node": "visual_object_segmentation_tracking", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "bytetrack_capability_review", "operation_node": "visual_object_segmentation_tracking", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "paddleocr_capability_review", "operation_node": "ocr_text_perception", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "whisper_sensevoice_capability_review", "operation_node": "audio_speech_speaker", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "kimera_hydra_capability_review", "operation_node": "spatial_slam_dynamic_scene_graph", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "hovsg_open3dsg_capability_review", "operation_node": "spatial_slam_dynamic_scene_graph", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "esper_flecs_capability_review", "operation_node": "ecs_entity_component", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "networkx_rdflib_capability_review", "operation_node": "lightweight_semantic_event_graph", "phase": "model_document_capability_review", "status": "pending"},
    {"target_id": "llm_reasoning_capability_review", "operation_node": "midplatform_reasoning", "phase": "model_document_capability_review", "status": "pending"},
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "ideal_operation_not_model_research",
    "requirement_mapping_not_model_selection",
    "model_document_review_deferred_to_next_phase",
    "operation_node_not_implementation",
    "self_work_primary_not_model_dependency",
    "reference_model_not_runtime_commitment",
    "ideal_operation_before_model_room_selection",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Model Document Capability Review"
