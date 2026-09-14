# -*- coding: utf-8 -*-
"""Field-First adapter placeholders v1 — registry only, no inference."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.model_adapters.field_first_adapter_types_v1 import ModelAdapterPlaceholder

ADAPTER_PLACEHOLDERS: Tuple[ModelAdapterPlaceholder, ...] = (
    ModelAdapterPlaceholder("visual_sam2_placeholder_v1", "SAM2", "visual_perception_room", ("MaskObservationCandidate", "TrackObservationCandidate")),
    ModelAdapterPlaceholder("visual_grounded_sam2_placeholder_v1", "Grounded_SAM2", "visual_perception_room", ("ObjectObservationCandidate", "MaskObservationCandidate", "TrackObservationCandidate")),
    ModelAdapterPlaceholder("visual_bytetrack_placeholder_v1", "ByteTrack", "visual_perception_room", ("TrackObservationCandidate",)),
    ModelAdapterPlaceholder("visual_yolo_placeholder_v1", "YOLO_lightweight", "visual_perception_room", ("ObjectObservationCandidate",)),
    ModelAdapterPlaceholder("ocr_paddleocr_placeholder_v1", "PaddleOCR", "ocr_text_perception_room", ("TextObservationCandidate", "TextRegionCandidate")),
    ModelAdapterPlaceholder("ocr_rapidocr_placeholder_v1", "RapidOCR", "ocr_text_perception_room", ("TextObservationCandidate", "TextRegionCandidate")),
    ModelAdapterPlaceholder("speech_whisper_placeholder_v1", "Whisper", "audio_speech_perception_room", ("SpeechObservationCandidate",)),
    ModelAdapterPlaceholder("speech_sensevoice_placeholder_v1", "SenseVoice", "audio_speech_perception_room", ("SpeechObservationCandidate", "IntentHintCandidate")),
    ModelAdapterPlaceholder("speech_pyannote_placeholder_v1", "pyannote_audio", "audio_speech_perception_room", ("SpeakerObservationCandidate",)),
    ModelAdapterPlaceholder("spatial_kimera_placeholder_v1", "Kimera", "spatial_slam_scene_graph_room", ("SpatialObservationCandidate", "SceneGraphReferenceCandidate")),
    ModelAdapterPlaceholder("spatial_hydra_placeholder_v1", "Hydra", "spatial_slam_scene_graph_room", ("SceneGraphReferenceCandidate",)),
    ModelAdapterPlaceholder("spatial_hovsg_placeholder_v1", "HOV_SG", "spatial_slam_scene_graph_room", ("SceneGraphReferenceCandidate",)),
    ModelAdapterPlaceholder("spatial_open3dsg_placeholder_v1", "Open3DSG", "spatial_slam_scene_graph_room", ("SceneRelationCandidate",)),
    ModelAdapterPlaceholder("ecs_luna_dataclass_placeholder_v1", "Luna_dataclass_ECS", "ecs_entity_component_room", ("EntityComponentCandidate", "AttributeStateCandidate")),
    ModelAdapterPlaceholder("semantic_luna_event_graph_placeholder_v1", "Luna_event_graph_skeleton", "semantic_event_graph_room", ("SemanticEventCandidate", "RiskZoneCandidate")),
    ModelAdapterPlaceholder("simulation_luna_geometry_placeholder_v1", "Luna_geometry_simulator", "field_simulation_room", ("FieldSimulationResultCandidate",)),
    ModelAdapterPlaceholder("reasoning_structured_llm_placeholder_v1", "structured_LLM_reasoning", "midplatform_reasoning_room", ("MidplatformReasoningCandidate",)),
)

def list_adapter_placeholders() -> Tuple[ModelAdapterPlaceholder, ...]:
    return ADAPTER_PLACEHOLDERS
