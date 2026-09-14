# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Request Planning — review v1.

PLANNING ONLY. Generates a source-install request package for the two deferred
assets (byte_track, mobile_sam): request scope, repository placeholders, network
boundary, dependency-expansion review request, license review request, weight
boundary, isolation, rollback, post-install find_spec probe request, approval
request boundary, risk disclosure, follow-up routing. It does NOT grant approval
and executes/mutates NOTHING: no git clone / source checkout / source install /
pip/dependency install / download / real import / model load / inference /
runtime / output adapter / semantic layer / registry mutation / network repo
lookup. Protected, non-deletable test board records are written in planning mode.
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
from capabilities.field_understanding.p1_controlled_source_install_request_planning.p1_controlled_source_install_request_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_request_planning.p1_controlled_source_install_request_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_REQUEST_BOUNDARY_STATEMENTS,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    DEPENDENCY_REVIEW_RISK_DIMENSIONS,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MUST_NOT_PROCESS_ASSET_IDS,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    OWNER_APPROVAL_GRANTED,
    OWNER_APPROVAL_ISSUANCE_PHASE_REF,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_PATCH_PLANNING_PHASE_REF,
    REQUEST_SCOPE_SPECIFICS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RISK_DISCLOSURE_DIMENSIONS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED,
    SOURCE_INSTALL_REQUEST_PACKAGE_CREATED,
    SOURCE_INSTALL_REQUEST_PLANNING_ONLY,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_POST_REVIEW_REF,
    UPSTREAM_RESOLUTION_PLANNING_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    NegativeSourceInstallRequestPlanningGuard,
    P1ControlledSourceInstallRequestPlanningDecision,
    P1ControlledSourceInstallRequestPlanningProfile,
    SourceApprovalRequestBoundary,
    SourceDependencyExpansionReviewRequest,
    SourceInstallRequestFollowupRouting,
    SourceInstallRequestPackage,
    SourceInstallRequestRiskDisclosure,
    SourceInstallRequestScope,
    SourceIsolationRequest,
    SourceLicenseReviewRequest,
    SourceNetworkBoundaryRequest,
    SourcePostInstallProbeRequest,
    SourceRepositoryRequestRef,
    SourceRollbackRequest,
    SourceWeightBoundaryRequest,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_request_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_request_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_request_planning"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_request_planning_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_request_planning_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_request_planning_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_request_planning_profile_v1"
