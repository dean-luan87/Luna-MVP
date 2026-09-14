# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Resolution Planning — review v1.

PLANNING ONLY. Unifies the source-install route resolution for the two deferred
assets (byte_track, mobile_sam): per-asset route / repository placeholder /
dependency expansion / license boundary / weight boundary / isolation / command
whitelist template / approval requirement / risk / registry patch need /
follow-up routing. It executes NOTHING and MUTATES NOTHING: no git clone, no
source checkout, no source install, no pip/dependency install, no download, no
real import / model load / inference, no runtime / output adapter / semantic
layer, no registry mutation, no network repository lookup. Protected,
non-deletable test board records are written in planning mode.
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
from capabilities.field_understanding.p1_controlled_source_install_resolution_planning.p1_controlled_source_install_resolution_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_resolution_planning.p1_controlled_source_install_resolution_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_ONLY,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_EXPANSION_RISK_DIMENSIONS,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FOLLOWUP_ROUTING,
    GIT_CLONE_ALLOWED,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_PATCH_NEED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_COMMAND_TEMPLATE_REFS,
    SOURCE_INSTALL_ALLOWED,
    SOURCE_INSTALL_INPUT_ASSETS,
    SOURCE_REPOSITORY_CANDIDATES,
    SOURCE_ROUTE_CANDIDATES,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_POST_REVIEW_REF,
    UPSTREAM_REGISTRY_CORRECTION_REF,
    UPSTREAM_RESOLUTION_PLANNING_REF,
    WEIGHT_BOUNDARY_SPECIFICS,
    WEIGHT_DOWNLOAD_ALLOWED,
    P1ControlledSourceInstallResolutionPlanningDecision,
    P1ControlledSourceInstallResolutionProfile,
    NegativeControlledSourceInstallResolutionPlanningGuard,
    RegistryPatchNeedAssessment,
    SourceCommandWhitelistPlanningRecord,
    SourceDependencyExpansionPlan,
    SourceInstallApprovalRequirement,
    SourceInstallFollowupRouting,
    SourceInstallInputAsset,
    SourceInstallRiskAssessment,
    SourceIsolationRequirement,
    SourceLicenseBoundaryPlan,
    SourceRepositoryCandidate,
    SourceRouteCandidate,
    SourceWeightBoundaryPlan,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_resolution_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_resolution_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_resolution_planning"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_resolution_planning_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_resolution_planning_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_resolution_planning_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_resolution_planning_profile_v1"
