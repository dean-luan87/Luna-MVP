# -*- coding: utf-8 -*-
"""Field-First adapter contracts v1 — interface definitions only."""

from __future__ import annotations

from typing import Any, Dict, Tuple

ADAPTER_CONTRACT_ID = "field_first_model_adapter_contract_v1"

ADAPTER_REQUIRED_FIELDS: Tuple[str, ...] = (
    "adapter_id", "model_ref", "model_room", "source_type", "input_schema_ref",
    "output_candidate_type", "confidence_mapping", "freshness_mapping",
    "failure_mode_mapping", "traceability_mapping", "governance_mapping",
    "non_execution_flags", "unsupported_output_policy", "placeholder_only",
)

CANDIDATE_OUTPUT_CONTRACTS: Tuple[Dict[str, Any], ...] = (
    {"candidate_type": "ObservationCandidate", "layer": "source_intake"},
    {"candidate_type": "ObjectObservationCandidate", "layer": "visual_perception"},
    {"candidate_type": "MaskObservationCandidate", "layer": "visual_perception"},
    {"candidate_type": "TrackObservationCandidate", "layer": "visual_perception"},
    {"candidate_type": "TextObservationCandidate", "layer": "ocr_text"},
    {"candidate_type": "SpeechObservationCandidate", "layer": "audio_speech"},
    {"candidate_type": "PoseObservationCandidate", "layer": "spatial_scene_graph"},
    {"candidate_type": "SceneGraphReferenceCandidate", "layer": "spatial_scene_graph"},
    {"candidate_type": "EntityComponentCandidate", "layer": "ecs"},
    {"candidate_type": "SemanticEventCandidate", "layer": "semantic_event_graph"},
    {"candidate_type": "FieldSimulationResultCandidate", "layer": "field_simulation"},
    {"candidate_type": "MidplatformReasoningCandidate", "layer": "midplatform_reasoning"},
)

PROHIBITED_ADAPTER_IMPORTS: Tuple[str, ...] = (
    "torch", "cv2", "paddle", "transformers", "tensorflow", "onnxruntime",
)

PROHIBITED_ADAPTER_ACTIONS: Tuple[str, ...] = (
    "load_checkpoint", "call_inference", "subprocess_clone", "subprocess_download",
    "pip_install_large_model_dependency",
)
