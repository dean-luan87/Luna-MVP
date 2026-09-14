# -*- coding: utf-8 -*-
"""P1 MobileSAM Multi Real Image Inference Trial Request Approval And Readiness — types v1."""

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

PHASE_ID = "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1"
MOBILE_SAM_ASSET_ID = "mobile_sam"

PLANNING_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only。登记另外 4 张街景图为 scoped local test asset，"
    "规划 multi-image manifest、每图 prompt plan、candidate-only output boundary、command whitelist、"
    "memory/timeout(600s)、rollback/cleanup，发行窄范围 owner approval。"
    "不执行 inference、不读图作为模型输入、不 import/model load、不 runtime/output/semantic/fact/navigation、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "multi_real_image_inference_trial_request_approval_readiness_only_no_inference"
)

COMPRESSED_PHASE = True
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
MULTI_REAL_IMAGE_TRIAL_REQUEST_INCLUDED = True
MULTI_REAL_IMAGE_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
MULTI_REAL_IMAGE_TRIAL_READINESS_REVIEW_INCLUDED = True
SCOPED_LOCAL_TEST_ASSET_REGISTRATION = True
MULTI_IMAGE_MANIFEST_PLANNING_ALLOWED = True
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
UPSTREAM_QUALITY_REVIEW_REF = (
    "Phase-P1-MobileSAM-Real-Image-Quality-Review-And-Prompt-Strategy-Planning-v1-001"
)
UPSTREAM_QUALITY_REVIEW_EXPECTED_GO = (
    "P1_MOBILE_SAM_REAL_IMAGE_QUALITY_REVIEW_PROMPT_STRATEGY_PLANNING_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_MULTI_EXECUTION = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)
SCOPED_FOR_PHASE = NEXT_PHASE_MULTI_EXECUTION

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
REQUIRED_READINESS_LEVEL = "inference_trial_verified"
SOURCE_TYPE = "user_supplied_scoped_local_test_asset"
MULTI_IMAGE_COUNT = 4

GOVERNANCE_MANIFEST_REL = (
    "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json"
)
GOVERNANCE_REFERENCE_POLICY_REL = (
    "capabilities/midplatform/governance_standards/index/governance_standards_reference_policy_v1.md"
)

EXECUTION_MANIFEST_OUTPUT_REL = (
    "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/"
    "mobile_sam_multi_real_image_manifest_v1.json"
)
CANDIDATE_OUTPUT_TARGET_DIR = (
    "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/"
)

PLANNED_MEMORY_LIMIT_MB = 4096
PLANNED_TIMEOUT_SECONDS = 600
TIMEOUT_RATIONALE = "multiple_image_prompt_execution_four_images_five_prompts_each"

CURSOR_ASSETS_DIR = (
    "/Users/luanlei/.cursor/projects/Users-luanlei-Desktop-Luna-Workspace-Min/assets"
)
MULTI_TEST_ASSETS_DIR_REL = "capabilities/test_assets/p1/mobile_sam/multi"
EXCLUDED_SINGLE_TRIAL_CURSOR_FILE = "image-46caa285-b501-4e06-a6c3-72ed6a9e474b.png"

MULTI_IMAGE_ASSET_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_001",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_001.png",
        "cursor_asset_filename": "image-37f0c55b-49c8-40fb-bc7c-3b468b354f12.png",
        "source_file_id": "cursor_asset_image_37f0c55b",
        "scene_type": "daytime_tree_lined_sidewalk_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_002",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_002.png",
        "cursor_asset_filename": "image-5cfa18a2-cd0f-47fc-9275-4a158ca23455.png",
        "source_file_id": "cursor_asset_image_5cfa18a2",
        "scene_type": "daytime_hazy_urban_street_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_003",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_003.png",
        "cursor_asset_filename": "image-25b23081-3486-4836-b093-8ef1d70c3664.png",
        "source_file_id": "cursor_asset_image_25b23081",
        "scene_type": "daytime_street_vendor_stalls_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_004",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_004.png",
        "cursor_asset_filename": "image-f0cfef10-0457-4294-bb6d-884ede06f4fe.png",
        "source_file_id": "cursor_asset_image_f0cfef10",
        "scene_type": "daytime_sidewalk_scooters_scene",
    },
)

