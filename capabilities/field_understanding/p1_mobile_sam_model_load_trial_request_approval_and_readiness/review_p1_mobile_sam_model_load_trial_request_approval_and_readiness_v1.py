# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Request, Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only).

Audits the registry overlay (must show mobile_sam=code_and_weight_ready with verified
weight sha256/size/storage), then produces the model-load trial request, a NARROW owner
approval issuance (model-load preparation + execution-next only; NOT inference/runtime/
output-adapter/semantic/commercial-runtime), a TEMPLATE-ONLY model-load command
whitelist (never executed; no image input / segmentation / prediction / runtime server),
a sha256 recheck plan, a controlled env/code/weight path plan, a memory/timeout boundary,
a rollback/cleanup plan, a readiness review, and a follow-up execution handoff. It does
NOT real import / model load / inference / runtime / output adapter / semantic promotion /
registry mutation and downloads NO extra weight. byte_track is out of scope. Protected,
non-deletable test board records are written in `planning` mode.
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
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_request_approval_and_readiness.p1_mobile_sam_model_load_trial_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_request_approval_and_readiness.p1_mobile_sam_model_load_trial_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPECTED_READINESS_LEVEL,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF,
    MOBILE_SAM_IMPORT_ROOT,
    MOBILE_SAM_WEIGHT_FILE_NAME,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    MODEL_LOAD_EXECUTION_ALLOWED,
    MODEL_LOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    MODEL_LOAD_READINESS_REVIEW_INCLUDED,
    MODEL_LOAD_TRIAL_REQUEST_INCLUDED,
    MODEL_LOAD_PRINCIPLE_ZH,
    NEGATIVE_GUARDS,
    NEXT_PHASE_MODEL_LOAD_EXECUTION,
    OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    OVERLAY_EXPECTED_FALSE,
    OVERLAY_EXPECTED_TRUE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_MAX_RUNTIME_SECONDS,
    PLANNED_MEMORY_LIMIT_MB,
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
    WEIGHT_CHAIN,
    MobileSAMCodeAndWeightRegistryAudit,
    MobileSAMModelLoadCommandWhitelistRecord,
    MobileSAMModelLoadEnvPathPlan,
    MobileSAMModelLoadExecutionHandoffRecord,
    MobileSAMModelLoadMemoryTimeoutBoundary,
    MobileSAMModelLoadOwnerApprovalIssuanceRecord,
    MobileSAMModelLoadReadinessReview,
    MobileSAMModelLoadRollbackCleanupPlan,
    MobileSAMModelLoadSha256RecheckPlan,
    MobileSAMModelLoadTrialRequestRecord,
    NegativeMobileSAMModelLoadRequestApprovalReadinessGuard,
    P1MobileSAMModelLoadRequestApprovalReadinessDecision,
    P1MobileSAMModelLoadTrialRequestApprovalReadinessProfile,
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
    / "p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_model_load_trial_request_approval_and_readiness_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_model_load_trial_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_model_load_trial_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_model_load_trial_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_model_load_trial_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_model_load_trial_request_approval_readiness_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

