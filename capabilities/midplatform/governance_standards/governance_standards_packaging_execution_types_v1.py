# -*- coding: utf-8 -*-
"""Midplatform Governance Standards Packaging Execution — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
SCOPE = "p1_midplatform_governance_standards_packaging_execution_and_post_review"
WEIGHT_CHAIN = "p1_midplatform_governance_standards_packaging_execution_v1"
LIBRARY_ROOT = "capabilities/midplatform/governance_standards"

EXECUTION_PRINCIPLE_ZH = (
    "中台治理标准库 packaging execution：创建子目录、复制标准文件至 canonical path，"
    "生成 manifest/index/path mapping/usage notes/legacy inventory，完成 post-review。"
    "不删除历史证据、不修改主程序、不 runtime、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "midplatform_governance_standards_packaging_execution_not_runtime_not_main_program"
)

REAL_EXECUTION_PHASE = True
MIDPLATFORM_GOVERNANCE_STANDARD_PACKAGING_EXECUTION = True
CENTRALIZED_REUSABLE_RULE_LIBRARY = True
MAIN_PROGRAM_SEPARATION_REQUIRED = True
CANONICAL_STANDARD_LIBRARY_CREATED = True
FILE_COPY_ALLOWED = True
FILE_CREATE_ALLOWED = True
FILE_MOVE_ALLOWED = False
FILE_DELETE_ALLOWED = False
ORIGINAL_EVIDENCE_DELETION_ALLOWED = False
MAIN_PROGRAM_MUTATION_ALLOWED = False
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
COMMERCIAL_RUNTIME_APPROVED = False

UPSTREAM_PLANNING_PHASE_REF = "Phase-P1-Midplatform-Governance-Standards-Packaging-Planning-v1-001"
UPSTREAM_PLANNING_EXPECTED_GO = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_PLANNING_GO"
UPSTREAM_PLANNING_REVIEW_REL = (
    "_tmp_eval_out/p1_midplatform_governance_standards_packaging_planning_v1_smoke_v0/"
    "p1_midplatform_governance_standards_packaging_planning_review_v1.json"
)
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "real_test"

REQUIRED_SUBDIRECTORIES: Tuple[str, ...] = (
    "index",
    "model_onboarding",
    "runtime_boundary",
    "registry_patch",
    "test_board",
    "approval_gates",
    "negative_guards",
    "rollback",
    "failure_semantics",
    "templates",
    "case_mappings",
    "usage_notes",
    "legacy_rules",
    "protocol_governance",
    "file_governance",
    "input_output_symmetry",
    "owner_approval",
    "validation_rules",
)

COPY_SPECS: Tuple[Dict[str, str], ...] = (
    {
        "standard_id": "ModelAssetOnboardingGovernanceStandardV1",
        "category": "model_onboarding",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_v1.md"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_v1.md"
        ),
    },
    {
        "standard_id": "ModelAssetOnboardingGovernanceStandardV1_types",
        "category": "model_onboarding",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_types_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_types_v1.py"
        ),
    },
    {
        "standard_id": "ModelAssetOnboardingGovernanceStandardV1_registry",
        "category": "model_onboarding",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_registry_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_registry_v1.py"
        ),
    },
    {
        "standard_id": "ModelAssetOnboardingGovernanceStandardV1_review",
        "category": "model_onboarding",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "review_model_asset_onboarding_governance_standard_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/review_model_asset_onboarding_governance_standard_v1.py"
        ),
    },
)

EVAL_ARTIFACT_COPY_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "standard_id": "ReusablePhaseTemplateMapV1",
        "category": "templates",
        "source_candidates": (
            "_tmp_eval_out/p1_controlled_install_governance_standardization_v1_smoke_v0/"
            "reusable_phase_template_map_v1.json",
        ),
        "canonical_path": f"{LIBRARY_ROOT}/templates/reusable_phase_template_map_v1.json",
    },
    {
        "standard_id": "MobileSAMCaseMappingV1",
        "category": "case_mappings",
        "source_candidates": (
            "_tmp_eval_out/p1_controlled_install_governance_standardization_v1_smoke_v0/"
            "mobile_sam_case_mapping_v1.json",
        ),
        "canonical_path": f"{LIBRARY_ROOT}/case_mappings/mobile_sam_case_mapping_v1.json",
    },
)

CANONICAL_GENERATED_RELS: Tuple[str, ...] = (
    f"{LIBRARY_ROOT}/governance_standards_manifest_v1.json",
    f"{LIBRARY_ROOT}/index/governance_standards_index_v1.md",
    f"{LIBRARY_ROOT}/index/governance_standards_path_mapping_v1.json",
    f"{LIBRARY_ROOT}/index/governance_standards_reference_policy_v1.md",
    f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_inventory_v1.json",
    f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_mapping_v1.md",
    f"{LIBRARY_ROOT}/usage_notes/governance_rule_usage_notes_index_v1.md",
    f"{LIBRARY_ROOT}/protocol_governance/protocol_governance_standard_index_v1.md",
    f"{LIBRARY_ROOT}/file_governance/file_size_module_split_governance_rule_v1.md",
    f"{LIBRARY_ROOT}/input_output_symmetry/input_output_symmetry_governance_standard_v1.md",
    f"{LIBRARY_ROOT}/owner_approval/owner_approval_governance_standard_v1.md",
    f"{LIBRARY_ROOT}/validation_rules/validate_once_reference_governance_standard_v1.md",
)

PLANNING_SOURCE_RELS: Tuple[str, ...] = (
    f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_inventory_v1.json",
    f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_mapping_v1.md",
    f"{LIBRARY_ROOT}/usage_notes/governance_rule_usage_notes_index_v1.md",
    f"{LIBRARY_ROOT}/protocol_governance/protocol_governance_standard_index_v1.md",
    f"{LIBRARY_ROOT}/file_governance/file_size_module_split_governance_rule_v1.md",
    f"{LIBRARY_ROOT}/input_output_symmetry/input_output_symmetry_governance_standard_v1.md",
    f"{LIBRARY_ROOT}/owner_approval/owner_approval_governance_standard_v1.md",
    f"{LIBRARY_ROOT}/validation_rules/validate_once_reference_governance_standard_v1.md",
)

INDEX_REQUIRED_SECTIONS: Tuple[str, ...] = (
    "Purpose",
    "Directory Layout",
    "Standard Categories",
    "Canonical Standard Paths",
    "Versioning Policy",
    "Reference Policy",
    "Reuse-before-create Policy",
    "Do Not Mix With Main Program",
    "Runtime Separation Policy",
    "Registry Patch Standard",
    "Test Board Standard",
    "Approval Gate Standard",
    "Failure Semantics Standard",
    "Negative Guard Standard",
    "Rollback Standard",
    "Input / Output Symmetry Standard",
    "Protocol Governance Standard",
    "File Governance Standard",
    "Evidence / Candidate Governance Standard",
    "Reusable Phase Templates",
    "Case Mappings",
    "Standard Patch Policy",
    "Future Migration / Packaging Execution Route",
)

LEGACY_RULE_CATEGORIES: Tuple[str, ...] = (
    "test_board_governance",
    "controlled_trial_governance",
    "owner_approval_governance",
    "negative_guard_pattern",
    "failure_semantics",
    "registry_patch_governance",
    "model_asset_onboarding_governance",
    "runtime_boundary_governance",
    "input_output_symmetry_governance",
    "protocol_governance",
    "file_size_module_split_governance",
    "validate_once_reference_governance",
    "evidence_candidate_governance",
    "runtime_output_semantic_exclusion",
    "rollback_governance",
    "artifact_protection_cleanup_governance",
    "runtime_not_main_program_rule",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"invalid_{chr(ord('a') + i)}", "go_key": k, "depends_on": k}
    for i, k in enumerate(
        (
            "pre_packaging_snapshot_before_copy",
            "no_file_move_or_delete",
            "no_main_program_mutation",
            "no_install_download_import_load_inference_runtime",
            "no_registry_write",
            "not_under_runtime_or_main_program",
            "no_weight_dataset_user_data_copied",
            "manifest_written",
            "index_written",
            "path_mapping_written",
            "legacy_inventory_written",
            "usage_notes_index_written",
            "legacy_rule_count_complete",
            "per_rule_usage_notes_present",
            "reuse_before_create_policy_present",
            "standard_patch_policy_present",
            "runtime_must_not_bypass_admission_gate",
            "candidate_output_boundary_strict",
            "post_review_present",
            "rollback_readiness_present",
            "test_board_record_required_true",
            "test_board_protected_non_deletable",
            "cleanup_does_not_delete_test_board",
        )
    )
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_governance_standards_packaging_execution_and_post_review",
    "file_copy_create_allowed_only_under_governance_standards",
    "file_move_is_not_allowed",
    "file_delete_is_not_allowed",
    "original_evidence_must_be_preserved",
    "main_program_mutation_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "no_install_is_allowed",
    "no_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "no_runtime_execution_is_allowed",
    "no_output_adapter_execution_is_allowed",
    "no_semantic_layer_promotion_is_allowed",
    "no_fact_write_is_allowed",
    "no_navigation_action_speech_is_allowed",
    "weight_files_must_not_be_copied",
    "dataset_files_must_not_be_copied",
    "user_data_must_not_be_copied",
    "manifest_is_required",
    "index_is_required",
    "path_mapping_is_required",
    "usage_notes_index_is_required",
    "legacy_rules_inventory_is_required",
    "seventeen_legacy_rule_categories_are_required",
    "per_rule_usage_note_is_required",
    "reuse_before_create_policy_is_required",
    "standard_patch_policy_is_required",
    "runtime_must_not_bypass_admission_gate",
    "output_adapter_must_not_consume_candidate_output_without_admission",
    "semantic_fact_navigation_must_not_consume_inference_trial_output_directly",
    "post_review_is_required",
    "rollback_readiness_is_required",
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
    "governance_standards_pre_packaging_snapshot_record",
    "governance_standards_directory_creation_record",
    "governance_standards_file_copy_record",
    "governance_standards_manifest_execution_record",
    "governance_standards_index_execution_record",
    "governance_standards_legacy_rules_inventory_record",
    "governance_standards_usage_notes_execution_record",
    "governance_standards_path_mapping_record",
    "governance_standards_main_program_separation_audit_record",
    "governance_standards_post_review_record",
    "governance_standards_rollback_readiness_record",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_EXECUTION_BLOCKED"

ROLLBACK_TRIGGER_CONDITIONS: Tuple[str, ...] = (
    "manifest_invalid",
    "index_invalid",
    "missing_usage_notes",
    "missing_legacy_inventory",
    "accidental_main_program_mutation",
    "accidental_registry_mutation",
    "weight_dataset_user_data_copied",
    "test_board_write_failure",
)


@dataclass(frozen=True)
class P1MidplatformGovernanceStandardsPackagingExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    midplatform_governance_standard_packaging_execution: bool
    file_copy_allowed: bool
    file_move_allowed: bool
    file_delete_allowed: bool
    main_program_mutation_allowed: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    library_root: str
    upstream_planning_phase_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class GovernanceStandardsPrePackagingSnapshotRecord:
    record_id: str
    governance_standards_root_exists_before: bool
    planned_root: str
    original_evidence_preserve_required: bool
    source_standard_count: int
    snapshot_written_before_copy: bool


@dataclass(frozen=True)
class GovernanceStandardsDirectoryCreationRecord:
    record_id: str
    directories_attempted: int
    directories_created: int
    directories_already_existing: int
    directory_creation_success: bool
    created_under_governance_standards_root: bool


@dataclass(frozen=True)
class GovernanceStandardsFileCopyRecord:
    record_id: str
    copied_file_count: int
    generated_file_count: int
    canonical_file_count: int
    copy_preserves_content: bool
    no_weight_files_copied: bool
    no_dataset_files_copied: bool
    no_user_data_copied: bool


@dataclass(frozen=True)
class GovernanceStandardsManifestExecutionRecord:
    record_id: str
    manifest_rel_path: str
    migration_mode: str
    legacy_rule_count: int
    original_evidence_preserved: bool


@dataclass(frozen=True)
class GovernanceStandardsIndexExecutionRecord:
    record_id: str
    index_rel_path: str
    sections_required: int
    sections_found: int


@dataclass(frozen=True)
class GovernanceStandardsLegacyRulesInventoryRecord:
    record_id: str
    inventory_rel_path: str
    rule_count: int
    per_rule_usage_note_present: bool


@dataclass(frozen=True)
class GovernanceStandardsUsageNotesExecutionRecord:
    record_id: str
    usage_notes_index_rel_path: str
    sections_complete: bool


@dataclass(frozen=True)
class GovernanceStandardsPathMappingRecord:
    record_id: str
    mapping_rel_path: str
    entry_count: int


@dataclass(frozen=True)
class GovernanceStandardsMainProgramSeparationAuditRecord:
    record_id: str
    governance_standards_under_midplatform: bool
    main_program_mutation_detected: bool
    registry_overlay_mutation_detected: bool
    contains_no_weight_files: bool


@dataclass
class GovernanceStandardsPostReviewAudit:
    audit_id: str
    pre_packaging_snapshot_exists: bool
    manifest_written: bool
    index_written: bool
    path_mapping_written: bool
    legacy_rule_count: int
    original_evidence_preserved: bool
    packaging_execution_success: bool
    audit_passed: bool


@dataclass(frozen=True)
class GovernanceStandardsRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_not_executed_by_default: bool
    rollback_must_preserve_original_evidence: bool
    rollback_must_preserve_test_board: bool


@dataclass
class NegativeGovernanceStandardsPackagingExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MidplatformGovernanceStandardsPackagingExecutionDecision:
    decision_ref: str
    midplatform_governance_standards_packaging_execution_profile_count: int
    governance_standards_pre_packaging_snapshot_record_count: int
    governance_standards_directory_creation_record_count: int
    governance_standards_file_copy_record_count: int
    governance_standards_manifest_execution_record_count: int
    governance_standards_index_execution_record_count: int
    governance_standards_legacy_rules_inventory_record_count: int
    governance_standards_usage_notes_execution_record_count: int
    governance_standards_path_mapping_record_count: int
    governance_standards_main_program_separation_audit_record_count: int
    governance_standards_post_review_audit_count: int
    governance_standards_rollback_readiness_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    packaging_execution_success: bool
    legacy_rule_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