PROMPT_TARGET_TEMPLATES: Tuple[Dict[str, Any], ...] = (
    {
        "prompt_id": "building_or_large_structure",
        "target_description": "building or large structure (test description only)",
        "prompt_type_preferred": "box",
        "approximate_region_placeholder": "left_or_dominant_building_region",
    },
    {
        "prompt_id": "road_or_crosswalk_or_large_plane",
        "target_description": "road or crosswalk or large plane (test description only)",
        "prompt_type_preferred": "box_plus_negative_or_multi_point",
        "approximate_region_placeholder": "lower_road_or_crosswalk_region",
    },
    {
        "prompt_id": "sign_or_advertisement_screen",
        "target_description": "sign or advertisement screen (test description only)",
        "prompt_type_preferred": "box_or_point",
        "approximate_region_placeholder": "sign_or_screen_region",
    },
    {
        "prompt_id": "vehicle_or_small_dynamic_object",
        "target_description": "vehicle or small dynamic object (test description only)",
        "prompt_type_preferred": "box_or_point",
        "approximate_region_placeholder": "vehicle_region",
    },
    {
        "prompt_id": "street_facility_or_pole_or_edge_object",
        "target_description": "street facility pole or edge object (test description only)",
        "prompt_type_preferred": "box_or_point",
        "approximate_region_placeholder": "pole_or_facility_region",
    },
)

