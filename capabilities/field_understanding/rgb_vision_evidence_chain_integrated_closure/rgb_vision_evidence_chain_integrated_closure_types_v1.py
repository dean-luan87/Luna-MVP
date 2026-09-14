# -*- coding: utf-8 -*-
"""RGB Vision Evidence Chain Integrated Closure — types v1.

Integrated closure for Luna's RGB-first vision evidence chain. Seals, as one RGB
vision evidence chain baseline: RGB Vision OCR Segmentation integrated planning +
dry-run, Roboflow dataset integrated dry-run, multi test-source integrated replay,
the Vision Test Source Backup Pool, and the RGB-first / cognition-first hardware
route.

  rgb frame/video + object/segmentation/tracking/ocr/monocular-depth/scene-relation
  + roboflow / coco / ade20k / textocr / visual_genome test sources
  -> source / license admission
  -> external vision interface adapter
  -> luna rgb-first evidence candidates
  -> Field / Task / Guidance candidate replay

Closure + Matrix Review only. No large dataset download, no model training, no live
camera, no vision runtime, no real sensors, no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
SCOPE = "rgb_vision_evidence_chain_integrated_closure"
SOURCE_CHAIN = "rgb_vision_evidence_chain_integrated_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "对 Luna RGB-first vision evidence chain 做 integrated closure。统一封存 RGB Vision OCR Segmentation "
    "integrated replay、Roboflow dataset integrated replay、多测试源 integrated replay、Vision Test "
    "Source Backup Pool，以及 RGB-first / cognition-first 硬件路线，归入同一条视觉证据链 baseline。只做 "
    "Closure + Matrix Review，集中验证不拆单一源；不下载大规模数据集，不训练模型，不接 live camera，不启动"
    "视觉 runtime，不接真实传感器，不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "rgb_vision_evidence_chain_integrated_closure_only"
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"
DEPTH_HARDWARE_DEFAULT = "not_required"
TOF_STEREO_DEPTH_ROLE = "optional_auxiliary_only"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_vision_interface_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
RGB_VISION_PLANNING_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
)
RGB_VISION_DRYRUN_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
)
ROBOFLOW_DATASET_DRYRUN_REF = (
    "Phase-RGB-Vision-Roboflow-Dataset-Integrated-Evidence-Replay-DryRun-v1-001"
)
VISION_TEST_SOURCE_BACKUP_POOL_REF = "Phase-Luna-Vision-Test-Source-Backup-Pool-v1-001"
VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF = (
    "Phase-RGB-Vision-Test-Source-Integrated-Evidence-Replay-DryRun-v1-001"
)
RTAB_MULTI_EXPORT_CLOSURE_REF = (
    "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)
SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
STAGE_REFS: Tuple[str, ...] = (
    "rgb_vision_integrated_planning",
    "rgb_vision_integrated_dryrun",
    "roboflow_dataset_integrated_dryrun",
    "vision_test_source_backup_pool",
    "vision_test_source_integrated_replay",
)

# --------------------------------------------------------------------------- #
# Source coverage closure
# --------------------------------------------------------------------------- #
SOURCE_COVERAGE_IDS: Tuple[str, ...] = (
    "rgb_frame_or_video",
    "object_detection_output",
    "segmentation_output",
    "tracking_output",
    "ocr_text_output",
    "monocular_depth_or_vio_output",
    "scene_relation_output",
    "roboflow_universe_test_source",
    "coco_test_source",
    "ade20k_test_source",
    "textocr_test_source",
    "visual_genome_test_source",
    "vision_test_source_backup_pool",
)

SOURCE_COVERED_GO_KEYS: Tuple[str, ...] = tuple(f"{s}_covered" for s in SOURCE_COVERAGE_IDS)

# --------------------------------------------------------------------------- #
# Candidate type coverage closure
# --------------------------------------------------------------------------- #
CANDIDATE_TYPE_IDS: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "text_evidence_candidate",
    "spatial_hint_candidate",
    "attribute_candidate",
    "scene_relation_candidate",
    "task_context_candidate",
    "task_risk_candidate",
    # Visual Symbol Evidence Extension (schema/governance/coverage only)
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
)

CANDIDATE_TYPE_COVERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_covered" for c in CANDIDATE_TYPE_IDS
)

# --------------------------------------------------------------------------- #
# Visual Symbol Evidence Extension
# --------------------------------------------------------------------------- #
# Schema/governance/closure coverage only — no model, no algorithm, no real
# image recognition in this phase. Color / shape / symbol are NOT facts; symbol
# meaning must be validated against OCR / object / region / scene context and
# must never directly trigger navigation / action / speech / fact_write.
SYMBOL_MEANING_CANDIDATE_ID = "symbol_meaning_candidate"

# meaning_ref : (color + shape + context) -> meaning candidate (candidate-only)
SYMBOL_MEANING_MAPPINGS: Tuple[Dict[str, str], ...] = (
    {
        "meaning_ref": "exit_direction_candidate",
        "color_hint": "green",
        "shape_hint": "arrow",
        "context_hint": "doorway/context",
        "requires_context_validation": "true",
    },
    {
        "meaning_ref": "danger_or_no_entry_candidate",
        "color_hint": "red",
        "shape_hint": "prohibition/cross/stop",
        "context_hint": "object/region/scene",
        "requires_context_validation": "true",
    },
    {
        "meaning_ref": "caution_candidate",
        "color_hint": "yellow",
        "shape_hint": "triangle/line/border",
        "context_hint": "object/region/scene",
        "requires_context_validation": "true",
    },
    {
        "meaning_ref": "direction_hint_candidate",
        "color_hint": "any",
        "shape_hint": "arrow",
        "context_hint": "direction",
        "requires_context_validation": "true",
    },
    {
        "meaning_ref": "facility_hint_candidate",
        "color_hint": "any",
        "shape_hint": "icon",
        "context_hint": "context",
        "requires_context_validation": "true",
    },
)

SYMBOL_MEANING_REFS: Tuple[str, ...] = tuple(m["meaning_ref"] for m in SYMBOL_MEANING_MAPPINGS)

VISUAL_SYMBOL_EXTENSION_GO_KEYS: Tuple[str, ...] = (
    "color_evidence_candidate_covered",
    "shape_evidence_candidate_covered",
    "visual_symbol_candidate_covered",
    "symbol_meaning_candidate_candidate_only",
    "color_shape_symbol_not_fact",
    "visual_symbol_not_direct_navigation",
    "visual_symbol_not_direct_speech",
    "visual_symbol_requires_context_validation",
)

# --------------------------------------------------------------------------- #
# Replay path closure
# --------------------------------------------------------------------------- #
REPLAY_PATH_GO_KEYS: Tuple[str, ...] = (
    "adapter_mapping_required",
    "source_admission_required",
    "source_chain_preserved",
    "confidence_preserved",
    "origin_metadata_preserved",
    "field_candidate_path_closed",
    "task_candidate_path_closed",
    "guidance_candidate_path_closed",
    "guidance_candidate_remains_candidate",
    "speech_gate_candidate_not_tts",
    "action_safety_candidate_exists",
    "observation_only_scope_preserved",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "rgb_vision_evidence_chain_closure_is_not_runtime_activation",
    "integrated_validation_mode_must_be_used_no_single_source_closure_split",
    "rgb_first_remains_default_vision_hardware_baseline",
    "tof_stereo_industrial_depth_remains_optional_auxiliary_only",
    "luna_objective_remains_cognitive_world_reconstruction_not_industrial_metric_measurement",
    "external_vision_output_must_pass_interface_adapter_before_luna_internal_format",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "dataset_labels_are_not_luna_truth",
    "annotation_is_evidence_candidate_not_fact",
    "ocr_output_is_text_evidence_not_fact",
    "segmentation_output_is_region_evidence_not_route_activation",
    "tracking_output_is_motion_risk_evidence_not_action_trigger",
    "monocular_depth_vio_output_is_spatial_hint_not_field_identity",
    "scene_relation_output_is_relation_candidate_not_final_interpretation",
    "source_chain_confidence_origin_metadata_must_be_preserved",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "no_live_camera_no_live_sensor_no_real_gps_no_map_api_no_ros",
    "no_navigation_no_action_no_speech_no_fact_write",
    "dataset_download_training_use_commercial_runtime_not_approved",
    "color_shape_visual_symbol_evidence_is_part_of_rgb_vision_evidence_chain",
    "color_is_not_fact_shape_is_not_fact_visual_symbol_is_not_fact",
    "symbol_meaning_must_be_validated_against_ocr_object_region_scene_context",
    "visual_symbol_must_not_directly_trigger_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "this_closure_seals_the_rgb_vision_evidence_chain_baseline",
)

CLOSURE_OBJECT_TYPES: Tuple[str, ...] = (
    "RGBVisionEvidenceChainClosureProfile",
    "RGBVisionEvidenceChainStageRef",
    "RGBVisionSourceCoverageClosure",
    "RGBVisionCandidateTypeCoverageClosure",
    "RGBVisionDatasetTestSourceClosure",
    "RGBVisionReplayPathClosure",
    "RGBVisionSafetyBoundaryClosure",
    "RGBVisionVisualSymbolEvidenceExtensionClosure",
    "RGBVisionEvidenceChainIntegratedClosureDecision",
)

FINAL_DECISION_GO = "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO"
FINAL_DECISION_BLOCKED = "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "single_source_validation_not_used": True,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RGBVisionEvidenceChainClosureProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    vision_test_source_integrated_replay_ref: str
    vision_test_source_backup_pool_ref: str
    slam_backend_evidence_chain_closure_ref: str
    interface_adapter_ref: str
    vision_hardware_baseline: str
    system_objective: str
    depth_hardware_default: str
    tof_stereo_depth_role: str
    target_entrypoint: str
    runtime_trial_mode: str
    stage_refs: Tuple[str, ...]
    source_coverage_ids: Tuple[str, ...]
    candidate_type_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RGBVisionEvidenceChainStageRef:
    stage_ref: str
    phase_ref: str
    expected_final_decision: str
    coverage: Tuple[str, ...]


@dataclass(frozen=True)
class RGBVisionSourceCoverageClosure:
    closure_ref: str
    source_coverage_ids: Tuple[str, ...]
    source_coverage_count: int
    all_sources_covered: bool


@dataclass(frozen=True)
class RGBVisionCandidateTypeCoverageClosure:
    closure_ref: str
    candidate_type_ids: Tuple[str, ...]
    candidate_type_coverage_count: int
    all_candidate_types_covered: bool


@dataclass(frozen=True)
class RGBVisionDatasetTestSourceClosure:
    closure_ref: str
    backup_pool_not_training_admission: bool
    backup_pool_not_runtime_admission: bool
    dataset_download_allowed: bool
    training_use_allowed: bool
    license_ref_required_for_all: bool
    dataset_ref_required_for_all: bool
    annotation_origin_required_for_all: bool
    sample_origin_required_for_all: bool
    roboflow_license_per_dataset_required: bool
    commercial_use_unknown_until_verified: bool
    non_commercial_sources_research_test_only: bool
    dataset_label_not_fact: bool
    annotation_as_evidence_candidate: bool


@dataclass(frozen=True)
class RGBVisionReplayPathClosure:
    closure_ref: str
    adapter_mapping_required: bool
    source_admission_required: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    origin_metadata_preserved: bool
    field_candidate_path_closed: bool
    task_candidate_path_closed: bool
    guidance_candidate_path_closed: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool


@dataclass(frozen=True)
class RGBVisionSafetyBoundaryClosure:
    closure_ref: str
    rgb_first_hardware_baseline_preserved: bool
    tof_stereo_depth_optional_auxiliary_only: bool
    cognitive_world_reconstruction_objective_preserved: bool
    ocr_output_not_fact: bool
    segmentation_output_not_route_activation: bool
    tracking_output_not_action_trigger: bool
    monocular_depth_vio_not_field_identity: bool
    scene_relation_not_final_interpretation: bool
    native_output_direct_to_field_blocked: bool
    no_live_camera_sensor_gps_map_api_ros: bool
    no_navigation_action_speech_fact_write: bool


@dataclass(frozen=True)
class RGBVisionVisualSymbolEvidenceExtensionClosure:
    closure_ref: str
    color_evidence_candidate_covered: bool
    shape_evidence_candidate_covered: bool
    visual_symbol_candidate_covered: bool
    symbol_meaning_candidate_candidate_only: bool
    color_shape_symbol_not_fact: bool
    visual_symbol_not_direct_navigation: bool
    visual_symbol_not_direct_speech: bool
    visual_symbol_not_direct_fact_write: bool
    visual_symbol_requires_context_validation: bool
    symbol_meaning_refs: Tuple[str, ...]
    symbol_meaning_mappings: Tuple[Dict[str, str], ...]


@dataclass(frozen=True)
class RGBVisionEvidenceChainIntegratedClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    source_coverage_count: int
    candidate_type_coverage_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
