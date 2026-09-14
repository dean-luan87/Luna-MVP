# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Resolution Planning — types v1.

PLANNING ONLY for the two honestly-deferred assets byte_track and mobile_sam.

Unifies their source-install route resolution and decides the follow-up:
  byte_track -> registry patch / source_component / source install approval
  mobile_sam -> source install approval / weight boundary review

It executes NOTHING and MUTATES NOTHING: no git clone, no source checkout, no
source install, no pip install, no dependency install, no model/weight/dataset
download, no real import, no model load, no inference, no runtime, no output
adapter, no semantic layer, NO registry mutation, and NO network repository
lookup (repository refs are planning-only placeholders).

Source install is higher risk than ordinary pip package install and must re-run
the full request -> approval -> preparation -> execution -> post-review chain.
Source install planning is NOT source install approval and NOT weight download
approval. Both assets REMAIN DEFERRED. Protected, non-deletable test board
records are written in planning mode.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
SCOPE = "p1_controlled_source_install_resolution_planning"
SOURCE_CHAIN = "p1_controlled_source_install_resolution_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "对 byte_track 与 mobile_sam 的源码安装路线进行统一解析规划。只做 source install resolution planning，不 git "
    "clone、不 source checkout、不源码安装、不 pip install、不安装依赖、不下载模型/权重/数据集、不真实 import / model "
    "load / inference、不进入 runtime / output adapter / 语义层、不修改 registry、不联网检索仓库（repository ref 仅为 "
    "planning placeholder）。源码安装链风险高于普通 pip 包安装，必须重新走 request → approval → preparation → "
    "execution → post-review。source install planning 成功 ≠ source install 批准 ≠ weight download 批准；byte_track 与 "
    "mobile_sam 保持 DEFERRED。byte_track 路线：registry patch / source_component / source install approval；"
    "mobile_sam 路线：source install approval / weight boundary review。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "byte_track_and_mobile_sam_source_routes_are_resolution_planning_only_no_clone_no_checkout_no_install_no_download_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_ONLY = True
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

UPSTREAM_REGISTRY_CORRECTION_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
UPSTREAM_RESOLUTION_PLANNING_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidates (this phase only routes; it does NOT create them).
SOURCE_INSTALL_REQUEST_PLANNING_PHASE_REF = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
REGISTRY_PATCH_PLANNING_PHASE_REF = "Phase-P1-Registry-Package-Name-Correction-Patch-Planning-v1-001"
NEXT_STEP_REF = SOURCE_INSTALL_REQUEST_PLANNING_PHASE_REF

UPSTREAM_REGISTRY_CORRECTION_EXPECTED_GO = "P1_REGISTRY_PACKAGE_NAME_CORRECTION_PLANNING_GO"
UPSTREAM_RESOLUTION_PLANNING_EXPECTED_GO = "P1_SOURCE_INSTALL_AND_PACKAGE_NAME_RESOLUTION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Input scope (locked) — ONLY the two deferred assets.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

# --------------------------------------------------------------------------- #
# Per-asset input + route data.
# --------------------------------------------------------------------------- #
SOURCE_INSTALL_INPUT_ASSETS: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "current_status": "DEFERRED",
        "from_execution_deferred": UPSTREAM_EXECUTION_REF,
        "from_post_review_deferred_asset_audit": UPSTREAM_POST_REVIEW_REF,
        "from_resolution_planning_candidate": UPSTREAM_RESOLUTION_PLANNING_REF,
        "from_registry_correction_planning": UPSTREAM_REGISTRY_CORRECTION_REF,
        "source_family": "ByteTrack_YOLOX",
        "registry_correction_recommendation": "source_component_or_unresolved_package",
        "clean_pypi_candidate": False,
        "git_source_install_detected": True,
        "source_install_resolution_required": True,
    },
    {
        "asset_id": "mobile_sam",
        "current_status": "DEFERRED",
        "from_execution_deferred": UPSTREAM_EXECUTION_REF,
        "from_post_review_deferred_asset_audit": UPSTREAM_POST_REVIEW_REF,
        "from_resolution_planning_candidate": UPSTREAM_RESOLUTION_PLANNING_REF,
        "from_registry_correction_planning": None,
        "source_family": "MobileSAM",
        "registry_correction_recommendation": "source_install_method_binding",
        "clean_pypi_candidate": False,
        "git_source_install_detected": True,
        "source_install_resolution_required": True,
    },
)

