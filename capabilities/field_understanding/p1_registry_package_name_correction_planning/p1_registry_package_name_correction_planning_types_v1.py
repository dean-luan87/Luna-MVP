# -*- coding: utf-8 -*-
"""P1 Registry Package Name Correction Planning — types v1.

PLANNING ONLY, scope = byte_track ONLY.

Goal is NOT to install byte_track but to clarify its IDENTITY relationship inside
the registry: is the registry package name wrong (A), the import name wrong (B),
is it actually NOT a clean PyPI package and should be a source_component (C), or
should it be split into a byte_track asset + a yolox dependency/source family
(D)?

It plans the registry correction; it MUTATES NOTHING and executes NOTHING: no
registry file write, no package/import name replacement, no pip install, no git
clone, no source install, no model/weight/dataset download, no real import, no
model load, no inference, no runtime, no output adapter, no semantic layer.

Registry correction planning success is NOT registry mutation approval, NOT
source install approval, and NOT weight download approval. byte_track remains
DEFERRED. Protected, non-deletable test board records are written in planning
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

PHASE_ID = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
SCOPE = "p1_registry_package_name_correction_planning"
SOURCE_CHAIN = "p1_registry_package_name_correction_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "针对 byte_track 的 registry package/import 映射问题做纠正规划。只规划 registry correction，不修改 registry、不写"
    " registry 文件、不替换 package/import 名、不 pip install、不 git clone、不源码安装、不下载模型/权重/数据集、不真实"
    " import / model load / inference、不进入 runtime / output adapter / 语义层。本阶段判断 byte_track 到底是 (A) "
    "registry 包名写错、(B) import 名写错、(C) 本就不是 clean PyPI package 应转 source_component、还是 (D) 应拆成 "
    "byte_track asset + yolox dependency/source family。registry correction planning 成功 ≠ registry mutation 批准 ≠ "
    "source install 批准 ≠ weight download 批准；byte_track 保持 DEFERRED。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "byte_track_registry_identity_is_correction_planning_only_no_registry_mutation_no_install_no_download"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
REGISTRY_CORRECTION_PLANNING_ONLY = True
REGISTRY_MUTATION_ALLOWED = False
PACKAGE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
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

UPSTREAM_RESOLUTION_PLANNING_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidates (this phase only routes; it does NOT create them).
SOURCE_INSTALL_RESOLUTION_PHASE_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
NEXT_STEP_REF = SOURCE_INSTALL_RESOLUTION_PHASE_REF

UPSTREAM_RESOLUTION_PLANNING_EXPECTED_GO = "P1_SOURCE_INSTALL_AND_PACKAGE_NAME_RESOLUTION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Input scope (locked) — ONLY byte_track.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_ID = "byte_track"
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "mobile_sam", "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

# byte_track provenance across the upstream chain (must be confirmed).
BYTE_TRACK_PROVENANCE: Dict[str, Any] = {
    "asset_id": "byte_track",
    "from_execution_deferred": UPSTREAM_EXECUTION_REF,
    "from_post_review_deferred_asset_audit": UPSTREAM_POST_REVIEW_REF,
    "from_resolution_planning_candidate": UPSTREAM_RESOLUTION_PLANNING_REF,
}

# Current registry mapping under review.
CURRENT_MAPPING: Dict[str, Any] = {
    "asset_id": "byte_track",
    "current_package_candidate": "bytetrack",
    "current_import_candidate": "yolox",
    "clean_pypi_install_status": "unresolved_or_failed",
    "find_spec_status": "not_found_or_deferred",
    "deferred_reason_tokens": ("package_name_resolution_required",),
    "current_mapping_is_not_accepted_for_full_install": True,
    "current_mapping_requires_correction_planning": True,
}

# Issue classifications (>=1 each kind).
PACKAGE_NAME_ISSUE_CLASSIFICATIONS: Tuple[Dict[str, Any], ...] = (
    {
        "classification_id": "byte_track_package_name_mismatch",
        "asset_id": "byte_track",
        "issue_kind": "package_name_mismatch",
        "current_package_candidate": "bytetrack",
        "clean_pypi_install_route_confirmed": False,
        "must_not_continue_as_clean_package_install_go": True,
        "notes": "package_candidate_bytetrack_may_not_be_correct_clean_pypi_name",
    },
)
IMPORT_NAME_ISSUE_CLASSIFICATIONS: Tuple[Dict[str, Any], ...] = (
    {
        "classification_id": "byte_track_import_name_mismatch",
        "asset_id": "byte_track",
        "issue_kind": "import_name_mismatch",
        "current_import_candidate": "yolox",
        "import_inconsistent_with_asset_id": True,
        "yolox_role_to_confirm": "dependency_or_source_family_or_runtime_import_root",
        "notes": "import_candidate_yolox_inconsistent_with_asset_id_byte_track",
    },
)
SOURCE_COMPONENT_CLASSIFICATIONS: Tuple[Dict[str, Any], ...] = (
    {
        "classification_id": "byte_track_source_component_classification",
        "asset_id": "byte_track",
        "issue_kind": "source_component_classification",
        "may_not_be_standalone_pypi_package": True,
        "may_model_as_source_component": "ByteTrack_YOLOX",
        "may_remove_from_clean_pypi_install_candidate": True,
        "notes": "byte_track_may_be_bytetrack_yolox_source_component_not_clean_pypi_package",
    },
)

# Registry correction options (>=3, + optional D).
REGISTRY_CORRECTION_OPTIONS: Tuple[Dict[str, Any], ...] = (
    {
        "option_id": "option_a_keep_asset_mark_package_unresolved",
        "asset_id": "byte_track",
        "package_name": "unresolved",
        "import_name": "yolox",
        "source_family": None,
        "primary_asset": None,
        "dependency_or_source_root": None,
        "install_method": "source_or_unresolved",
        "clean_pypi_candidate": False,
        "dependency_expansion_required": False,
        "requires_source_install_resolution": True,
    },
    {
        "option_id": "option_b_classify_as_source_component",
        "asset_id": "byte_track",
        "package_name": "none_or_source",
        "import_name": "yolox",
        "source_family": "ByteTrack_YOLOX",
        "primary_asset": None,
        "dependency_or_source_root": None,
        "install_method": "source_component",
        "clean_pypi_candidate": False,
        "dependency_expansion_required": False,
        "requires_source_install_resolution": True,
    },
    {
        "option_id": "option_c_split_into_asset_and_dependency",
        "asset_id": "byte_track",
        "package_name": "unresolved",
        "import_name": "yolox",
        "source_family": "ByteTrack_YOLOX",
        "primary_asset": "byte_track",
        "dependency_or_source_root": "yolox",
        "install_method": "source_component",
        "clean_pypi_candidate": False,
        "dependency_expansion_required": True,
        "requires_source_install_resolution": True,
    },
    {
        "option_id": "option_d_verified_clean_pypi_name_candidate_only",
        "asset_id": "byte_track",
        "package_name": "candidate_only_if_verified_in_local_registry_evidence",
        "import_name": "yolox",
        "source_family": None,
        "primary_asset": None,
        "dependency_or_source_root": None,
        "install_method": "candidate_only_no_install_no_mutation",
        "clean_pypi_candidate": False,
        "dependency_expansion_required": False,
        "requires_source_install_resolution": True,
    },
)

# Recommendation.
REGISTRY_CORRECTION_RECOMMENDATION: Dict[str, Any] = {
    "recommendation_id": "byte_track_registry_correction_recommendation",
    "asset_id": "byte_track",
    "byte_track_should_not_remain_clean_pypi_candidate_until_corrected": True,
    "byte_track_should_remain_deferred": True,
    "byte_track_should_enter_source_install_resolution_planning": True,
    "registry_mutation_requires_separate_review_or_patch_phase": True,
    "registry_correction_planning_success_is_not_registry_mutation_approval": True,
    "recommended_registry_action": "mark_byte_track_as_source_component_or_unresolved_package",
    "recommended_next_phase": SOURCE_INSTALL_RESOLUTION_PHASE_REF,
    "optional_patch_phase_required_before_runtime": True,
}

# Registry mutation boundary (must all hold).
REGISTRY_MUTATION_BOUNDARY: Dict[str, Any] = {
    "boundary_id": "byte_track_registry_mutation_boundary",
    "registry_mutation_allowed": False,
    "no_registry_file_write": True,
    "no_replacement_of_package_name": True,
    "no_replacement_of_import_name": True,
    "no_promotion_to_install_ready": True,
    "no_promotion_to_runtime_ready": True,
    "no_promotion_to_inference_ready": True,
    "no_promotion_to_model_ready": True,
}

# Follow-up review requirement.
FOLLOWUP_REVIEW_REQUIREMENT: Dict[str, Any] = {
    "requirement_id": "byte_track_followup_review_requirement",
    "asset_id": "byte_track",
    "source_install_resolution_required": True,
    "registry_patch_required_before_future_clean_execution": True,
    "owner_approval_required_before_source_install": True,
    "dependency_expansion_review_required": True,
    "license_review_required": True,
    "weight_download_requires_separate_approval": True,
    "recommended_next_phase": SOURCE_INSTALL_RESOLUTION_PHASE_REF,
}

# --------------------------------------------------------------------------- #
# Negative guards (19: Invalid A..S).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_registry_file_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_b_byte_track_marked_clean_pypi_install_ready", "go_key": "not_clean_pypi_install_ready", "depends_on": "not_clean_pypi_install_ready"},
    {"guard_id": "invalid_c_byte_track_marked_runtime_ready", "go_key": "not_runtime_ready", "depends_on": "not_runtime_ready"},
    {"guard_id": "invalid_d_byte_track_marked_inference_ready", "go_key": "not_inference_ready", "depends_on": "not_inference_ready"},
    {"guard_id": "invalid_e_pip_install_executed", "go_key": "no_pip_install", "depends_on": "no_pip_install"},
    {"guard_id": "invalid_f_git_clone_or_source_install_executed", "go_key": "no_git_clone_source_install", "depends_on": "no_git_clone_source_install"},
    {"guard_id": "invalid_g_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_h_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_i_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_j_package_name_mismatch_not_recorded", "go_key": "package_name_mismatch_recorded", "depends_on": "package_name_mismatch_recorded"},
    {"guard_id": "invalid_k_import_name_mismatch_not_recorded", "go_key": "import_name_mismatch_recorded", "depends_on": "import_name_mismatch_recorded"},
    {"guard_id": "invalid_l_source_component_classification_not_recorded", "go_key": "source_component_classification_recorded", "depends_on": "source_component_classification_recorded"},
    {"guard_id": "invalid_m_source_install_resolution_followup_not_output", "go_key": "source_install_resolution_followup_recorded", "depends_on": "source_install_resolution_followup_recorded"},
    {"guard_id": "invalid_n_planning_treated_as_registry_mutation_approval", "go_key": "planning_not_registry_mutation_approval", "depends_on": "planning_not_registry_mutation_approval"},
    {"guard_id": "invalid_o_planning_treated_as_source_install_approval", "go_key": "planning_not_source_install_approval", "depends_on": "planning_not_source_install_approval"},
    {"guard_id": "invalid_p_planning_treated_as_weight_download_approval", "go_key": "planning_not_weight_approval", "depends_on": "planning_not_weight_approval"},
    {"guard_id": "invalid_q_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_r_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_s_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (35 phase + 6 test board = 41).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_registry_package_name_correction_planning_only",
    "only_byte_track_is_in_scope",
    "mobile_sam_is_out_of_scope_for_this_phase",
    "no_registry_mutation_is_allowed",
    "no_registry_file_write_is_allowed",
    "no_pip_install_is_allowed",
    "no_git_clone_is_allowed",
    "no_source_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "byte_track_package_name_mismatch_must_be_recorded",
    "byte_track_import_name_mismatch_must_be_recorded",
    "byte_track_source_component_classification_must_be_recorded",
    "byte_track_must_not_be_promoted_to_clean_pypi_install_ready_in_this_phase",
    "byte_track_must_remain_deferred",
    "source_install_resolution_followup_is_required",
    "registry_mutation_requires_separate_patch_or_review",
    "registry_correction_planning_is_not_registry_mutation_approval",
    "registry_correction_planning_is_not_source_install_approval",
    "registry_correction_planning_is_not_weight_download_approval",
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
    "registry_correction_plan_record",
    "package_import_mapping_record",
    "source_component_classification_record",
    "registry_mutation_boundary_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1RegistryPackageNameCorrectionPlanningProfile",
    "RegistryCorrectionInputRecord",
    "CurrentPackageImportMappingRecord",
    "PackageNameIssueClassification",
    "ImportNameIssueClassification",
    "SourceComponentClassification",
    "RegistryCorrectionOption",
    "RegistryCorrectionRecommendation",
    "RegistryMutationBoundary",
    "FollowupReviewRequirement",
    "NegativeRegistryCorrectionPlanningGuard",
    "P1RegistryPackageNameCorrectionPlanningDecision",
)

FINAL_DECISION_GO = "P1_REGISTRY_PACKAGE_NAME_CORRECTION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_REGISTRY_PACKAGE_NAME_CORRECTION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1RegistryPackageNameCorrectionPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    registry_correction_planning_only: bool
    registry_mutation_allowed: bool
    package_install_allowed: bool
    pip_install_allowed: bool
    git_clone_allowed: bool
    source_install_allowed: bool
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
    in_scope_asset_id: str
    upstream_resolution_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RegistryCorrectionInputRecord:
    asset_id: str
    from_execution_deferred: str
    from_post_review_deferred_asset_audit: str
    from_resolution_planning_candidate: str
    provenance_confirmed: bool


@dataclass(frozen=True)
class CurrentPackageImportMappingRecord:
    asset_id: str
    current_package_candidate: str
    current_import_candidate: str
    clean_pypi_install_status: str
    find_spec_status: str
    deferred_reason_tokens: Tuple[str, ...]
    current_mapping_is_not_accepted_for_full_install: bool
    current_mapping_requires_correction_planning: bool


@dataclass(frozen=True)
class PackageNameIssueClassification:
    classification_id: str
    asset_id: str
    issue_kind: str
    current_package_candidate: str
    clean_pypi_install_route_confirmed: bool
    must_not_continue_as_clean_package_install_go: bool
    notes: str


@dataclass(frozen=True)
class ImportNameIssueClassification:
    classification_id: str
    asset_id: str
    issue_kind: str
    current_import_candidate: str
    import_inconsistent_with_asset_id: bool
    yolox_role_to_confirm: str
    notes: str


@dataclass(frozen=True)
class SourceComponentClassification:
    classification_id: str
    asset_id: str
    issue_kind: str
    may_not_be_standalone_pypi_package: bool
    may_model_as_source_component: str
    may_remove_from_clean_pypi_install_candidate: bool
    notes: str


@dataclass(frozen=True)
class RegistryCorrectionOption:
    option_id: str
    asset_id: str
    package_name: Any
    import_name: str
    source_family: Any
    primary_asset: Any
    dependency_or_source_root: Any
    install_method: str
    clean_pypi_candidate: bool
    dependency_expansion_required: bool
    requires_source_install_resolution: bool


@dataclass(frozen=True)
class RegistryCorrectionRecommendation:
    recommendation_id: str
    asset_id: str
    byte_track_should_not_remain_clean_pypi_candidate_until_corrected: bool
    byte_track_should_remain_deferred: bool
    byte_track_should_enter_source_install_resolution_planning: bool
    registry_mutation_requires_separate_review_or_patch_phase: bool
    registry_correction_planning_success_is_not_registry_mutation_approval: bool
    recommended_registry_action: str
    recommended_next_phase: str
    optional_patch_phase_required_before_runtime: bool


@dataclass(frozen=True)
class RegistryMutationBoundary:
    boundary_id: str
    registry_mutation_allowed: bool
    no_registry_file_write: bool
    no_replacement_of_package_name: bool
    no_replacement_of_import_name: bool
    no_promotion_to_install_ready: bool
    no_promotion_to_runtime_ready: bool
    no_promotion_to_inference_ready: bool
    no_promotion_to_model_ready: bool


@dataclass(frozen=True)
class FollowupReviewRequirement:
    requirement_id: str
    asset_id: str
    source_install_resolution_required: bool
    registry_patch_required_before_future_clean_execution: bool
    owner_approval_required_before_source_install: bool
    dependency_expansion_review_required: bool
    license_review_required: bool
    weight_download_requires_separate_approval: bool
    recommended_next_phase: str


@dataclass
class NegativeRegistryCorrectionPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1RegistryPackageNameCorrectionPlanningDecision:
    decision_ref: str
    registry_package_name_correction_planning_profile_count: int
    registry_correction_input_record_count: int
    current_package_import_mapping_record_count: int
    package_name_issue_classification_count: int
    import_name_issue_classification_count: int
    source_component_classification_count: int
    registry_correction_option_count: int
    registry_correction_recommendation_count: int
    registry_mutation_boundary_count: int
    followup_review_requirement_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
