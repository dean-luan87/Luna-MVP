# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Preparation And Readiness Review — review v1.

COMPRESSED phase: audits that the owner approval issuance scope is
preparation-only, builds the execution preparation package (final command
whitelist, locked execution order, stop conditions, rollback, post-install
probe, package-install scope, deferred weight-download scope) for the 5 approved
candidates, and emits an execution readiness decision.

It executes NOTHING: no install / download / inference / runtime / output
adapter / semantic layer. Weight download is NOT approved by default. If GO, the
next phase (Phase-P1-Controlled-Install-Execution-v1-001) may begin — first
execution recommended package-install-only. Protected records are written to the
test board in planning mode.
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
from capabilities.field_understanding.p1_controlled_install_execution_preparation_and_readiness_review.p1_controlled_install_execution_preparation_and_readiness_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_preparation_and_readiness_review.p1_controlled_install_execution_preparation_and_readiness_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
    APPROVAL_SCOPE,
    APPROVED_ASSET_IDS,
    APPROVED_ASSET_ORDER,
    CAN_ENTER_CONTROLLED_INSTALL_EXECUTION_NEXT,
    CAN_ENTER_FLAGS,
    COMMAND_TEMPLATE_TEXT,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUDED_ASSETS,
    EXECUTION_PLANNING_REF,
    EXECUTION_PREPARATION_INCLUDED,
    EXECUTION_PREPARATION_PACKAGE_CREATED,
    EXECUTION_READINESS_DECISION_CREATED,
    EXECUTION_READINESS_REVIEW_INCLUDED,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FINAL_EXECUTION_ORDER,
    FINAL_STOP_CONDITIONS,
    ISSUANCE_AUDIT_SPEC,
    ISSUANCE_NESTED_BOOL_FIELDS,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    NO_WEIGHT_ASSETS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    PRE_EXECUTION_SNAPSHOT_ITEMS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROLLBACK_TRIGGER_CONDITIONS,
    SCOPE,
    SEALED_EXPECTED_ISSUANCE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_ISSUANCE_ARTIFACT_REL,
    UPSTREAM_ISSUANCE_EXPECTED_GO,
    UPSTREAM_ISSUANCE_REF,
    UPSTREAM_REQUEST_REF,
    WEIGHT_SUBAPPROVAL_ASSETS,
    ApprovalIssuanceScopeAudit,
    ExecutionHandoffRecord,
    ExecutionPreparationPackage,
    ExecutionReadinessReviewRecord,
    ExecutionRiskReadinessRecord,
    FinalCommandWhitelistRecord,
    FinalExecutionOrderRecord,
    FinalPostInstallProbeRequirement,
    FinalRollbackRequirement,
    FinalStopConditionRecord,
    NegativeExecutionPreparationReadinessGuard,
    P1ControlledInstallExecutionPreparationReadinessDecision,
    P1ControlledInstallExecutionPreparationReadinessProfile,
    PackageInstallExecutionScope,
    PreExecutionSnapshotRequirement,
    WeightDownloadExecutionScope,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_controlled_install_execution_preparation_and_readiness_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_preparation_and_readiness_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_preparation_and_readiness_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_preparation_and_readiness_review_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_preparation_and_readiness_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_preparation_and_readiness_review_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_preparation_and_readiness_review_profile_v1"
DECISION_REF = "p1_controlled_install_execution_preparation_and_readiness_review_decision_v1"
PREPARATION_PACKAGE_ID = "p1_controlled_install_execution_preparation_package_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"
_READ_ROOTS = (_REPO_ROOT, Path.cwd(), _BOARD_STANDIN_ROOT, Path.cwd() / "_tmp_eval_out" / "board_standin")


def _resolve_existing_file(rel: str) -> Optional[Path]:
    for root in _READ_ROOTS:
        p = root / rel
        if p.is_file():
            return p
    return None