SOURCE_ROUTE_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "source_family": "ByteTrack_YOLOX",
        "clean_pypi_candidate": False,
        "source_checkout_required": True,
        "source_checkout_allowed_now": False,
        "source_install_required": True,
        "source_install_allowed_now": False,
        "dependency_expansion_required": True,
        "license_review_required": True,
        "registry_patch_may_be_required": True,
        "weight_download_not_approved": True,
        "weight_boundary_required": True,
        "source_install_planning_success_not_source_install_approval": True,
        "source_install_planning_success_not_weight_download_approval": True,
        "remains_deferred": True,
    },
    {
        "asset_id": "mobile_sam",
        "source_family": "MobileSAM",
        "clean_pypi_candidate": False,
        "source_checkout_required": True,
        "source_checkout_allowed_now": False,
        "source_install_required": True,
        "source_install_allowed_now": False,
        "dependency_expansion_required": True,
        "license_review_required": True,
        "registry_patch_may_be_required": True,
        "weight_download_not_approved": True,
        "weight_boundary_required": True,
        "source_install_planning_success_not_source_install_approval": True,
        "source_install_planning_success_not_weight_download_approval": True,
        "remains_deferred": True,
    },
)

SOURCE_REPOSITORY_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "repository_ref_type": "placeholder",
        "repository_url_unverified": True,
        "repository_commit_not_pinned": True,
        "repository_license_not_verified": True,
        "repository_requires_future_review": True,
        "source_checkout_allowed_now": False,
        "network_lookup_performed": False,
    },
    {
        "asset_id": "mobile_sam",
        "repository_ref_type": "placeholder",
        "repository_url_unverified": True,
        "repository_commit_not_pinned": True,
        "repository_license_not_verified": True,
        "repository_requires_future_review": True,
        "source_checkout_allowed_now": False,
        "network_lookup_performed": False,
    },
)

DEPENDENCY_EXPANSION_RISK_DIMENSIONS: Tuple[str, ...] = (
    "build_or_compile_risk",
    "torch_dependency_risk",
    "opencv_dependency_risk",
    "numpy_scipy_dependency_risk",
    "local_env_contamination_risk",
)

SOURCE_COMMAND_TEMPLATE_REFS: Dict[str, str] = {
    "byte_track": "source_install_command_template_byte_track_v1_placeholder",
    "mobile_sam": "source_install_command_template_mobile_sam_v1_placeholder",
}

# Per-asset weight boundary specifics.
WEIGHT_BOUNDARY_SPECIFICS: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "tracker_or_detector_weights_may_be_needed_later": True,
        "checkpoint_weights_may_be_needed_later": False,
        "weight_boundary_required": True,
    },
    "mobile_sam": {
        "tracker_or_detector_weights_may_be_needed_later": False,
        "checkpoint_weights_may_be_needed_later": True,
        "weight_boundary_required": True,
    },
}

# Per-asset registry patch need.
REGISTRY_PATCH_NEED: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "registry_patch_likely_required": "true",
        "recommended_patch_direction": "source_component_or_unresolved_package",
        "registry_patch_before_source_install": "optional_but_recommended",
        "registry_patch_before_runtime": "required",
    },
    "mobile_sam": {
        "registry_patch_likely_required": "maybe",
        "recommended_patch_direction": "source_install_method_binding",
        "registry_patch_before_source_install": "optional",
        "registry_patch_before_runtime": "required",
    },
}

# Per-asset follow-up routing.
FOLLOWUP_ROUTING: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "recommended_next_phase": SOURCE_INSTALL_REQUEST_PLANNING_PHASE_REF,
        "alternate_next_phase": REGISTRY_PATCH_PLANNING_PHASE_REF,
        "asset_route": "registry_patch_optional_before_source_request_but_required_before_runtime",
        "no_weight_download_phase_until_source_install_post_review": True,
    },
    "mobile_sam": {
        "recommended_next_phase": SOURCE_INSTALL_REQUEST_PLANNING_PHASE_REF,
        "alternate_next_phase": REGISTRY_PATCH_PLANNING_PHASE_REF,
        "asset_route": "source_install_request_planning",
        "no_weight_download_phase_until_source_install_post_review": True,
    },
}

