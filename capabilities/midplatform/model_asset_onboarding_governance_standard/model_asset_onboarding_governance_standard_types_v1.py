# -*- coding: utf-8 -*-
"""Model Asset Onboarding Governance Standard — types v1 (STANDARDIZATION ONLY)."""

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

PHASE_ID = "Phase-P1-Controlled-Install-Governance-Standardization-v1-001"
SCOPE = "p1_controlled_install_governance_standardization"
WEIGHT_CHAIN = "p1_controlled_install_governance_standardization_v1"
STANDARD_ID = "ModelAssetOnboardingGovernanceStandardV1"

STANDARDIZATION_PRINCIPLE_ZH = (
    "仅标准化沉淀，基于 MobileSAM P1 完整资产接入闭环，抽象为通用 Model Asset Onboarding Governance "
    "Standard V1。不执行安装、不下载权重、不 import、不 model load、不 inference、不 runtime、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_onboarding_governance_standardization_not_execution_not_runtime"
)

PLANNING_ONLY = True
STANDARDIZATION_PHASE = True
MOBILE_SAM_CASE_BASED = True
GENERAL_MODEL_ONBOARDING_STANDARD = True
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_INFERENCE_REGISTRY_PATCH_REF = (
    "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-Execution-And-Post-Review-v1-001"
)
UPSTREAM_INFERENCE_REGISTRY_PATCH_EXPECTED_GO = (
    "P1_MOBILE_SAM_INFERENCE_TRIAL_REGISTRY_PATCH_EXECUTION_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"
STANDARD_MARKDOWN_REL = (
    "capabilities/midplatform/model_asset_onboarding_governance_standard/"
    "model_asset_onboarding_governance_standard_v1.md"
)

READINESS_LEVELS: Tuple[str, ...] = (
    "registry_planned",
    "probe_observed",
    "install_required",
    "package_install_partial",
    "source_install_required",
    "code_only_ready",
    "weight_download_ready",
    "code_and_weight_ready",
    "model_load_requested",
    "model_load_verified",
    "inference_trial_requested",
    "inference_trial_verified",
    "runtime_boundary_planned",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
)

LIFECYCLE_STAGES: Tuple[str, ...] = (
    "asset_registry_planning",
    "local_availability_probe",
    "package_install_planning",
    "package_install_execution",
    "source_install_planning",
    "repository_verification",
    "commit_pin",
    "license_review",
    "dependency_review",
    "code_only_source_install",
    "registry_patch_code_only_readiness",
    "weight_download_request_approval_readiness",
    "weight_download_execution",
    "weight_registry_patch",
    "model_load_request_approval_readiness",
    "model_load_execution",
    "dependency_gap_repair",
    "dependency_install_request_approval_execution",
    "model_load_retry",
    "model_load_registry_patch",
    "inference_trial_request_approval_readiness",
    "inference_trial_execution",
    "inference_trial_registry_patch",
    "runtime_boundary_planning",
    "output_adapter_boundary_planning",
    "semantic_fact_navigation_exclusion",
    "commercial_runtime_exclusion",
)

APPROVAL_GATE_TYPES: Tuple[str, ...] = (
    "install_request_gate",
    "owner_approval_gate",
    "execution_readiness_gate",
    "execution_gate",
    "post_review_gate",
    "registry_patch_gate",
    "rollback_readiness_gate",
    "test_board_protection_gate",
)

PHASE_TEMPLATE_TYPES: Tuple[str, ...] = (
    "planning",
    "request_approval_readiness",
    "execution_post_review",
    "failure_review_repair_planning",
    "registry_patch_planning",
    "registry_patch_execution",
    "runtime_boundary_planning",
)

MOBILE_SAM_CASE_FACTS: Dict[str, Any] = {
    "asset_id": "mobile_sam",
    "install_route": "source_component_code_only_weight_excluding_checkout",
    "committed_weight_risk": True,
    "weight_sha256": "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f",
    "weight_size_bytes": 40728226,
    "readiness_progression": (
        "code_only_ready",
        "code_and_weight_ready",
        "model_load_verified",
        "inference_trial_verified",
    ),
    "model_load_failure_cause": "missing_timm_dependency",
    "timm_full_install_outcome": "timeout_transitive_heavy_deps",
    "timm_nodeps_install_outcome": "GO_version_1.0.27",
    "model_load_retry_outcome": "GO_Sam_checkpoint_load",
    "inference_trial_outcome": "GO_synthetic_128x128_candidate_only",
    "dependency_repair_method": "timm_no_deps_controlled_install",
}

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"invalid_{chr(ord('a') + i)}", "go_key": k, "depends_on": k}
    for i, k in enumerate(
        (
            "no_pip_or_source_install",
            "no_weight_or_dataset_download",
            "no_import_load_inference",
            "no_registry_write",
            "model_load_not_inference_ready",
            "inference_trial_not_runtime_ready",
            "candidate_output_boundary_strict",
            "inference_image_source_strict",
            "test_board_required",
            "failed_no_boundary_semantics_present",
            "rollback_readiness_in_standard",
            "registry_diff_post_review_in_standard",
            "source_repo_rules_present",
            "weight_governance_present",
            "dependency_repair_rules_present",
            "runtime_exclusion_present",
            "test_board_record_required_true",
            "test_board_protected_non_deletable",
            "cleanup_does_not_delete_test_board",
        )
    )
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_governance_standardization_only",
    "no_install_is_allowed",
    "no_source_checkout_is_allowed",
    "no_weight_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "no_runtime_execution_is_allowed",
    "no_output_adapter_is_allowed",
    "no_semantic_layer_is_allowed",
    "no_fact_write_is_allowed",
    "no_navigation_action_speech_is_allowed",
    "no_registry_mutation_is_allowed",
    "model_load_verified_is_not_inference_ready",
    "inference_trial_verified_is_not_broad_inference_ready",
    "inference_trial_verified_is_not_runtime_ready",
    "candidate_output_is_candidate_only",
    "candidate_output_must_not_enter_fact_runtime_output_semantic_navigation",
    "runtime_requires_separate_governance",
    "output_adapter_requires_separate_review",
    "semantic_fact_navigation_require_separate_governance",
    "weight_download_requires_separate_approval",
    "source_install_requires_repo_commit_license_dependency_review",
    "dependency_repair_requires_request_approval_execution_post_review",
    "registry_patch_requires_snapshot_diff_post_review_rollback",
    "failed_no_boundary_violation_must_be_preserved",
    "blocked_must_represent_boundary_violation_or_critical_governance_failure",
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
    "model_onboarding_lifecycle_standard_record",
    "install_strategy_standard_record",
    "source_repo_verification_standard_record",
    "weight_governance_standard_record",
    "dependency_repair_standard_record",
    "model_load_trial_standard_record",
    "inference_trial_standard_record",
    "registry_overlay_patch_standard_record",
    "failure_semantics_standard_record",
    "test_board_artifact_standard_record",
    "reusable_phase_template_route_record",
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_GOVERNANCE_STANDARDIZATION_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_GOVERNANCE_STANDARDIZATION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "mobile_sam_case_locked_and_abstracted": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
}


