# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution Post-Review — types v1 (AUDIT ONLY).

Post-review of the first real controlled source-install execution
(Phase-P1-Controlled-Source-Install-Execution-v1-001). It only AUDITS the
execution artifacts: snapshot, repository verification, commit pin, checkout /
code-install records, network log, find_spec probe, deferred results, the
all-deferred partial-go semantics, the test board, and the non-runtime boundary.

It introduces a precise PARTIAL_GO subtype taxonomy to avoid future confusion:
  * partial_success        -> at least 1 asset succeeded
  * all_deferred_no_violation -> 0 succeeded, all deferred, no boundary violation
This execution belongs to the SECOND subtype: it is NOT full GO, NOT source
install success, but also NOT a blocker.

It executes/mutates NOTHING and does NOT re-install deferred assets: no git clone,
no source checkout, no source install, no pip install, no dependency install, no
model/weight/dataset/example download, no real import, no model load, no
inference, no runtime, no output adapter, no semantic layer, no registry
mutation. Protected, non-deletable test board records are written in post_review
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Execution-Post-Review-v1-001"
SCOPE = "p1_controlled_source_install_execution_post_review"
SOURCE_CHAIN = "p1_controlled_source_install_execution_post_review_v1"

POST_REVIEW_PRINCIPLE_ZH = (
    "对第一次真实 controlled source install execution 的事后复核。只审查 execution artifact、snapshot、repository "
    "verification、commit pin、checkout/code install 记录、network log、find_spec probe、deferred 结果、all-deferred "
    "partial-go 语义、test board 与 non-runtime 边界。新增 PARTIAL_GO 子类型：partial_success（≥1 成功）与 "
    "all_deferred_no_violation（0 成功、全部 deferred、无边界违规）；本次属于第二类——不是 full GO、不是 source install "
    "成功，但也不是 blocker。本阶段不 clone、不 checkout、不源码安装、不 pip install、不安装依赖、不下载模型/权重/数据集/"
    "示例资产、不真实 import / model load / inference、不进入 runtime / output adapter / 语义层、不修改 registry、不补装 "
    "deferred 资产。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_install_execution_post_review_is_audit_only_all_deferred_partial_go_is_not_full_go_not_install_success_not_blocker"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
SOURCE_EXECUTION_POST_REVIEW = True
NO_NEW_EXECUTION_ALLOWED = True

REGISTRY_MUTATION_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_CHECKOUT_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Source-Install-Execution-v1-001"
UPSTREAM_PREP_READINESS_REF = "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001"
UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
UPSTREAM_RESOLUTION_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_EXECUTION_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_CODE_ONLY_PARTIAL_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# This post-review only ROUTES to the next planning phase; it does NOT create it.
RECOMMENDED_NEXT_PHASE_REF = "Phase-P1-Source-Repository-Verification-And-Commit-Pin-Planning-v1-001"
NEXT_STEP_REF = RECOMMENDED_NEXT_PHASE_REF

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "post_review"

PARTIAL_GO_SUBTYPE = "all_deferred_no_violation"
PARTIAL_GO_SUBTYPES: Tuple[str, ...] = ("partial_success", "all_deferred_no_violation")

# --------------------------------------------------------------------------- #
# Audited scope (the two deferred assets).
# --------------------------------------------------------------------------- #
AUDITED_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}

# Expected upstream execution summary (for the artifact audit).
EXPECTED_EXECUTION_SUMMARY: Dict[str, Any] = {
    "final_decision": UPSTREAM_EXECUTION_EXPECTED_GO,
    "blocker_count": 0,
    "negative_guard_passed": 22,
    "attempted_source_asset_count": 0,
    "successful_source_asset_count": 0,
    "deferred_source_asset_count": 2,
    "failed_source_asset_count": 0,
    "all_assets_deferred": True,
}

# Per-asset deferred-reason tokens.
DEFERRED_REASONS: Dict[str, Tuple[str, ...]] = {
    "byte_track": (
        "repository_placeholder_unverified",
        "commit_not_pinned",
        "license_not_verified",
        "package_import_identity_unresolved_or_source_component",
    ),
    "mobile_sam": (
        "repository_placeholder_unverified",
        "commit_not_pinned",
        "license_not_verified",
        "weight_excluding_checkout_required",
    ),
}

# Non-execution boundary statements (17 >= 16 required).
NON_EXECUTION_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "no_git_clone",
    "no_source_checkout",
    "no_source_install",
    "no_pip_install",
    "no_dependency_install",
    "no_model_download",
    "no_weight_download",
    "no_dataset_download",
    "no_example_asset_download",
    "no_real_import",
    "no_model_load",
    "no_inference",
    "no_runtime",
    "no_output_adapter",
    "no_semantic_layer",
    "no_registry_mutation",
    "no_commercial_runtime",
)

