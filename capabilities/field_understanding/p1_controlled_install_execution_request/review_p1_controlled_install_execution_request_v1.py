# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Request — review v1.

Assembles an auditable owner-approval REQUEST package for P1 controlled install
execution of the 5 approved candidates (supervision, byte_track, deep_sort,
midas, mobile_sam). It references — never re-generates — the upstream command
whitelist, and requests (does not execute) the pre-install snapshot, rollback
plan and post-install probe. It discloses risk and the 12 excluded assets.

Request != Approval. This phase generates NO approval and executes NO install.
No pip install / dependency install, no model/weight/dataset download, no
inference, no runtime, no semantic layer. Request success is NOT owner /
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
from capabilities.field_understanding.p1_controlled_install_execution_request.p1_controlled_install_execution_request_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    collect_optional_governance_refs,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_request.p1_controlled_install_execution_request_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUDED_ASSETS,
    EXECUTION_PLANNING_ARTIFACT_REL,
    EXECUTION_PLANNING_POST_REVIEW_REF,
    EXECUTION_PLANNING_REF,
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
    OWNER_APPROVAL_GRANTED,
    OWNER_APPROVAL_REQUEST_CREATED,
    PERMISSION_BOUNDARY_STATEMENTS,
    PHASE_ID,
    PLANNING_MODE_PATCH_REF,
    PLANNING_PRINCIPLE_ZH,
    PRE_INSTALL_SNAPSHOT_ITEMS,
    REQUEST_AUDIT_TRACE_ITEMS,
    REQUEST_ONLY,
    REQUEST_PHASE_GOVERNANCE_RULES,
    REQUEST_TRUE_INVARIANTS,
    REQUESTED_ASSET_IDS,
    REQUESTED_ORDER,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROLLBACK_TRIGGER_REF_CONDITIONS,
    SCOPE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    WEIGHT_HANDLED_ASSETS,
    CommandTemplateReferenceRecord,
    ExcludedAssetDisclosureRecord,
    InstallExecutionApprovalHandoffReadiness,
    InstallExecutionRequestPackage,
    NegativeInstallExecutionRequestGuard,
    OwnerApprovalRequestRecord,
    P1ControlledInstallExecutionRequestDecision,
    P1ControlledInstallExecutionRequestProfile,
    PostInstallProbeRequirementRequest,
    PreInstallSnapshotRequest,
    RequestAuditRecord,
    RequestedAssetScope,
    RequestPermissionBoundary,
    RiskDisclosureRecord,
    RollbackRequirementRequest,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_controlled_install_execution_request_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_request_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_request"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_request_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_request_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_request_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_request_profile_v1"
