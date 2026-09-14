# -*- coding: utf-8 -*-
"""Luna Vision Test Source Backup Pool — types v1.

Establishes a Luna RGB-first vision TEST-SOURCE backup pool. Open / public research
datasets (Roboflow Universe, COCO, Open Images, LVIS, ADE20K, TextOCR, Visual Genome,
BDD100K, Cityscapes, Mapillary Vistas, Ego4D, EPIC-KITCHENS, EgoTracks, RefEgo) are
registered strictly as test / replay / benchmark sources — never as training main data
or fact sources. This phase is Registry + Admission Matrix + Review only: no dataset
download, no training, no live camera, no runtime, no navigation/action/speech/fact_write.

  dataset source
  -> license / source admission
  -> annotation adapter
  -> Luna evidence candidate sample
  -> integrated replay
  -> Field / Task / Guidance candidate path
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Luna-Vision-Test-Source-Backup-Pool-v1-001"
SCOPE = "luna_vision_test_source_backup_pool"
SOURCE_CHAIN = "luna_vision_test_source_backup_pool_v1"

POOL_PRINCIPLE_ZH = (
    "建立 Luna RGB-first 视觉测试源备用池，统一收录 Roboflow Universe、COCO、Open Images、LVIS、"
    "ADE20K、TextOCR、Visual Genome、BDD100K、Cityscapes、Mapillary Vistas、Ego4D、EPIC-KITCHENS、"
    "EgoTracks、RefEgo 等开放/公开研究数据源，仅作为测试源 / replay source / benchmark source，"
    "不作为训练主数据或事实来源。本阶段只做 Backup Pool Registry + Admission Matrix + Review，"
    "不下载大规模数据，不训练模型，不接 live camera，不启动 runtime，"
    "不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"
TEST_SOURCE_POOL_MODE = "registry_and_admission_only"
COMMERCIAL_USE_DEFAULT = "unknown_until_license_verified"
INTERFACE_ADAPTER_REF = "external_vision_interface_adapter"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
RGB_VISION_PLANNING_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
)
RTAB_MULTI_EXPORT_CLOSURE_REF = (
    "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    RGB_VISION_PLANNING_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
)

# --------------------------------------------------------------------------- #
# Allowed-use / commercial-use vocab
# --------------------------------------------------------------------------- #
ALLOWED_USE_TEST_ONLY = "test_only"
ALLOWED_USE_RESEARCH_TEST_ONLY = "research_test_only"
ALLOWED_USE_BENCHMARK_ONLY = "benchmark_only"
ALLOWED_USE_UNKNOWN = "unknown_until_license_verified"

ALLOWED_USE_VALUES: Tuple[str, ...] = (
    ALLOWED_USE_TEST_ONLY,
    ALLOWED_USE_RESEARCH_TEST_ONLY,
    ALLOWED_USE_BENCHMARK_ONLY,
    ALLOWED_USE_UNKNOWN,
)

COMMERCIAL_UNKNOWN = "unknown_until_license_verified"
COMMERCIAL_PER_DATASET = "per_dataset_license_required"
COMMERCIAL_NON_COMMERCIAL = "non_commercial"

COMMERCIAL_USE_VALUES: Tuple[str, ...] = (
    COMMERCIAL_UNKNOWN,
    COMMERCIAL_PER_DATASET,
    COMMERCIAL_NON_COMMERCIAL,
)

# Fields every registry item must carry.
REGISTRY_ITEM_REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_id",
    "source_name",
    "source_family",
    "priority",
    "task_family",
    "annotation_types",
    "candidate_output_types",
    "license_ref_required",
    "source_chain_required",
    "annotation_origin_required",
    "sample_origin_required",
    "commercial_use_status",
    "allowed_use",
    "integrated_replay_compatible",
    "risk_notes",
)

# Ordered source ids (P0 -> P1 -> P2).
SOURCE_IDS: Tuple[str, ...] = (
    "roboflow_universe",
    "coco",
    "open_images_v7",
    "lvis",
    "ade20k",
    "textocr",
    "visual_genome",
    "bdd100k",
    "cityscapes",
    "mapillary_vistas",
    "ego4d",
    "epic_kitchens",
    "egotracks",
    "refego",
)

SOURCE_REGISTERED_GO_KEYS: Tuple[str, ...] = tuple(f"{sid}_registered" for sid in SOURCE_IDS)

GOVERNANCE_FIELDS: Tuple[str, ...] = (
    "dataset_ref",
    "license_ref",
    "source_chain",
    "annotation_origin",
    "sample_origin",
    "task_family",
    "allowed_use",
    "confidence",
    "candidate_mapping",
    "commercial_use_status",
)

POOL_GOVERNANCE_RULES: Tuple[str, ...] = (
    "backup_pool_is_not_training_admission",
    "backup_pool_is_not_runtime_admission",
    "dataset_source_must_pass_license_source_admission_before_use",
    "roboflow_dataset_license_must_be_checked_per_dataset",
    "non_commercial_datasets_must_be_marked_research_test_only",
    "annotation_is_evidence_candidate_not_fact",
    "dataset_label_is_not_luna_truth",
    "dataset_output_must_pass_interface_adapter_before_field_task_guidance",
    "source_chain_license_ref_annotation_origin_sample_origin_must_be_preserved",
    "commercial_use_is_unknown_until_license_verified",
    "integrated_validation_mode_must_be_used",
    "rgb_first_hardware_baseline_must_be_preserved",
    "no_live_camera_no_live_sensor_no_map_api_no_gps_no_ros",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

POOL_OBJECT_TYPES: Tuple[str, ...] = (
    "VisionTestSourceBackupPoolProfile",
    "VisionTestSourceRegistryItem",
    "VisionDatasetLicenseAdmissionPolicy",
    "VisionAnnotationFormatPolicy",
    "VisionEvidenceCandidateMappingPolicy",
    "VisionTestSourceRiskPolicy",
    "VisionTestSourceBackupPoolDecision",
)

FINAL_DECISION_GO = "LUNA_VISION_TEST_SOURCE_BACKUP_POOL_GO"
FINAL_DECISION_BLOCKED = "LUNA_VISION_TEST_SOURCE_BACKUP_POOL_BLOCKED"

NEXT_PHASE_REF = "Phase-RGB-Vision-Test-Source-Integrated-Evidence-Replay-DryRun-v1-001"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_required": True,
    "single_loader_validation_not_used": True,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "real_navigation_started": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class VisionTestSourceBackupPoolProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    rgb_vision_planning_ref: str
    rtab_multi_export_closure_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    vision_hardware_baseline: str
    system_objective: str
    test_source_pool_mode: str
    commercial_use_default: str
    target_internal_format: str
    target_entrypoint: str
    governance_fields: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class VisionTestSourceRegistryItem:
    source_id: str
    source_name: str
    source_family: str
    priority: str
    task_family: Tuple[str, ...]
    annotation_types: Tuple[str, ...]
    candidate_output_types: Tuple[str, ...]
    license_ref_required: bool
    source_chain_required: bool
    annotation_origin_required: bool
    sample_origin_required: bool
    commercial_use_status: str
    allowed_use: str
    integrated_replay_compatible: bool
    risk_notes: str
    use_case: str = ""
    license_policy: str = ""


@dataclass(frozen=True)
class VisionDatasetLicenseAdmissionPolicy:
    policy_ref: str
    license_ref_required: bool
    source_chain_required: bool
    annotation_origin_required: bool
    sample_origin_required: bool
    commercial_use_default: str
    per_dataset_license_required_for_roboflow: bool
    non_commercial_marked_research_test_only: bool
    commercial_use_unknown_until_verified: bool


@dataclass(frozen=True)
class VisionAnnotationFormatPolicy:
    policy_ref: str
    recognized_annotation_families: Tuple[str, ...]
    annotation_as_evidence_candidate: bool
    dataset_label_not_fact: bool


@dataclass(frozen=True)
class VisionEvidenceCandidateMappingPolicy:
    policy_ref: str
    interface_adapter_required: bool
    native_output_direct_to_field_blocked: bool
    candidate_only: bool
    integrated_replay_compatible_for_all: bool


@dataclass(frozen=True)
class VisionTestSourceRiskPolicy:
    policy_ref: str
    backup_pool_not_training_admission: bool
    backup_pool_not_runtime_admission: bool
    dataset_download_blocked: bool
    training_use_blocked: bool
    runtime_activation_blocked: bool
    rgb_first_hardware_baseline_preserved: bool
    no_live_camera: bool
    no_navigation_action_speech_fact_write: bool


@dataclass(frozen=True)
class VisionTestSourceBackupPoolDecision:
    decision_ref: str
    backup_pool_profile_count: int
    registry_item_count: int
    p0_source_count: int
    p1_source_count: int
    p2_source_count: int
    license_ref_required_for_all: bool
    source_chain_required_for_all: bool
    annotation_origin_required_for_all: bool
    sample_origin_required_for_all: bool
    commercial_use_unknown_until_verified: bool
    non_commercial_sources_marked_research_test_only: bool
    interface_adapter_required: bool
    integrated_replay_compatible_for_all: bool
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
