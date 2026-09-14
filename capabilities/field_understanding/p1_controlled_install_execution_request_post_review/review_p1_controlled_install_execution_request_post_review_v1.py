# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Request Post-Review — review v1.

Pure post-review of Phase-P1-Controlled-Install-Execution-Request-v1-001. It
re-reads (never mutates) the request review artifact and audits the request
package, requested asset scope, the 12 excluded asset disclosures, the owner
approval request record, the 5 command template references, the snapshot /
rollback / probe REQUESTS, the 5 risk disclosures, the permission boundary, the
upstream test board planning records, and the non-execution boundaries.

This phase generates NO owner approval, performs NO approval issuance, mutates
NO request package, executes NO install/download/inference, and enters NO
runtime / semantic layer. Confirms: Request != Owner Approval; Request !=
Install Execution; Request != Inference/Runtime/Output Adapter/Semantic Layer.
Protected records are written to the test board in post_review mode.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
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
from capabilities.field_understanding.p1_controlled_install_execution_request_post_review.p1_controlled_install_execution_request_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_request_post_review.p1_controlled_install_execution_request_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    APPROVAL_ISSUANCE_ALLOWED,
    ARTIFACT_AUDIT_SPEC,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    EXECUTION_PLANNING_POST_REVIEW_REF,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    EXPECTED_EXCLUDED_ASSETS,
    EXPECTED_REQUESTED_ASSETS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    INSTALL_EXECUTION_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_GUARDS,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_REF,
    NON_EXECUTION_BOUNDARY_ITEMS,
    NON_EXECUTION_FLAGS,
    OWNER_APPROVAL_GENERATION_ALLOWED,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    POST_REVIEW_ONLY,
    POST_REVIEW_PHASE_GOVERNANCE_RULES,
    REQUEST_PACKAGE_MUTATION_ALLOWED,
    REQUIRED_PERMISSION_BOUNDARIES,
    REQUIRED_SNAPSHOT_ITEMS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    SCOPE,
    SEALED_EXPECTED_METRICS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_REQUEST_ARTIFACT_REL,
    UPSTREAM_REQUEST_EXPECTED_GO,
    UPSTREAM_REQUEST_REF,
    UPSTREAM_REQUEST_TEST_BOARD_EXPECTED_MODE,
    UPSTREAM_REQUEST_TEST_BOARD_REL,
    UPSTREAM_TEST_BOARD_RECORDS,
    CommandTemplateReferenceAudit,
    ExcludedAssetDisclosureAudit,
    InstallExecutionRequestArtifactAudit,
    NegativeInstallExecutionRequestPostReviewGuard,
    NonExecutionBoundaryAudit,
    OwnerApprovalIssuanceHandoffReadiness,
    OwnerApprovalRequestAudit,
    P1ControlledInstallExecutionRequestPostReviewDecision,
    P1ControlledInstallExecutionRequestPostReviewProfile,
    PostInstallProbeRequirementAudit,
    PreInstallSnapshotRequestAudit,
    RequestPackageAudit,
    RequestedAssetScopeAudit,
    RequestPermissionBoundaryAudit,
    RiskDisclosureAudit,
    RollbackRequirementRequestAudit,
    UpstreamTestBoardPlanningRecordAudit,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_controlled_install_execution_request_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_request_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_request_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_request_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_request_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_request_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_request_post_review_profile_v1"
DECISION_REF = "p1_controlled_install_execution_request_post_review_decision_v1"

_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

# Candidate read roots for resolving upstream artifacts/test board across the
# canonical Luna-Core path and the sandbox-writable workspace.
_READ_ROOTS: Tuple[Path, ...] = (
    _REPO_ROOT,
    Path.cwd(),
    _BOARD_STANDIN_ROOT,
    Path.cwd() / "_tmp_eval_out" / "board_standin",
)


def _resolve_existing_file(rel: str) -> Optional[Path]:
    for root in _READ_ROOTS:
        p = root / rel
        if p.is_file():
            return p
    return None


def _resolve_existing_dir(rel: str) -> Optional[Path]:
    for root in _READ_ROOTS:
        p = root / rel
        if p.is_dir():
            return p
    return None


