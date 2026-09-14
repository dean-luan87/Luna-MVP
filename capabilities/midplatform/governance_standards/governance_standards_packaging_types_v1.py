# -*- coding: utf-8 -*-
"""Midplatform Governance Standards Packaging — types v1 (PLANNING ONLY)."""

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

PHASE_ID = "Phase-P1-Midplatform-Governance-Standards-Packaging-Planning-v1-001"
SCOPE = "p1_midplatform_governance_standards_packaging_planning"
WEIGHT_CHAIN = "p1_midplatform_governance_standards_packaging_planning_v1"
LIBRARY_ROOT = "capabilities/midplatform/governance_standards"

PACKAGING_PRINCIPLE_ZH = (
    "Luna 中台可复用治理标准库 packaging planning：扫描并纳入历史上所有可复用治理规则，"
    "为每条规则补充 usage note，与主程序、模型实现、runtime 执行代码隔离。"
    "不移动文件、不修改主程序、不执行 runtime。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "midplatform_governance_standards_packaging_planning_not_execution_not_runtime"
)

PLANNING_ONLY = True
MIDPLATFORM_GOVERNANCE_STANDARD_PACKAGING = True
CENTRALIZED_REUSABLE_RULE_LIBRARY = True
MAIN_PROGRAM_SEPARATION_REQUIRED = True
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
FILE_MOVE_ALLOWED = False
FILE_DELETE_ALLOWED = False
MAIN_PROGRAM_MUTATION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_STANDARDIZATION_PHASE_REF = "Phase-P1-Controlled-Install-Governance-Standardization-v1-001"
UPSTREAM_STANDARDIZATION_EXPECTED_GO = "P1_CONTROLLED_INSTALL_GOVERNANCE_STANDARDIZATION_GO"
MODEL_ASSET_ONBOARDING_STANDARD_ID = "ModelAssetOnboardingGovernanceStandardV1"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"
INDEX_MD_REL = f"{LIBRARY_ROOT}/governance_standards_index_v1.md"
MANIFEST_JSON_REL = f"{LIBRARY_ROOT}/governance_standards_manifest_v1.json"
PACKAGING_PLAN_MD_REL = f"{LIBRARY_ROOT}/reusable_governance_standard_packaging_plan_v1.md"

PLANNED_SUBDIRECTORIES: Tuple[str, ...] = (
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

STANDARD_CATEGORIES: Tuple[str, ...] = (
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
    "evidence_candidate",
    "artifact_protection",
    "main_program_separation",
)

LEGACY_INVENTORY_REL = f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_inventory_v1.json"
LEGACY_MAPPING_REL = f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_mapping_v1.md"
USAGE_NOTES_INDEX_REL = f"{LIBRARY_ROOT}/usage_notes/governance_rule_usage_notes_index_v1.md"

LIBRARY_STORES: Tuple[str, ...] = (
    "reusable_governance_rules",
    "lifecycle_flows",
    "approval_gate_templates",
    "negative_guard_templates",
    "readiness_level_standards",
    "registry_patch_standards",
    "test_board_protected_artifact_standards",
    "rollback_standards",
    "failure_semantics",
    "runtime_boundary_standards",
    "output_adapter_boundary_standards",
    "semantic_fact_navigation_exclusion_standards",
    "case_mappings",
    "reusable_phase_templates",
)

LIBRARY_EXCLUDES: Tuple[str, ...] = (
    "model_code",
    "runtime_main_program",
    "output_adapter_implementation",
    "business_logic",
    "inference_scripts",
    "weight_files",
    "datasets",
    "temporary_eval_output",
    "user_data",
    "fact_layer_records",
)

PLANNED_MIGRATIONS: Tuple[Dict[str, str], ...] = (
    {
        "standard_id": MODEL_ASSET_ONBOARDING_STANDARD_ID,
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_v1.md"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_v1.md"
        ),
        "category": "model_onboarding",
    },
    {
        "standard_id": f"{MODEL_ASSET_ONBOARDING_STANDARD_ID}_types",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_types_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_types_v1.py"
        ),
        "category": "model_onboarding",
    },
    {
        "standard_id": f"{MODEL_ASSET_ONBOARDING_STANDARD_ID}_registry",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "model_asset_onboarding_governance_standard_registry_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/model_asset_onboarding_governance_standard_registry_v1.py"
        ),
        "category": "model_onboarding",
    },
    {
        "standard_id": f"{MODEL_ASSET_ONBOARDING_STANDARD_ID}_review",
        "source_path": (
            "capabilities/midplatform/model_asset_onboarding_governance_standard/"
            "review_model_asset_onboarding_governance_standard_v1.py"
        ),
        "canonical_path": (
            f"{LIBRARY_ROOT}/model_onboarding/review_model_asset_onboarding_governance_standard_v1.py"
        ),
        "category": "model_onboarding",
    },
    {
        "standard_id": "ReusablePhaseTemplateMapV1",
        "source_path": (
            "_tmp_eval_out/p1_controlled_install_governance_standardization_v1_smoke_v0/"
            "reusable_phase_template_map_v1.json"
        ),
        "canonical_path": f"{LIBRARY_ROOT}/templates/reusable_phase_template_map_v1.json",
        "category": "templates",
    },
    {
        "standard_id": "MobileSAMCaseMappingV1",
        "source_path": (
            "_tmp_eval_out/p1_controlled_install_governance_standardization_v1_smoke_v0/"
            "mobile_sam_case_mapping_v1.json"
        ),
        "canonical_path": f"{LIBRARY_ROOT}/case_mappings/mobile_sam_case_mapping_v1.json",
        "category": "case_mappings",
    },
)

