# -*- coding: utf-8 -*-
"""Field-First Model I/O Compatibility Precheck item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

PRECHECK_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "model_io_precheck_principles_v1",
    "rules": (
        "io_precheck_before_skeleton_implementation",
        "not_full_document_review_not_model_selection",
        "no_download_no_inference_no_runtime",
        "calibrate_skeleton_entry_exit_not_commit_adapter",
    ),
}

IO_REVIEW_FIELDS: Tuple[str, ...] = (
    "model_project_id", "model_room", "operation_node_id",
    "expected_input_type", "expected_input_shape_or_payload", "expected_output_type",
    "spatial_output_fields", "temporal_output_fields", "confidence_or_score_fields",
    "identity_or_tracking_fields", "text_fields", "audio_segment_fields",
    "graph_or_relation_fields", "structured_output_fields", "required_adapter_transform",
    "maps_to_candidate_type", "candidate_fields_required_by_luna",
    "candidate_fields_confirmed_by_docs", "candidate_fields_missing_or_unclear",
    "skeleton_schema_adjustment_needed", "compatibility_status", "notes",
)

COMPATIBILITY_STATUS_OPTIONS: Tuple[str, ...] = (
    "compatible_with_current_candidate_schema",
    "compatible_with_minor_schema_extension",
    "compatible_but_adapter_required",
    "unclear_requires_later_review",
    "incompatible_with_phase1_schema",
    "reference_only_no_schema_commitment",
)

COMMON_SPATIAL_PAYLOAD: Tuple[str, ...] = (
    "bbox", "mask_ref", "point", "polygon", "depth_hint", "coordinate_frame",
)

COMMON_TEMPORAL_PAYLOAD: Tuple[str, ...] = (
    "timestamp", "frame_id", "segment_start", "segment_end", "ttl", "freshness_level",
)

COMMON_IDENTITY_PAYLOAD: Tuple[str, ...] = (
    "track_id", "entity_hint", "speaker_hint", "object_instance_hint",
)

COMMON_CONFIDENCE_PAYLOAD: Tuple[str, ...] = (
    "confidence", "detection_score", "recognition_score", "tracking_score", "source_reliability",
)

COMMON_GRAPH_PAYLOAD: Tuple[str, ...] = (
    "node_ref", "edge_ref", "relation_type", "relation_strength", "scene_graph_ref",
)

COMMON_TEXT_AUDIO_PAYLOAD: Tuple[str, ...] = (
    "recognized_text", "transcript", "word_timestamps", "reading_order", "language_hint",
)

CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS: Tuple[str, ...] = (
    "source_refs", "evidence_refs", "confidence", "freshness", "ttl",
    "conflict_status", "reason_codes", "non_execution_flags",
)

SKELETON_IO_REQUIREMENTS: Tuple[str, ...] = (
    "observation_candidate_spatial_payload",
    "observation_candidate_temporal_payload",
    "observation_candidate_identity_payload",
    "field_entity_hint_from_bbox_mask_track",
    "field_continuity_track_id_hint",
    "text_region_as_field_entity_or_attribute",
    "task_field_view_text_extraction",
    "speech_intent_hint_for_task_drive",
    "scene_relation_candidate_support",
    "graph_reference_candidate_support",
    "reasoning_reads_structured_candidates_only",
)


def _io(
    model_project_id: str, model_room: str, operation_node_id: str,
    compatibility_status: str, maps_to: Tuple[str, ...], **kwargs: Any,
) -> Dict[str, Any]:
    return {
        "model_project_id": model_project_id,
        "model_room": model_room,
        "operation_node_id": operation_node_id,
        "expected_input_type": kwargs.get("input_type", "modality_specific"),
        "expected_input_shape_or_payload": kwargs.get("input_payload", []),
        "expected_output_type": kwargs.get("output_type", "structured_candidate"),
        "spatial_output_fields": list(kwargs.get("spatial", [])),
        "temporal_output_fields": list(kwargs.get("temporal", [])),
        "confidence_or_score_fields": list(kwargs.get("confidence", [])),
        "identity_or_tracking_fields": list(kwargs.get("identity", [])),
        "text_fields": list(kwargs.get("text", [])),
        "audio_segment_fields": list(kwargs.get("audio", [])),
        "graph_or_relation_fields": list(kwargs.get("graph", [])),
        "structured_output_fields": list(kwargs.get("structured", [])),
        "required_adapter_transform": kwargs.get("adapter_transform", "model_raw_to_candidate"),
        "maps_to_candidate_type": list(maps_to),
        "candidate_fields_required_by_luna": list(kwargs.get("luna_required", [])),
        "candidate_fields_confirmed_by_docs": list(kwargs.get("confirmed", [])),
        "candidate_fields_missing_or_unclear": list(kwargs.get("missing", [])),
        "skeleton_schema_adjustment_needed": kwargs.get("adjustment", True),
        "compatibility_status": compatibility_status,
        "notes": kwargs.get("notes", "document_level_io_precheck_only"),
    }


MODEL_IO_REVIEW_ITEMS: Tuple[Dict[str, Any], ...] = (
    _io("PaddleOCR", "ocr_text_perception_room", "ocr_text_perception", "compatible_with_minor_schema_extension",
        ("TextObservationCandidate", "TextRegionCandidate", "ReadabilityCandidate"),
        input_type="image", input_payload=["image_ref", "frame_ref"],
        spatial=["text_region_bbox"], text=["recognized_text", "reading_order", "language_hint"],
        confidence=["detection_confidence", "recognition_confidence", "text_confidence"],
        temporal=["timestamp"], luna_required=["text_region_bbox", "recognized_text", "confidence", "source_ref"],
        confirmed=["text_region_bbox", "recognized_text", "detection_confidence", "recognition_confidence"],
        missing=["orientation_hint"], adjustment=True),
    _io("RapidOCR", "ocr_text_perception_room", "ocr_text_perception", "compatible_with_minor_schema_extension",
        ("TextObservationCandidate", "TextRegionCandidate"),
        spatial=["text_region_bbox"], text=["recognized_text"], confidence=["confidence"],
        confirmed=["text_region_bbox", "recognized_text"], missing=["reading_order"]),
    _io("ByteTrack", "visual_perception_room", "visual_object_segmentation_tracking", "compatible_but_adapter_required",
        ("TrackObservationCandidate",),
        input_type="detection_boxes_sequence", input_payload=["bbox", "frame_ref", "timestamp"],
        spatial=["bbox"], identity=["track_id"], confidence=["track_confidence", "detection_score"],
        temporal=["frame_ref", "timestamp"], luna_required=["bbox", "track_id", "confidence", "frame_ref"],
        confirmed=["bbox", "track_id"], missing=["mask_ref"]),
    _io("YOLO_lightweight", "visual_perception_room", "visual_object_segmentation_tracking", "compatible_with_minor_schema_extension",
        ("ObjectObservationCandidate",),
        spatial=["bbox"], confidence=["confidence", "detection_score"], identity=["class_name", "label"],
        temporal=["frame_ref", "timestamp"], confirmed=["bbox", "confidence", "class_name"]),
    _io("Whisper", "audio_speech_perception_room", "audio_speech_speaker", "compatible_with_minor_schema_extension",
        ("SpeechObservationCandidate", "IntentHintCandidate"),
        audio=["transcript", "segment_start", "segment_end"], temporal=["segment_start", "segment_end"],
        confidence=["avg_logprob", "confidence"], structured=["language"],
        confirmed=["transcript", "segment_start", "segment_end"], missing=["word_timestamps_native_all_modes"]),
    _io("faster_whisper", "audio_speech_perception_room", "audio_speech_speaker", "compatible_with_minor_schema_extension",
        ("SpeechObservationCandidate",),
        audio=["transcript", "word_timestamps"], temporal=["segment_start", "segment_end"],
        confidence=["avg_logprob"], confirmed=["transcript", "word_timestamps", "segment_start", "segment_end"]),
    _io("Luna_dataclass_ECS_skeleton", "ecs_entity_component_room", "ecs_entity_component", "compatible_with_current_candidate_schema",
        ("EntityComponentCandidate", "AttributeStateCandidate"),
        structured=["entity_id", "component_attach", "attribute_state"], luna_required=CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS,
        confirmed=list(CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS), missing=[], adjustment=True),
    _io("Luna_lightweight_event_graph_skeleton", "semantic_event_graph_room", "lightweight_semantic_event_graph", "compatible_with_current_candidate_schema",
        ("SemanticEventCandidate", "RiskZoneCandidate"),
        graph=["node_ref", "edge_ref", "relation_type"], structured=["event_semantics"],
        confirmed=["node_ref", "relation_type"], missing=[]),
    _io("Luna_geometry_simulator", "field_simulation_room", "field_simulation", "compatible_with_current_candidate_schema",
        ("FieldSimulationResultCandidate", "RiskProjectionCandidate"),
        spatial=["trajectory", "collision_hint"], temporal=["projection_window"], confirmed=["trajectory"], missing=[]),
    _io("rule_LLM_hybrid", "midplatform_reasoning_room", "midplatform_reasoning", "compatible_but_adapter_required",
        ("MidplatformReasoningCandidate",),
        input_type="structured_task_field_view", structured=["reason_codes", "route_candidate", "risk_candidate"],
        luna_required=["reason_codes", "non_execution_flags"], confirmed=["structured_io_feasible"],
        missing=["specific_model_schema"]),
    _io("SAM2", "visual_perception_room", "visual_object_segmentation_tracking", "compatible_with_minor_schema_extension",
        ("MaskObservationCandidate", "TrackObservationCandidate"),
        input_type="image_or_video", spatial=["mask_ref", "mask_payload_ref", "bbox"],
        identity=["tracklet", "track_id"], temporal=["frame_ref", "timestamp"],
        confidence=["confidence"], confirmed=["mask", "video_predictor", "masklet_propagation"],
        missing=["open_vocab_label_native"], notes="SAM2 docs: image/video segmentation, masklet propagation"),
    _io("Grounded_SAM2", "visual_perception_room", "visual_object_segmentation_tracking", "compatible_with_minor_schema_extension",
        ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate"),
        spatial=["bbox", "mask_ref"], identity=["track_id", "text_prompt_label"],
        confidence=["confidence"], confirmed=["open_vocab_grounding", "tracking", "segmentation"]),
    _io("GroundingDINO", "visual_perception_room", "visual_object_segmentation_tracking", "compatible_but_adapter_required",
        ("ObjectObservationCandidate",),
        spatial=["bbox"], identity=["text_prompt_label", "class_name"], confidence=["confidence"],
        confirmed=["bbox", "open_vocab_detection"], missing=["track_id"]),
    _io("SenseVoice", "audio_speech_perception_room", "audio_speech_speaker", "unclear_requires_later_review",
        ("SpeechObservationCandidate", "IntentHintCandidate"),
        audio=["transcript"], confidence=["confidence"], missing=["intent_hint_schema_confirmed"]),
    _io("pyannote_audio", "audio_speech_perception_room", "audio_speech_speaker", "compatible_but_adapter_required",
        ("SpeakerObservationCandidate",),
        audio=["speaker_segment_start", "speaker_segment_end"], identity=["speaker_label"],
        confidence=["speaker_confidence"], confirmed=["speaker_diarization_segments"],
        missing=["speaker_identity_fact_forbidden_by_design"]),
    _io("Kimera", "spatial_slam_scene_graph_room", "spatial_slam_dynamic_scene_graph", "reference_only_no_schema_commitment",
        ("PoseObservationCandidate", "SceneGraphReferenceCandidate"),
        spatial=["pose", "coordinate_frame"], graph=["object_node", "relation_edge"],
        confirmed=["vio", "metric_semantic_mapping"], missing=["wearable_realtime_confirmation"]),
    _io("Hydra", "spatial_slam_scene_graph_room", "spatial_slam_dynamic_scene_graph", "reference_only_no_schema_commitment",
        ("SceneGraphReferenceCandidate",),
        graph=["object_node", "room_node", "relation_edge"], confirmed=["realtime_3d_scene_graph"]),
    _io("HOV_SG", "spatial_slam_scene_graph_room", "spatial_slam_dynamic_scene_graph", "reference_only_no_schema_commitment",
        ("SceneGraphReferenceCandidate",), graph=["hierarchical_scene_graph"], confirmed=["open_vocab_hierarchy"]),
    _io("Open3DSG", "spatial_slam_scene_graph_room", "spatial_slam_dynamic_scene_graph", "reference_only_no_schema_commitment",
        ("SceneRelationCandidate",), graph=["object_relation_query"], confirmed=["point_cloud_scene_graph"]),
)

SKELETON_SCHEMA_ADJUSTMENT_PLAN: Dict[str, Any] = {
    "plan_id": "skeleton_schema_adjustment_plan_v1",
    "add_common_spatial_payload": True,
    "add_common_temporal_payload": True,
    "add_common_identity_payload": True,
    "add_common_confidence_payload": True,
    "add_common_graph_payload": True,
    "add_common_text_audio_payload": True,
    "observation_candidate_must_allow_spatial_payload": True,
    "field_continuity_must_allow_track_id": True,
    "text_region_as_field_entity_or_attribute": True,
    "reasoning_reads_structured_only_not_raw_audio_video": True,
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "io_precheck_not_model_selection",
    "io_precheck_not_download",
    "compatibility_not_production_ready",
    "schema_adjustment_not_runtime_implementation",
    "precheck_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Self-Developed-Skeleton-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Self-Developed Field-First Skeleton Implementation"
