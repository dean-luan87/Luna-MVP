# -*- coding: utf-8 -*-
"""P1 Source Install And Package Name Resolution Planning — types v1.

PLANNING ONLY for the two assets that were honestly DEFERRED during the first
real package-install-only execution: byte_track and mobile_sam.

It plans the source-install / package-name-resolution ROUTES; it executes
NOTHING: no git clone, no source install, no pip install, no dependency install,
no model/weight/dataset download, no real import, no model load, no inference, no
runtime, no output adapter, no semantic layer, and NO registry mutation.

Narrow goal:
  byte_track -> confirm the real install route for bytetrack / yolox / ByteTrack
                (registry package-name correction candidate + source install).
  mobile_sam -> confirm the git/source install route for mobile_sam / MobileSAM.

Source install is higher risk than a clean PyPI wheel, must be isolated, must
NOT share the package-install-only approval, and requires a SEPARATE approval.
Source install planning is NOT source install approval and NOT weight download
approval. Protected, non-deletable test board records are written in planning
mode.
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

PHASE_ID = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
SCOPE = "p1_source_install_and_package_name_resolution_planning"
SOURCE_CHAIN = "p1_source_install_and_package_name_resolution_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "对 package-install-only 执行阶段中被诚实 deferred 的两个资产 byte_track 与 mobile_sam，进行源码安装路线与包名解析"
    "规划。只规划，不执行源码安装、不 git clone、不 pip install、不下载模型/权重/数据集、不真实 import / model load / "
    "inference、不进入 runtime / output adapter / 语义层、不修改 registry。byte_track 规划 registry 包名纠正候选 + 源码"
    "安装候选（bytetrack / yolox / ByteTrack）；mobile_sam 规划 git/source install 路线（mobile_sam / MobileSAM）。"
    "源码安装风险高于 clean PyPI wheel，必须隔离、必须独立审批，不得复用 package-install-only 审批。源码安装规划 ≠ "
    "源码安装批准 ≠ 权重下载批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_source_install_and_package_name_resolution_is_planning_only_no_clone_no_source_install_no_download_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
SOURCE_INSTALL_PLANNING_ONLY = True
PACKAGE_NAME_RESOLUTION_PLANNING_ONLY = True
REGISTRY_MUTATION_ALLOWED = False
GIT_CLONE_ALLOWED = False
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

UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidates (this phase only routes; it does NOT create them).
REGISTRY_CORRECTION_PHASE_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
SOURCE_INSTALL_RESOLUTION_PHASE_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
# Recommended: do byte_track registry correction first, then source install.
NEXT_STEP_REF = REGISTRY_CORRECTION_PHASE_REF

UPSTREAM_POST_REVIEW_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_POST_REVIEW_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Input scope (locked) — ONLY the two deferred assets.
# --------------------------------------------------------------------------- #
DEFERRED_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

DEFERRED_ASSET_INPUTS: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "deferred_source_phase": UPSTREAM_EXECUTION_REF,
        "registry_package_candidate": "bytetrack",
        "registry_import_candidate": "yolox",
        "clean_pypi_install_completed": False,
        "find_spec_hit": False,
        "deferred_reason_tokens": ("package_name_resolution_required",),
    },
    {
        "asset_id": "mobile_sam",
        "deferred_source_phase": UPSTREAM_EXECUTION_REF,
        "registry_package_candidate": "mobile_sam_or_git_source",
        "registry_import_candidate": "mobile_sam",
        "clean_pypi_install_completed": False,
        "find_spec_hit": False,
        "deferred_reason_tokens": ("git_source", "not_clean_pypi_wheel"),
    },
)

# --------------------------------------------------------------------------- #
# Package-name resolution candidates (planning only; no registry mutation).
# --------------------------------------------------------------------------- #
PACKAGE_NAME_RESOLUTION_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "byte_track_registry_package_name_correction",
        "asset_id": "byte_track",
        "candidate_kind": "registry_package_name_correction",
        "issue": "package_name_mismatch_and_import_name_mismatch",
        "current_package_name": "bytetrack",
        "current_import_name": "yolox",
        "correction_required": True,
        "registry_mutation_now": False,
        "requires_registry_correction_review": True,
        "next_phase_candidate": REGISTRY_CORRECTION_PHASE_REF,
    },
)

# --------------------------------------------------------------------------- #
# Source install route candidates (planning only).
# --------------------------------------------------------------------------- #
SOURCE_INSTALL_ROUTE_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "byte_track_source_install_route",
        "asset_id": "byte_track",
        "source_family": "ByteTrack_yolox",
        "git_or_source_install_required": True,
        "git_clone_now": False,
        "source_install_now": False,
        "requires_source_install_approval": True,
        "requires_dependency_expansion_review": True,
        "requires_license_review": True,
        "requires_no_weight_download_boundary": True,
        "requires_weight_boundary_review": False,
        "next_phase_candidate": SOURCE_INSTALL_RESOLUTION_PHASE_REF,
    },
    {
        "candidate_id": "mobile_sam_source_install_route",
        "asset_id": "mobile_sam",
        "source_family": "MobileSAM",
        "git_or_source_install_required": True,
        "git_clone_now": False,
        "source_install_now": False,
        "requires_source_install_approval": True,
        "requires_dependency_expansion_review": True,
        "requires_license_review": True,
        "requires_no_weight_download_boundary": True,
        "requires_weight_boundary_review": True,
        "next_phase_candidate": SOURCE_INSTALL_RESOLUTION_PHASE_REF,
    },
)

# --------------------------------------------------------------------------- #
# Registry correction candidates (planning only; no mutation).
# --------------------------------------------------------------------------- #
REGISTRY_CORRECTION_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_id": "byte_track_registry_correction_candidate",
        "asset_id": "byte_track",
        "current_package_name": "bytetrack",
        "current_import_name": "yolox",
        "correction_required": True,
        "registry_mutation_now": False,
        "requires_registry_correction_review": True,
        "next_phase_candidate": REGISTRY_CORRECTION_PHASE_REF,
    },
)

# Per-asset risk dimensions (must all be recorded).
SOURCE_INSTALL_RISK_DIMENSIONS: Tuple[str, ...] = (
    "dependency_expansion_risk",
    "source_setup_side_effect_risk",
    "build_or_compile_risk",
    "license_risk",
    "transitive_dependency_risk",
    "network_access_risk",
    "weight_download_risk",
    "example_asset_download_risk",
    "import_side_effect_risk",
    "rollback_complexity_risk",
)

# Execution isolation requirement items (planned for the FUTURE source install).
EXECUTION_ISOLATION_ITEMS: Tuple[str, ...] = (
    "separate_isolated_environment_recommended",
    "pre_source_install_snapshot_required",
    "source_checkout_path_must_be_controlled",
    "no_global_site_packages_preferred_unless_separately_justified",
    "command_whitelist_required",
    "no_post_install_real_import",
    "post_install_probe_must_remain_find_spec_only",
    "rollback_path_required",
    "test_board_write_required",
)

# Follow-up routing (planning).
FOLLOWUP_ROUTING: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "requires_registry_package_name_correction_planning": True,
        "requires_source_install_resolution_planning": True,
        "recommended_next_phase_refs": (REGISTRY_CORRECTION_PHASE_REF, SOURCE_INSTALL_RESOLUTION_PHASE_REF),
        "route_split_allowed": True,
        "recommended_first": REGISTRY_CORRECTION_PHASE_REF,
    },
    {
        "asset_id": "mobile_sam",
        "requires_registry_package_name_correction_planning": False,
        "requires_source_install_resolution_planning": True,
        "recommended_next_phase_refs": (SOURCE_INSTALL_RESOLUTION_PHASE_REF,),
        "route_split_allowed": False,
        "recommended_first": SOURCE_INSTALL_RESOLUTION_PHASE_REF,
    },
)

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_git_clone_executed", "go_key": "no_git_clone", "depends_on": "no_git_clone"},
    {"guard_id": "invalid_b_source_install_executed", "go_key": "no_source_install", "depends_on": "no_source_install"},
    {"guard_id": "invalid_c_pip_install_executed", "go_key": "no_pip_install", "depends_on": "no_pip_install"},
    {"guard_id": "invalid_d_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_e_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_f_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_g_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_byte_track_resolution_not_recorded", "go_key": "byte_track_resolution_recorded", "depends_on": "byte_track_resolution_recorded"},
    {"guard_id": "invalid_i_mobile_sam_source_required_not_recorded", "go_key": "mobile_sam_source_required_recorded", "depends_on": "mobile_sam_source_required_recorded"},
    {"guard_id": "invalid_j_source_install_treated_as_clean_pypi", "go_key": "source_install_not_clean_pypi", "depends_on": "source_install_not_clean_pypi"},
    {"guard_id": "invalid_k_planning_treated_as_source_install_approval", "go_key": "planning_not_source_install_approval", "depends_on": "planning_not_source_install_approval"},
    {"guard_id": "invalid_l_planning_treated_as_weight_download_approval", "go_key": "planning_not_weight_approval", "depends_on": "planning_not_weight_approval"},
    {"guard_id": "invalid_m_weight_download_approved_by_default", "go_key": "weight_not_approved_by_default", "depends_on": "weight_not_approved_by_default"},
    {"guard_id": "invalid_n_license_review_skipped", "go_key": "license_review_required", "depends_on": "license_review_required"},
    {"guard_id": "invalid_o_dependency_expansion_review_skipped", "go_key": "dependency_expansion_review_required", "depends_on": "dependency_expansion_review_required"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (32 phase + 6 test board = 38).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_source_install_and_package_name_resolution_planning_only",
    "no_git_clone_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
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
    "byte_track_requires_package_name_resolution",
    "byte_track_source_install_requires_separate_approval",
    "mobile_sam_source_install_requires_separate_approval",
    "source_install_is_not_clean_pypi_package_install",
    "source_install_planning_is_not_source_install_approval",
    "source_install_planning_is_not_weight_download_approval",
    "weight_download_requires_separate_approval",
    "license_review_is_required",
    "dependency_expansion_review_is_required",
    "source_install_isolation_is_required",
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
    "deferred_asset_resolution_plan_record",
    "source_install_risk_record",
    "registry_correction_candidate_record",
    "weight_boundary_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1SourceInstallPackageResolutionProfile",
    "DeferredAssetResolutionInput",
    "PackageNameResolutionCandidate",
    "SourceInstallRouteCandidate",
    "RegistryCorrectionCandidate",
    "SourceInstallRiskAssessment",
    "DependencyExpansionAssessment",
    "WeightBoundaryAssessment",
    "LicenseBoundaryAssessment",
    "ExecutionIsolationRequirement",
    "FollowupPhaseRoutingRecord",
    "NegativeSourceInstallResolutionPlanningGuard",
    "P1SourceInstallPackageResolutionPlanningDecision",
)

FINAL_DECISION_GO = "P1_SOURCE_INSTALL_AND_PACKAGE_NAME_RESOLUTION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_SOURCE_INSTALL_AND_PACKAGE_NAME_RESOLUTION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1SourceInstallPackageResolutionProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    source_install_planning_only: bool
    package_name_resolution_planning_only: bool
    registry_mutation_allowed: bool
    git_clone_allowed: bool
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
    upstream_post_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    deferred_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class DeferredAssetResolutionInput:
    asset_id: str
    deferred_source_phase: str
    registry_package_candidate: str
    registry_import_candidate: str
    clean_pypi_install_completed: bool
    find_spec_hit: bool
    deferred_reason_tokens: Tuple[str, ...]
    confirmed_deferred_from_execution_phase: bool


@dataclass(frozen=True)
class PackageNameResolutionCandidate:
    candidate_id: str
    asset_id: str
    candidate_kind: str
    issue: str
    current_package_name: str
    current_import_name: str
    correction_required: bool
    registry_mutation_now: bool
    requires_registry_correction_review: bool
    next_phase_candidate: str


@dataclass(frozen=True)
class SourceInstallRouteCandidate:
    candidate_id: str
    asset_id: str
    source_family: str
    git_or_source_install_required: bool
    git_clone_now: bool
    source_install_now: bool
    requires_source_install_approval: bool
    requires_dependency_expansion_review: bool
    requires_license_review: bool
    requires_no_weight_download_boundary: bool
    requires_weight_boundary_review: bool
    next_phase_candidate: str


@dataclass(frozen=True)
class RegistryCorrectionCandidate:
    candidate_id: str
    asset_id: str
    current_package_name: str
    current_import_name: str
    correction_required: bool
    registry_mutation_now: bool
    requires_registry_correction_review: bool
    next_phase_candidate: str


@dataclass(frozen=True)
class SourceInstallRiskAssessment:
    asset_id: str
    risk_dimensions: Tuple[str, ...]
    source_install_higher_risk_than_clean_pypi: bool
    source_install_must_be_isolated: bool
    source_install_must_not_share_package_install_only_approval: bool
    source_install_requires_separate_approval: bool
    all_risk_dimensions_recorded: bool


@dataclass(frozen=True)
class DependencyExpansionAssessment:
    asset_id: str
    dependency_expansion_review_required: bool
    transitive_dependency_review_required: bool
    build_or_compile_dependency_possible: bool
    dependency_install_now: bool
    assessment_recorded: bool


@dataclass(frozen=True)
class WeightBoundaryAssessment:
    asset_id: str
    source_install_approval_is_not_weight_download_approval: bool
    source_install_planning_is_not_weight_readiness: bool
    weights_may_be_required_later_not_now: bool
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    weight_download_requires_separate_approval: bool
    weight_boundary_recorded: bool


@dataclass(frozen=True)
class LicenseBoundaryAssessment:
    asset_id: str
    license_review_required_before_source_install: bool
    source_license_must_bind_to_asset_id: bool
    transitive_dependency_license_review_required: bool
    commercial_runtime_not_approved: bool
    source_install_success_would_not_approve_commercial_runtime: bool
    license_boundary_recorded: bool


@dataclass(frozen=True)
class ExecutionIsolationRequirement:
    asset_id: str
    isolation_items: Tuple[str, ...]
    separate_isolated_environment_recommended: bool
    pre_source_install_snapshot_required: bool
    command_whitelist_required: bool
    post_install_probe_find_spec_only: bool
    rollback_path_required: bool
    test_board_write_required: bool
    all_isolation_items_recorded: bool


@dataclass(frozen=True)
class FollowupPhaseRoutingRecord:
    asset_id: str
    requires_registry_package_name_correction_planning: bool
    requires_source_install_resolution_planning: bool
    recommended_next_phase_refs: Tuple[str, ...]
    route_split_allowed: bool
    recommended_first: str
    deferred_assets_require_separate_phase: bool
    source_install_requires_separate_approval: bool
    registry_correction_requires_separate_review: bool


@dataclass
class NegativeSourceInstallResolutionPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1SourceInstallPackageResolutionPlanningDecision:
    decision_ref: str
    source_install_package_resolution_profile_count: int
    deferred_asset_resolution_input_count: int
    package_name_resolution_candidate_count: int
    source_install_route_candidate_count: int
    registry_correction_candidate_count: int
    source_install_risk_assessment_count: int
    dependency_expansion_assessment_count: int
    weight_boundary_assessment_count: int
    license_boundary_assessment_count: int
    execution_isolation_requirement_count: int
    followup_phase_routing_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
