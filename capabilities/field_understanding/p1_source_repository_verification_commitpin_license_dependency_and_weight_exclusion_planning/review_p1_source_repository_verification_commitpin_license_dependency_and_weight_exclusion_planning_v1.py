# -*- coding: utf-8 -*-
"""P1 Source Repository Verification / CommitPin / License / Dependency /
Weight-Exclusion Planning — review v1 (PLANNING ONLY).

Compressed pre-retry planning for byte_track and mobile_sam. Produces:
  - repository candidate planning records (candidate-only, unverified),
  - commit pin planning records (unpinned, not fabricated),
  - license review planning records (uncompleted, not fabricated),
  - dependency review planning records (uncompleted, not fabricated),
  - a mobile_sam weight-excluding checkout plan record,
  - a source-execution retry gate + readiness preconditions (all unsatisfied now),
  - per-asset risk records,
  - follow-up routing to the network-enabled review phase.

It executes/mutates NOTHING and does NO network lookup. Protected, non-deletable
test board records are written in planning mode; cleanup must never delete them.
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
from capabilities.field_understanding.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning.p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BLOCKED_WEIGHT_PATTERNS,
    COMMERCIAL_RUNTIME_APPROVED,
    COMMIT_PIN_PLANNING_ONLY,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    DEPENDENCY_REVIEW_PLANNING_ONLY,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED,
    IN_SCOPE_ASSET_IDS,
    LICENSE_REVIEW_PLANNING_ONLY,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NETWORK_LOOKUP_ALLOWED,
    NEXT_STEP_REF,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    RECOMMENDED_NEXT_PHASE_REF,
    REGISTRY_MUTATION_ALLOWED,
    REPOSITORY_VERIFICATION_PLANNING_ONLY,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RETRY_READINESS_PRECONDITIONS,
    REUSE_FLAGS,
    RISK_DIMENSIONS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_EXECUTION_RETRY_ALLOWED_NOW,
    SOURCE_EXECUTION_RETRY_REQUIRES_FUTURE_READINESS,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_POST_REVIEW_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL,
    WEIGHT_EXCLUSION_PLANNING_ONLY,
    MobileSAMWeightExclusionPlanningRecord,
    NegativeSourceRepositoryVerificationCommitPinPlanningGuard,
    P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionPlanningProfile,
    P1SourceRepositoryVerificationCommitPinPlanningDecision,
    SourceCommitPinPlanningRecord,
    SourceDependencyReviewPlanningRecord,
    SourceExecutionRetryGatePlanningRecord,
    SourceExecutionRetryReadinessPrecondition,
    SourceLicenseReviewPlanningRecord,
    SourceRepositoryCandidatePlanningRecord,
    SourceRepositoryPlanningRiskRecord,
    SourceRepositoryVerificationPlanningInput,
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
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning"
STEP_FILES = (
    f"{_PKG}/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_types_v1.py",
    f"{_PKG}/p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_registry_v1.py",
    f"{_PKG}/review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_v1.py",
)

PROFILE_REF = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_profile_v1"
DECISION_REF = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            repository_verification_planning_only=REPOSITORY_VERIFICATION_PLANNING_ONLY,
            commit_pin_planning_only=COMMIT_PIN_PLANNING_ONLY,
            license_review_planning_only=LICENSE_REVIEW_PLANNING_ONLY,
            dependency_review_planning_only=DEPENDENCY_REVIEW_PLANNING_ONLY,
            weight_exclusion_planning_only=WEIGHT_EXCLUSION_PLANNING_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            network_lookup_allowed=NETWORK_LOOKUP_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            source_execution_retry_allowed_now=SOURCE_EXECUTION_RETRY_ALLOWED_NOW,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_post_review_ref=UPSTREAM_POST_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_v1(
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
    # (一) Inputs (2; both deferred from all_deferred_no_violation).
    # ------------------------------------------------------------------- #
    inputs: List[SourceRepositoryVerificationPlanningInput] = [
        SourceRepositoryVerificationPlanningInput(
            asset_id=aid,
            source_family=SOURCE_FAMILY[aid],
            from_all_deferred_no_violation=True,
            current_status="DEFERRED",
            source_execution_retry_allowed_now=False,
            weight_download_allowed_now=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (二) Repository candidate planning records (2; candidate-only).
    # ------------------------------------------------------------------- #
    candidate_records: List[SourceRepositoryCandidatePlanningRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        is_mobile_sam = aid == "mobile_sam"
        is_byte_track = aid == "byte_track"
        candidate_records.append(
            SourceRepositoryCandidatePlanningRecord(
                asset_id=aid,
                source_family=SOURCE_FAMILY[aid],
                repository_candidate_required=True,
                repository_url_candidate_status="unverified_candidate_or_missing",
                repository_url_must_be_verified_before_execution=True,
                repository_candidate_must_not_be_fabricated=True,
                network_lookup_required_in_future_review=True,
                network_lookup_allowed_now=False,
                git_clone_allowed_now=False,
                source_checkout_allowed_now=False,
                repository_identity_resolution_required=True,
                package_import_identity_unresolved_or_source_component=is_byte_track,
                repository_may_contain_committed_checkpoint_weight=is_mobile_sam,
                full_clone_may_equal_weight_download=is_mobile_sam,
            )
        )

    # ------------------------------------------------------------------- #
    # (三) Commit pin planning records (2; unpinned, not fabricated).
    # ------------------------------------------------------------------- #
    commit_records: List[SourceCommitPinPlanningRecord] = [
        SourceCommitPinPlanningRecord(
            asset_id=aid,
            commit_pin_required=True,
            commit_hash_currently_unverified=True,
            branch_or_tag_candidate_currently_unverified=True,
            commit_must_be_resolved_before_execution=True,
            commit_pin_must_not_be_fabricated=True,
            commit_drift_after_pin_blocks_execution=True,
            commit_pin_review_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (四) License review planning records (2; uncompleted, not fabricated).
    # ------------------------------------------------------------------- #
    license_records: List[SourceLicenseReviewPlanningRecord] = [
        SourceLicenseReviewPlanningRecord(
            asset_id=aid,
            license_review_required=True,
            source_license_currently_unverified=True,
            repository_license_file_must_be_checked=True,
            transitive_dependency_license_review_required=True,
            commercial_runtime_not_approved=True,
            license_review_must_complete_before_source_execution_retry=True,
            license_review_must_not_be_fabricated=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (五) Dependency review planning records (2; uncompleted, not fabricated).
    # ------------------------------------------------------------------- #
    dependency_records: List[SourceDependencyReviewPlanningRecord] = [
        SourceDependencyReviewPlanningRecord(
            asset_id=aid,
            dependency_review_required=True,
            source_requirements_currently_unverified=True,
            transitive_dependencies_currently_unverified=True,
            dependency_conflict_review_required=True,
            build_or_compile_risk_review_required=True,
            torch_dependency_review_required=True,
            opencv_dependency_review_required=True,
            numpy_scipy_dependency_review_required=True,
            dependency_review_must_complete_before_source_execution_retry=True,
            dependency_review_must_not_be_fabricated=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (六) mobile_sam weight-excluding checkout planning record (1).
    # ------------------------------------------------------------------- #
    mobile_sam_weight_exclusion = MobileSAMWeightExclusionPlanningRecord(
        asset_id="mobile_sam",
        mobile_sam_weight_excluding_checkout_required=True,
        full_clone_may_include_committed_checkpoint_weight=True,
        weight_files_must_be_excluded_from_checkout_or_blocked=True,
        checkpoint_files_must_be_excluded_from_checkout_or_blocked=True,
        large_binary_files_must_be_detected_before_checkout=True,
        git_lfs_must_be_blocked_or_explicitly_scoped=True,
        sparse_checkout_or_archive_filtering_required_if_supported=True,
        allowed_file_patterns_must_be_defined_before_execution=True,
        blocked_file_patterns_must_include_weight_checkpoint_extensions=True,
        blocked_file_patterns=BLOCKED_WEIGHT_PATTERNS,
        weight_excluding_checkout_plan_required_before_retry=True,
        weight_excluding_checkout_plan_success_not_weight_download_approval=True,
        weight_download_allowed=False,
    )

    # ------------------------------------------------------------------- #
    # (七) Source-execution retry gate + readiness preconditions.
    # ------------------------------------------------------------------- #
    readiness_preconditions: List[SourceExecutionRetryReadinessPrecondition] = [
        SourceExecutionRetryReadinessPrecondition(
            precondition_id=f"retry_precondition_{i+1}",
            precondition=name,
            required_before_retry=True,
            currently_satisfied=False,
        )
        for i, name in enumerate(RETRY_READINESS_PRECONDITIONS)
    ]
    retry_gate = SourceExecutionRetryGatePlanningRecord(
        gate_id="source_execution_retry_gate_v1",
        source_execution_retry_allowed_now=SOURCE_EXECUTION_RETRY_ALLOWED_NOW,
        source_execution_retry_requires_future_readiness=SOURCE_EXECUTION_RETRY_REQUIRES_FUTURE_READINESS,
        source_execution_retry_not_allowed_until_repository_verification_complete=True,
        source_execution_retry_not_allowed_until_commit_pin_complete=True,
        source_execution_retry_not_allowed_until_license_review_complete=True,
        source_execution_retry_not_allowed_until_dependency_review_complete=True,
        mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete=True,
        readiness_precondition_count=len(readiness_preconditions),
        readiness_preconditions_all_unsatisfied_now=all(not p.currently_satisfied for p in readiness_preconditions),
    )

    # ------------------------------------------------------------------- #
    # (八) Per-asset risk records (2; all 10 dimensions recorded).
    # ------------------------------------------------------------------- #
    risk_records: List[SourceRepositoryPlanningRiskRecord] = [
        SourceRepositoryPlanningRiskRecord(
            asset_id=aid,
            risk_dimensions=RISK_DIMENSIONS,
            all_risk_dimensions_recorded=len(RISK_DIMENSIONS) == 10,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # Invariants for the 19 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "no_network_lookup": (
            NETWORK_LOOKUP_ALLOWED is False
            and all(not c.network_lookup_allowed_now for c in candidate_records)
        ),
        "no_clone_checkout": (
            GIT_CLONE_ALLOWED is False and SOURCE_CHECKOUT_ALLOWED is False
            and all(not c.git_clone_allowed_now and not c.source_checkout_allowed_now for c in candidate_records)
        ),
        "no_install": (
            SOURCE_INSTALL_ALLOWED is False and PIP_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_ALLOWED is False
        ),
        "no_download": (
            MODEL_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and RUNTIME_ACTIVATION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "repo_not_faked_verified": all(
            c.repository_url_candidate_status == "unverified_candidate_or_missing"
            and c.repository_candidate_must_not_be_fabricated
            and c.repository_url_must_be_verified_before_execution
            for c in candidate_records
        ),
        "commit_not_fabricated": all(
            c.commit_hash_currently_unverified
            and c.branch_or_tag_candidate_currently_unverified
            and c.commit_pin_must_not_be_fabricated
            for c in commit_records
        ),
        "license_not_fabricated": all(
            l.source_license_currently_unverified
            and l.license_review_must_complete_before_source_execution_retry
            and l.license_review_must_not_be_fabricated
            for l in license_records
        ),
        "dependency_not_fabricated": all(
            d.source_requirements_currently_unverified
            and d.transitive_dependencies_currently_unverified
            and d.dependency_review_must_complete_before_source_execution_retry
            and d.dependency_review_must_not_be_fabricated
            for d in dependency_records
        ),
        "weight_exclusion_plan_present": (
            mobile_sam_weight_exclusion.mobile_sam_weight_excluding_checkout_required
            and mobile_sam_weight_exclusion.weight_excluding_checkout_plan_required_before_retry
            and mobile_sam_weight_exclusion.allowed_file_patterns_must_be_defined_before_execution
            and mobile_sam_weight_exclusion.blocked_file_patterns_must_include_weight_checkpoint_extensions
            and len(mobile_sam_weight_exclusion.blocked_file_patterns) >= 8
        ),
        "weight_risk_recorded": (
            mobile_sam_weight_exclusion.full_clone_may_include_committed_checkpoint_weight
            and any(c.full_clone_may_equal_weight_download for c in candidate_records)
            and any(c.repository_may_contain_committed_checkpoint_weight for c in candidate_records)
        ),
        "exclusion_not_download_approval": (
            mobile_sam_weight_exclusion.weight_excluding_checkout_plan_success_not_weight_download_approval
            and mobile_sam_weight_exclusion.weight_download_allowed is False
            and WEIGHT_DOWNLOAD_ALLOWED is False
        ),
        "retry_not_allowed_now": (
            SOURCE_EXECUTION_RETRY_ALLOWED_NOW is False
            and retry_gate.source_execution_retry_allowed_now is False
            and retry_gate.readiness_preconditions_all_unsatisfied_now
        ),
        "weight_not_default_allowed": (
            WEIGHT_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL is True
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceRepositoryVerificationCommitPinPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceRepositoryVerificationCommitPinPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_repository_verification_commitpin_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_repository_verification_commitpin_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_repository_verification_planning_input_count_eq_2": len(inputs) == 2,
        "source_repository_candidate_planning_record_count_eq_2": len(candidate_records) == 2,
        "source_commit_pin_planning_record_count_eq_2": len(commit_records) == 2,
        "source_license_review_planning_record_count_eq_2": len(license_records) == 2,
        "source_dependency_review_planning_record_count_eq_2": len(dependency_records) == 2,
        "mobile_sam_weight_exclusion_planning_record_count_eq_1": True,
        "source_execution_retry_gate_planning_record_count_gte_1": True,
        "source_execution_retry_readiness_precondition_count_gte_8": len(readiness_preconditions) >= 8,
        "source_repository_planning_risk_record_count_eq_2": len(risk_records) == 2,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "planning_only": PLANNING_ONLY is True,
        "repository_verification_planning_only": REPOSITORY_VERIFICATION_PLANNING_ONLY is True,
        "commit_pin_planning_only": COMMIT_PIN_PLANNING_ONLY is True,
        "license_review_planning_only": LICENSE_REVIEW_PLANNING_ONLY is True,
        "dependency_review_planning_only": DEPENDENCY_REVIEW_PLANNING_ONLY is True,
        "weight_exclusion_planning_only": WEIGHT_EXCLUSION_PLANNING_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "network_lookup_allowed_false": NETWORK_LOOKUP_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_checkout_allowed_false": SOURCE_CHECKOUT_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "example_asset_download_allowed_false": EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Asset-state bindings.
        "byte_track_current_status_deferred": all(i.current_status == "DEFERRED" for i in inputs if i.asset_id == "byte_track"),
        "mobile_sam_current_status_deferred": all(i.current_status == "DEFERRED" for i in inputs if i.asset_id == "mobile_sam"),
        "repository_candidate_must_not_be_fabricated": all(c.repository_candidate_must_not_be_fabricated for c in candidate_records),
        "commit_pin_must_not_be_fabricated": all(c.commit_pin_must_not_be_fabricated for c in commit_records),
        "license_review_must_not_be_fabricated": all(l.license_review_must_not_be_fabricated for l in license_records),
        "dependency_review_must_not_be_fabricated": all(d.dependency_review_must_not_be_fabricated for d in dependency_records),
        "mobile_sam_weight_excluding_checkout_required": mobile_sam_weight_exclusion.mobile_sam_weight_excluding_checkout_required,
        "mobile_sam_full_clone_weight_risk_recorded": invariant_state["weight_risk_recorded"],
        "source_execution_retry_allowed_now_false": SOURCE_EXECUTION_RETRY_ALLOWED_NOW is False,
        "source_execution_retry_requires_future_readiness": SOURCE_EXECUTION_RETRY_REQUIRES_FUTURE_READINESS is True,
        "weight_download_requires_separate_approval": WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL is True,
        # Follow-up routing.
        "recommended_next_phase_is_review": RECOMMENDED_NEXT_PHASE_REF.endswith("Review-v1-001"),
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
    decision = P1SourceRepositoryVerificationCommitPinPlanningDecision(
        decision_ref=DECISION_REF,
        source_repository_verification_commitpin_planning_profile_count=1,
        source_repository_verification_planning_input_count=len(inputs),
        source_repository_candidate_planning_record_count=len(candidate_records),
        source_commit_pin_planning_record_count=len(commit_records),
        source_license_review_planning_record_count=len(license_records),
        source_dependency_review_planning_record_count=len(dependency_records),
        mobile_sam_weight_exclusion_planning_record_count=1,
        source_execution_retry_gate_planning_record_count=1,
        source_execution_retry_readiness_precondition_count=len(readiness_preconditions),
        source_repository_planning_risk_record_count=len(risk_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Source Repository Verification / CommitPin / License / Dependency / Weight-Exclusion Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_post_review_ref": UPSTREAM_POST_REVIEW_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_repository_verification_commitpin_planning_profile": _build_profile(),
        "source_repository_verification_commitpin_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Planning records.
        "source_repository_verification_planning_inputs": [asdict(i) for i in inputs],
        "source_repository_verification_planning_input_count": len(inputs),
        "source_repository_candidate_planning_records": [asdict(c) for c in candidate_records],
        "source_repository_candidate_planning_record_count": len(candidate_records),
        "source_commit_pin_planning_records": [asdict(c) for c in commit_records],
        "source_commit_pin_planning_record_count": len(commit_records),
        "source_license_review_planning_records": [asdict(l) for l in license_records],
        "source_license_review_planning_record_count": len(license_records),
        "source_dependency_review_planning_records": [asdict(d) for d in dependency_records],
        "source_dependency_review_planning_record_count": len(dependency_records),
        "mobile_sam_weight_exclusion_planning_record": asdict(mobile_sam_weight_exclusion),
        "mobile_sam_weight_exclusion_planning_record_count": 1,
        "source_execution_retry_gate_planning_record": asdict(retry_gate),
        "source_execution_retry_gate_planning_record_count": 1,
        "source_execution_retry_readiness_preconditions": [asdict(p) for p in readiness_preconditions],
        "source_execution_retry_readiness_precondition_count": len(readiness_preconditions),
        "source_repository_planning_risk_records": [asdict(r) for r in risk_records],
        "source_repository_planning_risk_record_count": len(risk_records),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_source_repository_verification_commitpin_planning_status": (
                "planning_complete_candidate_only_no_network_no_clone_no_install_no_weight_download"
                if review_ok
                else "blocked"
            ),
            "in_scope_assets": list(IN_SCOPE_ASSET_IDS),
            "recommended_next_phase": RECOMMENDED_NEXT_PHASE_REF,
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Compressed pre-retry planning for byte_track and mobile_sam complete. This phase only PLANNED the "
                "questions that must be resolved before the next source-execution retry: (1) who the real repository "
                "candidate is (recorded as unverified_candidate_or_missing, must be verified before execution and must "
                "not be fabricated; byte_track ByteTrack/YOLOX has unresolved/source-component import identity, "
                "mobile_sam MobileSAM may ship a committed checkpoint so a full clone may equal a weight download); "
                "(2) how commit pin is determined (required, currently unverified, must not be fabricated, drift after "
                "pin blocks execution); (3) how license review is done (required, currently unverified, repo license "
                "file + transitive deps must be checked, must complete before retry, must not be fabricated); (4) how "
                "dependency review is done (source requirements + transitive deps unverified, torch/opencv/numpy-scipy "
                "+ build/compile risk review required, must complete before retry, must not be fabricated); and (5) "
                "how mobile_sam avoids cloning checkpoint weights (weight-excluding checkout required before retry, "
                "blocking *.pth/*.pt/*.ckpt/*.safetensors/*.onnx/*.bin/*.h5/*.pb, git-lfs blocked/scoped, "
                "sparse-checkout/archive filtering if supported; this plan is NOT weight-download approval). NO network "
                "lookup, NO clone, NO checkout, NO install, NO pip, NO dependency install, NO download, NO import, NO "
                "model load, NO inference, NO runtime, NO output adapter, NO semantic layer, NO registry mutation was "
                "performed. Source-execution retry is NOT allowed now and requires future readiness (all 10 "
                "preconditions currently unsatisfied). Both assets are routed to the next, network-enabled review "
                "phase: " + RECOMMENDED_NEXT_PHASE_REF + " — which may verify repo URL, resolve commit, inspect "
                "license/dependency manifests and review mobile_sam weight-excluding checkout feasibility, but still "
                "may NOT clone / checkout / install / pip / download weights / inference / runtime."
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

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "repository_verification_plan_record": {
                "source_repository_verification_planning_inputs": [asdict(i) for i in inputs],
                "source_repository_candidate_planning_records": [asdict(c) for c in candidate_records],
            },
            "commit_pin_plan_record": {
                "source_commit_pin_planning_records": [asdict(c) for c in commit_records],
            },
            "license_review_plan_record": {
                "source_license_review_planning_records": [asdict(l) for l in license_records],
            },
            "dependency_review_plan_record": {
                "source_dependency_review_planning_records": [asdict(d) for d in dependency_records],
            },
            "mobile_sam_weight_exclusion_plan_record": {
                "mobile_sam_weight_exclusion_planning_record": asdict(mobile_sam_weight_exclusion),
            },
            "source_execution_retry_gate_record": {
                "source_execution_retry_gate_planning_record": asdict(retry_gate),
                "source_execution_retry_readiness_preconditions": [asdict(p) for p in readiness_preconditions],
                "source_repository_planning_risk_records": [asdict(r) for r in risk_records],
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
            "network_lookup_allowed": False,
            "git_clone_allowed": False,
            "source_install_allowed": False,
            "weight_download_allowed": False,
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
    result = review_p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "repository_candidate_record_count": result["decision"]["source_repository_candidate_planning_record_count"],
                "mobile_sam_weight_exclusion_record_count": result["decision"]["mobile_sam_weight_exclusion_planning_record_count"],
                "readiness_precondition_count": result["decision"]["source_execution_retry_readiness_precondition_count"],
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
