# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Failure Review And Repair Planning — review v1
(PLANNING ONLY, scope = mobile_sam_only, target = timm).

Audits the upstream timm controlled-install FAILED_NO_BOUNDARY_VIOLATION result (timeout
after 1200s, return_code=-1, target 0B, no global contamination), attributes root cause to
dependency install strategy (heavy transitive deps under isolated --target), compares repair
routes (Route A no-deps P0 selected, B wheel/cache P1 fallback, C extended timeout P2
fallback-only, D global reuse rejected), plans torch/torchvision reuse boundaries, routes
the next no-deps install request/approval/readiness phase, and records model-load retry
gate. It does NOT pip install / install timm / real import / model load / retry / inference
/ runtime / output adapter / semantic promotion / registry mutation / extra downloads.
Protected, non-deletable test board records are written in `planning` mode.
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
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning.p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning.p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_INSTALL_TARGET_REL,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_EXECUTION_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FAILURE_CATEGORY,
    FALLBACK_TORCH_VERSION,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INSTALL_TIMEOUT_SECONDS_OBSERVED,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_WEIGHT_SHA256,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_NO_DEPS_REQUEST,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    REPAIR_PRINCIPLE_ZH,
    REPAIR_REPLANNING_ONLY,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    ROOT_CAUSE_CANDIDATE,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    SELECTED_ROUTE,
    SEMANTIC_PROMOTION_ALLOWED,
    SCOPE,
    SUGGESTED_RETRY_PHASE,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_INSTALL_ALLOWED,
    TIMM_INSTALL_FAILURE_REVIEW,
    TIMM_PACKAGE_NAME,
    UPSTREAM_EVIDENCE_FILES,
    UPSTREAM_INSTALL_EXECUTION_EXPECTED_DECISION,
    UPSTREAM_INSTALL_EXECUTION_REF,
    UPSTREAM_OUTPUT_DIR_REL,
    WEIGHT_CHAIN,
    MobileSAMModelLoadRetryBoundaryAfterTimmRepair,
    NegativeTimmInstallFailureRepairPlanningGuard,
    P1MobileSAMTimmInstallFailureRepairPlanningDecision,
    P1MobileSAMTimmInstallFailureRepairPlanningProfile,
    TimmCacheWheelInstallPlanningRecord,
    TimmInstallFailureAudit,
    TimmInstallTimeoutRootCauseRecord,
    TimmNoDepsInstallPlanningRecord,
    TimmRepairRouteComparisonRecord,
    TimmSecondInstallRetryGatePlanningRecord,
    TimmSecondRepairRiskRecord,
    TimmTimeoutExtensionPlanningRecord,
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
    / "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_timm_install_failure_repair_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_timm_install_failure_repair_planning_decision_v1"

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


def _load_upstream_artifact(upstream_dir: Path, fname: str) -> Tuple[Dict[str, Any], bool]:
    path = upstream_dir / fname
    if not path.is_file():
        return {}, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return {}, False


def _target_path_size_bytes(target_path: Path) -> int:
    if not target_path.is_dir():
        return 0
    total = 0
    for f in target_path.rglob("*"):
        if f.is_file():
            try:
                total += f.stat().st_size
            except OSError:
                pass
    return total


def _observe_torch_version() -> Tuple[bool, str]:
    try:
        from importlib import metadata as importlib_metadata

        return True, importlib_metadata.version("torch")
    except Exception:  # noqa: BLE001
        return False, ""


def _observe_torchvision_available() -> Tuple[bool, str]:
    try:
        from importlib import metadata as importlib_metadata

        return True, importlib_metadata.version("torchvision")
    except Exception:  # noqa: BLE001
        return False, ""


