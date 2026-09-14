# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter Integration Planning — types v1.

Plans the recognition-model integration layer on top of the already-frozen Luna
Phase-One environment cognition evidence main chain. This phase does NOT run real
recognition, does NOT download models, does NOT build runtime. It only defines
how different recognition model outputs map, via an Interface Adapter, into Luna
evidence candidates and feed the already-completed RGB / SLAM / Cross-Modal /
Field-Task-Guidance mainline.

Core principle:
  - admit model OUTPUT first, model RUNTIME later;
  - validate adapter mapping first, real inference later;
  - model output must NOT bypass the Luna evidence main chain.

  model_native_output
  -> RecognitionModelOutputAdapter
  -> Luna evidence candidate
  -> evidence main chain (field_synthesis_v1)

Planning + Matrix Review only. No model download / repo clone / build / real
inference / dataset download / training / runtime / live camera/sensor / GPS /
map API / ROS, and no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Output-Adapter-Integration-Planning-v1-001"
SCOPE = "recognition_model_output_adapter_integration_planning"
SOURCE_CHAIN = "recognition_model_output_adapter_integration_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已冻结的 Luna Phase One Environment Cognition Evidence Main Chain，开始规划真实识别模型接入层。"
    "不执行真实识别、不下载模型、不构建 runtime，只定义不同识别模型输出如何通过 Interface Adapter 映射"
    "到 Luna evidence candidate，并接入已完成的 RGB / SLAM / Cross-Modal / Field-Task-Guidance 主链。"
    "核心原则：先接模型输出，再接真实模型运行；先验证 adapter mapping，再验证真实 inference；模型输出"
    "不得绕过 Luna evidence main chain。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_output_adapter_integration_planning_only"
TARGET_ENTRYPOINT = "field_synthesis_v1"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
MAIN_CHAIN_CLOSURE_REF = TARGET_CHAIN_REF
RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
)
SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"
)
RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF = (
    "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Model families
# --------------------------------------------------------------------------- #
MODEL_FAMILY_IDS: Tuple[str, ...] = (
    "ocr_model_family",
    "object_detection_model_family",
    "segmentation_model_family",
    "tracking_model_family",
    "depth_spatial_hint_model_family",
    "visual_symbol_model_family",
    "scene_relation_model_family",
)

MODEL_FAMILY_REGISTERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{m}_registered" for m in MODEL_FAMILY_IDS
)

# --------------------------------------------------------------------------- #
# Adapter mapping ids + GO keys
# --------------------------------------------------------------------------- #
ADAPTER_MAPPING_IDS: Tuple[str, ...] = (
    "text_output_to_text_evidence_mapping",
    "detection_output_to_object_evidence_mapping",
    "segmentation_output_to_region_evidence_mapping",
    "tracking_output_to_track_dynamic_risk_mapping",
    "depth_output_to_spatial_hint_mapping",
    "visual_symbol_output_mapping",
    "scene_relation_output_mapping",
    "uncertainty_conflict_output_mapping",
)

ADAPTER_MAPPING_SUPPORTED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{a}_supported" for a in ADAPTER_MAPPING_IDS
)

# --------------------------------------------------------------------------- #
# Planning scenarios
# --------------------------------------------------------------------------- #
SCENARIO_IDS: Tuple[str, ...] = (
    "ocr_model_output_adapter_planning",
    "object_detection_model_output_adapter_planning",
    "segmentation_model_output_adapter_planning",
    "tracking_model_output_adapter_planning",
    "depth_spatial_hint_model_output_adapter_planning",
    "visual_symbol_model_output_adapter_planning",
    "scene_relation_model_output_adapter_planning",
    "invalid_model_output_blocked",
)

# --------------------------------------------------------------------------- #
# Unified model output admission fields
# --------------------------------------------------------------------------- #
REQUIRED_MODEL_OUTPUT_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_family",
    "model_version_ref",
    "model_origin",
    "license_ref",
    "source_chain",
    "input_ref",
    "output_schema_ref",
    "confidence",
    "timestamp_ms_or_frame_ref",
    "adapter_mapping_ref",
    "allowed_use",
    "commercial_use_status",
)

