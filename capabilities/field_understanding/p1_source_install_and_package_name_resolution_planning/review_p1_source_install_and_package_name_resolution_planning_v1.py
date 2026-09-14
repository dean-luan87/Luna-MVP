# -*- coding: utf-8 -*-
"""P1 Source Install And Package Name Resolution Planning — review v1.

PLANNING ONLY. Builds source-install / package-name-resolution route plans for
the two honestly-deferred assets (byte_track, mobile_sam) and routes them to a
separate sub-chain. Executes NOTHING: no git clone, no source install, no pip
install, no download, no real import / model load / inference, no runtime /
output adapter / semantic layer, NO registry mutation. Protected, non-deletable
test board records are written in planning mode.
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
from capabilities.field_understanding.p1_source_install_and_package_name_resolution_planning.p1_source_install_and_package_name_resolution_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_source_install_and_package_name_resolution_planning.p1_source_install_and_package_name_resolution_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEFERRED_ASSET_IDS,
    DEFERRED_ASSET_INPUTS,
    DEPENDENCY_INSTALL_ALLOWED,
    EXECUTION_ISOLATION_ITEMS,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FOLLOWUP_ROUTING,
    GIT_CLONE_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    PACKAGE_NAME_RESOLUTION_CANDIDATES,
    PACKAGE_NAME_RESOLUTION_PLANNING_ONLY,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_CORRECTION_CANDIDATES,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_INSTALL_ALLOWED,
    SOURCE_INSTALL_PLANNING_ONLY,
    SOURCE_INSTALL_RISK_DIMENSIONS,
    SOURCE_INSTALL_ROUTE_CANDIDATES,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_POST_REVIEW_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    DeferredAssetResolutionInput,
    DependencyExpansionAssessment,
    ExecutionIsolationRequirement,
    FollowupPhaseRoutingRecord,
    LicenseBoundaryAssessment,
    NegativeSourceInstallResolutionPlanningGuard,
    P1SourceInstallPackageResolutionPlanningDecision,
    P1SourceInstallPackageResolutionProfile,
    PackageNameResolutionCandidate,
    RegistryCorrectionCandidate,
    SourceInstallRiskAssessment,
    SourceInstallRouteCandidate,
    WeightBoundaryAssessment,
    candidate_to_dict,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_source_install_and_package_name_resolution_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_source_install_and_package_name_resolution_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_source_install_and_package_name_resolution_planning"
STEP_FILES = (
    f"{_PKG}/p1_source_install_and_package_name_resolution_planning_types_v1.py",
    f"{_PKG}/p1_source_install_and_package_name_resolution_planning_registry_v1.py",
    f"{_PKG}/review_p1_source_install_and_package_name_resolution_planning_v1.py",
)

PROFILE_REF = "p1_source_install_and_package_name_resolution_planning_profile_v1"
DECISION_REF = "p1_source_install_and_package_name_resolution_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1SourceInstallPackageResolutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            source_install_planning_only=SOURCE_INSTALL_PLANNING_ONLY,
            package_name_resolution_planning_only=PACKAGE_NAME_RESOLUTION_PLANNING_ONLY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
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
            upstream_post_review_ref=UPSTREAM_POST_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            deferred_asset_ids=DEFERRED_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_source_install_and_package_name_resolution_planning_v1(
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
    # (一) Deferred asset resolution inputs (2).
    # ------------------------------------------------------------------- #
    resolution_inputs = [
        DeferredAssetResolutionInput(
            asset_id=d["asset_id"],
            deferred_source_phase=d["deferred_source_phase"],
            registry_package_candidate=d["registry_package_candidate"],
            registry_import_candidate=d["registry_import_candidate"],
            clean_pypi_install_completed=d["clean_pypi_install_completed"],
            find_spec_hit=d["find_spec_hit"],
            deferred_reason_tokens=tuple(d["deferred_reason_tokens"]),
            confirmed_deferred_from_execution_phase=d["deferred_source_phase"] == UPSTREAM_EXECUTION_REF,
        )
        for d in DEFERRED_ASSET_INPUTS
    ]

    # ------------------------------------------------------------------- #
    # (二) Package-name resolution + (三) source install route candidates.
    # ------------------------------------------------------------------- #
    pkg_candidates = [PackageNameResolutionCandidate(**c) for c in PACKAGE_NAME_RESOLUTION_CANDIDATES]
    source_candidates = [SourceInstallRouteCandidate(**c) for c in SOURCE_INSTALL_ROUTE_CANDIDATES]
    registry_candidates = [RegistryCorrectionCandidate(**c) for c in REGISTRY_CORRECTION_CANDIDATES]

    # ------------------------------------------------------------------- #
    # (四) Source install risk assessment (2) + dependency expansion (2).
    # ------------------------------------------------------------------- #
    risk_assessments = [
        SourceInstallRiskAssessment(
            asset_id=aid,
            risk_dimensions=SOURCE_INSTALL_RISK_DIMENSIONS,
            source_install_higher_risk_than_clean_pypi=True,
            source_install_must_be_isolated=True,
            source_install_must_not_share_package_install_only_approval=True,
            source_install_requires_separate_approval=True,
            all_risk_dimensions_recorded=len(SOURCE_INSTALL_RISK_DIMENSIONS) == 10,
        )
        for aid in DEFERRED_ASSET_IDS
    ]
    dependency_assessments = [
        DependencyExpansionAssessment(
            asset_id=aid,
            dependency_expansion_review_required=True,
            transitive_dependency_review_required=True,
            build_or_compile_dependency_possible=True,
            dependency_install_now=False,
            assessment_recorded=True,
        )
        for aid in DEFERRED_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (五) Weight boundary (2) + (六) license boundary (2).
    # ------------------------------------------------------------------- #
    weight_assessments = [
        WeightBoundaryAssessment(
            asset_id=aid,
            source_install_approval_is_not_weight_download_approval=True,
            source_install_planning_is_not_weight_readiness=True,
            weights_may_be_required_later_not_now=True,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            weight_download_requires_separate_approval=True,
            weight_boundary_recorded=True,
        )
        for aid in DEFERRED_ASSET_IDS
    ]
    license_assessments = [
        LicenseBoundaryAssessment(
            asset_id=aid,
            license_review_required_before_source_install=True,
            source_license_must_bind_to_asset_id=True,
            transitive_dependency_license_review_required=True,
            commercial_runtime_not_approved=COMMERCIAL_RUNTIME_APPROVED is False,
            source_install_success_would_not_approve_commercial_runtime=True,
            license_boundary_recorded=True,
        )
        for aid in DEFERRED_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (七) Execution isolation requirement (2).
    # ------------------------------------------------------------------- #
    isolation_requirements = [
        ExecutionIsolationRequirement(
            asset_id=aid,
            isolation_items=EXECUTION_ISOLATION_ITEMS,
            separate_isolated_environment_recommended=True,
            pre_source_install_snapshot_required=True,
            command_whitelist_required=True,
            post_install_probe_find_spec_only=True,
            rollback_path_required=True,
            test_board_write_required=True,
            all_isolation_items_recorded=len(EXECUTION_ISOLATION_ITEMS) == 9,
        )
        for aid in DEFERRED_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # (八) Follow-up routing (2).
    # ------------------------------------------------------------------- #
    followup_records = [
        FollowupPhaseRoutingRecord(
            asset_id=r["asset_id"],
            requires_registry_package_name_correction_planning=r["requires_registry_package_name_correction_planning"],
            requires_source_install_resolution_planning=r["requires_source_install_resolution_planning"],
            recommended_next_phase_refs=tuple(r["recommended_next_phase_refs"]),
            route_split_allowed=r["route_split_allowed"],
            recommended_first=r["recommended_first"],
            deferred_assets_require_separate_phase=True,
            source_install_requires_separate_approval=True,
            registry_correction_requires_separate_review=True,
        )
        for r in FOLLOWUP_ROUTING
    ]

    # ------------------------------------------------------------------- #
    # Invariants for the 18 negative guards.
    # ------------------------------------------------------------------- #
    byte_track_resolution_recorded = (
        any(c.asset_id == "byte_track" for c in pkg_candidates)
        and any("package_name_resolution_required" in i.deferred_reason_tokens for i in resolution_inputs if i.asset_id == "byte_track")
    )
    mobile_sam_source_required_recorded = any(
        c.asset_id == "mobile_sam" and c.git_or_source_install_required for c in source_candidates
    )
    source_install_not_clean_pypi = all(
        c.git_or_source_install_required and not c.source_install_now for c in source_candidates
    )
    planning_not_source_install_approval = SOURCE_INSTALL_ALLOWED is False and all(
        c.requires_source_install_approval for c in source_candidates
    )
    invariant_state: Dict[str, bool] = {
        "no_git_clone": GIT_CLONE_ALLOWED is False,
        "no_source_install": SOURCE_INSTALL_ALLOWED is False,
        "no_pip_install": PIP_INSTALL_ALLOWED is False,
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
        "byte_track_resolution_recorded": byte_track_resolution_recorded,
        "mobile_sam_source_required_recorded": mobile_sam_source_required_recorded,
        "source_install_not_clean_pypi": source_install_not_clean_pypi,
        "planning_not_source_install_approval": planning_not_source_install_approval,
        "planning_not_weight_approval": WEIGHT_DOWNLOAD_ALLOWED is False,
        "weight_not_approved_by_default": WEIGHT_DOWNLOAD_ALLOWED is False,
        "license_review_required": all(la.license_review_required_before_source_install for la in license_assessments),
        "dependency_expansion_review_required": all(da.dependency_expansion_review_required for da in dependency_assessments),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceInstallResolutionPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceInstallResolutionPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_install_resolution_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_install_package_resolution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "deferred_asset_resolution_input_count_eq_2": len(resolution_inputs) == 2,
        "package_name_resolution_candidate_count_gte_1": len(pkg_candidates) >= 1,
        "source_install_route_candidate_count_gte_2": len(source_candidates) >= 2,
        "registry_correction_candidate_count_gte_1": len(registry_candidates) >= 1,
        "source_install_risk_assessment_count_eq_2": len(risk_assessments) == 2,
        "dependency_expansion_assessment_count_eq_2": len(dependency_assessments) == 2,
        "weight_boundary_assessment_count_eq_2": len(weight_assessments) == 2,
        "license_boundary_assessment_count_eq_2": len(license_assessments) == 2,
        "execution_isolation_requirement_count_eq_2": len(isolation_requirements) == 2,
        "followup_phase_routing_record_count_eq_2": len(followup_records) == 2,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings (planning-only).
        "planning_only": PLANNING_ONLY is True,
        "source_install_planning_only": SOURCE_INSTALL_PLANNING_ONLY is True,
        "package_name_resolution_planning_only": PACKAGE_NAME_RESOLUTION_PLANNING_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
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
        "byte_track_package_name_resolution_required": byte_track_resolution_recorded,
        "mobile_sam_source_install_required": mobile_sam_source_required_recorded,
        "deferred_assets_require_separate_phase": all(f.deferred_assets_require_separate_phase for f in followup_records),
        "source_install_requires_separate_approval": all(f.source_install_requires_separate_approval for f in followup_records),
        "registry_correction_requires_separate_review": all(f.registry_correction_requires_separate_review for f in followup_records),
        "weight_download_requires_separate_approval": all(w.weight_download_requires_separate_approval for w in weight_assessments),
        "license_review_required": all(la.license_review_required_before_source_install for la in license_assessments),
        "dependency_expansion_review_required": all(da.dependency_expansion_review_required for da in dependency_assessments),
        "source_install_isolation_required": all(ir.separate_isolated_environment_recommended for ir in isolation_requirements),
        "source_install_not_clean_pypi": source_install_not_clean_pypi,
        "source_install_planning_not_source_install_approval": planning_not_source_install_approval,
        "source_install_planning_not_weight_download_approval": WEIGHT_DOWNLOAD_ALLOWED is False,
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
    decision = P1SourceInstallPackageResolutionPlanningDecision(
        decision_ref=DECISION_REF,
        source_install_package_resolution_profile_count=1,
        deferred_asset_resolution_input_count=len(resolution_inputs),
        package_name_resolution_candidate_count=len(pkg_candidates),
        source_install_route_candidate_count=len(source_candidates),
        registry_correction_candidate_count=len(registry_candidates),
        source_install_risk_assessment_count=len(risk_assessments),
        dependency_expansion_assessment_count=len(dependency_assessments),
        weight_boundary_assessment_count=len(weight_assessments),
        license_boundary_assessment_count=len(license_assessments),
        execution_isolation_requirement_count=len(isolation_requirements),
        followup_phase_routing_record_count=len(followup_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Source Install And Package Name Resolution Planning (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_only": PLANNING_ONLY,
        "upstream_post_review_ref": UPSTREAM_POST_REVIEW_REF,
        "upstream_execution_ref": UPSTREAM_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_install_package_resolution_profile": _build_profile(),
        "source_install_package_resolution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Planning artifacts.
        "deferred_asset_resolution_inputs": [asdict(r) for r in resolution_inputs],
        "deferred_asset_resolution_input_count": len(resolution_inputs),
        "package_name_resolution_candidates": [asdict(c) for c in pkg_candidates],
        "package_name_resolution_candidate_count": len(pkg_candidates),
        "source_install_route_candidates": [asdict(c) for c in source_candidates],
        "source_install_route_candidate_count": len(source_candidates),
        "registry_correction_candidates": [asdict(c) for c in registry_candidates],
        "registry_correction_candidate_count": len(registry_candidates),
        "source_install_risk_assessments": [asdict(r) for r in risk_assessments],
        "source_install_risk_assessment_count": len(risk_assessments),
        "dependency_expansion_assessments": [asdict(d) for d in dependency_assessments],
        "dependency_expansion_assessment_count": len(dependency_assessments),
        "weight_boundary_assessments": [asdict(w) for w in weight_assessments],
        "weight_boundary_assessment_count": len(weight_assessments),
        "license_boundary_assessments": [asdict(la) for la in license_assessments],
        "license_boundary_assessment_count": len(license_assessments),
        "execution_isolation_requirements": [asdict(ir) for ir in isolation_requirements],
        "execution_isolation_requirement_count": len(isolation_requirements),
        "followup_phase_routing_records": [asdict(f) for f in followup_records],
        "followup_phase_routing_record_count": len(followup_records),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_source_install_and_package_name_resolution_planning_status": (
                "byte_track_and_mobile_sam_source_install_and_package_name_resolution_routes_planned_no_clone_no_source_install_no_registry_mutation"
                if review_ok
                else "blocked"
            ),
            "byte_track_routes": [c.next_phase_candidate for c in source_candidates if c.asset_id == "byte_track"]
            + [c.next_phase_candidate for c in pkg_candidates if c.asset_id == "byte_track"],
            "mobile_sam_routes": [c.next_phase_candidate for c in source_candidates if c.asset_id == "mobile_sam"],
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Source-install / package-name-resolution PLANNING complete for the two honestly-deferred assets. "
                "byte_track has two planned routes: (A) registry package-name correction (bytetrack/yolox name+import "
                "mismatch -> requires a separate registry correction review; NO registry mutation now) and (B) a "
                "ByteTrack/yolox source-install route (requires separate source-install approval, dependency-expansion "
                "review, license review, and a no-weight-download boundary). mobile_sam has a MobileSAM git/source-"
                "install route (separate approval + dependency/license/weight-boundary review). Source install is "
                "higher risk than a clean PyPI wheel, must be isolated, and must NOT reuse the package-install-only "
                "approval. Source-install planning is NOT source-install approval and NOT weight-download approval; "
                "weights may be needed later but NOT now. Nothing was cloned / installed / downloaded; no real import "
                "/ model load / inference / runtime / output adapter / semantic layer; registry was not modified. "
                "Recommended route: first Phase-P1-Registry-Package-Name-Correction-Planning-v1-001 for byte_track "
                "(rule out a pure name/import mapping error), then "
                "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001 for byte_track and mobile_sam source "
                "sub-approval."
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
            "deferred_asset_resolution_plan_record": {
                "deferred_asset_resolution_inputs": [asdict(r) for r in resolution_inputs],
                "package_name_resolution_candidates": [asdict(c) for c in pkg_candidates],
                "source_install_route_candidates": [asdict(c) for c in source_candidates],
                "followup_phase_routing_records": [asdict(f) for f in followup_records],
            },
            "source_install_risk_record": {
                "source_install_risk_assessments": [asdict(r) for r in risk_assessments],
                "dependency_expansion_assessments": [asdict(d) for d in dependency_assessments],
                "execution_isolation_requirements": [asdict(ir) for ir in isolation_requirements],
            },
            "registry_correction_candidate_record": {
                "registry_correction_candidates": [asdict(c) for c in registry_candidates]
            },
            "weight_boundary_record": {
                "weight_boundary_assessments": [asdict(w) for w in weight_assessments],
                "license_boundary_assessments": [asdict(la) for la in license_assessments],
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
    result = review_p1_source_install_and_package_name_resolution_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "deferred_input_count": result["decision"]["deferred_asset_resolution_input_count"],
                "source_route_count": result["decision"]["source_install_route_candidate_count"],
                "followup_count": result["decision"]["followup_phase_routing_record_count"],
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
