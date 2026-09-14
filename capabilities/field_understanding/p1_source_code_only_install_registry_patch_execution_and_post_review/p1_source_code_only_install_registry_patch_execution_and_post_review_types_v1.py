# -*- coding: utf-8 -*-
"""P1 Source Code-Only Install Registry Patch Execution And Post-Review — types v1
(REAL REGISTRY WRITE + INLINE POST-REVIEW).

Executes the planned registry patch for byte_track and mobile_sam and runs the
registry-diff post-review in the same phase. This is the FIRST phase allowed to
actually mutate the registry — but ONLY code-only source-install metadata
(install_method, source repository / commit / branch / license, import_root,
code_only_install_verified, find_spec_verified, readiness_level, weight_not_downloaded,
and the explicit-false readiness fields). It must NEVER set weight / model / inference
/ runtime / output_adapter / semantic readiness true; it must NOT download any model /
weight / checkpoint / dataset / example asset; it must NOT install / pip / resolve
dependencies; and it must NOT do real import, model load, inference, runtime, output
adapter, or semantic promotion. The registry write is implemented as a scoped,
reversible OVERLAY artifact layered over the static REGISTRY_ASSETS table (pre-patch
snapshot + diff + rollback readiness). Protected, non-deletable test board records are
written in `real_test` mode.
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

PHASE_ID = "Phase-P1-Source-Code-Only-Install-Registry-Patch-Execution-And-Post-Review-v1-001"
SCOPE = "p1_source_code_only_install_registry_patch_execution_and_post_review"
PATCH_CHAIN = "p1_source_code_only_install_registry_patch_execution_and_post_review_v1"

PATCH_PRINCIPLE_ZH = (
    "执行 byte_track 与 mobile_sam 的 registry patch 并在同阶段做 registry diff post-review。这是第一次允许真正写 registry，"
    "但只写 code-only source install 元数据：install_method、source repository/commit/branch/license、import_root、"
    "code_only_install_verified、find_spec_verified、readiness_level=code_only_ready、weight not downloaded，以及显式 false 的 "
    "model_ready/inference_ready/runtime_ready/output_adapter_ready/semantic_layer_ready。绝不把任何 readiness 设为 true；"
    "不下载模型/权重/checkpoint/数据集/示例；不安装、不 pip、不装依赖；不真实 import、不 model load、不 inference、不进 runtime/"
    "output adapter/语义层。registry 写入用可回滚的 overlay 工件实现（pre-patch snapshot + diff + rollback readiness）。"
    "mobile_sam full_clone_allowed 必须保持 false、committed weights/mobile_sam.pt 必须保持 not downloaded。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "registry_patch_writes_code_only_source_install_metadata_only_no_readiness_true_no_weight_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REGISTRY_PATCH_EXECUTION = True
POST_REVIEW_INCLUDED = True
REGISTRY_MUTATION_ALLOWED = True
REGISTRY_FILE_WRITE_ALLOWED = True
ALLOWED_REGISTRY_PATCH_SCOPE = "code_only_source_install_metadata"

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

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PLANNING_REF = "Phase-P1-Source-Code-Only-Install-Registry-Patch-And-Readiness-Planning-v1-001"
UPSTREAM_PLANNING_EXPECTED_GO = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_AND_READINESS_PLANNING_GO"
UPSTREAM_RETRY_REF = "Phase-P1-Controlled-Source-Install-Execution-Retry-And-Post-Review-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_WEIGHT_DOWNLOAD = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# Source registry table that is being patched (read for "before"; overlay holds "after").
SOURCE_REGISTRY_MODULE = "capabilities.midplatform.model_version_dependency_registry_planning.model_version_dependency_registry_planning_types_v1"
SOURCE_REGISTRY_CONST = "REGISTRY_ASSETS"
# Canonical, reversible overlay artifact written by the patch (relative to repo root).
REGISTRY_OVERLAY_REL = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"

# Upstream evidence reference for the source install (for source_install_evidence_ref).
SOURCE_INSTALL_EVIDENCE_REF = (
    "_tmp_eval_out/p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0/"
    "source_retry_code_install_execution_records_v1.json"
)

IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_MODIFY_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "sam2_observation_node", "depth_anything",
    "zoe_depth", "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

# --------------------------------------------------------------------------- #
# The patched (after) values — code-only source install metadata only.
# --------------------------------------------------------------------------- #
PATCH_AFTER_VALUES: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "install_method": "source_component_code_only",
        "source_repository_url": "https://github.com/FoundationVision/ByteTrack",
        "source_repository_commit": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "source_repository_branch": "main",
        "source_license": "MIT",
        "import_root": "yolox",
        "package_name": "none_or_source",
        "clean_pypi_candidate": False,
        "code_only_install_verified": True,
        "find_spec_verified": True,
        "find_spec_import_root": "yolox",
        "source_install_evidence_ref": SOURCE_INSTALL_EVIDENCE_REF,
        "build_compile_risk": True,
        "cxx_extension_risk": True,
        "onnx_version_conflict_risk": True,
        "model_weight_status": "not_downloaded",
        "weight_download_required_before_model_ready": True,
        "readiness_level": "code_only_ready",
        "model_ready": False,
        "inference_ready": False,
        "runtime_ready": False,
        "output_adapter_ready": False,
        "semantic_layer_ready": False,
        "commercial_runtime_approved": False,
    },
    "mobile_sam": {
        "install_method": "source_component_code_only_weight_excluding_checkout",
        "source_repository_url": "https://github.com/ChaoningZhang/MobileSAM",
        "source_repository_commit": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "source_repository_branch": "master",
        "source_license": "Apache-2.0",
        "import_root": "mobile_sam",
        "package_name": "none_or_source",
        "clean_pypi_candidate": False,
        "code_only_install_verified": True,
        "find_spec_verified": True,
        "find_spec_import_root": "mobile_sam",
        "source_install_evidence_ref": SOURCE_INSTALL_EVIDENCE_REF,
        "full_clone_allowed": False,
        "weight_excluding_checkout_required": True,
        "committed_weight_file": "weights/mobile_sam.pt",
        "committed_weight_file_size_bytes": 40728226,
        "committed_weight_file_downloaded": False,
        "model_weight_status": "not_downloaded",
        "checkpoint_weight_status": "not_downloaded",
        "weight_download_required_before_model_ready": True,
        "readiness_level": "code_only_ready",
        "model_ready": False,
        "inference_ready": False,
        "runtime_ready": False,
        "output_adapter_ready": False,
        "semantic_layer_ready": False,
        "commercial_runtime_approved": False,
    },
}

# Allowed patch field keys (scope = code_only_source_install_metadata).
ALLOWED_PATCH_FIELD_KEYS: Tuple[str, ...] = tuple(
    sorted({k for asset in PATCH_AFTER_VALUES.values() for k in asset.keys()})
)
# Readiness keys that MUST remain false / not-true after the patch.
READINESS_FALSE_KEYS: Tuple[str, ...] = (
    "model_ready", "inference_ready", "runtime_ready",
    "output_adapter_ready", "semantic_layer_ready", "commercial_runtime_approved",
)
# Source-registry asset record keys captured for the "before" snapshot.
BEFORE_FIELDS_OF_INTEREST: Tuple[str, ...] = (
    "asset_id", "canonical_name", "open_form", "primary_package_name", "import_name",
    "weight_required", "expected_weight_paths", "license_type", "license_class",
    "runtime_eligibility_level", "risk",
    "install_method", "source_repository_url", "source_repository_commit",
    "code_only_install_verified", "readiness_level", "model_ready", "inference_ready",
    "runtime_ready",
)

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_write_registry_without_snapshot", "go_key": "snapshot_present", "depends_on": "snapshot_present"},
    {"guard_id": "invalid_b_modified_non_scope_asset", "go_key": "only_scope_assets_changed", "depends_on": "only_scope_assets_changed"},
    {"guard_id": "invalid_c_wrote_fields_beyond_code_only_metadata_scope", "go_key": "fields_within_scope", "depends_on": "fields_within_scope"},
    {"guard_id": "invalid_d_set_weight_model_inference_runtime_output_semantic_readiness_true", "go_key": "no_readiness_true", "depends_on": "no_readiness_true"},
    {"guard_id": "invalid_e_mobile_sam_full_clone_allowed_true", "go_key": "mobile_sam_full_clone_false", "depends_on": "mobile_sam_full_clone_false"},
    {"guard_id": "invalid_f_mobile_sam_committed_weight_marked_downloaded", "go_key": "mobile_sam_weight_not_downloaded", "depends_on": "mobile_sam_weight_not_downloaded"},
    {"guard_id": "invalid_g_clean_pypi_candidate_true", "go_key": "clean_pypi_candidate_false", "depends_on": "clean_pypi_candidate_false"},
    {"guard_id": "invalid_h_install_pip_dependency", "go_key": "no_install", "depends_on": "no_install"},
    {"guard_id": "invalid_i_download_model_weight_checkpoint_dataset_example", "go_key": "no_download", "depends_on": "no_download"},
    {"guard_id": "invalid_j_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_k_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_l_no_diff_after_patch", "go_key": "diff_present", "depends_on": "diff_present"},
    {"guard_id": "invalid_m_no_post_review_after_patch", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_n_patch_go_treated_as_weight_download_approval", "go_key": "patch_go_not_weight_approval", "depends_on": "patch_go_not_weight_approval"},
    {"guard_id": "invalid_o_patch_go_treated_as_inference_runtime_approval", "go_key": "patch_go_not_inference_runtime_approval", "depends_on": "patch_go_not_inference_runtime_approval"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (39 phase + 6 test board = 45).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_source_code_only_install_registry_patch_execution_and_post_review",
    "registry_mutation_is_allowed_only_for_code_only_source_install_metadata",
    "only_byte_track_and_mobile_sam_may_be_modified",
    "registry_pre_patch_snapshot_is_required",
    "registry_diff_is_required",
    "registry_post_review_is_required",
    "byte_track_must_remain_code_only_ready_only",
    "mobile_sam_must_remain_code_only_ready_only",
    "mobile_sam_full_clone_must_remain_forbidden",
    "mobile_sam_committed_weight_must_remain_not_downloaded",
    "clean_pypi_candidate_must_remain_false_for_source_components",
    "weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "checkpoint_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "no_install_is_allowed_in_this_phase",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_patch_success_is_not_model_readiness",
    "registry_patch_success_is_not_weight_readiness",
    "registry_patch_success_is_not_inference_approval",
    "registry_patch_success_is_not_runtime_approval",
    "registry_patch_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "weight_download_still_requires_separate_request_and_approval",
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
    "registry_patch_execution_record",
    "registry_patch_diff_record",
    "code_only_readiness_patch_record",
    "weight_boundary_patch_record",
    "model_runtime_boundary_patch_record",
    "registry_patch_post_review_record",
    "followup_weight_download_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1SourceCodeOnlyRegistryPatchExecutionPostReviewProfile",
    "RegistryPatchPreSnapshotRecord",
    "RegistryPatchExecutionRecord",
    "RegistryPatchDiffRecord",
    "CodeOnlyReadinessPatchRecord",
    "WeightBoundaryPatchRecord",
    "ModelRuntimeBoundaryPatchRecord",
    "RegistryPatchPostReviewAudit",
    "RegistryPatchRollbackReadinessRecord",
    "RegistryPatchFollowupWeightDownloadRoute",
    "NegativeSourceCodeOnlyRegistryPatchExecutionGuard",
    "P1SourceCodeOnlyRegistryPatchExecutionDecision",
)

FINAL_DECISION_GO = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "upstream_patch_planning_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1SourceCodeOnlyRegistryPatchExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    registry_patch_execution: bool
    post_review_included: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    allowed_registry_patch_scope: str
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
    upstream_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RegistryPatchPreSnapshotRecord:
    snapshot_id: str
    registry_file_refs: Tuple[str, ...]
    registry_asset_refs: Tuple[str, ...]
    byte_track_registry_before: Dict[str, Any]
    mobile_sam_registry_before: Dict[str, Any]
    timestamp: str
    upstream_planning_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_performed: bool
    snapshot_written_before_patch: bool


@dataclass(frozen=True)
class RegistryPatchExecutionRecord:
    execution_id: str
    overlay_file_ref: str
    changed_asset_ids: Tuple[str, ...]
    patched_field_keys: Tuple[str, ...]
    all_fields_within_scope: bool
    registry_patch_applied: bool
    registry_mutation_performed: bool
    only_scope_assets_changed: bool
    install_performed: bool
    download_performed: bool
    real_import_performed: bool


@dataclass(frozen=True)
class RegistryPatchDiffRecord:
    diff_id: str
    changed_asset_count: int
    changed_assets: Tuple[str, ...]
    changed_field_paths: Tuple[str, ...]
    before_values: Dict[str, Any]
    after_values: Dict[str, Any]
    no_unscoped_asset_changed: bool
    no_weight_ready_field_set_true: bool
    no_model_ready_field_set_true: bool
    no_inference_ready_field_set_true: bool
    no_runtime_ready_field_set_true: bool
    no_output_adapter_ready_field_set_true: bool
    no_semantic_layer_ready_field_set_true: bool


@dataclass(frozen=True)
class CodeOnlyReadinessPatchRecord:
    asset_id: str
    install_method: str
    code_only_install_verified: bool
    find_spec_verified: bool
    find_spec_import_root: str
    readiness_level: str
    readiness_not_model_ready: bool
    readiness_not_inference_ready: bool
    readiness_not_runtime_ready: bool


@dataclass(frozen=True)
class WeightBoundaryPatchRecord:
    asset_id: str
    model_weight_status: str
    checkpoint_weight_status: str
    weight_download_required_before_model_ready: bool
    committed_weight_file: Optional[str]
    committed_weight_file_size_bytes: int
    committed_weight_file_downloaded: bool
    full_clone_allowed: bool
    weight_excluding_checkout_required: bool
    weight_download_requires_separate_request: bool
    weight_download_requires_owner_approval: bool


@dataclass(frozen=True)
class ModelRuntimeBoundaryPatchRecord:
    asset_id: str
    model_ready: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool
    registry_patch_success_not_model_readiness: bool
    registry_patch_success_not_inference_approval: bool
    registry_patch_success_not_runtime_approval: bool


@dataclass(frozen=True)
class RegistryPatchPostReviewAudit:
    audit_id: str
    registry_patch_applied: bool
    registry_patch_scope_valid: bool
    changed_asset_count: int
    only_byte_track_and_mobile_sam_changed: bool
    code_only_install_verified_written: bool
    readiness_level_code_only_ready_written: bool
    weight_not_downloaded_written: bool
    model_ready_false_written: bool
    inference_ready_false_written: bool
    runtime_ready_false_written: bool
    output_adapter_ready_false_written: bool
    semantic_layer_ready_false_written: bool
    commercial_runtime_false_written: bool
    source_repository_commit_written: bool
    source_license_written: bool
    import_root_written: bool
    mobile_sam_weight_excluding_checkout_required_written: bool
    mobile_sam_full_clone_allowed_false_written: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_completed: bool


@dataclass(frozen=True)
class RegistryPatchRollbackReadinessRecord:
    asset_id: str
    rollback_available: bool
    rollback_snapshot_ref: str
    rollback_not_executed_by_default: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class RegistryPatchFollowupWeightDownloadRoute:
    routing_id: str
    recommended_next_phase: str
    registry_patch_go_allows_weight_download_request_planning: bool
    registry_patch_go_does_not_allow_weight_download_execution: bool
    registry_patch_go_does_not_allow_model_load: bool
    registry_patch_go_does_not_allow_inference: bool
    registry_patch_go_does_not_allow_runtime: bool
    registry_patch_go_does_not_allow_output_adapter: bool
    registry_patch_go_does_not_allow_semantic_layer: bool


@dataclass
class NegativeSourceCodeOnlyRegistryPatchExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1SourceCodeOnlyRegistryPatchExecutionDecision:
    decision_ref: str
    source_code_only_registry_patch_execution_profile_count: int
    registry_patch_pre_snapshot_record_count: int
    registry_patch_execution_record_count: int
    registry_patch_diff_record_count: int
    code_only_readiness_patch_record_count: int
    weight_boundary_patch_record_count: int
    model_runtime_boundary_patch_record_count: int
    registry_patch_post_review_audit_count: int
    registry_patch_rollback_readiness_record_count: int
    registry_patch_followup_weight_download_route_count: int
    changed_asset_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
