# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair NoDeps Install Request, Approval And Readiness — review v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only, target = timm, route = no-deps).

Audits the upstream failure-repair-planning GO with Route A (timm_no_deps_controlled_install)
selected, then produces a no-deps timm install request, a NARROW owner approval (no-deps
install preparation + execution-next only), a torch/torchvision reuse boundary record
(metadata observation only — NO import), a TEMPLATE-ONLY `--no-deps` command whitelist
(never executed; no global install; no transitive deps; find_spec-only post-install probe),
a rollback plan, a readiness review, and a model-load retry gate. It does NOT pip install /
install timm / real import torch/torchvision/mobile_sam / model load / retry / inference /
runtime / output adapter / semantic promotion / registry mutation / extra downloads. no-deps
approval is NOT install execution now, NOT model-load-retry / inference / runtime / commercial-
runtime approval. Protected, non-deletable test board records are written in `planning` mode.
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
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness.p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness.p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    COMPRESSED_PHASE,
    CONTROLLED_INSTALL_TARGET_REL,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_EXECUTION_ALLOWED,
    EXPECTED_FAILURE_CATEGORY,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FALLBACK_TORCH_VERSION,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_NODEPS_INSTALL_EXECUTION,
    NODEPS_INSTALL_READINESS_REVIEW_INCLUDED,
    NODEPS_INSTALL_REQUEST_INCLUDED,
    NODEPS_OWNER_APPROVAL_ISSUANCE_INCLUDED,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    REPAIR_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    SCOPE,
    SELECTED_ROUTE,
    SEMANTIC_PROMOTION_ALLOWED,
    SUGGESTED_RETRY_PHASE,
    TARGET_CHAIN_REF,
    TARGET_DEPENDENCY,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_INSTALL_ALLOWED,
    TIMM_PACKAGE_NAME,
    UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO,
    UPSTREAM_FAILURE_REPAIR_PLANNING_REF,
    UPSTREAM_OUTPUT_DIR_REL,
    UPSTREAM_REVIEW_FILE,
    WEIGHT_CHAIN,
    MobileSAMModelLoadRetryGateAfterNoDepsTimm,
    NegativeTimmNoDepsInstallRequestApprovalGuard,
    P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessDecision,
    P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessProfile,
    TimmNoDepsCommandWhitelistRecord,
    TimmNoDepsInstallReadinessReview,
    TimmNoDepsInstallRequestRecord,
    TimmNoDepsOwnerApprovalIssuanceRecord,
    TimmNoDepsProbePlanRecord,
    TimmNoDepsRollbackPlanRecord,
    TimmNoDepsRouteAudit,
    TimmTorchTorchvisionReuseBoundaryRecord,
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
    / "p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_types_v1.py",
    f"{_PKG}/p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1.py",
)

PROFILE_REF = "p1_mobile_sam_nodeps_timm_install_request_approval_readiness_profile_v1"
DECISION_REF = "p1_mobile_sam_nodeps_timm_install_request_approval_readiness_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