REUSABLE_RULE_CLASSIFICATION: Dict[str, Tuple[str, ...]] = {
    "model_onboarding": (
        "install_lifecycle",
        "weight_governance",
        "dependency_repair",
        "model_load_trial",
        "inference_trial",
    ),
    "runtime_boundary": ("runtime_admission_gate", "runtime_execution_prohibition"),
    "registry_patch": ("snapshot_diff_post_review", "scoped_asset_mutation"),
    "test_board": ("protected_artifact", "non_deletable_policy"),
    "approval_gates": (
        "install_request_gate",
        "owner_approval_gate",
        "execution_readiness_gate",
        "execution_gate",
        "post_review_gate",
    ),
    "negative_guards": ("blocked_conditions", "failed_no_boundary_distinction"),
    "rollback": ("pre_snapshot", "rollback_readiness", "cleanup_forbidden_scope"),
    "failure_semantics": ("GO", "FAILED_NO_BOUNDARY_VIOLATION", "BLOCKED"),
    "templates": ("planning", "request_approval_readiness", "execution_post_review"),
    "case_mappings": ("mobile_sam", "future_models"),
}

REFERENCE_POLICY_RULES: Tuple[str, ...] = (
    "prefer_governance_standards_root_for_rule_reference",
    "original_phase_artifacts_preserved_as_historical_evidence",
    "packaged_files_become_canonical_standard",
    "main_program_must_not_embed_full_governance_text",
    "runtime_must_use_admission_gate_not_self_interpret_readiness",
    "registry_patch_must_reference_registry_patch_standard",
    "test_board_must_reference_test_board_standard",
)

REUSE_BEFORE_CREATE_POLICY_RULES: Tuple[str, ...] = (
    "search_governance_standards_before_creating_new_rule",
    "if_rule_exists_must_reference_standard_id_not_duplicate",
    "extension_requires_standard_patch_phase_not_inline_fork",
    "no_ad_hoc_governance_in_business_phases",
    "no_governance_rules_in_runtime_main_program",
    "model_special_case_requires_standardization_phase_for_generalization",
    "new_rule_requires_usage_note_negative_guard_owner_layer_canonical_path_test_board",
)

