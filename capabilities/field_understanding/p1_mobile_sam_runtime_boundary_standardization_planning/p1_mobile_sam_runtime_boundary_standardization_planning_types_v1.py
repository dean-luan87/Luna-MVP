# -*- coding: utf-8 -*-
"""P1 MobileSAM Runtime Boundary Standardization Planning — types v1 (PLANNING ONLY)."""

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

PHASE_ID = "Phase-P1-MobileSAM-Runtime-Boundary-Standardization-Planning-v1-001"
SCOPE = "p1_mobile_sam_runtime_boundary_standardization_planning"
WEIGHT_CHAIN = "p1_mobile_sam_runtime_boundary_standardization_planning_v1"
MOBILE_SAM_ASSET_ID = "mobile_sam"

PLANNING_PRINCIPLE_ZH = (
    "仅 runtime boundary standardization planning，scope=mobile_sam_only。"
    "基于 inference_trial_verified 与 canonical governance_standards，规划 runtime admission、"
    "candidate output 接入、output adapter/semantic/fact/navigation/speech 隔离及实景图测试边界。"
    "不执行 runtime、不 inference、不读图、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "inference_trial_verified_is_not_runtime_ready_boundary_planning_is_not_execution"
)

PLANNING_ONLY = True
RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING = True
MOBILE_SAM_ONLY = True
GOVERNANCE_STANDARDS_REFERENCE_REQUIRED = True
INFERENCE_TRIAL_VERIFIED_REQUIRED = True
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
RUNTIME_READY_WRITE_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
OUTPUT_ADAPTER_READY_WRITE_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
SEMANTIC_LAYER_READY_WRITE_ALLOWED = False
FACT_WRITE_ALLOWED = False
FACT_WRITE_READY_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
NAVIGATION_ACTION_SPEECH_READY_WRITE_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_PACKAGING_EXECUTION_REF = (
    "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
)
UPSTREAM_PACKAGING_EXECUTION_EXPECTED_GO = (
    "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_EXECUTION_GO"
)
UPSTREAM_INFERENCE_REGISTRY_PATCH_REF = (
    "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-Execution-And-Post-Review-v1-001"
)
UPSTREAM_INFERENCE_REGISTRY_PATCH_EXPECTED_GO = (
    "P1_MOBILE_SAM_INFERENCE_TRIAL_REGISTRY_PATCH_EXECUTION_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_REAL_IMAGE_TRIAL_REQUEST = (
    "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION = (
    "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
REQUIRED_READINESS_LEVEL = "inference_trial_verified"

GOVERNANCE_MANIFEST_REL = (
    "capabilities/midplatform/governance_standards/governance_standards_manifest_v1.json"
)
GOVERNANCE_INDEX_REL = (
    "capabilities/midplatform/governance_standards/index/governance_standards_index_v1.md"
)
GOVERNANCE_REFERENCE_POLICY_REL = (
    "capabilities/midplatform/governance_standards/index/governance_standards_reference_policy_v1.md"
)
GOVERNANCE_LEGACY_INVENTORY_REL = (
    "capabilities/midplatform/governance_standards/legacy_rules/"
    "legacy_reusable_governance_rules_inventory_v1.json"
)
MODEL_ONBOARDING_STANDARD_REL = (
    "capabilities/midplatform/governance_standards/model_onboarding/"
    "model_asset_onboarding_governance_standard_v1.md"
)

STANDARD_ROOT_REL = (
    "capabilities/midplatform/governance_standards/runtime_boundary/"
    "mobile_sam_runtime_boundary_standardization"
)
STANDARD_PLAN_MD_REL = f"{STANDARD_ROOT_REL}/mobile_sam_runtime_boundary_standardization_plan_v1.md"
ADMISSION_CRITERIA_JSON_REL = f"{STANDARD_ROOT_REL}/mobile_sam_runtime_admission_criteria_v1.json"
CANDIDATE_POLICY_MD_REL = f"{STANDARD_ROOT_REL}/mobile_sam_candidate_output_admission_policy_v1.md"
OUTPUT_ADAPTER_EXCLUSION_MD_REL = f"{STANDARD_ROOT_REL}/mobile_sam_output_adapter_exclusion_policy_v1.md"
SEMANTIC_EXCLUSION_MD_REL = (
    f"{STANDARD_ROOT_REL}/mobile_sam_semantic_fact_navigation_exclusion_policy_v1.md"
)

BROAD_READINESS_MUST_BE_FALSE: Tuple[str, ...] = (
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "fact_write_ready",
    "navigation_action_speech_ready",
    "commercial_runtime_approved",
)

REQUIRED_REGISTRY_TRUE_FLAGS: Tuple[str, ...] = (
    "model_load_verified",
    "checkpoint_load_verified",
    "inference_trial_verified",
    "candidate_output_verified",
    "single_local_test_image_inference_verified",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"invalid_{chr(ord('a') + i)}", "go_key": k, "depends_on": k}
    for i, k in enumerate(
        (
            "governance_standards_referenced",
            "registry_inference_trial_verified",
            "no_runtime_ready_granted",
            "no_output_adapter_ready_granted",
            "no_semantic_fact_navigation_ready_granted",
            "no_inference_or_image_input",
            "no_runtime_output_semantic_execution",
            "no_registry_mutation",
            "runtime_admission_criteria_defined",
            "runtime_rejection_criteria_defined",
            "candidate_output_admission_policy_defined",
            "output_adapter_boundary_defined",
            "semantic_fact_navigation_exclusion_defined",
            "real_image_test_boundary_defined",
            "no_live_camera_or_external_url_next",
            "candidate_not_direct_fact_runtime",
            "test_board_record_required_true",
            "test_board_protected_non_deletable",
            "cleanup_does_not_delete_test_board",
        )
    )
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_runtime_boundary_standardization_planning_only",
    "governance_standards_canonical_library_must_be_referenced",
    "scope_is_mobile_sam_only",
    "mobile_sam_must_be_inference_trial_verified",
    "runtime_execution_is_not_allowed",
    "runtime_ready_must_not_be_written_true",
    "output_adapter_is_not_allowed",
    "output_adapter_ready_must_not_be_written_true",
    "semantic_layer_is_not_allowed",
    "semantic_layer_ready_must_not_be_written_true",
    "fact_write_is_not_allowed",
    "fact_write_ready_must_not_be_written_true",
    "navigation_action_speech_is_not_allowed",
    "navigation_action_speech_ready_must_not_be_written_true",
    "real_inference_is_not_allowed",
    "image_input_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "candidate_output_may_only_enter_runtime_admission_review",
    "candidate_output_must_remain_candidate",
    "candidate_output_must_not_enter_fact_layer",
    "candidate_output_must_not_enter_runtime_directly",
    "candidate_output_must_not_enter_output_adapter_directly",
    "candidate_output_must_not_enter_semantic_layer_directly",
    "candidate_output_must_not_trigger_navigation_action_speech",
    "runtime_requires_separate_request_approval_execution_post_review",
    "output_adapter_requires_separate_review",
    "semantic_fact_navigation_speech_require_separate_governance",
    "real_local_image_trial_requires_manifest",
    "live_camera_is_forbidden_for_next_image_trial",
    "external_url_image_is_forbidden_for_next_image_trial",
    "personal_sensitive_image_is_forbidden_for_next_image_trial",
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
    "mobile_sam_runtime_boundary_scope_record",
    "governance_standards_reference_audit_record",
    "mobile_sam_inference_trial_verified_audit_record",
    "mobile_sam_runtime_admission_criteria_record",
    "mobile_sam_candidate_output_admission_policy_record",
    "mobile_sam_runtime_rejection_criteria_record",
    "mobile_sam_output_adapter_boundary_record",
    "mobile_sam_semantic_fact_navigation_speech_exclusion_record",
    "mobile_sam_real_image_test_boundary_record",
    "mobile_sam_followup_real_image_trial_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "governance_standards_canonical_library_referenced": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMRuntimeBoundaryStandardizationPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    runtime_boundary_standardization_planning: bool
    mobile_sam_only: bool
    governance_standards_reference_required: bool
    inference_trial_verified_required: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    target_chain_ref: str
    upstream_packaging_execution_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMRuntimeBoundaryScopeRecord:
    record_id: str
    asset_id: str
    scope: str
    planning_only: bool
    standard_root_rel: str


@dataclass(frozen=True)
class GovernanceStandardsReferenceAuditRecord:
    record_id: str
    manifest_ref_ok: bool
    index_ref_ok: bool
    reference_policy_ref_ok: bool
    legacy_inventory_ref_ok: bool
    reuse_before_create_policy_present: bool
    runtime_admission_gate_present: bool


@dataclass(frozen=True)
class MobileSAMInferenceTrialVerifiedAuditRecord:
    record_id: str
    registry_overlay_rel: str
    readiness_level: str
    inference_trial_verified: bool
    broad_readiness_all_false: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMRuntimeAdmissionCriteriaRecord:
    record_id: str
    runtime_candidate_admission_possible: bool
    runtime_ready_granted_now: bool
    runtime_requires_separate_request: bool
    runtime_requires_owner_approval: bool
    runtime_requires_real_image_trial_suite: bool


@dataclass(frozen=True)
class MobileSAMCandidateOutputAdmissionPolicyRecord:
    record_id: str
    candidate_output_may_enter_runtime_admission_review: bool
    candidate_output_must_remain_candidate: bool
    candidate_output_requires_schema: bool
    candidate_output_requires_no_fact_write: bool


@dataclass(frozen=True)
class MobileSAMRuntimeRejectionCriteriaRecord:
    record_id: str
    rejection_criteria_count: int
    rejects_registry_below_inference_trial_verified: bool
    rejects_direct_user_visible_output: bool


@dataclass(frozen=True)
class MobileSAMOutputAdapterBoundaryRecord:
    record_id: str
    output_adapter_ready_granted_now: bool
    output_adapter_requires_separate_request: bool
    output_adapter_must_not_read_candidate_without_admission: bool


@dataclass(frozen=True)
class MobileSAMSemanticFactNavigationSpeechExclusionRecord:
    record_id: str
    semantic_layer_ready_granted_now: bool
    fact_write_ready_granted_now: bool
    navigation_action_speech_ready_granted_now: bool
    candidate_mask_must_not_become_fact: bool


@dataclass(frozen=True)
class MobileSAMRealImageTestBoundaryRecord:
    record_id: str
    real_local_image_trial_allowed_next: bool
    live_camera_forbidden: bool
    external_url_image_forbidden: bool
    personal_sensitive_image_forbidden: bool
    output_candidate_only: bool


@dataclass(frozen=True)
class MobileSAMFollowupRealImageTrialRouteRecord:
    record_id: str
    recommended_next_phase: str
    next_phase_allows_inference_execution: bool
    next_phase_still_no_runtime: bool


@dataclass
class NegativeMobileSAMRuntimeBoundaryStandardizationPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMRuntimeBoundaryStandardizationPlanningDecision:
    decision_ref: str
    mobile_sam_runtime_boundary_standardization_planning_profile_count: int
    mobile_sam_runtime_boundary_scope_record_count: int
    governance_standards_reference_audit_record_count: int
    mobile_sam_inference_trial_verified_audit_record_count: int
    mobile_sam_runtime_admission_criteria_record_count: int
    mobile_sam_candidate_output_admission_policy_record_count: int
    mobile_sam_runtime_rejection_criteria_record_count: int
    mobile_sam_output_adapter_boundary_record_count: int
    mobile_sam_semantic_fact_navigation_speech_exclusion_record_count: int
    mobile_sam_real_image_test_boundary_record_count: int
    mobile_sam_followup_real_image_trial_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    can_enter_real_local_image_trial_request_approval_next: bool
    blocker_count: int
    final_decision: str


def build_runtime_admission_criteria() -> Dict[str, Any]:
    return {
        "criteria_id": "MobileSAMRuntimeAdmissionCriteriaV1",
        "asset_id": MOBILE_SAM_ASSET_ID,
        "phase_id": PHASE_ID,
        "runtime_candidate_admission_possible": True,
        "runtime_ready_granted_now": False,
        "runtime_requires_separate_request": True,
        "runtime_requires_owner_approval": True,
        "runtime_requires_execution_phase": True,
        "runtime_requires_post_review": True,
        "runtime_requires_failure_mode_review": True,
        "runtime_requires_output_adapter_boundary": True,
        "runtime_requires_semantic_fact_navigation_boundary": True,
        "runtime_requires_candidate_output_contract": True,
        "runtime_requires_latency_memory_budget": True,
        "runtime_requires_multiple_image_cases_before_runtime": True,
        "runtime_requires_real_image_trial_suite": True,
        "minimum_prerequisites": {
            "inference_trial_verified": True,
            "model_load_verified": True,
            "candidate_output_verified": True,
            "governance_standards_reference_ok": True,
            "real_image_trial_boundary_defined": True,
            "candidate_output_schema_defined": True,
            "no_direct_fact_runtime_output_semantic_navigation": True,
        },
    }


def build_runtime_rejection_criteria() -> Tuple[str, ...]:
    return (
        "registry_readiness_below_inference_trial_verified",
        "inference_ready_or_runtime_ready_miswritten_true",
        "candidate_output_schema_missing",
        "output_adapter_boundary_missing",
        "semantic_fact_navigation_exclusion_missing",
        "no_rollback_plan",
        "no_memory_latency_budget",
        "no_owner_approval",
        "no_post_review",
        "output_intended_for_user_visible_channel",
        "test_image_contains_personal_data",
        "live_camera_without_runtime_approval",
        "candidate_output_intended_to_trigger_navigation_action_speech",
        "registry_drift_or_unreviewed_standard_drift",
    )


def build_real_image_test_boundary() -> Dict[str, Any]:
    return {
        "boundary_id": "MobileSAMRealImageTestBoundaryV1",
        "asset_id": MOBILE_SAM_ASSET_ID,
        "real_local_image_trial_allowed_next": True,
        "uploaded_image_can_be_scoped_test_asset": True,
        "real_image_test_requires_manifest": True,
        "real_image_test_requires_user_supplied_or_local_asset": True,
        "external_url_image_forbidden": True,
        "live_camera_forbidden": True,
        "personal_sensitive_image_forbidden": True,
        "output_candidate_only": True,
        "no_runtime": True,
        "no_output_adapter": True,
        "no_semantic_layer": True,
        "no_fact_write": True,
        "no_navigation_action_speech": True,
        "suggested_test_targets": (
            "road_sign",
            "building",
            "advertisement_screen",
            "vehicle",
            "crosswalk_road_region",
        ),
        "disclaimer": (
            "Object labels are prompt/test descriptions only. "
            "MobileSAM output is segmentation candidate, not semantic fact. "
            "Any object category judgment needs separate semantic/OCR/vision evidence."
        ),
    }


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
