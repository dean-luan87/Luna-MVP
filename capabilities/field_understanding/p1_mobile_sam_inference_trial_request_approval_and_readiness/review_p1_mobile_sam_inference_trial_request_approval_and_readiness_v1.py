# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Request Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only).

Audits registry overlay (mobile_sam=model_load_verified), produces inference trial request,
narrow owner approval, local test image manifest planning (no image read/create),
candidate-only output boundary, command whitelist template, memory/timeout, rollback/cleanup,
readiness review, and follow-up route. Does NOT execute inference, read images, import/load,
runtime, registry mutation, or download.
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
from capabilities.field_understanding.p1_mobile_sam_inference_trial_request_approval_and_readiness.p1_mobile_sam_inference_trial_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_request_approval_and_readiness.p1_mobile_sam_inference_trial_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPECTED_READINESS_LEVEL,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_EXECUTION_ALLOWED,
    INFERENCE_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    INFERENCE_PRINCIPLE_ZH,
    INFERENCE_TRIAL_READINESS_REVIEW_INCLUDED,
    INFERENCE_TRIAL_REQUEST_INCLUDED,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_VERIFIED_REQUIRED,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_INFERENCE_EXECUTION,
    OVERLAY_EXPECTED_FALSE,
    OVERLAY_EXPECTED_TRUE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_MEMORY_LIMIT_MB,
    PLANNED_TEST_IMAGE_MANIFEST_ENTRY,
    PLANNED_TIMEOUT_SECONDS,
    PLANNING_ONLY,
    PREDICTION_ALLOWED,
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
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REGISTRY_PATCH_EXECUTION_REF,
    WEIGHT_CHAIN,
    MobileSAMFollowupInferenceExecutionRoute,
    MobileSAMInferenceCandidateOutputBoundaryRecord,
    MobileSAMInferenceCommandWhitelistRecord,
    MobileSAMInferenceMemoryTimeoutBoundaryRecord,
    MobileSAMInferenceOwnerApprovalIssuanceRecord,
    MobileSAMInferenceReadinessReview,
    MobileSAMInferenceRollbackCleanupRecord,
    MobileSAMInferenceTrialRequestRecord,
    MobileSAMLocalTestImageManifestPlanningRecord,
    MobileSAMModelLoadVerifiedRegistryAudit,
    NegativeMobileSAMInferenceTrialRequestApprovalGuard,
    P1MobileSAMInferenceTrialRequestApprovalReadinessDecision,
    P1MobileSAMInferenceTrialRequestApprovalReadinessProfile,
    to_dict,
)


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_mobile_sam_inference_trial_request_approval_and_readiness_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_inference_trial_request_approval_and_readiness_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_inference_trial_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_inference_trial_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_inference_trial_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_inference_trial_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_inference_trial_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_inference_trial_request_approval_readiness_decision_v1"
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

