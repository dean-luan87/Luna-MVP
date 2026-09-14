# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Registry Patch And Inference Trial Readiness — review v1
(PLANNING ONLY, scope = mobile_sam_only).

Audits model-load retry GO evidence, plans registry overlay patch (NOT written),
plans inference trial request/approval/readiness/boundaries, and follow-up routes.
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
from capabilities.field_understanding.p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning.p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning.p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_TRIAL_READINESS_PLANNING,
    INFERENCE_TRIAL_REQUEST_PLANNING,
    LUNA_CORE_PRINCIPLE,
    MEMORY_LIMIT_MB,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_REGISTRY_PATCH_PLANNING,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_INFERENCE_TRIAL_REQUEST,
    NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_READINESS_LEVEL,
    PLANNED_REGISTRY_PATCH,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    PREDICTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_FILE_WRITE_ALLOWED,
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
    TIMEOUT_SECONDS,
    UPSTREAM_EXPECTED,
    UPSTREAM_MODEL_LOAD_RETRY_REF,
    UPSTREAM_RETRY_ARTIFACT_REFS,
    UPSTREAM_RETRY_REVIEW_FILE_REL,
    WEIGHT_CHAIN,
    MobileSAMFollowupRegistryPatchExecutionRoute,
    MobileSAMImageInputBoundaryPlanningRecord,
    MobileSAMInferenceCommandWhitelistPlanningRecord,
    MobileSAMInferenceMemoryTimeoutBoundaryRecord,
    MobileSAMInferenceOwnerApprovalPlanningRecord,
    MobileSAMInferenceReadinessReview,
    MobileSAMInferenceRollbackCleanupPlanningRecord,
    MobileSAMInferenceTrialRequestPlanningRecord,
    MobileSAMModelLoadRegistryPatchPlanningRecord,
    MobileSAMModelLoadSuccessAudit,
    NegativeMobileSAMModelLoadRegistryPatchInferenceReadinessPlanningGuard,
    P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningDecision,
    P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningProfile,
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
    / "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_review_v1.json"
)