BROAD_READINESS_MUST_BE_FALSE: Tuple[str, ...] = (
    "inference_ready", "runtime_ready", "output_adapter_ready", "semantic_layer_ready",
    "fact_write_ready", "navigation_action_speech_ready", "commercial_runtime_approved",
)
REQUIRED_REGISTRY_TRUE_FLAGS: Tuple[str, ...] = (
    "model_load_verified", "checkpoint_load_verified", "inference_trial_verified",
    "candidate_output_verified", "single_local_test_image_inference_verified",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_quality_not_go", "go_key": "upstream_quality_review_go", "depends_on": "upstream_quality_review_go"},
    {"guard_id": "invalid_b_registry_not_inference_trial_verified", "go_key": "registry_inference_trial_verified", "depends_on": "registry_inference_trial_verified"},
    {"guard_id": "invalid_c_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_d_image_input_to_model", "go_key": "no_image_input_to_model", "depends_on": "no_image_input_to_model"},
    {"guard_id": "invalid_e_import_model_load", "go_key": "no_real_import_load", "depends_on": "no_real_import_load"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_fact_navigation_speech", "go_key": "no_fact_navigation_speech", "depends_on": "no_fact_navigation_speech"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_j_forbidden_image_source", "go_key": "image_source_allowed", "depends_on": "image_source_allowed"},
    {"guard_id": "invalid_k_personal_sensitive", "go_key": "not_personal_sensitive", "depends_on": "not_personal_sensitive"},
    {"guard_id": "invalid_l_no_fabricated_assets", "go_key": "four_assets_discovered", "depends_on": "four_assets_discovered"},
    {"guard_id": "invalid_m_prompt_label_as_fact", "go_key": "prompt_labels_not_facts", "depends_on": "prompt_labels_not_facts"},
    {"guard_id": "invalid_n_candidate_boundary_missing", "go_key": "candidate_boundary_present", "depends_on": "candidate_boundary_present"},
    {"guard_id": "invalid_o_owner_approval_expanded", "go_key": "approval_not_downstream", "depends_on": "approval_not_downstream"},
    {"guard_id": "invalid_p_whitelist_forbidden", "go_key": "whitelist_strict", "depends_on": "whitelist_strict"},
    {"guard_id": "invalid_q_rollback_missing", "go_key": "rollback_present", "depends_on": "rollback_present"},
    {"guard_id": "invalid_r_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_s_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_t_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_multi_real_image_inference_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "source_images_must_be_scoped_local_test_assets",
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
    "multi_image_execution_requires_next_phase",
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
    "multi_real_image_asset_discovery_record",
    "multi_real_image_asset_registration_record",
    "multi_real_image_manifest_plan_record",
    "multi_real_image_prompt_plan_record",
    "multi_real_image_candidate_output_boundary_record",
    "multi_real_image_owner_approval_issuance_record",
    "multi_real_image_command_whitelist_record",
    "multi_real_image_memory_timeout_boundary_record",
    "multi_real_image_rollback_cleanup_plan_record",
    "multi_real_image_readiness_review_record",
    "multi_real_image_followup_execution_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_FAILED = (
    "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_FAILED_NO_BOUNDARY_VIOLATION"
)
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "upstream_quality_review_reused": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    planning_only: bool
    mobile_sam_only: bool
    multi_real_image_trial_request_included: bool
    multi_real_image_owner_approval_issuance_included: bool
    multi_real_image_trial_readiness_review_included: bool
    scoped_local_test_asset_registration: bool
    multi_image_manifest_planning_allowed: bool
    prompt_points_boxes_planning_allowed: bool
    real_inference_allowed: bool
    image_input_to_model_allowed: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    upstream_quality_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MultiRealImageAssetDiscoveryRecord:
    record_id: str
    discovery_sources: Tuple[str, ...]
    discovered_count: int
    required_count: int
    excluded_single_trial_asset: str
    discovery_succeeded: bool


@dataclass(frozen=True)
class MultiRealImageAssetRegistrationRecord:
    record_id: str
    registered_assets: Tuple[Dict[str, Any], ...]
    registered_count: int
    source_type: str
    scoped_for_phase: str
    candidate_only_use: bool
    image_read_this_phase: bool


@dataclass(frozen=True)
class MultiRealImageManifestPlanningRecord:
    record_id: str
    execution_manifest_output_rel: str
    planned_manifest_entries: Tuple[Dict[str, Any], ...]
    sha256_verification_deferred_to_execution: bool


@dataclass(frozen=True)
class MultiRealImagePromptPlanningRecord:
    record_id: str
    prompt_plans: Tuple[Dict[str, Any], ...]
    prompt_labels_are_test_descriptions_only: bool
    semantic_fact_assertion_allowed: bool


@dataclass(frozen=True)
class MultiRealImageCandidateOutputBoundaryRecord:
    record_id: str
    candidate_output_only: bool
    output_target_dir: str
    per_image_candidate_masks_required: bool
    per_prompt_quality_summary_required: bool
    aggregate_quality_summary_required: bool
    output_not_fact: bool
    output_requires_post_review: bool


@dataclass(frozen=True)
class MultiRealImageOwnerApprovalIssuanceRecord:
    record_id: str
    owner_approval_granted_for_multi_real_image_inference_preparation: bool
    owner_approval_granted_for_multi_real_image_inference_execution_next: bool
    runtime_approved: bool
    output_adapter_approved: bool
    semantic_layer_approved: bool
    fact_write_approved: bool
    multi_image_inference_approval_not_runtime_approval: bool


@dataclass(frozen=True)
class MultiRealImageCommandWhitelistRecord:
    record_id: str
    allowed_future_steps: Tuple[str, ...]
    forbidden_future_steps: Tuple[str, ...]
    command_template_only: bool


@dataclass(frozen=True)
class MultiRealImageMemoryTimeoutBoundaryRecord:
    record_id: str
    memory_limit_mb: int
    timeout_seconds: int
    timeout_rationale: str
    oom_handling_required: bool
    no_persistent_runtime_process_allowed: bool


@dataclass(frozen=True)
class MultiRealImageRollbackCleanupPlanningRecord:
    record_id: str
    pre_inference_snapshot_required: bool
    rollback_required: bool
    rollback_preserves_source_uploaded_images: bool
    rollback_preserves_test_board: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class MultiRealImageReadinessReview:
    review_id: str
    can_enter_multi_real_image_inference_trial_execution_next: bool
    multi_real_image_trial_execution_scope: str
    execution_requires_manifest: bool
    execution_requires_prompt_plan: bool
    can_enter_runtime_after_this_phase: bool


@dataclass(frozen=True)
class MultiRealImageFollowupExecutionRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_still_candidate_only: bool


@dataclass
class NegativeMultiRealImageInferenceTrialRequestApprovalGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMMultiRealImageInferenceTrialRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_multi_real_image_inference_request_readiness_profile_count: int
    multi_real_image_asset_discovery_record_count: int
    multi_real_image_asset_registration_record_count: int
    multi_real_image_manifest_plan_record_count: int
    multi_real_image_prompt_plan_record_count: int
    multi_real_image_candidate_output_boundary_record_count: int
    multi_real_image_owner_approval_issuance_record_count: int
    multi_real_image_command_whitelist_record_count: int
    multi_real_image_memory_timeout_boundary_record_count: int
    multi_real_image_rollback_cleanup_plan_record_count: int
    multi_real_image_readiness_review_record_count: int
    multi_real_image_followup_execution_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    source_image_count: int
    test_board_record_count: int
    can_enter_multi_real_image_inference_trial_execution_next: bool
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