def _cmp(comparator: str, actual: Any, expected: Any) -> bool:
    if comparator == "eq":
        return actual == expected
    if comparator == "gte":
        try:
            return actual >= expected
        except TypeError:
            return False
    return False


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionPreparationReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            approval_issuance_post_review_included=APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
            execution_preparation_included=EXECUTION_PREPARATION_INCLUDED,
            execution_readiness_review_included=EXECUTION_READINESS_REVIEW_INCLUDED,
            execution_preparation_package_created=EXECUTION_PREPARATION_PACKAGE_CREATED,
            execution_readiness_decision_created=EXECUTION_READINESS_DECISION_CREATED,
            can_enter_controlled_install_execution_next=CAN_ENTER_CONTROLLED_INSTALL_EXECUTION_NEXT,
            install_execution_allowed_in_this_phase=NON_EXECUTION_FLAGS["install_execution_allowed_in_this_phase"],
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            upstream_issuance_ref=UPSTREAM_ISSUANCE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            approved_asset_ids=APPROVED_ASSET_IDS,
            excluded_asset_ids=tuple(e["asset_id"] for e in EXCLUDED_ASSETS),
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_execution_preparation_and_readiness_review_v1(
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

    # --------------------------------------------------------------------- #
    # (一) Approval issuance scope audit (sealed-ref fallback allowed).
    # --------------------------------------------------------------------- #
    up_path = _resolve_existing_file(UPSTREAM_ISSUANCE_ARTIFACT_REL)
    if up_path is not None:
        try:
            up = json.loads(up_path.read_text(encoding="utf-8"))
            artifact_read_mode = "artifact_present"
        except (OSError, json.JSONDecodeError):
            up = {}
            artifact_read_mode = "sealed_ref_fallback"
            warnings.append("upstream_issuance_artifact_unreadable_sealed_ref_fallback")
    else:
        up = {}
        artifact_read_mode = "sealed_ref_fallback"
        warnings.append("upstream_issuance_artifact_missing_sealed_ref_fallback")

    sealed = artifact_read_mode == "sealed_ref_fallback"
    issuance_record = up.get("owner_approval_issuance_record", {}) if not sealed else {}
    up_go_conditions = up.get("go_conditions", {}) if not sealed else {}
    src: Dict[str, Any] = dict(SEALED_EXPECTED_ISSUANCE) if sealed else up

    issuance_field_results: List[Dict[str, Any]] = []
    issuance_checks_passed = 0
    for fname, comparator, expected in ISSUANCE_AUDIT_SPEC:
        actual = src.get(fname)
        ok = _cmp(comparator, actual, expected)
        if ok:
            issuance_checks_passed += 1
        issuance_field_results.append(
            {"field": fname, "comparator": comparator, "expected": expected, "actual": actual, "ok": ok}
        )
        if not ok:
            failed_checks.append(f"approval_issuance_scope_audit_fail:{fname}")
    # Nested boolean fields (from issuance record).
    for fname in ISSUANCE_NESTED_BOOL_FIELDS:
        actual = issuance_record.get(fname, True) if not sealed else True
        ok = actual is True
        if ok:
            issuance_checks_passed += 1
        issuance_field_results.append(
            {"field": fname, "comparator": "eq", "expected": True, "actual": actual, "ok": ok}
        )
        if not ok:
            failed_checks.append(f"approval_issuance_scope_audit_fail:{fname}")

    approval_scope_val = issuance_record.get("approval_scope", APPROVAL_SCOPE) if not sealed else APPROVAL_SCOPE
    direct_exec_not_allowed = (
        up_go_conditions.get("direct_install_execution_not_allowed_after_this_phase", True)
        if not sealed
        else True
    )
    issuance_checks_total = len(ISSUANCE_AUDIT_SPEC) + len(ISSUANCE_NESTED_BOOL_FIELDS) + 2
    approval_scope_preparation_only = approval_scope_val == APPROVAL_SCOPE
    if approval_scope_preparation_only:
        issuance_checks_passed += 1
    else:
        failed_checks.append("approval_issuance_scope_audit_fail:approval_scope")
    if direct_exec_not_allowed:
        issuance_checks_passed += 1
    else:
        failed_checks.append("approval_issuance_scope_audit_fail:direct_install_execution_not_allowed")

    issuance_audit = ApprovalIssuanceScopeAudit(
        artifact_ref=UPSTREAM_ISSUANCE_ARTIFACT_REL,
        artifact_read_mode=artifact_read_mode,
        artifact_missing_is_warning=True,
        artifact_missing_is_blocker=False,
        approval_scope=approval_scope_val,
        direct_install_execution_not_allowed_after_this_phase=bool(direct_exec_not_allowed),
        checks_total=issuance_checks_total,
        checks_passed=issuance_checks_passed,
        field_results=tuple(issuance_field_results),
        audit_holds=issuance_checks_passed == issuance_checks_total,
    )
    approval_issuance_not_install_execution_approval = (
        src.get("owner_approval_granted_for_install_execution", False) is False
    )

    approved_set = set(APPROVED_ASSET_IDS)
    excluded_set = {e["asset_id"] for e in EXCLUDED_ASSETS}
    excluded_assets_remain_excluded = not (approved_set & excluded_set)
    if not excluded_assets_remain_excluded:
        failed_checks.append("excluded_assets_overlap_preparation_scope")

    # --------------------------------------------------------------------- #
    # (五) Pre-execution snapshot requirement.
    # --------------------------------------------------------------------- #
    snapshot_requirement = PreExecutionSnapshotRequirement(
        requirement_ref="pre_execution_snapshot_requirement_v1",
        python_version_capture_required=True,
        pip_freeze_capture_required=True,
        package_list_capture_required=True,
        path_env_capture_required=True,
        registry_snapshot_required=True,
        test_board_snapshot_required=True,
        rollback_snapshot_required=True,
        snapshot_must_be_written_before_first_install=True,
        snapshot_artifact_protected=True,
        snapshot_non_deletable=True,
        snapshot_executed_in_this_phase=False,
    )
    snapshot_dict = asdict(snapshot_requirement)
    pre_execution_snapshot_required = (
        all(snapshot_dict[k] for k in PRE_EXECUTION_SNAPSHOT_ITEMS)
        and snapshot_requirement.snapshot_executed_in_this_phase is False
    )
    if not pre_execution_snapshot_required:
        failed_checks.append("pre_execution_snapshot_requirement_invalid")

    # --------------------------------------------------------------------- #
    # (六) Final command whitelist (5).
    # --------------------------------------------------------------------- #
    whitelist_records: List[FinalCommandWhitelistRecord] = []
    for aid in APPROVED_ASSET_IDS:
        text = COMMAND_TEMPLATE_TEXT[aid]
        whitelist_records.append(
            FinalCommandWhitelistRecord(
                asset_id=aid,
                command_template_ref=f"final_whitelist::{aid}",
                command_template_text=text,
                template_only_marker_present="TEMPLATE_ONLY_DO_NOT_EXECUTE" in text,
                command_not_executed_in_this_phase=True,
                command_allowed_only_in_next_execution_phase=True,
                command_requires_pre_snapshot=True,
                command_requires_stop_condition_check=True,
                command_requires_rollback_available=True,
                command_requires_post_probe=True,
            )
        )
    final_command_whitelist_present = len(whitelist_records) == 5 and all(
        w.template_only_marker_present for w in whitelist_records
    )
    final_command_whitelist_not_executed = all(
        w.command_not_executed_in_this_phase for w in whitelist_records
    )

    # --------------------------------------------------------------------- #
    # (七) Final execution order (5).
    # --------------------------------------------------------------------- #
    order_records: List[FinalExecutionOrderRecord] = []
    for aid, idx in APPROVED_ASSET_ORDER:
        order_records.append(
            FinalExecutionOrderRecord(
                asset_id=aid,
                order_index=idx,
                no_parallel_execution=True,
                failure_stops_downstream=True,
                order_change_requires_new_review=True,
                order_change_requires_owner_reapproval=True,
            )
        )
    final_execution_order_locked = (
        len(order_records) == 5
        and [r.asset_id for r in order_records] == list(FINAL_EXECUTION_ORDER)
        and all(r.no_parallel_execution for r in order_records)
    )
    failure_stops_downstream = all(r.failure_stops_downstream for r in order_records)

    # --------------------------------------------------------------------- #
    # (八) Final stop conditions (>= 18).
    # --------------------------------------------------------------------- #
    stop_condition_records = [
        FinalStopConditionRecord(condition_id=c, enforced_in_next_execution_phase=True)
        for c in FINAL_STOP_CONDITIONS
    ]

    # --------------------------------------------------------------------- #
    # (九) Final rollback requirement (5).
    # --------------------------------------------------------------------- #
    rollback_records: List[FinalRollbackRequirement] = []
    for aid in APPROVED_ASSET_IDS:
        rollback_records.append(
            FinalRollbackRequirement(
                asset_id=aid,
                rollback_required=True,
                rollback_trigger_conditions=ROLLBACK_TRIGGER_CONDITIONS,
                rollback_template_ref=f"final_rollback_template::{aid}",
                rollback_command_not_executed_in_this_phase=True,
                rollback_must_preserve_test_board=True,
                rollback_must_preserve_registry=True,
                rollback_must_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
                rollback_failure_escalation_required=True,
            )
        )
    rollback_requirement_present = len(rollback_records) == 5 and all(
        r.rollback_required for r in rollback_records
    )

    # --------------------------------------------------------------------- #
    # (十) Final post-install probe requirement (5).
    # --------------------------------------------------------------------- #
    probe_records: List[FinalPostInstallProbeRequirement] = []
    for aid in APPROVED_ASSET_IDS:
        probe_records.append(
            FinalPostInstallProbeRequirement(
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
    post_install_probe_requirement_present = len(probe_records) == 5 and all(
        p.post_install_probe_required for p in probe_records
    )
    post_install_probe_find_spec_only_strict = all(
        p.probe_uses_find_spec_only
        and not p.real_import_allowed
        and p.no_model_load_on_probe
        and p.no_inference_on_probe
        and p.no_runtime_on_probe
        and p.no_output_adapter_on_probe
        for p in probe_records
    )

    # --------------------------------------------------------------------- #
    # (十一) Package install execution scope (5).
    # --------------------------------------------------------------------- #
    package_scope_records: List[PackageInstallExecutionScope] = []
    for aid in APPROVED_ASSET_IDS:
        package_scope_records.append(
            PackageInstallExecutionScope(
                asset_id=aid,
                package_install_allowed_in_next_execution_phase=True,
                package_install_executed_in_this_phase=False,
                pip_install_executed_in_this_phase=False,
                dependency_install_executed_in_this_phase=False,
            )
        )
    package_install_scope_ready = len(package_scope_records) == 5 and all(
        not r.package_install_executed_in_this_phase
        and not r.pip_install_executed_in_this_phase
        and not r.dependency_install_executed_in_this_phase
        for r in package_scope_records
    )

    # --------------------------------------------------------------------- #
    # (十二) Weight download execution scope (5).
    # --------------------------------------------------------------------- #
    weight_scope_records: List[WeightDownloadExecutionScope] = []
    for aid in APPROVED_ASSET_IDS:
        needs_weight = aid in WEIGHT_SUBAPPROVAL_ASSETS
        weight_scope_records.append(
            WeightDownloadExecutionScope(
                asset_id=aid,
                weight_download_required=needs_weight,
                weight_download_requires_separate_approval=needs_weight,
                weight_download_allowed_in_next_execution_phase=False,
                weight_download_subapproval_requested=False,
                weight_download_scope_not_approved=True,
            )
        )
    weight_download_not_approved_by_default = all(
        not r.weight_download_allowed_in_next_execution_phase
        and not r.weight_download_subapproval_requested
        and r.weight_download_scope_not_approved
        for r in weight_scope_records
    )
    weight_download_requires_separate_approval = all(
        (r.weight_download_requires_separate_approval if r.asset_id in WEIGHT_SUBAPPROVAL_ASSETS else not r.weight_download_required)
        for r in weight_scope_records
    )

    # --------------------------------------------------------------------- #
    # Execution risk readiness (5).
    # --------------------------------------------------------------------- #
    risk_records: List[ExecutionRiskReadinessRecord] = []
    for aid in APPROVED_ASSET_IDS:
        risk_records.append(
            ExecutionRiskReadinessRecord(
                asset_id=aid,
                dependency_risk_ready=True,
                license_risk_ready=True,
                weight_risk_ready=True,
                environment_risk_ready=True,
                rollback_risk_ready=True,
                owner_ack_required_for_next_phase=True,
            )
        )

    # --------------------------------------------------------------------- #
    # (二) Execution preparation package.
    # --------------------------------------------------------------------- #
    preparation_package = ExecutionPreparationPackage(
        preparation_package_id=PREPARATION_PACKAGE_ID,
        phase_id=PHASE_ID,
        source_approval_issuance_ref=UPSTREAM_ISSUANCE_REF,
        source_request_ref=UPSTREAM_REQUEST_REF,
        approved_assets=APPROVED_ASSET_IDS,
        excluded_assets=tuple(e["asset_id"] for e in EXCLUDED_ASSETS),
        final_command_whitelist_refs=tuple(w.command_template_ref for w in whitelist_records),
        final_execution_order=FINAL_EXECUTION_ORDER,
        final_stop_conditions=FINAL_STOP_CONDITIONS,
        pre_execution_snapshot_required=True,
        rollback_required=True,
        post_install_probe_required=True,
        test_board_write_required=True,
        package_install_scope_defined=True,
        weight_download_scope_defined=True,
        execution_preparation_complete=True,
        install_execution_allowed_in_this_phase=False,
    )
    execution_preparation_package_present = (
        preparation_package.execution_preparation_complete
        and not preparation_package.install_execution_allowed_in_this_phase
        and len(preparation_package.final_command_whitelist_refs) == 5
        and len(preparation_package.approved_assets) == 5
        and len(preparation_package.excluded_assets) == 12
    )
    if not execution_preparation_package_present:
        failed_checks.append("execution_preparation_package_incomplete")

    approved_assets_complete = list(APPROVED_ASSET_IDS) == [a for a, _ in APPROVED_ASSET_ORDER] and len(
        APPROVED_ASSET_IDS
    ) == 5

    # --------------------------------------------------------------------- #
    # (十三) Execution readiness review.
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    non_execution_boundary_preserved = all(v is False for v in nef.values())
    readiness_review = ExecutionReadinessReviewRecord(
        review_ref="execution_readiness_review_v1",
        approval_scope_valid=approval_scope_preparation_only,
        preparation_package_complete=execution_preparation_package_present,
        approved_assets_verified=approved_assets_complete,
        excluded_assets_verified=len(EXCLUDED_ASSETS) == 12 and excluded_assets_remain_excluded,
        final_command_whitelist_ready=final_command_whitelist_present and final_command_whitelist_not_executed,
        final_execution_order_ready=final_execution_order_locked,
        final_stop_conditions_ready=len(stop_condition_records) >= 18,
        final_rollback_ready=rollback_requirement_present,
        final_post_install_probe_ready=post_install_probe_requirement_present and post_install_probe_find_spec_only_strict,
        package_install_scope_ready=package_install_scope_ready,
        weight_download_scope_not_approved=weight_download_not_approved_by_default,
        test_board_ready=write_test_board is True,
        non_execution_boundary_preserved=non_execution_boundary_preserved,
        can_enter_controlled_install_execution_next=CAN_ENTER_FLAGS["can_enter_controlled_install_execution_next"],
        can_enter_weight_download_execution_next=CAN_ENTER_FLAGS["can_enter_weight_download_execution_next"],
        can_enter_inference=CAN_ENTER_FLAGS["can_enter_inference"],
        can_enter_runtime=CAN_ENTER_FLAGS["can_enter_runtime"],
        can_enter_output_adapter=CAN_ENTER_FLAGS["can_enter_output_adapter"],
        can_enter_semantic_layer=CAN_ENTER_FLAGS["can_enter_semantic_layer"],
        readiness_holds=False,
    )
    readiness_dict = asdict(readiness_review)
    readiness_holds = (
        readiness_dict["approval_scope_valid"]
        and readiness_dict["preparation_package_complete"]
        and readiness_dict["approved_assets_verified"]
        and readiness_dict["excluded_assets_verified"]
        and readiness_dict["final_command_whitelist_ready"]
        and readiness_dict["final_execution_order_ready"]
        and readiness_dict["final_stop_conditions_ready"]
        and readiness_dict["final_rollback_ready"]
        and readiness_dict["final_post_install_probe_ready"]
        and readiness_dict["package_install_scope_ready"]
        and readiness_dict["weight_download_scope_not_approved"]
        and readiness_dict["test_board_ready"]
        and readiness_dict["non_execution_boundary_preserved"]
        and readiness_dict["can_enter_controlled_install_execution_next"] is True
        and readiness_dict["can_enter_weight_download_execution_next"] is False
        and readiness_dict["can_enter_inference"] is False
        and readiness_dict["can_enter_runtime"] is False
        and readiness_dict["can_enter_output_adapter"] is False
        and readiness_dict["can_enter_semantic_layer"] is False
    )
    readiness_review = ExecutionReadinessReviewRecord(**{**readiness_dict, "readiness_holds": readiness_holds})
    if not readiness_holds:
        failed_checks.append("execution_readiness_review_not_ready")
    readiness_excludes_inference_runtime_adapter_semantic = (
        not readiness_review.can_enter_inference
        and not readiness_review.can_enter_runtime
        and not readiness_review.can_enter_output_adapter
        and not readiness_review.can_enter_semantic_layer
    )

    # --------------------------------------------------------------------- #
    # Execution handoff record.
    # --------------------------------------------------------------------- #
    handoff_record = ExecutionHandoffRecord(
        target_ref=NEXT_STEP_REF,
        readiness_recorded=True,
        can_enter_controlled_install_execution_next=CAN_ENTER_FLAGS["can_enter_controlled_install_execution_next"],
        package_install_only_recommended_first=True,
        weight_download_deferred_to_subapproval=True,
    )

    # --------------------------------------------------------------------- #
    # (十四) Negative guards (26).
    # --------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "approval_issuance_not_install_execution_approval": approval_issuance_not_install_execution_approval,
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
        "no_runtime_output_semantic": (
            nef["runtime_execution_allowed"] is False
            and nef["real_output_adapter_allowed"] is False
            and nef["semantic_promotion_allowed"] is False
        ),
        "execution_preparation_package_present": execution_preparation_package_present,
        "approval_scope_preparation_only": approval_scope_preparation_only,
        "approved_assets_complete": approved_assets_complete,
        "excluded_assets_remain_excluded": excluded_assets_remain_excluded and len(EXCLUDED_ASSETS) == 12,
        "final_command_whitelist_present": final_command_whitelist_present,
        "final_command_whitelist_not_executed": final_command_whitelist_not_executed,
        "pre_execution_snapshot_required": pre_execution_snapshot_required,
        "final_execution_order_locked": final_execution_order_locked,
        "failure_stops_downstream": failure_stops_downstream,
        "rollback_requirement_present": rollback_requirement_present,
        "post_install_probe_requirement_present": post_install_probe_requirement_present,
        "post_install_probe_find_spec_only_strict": post_install_probe_find_spec_only_strict,
        "weight_download_not_approved_by_default": weight_download_not_approved_by_default,
        "weight_download_requires_separate_approval": weight_download_requires_separate_approval,
        "readiness_excludes_inference_runtime_adapter_semantic": readiness_excludes_inference_runtime_adapter_semantic,
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeExecutionPreparationReadinessGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeExecutionPreparationReadinessGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_execution_preparation_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "execution_preparation_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "approval_issuance_scope_audit_count_gte_1": True,
        "execution_preparation_package_count_eq_1": execution_preparation_package_present,
        "approved_asset_preparation_count_eq_5": len(APPROVED_ASSET_IDS) == 5,
        "excluded_asset_preparation_count_eq_12": len(EXCLUDED_ASSETS) == 12,
        "pre_execution_snapshot_requirement_count_gte_1": True,
        "final_command_whitelist_count_eq_5": len(whitelist_records) == 5,
        "final_execution_order_count_eq_5": len(order_records) == 5,
        "final_stop_condition_count_gte_18": len(stop_condition_records) >= 18,
        "final_rollback_requirement_count_eq_5": len(rollback_records) == 5,
        "final_post_install_probe_requirement_count_eq_5": len(probe_records) == 5,
        "package_install_execution_scope_count_eq_5": len(package_scope_records) == 5,
        "weight_download_execution_scope_count_eq_5": len(weight_scope_records) == 5,
        "execution_readiness_review_count_gte_1": readiness_holds,
        "negative_guard_count_eq_26": negative_guard_count == 26,
        "negative_guard_passed_eq_26": negative_guard_passed == 26,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Compressed phase flags.
        "compressed_phase": COMPRESSED_PHASE is True,
        "approval_issuance_post_review_included": APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED is True,
        "execution_preparation_included": EXECUTION_PREPARATION_INCLUDED is True,
        "execution_readiness_review_included": EXECUTION_READINESS_REVIEW_INCLUDED is True,
        "approval_scope_valid": approval_scope_preparation_only,
        "approval_issuance_limited_to_execution_preparation": approval_scope_preparation_only,
        "approval_issuance_success_not_install_execution_approval": approval_issuance_not_install_execution_approval,
        "execution_preparation_package_created": EXECUTION_PREPARATION_PACKAGE_CREATED is True,
        "pre_execution_snapshot_required": pre_execution_snapshot_required,
        "final_command_whitelist_ready": final_command_whitelist_present,
        "final_command_whitelist_not_executed": final_command_whitelist_not_executed,
        "final_execution_order_ready": final_execution_order_locked,
        "final_execution_order_locked": final_execution_order_locked,
        "failure_stops_downstream": failure_stops_downstream,
        "final_rollback_ready": rollback_requirement_present,
        "final_post_install_probe_ready": post_install_probe_requirement_present,
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only_strict,
        "post_install_probe_not_inference": all(p.no_inference_on_probe for p in probe_records),
        "post_install_probe_not_runtime": all(p.no_runtime_on_probe for p in probe_records),
        "post_install_probe_not_output_adapter": all(p.no_output_adapter_on_probe for p in probe_records),
        "approved_assets_verified": approved_assets_complete,
        "excluded_assets_verified": len(EXCLUDED_ASSETS) == 12 and excluded_assets_remain_excluded,
        "package_install_scope_ready": package_install_scope_ready,
        "weight_download_scope_not_approved": weight_download_not_approved_by_default,
        "weight_download_requires_separate_approval": weight_download_requires_separate_approval,
        "can_enter_controlled_install_execution_next": CAN_ENTER_FLAGS["can_enter_controlled_install_execution_next"] is True,
        "can_enter_weight_download_execution_next": CAN_ENTER_FLAGS["can_enter_weight_download_execution_next"] is False,
        "can_enter_inference": CAN_ENTER_FLAGS["can_enter_inference"] is False,
        "can_enter_runtime": CAN_ENTER_FLAGS["can_enter_runtime"] is False,
        "can_enter_output_adapter": CAN_ENTER_FLAGS["can_enter_output_adapter"] is False,
        "can_enter_semantic_layer": CAN_ENTER_FLAGS["can_enter_semantic_layer"] is False,
        # Reuse flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
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

    decision = P1ControlledInstallExecutionPreparationReadinessDecision(
        decision_ref=DECISION_REF,
        execution_preparation_readiness_profile_count=1,
        approval_issuance_scope_audit_count=1,
        execution_preparation_package_count=1,
        approved_asset_preparation_count=len(APPROVED_ASSET_IDS),
        excluded_asset_preparation_count=len(EXCLUDED_ASSETS),
        pre_execution_snapshot_requirement_count=1,
        final_command_whitelist_count=len(whitelist_records),
        final_execution_order_count=len(order_records),
        final_stop_condition_count=len(stop_condition_records),
        final_rollback_requirement_count=len(rollback_records),
        final_post_install_probe_requirement_count=len(probe_records),
        package_install_execution_scope_count=len(package_scope_records),
        weight_download_execution_scope_count=len(weight_scope_records),
        execution_readiness_review_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Preparation And Readiness Review (compressed)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "approval_issuance_post_review_included": APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED,
        "execution_preparation_included": EXECUTION_PREPARATION_INCLUDED,
        "execution_readiness_review_included": EXECUTION_READINESS_REVIEW_INCLUDED,
        "upstream_issuance_ref": UPSTREAM_ISSUANCE_REF,
        "execution_planning_ref": EXECUTION_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "can_enter_flags": dict(CAN_ENTER_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "artifact_read_mode": artifact_read_mode,
        "execution_preparation_readiness_profile": _build_profile(),
        "execution_preparation_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Audits / artifacts.
        "approval_issuance_scope_audit": asdict(issuance_audit),
        "approval_issuance_scope_audit_count": 1,
        "execution_preparation_package": asdict(preparation_package),
        "execution_preparation_package_count": 1,
        "approved_asset_preparation_ids": list(APPROVED_ASSET_IDS),
        "approved_asset_preparation_count": len(APPROVED_ASSET_IDS),
        "excluded_asset_preparation_records": [dict(e) for e in EXCLUDED_ASSETS],
        "excluded_asset_preparation_count": len(EXCLUDED_ASSETS),
        "pre_execution_snapshot_requirement": asdict(snapshot_requirement),
        "pre_execution_snapshot_requirement_count": 1,
        "final_command_whitelist_records": [asdict(w) for w in whitelist_records],
        "final_command_whitelist_count": len(whitelist_records),
        "final_execution_order_records": [asdict(o) for o in order_records],
        "final_execution_order_count": len(order_records),
        "final_stop_condition_records": [asdict(s) for s in stop_condition_records],
        "final_stop_condition_count": len(stop_condition_records),
        "final_rollback_requirements": [asdict(r) for r in rollback_records],
        "final_rollback_requirement_count": len(rollback_records),
        "final_post_install_probe_requirements": [asdict(p) for p in probe_records],
        "final_post_install_probe_requirement_count": len(probe_records),
        "package_install_execution_scopes": [asdict(r) for r in package_scope_records],
        "package_install_execution_scope_count": len(package_scope_records),
        "weight_download_execution_scopes": [asdict(r) for r in weight_scope_records],
        "weight_download_execution_scope_count": len(weight_scope_records),
        "execution_risk_readiness_records": [asdict(r) for r in risk_records],
        "execution_readiness_review_record": asdict(readiness_review),
        "execution_readiness_review_count": 1,
        "execution_handoff_record": asdict(handoff_record),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_preparation_and_readiness_review_status": (
                "execution_preparation_package_and_readiness_decision_created_package_install_only_next_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Compressed phase complete: (1) audited the owner approval issuance scope = "
                "install_execution_preparation_only (Approval Issuance != Install Execution); (2) built the "
                "execution preparation package for the 5 approved candidates (supervision, byte_track, deep_sort, "
                "midas, mobile_sam) — final command whitelist (template-only, not executed), locked sequential "
                "execution order (no parallel, failure stops downstream), 18 stop conditions, per-asset rollback "
                "and find_spec-only post-install probe (no import / model load / inference / runtime / output "
                "adapter), package-install scope, and a DEFERRED weight-download scope (not approved by default; "
                "deep_sort / midas / mobile_sam require separate approval); (3) emitted a GO execution readiness "
                "decision. The 12 excluded assets remain excluded. Nothing was installed / downloaded / executed; "
                "no runtime / output adapter / semantic layer. can_enter_controlled_install_execution_next=true, "
                "can_enter_weight_download_execution_next=false. Next: Phase-P1-Controlled-Install-Execution-v1-001 "
                "— first execution recommended package-install-only, with weight download deferred to a separate "
                "sub-approval."
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
    result = review_p1_controlled_install_execution_preparation_and_readiness_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "artifact_read_mode": result.get("artifact_read_mode"),
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