@dataclass(frozen=True)
class ModelAssetOnboardingGovernanceStandardProfile:
    profile_ref: str
    phase_id: str
    standard_id: str
    planning_only: bool
    standardization_phase: bool
    mobile_sam_case_based: bool
    general_model_onboarding_standard: bool
    runtime_execution_allowed: bool
    real_inference_allowed: bool
    model_load_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelOnboardingLifecycleStandardRecord:
    record_id: str
    lifecycle_stages: Tuple[str, ...]
    lifecycle_stage_count: int
    mobile_sam_case_based: bool


@dataclass(frozen=True)
class ModelInstallStrategyStandardRecord:
    record_id: str
    package_install_route_defined: bool
    source_install_route_defined: bool
    nodeps_dependency_repair_route_defined: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationStandardRecord:
    record_id: str
    canonical_repo_verification_required: bool
    commit_pin_required: bool
    license_review_required: bool
    dependency_review_required: bool
    weight_exclusion_checkout_required_when_committed_weight: bool


@dataclass(frozen=True)
class WeightGovernanceStandardRecord:
    record_id: str
    separate_request_required: bool
    sha256_required: bool
    size_required: bool
    controlled_storage_required: bool
    weight_downloaded_not_model_ready: bool


@dataclass(frozen=True)
class DependencyRepairGovernanceStandardRecord:
    record_id: str
    dependency_gap_not_model_corruption: bool
    request_approval_readiness_required: bool
    nodeps_route_when_torch_reuse_bounded: bool
    repair_success_not_model_load_success: bool


@dataclass(frozen=True)
class ModelLoadTrialGovernanceStandardRecord:
    record_id: str
    request_approval_readiness_required: bool
    sha256_recheck_required: bool
    image_input_prohibited_in_model_load: bool
    inference_prohibited_in_model_load: bool
    success_means_model_load_verified_only: bool


@dataclass(frozen=True)
class InferenceTrialGovernanceStandardRecord:
    record_id: str
    requires_model_load_verified: bool
    test_image_manifest_required: bool
    candidate_output_only: bool
    success_means_inference_trial_verified_only: bool
    broad_inference_ready_must_remain_false: bool


@dataclass(frozen=True)
class RegistryOverlayPatchGovernanceStandardRecord:
    record_id: str
    planning_before_execution: bool
    pre_patch_snapshot_required: bool
    diff_and_post_review_required: bool
    scoped_asset_only: bool
    narrow_trial_must_not_promote_broad_ready: bool


@dataclass(frozen=True)
class FailureSemanticsGovernanceStandardRecord:
    record_id: str
    go_semantics_defined: bool
    failed_no_boundary_violation_defined: bool
    blocked_semantics_defined: bool


@dataclass(frozen=True)
class TestBoardProtectedArtifactGovernanceStandardRecord:
    record_id: str
    protected_required: bool
    non_deletable_required: bool
    deletion_forbidden_required: bool
    planning_and_real_test_modes_supported: bool


@dataclass(frozen=True)
class ReusablePhaseTemplateRouteRecord:
    record_id: str
    template_types: Tuple[str, ...]
    output_path_convention: str
    test_board_convention: str


@dataclass
class NegativeModelOnboardingStandardizationGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallGovernanceStandardizationDecision:
    decision_ref: str
    model_asset_onboarding_governance_standard_profile_count: int
    model_onboarding_lifecycle_standard_record_count: int
    install_strategy_standard_record_count: int
    source_repo_verification_standard_record_count: int
    weight_governance_standard_record_count: int
    dependency_repair_standard_record_count: int
    model_load_trial_standard_record_count: int
    inference_trial_standard_record_count: int
    registry_overlay_patch_standard_record_count: int
    failure_semantics_standard_record_count: int
    test_board_artifact_standard_record_count: int
    reusable_phase_template_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    standard_markdown_written: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
