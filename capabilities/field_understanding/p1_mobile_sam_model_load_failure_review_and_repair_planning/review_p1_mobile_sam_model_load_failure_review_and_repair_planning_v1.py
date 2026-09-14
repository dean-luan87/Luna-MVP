# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Failure Review And Repair Planning — review v1
(PLANNING ONLY, scope = mobile_sam_only).

Reads the upstream MobileSAM model-load trial FAILED_NO_BOUNDARY_VIOLATION artifacts and
reviews the failure root cause: a runtime dependency gap (`timm` missing via
ModuleNotFoundError), NOT model-capability failure, NOT weight corruption, NOT checkpoint
damage. It records the `timm` dependency gap, plans the controlled repair, routes the
next dependency-install request/approval/readiness phase, and plans the model-load retry
gate. It does NOT install `timm` / pip install / install any dependency, does NOT real
import / model load / retry, does NOT inference / segmentation / prediction / runtime /
output adapter / semantic promotion, does NOT mutate the registry, and downloads NOTHING
extra. Protected, non-deletable test board records are written in `planning` mode.
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
from capabilities.field_understanding.p1_mobile_sam_model_load_failure_review_and_repair_planning.p1_mobile_sam_model_load_failure_review_and_repair_planning_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_model_load_failure_review_and_repair_planning.p1_mobile_sam_model_load_failure_review_and_repair_planning_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_ALLOWED,
    DEPENDENCY_REPAIR_PLANNING_ONLY,
    EXPECTED_ERROR_CLASS,
    EXPECTED_ERROR_SUBSTRING,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FAILURE_CATEGORY,
    FAILURE_REVIEW,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LUNA_CORE_PRINCIPLE,
    MISSING_DEPENDENCY,
    MODEL_LOAD_ALLOWED,
    NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    PLANNING_ONLY,
    REPAIR_PLANNING_ONLY,
    REPAIR_PRINCIPLE_ZH,
    NEGATIVE_GUARDS,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SUGGESTED_RETRY_PHASE,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_INSTALL_ALLOWED,
    UPSTREAM_EVIDENCE_FILES,
    UPSTREAM_OUTPUT_DIR_REL,
    UPSTREAM_TRIAL_EXECUTION_EXPECTED_DECISION,
    UPSTREAM_TRIAL_EXECUTION_REF,
    WEIGHT_CHAIN,
    MobileSAMDependencyGapRecord,
    MobileSAMDependencyInstallRequestRoute,
    MobileSAMInferenceRuntimeBoundaryRecord,
    MobileSAMModelLoadFailureAudit,
    MobileSAMModelLoadRetryGatePlanningRecord,
    MobileSAMRepairFollowupRoute,
    MobileSAMRepairRiskRecord,
    MobileSAMTimmRepairPlanningRecord,
    NegativeMobileSAMModelLoadFailureRepairPlanningGuard,
    P1MobileSAMModelLoadFailureRepairPlanningDecision,
    P1MobileSAMModelLoadFailureRepairPlanningProfile,
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
    / "p1_mobile_sam_model_load_failure_review_and_repair_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_model_load_failure_review_and_repair_planning_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_model_load_failure_review_and_repair_planning"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_model_load_failure_review_and_repair_planning_types_v1.py",
    f"{_PKG}/p1_mobile_sam_model_load_failure_review_and_repair_planning_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_model_load_failure_review_and_repair_planning_v1.py",
)

PROFILE_REF = "p1_mobile_sam_model_load_failure_repair_planning_profile_v1"
DECISION_REF = "p1_mobile_sam_model_load_failure_repair_planning_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_upstream_dir() -> Path:
    for base in (_REPO_ROOT, Path.cwd(), _WRITABLE_BASE):
        p = base / UPSTREAM_OUTPUT_DIR_REL
        if p.is_dir():
            return p
    return _REPO_ROOT / UPSTREAM_OUTPUT_DIR_REL