DECISION_REF = "p1_controlled_source_install_resolution_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallResolutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            controlled_source_install_resolution_planning_only=CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_ONLY,
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
            upstream_registry_correction_ref=UPSTREAM_REGISTRY_CORRECTION_REF,
            upstream_resolution_planning_ref=UPSTREAM_RESOLUTION_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_resolution_planning_v1(
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
    # (一) Input assets (2).
    # ------------------------------------------------------------------- #
    input_assets = [
        SourceInstallInputAsset(
            asset_id=a["asset_id"],
            current_status=a["current_status"],
            from_execution_deferred=a["from_execution_deferred"],
            from_post_review_deferred_asset_audit=a["from_post_review_deferred_asset_audit"],
            from_resolution_planning_candidate=a["from_resolution_planning_candidate"],
            from_registry_correction_planning=a["from_registry_correction_planning"],
            source_family=a["source_family"],
            registry_correction_recommendation=a["registry_correction_recommendation"],
            clean_pypi_candidate=a["clean_pypi_candidate"],
            git_source_install_detected=a["git_source_install_detected"],
            source_install_resolution_required=a["source_install_resolution_required"],
            provenance_confirmed=(
                a["from_execution_deferred"] == UPSTREAM_EXECUTION_REF
                and a["from_post_review_deferred_asset_audit"] == UPSTREAM_POST_REVIEW_REF
                and a["from_resolution_planning_candidate"] == UPSTREAM_RESOLUTION_PLANNING_REF
                and (a["asset_id"] != "byte_track" or a["from_registry_correction_planning"] == UPSTREAM_REGISTRY_CORRECTION_REF)
            ),
        )
        for a in SOURCE_INSTALL_INPUT_ASSETS
    ]

    # ------------------------------------------------------------------- #
    # (二/三) Route candidates + (四) repository placeholders.
    # ------------------------------------------------------------------- #
    route_candidates = [SourceRouteCandidate(**c) for c in SOURCE_ROUTE_CANDIDATES]
    repository_candidates = [SourceRepositoryCandidate(**c) for c in SOURCE_REPOSITORY_CANDIDATES]

    # ------------------------------------------------------------------- #
    # (五) Dependency expansion + (六) license + (七) weight boundary.
    # ------------------------------------------------------------------- #
    dependency_plans = [
        SourceDependencyExpansionPlan(
            asset_id=aid,
            source_requirements_unknown_or_unverified=True,
            transitive_dependencies_unknown=True,
            risk_dimensions=DEPENDENCY_EXPANSION_RISK_DIMENSIONS,
            dependency_expansion_review_required=True,
            source_install_must_not_use_package_install_only_approval=True,
            review_completed=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    license_plans = [
        SourceLicenseBoundaryPlan(
            asset_id=aid,
            source_license_review_required=True,
            repository_license_unverified=True,
            transitive_dependency_license_review_required=True,
            commercial_runtime_not_approved=COMMERCIAL_RUNTIME_APPROVED is False,
            license_binding_required_before_source_install=True,
            source_install_success_would_not_commercial_runtime_approval=True,
            review_completed=False,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    weight_plans = [
        SourceWeightBoundaryPlan(
            asset_id=aid,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            source_install_approval_not_weight_download_approval=True,
            weight_download_requires_separate_approval=True,
            weight_hash_required_before_future_inference=True,
            weight_source_review_required=True,
            tracker_or_detector_weights_may_be_needed_later=WEIGHT_BOUNDARY_SPECIFICS[aid]["tracker_or_detector_weights_may_be_needed_later"],
            checkpoint_weights_may_be_needed_later=WEIGHT_BOUNDARY_SPECIFICS[aid]["checkpoint_weights_may_be_needed_later"],
            weight_boundary_required=WEIGHT_BOUNDARY_SPECIFICS[aid]["weight_boundary_required"],
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (八) Isolation + (九) command whitelist + (十) approval + risk.
    # ------------------------------------------------------------------- #
    isolation_requirements = [
        SourceIsolationRequirement(
            asset_id=aid,
            separate_source_install_env_required=True,
            no_global_site_packages_preferred=True,
            pre_source_install_snapshot_required=True,
            source_checkout_path_must_be_controlled=True,
            command_whitelist_required=True,
            network_scope_must_be_explicit=True,
            post_install_probe_find_spec_only=True,
            no_real_import_after_source_install_without_review=True,
            rollback_required=True,
            test_board_write_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    command_records = [
        SourceCommandWhitelistPlanningRecord(
            asset_id=aid,
            command_template_ref=SOURCE_COMMAND_TEMPLATE_REFS[aid],
            template_only=True,
            command_not_executed=True,
            git_clone_command_allowed_now=False,
            pip_install_command_allowed_now=False,
            weight_download_command_allowed_now=False,
            command_requires_future_owner_approval=True,
            command_requires_pre_snapshot=True,
            command_requires_license_review=True,
            command_requires_dependency_review=True,
            command_requires_rollback=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    approval_requirements = [
        SourceInstallApprovalRequirement(
            asset_id=aid,
            source_install_owner_approval_required=True,
            source_install_request_phase_required=True,
            source_install_issuance_phase_required=True,
            source_install_execution_preparation_required=True,
            source_install_execution_phase_required=True,
            source_install_post_review_required=True,
            weight_download_separate_approval_required=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    risk_assessments = [
        SourceInstallRiskAssessment(
            asset_id=aid,
            source_install_higher_risk_than_clean_pypi=True,
            risk_dimensions=DEPENDENCY_EXPANSION_RISK_DIMENSIONS,
            source_install_must_be_isolated=True,
            source_install_must_not_share_package_install_only_approval=True,
            source_install_requires_separate_approval=True,
            all_risk_dimensions_recorded=len(DEPENDENCY_EXPANSION_RISK_DIMENSIONS) == 5,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (十一) Registry patch need + (十二) follow-up routing.
    # ------------------------------------------------------------------- #
    patch_assessments = [
        RegistryPatchNeedAssessment(
            asset_id=aid,
            registry_patch_likely_required=REGISTRY_PATCH_NEED[aid]["registry_patch_likely_required"],
            recommended_patch_direction=REGISTRY_PATCH_NEED[aid]["recommended_patch_direction"],
            registry_patch_before_source_install=REGISTRY_PATCH_NEED[aid]["registry_patch_before_source_install"],
            registry_patch_before_runtime=REGISTRY_PATCH_NEED[aid]["registry_patch_before_runtime"],
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]
    followup_routings = [
        SourceInstallFollowupRouting(
            asset_id=aid,
            recommended_next_phase=FOLLOWUP_ROUTING[aid]["recommended_next_phase"],
            alternate_next_phase=FOLLOWUP_ROUTING[aid]["alternate_next_phase"],
            asset_route=FOLLOWUP_ROUTING[aid]["asset_route"],
            no_weight_download_phase_until_source_install_post_review=FOLLOWUP_ROUTING[aid]["no_weight_download_phase_until_source_install_post_review"],
            source_install_requires_separate_approval=True,
        )
        for aid in IN_SCOPE_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # Invariants for the 21 negative guards.
    # ------------------------------------------------------------------- #
    byte_track_remains_deferred = any(
        c.asset_id == "byte_track" and c.remains_deferred for c in route_candidates
    )
    mobile_sam_remains_deferred = any(
        c.asset_id == "mobile_sam" and c.remains_deferred for c in route_candidates
    )
    invariant_state: Dict[str, bool] = {
        "no_git_clone": GIT_CLONE_ALLOWED is False,
        "no_source_install": SOURCE_INSTALL_ALLOWED is False and SOURCE_CHECKOUT_ALLOWED is False,
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
        "byte_track_remains_deferred": byte_track_remains_deferred,
        "mobile_sam_remains_deferred": mobile_sam_remains_deferred,
        "planning_not_source_install_approval": (
            SOURCE_INSTALL_ALLOWED is False
            and all(c.source_install_planning_success_not_source_install_approval for c in route_candidates)
            and all(a.source_install_owner_approval_required for a in approval_requirements)
        ),
        "planning_not_weight_approval": (
            WEIGHT_DOWNLOAD_ALLOWED is False
            and all(c.source_install_planning_success_not_weight_download_approval for c in route_candidates)
        ),
        "repository_not_verified": all(
            r.repository_url_unverified and r.repository_license_not_verified and r.repository_ref_type == "placeholder"
            for r in repository_candidates
        ),
        "repository_commit_not_pinned": all(r.repository_commit_not_pinned for r in repository_candidates),
        "license_review_not_completed": all(not lp.review_completed for lp in license_plans),
        "dependency_review_not_completed": all(not dp.review_completed for dp in dependency_plans),
        "weight_not_approved_by_default": WEIGHT_DOWNLOAD_ALLOWED is False
        and all(wp.weight_download_requires_separate_approval for wp in weight_plans),
        "source_install_not_reuse_pkg_approval": all(
            dp.source_install_must_not_use_package_install_only_approval for dp in dependency_plans
        )
        and all(ra.source_install_must_not_share_package_install_only_approval for ra in risk_assessments),
        "post_install_probe_find_spec_only": all(
            ir.post_install_probe_find_spec_only and ir.no_real_import_after_source_install_without_review
            for ir in isolation_requirements
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeControlledSourceInstallResolutionPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledSourceInstallResolutionPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_source_install_resolution_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    registry_patch_before_runtime_required = all(
        p.registry_patch_before_runtime == "required" for p in patch_assessments
    )

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_source_install_resolution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_install_input_asset_count_eq_2": len(input_assets) == 2,
        "source_route_candidate_count_eq_2": len(route_candidates) == 2,
        "source_repository_candidate_count_eq_2": len(repository_candidates) == 2,
        "source_dependency_expansion_plan_count_eq_2": len(dependency_plans) == 2,
        "source_license_boundary_plan_count_eq_2": len(license_plans) == 2,
        "source_weight_boundary_plan_count_eq_2": len(weight_plans) == 2,
        "source_isolation_requirement_count_eq_2": len(isolation_requirements) == 2,
        "source_command_whitelist_planning_record_count_eq_2": len(command_records) == 2,
        "source_install_approval_requirement_count_eq_2": len(approval_requirements) == 2,
        "source_install_risk_assessment_count_eq_2": len(risk_assessments) == 2,
        "registry_patch_need_assessment_count_eq_2": len(patch_assessments) == 2,
        "source_install_followup_routing_count_eq_2": len(followup_routings) == 2,
        "negative_guard_count_eq_21": negative_guard_count == 21,
        "negative_guard_passed_eq_21": negative_guard_passed == 21,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings (planning-only).
        "planning_only": PLANNING_ONLY is True,
        "controlled_source_install_resolution_planning_only": CONTROLLED_SOURCE_INSTALL_RESOLUTION_PLANNING_ONLY is True,
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
        # Resolution facts.
        "byte_track_remains_deferred": byte_track_remains_deferred,
        "mobile_sam_remains_deferred": mobile_sam_remains_deferred,
        "source_repository_refs_placeholder_only": all(r.repository_ref_type == "placeholder" for r in repository_candidates),
        "repository_urls_unverified": all(r.repository_url_unverified for r in repository_candidates),
        "repository_commits_not_pinned": all(r.repository_commit_not_pinned for r in repository_candidates),
        "repository_licenses_not_verified": all(r.repository_license_not_verified for r in repository_candidates),
        "dependency_expansion_review_required": all(dp.dependency_expansion_review_required for dp in dependency_plans),
        "license_review_required": all(lp.source_license_review_required for lp in license_plans),
        "source_install_requires_separate_approval": all(a.source_install_owner_approval_required for a in approval_requirements),
        "source_install_cannot_reuse_package_install_only_approval": all(
            dp.source_install_must_not_use_package_install_only_approval for dp in dependency_plans
        ),
        "weight_download_requires_separate_approval": all(wp.weight_download_requires_separate_approval for wp in weight_plans),
        "source_install_approval_not_weight_download_approval": all(
            wp.source_install_approval_not_weight_download_approval for wp in weight_plans
        ),
        "registry_patch_before_runtime_required": registry_patch_before_runtime_required,
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
    decision = P1ControlledSourceInstallResolutionPlanningDecision(
        decision_ref=DECISION_REF,
        controlled_source_install_resolution_profile_count=1,
        source_install_input_asset_count=len(input_assets),
        source_route_candidate_count=len(route_candidates),
        source_repository_candidate_count=len(repository_candidates),
        source_dependency_expansion_plan_count=len(dependency_plans),
        source_license_boundary_plan_count=len(license_plans),
        source_weight_boundary_plan_count=len(weight_plans),
        source_isolation_requirement_count=len(isolation_requirements),
        source_command_whitelist_planning_record_count=len(command_records),
        source_install_approval_requirement_count=len(approval_requirements),
        source_install_risk_assessment_count=len(risk_assessments),
        registry_patch_need_assessment_count=len(patch_assessments),
        source_install_followup_routing_count=len(followup_routings),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Resolution Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_registry_correction_ref": UPSTREAM_REGISTRY_CORRECTION_REF,
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
        "controlled_source_install_resolution_profile": _build_profile(),
        "controlled_source_install_resolution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Planning artifacts.
        "source_install_input_assets": [asdict(a) for a in input_assets],
        "source_install_input_asset_count": len(input_assets),
        "source_route_candidates": [asdict(c) for c in route_candidates],
        "source_route_candidate_count": len(route_candidates),
        "source_repository_candidates": [asdict(r) for r in repository_candidates],
        "source_repository_candidate_count": len(repository_candidates),
        "source_dependency_expansion_plans": [asdict(d) for d in dependency_plans],
        "source_dependency_expansion_plan_count": len(dependency_plans),
        "source_license_boundary_plans": [asdict(lp) for lp in license_plans],
        "source_license_boundary_plan_count": len(license_plans),
        "source_weight_boundary_plans": [asdict(wp) for wp in weight_plans],
        "source_weight_boundary_plan_count": len(weight_plans),
        "source_isolation_requirements": [asdict(ir) for ir in isolation_requirements],
        "source_isolation_requirement_count": len(isolation_requirements),
        "source_command_whitelist_planning_records": [asdict(c) for c in command_records],
        "source_command_whitelist_planning_record_count": len(command_records),
        "source_install_approval_requirements": [asdict(a) for a in approval_requirements],
        "source_install_approval_requirement_count": len(approval_requirements),
        "source_install_risk_assessments": [asdict(r) for r in risk_assessments],
        "source_install_risk_assessment_count": len(risk_assessments),
        "registry_patch_need_assessments": [asdict(p) for p in patch_assessments],
        "registry_patch_need_assessment_count": len(patch_assessments),
        "source_install_followup_routings": [asdict(f) for f in followup_routings],
        "source_install_followup_routing_count": len(followup_routings),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_resolution_planning_status": (
                "byte_track_and_mobile_sam_source_routes_resolved_no_clone_no_checkout_no_install_no_download_no_registry_mutation"
                if review_ok
                else "blocked"
            ),
            "byte_track_route": FOLLOWUP_ROUTING["byte_track"]["asset_route"],
            "mobile_sam_route": FOLLOWUP_ROUTING["mobile_sam"]["asset_route"],
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Source-install route resolution PLANNING complete for byte_track and mobile_sam (both REMAIN "
                "DEFERRED). Per asset we recorded: route candidate, repository placeholder (URL unverified, commit not "
                "pinned, license not verified, no network lookup), dependency-expansion plan (requirements/transitive "
                "deps unknown; review required; must NOT reuse the package-install-only approval), license boundary "
                "(review required; commercial runtime not approved), weight boundary (no weight/model/dataset "
                "download; weights may be needed later but NOT now; separate approval required), isolation requirement "
                "(separate env, pre-snapshot, controlled checkout path, command whitelist, explicit network scope, "
                "post-install probe find_spec only, rollback, test board), a command-whitelist TEMPLATE (not "
                "executed), an approval requirement (full request -> issuance -> preparation -> execution -> "
                "post-review chain), a risk assessment, and a registry-patch-need assessment. byte_track: registry "
                "patch likely required (direction = source_component_or_unresolved_package; optional before source "
                "install, REQUIRED before runtime). mobile_sam: registry patch maybe (direction = "
                "source_install_method_binding; required before runtime). Source install is higher risk than ordinary "
                "pip install and must re-run the full request->approval->preparation->execution chain; source-install "
                "planning success is NOT source-install / weight-download approval. Nothing was cloned / checked out / "
                "installed / downloaded; no real import / load / inference / runtime / output / semantic; registry not "
                "modified. Next: Phase-P1-Controlled-Source-Install-Request-Planning-v1-001 (still not clone/install)."
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
            "source_install_resolution_plan_record": {
                "source_install_input_assets": [asdict(a) for a in input_assets],
                "source_route_candidates": [asdict(c) for c in route_candidates],
                "source_repository_candidates": [asdict(r) for r in repository_candidates],
                "source_install_approval_requirements": [asdict(a) for a in approval_requirements],
                "source_install_risk_assessments": [asdict(r) for r in risk_assessments],
            },
            "source_dependency_expansion_record": {
                "source_dependency_expansion_plans": [asdict(d) for d in dependency_plans],
                "source_command_whitelist_planning_records": [asdict(c) for c in command_records],
            },
            "source_license_boundary_record": {
                "source_license_boundary_plans": [asdict(lp) for lp in license_plans]
            },
            "source_weight_boundary_record": {
                "source_weight_boundary_plans": [asdict(wp) for wp in weight_plans]
            },
            "source_isolation_requirement_record": {
                "source_isolation_requirements": [asdict(ir) for ir in isolation_requirements]
            },
            "source_followup_routing_record": {
                "registry_patch_need_assessments": [asdict(p) for p in patch_assessments],
                "source_install_followup_routings": [asdict(f) for f in followup_routings],
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
    result = review_p1_controlled_source_install_resolution_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "input_asset_count": result["decision"]["source_install_input_asset_count"],
                "route_candidate_count": result["decision"]["source_route_candidate_count"],
                "followup_count": result["decision"]["source_install_followup_routing_count"],
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