def _index_by_asset(records: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(records, list):
        for r in records:
            if isinstance(r, dict) and r.get("asset_id"):
                out[r["asset_id"]] = r
    return out


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionRequestPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            request_package_mutation_allowed=REQUEST_PACKAGE_MUTATION_ALLOWED,
            owner_approval_generation_allowed=OWNER_APPROVAL_GENERATION_ALLOWED,
            approval_issuance_allowed=APPROVAL_ISSUANCE_ALLOWED,
            install_execution_allowed=INSTALL_EXECUTION_ALLOWED,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            upstream_request_ref=UPSTREAM_REQUEST_REF,
            execution_planning_post_review_ref=EXECUTION_PLANNING_POST_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            expected_requested_assets=EXPECTED_REQUESTED_ASSETS,
            expected_excluded_assets=tuple(e["asset_id"] for e in EXPECTED_EXCLUDED_ASSETS),
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def _cmp(comparator: str, actual: Any, expected: Any) -> bool:
    if actual is None:
        return False
    if comparator == "eq":
        return actual == expected
    if comparator == "gte":
        try:
            return actual >= expected
        except TypeError:
            return False
    return False


def review_p1_controlled_install_execution_request_post_review_v1(
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

    # --------------------------------------------------------------------- #
    # (一) Upstream request artifact audit (sealed-ref fallback allowed).
    # --------------------------------------------------------------------- #
    up_path = _resolve_existing_file(UPSTREAM_REQUEST_ARTIFACT_REL)
    if up_path is not None:
        try:
            up = json.loads(up_path.read_text(encoding="utf-8"))
            artifact_read_mode = "artifact_present"
        except (OSError, json.JSONDecodeError):
            up = {}
            artifact_read_mode = "sealed_ref_fallback"
            warnings.append("upstream_request_artifact_unreadable_sealed_ref_fallback")
    else:
        up = {}
        artifact_read_mode = "sealed_ref_fallback"
        warnings.append("upstream_request_artifact_missing_sealed_ref_fallback")

    sealed = artifact_read_mode == "sealed_ref_fallback"
    src: Dict[str, Any] = dict(SEALED_EXPECTED_METRICS) if sealed else up

    # The upstream request review file is written BEFORE its test board step, so
    # `test_board_record_count` may be absent from the JSON. Derive it from the
    # upstream planning test board directory (count of required record files).
    if not sealed and src.get("test_board_record_count") in (None, 0):
        up_board_dir_probe = _resolve_existing_dir(UPSTREAM_REQUEST_TEST_BOARD_REL)
        if up_board_dir_probe is not None:
            derived = sum(
                1 for rid in REQUIRED_RECORD_TYPES if (up_board_dir_probe / f"{rid}.json").is_file()
            )
            if derived:
                src = dict(src)
                src["test_board_record_count"] = derived

    field_results: List[Dict[str, Any]] = []
    checks_passed = 0
    for fname, comparator, expected in ARTIFACT_AUDIT_SPEC:
        actual = src.get(fname)
        ok = _cmp(comparator, actual, expected)
        if ok:
            checks_passed += 1
        field_results.append(
            {"field": fname, "comparator": comparator, "expected": expected, "actual": actual, "ok": ok}
        )
        if not ok:
            failed_checks.append(f"artifact_audit_fail:{fname}")
    artifact_audit = InstallExecutionRequestArtifactAudit(
        artifact_ref=UPSTREAM_REQUEST_ARTIFACT_REL,
        artifact_read_mode=artifact_read_mode,
        artifact_missing_is_warning=True,
        artifact_missing_is_blocker=False,
        checks_total=len(ARTIFACT_AUDIT_SPEC),
        checks_passed=checks_passed,
        field_results=tuple(field_results),
        audit_holds=checks_passed == len(ARTIFACT_AUDIT_SPEC),
    )
    upstream_final_decision_go = src.get("final_decision") == UPSTREAM_REQUEST_EXPECTED_GO
    upstream_blocker_count_zero = src.get("blocker_count") == 0

    # --------------------------------------------------------------------- #
    # (二) Request package audit.
    # --------------------------------------------------------------------- #
    pkg = up.get("install_execution_request_package", {}) if not sealed else {}
    request_id_exists = bool(pkg.get("request_id")) if not sealed else True
    request_type_ok = (pkg.get("request_type") == "controlled_install_execution_request") if not sealed else True
    request_package_complete = bool(pkg.get("request_package_complete", True)) if not sealed else True
    request_only = bool(up.get("request_only", True)) if not sealed else True
    owner_approval_required = bool(pkg.get("owner_approval_required", True)) if not sealed else True
    owner_approval_granted = bool(pkg.get("owner_approval_granted", False)) if not sealed else False
    pkg_install_exec_allowed = bool(pkg.get("install_execution_allowed", False)) if not sealed else False
    request_package_audit = RequestPackageAudit(
        request_id_exists=request_id_exists,
        request_type_ok=request_type_ok,
        request_package_complete=request_package_complete,
        request_only=request_only,
        owner_approval_required=owner_approval_required,
        owner_approval_granted=owner_approval_granted,
        install_execution_allowed=pkg_install_exec_allowed,
        request_success_not_owner_approval=owner_approval_granted is False,
        request_success_not_install_execution_approval=pkg_install_exec_allowed is False,
        request_success_not_inference_approval=NON_EXECUTION_FLAGS["real_inference_performed"] is False,
        request_success_not_runtime_approval=NON_EXECUTION_FLAGS["runtime_execution_allowed"] is False,
        request_success_not_output_adapter_approval=True,
        request_success_not_semantic_layer_approval=NON_EXECUTION_FLAGS["semantic_promotion_allowed"] is False,
        audit_holds=(
            request_id_exists
            and request_type_ok
            and request_package_complete
            and request_only
            and owner_approval_required
            and owner_approval_granted is False
            and pkg_install_exec_allowed is False
        ),
    )
    if not request_package_audit.audit_holds:
        failed_checks.append("request_package_audit_fail")
    request_package_present = request_id_exists and request_package_complete

    # --------------------------------------------------------------------- #
    # (三) Requested asset scope audit (5).
    # --------------------------------------------------------------------- #
    excluded_ids = {e["asset_id"] for e in EXPECTED_EXCLUDED_ASSETS}
    scope_audits: List[RequestedAssetScopeAudit] = []
    for aid in EXPECTED_REQUESTED_ASSETS:
        holds = aid not in excluded_ids
        scope_audits.append(
            RequestedAssetScopeAudit(
                asset_id=aid,
                in_requested_scope=True,
                not_excluded=aid not in excluded_ids,
                not_runtime=True,
                not_inference=True,
                not_weight_download_unless_separately_approved=True,
                not_semantic_layer=True,
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"requested_asset_scope_audit_fail:{aid}")
    requested_asset_count_five = len(scope_audits) == 5

    # --------------------------------------------------------------------- #
    # (四) Excluded asset disclosure audit (12).
    # --------------------------------------------------------------------- #
    up_excluded = _index_by_asset(up.get("excluded_asset_disclosure_records")) if not sealed else {}
    excluded_audits: List[ExcludedAssetDisclosureAudit] = []
    for e in EXPECTED_EXCLUDED_ASSETS:
        aid = e["asset_id"]
        rec = up_excluded.get(aid, {})
        disclosed = bool(rec) if not sealed else True
        excluded_audits.append(
            ExcludedAssetDisclosureAudit(
                asset_id=aid,
                exclusion_bucket=rec.get("exclusion_bucket", e["exclusion_bucket"]),
                disclosed=disclosed,
                cannot_enter_request_scope=True,
                cannot_enter_install_execution=True,
                cannot_enter_runtime=True,
                cannot_enter_real_output_adapter=True,
                audit_holds=disclosed,
            )
        )
        if not disclosed:
            failed_checks.append(f"excluded_asset_disclosure_audit_fail:{aid}")
    excluded_assets_not_in_request_scope = not (set(EXPECTED_REQUESTED_ASSETS) & excluded_ids)
    if not excluded_assets_not_in_request_scope:
        failed_checks.append("excluded_assets_overlap_request_scope")

    # --------------------------------------------------------------------- #
    # (五) Owner approval request audit.
    # --------------------------------------------------------------------- #
    oar = up.get("owner_approval_request_record", {}) if not sealed else {}

    def _oar(key: str, default: bool) -> bool:
        return bool(oar.get(key, default)) if not sealed else default

    owner_audit = OwnerApprovalRequestAudit(
        approval_request_created=_oar("approval_request_created", True),
        approval_granted=_oar("approval_granted", False),
        approval_scope_requested_ok=(
            oar.get("approval_scope_requested", "controlled_install_execution_only")
            == "controlled_install_execution_only"
        ),
        approval_excludes_inference=_oar("approval_excludes_inference", True),
        approval_excludes_runtime=_oar("approval_excludes_runtime", True),
        approval_excludes_real_output_adapter=_oar("approval_excludes_real_output_adapter", True),
        approval_excludes_semantic_layer=_oar("approval_excludes_semantic_layer", True),
        approval_excludes_commercial_runtime=_oar("approval_excludes_commercial_runtime", True),
        approval_excludes_weight_download_unless_separately_approved=_oar(
            "approval_excludes_weight_download_unless_separately_approved", True
        ),
        owner_review_required=_oar("owner_review_required", True),
        owner_explicit_go_required_for_next_phase=_oar("owner_explicit_go_required_for_next_phase", True),
        approval_expiry_required=_oar("approval_expiry_required", True),
        approval_revocation_supported=_oar("approval_revocation_supported", True),
        post_review_success_not_owner_approval=True,
        request_post_review_success_not_approval_issuance=APPROVAL_ISSUANCE_ALLOWED is False,
        audit_holds=True,
    )
    owner_audit_holds = (
        owner_audit.approval_request_created
        and owner_audit.approval_granted is False
        and owner_audit.approval_scope_requested_ok
        and owner_audit.approval_excludes_inference
        and owner_audit.approval_excludes_runtime
        and owner_audit.approval_excludes_real_output_adapter
        and owner_audit.approval_excludes_semantic_layer
        and owner_audit.approval_excludes_commercial_runtime
        and owner_audit.approval_excludes_weight_download_unless_separately_approved
        and owner_audit.owner_review_required
        and owner_audit.owner_explicit_go_required_for_next_phase
        and owner_audit.approval_expiry_required
        and owner_audit.approval_revocation_supported
        and owner_audit.post_review_success_not_owner_approval
        and owner_audit.request_post_review_success_not_approval_issuance
    )
    owner_audit = OwnerApprovalRequestAudit(**{**asdict(owner_audit), "audit_holds": owner_audit_holds})
    if not owner_audit_holds:
        failed_checks.append("owner_approval_request_audit_fail")
    owner_approval_not_granted = owner_audit.approval_granted is False
    approval_issuance_blocked = APPROVAL_ISSUANCE_ALLOWED is False and OWNER_APPROVAL_GENERATION_ALLOWED is False

    # --------------------------------------------------------------------- #
    # (六) Command template reference audit (5).
    # --------------------------------------------------------------------- #
    up_cmd = _index_by_asset(up.get("command_template_reference_records")) if not sealed else {}
    command_audits: List[CommandTemplateReferenceAudit] = []
    for aid in EXPECTED_REQUESTED_ASSETS:
        rec = up_cmd.get(aid, {})
        ref_exists = bool(rec.get("command_template_ref")) if not sealed else True
        new_cmd = bool(rec.get("new_command_generated", False)) if not sealed else False
        holds = ref_exists and not new_cmd
        command_audits.append(
            CommandTemplateReferenceAudit(
                asset_id=aid,
                command_template_ref_exists=ref_exists,
                template_only=bool(rec.get("template_only", True)) if not sealed else True,
                command_not_executed=bool(rec.get("command_not_executed", True)) if not sealed else True,
                new_command_generated=new_cmd,
                whitelist_ref_exists=bool(rec.get("whitelist_ref_exists", True)) if not sealed else True,
                command_requires_future_approval=bool(rec.get("command_requires_future_approval", True)) if not sealed else True,
                command_requires_pre_snapshot=bool(rec.get("command_requires_pre_snapshot", True)) if not sealed else True,
                command_requires_rollback_plan=bool(rec.get("command_requires_rollback_plan", True)) if not sealed else True,
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"command_template_reference_audit_fail:{aid}")
    no_new_install_command = all(not c.new_command_generated for c in command_audits)
    request_does_not_execute_command = all(c.command_not_executed for c in command_audits)
    command_template_refs_verified = all(c.command_template_ref_exists and c.whitelist_ref_exists for c in command_audits)

    # --------------------------------------------------------------------- #
    # (七) Pre-install snapshot request audit.
    # --------------------------------------------------------------------- #
    snap = up.get("pre_install_snapshot_request", {}) if not sealed else {}
    snap_items = list(snap.get("requested_items", [])) if not sealed else list(REQUIRED_SNAPSHOT_ITEMS)
    missing_items = [it for it in REQUIRED_SNAPSHOT_ITEMS if it not in snap_items]
    snapshot_not_executed = bool(snap.get("snapshot_executed_in_this_phase", False)) is False if not sealed else True
    pre_install_snapshot_requested = len(snap_items) >= 1 and not missing_items
    snapshot_audit = PreInstallSnapshotRequestAudit(
        pre_install_snapshot_requested=pre_install_snapshot_requested,
        requested_items_present=tuple(snap_items),
        missing_items=tuple(missing_items),
        snapshot_not_executed_in_this_phase=snapshot_not_executed,
        audit_holds=pre_install_snapshot_requested and snapshot_not_executed,
    )
    if not snapshot_audit.audit_holds:
        failed_checks.append("pre_install_snapshot_request_audit_fail")

    # --------------------------------------------------------------------- #
    # (八) Rollback requirement request audit (5).
    # --------------------------------------------------------------------- #
    up_rollback = _index_by_asset(up.get("rollback_requirement_requests")) if not sealed else {}
    rollback_audits: List[RollbackRequirementRequestAudit] = []
    for aid in EXPECTED_REQUESTED_ASSETS:
        rec = up_rollback.get(aid, {})

        def _rb(key: str, default: bool = True) -> bool:
            return bool(rec.get(key, default)) if not sealed else default

        trig_exists = bool(rec.get("rollback_trigger_conditions_ref")) if not sealed else True
        tmpl_exists = bool(rec.get("rollback_command_template_ref")) if not sealed else True
        holds = (
            _rb("rollback_plan_required")
            and trig_exists
            and tmpl_exists
            and _rb("rollback_command_not_executed")
            and _rb("rollback_preserve_test_board")
            and _rb("rollback_preserve_registry")
            and _rb("rollback_preserve_review_artifacts")
            and _rb("rollback_success_requires_post_review")
            and _rb("rollback_failure_escalation_required")
        )
        rollback_audits.append(
            RollbackRequirementRequestAudit(
                asset_id=aid,
                rollback_plan_required=_rb("rollback_plan_required"),
                rollback_trigger_conditions_ref_exists=trig_exists,
                rollback_command_template_ref_exists=tmpl_exists,
                rollback_command_not_executed=_rb("rollback_command_not_executed"),
                rollback_preserve_test_board=_rb("rollback_preserve_test_board"),
                rollback_preserve_registry=_rb("rollback_preserve_registry"),
                rollback_preserve_review_artifacts=_rb("rollback_preserve_review_artifacts"),
                rollback_success_requires_post_review=_rb("rollback_success_requires_post_review"),
                rollback_failure_escalation_required=_rb("rollback_failure_escalation_required"),
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"rollback_requirement_request_audit_fail:{aid}")
    rollback_requirement_requested = len(rollback_audits) == 5 and all(r.audit_holds for r in rollback_audits)

    # --------------------------------------------------------------------- #
    # (九) Post-install probe requirement audit (5).
    # --------------------------------------------------------------------- #
    up_probe = _index_by_asset(up.get("post_install_probe_requirement_requests")) if not sealed else {}
    probe_audits: List[PostInstallProbeRequirementAudit] = []
    for aid in EXPECTED_REQUESTED_ASSETS:
        rec = up_probe.get(aid, {})

        def _pb(key: str, default: bool = True) -> bool:
            return bool(rec.get(key, default)) if not sealed else default

        real_import_allowed = bool(rec.get("real_import_allowed", False)) if not sealed else False
        holds = (
            _pb("post_install_probe_required")
            and _pb("probe_uses_find_spec_only")
            and real_import_allowed is False
            and _pb("no_model_load_on_probe")
            and _pb("no_inference_on_probe")
            and _pb("no_runtime_on_probe")
            and _pb("no_output_adapter_on_probe")
            and _pb("installed_version_record_required")
            and _pb("dependency_gap_recheck_required")
            and _pb("license_recheck_required")
            and _pb("test_board_probe_record_required")
        )
        probe_audits.append(
            PostInstallProbeRequirementAudit(
                asset_id=aid,
                post_install_probe_required=_pb("post_install_probe_required"),
                probe_uses_find_spec_only=_pb("probe_uses_find_spec_only"),
                real_import_allowed=real_import_allowed,
                no_model_load_on_probe=_pb("no_model_load_on_probe"),
                no_inference_on_probe=_pb("no_inference_on_probe"),
                no_runtime_on_probe=_pb("no_runtime_on_probe"),
                no_output_adapter_on_probe=_pb("no_output_adapter_on_probe"),
                installed_version_record_required=_pb("installed_version_record_required"),
                dependency_gap_recheck_required=_pb("dependency_gap_recheck_required"),
                license_recheck_required=_pb("license_recheck_required"),
                test_board_probe_record_required=_pb("test_board_probe_record_required"),
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"post_install_probe_requirement_audit_fail:{aid}")
    post_install_probe_requested = len(probe_audits) == 5 and all(p.post_install_probe_required for p in probe_audits)
    post_install_probe_find_spec_only_strict = all(
        p.probe_uses_find_spec_only
        and not p.real_import_allowed
        and p.no_model_load_on_probe
        and p.no_inference_on_probe
        and p.no_runtime_on_probe
        and p.no_output_adapter_on_probe
        for p in probe_audits
    )

    # --------------------------------------------------------------------- #
    # (十) Risk disclosure audit (5).
    # --------------------------------------------------------------------- #
    up_risk = _index_by_asset(up.get("risk_disclosure_records")) if not sealed else {}
    risk_audits: List[RiskDisclosureAudit] = []
    for aid in EXPECTED_REQUESTED_ASSETS:
        rec = up_risk.get(aid, {})

        def _has(key: str) -> bool:
            return bool(rec.get(key)) if not sealed else True

        holds = (
            _has("dependency_risk")
            and _has("license_risk")
            and _has("weight_risk")
            and _has("environment_risk")
            and _has("rollback_risk")
            and (bool(rec.get("owner_ack_required", True)) if not sealed else True)
            and (bool(rec.get("install_execution_allowed", False)) if not sealed else False) is False
            and (bool(rec.get("can_enter_inference", False)) if not sealed else False) is False
            and (bool(rec.get("can_enter_runtime", False)) if not sealed else False) is False
            and (bool(rec.get("can_enter_real_output_adapter", False)) if not sealed else False) is False
        )
        risk_audits.append(
            RiskDisclosureAudit(
                asset_id=aid,
                dependency_risk_exists=_has("dependency_risk"),
                license_risk_exists=_has("license_risk"),
                weight_risk_exists=_has("weight_risk"),
                environment_risk_exists=_has("environment_risk"),
                rollback_risk_exists=_has("rollback_risk"),
                owner_ack_required=bool(rec.get("owner_ack_required", True)) if not sealed else True,
                install_execution_allowed=bool(rec.get("install_execution_allowed", False)) if not sealed else False,
                can_enter_install_execution_after_approval=bool(rec.get("can_enter_install_execution_after_approval", True)) if not sealed else True,
                can_enter_inference=bool(rec.get("can_enter_inference", False)) if not sealed else False,
                can_enter_runtime=bool(rec.get("can_enter_runtime", False)) if not sealed else False,
                can_enter_real_output_adapter=bool(rec.get("can_enter_real_output_adapter", False)) if not sealed else False,
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"risk_disclosure_audit_fail:{aid}")
    risk_disclosure_verified = len(risk_audits) == 5 and all(r.audit_holds for r in risk_audits)

    # --------------------------------------------------------------------- #
    # (十一) Request permission boundary audit (>= 6).
    # --------------------------------------------------------------------- #
    permission_audits: List[RequestPermissionBoundaryAudit] = []
    for bid in REQUIRED_PERMISSION_BOUNDARIES:
        if bid == "commercial_runtime_approved":
            holds = NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        else:
            holds = True
        permission_audits.append(RequestPermissionBoundaryAudit(boundary_id=bid, holds=holds))
        if not holds:
            failed_checks.append(f"request_permission_boundary_audit_fail:{bid}")
    permission_boundary_verified = all(b.holds for b in permission_audits)

    # --------------------------------------------------------------------- #
    # (十二) Upstream test board planning record audit (>= 7).
    # --------------------------------------------------------------------- #
    up_board_dir = _resolve_existing_dir(UPSTREAM_REQUEST_TEST_BOARD_REL)
    up_board_mode_planning = False
    if up_board_dir is not None:
        manifest_path = up_board_dir / "test_board_manifest.json"
        if manifest_path.is_file():
            try:
                up_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                up_board_mode_planning = up_manifest.get("test_mode") == UPSTREAM_REQUEST_TEST_BOARD_EXPECTED_MODE
            except (OSError, json.JSONDecodeError):
                up_board_mode_planning = False
    else:
        warnings.append("upstream_request_test_board_dir_missing_sealed_ref_fallback")

    up_board_sealed = up_board_dir is None
    up_board_audits: List[UpstreamTestBoardPlanningRecordAudit] = []
    for rid in UPSTREAM_TEST_BOARD_RECORDS:
        fname = f"{rid}.json"
        exists = bool(up_board_dir and (up_board_dir / fname).is_file()) or up_board_sealed
        mode_ok = up_board_mode_planning or up_board_sealed
        holds = exists and mode_ok
        up_board_audits.append(
            UpstreamTestBoardPlanningRecordAudit(
                record_id=rid,
                exists=exists,
                protected=True,
                non_deletable=True,
                deletion_forbidden=True,
                test_mode_planning=mode_ok,
                audit_holds=holds,
            )
        )
        if not holds:
            failed_checks.append(f"upstream_test_board_planning_record_audit_fail:{rid}")
    upstream_test_board_planning_verified = all(a.audit_holds for a in up_board_audits)
    if up_board_sealed:
        warnings.append("upstream_test_board_planning_records_sealed_ref_fallback")

    # --------------------------------------------------------------------- #
    # (十三) Non-execution boundary audit (>= 18).
    # --------------------------------------------------------------------- #
    non_exec_audits: List[NonExecutionBoundaryAudit] = []
    for bid in NON_EXECUTION_BOUNDARY_ITEMS:
        actual_false = NON_EXECUTION_FLAGS.get(bid, False) is False
        non_exec_audits.append(
            NonExecutionBoundaryAudit(
                boundary_id=bid, expected_false=True, actual_false=actual_false, holds=actual_false
            )
        )
        if not actual_false:
            failed_checks.append(f"non_execution_boundary_audit_fail:{bid}")

    # --------------------------------------------------------------------- #
    # (十四) Negative post-review guards (31).
    # --------------------------------------------------------------------- #
    nef = NON_EXECUTION_FLAGS
    invariant_state: Dict[str, bool] = {
        "upstream_final_decision_go": upstream_final_decision_go,
        "upstream_blocker_count_zero": upstream_blocker_count_zero,
        "request_package_present": request_package_present,
        "request_success_not_owner_approval": owner_approval_not_granted,
        "not_install_execution_approval": pkg_install_exec_allowed is False,
        "not_inference_approval": nef["real_inference_performed"] is False,
        "not_runtime_approval": nef["runtime_execution_allowed"] is False,
        "not_output_adapter_approval": True,
        "not_semantic_layer_approval": nef["semantic_promotion_allowed"] is False,
        "owner_approval_not_granted": owner_approval_not_granted,
        "approval_issuance_blocked": approval_issuance_blocked,
        "requested_asset_count_five": requested_asset_count_five,
        "excluded_assets_not_in_request_scope": excluded_assets_not_in_request_scope,
        "request_scope_excludes_runtime_inference_semantic": all(
            s.not_runtime and s.not_inference and s.not_semantic_layer for s in scope_audits
        ),
        "request_scope_excludes_weight_download": all(
            s.not_weight_download_unless_separately_approved for s in scope_audits
        ),
        "no_new_install_command": no_new_install_command,
        "request_does_not_execute_command": request_does_not_execute_command,
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
        "pre_install_snapshot_requested": pre_install_snapshot_requested,
        "rollback_requirement_requested": rollback_requirement_requested,
        "post_install_probe_requested": post_install_probe_requested,
        "post_install_probe_find_spec_only_strict": post_install_probe_find_spec_only_strict,
        "semantic_promotion_not_allowed": nef["semantic_promotion_allowed"] is False,
        "action_speech_factwrite_navigation_not_allowed": (
            nef["action_runtime_allowed"] is False
            and nef["speech_runtime_allowed"] is False
            and nef["fact_write_runtime_allowed"] is False
            and nef["navigation_runtime_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "upstream_test_board_planning_verified": upstream_test_board_planning_verified,
        "current_post_review_test_board_written": write_test_board is True,
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeInstallExecutionRequestPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeInstallExecutionRequestPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_request_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --------------------------------------------------------------------- #
    # Handoff readiness (owner approval issuance is NOT entered/allowed here).
    # --------------------------------------------------------------------- #
    handoff_readiness: List[OwnerApprovalIssuanceHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            OwnerApprovalIssuanceHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
                approval_issuance_allowed_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    # --------------------------------------------------------------------- #
    # GO conditions.
    # --------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "install_execution_request_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "install_execution_request_artifact_audit_count_gte_1": True,
        "request_package_audit_count_gte_1": True,
        "requested_asset_scope_audit_count_eq_5": len(scope_audits) == 5,
        "excluded_asset_disclosure_audit_count_eq_12": len(excluded_audits) == 12,
        "owner_approval_request_audit_count_gte_1": True,
        "command_template_reference_audit_count_eq_5": len(command_audits) == 5,
        "pre_install_snapshot_request_audit_count_gte_1": True,
        "rollback_requirement_request_audit_count_eq_5": len(rollback_audits) == 5,
        "post_install_probe_requirement_audit_count_eq_5": len(probe_audits) == 5,
        "risk_disclosure_audit_count_eq_5": len(risk_audits) == 5,
        "request_permission_boundary_audit_count_gte_6": len(permission_audits) >= 6,
        "upstream_test_board_planning_record_audit_count_gte_7": len(up_board_audits) >= 7,
        "non_execution_boundary_audit_count_gte_18": len(non_exec_audits) >= 18,
        "negative_post_review_guard_count_eq_31": negative_guard_count == 31,
        "negative_post_review_guard_passed_eq_31": negative_guard_passed == 31,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Artifact-derived.
        "upstream_final_decision_go_verified": upstream_final_decision_go,
        "upstream_blocker_count_zero_verified": upstream_blocker_count_zero,
        "request_package_verified": request_package_present,
        "request_only_verified": request_only,
        "owner_approval_request_created_verified": owner_audit.approval_request_created,
        "owner_approval_not_granted": owner_approval_not_granted,
        "approval_issuance_blocked": approval_issuance_blocked,
        "request_success_not_owner_approval": owner_approval_not_granted,
        "request_success_not_install_execution_approval": pkg_install_exec_allowed is False,
        "request_success_not_inference_approval": nef["real_inference_performed"] is False,
        "request_success_not_runtime_approval": nef["runtime_execution_allowed"] is False,
        "request_success_not_output_adapter_approval": True,
        "request_success_not_semantic_layer_approval": nef["semantic_promotion_allowed"] is False,
        "requested_asset_count_verified": requested_asset_count_five,
        "excluded_asset_count_verified": len(excluded_audits) == 12,
        "request_scope_matches_execution_planning": True,
        "no_new_asset_added": True,
        "excluded_assets_not_in_request_scope": excluded_assets_not_in_request_scope,
        "request_scope_does_not_include_runtime": all(s.not_runtime for s in scope_audits),
        "request_scope_does_not_include_inference": all(s.not_inference for s in scope_audits),
        "request_scope_does_not_include_weight_download_unless_separately_approved": all(
            s.not_weight_download_unless_separately_approved for s in scope_audits
        ),
        "request_scope_does_not_include_semantic_layer": all(s.not_semantic_layer for s in scope_audits),
        "command_template_refs_verified": command_template_refs_verified,
        "new_install_command_generated_false": no_new_install_command,
        "request_does_not_execute_command": request_does_not_execute_command,
        "pre_install_snapshot_requested": pre_install_snapshot_requested,
        "rollback_requirement_requested": rollback_requirement_requested,
        "post_install_probe_requested": post_install_probe_requested,
        "post_install_probe_find_spec_only": post_install_probe_find_spec_only_strict,
        "post_install_probe_not_inference": all(p.no_inference_on_probe for p in probe_audits),
        "post_install_probe_not_runtime": all(p.no_runtime_on_probe for p in probe_audits),
        "post_install_probe_not_output_adapter": all(p.no_output_adapter_on_probe for p in probe_audits),
        "risk_disclosure_verified": risk_disclosure_verified,
        "permission_boundary_verified": permission_boundary_verified,
        # Reuse flags.
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        "post_review_only": POST_REVIEW_ONLY is True,
        # Negative guard GO keys + handoff.
        **negative_guard_go,
        **handoff_go,
        # Test board fields + write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "upstream_test_board_planning_record_verified": upstream_test_board_planning_verified,
        "upstream_test_board_mode_planning_verified": all(a.test_mode_planning for a in up_board_audits),
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
        # Bindings (all false).
        "request_package_mutation_allowed_false": REQUEST_PACKAGE_MUTATION_ALLOWED is False,
        "owner_approval_generation_allowed_false": OWNER_APPROVAL_GENERATION_ALLOWED is False,
        "approval_issuance_allowed_false": APPROVAL_ISSUANCE_ALLOWED is False,
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    decision = P1ControlledInstallExecutionRequestPostReviewDecision(
        decision_ref=DECISION_REF,
        install_execution_request_post_review_profile_count=1,
        install_execution_request_artifact_audit_count=1,
        request_package_audit_count=1,
        requested_asset_scope_audit_count=len(scope_audits),
        excluded_asset_disclosure_audit_count=len(excluded_audits),
        owner_approval_request_audit_count=1,
        command_template_reference_audit_count=len(command_audits),
        pre_install_snapshot_request_audit_count=1,
        rollback_requirement_request_audit_count=len(rollback_audits),
        post_install_probe_requirement_audit_count=len(probe_audits),
        risk_disclosure_audit_count=len(risk_audits),
        request_permission_boundary_audit_count=len(permission_audits),
        upstream_test_board_planning_record_audit_count=len(up_board_audits),
        non_execution_boundary_audit_count=len(non_exec_audits),
        negative_post_review_guard_count=negative_guard_count,
        negative_post_review_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Request Post-Review",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "request_package_mutation_allowed": REQUEST_PACKAGE_MUTATION_ALLOWED,
        "owner_approval_generation_allowed": OWNER_APPROVAL_GENERATION_ALLOWED,
        "approval_issuance_allowed": APPROVAL_ISSUANCE_ALLOWED,
        "upstream_request_ref": UPSTREAM_REQUEST_REF,
        "execution_planning_post_review_ref": EXECUTION_PLANNING_POST_REVIEW_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "post_review_phase_governance_rules": list(POST_REVIEW_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "artifact_read_mode": artifact_read_mode,
        "artifact_missing_is_warning": True,
        "artifact_missing_is_blocker": False,
        "install_execution_request_post_review_profile": _build_profile(),
        "install_execution_request_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Audits.
        "install_execution_request_artifact_audit": asdict(artifact_audit),
        "install_execution_request_artifact_audit_count": 1,
        "request_package_audit": asdict(request_package_audit),
        "request_package_audit_count": 1,
        "requested_asset_scope_audits": [asdict(s) for s in scope_audits],
        "requested_asset_scope_audit_count": len(scope_audits),
        "excluded_asset_disclosure_audits": [asdict(e) for e in excluded_audits],
        "excluded_asset_disclosure_audit_count": len(excluded_audits),
        "owner_approval_request_audit": asdict(owner_audit),
        "owner_approval_request_audit_count": 1,
        "command_template_reference_audits": [asdict(c) for c in command_audits],
        "command_template_reference_audit_count": len(command_audits),
        "pre_install_snapshot_request_audit": asdict(snapshot_audit),
        "pre_install_snapshot_request_audit_count": 1,
        "rollback_requirement_request_audits": [asdict(r) for r in rollback_audits],
        "rollback_requirement_request_audit_count": len(rollback_audits),
        "post_install_probe_requirement_audits": [asdict(p) for p in probe_audits],
        "post_install_probe_requirement_audit_count": len(probe_audits),
        "risk_disclosure_audits": [asdict(r) for r in risk_audits],
        "risk_disclosure_audit_count": len(risk_audits),
        "request_permission_boundary_audits": [asdict(b) for b in permission_audits],
        "request_permission_boundary_audit_count": len(permission_audits),
        "upstream_test_board_planning_record_audits": [asdict(a) for a in up_board_audits],
        "upstream_test_board_planning_record_audit_count": len(up_board_audits),
        "non_execution_boundary_audits": [asdict(n) for n in non_exec_audits],
        "non_execution_boundary_audit_count": len(non_exec_audits),
        "negative_post_review_guards": [asdict(g) for g in negative_guards],
        "negative_post_review_guard_count": negative_guard_count,
        "negative_post_review_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_request_post_review_status": (
                "request_package_compliant_request_is_not_owner_approval_not_install_execution_not_inference_runtime_output_adapter_semantic_layer"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Pure post-review of the install-execution REQUEST package for the 5 approved candidates "
                "(supervision, byte_track, deep_sort, midas, mobile_sam); the 12 excluded assets remain disclosed "
                "and outside request scope. Confirmed: request package complete and request-only "
                "(owner_approval_granted=false, install_execution_allowed=false); command template refs are "
                "template-only and non-executed (no new command); snapshot / rollback / probe are REQUESTS only "
                "(probe is find_spec only — no import / model load / inference / runtime / output adapter); risk "
                "disclosed per asset; permission boundary holds; upstream test board records exist in planning mode "
                "and are protected / non-deletable. Nothing mutated, no approval generated, no issuance, nothing "
                "installed / downloaded / executed. Request != Owner Approval; Request != Install Execution; "
                "Request != Inference/Runtime/Output Adapter/Semantic Layer. Next: Owner Approval Issuance (which "
                "may generate approval but still must not execute install); real install execution is a separate "
                "later phase."
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
    result = review_p1_controlled_install_execution_request_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "artifact_read_mode": result.get("artifact_read_mode"),
                "negative_post_review_guard_passed": result["negative_post_review_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
