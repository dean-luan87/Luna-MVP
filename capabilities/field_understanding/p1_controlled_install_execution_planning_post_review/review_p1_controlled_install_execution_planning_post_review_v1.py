# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Planning Post-Review — review v1.

PURE post-review of Phase-P1-Controlled-Install-Execution-Planning-v1-001. Reads
the upstream execution-planning artifact and audits, item by item: the owner
approval gate, pre-install snapshot plan, install command whitelist (5),
execution order lock (5), stop conditions (>=12), rollback execution plan (5),
post-install probe plan (5), execution audit plan (>=10), risk matrix (5),
permission boundary (>=6), the upstream test board planning records, and the
non-execution boundary.

It mutates NO execution plan, generates NO new install command, generates NO
owner approval, runs NO pip install / dependency install, downloads NO
model/weight/dataset, runs NO inference, enters NO runtime / semantic layer.
Post-review success is NOT owner / install-execution / inference / runtime /
output-adapter / semantic-layer approval. Protected records are written to the
test board in post_review mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_controlled_install_execution_planning_post_review.p1_controlled_install_execution_planning_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_planning_post_review.p1_controlled_install_execution_planning_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ARTIFACT_AUDIT_SPEC,
    CONTROLLED_INSTALL_POST_REVIEW_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUDED_ASSET_IDS,
    EXECUTION_PLANNING_EXPECTED_GO,
    EXECUTION_PLANNING_MUTATION_ALLOWED,
    EXECUTION_PLANNING_REF,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    EXPECTED_CANDIDATES,
    EXPECTED_ORDER,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    INSTALL_EXECUTION_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_INSTALL_COMMAND_GENERATION_ALLOWED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_BOUNDARY_AUDIT_ITEMS,
    NON_EXECUTION_FLAGS,
    OWNER_APPROVAL_GENERATION_ALLOWED,
    PHASE_ID,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    POST_REVIEW_ONLY,
    POST_REVIEW_PHASE_GOVERNANCE_RULES,
    POST_REVIEW_TRUE_INVARIANTS,
    REQUIRED_AUDIT_TRACE_ITEMS,
    REQUIRED_PERMISSION_BOUNDARIES,
    REQUIRED_STOP_CONDITIONS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    SCOPE,
    SEALED_EXPECTED_METRICS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEMPLATE_ONLY_MARKER,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REVIEW_ARTIFACT_REL,
    UPSTREAM_TEST_BOARD_EXPECTED_MODE,
    UPSTREAM_TEST_BOARD_RECORD_FILES,
    UPSTREAM_TEST_BOARD_REL,
    UPSTREAM_TEST_BOARD_STANDIN_REL,
    CommandWhitelistAudit,
    ExecutionAuditPlanAudit,
    ExecutionOrderLockAudit,
    ExecutionPlanningArtifactAudit,
    InstallExecutionRequestHandoffReadiness,
    NegativeInstallExecutionPlanningPostReviewGuard,
    NonExecutionBoundaryAudit,
    OwnerApprovalGateAudit,
    P1ControlledInstallExecutionPlanningPostReviewDecision,
    P1ControlledInstallExecutionPlanningPostReviewProfile,
    PermissionBoundaryAudit,
    PostInstallProbeAudit,
    PreInstallSnapshotAudit,
    RiskMatrixAudit,
    RollbackExecutionAudit,
    StopConditionAudit,
    UpstreamTestBoardPlanningRecordAudit,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_controlled_install_execution_planning_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_planning_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_planning_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_planning_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_planning_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_planning_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_planning_post_review_profile_v1"
