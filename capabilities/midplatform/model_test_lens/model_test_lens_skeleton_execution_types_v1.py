# -*- coding: utf-8 -*-
"""P1 Midplatform Model Test Lens Static Site Skeleton Execution — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Execution-And-Post-Review-v1-001"
SCOPE = "p1_midplatform_model_test_lens_static_site_skeleton_execution"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_static_site_skeleton_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "基于已 GO 的 Model Test Lens Planning，生成本地静态页 skeleton。"
    "只读本地 JSON、展示 candidate output/metrics/boundary/TestBoard refs。"
    "不执行模型、不 runtime、不写 registry/semantic/fact/navigation。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_test_lens_skeleton_is_local_json_viewer_not_whitebox_not_runtime"
)

REAL_EXECUTION_PHASE = True
STATIC_SITE_SKELETON_EXECUTION = True
LOCAL_STATIC_PAGE_ONLY = True
NOT_WHITEBOX_PRODUCT_PAGE = True
MODEL_TESTING_ONLY = True
READ_LOCAL_JSON_ONLY = True
MODEL_EXECUTION_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
EXTERNAL_URL_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
MICROPHONE_ALLOWED = False
FILE_DELETE_ALLOWED = False
TESTBOARD_DELETE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_PLANNING_REF = "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001"
UPSTREAM_PLANNING_EXPECTED_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_PLANNING_GO"
UPSTREAM_MOBILE_SAM_MULTI_EXECUTION_REF = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_DATA_ADAPTER = "Phase-P1-Midplatform-Model-Test-Lens-Data-Adapter-Planning-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "real_test"

STATIC_SITE_ROOT_REL = "capabilities/midplatform/model_test_lens/static_site"
EXAMPLE_ENVELOPE_REL = (
    "capabilities/midplatform/model_test_lens/examples/mobile_sam_multi_real_image_envelope_example_v1.json"
)
ENVELOPE_SCHEMA_REL = (
    "capabilities/midplatform/model_test_lens/schemas/model_test_result_envelope_schema_v1.json"
)
PLAN_MD_REL = "capabilities/midplatform/model_test_lens/model_test_lens_static_site_plan_v1.md"

REQUIRED_STATIC_FILES: Tuple[str, ...] = (
    f"{STATIC_SITE_ROOT_REL}/index.html",
    f"{STATIC_SITE_ROOT_REL}/app.js",
    f"{STATIC_SITE_ROOT_REL}/styles.css",
    f"{STATIC_SITE_ROOT_REL}/README_STATIC_SITE.md",
    f"{STATIC_SITE_ROOT_REL}/example_loader_config_v1.json",
)

FORBIDDEN_CODE_PATTERNS: Tuple[Dict[str, str], ...] = (
    {"pattern_id": "external_fetch", "regex": r"fetch\s*\(\s*['\"]https?://"},
    {"pattern_id": "camera_api", "regex": r"getUserMedia|mediaDevices\.getUserMedia"},
    {"pattern_id": "microphone_api", "regex": r"navigator\.mediaDevices"},
    {"pattern_id": "runtime_endpoint", "regex": r"runtime_server\s*\(|output_adapter_call\s*\("},
    {"pattern_id": "model_execution_button", "regex": r"runInference\s*\(|executeModel\s*\(|startInference\s*\("},
    {"pattern_id": "registry_mutation", "regex": r"mutateRegistry\s*\(|updateRegistry\s*\(|registry.*\.write\s*\("},
    {"pattern_id": "delete_artifact", "regex": r"deleteArtifact\s*\(|removeTestBoard\s*\("},
    {"pattern_id": "fact_write", "regex": r"writeFact\s*\(|semantic_write\s*\(|writeSemantic\s*\("},
    {"pattern_id": "navigation_speech", "regex": r"triggerSpeech\s*\(|triggerNavigation\s*\(|tts_output_gate\s*\("},
)

MODEL_PANEL_SKELETON_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {"panel_id": "segmentation", "label": "Segmentation / MobileSAM", "status": "active_example_available", "current_example": "mobile_sam_multi_real_image", "supported_layers": ("mask", "image_overlay", "table", "metrics")},
    {"panel_id": "ocr", "label": "OCR", "status": "placeholder", "supported_layers": ("bbox", "transcript", "reading_order", "confidence_table")},
    {"panel_id": "slam_vio", "label": "SLAM / VIO", "status": "placeholder", "supported_layers": ("trajectory", "keyframes", "map_candidate", "drift_metrics")},
    {"panel_id": "depth_world", "label": "Depth / World", "status": "placeholder", "supported_layers": ("heatmap", "walkable_area_candidate", "uncertainty")},
    {"panel_id": "detection_tracking", "label": "Detection / Tracking", "status": "placeholder", "supported_layers": ("bbox", "track_id", "timeline", "id_switch")},
    {"panel_id": "asr", "label": "ASR", "status": "placeholder", "supported_layers": ("transcript", "timeline", "word_confidence")},
    {"panel_id": "tts", "label": "TTS", "status": "placeholder", "supported_layers": ("waveform", "audio_ref", "duration", "pause_markers")},
    {"panel_id": "speaker", "label": "Speaker", "status": "placeholder", "supported_layers": ("speaker_segments", "timeline", "confidence")},
    {"panel_id": "face_expression_gesture", "label": "Face / Expression / Gesture", "status": "placeholder", "supported_layers": ("landmarks", "expression_candidate", "gesture_candidate")},
    {"panel_id": "multimodal_vlm", "label": "Multimodal / VLM", "status": "placeholder", "supported_layers": ("answer_candidate", "evidence_refs", "hallucination_risk")},
)

BOUNDARY_PANEL_FIELDS: Tuple[str, ...] = (
    "candidate_only", "not_fact", "not_runtime_output", "not_output_adapter_output",
    "not_semantic_output", "not_navigation_action_speech",
    "runtime_ready", "output_adapter_ready", "semantic_layer_ready",
    "fact_write_ready", "navigation_action_speech_ready",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_planning_not_go", "go_key": "upstream_planning_verified", "depends_on": "upstream_planning_verified"},
    {"guard_id": "invalid_b_whitebox_product_page", "go_key": "not_whitebox_product_page", "depends_on": "not_whitebox_product_page"},
    {"guard_id": "invalid_c_model_execution", "go_key": "no_model_execution", "depends_on": "no_model_execution"},
    {"guard_id": "invalid_d_runtime_output_adapter", "go_key": "no_runtime_output_adapter", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "invalid_e_semantic_fact_navigation", "go_key": "no_semantic_fact_navigation", "depends_on": "no_semantic_fact_navigation"},
    {"guard_id": "invalid_f_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_g_external_url", "go_key": "no_external_url", "depends_on": "no_external_url"},
    {"guard_id": "invalid_h_camera_microphone", "go_key": "no_camera_microphone", "depends_on": "no_camera_microphone"},
    {"guard_id": "invalid_i_delete_artifact", "go_key": "no_delete_artifact", "depends_on": "no_delete_artifact"},
    {"guard_id": "invalid_j_missing_panels", "go_key": "ten_panels_defined", "depends_on": "ten_panels_defined"},
    {"guard_id": "invalid_k_missing_envelope_loader", "go_key": "envelope_loader_present", "depends_on": "envelope_loader_present"},
    {"guard_id": "invalid_l_missing_boundary_panel", "go_key": "boundary_panel_present", "depends_on": "boundary_panel_present"},
    {"guard_id": "invalid_m_missing_testboard_panel", "go_key": "testboard_panel_present", "depends_on": "testboard_panel_present"},
    {"guard_id": "invalid_n_testboard_missing", "go_key": "testboard_required", "depends_on": "testboard_required"},
    {"guard_id": "invalid_o_testboard_not_protected", "go_key": "testboard_protected", "depends_on": "testboard_protected"},
    {"guard_id": "invalid_p_cleanup_deletes_testboard", "go_key": "cleanup_preserves_testboard", "depends_on": "cleanup_preserves_testboard"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_creates_local_static_model_test_lens_skeleton",
    "model_test_lens_is_not_whitebox_product_page",
    "model_test_lens_is_not_runtime",
    "model_test_lens_is_model_testing_viewer_only",
    "static_page_must_not_execute_models",
    "static_page_must_not_trigger_inference",
    "static_page_must_not_trigger_runtime",
    "static_page_must_not_call_output_adapter",
    "static_page_must_not_write_semantic_layer",
    "static_page_must_not_write_facts",
    "static_page_must_not_trigger_navigation_action_speech",
    "static_page_must_not_mutate_registry",
    "static_page_must_not_fetch_external_url",
    "static_page_must_not_access_camera",
    "static_page_must_not_access_microphone",
    "static_page_must_not_delete_artifacts",
    "local_json_loader_is_allowed",
    "builtin_example_loader_is_allowed",
    "mobile_sam_segmentation_example_is_required",
    "ten_model_panel_skeletons_are_required",
    "boundary_panel_is_required",
    "testboard_refs_panel_is_required",
    "candidate_outputs_remain_candidate",
    "readiness_effects_are_read_only",
    "testboard_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_testboard_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "model_test_lens_static_site_file_generation_record",
    "model_test_lens_example_loader_record",
    "model_test_lens_model_panel_skeleton_record",
    "model_test_lens_boundary_panel_record",
    "model_test_lens_no_runtime_no_model_execution_audit_record",
    "model_test_lens_static_site_post_review_record",
    "model_test_lens_followup_route_record",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_SKELETON_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_SKELETON_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_STATIC_SITE_SKELETON_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "model_test_lens_planning_reused": True,
}


@dataclass(frozen=True)
class P1MidplatformModelTestLensStaticSiteSkeletonExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    static_site_skeleton_execution: bool
    local_static_page_only: bool
    not_whitebox_product_page: bool
    model_testing_only: bool
    read_local_json_only: bool
    model_execution_allowed: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    upstream_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelTestLensStaticSiteFileGenerationRecord:
    record_id: str
    static_site_root_rel: str
    files_written: Tuple[str, ...]
    index_html_written: bool
    app_js_written: bool
    styles_css_written: bool
    readme_written: bool
    static_site_files_written: bool


@dataclass(frozen=True)
class ModelTestLensExampleLoaderRecord:
    record_id: str
    example_envelope_rel: str
    local_json_file_input: bool
    builtin_example_loader: bool
    example_loader_config_rel: str
    segmentation_example_available: bool
    no_external_url_fetch: bool


@dataclass(frozen=True)
class ModelTestLensModelPanelSkeletonRecord:
    record_id: str
    panels: Tuple[Dict[str, Any], ...]
    model_panel_count: int
    segmentation_active_example: bool


@dataclass(frozen=True)
class ModelTestLensBoundaryPanelRecord:
    record_id: str
    boundary_fields: Tuple[str, ...]
    boundary_panel_available: bool
    readiness_read_only: bool


@dataclass(frozen=True)
class ModelTestLensNoRuntimeNoModelExecutionAuditRecord:
    record_id: str
    no_model_execution: bool
    no_inference_execution: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_fact_navigation: bool
    no_registry_mutation: bool
    no_external_url: bool
    no_camera_microphone: bool
    no_delete_artifact_button: bool
    forbidden_pattern_scan_passed: bool


@dataclass(frozen=True)
class ModelTestLensStaticSitePostReviewAudit:
    audit_id: str
    static_site_files_written: bool
    index_html_written: bool
    app_js_written: bool
    styles_css_written: bool
    readme_written: bool
    model_panel_count: int
    segmentation_example_available: bool
    local_json_loader_available: bool
    example_loader_available: bool
    boundary_panel_available: bool
    testboard_refs_panel_available: bool
    no_model_execution: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_fact_navigation: bool
    no_registry_mutation: bool
    no_external_url: bool
    no_camera_microphone: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class ModelTestLensRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_can_remove_static_site_skeleton_files_if_needed: bool
    rollback_must_preserve_planning_artifacts: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_examples_if_referenced: bool
    rollback_not_executed_by_default: bool


@dataclass(frozen=True)
class ModelTestLensFollowupRouteRecord:
    route_id: str
    decision_branch: str
    recommended_next_phase: str
    next_phase_scope: str


@dataclass
class NegativeModelTestLensStaticSiteSkeletonGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MidplatformModelTestLensStaticSiteSkeletonExecutionDecision:
    decision_ref: str
    model_test_lens_static_site_skeleton_execution_profile_count: int
    static_site_files_written: bool
    model_panel_count: int
    segmentation_example_available: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