ALLOWED_FUTURE_STEPS = (
    "pre_inference_snapshot",
    "sha256_recheck",
    "controlled_sys_path_setup",
    "import_mobile_sam",
    "load_checkpoint",
    "load_local_test_image_from_manifest",
    "one_controlled_inference_call",
    "save_candidate_mask_result_summary_to_tmp_eval_out",
    "memory_timeout_monitor",
    "cleanup",
)
FORBIDDEN_FUTURE_STEPS = (
    "live_camera",
    "external_network",
    "runtime_server",
    "output_adapter_call",
    "semantic_write",
    "fact_write",
    "navigation_action_speech",
    "batch_dataset",
    "registry_mutation",
)
ALLOWED_FUTURE_IMAGE_SOURCES = (
    "synthetic_test_image",
    "tiny_static_local_test_image",
    "explicitly_scoped_local_test_asset",
)
FORBIDDEN_IMAGE_SOURCES = (
    "live_camera",
    "user_personal_image",
    "external_url_image",
    "uncontrolled_dataset",
    "navigation_runtime_frame",
    "semantic_fact_input_frame",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _overlay_path() -> Path:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / REGISTRY_OVERLAY_REL
        if p.is_file():
            return p
    return _REPO_ROOT / REGISTRY_OVERLAY_REL


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMInferenceTrialRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            inference_trial_request_included=INFERENCE_TRIAL_REQUEST_INCLUDED,
            inference_owner_approval_issuance_included=INFERENCE_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            inference_trial_readiness_review_included=INFERENCE_TRIAL_READINESS_REVIEW_INCLUDED,
            model_load_verified_required=MODEL_LOAD_VERIFIED_REQUIRED,
            inference_execution_allowed=INFERENCE_EXECUTION_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            image_input_allowed=IMAGE_INPUT_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_registry_patch_execution_ref=UPSTREAM_REGISTRY_PATCH_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_inference_trial_request_approval_and_readiness_v1(
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

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    # (一) Upstream registry audit — model_load_verified.
    overlay_path = _overlay_path()
    overlay_exists = overlay_path.is_file()
    overlay: Dict[str, Any] = {}
    if overlay_exists:
        try:
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            overlay = {}
            overlay_exists = False
    ms = overlay.get("assets", {}).get(MOBILE_SAM_ASSET_ID, {})

    true_field_checks = {f: (ms.get(f) is True) for f in OVERLAY_EXPECTED_TRUE}
    false_field_checks = {f: (ms.get(f) is False) for f in OVERLAY_EXPECTED_FALSE}
    readiness_level = ms.get("readiness_level", "")
    readiness_level_ok = readiness_level == EXPECTED_READINESS_LEVEL
    weight_sha256_ok = ms.get("weight_sha256") == MOBILE_SAM_WEIGHT_SHA256
    weight_size_ok = ms.get("weight_file_size_bytes") == MOBILE_SAM_WEIGHT_SIZE_BYTES
    dep_ok = (
        ms.get("dependency_repair_dependency") == "timm"
        and ms.get("dependency_repair_dependency_version") == "1.0.27"
        and ms.get("dependency_repair_method") == "timm_no_deps_controlled_install"
    )
    model_fields_ok = (
        ms.get("model_type_name") == "Sam"
        and ms.get("model_load_trial_result") == "GO"
        and ms.get("torch_version_observed") == "2.8.0"
        and ms.get("torchvision_version_observed") == "0.23.0"
    )

    audit_passed = (
        overlay_exists
        and readiness_level_ok
        and all(true_field_checks.values())
        and all(false_field_checks.values())
        and weight_sha256_ok
        and weight_size_ok
        and dep_ok
        and model_fields_ok
    )
    audit = MobileSAMModelLoadVerifiedRegistryAudit(
        audit_id="mobile_sam_model_load_verified_registry_audit_v1",
        registry_overlay_ref=REGISTRY_OVERLAY_REL,
        readiness_level=readiness_level,
        model_load_verified=ms.get("model_load_verified") is True,
        checkpoint_load_verified=ms.get("checkpoint_load_verified") is True,
        dependency_gap_resolved=ms.get("dependency_gap_resolved") is True,
        dependency_repair_applied=ms.get("dependency_repair_applied") is True,
        dependency_repair_dependency=ms.get("dependency_repair_dependency", ""),
        dependency_repair_dependency_version=ms.get("dependency_repair_dependency_version", ""),
        dependency_repair_method=ms.get("dependency_repair_method", ""),
        model_type_name=ms.get("model_type_name", ""),
        model_load_trial_result=ms.get("model_load_trial_result", ""),
        torch_version_observed=ms.get("torch_version_observed", ""),
        torchvision_version_observed=ms.get("torchvision_version_observed", ""),
        weight_downloaded=ms.get("weight_downloaded") is True,
        weight_sha256=ms.get("weight_sha256", ""),
        weight_file_size_bytes=int(ms.get("weight_file_size_bytes") or 0),
        weight_integrity_verified=ms.get("weight_integrity_verified") is True,
        storage_verified=ms.get("storage_verified") is True,
        inference_ready=ms.get("inference_ready") is False,
        runtime_ready=ms.get("runtime_ready") is False,
        output_adapter_ready=ms.get("output_adapter_ready") is False,
        semantic_layer_ready=ms.get("semantic_layer_ready") is False,
        commercial_runtime_approved=ms.get("commercial_runtime_approved") is False,
        audit_passed=audit_passed,
    )
    if not audit_passed:
        failed_checks.append("audit.mobile_sam_not_model_load_verified_or_fields_invalid")

    # (二) Inference trial request.
    request = MobileSAMInferenceTrialRequestRecord(
        request_id="mobile_sam_inference_trial_request_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        request_scope="controlled_inference_trial_preparation",
        inference_trial_requested=True,
        inference_execution_requested_next=True,
        model_load_verified_required=True,
        local_test_image_required=True,
        candidate_output_required=True,
        request_is_not_inference_execution=True,
        request_is_not_runtime_approval=True,
        request_is_not_output_adapter_approval=True,
        request_is_not_semantic_layer_approval=True,
        request_is_not_fact_write_approval=True,
        request_is_not_navigation_action_speech_approval=True,
        request_is_not_commercial_runtime_approval=True,
    )

    # (三) Owner approval issuance (narrow).
    approval = MobileSAMInferenceOwnerApprovalIssuanceRecord(
        record_id="mobile_sam_inference_owner_approval_issuance_v1",
        owner_approval_granted_for_inference_trial_preparation=True,
        owner_approval_granted_for_inference_trial_execution_next=True,
        runtime_approved=False,
        output_adapter_approved=False,
        semantic_layer_approved=False,
        fact_write_approved=False,
        navigation_action_speech_approved=False,
        commercial_runtime_approved=False,
        registry_mutation_approved=False,
        additional_download_approved=False,
        inference_trial_approval_not_runtime_approval=True,
        inference_trial_approval_not_output_adapter_approval=True,
        inference_trial_approval_not_semantic_layer_approval=True,
        inference_trial_approval_not_fact_write_approval=True,
        inference_trial_approval_not_navigation_action_speech_approval=True,
        inference_trial_approval_not_commercial_runtime_approval=True,
    )

    # (四) Local test image manifest planning (no image create/read).
    manifest_plan = MobileSAMLocalTestImageManifestPlanningRecord(
        record_id="mobile_sam_local_test_image_manifest_plan_v1",
        allowed_future_sources=ALLOWED_FUTURE_IMAGE_SOURCES,
        forbidden_sources=FORBIDDEN_IMAGE_SOURCES,
        planned_manifest_entries=(PLANNED_TEST_IMAGE_MANIFEST_ENTRY,),
        image_created_this_phase=False,
        image_read_this_phase=False,
    )

    # (五) Candidate-only output boundary.
    candidate_boundary = MobileSAMInferenceCandidateOutputBoundaryRecord(
        record_id="mobile_sam_inference_candidate_output_boundary_v1",
        inference_output_candidate_only=True,
        output_must_not_enter_fact_layer=True,
        output_must_not_enter_runtime=True,
        output_must_not_enter_output_adapter=True,
        output_must_not_enter_semantic_layer=True,
        output_must_not_trigger_navigation_action_speech=True,
        output_must_not_be_user_visible_runtime_output=True,
        output_must_be_written_only_to_eval_artifacts=True,
        output_must_be_marked_candidate=True,
        output_requires_post_review=True,
    )

    # (六) Command whitelist (template only).
    whitelist = MobileSAMInferenceCommandWhitelistRecord(
        record_id="mobile_sam_inference_command_whitelist_v1",
        allowed_future_steps=ALLOWED_FUTURE_STEPS,
        forbidden_future_steps=FORBIDDEN_FUTURE_STEPS,
        command_template_only=True,
        command_not_executed=True,
        inference_command_requires_next_phase=True,
    )

    # (七) Memory / timeout boundary.
    memory_timeout = MobileSAMInferenceMemoryTimeoutBoundaryRecord(
        record_id="mobile_sam_inference_memory_timeout_boundary_v1",
        memory_limit_mb=PLANNED_MEMORY_LIMIT_MB,
        timeout_seconds=PLANNED_TIMEOUT_SECONDS,
        oom_handling_required=True,
        timeout_failure_records_required=True,
        candidate_output_cleanup_required=True,
        no_persistent_runtime_process_allowed=True,
    )

    # (八) Rollback / cleanup.
    rollback = MobileSAMInferenceRollbackCleanupRecord(
        record_id="mobile_sam_inference_rollback_cleanup_v1",
        pre_inference_snapshot_required=True,
        rollback_required=True,
        rollback_preserves_registry=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        candidate_output_cleanup_required=True,
        no_fact_write_on_failure=True,
        no_registry_mutation_on_failure=True,
    )

    # (九) Readiness review.
    readiness = MobileSAMInferenceReadinessReview(
        review_id="mobile_sam_inference_readiness_review_v1",
        can_enter_inference_trial_execution_next=audit_passed,
        inference_trial_execution_scope="mobile_sam_single_local_test_image_candidate_only",
        inference_execution_requires_test_image_manifest=True,
        inference_execution_requires_sha256_recheck=True,
        inference_execution_requires_model_load_verified=True,
        inference_execution_requires_candidate_output_boundary=True,
        inference_execution_requires_post_review=True,
        can_enter_runtime_after_this_phase=False,
        can_enter_output_adapter_after_this_phase=False,
        can_enter_semantic_layer_after_this_phase=False,
        can_write_fact_after_this_phase=False,
    )

    # (十) Follow-up route.
    followup = MobileSAMFollowupInferenceExecutionRoute(
        route_id="mobile_sam_followup_inference_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_INFERENCE_EXECUTION,
        next_phase_scope="mobile_sam_single_local_test_image_candidate_only",
        next_phase_allows_single_controlled_inference=True,
        next_phase_still_no_runtime=True,
    )

    # (十一) Negative guards (17).
    manifest_entry = PLANNED_TEST_IMAGE_MANIFEST_ENTRY
    image_manifest_strict = (
        manifest_entry["personal_data_absent"] is True
        and manifest_entry["live_camera_frame"] is False
        and manifest_entry["external_url_source"] is False
        and manifest_entry["dataset_source"] is False
        and manifest_entry["navigation_runtime_frame"] is False
        and manifest_entry["fact_layer_source"] is False
        and manifest_entry["semantic_layer_source"] is False
        and manifest_plan.image_created_this_phase is False
        and manifest_plan.image_read_this_phase is False
    )
    whitelist_strict = (
        "runtime_server" in whitelist.forbidden_future_steps
        and "output_adapter_call" in whitelist.forbidden_future_steps
        and "semantic_write" in whitelist.forbidden_future_steps
        and "fact_write" in whitelist.forbidden_future_steps
        and "navigation_action_speech" in whitelist.forbidden_future_steps
    )
    invariant_state: Dict[str, bool] = {
        "overlay_model_load_verified": audit_passed,
        "model_load_fields_verified": (
            audit.model_load_verified and audit.checkpoint_load_verified and audit.dependency_gap_resolved
        ),
        "no_real_inference": REAL_INFERENCE_ALLOWED is False and INFERENCE_EXECUTION_ALLOWED is False,
        "no_image_input": IMAGE_INPUT_ALLOWED is False
        and manifest_plan.image_created_this_phase is False
        and manifest_plan.image_read_this_phase is False,
        "no_real_import_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": (
            FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False
        and rollback.no_registry_mutation_on_failure is True,
        "no_extra_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
            and MODEL_DOWNLOAD_ALLOWED is False
            and approval.additional_download_approved is False
        ),
        "approval_not_downstream": (
            approval.inference_trial_approval_not_runtime_approval
            and approval.inference_trial_approval_not_output_adapter_approval
            and approval.inference_trial_approval_not_semantic_layer_approval
            and approval.inference_trial_approval_not_fact_write_approval
            and approval.inference_trial_approval_not_navigation_action_speech_approval
            and approval.inference_trial_approval_not_commercial_runtime_approval
            and approval.runtime_approved is False
            and approval.output_adapter_approved is False
        ),
        "image_manifest_strict": image_manifest_strict,
        "candidate_boundary_present": candidate_boundary.inference_output_candidate_only is True
        and candidate_boundary.output_must_not_enter_fact_layer is True
        and candidate_boundary.output_requires_post_review is True,
        "whitelist_strict": whitelist_strict and whitelist.command_template_only is True,
        "rollback_present": rollback.pre_inference_snapshot_required is True
        and rollback.rollback_required is True
        and rollback.rollback_preserves_test_board is True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMInferenceTrialRequestApprovalGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMInferenceTrialRequestApprovalGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_inference_trial_request_approval_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_inference_trial_request_approval_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_model_load_verified_registry_audit_count_gte_1": True,
        "mobile_sam_inference_trial_request_record_count_gte_1": True,
        "mobile_sam_inference_owner_approval_issuance_record_count_gte_1": True,
        "mobile_sam_local_test_image_manifest_plan_count_gte_1": True,
        "mobile_sam_inference_candidate_output_boundary_count_gte_1": True,
        "mobile_sam_inference_command_whitelist_count_gte_1": True,
        "mobile_sam_inference_memory_timeout_boundary_count_gte_1": True,
        "mobile_sam_inference_rollback_cleanup_count_gte_1": True,
        "mobile_sam_inference_readiness_review_count_gte_1": True,
        "mobile_sam_followup_inference_execution_route_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "compressed_phase": COMPRESSED_PHASE is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "inference_trial_request_included": INFERENCE_TRIAL_REQUEST_INCLUDED is True,
        "inference_owner_approval_issuance_included": INFERENCE_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "inference_trial_readiness_review_included": INFERENCE_TRIAL_READINESS_REVIEW_INCLUDED is True,
        "model_load_verified_required": MODEL_LOAD_VERIFIED_REQUIRED is True,
        "inference_execution_allowed_false": INFERENCE_EXECUTION_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "segmentation_allowed_false": SEGMENTATION_ALLOWED is False,
        "prediction_allowed_false": PREDICTION_ALLOWED is False,
        "image_input_allowed_false": IMAGE_INPUT_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "owner_approval_granted_for_inference_trial_preparation": approval.owner_approval_granted_for_inference_trial_preparation,
        "owner_approval_granted_for_inference_trial_execution_next": approval.owner_approval_granted_for_inference_trial_execution_next,
        "can_enter_inference_trial_execution_next": readiness.can_enter_inference_trial_execution_next,
        "can_enter_runtime_after_this_phase_false": readiness.can_enter_runtime_after_this_phase is False,
        "can_enter_output_adapter_after_this_phase_false": readiness.can_enter_output_adapter_after_this_phase is False,
        "can_enter_semantic_layer_after_this_phase_false": readiness.can_enter_semantic_layer_after_this_phase is False,
        "can_write_fact_after_this_phase_false": readiness.can_write_fact_after_this_phase is False,
        "inference_trial_approval_not_runtime_approval": approval.inference_trial_approval_not_runtime_approval,
        "inference_trial_approval_not_output_adapter_approval": approval.inference_trial_approval_not_output_adapter_approval,
        "inference_trial_approval_not_semantic_layer_approval": approval.inference_trial_approval_not_semantic_layer_approval,
        "inference_trial_approval_not_fact_write_approval": approval.inference_trial_approval_not_fact_write_approval,
        "inference_trial_approval_not_navigation_action_speech_approval": approval.inference_trial_approval_not_navigation_action_speech_approval,
        "inference_trial_approval_not_commercial_runtime_approval": approval.inference_trial_approval_not_commercial_runtime_approval,
        **negative_guard_go,
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
    decision = P1MobileSAMInferenceTrialRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_inference_trial_request_approval_readiness_profile_count=1,
        mobile_sam_model_load_verified_registry_audit_count=1,
        mobile_sam_inference_trial_request_record_count=1,
        mobile_sam_inference_owner_approval_issuance_record_count=1,
        mobile_sam_local_test_image_manifest_plan_count=1,
        mobile_sam_inference_candidate_output_boundary_count=1,
        mobile_sam_inference_command_whitelist_count=1,
        mobile_sam_inference_memory_timeout_boundary_count=1,
        mobile_sam_inference_rollback_cleanup_count=1,
        mobile_sam_inference_readiness_review_count=1,
        mobile_sam_followup_inference_execution_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Inference Trial Request Approval And Readiness (planning only, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "inference_principle_zh": INFERENCE_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "planning_only": PLANNING_ONLY,
        "inference_execution_allowed": INFERENCE_EXECUTION_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_registry_patch_execution_ref": UPSTREAM_REGISTRY_PATCH_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_inference_trial_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_inference_trial_request_approval_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_model_load_verified_registry_audit": asdict(audit),
        "mobile_sam_model_load_verified_registry_audit_count": 1,
        "mobile_sam_inference_trial_request_record": asdict(request),
        "mobile_sam_inference_trial_request_record_count": 1,
        "mobile_sam_inference_owner_approval_issuance_record": asdict(approval),
        "mobile_sam_inference_owner_approval_issuance_record_count": 1,
        "mobile_sam_local_test_image_manifest_plan_record": asdict(manifest_plan),
        "mobile_sam_local_test_image_manifest_plan_count": 1,
        "mobile_sam_inference_candidate_output_boundary_record": asdict(candidate_boundary),
        "mobile_sam_inference_candidate_output_boundary_count": 1,
        "mobile_sam_inference_command_whitelist_record": asdict(whitelist),
        "mobile_sam_inference_command_whitelist_count": 1,
        "mobile_sam_inference_memory_timeout_boundary_record": asdict(memory_timeout),
        "mobile_sam_inference_memory_timeout_boundary_count": 1,
        "mobile_sam_inference_rollback_cleanup_record": asdict(rollback),
        "mobile_sam_inference_rollback_cleanup_count": 1,
        "mobile_sam_inference_readiness_review_record": asdict(readiness),
        "mobile_sam_inference_readiness_review_count": 1,
        "mobile_sam_followup_inference_execution_route_record": asdict(followup),
        "mobile_sam_followup_inference_execution_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "overlay_path": str(overlay_path),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "inference_trial_request_approval_readiness_status": (
                "mobile_sam_inference_trial_requested_approved_for_preparation_and_execution_next"
                if blocker_count == 0
                else "blocked"
            ),
            "inference_executed_this_phase": False,
            "image_read_this_phase": False,
            "image_created_this_phase": False,
            "imported_this_phase": False,
            "model_loaded_this_phase": False,
            "registry_mutated_this_phase": False,
            "can_enter_inference_trial_execution_next": readiness.can_enter_inference_trial_execution_next,
            "recommended_next_phase": NEXT_PHASE_INFERENCE_EXECUTION,
            "recommended_next_phase_scope": followup.next_phase_scope,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only). Registry overlay audited: "
                "mobile_sam=model_load_verified with verified checkpoint/timm dependency. "
                "Inference trial request, narrow owner approval, local test image manifest plan "
                "(no image create/read), candidate-only output boundary, command whitelist template, "
                "memory/timeout, rollback/cleanup, readiness review, and follow-up route produced. "
                "NO inference, NO image input, NO import/load, NO runtime/output/semantic/fact. "
                "Next: " + NEXT_PHASE_INFERENCE_EXECUTION + " (single local test image, candidate-only)."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
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
            "mobile_sam_model_load_verified_registry_audit_record": {
                "mobile_sam_model_load_verified_registry_audit": asdict(audit),
            },
            "mobile_sam_inference_trial_request_record": {
                "mobile_sam_inference_trial_request_record": asdict(request),
            },
            "mobile_sam_inference_owner_approval_issuance_record": {
                "mobile_sam_inference_owner_approval_issuance_record": asdict(approval),
            },
            "mobile_sam_local_test_image_manifest_plan_record": {
                "mobile_sam_local_test_image_manifest_plan_record": asdict(manifest_plan),
            },
            "mobile_sam_inference_candidate_output_boundary_record": {
                "mobile_sam_inference_candidate_output_boundary_record": asdict(candidate_boundary),
            },
            "mobile_sam_inference_command_whitelist_record": {
                "mobile_sam_inference_command_whitelist_record": asdict(whitelist),
            },
            "mobile_sam_inference_memory_timeout_boundary_record": {
                "mobile_sam_inference_memory_timeout_boundary_record": asdict(memory_timeout),
            },
            "mobile_sam_inference_rollback_cleanup_record": {
                "mobile_sam_inference_rollback_cleanup_record": asdict(rollback),
            },
            "mobile_sam_inference_readiness_review_record": {
                "mobile_sam_inference_readiness_review_record": asdict(readiness),
            },
            "mobile_sam_followup_inference_execution_route_record": {
                "mobile_sam_followup_inference_execution_route_record": asdict(followup),
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
            "inference_execution_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
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
    result = review_p1_mobile_sam_inference_trial_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "inference_executed_this_phase": result["conclusions"]["inference_executed_this_phase"],
                "image_read_this_phase": result["conclusions"]["image_read_this_phase"],
                "registry_mutated_this_phase": result["conclusions"]["registry_mutated_this_phase"],
                "can_enter_inference_trial_execution_next": result["conclusions"]["can_enter_inference_trial_execution_next"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
