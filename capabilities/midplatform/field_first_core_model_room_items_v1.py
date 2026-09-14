# -*- coding: utf-8 -*-
"""Field-First Core Model Room and Interface Logic item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

MODEL_ROOM_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "model_room_principles_v1",
    "rules": (
        "build_room_before_place_model",
        "model_output_default_candidate",
        "model_cannot_reverse_define_midplatform",
        "fixed_model_entry_exit",
        "interface_first_not_integration_first",
    ),
}

MODEL_ROOMS: Tuple[Dict[str, Any], ...] = (
    {
        "room_id": "source_intake_room",
        "name": "Source Intake Room",
        "role_ref": "source_intake_normalization_operator",
        "inputs": ("vision", "ocr", "speech", "depth", "imu", "map", "user_instruction", "health_signal"),
        "outputs": ("ObservationCandidate",),
        "forbidden": ("direct_field_entity", "world_model_write", "task_decision"),
    },
    {
        "room_id": "visual_perception_room",
        "name": "Visual Perception Room",
        "reference_models": ("SAM2", "Grounded_SAM2", "Grounding_DINO", "Florence2", "DINO_X", "ByteTrack", "YOLO_series"),
        "capabilities": (
            "object_detection", "segmentation", "mask_generation", "video_object_tracking",
            "track_id", "open_vocabulary_grounding", "object_candidate_extraction",
        ),
        "outputs": ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate", "VisualRelationHintCandidate"),
        "forbidden": ("direct_field_entity", "world_model_write", "task_decision"),
    },
    {
        "room_id": "ocr_text_perception_room",
        "name": "OCR / Text Perception Room",
        "reference_models": ("PaddleOCR", "RapidOCR"),
        "capabilities": ("text_region_detection", "text_recognition", "reading_order", "language_detection", "text_confidence"),
        "outputs": ("TextObservationCandidate", "TextRegionCandidate", "ReadabilityCandidate"),
        "forbidden": ("direct_reading_task_complete", "long_term_knowledge_write"),
    },
    {
        "room_id": "audio_speech_perception_room",
        "name": "Audio / Speech Perception Room",
        "reference_models": ("ASR", "speaker_diarization", "voiceprint", "VAD"),
        "capabilities": ("transcript", "speaker_segment", "user_intent_hint", "interruption_signal", "confidence"),
        "outputs": ("SpeechObservationCandidate", "SpeakerObservationCandidate", "IntentHintCandidate"),
        "forbidden": ("direct_authorization", "user_preference_fact_write", "direct_task_execution"),
    },
    {
        "room_id": "spatial_slam_scene_graph_room",
        "name": "Spatial / SLAM / Scene Graph Room",
        "reference_models": ("Kimera", "Hydra", "HOV_SG", "Open3DSG", "RTG_SLAM", "Splatt3R_SLAM"),
        "capabilities": (
            "visual_inertial_odometry", "metric_semantic_mapping", "scene_graph_3d",
            "object_room_place_hierarchy", "spatial_relation", "navigation_graph_reference",
        ),
        "outputs": ("SpatialObservationCandidate", "PoseObservationCandidate", "SceneRelationCandidate", "SceneGraphReferenceCandidate"),
        "current_position": "field_model_builder_reference_not_runtime",
        "forbidden": ("direct_runtime_integration_now",),
    },
    {
        "room_id": "ecs_entity_component_room",
        "name": "ECS / Entity Component Room",
        "reference_models": ("Esper", "Flecs"),
        "capabilities": ("entity_id", "component_attach_detach", "attribute_component", "dynamic_state_component", "update_policy", "ttl"),
        "outputs": ("EntityComponentCandidate", "AttributeStateCandidate", "EntityStateUpdateCandidate"),
        "current_position": "python_dataclass_simulation_first",
        "forbidden": ("force_ecs_runtime_now",),
    },
    {
        "room_id": "semantic_event_graph_room",
        "name": "Semantic / Event Graph Room",
        "reference_models": ("NetworkX", "RDFLib", "Neo4j"),
        "capabilities": (
            "event_node", "risk_node", "rule_zone", "place_function", "relationship_graph",
            "supports_conflicts_blocks_causes_or_enables",
        ),
        "outputs": ("SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate", "EventRelationCandidate"),
        "current_position": "lightweight_event_graph_first_no_full_kg",
        "forbidden": ("full_knowledge_graph_now", "emotional_graph_now"),
    },
    {
        "room_id": "field_simulation_room",
        "name": "Field Simulation Room",
        "reference_capabilities": (
            "trajectory_projection", "collision_path_intersection", "occlusion_update",
            "accessibility_check", "future_window_simulation", "task_specific_projection",
        ),
        "outputs": ("FieldSimulationResultCandidate", "TrajectoryProjectionCandidate", "RiskProjectionCandidate", "MissingInformationCandidate"),
        "current_position": "rule_geometry_state_machine_first_llm_interprets_not_simulates",
        "forbidden": ("llm_free_simulation",),
    },
    {
        "room_id": "midplatform_reasoning_room",
        "name": "Midplatform Reasoning Room",
        "reference_models": ("LLM", "VLM", "small_reasoning_model"),
        "capabilities": (
            "read_task_field_view", "read_field_simulation_result", "explain_candidate_conclusion",
            "generate_need_more_info_defer_risk_route", "structured_reasoning_result",
        ),
        "outputs": ("MidplatformReasoningCandidate",),
        "forbidden": (
            "read_all_raw_sources", "direct_field_model_write", "execute_actions",
            "create_facts", "replace_field_simulation",
        ),
    },
)

OPEN_SOURCE_REFERENCE_INVENTORY: Tuple[Dict[str, Any], ...] = (
    {"model_or_project_id": "SAM2", "open_source_status": "open_source", "primary_capability": "image_video_segmentation_mask_tracking", "likely_room": "visual_perception_room", "output_type": "MaskObservationCandidate", "useful_for_luna_phase_1": "reference_future_adapter", "runtime_required_now": False, "recommended_position": "reference_future_adapter_candidate"},
    {"model_or_project_id": "Grounded_SAM2", "open_source_status": "open_source", "primary_capability": "open_set_grounding_tracking_segmentation", "likely_room": "visual_perception_room", "output_type": "ObjectObservationCandidate_MaskObservationCandidate_TrackObservationCandidate", "useful_for_luna_phase_1": "external_tech_pool", "runtime_required_now": False, "recommended_position": "open_vocab_visual_candidate_reference"},
    {"model_or_project_id": "ByteTrack", "open_source_status": "open_source", "primary_capability": "multi_object_tracking_track_id_continuity", "likely_room": "visual_perception_room", "output_type": "TrackObservationCandidate", "useful_for_luna_phase_1": "entity_continuity_reference", "runtime_required_now": False, "recommended_position": "future_entity_continuity_reference"},
    {"model_or_project_id": "Kimera", "open_source_status": "open_source", "primary_capability": "VIO_metric_semantic_SLAM_3d_scene_graph", "likely_room": "spatial_slam_scene_graph_room", "output_type": "SpatialObservationCandidate_SceneGraphReferenceCandidate", "useful_for_luna_phase_1": "structure_reference_only", "runtime_required_now": False, "recommended_position": "field_model_reference_not_direct_integration"},
    {"model_or_project_id": "Hydra", "open_source_status": "open_source", "primary_capability": "realtime_3d_scene_graph_construction", "likely_room": "spatial_slam_scene_graph_room", "output_type": "SceneGraphReferenceCandidate", "useful_for_luna_phase_1": "field_model_three_layer_reference", "runtime_required_now": False, "recommended_position": "field_model_structure_reference"},
    {"model_or_project_id": "HOV_SG", "open_source_status": "open_source", "primary_capability": "open_vocab_hierarchical_3d_scene_graph_language_navigation", "likely_room": "spatial_slam_scene_graph_room", "output_type": "SceneGraphReferenceCandidate_SemanticRelationCandidate", "useful_for_luna_phase_1": "long_term_reference", "runtime_required_now": False, "recommended_position": "not_first_version_dependency"},
    {"model_or_project_id": "Open3DSG", "open_source_status": "open_source", "primary_capability": "open_vocab_3d_scene_graph_point_cloud_relation_query", "likely_room": "spatial_slam_scene_graph_room", "output_type": "SceneRelationCandidate", "useful_for_luna_phase_1": "long_term_reference", "runtime_required_now": False, "recommended_position": "long_term_reference"},
    {"model_or_project_id": "Esper", "open_source_status": "open_source", "primary_capability": "python_lightweight_ecs", "likely_room": "ecs_entity_component_room", "output_type": "EntityComponentCandidate_reference", "useful_for_luna_phase_1": "reference_dataclass_first", "runtime_required_now": False, "recommended_position": "reference_python_dataclass_simulation"},
    {"model_or_project_id": "Flecs", "open_source_status": "open_source", "primary_capability": "c_cpp_high_performance_ecs", "likely_room": "ecs_entity_component_room", "output_type": "EntityComponent_architecture_reference", "useful_for_luna_phase_1": "long_term_performance_reference", "runtime_required_now": False, "recommended_position": "long_term_performance_reference"},
    {"model_or_project_id": "NetworkX", "open_source_status": "open_source", "primary_capability": "python_graph_modeling_analysis", "likely_room": "semantic_event_graph_room", "output_type": "SemanticEventGraph_prototype", "useful_for_luna_phase_1": "phase1_optional_reference", "runtime_required_now": False, "recommended_position": "phase1_lightweight_graph_reference"},
    {"model_or_project_id": "RDFLib", "open_source_status": "open_source", "primary_capability": "rdf_graph_triples_sparql", "likely_room": "semantic_event_graph_room", "output_type": "SemanticRelationCandidate_reference", "useful_for_luna_phase_1": "long_term_kg_standard_reference", "runtime_required_now": False, "recommended_position": "not_mandatory_phase1"},
    {"model_or_project_id": "Neo4j", "open_source_status": "open_source", "primary_capability": "property_graph_database", "likely_room": "semantic_event_graph_room", "output_type": "long_term_graph_storage_reference", "useful_for_luna_phase_1": "future_backend_reference", "runtime_required_now": False, "recommended_position": "not_integrate_now"},
)

MODEL_ADAPTER_INTERFACE_FIELDS: Tuple[str, ...] = (
    "adapter_id", "model_ref", "source_type", "input_schema_ref", "output_candidate_type",
    "confidence_mapping", "freshness_mapping", "failure_mode_mapping", "traceability_mapping",
    "governance_mapping", "non_execution_flags", "unsupported_output_policy",
)

MODEL_ADAPTER_BUS: Dict[str, Any] = {
    "bus_id": "model_adapter_bus_v1",
    "chain": ("model_raw_output", "model_adapter", "observation_or_field_candidate", "validator", "field_model_or_reasoning_context"),
    "adapter_required_for_all_models": True,
}

CANDIDATE_OUTPUT_TYPES: Tuple[str, ...] = (
    "ObservationCandidate",
    "ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate",
    "TextObservationCandidate", "SpeechObservationCandidate", "PoseObservationCandidate",
    "SpatialObservationCandidate", "SceneRelationCandidate",
    "EntityComponentCandidate", "AttributeStateCandidate",
    "SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate",
    "FieldUpdateCandidate", "FieldSimulationResultCandidate", "TaskFieldViewCandidate",
    "MidplatformReasoningCandidate", "PerceptionRequestCandidate",
    "TextRegionCandidate", "ReadabilityCandidate", "SpeakerObservationCandidate",
    "IntentHintCandidate", "SceneGraphReferenceCandidate", "EntityStateUpdateCandidate",
    "EventRelationCandidate", "TrajectoryProjectionCandidate", "RiskProjectionCandidate",
    "MissingInformationCandidate", "VisualRelationHintCandidate",
)

PROHIBITED_MODEL_OUTPUTS: Tuple[str, ...] = (
    "WorldModelFact", "PersistentMemory", "RealAction", "Authorization",
    "Grant", "Record", "FinalDecision",
)

INTERFACE_LOGIC: Tuple[Dict[str, Any], ...] = (
    {"flow_id": "visual_model_exit", "chain": ("visual_raw_output", "visual_adapter", "object_mask_track_observation_candidate", "field_model_builder")},
    {"flow_id": "ocr_model_exit", "chain": ("ocr_raw_output", "ocr_adapter", "text_observation_candidate", "task_field_view_or_field_model")},
    {"flow_id": "asr_model_exit", "chain": ("speech_raw_output", "speech_adapter", "speech_intent_observation_candidate", "task_drive_or_source_intake")},
    {"flow_id": "slam_scene_graph_exit", "chain": ("spatial_raw_output", "spatial_adapter", "pose_scene_relation_candidate", "field_model_builder")},
    {"flow_id": "ecs_reference_exit", "chain": ("entity_component_operation", "entity_component_candidate", "field_model_ecs_layer")},
    {"flow_id": "semantic_graph_exit", "chain": ("event_relation_rule_node", "semantic_event_candidate", "field_semantic_layer")},
    {"flow_id": "simulation_exit", "chain": ("field_and_task", "simulation_adapter", "field_simulation_result_candidate", "midplatform_reasoning")},
    {"flow_id": "reasoning_model_exit", "chain": ("task_field_view_and_simulation_result", "reasoning_adapter", "midplatform_reasoning_candidate", "future_orchestration_drive_layer")},
)

MODEL_USAGE_ORDER: Tuple[str, ...] = (
    "define_model_rooms", "define_candidate_output_types", "define_adapter_interface",
    "define_field_model_candidate_reception", "define_field_simulation_reception",
    "define_midplatform_reasoning_reception", "then_decide_real_model_integration",
)

FIELD_MODEL_INPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_model_input_contract_from_models_v1",
    "accepts_from_rooms": (
        "source_intake_room", "visual_perception_room", "ocr_text_perception_room",
        "audio_speech_perception_room", "spatial_slam_scene_graph_room", "ecs_entity_component_room",
        "semantic_event_graph_room",
    ),
    "accepts_candidate_types": (
        "ObservationCandidate", "ObjectObservationCandidate", "MaskObservationCandidate",
        "TrackObservationCandidate", "TextObservationCandidate", "SpatialObservationCandidate",
        "PoseObservationCandidate", "SceneRelationCandidate", "EntityComponentCandidate",
        "AttributeStateCandidate", "SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate",
        "FieldUpdateCandidate",
    ),
    "requires_adapter": True,
    "direct_fact_write_forbidden": True,
    "validator_required": True,
}

FIELD_SIMULATION_IO_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_simulation_input_output_contract_v1",
    "input": ("field_model_candidate", "task_goal", "field_boundary", "field_session_state"),
    "output": ("FieldSimulationResultCandidate", "TrajectoryProjectionCandidate", "RiskProjectionCandidate", "MissingInformationCandidate"),
    "llm_simulation_forbidden": True,
    "rule_geometry_state_machine_first": True,
}

MIDPLATFORM_REASONING_IO_CONTRACT: Dict[str, Any] = {
    "contract_id": "midplatform_reasoning_model_input_output_contract_v1",
    "input": ("TaskFieldViewCandidate", "FieldSimulationResultCandidate", "risk_summary", "conflict_summary", "missing_information"),
    "output": ("MidplatformReasoningCandidate",),
    "raw_source_read_forbidden": True,
    "field_model_direct_write_forbidden": True,
    "action_execution_forbidden": True,
    "fact_creation_forbidden": True,
}

DEFERRED_MODEL_INTEGRATION: Tuple[Dict[str, Any], ...] = (
    {"integration_id": "kimera_runtime", "status": "deferred", "reason": "reference_only_structure"},
    {"integration_id": "hydra_runtime", "status": "deferred", "reason": "reference_only_structure"},
    {"integration_id": "hov_sg_runtime", "status": "deferred", "reason": "not_first_version_dependency"},
    {"integration_id": "open3dsg_runtime", "status": "deferred", "reason": "long_term_reference"},
    {"integration_id": "sam2_weight_download", "status": "deferred", "reason": "no_download_this_phase"},
    {"integration_id": "grounded_sam2_runtime", "status": "deferred", "reason": "future_adapter_candidate"},
    {"integration_id": "neo4j_backend", "status": "deferred", "reason": "no_database_now"},
    {"integration_id": "flecs_runtime", "status": "deferred", "reason": "dataclass_simulation_first"},
    {"integration_id": "module_handoff_contract", "status": "deferred_p3", "reason": "peripheral_premature"},
)

PRIOR_ASSET_REPOSITIONING: Tuple[Dict[str, Any], ...] = (
    {"asset_id": "information_processing_core", "model_room": "source_intake_room", "role": "observation_normalization_adapter_asset"},
    {"asset_id": "kimera_hydra_hovsg", "model_room": "spatial_slam_scene_graph_room", "role": "structure_reference_only"},
    {"asset_id": "sam2_grounded_sam2_bytetrack", "model_room": "visual_perception_room", "role": "reference_or_future_adapter"},
    {"asset_id": "esper_flecs", "model_room": "ecs_entity_component_room", "role": "ecs_reference_dataclass_first"},
    {"asset_id": "networkx_rdflib_neo4j", "model_room": "semantic_event_graph_room", "role": "lightweight_graph_reference_no_full_kg"},
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "model_room_not_model_integration",
    "reference_model_not_runtime_dependency",
    "candidate_output_not_fact",
    "adapter_not_optional",
    "hydra_kimera_reference_not_core_definition",
    "ecs_reference_not_force_runtime",
    "kg_reference_not_full_knowledge_graph",
    "model_room_definition_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Work-Manual-and-Architecture-Definition-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Work Manual and Architecture Definition"
