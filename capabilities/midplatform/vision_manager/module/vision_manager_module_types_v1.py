from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

VISION_MANAGER_MODULE_STATUSES_V1: Tuple[str, ...] = (
    "invalid_observation_request",
    "frame_quality_insufficient",
    "no_attention_target",
    "model_handoff_blocked",
    "ownership_blocked",
    "degraded_without_model",
    "human_correction_candidate",
    "ready",
)


@dataclass(frozen=True)
class VisionManagerModuleRequestV1:
    request_id: str
    capability: str
    observation_request: str
    attention_target: str
    frame_quality: str
    model_test_lens: str
    ownership_ok: bool
    version_snapshot: Dict[str, str]
    trace_context: Dict[str, Any]


@dataclass(frozen=True)
class VisionManagerModuleResultV1:
    module_status: str
    admitted_visual_input: bool
    frame_quality_status: str
    attention_plan: Dict[str, Any]
    roi_candidates: Tuple[Dict[str, Any], ...]
    region_candidates: Tuple[Dict[str, Any], ...]
    model_capability_request: Dict[str, Any]
    model_handoff_candidate: Dict[str, Any]
    detection_candidates: Tuple[Dict[str, Any], ...]
    segmentation_candidates: Tuple[Dict[str, Any], ...]
    tracking_candidates: Tuple[Dict[str, Any], ...]
    scene_evidence_candidates: Tuple[Dict[str, Any], ...]
    composed_visual_evidence: Dict[str, Any]
    correction_candidates: Tuple[Dict[str, Any], ...]
    degradation_plan: Dict[str, Any]
    diagnostics: Dict[str, Any]
    rejection_reasons: Tuple[str, ...]
    trace_ref: str
    replay_key: str
    camera_invoked: bool
    visual_model_invoked: bool
    ocr_provider_invoked: bool
    segmentation_runtime_invoked: bool
    tracking_runtime_invoked: bool
    world_model_written: bool
    memory_written: bool
    fact_written: bool
    navigation_action_triggered: bool
    production_runtime_executed: bool
