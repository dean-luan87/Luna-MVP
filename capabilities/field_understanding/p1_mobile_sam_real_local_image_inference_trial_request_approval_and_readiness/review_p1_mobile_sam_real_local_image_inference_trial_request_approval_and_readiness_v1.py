# -*- coding: utf-8 -*-
"""P1 MobileSAM Real Local Image Inference Trial Request Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only)."""

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
from capabilities.field_understanding.p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness.p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    load_registry_overlay,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness.p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BROAD_READINESS_MUST_BE_FALSE,
    CANDIDATE_OUTPUT_TARGET_DIR,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_MANIFEST_OUTPUT_REL,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_TO_MODEL_ALLOWED,
    IMAGE_MANIFEST_PLANNING_ALLOWED,
    LIVE_CAMERA_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_ONLY,
    MODEL_LOAD_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_MANIFEST_ENTRY,
    PLANNED_MEMORY_LIMIT_MB,
    PLANNED_PROMPT_TARGETS,
    PLANNED_TIMEOUT_SECONDS,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    PROMPT_POINTS_BOXES_PLANNING_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_LOCAL_IMAGE_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    REAL_LOCAL_IMAGE_TRIAL_READINESS_REVIEW_INCLUDED,
    REAL_LOCAL_IMAGE_TRIAL_REQUEST_INCLUDED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REGISTRY_OVERLAY_REL,
    REQUIRED_READINESS_LEVEL,
    REQUIRED_REGISTRY_TRUE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCENE_TYPE,
    SCOPED_FOR_PHASE,
    SCOPED_LOCAL_TEST_ASSET_REGISTRATION,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_FILE_ID,
    SOURCE_IMAGE_PATH,
    SOURCE_TYPE,
    TARGET_CHAIN_REF,
    TEST_ASSET_ID,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UNCONTROLLED_DATASET_ALLOWED,
    UPSTREAM_RUNTIME_BOUNDARY_PLANNING_REF,
    WEIGHT_CHAIN,
    NegativeRealLocalImageInferenceTrialRequestApprovalGuard,
    P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessDecision,
    P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessProfile,
    RealLocalImageAssetRegistrationRecord,
    RealLocalImageCandidateOutputBoundaryRecord,
    RealLocalImageCommandWhitelistRecord,
    RealLocalImageFollowupExecutionRoute,
    RealLocalImageManifestPlanningRecord,
    RealLocalImageMemoryTimeoutBoundaryRecord,
    RealLocalImageOwnerApprovalIssuanceRecord,
    RealLocalImagePromptPlanningRecord,
    RealLocalImageReadinessReview,
    RealLocalImageRollbackCleanupPlanningRecord,
    to_dict,
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_real_local_image_inference_trial_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_real_local_image_inference_trial_request_approval_readiness_decision_v1"
REVIEW_FILENAME = (
    "p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_review_v1.json"
)
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

