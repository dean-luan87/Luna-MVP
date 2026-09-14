# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Request Planning — types v1.

PLANNING ONLY for the two honestly-deferred assets byte_track and mobile_sam.

It only GENERATES a source-install request package (scope, candidate assets,
network boundary, source repo placeholders, dependency-expansion review request,
license review request, isolation environment, rollback, post-install find_spec
probe request, weight boundary). It does NOT grant owner approval and executes
NOTHING and MUTATES NOTHING: no git clone, no source checkout, no source install,
no pip install, no dependency install, no model/weight/dataset download, no real
import, no model load, no inference, no runtime, no output adapter, no semantic
layer, NO registry mutation, and NO network repository lookup.

Request != Approval. Source install request success is NOT owner approval, NOT
source install approval, NOT git clone approval, NOT weight download approval.
Both assets REMAIN DEFERRED. Protected, non-deletable test board records are
written in planning mode.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
SCOPE = "p1_controlled_source_install_request_planning"
SOURCE_CHAIN = "p1_controlled_source_install_request_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "为 byte_track 与 mobile_sam 生成源码安装 request planning。只生成 source install request package，不生成 owner "
    "approval、不 git clone、不 source checkout、不源码安装、不 pip install、不安装依赖、不下载模型/权重/数据集、不真实 "
    "import / model load / inference、不进入 runtime / output adapter / 语义层、不修改 registry、不联网检索仓库"
    "（repository ref 仅为 placeholder）。Request ≠ Approval：source install request 成功 ≠ owner approval ≠ source "
    "install 批准 ≠ git clone 批准 ≠ weight download 批准；byte_track 与 mobile_sam 保持 DEFERRED。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "byte_track_and_mobile_sam_source_install_request_is_request_package_only_no_approval_no_clone_no_install_no_download"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
SOURCE_INSTALL_REQUEST_PLANNING_ONLY = True
SOURCE_INSTALL_REQUEST_PACKAGE_CREATED = True
OWNER_APPROVAL_GRANTED = False
REGISTRY_MUTATION_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_CHECKOUT_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_RESOLUTION_PLANNING_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
UPSTREAM_REGISTRY_CORRECTION_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
UPSTREAM_PACKAGE_RESOLUTION_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidates (this phase only routes; it does NOT create them).
OWNER_APPROVAL_ISSUANCE_PHASE_REF = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
REGISTRY_PATCH_PLANNING_PHASE_REF = "Phase-P1-Registry-Package-Name-Correction-Patch-Planning-v1-001"
NEXT_STEP_REF = OWNER_APPROVAL_ISSUANCE_PHASE_REF

UPSTREAM_RESOLUTION_PLANNING_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Request scope (locked) — ONLY the two deferred assets.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}

# Per-asset request scope specifics.
REQUEST_SCOPE_SPECIFICS: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "registry_patch_likely_required": "true",
        "registry_patch_before_source_install": "optional_but_recommended",
        "registry_patch_before_runtime": "required",
        "tracker_or_detector_weights_may_be_needed_later": True,
        "checkpoint_weights_may_be_needed_later": False,
    },
    "mobile_sam": {
        "registry_patch_likely_required": "maybe",
        "registry_patch_before_source_install": "optional",
        "registry_patch_before_runtime": "required",
        "tracker_or_detector_weights_may_be_needed_later": False,
        "checkpoint_weights_may_be_needed_later": True,
    },
}

DEPENDENCY_REVIEW_RISK_DIMENSIONS: Tuple[str, ...] = (
    "build_compile_risk_review_required",
    "torch_dependency_review_required",
    "opencv_dependency_review_required",
    "numpy_scipy_dependency_review_required",
    "dependency_conflict_review_required",
    "existing_env_contamination_review_required",
)

RISK_DISCLOSURE_DIMENSIONS: Tuple[str, ...] = (
    "dependency_expansion_risk",
    "license_risk",
    "source_setup_side_effect_risk",
    "build_or_compile_risk",
    "network_access_risk",
    "weight_download_risk",
    "environment_contamination_risk",
    "rollback_complexity_risk",
)

# Approval request boundary statements (>=8).
APPROVAL_REQUEST_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "source_install_request_success_not_owner_approval",
    "source_install_request_success_not_source_install_approval",
    "source_install_request_success_not_git_clone_approval",
    "source_install_request_success_not_weight_download_approval",
    "source_install_request_success_not_inference_approval",
    "source_install_request_success_not_runtime_approval",
    "source_install_request_success_not_output_adapter_approval",
    "source_install_request_success_not_semantic_layer_approval",
)

