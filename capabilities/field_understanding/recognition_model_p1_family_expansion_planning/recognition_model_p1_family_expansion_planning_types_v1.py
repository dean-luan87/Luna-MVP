# -*- coding: utf-8 -*-
"""Recognition Model P1 Family Expansion Planning — types v1.

Plans Luna's recognition-model expansion from the frozen P0 stable baseline
toward P1/P2 multi-family coverage. This is a *planning-only* phase: it admits
more model families as planned candidates and fixes the expansion order, output
standard, adapter requirements, multi-model interaction route, and the
downstream midplatform model data-handling / control test entries.

Strictly no single-model debugging, no new model download, no real inference,
no model tuning, no dataset usage, no live camera/sensor, and no navigation/
action/speech/fact_write. Luna remains emotion-multimodal brain / cognition
first; the VLA action chain is excluded from current scope.

Core principle ordering:
  expand family coverage -> per-model debugging,
  check output conforms to Luna standard -> multi-model interaction,
  verify model interaction -> midplatform model data handling,
  finally test midplatform model call / admission / degrade / block / schedule control.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-P1-Family-Expansion-Planning-v1-001"
SCOPE = "recognition_model_p1_family_expansion_planning"
SOURCE_CHAIN = "recognition_model_p1_family_expansion_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model P0 Integration Closure,规划 Luna 识别模型从 P0 稳定基线向 P1/P2 "
    "多模型族扩张。本阶段不为单一模型调试、不补 YOLO 权重、不执行真实 inference、不下载新模型、不调优、"
    "不使用数据集,而是把更多模型族纳入 Luna 体系规划,明确接入顺序、输出标准、Adapter 要求、联动测试路线,"
    "以及后续中台模型治理与控制测试入口。先扩模型族覆盖,再做单模型调试;先检查输出是否符合 Luna 标准,"
    "再做模型联动;先验证模型间互动,再测中台对模型数据的处理能力;最后再测中台对模型调用、准入、降级、"
    "阻断、调度的控制能力。Luna 仍以情感多模态 + 大脑/世界理解为核心,VLA 行动链不在当前范围。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_p2_recognition_families_serve_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_p1_family_expansion_planning_only"
P1_FAMILY_EXPANSION_PLANNING_ONLY = True
P0_BASELINE_REF = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_PHASE_REF = "Phase-Recognition-Model-P1-Invocation-And-Local-Availability-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Family planned/reserved flag keys
# --------------------------------------------------------------------------- #
FAMILY_FLAG_KEYS: Dict[str, str] = {
    "p1_a_segmentation": "segmentation_family_planned",
    "p1_b_tracking": "tracking_family_planned",
    "p1_c_depth_spatial_hint": "depth_spatial_hint_family_planned",
    "p1_d_object_detection_completion": "object_detection_completion_family_planned",
    "p2_scene_relation_vlm": "scene_relation_vlm_family_planned",
    "p2_audio_speech_evidence": "audio_speech_evidence_family_reserved",
    "p2_emotion_multimodal_bridge": "emotion_multimodal_bridge_reserved",
}

# --------------------------------------------------------------------------- #
# Output standard
# --------------------------------------------------------------------------- #
OUTPUT_STANDARD_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_family",
    "model_version_ref",
    "model_origin",
    "license_ref",
    "source_chain",
    "input_ref",
    "output_schema_ref",
    "confidence",
    "frame_ref_or_timestamp_ms",
    "adapter_mapping_ref",
    "allowed_use",
    "commercial_use_status",
    "fallback_plan",
    "unavailable_record_policy",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
    "fallback_plan",
)

# output-standard required flag keys
OUTPUT_STANDARD_REQUIRED_FLAGS: Dict[str, str] = {
    "source_chain": "source_chain_required",
    "license_ref": "license_ref_required",
    "model_origin": "model_origin_required",
    "confidence": "confidence_required",
    "adapter_mapping_ref": "adapter_mapping_ref_required",
    "fallback_plan": "fallback_plan_required",
    "unavailable_record_policy": "unavailable_record_policy_required",
}

# --------------------------------------------------------------------------- #
# Sequencing flags
# --------------------------------------------------------------------------- #
SEQUENCING_FLAGS: Tuple[str, ...] = (
    "p1_expansion_before_single_model_debugging_enforced",
    "model_interaction_test_deferred_but_planned",
    "midplatform_data_handling_test_deferred_but_planned",
    "midplatform_model_control_test_deferred_but_planned",
    "model_tuning_deferred",
    "dataset_usage_deferred",
)

# --------------------------------------------------------------------------- #
# Mandatory rules
# --------------------------------------------------------------------------- #
PLANNING_RULES: Tuple[str, ...] = (
    "this_phase_is_p1_p2_family_expansion_planning_only",
    "p0_baseline_remains_frozen",
    "no_single_model_debugging_is_performed",
    "no_new_model_download_is_performed",
    "no_new_inference_is_performed",
    "no_model_tuning_is_performed",
    "no_dataset_usage_is_performed",
    "no_training_is_performed",
    "p1_p2_model_families_are_admitted_only_as_planned_candidates",
    "all_model_outputs_must_later_pass_recognition_model_output_adapter",
    "all_model_outputs_must_become_evidence_candidate_first",
    "multi_model_interaction_test_is_deferred_but_planned",
    "midplatform_model_data_handling_test_is_deferred_but_planned",
    "midplatform_model_control_test_is_deferred_but_planned",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelP1FamilyExpansionPlanningProfile",
    "RecognitionModelExpansionTierPolicy",
    "RecognitionModelFamilyExpansionPolicy",
    "RecognitionModelOutputStandardPolicy",
    "RecognitionModelAdapterReadinessPolicy",
    "RecognitionModelInteractionReadinessPolicy",
    "MidplatformModelDataHandlingReadinessPolicy",
    "MidplatformModelControlReadinessPolicy",
    "RecognitionModelP1FamilyExpansionPlanningDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_P1_FAMILY_EXPANSION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_P1_FAMILY_EXPANSION_PLANNING_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "new_model_download_allowed": False,
    "real_inference_allowed": False,
    "single_model_debugging_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelExpansionTierPolicy:
    tier: str
    description: str
    execution_status: str


@dataclass(frozen=True)
class RecognitionModelFamilyExpansionPolicy:
    family_id: str
    family_name: str
    tier: str
    execution_status: str
    candidate_models: Tuple[str, ...]
    target_candidates: Tuple[str, ...]
    boundaries: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelOutputStandardPolicy:
    family_id: str
    required_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    must_map_to_luna_standard: bool


@dataclass(frozen=True)
class RecognitionModelAdapterReadinessPolicy:
    family_id: str
    adapter_ref: str
    must_pass_adapter_before_candidate: bool
    output_becomes_evidence_candidate_first: bool


@dataclass(frozen=True)
class RecognitionModelInteractionReadinessPolicy:
    interaction_id: str
    description: str
    deferred_but_planned: bool


@dataclass(frozen=True)
class MidplatformModelDataHandlingReadinessPolicy:
    check_id: str
    description: str
    deferred_but_planned: bool


@dataclass(frozen=True)
class MidplatformModelControlReadinessPolicy:
    check_id: str
    description: str
    deferred_but_planned: bool


@dataclass(frozen=True)
class RecognitionModelP1FamilyExpansionPlanningProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    p1_family_expansion_planning_only: bool
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    output_standard_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    expansion_sequence: Tuple[str, ...]
    planning_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP1FamilyExpansionPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    upstream_stage_ref_count: int
    expansion_family_policy_count: int
    output_standard_policy_count: int
    adapter_readiness_policy_count: int
    interaction_readiness_policy_count: int
    midplatform_data_handling_readiness_count: int
    midplatform_control_readiness_count: int
    blocker_count: int
    final_decision: str


def planning_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