# Missing any of these must be rejected.
REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_output_adapter_planning_only",
    "no_model_download",
    "no_repo_clone",
    "no_model_build",
    "no_real_inference",
    "no_dataset_download",
    "no_training",
    "model_output_must_pass_interface_adapter",
    "model_native_output_must_not_enter_field_task_guidance_directly",
    "all_model_outputs_become_evidence_candidate_first",
    "ocr_output_is_not_fact",
    "object_identity_is_not_fact",
    "segmentation_is_not_route_activation",
    "tracking_is_not_action_trigger",
    "depth_vio_does_not_override_field_identity",
    "color_shape_symbol_is_not_fact",
    "visual_symbol_meaning_requires_context_validation",
    "scene_relation_is_not_final_interpretation",
    "low_confidence_or_conflict_becomes_uncertainty_or_conflict_candidate",
    "field_task_guidance_path_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelOutputAdapterIntegrationPlanningProfile",
    "RecognitionModelFamilyPolicy",
    "RecognitionModelOutputSchemaPolicy",
    "RecognitionModelOutputAdapterMappingPolicy",
    "RecognitionModelCandidateMappingPolicy",
    "RecognitionModelSafetyBoundaryPolicy",
    "RecognitionModelAdmissionBoundaryPolicy",
    "RecognitionModelOutputAdapterIntegrationPlanningDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_OUTPUT_ADAPTER_INTEGRATION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_OUTPUT_ADAPTER_INTEGRATION_PLANNING_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "model_runtime_execution_allowed": False,
    "model_download_allowed": False,
    "model_repo_clone_allowed": False,
    "model_build_allowed": False,
    "real_inference_allowed": False,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelOutputAdapterIntegrationPlanningProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    target_entrypoint: str
    target_chain_ref: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    model_family_ids: Tuple[str, ...]
    adapter_mapping_ids: Tuple[str, ...]
    scenario_ids: Tuple[str, ...]
    required_model_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelFamilyPolicy:
    model_family_id: str
    model_examples: Tuple[str, ...]
    output_schema: Tuple[str, ...]
    maps_to: Tuple[str, ...]
    boundary: str
    registered: bool


@dataclass(frozen=True)
class RecognitionModelOutputSchemaPolicy:
    policy_ref: str
    required_model_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelOutputAdapterMappingPolicy:
    adapter_mapping_id: str
    model_native_input: str
    luna_candidate_output: str
    boundary: str
    adapter_required: bool
    supported: bool


@dataclass(frozen=True)
class RecognitionModelCandidateMappingPolicy:
    policy_ref: str
    native_output_direct_to_field_blocked: bool
    all_model_outputs_become_evidence_candidate_first: bool
    candidate_mapping: Tuple[Dict[str, str], ...]


@dataclass(frozen=True)
class RecognitionModelSafetyBoundaryPolicy:
    policy_ref: str
    ocr_output_not_fact: bool
    object_identity_not_fact: bool
    segmentation_not_route_activation: bool
    tracking_not_action_trigger: bool
    depth_vio_not_field_identity: bool
    color_shape_symbol_not_fact: bool
    visual_symbol_requires_context_validation: bool
    scene_relation_not_final_interpretation: bool
    field_task_guidance_candidate_only: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool


@dataclass(frozen=True)
class RecognitionModelAdmissionBoundaryPolicy:
    policy_ref: str
    model_output_adapter_required: bool
    native_model_output_direct_to_field_blocked: bool
    source_chain_required: bool
    license_ref_required: bool
    model_origin_required: bool
    confidence_required: bool
    adapter_mapping_ref_required: bool


@dataclass(frozen=True)
class RecognitionModelScenarioPolicy:
    scenario_id: str
    planned_output: str
    boundary: str
    expected_result: str


@dataclass(frozen=True)
class RecognitionModelOutputAdapterIntegrationPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    model_family_policy_count: int
    adapter_mapping_policy_count: int
    scenario_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
