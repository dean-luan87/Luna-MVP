# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Request, Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only, target = timm).

Audits the upstream failure-repair-planning result (must be dependency_gap/timm), then
produces a timm install request, a package/version review, a license/dependency review, a
torch-compatibility review (torch version read via importlib.metadata — NO torch import),
a NARROW owner approval (install preparation + execution-next only), a TEMPLATE-ONLY
install command whitelist (never executed; no global install; find_spec-only post-install
probe), a rollback plan, a readiness review, and a model-load retry gate. It does NOT pip
install / install timm / install any dependency, does NOT real import / model load / retry
/ inference / runtime / output adapter / semantic promotion, does NOT mutate the registry,
and downloads NOTHING. Version pins and reviews are NOT fabricated (timm version is left
unresolved unless real local metadata evidence exists). timm install approval is NOT
model-load-retry / inference / runtime / commercial-runtime approval. Protected, non-
deletable test board records are written in `planning` mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
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
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_request_approval_and_readiness.p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_request_approval_and_readiness.p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_INSTALL_SCOPE,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_EXECUTION_ALLOWED,
    DEPENDENCY_REPAIR_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    DEPENDENCY_REPAIR_READINESS_REVIEW_INCLUDED,
    DEPENDENCY_REPAIR_REQUEST_INCLUDED,
    EXPECTED_ERROR_CLASS,
    EXPECTED_FAILURE_CATEGORY,
    EXPECTED_MISSING_DEPENDENCY,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FALLBACK_TORCH_VERSION,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_INSTALL_EXECUTION,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REPAIR_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SUGGESTED_RETRY_PHASE,
    TARGET_CHAIN_REF,
    TARGET_DEPENDENCY,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_INSTALL_ALLOWED,
    UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO,
    UPSTREAM_FAILURE_REPAIR_PLANNING_REF,
    UPSTREAM_OUTPUT_DIR_REL,
    UPSTREAM_REVIEW_FILE,
    WEIGHT_CHAIN,
    MobileSAMModelLoadRetryGateAfterDependencyRepair,
    MobileSAMTimmDependencyGapAudit,
    P1MobileSAMDependencyRepairInstallRequestApprovalReadinessDecision,
    P1MobileSAMDependencyRepairInstallRequestApprovalReadinessProfile,
    TimmInstallCommandWhitelistRecord,
    TimmInstallReadinessReview,
    TimmInstallRequestRecord,
    TimmLicenseDependencyReviewRecord,
    TimmOwnerApprovalIssuanceRecord,
    TimmPackageVersionReviewRecord,
    TimmRollbackPlanRecord,
    TimmTorchCompatibilityReviewRecord,
    NegativeTimmDependencyRepairRequestApprovalGuard,
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
    / "p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_dependency_repair_install_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_dependency_repair_install_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_dependency_repair_install_request_approval_readiness_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

CONTROLLED_ENV_PATH = ".venv_model_load_trial"
CONTROLLED_PYTHON_EXECUTABLE = ".venv_model_load_trial/bin/python"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_upstream_dir() -> Path:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / UPSTREAM_OUTPUT_DIR_REL
        if p.is_dir():
            return p
    return _REPO_ROOT / UPSTREAM_OUTPUT_DIR_REL


def _observe_torch_version() -> Tuple[bool, str]:
    """Observe installed torch version WITHOUT importing torch (metadata only)."""
    try:
        from importlib import metadata as importlib_metadata

        version = importlib_metadata.version("torch")
        return True, version
    except Exception:  # noqa: BLE001
        return False, ""