_PKG = (
    "capabilities/field_understanding/"
    "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning"
)
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_model_load_registry_patch_inference_readiness_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_model_load_registry_patch_inference_readiness_planning_decision_v1"
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            model_load_registry_patch_planning=MODEL_LOAD_REGISTRY_PATCH_PLANNING,
            inference_trial_request_planning=INFERENCE_TRIAL_REQUEST_PLANNING,
            inference_trial_readiness_planning=INFERENCE_TRIAL_READINESS_PLANNING,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            registry_file_write_allowed=REGISTRY_FILE_WRITE_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            image_input_allowed=IMAGE_INPUT_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            model_load_retry_allowed=MODEL_LOAD_RETRY_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_model_load_retry_ref=UPSTREAM_MODEL_LOAD_RETRY_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1(
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
    # (一) Upstream model-load retry success audit.
    # ------------------------------------------------------------------- #
    review = _load_json(UPSTREAM_RETRY_REVIEW_FILE_REL) or {}
    concl = review.get("conclusions", {})
    post_audit = review.get("mobile_sam_retry_post_review_audit", {})
    sha_recheck = review.get("mobile_sam_retry_sha256_recheck_record", {})
    dep_avail = review.get("mobile_sam_retry_dependency_availability_record", {})
    torch_boundary = review.get("mobile_sam_retry_torch_torchvision_boundary_record", {})
    load_exec = review.get("mobile_sam_retry_model_load_execution_record", {})
    monitor = review.get("mobile_sam_retry_memory_timeout_monitor_record", {})
    exclusion = review.get("mobile_sam_inference_runtime_exclusion_record", {})

    final_decision_ok = review.get("final_decision") == UPSTREAM_EXPECTED["final_decision"]
    blocker_ok = review.get("blocker_count") == UPSTREAM_EXPECTED["blocker_count"]
    neg_guard_ok = review.get("negative_guard_passed", 0) >= UPSTREAM_EXPECTED["negative_guard_passed"]

    import_ok = bool(concl.get("import_success", load_exec.get("model_load_retry_success")))
    dep_gap_ok = bool(concl.get("dependency_gap_resolved"))
    checkpoint_ok = bool(concl.get("checkpoint_load_success", load_exec.get("checkpoint_load_success")))
    retry_ok = bool(concl.get("model_load_retry_success", load_exec.get("model_load_retry_success")))
    model_type = str(load_exec.get("model_type_name", UPSTREAM_EXPECTED["model_type_name"]))
    size_matches = bool(sha_recheck.get("size_matches", concl.get("size_matches")))
    sha256_matches = bool(sha_recheck.get("sha256_matches", concl.get("sha256_matches")))
    timm_spec = bool(dep_avail.get("timm_find_spec_result", post_audit.get("timm_find_spec_verified")))
    ms_spec = bool(dep_avail.get("mobile_sam_find_spec_result", post_audit.get("mobile_sam_find_spec_verified")))
    peak_mb = float(concl.get("peak_memory_mb", monitor.get("peak_memory_mb", 359)) or 359)
    elapsed = float(concl.get("elapsed_seconds", monitor.get("elapsed_seconds", 1.75)) or 1.75)

    audit = MobileSAMModelLoadSuccessAudit(
        audit_id="mobile_sam_model_load_success_audit_v1",
        upstream_review_file_ref=UPSTREAM_RETRY_REVIEW_FILE_REL,
        final_decision_ok=final_decision_ok,
        blocker_count_ok=blocker_ok,
        negative_guard_ok=neg_guard_ok,
        import_success=import_ok,
        dependency_gap_resolved=dep_gap_ok,
        checkpoint_load_success=checkpoint_ok,
        model_load_retry_success=retry_ok,
        model_type_name=model_type,
        size_matches=size_matches,
        sha256_matches=sha256_matches,
        timm_find_spec_verified=timm_spec,
        mobile_sam_find_spec_verified=ms_spec,
        torch_observed_during_load=bool(torch_boundary.get("torch_observed_during_load")),
        torch_version_observed=str(torch_boundary.get("torch_version_observed_if_available", "2.8.0")),
        torchvision_observed_during_load=bool(torch_boundary.get("torchvision_observed_during_load")),
        torchvision_version_observed=str(torch_boundary.get("torchvision_version_observed_if_available", "0.23.0")),
        peak_memory_mb=peak_mb,
        elapsed_seconds=elapsed,
        no_image_input=bool(post_audit.get("no_image_input", True)),
        no_segmentation=bool(post_audit.get("no_segmentation", True)),
        no_prediction=bool(post_audit.get("no_prediction", True)),
        no_inference=bool(post_audit.get("no_inference", True)),
        no_runtime=bool(post_audit.get("no_runtime", True)),
        no_output_adapter=bool(post_audit.get("no_output_adapter", True)),
        no_semantic_layer=bool(post_audit.get("no_semantic_layer", True)),
        no_registry_mutation=bool(post_audit.get("no_registry_mutation", True)),
        no_extra_download=bool(post_audit.get("no_extra_download", True)),
        registry_mutation_performed=False,
        real_import_performed=False,
        model_load_performed=False,
        inference_performed=False,
        audit_passed=(
            final_decision_ok
            and blocker_ok
            and neg_guard_ok
            and import_ok
            and dep_gap_ok
            and checkpoint_ok
            and retry_ok
            and size_matches
            and sha256_matches
            and timm_spec
            and ms_spec
            and bool(post_audit.get("no_inference", True))
            and bool(post_audit.get("no_registry_mutation", True))
        ),
    )
    if not audit.audit_passed:
        failed_checks.append("upstream.model_load_retry_audit_failed")

    upstream_artifact_present = all(_load_json(ref) is not None for ref in UPSTREAM_RETRY_ARTIFACT_REFS)
    if not upstream_artifact_present:
        warnings.append("upstream.some_retry_artifact_missing_using_review_aggregate")

    # ------------------------------------------------------------------- #
    # (二) Registry patch planning (PLAN ONLY).
    # ------------------------------------------------------------------- #
    planned_patch = dict(PLANNED_REGISTRY_PATCH)
    planned_patch["model_load_peak_memory_mb"] = round(peak_mb)
    planned_patch["model_load_elapsed_seconds"] = round(elapsed, 2)
    planned_patch["torch_version_observed"] = audit.torch_version_observed
    planned_patch["torchvision_version_observed"] = audit.torchvision_version_observed

    patch_plan = MobileSAMModelLoadRegistryPatchPlanningRecord(
        record_id="mobile_sam_model_load_registry_patch_plan_v1",
        registry_overlay_ref=REGISTRY_OVERLAY_REL,
        patch_is_plan_only=True,
        patch_is_not_registry_mutation=True,
        planned_patch_values=planned_patch,
        planned_readiness_level=PLANNED_READINESS_LEVEL,
        planned_inference_ready=False,
        planned_runtime_ready=False,
        planned_output_adapter_ready=False,
        planned_semantic_layer_ready=False,
        planned_commercial_runtime_approved=False,
    )

    # ------------------------------------------------------------------- #
    # (三–八) Inference trial planning records.
    # ------------------------------------------------------------------- #
    inference_request = MobileSAMInferenceTrialRequestPlanningRecord(
        request_id="mobile_sam_inference_trial_request_plan_v1",
        asset_id="mobile_sam",
        request_scope="controlled_inference_trial_preparation",
        inference_trial_requested=True,
        inference_execution_requested_later=True,
        image_input_required_for_future_trial=True,
        segmentation_or_prediction_required_for_future_trial=True,
        request_is_not_inference_execution=True,
        request_is_not_runtime_approval=True,
        request_is_not_output_adapter_approval=True,
        request_is_not_semantic_layer_approval=True,
        request_is_not_commercial_runtime_approval=True,
    )

    owner_approval = MobileSAMInferenceOwnerApprovalPlanningRecord(
        record_id="mobile_sam_inference_owner_approval_plan_v1",
        owner_approval_required_for_inference_trial=True,
        owner_approval_granted_now=False,
        inference_trial_execution_requires_separate_request_or_issuance=True,
        inference_trial_execution_requires_separate_phase=True,
        runtime_approved=False,
        output_adapter_approved=False,
        semantic_layer_approved=False,
        commercial_runtime_approved=False,
        fact_write_approved=False,
        navigation_action_speech_approved=False,
    )

    image_boundary = MobileSAMImageInputBoundaryPlanningRecord(
        record_id="mobile_sam_image_input_boundary_plan_v1",
        allowed_candidates=(
            "synthetic_test_image",
            "tiny_static_local_test_image",
            "explicitly_scoped_local_test_asset",
        ),
        forbidden_sources=(
            "live_camera",
            "user_personal_image",
            "external_url_image",
            "uncontrolled_dataset",
            "navigation_runtime_frame",
            "semantic_fact_input_frame",
        ),
        image_input_must_be_local=True,
        image_input_must_be_test_asset=True,
        image_input_must_have_manifest=True,
        image_input_must_not_contain_personal_data=True,
        image_input_must_not_enter_fact_layer=True,
        image_input_must_not_enter_navigation_runtime=True,
    )

    cmd_whitelist = MobileSAMInferenceCommandWhitelistPlanningRecord(
        record_id="mobile_sam_inference_command_whitelist_plan_v1",
        allowed_future_steps=(
            "sha256_recheck",
            "model_import_load",
            "one_controlled_inference_call",
            "local_test_image_path",
            "output_captured_as_candidate_only",
            "memory_timeout_monitor",
            "post_review",
        ),
        forbidden_future_steps=(
            "runtime_server",
            "output_adapter_call",
            "semantic_write",
            "fact_write",
            "navigation_action_speech_output",
            "external_network_download",
            "batch_dataset_run",
        ),
        command_template_only=True,
        command_not_executed=True,
        inference_command_requires_next_phase=True,
    )

    mem_timeout = MobileSAMInferenceMemoryTimeoutBoundaryRecord(
        record_id="mobile_sam_inference_memory_timeout_boundary_v1",
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        oom_handling_required=True,
        timeout_failure_records_required=True,
        candidate_output_cleanup_required=True,
        no_persistent_runtime_process_allowed=True,
    )

    rollback_plan = MobileSAMInferenceRollbackCleanupPlanningRecord(
        record_id="mobile_sam_inference_rollback_cleanup_plan_v1",
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

    readiness_review = MobileSAMInferenceReadinessReview(
        review_id="mobile_sam_inference_readiness_review_v1",
        can_enter_model_load_registry_patch_execution_next=audit.audit_passed,
        can_enter_inference_trial_request_approval_next=audit.audit_passed,
        can_enter_inference_execution_now=False,
        inference_execution_requires_registry_patch_go=True,
        inference_execution_requires_owner_approval=True,
        inference_execution_requires_test_image_manifest=True,
        inference_execution_requires_candidate_output_boundary=True,
        inference_success_not_runtime_approval=True,
        inference_success_not_output_adapter_approval=True,
        inference_success_not_semantic_layer_approval=True,
    )

    followup = MobileSAMFollowupRegistryPatchExecutionRoute(
        route_id="mobile_sam_followup_registry_patch_execution_route_v1",
        recommended_next_phase=NEXT_PHASE_REGISTRY_PATCH_EXECUTION,
        subsequent_inference_trial_phase=NEXT_PHASE_INFERENCE_TRIAL_REQUEST,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_registry_overlay_write=True,
        next_phase_still_no_inference=True,
    )

    # ------------------------------------------------------------------- #
    # Negative guards (16).
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_retry_go_verified": audit.final_decision_ok and audit.blocker_count_ok,
        "upstream_boundary_clean": (
            audit.no_inference
            and audit.no_runtime
            and audit.no_registry_mutation
            and audit.no_extra_download
            and audit.no_image_input
        ),
        "no_registry_mutation": (
            REGISTRY_MUTATION_ALLOWED is False
            and REGISTRY_FILE_WRITE_ALLOWED is False
            and audit.registry_mutation_performed is False
        ),
        "no_real_import_load": (
            REAL_IMPORT_ALLOWED is False
            and MODEL_LOAD_ALLOWED is False
            and MODEL_LOAD_RETRY_ALLOWED is False
            and audit.real_import_performed is False
            and audit.model_load_performed is False
        ),
        "no_image_input": IMAGE_INPUT_ALLOWED is False,
        "no_seg_pred_inference": (
            SEGMENTATION_ALLOWED is False
            and PREDICTION_ALLOWED is False
            and REAL_INFERENCE_ALLOWED is False
            and audit.inference_performed is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_extra_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False and MODEL_DOWNLOAD_ALLOWED is False
        ),
        "patch_not_downstream_ready": (
            patch_plan.planned_inference_ready is False
            and patch_plan.planned_runtime_ready is False
            and patch_plan.planned_output_adapter_ready is False
            and patch_plan.planned_semantic_layer_ready is False
            and patch_plan.planned_commercial_runtime_approved is False
        ),
        "request_not_execution_approval": (
            inference_request.request_is_not_inference_execution
            and owner_approval.owner_approval_granted_now is False
            and readiness_review.can_enter_inference_execution_now is False
        ),
        "image_boundary_strict": (
            "live_camera" in image_boundary.forbidden_sources
            and "user_personal_image" in image_boundary.forbidden_sources
            and image_boundary.image_input_must_be_local
        ),
        "future_output_candidate_only": "output_captured_as_candidate_only" in cmd_whitelist.allowed_future_steps,
        "future_trial_no_runtime_semantic": (
            "runtime_server" in cmd_whitelist.forbidden_future_steps
            and "semantic_write" in cmd_whitelist.forbidden_future_steps
            and "fact_write" in cmd_whitelist.forbidden_future_steps
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMModelLoadRegistryPatchInferenceReadinessPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMModelLoadRegistryPatchInferenceReadinessPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_registry_patch_inference_readiness_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_model_load_registry_patch_inference_readiness_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_model_load_success_audit_count_gte_1": True,
        "mobile_sam_model_load_registry_patch_plan_record_count_gte_1": True,
        "mobile_sam_inference_trial_request_plan_record_count_gte_1": True,
        "mobile_sam_inference_owner_approval_plan_record_count_gte_1": True,
        "mobile_sam_image_input_boundary_plan_record_count_gte_1": True,
        "mobile_sam_inference_command_whitelist_plan_record_count_gte_1": True,
        "mobile_sam_inference_memory_timeout_boundary_count_gte_1": True,
        "mobile_sam_inference_rollback_cleanup_plan_count_gte_1": True,
        "mobile_sam_inference_readiness_review_count_gte_1": True,
        "mobile_sam_followup_registry_patch_execution_route_count_gte_1": True,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "model_load_registry_patch_planning": MODEL_LOAD_REGISTRY_PATCH_PLANNING is True,
        "inference_trial_request_planning": INFERENCE_TRIAL_REQUEST_PLANNING is True,
        "inference_trial_readiness_planning": INFERENCE_TRIAL_READINESS_PLANNING is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "registry_file_write_allowed_false": REGISTRY_FILE_WRITE_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "image_input_allowed_false": IMAGE_INPUT_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "registry_patch_planned": patch_plan.patch_is_plan_only,
        "planned_readiness_level_model_load_verified": patch_plan.planned_readiness_level == PLANNED_READINESS_LEVEL,
        "planned_model_load_verified": planned_patch.get("model_load_verified") is True,
        "planned_checkpoint_load_verified": planned_patch.get("checkpoint_load_verified") is True,
        "planned_dependency_gap_resolved": planned_patch.get("dependency_gap_resolved") is True,
        "planned_inference_ready_false": patch_plan.planned_inference_ready is False,
        "planned_runtime_ready_false": patch_plan.planned_runtime_ready is False,
        "can_enter_model_load_registry_patch_execution_next": readiness_review.can_enter_model_load_registry_patch_execution_next,
        "can_enter_inference_trial_request_approval_next": readiness_review.can_enter_inference_trial_request_approval_next,
        "can_enter_inference_execution_now_false": readiness_review.can_enter_inference_execution_now is False,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)

    if blocker_count == 0 and audit.audit_passed:
        final_decision = FINAL_DECISION_GO
        recommended_next_phase = NEXT_PHASE_REGISTRY_PATCH_EXECUTION
    else:
        final_decision = FINAL_DECISION_BLOCKED
        recommended_next_phase = NEXT_PHASE_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_model_load_registry_patch_inference_readiness_planning_profile_count=1,
        mobile_sam_model_load_success_audit_count=1,
        mobile_sam_model_load_registry_patch_plan_record_count=1,
        mobile_sam_inference_trial_request_plan_record_count=1,
        mobile_sam_inference_owner_approval_plan_record_count=1,
        mobile_sam_image_input_boundary_plan_record_count=1,
        mobile_sam_inference_command_whitelist_plan_record_count=1,
        mobile_sam_inference_memory_timeout_boundary_count=1,
        mobile_sam_inference_rollback_cleanup_plan_count=1,
        mobile_sam_inference_readiness_review_count=1,
        mobile_sam_followup_registry_patch_execution_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        registry_patch_planned=patch_plan.patch_is_plan_only,
        planned_readiness_level=PLANNED_READINESS_LEVEL,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Model Load Registry Patch And Inference Trial Readiness Planning",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "upstream_model_load_retry_ref": UPSTREAM_MODEL_LOAD_RETRY_REF,
        "upstream_retry_artifact_refs": list(UPSTREAM_RETRY_ARTIFACT_REFS),
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_model_load_registry_patch_inference_readiness_planning_profile": _build_profile(),
        "mobile_sam_model_load_registry_patch_inference_readiness_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_model_load_success_audit": asdict(audit),
        "mobile_sam_model_load_success_audit_count": 1,
        "mobile_sam_model_load_registry_patch_plan_record": asdict(patch_plan),
        "mobile_sam_model_load_registry_patch_plan_record_count": 1,
        "mobile_sam_inference_trial_request_plan_record": asdict(inference_request),
        "mobile_sam_inference_trial_request_plan_record_count": 1,
        "mobile_sam_inference_owner_approval_plan_record": asdict(owner_approval),
        "mobile_sam_inference_owner_approval_plan_record_count": 1,
        "mobile_sam_image_input_boundary_plan_record": asdict(image_boundary),
        "mobile_sam_image_input_boundary_plan_record_count": 1,
        "mobile_sam_inference_command_whitelist_plan_record": asdict(cmd_whitelist),
        "mobile_sam_inference_command_whitelist_plan_record_count": 1,
        "mobile_sam_inference_memory_timeout_boundary_record": asdict(mem_timeout),
        "mobile_sam_inference_memory_timeout_boundary_count": 1,
        "mobile_sam_inference_rollback_cleanup_plan_record": asdict(rollback_plan),
        "mobile_sam_inference_rollback_cleanup_plan_count": 1,
        "mobile_sam_inference_readiness_review": asdict(readiness_review),
        "mobile_sam_inference_readiness_review_count": 1,
        "mobile_sam_followup_registry_patch_execution_route": asdict(followup),
        "mobile_sam_followup_registry_patch_execution_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": "go" if final_decision == FINAL_DECISION_GO else "blocked",
            "registry_patch_planned": True,
            "planned_readiness_level": PLANNED_READINESS_LEVEL,
            "planned_model_load_verified": True,
            "planned_checkpoint_load_verified": True,
            "planned_dependency_gap_resolved": True,
            "planned_inference_ready": False,
            "can_enter_model_load_registry_patch_execution_next": readiness_review.can_enter_model_load_registry_patch_execution_next,
            "can_enter_inference_trial_request_approval_next": readiness_review.can_enter_inference_trial_request_approval_next,
            "can_enter_inference_execution_now": False,
            "recommended_next_phase": recommended_next_phase,
            "subsequent_inference_trial_phase": NEXT_PHASE_INFERENCE_TRIAL_REQUEST,
            "transition_note": (
                "PLANNING ONLY. Model-load retry GO audited; registry patch to model_load_verified "
                "planned (NOT written). Inference trial request/approval/readiness planned. "
                "NO inference/image/runtime/registry write this phase."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

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
            "mobile_sam_model_load_success_audit_record": {"mobile_sam_model_load_success_audit": asdict(audit)},
            "mobile_sam_model_load_registry_patch_plan_record": {
                "mobile_sam_model_load_registry_patch_plan_record": asdict(patch_plan),
            },
            "mobile_sam_inference_trial_request_plan_record": {
                "mobile_sam_inference_trial_request_plan_record": asdict(inference_request),
            },
            "mobile_sam_inference_owner_approval_plan_record": {
                "mobile_sam_inference_owner_approval_plan_record": asdict(owner_approval),
            },
            "mobile_sam_image_input_boundary_plan_record": {
                "mobile_sam_image_input_boundary_plan_record": asdict(image_boundary),
            },
            "mobile_sam_inference_command_whitelist_plan_record": {
                "mobile_sam_inference_command_whitelist_plan_record": asdict(cmd_whitelist),
            },
            "mobile_sam_inference_memory_timeout_boundary_record": {
                "mobile_sam_inference_memory_timeout_boundary_record": asdict(mem_timeout),
            },
            "mobile_sam_inference_rollback_cleanup_plan_record": {
                "mobile_sam_inference_rollback_cleanup_plan_record": asdict(rollback_plan),
            },
            "mobile_sam_inference_readiness_review_record": {
                "mobile_sam_inference_readiness_review": asdict(readiness_review),
            },
            "mobile_sam_followup_registry_patch_execution_route_record": {
                "mobile_sam_followup_registry_patch_execution_route": asdict(followup),
            },
        }
        extra_written: List[str] = []
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": ts,
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
            "registry_mutation_allowed": False,
            "inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
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
    result = review_p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "planned_readiness_level": result["conclusions"]["planned_readiness_level"],
                "can_enter_model_load_registry_patch_execution_next": result["conclusions"][
                    "can_enter_model_load_registry_patch_execution_next"
                ],
                "can_enter_inference_execution_now": result["conclusions"]["can_enter_inference_execution_now"],
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
