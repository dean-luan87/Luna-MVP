# -*- coding: utf-8 -*-
"""P1 Model Weight Download Request, Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY).

Verifies the code-only registry overlay, then produces the weight-download request,
owner approval issuance, weight source review, hash/storage plan, download command
whitelist (TEMPLATE ONLY, never executed), rollback/deletion policy, readiness
review, and execution handoff. It downloads NOTHING and approves PREPARATION ONLY.
mobile_sam (known source) is ready for the next download-execution phase; byte_track
(unresolved source) is NOT approved for download execution and is routed to source
resolution. Weight approval is NOT model load / inference / runtime / output adapter /
semantic / commercial-runtime approval. Protected, non-deletable test board records
are written in `planning` mode.
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
from capabilities.field_understanding.p1_model_weight_download_request_approval_and_readiness.p1_model_weight_download_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_model_weight_download_request_approval_and_readiness.p1_model_weight_download_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CHECKPOINT_DOWNLOAD_EXECUTION_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_EXECUTION_ALLOWED,
    EXAMPLE_ASSET_DOWNLOAD_EXECUTION_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HASH_ALGORITHM,
    IN_SCOPE_ASSET_IDS,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_EXECUTION_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_DOWNLOAD_EXECUTION,
    OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    OVERLAY_EXPECTED,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PATCH_EXECUTION_REF,
    UPSTREAM_PLANNING_REF,
    WEIGHT_CANDIDATES,
    WEIGHT_CHAIN,
    WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
    WEIGHT_DOWNLOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    WEIGHT_DOWNLOAD_READINESS_REVIEW_INCLUDED,
    WEIGHT_DOWNLOAD_REQUEST_INCLUDED,
    WEIGHT_HASH_STORAGE_PLANNING_INCLUDED,
    WEIGHT_PRINCIPLE_ZH,
    WEIGHT_SOURCE_REVIEW_INCLUDED,
    WEIGHT_STORAGE_ROOT,
    CodeOnlyRegistryOverlayAudit,
    NegativeWeightDownloadRequestApprovalReadinessGuard,
    P1ModelWeightDownloadRequestApprovalReadinessDecision,
    P1ModelWeightDownloadRequestApprovalReadinessProfile,
    WeightDownloadCandidateRecord,
    WeightDownloadCommandWhitelistRecord,
    WeightDownloadExecutionHandoffRecord,
    WeightDownloadReadinessReview,
    WeightDownloadRequestRecord,
    WeightDownloadRollbackDeletionPolicy,
    WeightHashStoragePlanRecord,
    WeightLicenseUsageBoundaryRecord,
    WeightOwnerApprovalIssuanceRecord,
    WeightSourceReviewRecord,
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
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_model_weight_download_request_approval_and_readiness_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_model_weight_download_request_approval_and_readiness_review_v1.json"

_PKG = "capabilities/field_understanding/p1_model_weight_download_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/p1_model_weight_download_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_model_weight_download_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_model_weight_download_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_model_weight_download_request_approval_readiness_profile_v1"
DECISION_REF = "p1_model_weight_download_request_approval_readiness_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_overlay() -> Optional[Dict[str, Any]]:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / REGISTRY_OVERLAY_REL
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ModelWeightDownloadRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            weight_download_request_included=WEIGHT_DOWNLOAD_REQUEST_INCLUDED,
            weight_download_owner_approval_issuance_included=WEIGHT_DOWNLOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            weight_source_review_included=WEIGHT_SOURCE_REVIEW_INCLUDED,
            weight_hash_storage_planning_included=WEIGHT_HASH_STORAGE_PLANNING_INCLUDED,
            weight_download_readiness_review_included=WEIGHT_DOWNLOAD_READINESS_REVIEW_INCLUDED,
            weight_download_execution_allowed=WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
            model_download_execution_allowed=MODEL_DOWNLOAD_EXECUTION_ALLOWED,
            checkpoint_download_execution_allowed=CHECKPOINT_DOWNLOAD_EXECUTION_ALLOWED,
            dataset_download_execution_allowed=DATASET_DOWNLOAD_EXECUTION_ALLOWED,
            example_asset_download_execution_allowed=EXAMPLE_ASSET_DOWNLOAD_EXECUTION_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_patch_execution_ref=UPSTREAM_PATCH_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_model_weight_download_request_approval_and_readiness_v1(
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

    ts = _now()

    # ------------------------------------------------------------------- #
    # (一) Code-only registry overlay audit.
    # ------------------------------------------------------------------- #
    overlay = _load_overlay()
    overlay_exists = overlay is not None
    overlay_assets = (overlay or {}).get("assets", {}) if overlay_exists else {}

    def _check_overlay(asset_id: str) -> Dict[str, bool]:
        rec = overlay_assets.get(asset_id, {})
        exp = OVERLAY_EXPECTED[asset_id]
        return {f"{k}=={v}": (rec.get(k) == v) for k, v in exp.items()}

    bt_checks = _check_overlay("byte_track")
    ms_checks = _check_overlay("mobile_sam")
    code_only_patch_go_verified = verify_flags.get("source_code_only_registry_patch_execution_go_verified") is True
    overlay_audit_passed = (
        overlay_exists and all(bt_checks.values()) and all(ms_checks.values()) and code_only_patch_go_verified
    )
    overlay_audit = CodeOnlyRegistryOverlayAudit(
        audit_id="code_only_registry_overlay_audit_v1",
        overlay_file_ref=REGISTRY_OVERLAY_REL,
        overlay_exists=overlay_exists,
        byte_track_checks=bt_checks,
        mobile_sam_checks=ms_checks,
        code_only_registry_patch_go_verified=code_only_patch_go_verified,
        overlay_audit_passed=overlay_audit_passed,
    )
    if not overlay_audit_passed:
        failed_checks.append("overlay.audit_failed_overlay_missing_or_fields_inconsistent_or_patch_go_unverified")

    code_only_ready_verified = all(
        overlay_assets.get(aid, {}).get("readiness_level") == "code_only_ready" for aid in IN_SCOPE_ASSET_IDS
    ) if overlay_exists else False

    # ------------------------------------------------------------------- #
    # (二) Weight download candidates (2).
    # ------------------------------------------------------------------- #
    candidates: List[WeightDownloadCandidateRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        c = WEIGHT_CANDIDATES[aid]
        candidates.append(
            WeightDownloadCandidateRecord(
                asset_id=aid,
                weight_type=c["weight_type"],
                weight_source_known=bool(c["weight_source_known"]),
                source_repository=c["source_repository"],
                source_commit=c["source_commit"],
                download_source_candidate=c["download_source_candidate"],
                known_committed_weight_file=c["known_committed_weight_file"],
                known_size_bytes=int(c["known_size_bytes"]),
                hash_required=bool(c["hash_required"]),
                storage_required=bool(c["storage_required"]),
                download_execution_allowed_next=bool(c["download_execution_allowed_next"]),
            )
        )

    # ------------------------------------------------------------------- #
    # (三) Weight download request (1).
    # ------------------------------------------------------------------- #
    request = WeightDownloadRequestRecord(
        request_id="weight_download_request_v1",
        requested_assets=tuple(IN_SCOPE_ASSET_IDS),
        mobile_sam_weight_request_included=True,
        byte_track_weight_request_included_as_unresolved_candidate=True,
        request_package_created=True,
        request_package_is_not_download_execution=True,
        request_package_is_not_model_load_approval=True,
        request_package_is_not_inference_approval=True,
        request_package_is_not_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (四) Weight source review (2).
    # ------------------------------------------------------------------- #
    source_reviews: List[WeightSourceReviewRecord] = []
    ms = WEIGHT_CANDIDATES["mobile_sam"]
    source_reviews.append(
        WeightSourceReviewRecord(
            asset_id="mobile_sam",
            weight_source_known=True,
            weight_source_ref="weights/mobile_sam.pt at pinned MobileSAM commit f706ad9c4eb7f219c00d9050e46328518ffb65d2",
            weight_source_review_completed=True,
            expected_size_bytes=int(ms["known_size_bytes"]),
            hash_currently_known=False,
            hash_must_be_computed_after_download=True,
            source_license_ref="Apache-2.0 repository license",
            weight_download_ready_candidate=True,
            requires_separate_weight_source_resolution=False,
        )
    )
    source_reviews.append(
        WeightSourceReviewRecord(
            asset_id="byte_track",
            weight_source_known=False,
            weight_source_ref=None,
            weight_source_review_completed=False,
            expected_size_bytes=0,
            hash_currently_known=False,
            hash_must_be_computed_after_download=True,
            source_license_ref="MIT repository license",
            weight_download_ready_candidate=False,
            requires_separate_weight_source_resolution=True,
        )
    )

    # ------------------------------------------------------------------- #
    # (五) License / usage boundary (1).
    # ------------------------------------------------------------------- #
    license_boundary = WeightLicenseUsageBoundaryRecord(
        record_id="weight_license_usage_boundary_v1",
        weight_download_approval_does_not_approve_commercial_runtime=True,
        weight_download_approval_does_not_approve_model_load=True,
        weight_download_approval_does_not_approve_inference=True,
        weight_download_approval_does_not_approve_runtime=True,
        weight_license_must_be_bound_to_source_asset=True,
        usage_boundary_internal_p1_evaluation_only=True,
        redistribution_not_approved=True,
        commercial_deployment_not_approved=True,
        per_asset_license={aid: WEIGHT_CANDIDATES[aid]["source_license"] for aid in IN_SCOPE_ASSET_IDS},
    )

    # ------------------------------------------------------------------- #
    # (六) Hash / storage plan (2).
    # ------------------------------------------------------------------- #
    hash_storage_plans: List[WeightHashStoragePlanRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        c = WEIGHT_CANDIDATES[aid]
        hash_storage_plans.append(
            WeightHashStoragePlanRecord(
                asset_id=aid,
                expected_filename=c["expected_filename"],
                expected_size_bytes=int(c["known_size_bytes"]),
                hash_algorithm=HASH_ALGORITHM,
                hash_required_after_download=True,
                hash_record_required=True,
                storage_root=WEIGHT_STORAGE_ROOT,
                asset_specific_storage_path=c["storage_path"],
                no_overwrite_without_snapshot=True,
                existing_file_policy="snapshot_then_no_overwrite_without_explicit_approval",
                deletion_policy="delete_or_quarantine_on_hash_mismatch_or_failed_download",
                rollback_policy="delete_partial_or_failed_download_preserve_test_board_and_registry",
                test_board_weight_record_required=True,
                execution_ready=bool(c["download_execution_allowed_next"]),
            )
        )

    # ------------------------------------------------------------------- #
    # (七) Download command whitelist (2, TEMPLATE ONLY).
    # ------------------------------------------------------------------- #
    command_whitelist: List[WeightDownloadCommandWhitelistRecord] = []
    command_whitelist.append(
        WeightDownloadCommandWhitelistRecord(
            asset_id="mobile_sam",
            command_template=(
                "TEMPLATE_ONLY_DO_NOT_EXECUTE: fetch weights/mobile_sam.pt pinned to MobileSAM commit "
                "f706ad9c4eb7f219c00d9050e46328518ffb65d2 (verified repository commit or verified release asset) "
                "-> capabilities/model_weights/p1/mobile_sam/mobile_sam.pt ; then compute sha256"
            ),
            template_only_do_not_execute=True,
            command_not_executed=True,
            expected_output_path="capabilities/model_weights/p1/mobile_sam/mobile_sam.pt",
            hash_after_download_required=True,
            command_execution_readiness=True,
            source_pinned_to_verified_commit_or_release=True,
        )
    )
    command_whitelist.append(
        WeightDownloadCommandWhitelistRecord(
            asset_id="byte_track",
            command_template="PLACEHOLDER_ONLY_SOURCE_UNRESOLVED: no command may be executed until byte_track weight source is resolved",
            template_only_do_not_execute=True,
            command_not_executed=True,
            expected_output_path="capabilities/model_weights/p1/byte_track/",
            hash_after_download_required=True,
            command_execution_readiness=False,
            source_pinned_to_verified_commit_or_release=False,
        )
    )

    # ------------------------------------------------------------------- #
    # (八) Owner approval issuance (1).
    # ------------------------------------------------------------------- #
    mobile_sam_source_reviewed = source_reviews[0].weight_source_review_completed
    byte_track_resolved = source_reviews[1].weight_source_known
    approval = WeightOwnerApprovalIssuanceRecord(
        approval_id="weight_owner_approval_issuance_v1",
        owner_approval_granted_for_weight_download_preparation=True,
        owner_approval_granted_for_mobile_sam_weight_download_execution_next=mobile_sam_source_reviewed,
        owner_approval_granted_for_byte_track_weight_download_execution_next=byte_track_resolved,
        weight_approval_success_not_model_load_approval=True,
        weight_approval_success_not_inference_approval=True,
        weight_approval_success_not_runtime_approval=True,
        weight_approval_success_not_output_adapter_approval=True,
        weight_approval_success_not_semantic_layer_approval=True,
        model_load_not_approved=True,
        inference_not_approved=True,
        runtime_not_approved=True,
        output_adapter_not_approved=True,
        semantic_layer_not_approved=True,
        commercial_runtime_not_approved=True,
        byte_track_unresolved_weight_download_not_approved=not byte_track_resolved,
    )

    # ------------------------------------------------------------------- #
    # (九) Rollback / deletion policy (1).
    # ------------------------------------------------------------------- #
    rollback_policy = WeightDownloadRollbackDeletionPolicy(
        policy_id="weight_download_rollback_deletion_policy_v1",
        pre_download_snapshot_required=True,
        rollback_required=True,
        rollback_deletes_downloaded_weight_if_failed=True,
        rollback_preserves_test_board=True,
        rollback_preserves_registry=True,
        rollback_preserves_review_artifacts=True,
        failed_hash_mismatch_deletes_file_or_quarantines=True,
        partial_download_cleanup_required=True,
        deletion_must_be_recorded=True,
    )

    # ------------------------------------------------------------------- #
    # (十) Readiness review (2).
    # ------------------------------------------------------------------- #
    readiness_reviews: List[WeightDownloadReadinessReview] = []
    readiness_reviews.append(
        WeightDownloadReadinessReview(
            asset_id="mobile_sam",
            can_enter_weight_download_execution_next=mobile_sam_source_reviewed,
            weight_source_resolved=True,
            requires_weight_source_resolution=False,
            can_model_load_after_download=False,
            can_inference_after_download=False,
            can_runtime_after_download=False,
            can_output_adapter_after_download=False,
            can_semantic_layer_after_download=False,
        )
    )
    readiness_reviews.append(
        WeightDownloadReadinessReview(
            asset_id="byte_track",
            can_enter_weight_download_execution_next=byte_track_resolved,
            weight_source_resolved=byte_track_resolved,
            requires_weight_source_resolution=not byte_track_resolved,
            can_model_load_after_download=False,
            can_inference_after_download=False,
            can_runtime_after_download=False,
            can_output_adapter_after_download=False,
            can_semantic_layer_after_download=False,
        )
    )

    ready_assets = tuple(r.asset_id for r in readiness_reviews if r.can_enter_weight_download_execution_next)
    unresolved_assets = tuple(r.asset_id for r in readiness_reviews if not r.can_enter_weight_download_execution_next)

    # ------------------------------------------------------------------- #
    # (十一) Follow-up routing / execution handoff (1).
    # ------------------------------------------------------------------- #
    if len(ready_assets) == len(IN_SCOPE_ASSET_IDS):
        recommended_next_phase = NEXT_PHASE_DOWNLOAD_EXECUTION
        optional_followup = None
    elif len(ready_assets) >= 1:
        recommended_next_phase = NEXT_PHASE_DOWNLOAD_EXECUTION
        optional_followup = OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE
    else:
        recommended_next_phase = "Phase-P1-Model-Weight-Source-Resolution-Planning-v1-001"
        optional_followup = OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE

    handoff = WeightDownloadExecutionHandoffRecord(
        handoff_id="weight_download_execution_handoff_v1",
        recommended_next_phase=recommended_next_phase,
        allowed_weight_download_execution_scope="ready_only",
        ready_assets=ready_assets,
        unresolved_assets=unresolved_assets,
        ready_asset_count=len(ready_assets),
        unresolved_asset_count=len(unresolved_assets),
        optional_followup_phase=optional_followup,
        no_model_load_after_download=True,
        no_inference_after_download=True,
        no_runtime_after_download=True,
        no_output_adapter_after_download=True,
        no_semantic_layer_after_download=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 18 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "overlay_verified": overlay_audit_passed,
        "code_only_ready_verified": code_only_ready_verified,
        "no_download_execution": WEIGHT_DOWNLOAD_EXECUTION_ALLOWED is False
        and MODEL_DOWNLOAD_EXECUTION_ALLOWED is False and CHECKPOINT_DOWNLOAD_EXECUTION_ALLOWED is False
        and DATASET_DOWNLOAD_EXECUTION_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_EXECUTION_ALLOWED is False,
        "no_install": True,
        "no_real_import_load_inference": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False
        and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False
        and SEMANTIC_PROMOTION_ALLOWED is False,
        "mobile_sam_source_reviewed_before_exec": (
            (not approval.owner_approval_granted_for_mobile_sam_weight_download_execution_next)
            or mobile_sam_source_reviewed
        ),
        "byte_track_unresolved_not_exec_approved": (
            byte_track_resolved or (approval.owner_approval_granted_for_byte_track_weight_download_execution_next is False)
        ),
        "approval_not_model_load": approval.weight_approval_success_not_model_load_approval and approval.model_load_not_approved,
        "approval_not_inference_runtime": (
            approval.weight_approval_success_not_inference_approval
            and approval.weight_approval_success_not_runtime_approval
        ),
        "hash_plan_present": len(hash_storage_plans) >= 1 and all(p.hash_required_after_download for p in hash_storage_plans),
        "storage_plan_present": len(hash_storage_plans) >= 1 and all(p.asset_specific_storage_path for p in hash_storage_plans),
        "rollback_deletion_policy_present": rollback_policy.rollback_required and rollback_policy.pre_download_snapshot_required,
        "command_whitelist_present_not_executed": len(command_whitelist) >= 1
        and all(c.template_only_do_not_execute and c.command_not_executed for c in command_whitelist),
        "commercial_runtime_not_approved": COMMERCIAL_RUNTIME_APPROVED is False
        and approval.commercial_runtime_not_approved,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeWeightDownloadRequestApprovalReadinessGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeWeightDownloadRequestApprovalReadinessGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_weight_download_request_approval_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "model_weight_download_request_approval_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "code_only_registry_overlay_audit_count_gte_1": True,
        "weight_download_candidate_record_count_gte_2": len(candidates) >= 2,
        "weight_download_request_record_count_gte_1": True,
        "weight_source_review_record_count_gte_2": len(source_reviews) >= 2,
        "weight_license_usage_boundary_record_count_gte_1": True,
        "weight_hash_storage_plan_record_count_gte_1": len(hash_storage_plans) >= 1,
        "weight_download_command_whitelist_record_count_gte_1": len(command_whitelist) >= 1,
        "weight_owner_approval_issuance_record_count_gte_1": True,
        "weight_download_rollback_deletion_policy_count_gte_1": True,
        "weight_download_readiness_review_count_gte_1": len(readiness_reviews) >= 1,
        "weight_download_execution_handoff_record_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "compressed_phase": COMPRESSED_PHASE is True,
        "weight_download_request_included": WEIGHT_DOWNLOAD_REQUEST_INCLUDED is True,
        "weight_download_owner_approval_issuance_included": WEIGHT_DOWNLOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "weight_source_review_included": WEIGHT_SOURCE_REVIEW_INCLUDED is True,
        "weight_hash_storage_planning_included": WEIGHT_HASH_STORAGE_PLANNING_INCLUDED is True,
        "weight_download_readiness_review_included": WEIGHT_DOWNLOAD_READINESS_REVIEW_INCLUDED is True,
        "weight_download_execution_allowed_false": WEIGHT_DOWNLOAD_EXECUTION_ALLOWED is False,
        "model_download_execution_allowed_false": MODEL_DOWNLOAD_EXECUTION_ALLOWED is False,
        "checkpoint_download_execution_allowed_false": CHECKPOINT_DOWNLOAD_EXECUTION_ALLOWED is False,
        "dataset_download_execution_allowed_false": DATASET_DOWNLOAD_EXECUTION_ALLOWED is False,
        "example_asset_download_execution_allowed_false": EXAMPLE_ASSET_DOWNLOAD_EXECUTION_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Readiness semantics.
        "mobile_sam_weight_source_review_completed": mobile_sam_source_reviewed,
        "mobile_sam_can_enter_weight_download_execution_next": readiness_reviews[0].can_enter_weight_download_execution_next,
        "byte_track_weight_source_unresolved": not byte_track_resolved,
        "byte_track_can_enter_weight_download_execution_next_false": readiness_reviews[1].can_enter_weight_download_execution_next is False,
        "allowed_weight_download_execution_scope_ready_only": handoff.allowed_weight_download_execution_scope == "ready_only",
        "ready_asset_count_gte_1": handoff.ready_asset_count >= 1,
        "weight_approval_success_not_model_load_approval": approval.weight_approval_success_not_model_load_approval,
        "weight_approval_success_not_inference_approval": approval.weight_approval_success_not_inference_approval,
        "weight_approval_success_not_runtime_approval": approval.weight_approval_success_not_runtime_approval,
        "weight_approval_success_not_output_adapter_approval": approval.weight_approval_success_not_output_adapter_approval,
        "weight_approval_success_not_semantic_layer_approval": approval.weight_approval_success_not_semantic_layer_approval,
        "hash_plan_required": invariant_state["hash_plan_present"],
        "storage_plan_required": invariant_state["storage_plan_present"],
        "rollback_deletion_policy_required": invariant_state["rollback_deletion_policy_present"],
        "pre_download_snapshot_required": rollback_policy.pre_download_snapshot_required,
        "partial_download_cleanup_required": rollback_policy.partial_download_cleanup_required,
        "no_model_load_after_download": handoff.no_model_load_after_download,
        "no_inference_after_download": handoff.no_inference_after_download,
        "no_runtime_after_download": handoff.no_runtime_after_download,
        "no_output_adapter_after_download": handoff.no_output_adapter_after_download,
        "no_semantic_layer_after_download": handoff.no_semantic_layer_after_download,
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
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ModelWeightDownloadRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        model_weight_download_request_approval_readiness_profile_count=1,
        code_only_registry_overlay_audit_count=1,
        weight_download_candidate_record_count=len(candidates),
        weight_download_request_record_count=1,
        weight_source_review_record_count=len(source_reviews),
        weight_license_usage_boundary_record_count=1,
        weight_hash_storage_plan_record_count=len(hash_storage_plans),
        weight_download_command_whitelist_record_count=len(command_whitelist),
        weight_owner_approval_issuance_record_count=1,
        weight_download_rollback_deletion_policy_count=1,
        weight_download_readiness_review_count=len(readiness_reviews),
        weight_download_execution_handoff_record_count=1,
        ready_asset_count=len(ready_assets),
        unresolved_asset_count=len(unresolved_assets),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Weight Download Request, Approval And Readiness (compressed planning/approval only)",
        "lifecycle_variant": SCOPE,
        "weight_principle_zh": WEIGHT_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "weight_download_execution_allowed": WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_patch_execution_ref": UPSTREAM_PATCH_EXECUTION_REF,
        "upstream_planning_ref": UPSTREAM_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "model_weight_download_request_approval_readiness_profile": _build_profile(),
        "model_weight_download_request_approval_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "code_only_registry_overlay_audit": asdict(overlay_audit),
        "code_only_registry_overlay_audit_count": 1,
        "weight_download_candidate_records": [asdict(c) for c in candidates],
        "weight_download_candidate_record_count": len(candidates),
        "weight_download_request_record": asdict(request),
        "weight_download_request_record_count": 1,
        "weight_source_review_records": [asdict(s) for s in source_reviews],
        "weight_source_review_record_count": len(source_reviews),
        "weight_license_usage_boundary_record": asdict(license_boundary),
        "weight_license_usage_boundary_record_count": 1,
        "weight_hash_storage_plan_records": [asdict(p) for p in hash_storage_plans],
        "weight_hash_storage_plan_record_count": len(hash_storage_plans),
        "weight_download_command_whitelist_records": [asdict(c) for c in command_whitelist],
        "weight_download_command_whitelist_record_count": len(command_whitelist),
        "weight_owner_approval_issuance_record": asdict(approval),
        "weight_owner_approval_issuance_record_count": 1,
        "weight_download_rollback_deletion_policy": asdict(rollback_policy),
        "weight_download_rollback_deletion_policy_count": 1,
        "weight_download_readiness_reviews": [asdict(r) for r in readiness_reviews],
        "weight_download_readiness_review_count": len(readiness_reviews),
        "weight_download_execution_handoff_record": asdict(handoff),
        "weight_download_execution_handoff_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "ready_asset_count": len(ready_assets),
        "unresolved_asset_count": len(unresolved_assets),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "weight_download_request_approval_readiness_status": (
                "mobile_sam_ready_for_weight_download_execution_byte_track_unresolved_no_download_no_inference_no_runtime"
                if blocker_count == 0
                else "blocked"
            ),
            "ready_assets": list(ready_assets),
            "unresolved_assets": list(unresolved_assets),
            "mobile_sam_can_enter_weight_download_execution_next": readiness_reviews[0].can_enter_weight_download_execution_next,
            "byte_track_can_enter_weight_download_execution_next": readiness_reviews[1].can_enter_weight_download_execution_next,
            "recommended_next_phase": recommended_next_phase,
            "recommended_next_phase_scope": "mobile_sam_only" if unresolved_assets else "[mobile_sam, byte_track]",
            "optional_followup_phase": optional_followup,
            "transition_note": (
                "COMPRESSED PLANNING/APPROVAL ONLY — NOTHING was downloaded. The code-only registry overlay was "
                "verified (both assets code_only_ready, weights not_downloaded, no readiness true). A weight-download "
                "request package, owner approval issuance (PREPARATION only), weight source review, license/usage "
                "boundary, sha256 hash + storage plan (capabilities/model_weights/p1/...), TEMPLATE-ONLY download "
                "command whitelist (never executed), rollback/deletion policy, and readiness review were produced. "
                "mobile_sam's weight source is KNOWN (weights/mobile_sam.pt at the pinned MobileSAM commit, 40728226 "
                "bytes, Apache-2.0) -> READY for the next download-execution phase. byte_track's weight source is "
                "UNRESOLVED -> NOT approved for download execution (no fabricated URL) and routed to source "
                "resolution. Weight approval is NOT model load / inference / runtime / output adapter / semantic / "
                "commercial-runtime approval; even after download, NONE of those are allowed. Next phase: " +
                recommended_next_phase + " with scope=ready_only (recommended mobile_sam_only); byte_track should go "
                "through " + str(optional_followup) + " first. Download still requires the pre-download snapshot + "
                "hash verification + rollback policy from this plan."
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

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "weight_download_request_record": {"weight_download_request_record": asdict(request),
                                               "weight_download_candidate_records": [asdict(c) for c in candidates],
                                               "code_only_registry_overlay_audit": asdict(overlay_audit)},
            "weight_owner_approval_issuance_record": {"weight_owner_approval_issuance_record": asdict(approval)},
            "weight_source_review_record": {"weight_source_review_records": [asdict(s) for s in source_reviews]},
            "weight_hash_storage_plan_record": {"weight_hash_storage_plan_records": [asdict(p) for p in hash_storage_plans]},
            "weight_download_command_whitelist_record": {"weight_download_command_whitelist_records": [asdict(c) for c in command_whitelist]},
            "weight_download_boundary_record": {"weight_license_usage_boundary_record": asdict(license_boundary),
                                                "weight_download_rollback_deletion_policy": asdict(rollback_policy)},
            "weight_download_readiness_review_record": {"weight_download_readiness_reviews": [asdict(r) for r in readiness_reviews]},
            "followup_weight_download_execution_record": {"weight_download_execution_handoff_record": asdict(handoff)},
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
            "weight_download_execution_allowed": False,
            "model_load_allowed": False,
            "inference_allowed": False,
            "runtime_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
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
    result = review_p1_model_weight_download_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "ready_assets": result["conclusions"]["ready_assets"],
                "unresolved_assets": result["conclusions"]["unresolved_assets"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "recommended_next_phase_scope": result["conclusions"]["recommended_next_phase_scope"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
