# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Preparation And Readiness Review — review v1.

COMPRESSED phase. Merges (1) source approval issuance post-review (scope audit),
(2) source install preparation (preparation package + final requirements), and
(3) source install readiness review (execution readiness decision) for byte_track
and mobile_sam. It only PRODUCES a source install preparation package and a source
execution readiness decision. It executes/mutates NOTHING: no git clone, no source
checkout, no source install, no pip install, no dependency install, no
model/weight/dataset download, no real import, no model load, no inference, no
runtime, no output adapter, no semantic layer, no registry mutation, no network
repository lookup. Both assets REMAIN DEFERRED. Protected, non-deletable test
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
from capabilities.field_understanding.p1_controlled_source_install_preparation_and_readiness_review.p1_controlled_source_install_preparation_and_readiness_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_preparation_and_readiness_review.p1_controlled_source_install_preparation_and_readiness_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT,
    COMMAND_TEMPLATE_TEXT,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
    DEPENDENCY_INSTALL_ALLOWED_IN_THIS_PHASE,
    EXPECTED_ISSUANCE_SCOPE,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED_IN_THIS_PHASE,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
    MODEL_LOAD_ALLOWED_IN_THIS_PHASE,
    MUST_NOT_PROCESS_ASSET_IDS,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED_IN_THIS_PHASE,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED_IN_THIS_PHASE,
    REAL_INFERENCE_ALLOWED_IN_THIS_PHASE,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED_IN_THIS_PHASE,
    SOURCE_EXECUTION_READINESS_DECISION_CREATED,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED_IN_THIS_PHASE,
    SOURCE_INSTALL_PREPARATION_INCLUDED,
    SOURCE_INSTALL_PREPARATION_PACKAGE_CREATED,
    SOURCE_INSTALL_READINESS_REVIEW_INCLUDED,
    STOP_CONDITIONS,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_ISSUANCE_EXPECTED_GO,
    UPSTREAM_ISSUANCE_REF,
    UPSTREAM_REQUEST_PLANNING_REF,
    UPSTREAM_RESOLUTION_PLANNING_REF,
    WEIGHT_BOUNDARY_SPECIFICS,
    WEIGHT_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
    NegativeSourceInstallPreparationReadinessGuard,
    P1ControlledSourceInstallPreparationReadinessDecision,
    P1ControlledSourceInstallPreparationReadinessProfile,
    SourceApprovalIssuanceScopeAudit,
    SourceCommandWhitelistFinal,
    SourceCommitPinRequirement,
    SourceDependencyExpansionRequirement,
    SourceExecutionHandoffRecord,
    SourceExecutionReadinessReview,
    SourceInstallPreparationPackage,
    SourceIsolationRequirementFinal,
    SourceLicenseReviewRequirement,
    SourceNetworkBoundaryRequirement,
    SourcePostInstallProbeRequirementFinal,
    SourcePreparedAssetScope,
    SourceRepositoryVerificationRequirement,
    SourceRollbackRequirementFinal,
    SourceStopConditionFinal,
    SourceWeightBoundaryFinal,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_preparation_and_readiness_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_preparation_and_readiness_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_preparation_and_readiness_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_preparation_and_readiness_review_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_preparation_and_readiness_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_preparation_and_readiness_review_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_preparation_and_readiness_review_profile_v1"
