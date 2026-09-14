# -*- coding: utf-8 -*-
"""Observation Attention Layer V1 — types, enums, and boundary constants."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Tuple


PHASE_REF = "Phase-P1-Midplatform-Model-Test-Lens-Observation-Attention-Layer-Planning-v1-001"
LAYER_ID = "ObservationAttentionLayerV1"


class PriorityLevel(str, Enum):
    P0_IMMEDIATE = "P0_immediate_attention"
    P1_HIGH = "P1_high_attention"
    P2_MEDIUM = "P2_medium_attention"
    P3_LOW = "P3_low_attention"
    IGNORE = "ignore_for_now"


class TaskContext(str, Enum):
    GENERAL_SCENE = "general_scene_understanding"
    STREET_NAVIGATION = "street_navigation_test"
    CROSSING_ROAD = "crossing_road_test"
    FIND_OBJECT = "find_object_test"
    FIND_TEXT = "find_text_test"
    INDOOR_NAVIGATION = "indoor_navigation_test"
    MODEL_QUALITY_REVIEW = "model_quality_review"


class FollowupModel(str, Enum):
    DETECTION = "detection"
    OCR = "ocr"
    DEPTH = "depth"
    SLAM = "slam"
    TRACKING = "tracking"
    VLM = "vlm"
    HUMAN_REVIEW = "human_review"
    MOTION_ANALYSIS = "motion_analysis"
    SLAM_REFERENCE = "slam_reference"
    WALKABLE_AREA_REVIEW = "walkable_area_review"
    VIO = "vio"
    NO_FOLLOWUP = "no_followup_required"


class RoutePriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class MotionStateCandidate(str, Enum):
    STATIC = "static_candidate"
    DYNAMIC = "dynamic_candidate"
    SCENE_STRUCTURE = "scene_structure_candidate"
    UNKNOWN = "unknown_motion_state"
    NEEDS_TRACKING_REVIEW = "needs_tracking_review"


class VideoFrameContext(str, Enum):
    SINGLE_FRAME = "single_frame"
    VIDEO_MULTI_FRAME = "video_multi_frame"
    FRAME_SEQUENCE = "frame_sequence"


ATTENTION_PIPELINE: Tuple[str, ...] = (
    "region_segmentation",
    "static_dynamic_candidate_judgment",
    "observation_priority",
    "followup_model_route",
)

MOTION_STATE_LABELS_ZH: Dict[MotionStateCandidate, str] = {
    MotionStateCandidate.STATIC: "静态观察候选",
    MotionStateCandidate.DYNAMIC: "动态观察候选",
    MotionStateCandidate.SCENE_STRUCTURE: "场景结构候选",
    MotionStateCandidate.UNKNOWN: "运动状态未知",
    MotionStateCandidate.NEEDS_TRACKING_REVIEW: "需跟踪复核",
}

PRIORITY_LEVEL_LABELS_ZH: Dict[PriorityLevel, str] = {
    PriorityLevel.P0_IMMEDIATE: "立即关注",
    PriorityLevel.P1_HIGH: "高优先级",
    PriorityLevel.P2_MEDIUM: "中优先级",
    PriorityLevel.P3_LOW: "低优先级",
    PriorityLevel.IGNORE: "暂时忽略",
}

FORBIDDEN_OPERATIONS: Tuple[str, ...] = (
    "execute_detection",
    "execute_ocr",
    "execute_slam",
    "execute_depth",
    "execute_inference",
    "write_fact",
    "write_semantic",
    "mutate_registry",
    "trigger_runtime",
    "call_output_adapter",
    "trigger_navigation",
    "trigger_speech",
    "modify_original_envelope",
    "overwrite_model_output",
    "upgrade_prompt_label_to_fact",
    "treat_correction_as_ground_truth",
    "execute_followup_route_immediately",
    "output_confirmed_dynamic_from_single_frame",
    "treat_correction_as_motion_ground_truth",
)

STATIC_DYNAMIC_POLICY_REFS: Tuple[str, ...] = (
    "schemas/observation_attention/static_dynamic_observation_policy_v1.json",
    "schemas/observation_attention/observation_target_motion_state_schema_v1.json",
)

BOUNDARY_FLAGS: Dict[str, bool] = {
    "planning_only": True,
    "observation_attention_layer_planning": True,
    "observation_attention_candidate_only": True,
    "region_priority_candidate_only": True,
    "followup_model_route_candidate_only": True,
    "uses_existing_segmentation_outputs": True,
    "uses_existing_hud_annotations": True,
    "must_not_modify_original_envelope": True,
    "must_not_modify_model_output": True,
    "must_not_write_fact": True,
    "must_not_write_semantic": True,
    "must_not_trigger_runtime": True,
    "must_not_trigger_navigation_action_speech": True,
    "must_not_call_output_adapter": True,
    "must_not_mutate_registry": True,
    "model_execution_allowed": False,
    "runtime_execution_allowed": False,
    "output_adapter_allowed": False,
    "semantic_layer_allowed": False,
    "fact_write_allowed": False,
    "navigation_action_speech_allowed": False,
    "registry_mutation_allowed": False,
    "external_network_allowed": False,
    "live_camera_allowed": False,
    "live_microphone_allowed": False,
    "prompt_label_is_candidate_only": True,
    "human_correction_is_priority_signal_only": True,
    "single_frame_no_confirmed_dynamic": True,
    "static_dynamic_candidate_only": True,
}

ATTENTION_QUESTIONS: Tuple[str, ...] = (
    "哪些区域值得继续观察？",
    "哪些区域和当前任务相关？",
    "哪些区域可能有风险？",
    "哪些区域不确定，需要复核？",
    "下一步应该调用哪个模型继续看？",
)

NOT_ANSWERED: Tuple[str, ...] = (
    "事实类别是什么",
    "是否可以导航",
    "是否可以行动",
    "是否可以语音输出",
    "是否写入事实层",
)


@dataclass
class ObservationAttentionLayerProfile:
    layer_id: str = LAYER_ID
    phase_ref: str = PHASE_REF
    planning_only: bool = True
    observation_attention_candidate_only: bool = True
    region_priority_candidate_only: bool = True
    followup_model_route_candidate_only: bool = True
    boundary_flags: Dict[str, bool] = field(default_factory=lambda: dict(BOUNDARY_FLAGS))
    task_contexts: Tuple[str, ...] = field(default_factory=lambda: tuple(t.value for t in TaskContext))
    priority_levels: Tuple[str, ...] = field(default_factory=lambda: tuple(p.value for p in PriorityLevel))
    followup_models: Tuple[str, ...] = field(default_factory=lambda: tuple(f.value for f in FollowupModel))
