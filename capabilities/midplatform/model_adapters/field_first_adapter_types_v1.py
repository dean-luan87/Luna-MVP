# -*- coding: utf-8 -*-
"""Field-First adapter placeholder types v1 — no real model imports."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

MODEL_ROOM_IDS: Tuple[str, ...] = (
    "visual_perception_room",
    "ocr_text_perception_room",
    "audio_speech_perception_room",
    "spatial_slam_scene_graph_room",
    "ecs_entity_component_room",
    "semantic_event_graph_room",
    "field_simulation_room",
    "midplatform_reasoning_room",
)

PREINSTALL_STATUS_OPTIONS: Tuple[str, ...] = (
    "directory_only",
    "adapter_placeholder_only",
    "document_review_pending",
    "reference_only_now",
    "near_term_candidate_pending_review",
    "deferred_due_to_runtime_cost",
    "blocked_until_download_authorized",
)

MANIFEST_FIELDS: Tuple[str, ...] = (
    "model_project_id", "display_name", "model_room", "operation_node_refs",
    "expected_candidate_outputs", "source_url_placeholder", "docs_url_placeholder",
    "license_status", "weights_required", "weights_downloaded", "download_authorized",
    "runtime_build_required", "runtime_build_completed", "inference_ready",
    "adapter_required", "adapter_placeholder_created", "capability_review_required",
    "capability_review_status", "recommended_preinstall_status", "reason_for_status",
    "hardware_risk", "integration_risk", "notes",
)


@dataclass(frozen=True)
class ModelRoomRef:
    room_id: str
    display_name: str
    directory_path: str


@dataclass(frozen=True)
class ModelAdapterPlaceholder:
    adapter_id: str
    model_project_id: str
    model_room: str
    output_candidate_types: Tuple[str, ...]
    placeholder_only: bool = True
    inference_allowed: bool = False


@dataclass(frozen=True)
class ModelPreinstallCandidate:
    model_project_id: str
    display_name: str
    model_room: str
    operation_node_refs: Tuple[str, ...]
    expected_candidate_outputs: Tuple[str, ...]
    weights_downloaded: bool = False
    download_authorized: bool = False
    inference_ready: bool = False
    runtime_build_completed: bool = False
    adapter_required: bool = True
    adapter_placeholder_created: bool = True
    capability_review_required: bool = True
    capability_review_status: str = "pending"
    recommended_preinstall_status: str = "document_review_pending"


@dataclass(frozen=True)
class ModelCapabilityReviewTarget:
    target_id: str
    model_project_id: str
    operation_node_id: str
    model_room: str
    review_priority: str
    review_reason: str
    current_preinstall_action: str


@dataclass(frozen=True)
class ModelDownloadAuthorizationStatus:
    model_project_id: str
    download_authorized: bool = False
    authorization_reason: str = "capability_review_not_complete"


@dataclass(frozen=True)
class ModelRuntimeStatus:
    model_project_id: str
    runtime_build_completed: bool = False
    inference_ready: bool = False
    weights_downloaded: bool = False


@dataclass(frozen=True)
class CandidateOutputContract:
    candidate_type: str
    is_fact: bool = False
    requires_adapter: bool = True
    requires_validator: bool = True
