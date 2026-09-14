# -*- coding: utf-8 -*-
"""Midplatform Model Test Lens Static Site Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001"
SCOPE = "p1_midplatform_model_test_lens_static_site_planning"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_static_site_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "规划 Luna 本地静态 Model Test Lens（模型测试镜头页）。与白盒产品页分离："
    "白盒偏系统运行态/参数/链路解释；镜头页只服务模型研发测试与能力评估，"
    "读取 _tmp_eval_out / TestBoard / test_assets 产物并可视化 candidate output、"
    "metrics、failure mode、trace。本阶段仅 planning，不执行模型、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_test_lens_is_local_static_model_capability_observation_not_whitebox_not_runtime"
)

PLANNING_ONLY = True
MODEL_TEST_LENS_STATIC_SITE_PLANNING = True
LOCAL_STATIC_PAGE_ONLY = True
NOT_WHITEBOX_PRODUCT_PAGE = True
MODEL_TESTING_ONLY = True
SINGLE_MODEL_CAPABILITY_TEST_FOCUS = True
RUNTIME_EXECUTION_ALLOWED = False
MODEL_EXECUTION_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
AUDIO_INPUT_ALLOWED = False
VIDEO_INPUT_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_PACKAGING_EXECUTION_REF = (
    "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
)
UPSTREAM_MOBILE_SAM_MULTI_REQUEST_REF = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
UPSTREAM_MOBILE_SAM_QUALITY_REVIEW_REF = (
    "Phase-P1-MobileSAM-Real-Image-Quality-Review-And-Prompt-Strategy-Planning-v1-001"
)
UPSTREAM_MOBILE_SAM_REAL_EXECUTION_REF = (
    "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)
MODEL_ONBOARDING_STANDARD_REL = (
    "capabilities/midplatform/governance_standards/model_onboarding/"
    "model_asset_onboarding_governance_standard_v1.md"
)
GOVERNANCE_MANIFEST_REL = (
    "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json"
)
GOVERNANCE_LEGACY_INVENTORY_REL = (
    "capabilities/midplatform/governance_standards/legacy_rules/"
    "legacy_reusable_governance_rules_inventory_v1.json"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_SKELETON_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

MODEL_TEST_LENS_ROOT_REL = "capabilities/midplatform/model_test_lens"
STATIC_SITE_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/static_site"
SCHEMAS_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/schemas"
MODEL_PANELS_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/model_panels"
EXAMPLES_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/examples"

READ_SOURCES_V1: Tuple[str, ...] = (
    "_tmp_eval_out/",
    "capabilities/test_board/",
    "capabilities/test_assets/",
    f"{SCHEMAS_ROOT_REL}/",
)

FORBIDDEN_INPUTS_V1: Tuple[str, ...] = (
    "external_url_import",
    "live_camera",
    "realtime_microphone",
    "runtime_server",
    "automatic_dataset_download",
    "direct_model_inference_from_page",
)

PAGE_MODULES: Tuple[Dict[str, str], ...] = (
    {"module_id": "model_selector", "role": "select_model_category_and_panel"},
    {"module_id": "test_case_importer", "role": "import_local_manifest_tmp_eval_out_testboard"},
    {"module_id": "input_preview_panel", "role": "preview_image_video_audio_text_trajectory"},
    {"module_id": "process_trace_panel", "role": "show_execution_trace_prompt_recheck_memory"},
    {"module_id": "result_visualization_panel", "role": "model_specific_candidate_visualization"},
    {"module_id": "metrics_panel", "role": "scores_iou_area_ratio_wer_drift_id_switch"},
    {"module_id": "failure_mode_panel", "role": "risk_labels_failure_modes_requires_review"},
    {"module_id": "testboard_refs_panel", "role": "test_process_conclusion_artifact_refs_protected"},
    {"module_id": "boundary_panel", "role": "candidate_only_readiness_false_exclusions"},
)

MODEL_PANEL_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "panel_id": "ocr",
        "panel_path": "model_panels/ocr",
        "model_category": "ocr",
        "input_types": ("image", "video_frame"),
        "visualization_outputs": ("text_boxes", "recognized_text", "confidence", "reading_order", "candidate_correction", "failure_modes"),
        "fact_write_allowed": False,
    },
    {
        "panel_id": "slam_vio",
        "panel_path": "model_panels/slam",
        "model_category": "slam_vio",
        "input_types": ("frame_sequence", "pose_trace", "imu_candidate", "map_candidate"),
        "visualization_outputs": ("trajectory", "keyframes", "local_map", "drift_metrics", "tracking_lost_points"),
        "navigation_drive_allowed": False,
    },
    {
        "panel_id": "depth_world",
        "panel_path": "model_panels/depth",
        "model_category": "depth_world",
        "input_types": ("image", "video_frame"),
        "visualization_outputs": ("depth_map", "walkable_area_candidate", "scale_uncertainty", "quality_risk"),
        "actionable_fact_write_allowed": False,
    },
    {
        "panel_id": "vision_segmentation",
        "panel_path": "model_panels/vision_segmentation",
        "model_category": "segmentation",
        "input_types": ("image", "prompt_box", "prompt_point"),
        "visualization_outputs": ("mask_overlay", "area_ratio", "score", "prompt_type", "candidate_mask"),
        "primary_model_example": "mobile_sam",
        "candidate_only": True,
    },
    {
        "panel_id": "detection_tracking",
        "panel_path": "model_panels/tracking",
        "model_category": "detection_tracking",
        "input_types": ("image", "video"),
        "visualization_outputs": ("bbox", "track_id", "confidence", "id_switch", "lost_track"),
        "action_layer_allowed": False,
    },
    {
        "panel_id": "asr",
        "panel_path": "model_panels/asr",
        "model_category": "asr",
        "input_types": ("audio",),
        "visualization_outputs": ("transcript", "timestamp", "segment_confidence", "wer_if_reference"),
    },
    {
        "panel_id": "tts",
        "panel_path": "model_panels/tts",
        "model_category": "tts",
        "input_types": ("text", "style_params"),
        "visualization_outputs": ("audio_ref", "waveform", "duration", "pause_markers", "quality_notes"),
        "speech_output_gate_allowed": False,
    },
    {
        "panel_id": "speaker",
        "panel_path": "model_panels/speaker",
        "model_category": "speaker",
        "input_types": ("audio",),
        "visualization_outputs": ("speaker_segments", "candidate_speaker_id", "confidence"),
        "identity_fact_write_allowed": False,
    },
    {
        "panel_id": "face_expression_gesture",
        "panel_path": "model_panels/face_expression",
        "model_category": "face_expression_gesture",
        "input_types": ("image", "video"),
        "visualization_outputs": ("face_boxes", "landmarks", "expression_candidate", "gesture_candidate"),
        "identity_emotion_fact_write_allowed": False,
    },
    {
        "panel_id": "multimodal_vlm",
        "panel_path": "model_panels/multimodal",
        "model_category": "multimodal_vlm",
        "input_types": ("image", "video", "text_prompt"),
        "visualization_outputs": ("answer_candidate", "evidence_refs", "hallucination_risk"),
        "fact_layer_allowed": False,
    },
)

LAYOUT_REGIONS: Tuple[str, ...] = (
    "left_model_list_and_test_type",
    "center_input_preview",
    "right_output_visualization",
    "bottom_trace_metrics_failure_testboard",
)

VISUALIZATION_LAYER_TYPES: Tuple[str, ...] = (
    "image_overlay", "mask", "bbox", "polyline", "trajectory", "heatmap",
    "waveform", "transcript", "table", "timeline",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_whitebox_product_page", "go_key": "not_whitebox_product_page", "depends_on": "not_whitebox_product_page"},
    {"guard_id": "invalid_b_direct_model_execution", "go_key": "no_model_execution", "depends_on": "no_model_execution"},
    {"guard_id": "invalid_c_runtime_output_semantic_fact_nav", "go_key": "no_runtime_downstream", "depends_on": "no_runtime_downstream"},
    {"guard_id": "invalid_d_external_live_realtime", "go_key": "no_external_live_realtime", "depends_on": "no_external_live_realtime"},
    {"guard_id": "invalid_e_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_f_delete_testboard_artifacts", "go_key": "no_delete_testboard", "depends_on": "no_delete_testboard"},
    {"guard_id": "invalid_g_candidate_as_fact", "go_key": "candidate_not_fact", "depends_on": "candidate_not_fact"},
    {"guard_id": "invalid_h_missing_multi_model_panels", "go_key": "all_model_panels_defined", "depends_on": "all_model_panels_defined"},
    {"guard_id": "invalid_i_missing_result_envelope", "go_key": "unified_result_envelope_defined", "depends_on": "unified_result_envelope_defined"},
    {"guard_id": "invalid_j_missing_visualization_schema", "go_key": "visualization_layer_schema_defined", "depends_on": "visualization_layer_schema_defined"},
    {"guard_id": "invalid_k_missing_boundary_panel", "go_key": "boundary_panel_defined", "depends_on": "boundary_panel_defined"},
    {"guard_id": "invalid_l_bypass_governance", "go_key": "governance_standards_referenced", "depends_on": "governance_standards_referenced"},
    {"guard_id": "invalid_m_testboard_not_required", "go_key": "testboard_required", "depends_on": "testboard_required"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "model_test_lens_is_a_local_static_model_testing_page",
    "model_test_lens_is_not_whitebox_product_page",
    "model_test_lens_is_not_runtime",
    "model_test_lens_must_not_execute_models_in_planning_phase",
    "model_test_lens_must_not_trigger_runtime",
    "model_test_lens_must_not_trigger_output_adapter",
    "model_test_lens_must_not_write_semantic_fact_navigation_speech",
    "model_test_lens_must_not_mutate_registry",
    "model_test_lens_must_not_delete_testboard_artifacts",
    "model_test_lens_must_support_multi_model_panels",
    "ocr_panel_is_required",
    "slam_vio_panel_is_required",
    "depth_world_panel_is_required",
    "segmentation_panel_is_required",
    "detection_tracking_panel_is_required",
    "asr_panel_is_required",
    "tts_panel_is_required",
    "speaker_panel_is_required",
    "face_expression_gesture_panel_is_required",
    "multimodal_vlm_panel_is_required",
    "unified_result_envelope_is_required",
    "visualization_layer_schema_is_required",
    "boundary_panel_is_required",
    "testboard_refs_panel_is_required",
    "governance_standards_reference_is_required",
    "testboard_record_is_required",
    "test_artifacts_are_protected",
    "cleanup_must_not_delete_testboard_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "model_test_lens_page_structure_record",
    "model_test_lens_model_panel_registry_record",
    "model_test_lens_result_envelope_schema_record",
    "model_test_lens_visualization_layer_schema_record",
    "model_test_lens_boundary_policy_record",
    "model_test_lens_whitebox_separation_record",
    "model_test_lens_governance_reference_record",
    "model_test_lens_followup_skeleton_route_record",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "governance_standards_packaging_reused": True,
    "model_asset_onboarding_standard_reused": True,
}


@dataclass(frozen=True)
class ModelTestLensStaticSitePlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    model_test_lens_static_site_planning: bool
    local_static_page_only: bool
    not_whitebox_product_page: bool
    model_testing_only: bool
    single_model_capability_test_focus: bool
    runtime_execution_allowed: bool
    model_execution_allowed: bool
    registry_mutation_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelTestLensPageStructureRecord:
    record_id: str
    layout_regions: Tuple[str, ...]
    page_modules: Tuple[Dict[str, str], ...]
    read_sources: Tuple[str, ...]
    forbidden_inputs: Tuple[str, ...]
    static_site_root_rel: str


@dataclass(frozen=True)
class ModelTestLensModelPanelRegistryRecord:
    record_id: str
    panels: Tuple[Dict[str, Any], ...]
    panel_count: int
    all_required_panels_defined: bool


@dataclass(frozen=True)
class ModelTestLensBoundaryPolicyRecord:
    record_id: str
    candidate_only: bool
    not_fact: bool
    not_runtime_output: bool
    not_output_adapter_output: bool
    not_semantic_output: bool
    not_navigation_action_speech: bool
    readiness_effect_all_false: bool
    page_generates_readiness: bool


@dataclass(frozen=True)
class ModelTestLensWhiteboxSeparationRecord:
    record_id: str
    whitebox_purpose: str
    model_test_lens_purpose: str
    whitebox_covers_runtime_product_explanation: bool
    model_test_lens_covers_model_capability_evaluation: bool


@dataclass(frozen=True)
class ModelTestLensGovernanceReferenceRecord:
    record_id: str
    governance_manifest_ref: str
    legacy_inventory_ref: str
    model_onboarding_standard_ref: str
    test_board_protocol_ref: str
    page_bypasses_approval_gate: bool


@dataclass(frozen=True)
class ModelTestLensFollowupSkeletonRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str


@dataclass
class NegativeModelTestLensPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ModelTestLensStaticSitePlanningDecision:
    decision_ref: str
    model_test_lens_static_site_planning_profile_count: int
    model_panel_registry_defined: bool
    unified_result_envelope_defined: bool
    visualization_layer_schema_defined: bool
    boundary_panel_defined: bool
    testboard_refs_panel_defined: bool
    governance_standards_reference_defined: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
