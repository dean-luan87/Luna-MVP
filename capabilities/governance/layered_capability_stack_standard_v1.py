# -*- coding: utf-8 -*-
"""Layered Capability Stack Standard v1 — shared constants for all Luna modules."""

from __future__ import annotations

from typing import Any, Dict, Tuple

STANDARD_ID = "layered_capability_stack_standard_v1"
STANDARD_NAME = "Layered Capability Stack Standard"
STANDARD_NAME_ZH = "能力分层叠加标准"

STANDARD_EN = (
    "All capability modules must declare layered capability stack. "
    "No capability module may expose a high-level application ability "
    "without lower-layer candidate contracts and test boundaries."
)

STANDARD_ZH = (
    "所有能力模块必须声明能力分层。"
    "任何模块不得在没有底层候选合同和测试边界的情况下，直接暴露高层应用能力。"
)

GOVERNANCE_ADDENDUM_ID = "layered_governance_mapping_v1"
GOVERNANCE_ADDENDUM_NAME = "Layered Governance Mapping Addendum"
GOVERNANCE_PRINCIPLE_ZH = "治理原则一致，治理落点分层。"
GOVERNANCE_SLOGAN_ZH = "宪法精神统一，执法方式分层。"

MODULE_SUBMISSION_ARTIFACTS: Tuple[str, ...] = (
    "capability_stack_definition",
    "layered_governance_mapping",
)

UNIVERSAL_RULES: Tuple[str, ...] = (
    "each module must be layered",
    "each layer must have independent input and output",
    "each layer must have independent candidate objects",
    "each layer must have independent tests",
    "each layer must have independent failure routes",
    "upper layer depends on lower layer",
    "upper layer cannot reverse-override lower layer",
    "application layer cannot masquerade as foundation layer",
    "runtime layer cannot bypass governance layer",
    "no mega-capability mixing",
    "each module must submit layered_governance_mapping aligned to capability layers",
    "governance principles consistent across layers; enforcement granularity adapts per layer",
)

CAPABILITY_STACK_DEFINITION_FIELDS: Tuple[str, ...] = (
    "module_id",
    "capability_domain",
    "layer_count",
    "layer_definitions",
    "lower_layer_dependencies",
    "candidate_object_set",
    "input_contracts",
    "output_contracts",
    "decision_review_scope",
    "test_case_set",
    "failure_route_set",
    "forbidden_cross_layer_override",
    "runtime_boundary",
    "memory_worldmodel_boundary",
)

LAYER_DEFINITION_FIELDS: Tuple[str, ...] = (
    "layer_id",
    "layer_name",
    "capability_scope",
    "capability_boundary",
    "input_sources",
    "output_objects",
    "required_lower_layers",
    "candidate_objects",
    "integration_path",
    "decision_review_scope",
    "test_scope",
    "failure_routes",
    "forbidden_cross_layer_override",
    "metrics",
)

VOICE_CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "voice_layer_1",
        "layer_name": "Audio Capture Candidate",
        "capability_scope": "audio_capture_candidate",
    },
    {
        "layer_id": "voice_layer_2",
        "layer_name": "ASR / Speech Recognition",
        "capability_scope": "asr_speech_recognition_candidate",
        "required_lower_layers": ["voice_layer_1"],
    },
    {
        "layer_id": "voice_layer_3",
        "layer_name": "Speaker / Intent / Emotion Signal",
        "capability_scope": "speaker_intent_emotion_signal_candidate",
        "required_lower_layers": ["voice_layer_2"],
    },
    {
        "layer_id": "voice_layer_4",
        "layer_name": "Dialogue Context Integration",
        "capability_scope": "dialogue_context_integration",
        "required_lower_layers": ["voice_layer_3"],
    },
    {
        "layer_id": "voice_layer_5",
        "layer_name": "Speech Gate / Output Policy",
        "capability_scope": "speech_gate_output_policy",
        "required_lower_layers": ["voice_layer_4"],
    },
    {
        "layer_id": "voice_layer_6",
        "layer_name": "Voice Output / TTS Runtime",
        "capability_scope": "voice_output_tts_runtime",
        "required_lower_layers": ["voice_layer_5"],
        "runtime_layer": True,
        "later": True,
    },
)

OCR_CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "ocr_layer_1",
        "layer_name": "Text Region Detection",
        "capability_scope": "text_region_detection",
    },
    {
        "layer_id": "ocr_layer_2",
        "layer_name": "OCR Reading Candidate",
        "capability_scope": "ocr_reading_candidate",
        "required_lower_layers": ["ocr_layer_1"],
    },
    {
        "layer_id": "ocr_layer_3",
        "layer_name": "Text Structure Understanding",
        "capability_scope": "text_structure_understanding",
        "required_lower_layers": ["ocr_layer_2"],
    },
    {
        "layer_id": "ocr_layer_4",
        "layer_name": "Semantic Context / Signage Meaning",
        "capability_scope": "semantic_context_signage_meaning",
        "required_lower_layers": ["ocr_layer_3"],
    },
    {
        "layer_id": "ocr_layer_5",
        "layer_name": "Task / Navigation / Reading Application",
        "capability_scope": "task_navigation_reading_application",
        "required_lower_layers": ["ocr_layer_4"],
        "application_layer": True,
    },
    {
        "layer_id": "ocr_layer_6",
        "layer_name": "Memory / WorldModel Admission",
        "capability_scope": "memory_worldmodel_admission",
        "required_lower_layers": ["ocr_layer_5"],
        "later": True,
    },
)

