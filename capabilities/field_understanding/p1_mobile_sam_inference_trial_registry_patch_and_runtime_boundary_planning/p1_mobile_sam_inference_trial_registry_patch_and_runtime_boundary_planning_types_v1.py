# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Registry Patch And Runtime Boundary Planning — types v1
(PLANNING ONLY, scope = mobile_sam_only).

Plans registry overlay patch (inference_trial_verified, candidate_output_verified) and
runtime/output adapter/semantic/fact/navigation boundaries. Does NOT write registry,
inference, runtime, or download.
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

PHASE_ID = "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-And-Runtime-Boundary-Planning-v1-001"
SCOPE = "p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning"
WEIGHT_CHAIN = "p1_mobile_sam_inference_trial_registry_patch_and_runtime_boundary_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "仅规划，scope=mobile_sam_only。基于 inference trial execution GO，规划 registry overlay 写入 "
    "inference_trial_verified / candidate_output_verified（不写 registry），并规划 runtime、output adapter、"
    "semantic/fact/navigation 边界与 commercial runtime 排除。不修改 registry、不 inference、不 runtime、"
    "不 output adapter、不语义层、不写 fact、不 navigation/action/speech、不额外下载。"
    "单次 trial 成功 ≠ broad inference_ready；registry patch planning ≠ registry mutation。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "inference_trial_verified_is_not_runtime_not_broad_inference_ready_planning_is_not_mutation"
)

PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
INFERENCE_REGISTRY_PATCH_PLANNING = True
RUNTIME_BOUNDARY_PLANNING = True
OUTPUT_ADAPTER_BOUNDARY_PLANNING = True
SEMANTIC_FACT_NAVIGATION_EXCLUSION_PLANNING = True
REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_INFERENCE_EXECUTION_REF = (
    "Phase-P1-MobileSAM-Inference-Trial-Execution-And-Post-Review-v1-001"
)
UPSTREAM_INFERENCE_EXECUTION_EXPECTED_GO = "P1_MOBILE_SAM_INFERENCE_TRIAL_EXECUTION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_REGISTRY_PATCH_EXECUTION = (
    "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-Execution-And-Post-Review-v1-001"
)
NEXT_PHASE_BLOCKED = (
    "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-And-Runtime-Boundary-Blocker-Review-v1-001"
)

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

UPSTREAM_INFERENCE_OUTPUT_DIR_REL = (
    "_tmp_eval_out/p1_mobile_sam_inference_trial_execution_and_post_review_v1_smoke_v0"
)
UPSTREAM_INFERENCE_REVIEW_FILE_REL = (
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/"
    "p1_mobile_sam_inference_trial_execution_and_post_review_review_v1.json"
)
UPSTREAM_INFERENCE_ARTIFACT_REFS: Tuple[str, ...] = (
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_pre_inference_snapshot_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_local_test_image_manifest_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_inference_sha256_registry_recheck_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_inference_model_load_record_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_single_inference_execution_record_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_inference_candidate_output_v1.json",
    f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_inference_post_review_audit_v1.json",
)

MOBILE_SAM_ASSET_ID = "mobile_sam"
REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
PLANNED_READINESS_LEVEL = "inference_trial_verified"

PLANNED_REGISTRY_PATCH: Dict[str, Any] = {
    "asset_id": MOBILE_SAM_ASSET_ID,
    "inference_trial_verified": True,
    "candidate_output_verified": True,
    "single_local_test_image_inference_verified": True,
    "inference_trial_phase_ref": UPSTREAM_INFERENCE_EXECUTION_REF,
    "inference_trial_result": "GO",
    "inference_trial_input_type": "synthetic_test_image",
    "inference_trial_input_manifest_ref": (
        f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_local_test_image_manifest_v1.json"
    ),
    "inference_trial_candidate_output_ref": (
        f"{UPSTREAM_INFERENCE_OUTPUT_DIR_REL}/mobile_sam_inference_candidate_output_v1.json"
    ),
    "inference_output_boundary": "candidate_only",
    "readiness_level": PLANNED_READINESS_LEVEL,
    "model_load_verified": True,
    "checkpoint_load_verified": True,
    "dependency_gap_resolved": True,
    "dependency_repair_dependency": "timm",
    "dependency_repair_dependency_version": "1.0.27",
    "weight_downloaded": True,
    "weight_integrity_verified": True,
    "storage_verified": True,
    "inference_ready": False,
    "runtime_ready": False,
    "output_adapter_ready": False,
    "semantic_layer_ready": False,
    "fact_write_ready": False,
    "navigation_action_speech_ready": False,
    "commercial_runtime_approved": False,
}

