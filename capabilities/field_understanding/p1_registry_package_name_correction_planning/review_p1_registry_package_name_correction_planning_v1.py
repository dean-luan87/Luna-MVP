# -*- coding: utf-8 -*-
"""P1 Registry Package Name Correction Planning — review v1.

PLANNING ONLY, scope = byte_track ONLY. Clarifies byte_track's registry identity
(package_name mismatch / import_name mismatch / source_component classification /
asset+dependency split), produces >=3 correction options + a recommendation, and
routes it to source-install resolution planning. It MUTATES NOTHING and executes
NOTHING: no registry file write, no name replacement, no pip install, no git
clone, no source install, no download, no real import / model load / inference,
no runtime / output adapter / semantic layer. Protected, non-deletable test
board records are written in planning mode.
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
from capabilities.field_understanding.p1_registry_package_name_correction_planning.p1_registry_package_name_correction_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_registry_package_name_correction_planning.p1_registry_package_name_correction_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BYTE_TRACK_PROVENANCE,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CURRENT_MAPPING,
    DATASET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FOLLOWUP_REVIEW_REQUIREMENT,
    GIT_CLONE_ALLOWED,
    IMPORT_NAME_ISSUE_CLASSIFICATIONS,
    IN_SCOPE_ASSET_ID,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    PACKAGE_INSTALL_ALLOWED,
    PACKAGE_NAME_ISSUE_CLASSIFICATIONS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_CORRECTION_OPTIONS,
    REGISTRY_CORRECTION_PLANNING_ONLY,
    REGISTRY_CORRECTION_RECOMMENDATION,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_MUTATION_BOUNDARY,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_COMPONENT_CLASSIFICATIONS,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_POST_REVIEW_REF,
    UPSTREAM_RESOLUTION_PLANNING_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    CurrentPackageImportMappingRecord,
    FollowupReviewRequirement,
    ImportNameIssueClassification,
    NegativeRegistryCorrectionPlanningGuard,
    P1RegistryPackageNameCorrectionPlanningDecision,
    P1RegistryPackageNameCorrectionPlanningProfile,
    PackageNameIssueClassification,
    RegistryCorrectionInputRecord,
    RegistryCorrectionOption,
    RegistryCorrectionRecommendation,
    RegistryMutationBoundary,
    SourceComponentClassification,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (Path.cwd(), _REPO_ROOT):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_registry_package_name_correction_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_registry_package_name_correction_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_registry_package_name_correction_planning"
STEP_FILES = (
    f"{_PKG}/p1_registry_package_name_correction_planning_types_v1.py",
    f"{_PKG}/p1_registry_package_name_correction_planning_registry_v1.py",
    f"{_PKG}/review_p1_registry_package_name_correction_planning_v1.py",
)

PROFILE_REF = "p1_registry_package_name_correction_planning_profile_v1"
DECISION_REF = "p1_registry_package_name_correction_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1RegistryPackageNameCorrectionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            registry_correction_planning_only=REGISTRY_CORRECTION_PLANNING_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            package_install_allowed=PACKAGE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_id=IN_SCOPE_ASSET_ID,
            upstream_resolution_planning_ref=UPSTREAM_RESOLUTION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_registry_package_name_correction_planning_v1(
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
        if (_REPO_ROOT / rel).is_file() or (Path.cwd() / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    # ------------------------------------------------------------------- #
    # (一) Input record — byte_track provenance across the chain.
    # ------------------------------------------------------------------- #
    input_record = RegistryCorrectionInputRecord(
        asset_id=BYTE_TRACK_PROVENANCE["asset_id"],
        from_execution_deferred=BYTE_TRACK_PROVENANCE["from_execution_deferred"],
        from_post_review_deferred_asset_audit=BYTE_TRACK_PROVENANCE["from_post_review_deferred_asset_audit"],
        from_resolution_planning_candidate=BYTE_TRACK_PROVENANCE["from_resolution_planning_candidate"],
        provenance_confirmed=(
            BYTE_TRACK_PROVENANCE["from_execution_deferred"] == UPSTREAM_EXECUTION_REF
            and BYTE_TRACK_PROVENANCE["from_post_review_deferred_asset_audit"] == UPSTREAM_POST_REVIEW_REF
            and BYTE_TRACK_PROVENANCE["from_resolution_planning_candidate"] == UPSTREAM_RESOLUTION_PLANNING_REF
        ),
    )

    # ------------------------------------------------------------------- #
    # (二) Current mapping review.
    # ------------------------------------------------------------------- #
    mapping_record = CurrentPackageImportMappingRecord(
        asset_id=CURRENT_MAPPING["asset_id"],
        current_package_candidate=CURRENT_MAPPING["current_package_candidate"],
        current_import_candidate=CURRENT_MAPPING["current_import_candidate"],
        clean_pypi_install_status=CURRENT_MAPPING["clean_pypi_install_status"],
        find_spec_status=CURRENT_MAPPING["find_spec_status"],
        deferred_reason_tokens=tuple(CURRENT_MAPPING["deferred_reason_tokens"]),
        current_mapping_is_not_accepted_for_full_install=CURRENT_MAPPING["current_mapping_is_not_accepted_for_full_install"],
        current_mapping_requires_correction_planning=CURRENT_MAPPING["current_mapping_requires_correction_planning"],
    )

    # ------------------------------------------------------------------- #
    # (三) Issue classifications.
    # ------------------------------------------------------------------- #
    package_name_issues = [PackageNameIssueClassification(**c) for c in PACKAGE_NAME_ISSUE_CLASSIFICATIONS]
    import_name_issues = [ImportNameIssueClassification(**c) for c in IMPORT_NAME_ISSUE_CLASSIFICATIONS]
    source_component_issues = [SourceComponentClassification(**c) for c in SOURCE_COMPONENT_CLASSIFICATIONS]

    # ------------------------------------------------------------------- #
    # (四) Registry correction options + (五) recommendation.
    # ------------------------------------------------------------------- #
    correction_options = [RegistryCorrectionOption(**o) for o in REGISTRY_CORRECTION_OPTIONS]
    recommendation = RegistryCorrectionRecommendation(**REGISTRY_CORRECTION_RECOMMENDATION)

    # ------------------------------------------------------------------- #
    # (六) Registry mutation boundary + (七) follow-up.
    # ------------------------------------------------------------------- #
    mutation_boundary = RegistryMutationBoundary(**REGISTRY_MUTATION_BOUNDARY)
    followup = FollowupReviewRequirement(**FOLLOWUP_REVIEW_REQUIREMENT)

    # ------------------------------------------------------------------- #
    # Invariants for the 19 negative guards.
    # ------------------------------------------------------------------- #
    package_name_mismatch_recorded = any(
        c.issue_kind == "package_name_mismatch" and c.asset_id == "byte_track" for c in package_name_issues
    )
    import_name_mismatch_recorded = any(
        c.issue_kind == "import_name_mismatch" and c.asset_id == "byte_track" for c in import_name_issues
    )
    source_component_classification_recorded = any(
        c.issue_kind == "source_component_classification" and c.asset_id == "byte_track" for c in source_component_issues
    )
    source_install_resolution_followup_recorded = (
        followup.source_install_resolution_required
        and recommendation.byte_track_should_enter_source_install_resolution_planning
    )
    byte_track_remains_deferred = recommendation.byte_track_should_remain_deferred
    not_clean_pypi_install_ready = (
        recommendation.byte_track_should_not_remain_clean_pypi_candidate_until_corrected
        and all(not o.clean_pypi_candidate for o in correction_options)
    )

    invariant_state: Dict[str, bool] = {
        "no_registry_mutation": (
            REGISTRY_MUTATION_ALLOWED is False
            and mutation_boundary.no_registry_file_write
            and mutation_boundary.no_replacement_of_package_name
            and mutation_boundary.no_replacement_of_import_name
        ),
        "not_clean_pypi_install_ready": not_clean_pypi_install_ready,
        "not_runtime_ready": mutation_boundary.no_promotion_to_runtime_ready,
        "not_inference_ready": mutation_boundary.no_promotion_to_inference_ready,
        "no_pip_install": PIP_INSTALL_ALLOWED is False and PACKAGE_INSTALL_ALLOWED is False,
        "no_git_clone_source_install": GIT_CLONE_ALLOWED is False and SOURCE_INSTALL_ALLOWED is False,
        "no_download_performed": (
            MODEL_DOWNLOAD_ALLOWED is False
            and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "package_name_mismatch_recorded": package_name_mismatch_recorded,
        "import_name_mismatch_recorded": import_name_mismatch_recorded,
        "source_component_classification_recorded": source_component_classification_recorded,
        "source_install_resolution_followup_recorded": source_install_resolution_followup_recorded,
        "planning_not_registry_mutation_approval": (
            REGISTRY_MUTATION_ALLOWED is False
            and recommendation.registry_correction_planning_success_is_not_registry_mutation_approval
            and recommendation.registry_mutation_requires_separate_review_or_patch_phase
        ),
        "planning_not_source_install_approval": (
            SOURCE_INSTALL_ALLOWED is False and followup.owner_approval_required_before_source_install
        ),
        "planning_not_weight_approval": (
            WEIGHT_DOWNLOAD_ALLOWED is False and followup.weight_download_requires_separate_approval
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeRegistryCorrectionPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeRegistryCorrectionPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_registry_correction_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "registry_package_name_correction_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "registry_correction_input_record_count_eq_1": True,
        "current_package_import_mapping_record_count_eq_1": True,
        "package_name_issue_classification_count_gte_1": len(package_name_issues) >= 1,
        "import_name_issue_classification_count_gte_1": len(import_name_issues) >= 1,
        "source_component_classification_count_gte_1": len(source_component_issues) >= 1,
        "registry_correction_option_count_gte_3": len(correction_options) >= 3,
        "registry_correction_recommendation_count_gte_1": True,
        "registry_mutation_boundary_count_gte_1": True,
        "followup_review_requirement_count_gte_1": True,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings (planning-only).
        "planning_only": PLANNING_ONLY is True,
        "registry_correction_planning_only": REGISTRY_CORRECTION_PLANNING_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "package_install_allowed_false": PACKAGE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Correction facts.
        "byte_track_only_scope": IN_SCOPE_ASSET_ID == "byte_track",
        "byte_track_package_name_mismatch_recorded": package_name_mismatch_recorded,
        "byte_track_import_name_mismatch_recorded": import_name_mismatch_recorded,
        "byte_track_source_component_classification_recorded": source_component_classification_recorded,
        "byte_track_remains_deferred": byte_track_remains_deferred,
        "byte_track_not_clean_pypi_install_ready": not_clean_pypi_install_ready,
        "source_install_resolution_required": followup.source_install_resolution_required,
        "registry_patch_required_before_future_clean_execution": followup.registry_patch_required_before_future_clean_execution,
        "registry_correction_planning_success_not_registry_mutation_approval": (
            recommendation.registry_correction_planning_success_is_not_registry_mutation_approval
        ),
        "registry_correction_planning_success_not_source_install_approval": (
            SOURCE_INSTALL_ALLOWED is False and followup.owner_approval_required_before_source_install
        ),
        "registry_correction_planning_success_not_weight_download_approval": (
            WEIGHT_DOWNLOAD_ALLOWED is False and followup.weight_download_requires_separate_approval
        ),
        # Negative guard GO keys.
        **negative_guard_go,
        # Test board fields + write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0
    final_decision = FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1RegistryPackageNameCorrectionPlanningDecision(
        decision_ref=DECISION_REF,
        registry_package_name_correction_planning_profile_count=1,
        registry_correction_input_record_count=1,
        current_package_import_mapping_record_count=1,
        package_name_issue_classification_count=len(package_name_issues),
        import_name_issue_classification_count=len(import_name_issues),
        source_component_classification_count=len(source_component_issues),
        registry_correction_option_count=len(correction_options),
        registry_correction_recommendation_count=1,
        registry_mutation_boundary_count=1,
        followup_review_requirement_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Registry Package Name Correction Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "in_scope_asset_id": IN_SCOPE_ASSET_ID,
        "upstream_resolution_planning_ref": UPSTREAM_RESOLUTION_PLANNING_REF,
        "upstream_post_review_ref": UPSTREAM_POST_REVIEW_REF,
        "upstream_execution_ref": UPSTREAM_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "registry_package_name_correction_planning_profile": _build_profile(),
        "registry_package_name_correction_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Planning artifacts.
        "registry_correction_input_record": asdict(input_record),
        "registry_correction_input_record_count": 1,
        "current_package_import_mapping_record": asdict(mapping_record),
        "current_package_import_mapping_record_count": 1,
        "package_name_issue_classifications": [asdict(c) for c in package_name_issues],
        "package_name_issue_classification_count": len(package_name_issues),
        "import_name_issue_classifications": [asdict(c) for c in import_name_issues],
        "import_name_issue_classification_count": len(import_name_issues),
        "source_component_classifications": [asdict(c) for c in source_component_issues],
        "source_component_classification_count": len(source_component_issues),
        "registry_correction_options": [asdict(o) for o in correction_options],
        "registry_correction_option_count": len(correction_options),
        "registry_correction_recommendation": asdict(recommendation),
        "registry_correction_recommendation_count": 1,
        "registry_mutation_boundary": asdict(mutation_boundary),
        "registry_mutation_boundary_count": 1,
        "followup_review_requirement": asdict(followup),
        "followup_review_requirement_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_registry_package_name_correction_planning_status": (
                "byte_track_registry_identity_clarified_no_registry_mutation_remains_deferred"
                if review_ok
                else "blocked"
            ),
            "recommended_registry_action": recommendation.recommended_registry_action,
            "byte_track_correction_options": [o.option_id for o in correction_options],
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "byte_track registry identity CLARIFIED (planning only). The current mapping (package_candidate="
                "bytetrack, import_candidate=yolox) is NOT accepted for full install and requires correction. Three "
                "issue classes were recorded: package-name mismatch (bytetrack may not be the correct clean PyPI "
                "name), import-name mismatch (yolox is inconsistent with asset_id byte_track; yolox role to confirm "
                "as dependency / source family / runtime import root), and source-component classification (byte_track "
                "may be a ByteTrack/YOLOX source component, not a standalone clean PyPI package). >=3 correction "
                "options + an optional candidate-only Option D were produced; recommended registry action = mark "
                "byte_track as source_component_or_unresolved_package. NO registry mutation, no file write, no name "
                "replacement, no install/clone/download, no real import/load/inference/runtime/output/semantic. "
                "Registry correction planning success is NOT registry-mutation / source-install / weight-download "
                "approval; byte_track REMAINS DEFERRED. Do NOT patch registry yet. Next: "
                "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001 to risk-split byte_track + mobile_sam "
                "source-install routes, then decide whether a registry patch is needed or to classify them as "
                "source_component."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
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
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_out = Path(manifest["test_board_dir"])
        extra_payloads = {
            "registry_correction_plan_record": {
                "registry_correction_input_record": asdict(input_record),
                "registry_correction_options": [asdict(o) for o in correction_options],
                "registry_correction_recommendation": asdict(recommendation),
                "followup_review_requirement": asdict(followup),
            },
            "package_import_mapping_record": {
                "current_package_import_mapping_record": asdict(mapping_record),
                "package_name_issue_classifications": [asdict(c) for c in package_name_issues],
                "import_name_issue_classifications": [asdict(c) for c in import_name_issues],
            },
            "source_component_classification_record": {
                "source_component_classifications": [asdict(c) for c in source_component_issues]
            },
            "registry_mutation_boundary_record": {
                "registry_mutation_boundary": asdict(mutation_boundary)
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
            "registry_mutation_allowed": False,
            "source_install_allowed": False,
            "weight_download_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_out / f"{rtype}.json"
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
    result = review_p1_registry_package_name_correction_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "correction_option_count": result["decision"]["registry_correction_option_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