MAP_NAVIGATION_CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "map_layer_1",
        "layer_name": "Location Candidate",
        "capability_scope": "location_candidate",
    },
    {
        "layer_id": "map_layer_2",
        "layer_name": "Spatial Context Candidate",
        "capability_scope": "spatial_context_candidate",
        "required_lower_layers": ["map_layer_1"],
    },
    {
        "layer_id": "map_layer_3",
        "layer_name": "Route Context Candidate",
        "capability_scope": "route_context_candidate",
        "required_lower_layers": ["map_layer_2"],
    },
    {
        "layer_id": "map_layer_4",
        "layer_name": "Scene-Spatial Alignment",
        "capability_scope": "scene_spatial_alignment",
        "required_lower_layers": ["map_layer_3"],
    },
    {
        "layer_id": "map_layer_5",
        "layer_name": "Navigation Application Decision",
        "capability_scope": "navigation_application_decision",
        "required_lower_layers": ["map_layer_4"],
        "application_layer": True,
    },
    {
        "layer_id": "map_layer_6",
        "layer_name": "Navigation Execution Runtime",
        "capability_scope": "navigation_execution_runtime",
        "required_lower_layers": ["map_layer_5"],
        "runtime_layer": True,
        "later": True,
    },
)

MEMORY_CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "memory_layer_1",
        "layer_name": "Retrieval Candidate",
        "capability_scope": "retrieval_candidate",
    },
    {
        "layer_id": "memory_layer_2",
        "layer_name": "Memory Relevance Candidate",
        "capability_scope": "memory_relevance_candidate",
        "required_lower_layers": ["memory_layer_1"],
    },
    {
        "layer_id": "memory_layer_3",
        "layer_name": "Memory Context Integration",
        "capability_scope": "memory_context_integration",
        "required_lower_layers": ["memory_layer_2"],
    },
    {
        "layer_id": "memory_layer_4",
        "layer_name": "Memory Write Proposal",
        "capability_scope": "memory_write_proposal",
        "required_lower_layers": ["memory_layer_3"],
    },
    {
        "layer_id": "memory_layer_5",
        "layer_name": "Memory Admission / Validation",
        "capability_scope": "memory_admission_validation",
        "required_lower_layers": ["memory_layer_4"],
    },
    {
        "layer_id": "memory_layer_6",
        "layer_name": "Personal Continuity Update",
        "capability_scope": "personal_continuity_update",
        "required_lower_layers": ["memory_layer_5"],
        "later": True,
    },
)

EMOTION_CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "emotion_layer_1",
        "layer_name": "Emotion Signal Candidate",
        "capability_scope": "emotion_signal_candidate",
    },
    {
        "layer_id": "emotion_layer_2",
        "layer_name": "Relationship Context Candidate",
        "capability_scope": "relationship_context_candidate",
        "required_lower_layers": ["emotion_layer_1"],
    },
    {
        "layer_id": "emotion_layer_3",
        "layer_name": "Social Adaptation Hint",
        "capability_scope": "social_adaptation_hint",
        "required_lower_layers": ["emotion_layer_2"],
    },
    {
        "layer_id": "emotion_layer_4",
        "layer_name": "Response Tone / Rhythm Influence",
        "capability_scope": "response_tone_rhythm_influence",
        "required_lower_layers": ["emotion_layer_3"],
    },
    {
        "layer_id": "emotion_layer_5",
        "layer_name": "Personal Continuity / Emotion State Admission",
        "capability_scope": "personal_continuity_emotion_state_admission",
        "required_lower_layers": ["emotion_layer_4"],
    },
    {
        "layer_id": "emotion_layer_6",
        "layer_name": "Evolution / Social Learning",
        "capability_scope": "evolution_social_learning",
        "required_lower_layers": ["emotion_layer_5"],
        "later": True,
    },
)

DOMAIN_STACK_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {"domain_id": "voice", "stack_name": "Voice Capability Stack", "layers": VOICE_CAPABILITY_STACK_LAYERS},
    {"domain_id": "ocr", "stack_name": "OCR Capability Stack", "layers": OCR_CAPABILITY_STACK_LAYERS},
    {
        "domain_id": "map_navigation",
        "stack_name": "Map-Navigation Capability Stack",
        "layers": MAP_NAVIGATION_CAPABILITY_STACK_LAYERS,
    },
    {"domain_id": "memory", "stack_name": "Memory Capability Stack", "layers": MEMORY_CAPABILITY_STACK_LAYERS},
    {"domain_id": "emotion", "stack_name": "Emotion Capability Stack", "layers": EMOTION_CAPABILITY_STACK_LAYERS},
)