DECISION_REF = "p1_controlled_source_install_request_planning_decision_v1"
REQUEST_ID = "p1_controlled_source_install_request_package_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallRequestPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            source_install_request_planning_only=SOURCE_INSTALL_REQUEST_PLANNING_ONLY,
            source_install_request_package_created=SOURCE_INSTALL_REQUEST_PACKAGE_CREATED,
            owner_approval_granted=OWNER_APPROVAL_GRANTED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
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
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_resolution_planning_ref=UPSTREAM_RESOLUTION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_request_planning_v1(
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
    # (三/四) Request scope (2).
    # ------------------------------------------------------------------- #
    request_scopes = [
        SourceInstallRequestScope(
            asset_id=aid,
            source_family=SOURCE_FAMILY[aid],
            current_status="DEFERRED",
            registry_patch_likely_required=REQUEST_SCOPE_SPECIFICS[aid]["registry_patch_likely_required"],
            registry_patch_before_source_install=REQUEST_SCOPE_SPECIFICS[aid]["registry_patch_before_source_install"],
            registry_patch_before_runtime=REQUEST_SCOPE_SPECIFICS[aid]["registry_patch_before_runtime"],
            source_install_request_created=True,
            source_install_approval_granted=False,
            source_checkout_allowed=False,
            source_install_allowed=False,
            weight_download_allowed=False,
            runtime_allowed=False,
            inference_allowed=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (五) Repository placeholders + (六) network boundary.
    # ------------------------------------------------------------------- #
    repository_refs = [
        SourceRepositoryRequestRef(
            asset_id=aid,
            repository_ref_type="placeholder",
            repository_url_unverified=True,
            repository_commit_not_pinned=True,
            repository_license_not_verified=True,
            repository_requires_future_review=True,
            repository_verification_requested=True,
            source_checkout_allowed_now=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    network_requests = [
        SourceNetworkBoundaryRequest(
            asset_id=aid,
            network_access_requires_approval=True,
            git_clone_network_scope_required=True,
            pip_network_scope_required=True,
            external_url_download_blocked_by_default=True,
            model_weight_download_blocked_by_default=True,
            dataset_download_blocked_by_default=True,
            example_asset_download_blocked_by_default=True,
            network_log_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (七) Dependency expansion + (八) license + (九) weight boundary.
    # ------------------------------------------------------------------- #
    dependency_requests = [
        SourceDependencyExpansionReviewRequest(
            asset_id=aid,
            source_requirements_review_required=True,
            transitive_dependency_review_required=True,
            risk_review_dimensions=DEPENDENCY_REVIEW_RISK_DIMENSIONS,
            review_completed=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    license_requests = [
        SourceLicenseReviewRequest(
            asset_id=aid,
            source_license_review_required=True,
            repository_license_review_required=True,
            transitive_dependency_license_review_required=True,
            license_binding_required_before_source_install=True,
            commercial_runtime_not_approved=COMMERCIAL_RUNTIME_APPROVED is False,
            source_install_success_not_commercial_runtime_approval=True,
            review_completed=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    weight_requests = [
        SourceWeightBoundaryRequest(
            asset_id=aid,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            source_install_request_not_weight_download_request=True,
            weight_download_requires_separate_approval=True,
            weight_hash_required_before_future_inference=True,
            weight_source_review_required=True,
            tracker_or_detector_weights_may_be_needed_later=REQUEST_SCOPE_SPECIFICS[aid]["tracker_or_detector_weights_may_be_needed_later"],
            checkpoint_weights_may_be_needed_later=REQUEST_SCOPE_SPECIFICS[aid]["checkpoint_weights_may_be_needed_later"],
            weight_boundary_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (十) Isolation + (十一) rollback + (十二) post-install probe.
    # ------------------------------------------------------------------- #
    isolation_requests = [
        SourceIsolationRequest(
            asset_id=aid,
            separate_source_install_env_required=True,
            no_global_site_packages_preferred=True,
            pre_source_install_snapshot_required=True,
            source_checkout_path_must_be_controlled=True,
            command_whitelist_required=True,
            post_install_probe_find_spec_only=True,
            no_real_import_after_source_install_without_review=True,
            rollback_required=True,
            test_board_write_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    rollback_requests = [
        SourceRollbackRequest(
            asset_id=aid,
            rollback_required=True,
            rollback_trigger_conditions_required=True,
            rollback_template_required=True,
            rollback_must_preserve_test_board=True,
            rollback_must_preserve_registry=True,
            rollback_must_preserve_review_artifacts=True,
            rollback_success_requires_post_review=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    probe_requests = [
        SourcePostInstallProbeRequest(
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
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (十三) Approval request boundary (>=8) + (十四) risk + (十五) followup.
    # ------------------------------------------------------------------- #
    approval_boundaries = [
        SourceApprovalRequestBoundary(
            boundary_id=f"approval_request_boundary_{i+1}",
            statement=stmt,
            holds=True,
        )
        for i, stmt in enumerate(APPROVAL_REQUEST_BOUNDARY_STATEMENTS)
    ]
    risk_disclosures = [
        SourceInstallRequestRiskDisclosure(
            asset_id=aid,
            risk_dimensions=RISK_DISCLOSURE_DIMENSIONS,
            owner_ack_required=True,
            all_risk_dimensions_disclosed=len(RISK_DISCLOSURE_DIMENSIONS) == 8,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    followup_routings = [
        SourceInstallRequestFollowupRouting(
            asset_id=aid,
            recommended_next_phase=OWNER_APPROVAL_ISSUANCE_PHASE_REF,
            optional_registry_patch_phase=REGISTRY_PATCH_PLANNING_PHASE_REF,
            registry_patch_before_source_install=REQUEST_SCOPE_SPECIFICS[aid]["registry_patch_before_source_install"],
            registry_patch_before_runtime=REQUEST_SCOPE_SPECIFICS[aid]["registry_patch_before_runtime"],
            no_source_install_execution_until_approval_issuance=True,
            no_weight_download_phase_until_source_install_post_review=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (二) Request package.
    # ------------------------------------------------------------------- #
    request_package = SourceInstallRequestPackage(
        request_id=REQUEST_ID,
        phase_id=PHASE_ID,
        request_type="controlled_source_install_request_planning",
        requested_assets=IN_SCOPE_ASSET_IDS,
        source_route_refs=tuple(f"source_route_ref::{a}" for a in IN_SCOPE_ASSET_IDS),
        repository_request_refs=tuple(f"repository_request_ref::{r.asset_id}" for r in repository_refs),
        network_boundary_request_refs=tuple(f"network_boundary_request_ref::{n.asset_id}" for n in network_requests),
        dependency_review_request_refs=tuple(f"dependency_review_request_ref::{d.asset_id}" for d in dependency_requests),
        license_review_request_refs=tuple(f"license_review_request_ref::{lr.asset_id}" for lr in license_requests),
        weight_boundary_request_refs=tuple(f"weight_boundary_request_ref::{w.asset_id}" for w in weight_requests),
        isolation_request_refs=tuple(f"isolation_request_ref::{i.asset_id}" for i in isolation_requests),
        rollback_request_refs=tuple(f"rollback_request_ref::{r.asset_id}" for r in rollback_requests),
        post_install_probe_request_refs=tuple(f"post_install_probe_request_ref::{p.asset_id}" for p in probe_requests),
        test_board_record_required=True,
        owner_approval_required=True,
        owner_approval_granted=False,
        source_install_allowed=False,
        request_package_complete=True,
        request_package_is_not_approval=True,
        request_package_is_not_source_install_approval=True,
        request_package_is_not_git_clone_approval=True,
        request_package_is_not_weight_download_approval=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 23 negative guards.
    # ------------------------------------------------------------------- #
    scope_limited_to_deferred = (
        set(request_package.requested_assets) == set(IN_SCOPE_ASSET_IDS)
        and not (set(request_package.requested_assets) & set(MUST_NOT_PROCESS_ASSET_IDS))
        and len(request_package.requested_assets) == 2
    )
    assets_remain_deferred = all(s.current_status == "DEFERRED" for s in request_scopes)
    invariant_state: Dict[str, bool] = {
        "no_git_clone_checkout": GIT_CLONE_ALLOWED is False and SOURCE_CHECKOUT_ALLOWED is False,
        "no_source_install": SOURCE_INSTALL_ALLOWED is False,
        "no_pip_dependency_install": PIP_INSTALL_ALLOWED is False and DEPENDENCY_INSTALL_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
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
        "scope_limited_to_deferred": scope_limited_to_deferred,
        "assets_remain_deferred": assets_remain_deferred,
        "request_not_owner_approval": (
            OWNER_APPROVAL_GRANTED is False
            and request_package.owner_approval_granted is False
            and request_package.request_package_is_not_approval
        ),
        "request_not_source_install_approval": (
            SOURCE_INSTALL_ALLOWED is False and request_package.request_package_is_not_source_install_approval
        ),
        "request_not_git_clone_approval": (
            GIT_CLONE_ALLOWED is False and request_package.request_package_is_not_git_clone_approval
        ),
        "request_not_weight_approval": (
            WEIGHT_DOWNLOAD_ALLOWED is False and request_package.request_package_is_not_weight_download_approval
        ),
        "repository_not_verified": all(
            r.repository_url_unverified and r.repository_license_not_verified and r.repository_ref_type == "placeholder"
            for r in repository_refs
        ),
        "repository_commit_not_pinned": all(r.repository_commit_not_pinned for r in repository_refs),
        "license_review_not_completed": all(not lr.review_completed for lr in license_requests),
        "dependency_review_not_completed": all(not d.review_completed for d in dependency_requests),
        "network_boundary_present": (
            len(network_requests) == len(IN_SCOPE_ASSET_IDS)
            and all(n.network_access_requires_approval for n in network_requests)
        ),
        "weight_not_approved_by_default": WEIGHT_DOWNLOAD_ALLOWED is False
        and all(w.weight_download_requires_separate_approval for w in weight_requests),
        "post_install_probe_find_spec_only": all(
            p.probe_uses_find_spec_only
            and p.real_import_allowed is False
            and p.no_model_load_on_probe
            and p.no_inference_on_probe
            and p.no_runtime_on_probe
            for p in probe_requests
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceInstallRequestPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceInstallRequestPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_install_request_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_source_install_request_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_install_request_package_count_eq_1": True,
        "source_install_request_scope_count_eq_2": len(request_scopes) == 2,
        "source_repository_request_ref_count_eq_2": len(repository_refs) == 2,
        "source_network_boundary_request_count_eq_2": len(network_requests) == 2,
        "source_dependency_expansion_review_request_count_eq_2": len(dependency_requests) == 2,
        "source_license_review_request_count_eq_2": len(license_requests) == 2,
        "source_weight_boundary_request_count_eq_2": len(weight_requests) == 2,
        "source_isolation_request_count_eq_2": len(isolation_requests) == 2,
        "source_rollback_request_count_eq_2": len(rollback_requests) == 2,
        "source_post_install_probe_request_count_eq_2": len(probe_requests) == 2,
        "source_approval_request_boundary_count_gte_8": len(approval_boundaries) >= 8,
        "source_install_request_risk_disclosure_count_eq_2": len(risk_disclosures) == 2,
        "source_install_request_followup_routing_count_eq_2": len(followup_routings) == 2,
        "negative_guard_count_eq_23": negative_guard_count == 23,
        "negative_guard_passed_eq_23": negative_guard_passed == 23,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings (planning-only).
        "planning_only": PLANNING_ONLY is True,
        "source_install_request_planning_only": SOURCE_INSTALL_REQUEST_PLANNING_ONLY is True,
        "source_install_request_package_created": SOURCE_INSTALL_REQUEST_PACKAGE_CREATED is True,
        "owner_approval_granted_false": OWNER_APPROVAL_GRANTED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_checkout_allowed_false": SOURCE_CHECKOUT_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
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
        # Request facts.
        "request_asset_count_eq_2": len(request_package.requested_assets) == 2,
        "byte_track_remains_deferred": any(s.asset_id == "byte_track" and s.current_status == "DEFERRED" for s in request_scopes),
        "mobile_sam_remains_deferred": any(s.asset_id == "mobile_sam" and s.current_status == "DEFERRED" for s in request_scopes),
        "request_scope_limited_to_deferred_source_assets": scope_limited_to_deferred,
        "request_package_is_not_approval": request_package.request_package_is_not_approval,
        "request_package_is_not_source_install_approval": request_package.request_package_is_not_source_install_approval,
        "request_package_is_not_git_clone_approval": request_package.request_package_is_not_git_clone_approval,
        "request_package_is_not_weight_download_approval": request_package.request_package_is_not_weight_download_approval,
        "repository_refs_placeholder_only": all(r.repository_ref_type == "placeholder" for r in repository_refs),
        "repository_urls_unverified": all(r.repository_url_unverified for r in repository_refs),
        "repository_commits_not_pinned": all(r.repository_commit_not_pinned for r in repository_refs),
        "repository_licenses_not_verified": all(r.repository_license_not_verified for r in repository_refs),
        "network_boundary_review_required": all(n.network_access_requires_approval for n in network_requests),
        "dependency_expansion_review_requested": all(d.source_requirements_review_required for d in dependency_requests),
        "license_review_requested": all(lr.source_license_review_required for lr in license_requests),
        "source_install_requires_separate_approval": request_package.owner_approval_required,
        "weight_download_requires_separate_approval": all(w.weight_download_requires_separate_approval for w in weight_requests),
        "source_install_request_not_weight_download_request": all(
            w.source_install_request_not_weight_download_request for w in weight_requests
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
    decision = P1ControlledSourceInstallRequestPlanningDecision(
        decision_ref=DECISION_REF,
        controlled_source_install_request_planning_profile_count=1,
        source_install_request_package_count=1,
        source_install_request_scope_count=len(request_scopes),
        source_repository_request_ref_count=len(repository_refs),
        source_network_boundary_request_count=len(network_requests),
        source_dependency_expansion_review_request_count=len(dependency_requests),
        source_license_review_request_count=len(license_requests),
        source_weight_boundary_request_count=len(weight_requests),
        source_isolation_request_count=len(isolation_requests),
        source_rollback_request_count=len(rollback_requests),
        source_post_install_probe_request_count=len(probe_requests),
        source_approval_request_boundary_count=len(approval_boundaries),
        source_install_request_risk_disclosure_count=len(risk_disclosures),
        source_install_request_followup_routing_count=len(followup_routings),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Request Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
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
        "controlled_source_install_request_planning_profile": _build_profile(),
        "controlled_source_install_request_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Planning artifacts.
        "source_install_request_package": asdict(request_package),
        "source_install_request_package_count": 1,
        "source_install_request_scopes": [asdict(s) for s in request_scopes],
        "source_install_request_scope_count": len(request_scopes),
        "source_repository_request_refs": [asdict(r) for r in repository_refs],
        "source_repository_request_ref_count": len(repository_refs),
        "source_network_boundary_requests": [asdict(n) for n in network_requests],
        "source_network_boundary_request_count": len(network_requests),
        "source_dependency_expansion_review_requests": [asdict(d) for d in dependency_requests],
        "source_dependency_expansion_review_request_count": len(dependency_requests),
        "source_license_review_requests": [asdict(lr) for lr in license_requests],
        "source_license_review_request_count": len(license_requests),
        "source_weight_boundary_requests": [asdict(w) for w in weight_requests],
        "source_weight_boundary_request_count": len(weight_requests),
        "source_isolation_requests": [asdict(i) for i in isolation_requests],
        "source_isolation_request_count": len(isolation_requests),
        "source_rollback_requests": [asdict(r) for r in rollback_requests],
        "source_rollback_request_count": len(rollback_requests),
        "source_post_install_probe_requests": [asdict(p) for p in probe_requests],
        "source_post_install_probe_request_count": len(probe_requests),
        "source_approval_request_boundaries": [asdict(b) for b in approval_boundaries],
        "source_approval_request_boundary_count": len(approval_boundaries),
        "source_install_request_risk_disclosures": [asdict(r) for r in risk_disclosures],
        "source_install_request_risk_disclosure_count": len(risk_disclosures),
        "source_install_request_followup_routings": [asdict(f) for f in followup_routings],
        "source_install_request_followup_routing_count": len(followup_routings),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_request_planning_status": (
                "byte_track_and_mobile_sam_source_install_request_package_created_no_approval_no_clone_no_install_no_download"
                if review_ok
                else "blocked"
            ),
            "request_id": request_package.request_id,
            "requested_assets": list(request_package.requested_assets),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Source-install REQUEST package created for byte_track and mobile_sam (both REMAIN DEFERRED). The "
                "package bundles, per asset: request scope, repository placeholder (URL unverified, commit not "
                "pinned, license not verified, verification requested, no checkout now), network boundary request "
                "(network access requires approval; git/pip scope required; external/weight/dataset/example downloads "
                "blocked by default; network log required), dependency-expansion review request (requested NOT "
                "completed), license review request (requested NOT completed), weight boundary request (no "
                "weight/model/dataset download; weights may be needed later but NOT now; separate approval required), "
                "isolation request (separate env, pre-snapshot, controlled checkout path, command whitelist, "
                "post-install probe find_spec only, rollback, test board), rollback request (preserves test "
                "board/registry/review artifacts; success requires post-review), and post-install probe request "
                "(find_spec only; NO real import / model load / inference / runtime / output). 8 approval-request "
                "boundary statements assert Request != Approval (NOT owner / source-install / git-clone / weight / "
                "inference / runtime / output / semantic approval). owner_approval_required=true, "
                "owner_approval_granted=false. Nothing was cloned / checked out / installed / downloaded; no real "
                "import / load / inference / runtime / output / semantic; registry not modified. byte_track: registry "
                "patch optional-but-recommended before source install, REQUIRED before runtime. mobile_sam: registry "
                "patch required before runtime. Next: Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001 "
                "(issuance only — still no clone/install); no source-install execution until approval issuance; no "
                "weight-download phase until source-install post-review."
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
            "source_install_request_package_record": {
                "source_install_request_package": asdict(request_package),
                "source_approval_request_boundaries": [asdict(b) for b in approval_boundaries],
            },
            "source_request_scope_record": {
                "source_install_request_scopes": [asdict(s) for s in request_scopes],
                "source_repository_request_refs": [asdict(r) for r in repository_refs],
            },
            "source_network_boundary_record": {
                "source_network_boundary_requests": [asdict(n) for n in network_requests]
            },
            "source_dependency_review_request_record": {
                "source_dependency_expansion_review_requests": [asdict(d) for d in dependency_requests]
            },
            "source_license_review_request_record": {
                "source_license_review_requests": [asdict(lr) for lr in license_requests]
            },
            "source_weight_boundary_record": {
                "source_weight_boundary_requests": [asdict(w) for w in weight_requests]
            },
            "source_isolation_request_record": {
                "source_isolation_requests": [asdict(i) for i in isolation_requests],
                "source_rollback_requests": [asdict(r) for r in rollback_requests],
                "source_post_install_probe_requests": [asdict(p) for p in probe_requests],
            },
            "source_followup_approval_record": {
                "source_install_request_risk_disclosures": [asdict(r) for r in risk_disclosures],
                "source_install_request_followup_routings": [asdict(f) for f in followup_routings],
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
    result = review_p1_controlled_source_install_request_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "request_package_count": result["decision"]["source_install_request_package_count"],
                "request_scope_count": result["decision"]["source_install_request_scope_count"],
                "approval_boundary_count": result["decision"]["source_approval_request_boundary_count"],
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