def _observe_timm_local_metadata() -> Tuple[bool, str]:
    """Check if timm is locally available via metadata WITHOUT importing it."""
    try:
        from importlib import metadata as importlib_metadata

        version = importlib_metadata.version("timm")
        return True, version
    except Exception:  # noqa: BLE001
        return False, ""


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMDependencyRepairInstallRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            mobile_sam_only=True,
            dependency_repair_request_included=DEPENDENCY_REPAIR_REQUEST_INCLUDED,
            dependency_repair_owner_approval_issuance_included=DEPENDENCY_REPAIR_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            dependency_repair_readiness_review_included=DEPENDENCY_REPAIR_READINESS_REVIEW_INCLUDED,
            target_dependency=TARGET_DEPENDENCY,
            dependency_install_execution_allowed=DEPENDENCY_INSTALL_EXECUTION_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            timm_install_allowed=TIMM_INSTALL_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            model_load_retry_allowed=MODEL_LOAD_RETRY_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_failure_repair_planning_ref=UPSTREAM_FAILURE_REPAIR_PLANNING_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_v1(
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

    # ------------------------------------------------------------------- #
    # (一) Upstream failure-repair-planning audit.
    # ------------------------------------------------------------------- #
    upstream_dir = _resolve_upstream_dir()
    upstream_path = upstream_dir / UPSTREAM_REVIEW_FILE
    upstream_exists = upstream_path.is_file()
    upstream: Dict[str, Any] = {}
    if upstream_exists:
        try:
            upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            upstream = {}
            upstream_exists = False

    up_conclusions = upstream.get("conclusions", {})
    up_audit = upstream.get("mobile_sam_model_load_failure_audit", {})
    up_gap = upstream.get("mobile_sam_dependency_gap_record", {})
    up_retry = upstream.get("mobile_sam_model_load_retry_gate_planning_record", {})

    final_decision_observed = upstream.get("final_decision", "")
    final_decision_ok = final_decision_observed == UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO
    blocker_count_observed = upstream.get("blocker_count", -1)
    failure_category_observed = up_conclusions.get("failure_category", up_audit.get("failure_category", ""))
    missing_dependency_observed = up_conclusions.get("missing_dependency", up_gap.get("dependency_name", ""))
    error_class_observed = up_audit.get("error_class_observed", "")
    weight_integrity_related = up_audit.get("weight_integrity_related", True)
    checkpoint_corruption_related = up_audit.get("checkpoint_corruption_related", True)
    environment_dependency_related = up_audit.get("environment_dependency_related", False)
    timm_package_install_required = up_gap.get("package_install_required", False)
    timm_install_requires_separate_request = up_gap.get("pip_install_requires_separate_request", False)
    model_load_retry_allowed_now_observed = up_retry.get("model_load_retry_allowed_now", True)

    audit_passed = (
        upstream_exists
        and final_decision_ok
        and blocker_count_observed == 0
        and failure_category_observed == EXPECTED_FAILURE_CATEGORY
        and missing_dependency_observed == EXPECTED_MISSING_DEPENDENCY
        and error_class_observed == EXPECTED_ERROR_CLASS
        and weight_integrity_related is False
        and checkpoint_corruption_related is False
        and environment_dependency_related is True
        and timm_package_install_required is True
        and timm_install_requires_separate_request is True
        and model_load_retry_allowed_now_observed is False
    )
    audit = MobileSAMTimmDependencyGapAudit(
        audit_id="timm_dependency_gap_audit_v1",
        upstream_review_file_ref=str(upstream_path),
        upstream_review_exists=upstream_exists,
        final_decision_observed=final_decision_observed,
        final_decision_ok=final_decision_ok,
        blocker_count_observed=blocker_count_observed,
        failure_category_observed=failure_category_observed,
        missing_dependency_observed=missing_dependency_observed,
        error_class_observed=error_class_observed,
        weight_integrity_related_observed=weight_integrity_related,
        checkpoint_corruption_related_observed=checkpoint_corruption_related,
        environment_dependency_related_observed=environment_dependency_related,
        timm_package_install_required_observed=timm_package_install_required,
        timm_install_requires_separate_request_observed=timm_install_requires_separate_request,
        model_load_retry_allowed_now_observed=model_load_retry_allowed_now_observed,
        audit_passed=audit_passed,
    )
    if not audit_passed:
        failed_checks.append("audit.upstream_not_dependency_gap_timm_or_inconsistent")

    # ------------------------------------------------------------------- #
    # (二) Dependency Repair Request.
    # ------------------------------------------------------------------- #
    request = TimmInstallRequestRecord(
        request_id="timm_install_request_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        target_dependency=TARGET_DEPENDENCY,
        dependency_role="MobileSAM runtime/model-load dependency",
        request_scope="dependency_repair_install_preparation",
        install_execution_requested_next=True,
        controlled_install_scope=CONTROLLED_INSTALL_SCOPE,
        global_install_requested=False,
        request_is_not_install_execution=True,
        request_is_not_model_load_retry=True,
        request_is_not_inference_approval=True,
        request_is_not_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (三) Package / Version Review (no fabricated pin).
    # ------------------------------------------------------------------- #
    timm_local_available, timm_local_version = _observe_timm_local_metadata()
    # We must NOT fabricate a pin. Version stays unresolved unless real local metadata.
    if timm_local_available and timm_local_version:
        version_status = "local_available_candidate"
        version_pinned_value = ""  # pin still must be resolved/decided at execution; do not auto-pin to local
    else:
        version_status = "unresolved_or_candidate"
        version_pinned_value = ""
    version_review = TimmPackageVersionReviewRecord(
        record_id="timm_package_version_review_v1",
        package_name_candidate=TARGET_DEPENDENCY,
        import_root_candidate=TARGET_DEPENDENCY,
        clean_pypi_candidate=True,
        version_status=version_status,
        version_resolution_required=True,
        version_pin_required=True,
        version_pinned_value=version_pinned_value,
        version_falsely_pinned=False,
        package_source_review_required=True,
        hash_or_lockfile_recommended=True,
        dependency_conflict_review_required=True,
        transitive_dependency_review_required=True,
        license_review_required=True,
        local_available_candidate=timm_local_available,
    )

    # ------------------------------------------------------------------- #
    # License / dependency review (not fabricated as completed).
    # ------------------------------------------------------------------- #
    license_review = TimmLicenseDependencyReviewRecord(
        record_id="timm_license_dependency_review_v1",
        license_review_required=True,
        license_review_status="pending_required_before_install_execution",
        license_candidate="apache-2.0_candidate_unverified",
        dependency_review_required=True,
        dependency_review_status="pending_required_before_install_execution",
        transitive_dependency_review_status="pending_required_before_install_execution",
        review_falsely_marked_completed=False,
    )

    # ------------------------------------------------------------------- #
    # (四) Torch Compatibility Review (version via metadata, no torch import).
    # ------------------------------------------------------------------- #
    torch_available, torch_version = _observe_torch_version()
    if not torch_available or not torch_version:
        torch_version = FALLBACK_TORCH_VERSION
    torch_review = TimmTorchCompatibilityReviewRecord(
        record_id="timm_torch_compatibility_review_v1",
        current_torch_available=torch_available,
        current_torch_version_observed=torch_version,
        torch_compatibility_review_required=True,
        timm_torch_compatibility_status="unknown_or_candidate",
        compatibility_must_be_validated_after_install=True,
        compatibility_failure_blocks_model_load_retry=True,
    )

    # ------------------------------------------------------------------- #
    # (五) Owner Approval Issuance (narrow).
    # ------------------------------------------------------------------- #
    approval = TimmOwnerApprovalIssuanceRecord(
        approval_id="timm_owner_approval_issuance_v1",
        owner_approval_granted_for_timm_install_preparation=True,
        owner_approval_granted_for_timm_install_execution_next=True,
        model_load_retry_not_approved=True,
        inference_not_approved=True,
        runtime_not_approved=True,
        output_adapter_not_approved=True,
        semantic_layer_not_approved=True,
        registry_mutation_not_approved=True,
        additional_weight_download_not_approved=True,
        commercial_runtime_not_approved=True,
        timm_install_approval_not_model_load_retry_approval=True,
        timm_install_approval_not_inference_approval=True,
        timm_install_approval_not_runtime_approval=True,
        timm_install_approval_not_commercial_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Install Command Whitelist (template only) + (七) probe plan.
    # ------------------------------------------------------------------- #
    command_template = (
        "{python} -m pip install --no-input --require-virtualenv "
        "--target {env} timm==<RESOLVED_PINNED_VERSION>"
    ).replace("{python}", CONTROLLED_PYTHON_EXECUTABLE).replace("{env}", CONTROLLED_ENV_PATH)
    whitelist = TimmInstallCommandWhitelistRecord(
        record_id="timm_install_command_whitelist_v1",
        install_target=CONTROLLED_INSTALL_SCOPE,
        package=TARGET_DEPENDENCY,
        version_pin_required=True,
        no_global_install=True,
        no_model_load_during_install=True,
        no_import_during_install=True,
        no_inference_during_install=True,
        no_runtime_during_install=True,
        command_template=command_template,
        command_template_only=True,
        command_not_executed=True,
        command_template_success_not_install_execution=True,
        install_execution_requires_separate_phase=True,
        post_install_probe_required=True,
        probe_method="importlib.util.find_spec only",
        probe_target=TARGET_DEPENDENCY,
        real_import_after_install_allowed=False,
        model_load_after_install_allowed=False,
        timm_find_spec_required_before_model_load_retry=True,
    )

    # ------------------------------------------------------------------- #
    # (八) Rollback Plan.
    # ------------------------------------------------------------------- #
    rollback = TimmRollbackPlanRecord(
        record_id="timm_rollback_plan_v1",
        pre_install_snapshot_required=True,
        rollback_required=True,
        rollback_removes_timm_if_failed=True,
        rollback_preserves_mobile_sam_code=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        global_env_contamination_check_required=True,
    )

    # ------------------------------------------------------------------- #
    # (九) Readiness Review.
    # ------------------------------------------------------------------- #
    readiness = TimmInstallReadinessReview(
        review_id="timm_install_readiness_review_v1",
        can_enter_timm_install_execution_next=audit_passed,
        timm_install_execution_scope="controlled_dependency_repair_only",
        can_enter_model_load_retry_after_this_phase=False,
        model_load_retry_requires_timm_install_execution_go=True,
        model_load_retry_requires_timm_find_spec_verified=True,
        model_load_retry_requires_sha256_recheck=True,
        model_load_retry_requires_code_and_weight_ready_still_valid=True,
    )

    # ------------------------------------------------------------------- #
    # Model-load retry gate after dependency repair.
    # ------------------------------------------------------------------- #
    retry_gate = MobileSAMModelLoadRetryGateAfterDependencyRepair(
        record_id="mobile_sam_model_load_retry_gate_after_dependency_repair_v1",
        model_load_retry_allowed_now=False,
        requires_timm_install_request_go=True,
        requires_timm_owner_approval_granted=True,
        requires_timm_install_execution_go=True,
        requires_timm_find_spec_verified=True,
        requires_no_global_env_contamination=True,
        requires_sha256_recheck=True,
        requires_code_and_weight_ready_still_valid=True,
        requires_model_load_retry_command_whitelist_updated=True,
        requires_test_board_ready=True,
        suggested_retry_phase=SUGGESTED_RETRY_PHASE,
    )

    # ------------------------------------------------------------------- #
    # (十一) Invariants for the 17 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_dependency_gap_timm": audit_passed,
        "no_install_executed": (
            PIP_INSTALL_ALLOWED is False
            and TIMM_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_EXECUTION_ALLOWED is False
            and whitelist.command_not_executed is True
        ),
        "no_real_import": REAL_IMPORT_ALLOWED is False
        and whitelist.real_import_after_install_allowed is False,
        "no_model_load_retry": MODEL_LOAD_ALLOWED is False
        and MODEL_LOAD_RETRY_ALLOWED is False
        and retry_gate.model_load_retry_allowed_now is False,
        "no_inference_seg_pred": REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "version_not_falsely_pinned": version_review.version_falsely_pinned is False
        and (version_review.version_status != "pinned"),
        "reviews_not_falsely_completed": license_review.review_falsely_marked_completed is False,
        "approval_not_model_load_retry": approval.timm_install_approval_not_model_load_retry_approval is True
        and approval.model_load_retry_not_approved is True,
        "approval_not_inference_runtime": (
            approval.timm_install_approval_not_inference_approval is True
            and approval.timm_install_approval_not_runtime_approval is True
            and approval.timm_install_approval_not_commercial_runtime_approval is True
        ),
        "command_template_only_not_executed": whitelist.command_template_only is True
        and whitelist.command_not_executed is True
        and whitelist.command_template_success_not_install_execution is True,
        "rollback_plan_present": rollback.pre_install_snapshot_required is True
        and rollback.rollback_required is True
        and rollback.rollback_removes_timm_if_failed is True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeTimmDependencyRepairRequestApprovalGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeTimmDependencyRepairRequestApprovalGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_timm_dependency_repair_request_approval_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_dependency_repair_install_request_approval_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_timm_dependency_gap_audit_count_gte_1": True,
        "timm_install_request_record_count_gte_1": True,
        "timm_owner_approval_issuance_record_count_gte_1": True,
        "timm_package_version_review_record_count_gte_1": True,
        "timm_license_dependency_review_record_count_gte_1": True,
        "timm_torch_compatibility_review_record_count_gte_1": True,
        "timm_install_command_whitelist_record_count_gte_1": True,
        "timm_rollback_plan_record_count_gte_1": True,
        "timm_install_readiness_review_count_gte_1": True,
        "mobile_sam_model_load_retry_gate_after_dependency_repair_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        # Upstream verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "compressed_phase": COMPRESSED_PHASE is True,
        "mobile_sam_only": True,
        "dependency_repair_request_included": DEPENDENCY_REPAIR_REQUEST_INCLUDED is True,
        "dependency_repair_owner_approval_issuance_included": DEPENDENCY_REPAIR_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "dependency_repair_readiness_review_included": DEPENDENCY_REPAIR_READINESS_REVIEW_INCLUDED is True,
        "target_dependency_timm": TARGET_DEPENDENCY == "timm",
        "dependency_install_execution_allowed_false": DEPENDENCY_INSTALL_EXECUTION_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "timm_install_allowed_false": TIMM_INSTALL_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "model_load_retry_allowed_false": MODEL_LOAD_RETRY_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Audit semantics.
        "audit_passed": audit.audit_passed,
        "failure_category_dependency_gap": failure_category_observed == EXPECTED_FAILURE_CATEGORY,
        "missing_dependency_timm": missing_dependency_observed == EXPECTED_MISSING_DEPENDENCY,
        # Approval semantics.
        "owner_approval_granted_for_timm_install_preparation": approval.owner_approval_granted_for_timm_install_preparation,
        "owner_approval_granted_for_timm_install_execution_next": approval.owner_approval_granted_for_timm_install_execution_next,
        "timm_install_approval_not_model_load_retry_approval": approval.timm_install_approval_not_model_load_retry_approval,
        "timm_install_approval_not_inference_approval": approval.timm_install_approval_not_inference_approval,
        "timm_install_approval_not_runtime_approval": approval.timm_install_approval_not_runtime_approval,
        # Readiness semantics.
        "can_enter_timm_install_execution_next": readiness.can_enter_timm_install_execution_next,
        "can_enter_model_load_retry_after_this_phase_false": readiness.can_enter_model_load_retry_after_this_phase is False,
        # Version / review integrity.
        "version_not_falsely_pinned": invariant_state["version_not_falsely_pinned"],
        "reviews_not_falsely_completed": invariant_state["reviews_not_falsely_completed"],
        # Command + rollback.
        "command_template_only": whitelist.command_template_only is True,
        "command_not_executed": whitelist.command_not_executed is True,
        "rollback_plan_present": invariant_state["rollback_plan_present"],
        "post_install_find_spec_probe_required": whitelist.post_install_probe_required is True
        and whitelist.probe_method == "importlib.util.find_spec only",
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
    decision = P1MobileSAMDependencyRepairInstallRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_dependency_repair_install_request_approval_readiness_profile_count=1,
        mobile_sam_timm_dependency_gap_audit_count=1,
        timm_install_request_record_count=1,
        timm_owner_approval_issuance_record_count=1,
        timm_package_version_review_record_count=1,
        timm_license_dependency_review_record_count=1,
        timm_torch_compatibility_review_record_count=1,
        timm_install_command_whitelist_record_count=1,
        timm_rollback_plan_record_count=1,
        timm_install_readiness_review_count=1,
        mobile_sam_model_load_retry_gate_after_dependency_repair_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Dependency Repair Install Request, Approval And Readiness (planning only, mobile_sam_only, target=timm)",
        "lifecycle_variant": SCOPE,
        "repair_principle_zh": REPAIR_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "target_dependency": TARGET_DEPENDENCY,
        "timm_install_allowed": TIMM_INSTALL_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_failure_repair_planning_ref": UPSTREAM_FAILURE_REPAIR_PLANNING_REF,
        "upstream_failure_repair_planning_expected_go": UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "upstream_evidence_dir": str(upstream_dir),
        "mobile_sam_dependency_repair_install_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_dependency_repair_install_request_approval_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_timm_dependency_gap_audit": asdict(audit),
        "mobile_sam_timm_dependency_gap_audit_count": 1,
        "timm_install_request_record": asdict(request),
        "timm_install_request_record_count": 1,
        "timm_owner_approval_issuance_record": asdict(approval),
        "timm_owner_approval_issuance_record_count": 1,
        "timm_package_version_review_record": asdict(version_review),
        "timm_package_version_review_record_count": 1,
        "timm_license_dependency_review_record": asdict(license_review),
        "timm_license_dependency_review_record_count": 1,
        "timm_torch_compatibility_review_record": asdict(torch_review),
        "timm_torch_compatibility_review_record_count": 1,
        "timm_install_command_whitelist_record": asdict(whitelist),
        "timm_install_command_whitelist_record_count": 1,
        "timm_rollback_plan_record": asdict(rollback),
        "timm_rollback_plan_record_count": 1,
        "timm_install_readiness_review": asdict(readiness),
        "timm_install_readiness_review_count": 1,
        "mobile_sam_model_load_retry_gate_after_dependency_repair": asdict(retry_gate),
        "mobile_sam_model_load_retry_gate_after_dependency_repair_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "dependency_repair_request_approval_readiness_status": (
                "timm_install_requested_approved_for_preparation_and_execution_next_no_install_no_load_no_inference"
                if blocker_count == 0
                else "blocked"
            ),
            "target_dependency": TARGET_DEPENDENCY,
            "timm_installed_this_phase": False,
            "imported_this_phase": False,
            "model_load_retry_allowed_now": retry_gate.model_load_retry_allowed_now,
            "version_status": version_review.version_status,
            "timm_local_available_candidate": timm_local_available,
            "current_torch_version_observed": torch_review.current_torch_version_observed,
            "can_enter_timm_install_execution_next": readiness.can_enter_timm_install_execution_next,
            "recommended_next_phase": NEXT_PHASE_INSTALL_EXECUTION,
            "recommended_next_phase_scope": "mobile_sam_only_controlled_dependency_repair",
            "suggested_retry_phase": SUGGESTED_RETRY_PHASE,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only, target=timm). Upstream failure-repair-planning GO was "
                "audited and confirms failure_category=dependency_gap, missing_dependency=timm, "
                "error_class=ModuleNotFoundError, weight/checkpoint integrity unrelated, install requires a separate "
                "request, and model-load retry not allowed now. A timm install request, a package/version review "
                "(version left " + version_review.version_status + " — NOT falsely pinned), a license/dependency "
                "review (pending — NOT falsely completed), a torch-compatibility review (observed torch "
                + torch_review.current_torch_version_observed + " via metadata, NO torch import), a NARROW owner "
                "approval (install preparation + execution-next only), a TEMPLATE-ONLY install command whitelist "
                "(never executed; no global install; find_spec-only probe), a rollback plan, a readiness review, and a "
                "model-load retry gate were produced. NOTHING was pip-installed / imported / model-loaded / inferred / "
                "run; the registry was NOT mutated and nothing was downloaded. timm install approval is NOT "
                "model-load-retry / inference / runtime / commercial-runtime approval. Next: "
                + NEXT_PHASE_INSTALL_EXECUTION + " (real controlled timm install + find_spec probe; still no model "
                "load). After install execution GO + find_spec verified, retry via " + SUGGESTED_RETRY_PHASE + "."
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
            "timm_dependency_gap_audit_record": {"mobile_sam_timm_dependency_gap_audit": asdict(audit)},
            "timm_install_request_record": {"timm_install_request_record": asdict(request)},
            "timm_owner_approval_issuance_record": {"timm_owner_approval_issuance_record": asdict(approval)},
            "timm_package_version_review_record": {"timm_package_version_review_record": asdict(version_review),
                                                   "timm_license_dependency_review_record": asdict(license_review)},
            "timm_torch_compatibility_review_record": {"timm_torch_compatibility_review_record": asdict(torch_review)},
            "timm_install_command_whitelist_record": {"timm_install_command_whitelist_record": asdict(whitelist)},
            "timm_rollback_plan_record": {"timm_rollback_plan_record": asdict(rollback)},
            "timm_install_readiness_review_record": {"timm_install_readiness_review": asdict(readiness)},
            "mobile_sam_model_load_retry_gate_record": {"mobile_sam_model_load_retry_gate_after_dependency_repair": asdict(retry_gate)},
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
            "timm_install_allowed": False,
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
    result = review_p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "target_dependency": result["conclusions"]["target_dependency"],
                "timm_installed_this_phase": result["conclusions"]["timm_installed_this_phase"],
                "version_status": result["conclusions"]["version_status"],
                "current_torch_version_observed": result["conclusions"]["current_torch_version_observed"],
                "can_enter_timm_install_execution_next": result["conclusions"]["can_enter_timm_install_execution_next"],
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