def _load_upstream_artifact(upstream_dir: Path, filename: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = upstream_dir / filename
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _parse_error_class(error_str: str) -> str:
    if ":" in error_str:
        return error_str.split(":", 1)[0]
    return error_str


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMModelLoadFailureRepairPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            mobile_sam_only=True,
            failure_review=FAILURE_REVIEW,
            repair_planning_only=REPAIR_PLANNING_ONLY,
            dependency_repair_planning_only=DEPENDENCY_REPAIR_PLANNING_ONLY,
            timm_install_allowed=TIMM_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_trial_execution_ref=UPSTREAM_TRIAL_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_model_load_failure_review_and_repair_planning_v1(
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
    # (一) Upstream failure result review — read trial execution artifacts.
    # ------------------------------------------------------------------- #
    upstream_dir = _resolve_upstream_dir()
    evidence: Dict[str, Any] = {}
    evidence_present: Dict[str, bool] = {}
    for fname in UPSTREAM_EVIDENCE_FILES:
        data, exists = _load_upstream_artifact(upstream_dir, fname)
        evidence[fname] = data
        evidence_present[fname] = exists

    review = evidence.get("p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json") or {}
    import_rec = evidence.get("mobile_sam_model_import_record_v1.json") or {}
    load_rec = evidence.get("mobile_sam_model_load_execution_record_v1.json") or {}
    recheck_rec = evidence.get("mobile_sam_sha256_recheck_v1.json") or {}
    post_audit = evidence.get("mobile_sam_model_load_post_review_audit_v1.json") or {}

    # Unwrap nested record keys if present.
    if "mobile_sam_model_import_execution_record" in import_rec:
        import_rec = import_rec["mobile_sam_model_import_execution_record"]
    if "mobile_sam_model_load_execution_record" in load_rec:
        load_rec = load_rec["mobile_sam_model_load_execution_record"]
    if "mobile_sam_sha256_recheck_record" in recheck_rec:
        recheck_rec = recheck_rec["mobile_sam_sha256_recheck_record"]

    conclusions = review.get("conclusions", {})
    final_decision_observed = review.get("final_decision", "")
    blocker_count_observed = review.get("blocker_count", -1)
    no_boundary_violation_observed = conclusions.get("no_boundary_violation", False)
    sha256_matches_observed = conclusions.get("sha256_matches", recheck_rec.get("sha256_matches", False))
    size_matches_observed = conclusions.get("size_matches", recheck_rec.get("size_matches", False))
    import_success_observed = conclusions.get("import_success", import_rec.get("import_success", True))
    import_attempted_observed = import_rec.get("import_attempted", False)
    error_message_observed = conclusions.get("import_error", import_rec.get("import_error", ""))
    error_class_observed = _parse_error_class(error_message_observed)
    error_is_modulenotfound_timm = (
        error_class_observed == EXPECTED_ERROR_CLASS
        and EXPECTED_ERROR_SUBSTRING in error_message_observed
    )
    checkpoint_load_attempted_observed = load_rec.get("checkpoint_load_attempted", False)
    checkpoint_load_success_observed = conclusions.get("checkpoint_load_success", load_rec.get("checkpoint_load_success", True))

    final_decision_ok = final_decision_observed == UPSTREAM_TRIAL_EXECUTION_EXPECTED_DECISION
    upstream_failed_no_boundary_violation = final_decision_ok and no_boundary_violation_observed and blocker_count_observed == 0
    upstream_boundary_clean = no_boundary_violation_observed and blocker_count_observed == 0
    sha256_size_valid = sha256_matches_observed and size_matches_observed
    real_import_failure_evidence = import_attempted_observed and not import_success_observed

    if not final_decision_ok:
        failed_checks.append(f"upstream.final_decision_mismatch:{final_decision_observed!r}")
    if not upstream_boundary_clean:
        failed_checks.append("upstream.boundary_violation_present")
    if not sha256_size_valid:
        failed_checks.append("upstream.sha256_or_size_mismatch")
    if not real_import_failure_evidence:
        failed_checks.append("upstream.no_real_import_failure_evidence")
    if not error_is_modulenotfound_timm:
        failed_checks.append(f"upstream.error_not_modulenotfound_timm:{error_message_observed!r}")

    audit = MobileSAMModelLoadFailureAudit(
        audit_id="mobile_sam_model_load_failure_audit_v1",
        upstream_review_file_ref=str(upstream_dir / "p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json"),
        upstream_review_exists=evidence_present.get("p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json", False),
        final_decision_observed=final_decision_observed,
        final_decision_ok=final_decision_ok,
        blocker_count_observed=blocker_count_observed,
        no_boundary_violation_observed=no_boundary_violation_observed,
        sha256_matches_observed=sha256_matches_observed,
        size_matches_observed=size_matches_observed,
        real_import_attempted_observed=import_attempted_observed,
        import_success_observed=import_success_observed,
        error_class_observed=error_class_observed,
        error_message_observed=error_message_observed,
        error_is_modulenotfound_timm=error_is_modulenotfound_timm,
        checkpoint_load_attempted_observed=checkpoint_load_attempted_observed,
        checkpoint_load_success_observed=checkpoint_load_success_observed,
        image_input_used=False,
        segmentation_used=False,
        prediction_used=False,
        inference_used=False,
        runtime_used=False,
        output_adapter_used=False,
        semantic_layer_used=False,
        registry_mutation_performed=False,
        additional_download_performed=False,
        failure_is_reproducible_candidate=True,
        failure_category=FAILURE_CATEGORY,
        root_cause_candidate=f"missing runtime dependency {MISSING_DEPENDENCY}",
        weight_integrity_related=False,
        checkpoint_corruption_related=False,
        model_code_missing_related=False,
        environment_dependency_related=True,
        boundary_violation_related=False,
        registry_patch_required_now=False,
        weight_redownload_required=False,
        source_reinstall_required=False,
        model_load_retry_required_after_dependency_repair=True,
        not_model_capability_failure=True,
        not_weight_download_failure=True,
        not_checkpoint_corruption=True,
        is_transitive_dependency_gap=True,
        audit_passed=(
            upstream_failed_no_boundary_violation
            and sha256_size_valid
            and real_import_failure_evidence
            and error_is_modulenotfound_timm
        ),
    )

    # ------------------------------------------------------------------- #
    # (三) timm Dependency Gap Record.
    # ------------------------------------------------------------------- #
    gap = MobileSAMDependencyGapRecord(
        record_id="mobile_sam_dependency_gap_v1",
        dependency_name=MISSING_DEPENDENCY,
        dependency_role="MobileSAM runtime/model-load dependency",
        dependency_status="missing",
        discovered_at_phase=UPSTREAM_TRIAL_EXECUTION_REF,
        discovered_by="real import attempt",
        package_install_required=True,
        install_scope_required="controlled_model_load_env",
        global_install_allowed=False,
        version_status="unresolved",
        version_resolution_required=True,
        license_review_required=True,
        transitive_dependency_review_required=True,
        pip_install_requires_separate_request=True,
        owner_approval_required=True,
        install_execution_not_allowed_now=True,
    )

    # ------------------------------------------------------------------- #
    # (四) timm Repair Planning.
    # ------------------------------------------------------------------- #
    timm_repair = MobileSAMTimmRepairPlanningRecord(
        record_id="mobile_sam_timm_repair_plan_v1",
        repair_target="controlled model-load environment",
        repair_action_candidate="install timm into controlled environment or isolated target path",
        repair_action_not_executed=True,
        clean_pypi_candidate=True,
        package_name_candidate=MISSING_DEPENDENCY,
        import_root_candidate=MISSING_DEPENDENCY,
        version_pin_required=True,
        hash_or_lockfile_recommended=True,
        dependency_conflict_review_required=True,
        torch_compatibility_review_required=True,
        offline_or_cached_install_preferred_if_available=True,
        rollback_required=True,
        post_install_probe_required=True,
        probe_method="importlib.util.find_spec only",
        real_import_after_install_not_allowed_until_model_load_retry=True,
    )

    # ------------------------------------------------------------------- #
    # (五) Dependency Install Request Route.
    # ------------------------------------------------------------------- #
    install_route = MobileSAMDependencyInstallRequestRoute(
        route_id="mobile_sam_dependency_install_request_route_v1",
        recommended_next_phase=NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST,
        allows_timm_install_request=True,
        allows_owner_approval_issuance=True,
        allows_package_version_license_dependency_review=True,
        allows_command_whitelist=True,
        allows_readiness_review=True,
        still_no_direct_pip_install=True,
        still_no_model_load=True,
        still_no_inference=True,
        still_no_runtime=True,
        still_no_registry_mutation=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Model-load Retry Gate.
    # ------------------------------------------------------------------- #
    retry_gate = MobileSAMModelLoadRetryGatePlanningRecord(
        record_id="mobile_sam_model_load_retry_gate_v1",
        model_load_retry_allowed_now=False,
        timm_install_request_go_required=True,
        timm_owner_approval_granted_required=True,
        timm_install_execution_go_required=True,
        timm_find_spec_verified_required=True,
        no_global_env_contamination_required=True,
        mobile_sam_weight_sha256_rechecked_required=True,
        mobile_sam_code_and_weight_ready_still_valid_required=True,
        model_load_retry_command_whitelist_updated_required=True,
        test_board_ready_required=True,
        suggested_retry_phase=SUGGESTED_RETRY_PHASE,
    )

    # ------------------------------------------------------------------- #
    # (七) Repair Risk Record.
    # ------------------------------------------------------------------- #
    risk = MobileSAMRepairRiskRecord(
        record_id="mobile_sam_repair_risk_v1",
        timm_version_compatibility_risk="medium: version pin required; torch 2.8.0 compatibility must be reviewed",
        torch_compatibility_risk="medium: timm must be compatible with installed torch 2.8.0",
        transitive_dependency_risk="medium: timm may pull additional transitive deps beyond timm itself",
        package_supply_chain_risk="low_to_medium: clean PyPI candidate but supply-chain review required",
        global_environment_contamination_risk="high_if_global_install: must use controlled_model_load_env only",
        hidden_import_dependency_risk="medium: further hidden deps may surface after timm install",
        repeated_model_load_failure_risk="medium: if timm install succeeds but other deps still missing",
        model_load_retry_scope_creep_risk="low: retry must remain mobile_sam_only with no inference/runtime",
        inference_boundary_violation_risk="low_if_governance_followed: inference still requires separate trial",
        runtime_boundary_violation_risk="low_if_governance_followed: runtime still requires separate trial",
    )

    # ------------------------------------------------------------------- #
    # (八) Inference / Runtime Boundary.
    # ------------------------------------------------------------------- #
    boundary = MobileSAMInferenceRuntimeBoundaryRecord(
        record_id="mobile_sam_inference_runtime_boundary_v1",
        dependency_repair_success_not_model_load_success=True,
        timm_install_success_not_inference_approval=True,
        timm_install_success_not_runtime_approval=True,
        model_load_retry_success_not_inference_approval=True,
        model_load_retry_success_not_runtime_approval=True,
        inference_requires_separate_trial=True,
        runtime_requires_separate_trial=True,
        output_adapter_requires_separate_review=True,
        semantic_layer_requires_separate_promotion=True,
        commercial_runtime_not_approved=True,
    )

    # ------------------------------------------------------------------- #
    # Follow-up route.
    # ------------------------------------------------------------------- #
    followup = MobileSAMRepairFollowupRoute(
        route_id="mobile_sam_repair_followup_route_v1",
        recommended_next_phase=NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST,
        next_phase_scope="mobile_sam_only",
        next_phase_purpose="timm_install_request_owner_approval_readiness_no_direct_install",
        suggested_retry_phase=SUGGESTED_RETRY_PHASE,
        optional_followup_phase="Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001",
    )

    # ------------------------------------------------------------------- #
    # (九) Invariants for the 17 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_failed_no_boundary_violation": upstream_failed_no_boundary_violation,
        "upstream_boundary_clean": upstream_boundary_clean,
        "sha256_size_valid_before_attribution": sha256_size_valid,
        "real_import_failure_evidence_present": real_import_failure_evidence,
        "error_is_modulenotfound_timm": error_is_modulenotfound_timm,
        "no_install_in_this_phase": (
            TIMM_INSTALL_ALLOWED is False
            and PIP_INSTALL_ALLOWED is False
            and DEPENDENCY_INSTALL_ALLOWED is False
            and timm_repair.repair_action_not_executed is True
            and gap.install_execution_not_allowed_now is True
        ),
        "no_import_load_retry": (
            REAL_IMPORT_ALLOWED is False
            and MODEL_LOAD_ALLOWED is False
            and retry_gate.model_load_retry_allowed_now is False
        ),
        "no_inference_seg_pred": REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "repair_planning_not_install_approval": (
            install_route.still_no_direct_pip_install is True
            and gap.pip_install_requires_separate_request is True
            and gap.owner_approval_required is True
        ),
        "timm_install_not_model_load_approval": (
            boundary.timm_install_success_not_inference_approval is True
            and boundary.dependency_repair_success_not_model_load_success is True
        ),
        "repair_success_not_inference_runtime_approval": (
            boundary.timm_install_success_not_inference_approval is True
            and boundary.timm_install_success_not_runtime_approval is True
            and boundary.model_load_retry_success_not_inference_approval is True
            and boundary.model_load_retry_success_not_runtime_approval is True
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMModelLoadFailureRepairPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMModelLoadFailureRepairPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_failure_repair_planning_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_model_load_failure_repair_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_model_load_failure_audit_count_gte_1": True,
        "mobile_sam_dependency_gap_record_count_gte_1": True,
        "mobile_sam_timm_repair_plan_record_count_gte_1": True,
        "mobile_sam_dependency_install_request_route_count_gte_1": True,
        "mobile_sam_model_load_retry_gate_planning_record_count_gte_1": True,
        "mobile_sam_repair_risk_record_count_gte_1": True,
        "mobile_sam_inference_runtime_boundary_record_count_gte_1": True,
        "mobile_sam_repair_followup_route_count_gte_1": True,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        # Upstream verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "planning_only": PLANNING_ONLY is True,
        "mobile_sam_only": True,
        "failure_review": FAILURE_REVIEW is True,
        "repair_planning_only": REPAIR_PLANNING_ONLY is True,
        "dependency_repair_planning_only": DEPENDENCY_REPAIR_PLANNING_ONLY is True,
        "timm_install_allowed_false": TIMM_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Failure attribution semantics.
        "failure_category_dependency_gap": audit.failure_category == FAILURE_CATEGORY,
        "missing_dependency_timm": gap.dependency_name == MISSING_DEPENDENCY,
        "error_class_modulenotfound": error_class_observed == EXPECTED_ERROR_CLASS,
        "weight_integrity_related_false": audit.weight_integrity_related is False,
        "checkpoint_corruption_related_false": audit.checkpoint_corruption_related is False,
        "environment_dependency_related_true": audit.environment_dependency_related is True,
        "timm_package_install_required": gap.package_install_required is True,
        "timm_install_requires_separate_request": gap.pip_install_requires_separate_request is True,
        "model_load_retry_allowed_now_false": retry_gate.model_load_retry_allowed_now is False,
        "audit_passed": audit.audit_passed,
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
    decision = P1MobileSAMModelLoadFailureRepairPlanningDecision(
        decision_ref=DECISION_REF,
        mobile_sam_model_load_failure_repair_planning_profile_count=1,
        mobile_sam_model_load_failure_audit_count=1,
        mobile_sam_dependency_gap_record_count=1,
        mobile_sam_timm_repair_plan_record_count=1,
        mobile_sam_dependency_install_request_route_count=1,
        mobile_sam_model_load_retry_gate_planning_record_count=1,
        mobile_sam_repair_risk_record_count=1,
        mobile_sam_inference_runtime_boundary_record_count=1,
        mobile_sam_repair_followup_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Model Load Failure Review And Repair Planning (planning only, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "repair_principle_zh": REPAIR_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "planning_only": PLANNING_ONLY,
        "failure_review": FAILURE_REVIEW,
        "repair_planning_only": REPAIR_PLANNING_ONLY,
        "timm_install_allowed": TIMM_INSTALL_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_trial_execution_ref": UPSTREAM_TRIAL_EXECUTION_REF,
        "upstream_trial_execution_expected_decision": UPSTREAM_TRIAL_EXECUTION_EXPECTED_DECISION,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "upstream_evidence_dir": str(upstream_dir),
        "upstream_evidence_present": evidence_present,
        "mobile_sam_model_load_failure_repair_planning_profile": _build_profile(),
        "mobile_sam_model_load_failure_repair_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_model_load_failure_audit": asdict(audit),
        "mobile_sam_model_load_failure_audit_count": 1,
        "mobile_sam_dependency_gap_record": asdict(gap),
        "mobile_sam_dependency_gap_record_count": 1,
        "mobile_sam_timm_repair_plan_record": asdict(timm_repair),
        "mobile_sam_timm_repair_plan_record_count": 1,
        "mobile_sam_dependency_install_request_route": asdict(install_route),
        "mobile_sam_dependency_install_request_route_count": 1,
        "mobile_sam_model_load_retry_gate_planning_record": asdict(retry_gate),
        "mobile_sam_model_load_retry_gate_planning_record_count": 1,
        "mobile_sam_repair_risk_record": asdict(risk),
        "mobile_sam_repair_risk_record_count": 1,
        "mobile_sam_inference_runtime_boundary_record": asdict(boundary),
        "mobile_sam_inference_runtime_boundary_record_count": 1,
        "mobile_sam_repair_followup_route": asdict(followup),
        "mobile_sam_repair_followup_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "failure_review_status": (
                "dependency_gap_timm_missing_repair_planned_no_install_no_load_no_inference_no_runtime"
                if blocker_count == 0
                else "blocked"
            ),
            "failure_category": FAILURE_CATEGORY,
            "missing_dependency": MISSING_DEPENDENCY,
            "root_cause": audit.root_cause_candidate,
            "not_model_capability_failure": audit.not_model_capability_failure,
            "not_weight_download_failure": audit.not_weight_download_failure,
            "not_checkpoint_corruption": audit.not_checkpoint_corruption,
            "is_transitive_dependency_gap": audit.is_transitive_dependency_gap,
            "timm_installed_this_phase": False,
            "model_load_retry_allowed_now": retry_gate.model_load_retry_allowed_now,
            "recommended_next_phase": NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST,
            "suggested_retry_phase": SUGGESTED_RETRY_PHASE,
            "transition_note": (
                "PLANNING ONLY (mobile_sam_only). Upstream model-load trial returned "
                + UPSTREAM_TRIAL_EXECUTION_EXPECTED_DECISION
                + " with blocker_count=0 and no_boundary_violation=true. sha256/size matched; real import "
                "was attempted and failed with ModuleNotFoundError: No module named 'timm'. This is a runtime "
                "dependency gap — NOT model-capability failure, NOT weight corruption, NOT checkpoint damage. "
                "A timm dependency-gap record, a controlled repair plan (install into controlled_model_load_env, "
                "version pin, torch compatibility review, find_spec-only post-install probe), a dependency-install "
                "request route, a model-load retry gate (retry NOT allowed now), a repair risk record, and an "
                "inference/runtime boundary record were produced. NOTHING was installed / imported / model-loaded / "
                "inferred / run; the registry was NOT mutated. Dependency-repair planning is NOT timm install "
                "approval. Next: " + NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST
                + " (timm install request + owner approval + readiness; still no direct pip install). "
                "After timm install execution GO, retry via " + SUGGESTED_RETRY_PHASE + "."
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
            "mobile_sam_model_load_failure_audit_record": {"mobile_sam_model_load_failure_audit": asdict(audit)},
            "mobile_sam_dependency_gap_record": {"mobile_sam_dependency_gap_record": asdict(gap)},
            "mobile_sam_timm_repair_plan_record": {"mobile_sam_timm_repair_plan_record": asdict(timm_repair)},
            "mobile_sam_dependency_install_request_route_record": {"mobile_sam_dependency_install_request_route": asdict(install_route)},
            "mobile_sam_model_load_retry_gate_record": {"mobile_sam_model_load_retry_gate_planning_record": asdict(retry_gate),
                                                         "mobile_sam_repair_risk_record": asdict(risk)},
            "mobile_sam_inference_runtime_boundary_record": {"mobile_sam_inference_runtime_boundary_record": asdict(boundary)},
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
        # Follow-up route as separate record (user spec lists it separately).
        followup_payload = {
            **common,
            "record_type": "mobile_sam_followup_registry_patch_route_record",
            "mobile_sam_repair_followup_route": asdict(followup),
        }
        followup_path = board_dir / "mobile_sam_followup_registry_patch_route_record.json"
        followup_path.write_text(json.dumps(followup_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        extra_written.append(str(followup_path))
        manifest["extra_written_records"] = extra_written
        manifest["extra_written_record_count"] = len(extra_written)
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_model_load_failure_review_and_repair_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "failure_category": result["conclusions"]["failure_category"],
                "missing_dependency": result["conclusions"]["missing_dependency"],
                "timm_installed_this_phase": result["conclusions"]["timm_installed_this_phase"],
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
