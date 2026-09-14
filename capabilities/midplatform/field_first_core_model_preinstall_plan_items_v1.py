# -*- coding: utf-8 -*-
"""Field-First Model Preinstall Plan item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

PREINSTALL_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "model_preinstall_principles_v1",
    "scope": "model_preinstall_planning_cache_manifest_prepare_only",
    "rules": (
        "build_room_before_place_model",
        "no_weight_download",
        "no_inference",
        "no_skip_capability_review",
        "model_output_candidate_only",
    ),
}

MODEL_ROOM_DIRECTORIES: Tuple[str, ...] = (
    "configs/models/field_first/model_rooms/",
    "configs/models/field_first/model_rooms/visual_perception/",
    "configs/models/field_first/model_rooms/ocr_text/",
    "configs/models/field_first/model_rooms/audio_speech/",
    "configs/models/field_first/model_rooms/spatial_scene_graph/",
    "configs/models/field_first/model_rooms/ecs_entity_component/",
    "configs/models/field_first/model_rooms/semantic_event_graph/",
    "configs/models/field_first/model_rooms/field_simulation/",
    "configs/models/field_first/model_rooms/midplatform_reasoning/",
)

CONFIG_MANIFEST_FILES: Tuple[str, ...] = (
    "configs/models/field_first/preinstall_manifest_v1.json",
    "configs/models/field_first/model_room_registry_v1.json",
    "configs/models/field_first/model_download_authorization_v1.json",
    "configs/models/field_first/model_adapter_placeholder_registry_v1.json",
    "configs/models/field_first/model_capability_review_queue_v1.json",
)

MODEL_ROOM_PREINSTALL_PLANS: Tuple[Dict[str, Any], ...] = (
    {
        "room_id": "visual_perception_room",
        "candidates": ("SAM2", "Grounded_SAM2", "ByteTrack", "YOLO_lightweight", "GroundingDINO", "Florence2", "DINO_X"),
        "expected_outputs": ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate", "VisualRelationHintCandidate"),
        "directory_prepare_allowed": True, "adapter_placeholder_allowed": True,
        "weight_download_allowed": False, "inference_allowed": False,
    },
    {
        "room_id": "ocr_text_perception_room",
        "candidates": ("PaddleOCR", "RapidOCR"),
        "expected_outputs": ("TextObservationCandidate", "TextRegionCandidate", "ReadabilityCandidate"),
        "directory_prepare_allowed": True, "adapter_placeholder_allowed": True,
        "weight_download_allowed": False, "inference_allowed": False,
    },
    {
        "room_id": "audio_speech_perception_room",
        "candidates": ("Whisper", "faster_whisper", "SenseVoice", "pyannote_audio", "VAD_placeholder", "voiceprint_placeholder"),
        "expected_outputs": ("SpeechObservationCandidate", "SpeakerObservationCandidate", "IntentHintCandidate", "InterruptSignalCandidate"),
        "directory_prepare_allowed": True, "adapter_placeholder_allowed": True,
        "weight_download_allowed": False, "inference_allowed": False,
    },
    {
        "room_id": "spatial_slam_scene_graph_room",
        "candidates": ("Kimera", "Hydra", "HOV_SG", "Open3DSG", "RTG_SLAM_placeholder", "Splatt3R_SLAM_placeholder"),
        "expected_outputs": ("PoseObservationCandidate", "SpatialObservationCandidate", "SceneRelationCandidate", "SceneGraphReferenceCandidate", "AccessibilityRelationCandidate"),
        "reference_only_now": True, "directory_prepare_allowed": True, "adapter_placeholder_allowed": True,
        "weight_download_allowed": False, "runtime_build_allowed": False, "inference_allowed": False,
    },
    {
        "room_id": "ecs_entity_component_room",
        "candidates": ("Luna_dataclass_ECS_skeleton", "Esper", "Flecs"),
        "expected_outputs": ("WorldEntityCandidate", "EntityComponentCandidate", "AttributeStateCandidate", "EntityStateUpdateCandidate"),
        "dataclass_skeleton_allowed": True, "external_runtime_dependency_allowed": False, "reference_manifest_allowed": True,
    },
    {
        "room_id": "semantic_event_graph_room",
        "candidates": ("Luna_lightweight_event_graph_skeleton", "NetworkX", "RDFLib", "Neo4j"),
        "expected_outputs": ("SemanticEventCandidate", "RiskZoneCandidate", "RuleZoneCandidate", "PlaceFunctionCandidate", "EventRelationCandidate"),
        "lightweight_skeleton_allowed": True, "external_database_allowed": False, "reference_manifest_allowed": True,
    },
    {
        "room_id": "field_simulation_room",
        "candidates": ("Luna_geometry_simulator", "collision_path_intersection_placeholder", "occlusion_update_placeholder"),
        "expected_outputs": ("FieldSimulationResultCandidate", "TrajectoryProjectionCandidate", "RiskProjectionCandidate", "MissingInformationCandidate", "SafeWindowCandidate"),
        "self_developed_placeholder_allowed": True, "external_model_dependency_required_now": False,
    },
    {
        "room_id": "midplatform_reasoning_room",
        "candidates": ("structured_LLM_reasoning", "local_small_model", "cloud_LLM", "rule_LLM_hybrid"),
        "expected_outputs": ("MidplatformReasoningCandidate", "NeedMoreInfoCandidate", "RiskCandidate", "RouteCandidate", "PerceptionNeedCandidate", "TaskBlockedCandidate"),
        "adapter_placeholder_allowed": True, "model_selection_allowed": False, "inference_allowed": False,
    },
)

def _candidate(
    model_project_id: str, display_name: str, model_room: str,
    operation_node_refs: Tuple[str, ...], expected_outputs: Tuple[str, ...],
    preinstall_status: str, reason: str, hardware_risk: str = "medium", integration_risk: str = "medium",
) -> Dict[str, Any]:
    return {
        "model_project_id": model_project_id, "display_name": display_name, "model_room": model_room,
        "operation_node_refs": list(operation_node_refs), "expected_candidate_outputs": list(expected_outputs),
        "source_url_placeholder": f"https://placeholder.luna/{model_project_id}",
        "docs_url_placeholder": f"https://docs.placeholder.luna/{model_project_id}",
        "license_status": "pending_review", "weights_required": model_project_id not in ("NetworkX", "RDFLib", "Esper"),
        "weights_downloaded": False, "download_authorized": False,
        "runtime_build_required": model_room in ("spatial_slam_scene_graph_room", "visual_perception_room"),
        "runtime_build_completed": False, "inference_ready": False,
        "adapter_required": True, "adapter_placeholder_created": True,
        "capability_review_required": True, "capability_review_status": "pending",
        "recommended_preinstall_status": preinstall_status, "reason_for_status": reason,
        "hardware_risk": hardware_risk, "integration_risk": integration_risk,
        "notes": "preinstall_plan_only_no_download",
    }


PREINSTALL_MANIFEST_ENTRIES: Tuple[Dict[str, Any], ...] = (
    _candidate("SAM2", "SAM 2", "visual_perception_room", ("visual_object_segmentation_tracking",), ("MaskObservationCandidate", "TrackObservationCandidate"), "document_review_pending", "await_capability_review"),
    _candidate("Grounded_SAM2", "Grounded SAM 2", "visual_perception_room", ("visual_object_segmentation_tracking",), ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate"), "near_term_candidate_pending_review", "open_vocab_visual"),
    _candidate("ByteTrack", "ByteTrack", "visual_perception_room", ("visual_object_segmentation_tracking",), ("TrackObservationCandidate",), "document_review_pending", "entity_continuity_reference"),
    _candidate("YOLO_lightweight", "YOLO Lightweight", "visual_perception_room", ("visual_object_segmentation_tracking",), ("ObjectObservationCandidate",), "adapter_placeholder_only", "lightweight_detector_placeholder"),
    _candidate("PaddleOCR", "PaddleOCR", "ocr_text_perception_room", ("ocr_text_perception",), ("TextObservationCandidate", "TextRegionCandidate"), "near_term_candidate_pending_review", "ocr_primary_candidate"),
    _candidate("RapidOCR", "RapidOCR", "ocr_text_perception_room", ("ocr_text_perception",), ("TextObservationCandidate", "TextRegionCandidate"), "document_review_pending", "lightweight_ocr_alternative"),
    _candidate("Whisper", "Whisper", "audio_speech_perception_room", ("audio_speech_speaker",), ("SpeechObservationCandidate",), "document_review_pending", "asr_reference"),
    _candidate("faster_whisper", "faster-whisper", "audio_speech_perception_room", ("audio_speech_speaker",), ("SpeechObservationCandidate",), "document_review_pending", "asr_edge_candidate"),
    _candidate("SenseVoice", "SenseVoice", "audio_speech_perception_room", ("audio_speech_speaker",), ("SpeechObservationCandidate", "IntentHintCandidate"), "document_review_pending", "chinese_asr_candidate"),
    _candidate("pyannote_audio", "pyannote.audio", "audio_speech_perception_room", ("audio_speech_speaker",), ("SpeakerObservationCandidate",), "document_review_pending", "speaker_diarization"),
    _candidate("Kimera", "Kimera", "spatial_slam_scene_graph_room", ("spatial_slam_dynamic_scene_graph",), ("SpatialObservationCandidate", "SceneGraphReferenceCandidate"), "reference_only_now", "structure_reference_not_runtime", "high", "high"),
    _candidate("Hydra", "Hydra", "spatial_slam_scene_graph_room", ("spatial_slam_dynamic_scene_graph",), ("SceneGraphReferenceCandidate",), "reference_only_now", "field_model_structure_reference", "high", "high"),
    _candidate("HOV_SG", "HOV-SG", "spatial_slam_scene_graph_room", ("spatial_slam_dynamic_scene_graph",), ("SceneGraphReferenceCandidate",), "reference_only_now", "long_term_reference", "high", "high"),
    _candidate("Open3DSG", "Open3DSG", "spatial_slam_scene_graph_room", ("spatial_slam_dynamic_scene_graph",), ("SceneRelationCandidate",), "reference_only_now", "long_term_reference", "high", "high"),
    _candidate("Esper", "Esper", "ecs_entity_component_room", ("ecs_entity_component",), ("EntityComponentCandidate",), "reference_only_now", "ecs_reference_dataclass_first", "low", "low"),
    _candidate("Flecs", "Flecs", "ecs_entity_component_room", ("ecs_entity_component",), ("EntityComponentCandidate",), "reference_only_now", "long_term_performance_reference", "medium", "medium"),
    _candidate("NetworkX", "NetworkX", "semantic_event_graph_room", ("lightweight_semantic_event_graph",), ("SemanticEventCandidate",), "directory_only", "lightweight_graph_reference", "low", "low"),
    _candidate("RDFLib", "RDFLib", "semantic_event_graph_room", ("lightweight_semantic_event_graph",), ("SemanticEventCandidate",), "reference_only_now", "kg_standard_reference", "low", "low"),
    _candidate("Neo4j", "Neo4j", "semantic_event_graph_room", ("lightweight_semantic_event_graph",), ("SemanticEventCandidate",), "deferred_due_to_runtime_cost", "no_database_now", "medium", "high"),
    _candidate("Luna_dataclass_ECS_skeleton", "Luna ECS Skeleton", "ecs_entity_component_room", ("ecs_entity_component",), ("EntityComponentCandidate", "AttributeStateCandidate"), "adapter_placeholder_only", "self_developed_primary"),
    _candidate("Luna_geometry_simulator", "Luna Geometry Simulator", "field_simulation_room", ("field_simulation",), ("FieldSimulationResultCandidate",), "adapter_placeholder_only", "self_developed_primary"),
    _candidate("structured_LLM_reasoning", "Structured LLM Reasoning", "midplatform_reasoning_room", ("midplatform_reasoning",), ("MidplatformReasoningCandidate",), "blocked_until_download_authorized", "model_selection_not_allowed", "medium", "medium"),
)

CAPABILITY_REVIEW_QUEUE: Tuple[Dict[str, Any], ...] = tuple(
    {
        "target_id": f"{e['model_project_id'].lower()}_capability_review",
        "model_project_id": e["model_project_id"],
        "operation_node_id": e["operation_node_refs"][0],
        "model_room": e["model_room"],
        "requirement_matrix_refs": e["operation_node_refs"],
        "expected_output_candidate": e["expected_candidate_outputs"],
        "review_priority": "P1" if e["recommended_preinstall_status"] == "near_term_candidate_pending_review" else "P2",
        "review_reason": e["reason_for_status"],
        "current_preinstall_action": e["recommended_preinstall_status"],
        "status": "pending",
    }
    for e in PREINSTALL_MANIFEST_ENTRIES
)

PROHIBITED_PREINSTALL_ACTIONS: Tuple[str, ...] = (
    "download_model_weights", "clone_large_repository", "pip_install_large_model_dependency",
    "run_inference", "run_benchmark", "mark_model_selected", "mark_production_ready",
    "create_runtime_adapter", "write_world_model_fact", "create_integration_test",
    "implement_handoff_contract", "implement_candidate_lifecycle_manager",
    "modify_ipc_core_implementation",
)

PRIOR_ASSET_REPOSITIONING: Tuple[Dict[str, str], ...] = (
    {"asset_id": "information_processing_core", "role": "source_normalization_not_model_preinstall_center"},
    {"asset_id": "model_room_phase", "role": "aligned_with_preinstall_plan_not_runtime"},
    {"asset_id": "ideal_operation_mechanism", "role": "requirement_source_for_review_queue"},
    {"asset_id": "module_handoff_contract", "role": "p3_defer_continues"},
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "preinstall_plan_not_model_download",
    "cache_manifest_not_weight_cache",
    "adapter_placeholder_not_runtime_adapter",
    "directory_prepare_not_model_selected",
    "capability_review_still_required",
    "preinstall_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Model Document Capability Review"