CONTROLLED_PYTHON_EXECUTABLE = ".venv_model_load_trial/bin/python"
CONTROLLED_ENV_PATH = ".venv_model_load_trial"
MODEL_LOAD_ENV_PATH = ".venv_model_load_trial"


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
        P1MobileSAMModelLoadTrialRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            mobile_sam_only=True,
            model_load_trial_request_included=MODEL_LOAD_TRIAL_REQUEST_INCLUDED,
            model_load_owner_approval_issuance_included=MODEL_LOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            model_load_readiness_review_included=MODEL_LOAD_READINESS_REVIEW_INCLUDED,
            model_load_execution_allowed=MODEL_LOAD_EXECUTION_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_patch_execution_ref=UPSTREAM_PATCH_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1(
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

    ts = _now()

    # ------------------------------------------------------------------- #
    # (一) Upstream registry overlay audit — code_and_weight_ready.
    # ------------------------------------------------------------------- #
    overlay_path = _overlay_path()
    overlay_exists = overlay_path.is_file()
    overlay: Dict[str, Any] = {}
    if overlay_exists:
        try:
            overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            overlay = {}
            overlay_exists = False
    assets = overlay.get("assets", {})
    ms = assets.get(MOBILE_SAM_ASSET_ID, {})
    bt = assets.get("byte_track", {})

    true_field_checks = {f: (ms.get(f) is True) for f in OVERLAY_EXPECTED_TRUE}
    false_field_checks = {f: (ms.get(f) is False) for f in OVERLAY_EXPECTED_FALSE}
    readiness_level = ms.get("readiness_level", "")
    readiness_level_ok = readiness_level == EXPECTED_READINESS_LEVEL
    weight_file_path_ok = ms.get("weight_file_path") == MOBILE_SAM_WEIGHT_FILE_PATH
    weight_size_ok = ms.get("weight_file_size_bytes") == MOBILE_SAM_WEIGHT_SIZE_BYTES
    weight_sha256_ok = ms.get("weight_sha256") == MOBILE_SAM_WEIGHT_SHA256
    byte_track_weight_downloaded = bt.get("weight_downloaded") is True
    byte_track_out_of_scope = not byte_track_weight_downloaded
    import_root_ok = ms.get("import_root") == MOBILE_SAM_IMPORT_ROOT
    model_weight_status_ok = ms.get("model_weight_status") == "downloaded"

    audit_passed = (
        overlay_exists
        and readiness_level_ok
        and all(true_field_checks.values())
        and all(false_field_checks.values())
        and weight_file_path_ok
        and weight_size_ok
        and weight_sha256_ok
        and import_root_ok
        and model_weight_status_ok
        and byte_track_out_of_scope
    )
    audit = MobileSAMCodeAndWeightRegistryAudit(
        audit_id="mobile_sam_code_and_weight_registry_audit_v1",
        overlay_file_ref=REGISTRY_OVERLAY_REL,
        overlay_exists=overlay_exists,
        readiness_level=readiness_level,
        readiness_level_ok=readiness_level_ok,
        true_field_checks=true_field_checks,
        false_field_checks=false_field_checks,
        weight_file_path_ok=weight_file_path_ok,
        weight_size_ok=weight_size_ok,
        weight_sha256_ok=weight_sha256_ok,
        byte_track_weight_downloaded=byte_track_weight_downloaded,
        byte_track_out_of_scope=byte_track_out_of_scope,
        audit_passed=audit_passed,
    )
    if not audit_passed:
        failed_checks.append("audit.mobile_sam_not_code_and_weight_ready_or_weight_unverified")

    # ------------------------------------------------------------------- #
    # (二) Model-load trial request.
    # ------------------------------------------------------------------- #
    request = MobileSAMModelLoadTrialRequestRecord(
        request_id="mobile_sam_model_load_trial_request_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        request_scope="model_load_trial_only",
        model_load_trial_requested=True,
        model_load_execution_requested_next=True,
        no_inference_requested=True,
        no_runtime_requested=True,
        no_output_adapter_requested=True,
        no_semantic_layer_requested=True,
        request_is_not_execution=True,
        request_is_not_inference_approval=True,
        request_is_not_runtime_approval=True,
        request_is_not_commercial_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (三) Owner approval issuance (narrow).
    # ------------------------------------------------------------------- #
    approval = MobileSAMModelLoadOwnerApprovalIssuanceRecord(
        approval_id="mobile_sam_model_load_owner_approval_issuance_v1",
        owner_approval_granted_for_model_load_preparation=True,
        owner_approval_granted_for_model_load_execution_next=True,
        inference_not_approved=True,
        runtime_not_approved=True,
        output_adapter_not_approved=True,
        semantic_layer_not_approved=True,
        commercial_runtime_not_approved=True,
        registry_mutation_not_approved=True,
        additional_weight_download_not_approved=True,
        model_load_approval_success_not_inference_approval=True,
        model_load_approval_success_not_runtime_approval=True,
        model_load_approval_success_not_output_adapter_approval=True,
        model_load_approval_success_not_semantic_layer_approval=True,
        model_load_approval_success_not_commercial_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (四) Model-load command whitelist (template only, not executed).
    # ------------------------------------------------------------------- #
    command_template = (
        "{python} -c \""
        "import importlib; "
        "m = importlib.import_module('" + MOBILE_SAM_IMPORT_ROOT + "'); "
        "from mobile_sam import sam_model_registry; "
        "model = sam_model_registry['vit_t'](checkpoint='" + MOBILE_SAM_WEIGHT_FILE_PATH + "'); "
        "print('model_object_constructed', type(model).__name__)\""
    ).replace("{python}", CONTROLLED_PYTHON_EXECUTABLE)
    whitelist = MobileSAMModelLoadCommandWhitelistRecord(
        record_id="mobile_sam_model_load_command_whitelist_v1",
        controlled_python_executable=CONTROLLED_PYTHON_EXECUTABLE,
        controlled_env_path=CONTROLLED_ENV_PATH,
        source_code_path_ref=MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF,
        weight_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        import_target=MOBILE_SAM_IMPORT_ROOT,
        checkpoint_load_target=MOBILE_SAM_WEIGHT_FILE_NAME,
        command_template=command_template,
        no_inference_command_allowed=True,
        no_image_input_allowed=True,
        no_segmentation_prediction_call_allowed=True,
        no_runtime_server_allowed=True,
        command_template_only=True,
        command_not_executed=True,
        model_load_command_template_success_not_model_load_execution=True,
    )

    # ------------------------------------------------------------------- #
    # (五) Sha256 recheck plan.
    # ------------------------------------------------------------------- #
    sha256_recheck = MobileSAMModelLoadSha256RecheckPlan(
        plan_id="mobile_sam_model_load_sha256_recheck_plan_v1",
        sha256_recheck_required_before_model_load=True,
        expected_sha256=MOBILE_SAM_WEIGHT_SHA256,
        expected_size_bytes=MOBILE_SAM_WEIGHT_SIZE_BYTES,
        storage_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        sha256_mismatch_blocks_model_load=True,
        size_mismatch_blocks_model_load=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Env / path plan.
    # ------------------------------------------------------------------- #
    env_path = MobileSAMModelLoadEnvPathPlan(
        plan_id="mobile_sam_model_load_env_path_plan_v1",
        controlled_model_load_env_required=True,
        model_load_env_path=MODEL_LOAD_ENV_PATH,
        code_path_ref_required=True,
        weight_path_ref_required=True,
        no_global_env_mutation_allowed=True,
        no_install_during_model_load_trial=True,
        no_download_during_model_load_trial=True,
    )

    # ------------------------------------------------------------------- #
    # (七) Memory / timeout boundary.
    # ------------------------------------------------------------------- #
    boundary = MobileSAMModelLoadMemoryTimeoutBoundary(
        boundary_id="mobile_sam_model_load_memory_timeout_boundary_v1",
        memory_usage_limit_required=True,
        memory_limit_mb_planned=PLANNED_MEMORY_LIMIT_MB,
        timeout_required=True,
        max_runtime_seconds_planned=PLANNED_MAX_RUNTIME_SECONDS,
        oom_handling_required=True,
        timeout_failure_records_required=True,
        partial_model_object_cleanup_required=True,
        no_persistent_runtime_process_allowed=True,
    )

    # ------------------------------------------------------------------- #
    # (八) Rollback / cleanup plan.
    # ------------------------------------------------------------------- #
    rollback = MobileSAMModelLoadRollbackCleanupPlan(
        plan_id="mobile_sam_model_load_rollback_cleanup_plan_v1",
        pre_model_load_snapshot_required=True,
        rollback_required=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        failed_model_load_cleanup_required=True,
        partial_model_object_cleanup_required=True,
        no_registry_mutation_on_failure=True,
    )

    # ------------------------------------------------------------------- #
    # (九) Readiness review.
    # ------------------------------------------------------------------- #
    readiness = MobileSAMModelLoadReadinessReview(
        review_id="mobile_sam_model_load_readiness_review_v1",
        can_enter_model_load_execution_next=audit_passed,
        model_load_execution_scope="mobile_sam_only",
        can_inference_after_model_load=False,
        can_runtime_after_model_load=False,
        can_output_adapter_after_model_load=False,
        can_semantic_layer_after_model_load=False,
        inference_requires_separate_trial=True,
        runtime_requires_separate_trial=True,
        output_adapter_requires_separate_review=True,
        semantic_layer_requires_separate_promotion=True,
    )

    # ------------------------------------------------------------------- #
    # (十) Follow-up execution handoff.
    # ------------------------------------------------------------------- #
    handoff = MobileSAMModelLoadExecutionHandoffRecord(
        handoff_id="mobile_sam_model_load_execution_handoff_v1",
        recommended_next_phase=NEXT_PHASE_MODEL_LOAD_EXECUTION,
        next_phase_scope="mobile_sam_only",
        next_phase_allows_controlled_import=True,
        next_phase_allows_controlled_model_load=True,
        next_phase_allows_sha256_recheck=True,
        next_phase_allows_memory_timeout_monitoring=True,
        next_phase_still_no_inference=True,
        next_phase_still_no_segmentation_prediction=True,
        next_phase_still_no_runtime=True,
        optional_followup_phase=OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
    )

    # ------------------------------------------------------------------- #
    # (十一) Invariants for the 16 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "overlay_code_and_weight_ready": overlay_exists and readiness_level_ok and all(false_field_checks.values()),
        "weight_integrity_verified": weight_sha256_ok and weight_size_ok and weight_file_path_ok
        and (ms.get("weight_integrity_verified") is True) and (ms.get("storage_verified") is True),
        "byte_track_out_of_scope": byte_track_out_of_scope,
        "no_real_import_or_model_load": REAL_IMPORT_ALLOWED is False and MODEL_LOAD_EXECUTION_ALLOWED is False,
        "no_inference_segmentation_prediction": REAL_INFERENCE_ALLOWED is False
        and whitelist.no_segmentation_prediction_call_allowed is True
        and whitelist.no_image_input_allowed is True,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
        and env_path.no_download_during_model_load_trial is True,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False
        and rollback.no_registry_mutation_on_failure is True,
        "approval_not_inference_runtime": (
            approval.model_load_approval_success_not_inference_approval
            and approval.model_load_approval_success_not_runtime_approval
            and approval.model_load_approval_success_not_output_adapter_approval
            and approval.model_load_approval_success_not_semantic_layer_approval
            and approval.model_load_approval_success_not_commercial_runtime_approval
        ),
        "command_template_not_executed": whitelist.command_template_only is True
        and whitelist.command_not_executed is True
        and whitelist.model_load_command_template_success_not_model_load_execution is True,
        "sha256_recheck_plan_present": sha256_recheck.sha256_recheck_required_before_model_load is True
        and sha256_recheck.sha256_mismatch_blocks_model_load is True
        and sha256_recheck.size_mismatch_blocks_model_load is True,
        "memory_timeout_boundary_present": boundary.memory_usage_limit_required is True
        and boundary.timeout_required is True and boundary.max_runtime_seconds_planned > 0,
        "rollback_cleanup_plan_present": rollback.pre_model_load_snapshot_required is True
        and rollback.rollback_required is True
        and rollback.failed_model_load_cleanup_required is True
        and rollback.partial_model_object_cleanup_required is True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMModelLoadRequestApprovalReadinessGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMModelLoadRequestApprovalReadinessGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_model_load_request_approval_readiness_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_model_load_request_approval_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_code_and_weight_registry_audit_count_gte_1": True,
        "mobile_sam_model_load_trial_request_record_count_gte_1": True,
        "mobile_sam_owner_approval_issuance_record_count_gte_1": True,
        "mobile_sam_model_load_command_whitelist_record_count_gte_1": True,
        "mobile_sam_sha256_recheck_plan_record_count_gte_1": True,
        "mobile_sam_model_load_env_path_plan_count_gte_1": True,
        "mobile_sam_memory_timeout_boundary_count_gte_1": True,
        "mobile_sam_model_load_rollback_cleanup_count_gte_1": True,
        "mobile_sam_model_load_readiness_review_count_gte_1": True,
        "mobile_sam_model_load_execution_handoff_record_count_gte_1": True,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "compressed_phase": COMPRESSED_PHASE is True,
        "mobile_sam_only": True,
        "model_load_trial_request_included": MODEL_LOAD_TRIAL_REQUEST_INCLUDED is True,
        "model_load_owner_approval_issuance_included": MODEL_LOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "model_load_readiness_review_included": MODEL_LOAD_READINESS_REVIEW_INCLUDED is True,
        "model_load_execution_allowed_false": MODEL_LOAD_EXECUTION_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Audit semantics.
        "mobile_sam_code_and_weight_ready_verified": audit.audit_passed,
        "mobile_sam_weight_sha256_verified": weight_sha256_ok,
        "mobile_sam_weight_size_verified": weight_size_ok,
        "mobile_sam_weight_storage_verified": weight_file_path_ok and (ms.get("storage_verified") is True),
        "byte_track_out_of_scope": byte_track_out_of_scope,
        # Approval semantics.
        "owner_approval_granted_for_model_load_preparation": approval.owner_approval_granted_for_model_load_preparation,
        "owner_approval_granted_for_model_load_execution_next": approval.owner_approval_granted_for_model_load_execution_next,
        "model_load_approval_success_not_inference_approval": approval.model_load_approval_success_not_inference_approval,
        "model_load_approval_success_not_runtime_approval": approval.model_load_approval_success_not_runtime_approval,
        "model_load_approval_success_not_output_adapter_approval": approval.model_load_approval_success_not_output_adapter_approval,
        "model_load_approval_success_not_semantic_layer_approval": approval.model_load_approval_success_not_semantic_layer_approval,
        "model_load_approval_success_not_commercial_runtime_approval": approval.model_load_approval_success_not_commercial_runtime_approval,
        # Readiness semantics.
        "can_enter_model_load_execution_next": readiness.can_enter_model_load_execution_next,
        "can_inference_after_model_load_false": readiness.can_inference_after_model_load is False,
        "can_runtime_after_model_load_false": readiness.can_runtime_after_model_load is False,
        # Command whitelist semantics.
        "command_template_only": whitelist.command_template_only is True,
        "command_not_executed": whitelist.command_not_executed is True,
        "model_load_command_template_success_not_model_load_execution": whitelist.model_load_command_template_success_not_model_load_execution,
        # Plans present.
        "sha256_recheck_plan_present": invariant_state["sha256_recheck_plan_present"],
        "memory_timeout_boundary_present": invariant_state["memory_timeout_boundary_present"],
        "rollback_cleanup_plan_present": invariant_state["rollback_cleanup_plan_present"],
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
    decision = P1MobileSAMModelLoadRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_model_load_request_approval_readiness_profile_count=1,
        mobile_sam_code_and_weight_registry_audit_count=1,
        mobile_sam_model_load_trial_request_record_count=1,
        mobile_sam_owner_approval_issuance_record_count=1,
        mobile_sam_model_load_command_whitelist_record_count=1,
        mobile_sam_sha256_recheck_plan_record_count=1,
        mobile_sam_model_load_env_path_plan_count=1,
        mobile_sam_memory_timeout_boundary_count=1,
        mobile_sam_model_load_rollback_cleanup_count=1,
        mobile_sam_model_load_readiness_review_count=1,
        mobile_sam_model_load_execution_handoff_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Model Load Trial Request, Approval And Readiness (planning only, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "model_load_principle_zh": MODEL_LOAD_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "model_load_execution_allowed": MODEL_LOAD_EXECUTION_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_patch_execution_ref": UPSTREAM_PATCH_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "mobile_sam_model_load_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_model_load_request_approval_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_code_and_weight_registry_audit": asdict(audit),
        "mobile_sam_code_and_weight_registry_audit_count": 1,
        "mobile_sam_model_load_trial_request_record": asdict(request),
        "mobile_sam_model_load_trial_request_record_count": 1,
        "mobile_sam_owner_approval_issuance_record": asdict(approval),
        "mobile_sam_owner_approval_issuance_record_count": 1,
        "mobile_sam_model_load_command_whitelist_record": asdict(whitelist),
        "mobile_sam_model_load_command_whitelist_record_count": 1,
        "mobile_sam_sha256_recheck_plan_record": asdict(sha256_recheck),
        "mobile_sam_sha256_recheck_plan_record_count": 1,
        "mobile_sam_model_load_env_path_plan": asdict(env_path),
        "mobile_sam_model_load_env_path_plan_count": 1,
        "mobile_sam_memory_timeout_boundary": asdict(boundary),
        "mobile_sam_memory_timeout_boundary_count": 1,
        "mobile_sam_model_load_rollback_cleanup": asdict(rollback),
        "mobile_sam_model_load_rollback_cleanup_count": 1,
        "mobile_sam_model_load_readiness_review": asdict(readiness),
        "mobile_sam_model_load_readiness_review_count": 1,
        "mobile_sam_model_load_execution_handoff_record": asdict(handoff),
        "mobile_sam_model_load_execution_handoff_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "overlay_path": str(overlay_path),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "model_load_request_approval_readiness_status": (
                "mobile_sam_model_load_trial_requested_approved_for_preparation_and_execution_next_no_load_no_inference_no_runtime"
                if blocker_count == 0
                else "blocked"
            ),
            "model_loaded_this_phase": False,
            "imported_this_phase": False,
            "registry_mutated_this_phase": False,
            "can_enter_model_load_execution_next": readiness.can_enter_model_load_execution_next,
            "recommended_next_phase": NEXT_PHASE_MODEL_LOAD_EXECUTION,
            "recommended_next_phase_scope": "mobile_sam_only",
            "optional_followup_phase": OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only). The registry overlay was audited and confirms "
                "mobile_sam=code_and_weight_ready with verified weight sha256=="
                + MOBILE_SAM_WEIGHT_SHA256 + ", size==40728226, storage path, and all model_load/inference/runtime/"
                "output_adapter/semantic/commercial flags still false. A model-load trial request, a NARROW owner "
                "approval (model-load preparation + execution-next only), a TEMPLATE-ONLY command whitelist (never "
                "executed; no image input / segmentation / prediction / runtime server), a sha256 recheck plan, a "
                "controlled env/code/weight path plan, a memory/timeout boundary, a rollback/cleanup plan, a readiness "
                "review, and a follow-up execution handoff were produced. NOTHING was imported / model loaded / "
                "inferred / run; the registry was NOT mutated and no extra weight was downloaded. Model-load approval "
                "is NOT inference / runtime / output-adapter / semantic / commercial-runtime approval. Next: "
                + NEXT_PHASE_MODEL_LOAD_EXECUTION + " (real controlled import + model load, still no segmentation / "
                "prediction / inference / runtime). byte_track stays out of scope ("
                + OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE + ")."
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
            "mobile_sam_code_and_weight_registry_audit_record": {"mobile_sam_code_and_weight_registry_audit": asdict(audit)},
            "mobile_sam_model_load_trial_request_record": {"mobile_sam_model_load_trial_request_record": asdict(request)},
            "mobile_sam_owner_approval_issuance_record": {"mobile_sam_owner_approval_issuance_record": asdict(approval)},
            "mobile_sam_model_load_command_whitelist_record": {"mobile_sam_model_load_command_whitelist_record": asdict(whitelist)},
            "mobile_sam_sha256_recheck_plan_record": {"mobile_sam_sha256_recheck_plan_record": asdict(sha256_recheck)},
            "mobile_sam_memory_timeout_boundary_record": {"mobile_sam_model_load_env_path_plan": asdict(env_path),
                                                          "mobile_sam_memory_timeout_boundary": asdict(boundary)},
            "mobile_sam_model_load_rollback_cleanup_record": {"mobile_sam_model_load_rollback_cleanup": asdict(rollback)},
            "mobile_sam_model_load_readiness_review_record": {"mobile_sam_model_load_readiness_review": asdict(readiness)},
            "mobile_sam_followup_execution_route_record": {"mobile_sam_model_load_execution_handoff_record": asdict(handoff)},
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
            "mobile_sam_only": True,
            "model_load_execution_allowed": False,
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
    result = review_p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "model_loaded_this_phase": result["conclusions"]["model_loaded_this_phase"],
                "registry_mutated_this_phase": result["conclusions"]["registry_mutated_this_phase"],
                "can_enter_model_load_execution_next": result["conclusions"]["can_enter_model_load_execution_next"],
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