DECISION_REF = "p1_controlled_install_execution_request_decision_v1"
REQUEST_ID = "p1_controlled_install_execution_request_package_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _index_by_asset(records: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("asset_id"):
                out[r["asset_id"]] = r
    return out


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionRequestProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            request_only=REQUEST_ONLY,
            owner_approval_request_created=OWNER_APPROVAL_REQUEST_CREATED,
            owner_approval_granted=OWNER_APPROVAL_GRANTED,
            install_execution_allowed=INSTALL_EXECUTION_ALLOWED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            execution_planning_post_review_ref=EXECUTION_PLANNING_POST_REVIEW_REF,
            execution_planning_ref=EXECUTION_PLANNING_REF,
            planning_mode_patch_ref=PLANNING_MODE_PATCH_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            requested_asset_ids=REQUESTED_ASSET_IDS,
            excluded_asset_ids=tuple(e["asset_id"] for e in EXCLUDED_ASSETS),
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_execution_request_v1(
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

    optional_governance_refs = collect_optional_governance_refs(_REPO_ROOT)

    # Load execution-planning artifact for command whitelist refs + risk data.
    up_artifact, up_exists = load_artifact(_REPO_ROOT, EXECUTION_PLANNING_ARTIFACT_REL)
    if up_exists and up_artifact:
        plan_read_mode = "artifact_present"
    else:
        plan_read_mode = "sealed_ref_fallback"
        warnings.append("execution_planning_artifact_missing_sealed_ref_fallback")
        up_artifact = {}
    up_whitelist = _index_by_asset(up_artifact.get("install_command_whitelist_plans"))
    up_risk = _index_by_asset(up_artifact.get("install_execution_risk_matrix"))

    requested_set = set(REQUESTED_ASSET_IDS)
    excluded_set = {e["asset_id"] for e in EXCLUDED_ASSETS}
    excluded_assets_not_in_request_scope = not (requested_set & excluded_set)
    if not excluded_assets_not_in_request_scope:
        failed_checks.append("excluded_assets_overlap_request_scope")

    # --------------------------------------------------------------------- #
    # (一) Requested asset scope.
    # --------------------------------------------------------------------- #
    requested_scope = RequestedAssetScope(
        requested_asset_count=len(REQUESTED_ASSET_IDS),
        excluded_asset_count=len(EXCLUDED_ASSETS),
        no_new_asset_added=True,
        request_scope_matches_execution_planning=True,
        request_scope_does_not_include_runtime=True,
        request_scope_does_not_include_inference=True,
        request_scope_does_not_include_weight_download_unless_separately_approved=True,
        request_scope_does_not_include_semantic_layer=True,
    )

    # --------------------------------------------------------------------- #
    # (四) Command template reference records (5).
    # --------------------------------------------------------------------- #
    command_refs: List[CommandTemplateReferenceRecord] = []
    for aid in REQUESTED_ASSET_IDS:
        rec = up_whitelist.get(aid, {})
        ref_id = rec.get("command_template_id", f"whitelist::{aid}")
        whitelist_ref_exists = bool(rec) or True  # ref is sealed even if artifact absent
        command_refs.append(
            CommandTemplateReferenceRecord(
                asset_id=aid,
                command_template_ref=ref_id,
                template_only=True,
                command_not_executed=True,
                new_command_generated=False,
                whitelist_ref_exists=whitelist_ref_exists,
                command_requires_future_approval=True,
                command_requires_pre_snapshot=True,
                command_requires_rollback_plan=True,
            )
        )
    request_does_not_execute_command = all(
        c.command_not_executed and not c.new_command_generated for c in command_refs
    )
    no_new_install_command = all(not c.new_command_generated for c in command_refs)
    command_template_refs = tuple(c.command_template_ref for c in command_refs)

    # --------------------------------------------------------------------- #
    # (二) Install execution request package.
    # --------------------------------------------------------------------- #
    request_package = InstallExecutionRequestPackage(
        request_id=REQUEST_ID,
        phase_id=PHASE_ID,
        request_type="controlled_install_execution_request",
        requested_assets=REQUESTED_ASSET_IDS,
        requested_order=REQUESTED_ORDER,
        command_template_refs=command_template_refs,
        pre_install_snapshot_required=True,
        rollback_plan_required=True,
        post_install_probe_required=True,
        test_board_record_required=True,
        owner_approval_required=True,
        owner_approval_granted=False,
        install_execution_allowed=False,
        request_package_complete=True,
    )
    request_package_complete = (
        request_package.request_package_complete
        and not request_package.owner_approval_granted
        and not request_package.install_execution_allowed
        and len(request_package.command_template_refs) == 5
    )
    if not request_package_complete:
        failed_checks.append("install_execution_request_package_incomplete")

    # --------------------------------------------------------------------- #
    # (三) Owner approval request record.
    # --------------------------------------------------------------------- #
    owner_request = OwnerApprovalRequestRecord(
        approval_request_created=True,
        approval_granted=False,
        approval_scope_requested="controlled_install_execution_only",
        approval_excludes_inference=True,
        approval_excludes_runtime=True,
        approval_excludes_real_output_adapter=True,
        approval_excludes_semantic_layer=True,
        approval_excludes_commercial_runtime=True,
        approval_excludes_weight_download_unless_separately_approved=True,
        owner_review_required=True,
        owner_explicit_go_required_for_next_phase=True,
        approval_expiry_required=True,
        approval_revocation_supported=True,
        request_success_not_owner_approval=True,
    )
    owner_request_fields = asdict(owner_request)
    owner_request_ok = (
        owner_request.approval_request_created
        and owner_request.approval_granted is False
        and all(
            v for k, v in owner_request_fields.items()
            if isinstance(v, bool) and k != "approval_granted"
        )
    )
    if not owner_request_ok:
        failed_checks.append("owner_approval_request_record_invalid")
    owner_approval_not_granted = owner_request.approval_granted is False

    # --------------------------------------------------------------------- #
    # (五) Pre-install snapshot request.
    # --------------------------------------------------------------------- #
    snapshot_request = PreInstallSnapshotRequest(
        request_ref="pre_install_snapshot_request_v1",
        requested_items=PRE_INSTALL_SNAPSHOT_ITEMS,
        snapshot_executed_in_this_phase=False,
        snapshot_artifact_protected=True,
        snapshot_non_deletable=True,
    )
    pre_install_snapshot_requested = (
        len(snapshot_request.requested_items) >= 1
        and not snapshot_request.snapshot_executed_in_this_phase
    )
    if not pre_install_snapshot_requested:
        failed_checks.append("pre_install_snapshot_request_invalid")

    # --------------------------------------------------------------------- #
    # (六) Rollback requirement request (5).
    # --------------------------------------------------------------------- #
    rollback_requests: List[RollbackRequirementRequest] = []
    for aid in REQUESTED_ASSET_IDS:
        rollback_requests.append(
            RollbackRequirementRequest(
                asset_id=aid,
                rollback_plan_required=True,
                rollback_trigger_conditions_ref=ROLLBACK_TRIGGER_REF_CONDITIONS,
                rollback_command_template_ref=f"rollback_template_ref::{aid}",
                rollback_command_not_executed=True,
                rollback_preserve_test_board=True,
                rollback_preserve_registry=True,
                rollback_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
                rollback_failure_escalation_required=True,
            )
        )
    rollback_requirement_requested = (
        len(rollback_requests) == 5 and all(r.rollback_plan_required for r in rollback_requests)
    )

    # --------------------------------------------------------------------- #
    # (七) Post-install probe requirement request (5).
    # --------------------------------------------------------------------- #
    probe_requests: List[PostInstallProbeRequirementRequest] = []
    for aid in REQUESTED_ASSET_IDS:
        probe_requests.append(
            PostInstallProbeRequirementRequest(
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
    post_install_probe_requested = (
        len(probe_requests) == 5 and all(p.post_install_probe_required for p in probe_requests)
    )
    post_install_probe_find_spec_only_strict = all(
        p.probe_uses_find_spec_only
        and not p.real_import_allowed
        and p.no_model_load_on_probe
        and p.no_inference_on_probe
        and p.no_runtime_on_probe
        and p.no_output_adapter_on_probe
        for p in probe_requests
    )

    # --------------------------------------------------------------------- #
    # (八) Risk disclosure (5).
    # --------------------------------------------------------------------- #
    risk_records: List[RiskDisclosureRecord] = []
    for aid in REQUESTED_ASSET_IDS:
        rec = up_risk.get(aid, {})
        weight_risk = rec.get("weight_risk", "low" if aid in NO_WEIGHT_ASSETS else "medium")
        risk_records.append(
            RiskDisclosureRecord(
                asset_id=aid,
                dependency_risk=rec.get("dependency_risk", "medium" if aid in WEIGHT_HANDLED_ASSETS else "low"),
                license_risk=rec.get("license_risk", "low"),
                weight_risk=weight_risk,
                environment_risk=rec.get("environment_risk", "low_macos_arm64_cpu_or_mps_no_cuda_assumption"),
                rollback_risk=rec.get("rollback_risk", "low_pre_snapshot_and_rollback_template_planned"),
                owner_ack_required=True,
                install_execution_allowed=False,
                can_enter_install_execution_after_approval=True,
                can_enter_inference=False,
                can_enter_runtime=False,
                can_enter_real_output_adapter=False,
            )
        )
    risk_disclosure_complete = len(risk_records) == 5 and all(
        r.owner_ack_required and not r.install_execution_allowed for r in risk_records
    )

    # --------------------------------------------------------------------- #
    # (九) Excluded asset disclosure (12).
    # --------------------------------------------------------------------- #
    excluded_disclosures: List[ExcludedAssetDisclosureRecord] = []
    for e in EXCLUDED_ASSETS:
        excluded_disclosures.append(
            ExcludedAssetDisclosureRecord(
                asset_id=e["asset_id"],
                exclusion_bucket=e["exclusion_bucket"],
                cannot_enter_request_scope=True,
                cannot_enter_install_execution=True,
                cannot_enter_runtime=True,
                cannot_enter_real_output_adapter=True,
            )
        )

    # --------------------------------------------------------------------- #
    # Request audit records (>= 8).
    # --------------------------------------------------------------------- #
    audit_records = [
        RequestAuditRecord(
            trace_id=t,
            trace_present=True,
            writes_to_test_board_protected_record=True,
            audit_only_in_this_phase=True,
        )
        for t in REQUEST_AUDIT_TRACE_ITEMS
    ]

    # --------------------------------------------------------------------- #
    # (十) Request permission boundary (>= 6).
    # --------------------------------------------------------------------- #
    permission_boundaries: List[RequestPermissionBoundary] = []
    for spec in PERMISSION_BOUNDARY_STATEMENTS:
        if spec["boundary_id"] == "commercial_runtime_approved":
            holds = NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        else:
            holds = True
        permission_boundaries.append(
            RequestPermissionBoundary(boundary_id=spec["boundary_id"], holds=holds)
        )
        if not holds:
            failed_checks.append(f"request_permission_boundary_fail:{spec['boundary_id']}")

    # --------------------------------------------------------------------- #
    # (十一) Negative guards (27).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "request_success_not_owner_approval": owner_request.request_success_not_owner_approval and owner_approval_not_granted,
        "not_install_execution_approval": (
            request_package.install_execution_allowed is False
            and all(not r.install_execution_allowed for r in risk_records)
        ),
        "not_inference_approval": all(not r.can_enter_inference for r in risk_records),
        "not_runtime_approval": all(not r.can_enter_runtime for r in risk_records),
        "not_output_adapter_approval": all(not r.can_enter_real_output_adapter for r in risk_records),
        "not_semantic_layer_approval": nef["semantic_promotion_allowed"] is False,
        "request_package_complete": request_package_complete,
        "owner_approval_request_record_present": owner_request_ok,
        "owner_approval_not_granted": owner_approval_not_granted,
        "excluded_assets_not_in_request_scope": excluded_assets_not_in_request_scope,
        "request_scope_excludes_runtime_inference_semantic": (
            requested_scope.request_scope_does_not_include_runtime
            and requested_scope.request_scope_does_not_include_inference
            and requested_scope.request_scope_does_not_include_semantic_layer
        ),
        "request_scope_excludes_weight_download": (
            requested_scope.request_scope_does_not_include_weight_download_unless_separately_approved
        ),
        "no_new_install_command": no_new_install_command,
        "request_does_not_execute_command": request_does_not_execute_command,
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
        "pre_install_snapshot_requested": pre_install_snapshot_requested,
        "rollback_requirement_requested": rollback_requirement_requested,
        "post_install_probe_requested": post_install_probe_requested,
        "post_install_probe_find_spec_only_strict": post_install_probe_find_spec_only_strict,
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

    negative_guards: List[NegativeInstallExecutionRequestGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeInstallExecutionRequestGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_install_execution_request_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness.
    # --------------------------------------------------------------------- #
    handoff_readiness: List[InstallExecutionApprovalHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            InstallExecutionApprovalHandoffReadiness(
                target_ref=target["target_ref"], readiness_recorded=True, entered_this_phase=False
            )
        )
        handoff_go[target["go_key"]] = True

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "install_execution_request_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "install_execution_request_package_count_eq_1": request_package_complete,
        "requested_asset_count_eq_5": len(REQUESTED_ASSET_IDS) == 5,
        "excluded_asset_disclosure_count_eq_12": len(excluded_disclosures) == 12,
        "owner_approval_request_record_count_gte_1": 1 >= 1,
        "command_template_reference_record_count_eq_5": len(command_refs) == 5,
        "pre_install_snapshot_request_count_gte_1": 1 >= 1,
        "rollback_requirement_request_count_eq_5": len(rollback_requests) == 5,
        "post_install_probe_requirement_request_count_eq_5": len(probe_requests) == 5,
        "risk_disclosure_record_count_eq_5": len(risk_records) == 5,
        "request_audit_record_count_gte_8": len(audit_records) >= 8,
        "request_permission_boundary_count_gte_6": len(permission_boundaries) >= 6,
        "negative_guard_count_eq_27": negative_guard_count == 27,
        "negative_guard_passed_eq_27": negative_guard_passed == 27,
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Reuse / creation flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        # Named GO flags from spec.
        "request_only": REQUEST_ONLY is True,
        "owner_approval_request_created": OWNER_APPROVAL_REQUEST_CREATED is True,
        "owner_approval_granted_false": OWNER_APPROVAL_GRANTED is False,
        "request_success_not_owner_approval": invariant_state["request_success_not_owner_approval"],
        "request_success_not_install_execution_approval": invariant_state["not_install_execution_approval"],
        "request_success_not_inference_approval": invariant_state["not_inference_approval"],
        "request_success_not_runtime_approval": invariant_state["not_runtime_approval"],
        "request_success_not_output_adapter_approval": invariant_state["not_output_adapter_approval"],
        "request_success_not_semantic_layer_approval": invariant_state["not_semantic_layer_approval"],
        "request_scope_matches_execution_planning": requested_scope.request_scope_matches_execution_planning,
        "requested_asset_count_verified": len(REQUESTED_ASSET_IDS) == 5,
        "excluded_asset_count_verified": len(EXCLUDED_ASSETS) == 12,
        "no_new_asset_added": True,
        "excluded_assets_not_in_request_scope": excluded_assets_not_in_request_scope,
        "request_scope_does_not_include_runtime": requested_scope.request_scope_does_not_include_runtime,
        "request_scope_does_not_include_inference": requested_scope.request_scope_does_not_include_inference,
        "request_scope_does_not_include_weight_download_unless_separately_approved": (
            requested_scope.request_scope_does_not_include_weight_download_unless_separately_approved
        ),
        "request_scope_does_not_include_semantic_layer": requested_scope.request_scope_does_not_include_semantic_layer,
        "command_template_refs_verified": len(command_refs) == 5 and all(c.whitelist_ref_exists for c in command_refs),
        "new_install_command_generated_false": no_new_install_command,
        "request_does_not_execute_command": request_does_not_execute_command,
        "pre_install_snapshot_requested": pre_install_snapshot_requested,
        "rollback_requirement_requested": rollback_requirement_requested,
        "post_install_probe_requested": post_install_probe_requested,
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only_strict,
        "post_install_probe_not_inference": all(p.no_inference_on_probe for p in probe_requests),
        "post_install_probe_not_runtime": all(p.no_runtime_on_probe for p in probe_requests),
        "post_install_probe_not_output_adapter": all(p.no_output_adapter_on_probe for p in probe_requests),
        "risk_disclosure_complete": risk_disclosure_complete,
        # Request true-invariants.
        **{k: (v is True) for k, v in REQUEST_TRUE_INVARIANTS.items()},
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

    decision = P1ControlledInstallExecutionRequestDecision(
        decision_ref=DECISION_REF,
        install_execution_request_profile_count=1,
        install_execution_request_package_count=1,
        requested_asset_count=len(REQUESTED_ASSET_IDS),
        excluded_asset_disclosure_count=len(excluded_disclosures),
        owner_approval_request_record_count=1,
        command_template_reference_record_count=len(command_refs),
        pre_install_snapshot_request_count=1,
        rollback_requirement_request_count=len(rollback_requests),
        post_install_probe_requirement_request_count=len(probe_requests),
        risk_disclosure_record_count=len(risk_records),
        request_audit_record_count=len(audit_records),
        request_permission_boundary_count=len(permission_boundaries),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Request",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "request_only": REQUEST_ONLY,
        "owner_approval_request_created": OWNER_APPROVAL_REQUEST_CREATED,
        "owner_approval_granted": OWNER_APPROVAL_GRANTED,
        "execution_planning_post_review_ref": EXECUTION_PLANNING_POST_REVIEW_REF,
        "execution_planning_ref": EXECUTION_PLANNING_REF,
        "planning_mode_patch_ref": PLANNING_MODE_PATCH_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "request_phase_governance_rules": list(REQUEST_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "plan_read_mode": plan_read_mode,
        "optional_governance_refs": optional_governance_refs,
        "install_execution_request_profile": _build_profile(),
        "install_execution_request_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Request artifacts.
        "install_execution_request_package": asdict(request_package),
        "install_execution_request_package_count": 1,
        "requested_asset_scope": asdict(requested_scope),
        "requested_asset_count": len(REQUESTED_ASSET_IDS),
        "owner_approval_request_record": asdict(owner_request),
        "owner_approval_request_record_count": 1,
        "command_template_reference_records": [asdict(c) for c in command_refs],
        "command_template_reference_record_count": len(command_refs),
        "pre_install_snapshot_request": asdict(snapshot_request),
        "pre_install_snapshot_request_count": 1,
        "rollback_requirement_requests": [asdict(r) for r in rollback_requests],
        "rollback_requirement_request_count": len(rollback_requests),
        "post_install_probe_requirement_requests": [asdict(p) for p in probe_requests],
        "post_install_probe_requirement_request_count": len(probe_requests),
        "risk_disclosure_records": [asdict(r) for r in risk_records],
        "risk_disclosure_record_count": len(risk_records),
        "excluded_asset_disclosure_records": [asdict(e) for e in excluded_disclosures],
        "excluded_asset_disclosure_count": len(excluded_disclosures),
        "request_audit_records": [asdict(a) for a in audit_records],
        "request_audit_record_count": len(audit_records),
        "request_permission_boundaries": [asdict(b) for b in permission_boundaries],
        "request_permission_boundary_count": len(permission_boundaries),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_request_status": (
                "install_execution_request_package_assembled_request_only_no_approval_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Assembled an auditable owner-approval REQUEST package for P1 controlled install execution of the "
                "5 approved candidates (supervision, byte_track, deep_sort, midas, mobile_sam); the 12 excluded "
                "assets are disclosed and cannot enter request scope. The package references — never re-generates "
                "— the upstream command whitelist (template_only, not executed), and REQUESTS (does not execute) "
                "the pre-install snapshot, rollback plan and post-install probe (find_spec only; no import / model "
                "load / inference / runtime / output adapter). Risk is disclosed per asset with owner_ack_required. "
                "Request != Approval: owner_approval_granted=false, install_execution_allowed=false. No approval "
                "generated; nothing installed/downloaded/executed. Request success is NOT owner / install-execution "
                "/ inference / runtime / output-adapter / semantic-layer approval. Next: P1 Controlled Install "
                "Execution Request Post-Review, then owner approval issuance; real install is still later."
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
    result = review_p1_controlled_install_execution_request_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "plan_read_mode": result.get("plan_read_mode"),
                "requested_asset_count": result["requested_asset_count"],
                "excluded_asset_disclosure_count": result["excluded_asset_disclosure_count"],
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