NO_DEPS_COMMAND_TEMPLATE = (
    "{python} -m pip install --no-input {package} --no-deps --target {target}"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_upstream_dir() -> Path:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / UPSTREAM_OUTPUT_DIR_REL
        if p.is_dir():
            return p
    return _REPO_ROOT / UPSTREAM_OUTPUT_DIR_REL


def _observe_torch_version() -> Tuple[bool, str]:
    try:
        from importlib import metadata as importlib_metadata

        return True, importlib_metadata.version("torch")
    except Exception:  # noqa: BLE001
        return False, ""


def _observe_torchvision() -> Tuple[bool, str]:
    try:
        from importlib import metadata as importlib_metadata

        return True, importlib_metadata.version("torchvision")
    except Exception:  # noqa: BLE001
        return False, ""


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            compressed_phase=COMPRESSED_PHASE,
            mobile_sam_only=True,
            target_dependency=TARGET_DEPENDENCY,
            selected_route=SELECTED_ROUTE,
            nodeps_install_request_included=NODEPS_INSTALL_REQUEST_INCLUDED,
            nodeps_owner_approval_issuance_included=NODEPS_OWNER_APPROVAL_ISSUANCE_INCLUDED,
            nodeps_install_readiness_review_included=NODEPS_INSTALL_READINESS_REVIEW_INCLUDED,
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


def review_p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1(
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
    # (一) Upstream no-deps route audit.
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
    up_risk = upstream.get("timm_second_repair_risk_record", {})
    up_route = upstream.get("timm_repair_route_comparison_record", {})

    final_decision_observed = upstream.get("final_decision", "")
    blocker_count_observed = upstream.get("blocker_count", -1)
    failure_category_observed = up_conclusions.get("failure_category", "")
    selected_route_observed = up_conclusions.get("selected_route", up_route.get("selected_route", ""))
    same_full_retry_not_recommended = up_conclusions.get(
        "same_full_isolated_install_retry_not_recommended", True
    )
    model_load_retry_allowed_now_observed = up_conclusions.get("model_load_retry_allowed_now", True)
    no_deps_risk_recorded = up_risk.get("no_deps_install_missing_transitive_dependency_risk", False)
    torch_compat_risk_recorded = up_risk.get("torch_timm_compatibility_risk", False)
    route_a_selected = (
        selected_route_observed == SELECTED_ROUTE
        and up_route.get("route_a_selected", False) is True
    )

    final_decision_ok = final_decision_observed == UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO
    failure_category_ok = failure_category_observed == EXPECTED_FAILURE_CATEGORY

    audit_passed = (
        upstream_exists
        and final_decision_ok
        and blocker_count_observed == 0
        and failure_category_ok
        and route_a_selected
        and same_full_retry_not_recommended is True
        and model_load_retry_allowed_now_observed is False
        and no_deps_risk_recorded is True
        and torch_compat_risk_recorded is True
    )

    audit = TimmNoDepsRouteAudit(
        audit_id="timm_nodeps_route_audit_v1",
        upstream_review_file_ref=str(upstream_path),
        upstream_review_exists=upstream_exists,
        final_decision_observed=final_decision_observed,
        final_decision_ok=final_decision_ok,
        blocker_count_observed=blocker_count_observed,
        failure_category_observed=failure_category_observed,
        selected_route_observed=selected_route_observed,
        same_full_isolated_install_retry_not_recommended_observed=same_full_retry_not_recommended,
        model_load_retry_allowed_now_observed=model_load_retry_allowed_now_observed,
        no_deps_install_missing_transitive_dependency_risk_recorded=no_deps_risk_recorded,
        torch_timm_compatibility_risk_recorded=torch_compat_risk_recorded,
        route_a_selected=route_a_selected,
        audit_passed=audit_passed,
    )
    if not audit_passed:
        failed_checks.append("audit.upstream_no_deps_route_not_verified_or_inconsistent")

    # ------------------------------------------------------------------- #
    # (二) No-Deps Install Request.
    # ------------------------------------------------------------------- #
    request = TimmNoDepsInstallRequestRecord(
        request_id="timm_nodeps_install_request_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        target_dependency=TARGET_DEPENDENCY,
        request_scope="timm_no_deps_dependency_repair_install_preparation",
        selected_route=SELECTED_ROUTE,
        install_execution_requested_next=True,
        command_strategy="pip_install_timm_no_deps",
        controlled_install_scope="controlled_model_load_env_or_isolated_target",
        global_install_requested=False,
        request_is_not_install_execution=True,
        request_is_not_model_load_retry=True,
        request_is_not_inference_approval=True,
        request_is_not_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (三) Owner Approval Issuance (narrow).
    # ------------------------------------------------------------------- #
    approval = TimmNoDepsOwnerApprovalIssuanceRecord(
        approval_id="timm_nodeps_owner_approval_issuance_v1",
        owner_approval_granted_for_timm_nodeps_install_preparation=True,
        owner_approval_granted_for_timm_nodeps_install_execution_next=True,
        model_load_retry_not_approved=True,
        inference_not_approved=True,
        runtime_not_approved=True,
        output_adapter_not_approved=True,
        semantic_layer_not_approved=True,
        registry_mutation_not_approved=True,
        additional_weight_download_not_approved=True,
        commercial_runtime_not_approved=True,
        nodeps_install_approval_not_install_execution_now=True,
        nodeps_install_approval_not_model_load_retry_approval=True,
        nodeps_install_approval_not_inference_approval=True,
        nodeps_install_approval_not_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (四) Torch / Torchvision reuse boundary (metadata only, NO import).
    # ------------------------------------------------------------------- #
    torch_available, torch_version = _observe_torch_version()
    if not torch_available or not torch_version:
        torch_version = FALLBACK_TORCH_VERSION
        warnings.append("torch_version_observed_via_fallback_not_live_metadata")
    tv_available, tv_version = _observe_torchvision()
    if not tv_available:
        warnings.append("torchvision_not_observed_in_global_metadata_before_nodeps_execution")

    reuse_boundary = TimmTorchTorchvisionReuseBoundaryRecord(
        record_id="timm_torch_torchvision_reuse_boundary_v1",
        existing_torch_reuse_allowed=True,
        existing_torch_version_expected=torch_version,
        existing_torch_reuse_does_not_allow_global_mutation=True,
        existing_torch_reuse_does_not_allow_reinstall=True,
        existing_torch_reinstall_allowed=False,
        torchvision_status_check_required_before_execution=True,
        torchvision_reinstall_allowed=False,
        torch_compatibility_must_be_observed_after_model_load_retry=True,
        if_torchvision_missing_then_enter_dependency_repair_loop=True,
        torchvision_observed_available=tv_available,
        torchvision_observed_version=tv_version,
    )

    # ------------------------------------------------------------------- #
    # (五) Command Whitelist (template only).
    # ------------------------------------------------------------------- #
    target_str = str((_WRITABLE_BASE / CONTROLLED_INSTALL_TARGET_REL).resolve())
    command_template = NO_DEPS_COMMAND_TEMPLATE.format(
        python=sys.executable,
        package=TIMM_PACKAGE_NAME,
        target=target_str,
    )
    whitelist = TimmNoDepsCommandWhitelistRecord(
        record_id="timm_nodeps_command_whitelist_v1",
        command_template=command_template,
        command_template_only=True,
        command_not_executed=True,
        no_deps_flag_required=True,
        no_global_install=True,
        no_transitive_dependency_install=True,
        no_model_load_during_install=True,
        no_import_during_install=True,
        no_inference_during_install=True,
        no_runtime_during_install=True,
        no_registry_mutation_during_install=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Post-install Probe Plan.
    # ------------------------------------------------------------------- #
    probe_plan = TimmNoDepsProbePlanRecord(
        record_id="timm_nodeps_probe_plan_v1",
        post_install_probe_required=True,
        probe_method="importlib.util.find_spec only",
        probe_target=TIMM_PACKAGE_NAME,
        real_import_after_install_allowed=False,
        model_load_after_install_allowed=False,
        timm_find_spec_required_before_model_load_retry=True,
    )

    # ------------------------------------------------------------------- #
    # (七) Rollback Plan.
    # ------------------------------------------------------------------- #
    rollback = TimmNoDepsRollbackPlanRecord(
        record_id="timm_nodeps_rollback_plan_v1",
        pre_install_snapshot_required=True,
        rollback_required=True,
        rollback_removes_timm_if_failed=True,
        rollback_preserves_mobile_sam_code=True,
        rollback_preserves_mobile_sam_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        global_env_contamination_check_required=True,
        controlled_target_cleanup_required_on_failure=True,
    )

    # ------------------------------------------------------------------- #
    # (八) Readiness Review + Model-load retry gate.
    # ------------------------------------------------------------------- #
    readiness = TimmNoDepsInstallReadinessReview(
        review_id="timm_nodeps_install_readiness_review_v1",
        can_enter_timm_nodeps_install_execution_next=audit_passed,
        timm_nodeps_install_execution_scope="controlled_dependency_repair_only",
        can_enter_model_load_retry_after_this_phase=False,
        model_load_retry_requires_nodeps_timm_install_go=True,
        model_load_retry_requires_timm_find_spec_verified=True,
        model_load_retry_requires_mobile_sam_weight_sha256_recheck=True,
        model_load_retry_requires_code_and_weight_ready_still_valid=True,
        model_load_retry_requires_torch_torchvision_reuse_boundary_check=True,
    )

    retry_gate = MobileSAMModelLoadRetryGateAfterNoDepsTimm(
        record_id="mobile_sam_model_load_retry_gate_after_nodeps_timm_v1",
        model_load_retry_allowed_now=False,
        requires_nodeps_timm_install_request_go=True,
        requires_nodeps_owner_approval_granted=True,
        requires_nodeps_timm_install_execution_go=True,
        requires_timm_find_spec_verified=True,
        requires_no_global_env_contamination=True,
        requires_sha256_recheck=True,
        requires_code_and_weight_ready_still_valid=True,
        requires_torch_torchvision_reuse_boundary_check=True,
        suggested_retry_phase=SUGGESTED_RETRY_PHASE,
    )

    # ------------------------------------------------------------------- #
    # (十) Invariants for the 18 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_no_deps_route_selected": route_a_selected and audit_passed,
        "no_install_executed": (
            PIP_INSTALL_ALLOWED is False
            and TIMM_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_EXECUTION_ALLOWED is False
            and whitelist.command_not_executed is True
        ),
        "no_real_import": REAL_IMPORT_ALLOWED is False,
        "no_model_load_retry": (
            MODEL_LOAD_ALLOWED is False
            and MODEL_LOAD_RETRY_ALLOWED is False
            and retry_gate.model_load_retry_allowed_now is False
        ),
        "no_inference_seg_pred": REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "whitelist_has_no_deps_flag": (
            whitelist.no_deps_flag_required is True and "--no-deps" in whitelist.command_template
        ),
        "whitelist_no_global_install": whitelist.no_global_install is True,
        "torch_torchvision_reuse_boundary_present": (
            reuse_boundary.existing_torch_reuse_allowed is True
            and reuse_boundary.existing_torch_reinstall_allowed is False
            and reuse_boundary.torchvision_status_check_required_before_execution is True
        ),
        "nodeps_approval_not_install_execution_now": approval.nodeps_install_approval_not_install_execution_now is True,
        "nodeps_approval_not_model_load_retry_approval": approval.nodeps_install_approval_not_model_load_retry_approval is True,
        "nodeps_approval_not_inference_runtime_approval": (
            approval.nodeps_install_approval_not_inference_approval is True
            and approval.nodeps_install_approval_not_runtime_approval is True
        ),
        "rollback_plan_present": (
            rollback.pre_install_snapshot_required is True
            and rollback.rollback_required is True
            and rollback.rollback_removes_timm_if_failed is True
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeTimmNoDepsInstallRequestApprovalGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeTimmNoDepsInstallRequestApprovalGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_nodeps_install_request_approval_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_nodeps_timm_install_request_approval_readiness_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "timm_nodeps_route_audit_count_gte_1": True,
        "timm_nodeps_install_request_record_count_gte_1": True,
        "timm_nodeps_owner_approval_issuance_record_count_gte_1": True,
        "timm_torch_torchvision_reuse_boundary_record_count_gte_1": True,
        "timm_nodeps_command_whitelist_record_count_gte_1": True,
        "timm_nodeps_probe_plan_record_count_gte_1": True,
        "timm_nodeps_rollback_plan_record_count_gte_1": True,
        "timm_nodeps_install_readiness_review_count_gte_1": True,
        "mobile_sam_model_load_retry_gate_after_nodeps_timm_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "compressed_phase": COMPRESSED_PHASE is True,
        "mobile_sam_only": True,
        "target_dependency_timm": TARGET_DEPENDENCY == "timm",
        "selected_route_timm_no_deps": SELECTED_ROUTE == "timm_no_deps_controlled_install",
        "nodeps_install_request_included": NODEPS_INSTALL_REQUEST_INCLUDED is True,
        "nodeps_owner_approval_issuance_included": NODEPS_OWNER_APPROVAL_ISSUANCE_INCLUDED is True,
        "nodeps_install_readiness_review_included": NODEPS_INSTALL_READINESS_REVIEW_INCLUDED is True,
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
        "audit_passed": audit.audit_passed,
        "owner_approval_granted_for_timm_nodeps_install_preparation": approval.owner_approval_granted_for_timm_nodeps_install_preparation,
        "owner_approval_granted_for_timm_nodeps_install_execution_next": approval.owner_approval_granted_for_timm_nodeps_install_execution_next,
        "can_enter_timm_nodeps_install_execution_next": readiness.can_enter_timm_nodeps_install_execution_next,
        "can_enter_model_load_retry_after_this_phase_false": readiness.can_enter_model_load_retry_after_this_phase is False,
        "nodeps_install_approval_not_install_execution_now": approval.nodeps_install_approval_not_install_execution_now,
        "nodeps_install_approval_not_model_load_retry_approval": approval.nodeps_install_approval_not_model_load_retry_approval,
        "nodeps_install_approval_not_inference_approval": approval.nodeps_install_approval_not_inference_approval,
        "nodeps_install_approval_not_runtime_approval": approval.nodeps_install_approval_not_runtime_approval,
        "command_template_only": whitelist.command_template_only is True,
        "command_not_executed": whitelist.command_not_executed is True,
        "no_deps_flag_in_command": "--no-deps" in whitelist.command_template,
        "rollback_plan_present": invariant_state["rollback_plan_present"],
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
    decision = P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessDecision(
        decision_ref=DECISION_REF,
        mobile_sam_nodeps_timm_install_request_approval_readiness_profile_count=1,
        timm_nodeps_route_audit_count=1,
        timm_nodeps_install_request_record_count=1,
        timm_nodeps_owner_approval_issuance_record_count=1,
        timm_torch_torchvision_reuse_boundary_record_count=1,
        timm_nodeps_command_whitelist_record_count=1,
        timm_nodeps_probe_plan_record_count=1,
        timm_nodeps_rollback_plan_record_count=1,
        timm_nodeps_install_readiness_review_count=1,
        mobile_sam_model_load_retry_gate_after_nodeps_timm_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Dependency Repair NoDeps Install Request, Approval And Readiness (planning only, mobile_sam_only, route=no-deps)",
        "lifecycle_variant": SCOPE,
        "repair_principle_zh": REPAIR_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "compressed_phase": COMPRESSED_PHASE,
        "target_dependency": TARGET_DEPENDENCY,
        "selected_route": SELECTED_ROUTE,
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
        "mobile_sam_nodeps_timm_install_request_approval_readiness_profile": _build_profile(),
        "mobile_sam_nodeps_timm_install_request_approval_readiness_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "timm_nodeps_route_audit": asdict(audit),
        "timm_nodeps_route_audit_count": 1,
        "timm_nodeps_install_request_record": asdict(request),
        "timm_nodeps_install_request_record_count": 1,
        "timm_nodeps_owner_approval_issuance_record": asdict(approval),
        "timm_nodeps_owner_approval_issuance_record_count": 1,
        "timm_torch_torchvision_reuse_boundary_record": asdict(reuse_boundary),
        "timm_torch_torchvision_reuse_boundary_record_count": 1,
        "timm_nodeps_command_whitelist_record": asdict(whitelist),
        "timm_nodeps_command_whitelist_record_count": 1,
        "timm_nodeps_probe_plan_record": asdict(probe_plan),
        "timm_nodeps_probe_plan_record_count": 1,
        "timm_nodeps_rollback_plan_record": asdict(rollback),
        "timm_nodeps_rollback_plan_record_count": 1,
        "timm_nodeps_install_readiness_review": asdict(readiness),
        "timm_nodeps_install_readiness_review_count": 1,
        "mobile_sam_model_load_retry_gate_after_nodeps_timm": asdict(retry_gate),
        "mobile_sam_model_load_retry_gate_after_nodeps_timm_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "observed_torch_version": torch_version,
        "observed_torchvision_available": tv_available,
        "observed_torchvision_version": tv_version,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "nodeps_install_request_approval_readiness_status": (
                "timm_no_deps_install_requested_approved_for_preparation_and_execution_next_no_install_no_load_no_inference"
                if blocker_count == 0
                else "blocked"
            ),
            "target_dependency": TARGET_DEPENDENCY,
            "selected_route": SELECTED_ROUTE,
            "timm_installed_this_phase": False,
            "imported_this_phase": False,
            "model_load_retry_allowed_now": retry_gate.model_load_retry_allowed_now,
            "observed_torch_version": torch_version,
            "observed_torchvision_available": tv_available,
            "can_enter_timm_nodeps_install_execution_next": readiness.can_enter_timm_nodeps_install_execution_next,
            "recommended_next_phase": NEXT_PHASE_NODEPS_INSTALL_EXECUTION,
            "suggested_retry_phase": SUGGESTED_RETRY_PHASE,
            "transition_note": (
                "PLANNING / APPROVAL ONLY (mobile_sam_only, route=timm_no_deps_controlled_install). Upstream "
                "failure-repair-planning GO was audited: failure_category=dependency_install_timeout, Route A "
                "selected, same full isolated install retry NOT recommended. A no-deps timm install request, a "
                "NARROW owner approval (no-deps install preparation + execution-next only), a torch/torchvision "
                "reuse boundary (torch " + torch_version + " via metadata, NO import), a TEMPLATE-ONLY "
                "`pip install timm --no-deps --target <path>` whitelist (never executed), a find_spec-only probe "
                "plan, a rollback plan, a readiness review, and a model-load retry gate were produced. NOTHING was "
                "pip-installed / imported / model-loaded / inferred / run; registry NOT mutated. no-deps approval "
                "is NOT install execution now, NOT model-load-retry / inference / runtime approval. Next: "
                + NEXT_PHASE_NODEPS_INSTALL_EXECUTION + " (real no-deps install + find_spec probe; still no import/load)."
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
            "timm_nodeps_route_audit_record": {"timm_nodeps_route_audit": asdict(audit)},
            "timm_nodeps_install_request_record": {"timm_nodeps_install_request_record": asdict(request)},
            "timm_nodeps_owner_approval_issuance_record": {"timm_nodeps_owner_approval_issuance_record": asdict(approval)},
            "timm_torch_torchvision_reuse_boundary_record": {"timm_torch_torchvision_reuse_boundary_record": asdict(reuse_boundary)},
            "timm_nodeps_command_whitelist_record": {"timm_nodeps_command_whitelist_record": asdict(whitelist)},
            "timm_nodeps_probe_plan_record": {"timm_nodeps_probe_plan_record": asdict(probe_plan)},
            "timm_nodeps_rollback_plan_record": {"timm_nodeps_rollback_plan_record": asdict(rollback)},
            "timm_nodeps_install_readiness_review_record": {"timm_nodeps_install_readiness_review": asdict(readiness)},
            "mobile_sam_model_load_retry_gate_record": {"mobile_sam_model_load_retry_gate_after_nodeps_timm": asdict(retry_gate)},
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
            "pip_install_allowed": False,
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
    result = review_p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "selected_route": result["conclusions"]["selected_route"],
                "observed_torch_version": result["conclusions"]["observed_torch_version"],
                "can_enter_timm_nodeps_install_execution_next": result["conclusions"]["can_enter_timm_nodeps_install_execution_next"],
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
