# -*- coding: utf-8 -*-
"""P1 MobileSAM Real Local Image Inference Trial Request Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only).

Registers user-supplied scoped local test asset, plans image manifest and prompt points/boxes,
candidate-only output boundary, command whitelist, memory/timeout, rollback/cleanup, readiness.
Does NOT execute inference, read images as model input, import/load, runtime, registry mutation.
"""

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

PHASE_ID = "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1"
MOBILE_SAM_ASSET_ID = "mobile_sam"

PLANNING_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only。将用户上传实景图登记为 scoped local test asset，"
    "规划 image manifest、prompt points/boxes、candidate-only output boundary、command whitelist、"
    "memory/timeout、rollback/cleanup，发行窄范围 owner approval（仅 preparation + execution-next）。"
    "不执行 inference、不读图作为模型输入、不 import/model load、不 runtime/output adapter/语义层、"
    "不写 fact、不 navigation/action/speech、不改 registry、不额外下载。"
    "real image inference approval ≠ runtime/output/semantic/fact/navigation 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "real_local_image_inference_trial_request_approval_readiness_only_"
    "no_inference_no_image_input_approval_is_not_runtime"
)

COMPRESSED_PHASE = True
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
REAL_LOCAL_IMAGE_TRIAL_REQUEST_INCLUDED = True
REAL_LOCAL_IMAGE_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
REAL_LOCAL_IMAGE_TRIAL_READINESS_REVIEW_INCLUDED = True
SCOPED_LOCAL_TEST_ASSET_REGISTRATION = True
IMAGE_MANIFEST_PLANNING_ALLOWED = True
PROMPT_POINTS_BOXES_PLANNING_ALLOWED = True
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_TO_MODEL_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
UNCONTROLLED_DATASET_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_RUNTIME_BOUNDARY_PLANNING_REF = (
    "Phase-P1-MobileSAM-Runtime-Boundary-Standardization-Planning-v1-001"
)
UPSTREAM_RUNTIME_BOUNDARY_PLANNING_EXPECTED_GO = (
    "P1_MOBILE_SAM_RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING_GO"
)
UPSTREAM_PACKAGING_EXECUTION_REF = (
    "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION = (
    "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
REQUIRED_READINESS_LEVEL = "inference_trial_verified"

GOVERNANCE_MANIFEST_REL = (
    "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json"
)
GOVERNANCE_REFERENCE_POLICY_REL = (
    "capabilities/midplatform/governance_standards/index/governance_standards_reference_policy_v1.md"
)
RUNTIME_BOUNDARY_PLAN_MD_REL = (
    "capabilities/midplatform/governance_standards/runtime_boundary/"
    "mobile_sam_runtime_boundary_standardization/mobile_sam_runtime_boundary_standardization_plan_v1.md"
)
RUNTIME_ADMISSION_CRITERIA_JSON_REL = (
    "capabilities/midplatform/governance_standards/runtime_boundary/"
    "mobile_sam_runtime_boundary_standardization/mobile_sam_runtime_admission_criteria_v1.json"
)

TEST_ASSET_ID = "mobile_sam_real_local_image_street_scene_v1"
SOURCE_IMAGE_PATH = "/mnt/data/0B27F925-896F-4B92-B538-1D34253BB5A8.jpeg"
SOURCE_FILE_ID = "file_00000000dc487209a727d27711cc79d1"
SOURCE_TYPE = "user_supplied_scoped_local_test_asset"
SCENE_TYPE = "night_urban_street_scene"
SCOPED_FOR_PHASE = NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION

EXECUTION_MANIFEST_OUTPUT_REL = (
    "_tmp_eval_out/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1_smoke_v0/"
    "mobile_sam_real_local_image_manifest_v1.json"
)
CANDIDATE_OUTPUT_TARGET_DIR = (
    "_tmp_eval_out/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1_smoke_v0/"
)

PLANNED_MEMORY_LIMIT_MB = 4096
PLANNED_TIMEOUT_SECONDS = 300

BROAD_READINESS_MUST_BE_FALSE: Tuple[str, ...] = (
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "fact_write_ready",
    "navigation_action_speech_ready",
    "commercial_runtime_approved",
)

REQUIRED_REGISTRY_TRUE_FLAGS: Tuple[str, ...] = (
    "model_load_verified",
    "checkpoint_load_verified",
    "inference_trial_verified",
    "candidate_output_verified",
    "single_local_test_image_inference_verified",
)

PLANNED_MANIFEST_ENTRY: Dict[str, Any] = {
    "test_image_id": TEST_ASSET_ID,
    "local_path": SOURCE_IMAGE_PATH,
    "sha256": "pending_verification_in_execution_phase",
    "width": 0,
    "height": 0,
    "file_size_bytes": 0,
    "source_type": SOURCE_TYPE,
    "scene_type": SCENE_TYPE,
    "user_supplied": True,
    "personal_sensitive_image": False,
    "live_camera_frame": False,
    "external_url_source": False,
    "dataset_source": False,
    "navigation_runtime_frame": False,
    "fact_layer_source": False,
    "semantic_layer_source": False,
    "allowed_for_single_inference_trial": True,
    "must_not_enter_fact_layer": True,
    "must_not_enter_navigation_runtime": True,
    "must_not_enter_output_adapter": True,
    "must_not_enter_semantic_layer": True,
    "manifest_status": "planned_not_verified",
}

PLANNED_PROMPT_TARGETS: Tuple[Dict[str, Any], ...] = (
    {
        "target_id": "road_sign",
        "target_description": "road sign region (test prompt only)",
        "prompt_type": "point_or_box",
        "approximate_region": {"x_norm": 0.15, "y_norm": 0.25, "w_norm": 0.12, "h_norm": 0.10},
        "expected_output": "candidate_mask",
        "semantic_assertion_allowed": False,
        "fact_write_allowed": False,
    },
    {
        "target_id": "left_building",
        "target_description": "left building facade (test prompt only)",
        "prompt_type": "point_or_box",
        "approximate_region": {"x_norm": 0.05, "y_norm": 0.20, "w_norm": 0.25, "h_norm": 0.55},
        "expected_output": "candidate_mask",
        "semantic_assertion_allowed": False,
        "fact_write_allowed": False,
    },
    {
        "target_id": "center_advertisement_screen",
        "target_description": "center advertisement screen (test prompt only)",
        "prompt_type": "point_or_box",
        "approximate_region": {"x_norm": 0.42, "y_norm": 0.30, "w_norm": 0.18, "h_norm": 0.15},
        "expected_output": "candidate_mask",
        "semantic_assertion_allowed": False,
        "fact_write_allowed": False,
    },
    {
        "target_id": "front_vehicle",
        "target_description": "front vehicle region (test prompt only)",
        "prompt_type": "point_or_box",
        "approximate_region": {"x_norm": 0.55, "y_norm": 0.55, "w_norm": 0.30, "h_norm": 0.25},
        "expected_output": "candidate_mask",
        "semantic_assertion_allowed": False,
        "fact_write_allowed": False,
    },
    {
        "target_id": "crosswalk_or_road_region",
        "target_description": "crosswalk or road region (test prompt only)",
        "prompt_type": "point_or_box",
        "approximate_region": {"x_norm": 0.20, "y_norm": 0.70, "w_norm": 0.60, "h_norm": 0.20},
        "expected_output": "candidate_mask",
        "semantic_assertion_allowed": False,
        "fact_write_allowed": False,
    },
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_runtime_boundary_not_go", "go_key": "upstream_runtime_boundary_go", "depends_on": "upstream_runtime_boundary_go"},
    {"guard_id": "invalid_b_registry_not_inference_trial_verified", "go_key": "registry_inference_trial_verified", "depends_on": "registry_inference_trial_verified"},
    {"guard_id": "invalid_c_real_inference_executed", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_d_image_input_to_model", "go_key": "no_image_input_to_model", "depends_on": "no_image_input_to_model"},
    {"guard_id": "invalid_e_real_import_model_load", "go_key": "no_real_import_load", "depends_on": "no_real_import_load"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_fact_navigation_speech", "go_key": "no_fact_navigation_speech", "depends_on": "no_fact_navigation_speech"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_j_forbidden_image_source", "go_key": "image_source_allowed", "depends_on": "image_source_allowed"},
    {"guard_id": "invalid_k_personal_sensitive_image", "go_key": "not_personal_sensitive", "depends_on": "not_personal_sensitive"},
    {"guard_id": "invalid_l_prompt_label_as_semantic_fact", "go_key": "prompt_labels_not_semantic_facts", "depends_on": "prompt_labels_not_semantic_facts"},
    {"guard_id": "invalid_m_candidate_boundary_missing", "go_key": "candidate_boundary_present", "depends_on": "candidate_boundary_present"},
    {"guard_id": "invalid_n_owner_approval_expanded", "go_key": "approval_not_downstream", "depends_on": "approval_not_downstream"},
    {"guard_id": "invalid_o_whitelist_allows_forbidden", "go_key": "whitelist_strict", "depends_on": "whitelist_strict"},
    {"guard_id": "invalid_p_rollback_missing", "go_key": "rollback_present", "depends_on": "rollback_present"},
    {"guard_id": "invalid_q_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_r_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_s_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_real_local_image_inference_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "source_image_must_be_scoped_local_test_asset",
    "live_camera_is_not_allowed",
    "external_url_image_is_not_allowed",
    "uncontrolled_dataset_is_not_allowed",
    "personal_sensitive_image_is_not_allowed",
    "real_inference_is_not_allowed_in_this_phase",
    "image_input_to_model_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed_in_this_phase",
    "model_load_is_not_allowed_in_this_phase",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "prompt_labels_are_test_descriptions_only",
    "prompt_labels_are_not_semantic_facts",
    "segmentation_output_is_candidate_mask_only",
    "candidate_output_must_not_enter_fact_layer",
    "candidate_output_must_not_enter_runtime",
    "candidate_output_must_not_enter_output_adapter",
    "candidate_output_must_not_enter_semantic_layer",
    "candidate_output_must_not_trigger_navigation_action_speech",
    "approval_is_not_runtime_approval",
    "approval_is_not_output_adapter_approval",
    "approval_is_not_semantic_fact_navigation_approval",
    "approval_is_not_registry_mutation_approval",
    "real_image_execution_requires_next_phase",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "real_local_image_asset_registration_record",
    "real_local_image_manifest_plan_record",
    "real_local_image_prompt_plan_record",
    "real_local_image_candidate_output_boundary_record",
    "real_local_image_owner_approval_issuance_record",
    "real_local_image_command_whitelist_record",
    "real_local_image_memory_timeout_boundary_record",
    "real_local_image_rollback_cleanup_plan_record",
    "real_local_image_readiness_review_record",
    "real_local_image_followup_execution_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_REAL_LOCAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_REAL_LOCAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "governance_standards_canonical_library_referenced": True,
    "runtime_boundary_standardization_reused": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    planning_only: bool
    mobile_sam_only: bool
    real_local_image_trial_request_included: bool
    real_local_image_owner_approval_issuance_included: bool
    real_local_image_trial_readiness_review_included: bool
    scoped_local_test_asset_registration: bool
    image_manifest_planning_allowed: bool
    prompt_points_boxes_planning_allowed: bool
    real_inference_allowed: bool
    segmentation_allowed: bool
    prediction_allowed: bool
    image_input_to_model_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    external_image_download_allowed: bool
    live_camera_allowed: bool
    uncontrolled_dataset_allowed: bool
    commercial_runtime_approved: bool
    upstream_runtime_boundary_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RealLocalImageAssetRegistrationRecord:
    record_id: str
    test_asset_id: str
    asset_id: str
    source_image_path: str
    source_file_id: str
    source_type: str
    scene_type: str
    scoped_for_phase: str
    allowed_for_single_phase_execution: bool
    live_camera_frame: bool
    external_url_source: bool
    uncontrolled_dataset_source: bool
    personal_sensitive_image: bool
    fact_layer_source: bool
    semantic_layer_source: bool
    navigation_runtime_frame: bool
    candidate_only_use: bool
    image_read_this_phase: bool
    inference_executed_this_phase: bool


@dataclass(frozen=True)
class RealLocalImageManifestPlanningRecord:
    record_id: str
    execution_manifest_output_rel: str
    planned_manifest_entry: Dict[str, Any]
    manifest_status: str
    sha256_verification_deferred_to_execution: bool
    image_read_this_phase: bool


@dataclass(frozen=True)
class RealLocalImagePromptPlanningRecord:
    record_id: str
    prompt_targets: Tuple[Dict[str, Any], ...]
    prompt_labels_are_test_descriptions_only: bool
    mobile_sam_does_not_produce_semantic_facts: bool
    prompt_target_label_is_not_fact_recognition: bool
    segmentation_output_is_candidate_mask_only: bool
    object_category_judgment_requires_separate_evidence: bool
    coordinates_are_test_prompts_not_fact_layer_positioning: bool


@dataclass(frozen=True)
class RealLocalImageCandidateOutputBoundaryRecord:
    record_id: str
    candidate_output_only: bool
    output_target_dir: str
    output_must_be_candidate: bool
    output_not_fact: bool
    output_not_runtime_output: bool
    output_not_output_adapter_output: bool
    output_not_semantic_output: bool
    output_not_navigation_action_speech: bool
    output_not_user_visible_runtime_output: bool
    output_requires_post_review: bool
    output_requires_quality_summary: bool
    output_requires_failure_mode_annotation: bool


@dataclass(frozen=True)
class RealLocalImageOwnerApprovalIssuanceRecord:
    record_id: str
    owner_approval_granted_for_real_local_image_inference_preparation: bool
    owner_approval_granted_for_real_local_image_inference_execution_next: bool
    runtime_approved: bool
    output_adapter_approved: bool
    semantic_layer_approved: bool
    fact_write_approved: bool
    navigation_action_speech_approved: bool
    commercial_runtime_approved: bool
    registry_mutation_approved: bool
    additional_download_approved: bool
    external_image_use_approved: bool
    live_camera_use_approved: bool
    real_image_inference_approval_not_runtime_approval: bool
    real_image_inference_approval_not_output_adapter_approval: bool
    real_image_inference_approval_not_semantic_layer_approval: bool
    real_image_inference_approval_not_fact_write_approval: bool
    real_image_inference_approval_not_navigation_action_speech_approval: bool
    real_image_inference_approval_not_registry_mutation_approval: bool
    real_image_inference_approval_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class RealLocalImageCommandWhitelistRecord:
    record_id: str
    allowed_future_steps: Tuple[str, ...]
    forbidden_future_steps: Tuple[str, ...]
    command_template_only: bool
    command_not_executed: bool
    real_image_command_requires_next_phase: bool


@dataclass(frozen=True)
class RealLocalImageMemoryTimeoutBoundaryRecord:
    record_id: str
    memory_limit_mb: int
    timeout_seconds: int
    oom_handling_required: bool
    timeout_failure_records_required: bool
    candidate_output_cleanup_required_if_failed: bool
    no_persistent_runtime_process_allowed: bool


@dataclass(frozen=True)
class RealLocalImageRollbackCleanupPlanningRecord:
    record_id: str
    pre_inference_snapshot_required: bool
    rollback_required: bool
    rollback_preserves_registry: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    rollback_preserves_source_uploaded_image: bool
    candidate_output_cleanup_required_if_failed: bool
    no_fact_write_on_failure: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class RealLocalImageReadinessReview:
    review_id: str
    can_enter_real_local_image_inference_trial_execution_next: bool
    real_local_image_trial_execution_scope: str
    execution_requires_manifest: bool
    execution_requires_weight_sha256_recheck: bool
    execution_requires_model_load_verified: bool
    execution_requires_inference_trial_verified: bool
    execution_requires_candidate_output_boundary: bool
    execution_requires_prompt_plan: bool
    execution_requires_post_review: bool
    can_enter_runtime_after_this_phase: bool
    can_enter_output_adapter_after_this_phase: bool
    can_enter_semantic_layer_after_this_phase: bool
    can_write_fact_after_this_phase: bool
    can_trigger_navigation_action_speech_after_this_phase: bool


@dataclass(frozen=True)
class RealLocalImageFollowupExecutionRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_manifest_image_read: bool
    next_phase_allows_import_model_load: bool
    next_phase_allows_planned_prompt_segmentation: bool
    next_phase_still_no_runtime: bool
    next_phase_still_candidate_only: bool


@dataclass
class NegativeRealLocalImageInferenceTrialRequestApprovalGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_real_local_image_inference_request_readiness_profile_count: int
    real_local_image_asset_registration_record_count: int
    real_local_image_manifest_plan_record_count: int
    real_local_image_prompt_plan_record_count: int
    real_local_image_candidate_output_boundary_record_count: int
    real_local_image_owner_approval_issuance_record_count: int
    real_local_image_command_whitelist_record_count: int
    real_local_image_memory_timeout_boundary_record_count: int
    real_local_image_rollback_cleanup_plan_record_count: int
    real_local_image_readiness_review_record_count: int
    real_local_image_followup_execution_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    can_enter_real_local_image_inference_trial_execution_next: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