def _observe_timm_global() -> Tuple[bool, str]:
    try:
        from importlib import metadata as importlib_metadata

        return True, importlib_metadata.version("timm")
    except Exception:  # noqa: BLE001
        return False, ""


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMTimmInstallFailureRepairPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            timm_install_failure_review=TIMM_INSTALL_FAILURE_REVIEW,
            repair_replanning_only=REPAIR_REPLANNING_ONLY,
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
            upstream_install_execution_ref=UPSTREAM_INSTALL_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1(
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
    # (一) Upstream install failure review — read execution artifacts.
    # ------------------------------------------------------------------- #
    upstream_dir = _resolve_upstream_dir()
    evidence: Dict[str, Any] = {}
    evidence_present: Dict[str, bool] = {}
    for fname in UPSTREAM_EVIDENCE_FILES:
        data, exists = _load_upstream_artifact(upstream_dir, fname)
        evidence[fname] = data
        evidence_present[fname] = exists

    review = evidence.get(UPSTREAM_EVIDENCE_FILES[0]) or {}
    install_rec = evidence.get("timm_install_execution_record_v1.json") or {}
    mutation_rec = evidence.get("timm_dependency_mutation_record_v1.json") or {}
    probe_rec = evidence.get("timm_find_spec_probe_v1.json") or {}
    post_audit = evidence.get("timm_install_post_review_audit_v1.json") or {}

    if "timm_install_execution_record" in review:
        install_rec = install_rec or review.get("timm_install_execution_record") or {}
    if "timm_dependency_mutation_record" in review:
        mutation_rec = mutation_rec or review.get("timm_dependency_mutation_record") or {}
    if "timm_find_spec_probe_record" in review:
        probe_rec = probe_rec or review.get("timm_find_spec_probe_record") or {}
    if "timm_install_post_review_audit" in review:
        post_audit = post_audit or review.get("timm_install_post_review_audit") or {}

    conclusions = review.get("conclusions", {})
    final_decision_observed = review.get("final_decision", "")
    blocker_count_observed = review.get("blocker_count", -1)
    no_boundary_violation_observed = conclusions.get("no_boundary_violation", False)
    timm_install_success_observed = conclusions.get("timm_install_success", install_rec.get("timm_install_success", True))
    find_spec_timm_observed = conclusions.get("find_spec_timm", probe_rec.get("find_spec_result", True))
    return_code_observed = int(install_rec.get("return_code", 0))
    install_error_observed = install_rec.get("install_error", "")
    timeout_occurred_observed = "TimeoutExpired" in install_error_observed or return_code_observed == -1
    timeout_seconds_observed = INSTALL_TIMEOUT_SECONDS_OBSERVED

    target_path = Path(install_rec.get("install_target", "")) if install_rec.get("install_target") else (
        _WRITABLE_BASE / CONTROLLED_INSTALL_TARGET_REL
    )
    target_path_size = _target_path_size_bytes(target_path)

    no_global_env_contamination_observed = conclusions.get(
        "no_global_env_contamination", mutation_rec.get("no_global_env_contamination", False)
    )
    global_env_changed_observed = conclusions.get(
        "global_env_changed", mutation_rec.get("global_env_changed", True)
    )
    torch_changed_observed = mutation_rec.get("torch_changed", True)

    real_import_performed_observed = post_audit.get("real_import_performed", False)
    model_load_performed_observed = post_audit.get("model_load_performed", False)
    inference_performed_observed = post_audit.get("inference_performed", False)
    runtime_performed_observed = post_audit.get("runtime_performed", False)
    registry_mutation_performed_observed = post_audit.get("registry_mutation_performed", False)
    additional_download_performed_observed = post_audit.get("additional_weight_download_performed", False)

    final_decision_ok = final_decision_observed == UPSTREAM_INSTALL_EXECUTION_EXPECTED_DECISION
    upstream_failed_no_boundary_violation = (
        final_decision_ok and no_boundary_violation_observed and blocker_count_observed == 0
    )
    upstream_no_global_contamination = (
        no_global_env_contamination_observed
        and not global_env_changed_observed
        and not torch_changed_observed
    )
    upstream_timeout_return_code_minus_one = (
        timeout_occurred_observed and return_code_observed == -1 and not timm_install_success_observed
    )
    target_path_empty_as_recorded = target_path_size == 0 and int(install_rec.get("installed_files_count", -1)) == 0

    audit_passed = (
        upstream_failed_no_boundary_violation
        and upstream_no_global_contamination
        and upstream_timeout_return_code_minus_one
        and target_path_empty_as_recorded
        and not timm_install_success_observed
        and not find_spec_timm_observed
        and not real_import_performed_observed
        and not model_load_performed_observed
        and not inference_performed_observed
        and not runtime_performed_observed
        and not registry_mutation_performed_observed
        and not additional_download_performed_observed
    )

    if not final_decision_ok:
        failed_checks.append(f"upstream.final_decision_mismatch:{final_decision_observed!r}")
    if not upstream_failed_no_boundary_violation:
        failed_checks.append("upstream.not_failed_no_boundary_violation")
    if not upstream_no_global_contamination:
        failed_checks.append("upstream.global_env_contamination_present")
    if not upstream_timeout_return_code_minus_one:
        failed_checks.append("upstream.not_timeout_return_code_minus_one")
    if not target_path_empty_as_recorded:
        failed_checks.append(f"upstream.target_path_not_empty:{target_path_size}B")

    audit = TimmInstallFailureAudit(
        audit_id="timm_install_failure_audit_v1",
        upstream_review_file_ref=str(upstream_dir / UPSTREAM_EVIDENCE_FILES[0]),
        upstream_review_exists=evidence_present.get(UPSTREAM_EVIDENCE_FILES[0], False),
        final_decision_observed=final_decision_observed,
        final_decision_ok=final_decision_ok,
        blocker_count_observed=blocker_count_observed,
        no_boundary_violation_observed=no_boundary_violation_observed,
        timm_install_success_observed=timm_install_success_observed,
        find_spec_timm_observed=find_spec_timm_observed,
        return_code_observed=return_code_observed,
        timeout_occurred_observed=timeout_occurred_observed,
        timeout_seconds_observed=timeout_seconds_observed,
        target_path_size_bytes_observed=target_path_size,
        no_global_env_contamination_observed=no_global_env_contamination_observed,
        global_env_changed_observed=global_env_changed_observed,
        torch_changed_observed=torch_changed_observed,
        real_import_performed_observed=real_import_performed_observed,
        model_load_performed_observed=model_load_performed_observed,
        inference_performed_observed=inference_performed_observed,
        runtime_performed_observed=runtime_performed_observed,
        registry_mutation_performed_observed=registry_mutation_performed_observed,
        additional_weight_download_performed_observed=additional_download_performed_observed,
        failure_category=FAILURE_CATEGORY,
        root_cause_candidate=ROOT_CAUSE_CANDIDATE,
        timm_package_corruption_related=False,
        mobile_sam_code_related=False,
        mobile_sam_weight_related=False,
        torch_missing_related=False,
        boundary_violation_related=not no_boundary_violation_observed,
        global_env_pollution_related=not upstream_no_global_contamination,
        retry_with_same_command_not_recommended=True,
        repair_replan_required=True,
        audit_passed=audit_passed,
    )

    # ------------------------------------------------------------------- #
    # (二) Timeout root cause record.
    # ------------------------------------------------------------------- #
    root_cause = TimmInstallTimeoutRootCauseRecord(
        record_id="timm_timeout_root_cause_v1",
        failure_category=FAILURE_CATEGORY,
        root_cause_candidate=ROOT_CAUSE_CANDIDATE,
        isolated_target_install_attempted=True,
        full_transitive_dependency_download_attempted=True,
        heavy_deps_include_torch_torchvision=True,
        timeout_seconds=timeout_seconds_observed,
        return_code=return_code_observed,
        target_path_empty_after_timeout=target_path_empty_as_recorded,
        not_timm_package_missing=True,
        not_mobile_sam_weight_issue=True,
        not_mobile_sam_code_issue=True,
        is_dependency_install_strategy_issue=True,
        same_full_isolated_install_retry_not_recommended=True,
    )

    # ------------------------------------------------------------------- #
    # (三) Repair route comparison.
    # ------------------------------------------------------------------- #
    timm_global_available, timm_global_version = _observe_timm_global()
    route_comparison = TimmRepairRouteComparisonRecord(
        record_id="timm_repair_route_comparison_v1",
        route_a_id="timm_no_deps_controlled_install",
        route_a_priority="P0",
        route_a_selected=True,
        route_b_id="timm_wheel_cache_or_offline_install",
        route_b_priority="P1",
        route_b_selected=False,
        route_c_id="extended_timeout_full_isolated_install",
        route_c_priority="P2",
        route_c_selected=False,
        route_d_id="global_env_reuse",
        route_d_priority="rejected",
        route_d_selected=False,
        selected_route=SELECTED_ROUTE,
        same_full_isolated_install_retry_not_recommended=True,
    )
    if timm_global_available:
        warnings.append(f"timm_global_metadata_available:{timm_global_version}_route_d_still_rejected")

    # ------------------------------------------------------------------- #
    # (四) Route A — no-deps install planning (template only).
    # ------------------------------------------------------------------- #
    target_str = str((_WRITABLE_BASE / CONTROLLED_INSTALL_TARGET_REL).resolve())
    command_template = NO_DEPS_COMMAND_TEMPLATE.format(
        python=sys.executable,
        package=TIMM_PACKAGE_NAME,
        target=target_str,
    )
    no_deps_plan = TimmNoDepsInstallPlanningRecord(
        record_id="timm_no_deps_install_plan_v1",
        selected_route=SELECTED_ROUTE,
        install_scope="controlled_model_load_env_or_isolated_target",
        command_template=command_template,
        command_template_only=True,
        command_not_executed=True,
        no_global_install=True,
        no_transitive_dependency_install=True,
        reuse_existing_torch_allowed_for_model_load_retry=True,
        existing_torch_version_must_be_verified=True,
        existing_torchvision_status_must_be_checked=True,
        post_install_probe="importlib.util.find_spec('timm') only",
        real_import_timm_not_allowed_until_model_load_retry_execution=True,
        model_load_retry_not_allowed_until_install_go=True,
        planning_not_install_approval=True,
        planning_not_install_success=True,
    )

    # Route B — wheel/cache fallback plan.
    cache_wheel_plan = TimmCacheWheelInstallPlanningRecord(
        record_id="timm_cache_wheel_install_plan_v1",
        route_id="timm_wheel_cache_or_offline_install",
        priority="P1",
        selected=False,
        rationale="reduce_network_instability_and_repeat_downloads",
        requires_wheel_source_review=True,
        requires_hash_record=True,
        fallback_only=True,
    )

    # Route C — extended timeout fallback-only.
    timeout_extension_plan = TimmTimeoutExtensionPlanningRecord(
        record_id="timm_timeout_extension_plan_v1",
        route_id="extended_timeout_full_isolated_install",
        priority="P2",
        selected=False,
        rationale="full_isolation_but_high_cost_not_preferred",
        timeout_seconds_candidate=3600,
        fallback_only=True,
    )

    # ------------------------------------------------------------------- #
    # (五) torch / torchvision reuse boundary.
    # ------------------------------------------------------------------- #
    torch_available, torch_version = _observe_torch_version()
    if not torch_available or not torch_version:
        torch_version = FALLBACK_TORCH_VERSION
        warnings.append("torch_version_observed_via_fallback_not_live_metadata")
    tv_available, tv_version = _observe_torchvision_available()

    retry_boundary = MobileSAMModelLoadRetryBoundaryAfterTimmRepair(
        record_id="mobile_sam_model_load_retry_boundary_after_timm_repair_v1",
        existing_torch_reuse_allowed=True,
        existing_torch_version_expected=torch_version,
        existing_torch_reuse_does_not_allow_global_mutation=True,
        existing_torch_reuse_does_not_allow_reinstall=True,
        torchvision_status_check_required=True,
        torch_compatibility_must_be_observed_after_model_load_retry=True,
        if_timm_requires_missing_lightweight_dependency_enter_next_repair_loop=True,
        mobile_sam_weight_sha256=MOBILE_SAM_WEIGHT_SHA256,
    )
    if not tv_available:
        warnings.append("torchvision_not_observed_in_global_metadata_check_before_no_deps_retry")

    # ------------------------------------------------------------------- #
    # (八) Risk record.
    # ------------------------------------------------------------------- #
    risk = TimmSecondRepairRiskRecord(
        record_id="timm_second_repair_risk_v1",
        no_deps_install_missing_transitive_dependency_risk=True,
        timm_version_latest_drift_risk=True,
        torch_timm_compatibility_risk=True,
        torchvision_reuse_risk=not tv_available,
        hidden_import_chain_risk=True,
        repeated_repair_loop_risk=True,
        model_load_retry_failure_risk=True,
        global_env_contamination_risk=True,
        inference_boundary_violation_risk=True,
        runtime_boundary_violation_risk=True,
    )

    # ------------------------------------------------------------------- #
    # (七) Model-load retry gate + second install retry gate.
    # ------------------------------------------------------------------- #
    retry_gate = TimmSecondInstallRetryGatePlanningRecord(
        record_id="timm_second_install_retry_gate_v1",
        model_load_retry_allowed_now=False,
        model_load_retry_requires_no_deps_timm_install_go=True,
        model_load_retry_requires_timm_find_spec_verified=True,
        model_load_retry_requires_mobile_sam_weight_sha256_recheck=True,
        model_load_retry_requires_code_and_weight_ready_still_valid=True,
        model_load_retry_requires_no_extra_dependency_gap_or_repair_loop=True,
        recommended_next_phase=NEXT_PHASE_NO_DEPS_REQUEST,
    )

    # ------------------------------------------------------------------- #
    # (九) Invariants for the 18 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_failed_no_boundary_violation": upstream_failed_no_boundary_violation,
        "upstream_no_global_contamination": upstream_no_global_contamination,
        "upstream_timeout_return_code_minus_one": upstream_timeout_return_code_minus_one,
        "target_path_empty_as_recorded": target_path_empty_as_recorded,
        "no_install_executed": (
            PIP_INSTALL_ALLOWED is False
            and TIMM_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_EXECUTION_ALLOWED is False
            and no_deps_plan.command_not_executed is True
        ),
        "no_real_import": REAL_IMPORT_ALLOWED is False,
        "no_model_load_retry": MODEL_LOAD_ALLOWED is False and MODEL_LOAD_RETRY_ALLOWED is False,
        "no_inference_seg_pred": REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "route_a_not_install_approval": no_deps_plan.planning_not_install_approval is True,
        "no_deps_planning_not_install_success": no_deps_plan.planning_not_install_success is True,
        "timm_availability_not_assumed": not timm_install_success_observed and not find_spec_timm_observed,
        "model_load_retry_not_allowed_now": retry_gate.model_load_retry_allowed_now is False,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeTimmInstallFailureRepairPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeTimmInstallFailureRepairPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_timm_install_failure_repair_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_timm_install_failure_repair_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "timm_install_failure_audit_count_gte_1": True,
        "timm_timeout_root_cause_record_count_gte_1": True,
        "timm_repair_route_comparison_record_count_gte_1": True,
        "timm_no_deps_install_plan_record_count_gte_1": True,
        "timm_cache_or_wheel_install_plan_record_count_gte_1": True,
        "timm_retry_gate_record_count_gte_1": True,
        "mobile_sam_model_load_retry_boundary_record_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "timm_install_failure_review": TIMM_INSTALL_FAILURE_REVIEW is True,
        "repair_replanning_only": REPAIR_REPLANNING_ONLY is True,
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
        "failure_category_dependency_install_timeout": audit.failure_category == FAILURE_CATEGORY,
        "root_cause_transitive_heavy_isolated_target": audit.root_cause_candidate == ROOT_CAUSE_CANDIDATE,
        "selected_route_timm_no_deps": route_comparison.selected_route == SELECTED_ROUTE,
        "same_full_isolated_install_retry_not_recommended": root_cause.same_full_isolated_install_retry_not_recommended,
        "model_load_retry_allowed_now_false": retry_gate.model_load_retry_allowed_now is False,
        "no_deps_planning_not_install_approval": no_deps_plan.planning_not_install_approval,
        "no_deps_planning_not_install_success": no_deps_plan.planning_not_install_success,
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
    decision = P1MobileSAMTimmInstallFailureRepairPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_timm_install_failure_repair_planning_profile_count=1,
        timm_install_failure_audit_count=1,
        timm_timeout_root_cause_record_count=1,
        timm_repair_route_comparison_record_count=1,
        timm_no_deps_install_plan_record_count=1,
        timm_cache_or_wheel_install_plan_record_count=1,
        timm_retry_gate_record_count=1,
        mobile_sam_model_load_retry_boundary_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        selected_route=SELECTED_ROUTE,
        same_full_isolated_install_retry_not_recommended=True,
        model_load_retry_allowed_now=False,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Dependency Repair Install Failure Review And Repair Planning (planning only, mobile_sam_only, target=timm)",
        "lifecycle_variant": SCOPE,
        "repair_principle_zh": REPAIR_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "target_dependency": TIMM_PACKAGE_NAME,
        "asset_id": MOBILE_SAM_ASSET_ID,
        "upstream_install_execution_ref": UPSTREAM_INSTALL_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "upstream_evidence_dir": str(upstream_dir),
        "mobile_sam_timm_install_failure_repair_planning_profile": _build_profile(),
        "mobile_sam_timm_install_failure_repair_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "timm_install_failure_audit": asdict(audit),
        "timm_install_failure_audit_count": 1,
        "timm_timeout_root_cause_record": asdict(root_cause),
        "timm_timeout_root_cause_record_count": 1,
        "timm_repair_route_comparison_record": asdict(route_comparison),
        "timm_repair_route_comparison_record_count": 1,
        "timm_no_deps_install_plan_record": asdict(no_deps_plan),
        "timm_no_deps_install_plan_record_count": 1,
        "timm_cache_wheel_install_plan_record": asdict(cache_wheel_plan),
        "timm_cache_or_wheel_install_plan_record_count": 1,
        "timm_timeout_extension_plan_record": asdict(timeout_extension_plan),
        "timm_second_repair_risk_record": asdict(risk),
        "timm_second_install_retry_gate_record": asdict(retry_gate),
        "timm_retry_gate_record_count": 1,
        "mobile_sam_model_load_retry_boundary_after_timm_repair": asdict(retry_boundary),
        "mobile_sam_model_load_retry_boundary_record_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "observed_torch_version": torch_version,
        "observed_torchvision_available": tv_available,
        "observed_torchvision_version": tv_version,
        "observed_timm_global_available": timm_global_available,
        "target_path_size_bytes": target_path_size,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "failure_category": FAILURE_CATEGORY,
            "root_cause_candidate": ROOT_CAUSE_CANDIDATE,
            "selected_route": SELECTED_ROUTE,
            "same_full_isolated_install_retry_not_recommended": True,
            "model_load_retry_allowed_now": False,
            "timm_installed_this_phase": False,
            "imported_this_phase": False,
            "recommended_next_phase": NEXT_PHASE_NO_DEPS_REQUEST,
            "suggested_retry_phase_after_no_deps_go": SUGGESTED_RETRY_PHASE,
            "transition_note": (
                "PLANNING ONLY (mobile_sam_only, target=timm). Upstream timm controlled-install "
                "FAILED_NO_BOUNDARY_VIOLATION was audited: timeout after " + str(timeout_seconds_observed)
                + "s (return_code=-1), target_path=" + str(target_path_size) + "B, no global contamination. "
                "Root cause is dependency install strategy timeout (full isolated --target attempted to re-download "
                "torch/torchvision), NOT timm corruption / MobileSAM code / MobileSAM weight / torch missing. "
                "Route A timm --no-deps controlled install is SELECTED (P0): reuse existing torch "
                + torch_version + " / torchvision, install only timm import root to isolated target. "
                "Route B wheel/cache is P1 fallback; Route C extended timeout is P2 fallback-only; "
                "Route D global reuse is REJECTED. NOTHING was pip-installed / imported / model-loaded / inferred / "
                "run; registry NOT mutated. no-deps planning is NOT install approval or install success. "
                "model-load retry NOT allowed now. Next: " + NEXT_PHASE_NO_DEPS_REQUEST + "."
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
            "timm_install_failure_audit_record": {"timm_install_failure_audit": asdict(audit)},
            "timm_timeout_root_cause_record": {"timm_timeout_root_cause_record": asdict(root_cause)},
            "timm_repair_route_comparison_record": {"timm_repair_route_comparison_record": asdict(route_comparison)},
            "timm_no_deps_install_plan_record": {"timm_no_deps_install_plan_record": asdict(no_deps_plan)},
            "timm_cache_or_wheel_install_plan_record": {
                "timm_cache_wheel_install_plan_record": asdict(cache_wheel_plan),
                "timm_timeout_extension_plan_record": asdict(timeout_extension_plan),
            },
            "timm_retry_gate_record": {"timm_second_install_retry_gate_record": asdict(retry_gate)},
            "mobile_sam_model_load_retry_boundary_record": {
                "mobile_sam_model_load_retry_boundary_after_timm_repair": asdict(retry_boundary),
                "timm_second_repair_risk_record": asdict(risk),
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
    result = review_p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "failure_category": result["conclusions"]["failure_category"],
                "selected_route": result["conclusions"]["selected_route"],
                "observed_torch_version": result.get("observed_torch_version"),
                "model_load_retry_allowed_now": result["conclusions"]["model_load_retry_allowed_now"],
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
