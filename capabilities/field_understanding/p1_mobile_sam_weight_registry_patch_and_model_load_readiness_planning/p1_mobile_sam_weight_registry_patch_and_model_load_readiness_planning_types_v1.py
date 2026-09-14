# -*- coding: utf-8 -*-
"""P1 MobileSAM Weight Registry Patch And Model Load Readiness — planning types v1
(PLANNING ONLY, scope = mobile_sam_only).

Translates the REAL mobile_sam.pt download result into (a) a registry-patch PLAN and
(b) a model-load-trial readiness PLAN. It does NOT write the registry, does NOT model
load / real import / inference / runtime / output adapter / semantic promotion, does
NOT download any extra weight, and does NOT touch byte_track. The planned readiness
level is `code_and_weight_ready` — explicitly NOT model-loaded / model-ready /
inference-ready / runtime-ready. Registry patch planning is NOT registry mutation, and
model-load-trial readiness planning is NOT model-load approval. Protected, non-
deletable test board records are written in `planning` mode.
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

PHASE_ID = "Phase-P1-MobileSAM-Weight-Registry-Patch-And-Model-Load-Readiness-Planning-v1-001"
SCOPE = "p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning"
WEIGHT_CHAIN = "p1_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "仅规划，scope=mobile_sam_only。把真实下载结果（mobile_sam.pt 已下载、sha256 已记录、size 与 storage 已验证）转成两份规划："
    "(a) registry overlay patch 规划（不写 registry），(b) model-load trial readiness 规划（不 load model）。规划的 readiness_level "
    "= code_and_weight_ready，但显式 NOT model_loaded / model_ready / inference_ready / runtime_ready。registry patch planning ≠ "
    "registry mutation；model-load trial readiness planning ≠ model-load approval。不修改 registry、不写 registry 文件、不加载模型、"
    "不真实 import、不 inference、不 runtime、不 output adapter、不语义层、不下载额外权重、不处理 byte_track。测试板块 planning 模式，"
    "protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "code_and_weight_ready_is_not_model_loaded_not_inference_not_runtime_planning_is_not_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
WEIGHT_REGISTRY_PATCH_PLANNING_ONLY = True
MODEL_LOAD_READINESS_PLANNING_ONLY = True
REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_DOWNLOAD_EXECUTION_REF = "Phase-P1-Model-Weight-Download-Execution-And-Post-Review-v1-001"
UPSTREAM_DOWNLOAD_EXECUTION_EXPECTED_GO = "P1_MODEL_WEIGHT_DOWNLOAD_EXECUTION_AND_POST_REVIEW_GO"
UPSTREAM_REQUEST_APPROVAL_READINESS_REF = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routing.
NEXT_PHASE_REGISTRY_PATCH_EXECUTION = "Phase-P1-MobileSAM-Weight-Registry-Patch-Execution-And-Post-Review-v1-001"
NEXT_PHASE_MODEL_LOAD_TRIAL = "Phase-P1-MobileSAM-Model-Load-Trial-Request-Approval-And-Readiness-v1-001"
OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE = "Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Upstream download evidence artifacts (read-only audit inputs).
# --------------------------------------------------------------------------- #
UPSTREAM_OUTPUT_DIR_REL = "_tmp_eval_out/p1_model_weight_download_execution_and_post_review_v1_smoke_v0"
UPSTREAM_REVIEW_FILE_REL = f"{UPSTREAM_OUTPUT_DIR_REL}/p1_model_weight_download_execution_and_post_review_review_v1.json"
UPSTREAM_INTEGRITY_FILE_REL = f"{UPSTREAM_OUTPUT_DIR_REL}/weight_file_integrity_record_v1.json"
UPSTREAM_HASH_FILE_REL = f"{UPSTREAM_OUTPUT_DIR_REL}/weight_hash_record_v1.json"
UPSTREAM_STORAGE_FILE_REL = f"{UPSTREAM_OUTPUT_DIR_REL}/weight_storage_record_v1.json"
UPSTREAM_POST_REVIEW_FILE_REL = f"{UPSTREAM_OUTPUT_DIR_REL}/weight_download_post_review_audit_v1.json"

# Verified mobile_sam weight facts (from the real download).
MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_WEIGHT_FILE_NAME = "mobile_sam.pt"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
MOBILE_SAM_WEIGHT_SOURCE_URL = (
    "https://raw.githubusercontent.com/ChaoningZhang/MobileSAM/"
    "f706ad9c4eb7f219c00d9050e46328518ffb65d2/weights/mobile_sam.pt"
)
MOBILE_SAM_WEIGHT_SOURCE_COMMIT = "f706ad9c4eb7f219c00d9050e46328518ffb65d2"
MOBILE_SAM_WEIGHT_SOURCE_FILE = "weights/mobile_sam.pt"
MOBILE_SAM_WEIGHT_LICENSE_REF = "Apache-2.0 repository license"
PLANNED_READINESS_LEVEL = "code_and_weight_ready"

# Existing code-only overlay (reference; patch will layer on top in the NEXT phase).
REGISTRY_OVERLAY_REL = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"

# Expected upstream verification fields.
UPSTREAM_EXPECTED: Dict[str, Any] = {
    "final_decision": UPSTREAM_DOWNLOAD_EXECUTION_EXPECTED_GO,
    "blocker_count": 0,
    "execution_scope": "mobile_sam_only",
}

# --------------------------------------------------------------------------- #
# Planned registry patch content (PLAN ONLY; NOT written this phase).
# --------------------------------------------------------------------------- #
PLANNED_REGISTRY_PATCH: Dict[str, Any] = {
    "asset_id": MOBILE_SAM_ASSET_ID,
    "weight_downloaded": True,
    "model_weight_status": "downloaded",
    "checkpoint_weight_status": "downloaded",
    "weight_file_path": MOBILE_SAM_WEIGHT_FILE_PATH,
    "weight_file_name": MOBILE_SAM_WEIGHT_FILE_NAME,
    "weight_file_size_bytes": MOBILE_SAM_WEIGHT_SIZE_BYTES,
    "weight_sha256": MOBILE_SAM_WEIGHT_SHA256,
    "weight_source_url": MOBILE_SAM_WEIGHT_SOURCE_URL,
    "weight_source_commit": MOBILE_SAM_WEIGHT_SOURCE_COMMIT,
    "weight_source_file": MOBILE_SAM_WEIGHT_SOURCE_FILE,
    "weight_license_ref": MOBILE_SAM_WEIGHT_LICENSE_REF,
    "weight_download_evidence_ref": UPSTREAM_REVIEW_FILE_REL,
    "weight_integrity_verified": True,
    "storage_verified": True,
    "readiness_level": PLANNED_READINESS_LEVEL,
    "model_load_ready": False,
    "model_ready": False,
    "inference_ready": False,
    "runtime_ready": False,
    "output_adapter_ready": False,
    "semantic_layer_ready": False,
    "commercial_runtime_approved": False,
}

# --------------------------------------------------------------------------- #
# Negative guards (15: Invalid A..O).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_download_go_unconfirmed_but_patch_planning", "go_key": "upstream_download_go_verified", "depends_on": "upstream_download_go_verified"},
    {"guard_id": "invalid_b_sha256_missing_or_mismatch", "go_key": "sha256_verified", "depends_on": "sha256_verified"},
    {"guard_id": "invalid_c_size_missing_or_mismatch", "go_key": "size_verified", "depends_on": "size_verified"},
    {"guard_id": "invalid_d_registry_mutated_this_phase", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_e_extra_weight_model_checkpoint_dataset_example_downloaded", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_f_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_g_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_byte_track_in_scope", "go_key": "byte_track_out_of_scope", "depends_on": "byte_track_out_of_scope"},
    {"guard_id": "invalid_i_weight_downloaded_marked_model_load_ready", "go_key": "not_model_load_ready", "depends_on": "not_model_load_ready"},
    {"guard_id": "invalid_j_weight_downloaded_marked_inference_runtime_ready", "go_key": "not_inference_runtime_ready", "depends_on": "not_inference_runtime_ready"},
    {"guard_id": "invalid_k_patch_planning_treated_as_registry_mutation", "go_key": "patch_planning_not_mutation", "depends_on": "patch_planning_not_mutation"},
    {"guard_id": "invalid_l_model_load_trial_planning_treated_as_model_load_approval", "go_key": "trial_planning_not_approval", "depends_on": "trial_planning_not_approval"},
    {"guard_id": "invalid_m_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_n_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_o_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (33 phase + 6 test board = 39).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_weight_registry_patch_and_model_load_readiness_planning_only",
    "scope_is_mobile_sam_only",
    "byte_track_is_out_of_scope",
    "registry_mutation_is_not_allowed",
    "registry_file_write_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "checkpoint_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "weight_sha256_must_be_verified",
    "weight_size_must_be_verified",
    "weight_storage_path_must_be_verified",
    "weight_downloaded_is_not_model_load_approval",
    "weight_downloaded_is_not_model_readiness",
    "weight_downloaded_is_not_inference_readiness",
    "weight_downloaded_is_not_runtime_readiness",
    "registry_patch_planning_is_not_registry_mutation",
    "model_load_trial_requires_separate_request_and_approval",
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
    "mobile_sam_weight_download_audit_record",
    "mobile_sam_weight_registry_patch_plan_record",
    "mobile_sam_model_load_readiness_plan_record",
    "mobile_sam_inference_runtime_boundary_record",
    "mobile_sam_followup_model_load_trial_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMWeightRegistryPatchModelLoadReadinessPlanningProfile",
    "MobileSAMWeightDownloadAudit",
    "MobileSAMWeightRegistryPatchPlanningRecord",
    "MobileSAMWeightReadinessRecord",
    "MobileSAMModelLoadTrialReadinessPlanningRecord",
    "MobileSAMModelLoadBoundaryRecord",
    "MobileSAMInferenceRuntimeBoundaryRecord",
    "MobileSAMFollowupModelLoadTrialRoute",
    "NegativeMobileSAMWeightRegistryPatchReadinessPlanningGuard",
    "P1MobileSAMWeightRegistryPatchReadinessPlanningDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_AND_MODEL_LOAD_READINESS_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_AND_MODEL_LOAD_READINESS_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "download_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMWeightRegistryPatchModelLoadReadinessPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    mobile_sam_only: bool
    weight_registry_patch_planning_only: bool
    model_load_readiness_planning_only: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    model_load_allowed: bool
    real_import_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    additional_weight_download_allowed: bool
    byte_track_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_download_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMWeightDownloadAudit:
    audit_id: str
    upstream_review_file_ref: str
    final_decision_ok: bool
    blocker_count_ok: bool
    execution_scope_ok: bool
    mobile_sam_weight_downloaded: bool
    mobile_sam_weight_file_present: bool
    mobile_sam_weight_sha256_recorded: bool
    mobile_sam_weight_storage_verified: bool
    expected_size_bytes: int
    actual_size_bytes: int
    size_matches: bool
    sha256_value: str
    sha256_matches: bool
    storage_path: str
    byte_track_weight_downloaded: bool
    no_extra_weight_files_created: bool
    model_load_performed: bool
    real_import_performed: bool
    inference_performed: bool
    runtime_execution_performed: bool
    registry_mutation_performed: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMWeightRegistryPatchPlanningRecord:
    record_id: str
    registry_overlay_ref: str
    patch_is_plan_only: bool
    patch_is_not_registry_mutation: bool
    planned_patch_values: Dict[str, Any]


@dataclass(frozen=True)
class MobileSAMWeightReadinessRecord:
    asset_id: str
    code_ready: bool
    weight_ready: bool
    weight_integrity_verified: bool
    storage_ready: bool
    model_load_ready: bool
    model_ready: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    readiness_level: str
    code_and_weight_ready_not_model_loaded: bool
    code_and_weight_ready_not_model_ready: bool
    code_and_weight_ready_not_inference_ready: bool
    code_and_weight_ready_not_runtime_ready: bool


@dataclass(frozen=True)
class MobileSAMModelLoadTrialReadinessPlanningRecord:
    record_id: str
    next_phase_suggested: str
    model_load_trial_request_required: bool
    owner_approval_required_for_model_load: bool
    model_load_pre_snapshot_required: bool
    model_load_env_path_required: bool
    code_path_ref_required: bool
    weight_path_ref_required: bool
    sha256_recheck_required_before_model_load: bool
    memory_usage_limit_required: bool
    timeout_required: bool
    no_inference_during_model_load_trial: bool
    no_runtime_during_model_load_trial: bool
    no_output_adapter_during_model_load_trial: bool
    no_semantic_layer_during_model_load_trial: bool
    post_model_load_review_required: bool


@dataclass(frozen=True)
class MobileSAMModelLoadBoundaryRecord:
    record_id: str
    weight_download_success_not_model_load_approval: bool
    weight_registry_patch_planning_not_registry_mutation: bool
    weight_registry_patch_planning_not_model_load_approval: bool
    model_load_requires_separate_request: bool
    model_load_requires_owner_approval: bool
    model_load_success_not_inference_approval: bool
    model_load_success_not_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMInferenceRuntimeBoundaryRecord:
    record_id: str
    inference_requires_separate_trial: bool
    runtime_requires_separate_trial: bool
    output_adapter_requires_separate_review: bool
    semantic_layer_requires_separate_promotion: bool
    commercial_runtime_not_approved: bool


@dataclass(frozen=True)
class MobileSAMFollowupModelLoadTrialRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_registry_overlay_write: bool
    next_phase_writes_readiness_level: str
    next_phase_still_no_model_load: bool
    next_phase_still_no_inference: bool
    next_phase_still_no_runtime: bool
    subsequent_model_load_trial_phase: str
    optional_followup_phase: Optional[str]


@dataclass
class NegativeMobileSAMWeightRegistryPatchReadinessPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMWeightRegistryPatchReadinessPlanningDecision:
    decision_ref: str
    mobile_sam_weight_registry_patch_model_load_readiness_planning_profile_count: int
    mobile_sam_weight_download_audit_count: int
    mobile_sam_weight_registry_patch_planning_record_count: int
    mobile_sam_weight_readiness_record_count: int
    mobile_sam_model_load_trial_readiness_planning_record_count: int
    mobile_sam_model_load_boundary_record_count: int
    mobile_sam_inference_runtime_boundary_record_count: int
    mobile_sam_followup_model_load_trial_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
