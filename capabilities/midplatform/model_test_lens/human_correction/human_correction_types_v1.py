# -*- coding: utf-8 -*-
"""Human Correction Layer V1 — types, enums, and boundary constants."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Tuple


PHASE_REF = "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-Planning-v1-001"
LAYER_ID = "HumanCorrectionLayerV1"


class CorrectionType(str, Enum):
    FALSE_POSITIVE = "false_positive"
    FALSE_NEGATIVE = "false_negative"
    WRONG_LABEL = "wrong_label"
    BOUNDARY_INACCURATE = "boundary_inaccurate"
    CONFIDENCE_MISMATCH = "confidence_mismatch"
    TASK_RELEVANCE_ERROR = "task_relevance_error"
    RISK_ASSESSMENT_ERROR = "risk_assessment_error"
    RECOMMENDATION_ERROR = "recommendation_error"
    DUPLICATE_OR_OVERLAPPING_DETECTION = "duplicate_or_overlapping_detection"
    UNCLEAR_NEED_REVIEW = "unclear_need_review"


class CorrectionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"


class CorrectionTargetType(str, Enum):
    OBJECT_CHIP = "object_chip"
    HUD_ANNOTATION = "hud_annotation"
    SEGMENTATION_MASK = "segmentation_mask"
    DETECTION_BOX = "detection_box"
    OCR_TEXT_BOX = "ocr_text_box"
    SLAM_TRACK = "slam_track"
    DEPTH_REGION = "depth_region"
    REASONING_PANEL_STATEMENT = "reasoning_panel_statement"
    RECOMMENDATION_ITEM = "recommendation_item"
    WHOLE_SCENE = "whole_scene"
    MISSING_REGION = "missing_region"


class MarkedRegionType(str, Enum):
    POINT = "point"
    BOX = "box"
    POLYGON = "polygon"
    FREEHAND = "freehand"


class RecommendedFollowupModel(str, Enum):
    DETECTION = "detection"
    OCR = "ocr"
    SLAM = "slam"
    DEPTH = "depth"
    HUMAN_REVIEW = "human_review"
    DATASET_REVIEW = "dataset_review"


class ErrorCauseHypothesis(str, Enum):
    LOW_LIGHT = "low_light"
    OCCLUSION = "occlusion"
    SMALL_OBJECT = "small_object"
    FAR_DISTANCE = "far_distance"
    MOTION_BLUR = "motion_blur"
    REFLECTIVE_SURFACE = "reflective_surface"
    CROWDED_SCENE = "crowded_scene"
    SIMILAR_TEXTURE = "similar_texture"
    PROMPT_TOO_LOOSE = "prompt_too_loose"
    PROMPT_TOO_NARROW = "prompt_too_narrow"
    MISSING_DETECTION_MODEL = "missing_detection_model"
    MISSING_OCR_MODEL = "missing_ocr_model"
    MISSING_DEPTH = "missing_depth"
    MISSING_TRACKING = "missing_tracking"
    MODEL_LIMITATION = "model_limitation"
    ANNOTATION_INCOMPLETE = "annotation_incomplete"
    UNKNOWN = "unknown"


CORRECTION_TYPE_LABELS_ZH: Dict[CorrectionType, str] = {
    CorrectionType.FALSE_POSITIVE: "误识别",
    CorrectionType.FALSE_NEGATIVE: "漏识别",
    CorrectionType.WRONG_LABEL: "标签错误",
    CorrectionType.BOUNDARY_INACCURATE: "边界不准",
    CorrectionType.CONFIDENCE_MISMATCH: "置信度不合理",
    CorrectionType.TASK_RELEVANCE_ERROR: "任务相关性错误",
    CorrectionType.RISK_ASSESSMENT_ERROR: "风险判断错误",
    CorrectionType.RECOMMENDATION_ERROR: "建议不合理",
    CorrectionType.DUPLICATE_OR_OVERLAPPING_DETECTION: "重复或重叠识别",
    CorrectionType.UNCLEAR_NEED_REVIEW: "不确定需复核",
}

MOBILE_SAM_PRIORITY_TYPES: FrozenSet[CorrectionType] = frozenset({
    CorrectionType.FALSE_NEGATIVE,
    CorrectionType.BOUNDARY_INACCURATE,
    CorrectionType.WRONG_LABEL,
    CorrectionType.TASK_RELEVANCE_ERROR,
    CorrectionType.UNCLEAR_NEED_REVIEW,
})

FORBIDDEN_CORRECTION_OPERATIONS: Tuple[str, ...] = (
    "modify_original_envelope",
    "overwrite_model_output",
    "write_fact",
    "write_semantic",
    "mutate_registry",
    "trigger_runtime",
    "call_output_adapter",
    "trigger_navigation",
    "trigger_speech",
    "auto_enter_training",
    "auto_become_ground_truth",
    "delete_original_model_output",
    "delete_test_board",
)

ALLOWED_CORRECTION_OPERATIONS: Tuple[str, ...] = (
    "create_correction_candidate",
    "create_training_signal_candidate",
    "create_hard_case_candidate",
    "create_regression_test_candidate",
    "write_test_board",
    "export_correction_json",
    "view_correction_in_developer_mode",
)

BOUNDARY_FLAGS: Dict[str, bool] = {
    "planning_only": True,
    "correction_candidate_only": True,
    "training_signal_candidate": True,
    "correction_must_not_modify_original_envelope": True,
    "correction_must_not_modify_model_output": True,
    "correction_must_not_write_fact": True,
    "correction_must_not_write_semantic": True,
    "correction_must_not_trigger_runtime": True,
    "correction_must_not_trigger_navigation_action_speech": True,
    "correction_must_not_call_output_adapter": True,
    "correction_must_not_mutate_registry": True,
    "correction_requires_testboard_record": True,
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
    "future_training_requires_owner_review": True,
}

UI_ENTRY_POINTS: Tuple[Dict[str, str], ...] = (
    {"entry_id": "object_chip", "trigger_zh": "指错", "ui_slot": "hud_object_chip_bar_v1"},
    {"entry_id": "hud_canvas", "trigger_zh": "点击框/mask/编号", "ui_slot": "perception_hud_view_v1"},
    {"entry_id": "missing_region", "trigger_zh": "标记漏识别", "ui_slot": "perception_hud_view_v1"},
    {"entry_id": "reasoning_panel", "trigger_zh": "指出问题", "ui_slot": "hud_reasoning_compression_v1"},
    {"entry_id": "bottom_drawer", "trigger_zh": "纠错", "ui_slot": "luna_bottom_drawer_tabs_v1"},
)


@dataclass
class HumanCorrectionLayerProfile:
    layer_id: str = LAYER_ID
    phase_ref: str = PHASE_REF
    planning_only: bool = True
    correction_candidate_only: bool = True
    training_signal_candidate: bool = True
    boundary_flags: Dict[str, bool] = field(default_factory=lambda: dict(BOUNDARY_FLAGS))
    correction_types: Tuple[str, ...] = field(
        default_factory=lambda: tuple(t.value for t in CorrectionType)
    )
    ui_entry_points: Tuple[Dict[str, str], ...] = UI_ENTRY_POINTS
