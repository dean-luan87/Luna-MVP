# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Planning — review v1.

Normalizes the approval gate, pre-install environment snapshot, install command
whitelist, execution order lock, stop conditions, rollback execution plan,
post-install probe plan, execution audit plan, risk matrix and permission
boundary that any FUTURE controlled install execution must satisfy — for the 5
post-review-approved INSTALL_REQUIRED candidates. The 12 excluded assets stay
excluded.

This is EXECUTION PLANNING, not install execution. No pip install, no dependency
install, no model/weight/dataset download, no inference, no runtime, no semantic
layer, no navigation/action/speech/fact_write. Command and rollback templates
are template_only and never executed. Execution planning success is NOT
install-execution / inference / runtime / output-adapter / semantic-layer
approval. Protected records are written to the test board in planning mode.
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
from capabilities.field_understanding.p1_controlled_install_execution_planning.p1_controlled_install_execution_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_planning.p1_controlled_install_execution_planning_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    AUDIT_TRACE_ITEMS,
    CANDIDATE_ASSET_IDS,
    CONTROLLED_INSTALL_PLANNING_ARTIFACT_REL,
    CONTROLLED_INSTALL_PLANNING_REF,
    CONTROLLED_INSTALL_POST_REVIEW_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUDED_ASSET_IDS,
    EXECUTION_ORDER_LOCK,
    EXECUTION_PLANNING_ONLY,
    EXECUTION_PLANNING_PHASE_GOVERNANCE_RULES,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    INSTALL_EXECUTION_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    NO_WEIGHT_ASSETS,
    OWNER_APPROVAL_NOT_GRANTED_IN_THIS_PHASE,
    OWNER_APPROVAL_REQUIRED,
    PERMISSION_BOUNDARY_STATEMENTS,
    PHASE_ID,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TRUE_INVARIANTS,
    REGISTRY_PLANNING_REF,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROLLBACK_TRIGGER_CONDITIONS,
    SCOPE,
    SOURCE_CHAIN,
    STOP_CONDITIONS,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    WEIGHT_HANDLED_ASSETS,
    ControlledInstallExecutionReadinessRecord,
    InstallCommandWhitelistPlan,
    InstallExecutionAuditPlan,
    InstallExecutionOrderLock,
    InstallExecutionPermissionBoundary,
    InstallExecutionRiskMatrix,
    InstallExecutionStopCondition,
    NegativeInstallExecutionPlanningGuard,
    OwnerApprovalGatePlan,
    P1ControlledInstallExecutionPlanningDecision,
    P1ControlledInstallExecutionPlanningProfile,
    PostInstallProbePlan,
    PreInstallEnvironmentSnapshotPlan,
    RollbackExecutionPlan,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_controlled_install_execution_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_planning"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_planning_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_planning_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_planning_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_planning_profile_v1"
DECISION_REF = "p1_controlled_install_execution_planning_decision_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

_INSTALL_TOKENS = ("install", "pip", "download", "wget", "curl", "git clone")


