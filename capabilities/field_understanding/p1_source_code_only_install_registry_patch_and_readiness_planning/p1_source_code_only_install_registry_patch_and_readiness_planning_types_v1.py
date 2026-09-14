# -*- coding: utf-8 -*-
"""P1 Source Code-Only Install Registry Patch And Readiness Planning — types v1
(PLANNING ONLY).

Turns the REAL code-only source-install GO result (byte_track + mobile_sam, both
code-only verified) into a plan for HOW the registry should be patched and HOW
readiness should be marked. This phase plans only: it does NOT mutate the registry,
does NOT write registry files, does NOT install, pip, or resolve dependencies, and
does NOT download any model / weight / checkpoint / dataset / example asset; it does
NOT do real import, model load, inference, runtime, output adapter, or semantic
promotion. Both assets reach CODE-ONLY readiness only — explicitly NOT weight /
model / inference / runtime readiness. Weight download remains a separate, future,
owner-approved, post-reviewed phase. Protected, non-deletable test board records are
written in `planning` mode.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Source-Code-Only-Install-Registry-Patch-And-Readiness-Planning-v1-001"
SCOPE = "p1_source_code_only_install_registry_patch_and_readiness_planning"
PLANNING_CHAIN = "p1_source_code_only_install_registry_patch_and_readiness_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "把 byte_track 与 mobile_sam 真实 code-only source install 成功结果，规划成“registry 应如何修 / readiness 应如何标记”。"
    "本阶段只规划：不修改 registry、不写 registry 文件、不安装、不 pip、不装依赖、不下载模型/权重/checkpoint/数据集/示例，"
    "不真实 import、不 model load、不 inference、不进 runtime/output adapter/语义层。byte_track 修正为 code-only source "
    "install verified（import_root=yolox，build/C++/onnx 风险已知）；mobile_sam 修正为 code-only source install verified + "
    "weight-excluding checkout required（import_root=mobile_sam，committed weights/mobile_sam.pt 未下载）。两者只达 code "
    "readiness，不达 weight/model/inference/runtime readiness。权重下载是后续单独的 request/approval/readiness 阶段，"
    "且必须在 registry patch post-review 之后才开。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "registry_patch_planning_only_no_mutation_no_install_no_weight_download_code_only_readiness_only"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
REGISTRY_PATCH_PLANNING_ONLY = True
CODE_ONLY_READINESS_PLANNING_ONLY = True

REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
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

WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_REQUEST = True
WEIGHT_DOWNLOAD_REQUIRES_OWNER_APPROVAL = True
NO_INFERENCE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_RETRY_REF = "Phase-P1-Controlled-Source-Install-Execution-Retry-And-Post-Review-v1-001"
UPSTREAM_RETRY_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_RETRY_CODE_ONLY_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_PATCH_EXECUTION = "Phase-P1-Source-Code-Only-Install-Registry-Patch-Execution-And-Post-Review-v1-001"
NEXT_PHASE_WEIGHT_DOWNLOAD = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# Upstream retry artifacts that must be referenced / verified.
UPSTREAM_RETRY_ARTIFACT_DIR = "_tmp_eval_out/p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0"
UPSTREAM_RETRY_REVIEW_FILE = f"{UPSTREAM_RETRY_ARTIFACT_DIR}/p1_controlled_source_install_execution_retry_and_post_review_review_v1.json"
UPSTREAM_RETRY_EVIDENCE_FILES: Tuple[str, ...] = (
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_pre_execution_snapshot_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_checkout_execution_records_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_code_install_execution_records_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_post_install_probe_records_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_network_boundary_records_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_weight_exclusion_records_v1.json",
    f"{UPSTREAM_RETRY_ARTIFACT_DIR}/source_retry_post_review_audit_v1.json",
)

# Expected upstream values that must hold for this planning phase to proceed.
UPSTREAM_EXPECTED: Dict[str, Any] = {
    "final_decision": UPSTREAM_RETRY_EXPECTED_GO,
    "blocker_count": 0,
    "attempted_source_asset_count": 2,
    "successful_source_asset_count": 2,
    "failed_or_deferred_source_asset_count": 0,
}

IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")

# --------------------------------------------------------------------------- #
# Registry patch planning content (planned values only — NOT applied).
# --------------------------------------------------------------------------- #
PATCH_PLANNING: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "asset_id": "byte_track",
        "previous_status": "DEFERRED/source_component_or_unresolved_package",
        "new_planned_install_method": "source_component_code_only",
        "repository_url": "https://github.com/FoundationVision/ByteTrack",
        "repository_commit": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "license": "MIT",
        "import_root": "yolox",
        "package_name": "none_or_source",
        "clean_pypi_candidate": False,
        "code_only_install_verified": True,
        "find_spec_verified": "yolox",
        "full_clone_allowed": True,
        "weight_excluding_checkout_required": False,
        "committed_weight_file": None,
        "committed_weight_file_size_bytes": 0,
        "build_compile_risk": True,
        "cxx_extension_risk": True,
        "onnx_version_conflict_risk": True,
        "weight_required_for_future_inference": "unknown_or_detector_dependent",
        "model_weight_status": "not_downloaded",
        "checkpoint_weight_status": "not_downloaded",
        "inference_ready": False,
        "runtime_ready": False,
        "future_weight_need": "detector_or_tracker_weight_to_be_determined",
        "weight_download_target_not_selected": True,
    },
    "mobile_sam": {
        "asset_id": "mobile_sam",
        "previous_status": "DEFERRED/git_source",
        "new_planned_install_method": "source_component_code_only_weight_excluding_checkout",
        "repository_url": "https://github.com/ChaoningZhang/MobileSAM",
        "repository_commit": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "license": "Apache-2.0",
        "import_root": "mobile_sam",
        "package_name": "none_or_source",
        "clean_pypi_candidate": False,
        "code_only_install_verified": True,
        "find_spec_verified": "mobile_sam",
        "full_clone_allowed": False,
        "weight_excluding_checkout_required": True,
        "committed_weight_file": "weights/mobile_sam.pt",
        "committed_weight_file_size_bytes": 40728226,
        "build_compile_risk": False,
        "cxx_extension_risk": False,
        "onnx_version_conflict_risk": False,
        "weight_required_for_future_inference": "mobile_sam_checkpoint",
        "model_weight_status": "not_downloaded",
        "checkpoint_weight_status": "not_downloaded",
        "inference_ready": False,
        "runtime_ready": False,
        "future_weight_need": "mobile_sam_checkpoint",
        "committed_checkpoint_known": "weights/mobile_sam.pt",
        "committed_checkpoint_not_downloaded": True,
        "future_download_must_be_explicit_weight_download_phase": True,
    },
}

# --------------------------------------------------------------------------- #
# Negative guards (17: Invalid A..Q).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_phase_mutates_registry", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_b_phase_executes_install_pip_dependency", "go_key": "no_install", "depends_on": "no_install"},
    {"guard_id": "invalid_c_phase_downloads_model_weight_checkpoint_dataset_example", "go_key": "no_download", "depends_on": "no_download"},
    {"guard_id": "invalid_d_phase_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_e_phase_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_f_byte_track_code_only_success_not_audited", "go_key": "byte_track_audited", "depends_on": "byte_track_audited"},
    {"guard_id": "invalid_g_mobile_sam_code_only_success_not_audited", "go_key": "mobile_sam_audited", "depends_on": "mobile_sam_audited"},
    {"guard_id": "invalid_h_mobile_sam_weight_excluding_checkout_not_recorded", "go_key": "mobile_sam_weight_excluding_recorded", "depends_on": "mobile_sam_weight_excluding_recorded"},
    {"guard_id": "invalid_i_code_only_success_marked_weight_readiness", "go_key": "success_not_weight_readiness", "depends_on": "success_not_weight_readiness"},
    {"guard_id": "invalid_j_code_only_success_marked_model_readiness", "go_key": "success_not_model_readiness", "depends_on": "success_not_model_readiness"},
    {"guard_id": "invalid_k_code_only_success_marked_inference_runtime_readiness", "go_key": "success_not_inference_runtime_readiness", "depends_on": "success_not_inference_runtime_readiness"},
    {"guard_id": "invalid_l_registry_patch_planning_treated_as_mutation", "go_key": "patch_planning_not_mutation", "depends_on": "patch_planning_not_mutation"},
    {"guard_id": "invalid_m_registry_patch_planning_loses_no_weight_no_inference_no_runtime_boundary", "go_key": "patch_planning_preserves_boundary", "depends_on": "patch_planning_preserves_boundary"},
    {"guard_id": "invalid_n_weight_download_allowed_by_default", "go_key": "weight_download_not_default", "depends_on": "weight_download_not_default"},
    {"guard_id": "invalid_o_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (35 phase + 6 test board = 41).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_source_code_only_install_registry_patch_and_readiness_planning_only",
    "no_registry_mutation_is_allowed",
    "no_registry_file_write_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_checkpoint_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_example_asset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "byte_track_code_only_source_install_success_must_be_audited",
    "mobile_sam_code_only_source_install_success_must_be_audited",
    "mobile_sam_weight_excluding_checkout_must_be_preserved",
    "code_only_install_success_is_not_model_readiness",
    "code_only_install_success_is_not_weight_readiness",
    "code_only_install_success_is_not_inference_readiness",
    "code_only_install_success_is_not_runtime_readiness",
    "weight_download_requires_separate_request_and_approval",
    "registry_patch_requires_separate_execution_phase",
    "registry_patch_is_required_before_inference_or_runtime",
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
    "code_only_install_result_audit_record",
    "registry_patch_planning_record",
    "code_only_readiness_record",
    "weight_readiness_exclusion_record",
    "model_runtime_boundary_record",
    "followup_weight_download_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1SourceCodeOnlyInstallRegistryPatchReadinessPlanningProfile",
    "CodeOnlySourceInstallResultAudit",
    "SourceRegistryPatchPlanningRecord",
    "SourceCodeOnlyReadinessRecord",
    "SourceWeightReadinessExclusionRecord",
    "SourceModelRuntimeBoundaryRecord",
    "RegistryPatchRequirementRecord",
    "WeightDownloadPrerequisitePlanningRecord",
    "FollowupWeightDownloadRouteRecord",
    "NegativeSourceCodeOnlyRegistryPatchReadinessPlanningGuard",
    "P1SourceCodeOnlyRegistryPatchReadinessPlanningDecision",
)

FINAL_DECISION_GO = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_AND_READINESS_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_AND_READINESS_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "upstream_code_only_install_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1SourceCodeOnlyInstallRegistryPatchReadinessPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    registry_patch_planning_only: bool
    code_only_readiness_planning_only: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    checkpoint_download_allowed: bool
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
    in_scope_asset_ids: Tuple[str, ...]
    upstream_retry_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class CodeOnlySourceInstallResultAudit:
    asset_id: str
    upstream_review_ref: str
    code_only_install_success: bool
    find_spec_verified_symbol: str
    find_spec_result: bool
    full_clone_used: bool
    weight_excluding_checkout_used: bool
    weight_files_materialized: Tuple[str, ...]
    global_env_contamination: bool
    weight_download_performed: bool
    real_import_performed: bool
    model_load_performed: bool
    inference_performed: bool
    runtime_execution_performed: bool
    audit_passed: bool


@dataclass(frozen=True)
class SourceRegistryPatchPlanningRecord:
    asset_id: str
    previous_status: str
    new_planned_install_method: str
    repository_url: str
    repository_commit: str
    license: str
    import_root: str
    package_name: str
    clean_pypi_candidate: bool
    code_only_install_verified: bool
    find_spec_verified: str
    full_clone_allowed: bool
    weight_excluding_checkout_required: bool
    committed_weight_file: Optional[str]
    committed_weight_file_size_bytes: int
    build_compile_risk: bool
    cxx_extension_risk: bool
    onnx_version_conflict_risk: bool
    model_weight_status: str
    checkpoint_weight_status: str
    inference_ready: bool
    runtime_ready: bool
    is_planning_only: bool
    registry_mutation_performed: bool


@dataclass(frozen=True)
class SourceCodeOnlyReadinessRecord:
    asset_id: str
    code_only_source_available: bool
    code_only_install_verified: bool
    import_spec_probe_verified: bool
    real_import_verified: bool
    model_load_verified: bool
    inference_verified: bool
    runtime_verified: bool
    output_adapter_verified: bool
    semantic_layer_verified: bool
    model_weight_available: bool
    model_weight_verified: bool
    weight_hash_verified: bool
    weight_source_verified: bool
    readiness_level: str
    readiness_not_model_ready: bool
    readiness_not_inference_ready: bool
    readiness_not_runtime_ready: bool


@dataclass(frozen=True)
class SourceWeightReadinessExclusionRecord:
    asset_id: str
    code_only_install_success_not_weight_readiness: bool
    code_only_install_success_not_model_readiness: bool
    code_only_install_success_not_inference_readiness: bool
    code_only_install_success_not_runtime_readiness: bool
    weight_download_requires_separate_request: bool
    weight_download_requires_owner_approval: bool
    weight_download_requires_source_review: bool
    weight_download_requires_hash_plan: bool
    weight_download_requires_storage_plan: bool
    weight_download_requires_post_review: bool
    no_inference_until_weight_download_post_review: bool
    future_weight_need: str
    committed_checkpoint_known: Optional[str]
    committed_checkpoint_not_downloaded: bool
    future_download_must_be_explicit_weight_download_phase: bool


@dataclass(frozen=True)
class SourceModelRuntimeBoundaryRecord:
    asset_id: str
    code_only_ready_not_model_ready: bool
    model_ready_requires_weight_available: bool
    model_ready_requires_weight_hash_verified: bool
    model_ready_requires_model_load_review: bool
    inference_ready_requires_separate_inference_trial: bool
    runtime_ready_requires_runtime_trial: bool
    output_adapter_ready_requires_output_adapter_review: bool
    semantic_layer_ready_requires_separate_promotion: bool
    commercial_runtime_not_approved: bool


@dataclass(frozen=True)
class RegistryPatchRequirementRecord:
    requirement_id: str
    registry_patch_required_before_weight_download_request: str
    registry_patch_required_before_inference: bool
    registry_patch_required_before_runtime: bool
    registry_patch_review_required: bool
    registry_patch_execution_requires_separate_phase: bool
    registry_patch_planning_success_not_registry_mutation: bool


@dataclass(frozen=True)
class WeightDownloadPrerequisitePlanningRecord:
    plan_id: str
    weight_download_requires_separate_request: bool
    weight_download_requires_owner_approval: bool
    weight_download_requires_source_review: bool
    weight_download_requires_hash_plan: bool
    weight_download_requires_storage_plan: bool
    weight_download_requires_post_review: bool
    registry_patch_post_review_required_before_weight_download: bool
    no_inference_until_weight_download_post_review: bool
    per_asset_future_weight_need: Dict[str, str]


@dataclass(frozen=True)
class FollowupWeightDownloadRouteRecord:
    routing_id: str
    recommended_next_phase: str
    next_phase_allows_registry_patch_execution: bool
    next_phase_still_forbids_weight_download: bool
    weight_download_phase_after_patch_post_review: str
    no_weight_download_until_registry_patch_post_review: bool


@dataclass
class NegativeSourceCodeOnlyRegistryPatchReadinessPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1SourceCodeOnlyRegistryPatchReadinessPlanningDecision:
    decision_ref: str
    source_code_only_registry_patch_readiness_planning_profile_count: int
    code_only_source_install_result_audit_count: int
    source_registry_patch_planning_record_count: int
    source_code_only_readiness_record_count: int
    source_weight_readiness_exclusion_record_count: int
    source_model_runtime_boundary_record_count: int
    registry_patch_requirement_record_count: int
    weight_download_prerequisite_planning_record_count: int
    followup_weight_download_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
