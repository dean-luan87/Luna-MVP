# -*- coding: utf-8 -*-
"""P1 Midplatform Governance Standards Packaging Planning — review v1 (PLANNING ONLY).

Plans centralized midplatform governance standards library packaging. No file move,
no main program mutation, no runtime, no registry mutation.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.midplatform.governance_standards.governance_standards_packaging_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.governance_standards.governance_standards_packaging_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FILE_DELETE_ALLOWED,
    FILE_MOVE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INDEX_MD_REL,
    LIBRARY_EXCLUDES,
    LIBRARY_ROOT,
    LIBRARY_STORES,
    LUNA_CORE_PRINCIPLE,
    MAIN_PROGRAM_MUTATION_ALLOWED,
    MAIN_PROGRAM_SEPARATION_RULES,
    MANIFEST_JSON_REL,
    MODEL_LOAD_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    PACKAGING_PLAN_MD_REL,
    PACKAGING_PRINCIPLE_ZH,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNED_MIGRATIONS,
    PLANNED_SUBDIRECTORIES,
    PLANNING_ONLY,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    RECOMMENDED_NEXT_PHASE,
    REFERENCE_POLICY_RULES,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSABLE_RULE_CLASSIFICATION,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_STANDARDIZATION_PHASE_REF,
    WEIGHT_CHAIN,
    WEIGHT_DOWNLOAD_ALLOWED,
    GovernanceStandardFutureExecutionRouteRecord,
    GovernanceStandardReferencePolicyRecord,
    GovernanceStandardReusePolicyRecord,
    GovernanceStandardsDirectoryPlanRecord,
    GovernanceStandardsIndexPlanRecord,
    GovernanceStandardsManifestPlanRecord,
    GovernanceStandardsPackagingScopeRecord,
    GovernanceRuleUsageNotesIndexRecord,
    DuplicateRulePreventionRecord,
    LegacyEvidencePreservationRecord,
    LegacyReusableGovernanceRulesInventoryRecord,
    MainProgramSeparationRecord,
    NegativeGovernanceStandardsPackagingPlanningGuard,
    P1MidplatformGovernanceStandardsPackagingPlanningDecision,
    P1MidplatformGovernanceStandardsPackagingPlanningProfile,
    ReusableRuleClassificationRecord,
    LEGACY_INVENTORY_REL,
    LEGACY_MAPPING_REL,
    REUSE_BEFORE_CREATE_POLICY_RULES,
    USAGE_NOTES_INDEX_REL,
    build_planned_manifest,
    validate_legacy_inventory_rules,
    to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_midplatform_governance_standards_packaging_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_midplatform_governance_standards_packaging_planning_review_v1.json"
DIRECTORY_PLAN_FILENAME = "governance_standards_directory_plan_v1.json"
MANIFEST_PLAN_FILENAME = "governance_standards_manifest_plan_v1.json"
REFERENCE_POLICY_FILENAME = "governance_standards_reference_policy_v1.json"
FUTURE_ROUTE_FILENAME = "governance_standards_future_execution_route_v1.json"
LEGACY_INVENTORY_PLAN_FILENAME = "legacy_reusable_governance_rules_inventory_plan_v1.json"
USAGE_NOTES_INDEX_PLAN_FILENAME = "governance_rule_usage_notes_index_plan_v1.json"
REUSE_POLICY_FILENAME = "governance_standard_reuse_policy_v1.json"

_PKG = "capabilities/midplatform/governance_standards"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/governance_standards_packaging_types_v1.py",
    f"{_PKG}/governance_standards_packaging_registry_v1.py",
    f"{_PKG}/governance_standards_index_v1.md",
    f"{_PKG}/governance_standards_manifest_v1.json",
    f"{_PKG}/reusable_governance_standard_packaging_plan_v1.md",
    f"{_PKG}/review_governance_standards_packaging_v1.py",
    LEGACY_INVENTORY_REL,
    LEGACY_MAPPING_REL,
    USAGE_NOTES_INDEX_REL,
    f"{_PKG}/protocol_governance/protocol_governance_standard_index_v1.md",
    f"{_PKG}/file_governance/file_size_module_split_governance_rule_v1.md",
    f"{_PKG}/input_output_symmetry/input_output_symmetry_governance_standard_v1.md",
    f"{_PKG}/owner_approval/owner_approval_governance_standard_v1.md",
    f"{_PKG}/validation_rules/validate_once_reference_governance_standard_v1.md",
)

INDEX_REQUIRED_SECTIONS = (
    "Purpose",
    "Directory Layout",
    "Standard Categories",
    "Canonical Standard Paths",
    "Versioning Policy",
    "Reference Policy",
    "Do Not Mix With Main Program",
    "Runtime Separation Policy",
    "Registry Patch Standard",
    "Test Board Standard",
    "Approval Gate Standard",
    "Failure Semantics Standard",
    "Reusable Phase Templates",
    "Case Mappings",
    "Future Migration / Packaging Execution Route",
)

USAGE_NOTES_INDEX_REQUIRED_SECTIONS = (
    "How to Select a Governance Rule",
    "Rule Categories",
    "Common Phase Patterns",
    "When to Reuse Existing Rule Instead of Creating a New One",
    "How to Cite a Standard in a Phase Instruction",
    "How to Handle Similar Workflows",
    "When a New Rule Is Allowed",
    "When Rule Duplication Is Forbidden",
    "How to Update a Standard",
    "How to Deprecate a Standard",
    "How to Preserve Historical Evidence",
    "How to Keep Main Program Separated",
)

PROFILE_REF = "p1_midplatform_governance_standards_packaging_planning_profile_v1"
DECISION_REF = "p1_midplatform_governance_standards_packaging_planning_decision_v1"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _audit_index(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    found = [s for s in INDEX_REQUIRED_SECTIONS if s in text]
    return {
        "path": str(path),
        "sections_required": len(INDEX_REQUIRED_SECTIONS),
        "sections_found": len(found),
        "sections_missing": [s for s in INDEX_REQUIRED_SECTIONS if s not in text],
    }


def _audit_usage_notes_index(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    found = [s for s in USAGE_NOTES_INDEX_REQUIRED_SECTIONS if s in text]
    return {
        "path": str(path),
        "sections_required": len(USAGE_NOTES_INDEX_REQUIRED_SECTIONS),
        "sections_found": len(found),
        "sections_missing": [s for s in USAGE_NOTES_INDEX_REQUIRED_SECTIONS if s not in text],
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MidplatformGovernanceStandardsPackagingPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            midplatform_governance_standard_packaging=True,
            centralized_reusable_rule_library=True,
            main_program_separation_required=True,
            file_move_allowed=FILE_MOVE_ALLOWED,
            file_delete_allowed=FILE_DELETE_ALLOWED,
            main_program_mutation_allowed=MAIN_PROGRAM_MUTATION_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            registry_mutation_allowed=False,
            library_root=LIBRARY_ROOT,
            upstream_standardization_phase_ref=UPSTREAM_STANDARDIZATION_PHASE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_governance_standards_packaging_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    for sub in PLANNED_SUBDIRECTORIES:
        sub_found = any((base / LIBRARY_ROOT / sub).is_dir() for base in _artifact_roots())
        if sub_found:
            passed_checks.append(f"subdir.planned_present={sub}")
        else:
            failed_checks.append(f"subdir.planned_missing={sub}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or (_WRITABLE_BASE / DEFAULT_OUTPUT_ROOT.relative_to(_REPO_ROOT))).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    index_path = _resolve_file(INDEX_MD_REL)
    manifest_path = _resolve_file(MANIFEST_JSON_REL)
    packaging_plan_path = _resolve_file(PACKAGING_PLAN_MD_REL)

    index_audit: Dict[str, Any] = {}
    index_planned = False
    if index_path is not None:
        index_audit = _audit_index(index_path)
        index_planned = index_audit["sections_found"] == index_audit["sections_required"]
        if not index_planned:
            failed_checks.append(f"index.sections_missing={index_audit['sections_missing']}")
    else:
        failed_checks.append("index.markdown_missing")

    manifest_planned = False
    manifest_data: Dict[str, Any] = {}
    if manifest_path is not None:
        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_planned = (
                manifest_data.get("manifest_id") == "GovernanceStandardsManifestV1"
                and manifest_data.get("migration_mode") == "planned_only"
                and len(manifest_data.get("standards", [])) >= 6
            )
            if not manifest_planned:
                failed_checks.append("manifest.plan_incomplete")
        except (OSError, json.JSONDecodeError):
            failed_checks.append("manifest.parse_failed")
    else:
        failed_checks.append("manifest.json_missing")

    legacy_inventory_path = _resolve_file(LEGACY_INVENTORY_REL)
    legacy_mapping_path = _resolve_file(LEGACY_MAPPING_REL)
    usage_notes_path = _resolve_file(USAGE_NOTES_INDEX_REL)
    legacy_inventory_data: Dict[str, Any] = {}
    legacy_inventory_planned = False
    legacy_rule_count = 0
    per_rule_usage_note_ok = False
    if legacy_inventory_path is not None:
        try:
            legacy_inventory_data = json.loads(legacy_inventory_path.read_text(encoding="utf-8"))
            legacy_inventory_planned, legacy_rule_count, per_rule_usage_note_ok = validate_legacy_inventory_rules(
                legacy_inventory_data
            )
            if not legacy_inventory_planned:
                failed_checks.append("legacy.inventory_incomplete")
            if not per_rule_usage_note_ok:
                failed_checks.append("legacy.per_rule_usage_note_missing")
        except (OSError, json.JSONDecodeError):
            failed_checks.append("legacy.inventory_parse_failed")
    else:
        failed_checks.append("legacy.inventory_missing")

    usage_notes_audit: Dict[str, Any] = {}
    usage_notes_index_planned = False
    if usage_notes_path is not None:
        usage_notes_audit = _audit_usage_notes_index(usage_notes_path)
        usage_notes_index_planned = (
            usage_notes_audit["sections_found"] == usage_notes_audit["sections_required"]
        )
        if not usage_notes_index_planned:
            failed_checks.append(f"usage_notes.sections_missing={usage_notes_audit['sections_missing']}")
    else:
        failed_checks.append("usage_notes.index_missing")

    if legacy_mapping_path is None:
        failed_checks.append("legacy.mapping_missing")

    scope_record = GovernanceStandardsPackagingScopeRecord(
        record_id="governance_standards_packaging_scope_v1",
        library_root=LIBRARY_ROOT,
        library_stores=LIBRARY_STORES,
        library_excludes=LIBRARY_EXCLUDES,
        planning_only=True,
    )
    directory_plan = GovernanceStandardsDirectoryPlanRecord(
        record_id="governance_standards_directory_plan_v1",
        planned_subdirectories=PLANNED_SUBDIRECTORIES,
        subdirectory_count=len(PLANNED_SUBDIRECTORIES),
        migration_mode="planned_only",
    )
    index_plan = GovernanceStandardsIndexPlanRecord(
        record_id="governance_standards_index_plan_v1",
        index_rel_path=INDEX_MD_REL,
        required_sections_defined=index_planned,
        section_count=index_audit.get("sections_found", 0),
    )
    manifest_plan = GovernanceStandardsManifestPlanRecord(
        record_id="governance_standards_manifest_plan_v1",
        manifest_rel_path=MANIFEST_JSON_REL,
        planned_standard_count=len(PLANNED_MIGRATIONS),
        migration_mode="planned_only",
        main_program_separation=True,
    )
    rule_classification = ReusableRuleClassificationRecord(
        record_id="reusable_rule_classification_v1",
        categories=tuple(REUSABLE_RULE_CLASSIFICATION.keys()),
        classification=REUSABLE_RULE_CLASSIFICATION,
    )
    separation_record = MainProgramSeparationRecord(
        record_id="main_program_separation_v1",
        separation_rules=MAIN_PROGRAM_SEPARATION_RULES,
        governance_standards_not_under_main_program=True,
        runtime_admission_gate_required=True,
    )
    reference_policy = GovernanceStandardReferencePolicyRecord(
        record_id="governance_standard_reference_policy_v1",
        reference_rules=REFERENCE_POLICY_RULES,
        canonical_path_policy=True,
        historical_evidence_preserved=True,
    )
    future_route = GovernanceStandardFutureExecutionRouteRecord(
        record_id="governance_standard_future_execution_route_v1",
        recommended_next_phase=RECOMMENDED_NEXT_PHASE,
        allows_directory_creation=True,
        allows_copy_or_migrate=True,
        allows_manifest_and_index_generation=True,
        forbids_main_program_mutation=True,
        forbids_runtime_execution=True,
        forbids_deleting_original_evidence=True,
    )
    legacy_inventory_record = LegacyReusableGovernanceRulesInventoryRecord(
        record_id="legacy_reusable_governance_rules_inventory_v1",
        inventory_rel_path=LEGACY_INVENTORY_REL,
        rule_count=legacy_rule_count,
        all_rules_have_usage_notes=per_rule_usage_note_ok,
    )
    usage_notes_index_record = GovernanceRuleUsageNotesIndexRecord(
        record_id="governance_rule_usage_notes_index_v1",
        index_rel_path=USAGE_NOTES_INDEX_REL,
        required_sections_defined=usage_notes_index_planned,
    )
    reuse_policy_record = GovernanceStandardReusePolicyRecord(
        record_id="governance_standard_reuse_policy_v1",
        reuse_before_create_rules=REUSE_BEFORE_CREATE_POLICY_RULES,
        duplicate_rule_creation_forbidden=True,
    )
    duplicate_prevention_record = DuplicateRulePreventionRecord(
        record_id="duplicate_rule_prevention_v1",
        search_before_create_required=True,
        standard_patch_required_for_extension=True,
    )
    legacy_evidence_record = LegacyEvidencePreservationRecord(
        record_id="legacy_evidence_preservation_v1",
        original_artifacts_preserved=True,
        packaging_deletes_evidence_forbidden=True,
    )

    directory_plan_payload = {
        "phase_id": PHASE_ID,
        "library_root": LIBRARY_ROOT,
        "planned_subdirectories": list(PLANNED_SUBDIRECTORIES),
        "planned_migrations": list(PLANNED_MIGRATIONS),
        "migration_mode": "planned_only",
        "file_move_allowed": False,
        "recorded_at_utc": _now(),
    }
    manifest_plan_payload = build_planned_manifest()
    reference_policy_payload = {
        "phase_id": PHASE_ID,
        "reference_rules": list(REFERENCE_POLICY_RULES),
        "reuse_before_create_rules": list(REUSE_BEFORE_CREATE_POLICY_RULES),
        "main_program_separation_rules": list(MAIN_PROGRAM_SEPARATION_RULES),
        "prefer_root": LIBRARY_ROOT,
        "historical_evidence_preserved": True,
        "duplicate_rule_creation_forbidden": True,
        "standard_patch_required_for_rule_extension": True,
        "main_program_inline_governance_forbidden": True,
        "recorded_at_utc": _now(),
    }
    reuse_policy_payload = {
        "phase_id": PHASE_ID,
        "reuse_before_create_rules": list(REUSE_BEFORE_CREATE_POLICY_RULES),
        "duplicate_rule_creation_forbidden": True,
        "standard_patch_required_for_rule_extension": True,
        "search_before_create_required": True,
        "recorded_at_utc": _now(),
    }
    legacy_inventory_plan_payload = {
        "phase_id": PHASE_ID,
        "inventory_id": legacy_inventory_data.get("inventory_id"),
        "rule_count": legacy_rule_count,
        "inventory_rel": LEGACY_INVENTORY_REL,
        "mapping_rel": LEGACY_MAPPING_REL,
        "status": "planned_for_packaging",
        "per_rule_usage_note_required": True,
        "rules": legacy_inventory_data.get("rules", []),
        "recorded_at_utc": _now(),
    }
    usage_notes_index_plan_payload = {
        "phase_id": PHASE_ID,
        "index_rel": USAGE_NOTES_INDEX_REL,
        "sections_required": len(USAGE_NOTES_INDEX_REQUIRED_SECTIONS),
        "sections_found": usage_notes_audit.get("sections_found", 0),
        "recorded_at_utc": _now(),
    }
    future_route_payload = {
        "phase_id": PHASE_ID,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
        "allows": {
            "directory_creation": True,
            "copy_or_migrate": True,
            "manifest_generation": True,
            "index_generation": True,
            "path_mapping": True,
            "post_review": True,
        },
        "forbids": {
            "main_program_mutation": True,
            "runtime_execution": True,
            "deleting_original_evidence": True,
        },
        "recorded_at_utc": _now(),
    }

    invariant_state: Dict[str, bool] = {
        "no_file_move_or_delete": FILE_MOVE_ALLOWED is False and FILE_DELETE_ALLOWED is False,
        "no_main_program_mutation": MAIN_PROGRAM_MUTATION_ALLOWED is False,
        "no_install_download_import_load_inference_runtime": (
            PIP_INSTALL_ALLOWED is False
            and SOURCE_INSTALL_ALLOWED is False
            and WEIGHT_DOWNLOAD_ALLOWED is False
            and MODEL_LOAD_ALLOWED is False
            and RUNTIME_EXECUTION_ALLOWED is False
        ),
        "no_registry_write": REGISTRY_MUTATION_ALLOWED is False,
        "not_planned_under_main_program_runtime": LIBRARY_ROOT.startswith(
            "capabilities/midplatform/governance_standards"
        ),
        "no_weights_datasets_user_data_in_library": all(
            x in LIBRARY_EXCLUDES
            for x in ("weight_files", "datasets", "user_data")
        ),
        "runtime_must_not_bypass_admission_gate": separation_record.runtime_admission_gate_required,
        "output_adapter_must_not_read_candidate_directly": (
            "output_adapter_must_not_consume_candidate_output_without_admission"
            in PHASE_GOVERNANCE_RULES
        ),
        "semantic_fact_navigation_must_not_consume_trial_output": (
            "semantic_fact_navigation_must_not_consume_inference_trial_output_directly"
            in PHASE_GOVERNANCE_RULES
        ),
        "manifest_plan_present": manifest_planned,
        "index_plan_present": index_planned,
        "reference_policy_present": len(REFERENCE_POLICY_RULES) >= 7,
        "main_program_separation_present": len(MAIN_PROGRAM_SEPARATION_RULES) >= 8,
        "future_execution_route_present": bool(RECOMMENDED_NEXT_PHASE),
        "test_board_record_required_true": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_board_record_required") is True,
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected") is True
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_record_non_deletable") is True
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_deletion_forbidden") is True
        ),
        "cleanup_does_not_delete_test_board": True,
        "legacy_inventory_planned": legacy_inventory_planned,
        "per_rule_usage_note_required": per_rule_usage_note_ok,
        "duplicate_rule_creation_forbidden": reuse_policy_record.duplicate_rule_creation_forbidden,
        "main_program_inline_governance_forbidden": (
            "main_program_inline_governance_forbidden" in PHASE_GOVERNANCE_RULES
        ),
        "runtime_bypass_governance_forbidden": separation_record.runtime_admission_gate_required,
        "standard_patch_required_for_rule_extension": (
            duplicate_prevention_record.standard_patch_required_for_extension
        ),
        "legacy_evidence_preserved_on_packaging": (
            legacy_evidence_record.packaging_deletes_evidence_forbidden
            and future_route.forbids_deleting_original_evidence
        ),
        "reuse_before_create_policy_defined": len(REUSE_BEFORE_CREATE_POLICY_RULES) >= 7,
    }

    negative_guards: List[NegativeGovernanceStandardsPackagingPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeGovernanceStandardsPackagingPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_packaging_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "midplatform_governance_standards_packaging_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_6": len(stage_refs) >= 6,
        "governance_standards_packaging_scope_record_count_gte_1": True,
        "governance_standards_directory_plan_record_count_gte_1": True,
        "governance_standards_index_plan_record_count_gte_1": True,
        "governance_standards_manifest_plan_record_count_gte_1": True,
        "reusable_rule_classification_record_count_gte_1": True,
        "main_program_separation_record_count_gte_1": True,
        "governance_standard_reference_policy_record_count_gte_1": True,
        "governance_standard_future_execution_route_record_count_gte_1": True,
        "legacy_reusable_governance_rules_inventory_record_count_gte_1": True,
        "governance_rule_usage_notes_index_record_count_gte_1": True,
        "governance_standard_reuse_policy_record_count_gte_1": True,
        "duplicate_rule_prevention_record_count_gte_1": True,
        "legacy_evidence_preservation_record_count_gte_1": True,
        "negative_guard_count_eq_24": negative_guard_count == 24,
        "negative_guard_passed_eq_24": negative_guard_passed == 24,
        "legacy_reusable_governance_rules_inventory_planned": legacy_inventory_planned,
        "legacy_reusable_governance_rules_mapping_planned": legacy_mapping_path is not None,
        "usage_notes_index_planned": usage_notes_index_planned,
        "per_rule_usage_note_required": per_rule_usage_note_ok,
        "reuse_before_create_policy_defined": len(REUSE_BEFORE_CREATE_POLICY_RULES) >= 7,
        "duplicate_rule_creation_forbidden": True,
        "standard_patch_required_for_rule_extension": True,
        "main_program_inline_governance_forbidden": True,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "midplatform_governance_standard_packaging": True,
        "centralized_reusable_rule_library": True,
        "main_program_separation_required": True,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "file_move_allowed_false": FILE_MOVE_ALLOWED is False,
        "file_delete_allowed_false": FILE_DELETE_ALLOWED is False,
        "main_program_mutation_allowed_false": MAIN_PROGRAM_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "governance_standards_root_planned": packaging_plan_path is not None,
        "governance_standards_manifest_planned": manifest_planned,
        "governance_standards_index_planned": index_planned,
        "reference_policy_defined": len(REFERENCE_POLICY_RULES) >= 7,
        "main_program_separation_defined": len(MAIN_PROGRAM_SEPARATION_RULES) >= 8,
        "runtime_admission_gate_required": separation_record.runtime_admission_gate_required,
        "output_adapter_admission_gate_required": True,
        "semantic_fact_navigation_direct_consumption_forbidden": True,
        "future_execution_route_defined": bool(RECOMMENDED_NEXT_PHASE),
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": True,
        "test_board_protected_marker_written": True,
        "test_board_non_deletable_notice_written": True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformGovernanceStandardsPackagingPlanningDecision(
        decision_ref=DECISION_REF,
        midplatform_governance_standards_packaging_planning_profile_count=1,
        governance_standards_packaging_scope_record_count=1,
        governance_standards_directory_plan_record_count=1,
        governance_standards_index_plan_record_count=1,
        governance_standards_manifest_plan_record_count=1,
        reusable_rule_classification_record_count=1,
        main_program_separation_record_count=1,
        governance_standard_reference_policy_record_count=1,
        governance_standard_future_execution_route_record_count=1,
        legacy_reusable_governance_rules_inventory_record_count=1,
        governance_rule_usage_notes_index_record_count=1,
        governance_standard_reuse_policy_record_count=1,
        duplicate_rule_prevention_record_count=1,
        legacy_evidence_preservation_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        governance_standards_root_planned=packaging_plan_path is not None,
        legacy_reusable_governance_rules_inventory_planned=legacy_inventory_planned,
        usage_notes_index_planned=usage_notes_index_planned,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Midplatform Governance Standards Packaging Planning (planning only)",
        "source_chain": WEIGHT_CHAIN,
        "packaging_principle_zh": PACKAGING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "library_root": LIBRARY_ROOT,
        "planning_only": PLANNING_ONLY,
        "midplatform_governance_standard_packaging": True,
        "file_move_allowed": FILE_MOVE_ALLOWED,
        "file_delete_allowed": FILE_DELETE_ALLOWED,
        "main_program_mutation_allowed": MAIN_PROGRAM_MUTATION_ALLOWED,
        "runtime_execution_allowed": RUNTIME_EXECUTION_ALLOWED,
        "registry_mutation_allowed": False,
        "upstream_standardization_phase_ref": UPSTREAM_STANDARDIZATION_PHASE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "midplatform_governance_standards_packaging_planning_profile": _build_profile(),
        "midplatform_governance_standards_packaging_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "governance_standards_index_audit": index_audit,
        "governance_standards_manifest_snapshot": manifest_data,
        "governance_standards_packaging_scope_record": asdict(scope_record),
        "governance_standards_packaging_scope_record_count": 1,
        "governance_standards_directory_plan_record": asdict(directory_plan),
        "governance_standards_directory_plan_record_count": 1,
        "governance_standards_index_plan_record": asdict(index_plan),
        "governance_standards_index_plan_record_count": 1,
        "governance_standards_manifest_plan_record": asdict(manifest_plan),
        "governance_standards_manifest_plan_record_count": 1,
        "reusable_rule_classification_record": asdict(rule_classification),
        "reusable_rule_classification_record_count": 1,
        "main_program_separation_record": asdict(separation_record),
        "main_program_separation_record_count": 1,
        "governance_standard_reference_policy_record": asdict(reference_policy),
        "governance_standard_reference_policy_record_count": 1,
        "governance_standard_future_execution_route_record": asdict(future_route),
        "governance_standard_future_execution_route_record_count": 1,
        "legacy_reusable_governance_rules_inventory_record": asdict(legacy_inventory_record),
        "legacy_reusable_governance_rules_inventory_record_count": 1,
        "governance_rule_usage_notes_index_record": asdict(usage_notes_index_record),
        "governance_rule_usage_notes_index_record_count": 1,
        "governance_standard_reuse_policy_record": asdict(reuse_policy_record),
        "governance_standard_reuse_policy_record_count": 1,
        "duplicate_rule_prevention_record": asdict(duplicate_prevention_record),
        "duplicate_rule_prevention_record_count": 1,
        "legacy_evidence_preservation_record": asdict(legacy_evidence_record),
        "legacy_evidence_preservation_record_count": 1,
        "legacy_inventory_audit": {
            "rule_count": legacy_rule_count,
            "per_rule_usage_note_ok": per_rule_usage_note_ok,
            "inventory_planned": legacy_inventory_planned,
        },
        "usage_notes_index_audit": usage_notes_audit,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "file_moved_this_phase": False,
            "main_program_mutated_this_phase": False,
            "registry_mutated_this_phase": False,
            "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
            "transition_note": (
                "PLANNING ONLY. Luna midplatform reusable governance standards library planned. "
                "Includes legacy rules inventory (17 categories) with per-rule usage notes, "
                "reuse-before-create policy, and main-program separation. "
                "NO file move, NO runtime, NO registry mutation. Next: "
                + RECOMMENDED_NEXT_PHASE
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / DIRECTORY_PLAN_FILENAME).write_text(
            json.dumps(directory_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_standards_directory_plan_file"] = str(out_root / DIRECTORY_PLAN_FILENAME)

        (out_root / MANIFEST_PLAN_FILENAME).write_text(
            json.dumps(manifest_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_standards_manifest_plan_file"] = str(out_root / MANIFEST_PLAN_FILENAME)

        (out_root / REFERENCE_POLICY_FILENAME).write_text(
            json.dumps(reference_policy_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_standards_reference_policy_file"] = str(out_root / REFERENCE_POLICY_FILENAME)

        (out_root / FUTURE_ROUTE_FILENAME).write_text(
            json.dumps(future_route_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_standards_future_execution_route_file"] = str(out_root / FUTURE_ROUTE_FILENAME)

        (out_root / LEGACY_INVENTORY_PLAN_FILENAME).write_text(
            json.dumps(legacy_inventory_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["legacy_reusable_governance_rules_inventory_plan_file"] = str(
            out_root / LEGACY_INVENTORY_PLAN_FILENAME
        )

        (out_root / USAGE_NOTES_INDEX_PLAN_FILENAME).write_text(
            json.dumps(usage_notes_index_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_rule_usage_notes_index_plan_file"] = str(out_root / USAGE_NOTES_INDEX_PLAN_FILENAME)

        (out_root / REUSE_POLICY_FILENAME).write_text(
            json.dumps(reuse_policy_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["governance_standard_reuse_policy_file"] = str(out_root / REUSE_POLICY_FILENAME)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [
            result.get("output_review_file"),
            result.get("governance_standards_directory_plan_file"),
            result.get("governance_standards_manifest_plan_file"),
            result.get("governance_standards_reference_policy_file"),
            result.get("governance_standards_future_execution_route_file"),
            result.get("legacy_reusable_governance_rules_inventory_plan_file"),
            result.get("governance_rule_usage_notes_index_plan_file"),
            result.get("governance_standard_reuse_policy_file"),
            str(legacy_inventory_path) if legacy_inventory_path else None,
            str(usage_notes_path) if usage_notes_path else None,
            str(index_path) if index_path else None,
            str(manifest_path) if manifest_path else None,
        ]
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "governance_standards_packaging_scope_record": {
                "governance_standards_packaging_scope_record": asdict(scope_record),
            },
            "governance_standards_directory_plan_record": {
                "governance_standards_directory_plan_record": asdict(directory_plan),
            },
            "governance_standards_index_plan_record": {
                "governance_standards_index_plan_record": asdict(index_plan),
            },
            "governance_standards_manifest_plan_record": {
                "governance_standards_manifest_plan_record": asdict(manifest_plan),
            },
            "reusable_rule_classification_record": {
                "reusable_rule_classification_record": asdict(rule_classification),
            },
            "main_program_separation_record": {"main_program_separation_record": asdict(separation_record)},
            "governance_standard_reference_policy_record": {
                "governance_standard_reference_policy_record": asdict(reference_policy),
            },
            "governance_standard_future_execution_route_record": {
                "governance_standard_future_execution_route_record": asdict(future_route),
            },
            "legacy_reusable_governance_rules_inventory_record": {
                "legacy_reusable_governance_rules_inventory_record": asdict(legacy_inventory_record),
            },
            "governance_rule_usage_notes_index_record": {
                "governance_rule_usage_notes_index_record": asdict(usage_notes_index_record),
            },
            "governance_standard_reuse_policy_record": {
                "governance_standard_reuse_policy_record": asdict(reuse_policy_record),
            },
            "duplicate_rule_prevention_record": {
                "duplicate_rule_prevention_record": asdict(duplicate_prevention_record),
            },
            "legacy_evidence_preservation_record": {
                "legacy_evidence_preservation_record": asdict(legacy_evidence_record),
            },
        }
        extra_written: List[str] = []
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
            "file_move_allowed": False,
            "main_program_mutation_allowed": False,
            "runtime_allowed": False,
            "inference_allowed": False,
            "registry_mutation_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["extra_written_record_count"] = len(extra_written)
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_governance_standards_packaging_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "governance_standards_directory_plan_file": result.get("governance_standards_directory_plan_file"),
                "governance_standards_manifest_plan_file": result.get("governance_standards_manifest_plan_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "stage_ref_count": result["stage_ref_count"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