MAIN_PROGRAM_SEPARATION_RULES: Tuple[str, ...] = (
    "governance_standards_must_not_import_main_program_runtime",
    "main_program_runtime_must_not_depend_on_governance_test_executors",
    "runtime_reads_admission_results_only",
    "governance_rules_must_not_call_models",
    "governance_rules_must_not_download_weights",
    "governance_rules_must_not_write_fact",
    "governance_rules_must_not_trigger_navigation_action_speech",
    "governance_standards_are_policy_protocol_template_not_execution_logic",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    *tuple(
        {"guard_id": f"invalid_{chr(ord('a') + i)}", "go_key": k, "depends_on": k}
        for i, k in enumerate(
            (
                "no_file_move_or_delete",
                "no_main_program_mutation",
                "no_install_download_import_load_inference_runtime",
                "no_registry_write",
                "not_planned_under_main_program_runtime",
                "no_weights_datasets_user_data_in_library",
                "runtime_must_not_bypass_admission_gate",
                "output_adapter_must_not_read_candidate_directly",
                "semantic_fact_navigation_must_not_consume_trial_output",
                "manifest_plan_present",
                "index_plan_present",
                "reference_policy_present",
                "main_program_separation_present",
                "future_execution_route_present",
                "test_board_record_required_true",
                "test_board_protected_non_deletable",
                "cleanup_does_not_delete_test_board",
            )
        )
    ),
    *tuple(
        {"guard_id": f"invalid_r{i}", "go_key": k, "depends_on": k}
        for i, k in enumerate(
            (
                "legacy_inventory_planned",
                "per_rule_usage_note_required",
                "duplicate_rule_creation_forbidden",
                "main_program_inline_governance_forbidden",
                "runtime_bypass_governance_forbidden",
                "standard_patch_required_for_rule_extension",
                "legacy_evidence_preserved_on_packaging",
            ),
            start=1,
        )
    ),
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_governance_standards_packaging_planning_only",
    "no_file_move_is_allowed",
    "no_file_delete_is_allowed",
    "no_main_program_mutation_is_allowed",
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
    "no_registry_mutation_is_allowed",
    "governance_standards_must_be_separated_from_main_program",
    "governance_standards_must_not_contain_weights",
    "governance_standards_must_not_contain_datasets",
    "governance_standards_must_not_contain_user_data",
    "governance_standards_must_define_manifest",
    "governance_standards_must_define_index",
    "governance_standards_must_define_reference_policy",
    "governance_standards_must_define_main_program_separation_policy",
    "governance_standards_must_define_future_packaging_execution_route",
    "runtime_must_not_bypass_admission_gate",
    "output_adapter_must_not_consume_candidate_output_without_admission",
    "semantic_fact_navigation_must_not_consume_inference_trial_output_directly",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
    "legacy_reusable_rules_must_be_inventoried",
    "per_rule_usage_note_required",
    "reuse_before_create_policy_required",
    "duplicate_rule_creation_forbidden",
    "standard_patch_required_for_rule_extension",
    "main_program_inline_governance_forbidden",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "governance_standards_packaging_scope_record",
    "governance_standards_directory_plan_record",
    "governance_standards_index_plan_record",
    "governance_standards_manifest_plan_record",
    "reusable_rule_classification_record",
    "main_program_separation_record",
    "governance_standard_reference_policy_record",
    "governance_standard_future_execution_route_record",
    "legacy_reusable_governance_rules_inventory_record",
    "governance_rule_usage_notes_index_record",
    "governance_standard_reuse_policy_record",
    "duplicate_rule_prevention_record",
    "legacy_evidence_preservation_record",
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_GOVERNANCE_STANDARDS_PACKAGING_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "model_asset_onboarding_standard_referenced": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "legacy_reusable_rules_inclusion": True,
    "usage_notes_per_rule": True,
}


@dataclass(frozen=True)
class P1MidplatformGovernanceStandardsPackagingPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    midplatform_governance_standard_packaging: bool
    centralized_reusable_rule_library: bool
    main_program_separation_required: bool
    file_move_allowed: bool
    file_delete_allowed: bool
    main_program_mutation_allowed: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    library_root: str
    upstream_standardization_phase_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class GovernanceStandardsPackagingScopeRecord:
    record_id: str
    library_root: str
    library_stores: Tuple[str, ...]
    library_excludes: Tuple[str, ...]
    planning_only: bool


@dataclass(frozen=True)
class GovernanceStandardsDirectoryPlanRecord:
    record_id: str
    planned_subdirectories: Tuple[str, ...]
    subdirectory_count: int
    migration_mode: str


@dataclass(frozen=True)
class GovernanceStandardsIndexPlanRecord:
    record_id: str
    index_rel_path: str
    required_sections_defined: bool
    section_count: int


@dataclass(frozen=True)
class GovernanceStandardsManifestPlanRecord:
    record_id: str
    manifest_rel_path: str
    planned_standard_count: int
    migration_mode: str
    main_program_separation: bool


@dataclass(frozen=True)
class ReusableRuleClassificationRecord:
    record_id: str
    categories: Tuple[str, ...]
    classification: Dict[str, Tuple[str, ...]]