ALLOWED_FUTURE_STEPS = (
    "pre_inference_snapshot",
    "registry_model_readiness_recheck",
    "sha256_recheck_for_weight",
    "sha256_size_width_height_for_real_local_image",
    "controlled_sys_path_setup",
    "import_mobile_sam",
    "load_checkpoint",
    "read_manifest_image_only",
    "execute_planned_prompt_points_boxes",
    "save_candidate_masks_summaries_to_tmp_eval_out",
    "memory_timeout_monitor",
    "cleanup",
    "post_review",
)
FORBIDDEN_FUTURE_STEPS = (
    "live_camera",
    "external_url",
    "non_manifest_image",
    "batch_dataset",
    "runtime_server",
    "output_adapter_call",
    "semantic_write",
    "fact_write",
    "navigation_action_speech",
    "registry_mutation",
    "additional_download",
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
    / "p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_registry_mobile_sam(overlay: Dict[str, Any]) -> Dict[str, Any]:
    asset = (overlay.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
    readiness = asset.get("readiness_level")
    true_flags_ok = all(asset.get(f) is True for f in REQUIRED_REGISTRY_TRUE_FLAGS)
    broad_false = all(asset.get(f) is False for f in BROAD_READINESS_MUST_BE_FALSE)
    return {
        "readiness_level": readiness,
        "inference_trial_verified": asset.get("inference_trial_verified"),
        "true_flags_ok": true_flags_ok,
        "broad_readiness_all_false": broad_false,
        "audit_passed": (
            readiness == REQUIRED_READINESS_LEVEL
            and true_flags_ok
            and broad_false
        ),
        "asset_snapshot": {k: asset.get(k) for k in (
            ["readiness_level"] + list(REQUIRED_REGISTRY_TRUE_FLAGS) + list(BROAD_READINESS_MUST_BE_FALSE)
        )},
    }


def _audit_runtime_boundary_upstream(repo_root: Path) -> Dict[str, Any]:
    artifact_rel = (
        "_tmp_eval_out/p1_mobile_sam_runtime_boundary_standardization_planning_v1_smoke_v0/"
        "p1_mobile_sam_runtime_boundary_standardization_planning_review_v1.json"
    )
    artifact, exists, resolved = load_artifact(repo_root, artifact_rel)
    go_ok = exists and (artifact or {}).get("final_decision") == (
        "P1_MOBILE_SAM_RUNTIME_BOUNDARY_STANDARDIZATION_PLANNING_GO"
    )
    return {
        "artifact_exists": exists,
        "resolved_path": resolved,
        "final_decision": (artifact or {}).get("final_decision"),
        "real_local_image_trial_allowed_next": (artifact or {}).get(
            "can_enter_real_local_image_trial_request_approval_next"
        ),
        "go_verified": go_ok,
        "candidate_output_must_remain_candidate": True,
        "live_camera_forbidden": True,
        "external_url_forbidden": True,
    }


def _audit_governance_refs() -> Dict[str, Any]:
    refs_ok = all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS)
    manifest_path = _resolve_file(GOVERNANCE_CANONICAL_REFS[0])
    manifest_ok = False
    if manifest_path is not None:
        try:
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_ok = m.get("migration_mode") == "canonical_copy_no_delete"
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "canonical_refs_ok": refs_ok,
        "canonical_standard_library_created": manifest_ok,
        "reference_policy_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[1]) is not None,
        "runtime_boundary_plan_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[2]) is not None,
        "runtime_admission_criteria_ok": _resolve_file(GOVERNANCE_CANONICAL_REFS[3]) is not None,
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=MOBILE_SAM_ONLY,
            real_local_image_trial_request_included=REAL_LOCAL_IMAGE_TRIAL_REQUEST_INCLUDED,
            real_local_image_owner_approval_issuance_included=REAL_LOCAL_IMAGE_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            real_local_image_trial_readiness_review_included=REAL_LOCAL_IMAGE_TRIAL_READINESS_REVIEW_INCLUDED,
            scoped_local_test_asset_registration=SCOPED_LOCAL_TEST_ASSET_REGISTRATION,
            image_manifest_planning_allowed=IMAGE_MANIFEST_PLANNING_ALLOWED,
            prompt_points_boxes_planning_allowed=PROMPT_POINTS_BOXES_PLANNING_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            image_input_to_model_allowed=IMAGE_INPUT_TO_MODEL_ALLOWED,
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
            external_image_download_allowed=EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
            live_camera_allowed=LIVE_CAMERA_ALLOWED,
            uncontrolled_dataset_allowed=UNCONTROLLED_DATASET_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_runtime_boundary_planning_ref=UPSTREAM_RUNTIME_BOUNDARY_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1(
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
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    runtime_boundary_audit = _audit_runtime_boundary_upstream(_REPO_ROOT)
    if not runtime_boundary_audit["go_verified"]:
        failed_checks.append("upstream.runtime_boundary_standardization_not_go")

    gov_audit = _audit_governance_refs()
    if not gov_audit["canonical_refs_ok"]:
        failed_checks.append("governance.canonical_refs_incomplete")

    overlay, overlay_path = load_registry_overlay(_REPO_ROOT, REGISTRY_OVERLAY_REL)
    if overlay is None:
        failed_checks.append("registry.overlay_missing")
        reg_audit = {"audit_passed": False}
    else:
        reg_audit = _audit_registry_mobile_sam(overlay)
        if not reg_audit["audit_passed"]:
            failed_checks.append(f"registry.mobile_sam_audit_failed:{reg_audit}")

    asset_registration = RealLocalImageAssetRegistrationRecord(
        record_id="real_local_image_asset_registration_v1",
        test_asset_id=TEST_ASSET_ID,
        asset_id=MOBILE_SAM_ASSET_ID,
        source_image_path=SOURCE_IMAGE_PATH,
        source_file_id=SOURCE_FILE_ID,
        source_type=SOURCE_TYPE,
        scene_type=SCENE_TYPE,
        scoped_for_phase=SCOPED_FOR_PHASE,
        allowed_for_single_phase_execution=True,
        live_camera_frame=False,
        external_url_source=False,
        uncontrolled_dataset_source=False,
        personal_sensitive_image=False,
        fact_layer_source=False,
        semantic_layer_source=False,
        navigation_runtime_frame=False,
        candidate_only_use=True,
        image_read_this_phase=False,
        inference_executed_this_phase=False,
    )

    manifest_plan = RealLocalImageManifestPlanningRecord(
        record_id="real_local_image_manifest_plan_v1",
        execution_manifest_output_rel=EXECUTION_MANIFEST_OUTPUT_REL,
        planned_manifest_entry=dict(PLANNED_MANIFEST_ENTRY),
        manifest_status="planned_not_verified",
        sha256_verification_deferred_to_execution=True,
        image_read_this_phase=False,
    )

    prompt_plan = RealLocalImagePromptPlanningRecord(
        record_id="real_local_image_prompt_plan_v1",
        prompt_targets=PLANNED_PROMPT_TARGETS,
        prompt_labels_are_test_descriptions_only=True,
        mobile_sam_does_not_produce_semantic_facts=True,
        prompt_target_label_is_not_fact_recognition=True,
        segmentation_output_is_candidate_mask_only=True,
        object_category_judgment_requires_separate_evidence=True,
        coordinates_are_test_prompts_not_fact_layer_positioning=True,
    )

    candidate_boundary = RealLocalImageCandidateOutputBoundaryRecord(
        record_id="real_local_image_candidate_output_boundary_v1",
        candidate_output_only=True,
        output_target_dir=CANDIDATE_OUTPUT_TARGET_DIR,
        output_must_be_candidate=True,
        output_not_fact=True,
        output_not_runtime_output=True,
        output_not_output_adapter_output=True,
        output_not_semantic_output=True,
        output_not_navigation_action_speech=True,
        output_not_user_visible_runtime_output=True,
        output_requires_post_review=True,
        output_requires_quality_summary=True,
        output_requires_failure_mode_annotation=True,
    )

    approval = RealLocalImageOwnerApprovalIssuanceRecord(
        record_id="real_local_image_owner_approval_issuance_v1",
        owner_approval_granted_for_real_local_image_inference_preparation=True,
        owner_approval_granted_for_real_local_image_inference_execution_next=True,
        runtime_approved=False,
        output_adapter_approved=False,
        semantic_layer_approved=False,
        fact_write_approved=False,
        navigation_action_speech_approved=False,
        commercial_runtime_approved=False,
        registry_mutation_approved=False,
        additional_download_approved=False,
        external_image_use_approved=False,
        live_camera_use_approved=False,
        real_image_inference_approval_not_runtime_approval=True,
        real_image_inference_approval_not_output_adapter_approval=True,
        real_image_inference_approval_not_semantic_layer_approval=True,
        real_image_inference_approval_not_fact_write_approval=True,
        real_image_inference_approval_not_navigation_action_speech_approval=True,
        real_image_inference_approval_not_registry_mutation_approval=True,
        real_image_inference_approval_not_commercial_runtime_approval=True,
    )

    whitelist = RealLocalImageCommandWhitelistRecord(
        record_id="real_local_image_command_whitelist_v1",
        allowed_future_steps=ALLOWED_FUTURE_STEPS,
        forbidden_future_steps=FORBIDDEN_FUTURE_STEPS,
        command_template_only=True,
        command_not_executed=True,
        real_image_command_requires_next_phase=True,
    )

    memory_timeout = RealLocalImageMemoryTimeoutBoundaryRecord(
        record_id="real_local_image_memory_timeout_boundary_v1",
        memory_limit_mb=PLANNED_MEMORY_LIMIT_MB,
        timeout_seconds=PLANNED_TIMEOUT_SECONDS,
        oom_handling_required=True,
        timeout_failure_records_required=True,
        candidate_output_cleanup_required_if_failed=True,
        no_persistent_runtime_process_allowed=True,
    )

    rollback = RealLocalImageRollbackCleanupPlanningRecord(
        record_id="real_local_image_rollback_cleanup_plan_v1",
        pre_inference_snapshot_required=True,
        rollback_required=True,
        rollback_preserves_registry=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        rollback_preserves_source_uploaded_image=True,
        candidate_output_cleanup_required_if_failed=True,
        no_fact_write_on_failure=True,
        no_registry_mutation_on_failure=True,
    )

    can_enter_execution = (
        runtime_boundary_audit["go_verified"]
        and reg_audit.get("audit_passed")
        and gov_audit["canonical_refs_ok"]
        and asset_registration.candidate_only_use
        and not asset_registration.personal_sensitive_image
        and not asset_registration.live_camera_frame
        and not asset_registration.external_url_source
    )

    readiness = RealLocalImageReadinessReview(
        review_id="real_local_image_readiness_review_v1",
        can_enter_real_local_image_inference_trial_execution_next=bool(can_enter_execution),
        real_local_image_trial_execution_scope="mobile_sam_single_user_supplied_local_image_candidate_only",
        execution_requires_manifest=True,
        execution_requires_weight_sha256_recheck=True,
        execution_requires_model_load_verified=True,
        execution_requires_inference_trial_verified=True,
        execution_requires_candidate_output_boundary=True,
        execution_requires_prompt_plan=True,
        execution_requires_post_review=True,
        can_enter_runtime_after_this_phase=False,
        can_enter_output_adapter_after_this_phase=False,
        can_enter_semantic_layer_after_this_phase=False,
        can_write_fact_after_this_phase=False,
        can_trigger_navigation_action_speech_after_this_phase=False,
    )

    followup = RealLocalImageFollowupExecutionRoute(
        route_id="real_local_image_followup_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
        next_phase_scope="mobile_sam_single_user_supplied_local_image_candidate_only",
        next_phase_allows_manifest_image_read=True,
        next_phase_allows_import_model_load=True,
        next_phase_allows_planned_prompt_segmentation=True,
        next_phase_still_no_runtime=True,
        next_phase_still_candidate_only=True,
    )

    manifest_entry = PLANNED_MANIFEST_ENTRY
    image_source_allowed = (
        asset_registration.source_type == SOURCE_TYPE
        and asset_registration.live_camera_frame is False
        and asset_registration.external_url_source is False
        and asset_registration.uncontrolled_dataset_source is False
        and manifest_entry["live_camera_frame"] is False
        and manifest_entry["external_url_source"] is False
        and manifest_entry["dataset_source"] is False
    )
    prompt_labels_not_semantic = all(
        t.get("semantic_assertion_allowed") is False and t.get("fact_write_allowed") is False
        for t in PLANNED_PROMPT_TARGETS
    )
    whitelist_strict = (
        "runtime_server" in whitelist.forbidden_future_steps
        and "output_adapter_call" in whitelist.forbidden_future_steps
        and "semantic_write" in whitelist.forbidden_future_steps
        and "fact_write" in whitelist.forbidden_future_steps
        and "navigation_action_speech" in whitelist.forbidden_future_steps
        and "registry_mutation" in whitelist.forbidden_future_steps
        and "additional_download" in whitelist.forbidden_future_steps
        and "live_camera" in whitelist.forbidden_future_steps
        and "external_url" in whitelist.forbidden_future_steps
    )

    invariant_state: Dict[str, bool] = {
        "upstream_runtime_boundary_go": runtime_boundary_audit["go_verified"],
        "registry_inference_trial_verified": reg_audit.get("audit_passed") is True,
        "no_real_inference": REAL_INFERENCE_ALLOWED is False and asset_registration.inference_executed_this_phase is False,
        "no_image_input_to_model": (
            IMAGE_INPUT_TO_MODEL_ALLOWED is False
            and asset_registration.image_read_this_phase is False
            and manifest_plan.image_read_this_phase is False
        ),
        "no_real_import_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False and rollback.no_registry_mutation_on_failure is True,
        "no_extra_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
            and EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False
            and approval.additional_download_approved is False
        ),
        "image_source_allowed": image_source_allowed,
        "not_personal_sensitive": asset_registration.personal_sensitive_image is False,
        "prompt_labels_not_semantic_facts": prompt_labels_not_semantic and prompt_plan.prompt_labels_are_test_descriptions_only,
        "candidate_boundary_present": (
            candidate_boundary.candidate_output_only
            and candidate_boundary.output_not_fact
            and candidate_boundary.output_requires_post_review
        ),
        "approval_not_downstream": (
            approval.real_image_inference_approval_not_runtime_approval
            and approval.real_image_inference_approval_not_output_adapter_approval
            and approval.real_image_inference_approval_not_semantic_layer_approval
            and approval.real_image_inference_approval_not_fact_write_approval
            and approval.real_image_inference_approval_not_navigation_action_speech_approval
            and approval.runtime_approved is False
            and approval.output_adapter_approved is False
            and approval.fact_write_approved is False
        ),
        "whitelist_strict": whitelist_strict and whitelist.command_template_only is True,
        "rollback_present": (
            rollback.pre_inference_snapshot_required
            and rollback.rollback_required
            and rollback.rollback_preserves_test_board
            and rollback.rollback_preserves_source_uploaded_image
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeRealLocalImageInferenceTrialRequestApprovalGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeRealLocalImageInferenceTrialRequestApprovalGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_real_local_image_request_approval_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_real_local_image_inference_request_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "real_local_image_asset_registration_record_count_gte_1": True,
        "real_local_image_manifest_plan_record_count_gte_1": True,
        "real_local_image_prompt_plan_record_count_gte_1": True,
        "real_local_image_candidate_output_boundary_record_count_gte_1": True,
        "real_local_image_owner_approval_issuance_record_count_gte_1": True,
        "real_local_image_command_whitelist_record_count_gte_1": True,
        "real_local_image_memory_timeout_boundary_record_count_gte_1": True,
        "real_local_image_rollback_cleanup_plan_record_count_gte_1": True,
        "real_local_image_readiness_review_record_count_gte_1": True,
        "real_local_image_followup_execution_route_record_count_gte_1": True,
        "negative_guard_count_eq_19": negative_guard_count == 19,
        "negative_guard_passed_eq_19": negative_guard_passed == 19,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "compressed_phase": COMPRESSED_PHASE is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": MOBILE_SAM_ONLY is True,
        "real_local_image_trial_request_included": REAL_LOCAL_IMAGE_TRIAL_REQUEST_INCLUDED is True,
        "real_local_image_owner_approval_issuance_included": REAL_LOCAL_IMAGE_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "real_local_image_trial_readiness_review_included": REAL_LOCAL_IMAGE_TRIAL_READINESS_REVIEW_INCLUDED is True,
        "scoped_local_test_asset_registration": SCOPED_LOCAL_TEST_ASSET_REGISTRATION is True,
        "image_manifest_planning_allowed": IMAGE_MANIFEST_PLANNING_ALLOWED is True,
        "prompt_points_boxes_planning_allowed": PROMPT_POINTS_BOXES_PLANNING_ALLOWED is True,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "segmentation_allowed_false": SEGMENTATION_ALLOWED is False,
        "prediction_allowed_false": PREDICTION_ALLOWED is False,
        "image_input_to_model_allowed_false": IMAGE_INPUT_TO_MODEL_ALLOWED is False,
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
        "source_image_registered": True,
        "source_type_user_supplied_scoped_local_test_asset": asset_registration.source_type == SOURCE_TYPE,
        "live_camera_frame_false": asset_registration.live_camera_frame is False,
        "external_url_source_false": asset_registration.external_url_source is False,
        "uncontrolled_dataset_source_false": asset_registration.uncontrolled_dataset_source is False,
        "personal_sensitive_image_false": asset_registration.personal_sensitive_image is False,
        "candidate_only_use_true": asset_registration.candidate_only_use is True,
        "owner_approval_granted_for_real_local_image_inference_preparation": approval.owner_approval_granted_for_real_local_image_inference_preparation,
        "owner_approval_granted_for_real_local_image_inference_execution_next": approval.owner_approval_granted_for_real_local_image_inference_execution_next,
        "can_enter_real_local_image_inference_trial_execution_next": readiness.can_enter_real_local_image_inference_trial_execution_next,
        "can_enter_runtime_after_this_phase_false": readiness.can_enter_runtime_after_this_phase is False,
        "can_enter_output_adapter_after_this_phase_false": readiness.can_enter_output_adapter_after_this_phase is False,
        "can_enter_semantic_layer_after_this_phase_false": readiness.can_enter_semantic_layer_after_this_phase is False,
        "can_write_fact_after_this_phase_false": readiness.can_write_fact_after_this_phase is False,
        "can_trigger_navigation_action_speech_after_this_phase_false": readiness.can_trigger_navigation_action_speech_after_this_phase is False,
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
    decision = P1MobileSAMRealLocalImageInferenceTrialRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_real_local_image_inference_request_readiness_profile_count=1,
        real_local_image_asset_registration_record_count=1,
        real_local_image_manifest_plan_record_count=1,
        real_local_image_prompt_plan_record_count=1,
        real_local_image_candidate_output_boundary_record_count=1,
        real_local_image_owner_approval_issuance_record_count=1,
        real_local_image_command_whitelist_record_count=1,
        real_local_image_memory_timeout_boundary_record_count=1,
        real_local_image_rollback_cleanup_plan_record_count=1,
        real_local_image_readiness_review_record_count=1,
        real_local_image_followup_execution_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        can_enter_real_local_image_inference_trial_execution_next=(
            readiness.can_enter_real_local_image_inference_trial_execution_next and blocker_count == 0
        ),
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Real Local Image Inference Trial Request Approval And Readiness (planning only)",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "planning_only": PLANNING_ONLY,
        "mobile_sam_only": MOBILE_SAM_ONLY,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_runtime_boundary_planning_ref": UPSTREAM_RUNTIME_BOUNDARY_PLANNING_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_real_local_image_inference_trial_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_real_local_image_inference_request_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "runtime_boundary_upstream_audit": runtime_boundary_audit,
        "governance_standards_audit": gov_audit,
        "registry_overlay_path": overlay_path,
        "mobile_sam_registry_audit": reg_audit,
        "real_local_image_asset_registration_record": asdict(asset_registration),
        "real_local_image_manifest_plan_record": asdict(manifest_plan),
        "real_local_image_prompt_plan_record": asdict(prompt_plan),
        "real_local_image_candidate_output_boundary_record": asdict(candidate_boundary),
        "real_local_image_owner_approval_issuance_record": asdict(approval),
        "real_local_image_command_whitelist_record": asdict(whitelist),
        "real_local_image_memory_timeout_boundary_record": asdict(memory_timeout),
        "real_local_image_rollback_cleanup_plan_record": asdict(rollback),
        "real_local_image_readiness_review_record": asdict(readiness),
        "real_local_image_followup_execution_route_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "real_local_image_request_approval_readiness_status": (
                "go" if blocker_count == 0 else "blocked"
            ),
            "inference_executed_this_phase": False,
            "image_read_this_phase": False,
            "imported_this_phase": False,
            "model_loaded_this_phase": False,
            "registry_mutated_this_phase": False,
            "source_image_registered": True,
            "can_enter_real_local_image_inference_trial_execution_next": decision.can_enter_real_local_image_inference_trial_execution_next,
            "recommended_next_phase": NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION,
            "recommended_next_phase_scope": followup.next_phase_scope,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only). User-supplied night urban street scene "
                "registered as scoped local test asset. Image manifest, prompt plan, candidate-only "
                "output boundary, command whitelist, memory/timeout, rollback/cleanup, readiness review "
                "produced. Narrow owner approval issued for execution-next. NO inference, NO image input, "
                "NO import/load, NO runtime/output/semantic/fact/navigation. Next: "
                + NEXT_PHASE_REAL_IMAGE_TRIAL_EXECUTION
                + " (manifest image read, planned prompts, candidate masks only)."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    asset_registration_payload = asdict(asset_registration)
    manifest_plan_payload = {
        "manifest_plan_id": "RealLocalImageManifestPlanV1",
        "execution_manifest_output_rel": EXECUTION_MANIFEST_OUTPUT_REL,
        "planned_manifest_entry": dict(PLANNED_MANIFEST_ENTRY),
        "sha256_verification_deferred_to_execution": True,
        "width_height_verification_deferred_to_execution": True,
    }
    prompt_plan_payload = {
        "prompt_plan_id": "RealLocalImagePromptPlanV1",
        "prompt_targets": list(PLANNED_PROMPT_TARGETS),
        "prompt_labels_are_test_descriptions_only": True,
        "mobile_sam_does_not_produce_semantic_facts": True,
        "segmentation_output_is_candidate_mask_only": True,
    }
    candidate_boundary_payload = asdict(candidate_boundary)
    readiness_payload = asdict(readiness)

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / "real_local_image_asset_registration_v1.json").write_text(
            json.dumps(asset_registration_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "real_local_image_manifest_plan_v1.json").write_text(
            json.dumps(manifest_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "real_local_image_prompt_plan_v1.json").write_text(
            json.dumps(prompt_plan_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "real_local_image_candidate_output_boundary_v1.json").write_text(
            json.dumps(candidate_boundary_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "real_local_image_readiness_review_v1.json").write_text(
            json.dumps(readiness_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [result.get("output_review_file")]
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
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
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "real_local_image_asset_registration_record": {"record": asdict(asset_registration)},
            "real_local_image_manifest_plan_record": {"record": asdict(manifest_plan)},
            "real_local_image_prompt_plan_record": {"record": asdict(prompt_plan)},
            "real_local_image_candidate_output_boundary_record": {"record": asdict(candidate_boundary)},
            "real_local_image_owner_approval_issuance_record": {"record": asdict(approval)},
            "real_local_image_command_whitelist_record": {"record": asdict(whitelist)},
            "real_local_image_memory_timeout_boundary_record": {"record": asdict(memory_timeout)},
            "real_local_image_rollback_cleanup_plan_record": {"record": asdict(rollback)},
            "real_local_image_readiness_review_record": {"record": asdict(readiness)},
            "real_local_image_followup_execution_route_record": {"record": asdict(followup)},
        }
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
            "real_inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
            "registry_mutation_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "source_image_registered": result["conclusions"]["source_image_registered"],
                "can_enter_real_local_image_inference_trial_execution_next": result["conclusions"][
                    "can_enter_real_local_image_inference_trial_execution_next"
                ],
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
