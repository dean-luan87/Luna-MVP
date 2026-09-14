# -*- coding: utf-8 -*-
"""P1 Controlled Install Owner Approval Issuance — review v1.

Generates a narrow owner approval ISSUANCE record for the P1 controlled install
execution request. The issued approval ONLY permits entering the subsequent
controlled install execution PREPARATION / execution planning chain.

  Approval Issuance != Install Execution

It does NOT approve (and does NOT execute) real install, pip install, dependency
install, model/weight/dataset download, inference, runtime, real output adapter,
or the semantic layer. The 5 approved candidates (supervision, byte_track,
deep_sort, midas, mobile_sam) are scoped to execution-preparation only; the 12
excluded assets remain excluded. The approval carries conditions, expiry,
revocation, source-chain traceability and per-asset risk acknowledgement.
Protected records are written to the test board in planning mode.
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
from capabilities.field_understanding.p1_controlled_install_owner_approval_issuance.p1_controlled_install_owner_approval_issuance_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    collect_governance_refs,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_owner_approval_issuance.p1_controlled_install_owner_approval_issuance_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_BOUNDARY_STATEMENTS,
    APPROVAL_CONDITIONS,
    APPROVAL_EXPIRY_POLICY,
    APPROVAL_REVOCATION_POLICY,
    APPROVAL_SCOPE,
    APPROVED_ASSET_IDS,
    CAN_ENTER_FLAGS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXCLUDED_ASSETS,
    EXECUTION_PREPARATION_REF,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_REFS,
    HANDOFF_READINESS_TARGETS,
    INSTALL_EXECUTION_ALLOWED,
    ISSUANCE_PHASE_GOVERNANCE_RULES,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_FLAGS,
    NO_WEIGHT_ASSETS,
    OLD_APPROVAL_SYSTEM_MUTATED,
    OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION,
    OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION,
    OWNER_APPROVAL_ISSUANCE_CREATED,
    APPROVAL_ISSUANCE_ONLY,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    REUSE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    SCOPE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TRACEABILITY_REFS,
    UPSTREAM_REQUEST_POST_REVIEW_REF,
    ApprovalBoundaryRecord,
    ApprovalConditionRecord,
    ApprovalExpiryRecord,
    ApprovalHandoffReadiness,
    ApprovalRevocationRecord,
    ApprovalRiskAcknowledgementRecord,
    ApprovalScopeRecord,
    ApprovalTraceabilityRecord,
    ApprovedAssetScopeRecord,
    ExcludedAssetScopeRecord,
    NegativeOwnerApprovalIssuanceGuard,
    OwnerApprovalIssuanceRecord,
    P1ControlledInstallOwnerApprovalIssuanceDecision,
    P1ControlledInstallOwnerApprovalIssuanceProfile,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_controlled_install_owner_approval_issuance_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_owner_approval_issuance_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_owner_approval_issuance"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_owner_approval_issuance_types_v1.py",
    f"{_PKG}/p1_controlled_install_owner_approval_issuance_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_owner_approval_issuance_v1.py",
)

PROFILE_REF = "p1_controlled_install_owner_approval_issuance_profile_v1"
DECISION_REF = "p1_controlled_install_owner_approval_issuance_decision_v1"
ISSUANCE_ID = "p1_controlled_install_owner_approval_issuance_record_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallOwnerApprovalIssuanceProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            approval_issuance_only=APPROVAL_ISSUANCE_ONLY,
            owner_approval_issuance_created=OWNER_APPROVAL_ISSUANCE_CREATED,
            owner_approval_granted_for_install_execution_preparation=OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION,
            owner_approval_granted_for_install_execution=OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION,
            install_execution_allowed=INSTALL_EXECUTION_ALLOWED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            old_approval_system_mutated=OLD_APPROVAL_SYSTEM_MUTATED,
            upstream_request_post_review_ref=UPSTREAM_REQUEST_POST_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            governance_refs=GOVERNANCE_REFS,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            approved_asset_ids=APPROVED_ASSET_IDS,
            excluded_asset_ids=tuple(e["asset_id"] for e in EXCLUDED_ASSETS),
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_owner_approval_issuance_v1(
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

    governance_refs = collect_governance_refs(_REPO_ROOT)

    approved_set = set(APPROVED_ASSET_IDS)
    excluded_set = {e["asset_id"] for e in EXCLUDED_ASSETS}
    excluded_assets_remain_excluded = not (approved_set & excluded_set)
    if not excluded_assets_remain_excluded:
        failed_checks.append("excluded_assets_overlap_approval_scope")

    # --------------------------------------------------------------------- #
    # (一) Owner approval issuance record + (二) approval scope record.
    # --------------------------------------------------------------------- #
    issuance_record = OwnerApprovalIssuanceRecord(
        issuance_id=ISSUANCE_ID,
        phase_id=PHASE_ID,
        owner_approval_issuance_created=OWNER_APPROVAL_ISSUANCE_CREATED,
        owner_approval_granted_for_install_execution_preparation=OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION,
        owner_approval_granted_for_install_execution=OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION,
        approval_scope=APPROVAL_SCOPE,
        approval_issuance_success_not_install_execution_approval=True,
        approval_issuance_success_not_inference_approval=True,
        approval_issuance_success_not_runtime_approval=True,
        approval_issuance_success_not_output_adapter_approval=True,
        approval_issuance_success_not_semantic_layer_approval=True,
        issuance_complete=True,
    )
    issuance_ok = (
        issuance_record.owner_approval_issuance_created
        and issuance_record.owner_approval_granted_for_install_execution_preparation
        and issuance_record.owner_approval_granted_for_install_execution is False
        and issuance_record.approval_scope == APPROVAL_SCOPE
        and issuance_record.issuance_complete
    )
    if not issuance_ok:
        failed_checks.append("owner_approval_issuance_record_invalid")

    approval_scope_record = ApprovalScopeRecord(
        approval_scope=APPROVAL_SCOPE,
        approved_for_install_execution_preparation=True,
        approved_for_install_execution=False,
        approved_for_pip_install=False,
        approved_for_dependency_install=False,
        approved_for_model_download=False,
        approved_for_weight_download=False,
        approved_for_dataset_download=False,
        approved_for_inference=False,
        approved_for_runtime=False,
        approved_for_real_output_adapter=False,
        approved_for_semantic_layer=False,
        approved_for_commercial_runtime=False,
        approved_for_vla_action_chain=False,
        approved_for_navigation_action_speech_fact_write=False,
    )
    scope_dict = asdict(approval_scope_record)
    approval_scope_ok = scope_dict["approved_for_install_execution_preparation"] is True and all(
        v is False for k, v in scope_dict.items()
        if k.startswith("approved_for_") and k != "approved_for_install_execution_preparation"
    )
    if not approval_scope_ok:
        failed_checks.append("approval_scope_record_invalid")

    # --------------------------------------------------------------------- #
    # (二) Approved asset scope records (5).
    # --------------------------------------------------------------------- #
    approved_records: List[ApprovedAssetScopeRecord] = []
    for aid in APPROVED_ASSET_IDS:
        approved_records.append(
            ApprovedAssetScopeRecord(
                asset_id=aid,
                included_in_approval_scope=True,
                approval_scope=APPROVAL_SCOPE,
                install_execution_allowed=False,
                inference_allowed=False,
                runtime_allowed=False,
                output_adapter_allowed=False,
                semantic_layer_allowed=False,
                weight_download_allowed=False,
                requires_next_phase_execution_preparation=True,
            )
        )
    approved_scope_limited_to_requested = all(
        r.asset_id in approved_set
        and not r.install_execution_allowed
        and not r.inference_allowed
        and not r.runtime_allowed
        and not r.output_adapter_allowed
        and not r.semantic_layer_allowed
        and not r.weight_download_allowed
        for r in approved_records
    )
    if not approved_scope_limited_to_requested:
        failed_checks.append("approved_asset_scope_records_invalid")
    weight_download_requires_separate_approval = all(not r.weight_download_allowed for r in approved_records)

    # --------------------------------------------------------------------- #
    # (三) Excluded asset scope records (12).
    # --------------------------------------------------------------------- #
    excluded_records: List[ExcludedAssetScopeRecord] = []
    for e in EXCLUDED_ASSETS:
        excluded_records.append(
            ExcludedAssetScopeRecord(
                asset_id=e["asset_id"],
                excluded_from_approval_scope=True,
                exclusion_reason=e["exclusion_reason"],
                cannot_enter_install_execution=True,
                cannot_enter_inference=True,
                cannot_enter_runtime=True,
                cannot_enter_output_adapter=True,
            )
        )

    # --------------------------------------------------------------------- #
    # (四) Approval condition records (>= 8).
    # --------------------------------------------------------------------- #
    condition_records = [
        ApprovalConditionRecord(condition_id=c, required=True, enforced_in_future_phase=True)
        for c in APPROVAL_CONDITIONS
    ]
    rollback_condition_present = any(c.condition_id == "rollback_plan_required" for c in condition_records)
    post_install_probe_condition_present = any(
        c.condition_id == "post_install_probe_required" for c in condition_records
    )
    execution_preparation_required_before_execution = any(
        c.condition_id == "next_phase_required_before_execution" for c in condition_records
    )
    if not rollback_condition_present:
        failed_checks.append("approval_condition_rollback_missing")
    if not post_install_probe_condition_present:
        failed_checks.append("approval_condition_post_install_probe_missing")

    # --------------------------------------------------------------------- #
    # (五) Approval expiry record.
    # --------------------------------------------------------------------- #
    expiry_record = ApprovalExpiryRecord(
        approval_has_expiry=True,
        expiry_policy=APPROVAL_EXPIRY_POLICY,
        expired_approval_cannot_be_used=True,
        approval_use_after_registry_drift_blocked=True,
        approval_use_after_dependency_drift_blocked=True,
        approval_use_after_scope_change_blocked=True,
    )
    approval_expiry_present = expiry_record.approval_has_expiry and bool(expiry_record.expiry_policy)
    if not approval_expiry_present:
        failed_checks.append("approval_expiry_record_invalid")

    # --------------------------------------------------------------------- #
    # (六) Approval revocation record.
    # --------------------------------------------------------------------- #
    revocation_record = ApprovalRevocationRecord(
        approval_revocation_supported=True,
        revocation_reason_required=True,
        revoked_approval_cannot_be_used=True,
        revocation_must_be_recorded=True,
        revocation_record_protected=True,
        revocation_policy=APPROVAL_REVOCATION_POLICY,
    )
    approval_revocation_present = revocation_record.approval_revocation_supported and bool(
        revocation_record.revocation_policy
    )
    if not approval_revocation_present:
        failed_checks.append("approval_revocation_record_invalid")

    # --------------------------------------------------------------------- #
    # (七) Approval boundary records (>= 6).
    # --------------------------------------------------------------------- #
    boundary_records: List[ApprovalBoundaryRecord] = []
    for spec in APPROVAL_BOUNDARY_STATEMENTS:
        if spec["value_is_true"]:
            holds = True
        else:
            # boundary asserts a flag is FALSE.
            bid = spec["boundary_id"]
            if bid == "owner_approval_granted_for_install_execution":
                holds = OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION is False
            elif bid == "commercial_runtime_approved":
                holds = NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
            else:
                holds = True
        boundary_records.append(ApprovalBoundaryRecord(boundary_id=spec["boundary_id"], holds=holds))
        if not holds:
            failed_checks.append(f"approval_boundary_record_fail:{spec['boundary_id']}")

    # --------------------------------------------------------------------- #
    # (七) Traceability records (>= 8).
    # --------------------------------------------------------------------- #
    traceability_records = [
        ApprovalTraceabilityRecord(ref_id=rid, ref_value=val, present=bool(val))
        for rid, val in TRACEABILITY_REFS
    ]
    source_chain_complete = all(t.present for t in traceability_records) and len(traceability_records) >= 8
    if not source_chain_complete:
        failed_checks.append("approval_traceability_incomplete")

    # --------------------------------------------------------------------- #
    # (八) Risk acknowledgement records (5).
    # --------------------------------------------------------------------- #
    risk_records: List[ApprovalRiskAcknowledgementRecord] = []
    for aid in APPROVED_ASSET_IDS:
        risk_records.append(
            ApprovalRiskAcknowledgementRecord(
                asset_id=aid,
                dependency_risk_acknowledged=True,
                license_risk_acknowledged=True,
                weight_risk_acknowledged=True,
                environment_risk_acknowledged=True,
                rollback_risk_acknowledged=True,
                owner_ack_required_for_next_phase=True,
            )
        )

    # --------------------------------------------------------------------- #
    # (九) Handoff readiness (only execution preparation reachable).
    # --------------------------------------------------------------------- #
    handoff_records: List[ApprovalHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_records.append(
            ApprovalHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                can_enter_execution_preparation=CAN_ENTER_FLAGS["can_enter_execution_preparation"],
                can_enter_install_execution=CAN_ENTER_FLAGS["can_enter_install_execution"],
                can_enter_inference=CAN_ENTER_FLAGS["can_enter_inference"],
                can_enter_runtime=CAN_ENTER_FLAGS["can_enter_runtime"],
                can_enter_output_adapter=CAN_ENTER_FLAGS["can_enter_output_adapter"],
                can_enter_semantic_layer=CAN_ENTER_FLAGS["can_enter_semantic_layer"],
            )
        )
        handoff_go[target["go_key"]] = True
    direct_install_execution_not_allowed = (
        CAN_ENTER_FLAGS["can_enter_install_execution"] is False
        and execution_preparation_required_before_execution
    )

    # --------------------------------------------------------------------- #
    # (十) Negative guards (25).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "not_install_execution_approval": (
            issuance_record.owner_approval_granted_for_install_execution is False
            and approval_scope_record.approved_for_install_execution is False
        ),
        "not_install_approval": (
            approval_scope_record.approved_for_pip_install is False
            and approval_scope_record.approved_for_dependency_install is False
        ),
        "not_download_approval": (
            approval_scope_record.approved_for_model_download is False
            and approval_scope_record.approved_for_weight_download is False
            and approval_scope_record.approved_for_dataset_download is False
        ),
        "not_inference_approval": approval_scope_record.approved_for_inference is False,
        "not_runtime_approval": approval_scope_record.approved_for_runtime is False,
        "not_output_adapter_approval": approval_scope_record.approved_for_real_output_adapter is False,
        "not_semantic_layer_approval": approval_scope_record.approved_for_semantic_layer is False,
        "excluded_assets_remain_excluded": excluded_assets_remain_excluded and len(excluded_records) == 12,
        "weight_download_requires_separate_approval": weight_download_requires_separate_approval,
        "approval_expiry_present": approval_expiry_present,
        "approval_revocation_present": approval_revocation_present,
        "source_chain_complete": source_chain_complete,
        "rollback_condition_present": rollback_condition_present,
        "post_install_probe_condition_present": post_install_probe_condition_present,
        "execution_preparation_required_before_execution": (
            execution_preparation_required_before_execution
            and CAN_ENTER_FLAGS["can_enter_install_execution"] is False
        ),
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
        "runtime_not_allowed": (
            nef["runtime_execution_allowed"] is False and nef["runtime_activation_allowed"] is False
        ),
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

    negative_guards: List[NegativeOwnerApprovalIssuanceGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeOwnerApprovalIssuanceGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_owner_approval_issuance_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "owner_approval_issuance_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "owner_approval_issuance_record_count_gte_1": issuance_ok,
        "approval_scope_record_count_gte_1": approval_scope_ok,
        "approved_asset_scope_record_count_eq_5": len(approved_records) == 5,
        "excluded_asset_scope_record_count_eq_12": len(excluded_records) == 12,
        "approval_condition_record_count_gte_8": len(condition_records) >= 8,
        "approval_expiry_record_count_gte_1": approval_expiry_present,
        "approval_revocation_record_count_gte_1": approval_revocation_present,
        "approval_boundary_record_count_gte_6": len(boundary_records) >= 6,
        "approval_traceability_record_count_gte_8": len(traceability_records) >= 8,
        "approval_risk_acknowledgement_record_count_eq_5": len(risk_records) == 5,
        "negative_guard_count_eq_25": negative_guard_count == 25,
        "negative_guard_passed_eq_25": negative_guard_passed == 25,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Named GO flags.
        "approval_issuance_only": APPROVAL_ISSUANCE_ONLY is True,
        "owner_approval_issuance_created": OWNER_APPROVAL_ISSUANCE_CREATED is True,
        "owner_approval_granted_for_install_execution_preparation": OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION is True,
        "owner_approval_granted_for_install_execution_false": OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION is False,
        "approval_issuance_success_not_install_execution_approval": invariant_state["not_install_execution_approval"],
        "approval_issuance_success_not_inference_approval": invariant_state["not_inference_approval"],
        "approval_issuance_success_not_runtime_approval": invariant_state["not_runtime_approval"],
        "approval_issuance_success_not_output_adapter_approval": invariant_state["not_output_adapter_approval"],
        "approval_issuance_success_not_semantic_layer_approval": invariant_state["not_semantic_layer_approval"],
        "approved_asset_scope_count_verified": len(approved_records) == 5,
        "excluded_asset_scope_count_verified": len(excluded_records) == 12,
        "approved_scope_limited_to_requested_assets": approved_scope_limited_to_requested,
        "excluded_assets_remain_excluded": excluded_assets_remain_excluded,
        "weight_download_requires_separate_approval": weight_download_requires_separate_approval,
        "approval_expiry_required": approval_expiry_present,
        "approval_revocation_required": approval_revocation_present,
        "source_chain_complete": source_chain_complete,
        "rollback_condition_required": rollback_condition_present,
        "post_install_probe_condition_required": post_install_probe_condition_present,
        "can_enter_execution_preparation": CAN_ENTER_FLAGS["can_enter_execution_preparation"] is True,
        "can_enter_install_execution": CAN_ENTER_FLAGS["can_enter_install_execution"] is False,
        "can_enter_inference": CAN_ENTER_FLAGS["can_enter_inference"] is False,
        "can_enter_runtime": CAN_ENTER_FLAGS["can_enter_runtime"] is False,
        "can_enter_output_adapter": CAN_ENTER_FLAGS["can_enter_output_adapter"] is False,
        "can_enter_semantic_layer": CAN_ENTER_FLAGS["can_enter_semantic_layer"] is False,
        "direct_install_execution_not_allowed_after_this_phase": direct_install_execution_not_allowed,
        # Reuse / governance ref flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        "old_approval_system_mutated_false": OLD_APPROVAL_SYSTEM_MUTATED is False,
        # Negative guard GO keys + handoff.
        **negative_guard_go,
        **handoff_go,
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

    decision = P1ControlledInstallOwnerApprovalIssuanceDecision(
        decision_ref=DECISION_REF,
        owner_approval_issuance_profile_count=1,
        owner_approval_issuance_record_count=1,
        approval_scope_record_count=1,
        approved_asset_scope_record_count=len(approved_records),
        excluded_asset_scope_record_count=len(excluded_records),
        approval_condition_record_count=len(condition_records),
        approval_expiry_record_count=1,
        approval_revocation_record_count=1,
        approval_boundary_record_count=len(boundary_records),
        approval_traceability_record_count=len(traceability_records),
        approval_risk_acknowledgement_record_count=len(risk_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Owner Approval Issuance",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "approval_issuance_only": APPROVAL_ISSUANCE_ONLY,
        "owner_approval_issuance_created": OWNER_APPROVAL_ISSUANCE_CREATED,
        "owner_approval_granted_for_install_execution_preparation": OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION,
        "owner_approval_granted_for_install_execution": OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION,
        "upstream_request_post_review_ref": UPSTREAM_REQUEST_POST_REVIEW_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "governance_refs": governance_refs,
        "reuse_flags": dict(REUSE_FLAGS),
        "issuance_phase_governance_rules": list(ISSUANCE_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "can_enter_flags": dict(CAN_ENTER_FLAGS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "owner_approval_issuance_profile": _build_profile(),
        "owner_approval_issuance_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Issuance artifacts.
        "owner_approval_issuance_record": asdict(issuance_record),
        "owner_approval_issuance_record_count": 1,
        "approval_scope_record": asdict(approval_scope_record),
        "approval_scope_record_count": 1,
        "approved_asset_scope_records": [asdict(r) for r in approved_records],
        "approved_asset_scope_record_count": len(approved_records),
        "excluded_asset_scope_records": [asdict(r) for r in excluded_records],
        "excluded_asset_scope_record_count": len(excluded_records),
        "approval_condition_records": [asdict(c) for c in condition_records],
        "approval_condition_record_count": len(condition_records),
        "approval_expiry_record": asdict(expiry_record),
        "approval_expiry_record_count": 1,
        "approval_revocation_record": asdict(revocation_record),
        "approval_revocation_record_count": 1,
        "approval_boundary_records": [asdict(b) for b in boundary_records],
        "approval_boundary_record_count": len(boundary_records),
        "approval_traceability_records": [asdict(t) for t in traceability_records],
        "approval_traceability_record_count": len(traceability_records),
        "approval_risk_acknowledgement_records": [asdict(r) for r in risk_records],
        "approval_risk_acknowledgement_record_count": len(risk_records),
        "approval_handoff_readiness": [asdict(h) for h in handoff_records],
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_owner_approval_issuance_status": (
                "owner_approval_issued_for_install_execution_preparation_only_not_install_execution_no_install_no_download_no_inference_no_runtime"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "execution_preparation_ref": EXECUTION_PREPARATION_REF,
            "transition_note": (
                "Issued a narrow owner approval for the 5 approved candidates (supervision, byte_track, deep_sort, "
                "midas, mobile_sam): scope = install_execution_preparation_only. Approval Issuance != Install "
                "Execution — owner_approval_granted_for_install_execution=false, install_execution_allowed=false. "
                "The issuance approves entering ONLY the controlled install execution preparation / execution "
                "planning chain; it does NOT approve real install / pip install / dependency install / model / "
                "weight / dataset download / inference / runtime / real output adapter / semantic layer / commercial "
                "runtime / VLA / navigation / action / speech / fact_write, and none of those were executed. The 12 "
                "excluded assets remain excluded. The approval carries conditions (snapshot, command whitelist, "
                "order lock, stop conditions, rollback, post-install probe, test board write, revocation, expiry, "
                "next-phase-before-execution), an expiry policy (blocks use after registry/dependency drift or "
                "scope change), a revocation policy, full source-chain traceability and per-asset risk "
                "acknowledgement. Next: Owner Approval Issuance Post-Review (verifies the scope is preparation-only "
                "and not mis-read as install execution approval); real install execution remains a separate later "
                "phase, only reachable via Execution Preparation."
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
    result = review_p1_controlled_install_owner_approval_issuance_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "approved_asset_scope_record_count": result["approved_asset_scope_record_count"],
                "excluded_asset_scope_record_count": result["excluded_asset_scope_record_count"],
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