@dataclass(frozen=True)
class MainProgramSeparationRecord:
    record_id: str
    separation_rules: Tuple[str, ...]
    governance_standards_not_under_main_program: bool
    runtime_admission_gate_required: bool


@dataclass(frozen=True)
class GovernanceStandardReferencePolicyRecord:
    record_id: str
    reference_rules: Tuple[str, ...]
    canonical_path_policy: bool
    historical_evidence_preserved: bool


@dataclass(frozen=True)
class GovernanceStandardFutureExecutionRouteRecord:
    record_id: str
    recommended_next_phase: str
    allows_directory_creation: bool
    allows_copy_or_migrate: bool
    allows_manifest_and_index_generation: bool
    forbids_main_program_mutation: bool
    forbids_runtime_execution: bool
    forbids_deleting_original_evidence: bool


@dataclass
class NegativeGovernanceStandardsPackagingPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class LegacyReusableGovernanceRulesInventoryRecord:
    record_id: str
    inventory_rel_path: str
    rule_count: int
    all_rules_have_usage_notes: bool


@dataclass(frozen=True)
class GovernanceRuleUsageNotesIndexRecord:
    record_id: str
    index_rel_path: str
    required_sections_defined: bool


@dataclass(frozen=True)
class GovernanceStandardReusePolicyRecord:
    record_id: str
    reuse_before_create_rules: Tuple[str, ...]
    duplicate_rule_creation_forbidden: bool


@dataclass(frozen=True)
class DuplicateRulePreventionRecord:
    record_id: str
    search_before_create_required: bool
    standard_patch_required_for_extension: bool


@dataclass(frozen=True)
class LegacyEvidencePreservationRecord:
    record_id: str
    original_artifacts_preserved: bool
    packaging_deletes_evidence_forbidden: bool


@dataclass(frozen=True)
class P1MidplatformGovernanceStandardsPackagingPlanningDecision:
    decision_ref: str
    midplatform_governance_standards_packaging_planning_profile_count: int
    governance_standards_packaging_scope_record_count: int
    governance_standards_directory_plan_record_count: int
    governance_standards_index_plan_record_count: int
    governance_standards_manifest_plan_record_count: int
    reusable_rule_classification_record_count: int
    main_program_separation_record_count: int
    governance_standard_reference_policy_record_count: int
    governance_standard_future_execution_route_record_count: int
    legacy_reusable_governance_rules_inventory_record_count: int
    governance_rule_usage_notes_index_record_count: int
    governance_standard_reuse_policy_record_count: int
    duplicate_rule_prevention_record_count: int
    legacy_evidence_preservation_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    governance_standards_root_planned: bool
    legacy_reusable_governance_rules_inventory_planned: bool
    usage_notes_index_planned: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)

def load_legacy_inventory() -> Dict[str, Any]:
    """Load legacy inventory from repo-relative path (caller resolves file)."""
    return {}


def validate_legacy_inventory_rules(inventory: Dict[str, Any]) -> Tuple[bool, int, bool]:
    rules = inventory.get("rules", [])
    count = len(rules)
    if count < 17:
        return False, count, False
    usage_ok = all(
        bool(r.get("when_to_use")) and bool(r.get("how_to_use")) and bool(r.get("forbidden_usage"))
        for r in rules
    )
    return True, count, usage_ok


def build_planned_manifest() -> Dict[str, Any]:
    return {
        "manifest_id": "GovernanceStandardsManifestV1",
        "version": "1.0.0-planning",
        "created_by_phase": PHASE_ID,
        "standard_library_root": LIBRARY_ROOT,
        "standards": [
            {
                "standard_id": m["standard_id"],
                "standard_name": m["standard_id"],
                "category": m["category"],
                "canonical_path": m["canonical_path"],
                "source_path": m["source_path"],
                "version": "1",
                "lifecycle_status": "planned_migration",
                "reusable_scope": "midplatform_governance",
                "dependencies": [MODEL_ASSET_ONBOARDING_STANDARD_ID]
                if m["category"] == "model_onboarding"
                else [],
                "referenced_by_phases": [UPSTREAM_STANDARDIZATION_PHASE_REF],
                "protected": True,
                "non_deletable": True,
            }
            for m in PLANNED_MIGRATIONS
        ],
        "categories": list(STANDARD_CATEGORIES),
        "future_execution_required": True,
        "migration_mode": "planned_only",
        "main_program_separation": True,
        "runtime_execution_allowed": False,
    }