# --------------------------------------------------------------------------- #
# Negative guards (20: Invalid A..T).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_post_review_clone_checkout_install", "go_key": "no_execution_in_post_review", "depends_on": "no_execution_in_post_review"},
    {"guard_id": "invalid_b_post_review_pip_dependency_install", "go_key": "no_pip_dependency_install", "depends_on": "no_pip_dependency_install"},
    {"guard_id": "invalid_c_post_review_model_weight_dataset_example_download", "go_key": "no_download", "depends_on": "no_download"},
    {"guard_id": "invalid_d_post_review_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_e_post_review_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_f_post_review_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_g_all_deferred_faked_as_full_go", "go_key": "not_faked_full_go", "depends_on": "not_faked_full_go"},
    {"guard_id": "invalid_h_all_deferred_faked_as_install_success", "go_key": "not_faked_install_success", "depends_on": "not_faked_install_success"},
    {"guard_id": "invalid_i_zero_success_faked_as_nonzero", "go_key": "not_faked_success_count", "depends_on": "not_faked_success_count"},
    {"guard_id": "invalid_j_repository_placeholder_faked_verified", "go_key": "repo_not_faked_verified", "depends_on": "repo_not_faked_verified"},
    {"guard_id": "invalid_k_commit_hash_fabricated_pinned", "go_key": "commit_not_fabricated", "depends_on": "commit_not_fabricated"},
    {"guard_id": "invalid_l_license_review_fabricated_completed", "go_key": "license_not_fabricated", "depends_on": "license_not_fabricated"},
    {"guard_id": "invalid_m_dependency_review_fabricated_completed", "go_key": "dependency_not_fabricated", "depends_on": "dependency_not_fabricated"},
    {"guard_id": "invalid_n_mobile_sam_weight_risk_unrecorded", "go_key": "mobile_sam_weight_risk_recorded", "depends_on": "mobile_sam_weight_risk_recorded"},
    {"guard_id": "invalid_o_deferred_not_routed_to_followup", "go_key": "deferred_routed_to_followup", "depends_on": "deferred_routed_to_followup"},
    {"guard_id": "invalid_p_probe_not_find_spec_only", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_q_success_marked_weight_inference_runtime_readiness", "go_key": "success_not_readiness", "depends_on": "success_not_readiness"},
    {"guard_id": "invalid_r_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_s_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_t_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (39 phase + 6 test board = 45).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_source_install_execution_post_review_only",
    "no_new_execution_is_allowed",
    "no_git_clone_is_allowed",
    "no_source_checkout_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_example_asset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "all_deferred_partial_go_is_allowed_when_no_boundary_violation_exists",
    "all_deferred_partial_go_is_not_full_go",
    "all_deferred_partial_go_is_not_source_install_success",
    "all_deferred_partial_go_is_not_weight_readiness",
    "all_deferred_partial_go_is_not_inference_readiness",
    "all_deferred_partial_go_is_not_runtime_readiness",
    "repository_placeholder_must_not_be_treated_as_verified",
    "commit_must_not_be_fabricated",
    "license_review_must_not_be_fabricated",
    "dependency_review_must_not_be_fabricated",
    "mobile_sam_weight_excluding_checkout_risk_must_be_recorded",
    "deferred_source_assets_require_repository_verification_commit_pin_followup",
    "no_weight_download_phase_until_successful_source_execution_post_review",
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
    "source_execution_artifact_audit_record",
    "all_deferred_partial_go_audit_record",
    "repository_verification_audit_record",
    "network_boundary_audit_record",
    "source_non_execution_boundary_record",
    "source_followup_resolution_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallExecutionPostReviewProfile",
    "SourceExecutionArtifactAudit",
    "SourcePreExecutionSnapshotAudit",
    "SourceRepositoryVerificationAudit",
    "SourceCommitPinAudit",
    "SourceCheckoutCodeInstallAudit",
    "SourceNetworkBoundaryAudit",
    "SourcePostInstallProbeAudit",
    "AllDeferredPartialGoAudit",
    "SourceDeferredAssetAudit",
    "SourceNonExecutionBoundaryAudit",
    "SourceFollowupResolutionRouting",
    "NegativeSourceInstallExecutionPostReviewGuard",
    "P1ControlledSourceInstallExecutionPostReviewDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "post_review_test_mode_used": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    source_execution_post_review: bool
    no_new_execution_allowed: bool
    registry_mutation_allowed: bool
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    example_asset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    partial_go_subtype: str
    audited_asset_ids: Tuple[str, ...]
    upstream_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceExecutionArtifactAudit:
    audit_id: str
    upstream_execution_ref: str
    review_artifact_present: bool
    expected_final_decision: str
    actual_final_decision: str
    final_decision_matches: bool
    blocker_count: int
    negative_guard_passed: int
    attempted_source_asset_count: int
    successful_source_asset_count: int
    deferred_source_asset_count: int
    failed_source_asset_count: int
    all_assets_deferred: bool
    artifact_files_referenced: Tuple[str, ...]
    artifact_audit_consistent: bool


@dataclass(frozen=True)
class SourcePreExecutionSnapshotAudit:
    audit_id: str
    snapshot_present: bool
    snapshot_performed: bool
    snapshot_written_before_execution: bool
    snapshot_protected: bool
    snapshot_non_deletable: bool
    audit_passed: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationAudit:
    asset_id: str
    repository_verification_gate_executed: bool
    repository_url_remained_placeholder: bool
    commit_remained_unpinned: bool
    license_remained_unverified: bool
    network_lookup_performed: bool
    no_fabricated_repository_url: bool
    no_repository_marked_verified_without_evidence: bool
    no_commit_hash_fabricated: bool
    no_license_review_fabricated: bool
    repository_verification_failed_honestly: bool
    repository_verification_failure_caused_defer: bool
    repository_verification_failure_not_blocker_if_no_boundary_violation: bool


@dataclass(frozen=True)
class SourceCommitPinAudit:
    asset_id: str
    commit_pin_required: bool
    commit_pin_recorded: bool
    commit_pin_fabricated: bool
    commit_pin_audit_passed: bool


@dataclass(frozen=True)
class SourceCheckoutCodeInstallAudit:
    asset_id: str
    checkout_record_present: bool
    code_install_record_present: bool
    source_checkout_performed: bool
    source_install_performed: bool
    pip_install_performed: bool
    dependency_install_performed: bool
    checkout_path_controlled: bool
    install_target_controlled: bool
    controlled_env_not_polluted: bool
    package_install_only_env_preserved: bool
    registry_preserved: bool
    test_board_preserved: bool
    audit_passed: bool


@dataclass(frozen=True)
class SourceNetworkBoundaryAudit:
    audit_id: str
    network_log_present: bool
    network_access_performed: bool
    scoped_git_clone_performed: bool
    unscoped_network_access_performed: bool
    external_url_download_performed: bool
    model_weight_download_performed: bool
    checkpoint_download_performed: bool
    dataset_download_performed: bool
    example_asset_download_performed: bool
    no_network_boundary_violation: bool
    mobile_sam_canonical_repo_may_contain_committed_checkpoint_weight: bool
    mobile_sam_full_clone_may_equal_weight_download: bool
    mobile_sam_weight_excluding_checkout_required_before_retry: bool


@dataclass(frozen=True)
class SourcePostInstallProbeAudit:
    asset_id: str
    probe_record_present: bool
    probe_status: str
    probe_uses_find_spec_only: bool
    real_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool
    output_adapter_used: bool
    audit_passed: bool


@dataclass(frozen=True)
class AllDeferredPartialGoAudit:
    audit_id: str
    partial_go_subtype: str
    all_assets_deferred: bool
    successful_source_asset_count: int
    deferred_source_asset_count: int
    failed_source_asset_count: int
    blocker_count: int
    no_boundary_violation: bool
    no_environment_contamination: bool
    no_fabricated_repository_url: bool
    no_forced_clone: bool
    no_forced_install: bool
    partial_go_not_full_go: bool
    all_deferred_partial_go_not_source_install_success: bool
    all_deferred_partial_go_not_weight_readiness: bool
    all_deferred_partial_go_not_inference_readiness: bool
    all_deferred_partial_go_not_runtime_readiness: bool
    semantics_note: str


@dataclass(frozen=True)
class SourceDeferredAssetAudit:
    asset_id: str
    execution_status: str
    source_family: str
    deferred_reasons: Tuple[str, ...]
    source_checkout_not_attempted: bool
    source_install_not_attempted: bool
    weight_download_not_attempted: bool
    requires_real_repository_verification_phase: bool
    requires_commit_pin_phase: bool
    requires_license_review_phase: bool
    requires_dependency_review_phase: bool
    requires_weight_excluding_checkout_plan: bool


@dataclass(frozen=True)
class SourceNonExecutionBoundaryAudit:
    boundary_id: str
    statement: str
    holds: bool


@dataclass(frozen=True)
class SourceFollowupResolutionRouting:
    routing_id: str
    recommended_next_phase: str
    handles_byte_track_repository_verification: bool
    handles_mobile_sam_repository_verification: bool
    handles_mobile_sam_weight_excluding_checkout_plan: bool
    no_clone_in_planning: bool
    no_install_in_planning: bool
    no_weight_download_in_planning: bool
    source_execution_retry_not_allowed_until_repository_verification_complete: bool
    source_execution_retry_not_allowed_until_commit_pin_complete: bool
    source_execution_retry_not_allowed_until_license_review_complete: bool
    source_execution_retry_not_allowed_until_dependency_review_complete: bool
    mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete: bool
    no_weight_download_phase_until_successful_source_execution_post_review: bool


@dataclass
class NegativeSourceInstallExecutionPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionPostReviewDecision:
    decision_ref: str
    source_install_execution_post_review_profile_count: int
    source_execution_artifact_audit_count: int
    source_pre_execution_snapshot_audit_count: int
    source_repository_verification_audit_count: int
    source_commit_pin_audit_count: int
    source_checkout_code_install_audit_count: int
    source_network_boundary_audit_count: int
    source_post_install_probe_audit_count: int
    all_deferred_partial_go_audit_count: int
    source_deferred_asset_audit_count: int
    source_non_execution_boundary_audit_count: int
    source_followup_resolution_routing_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
