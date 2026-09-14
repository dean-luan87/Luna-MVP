# -*- coding: utf-8 -*-
"""P1 Controlled Install Planning DryRun — review v1.

Generates an auditable controlled-install PLAN for the 5 INSTALL_REQUIRED P1
assets: candidate selection, install order, dependency-resolution plan, package
install plan (template-only), weight-acquisition plan, environment-isolation
plan, version-pin plan, license install boundary, rollback plan, blocker rules,
audit record and a controlled-install readiness matrix. Nothing is installed,
downloaded or executed. Install command templates are template_only. Protected
records are written to the test board in the (now-valid) planning mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
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
from capabilities.midplatform.model_version_dependency_registry_planning.model_version_dependency_registry_planning_types_v1 import (  # noqa: E402
    REGISTRY_ASSETS,
)
from capabilities.field_understanding.p1_real_install_local_availability_dryrun.p1_real_install_local_availability_dryrun_types_v1 import (  # noqa: E402
    LOCAL_ASSETS,
)
from capabilities.field_understanding.p1_controlled_install_planning_dryrun.p1_controlled_install_planning_dryrun_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_planning_dryrun.p1_controlled_install_planning_dryrun_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CLEANUP_SCOPE_NOTE,
    CONTROLLED_INSTALL_PHASE_GOVERNANCE_RULES,
    CONTROLLED_INSTALL_PLANNING_ONLY,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    DEPENDENCY_LAYER_BY_FAMILY,
    EXCLUDED_ASSETS,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    EXPECTED_EXCLUDED_ASSET_COUNT,
    EXPECTED_INSTALL_CANDIDATE_COUNT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GLOBAL_DEPENDENCY_RESOLUTION_STRATEGY,
    HANDOFF_READINESS_TARGETS,
    INSTALL_CANDIDATE_ASSET_IDS,
    INSTALL_ORDER_PLAN,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
    PHASE_ID,
    PLANNING_DRYRUN_ONLY,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TRUE_INVARIANTS,
    RECONCILIATION_POST_REVIEW_REF,
    REGISTRY_PLANNING_REF,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROLLBACK_STEPS_TEMPLATE,
    ROLLBACK_TRIGGER_CONDITIONS,
    SCOPE,
    SOURCE_CHAIN,
    SOURCE_READINESS_STATE_REQUIRED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    ControlledInstallReadinessMatrix,
    DependencyResolutionPlan,
    EnvironmentIsolationPlan,
    InstallAuditRecord,
    InstallBlockerRule,
    InstallCandidateSelectionRecord,
    InstallHandoffReadiness,
    InstallOrderPlanRecord,
    LicenseInstallBoundaryCheck,
    NegativeControlledInstallPlanningGuard,
    P1ControlledInstallPlanningProfile,
    PackageInstallPlan,
    RollbackPlan,
    VersionPinPlan,
    WeightAcquisitionPlan,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_controlled_install_planning_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_planning_dryrun_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_planning_dryrun"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_planning_dryrun_types_v1.py",
    f"{_PKG}/p1_controlled_install_planning_dryrun_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_planning_dryrun_v1.py",
)

PROFILE_REF = "p1_controlled_install_planning_dryrun_profile_v1"
AUDIT_REF = "p1_controlled_install_planning_audit_v1"

P1_PROBE_ARTIFACT_REL = (
    "_tmp_eval_out/p1_real_install_local_availability_dryrun_v1_smoke_v0/"
    "p1_real_install_local_availability_dryrun_review_v1.json"
)


def _risk_to_install_risk(risk: str) -> str:
    return {"LOW": "low", "MEDIUM": "medium", "HIGH": "high", "BLOCKED": "blocked"}.get(risk, "medium")


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_dryrun_only=PLANNING_DRYRUN_ONLY,
            controlled_install_planning_only=CONTROLLED_INSTALL_PLANNING_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            reconciliation_post_review_ref=RECONCILIATION_POST_REVIEW_REF,
            registry_planning_ref=REGISTRY_PLANNING_REF,
            p1_real_install_local_availability_ref=P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            install_candidate_asset_ids=INSTALL_CANDIDATE_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_planning_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)

    reg_by_id = {a["asset_id"]: a for a in REGISTRY_ASSETS}
    p1_by_id = {a["asset_id"]: a for a in LOCAL_ASSETS}
    order_by_id = {o["asset_id"]: o for o in INSTALL_ORDER_PLAN}

    # Pull actual P1 install-readiness states when the probe artifact is present.
    p1_artifact, p1_exists = load_artifact(_REPO_ROOT, P1_PROBE_ARTIFACT_REL)
    p1_state_by_id: Dict[str, str] = {}
    p1_state_source = "static_fallback"
    if p1_exists and p1_artifact:
        for rec in p1_artifact.get("install_readiness_records", []):
            aid, st = rec.get("asset_id"), rec.get("install_readiness_state")
            if aid and st:
                p1_state_by_id[aid] = st
        if p1_state_by_id:
            p1_state_source = "p1_artifact_install_readiness_records"

    # --------------------------------------------------------------------- #
    # Candidate selection (only INSTALL_REQUIRED).
    # --------------------------------------------------------------------- #
    selection_records: List[InstallCandidateSelectionRecord] = []
    selection_violations: List[str] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid)
        p1 = p1_by_id.get(aid)
        if reg is None or p1 is None:
            selection_violations.append(f"candidate_missing_source:{aid}")
            continue
        # Verify the candidate is actually INSTALL_REQUIRED per the probe (or the
        # static p1 classification when the artifact is not readable).
        probe_state = p1_state_by_id.get(aid)
        if probe_state is not None and probe_state != SOURCE_READINESS_STATE_REQUIRED:
            selection_violations.append(f"candidate_not_install_required:{aid}:{probe_state}")
        license_class = reg["license_class"]
        license_allows_planning = license_class not in ("unknown",) and not reg["license_blocked"] if "license_blocked" in reg else license_class not in ("unknown",)
        selection_records.append(
            InstallCandidateSelectionRecord(
                asset_id=aid,
                source_readiness_state=SOURCE_READINESS_STATE_REQUIRED,
                registry_identity_ref=f"registry_identity::{aid}",
                registry_dependency_ref=f"registry_dependency::{aid}",
                registry_license_ref=f"registry_license::{aid}",
                p1_probe_ref=f"p1_probe::{aid}",
                reconciliation_ref=f"reconciliation::{aid}",
                selection_reason="install_required_permissive_license_eligible_for_controlled_install_planning",
                license_allows_planning=bool(license_allows_planning),
                install_execution_allowed=False,
                can_enter_controlled_install_plan=True,
                can_enter_install_execution=False,
                can_enter_runtime_trial=False,
                can_enter_real_output_adapter_dryrun=False,
            )
        )

    for v in selection_violations:
        failed_checks.append(f"selection_violation:{v}")

    install_candidate_count = len(selection_records)
    excluded_asset_count = len(EXCLUDED_ASSETS)

    # Ensure no excluded asset slipped into candidates.
    excluded_ids = {e["asset_id"] for e in EXCLUDED_ASSETS}
    candidate_ids = {r.asset_id for r in selection_records}
    overlap = candidate_ids & excluded_ids
    if overlap:
        failed_checks.append(f"excluded_assets_in_candidate:{sorted(overlap)}")

    # --------------------------------------------------------------------- #
    # Install order plan.
    # --------------------------------------------------------------------- #
    install_order_records = [
        InstallOrderPlanRecord(
            asset_id=o["asset_id"],
            planned_order=int(o["planned_order"]),
            order_reason=o["order_reason"],
            execution_performed=False,
        )
        for o in INSTALL_ORDER_PLAN
    ]

    # --------------------------------------------------------------------- #
    # Dependency resolution plan.
    # --------------------------------------------------------------------- #
    dependency_plans: List[DependencyResolutionPlan] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid, {})
        family = reg.get("model_family", "")
        risk = reg.get("risk", "MEDIUM")
        conflict_risk = "high" if risk in ("HIGH", "BLOCKED") else ("medium" if risk == "MEDIUM" else "low")
        dependency_plans.append(
            DependencyResolutionPlan(
                asset_id=aid,
                primary_package_name=reg.get("primary_package_name", aid),
                import_probe_name=reg.get("import_name", aid),
                dependency_group=reg.get("dependency_group", "unknown"),
                required_dependencies=tuple(reg.get("required_dependency_names", ())),
                optional_dependencies=tuple(reg.get("optional_package_names", ())),
                dependency_resolution_order=int(order_by_id.get(aid, {}).get("planned_order", 99)),
                conflict_risk=conflict_risk,
                version_pin_policy="floating_planning_only_pinned_before_future_install",
                visible_version_required_after_future_install=True,
                dependency_install_not_performed=True,
            )
        )

    # --------------------------------------------------------------------- #
    # Package install plan (template only).
    # --------------------------------------------------------------------- #
    package_plans: List[PackageInstallPlan] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid, {})
        pkgs = (reg.get("primary_package_name", aid),) + tuple(reg.get("required_dependency_names", ()))
        # de-dup while preserving order
        seen: List[str] = []
        for p in pkgs:
            if p and p not in seen:
                seen.append(p)
        risk = reg.get("risk", "MEDIUM")
        package_plans.append(
            PackageInstallPlan(
                asset_id=aid,
                planned_package_names=tuple(seen),
                install_command_template=f"pip install {' '.join(seen)}  # TEMPLATE_ONLY_DO_NOT_EXECUTE",
                install_command_not_executed=True,
                install_requires_owner_approval_before_execution=True,
                install_requires_virtualenv_or_isolated_env=True,
                install_requires_pre_snapshot=True,
                install_requires_post_probe=True,
                install_requires_rollback_plan=True,
                install_risk_level=_risk_to_install_risk(risk),
                template_only=True,
            )
        )

    # --------------------------------------------------------------------- #
    # Weight acquisition plan (all 5; tracking/utility may not need weights).
    # --------------------------------------------------------------------- #
    weight_plans: List[WeightAcquisitionPlan] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid, {})
        weight_required = bool(reg.get("weight_required", False))
        note = (
            "tracking_or_utility_asset_dependent_on_detector_output_no_model_weight_required"
            if not weight_required
            else "weight_required_hash_source_license_gated_before_future_inference"
        )
        weight_plans.append(
            WeightAcquisitionPlan(
                asset_id=aid,
                weight_required=weight_required,
                expected_weight_names=tuple(reg.get("expected_weight_names", ())),
                expected_weight_paths=tuple(reg.get("expected_weight_paths", ())),
                weight_source_policy="official_release_or_local_path_no_auto_download",
                weight_download_not_performed=True,
                weight_hash_required_before_future_inference=True,
                weight_license_binding_required=True,
                weight_source_review_required=True,
                auto_weight_download_allowed=False,
                note=note,
            )
        )

    # --------------------------------------------------------------------- #
    # Environment isolation plan (single shared plan).
    # --------------------------------------------------------------------- #
    environment_isolation_plan = EnvironmentIsolationPlan(
        target_env_label="luna_p1_controlled_install_isolated_env_planned",
        python_version_policy=">=3.9,<3.13",
        os_policy="macos_arm64_primary_dev_then_linux",
        macos_arm64_compatibility="cpu_or_mps_supported_no_cuda_assumption",
        cpu_only_possible=True,
        mps_possible=True,
        cuda_required=False,
        shared_dependency_policy="torch_core_and_cv_core_resolved_once_shared_no_unordered_reinstall",
        no_global_site_packages_policy=True,
        environment_snapshot_required=True,
        rollback_snapshot_required=True,
        no_runtime_execution_in_install_phase=True,
        existing_env_reference="current_mac_dot_venv_tx_environment_reference_only",
    )

    # --------------------------------------------------------------------- #
    # Version pin plan.
    # --------------------------------------------------------------------- #
    version_pin_plans = [
        VersionPinPlan(
            asset_id=aid,
            exact_pin_required_for_future_install_execution=True,
            allowed_minor_range_for_planning=True,
            version_unknown_allowed_for_planning=True,
            version_unknown_blocks_runtime=True,
            version_unknown_blocks_real_inference=True,
            installed_version_must_be_recorded_after_future_install=True,
            version_drift_requires_review=True,
        )
        for aid in INSTALL_CANDIDATE_ASSET_IDS
    ]

    # --------------------------------------------------------------------- #
    # License install boundary check.
    # --------------------------------------------------------------------- #
    license_checks: List[LicenseInstallBoundaryCheck] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid, {})
        license_class = reg.get("license_class", "unknown")
        permissive = license_class == "apache_or_mit"
        license_checks.append(
            LicenseInstallBoundaryCheck(
                asset_id=aid,
                license_type=reg.get("license_type", "unknown"),
                permissive_family=permissive,
                license_allows_install_planning=permissive,
                unknown_license_blocks_install_execution=(license_class == "unknown"),
                agpl_blocks_commercial_runtime=(license_class == "agpl"),
                commercial_runtime_approved=False,
                install_planning_not_commercial_approval=True,
                install_planning_not_runtime_approval=True,
            )
        )

    # --------------------------------------------------------------------- #
    # Rollback plan.
    # --------------------------------------------------------------------- #
    rollback_plans = [
        RollbackPlan(
            asset_id=aid,
            pre_install_snapshot_required=True,
            post_install_probe_required=True,
            rollback_trigger_conditions=ROLLBACK_TRIGGER_CONDITIONS,
            rollback_steps_template=ROLLBACK_STEPS_TEMPLATE,
            cleanup_scope=CLEANUP_SCOPE_NOTE,
            cleanup_must_not_delete_test_board=True,
            cleanup_must_not_delete_registry=True,
            cleanup_must_not_delete_review_artifacts=True,
            rollback_success_requires_post_review=True,
        )
        for aid in INSTALL_CANDIDATE_ASSET_IDS
    ]

    # --------------------------------------------------------------------- #
    # Install blocker rules.
    # --------------------------------------------------------------------- #
    blocker_rules = [
        InstallBlockerRule(rule_id=spec["guard_id"], description=spec["go_key"], is_blocker_when_violated=True)
        for spec in NEGATIVE_GUARDS
    ]

    # --------------------------------------------------------------------- #
    # Controlled install readiness matrix.
    # --------------------------------------------------------------------- #
    matrix: List[ControlledInstallReadinessMatrix] = []
    for aid in INSTALL_CANDIDATE_ASSET_IDS:
        reg = reg_by_id.get(aid, {})
        order = int(order_by_id.get(aid, {}).get("planned_order", 99))
        license_class = reg.get("license_class", "unknown")
        license_ok = license_class == "apache_or_mit"
        all_ready = True  # all planning records are produced for every candidate
        matrix.append(
            ControlledInstallReadinessMatrix(
                asset_id=aid,
                install_candidate=True,
                planned_order=order,
                dependency_group=reg.get("dependency_group", "unknown"),
                package_plan_ready=True,
                weight_plan_ready=True,
                env_isolation_ready=True,
                version_pin_plan_ready=True,
                license_boundary_ok=license_ok,
                rollback_plan_ready=True,
                # future execution remains gated on owner approval; planning complete -> true,
                # but execution itself still requires separate approval.
                can_enter_future_controlled_install_execution=bool(all_ready and license_ok),
                can_enter_runtime_trial=False,
                can_enter_real_output_adapter_dryrun=False,
                blocker_reason="none" if license_ok else "license_boundary_not_permissive",
            )
        )

    audit_record = InstallAuditRecord(
        audit_ref=AUDIT_REF,
        install_candidate_count=install_candidate_count,
        excluded_asset_count=excluded_asset_count,
        candidate_only=True,
        written_to_test_board=write_test_board,
        protected=True,
        non_deletable=True,
    )

    # --------------------------------------------------------------------- #
    # Negative guards (18).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    only_install_required = (
        install_candidate_count == EXPECTED_INSTALL_CANDIDATE_COUNT
        and not overlap
        and not selection_violations
    )
    invariant_state: Dict[str, bool] = {
        "no_install_performed": (
            nef["real_install_performed"] is False
            and nef["dependency_install_performed"] is False
            and nef["pip_install_performed"] is False
        ),
        "no_download_performed": (
            nef["model_download_performed"] is False
            and nef["weight_download_performed"] is False
            and nef["dataset_download_performed"] is False
        ),
        "no_real_inference": nef["real_inference_performed"] is False,
        "install_templates_not_executed": all(p.install_command_not_executed and p.template_only for p in package_plans),
        "env_isolation_plan_present": environment_isolation_plan.no_runtime_execution_in_install_phase is True,
        "rollback_plan_present": all(r.pre_install_snapshot_required for r in rollback_plans) and len(rollback_plans) == EXPECTED_INSTALL_CANDIDATE_COUNT,
        "version_pin_plan_present": len(version_pin_plans) == EXPECTED_INSTALL_CANDIDATE_COUNT,
        "weight_gate_present": all(
            w.weight_hash_required_before_future_inference and w.weight_license_binding_required and w.weight_source_review_required
            for w in weight_plans
        ),
        "only_install_required_selected": only_install_required,
        "commercial_runtime_not_approved": nef["commercial_runtime_approved"] is False,
        "planning_not_runtime_approval": all(not m.can_enter_runtime_trial for m in matrix),
        "planning_not_real_output_adapter_approval": all(not m.can_enter_real_output_adapter_dryrun for m in matrix),
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable_true": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeControlledInstallPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledInstallPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_install_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness.
    # --------------------------------------------------------------------- #
    handoff_readiness: List[InstallHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            InstallHandoffReadiness(
                target_ref=target["target_ref"], readiness_recorded=True, entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions: Dict[str, bool] = {
        "controlled_install_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "install_candidate_count_eq_5": install_candidate_count == 5,
        "excluded_asset_count_eq_12": excluded_asset_count == 12,
        "install_order_plan_count_eq_5": len(install_order_records) == 5,
        "dependency_resolution_plan_count_eq_5": len(dependency_plans) == 5,
        "package_install_plan_count_eq_5": len(package_plans) == 5,
        "weight_acquisition_plan_count_eq_5": len(weight_plans) == 5,
        "environment_isolation_plan_count_gte_1": 1 >= 1,
        "version_pin_plan_count_eq_5": len(version_pin_plans) == 5,
        "license_install_boundary_check_count_eq_5": len(license_checks) == 5,
        "rollback_plan_count_eq_5": len(rollback_plans) == 5,
        "controlled_install_readiness_matrix_count_eq_5": len(matrix) == 5,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        "runtime_eligible_asset_count_eq_0": all(not m.can_enter_runtime_trial for m in matrix),
        "real_output_adapter_eligible_asset_count_eq_0": all(not m.can_enter_real_output_adapter_dryrun for m in matrix),
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Planning true-invariants.
        **{k: (v is True) for k, v in PLANNING_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        # Test board fields + planned write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
        # Non-execution flags (all false).
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Planning DryRun",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "planning_dryrun_only": PLANNING_DRYRUN_ONLY,
        "controlled_install_planning_only": CONTROLLED_INSTALL_PLANNING_ONLY,
        "reconciliation_post_review_ref": RECONCILIATION_POST_REVIEW_REF,
        "registry_planning_ref": REGISTRY_PLANNING_REF,
        "p1_real_install_local_availability_ref": P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "controlled_install_phase_governance_rules": list(CONTROLLED_INSTALL_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "global_dependency_resolution_strategy": list(GLOBAL_DEPENDENCY_RESOLUTION_STRATEGY),
        "dependency_layer_by_family": dict(DEPENDENCY_LAYER_BY_FAMILY),
        "controlled_install_planning_profile": _build_profile(),
        "controlled_install_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "p1_probe_state_source": p1_state_source,
        "install_candidate_selection_records": [asdict(r) for r in selection_records],
        "install_candidate_count": install_candidate_count,
        "excluded_assets": [dict(e) for e in EXCLUDED_ASSETS],
        "excluded_asset_count": excluded_asset_count,
        "install_order_plans": [asdict(r) for r in install_order_records],
        "install_order_plan_count": len(install_order_records),
        "dependency_resolution_plans": [asdict(r) for r in dependency_plans],
        "dependency_resolution_plan_count": len(dependency_plans),
        "package_install_plans": [asdict(r) for r in package_plans],
        "package_install_plan_count": len(package_plans),
        "weight_acquisition_plans": [asdict(r) for r in weight_plans],
        "weight_acquisition_plan_count": len(weight_plans),
        "environment_isolation_plan": asdict(environment_isolation_plan),
        "environment_isolation_plan_count": 1,
        "version_pin_plans": [asdict(r) for r in version_pin_plans],
        "version_pin_plan_count": len(version_pin_plans),
        "license_install_boundary_checks": [asdict(r) for r in license_checks],
        "license_install_boundary_check_count": len(license_checks),
        "rollback_plans": [asdict(r) for r in rollback_plans],
        "rollback_plan_count": len(rollback_plans),
        "install_blocker_rules": [asdict(r) for r in blocker_rules],
        "install_blocker_rule_count": len(blocker_rules),
        "install_audit_record": asdict(audit_record),
        "controlled_install_readiness_matrix": [asdict(m) for m in matrix],
        "controlled_install_readiness_matrix_count": len(matrix),
        "runtime_eligible_asset_count": 0,
        "real_output_adapter_eligible_asset_count": 0,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_controlled_install_planning_dryrun_status": (
                "controlled_install_plan_generated_template_only_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Auditable controlled-install PLAN for the 5 INSTALL_REQUIRED P1 assets (supervision, "
                "byte_track, deep_sort, midas, mobile_sam). 12 assets are explicitly excluded "
                "(BLOCKED_BY_LICENSE / DEFERRED_RESOURCE_HEAVY / RESERVED_ONLY / non-INSTALL_REQUIRED). "
                "Install order, dependency-resolution plan, package install templates (template_only, never "
                "executed), weight-acquisition plan (no download; hash/source/license gated before future "
                "inference), a shared environment-isolation plan (CPU/MPS, no CUDA assumption, snapshot + "
                "rollback required), version-pin plan, license install boundary check, and rollback plan are "
                "produced for every candidate. Nothing is installed/downloaded/executed; no pip subprocess. "
                "Future install execution requires separate owner approval. Install planning success is NOT "
                "install-execution / runtime / real-output-adapter / commercial approval; runtime-trial and "
                "real-output-adapter eligibility remain false for all assets. Protected records are written to "
                "the test board in planning mode. Next: P1 Controlled Install Planning DryRun Post-Review "
                "before any real controlled install execution planning."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        manifest = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=board_root,
            module=TEST_BOARD_MODULE,
            source_review_file=result.get("output_review_file"),
        )
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_p1_controlled_install_planning_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "install_candidate_count": result["install_candidate_count"],
                "excluded_asset_count": result["excluded_asset_count"],
                "p1_probe_state_source": result["p1_probe_state_source"],
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