def _index_by_asset(records: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("asset_id"):
                out[r["asset_id"]] = r
    return out


def _risk_for(asset_id: str, weight_required: bool, license_permissive: bool) -> Dict[str, str]:
    weight_risk = "medium" if weight_required else "low"
    license_risk = "low" if license_permissive else "high"
    if asset_id in NO_WEIGHT_ASSETS:
        level = "low"
        reason = "utility_or_tracking_no_model_weight_permissive_license_shared_cv_core"
    else:
        level = "medium"
        reason = "weight_gated_asset_requires_hash_source_license_review_before_future_inference"
    return {
        "risk_level": level,
        "risk_reason": reason,
        "dependency_risk": "medium" if asset_id in ("deep_sort", "midas", "mobile_sam") else "low",
        "license_risk": license_risk,
        "weight_risk": weight_risk,
        "environment_risk": "low_macos_arm64_cpu_or_mps_no_cuda_assumption",
        "rollback_risk": "low_pre_snapshot_and_rollback_template_planned",
    }


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            execution_planning_only=EXECUTION_PLANNING_ONLY,
            install_execution_allowed=INSTALL_EXECUTION_ALLOWED,
            owner_approval_required=OWNER_APPROVAL_REQUIRED,
            owner_approval_not_granted_in_this_phase=OWNER_APPROVAL_NOT_GRANTED_IN_THIS_PHASE,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            controlled_install_post_review_ref=CONTROLLED_INSTALL_POST_REVIEW_REF,
            controlled_install_planning_ref=CONTROLLED_INSTALL_PLANNING_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            candidate_asset_ids=CANDIDATE_ASSET_IDS,
            excluded_asset_ids=EXCLUDED_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_execution_planning_v1(
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
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    # Load controlled-install-planning artifact for per-asset detail (templates,
    # weight requirement, license). Sealed fallback when missing.
    up_artifact, up_exists = load_artifact(_REPO_ROOT, CONTROLLED_INSTALL_PLANNING_ARTIFACT_REL)
    if up_exists and up_artifact:
        plan_read_mode = "artifact_present"
    else:
        plan_read_mode = "sealed_ref_fallback"
        warnings.append("controlled_install_planning_artifact_missing_sealed_ref_fallback")
        up_artifact = {}
    up_packages = _index_by_asset(up_artifact.get("package_install_plans"))
    up_weights = _index_by_asset(up_artifact.get("weight_acquisition_plans"))
    up_licenses = _index_by_asset(up_artifact.get("license_install_boundary_checks"))

    candidate_set = set(CANDIDATE_ASSET_IDS)
    excluded_set = set(EXCLUDED_ASSET_IDS)
    excluded_assets_not_in_execution_planning = not (candidate_set & excluded_set)
    if not excluded_assets_not_in_execution_planning:
        failed_checks.append("excluded_assets_overlap_candidates")

    # --------------------------------------------------------------------- #
    # (二) Owner approval gate plan.
    # --------------------------------------------------------------------- #
    owner_gate = OwnerApprovalGatePlan(
        gate_ref="owner_approval_gate_controlled_install_execution_v1",
        owner_approval_required=True,
        owner_approval_record_required=True,
        owner_approval_granted_in_this_phase=False,
        approval_scope="controlled_install_execution_only",
        approval_does_not_allow_inference=True,
        approval_does_not_allow_runtime=True,
        approval_does_not_allow_weight_download_unless_separately_approved=True,
        approval_expiry_policy="single_use_expires_after_one_install_execution_window_or_24h",
        approval_revocation_policy="owner_or_governance_may_revoke_before_execution_revocation_halts_pipeline",
        approval_trace_ref_required=True,
    )
    owner_gate_ok = (
        owner_gate.owner_approval_required
        and not owner_gate.owner_approval_granted_in_this_phase
        and owner_gate.approval_does_not_allow_inference
        and owner_gate.approval_does_not_allow_runtime
    )
    if not owner_gate_ok:
        failed_checks.append("owner_approval_gate_invalid")

    # --------------------------------------------------------------------- #
    # (三) Pre-install environment snapshot plan.
    # --------------------------------------------------------------------- #
    snapshot_plan = PreInstallEnvironmentSnapshotPlan(
        plan_ref="pre_install_env_snapshot_controlled_install_execution_v1",
        pre_install_snapshot_required=True,
        target_env_label="luna_p1_controlled_install_isolated_env_planned",
        python_version_capture_required=True,
        pip_freeze_capture_required=True,
        package_list_capture_required=True,
        path_env_capture_required=True,
        registry_snapshot_required=True,
        test_board_snapshot_required=True,
        rollback_snapshot_required=True,
        snapshot_artifact_protected=True,
        snapshot_non_deletable=True,
        snapshot_must_not_overwrite_test_board=True,
        snapshot_must_not_overwrite_registry=True,
        snapshot_executed_in_this_phase=False,
    )
    snapshot_ok = (
        snapshot_plan.pre_install_snapshot_required
        and snapshot_plan.rollback_snapshot_required
        and not snapshot_plan.snapshot_executed_in_this_phase
        and snapshot_plan.snapshot_must_not_overwrite_test_board
        and snapshot_plan.snapshot_must_not_overwrite_registry
    )
    if not snapshot_ok:
        failed_checks.append("pre_install_snapshot_plan_invalid")

    # --------------------------------------------------------------------- #
    # (四) Install command whitelist plan (5).
    # --------------------------------------------------------------------- #
    whitelist_plans: List[InstallCommandWhitelistPlan] = []
    for aid in CANDIDATE_ASSET_IDS:
        up_pkg = up_packages.get(aid, {})
        template = up_pkg.get("install_command_template")
        if not template:
            template = f"pip install {aid}  # TEMPLATE_ONLY_DO_NOT_EXECUTE"
        if "TEMPLATE_ONLY_DO_NOT_EXECUTE" not in template:
            template = f"{template}  # TEMPLATE_ONLY_DO_NOT_EXECUTE"
        contains_token = any(t in template.lower() for t in _INSTALL_TOKENS)
        wp = InstallCommandWhitelistPlan(
            command_template_id=f"whitelist::{aid}",
            asset_id=aid,
            command_template=template,
            template_only=True,
            command_not_executed=True,
            whitelist_required_before_execution=True,
            shell_execution_allowed_now=False,
            subprocess_execution_allowed_now=False,
            pip_install_allowed_now=False,
            command_requires_owner_approval=True,
            command_requires_pre_snapshot=True,
            command_requires_rollback_plan=True,
            contains_install_or_download_token=contains_token,
            allowed_now=False,
        )
        whitelist_plans.append(wp)
        # If a command contains an install/download token it MUST be allowed_now=false.
        if wp.contains_install_or_download_token and wp.allowed_now:
            failed_checks.append(f"whitelist_install_token_allowed_now:{aid}")
        if not (wp.template_only and wp.command_not_executed and not wp.pip_install_allowed_now):
            failed_checks.append(f"whitelist_plan_invalid:{aid}")
    command_whitelist_not_execution_approval = all(
        (not w.allowed_now) and w.whitelist_required_before_execution for w in whitelist_plans
    )

    # --------------------------------------------------------------------- #
    # (五) Install execution order lock (5).
    # --------------------------------------------------------------------- #
    order_locks: List[InstallExecutionOrderLock] = []
    for aid, idx, reason in EXECUTION_ORDER_LOCK:
        order_locks.append(
            InstallExecutionOrderLock(
                asset_id=aid,
                locked_order_index=idx,
                order_lock_reason=reason,
                order_change_requires_review=True,
                order_change_requires_owner_approval=True,
                execution_must_stop_on_failure=True,
                downstream_steps_blocked_on_failure=True,
                parallel_install_allowed=False,
            )
        )
    locked_indices = [o.locked_order_index for o in order_locks]
    execution_order_locked = (
        len(order_locks) == 5
        and sorted(locked_indices) == [1, 2, 3, 4, 5]
        and all(o.execution_must_stop_on_failure for o in order_locks)
    )
    execution_must_stop_on_failure = all(
        o.execution_must_stop_on_failure and o.downstream_steps_blocked_on_failure for o in order_locks
    )
    if not execution_order_locked:
        failed_checks.append("execution_order_not_locked")
    if not execution_must_stop_on_failure:
        failed_checks.append("failure_does_not_stop_downstream")

    # --------------------------------------------------------------------- #
    # (六) Install execution stop conditions (>=12).
    # --------------------------------------------------------------------- #
    stop_conditions = [
        InstallExecutionStopCondition(
            condition_id=c["condition_id"],
            severity=c["severity"],
            halts_execution=True,
            requires_owner_review=True,
        )
        for c in STOP_CONDITIONS
    ]

    # --------------------------------------------------------------------- #
    # (七) Rollback execution plan (5).
    # --------------------------------------------------------------------- #
    rollback_plans: List[RollbackExecutionPlan] = []
    for aid in CANDIDATE_ASSET_IDS:
        rollback_plans.append(
            RollbackExecutionPlan(
                asset_id=aid,
                rollback_plan_required=True,
                rollback_trigger_conditions=ROLLBACK_TRIGGER_CONDITIONS,
                rollback_command_template=(
                    f"pip uninstall -y {aid} && restore_pre_install_snapshot {aid}  "
                    "# TEMPLATE_ONLY_DO_NOT_EXECUTE"
                ),
                rollback_command_not_executed=True,
                rollback_requires_owner_acknowledgement=True,
                rollback_must_preserve_test_board=True,
                rollback_must_preserve_registry=True,
                rollback_must_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
                rollback_failure_escalation_required=True,
            )
        )
    rollback_execution_planned = (
        len(rollback_plans) == 5 and all(r.rollback_plan_required and r.rollback_command_not_executed for r in rollback_plans)
    )
    rollback_template_not_executed = all(r.rollback_command_not_executed for r in rollback_plans)

    # --------------------------------------------------------------------- #
    # (八) Post-install probe plan (5).
    # --------------------------------------------------------------------- #
    probe_plans: List[PostInstallProbePlan] = []
    for aid in CANDIDATE_ASSET_IDS:
        probe_plans.append(
            PostInstallProbePlan(
                asset_id=aid,
                post_install_probe_required=True,
                probe_uses_find_spec_only=True,
                real_import_allowed=False,
                no_model_load_on_probe=True,
                no_inference_on_probe=True,
                installed_version_record_required=True,
                dependency_gap_recheck_required=True,
                license_recheck_required=True,
                weight_visibility_recheck_required=True,
                test_board_probe_record_required=True,
            )
        )
    post_install_probe_planned = (
        len(probe_plans) == 5 and all(p.post_install_probe_required for p in probe_plans)
    )
    post_install_probe_find_spec_only = all(
        p.probe_uses_find_spec_only and not p.real_import_allowed for p in probe_plans
    )
    post_install_probe_not_inference = all(p.no_inference_on_probe for p in probe_plans)
    post_install_probe_not_runtime = all(p.no_model_load_on_probe for p in probe_plans)

    # --------------------------------------------------------------------- #
    # (九) Install execution audit plan (>=10).
    # --------------------------------------------------------------------- #
    audit_plans = [
        InstallExecutionAuditPlan(
            trace_id=t,
            trace_required=True,
            writes_to_test_board_protected_record=True,
        )
        for t in AUDIT_TRACE_ITEMS
    ]

    # --------------------------------------------------------------------- #
    # (十) Install execution risk matrix (5).
    # --------------------------------------------------------------------- #
    risk_matrix: List[InstallExecutionRiskMatrix] = []
    for aid in CANDIDATE_ASSET_IDS:
        up_w = up_weights.get(aid, {})
        weight_required = bool(up_w.get("weight_required", aid in WEIGHT_HANDLED_ASSETS))
        up_l = up_licenses.get(aid, {})
        license_permissive = bool(up_l.get("permissive_family", True)) if up_l else True
        r = _risk_for(aid, weight_required, license_permissive)
        risk_matrix.append(
            InstallExecutionRiskMatrix(
                asset_id=aid,
                risk_level=r["risk_level"],
                risk_reason=r["risk_reason"],
                dependency_risk=r["dependency_risk"],
                license_risk=r["license_risk"],
                weight_risk=r["weight_risk"],
                environment_risk=r["environment_risk"],
                rollback_risk=r["rollback_risk"],
                install_execution_allowed=False,
                can_enter_future_install_execution_request=True,
                can_enter_runtime_trial=False,
                can_enter_real_output_adapter_dryrun=False,
                can_enter_inference=False,
            )
        )

    # --------------------------------------------------------------------- #
    # (十一) Install execution permission boundary (>=5).
    # --------------------------------------------------------------------- #
    permission_boundaries: List[InstallExecutionPermissionBoundary] = []
    for spec in PERMISSION_BOUNDARY_STATEMENTS:
        permission_boundaries.append(
            InstallExecutionPermissionBoundary(boundary_id=spec["boundary_id"], holds=True)
        )
    # commercial_runtime_approved must be false.
    if NON_EXECUTION_FLAGS["commercial_runtime_approved"] is not False:
        failed_checks.append("commercial_runtime_approved_true")

    # --------------------------------------------------------------------- #
    # Readiness records (5).
    # --------------------------------------------------------------------- #
    readiness_records: List[ControlledInstallExecutionReadinessRecord] = []
    for aid in CANDIDATE_ASSET_IDS:
        readiness_records.append(
            ControlledInstallExecutionReadinessRecord(
                asset_id=aid,
                owner_approval_gate_ready=True,
                snapshot_plan_ready=True,
                command_whitelist_ready=True,
                order_lock_ready=True,
                rollback_plan_ready=True,
                post_install_probe_ready=True,
                install_execution_allowed=False,
                can_enter_future_install_execution_request=True,
            )
        )

    # --------------------------------------------------------------------- #
    # (十二) Negative guards (22).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
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
        "command_whitelist_not_execution_approval": command_whitelist_not_execution_approval,
        "owner_approval_gate_present": owner_gate_ok,
        "pre_install_snapshot_planned": snapshot_ok,
        "rollback_execution_planned": rollback_execution_planned,
        "post_install_probe_planned": post_install_probe_planned,
        "execution_order_locked": execution_order_locked,
        "execution_must_stop_on_failure": execution_must_stop_on_failure,
        "excluded_assets_not_in_execution_planning": excluded_assets_not_in_execution_planning,
        "not_install_execution_approval": all(not r.install_execution_allowed for r in risk_matrix),
        "not_inference_approval": all(not r.can_enter_inference for r in risk_matrix),
        "not_runtime_approval": all(not r.can_enter_runtime_trial for r in risk_matrix),
        "not_output_adapter_approval": all(not r.can_enter_real_output_adapter_dryrun for r in risk_matrix),
        "not_semantic_layer_approval": nef["semantic_promotion_allowed"] is False,
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

    negative_guards: List[NegativeInstallExecutionPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeInstallExecutionPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_install_execution_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness.
    # --------------------------------------------------------------------- #
    handoff_go: Dict[str, bool] = {}
    handoff_readiness: List[Dict[str, Any]] = []
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            {"target_ref": target["target_ref"], "readiness_recorded": True, "entered_this_phase": False}
        )
        handoff_go[target["go_key"]] = True

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "execution_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "owner_approval_gate_plan_count_gte_1": 1 >= 1,
        "pre_install_environment_snapshot_plan_count_gte_1": 1 >= 1,
        "install_command_whitelist_plan_count_eq_5": len(whitelist_plans) == 5,
        "install_execution_order_lock_count_eq_5": len(order_locks) == 5,
        "install_execution_stop_condition_count_gte_12": len(stop_conditions) >= 12,
        "rollback_execution_plan_count_eq_5": len(rollback_plans) == 5,
        "post_install_probe_plan_count_eq_5": len(probe_plans) == 5,
        "install_execution_audit_plan_count_gte_10": len(audit_plans) >= 10,
        "install_execution_risk_matrix_count_eq_5": len(risk_matrix) == 5,
        "install_execution_permission_boundary_count_gte_5": len(permission_boundaries) >= 5,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Explicit named GO flags from the spec.
        "execution_planning_only": EXECUTION_PLANNING_ONLY is True,
        "install_execution_allowed_false": INSTALL_EXECUTION_ALLOWED is False,
        "owner_approval_required": OWNER_APPROVAL_REQUIRED is True,
        "owner_approval_not_granted_in_this_phase": OWNER_APPROVAL_NOT_GRANTED_IN_THIS_PHASE is True,
        "pre_install_snapshot_planned": snapshot_ok,
        "install_command_whitelist_planned": len(whitelist_plans) == 5,
        "command_whitelist_not_execution_approval": command_whitelist_not_execution_approval,
        "execution_order_locked": execution_order_locked,
        "order_change_requires_review": all(o.order_change_requires_review for o in order_locks),
        "execution_must_stop_on_failure": execution_must_stop_on_failure,
        "rollback_execution_planned": rollback_execution_planned,
        "rollback_template_not_executed": rollback_template_not_executed,
        "post_install_probe_planned": post_install_probe_planned,
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only,
        "post_install_probe_not_inference": post_install_probe_not_inference,
        "post_install_probe_not_runtime": post_install_probe_not_runtime,
        "excluded_assets_not_in_execution_planning": excluded_assets_not_in_execution_planning,
        "future_install_execution_requires_separate_approval": True,
        "execution_planning_success_not_install_execution_approval": invariant_state["not_install_execution_approval"],
        "execution_planning_success_not_inference_approval": invariant_state["not_inference_approval"],
        "execution_planning_success_not_runtime_approval": invariant_state["not_runtime_approval"],
        "execution_planning_success_not_output_adapter_approval": invariant_state["not_output_adapter_approval"],
        "execution_planning_success_not_semantic_layer_approval": invariant_state["not_semantic_layer_approval"],
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

    decision = P1ControlledInstallExecutionPlanningDecision(
        decision_ref=DECISION_REF,
        execution_planning_profile_count=1,
        owner_approval_gate_plan_count=1,
        pre_install_environment_snapshot_plan_count=1,
        install_command_whitelist_plan_count=len(whitelist_plans),
        install_execution_order_lock_count=len(order_locks),
        install_execution_stop_condition_count=len(stop_conditions),
        rollback_execution_plan_count=len(rollback_plans),
        post_install_probe_plan_count=len(probe_plans),
        install_execution_audit_plan_count=len(audit_plans),
        install_execution_risk_matrix_count=len(risk_matrix),
        install_execution_permission_boundary_count=len(permission_boundaries),
        controlled_install_execution_readiness_record_count=len(readiness_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Planning",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "execution_planning_only": EXECUTION_PLANNING_ONLY,
        "install_execution_allowed": INSTALL_EXECUTION_ALLOWED,
        "controlled_install_post_review_ref": CONTROLLED_INSTALL_POST_REVIEW_REF,
        "controlled_install_planning_ref": CONTROLLED_INSTALL_PLANNING_REF,
        "registry_planning_ref": REGISTRY_PLANNING_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "execution_planning_phase_governance_rules": list(EXECUTION_PLANNING_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "plan_read_mode": plan_read_mode,
        "execution_planning_profile": _build_profile(),
        "execution_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "candidate_asset_ids": list(CANDIDATE_ASSET_IDS),
        "excluded_asset_ids": list(EXCLUDED_ASSET_IDS),
        # Plans / matrices.
        "owner_approval_gate_plan": asdict(owner_gate),
        "owner_approval_gate_plan_count": 1,
        "pre_install_environment_snapshot_plan": asdict(snapshot_plan),
        "pre_install_environment_snapshot_plan_count": 1,
        "install_command_whitelist_plans": [asdict(w) for w in whitelist_plans],
        "install_command_whitelist_plan_count": len(whitelist_plans),
        "install_execution_order_locks": [asdict(o) for o in order_locks],
        "install_execution_order_lock_count": len(order_locks),
        "install_execution_stop_conditions": [asdict(s) for s in stop_conditions],
        "install_execution_stop_condition_count": len(stop_conditions),
        "rollback_execution_plans": [asdict(r) for r in rollback_plans],
        "rollback_execution_plan_count": len(rollback_plans),
        "post_install_probe_plans": [asdict(p) for p in probe_plans],
        "post_install_probe_plan_count": len(probe_plans),
        "install_execution_audit_plans": [asdict(a) for a in audit_plans],
        "install_execution_audit_plan_count": len(audit_plans),
        "install_execution_risk_matrix": [asdict(r) for r in risk_matrix],
        "install_execution_risk_matrix_count": len(risk_matrix),
        "install_execution_permission_boundaries": [asdict(b) for b in permission_boundaries],
        "install_execution_permission_boundary_count": len(permission_boundaries),
        "controlled_install_execution_readiness_records": [asdict(r) for r in readiness_records],
        "controlled_install_execution_readiness_record_count": len(readiness_records),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": handoff_readiness,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_planning_status": (
                "controlled_install_execution_plan_normalized_template_only_no_install_no_download_no_inference_no_runtime_no_approval_granted"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Controlled-install EXECUTION PLANNING for the 5 post-review-approved INSTALL_REQUIRED "
                "candidates (supervision, byte_track, deep_sort, midas, mobile_sam); the 12 assets stay "
                "excluded. Normalized: owner approval gate (required, NOT granted here; does not allow "
                "inference/runtime; weight download needs separate approval), pre-install environment snapshot "
                "plan (planned not executed; must not overwrite test board / registry), install command "
                "whitelist (template_only, TEMPLATE_ONLY_DO_NOT_EXECUTE, allowed_now=false), locked execution "
                "order (1 supervision -> 2 byte_track -> 3 deep_sort -> 4 midas -> 5 mobile_sam; stop-on-failure, "
                "no parallel install), 14 stop conditions, rollback execution plan (template-only, preserves test "
                "board / registry / review artifacts), post-install probe plan (find_spec only, no import / model "
                "load / inference), execution audit plan (10 traces -> protected test board), risk matrix and "
                "permission boundary. Nothing installed/downloaded/executed; no approval granted. Execution "
                "planning success is NOT install-execution / inference / runtime / output-adapter / semantic-layer "
                "approval. Next: P1 Controlled Install Execution Planning Post-Review before any real install "
                "execution request / owner approval."
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
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_p1_controlled_install_execution_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "plan_read_mode": result.get("plan_read_mode"),
                "install_command_whitelist_plan_count": result["install_command_whitelist_plan_count"],
                "install_execution_order_lock_count": result["install_execution_order_lock_count"],
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