UPSTREAM_EXPECTED: Dict[str, Any] = {
    "final_decision": UPSTREAM_INFERENCE_EXECUTION_EXPECTED_GO,
    "blocker_count": 0,
    "negative_guard_passed": 22,
    "inference_attempted": True,
    "inference_success": True,
    "candidate_output_written": True,
    "candidate_output_only": True,
    "single_local_test_image_inference_verified": True,
}

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go_but_patch_planned", "go_key": "upstream_inference_go_verified", "depends_on": "upstream_inference_go_verified"},
    {"guard_id": "invalid_b_upstream_boundary_violation_but_patch_planned", "go_key": "upstream_boundary_clean", "depends_on": "upstream_boundary_clean"},
    {"guard_id": "invalid_c_registry_mutated_this_phase", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_d_inference_segmentation_prediction", "go_key": "no_seg_pred_inference", "depends_on": "no_seg_pred_inference"},
    {"guard_id": "invalid_e_image_input", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_f_real_import_model_load", "go_key": "no_real_import_load", "depends_on": "no_real_import_load"},
    {"guard_id": "invalid_g_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_fact_navigation_speech", "go_key": "no_fact_navigation_speech", "depends_on": "no_fact_navigation_speech"},
    {"guard_id": "invalid_i_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_j_patch_sets_downstream_ready", "go_key": "patch_not_downstream_ready", "depends_on": "patch_not_downstream_ready"},
    {"guard_id": "invalid_k_broad_inference_ready", "go_key": "no_broad_inference_ready", "depends_on": "no_broad_inference_ready"},
    {"guard_id": "invalid_l_candidate_boundary_missing", "go_key": "candidate_boundary_present", "depends_on": "candidate_boundary_present"},
    {"guard_id": "invalid_m_runtime_boundary_missing", "go_key": "runtime_boundary_present", "depends_on": "runtime_boundary_present"},
    {"guard_id": "invalid_n_output_adapter_boundary_missing", "go_key": "output_adapter_boundary_present", "depends_on": "output_adapter_boundary_present"},
    {"guard_id": "invalid_o_semantic_fact_navigation_missing", "go_key": "semantic_fact_navigation_present", "depends_on": "semantic_fact_navigation_present"},
    {"guard_id": "invalid_p_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_inference_trial_registry_patch_and_runtime_boundary_planning_only",
    "scope_is_mobile_sam_only",
    "upstream_inference_trial_must_be_go",
    "upstream_boundary_must_be_clean",
    "registry_mutation_is_not_allowed",
    "real_inference_is_not_allowed",
    "image_input_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "additional_download_is_not_allowed",
    "single_trial_success_is_not_broad_inference_readiness",
    "inference_trial_verified_may_be_planned_true",
    "candidate_output_verified_may_be_planned_true",
    "runtime_ready_must_remain_false",
    "output_adapter_ready_must_remain_false",
    "semantic_layer_ready_must_remain_false",
    "fact_write_ready_must_remain_false",
    "navigation_action_speech_ready_must_remain_false",
    "commercial_runtime_approved_must_remain_false",
    "candidate_output_must_remain_candidate_only",
    "candidate_output_must_not_enter_fact_layer",
    "candidate_output_must_not_enter_runtime",
    "candidate_output_must_not_enter_output_adapter",
    "candidate_output_must_not_enter_semantic_layer",
    "candidate_output_must_not_trigger_navigation_action_speech",
    "runtime_requires_separate_request_approval_execution",
    "output_adapter_requires_separate_review",
    "semantic_fact_promotion_requires_separate_governance",
    "commercial_runtime_is_not_approved",
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
    "mobile_sam_inference_success_audit_record",
    "mobile_sam_inference_registry_patch_plan_record",
    "mobile_sam_candidate_output_registry_plan_record",
    "mobile_sam_runtime_boundary_plan_record",
    "mobile_sam_output_adapter_boundary_plan_record",
    "mobile_sam_semantic_fact_navigation_exclusion_record",
    "mobile_sam_commercial_runtime_exclusion_record",
    "mobile_sam_followup_inference_registry_patch_execution_route_record",
)

FINAL_DECISION_GO = (
    "P1_MOBILE_SAM_INFERENCE_TRIAL_REGISTRY_PATCH_AND_RUNTIME_BOUNDARY_PLANNING_GO"
)
FINAL_DECISION_BLOCKED = (
    "P1_MOBILE_SAM_INFERENCE_TRIAL_REGISTRY_PATCH_AND_RUNTIME_BOUNDARY_PLANNING_BLOCKED"
)

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "inference_trial_execution_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    mobile_sam_only: bool
    inference_registry_patch_planning: bool
    runtime_boundary_planning: bool
    output_adapter_boundary_planning: bool
    semantic_fact_navigation_exclusion_planning: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    commercial_runtime_approved: bool
    upstream_inference_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMInferenceSuccessAudit:
    audit_id: str
    upstream_review_ref: str
    final_decision: str
    blocker_count: int
    negative_guard_passed: int
    inference_attempted: bool
    inference_success: bool
    candidate_output_written: bool
    candidate_output_only: bool
    single_local_test_image_inference_verified: bool
    local_test_image_manifest_valid: bool
    image_source_allowed: bool
    no_live_camera: bool
    no_personal_image: bool
    no_external_url_image: bool
    no_uncontrolled_dataset: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_fact_write: bool
    no_navigation_action_speech: bool
    no_registry_mutation: bool
    no_extra_download: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMInferenceRegistryPatchPlanningRecord:
    record_id: str
    target_overlay_ref: str
    target_asset_id: str
    planned_patch: Dict[str, Any]
    registry_file_write_allowed: bool
    registry_mutated_this_phase: bool
    planned_broad_inference_ready: bool


@dataclass(frozen=True)
class MobileSAMCandidateOutputRegistryPlanningRecord:
    record_id: str
    candidate_output_only: bool
    candidate_output_not_fact: bool
    candidate_output_not_runtime_output: bool
    candidate_output_not_output_adapter_output: bool
    candidate_output_not_semantic_output: bool
    candidate_output_not_navigation_action_speech: bool
    candidate_output_eval_artifact_only: bool
    candidate_output_requires_review_before_any_runtime_use: bool


@dataclass(frozen=True)
class MobileSAMRuntimeBoundaryPlanningRecord:
    record_id: str
    runtime_execution_allowed_now: bool
    runtime_activation_allowed_now: bool
    runtime_ready_must_remain_false: bool
    runtime_requires_separate_request: bool
    runtime_requires_separate_owner_approval: bool
    runtime_requires_separate_execution_phase: bool
    runtime_requires_output_adapter_boundary: bool
    runtime_requires_semantic_fact_boundary: bool
    runtime_requires_navigation_action_speech_boundary: bool


@dataclass(frozen=True)
class MobileSAMOutputAdapterBoundaryPlanningRecord:
    record_id: str
    output_adapter_allowed_now: bool
    output_adapter_ready_must_remain_false: bool
    output_adapter_requires_separate_review: bool
    output_adapter_requires_candidate_to_output_mapping: bool
    output_adapter_requires_failure_mode_review: bool
    output_adapter_requires_user_visible_output_policy: bool
    output_adapter_requires_speech_gate_if_speech: bool


@dataclass(frozen=True)
class MobileSAMSemanticFactNavigationExclusionRecord:
    record_id: str
    semantic_layer_allowed_now: bool
    semantic_layer_ready_must_remain_false: bool
    fact_write_allowed_now: bool
    fact_write_ready_must_remain_false: bool
    navigation_action_speech_allowed_now: bool
    navigation_action_speech_ready_must_remain_false: bool
    candidate_result_must_not_enter_fact_layer: bool
    candidate_result_must_not_enter_navigation_runtime: bool
    candidate_result_must_not_trigger_speech: bool


@dataclass(frozen=True)
class MobileSAMCommercialRuntimeExclusionRecord:
    record_id: str
    commercial_runtime_approved: bool
    commercial_runtime_requires_separate_governance: bool
    commercial_runtime_requires_stability_benchmark: bool
    commercial_runtime_requires_runtime_safety_review: bool
    commercial_runtime_requires_output_policy_review: bool


@dataclass(frozen=True)
class MobileSAMFollowupInferenceRegistryPatchExecutionRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_registry_write: bool
    next_phase_still_no_runtime: bool


@dataclass
class NegativeMobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMInferenceRegistryPatchRuntimeBoundaryPlanningDecision:
    decision_ref: str
    mobile_sam_inference_registry_patch_runtime_boundary_planning_profile_count: int
    mobile_sam_inference_success_audit_count: int
    mobile_sam_inference_registry_patch_plan_count: int
    mobile_sam_candidate_output_registry_plan_count: int
    mobile_sam_runtime_boundary_plan_count: int
    mobile_sam_output_adapter_boundary_plan_count: int
    mobile_sam_semantic_fact_navigation_exclusion_count: int
    mobile_sam_commercial_runtime_exclusion_count: int
    mobile_sam_followup_inference_registry_patch_execution_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    registry_patch_planned: bool
    planned_readiness_level: str
    can_enter_inference_trial_registry_patch_execution_next: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