# --------------------------------------------------------------------------- #
# Negative guards (21: Invalid A..U).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_git_clone_executed", "go_key": "no_git_clone", "depends_on": "no_git_clone"},
    {"guard_id": "invalid_b_source_install_executed", "go_key": "no_source_install", "depends_on": "no_source_install"},
    {"guard_id": "invalid_c_pip_or_dependency_install_executed", "go_key": "no_pip_dependency_install", "depends_on": "no_pip_dependency_install"},
    {"guard_id": "invalid_d_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_e_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_f_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_g_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_byte_track_not_deferred", "go_key": "byte_track_remains_deferred", "depends_on": "byte_track_remains_deferred"},
    {"guard_id": "invalid_i_mobile_sam_not_deferred", "go_key": "mobile_sam_remains_deferred", "depends_on": "mobile_sam_remains_deferred"},
    {"guard_id": "invalid_j_planning_treated_as_source_install_approval", "go_key": "planning_not_source_install_approval", "depends_on": "planning_not_source_install_approval"},
    {"guard_id": "invalid_k_planning_treated_as_weight_download_approval", "go_key": "planning_not_weight_approval", "depends_on": "planning_not_weight_approval"},
    {"guard_id": "invalid_l_source_repository_marked_verified", "go_key": "repository_not_verified", "depends_on": "repository_not_verified"},
    {"guard_id": "invalid_m_repository_commit_marked_pinned", "go_key": "repository_commit_not_pinned", "depends_on": "repository_commit_not_pinned"},
    {"guard_id": "invalid_n_license_review_marked_completed", "go_key": "license_review_not_completed", "depends_on": "license_review_not_completed"},
    {"guard_id": "invalid_o_dependency_expansion_review_marked_completed", "go_key": "dependency_review_not_completed", "depends_on": "dependency_review_not_completed"},
    {"guard_id": "invalid_p_weight_download_approved_by_default", "go_key": "weight_not_approved_by_default", "depends_on": "weight_not_approved_by_default"},
    {"guard_id": "invalid_q_source_install_reuses_package_install_only_approval", "go_key": "source_install_not_reuse_pkg_approval", "depends_on": "source_install_not_reuse_pkg_approval"},
    {"guard_id": "invalid_r_post_install_probe_real_import_load_inference", "go_key": "post_install_probe_find_spec_only", "depends_on": "post_install_probe_find_spec_only"},
    {"guard_id": "invalid_s_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_t_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_u_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (38 phase + 6 test board = 44).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_source_install_resolution_planning_only",
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
    "byte_track_remains_deferred",
    "mobile_sam_remains_deferred",
    "source_repository_refs_are_placeholders_only",
    "repository_urls_are_unverified",
    "repository_commits_are_not_pinned",
    "repository_licenses_are_not_verified",
    "dependency_expansion_review_is_required",
    "license_review_is_required",
    "source_install_requires_separate_approval",
    "source_install_cannot_reuse_package_install_only_approval",
    "weight_download_requires_separate_approval",
    "source_install_approval_is_not_weight_download_approval",
    "commercial_runtime_is_not_approved",
    "registry_patch_before_runtime_is_required",
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
    "source_install_resolution_plan_record",
    "source_dependency_expansion_record",
    "source_license_boundary_record",
    "source_weight_boundary_record",
    "source_isolation_requirement_record",
    "source_followup_routing_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallResolutionProfile",
    "SourceInstallInputAsset",
    "SourceRouteCandidate",
    "SourceRepositoryCandidate",
    "SourceDependencyExpansionPlan",
    "SourceLicenseBoundaryPlan",
    "SourceWeightBoundaryPlan",
    "SourceIsolationRequirement",
    "SourceCommandWhitelistPlanningRecord",
    "SourceInstallApprovalRequirement",
    "SourceInstallRiskAssessment",
    "RegistryPatchNeedAssessment",
    "SourceInstallFollowupRouting",
    "NegativeControlledSourceInstallResolutionPlanningGuard",
    "P1ControlledSourceInstallResolutionPlanningDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallResolutionProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    controlled_source_install_resolution_planning_only: bool
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
    upstream_registry_correction_ref: str
    upstream_resolution_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceInstallInputAsset:
    asset_id: str
    current_status: str
    from_execution_deferred: str
    from_post_review_deferred_asset_audit: str
    from_resolution_planning_candidate: str
    from_registry_correction_planning: Any
    source_family: str
    registry_correction_recommendation: str
    clean_pypi_candidate: bool
    git_source_install_detected: bool
    source_install_resolution_required: bool
    provenance_confirmed: bool


@dataclass(frozen=True)
class SourceRouteCandidate:
    asset_id: str
    source_family: str
    clean_pypi_candidate: bool
    source_checkout_required: bool
    source_checkout_allowed_now: bool
    source_install_required: bool
    source_install_allowed_now: bool
    dependency_expansion_required: bool
    license_review_required: bool
    registry_patch_may_be_required: bool
    weight_download_not_approved: bool
    weight_boundary_required: bool
    source_install_planning_success_not_source_install_approval: bool
    source_install_planning_success_not_weight_download_approval: bool
    remains_deferred: bool


@dataclass(frozen=True)
class SourceRepositoryCandidate:
    asset_id: str
    repository_ref_type: str
    repository_url_unverified: bool
    repository_commit_not_pinned: bool
    repository_license_not_verified: bool
    repository_requires_future_review: bool
    source_checkout_allowed_now: bool
    network_lookup_performed: bool


@dataclass(frozen=True)
class SourceDependencyExpansionPlan:
    asset_id: str
    source_requirements_unknown_or_unverified: bool
    transitive_dependencies_unknown: bool
    risk_dimensions: Tuple[str, ...]
    dependency_expansion_review_required: bool
    source_install_must_not_use_package_install_only_approval: bool
    review_completed: bool


@dataclass(frozen=True)
class SourceLicenseBoundaryPlan:
    asset_id: str
    source_license_review_required: bool
    repository_license_unverified: bool
    transitive_dependency_license_review_required: bool
    commercial_runtime_not_approved: bool
    license_binding_required_before_source_install: bool
    source_install_success_would_not_commercial_runtime_approval: bool
    review_completed: bool


@dataclass(frozen=True)
class SourceWeightBoundaryPlan:
    asset_id: str
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    source_install_approval_not_weight_download_approval: bool
    weight_download_requires_separate_approval: bool
    weight_hash_required_before_future_inference: bool
    weight_source_review_required: bool
    tracker_or_detector_weights_may_be_needed_later: bool
    checkpoint_weights_may_be_needed_later: bool
    weight_boundary_required: bool


@dataclass(frozen=True)
class SourceIsolationRequirement:
    asset_id: str
    separate_source_install_env_required: bool
    no_global_site_packages_preferred: bool
    pre_source_install_snapshot_required: bool
    source_checkout_path_must_be_controlled: bool
    command_whitelist_required: bool
    network_scope_must_be_explicit: bool
    post_install_probe_find_spec_only: bool
    no_real_import_after_source_install_without_review: bool
    rollback_required: bool
    test_board_write_required: bool


@dataclass(frozen=True)
class SourceCommandWhitelistPlanningRecord:
    asset_id: str
    command_template_ref: str
    template_only: bool
    command_not_executed: bool
    git_clone_command_allowed_now: bool
    pip_install_command_allowed_now: bool
    weight_download_command_allowed_now: bool
    command_requires_future_owner_approval: bool
    command_requires_pre_snapshot: bool
    command_requires_license_review: bool
    command_requires_dependency_review: bool
    command_requires_rollback: bool


@dataclass(frozen=True)
class SourceInstallApprovalRequirement:
    asset_id: str
    source_install_owner_approval_required: bool
    source_install_request_phase_required: bool
    source_install_issuance_phase_required: bool
    source_install_execution_preparation_required: bool
    source_install_execution_phase_required: bool
    source_install_post_review_required: bool
    weight_download_separate_approval_required: bool


@dataclass(frozen=True)
class SourceInstallRiskAssessment:
    asset_id: str
    source_install_higher_risk_than_clean_pypi: bool
    risk_dimensions: Tuple[str, ...]
    source_install_must_be_isolated: bool
    source_install_must_not_share_package_install_only_approval: bool
    source_install_requires_separate_approval: bool
    all_risk_dimensions_recorded: bool


@dataclass(frozen=True)
class RegistryPatchNeedAssessment:
    asset_id: str
    registry_patch_likely_required: str
    recommended_patch_direction: str
    registry_patch_before_source_install: str
    registry_patch_before_runtime: str


@dataclass(frozen=True)
class SourceInstallFollowupRouting:
    asset_id: str
    recommended_next_phase: str
    alternate_next_phase: str
    asset_route: str
    no_weight_download_phase_until_source_install_post_review: bool
    source_install_requires_separate_approval: bool


@dataclass
class NegativeControlledSourceInstallResolutionPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallResolutionPlanningDecision:
    decision_ref: str
    controlled_source_install_resolution_profile_count: int
    source_install_input_asset_count: int
    source_route_candidate_count: int
    source_repository_candidate_count: int
    source_dependency_expansion_plan_count: int
    source_license_boundary_plan_count: int
    source_weight_boundary_plan_count: int
    source_isolation_requirement_count: int
    source_command_whitelist_planning_record_count: int
    source_install_approval_requirement_count: int
    source_install_risk_assessment_count: int
    registry_patch_need_assessment_count: int
    source_install_followup_routing_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