# --------------------------------------------------------------------------- #
# Negative guards (23: Invalid A..W).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_git_clone_or_source_checkout_executed", "go_key": "no_git_clone_checkout", "depends_on": "no_git_clone_checkout"},
    {"guard_id": "invalid_b_source_install_executed", "go_key": "no_source_install", "depends_on": "no_source_install"},
    {"guard_id": "invalid_c_pip_or_dependency_install_executed", "go_key": "no_pip_dependency_install", "depends_on": "no_pip_dependency_install"},
    {"guard_id": "invalid_d_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_e_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_f_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_g_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_request_scope_contains_other_asset", "go_key": "scope_limited_to_deferred", "depends_on": "scope_limited_to_deferred"},
    {"guard_id": "invalid_i_byte_track_or_mobile_sam_not_deferred", "go_key": "assets_remain_deferred", "depends_on": "assets_remain_deferred"},
    {"guard_id": "invalid_j_request_package_treated_as_owner_approval", "go_key": "request_not_owner_approval", "depends_on": "request_not_owner_approval"},
    {"guard_id": "invalid_k_request_package_treated_as_source_install_approval", "go_key": "request_not_source_install_approval", "depends_on": "request_not_source_install_approval"},
    {"guard_id": "invalid_l_request_package_treated_as_git_clone_approval", "go_key": "request_not_git_clone_approval", "depends_on": "request_not_git_clone_approval"},
    {"guard_id": "invalid_m_request_package_treated_as_weight_download_approval", "go_key": "request_not_weight_approval", "depends_on": "request_not_weight_approval"},
    {"guard_id": "invalid_n_repository_marked_verified", "go_key": "repository_not_verified", "depends_on": "repository_not_verified"},
    {"guard_id": "invalid_o_repository_commit_marked_pinned", "go_key": "repository_commit_not_pinned", "depends_on": "repository_commit_not_pinned"},
    {"guard_id": "invalid_p_license_review_marked_completed", "go_key": "license_review_not_completed", "depends_on": "license_review_not_completed"},
    {"guard_id": "invalid_q_dependency_expansion_review_marked_completed", "go_key": "dependency_review_not_completed", "depends_on": "dependency_review_not_completed"},
    {"guard_id": "invalid_r_network_boundary_request_missing", "go_key": "network_boundary_present", "depends_on": "network_boundary_present"},
    {"guard_id": "invalid_s_weight_download_approved_by_default", "go_key": "weight_not_approved_by_default", "depends_on": "weight_not_approved_by_default"},
    {"guard_id": "invalid_t_post_install_probe_real_import_load_inference_runtime", "go_key": "post_install_probe_find_spec_only", "depends_on": "post_install_probe_find_spec_only"},
    {"guard_id": "invalid_u_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_v_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_w_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (37 phase + 6 test board = 43).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_source_install_request_planning_only",
    "only_byte_track_and_mobile_sam_are_in_scope",
    "no_git_clone_is_allowed",
    "no_source_checkout_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_registry_mutation_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "source_install_request_is_not_owner_approval",
    "source_install_request_is_not_source_install_approval",
    "source_install_request_is_not_git_clone_approval",
    "source_install_request_is_not_weight_download_approval",
    "repository_refs_remain_placeholders",
    "repository_urls_remain_unverified",
    "repository_commits_remain_unpinned",
    "license_review_is_requested_not_completed",
    "dependency_expansion_review_is_requested_not_completed",
    "network_boundary_review_is_required",
    "weight_download_requires_separate_approval",
    "source_install_approval_cannot_approve_weight_download",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "source_install_request_package_record",
    "source_request_scope_record",
    "source_network_boundary_record",
    "source_dependency_review_request_record",
    "source_license_review_request_record",
    "source_weight_boundary_record",
    "source_isolation_request_record",
    "source_followup_approval_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallRequestPlanningProfile",
    "SourceInstallRequestPackage",
    "SourceInstallRequestScope",
    "SourceRepositoryRequestRef",
    "SourceNetworkBoundaryRequest",
    "SourceDependencyExpansionReviewRequest",
    "SourceLicenseReviewRequest",
    "SourceWeightBoundaryRequest",
    "SourceIsolationRequest",
    "SourceRollbackRequest",
    "SourcePostInstallProbeRequest",
    "SourceApprovalRequestBoundary",
    "SourceInstallRequestRiskDisclosure",
    "SourceInstallRequestFollowupRouting",
    "NegativeSourceInstallRequestPlanningGuard",
    "P1ControlledSourceInstallRequestPlanningDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_REQUEST_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_REQUEST_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallRequestPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    source_install_request_planning_only: bool
    source_install_request_package_created: bool
    owner_approval_granted: bool
    registry_mutation_allowed: bool
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_resolution_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceInstallRequestPackage:
    request_id: str
    phase_id: str
    request_type: str
    requested_assets: Tuple[str, ...]
    source_route_refs: Tuple[str, ...]
    repository_request_refs: Tuple[str, ...]
    network_boundary_request_refs: Tuple[str, ...]
    dependency_review_request_refs: Tuple[str, ...]
    license_review_request_refs: Tuple[str, ...]
    weight_boundary_request_refs: Tuple[str, ...]
    isolation_request_refs: Tuple[str, ...]
    rollback_request_refs: Tuple[str, ...]
    post_install_probe_request_refs: Tuple[str, ...]
    test_board_record_required: bool
    owner_approval_required: bool
    owner_approval_granted: bool
    source_install_allowed: bool
    request_package_complete: bool
    request_package_is_not_approval: bool
    request_package_is_not_source_install_approval: bool
    request_package_is_not_git_clone_approval: bool
    request_package_is_not_weight_download_approval: bool


@dataclass(frozen=True)
class SourceInstallRequestScope:
    asset_id: str
    source_family: str
    current_status: str
    registry_patch_likely_required: str
    registry_patch_before_source_install: str
    registry_patch_before_runtime: str
    source_install_request_created: bool
    source_install_approval_granted: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    weight_download_allowed: bool
    runtime_allowed: bool
    inference_allowed: bool


@dataclass(frozen=True)
class SourceRepositoryRequestRef:
    asset_id: str
    repository_ref_type: str
    repository_url_unverified: bool
    repository_commit_not_pinned: bool
    repository_license_not_verified: bool
    repository_requires_future_review: bool
    repository_verification_requested: bool
    source_checkout_allowed_now: bool


@dataclass(frozen=True)
class SourceNetworkBoundaryRequest:
    asset_id: str
    network_access_requires_approval: bool
    git_clone_network_scope_required: bool
    pip_network_scope_required: bool
    external_url_download_blocked_by_default: bool
    model_weight_download_blocked_by_default: bool
    dataset_download_blocked_by_default: bool
    example_asset_download_blocked_by_default: bool
    network_log_required: bool


@dataclass(frozen=True)
class SourceDependencyExpansionReviewRequest:
    asset_id: str
    source_requirements_review_required: bool
    transitive_dependency_review_required: bool
    risk_review_dimensions: Tuple[str, ...]
    review_completed: bool


@dataclass(frozen=True)
class SourceLicenseReviewRequest:
    asset_id: str
    source_license_review_required: bool
    repository_license_review_required: bool
    transitive_dependency_license_review_required: bool
    license_binding_required_before_source_install: bool
    commercial_runtime_not_approved: bool
    source_install_success_not_commercial_runtime_approval: bool
    review_completed: bool


@dataclass(frozen=True)
class SourceWeightBoundaryRequest:
    asset_id: str
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    source_install_request_not_weight_download_request: bool
    weight_download_requires_separate_approval: bool
    weight_hash_required_before_future_inference: bool
    weight_source_review_required: bool
    tracker_or_detector_weights_may_be_needed_later: bool
    checkpoint_weights_may_be_needed_later: bool
    weight_boundary_required: bool


@dataclass(frozen=True)
class SourceIsolationRequest:
    asset_id: str
    separate_source_install_env_required: bool
    no_global_site_packages_preferred: bool
    pre_source_install_snapshot_required: bool
    source_checkout_path_must_be_controlled: bool
    command_whitelist_required: bool
    post_install_probe_find_spec_only: bool
    no_real_import_after_source_install_without_review: bool
    rollback_required: bool
    test_board_write_required: bool


@dataclass(frozen=True)
class SourceRollbackRequest:
    asset_id: str
    rollback_required: bool
    rollback_trigger_conditions_required: bool
    rollback_template_required: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class SourcePostInstallProbeRequest:
    asset_id: str
    post_install_probe_required: bool
    probe_uses_find_spec_only: bool
    real_import_allowed: bool
    no_model_load_on_probe: bool
    no_inference_on_probe: bool
    no_runtime_on_probe: bool
    no_output_adapter_on_probe: bool
    installed_version_record_required: bool
    dependency_gap_recheck_required: bool
    license_recheck_required: bool
    test_board_probe_record_required: bool


@dataclass(frozen=True)
class SourceApprovalRequestBoundary:
    boundary_id: str
    statement: str
    holds: bool


@dataclass(frozen=True)
class SourceInstallRequestRiskDisclosure:
    asset_id: str
    risk_dimensions: Tuple[str, ...]
    owner_ack_required: bool
    all_risk_dimensions_disclosed: bool


@dataclass(frozen=True)
class SourceInstallRequestFollowupRouting:
    asset_id: str
    recommended_next_phase: str
    optional_registry_patch_phase: str
    registry_patch_before_source_install: str
    registry_patch_before_runtime: str
    no_source_install_execution_until_approval_issuance: bool
    no_weight_download_phase_until_source_install_post_review: bool


@dataclass
class NegativeSourceInstallRequestPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallRequestPlanningDecision:
    decision_ref: str
    controlled_source_install_request_planning_profile_count: int
    source_install_request_package_count: int
    source_install_request_scope_count: int
    source_repository_request_ref_count: int
    source_network_boundary_request_count: int
    source_dependency_expansion_review_request_count: int
    source_license_review_request_count: int
    source_weight_boundary_request_count: int
    source_isolation_request_count: int
    source_rollback_request_count: int
    source_post_install_probe_request_count: int
    source_approval_request_boundary_count: int
    source_install_request_risk_disclosure_count: int
    source_install_request_followup_routing_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