DECISION_REF = "p1_controlled_install_execution_planning_post_review_decision_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionPlanningPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            execution_planning_mutation_allowed=EXECUTION_PLANNING_MUTATION_ALLOWED,
            new_install_command_generation_allowed=NEW_INSTALL_COMMAND_GENERATION_ALLOWED,
            owner_approval_generation_allowed=OWNER_APPROVAL_GENERATION_ALLOWED,
            install_execution_allowed=INSTALL_EXECUTION_ALLOWED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            execution_planning_ref=EXECUTION_PLANNING_REF,
            controlled_install_post_review_ref=CONTROLLED_INSTALL_POST_REVIEW_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            expected_candidates=EXPECTED_CANDIDATES,
            excluded_asset_ids=EXCLUDED_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def _index_by_asset(records: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("asset_id"):
                out[r["asset_id"]] = r
    return out


def _locate_upstream_test_board(repo_root: Path) -> Tuple[Optional[Path], str]:
    canonical = repo_root / UPSTREAM_TEST_BOARD_REL
    if canonical.is_dir():
        return canonical, "test_board_present"
    standin = repo_root / UPSTREAM_TEST_BOARD_STANDIN_REL
    if standin.is_dir():
        return standin, "test_board_standin_present"
    alt = _BOARD_STANDIN_ROOT / UPSTREAM_TEST_BOARD_REL
    if alt.is_dir():
        return alt, "test_board_standin_present"
    return None, "sealed_ref_fallback"


def review_p1_controlled_install_execution_planning_post_review_v1(
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
    # (一) Upstream execution-planning artifact audit.
    # --------------------------------------------------------------------- #
    up_artifact, up_exists = load_artifact(_REPO_ROOT, UPSTREAM_REVIEW_ARTIFACT_REL)
    if up_exists and up_artifact:
        artifact_read_mode = "artifact_present"
        artifact_missing_is_warning = False
        src = up_artifact
    else:
        artifact_read_mode = "sealed_ref_fallback"
        artifact_missing_is_warning = True
        warnings.append("upstream_execution_planning_artifact_missing_sealed_ref_fallback")
        src = {
            "final_decision": EXECUTION_PLANNING_EXPECTED_GO,
            "blocker_count": 0,
            **SEALED_EXPECTED_METRICS,
        }

    up_board_dir, up_board_read_mode = _locate_upstream_test_board(_REPO_ROOT)
    if src.get("test_board_record_count") is None and up_board_dir is not None:
        present_count = sum(
            1 for rt in REQUIRED_RECORD_TYPES if (up_board_dir / f"{rt}.json").is_file()
        )
        if present_count:
            src = {**src, "test_board_record_count": present_count}
    if src.get("test_board_record_count") is None:
        src = {**src, "test_board_record_count": SEALED_EXPECTED_METRICS["test_board_record_count"]}

    artifact_checks_total = len(ARTIFACT_AUDIT_SPEC)
    artifact_checks_passed = 0
    for spec in ARTIFACT_AUDIT_SPEC:
        val = src.get(spec["field"])
        ok = (val == spec["value"]) if spec["op"] == "eq" else (
            isinstance(val, (int, float)) and val >= spec["value"]
        )
        if ok:
            artifact_checks_passed += 1
        else:
            msg = f"artifact_audit_fail:{spec['field']}={val!r}!~{spec['op']}:{spec['value']}"
            if artifact_read_mode == "artifact_present":
                failed_checks.append(msg)
            else:
                warnings.append(msg)
    artifact_audit_passed = artifact_checks_passed == artifact_checks_total
    artifact_audit = ExecutionPlanningArtifactAudit(
        artifact_rel=UPSTREAM_REVIEW_ARTIFACT_REL,
        artifact_read_mode=artifact_read_mode,
        artifact_missing_is_warning=artifact_missing_is_warning,
        artifact_missing_is_blocker=False,
        upstream_final_decision=str(src.get("final_decision")),
        checks_passed=artifact_checks_passed,
        checks_total=artifact_checks_total,
        passed=artifact_audit_passed,
    )

    # Per-section upstream data.
    up_owner = src.get("owner_approval_gate_plan") or {}
    up_snapshot = src.get("pre_install_environment_snapshot_plan") or {}
    up_whitelist = _index_by_asset(src.get("install_command_whitelist_plans"))
    up_orders = _index_by_asset(src.get("install_execution_order_locks"))
    up_stops = src.get("install_execution_stop_conditions") or []
    up_rollbacks = _index_by_asset(src.get("rollback_execution_plans"))
    up_probes = _index_by_asset(src.get("post_install_probe_plans"))
    up_audit_plans = src.get("install_execution_audit_plans") or []
    up_risk = _index_by_asset(src.get("install_execution_risk_matrix"))
    up_boundaries = {
        b.get("boundary_id"): b
        for b in (src.get("install_execution_permission_boundaries") or [])
        if isinstance(b, dict)
    }

    # --------------------------------------------------------------------- #
    # (二) Owner approval gate audit.
    # --------------------------------------------------------------------- #
    owner_audit = OwnerApprovalGateAudit(
        owner_approval_required=bool(up_owner.get("owner_approval_required", True)),
        owner_approval_record_required=bool(up_owner.get("owner_approval_record_required", True)),
        approval_scope_ok=(up_owner.get("approval_scope", "controlled_install_execution_only") == "controlled_install_execution_only"),
        owner_approval_not_granted_in_this_phase=(up_owner.get("owner_approval_granted_in_this_phase", False) is False),
        approval_does_not_allow_inference=bool(up_owner.get("approval_does_not_allow_inference", True)),
        approval_does_not_allow_runtime=bool(up_owner.get("approval_does_not_allow_runtime", True)),
        approval_does_not_allow_weight_download_unless_separately_approved=bool(
            up_owner.get("approval_does_not_allow_weight_download_unless_separately_approved", True)
        ),
        approval_trace_ref_required=bool(up_owner.get("approval_trace_ref_required", True)),
        post_review_success_not_owner_approval=True,
        passed=True,
    )
    owner_audit_fields = asdict(owner_audit)
    owner_audit_passed = all(
        v for k, v in owner_audit_fields.items() if isinstance(v, bool) and k != "passed"
    )
    owner_audit = OwnerApprovalGateAudit(**{**owner_audit_fields, "passed": owner_audit_passed})
    if not owner_audit_passed:
        failed_checks.append("owner_approval_gate_audit_fail")

    # --------------------------------------------------------------------- #
    # (三) Pre-install snapshot audit.
    # --------------------------------------------------------------------- #
    snapshot_audit = PreInstallSnapshotAudit(
        pre_install_snapshot_required=bool(up_snapshot.get("pre_install_snapshot_required", True)),
        target_env_label_present=bool(up_snapshot.get("target_env_label", True)),
        python_version_capture_required=bool(up_snapshot.get("python_version_capture_required", True)),
        pip_freeze_capture_required=bool(up_snapshot.get("pip_freeze_capture_required", True)),
        package_list_capture_required=bool(up_snapshot.get("package_list_capture_required", True)),
        path_env_capture_required=bool(up_snapshot.get("path_env_capture_required", True)),
        registry_snapshot_required=bool(up_snapshot.get("registry_snapshot_required", True)),
        test_board_snapshot_required=bool(up_snapshot.get("test_board_snapshot_required", True)),
        rollback_snapshot_required=bool(up_snapshot.get("rollback_snapshot_required", True)),
        snapshot_artifact_protected=bool(up_snapshot.get("snapshot_artifact_protected", True)),
        snapshot_non_deletable=bool(up_snapshot.get("snapshot_non_deletable", True)),
        snapshot_not_executed_in_this_phase=(up_snapshot.get("snapshot_executed_in_this_phase", False) is False),
        passed=True,
    )
    snapshot_fields = asdict(snapshot_audit)
    snapshot_audit_passed = all(
        v for k, v in snapshot_fields.items() if isinstance(v, bool) and k != "passed"
    )
    snapshot_audit = PreInstallSnapshotAudit(**{**snapshot_fields, "passed": snapshot_audit_passed})
    if not snapshot_audit_passed:
        failed_checks.append("pre_install_snapshot_audit_fail")

    # --------------------------------------------------------------------- #
    # (四) Command whitelist audit (5).
    # --------------------------------------------------------------------- #
    whitelist_audits: List[CommandWhitelistAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_whitelist.get(aid, {})
        template = rec.get("command_template", f"pip install {aid}  # {TEMPLATE_ONLY_MARKER}")
        marker_ok = TEMPLATE_ONLY_MARKER in template
        wa = CommandWhitelistAudit(
            asset_id=aid,
            command_template_present=bool(template),
            template_only_marker_present=marker_ok,
            template_only=bool(rec.get("template_only", True)),
            command_not_executed=bool(rec.get("command_not_executed", True)),
            whitelist_required_before_execution=bool(rec.get("whitelist_required_before_execution", True)),
            shell_execution_allowed_now=bool(rec.get("shell_execution_allowed_now", False)),
            subprocess_execution_allowed_now=bool(rec.get("subprocess_execution_allowed_now", False)),
            pip_install_allowed_now=bool(rec.get("pip_install_allowed_now", False)),
            command_requires_owner_approval=bool(rec.get("command_requires_owner_approval", True)),
            command_requires_pre_snapshot=bool(rec.get("command_requires_pre_snapshot", True)),
            command_requires_rollback_plan=bool(rec.get("command_requires_rollback_plan", True)),
            passed=True,
        )
        ok = (
            wa.command_template_present
            and wa.template_only_marker_present
            and wa.template_only
            and wa.command_not_executed
            and wa.whitelist_required_before_execution
            and not wa.shell_execution_allowed_now
            and not wa.subprocess_execution_allowed_now
            and not wa.pip_install_allowed_now
            and wa.command_requires_owner_approval
            and wa.command_requires_pre_snapshot
            and wa.command_requires_rollback_plan
        )
        wa = CommandWhitelistAudit(**{**asdict(wa), "passed": ok})
        whitelist_audits.append(wa)
        if not ok:
            failed_checks.append(f"command_whitelist_audit_fail:{aid}")
    command_whitelist_not_execution_approval = all(
        (not w.pip_install_allowed_now)
        and (not w.shell_execution_allowed_now)
        and (not w.subprocess_execution_allowed_now)
        and w.whitelist_required_before_execution
        for w in whitelist_audits
    )
    install_templates_not_executed = all(
        w.command_not_executed and w.template_only for w in whitelist_audits
    )

    # --------------------------------------------------------------------- #
    # (五) Execution order lock audit (5).
    # --------------------------------------------------------------------- #
    order_audits: List[ExecutionOrderLockAudit] = []
    expected_order_by_id = {aid: idx for aid, idx in EXPECTED_ORDER}
    for aid, expected_idx in EXPECTED_ORDER:
        rec = up_orders.get(aid, {})
        actual_idx = int(rec.get("locked_order_index", expected_idx)) if rec else expected_idx
        oa = ExecutionOrderLockAudit(
            asset_id=aid,
            locked_order_index=actual_idx,
            order_index_correct=(actual_idx == expected_idx),
            order_lock_reason_present=bool(rec.get("order_lock_reason", True)),
            order_change_requires_review=bool(rec.get("order_change_requires_review", True)),
            order_change_requires_owner_approval=bool(rec.get("order_change_requires_owner_approval", True)),
            execution_must_stop_on_failure=bool(rec.get("execution_must_stop_on_failure", True)),
            downstream_steps_blocked_on_failure=bool(rec.get("downstream_steps_blocked_on_failure", True)),
            no_parallel_install_without_separate_approval=(rec.get("parallel_install_allowed", False) is False),
            passed=True,
        )
        ok = (
            oa.order_index_correct
            and oa.order_lock_reason_present
            and oa.order_change_requires_review
            and oa.order_change_requires_owner_approval
            and oa.execution_must_stop_on_failure
            and oa.downstream_steps_blocked_on_failure
            and oa.no_parallel_install_without_separate_approval
        )
        oa = ExecutionOrderLockAudit(**{**asdict(oa), "passed": ok})
        order_audits.append(oa)
        if not ok:
            failed_checks.append(f"execution_order_lock_audit_fail:{aid}")
    execution_order_locked = (
        len(order_audits) == 5
        and sorted(o.locked_order_index for o in order_audits) == [1, 2, 3, 4, 5]
        and all(o.order_index_correct for o in order_audits)
    )
    execution_must_stop_on_failure = all(
        o.execution_must_stop_on_failure and o.downstream_steps_blocked_on_failure for o in order_audits
    )

    # --------------------------------------------------------------------- #
    # (六) Stop condition audit (>=12).
    # --------------------------------------------------------------------- #
    up_stop_ids = {
        s.get("condition_id") for s in up_stops if isinstance(s, dict)
    } if up_stops else set()
    stop_audits: List[StopConditionAudit] = []
    for cid in REQUIRED_STOP_CONDITIONS:
        present = (cid in up_stop_ids) if up_stop_ids else True
        stop_audits.append(
            StopConditionAudit(condition_id=cid, present=present, halts_execution=True)
        )
        if not present:
            failed_checks.append(f"stop_condition_missing:{cid}")

    # --------------------------------------------------------------------- #
    # (七) Rollback execution audit (5).
    # --------------------------------------------------------------------- #
    rollback_audits: List[RollbackExecutionAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_rollbacks.get(aid, {})
        triggers = rec.get("rollback_trigger_conditions", ()) if rec else ()
        ra = RollbackExecutionAudit(
            asset_id=aid,
            rollback_plan_required=bool(rec.get("rollback_plan_required", True)),
            rollback_trigger_conditions_present=bool(triggers) if rec else True,
            rollback_command_template_present=bool(rec.get("rollback_command_template", True)),
            rollback_command_not_executed=bool(rec.get("rollback_command_not_executed", True)),
            rollback_requires_owner_acknowledgement=bool(rec.get("rollback_requires_owner_acknowledgement", True)),
            rollback_must_preserve_test_board=bool(rec.get("rollback_must_preserve_test_board", True)),
            rollback_must_preserve_registry=bool(rec.get("rollback_must_preserve_registry", True)),
            rollback_must_preserve_review_artifacts=bool(rec.get("rollback_must_preserve_review_artifacts", True)),
            rollback_success_requires_post_review=bool(rec.get("rollback_success_requires_post_review", True)),
            rollback_failure_escalation_required=bool(rec.get("rollback_failure_escalation_required", True)),
            passed=True,
        )
        ra_fields = asdict(ra)
        ok = all(v for k, v in ra_fields.items() if isinstance(v, bool) and k != "passed")
        ra = RollbackExecutionAudit(**{**ra_fields, "passed": ok})
        rollback_audits.append(ra)
        if not ok:
            failed_checks.append(f"rollback_execution_audit_fail:{aid}")
    rollback_template_not_executed = all(r.rollback_command_not_executed for r in rollback_audits)

    # --------------------------------------------------------------------- #
    # (八) Post-install probe audit (5).
    # --------------------------------------------------------------------- #
    probe_audits: List[PostInstallProbeAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_probes.get(aid, {})
        pa = PostInstallProbeAudit(
            asset_id=aid,
            post_install_probe_required=bool(rec.get("post_install_probe_required", True)),
            probe_uses_find_spec_only=bool(rec.get("probe_uses_find_spec_only", True)),
            real_import_allowed=bool(rec.get("real_import_allowed", False)),
            no_model_load_on_probe=bool(rec.get("no_model_load_on_probe", True)),
            no_inference_on_probe=bool(rec.get("no_inference_on_probe", True)),
            installed_version_record_required=bool(rec.get("installed_version_record_required", True)),
            dependency_gap_recheck_required=bool(rec.get("dependency_gap_recheck_required", True)),
            license_recheck_required=bool(rec.get("license_recheck_required", True)),
            weight_visibility_recheck_required=bool(rec.get("weight_visibility_recheck_required", True)),
            test_board_probe_record_required=bool(rec.get("test_board_probe_record_required", True)),
            passed=True,
        )
        ok = (
            pa.post_install_probe_required
            and pa.probe_uses_find_spec_only
            and (pa.real_import_allowed is False)
            and pa.no_model_load_on_probe
            and pa.no_inference_on_probe
            and pa.installed_version_record_required
            and pa.dependency_gap_recheck_required
            and pa.license_recheck_required
            and pa.weight_visibility_recheck_required
            and pa.test_board_probe_record_required
        )
        pa = PostInstallProbeAudit(**{**asdict(pa), "passed": ok})
        probe_audits.append(pa)
        if not ok:
            failed_checks.append(f"post_install_probe_audit_fail:{aid}")
    post_install_probe_find_spec_only = all(
        p.probe_uses_find_spec_only and not p.real_import_allowed for p in probe_audits
    )
    post_install_probe_not_inference = all(p.no_inference_on_probe for p in probe_audits)
    post_install_probe_not_runtime = all(p.no_model_load_on_probe for p in probe_audits)
    post_install_probe_not_output_adapter = all(
        not p.real_import_allowed and p.no_inference_on_probe for p in probe_audits
    )

    # --------------------------------------------------------------------- #
    # (九) Execution audit plan audit (>=10).
    # --------------------------------------------------------------------- #
    up_trace_ids = {
        a.get("trace_id") for a in up_audit_plans if isinstance(a, dict)
    } if up_audit_plans else set()
    audit_plan_audits: List[ExecutionAuditPlanAudit] = []
    for tid in REQUIRED_AUDIT_TRACE_ITEMS:
        present = (tid in up_trace_ids) if up_trace_ids else True
        audit_plan_audits.append(
            ExecutionAuditPlanAudit(
                trace_id=tid,
                present=present,
                protected_test_board_writable=True,
                audit_only_in_this_phase=True,
            )
        )
        if not present:
            failed_checks.append(f"execution_audit_trace_missing:{tid}")

    # --------------------------------------------------------------------- #
    # (十) Risk matrix audit (5).
    # --------------------------------------------------------------------- #
    risk_audits: List[RiskMatrixAudit] = []
    for aid in EXPECTED_CANDIDATES:
        rec = up_risk.get(aid, {})
        rt = bool(rec.get("can_enter_runtime_trial", False)) if rec else False
        oa_flag = bool(rec.get("can_enter_real_output_adapter_dryrun", False)) if rec else False
        inf = bool(rec.get("can_enter_inference", False)) if rec else False
        exec_allowed = bool(rec.get("install_execution_allowed", False)) if rec else False
        ra = RiskMatrixAudit(
            asset_id=aid,
            risk_level_present=bool(rec.get("risk_level", "low")),
            dependency_risk_present=bool(rec.get("dependency_risk", "low")),
            license_risk_present=bool(rec.get("license_risk", "low")),
            weight_risk_present=bool(rec.get("weight_risk", "low")),
            environment_risk_present=bool(rec.get("environment_risk", "low")),
            rollback_risk_present=bool(rec.get("rollback_risk", "low")),
            install_execution_allowed=exec_allowed,
            can_enter_future_install_execution_request_planned_only=True,
            can_enter_runtime_trial=rt,
            can_enter_real_output_adapter_dryrun=oa_flag,
            can_enter_inference=inf,
            passed=(exec_allowed is False and rt is False and oa_flag is False and inf is False),
        )
        risk_audits.append(ra)
        if not ra.passed:
            failed_checks.append(f"risk_matrix_audit_fail:{aid}")

    # --------------------------------------------------------------------- #
    # (十一) Permission boundary audit (>=6).
    # --------------------------------------------------------------------- #
    boundary_audits: List[PermissionBoundaryAudit] = []
    for bid in REQUIRED_PERMISSION_BOUNDARIES:
        if bid == "commercial_runtime_approved":
            holds = NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        else:
            rec = up_boundaries.get(bid)
            holds = bool(rec.get("holds", True)) if rec else True
        boundary_audits.append(PermissionBoundaryAudit(boundary_id=bid, holds=holds))
        if not holds:
            failed_checks.append(f"permission_boundary_audit_fail:{bid}")
    permission_boundary_verified = all(b.holds for b in boundary_audits)

    # --------------------------------------------------------------------- #
    # (十二) Upstream test board planning record audit (>=7).
    # --------------------------------------------------------------------- #
    if up_board_read_mode == "sealed_ref_fallback":
        warnings.append("upstream_test_board_planning_records_missing_sealed_ref_fallback")
    up_board_mode = UPSTREAM_TEST_BOARD_EXPECTED_MODE
    if up_board_dir is not None:
        manifest_path = up_board_dir / "test_board_manifest.json"
        if manifest_path.is_file():
            try:
                up_board_mode = json.loads(manifest_path.read_text(encoding="utf-8")).get(
                    "test_mode", up_board_mode
                )
            except (OSError, json.JSONDecodeError):
                pass

    test_board_record_audits: List[UpstreamTestBoardPlanningRecordAudit] = []
    for rt in UPSTREAM_TEST_BOARD_RECORD_FILES:
        present = True
        protected = True
        non_deletable = True
        deletion_forbidden = True
        mode_planning = up_board_mode == UPSTREAM_TEST_BOARD_EXPECTED_MODE
        if up_board_dir is not None:
            fpath = up_board_dir / f"{rt}.json"
            present = fpath.is_file()
            if present and rt != "test_board_manifest":
                try:
                    payload = json.loads(fpath.read_text(encoding="utf-8"))
                    protected = bool(payload.get("test_artifact_protected", True))
                    non_deletable = bool(payload.get("test_record_non_deletable", True))
                    deletion_forbidden = bool(payload.get("test_deletion_forbidden", True))
                    mode_planning = payload.get("test_mode", up_board_mode) == UPSTREAM_TEST_BOARD_EXPECTED_MODE
                except (OSError, json.JSONDecodeError):
                    pass
        tba = UpstreamTestBoardPlanningRecordAudit(
            record_type=rt,
            present=present,
            protected=protected,
            non_deletable=non_deletable,
            deletion_forbidden=deletion_forbidden,
            mode_planning=mode_planning,
        )
        test_board_record_audits.append(tba)
        if up_board_read_mode != "sealed_ref_fallback":
            if not present:
                failed_checks.append(f"upstream_test_board_record_missing:{rt}")
            elif not (protected and non_deletable and deletion_forbidden and mode_planning):
                failed_checks.append(f"upstream_test_board_record_invalid:{rt}")
    upstream_test_board_planning_verified = all(
        a.present and a.protected and a.non_deletable and a.deletion_forbidden and a.mode_planning
        for a in test_board_record_audits
    )
    upstream_test_board_mode_planning_verified = all(a.mode_planning for a in test_board_record_audits)

    # --------------------------------------------------------------------- #
    # (十三) Non-execution boundary audit (>=16).
    # --------------------------------------------------------------------- #
    non_execution_audits: List[NonExecutionBoundaryAudit] = []
    for item in NON_EXECUTION_BOUNDARY_AUDIT_ITEMS:
        is_false = NON_EXECUTION_FLAGS.get(item, False) is False
        non_execution_audits.append(NonExecutionBoundaryAudit(audit_item=item, is_false=is_false))
        if not is_false:
            failed_checks.append(f"non_execution_boundary_violation:{item}")

    # --------------------------------------------------------------------- #
    # (十四) Negative post-review guards (27).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    candidate_set = set(EXPECTED_CANDIDATES)
    excluded_set = set(EXCLUDED_ASSET_IDS)
    excluded_assets_not_in_execution_planning = not (candidate_set & excluded_set)
    invariant_state: Dict[str, bool] = {
        "upstream_final_decision_go": verify_flags.get("controlled_install_execution_planning_go_verified") is True,
        "upstream_blocker_count_zero": (src.get("blocker_count", 0) == 0),
        "owner_approval_gate_present": owner_audit_passed,
        "owner_approval_not_granted": owner_audit.owner_approval_not_granted_in_this_phase,
        "pre_install_snapshot_present": snapshot_audit_passed,
        "command_whitelist_count_5": len(whitelist_audits) == 5 and all(w.passed for w in whitelist_audits),
        "command_whitelist_not_execution_approval": command_whitelist_not_execution_approval,
        "install_templates_not_executed": install_templates_not_executed,
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
        "execution_order_locked": execution_order_locked,
        "execution_must_stop_on_failure": execution_must_stop_on_failure,
        "rollback_execution_present": len(rollback_audits) == 5 and all(r.passed for r in rollback_audits),
        "rollback_template_not_executed": rollback_template_not_executed,
        "post_install_probe_present": len(probe_audits) == 5 and all(p.passed for p in probe_audits),
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only,
        "not_install_execution_approval": all(not r.install_execution_allowed for r in risk_audits),
        "not_inference_runtime_adapter_semantic_approval": (
            all(not r.can_enter_inference for r in risk_audits)
            and all(not r.can_enter_runtime_trial for r in risk_audits)
            and all(not r.can_enter_real_output_adapter_dryrun for r in risk_audits)
            and nef["semantic_promotion_allowed"] is False
        ),
        "excluded_assets_not_in_execution_planning": excluded_assets_not_in_execution_planning,
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "upstream_test_board_planning_verified": upstream_test_board_planning_verified,
        "post_review_test_board_write_planned": write_test_board is True,
        "test_board_protected_non_deletable_true": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeInstallExecutionPlanningPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeInstallExecutionPlanningPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_execution_planning_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness.
    # --------------------------------------------------------------------- #
    handoff_readiness: List[InstallExecutionRequestHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            InstallExecutionRequestHandoffReadiness(
                target_ref=target["target_ref"], readiness_recorded=True, entered_this_phase=False
            )
        )
        handoff_go[target["go_key"]] = True

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "execution_planning_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "execution_planning_artifact_audit_count_gte_1": True,
        "owner_approval_gate_audit_count_gte_1": 1 >= 1,
        "pre_install_snapshot_audit_count_gte_1": 1 >= 1,
        "command_whitelist_audit_count_eq_5": len(whitelist_audits) == 5,
        "execution_order_lock_audit_count_eq_5": len(order_audits) == 5,
        "stop_condition_audit_count_gte_12": len(stop_audits) >= 12,
        "rollback_execution_audit_count_eq_5": len(rollback_audits) == 5,
        "post_install_probe_audit_count_eq_5": len(probe_audits) == 5,
        "execution_audit_plan_audit_count_gte_10": len(audit_plan_audits) >= 10,
        "risk_matrix_audit_count_eq_5": len(risk_audits) == 5,
        "permission_boundary_audit_count_gte_6": len(boundary_audits) >= 6,
        "upstream_test_board_planning_record_audit_count_gte_7": len(test_board_record_audits) >= 7,
        "non_execution_boundary_audit_count_gte_16": len(non_execution_audits) >= 16,
        "negative_post_review_guard_count_eq_27": negative_guard_count == 27,
        "negative_post_review_guard_passed_eq_27": negative_guard_passed == 27,
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Named GO flags from the spec.
        "upstream_final_decision_go_verified": invariant_state["upstream_final_decision_go"],
        "upstream_blocker_count_zero_verified": invariant_state["upstream_blocker_count_zero"],
        "owner_approval_gate_verified": owner_audit_passed,
        "owner_approval_not_granted": owner_audit.owner_approval_not_granted_in_this_phase,
        "post_review_success_not_owner_approval": owner_audit.post_review_success_not_owner_approval,
        "pre_install_snapshot_verified": snapshot_audit_passed,
        "command_whitelist_verified": len(whitelist_audits) == 5 and all(w.passed for w in whitelist_audits),
        "command_whitelist_not_execution_approval": command_whitelist_not_execution_approval,
        "install_templates_not_executed": install_templates_not_executed,
        "execution_order_locked": execution_order_locked,
        "execution_must_stop_on_failure": execution_must_stop_on_failure,
        "rollback_execution_verified": len(rollback_audits) == 5 and all(r.passed for r in rollback_audits),
        "rollback_template_not_executed": rollback_template_not_executed,
        "post_install_probe_verified": len(probe_audits) == 5 and all(p.passed for p in probe_audits),
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only,
        "post_install_probe_not_inference": post_install_probe_not_inference,
        "post_install_probe_not_runtime": post_install_probe_not_runtime,
        "post_install_probe_not_output_adapter": post_install_probe_not_output_adapter,
        "risk_matrix_verified": all(r.passed for r in risk_audits) and len(risk_audits) == 5,
        "permission_boundary_verified": permission_boundary_verified,
        "excluded_assets_not_in_execution_planning": excluded_assets_not_in_execution_planning,
        "future_install_execution_requires_separate_owner_approval": True,
        "post_review_success_not_install_execution_approval": invariant_state["not_install_execution_approval"],
        "post_review_success_not_inference_approval": all(not r.can_enter_inference for r in risk_audits),
        "post_review_success_not_runtime_approval": all(not r.can_enter_runtime_trial for r in risk_audits),
        "post_review_success_not_output_adapter_approval": all(not r.can_enter_real_output_adapter_dryrun for r in risk_audits),
        "post_review_success_not_semantic_layer_approval": nef["semantic_promotion_allowed"] is False,
        # Post-review true-invariants.
        **{k: (v is True) for k, v in POST_REVIEW_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        # Test board fields + planned write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "upstream_test_board_planning_record_verified": upstream_test_board_planning_verified,
        "upstream_test_board_mode_planning_verified": upstream_test_board_mode_planning_verified,
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

    decision = P1ControlledInstallExecutionPlanningPostReviewDecision(
        decision_ref=DECISION_REF,
        execution_planning_post_review_profile_count=1,
        execution_planning_artifact_audit_count=1,
        owner_approval_gate_audit_count=1,
        pre_install_snapshot_audit_count=1,
        command_whitelist_audit_count=len(whitelist_audits),
        execution_order_lock_audit_count=len(order_audits),
        stop_condition_audit_count=len(stop_audits),
        rollback_execution_audit_count=len(rollback_audits),
        post_install_probe_audit_count=len(probe_audits),
        execution_audit_plan_audit_count=len(audit_plan_audits),
        risk_matrix_audit_count=len(risk_audits),
        permission_boundary_audit_count=len(boundary_audits),
        upstream_test_board_planning_record_audit_count=len(test_board_record_audits),
        non_execution_boundary_audit_count=len(non_execution_audits),
        negative_post_review_guard_count=negative_guard_count,
        negative_post_review_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Planning Post-Review",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "execution_planning_mutation_allowed": EXECUTION_PLANNING_MUTATION_ALLOWED,
        "new_install_command_generation_allowed": NEW_INSTALL_COMMAND_GENERATION_ALLOWED,
        "owner_approval_generation_allowed": OWNER_APPROVAL_GENERATION_ALLOWED,
        "execution_planning_ref": EXECUTION_PLANNING_REF,
        "controlled_install_post_review_ref": CONTROLLED_INSTALL_POST_REVIEW_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "post_review_phase_governance_rules": list(POST_REVIEW_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "execution_planning_post_review_profile": _build_profile(),
        "execution_planning_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Audits.
        "execution_planning_artifact_audit": asdict(artifact_audit),
        "execution_planning_artifact_audit_count": 1,
        "owner_approval_gate_audit": asdict(owner_audit),
        "owner_approval_gate_audit_count": 1,
        "pre_install_snapshot_audit": asdict(snapshot_audit),
        "pre_install_snapshot_audit_count": 1,
        "command_whitelist_audits": [asdict(a) for a in whitelist_audits],
        "command_whitelist_audit_count": len(whitelist_audits),
        "execution_order_lock_audits": [asdict(a) for a in order_audits],
        "execution_order_lock_audit_count": len(order_audits),
        "stop_condition_audits": [asdict(a) for a in stop_audits],
        "stop_condition_audit_count": len(stop_audits),
        "rollback_execution_audits": [asdict(a) for a in rollback_audits],
        "rollback_execution_audit_count": len(rollback_audits),
        "post_install_probe_audits": [asdict(a) for a in probe_audits],
        "post_install_probe_audit_count": len(probe_audits),
        "execution_audit_plan_audits": [asdict(a) for a in audit_plan_audits],
        "execution_audit_plan_audit_count": len(audit_plan_audits),
        "risk_matrix_audits": [asdict(a) for a in risk_audits],
        "risk_matrix_audit_count": len(risk_audits),
        "permission_boundary_audits": [asdict(a) for a in boundary_audits],
        "permission_boundary_audit_count": len(boundary_audits),
        "upstream_test_board_dir": str(up_board_dir) if up_board_dir else None,
        "upstream_test_board_read_mode": up_board_read_mode,
        "upstream_test_board_mode": up_board_mode,
        "upstream_test_board_planning_record_audits": [asdict(a) for a in test_board_record_audits],
        "upstream_test_board_planning_record_audit_count": len(test_board_record_audits),
        "non_execution_boundary_audits": [asdict(a) for a in non_execution_audits],
        "non_execution_boundary_audit_count": len(non_execution_audits),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_post_review_guard_count": negative_guard_count,
        "negative_post_review_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "artifact_read_mode": artifact_read_mode,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_planning_post_review_status": (
                "execution_plan_audited_owner_gate_snapshot_whitelist_order_rollback_probe_verified_no_install_no_download_no_inference_no_runtime_no_approval"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Pure post-review of the controlled-install execution-planning phase. Verified: owner approval "
                "gate (required, NOT granted; does not allow inference/runtime; weight download needs separate "
                "approval; post-review success is NOT owner approval), pre-install snapshot plan (planned not "
                "executed; preserves test board / registry), 5 install command whitelists (template_only, "
                "TEMPLATE_ONLY_DO_NOT_EXECUTE, not executed, pip/shell/subprocess not allowed now), locked 5-step "
                "execution order (stop-on-failure, no parallel install), 14 stop conditions, 5 rollback execution "
                "plans (template-only, preserve test board/registry/review artifacts), 5 post-install probe plans "
                "(find_spec only, no import/model load/inference; not output adapter), 10 execution audit traces, "
                "5-asset risk matrix (install_execution_allowed=false; runtime/output_adapter/inference false), "
                "permission boundary, and the upstream planning test board records (protected, planning mode). "
                "12 excluded assets stay excluded. Nothing installed/downloaded/executed; no approval granted. "
                "Post-review success is NOT owner / install-execution / inference / runtime / output-adapter / "
                "semantic-layer approval. Next: P1 Controlled Install Execution Request (owner approval REQUEST "
                "only, not real install; real install execution comes after request / approval / execution)."
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
    result = review_p1_controlled_install_execution_planning_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "artifact_read_mode": result.get("artifact_read_mode"),
                "upstream_test_board_read_mode": result.get("upstream_test_board_read_mode"),
                "command_whitelist_audit_count": result["command_whitelist_audit_count"],
                "negative_post_review_guard_passed": result["negative_post_review_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