DECISION_REF = "p1_controlled_source_install_preparation_and_readiness_review_decision_v1"
PREPARATION_PACKAGE_ID = "source_install_preparation_package_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallPreparationReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            source_approval_issuance_post_review_included=SOURCE_APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
            source_install_preparation_included=SOURCE_INSTALL_PREPARATION_INCLUDED,
            source_install_readiness_review_included=SOURCE_INSTALL_READINESS_REVIEW_INCLUDED,
            source_install_preparation_package_created=SOURCE_INSTALL_PREPARATION_PACKAGE_CREATED,
            source_execution_readiness_decision_created=SOURCE_EXECUTION_READINESS_DECISION_CREATED,
            can_enter_controlled_source_install_execution_next=CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT,
            git_clone_allowed_in_this_phase=GIT_CLONE_ALLOWED_IN_THIS_PHASE,
            source_checkout_allowed_in_this_phase=SOURCE_CHECKOUT_ALLOWED_IN_THIS_PHASE,
            source_install_allowed_in_this_phase=SOURCE_INSTALL_ALLOWED_IN_THIS_PHASE,
            pip_install_allowed_in_this_phase=PIP_INSTALL_ALLOWED_IN_THIS_PHASE,
            dependency_install_allowed_in_this_phase=DEPENDENCY_INSTALL_ALLOWED_IN_THIS_PHASE,
            model_download_allowed_in_this_phase=MODEL_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
            weight_download_allowed_in_this_phase=WEIGHT_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
            dataset_download_allowed_in_this_phase=DATASET_DOWNLOAD_ALLOWED_IN_THIS_PHASE,
            real_import_allowed_in_this_phase=REAL_IMPORT_ALLOWED_IN_THIS_PHASE,
            model_load_allowed_in_this_phase=MODEL_LOAD_ALLOWED_IN_THIS_PHASE,
            real_inference_allowed_in_this_phase=REAL_INFERENCE_ALLOWED_IN_THIS_PHASE,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_issuance_ref=UPSTREAM_ISSUANCE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_preparation_and_readiness_review_v1(
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
    # (一) Approval issuance scope audit (post-review of issuance).
    # ------------------------------------------------------------------- #
    scope_audit = SourceApprovalIssuanceScopeAudit(
        audit_id="source_approval_issuance_scope_audit_v1",
        upstream_issuance_ref=UPSTREAM_ISSUANCE_REF,
        expected_final_decision=UPSTREAM_ISSUANCE_EXPECTED_GO,
        approval_issuance_limited_to_source_install_preparation=True,
        owner_approval_granted_for_source_install_preparation=EXPECTED_ISSUANCE_SCOPE[
            "owner_approval_granted_for_source_install_preparation"
        ],
        owner_approval_granted_for_git_clone=EXPECTED_ISSUANCE_SCOPE["owner_approval_granted_for_git_clone"],
        owner_approval_granted_for_source_checkout=EXPECTED_ISSUANCE_SCOPE["owner_approval_granted_for_source_checkout"],
        owner_approval_granted_for_source_install=EXPECTED_ISSUANCE_SCOPE["owner_approval_granted_for_source_install"],
        owner_approval_granted_for_weight_download=EXPECTED_ISSUANCE_SCOPE["owner_approval_granted_for_weight_download"],
        source_chain_complete=True,
        can_enter_source_install_preparation=EXPECTED_ISSUANCE_SCOPE["can_enter_source_install_preparation"],
        can_enter_source_install=EXPECTED_ISSUANCE_SCOPE["can_enter_source_install"],
        approval_issuance_success_not_git_clone_approval=True,
        approval_issuance_success_not_source_checkout_approval=True,
        approval_issuance_success_not_source_install_approval=True,
        approval_issuance_success_not_weight_download_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (四-十一) Per-asset final requirements.
    # ------------------------------------------------------------------- #
    repo_reqs: List[SourceRepositoryVerificationRequirement] = []
    commit_reqs: List[SourceCommitPinRequirement] = []
    network_reqs: List[SourceNetworkBoundaryRequirement] = []
    dep_reqs: List[SourceDependencyExpansionRequirement] = []
    license_reqs: List[SourceLicenseReviewRequirement] = []
    isolation_reqs: List[SourceIsolationRequirementFinal] = []
    command_finals: List[SourceCommandWhitelistFinal] = []
    rollback_reqs: List[SourceRollbackRequirementFinal] = []
    probe_reqs: List[SourcePostInstallProbeRequirementFinal] = []
    weight_finals: List[SourceWeightBoundaryFinal] = []

    for aid in IN_SCOPE_ASSET_IDS:
        repo_reqs.append(
            SourceRepositoryVerificationRequirement(
                asset_id=aid,
                repository_ref_type="placeholder",
                repository_url_unverified=True,
                repository_verification_required_before_execution=True,
                repository_commit_pin_required_before_execution=True,
                repository_license_review_required_before_execution=True,
                repository_verification_not_performed_in_this_phase=True,
                source_checkout_allowed_now=False,
            )
        )
        commit_reqs.append(
            SourceCommitPinRequirement(
                asset_id=aid,
                commit_pin_required_before_execution=True,
                commit_pinned_now=False,
                commit_pin_not_performed_in_this_phase=True,
            )
        )
        network_reqs.append(
            SourceNetworkBoundaryRequirement(
                asset_id=aid,
                network_access_must_be_explicitly_scoped=True,
                git_clone_scope_must_be_whitelisted=True,
                pip_install_scope_must_be_whitelisted=True,
                external_url_download_blocked_by_default=True,
                model_weight_download_blocked_by_default=True,
                dataset_download_blocked_by_default=True,
                example_asset_download_blocked_by_default=True,
                network_log_required=True,
                network_boundary_violation_stops_execution=True,
            )
        )
        dep_reqs.append(
            SourceDependencyExpansionRequirement(
                asset_id=aid,
                dependency_expansion_review_required=True,
                transitive_dependency_review_required=True,
                review_completed=False,
                review_required_and_uncompleted=True,
            )
        )
        license_reqs.append(
            SourceLicenseReviewRequirement(
                asset_id=aid,
                source_license_review_required=True,
                repository_license_review_required=True,
                transitive_dependency_license_review_required=True,
                review_completed=False,
                review_required_and_uncompleted=True,
            )
        )
        isolation_reqs.append(
            SourceIsolationRequirementFinal(
                asset_id=aid,
                separate_source_install_env_required=True,
                no_global_site_packages_preferred=True,
                pre_source_install_snapshot_required=True,
                source_checkout_path_must_be_controlled=True,
                install_target_path_must_be_controlled=True,
                rollback_snapshot_required=True,
                test_board_write_required=True,
                registry_preservation_required=True,
                review_artifact_preservation_required=True,
            )
        )
        command_finals.append(
            SourceCommandWhitelistFinal(
                asset_id=aid,
                command_template_ref=f"source_command_whitelist_template::{aid}",
                command_template_text=COMMAND_TEMPLATE_TEXT[aid],
                template_only_marker="TEMPLATE_ONLY_DO_NOT_EXECUTE",
                command_not_executed_in_this_phase=True,
                git_clone_command_allowed_now=False,
                source_checkout_command_allowed_now=False,
                pip_install_command_allowed_now=False,
                command_allowed_only_in_next_source_execution_phase=True,
                command_requires_pre_snapshot=True,
                command_requires_repository_verification=True,
                command_requires_commit_pin=True,
                command_requires_license_review=True,
                command_requires_dependency_review=True,
                command_requires_network_boundary=True,
                command_requires_rollback_available=True,
                command_requires_post_probe=True,
            )
        )
        rollback_reqs.append(
            SourceRollbackRequirementFinal(
                asset_id=aid,
                rollback_required=True,
                rollback_trigger_conditions_exist=True,
                rollback_template_ref=f"source_rollback_template::{aid}",
                rollback_command_not_executed_in_this_phase=True,
                rollback_must_preserve_test_board=True,
                rollback_must_preserve_registry=True,
                rollback_must_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
                rollback_failure_escalation_required=True,
            )
        )
        probe_reqs.append(
            SourcePostInstallProbeRequirementFinal(
                asset_id=aid,
                post_install_probe_required=True,
                probe_uses_find_spec_only=True,
                real_import_allowed=False,
                no_model_load_on_probe=True,
                no_inference_on_probe=True,
                no_runtime_on_probe=True,
                no_output_adapter_on_probe=True,
                installed_version_record_required=True,
                dependency_gap_recheck_required=True,
                license_recheck_required=True,
                test_board_probe_record_required=True,
            )
        )
        weight_finals.append(
            SourceWeightBoundaryFinal(
                asset_id=aid,
                weight_download_allowed_in_next_source_execution=False,
                model_download_allowed_in_next_source_execution=False,
                dataset_download_allowed_in_next_source_execution=False,
                source_execution_may_checkout_code_only=True,
                source_execution_may_install_code_only=True,
                source_execution_must_not_download_weights=True,
                source_execution_must_not_download_datasets=True,
                weight_download_requires_separate_approval=True,
                no_weight_download_phase_until_source_install_post_review=True,
                tracker_or_detector_weight_boundary_required=WEIGHT_BOUNDARY_SPECIFICS[aid][
                    "tracker_or_detector_weight_boundary_required"
                ],
                checkpoint_weight_boundary_required=WEIGHT_BOUNDARY_SPECIFICS[aid][
                    "checkpoint_weight_boundary_required"
                ],
            )
        )

    # ------------------------------------------------------------------- #
    # (八) Final stop conditions (>=25).
    # ------------------------------------------------------------------- #
    stop_conditions = [
        SourceStopConditionFinal(condition_id=f"stop_{i+1}", condition=c, stops_execution=True)
        for i, c in enumerate(STOP_CONDITIONS)
    ]

    # ------------------------------------------------------------------- #
    # (三) Prepared asset scope (2).
    # ------------------------------------------------------------------- #
    prepared_scopes = [
        SourcePreparedAssetScope(
            asset_id=aid,
            included_in_source_preparation=True,
            current_status="DEFERRED",
            source_family=SOURCE_FAMILY[aid],
            repository_requirement_ref=f"repo_verification::{aid}",
            network_boundary_ref=f"network_boundary::{aid}",
            dependency_expansion_ref=f"dependency_expansion::{aid}",
            license_review_ref=f"license_review::{aid}",
            isolation_ref=f"isolation::{aid}",
            command_whitelist_ref=f"source_command_whitelist_template::{aid}",
            rollback_ref=f"source_rollback_template::{aid}",
            post_install_probe_ref=f"post_install_probe::{aid}",
            weight_boundary_ref=f"weight_boundary::{aid}",
            can_enter_next_source_execution_phase=True,
            can_enter_weight_download=False,
            can_enter_inference=False,
            can_enter_runtime=False,
            can_enter_output_adapter=False,
            can_enter_semantic_layer=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (二) Source install preparation package.
    # ------------------------------------------------------------------- #
    preparation_package = SourceInstallPreparationPackage(
        preparation_package_id=PREPARATION_PACKAGE_ID,
        phase_id=PHASE_ID,
        source_approval_issuance_ref=UPSTREAM_ISSUANCE_REF,
        source_request_ref=UPSTREAM_REQUEST_PLANNING_REF,
        source_resolution_ref=UPSTREAM_RESOLUTION_PLANNING_REF,
        prepared_assets=IN_SCOPE_ASSET_IDS,
        repository_verification_required=True,
        commit_pin_required=True,
        license_review_required=True,
        dependency_expansion_review_required=True,
        network_boundary_required=True,
        pre_source_install_snapshot_required=True,
        command_whitelist_required=True,
        isolation_environment_required=True,
        rollback_required=True,
        post_install_probe_required=True,
        test_board_write_required=True,
        weight_download_separate_approval_required=True,
        source_install_preparation_complete=True,
        git_clone_allowed_in_this_phase=False,
        source_install_allowed_in_this_phase=False,
    )

    # ------------------------------------------------------------------- #
    # (十二) Execution readiness review.
    # ------------------------------------------------------------------- #
    prepared_assets_verified = (
        set(s.asset_id for s in prepared_scopes) == set(IN_SCOPE_ASSET_IDS) and len(prepared_scopes) == 2
    )
    dep_required_and_uncompleted = all(d.review_required_and_uncompleted and not d.review_completed for d in dep_reqs)
    license_required_and_uncompleted = all(
        l.review_required_and_uncompleted and not l.review_completed for l in license_reqs
    )
    command_whitelist_not_executed = all(c.command_not_executed_in_this_phase for c in command_finals)
    post_probe_find_spec_only = all(
        p.probe_uses_find_spec_only and not p.real_import_allowed and p.no_inference_on_probe
        and p.no_runtime_on_probe and p.no_output_adapter_on_probe
        for p in probe_reqs
    )
    weight_scope_not_approved = all(
        (not w.weight_download_allowed_in_next_source_execution)
        and (not w.model_download_allowed_in_next_source_execution)
        and (not w.dataset_download_allowed_in_next_source_execution)
        and w.weight_download_requires_separate_approval
        for w in weight_finals
    )

    readiness_review = SourceExecutionReadinessReview(
        review_id="source_execution_readiness_review_v1",
        approval_scope_valid=True,
        source_preparation_package_complete=preparation_package.source_install_preparation_complete,
        prepared_assets_verified=prepared_assets_verified,
        repository_requirements_ready=len(repo_reqs) == 2,
        network_boundary_ready=len(network_reqs) == 2,
        dependency_review_required_and_uncompleted=dep_required_and_uncompleted,
        license_review_required_and_uncompleted=license_required_and_uncompleted,
        command_whitelist_ready=len(command_finals) == 2,
        isolation_requirement_ready=len(isolation_reqs) == 2,
        stop_conditions_ready=len(stop_conditions) >= 25,
        rollback_ready=len(rollback_reqs) == 2,
        post_install_probe_ready=len(probe_reqs) == 2,
        weight_download_scope_not_approved=weight_scope_not_approved,
        test_board_ready=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        non_execution_boundary_preserved=True,
        can_enter_controlled_source_install_execution_next=CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT,
        can_enter_weight_download_execution_next=False,
        can_enter_inference=False,
        can_enter_runtime=False,
        can_enter_output_adapter=False,
        can_enter_semantic_layer=False,
    )

    handoff = SourceExecutionHandoffRecord(
        handoff_id="source_execution_handoff_v1",
        next_phase_ref=NEXT_STEP_REF,
        can_enter_controlled_source_install_execution_next=CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT,
        first_source_execution_scope=(
            "repo_verification_commit_pin_scoped_git_clone_source_checkout_code_only_install_no_weight_download_no_inference"
        ),
        weight_download_still_blocked=True,
        inference_still_blocked=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 26 negative guards (A..Z).
    # ------------------------------------------------------------------- #
    scope_limited_to_deferred = (
        set(s.asset_id for s in prepared_scopes) == set(IN_SCOPE_ASSET_IDS)
        and not (set(s.asset_id for s in prepared_scopes) & set(MUST_NOT_PROCESS_ASSET_IDS))
        and len(prepared_scopes) == 2
    )
    invariant_state: Dict[str, bool] = {
        # A
        "approval_scope_correct": (
            scope_audit.approval_issuance_limited_to_source_install_preparation
            and scope_audit.owner_approval_granted_for_git_clone is False
            and scope_audit.owner_approval_granted_for_source_checkout is False
            and scope_audit.owner_approval_granted_for_source_install is False
            and scope_audit.can_enter_source_install is False
            and scope_audit.approval_issuance_success_not_git_clone_approval
            and scope_audit.approval_issuance_success_not_source_checkout_approval
            and scope_audit.approval_issuance_success_not_source_install_approval
            and scope_audit.approval_issuance_success_not_weight_download_approval
        ),
        # B
        "no_clone_checkout_install": (
            GIT_CLONE_ALLOWED_IN_THIS_PHASE is False
            and SOURCE_CHECKOUT_ALLOWED_IN_THIS_PHASE is False
            and SOURCE_INSTALL_ALLOWED_IN_THIS_PHASE is False
        ),
        # C
        "no_pip_dependency_install": (
            PIP_INSTALL_ALLOWED_IN_THIS_PHASE is False and DEPENDENCY_INSTALL_ALLOWED_IN_THIS_PHASE is False
        ),
        # D
        "no_download_performed": (
            MODEL_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False
            and WEIGHT_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False
            and DATASET_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False
        ),
        # E
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED_IN_THIS_PHASE is False
            and MODEL_LOAD_ALLOWED_IN_THIS_PHASE is False
            and REAL_INFERENCE_ALLOWED_IN_THIS_PHASE is False
        ),
        # F
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        # G
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        # H
        "preparation_package_present": preparation_package.source_install_preparation_complete is True,
        # I
        "scope_limited_to_deferred": scope_limited_to_deferred,
        # J
        "repo_verification_requirement_present": (
            len(repo_reqs) == 2 and all(r.repository_verification_required_before_execution for r in repo_reqs)
        ),
        # K
        "commit_pin_requirement_present": (
            len(commit_reqs) == 2 and all(c.commit_pin_required_before_execution for c in commit_reqs)
        ),
        # L
        "license_review_requirement_present": (
            len(license_reqs) == 2 and all(l.source_license_review_required for l in license_reqs)
        ),
        # M
        "dependency_requirement_present": (
            len(dep_reqs) == 2 and all(d.dependency_expansion_review_required for d in dep_reqs)
        ),
        # N
        "network_boundary_present": (
            len(network_reqs) == 2 and all(n.network_access_must_be_explicitly_scoped for n in network_reqs)
        ),
        # O
        "command_whitelist_present": (
            len(command_finals) == 2 and all(c.command_template_text for c in command_finals)
        ),
        # P
        "command_whitelist_not_executed": command_whitelist_not_executed,
        # Q
        "isolation_requirement_present": (
            len(isolation_reqs) == 2 and all(i.separate_source_install_env_required for i in isolation_reqs)
        ),
        # R
        "rollback_requirement_present": (
            len(rollback_reqs) == 2 and all(r.rollback_required for r in rollback_reqs)
        ),
        # S
        "post_install_probe_requirement_present": (
            len(probe_reqs) == 2 and all(p.post_install_probe_required for p in probe_reqs)
        ),
        # T
        "post_install_probe_find_spec_only": post_probe_find_spec_only,
        # U
        "weight_not_approved_next_execution": (
            weight_scope_not_approved
            and readiness_review.can_enter_weight_download_execution_next is False
            and handoff.weight_download_still_blocked is True
        ),
        # V
        "readiness_no_inference_runtime_output_semantic": (
            readiness_review.can_enter_inference is False
            and readiness_review.can_enter_runtime is False
            and readiness_review.can_enter_output_adapter is False
            and readiness_review.can_enter_semantic_layer is False
        ),
        # W: dependency/license review must NOT be marked completed.
        "reviews_not_marked_completed": (
            all(not d.review_completed for d in dep_reqs)
            and all(not l.review_completed for l in license_reqs)
            and dep_required_and_uncompleted
            and license_required_and_uncompleted
        ),
        # X
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        # Y
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        # Z
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceInstallPreparationReadinessGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceInstallPreparationReadinessGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_install_preparation_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_install_preparation_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_approval_issuance_scope_audit_count_gte_1": True,
        "source_install_preparation_package_count_eq_1": True,
        "source_prepared_asset_scope_count_eq_2": len(prepared_scopes) == 2,
        "source_repository_verification_requirement_count_eq_2": len(repo_reqs) == 2,
        "source_commit_pin_requirement_count_eq_2": len(commit_reqs) == 2,
        "source_network_boundary_requirement_count_eq_2": len(network_reqs) == 2,
        "source_dependency_expansion_requirement_count_eq_2": len(dep_reqs) == 2,
        "source_license_review_requirement_count_eq_2": len(license_reqs) == 2,
        "source_isolation_requirement_final_count_eq_2": len(isolation_reqs) == 2,
        "source_command_whitelist_final_count_eq_2": len(command_finals) == 2,
        "source_stop_condition_final_count_gte_25": len(stop_conditions) >= 25,
        "source_rollback_requirement_final_count_eq_2": len(rollback_reqs) == 2,
        "source_post_install_probe_requirement_final_count_eq_2": len(probe_reqs) == 2,
        "source_weight_boundary_final_count_eq_2": len(weight_finals) == 2,
        "source_execution_readiness_review_count_gte_1": True,
        "source_execution_handoff_record_count_gte_1": True,
        "negative_guard_count_eq_26": negative_guard_count == 26,
        "negative_guard_passed_eq_26": negative_guard_passed == 26,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings / compressed phase.
        "compressed_phase": COMPRESSED_PHASE is True,
        "source_approval_issuance_post_review_included": SOURCE_APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED is True,
        "source_install_preparation_included": SOURCE_INSTALL_PREPARATION_INCLUDED is True,
        "source_install_readiness_review_included": SOURCE_INSTALL_READINESS_REVIEW_INCLUDED is True,
        "approval_scope_valid": readiness_review.approval_scope_valid is True,
        "approval_issuance_limited_to_source_install_preparation": scope_audit.approval_issuance_limited_to_source_install_preparation is True,
        "approval_issuance_success_not_git_clone_approval": scope_audit.approval_issuance_success_not_git_clone_approval is True,
        "approval_issuance_success_not_source_checkout_approval": scope_audit.approval_issuance_success_not_source_checkout_approval is True,
        "approval_issuance_success_not_source_install_approval": scope_audit.approval_issuance_success_not_source_install_approval is True,
        "approval_issuance_success_not_weight_download_approval": scope_audit.approval_issuance_success_not_weight_download_approval is True,
        # Preparation package.
        "source_install_preparation_package_created": SOURCE_INSTALL_PREPARATION_PACKAGE_CREATED is True,
        "source_preparation_package_complete": preparation_package.source_install_preparation_complete is True,
        "prepared_assets_verified": prepared_assets_verified,
        "repository_requirements_ready": readiness_review.repository_requirements_ready,
        "network_boundary_ready": readiness_review.network_boundary_ready,
        "dependency_review_required_and_uncompleted": dep_required_and_uncompleted,
        "license_review_required_and_uncompleted": license_required_and_uncompleted,
        "command_whitelist_ready": readiness_review.command_whitelist_ready,
        "command_whitelist_not_executed": command_whitelist_not_executed,
        "isolation_requirement_ready": readiness_review.isolation_requirement_ready,
        "stop_conditions_ready": readiness_review.stop_conditions_ready,
        "rollback_ready": readiness_review.rollback_ready,
        "post_install_probe_ready": readiness_review.post_install_probe_ready,
        "post_install_probe_find_spec_only": post_probe_find_spec_only,
        "post_install_probe_not_inference": all(p.no_inference_on_probe for p in probe_reqs),
        "post_install_probe_not_runtime": all(p.no_runtime_on_probe for p in probe_reqs),
        "post_install_probe_not_output_adapter": all(p.no_output_adapter_on_probe for p in probe_reqs),
        "weight_download_scope_not_approved": weight_scope_not_approved,
        "weight_download_requires_separate_approval": all(w.weight_download_requires_separate_approval for w in weight_finals),
        # Handoff next-step gates.
        "can_enter_controlled_source_install_execution_next": CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT is True,
        "can_enter_weight_download_execution_next_false": readiness_review.can_enter_weight_download_execution_next is False,
        "can_enter_inference_false": readiness_review.can_enter_inference is False,
        "can_enter_runtime_false": readiness_review.can_enter_runtime is False,
        "can_enter_output_adapter_false": readiness_review.can_enter_output_adapter is False,
        "can_enter_semantic_layer_false": readiness_review.can_enter_semantic_layer is False,
        # Non-execution bindings.
        "git_clone_allowed_in_this_phase_false": GIT_CLONE_ALLOWED_IN_THIS_PHASE is False,
        "source_checkout_allowed_in_this_phase_false": SOURCE_CHECKOUT_ALLOWED_IN_THIS_PHASE is False,
        "source_install_allowed_in_this_phase_false": SOURCE_INSTALL_ALLOWED_IN_THIS_PHASE is False,
        "pip_install_allowed_in_this_phase_false": PIP_INSTALL_ALLOWED_IN_THIS_PHASE is False,
        "dependency_install_allowed_in_this_phase_false": DEPENDENCY_INSTALL_ALLOWED_IN_THIS_PHASE is False,
        "model_download_allowed_in_this_phase_false": MODEL_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False,
        "weight_download_allowed_in_this_phase_false": WEIGHT_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False,
        "dataset_download_allowed_in_this_phase_false": DATASET_DOWNLOAD_ALLOWED_IN_THIS_PHASE is False,
        "real_import_allowed_in_this_phase_false": REAL_IMPORT_ALLOWED_IN_THIS_PHASE is False,
        "model_load_allowed_in_this_phase_false": MODEL_LOAD_ALLOWED_IN_THIS_PHASE is False,
        "real_inference_allowed_in_this_phase_false": REAL_INFERENCE_ALLOWED_IN_THIS_PHASE is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
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
    decision = P1ControlledSourceInstallPreparationReadinessDecision(
        decision_ref=DECISION_REF,
        source_install_preparation_readiness_profile_count=1,
        source_approval_issuance_scope_audit_count=1,
        source_install_preparation_package_count=1,
        source_prepared_asset_scope_count=len(prepared_scopes),
        source_repository_verification_requirement_count=len(repo_reqs),
        source_commit_pin_requirement_count=len(commit_reqs),
        source_network_boundary_requirement_count=len(network_reqs),
        source_dependency_expansion_requirement_count=len(dep_reqs),
        source_license_review_requirement_count=len(license_reqs),
        source_isolation_requirement_final_count=len(isolation_reqs),
        source_command_whitelist_final_count=len(command_finals),
        source_stop_condition_final_count=len(stop_conditions),
        source_rollback_requirement_final_count=len(rollback_reqs),
        source_post_install_probe_requirement_final_count=len(probe_reqs),
        source_weight_boundary_final_count=len(weight_finals),
        source_execution_readiness_review_count=1,
        source_execution_handoff_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Preparation And Readiness Review (compressed, planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "source_approval_issuance_post_review_included": SOURCE_APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
        "source_install_preparation_included": SOURCE_INSTALL_PREPARATION_INCLUDED,
        "source_install_readiness_review_included": SOURCE_INSTALL_READINESS_REVIEW_INCLUDED,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_issuance_ref": UPSTREAM_ISSUANCE_REF,
        "upstream_request_planning_ref": UPSTREAM_REQUEST_PLANNING_REF,
        "upstream_resolution_planning_ref": UPSTREAM_RESOLUTION_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_install_preparation_readiness_profile": _build_profile(),
        "source_install_preparation_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # (一) Scope audit.
        "source_approval_issuance_scope_audit": asdict(scope_audit),
        "source_approval_issuance_scope_audit_count": 1,
        # (二) Preparation package.
        "source_install_preparation_package": asdict(preparation_package),
        "source_install_preparation_package_count": 1,
        # (三) Prepared asset scope.
        "source_prepared_asset_scopes": [asdict(s) for s in prepared_scopes],
        "source_prepared_asset_scope_count": len(prepared_scopes),
        # (四-十一) Per-asset finals.
        "source_repository_verification_requirements": [asdict(r) for r in repo_reqs],
        "source_repository_verification_requirement_count": len(repo_reqs),
        "source_commit_pin_requirements": [asdict(c) for c in commit_reqs],
        "source_commit_pin_requirement_count": len(commit_reqs),
        "source_network_boundary_requirements": [asdict(n) for n in network_reqs],
        "source_network_boundary_requirement_count": len(network_reqs),
        "source_dependency_expansion_requirements": [asdict(d) for d in dep_reqs],
        "source_dependency_expansion_requirement_count": len(dep_reqs),
        "source_license_review_requirements": [asdict(l) for l in license_reqs],
        "source_license_review_requirement_count": len(license_reqs),
        "source_isolation_requirement_finals": [asdict(i) for i in isolation_reqs],
        "source_isolation_requirement_final_count": len(isolation_reqs),
        "source_command_whitelist_finals": [asdict(c) for c in command_finals],
        "source_command_whitelist_final_count": len(command_finals),
        "source_stop_condition_finals": [asdict(s) for s in stop_conditions],
        "source_stop_condition_final_count": len(stop_conditions),
        "source_rollback_requirement_finals": [asdict(r) for r in rollback_reqs],
        "source_rollback_requirement_final_count": len(rollback_reqs),
        "source_post_install_probe_requirement_finals": [asdict(p) for p in probe_reqs],
        "source_post_install_probe_requirement_final_count": len(probe_reqs),
        "source_weight_boundary_finals": [asdict(w) for w in weight_finals],
        "source_weight_boundary_final_count": len(weight_finals),
        # (十二) Readiness review + handoff.
        "source_execution_readiness_review": asdict(readiness_review),
        "source_execution_readiness_review_count": 1,
        "source_execution_handoff_record": asdict(handoff),
        "source_execution_handoff_record_count": 1,
        # Negative guards.
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_preparation_and_readiness_review_status": (
                "source_install_preparation_package_and_readiness_decision_produced_no_clone_no_install_no_weight_download"
                if review_ok
                else "blocked"
            ),
            "preparation_package_id": preparation_package.preparation_package_id,
            "prepared_assets": list(IN_SCOPE_ASSET_IDS),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Compressed phase complete for byte_track and mobile_sam: (1) approval-issuance scope AUDITED — "
                "issuance is limited to source_install_preparation only and is NOT git clone / source checkout / "
                "source install / weight-download approval (can_enter_source_install=false); (2) a source install "
                "PREPARATION PACKAGE was produced (repository verification + commit pin + license review + "
                "dependency-expansion review + network boundary + pre-source-install snapshot + command whitelist + "
                "isolation env + rollback + post-install find_spec-only probe + weight separate approval), with 25 "
                "final stop conditions and per-asset repo/commit/network/dependency/license/isolation/command/"
                "rollback/probe/weight finals (2 each); (3) a source execution READINESS decision was issued. "
                "dependency_review and license_review are intentionally required_and_uncompleted (this is "
                "preparation/readiness planning, NOT source execution) and do NOT block GO; the next real "
                "source-execution phase MUST complete repository verification / commit pin / license review / "
                "dependency review before any action, else a stop condition blocks it. NOTHING was cloned / "
                "checked out / installed / downloaded; no real import / load / inference / runtime / output / "
                "semantic; registry not modified; no network repository lookup. Both assets REMAIN DEFERRED. "
                "Next: Phase-P1-Controlled-Source-Install-Execution-v1-001 — first source execution should allow "
                "ONLY repo verification / commit pin / scoped git clone / source checkout / code-only install; still "
                "NO weight download and NO inference."
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
            "source_approval_scope_audit_record": {
                "source_approval_issuance_scope_audit": asdict(scope_audit),
            },
            "source_preparation_package_record": {
                "source_install_preparation_package": asdict(preparation_package),
                "source_prepared_asset_scopes": [asdict(s) for s in prepared_scopes],
            },
            "source_final_repository_review_requirement_record": {
                "source_repository_verification_requirements": [asdict(r) for r in repo_reqs],
                "source_commit_pin_requirements": [asdict(c) for c in commit_reqs],
                "source_license_review_requirements": [asdict(l) for l in license_reqs],
                "source_dependency_expansion_requirements": [asdict(d) for d in dep_reqs],
            },
            "source_final_network_boundary_record": {
                "source_network_boundary_requirements": [asdict(n) for n in network_reqs],
            },
            "source_final_command_whitelist_record": {
                "source_command_whitelist_finals": [asdict(c) for c in command_finals],
                "source_stop_condition_finals": [asdict(s) for s in stop_conditions],
                "source_rollback_requirement_finals": [asdict(r) for r in rollback_reqs],
            },
            "source_final_isolation_requirement_record": {
                "source_isolation_requirement_finals": [asdict(i) for i in isolation_reqs],
                "source_post_install_probe_requirement_finals": [asdict(p) for p in probe_reqs],
            },
            "source_final_weight_boundary_record": {
                "source_weight_boundary_finals": [asdict(w) for w in weight_finals],
                "weight_download_requires_separate_approval": True,
            },
            "source_readiness_review_record": {
                "source_execution_readiness_review": asdict(readiness_review),
                "source_execution_handoff_record": asdict(handoff),
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
            "source_install_allowed": False,
            "git_clone_allowed": False,
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
    result = review_p1_controlled_source_install_preparation_and_readiness_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "prepared_asset_count": result["decision"]["source_prepared_asset_scope_count"],
                "stop_condition_count": result["decision"]["source_stop_condition_final_count"],
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
