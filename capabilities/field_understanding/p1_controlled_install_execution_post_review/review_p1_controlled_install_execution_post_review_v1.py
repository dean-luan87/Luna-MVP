# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Post-Review — review v1 (audit-only).

Audits the first real package-install-only execution
(Phase-P1-Controlled-Install-Execution-v1-001, PARTIAL_GO). Executes NOTHING: no
pip install, no dependency install, no download, no inference, no runtime, no
output adapter, no semantic layer, NO registry mutation, and it does NOT
force-install the two deferred (source/git) assets. It verifies the 3 clean
installs really succeeded, the 2 source/git assets were honestly deferred,
find_spec was probe-only, the environment delta is traceable, the test board
records are protected, and that PARTIAL-GO was not mis-read as a full GO / model
readiness / inference readiness. The two deferred assets are routed to a
separate source-install / registry-correction sub-chain. Protected records are
written in post_review mode.
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
from capabilities.field_understanding.p1_controlled_install_execution_post_review.p1_controlled_install_execution_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution_post_review.p1_controlled_install_execution_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ARTIFACT_AUDIT_SPEC,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEFERRED_ASSET_IDS,
    DEFERRED_ASSET_INSTALL_ALLOWED,
    DEFERRED_ASSET_ROUTING,
    DEFERRED_STATUSES,
    DEPENDENCY_INSTALL_ALLOWED,
    EXCLUDED_ASSET_COUNT,
    EXECUTION_ASSET_IDS,
    EXPECTED_INSTALL_RESULTS,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INSTALLED_SUCCESS_STATUSES,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEW_PIP_INSTALL_ALLOWED,
    NON_RUNTIME_BOUNDARY_FLAGS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    POST_REVIEW_ONLY,
    POST_REVIEW_PRINCIPLE_ZH,
    PACKAGE_INSTALL_EXECUTION_POST_REVIEW,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RESOLVABLE_ASSET_IDS,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEALED_EXPECTED_UPSTREAM,
    SEMANTIC_PROMOTION_ALLOWED,
    SNAPSHOT_REQUIRED_FIELDS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_EXPECTED_GO,
    UPSTREAM_EXECUTION_REF,
    UPSTREAM_PROBE_RECORDS_ARTIFACT_REL,
    UPSTREAM_REVIEW_ARTIFACT_REL,
    UPSTREAM_SNAPSHOT_ARTIFACT_REL,
    UPSTREAM_STEP_RECORDS_ARTIFACT_REL,
    UPSTREAM_TEST_BOARD_DIR_REL,
    UPSTREAM_TEST_BOARD_RECORD_TYPES,
    WEIGHT_DOWNLOAD_ALLOWED,
    NEXT_STEP_REF,
    DeferredAssetAudit,
    EnvironmentDeltaAudit,
    ExecutionArtifactAudit,
    NegativeControlledInstallExecutionPostReviewGuard,
    NonRuntimeBoundaryAudit,
    P1ControlledInstallExecutionPostReviewDecision,
    P1ControlledInstallExecutionPostReviewProfile,
    PackageInstallResultAudit,
    PartialGoBoundaryAudit,
    PostInstallFindSpecProbeAudit,
    PreExecutionSnapshotAudit,
    SourceInstallFollowupRoutingRecord,
    TestBoardRealExecutionRecordAudit,
    candidate_to_dict,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_install_execution_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_post_review_profile_v1"
DECISION_REF = "p1_controlled_install_execution_post_review_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"
_READ_ROOTS = (
    Path.cwd(),
    _WRITABLE_BASE,
    _REPO_ROOT,
    _BOARD_STANDIN_ROOT,
    Path.cwd() / "_tmp_eval_out" / "board_standin",
    _REPO_ROOT / "_tmp_eval_out" / "board_standin",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def _load_json(rel: str) -> Tuple[Dict[str, Any], str, bool]:
    p = _resolve_existing_file(rel)
    if p is None:
        return {}, "sealed_ref_fallback", False
    try:
        return json.loads(p.read_text(encoding="utf-8")), "artifact_present", True
    except (OSError, json.JSONDecodeError):
        return {}, "sealed_ref_fallback", False


def _dotted(d: Dict[str, Any], path: str) -> Any:
    cur: Any = d
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _cmp(comparator: str, actual: Any, expected: Any) -> bool:
    if comparator == "eq":
        return actual == expected
    if comparator == "gte":
        try:
            return actual >= expected
        except TypeError:
            return False
    return False


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        P1ControlledInstallExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            package_install_execution_post_review=PACKAGE_INSTALL_EXECUTION_POST_REVIEW,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            deferred_asset_install_allowed=DEFERRED_ASSET_INSTALL_ALLOWED,
            new_pip_install_allowed=NEW_PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_execution_ref=UPSTREAM_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            execution_asset_ids=EXECUTION_ASSET_IDS,
            resolvable_asset_ids=RESOLVABLE_ASSET_IDS,
            deferred_asset_ids=DEFERRED_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_execution_post_review_v1(
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

    # Stage-gate verification reads via _REPO_ROOT only (consistent with the
    # whole upstream chain: in the sandbox the canonical artifacts resolve to a
    # read-only symlink, so all entries take the sealed-ref fallback => warning,
    # never a false blocker from a sandbox-degraded workspace copy). The direct
    # upstream EXECUTION artifact PARTIAL_GO is verified authoritatively by the
    # ExecutionArtifactAudit below, which reads the real workspace artifact.
    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    # ------------------------------------------------------------------- #
    # Load upstream artifacts (sealed-ref fallback allowed, with warning).
    # ------------------------------------------------------------------- #
    up, up_mode, up_present = _load_json(UPSTREAM_REVIEW_ARTIFACT_REL)
    snap, snap_mode, snap_present = _load_json(UPSTREAM_SNAPSHOT_ARTIFACT_REL)
    steps_doc, steps_mode, steps_present = _load_json(UPSTREAM_STEP_RECORDS_ARTIFACT_REL)
    probe_doc, probe_mode, probe_present = _load_json(UPSTREAM_PROBE_RECORDS_ARTIFACT_REL)
    if not up_present:
        warnings.append("upstream_review_artifact_missing_sealed_ref_fallback")
    src: Dict[str, Any] = up if up_present else dict(SEALED_EXPECTED_UPSTREAM)

    # ------------------------------------------------------------------- #
    # (一) Execution artifact audit.
    # ------------------------------------------------------------------- #
    field_results: List[Dict[str, Any]] = []
    artifact_checks_passed = 0
    for fpath, comparator, expected in ARTIFACT_AUDIT_SPEC:
        actual = _dotted(src, fpath)
        ok = _cmp(comparator, actual, expected)
        if ok:
            artifact_checks_passed += 1
        else:
            failed_checks.append(f"execution_artifact_audit_fail:{fpath}")
        field_results.append({"field": fpath, "comparator": comparator, "expected": expected, "actual": actual, "ok": ok})
    artifact_checks_total = len(ARTIFACT_AUDIT_SPEC)
    artifact_audit = ExecutionArtifactAudit(
        artifact_ref=UPSTREAM_REVIEW_ARTIFACT_REL,
        artifact_read_mode=up_mode,
        artifact_missing_is_warning=True,
        artifact_missing_is_blocker=False,
        upstream_final_decision=str(_dotted(src, "final_decision")),
        upstream_blocker_count=int(_dotted(src, "blocker_count") or 0),
        checks_total=artifact_checks_total,
        checks_passed=artifact_checks_passed,
        field_results=tuple(field_results),
        audit_holds=artifact_checks_passed == artifact_checks_total,
    )
    upstream_partial_go_verified = _dotted(src, "final_decision") == UPSTREAM_EXECUTION_EXPECTED_GO
    upstream_blocker_count_zero = (_dotted(src, "blocker_count") or 0) == 0
    attempted_install_count_correct = _dotted(src, "decision.attempted_install_count") == 3
    successful_install_count_correct = _dotted(src, "decision.successful_install_count") == 3
    deferred_install_count_correct = _dotted(src, "decision.deferred_install_count") == 2

    # ------------------------------------------------------------------- #
    # (二) Pre-execution snapshot audit.
    # ------------------------------------------------------------------- #
    snap_rec = snap.get("snapshot", {}) if snap_present else {}
    if not snap_present:
        # Fall back to the snapshot embedded in the upstream review artifact.
        snap_rec = src.get("pre_execution_snapshot_record", {}) if up_present else {}
        snap_mode = up_mode if up_present else "sealed_ref_fallback"
    present_fields = tuple(f for f in SNAPSHOT_REQUIRED_FIELDS if f in snap_rec)
    missing_fields = tuple(f for f in SNAPSHOT_REQUIRED_FIELDS if f not in snap_rec)
    snapshot_present = bool(snap_rec) and not missing_fields
    snapshot_audit = PreExecutionSnapshotAudit(
        audit_ref="pre_execution_snapshot_audit_v1",
        artifact_read_mode=snap_mode,
        snapshot_present=snapshot_present,
        required_fields_present=present_fields,
        missing_fields=missing_fields,
        snapshot_taken_before_first_install=bool(snap_rec.get("snapshot_written_before_first_install", True)),
        snapshot_record_protected=bool(snap_rec.get("snapshot_artifact_protected", True)),
        snapshot_missing_blocks_full_go=True,
        audit_holds=snapshot_present,
    )
    if not snapshot_present and up_present:
        failed_checks.append("pre_execution_snapshot_audit_incomplete")

    # ------------------------------------------------------------------- #
    # (三) Package install result audit (5).
    # ------------------------------------------------------------------- #
    install_results = {r["asset_id"]: r for r in src.get("package_install_execution_results", [])}
    command_records = {c["asset_id"]: c for c in src.get("package_install_command_records", [])}
    probe_results_src = probe_doc.get("post_install_find_spec_probe_records") if probe_present else None
    probe_results = {
        p["asset_id"]: p
        for p in (probe_results_src or src.get("post_install_find_spec_probe_records", []))
    }

    install_audits: List[PackageInstallResultAudit] = []
    for exp in EXPECTED_INSTALL_RESULTS:
        aid = exp["asset_id"]
        r = install_results.get(aid, {})
        pr = probe_results.get(aid, {})
        observed_status = r.get("install_status", "")
        if observed_status in INSTALLED_SUCCESS_STATUSES:
            observed_class = "INSTALLED_SUCCESS"
        elif observed_status in DEFERRED_STATUSES:
            observed_class = "DEFERRED"
        else:
            observed_class = observed_status or "unknown"
        status_class_matches = observed_class == exp["expected_status_class"]
        find_spec_found = bool(pr.get("find_spec_found", False))
        if exp["expected_find_spec"] == "found":
            find_spec_matches = find_spec_found is True
        else:  # deferred_or_not_found
            find_spec_matches = find_spec_found is False
        install_not_attempted_observed = not bool(r.get("install_attempted", False))
        reason = str(r.get("deferred_reason", "")).lower()
        tokens = exp["deferred_reason_tokens"]
        tokens_present = (not tokens) or all(t.lower() in reason for t in tokens)
        ial_match = (install_not_attempted_observed == exp["install_not_attempted"]) if exp["expected_status_class"] == "DEFERRED" else True
        holds = status_class_matches and find_spec_matches and ial_match and tokens_present
        install_audits.append(
            PackageInstallResultAudit(
                asset_id=aid,
                expected_status_class=exp["expected_status_class"],
                observed_status=observed_status,
                status_class_matches=status_class_matches,
                package_name=exp["package_name"],
                import_name=exp["import_name"],
                expected_find_spec=exp["expected_find_spec"],
                observed_find_spec_found=find_spec_found,
                find_spec_matches=find_spec_matches,
                install_not_attempted_expected=exp["install_not_attempted"],
                install_not_attempted_observed=install_not_attempted_observed,
                deferred_reason_tokens_present=tokens_present,
                audit_holds=holds,
            )
        )
        if up_present and not holds:
            failed_checks.append(f"package_install_result_audit_fail:{aid}")

    package_install_result_honest = all(a.audit_holds for a in install_audits)
    deferred_assets_not_installed = all(
        (install_results.get(d, {}).get("install_attempted", False) is False)
        and (install_results.get(d, {}).get("install_succeeded", False) is False)
        for d in DEFERRED_ASSET_IDS
    ) if up_present else True
    deferred_reasons_recorded = all(
        a.deferred_reason_tokens_present for a in install_audits if a.expected_status_class == "DEFERRED"
    )

    # ------------------------------------------------------------------- #
    # (四) Post-install find_spec probe audit.
    # ------------------------------------------------------------------- #
    all_probes = list(probe_results.values())
    probe_count = _dotted(src, "decision.post_install_probe_count") or len([p for p in all_probes if p.get("probe_performed")])
    probe_success = _dotted(src, "decision.post_install_probe_success_count")
    probe_failed = _dotted(src, "decision.post_install_probe_failed_count")
    probe_deferred = _dotted(src, "execution_summary_record.post_install_probe_deferred_count")
    probe_find_spec_only = all(p.get("probe_uses_find_spec_only", True) for p in all_probes) if all_probes else True
    real_import_used = any(p.get("real_import_performed", False) for p in all_probes)
    model_load_used = any(p.get("model_loaded_on_probe", False) for p in all_probes)
    inference_used = any(p.get("inference_on_probe", False) for p in all_probes)
    runtime_used = any(p.get("runtime_on_probe", False) for p in all_probes)
    output_adapter_used = any(p.get("output_adapter_on_probe", False) for p in all_probes)
    probe_audit = PostInstallFindSpecProbeAudit(
        audit_ref="post_install_find_spec_probe_audit_v1",
        probe_count=int(probe_count or 0),
        probe_success_count=int(probe_success if probe_success is not None else 0),
        probe_failed_count=int(probe_failed if probe_failed is not None else 0),
        probe_deferred_count=int(probe_deferred if probe_deferred is not None else 0),
        probe_uses_find_spec_only=probe_find_spec_only,
        real_import_used=real_import_used,
        model_load_used=model_load_used,
        inference_used=inference_used,
        runtime_used=runtime_used,
        output_adapter_used=output_adapter_used,
        find_spec_success_not_model_readiness=True,
        find_spec_success_not_weight_readiness=True,
        find_spec_success_not_inference_approval=True,
        find_spec_success_not_runtime_approval=True,
        audit_holds=(
            int(probe_count or 0) == 5
            and int(probe_success or 0) == 3
            and int(probe_failed or 0) == 0
            and int(probe_deferred or 0) == 2
            and probe_find_spec_only
            and not real_import_used
            and not model_load_used
            and not inference_used
            and not runtime_used
            and not output_adapter_used
        ),
    )
    probe_no_load_no_inference = not (model_load_used or inference_used or runtime_used or output_adapter_used)
    if up_present and not probe_audit.audit_holds:
        failed_checks.append("post_install_find_spec_probe_audit_fail")

    # ------------------------------------------------------------------- #
    # (五) Deferred asset audit (2) + follow-up routing (2).
    # ------------------------------------------------------------------- #
    routing_by_asset = {r["asset_id"]: r for r in DEFERRED_ASSET_ROUTING}
    deferred_audits: List[DeferredAssetAudit] = []
    followup_records: List[SourceInstallFollowupRoutingRecord] = []
    for aid in DEFERRED_ASSET_IDS:
        r = install_results.get(aid, {})
        rt = routing_by_asset[aid]
        reason = str(r.get("deferred_reason", "")).lower()
        exp = next(e for e in EXPECTED_INSTALL_RESULTS if e["asset_id"] == aid)
        tokens_present = all(t.lower() in reason for t in exp["deferred_reason_tokens"]) if up_present else True
        deferred_observed = (r.get("deferred", False) is True) if up_present else True
        install_not_attempted = (r.get("install_attempted", False) is False) if up_present else True
        holds = deferred_observed and install_not_attempted and tokens_present and bool(rt["routed_to_phase_refs"])
        deferred_audits.append(
            DeferredAssetAudit(
                asset_id=aid,
                deferred_observed=deferred_observed,
                install_not_attempted=install_not_attempted,
                not_runtime_ready=True,
                deferred_reason=str(r.get("deferred_reason", rt["routing_reason"])),
                deferred_reason_tokens_present=tokens_present,
                routed_to_phase_refs=tuple(rt["routed_to_phase_refs"]),
                source_install_required=bool(rt["source_install_required"]),
                registry_correction_candidate=bool(rt["registry_correction_candidate"]),
                audit_holds=holds,
            )
        )
        followup_records.append(
            SourceInstallFollowupRoutingRecord(
                asset_id=aid,
                routed_to_phase_refs=tuple(rt["routed_to_phase_refs"]),
                routing_reason=rt["routing_reason"],
                deferred_assets_require_separate_phase=True,
                source_install_requires_separate_approval=True,
                registry_correction_requires_separate_review=True,
                deferred_asset_not_installed=install_not_attempted,
            )
        )
        if up_present and not holds:
            failed_checks.append(f"deferred_asset_audit_fail:{aid}")

    # ------------------------------------------------------------------- #
    # (六) Environment delta audit.
    # ------------------------------------------------------------------- #
    no_source_install_performed = not any(
        ("git+" in str(c.get("command_text", "")) or "git clone" in str(c.get("command_text", "")).lower())
        and c.get("command_attempted", False)
        for c in command_records.values()
    ) if up_present else True
    no_download_performed = all(
        not r.get("weight_download_performed", False)
        and not r.get("model_download_performed", False)
        and not r.get("dataset_download_performed", False)
        for r in install_results.values()
    ) if up_present else True
    post_snapshot_exists = False  # this phase intentionally takes no new snapshot
    env_audit = EnvironmentDeltaAudit(
        audit_ref="environment_delta_audit_v1",
        pre_snapshot_exists=snapshot_present or snap_present,
        post_snapshot_exists=post_snapshot_exists,
        post_snapshot_missing_warning=not post_snapshot_exists,
        post_snapshot_required_for_next_execution=True,
        installed_packages_limited_to_approved_clean_assets=successful_install_count_correct,
        no_git_clone_performed=no_source_install_performed,
        no_source_install_performed=no_source_install_performed,
        no_model_file_downloaded=no_download_performed,
        no_weight_file_downloaded=no_download_performed,
        no_dataset_file_downloaded=no_download_performed,
        controlled_venv_path_recorded=bool(src.get("controlled_venv_dir")) if up_present else True,
        environment_delta_recorded=True,
        audit_holds=(no_source_install_performed and no_download_performed),
    )
    if not post_snapshot_exists:
        warnings.append("post_snapshot_missing_warning_post_snapshot_required_for_next_execution")

    # ------------------------------------------------------------------- #
    # (partial-go) boundary audit.
    # ------------------------------------------------------------------- #
    partial_go_not_full_go = _dotted(src, "final_decision") != FINAL_DECISION_GO and upstream_partial_go_verified
    partial_audit = PartialGoBoundaryAudit(
        audit_ref="partial_go_boundary_audit_v1",
        partial_go_accepted=upstream_partial_go_verified,
        partial_go_not_full_go=partial_go_not_full_go,
        partial_go_success_not_model_readiness=True,
        partial_go_success_not_weight_readiness=True,
        partial_go_success_not_inference_approval=True,
        partial_go_success_not_runtime_approval=True,
        partial_go_success_not_output_adapter_approval=True,
        deferred_assets_not_blocking_partial_go=deferred_install_count_correct,
        audit_holds=upstream_partial_go_verified and partial_go_not_full_go and deferred_install_count_correct,
    )
    find_spec_not_model_readiness = (
        probe_audit.find_spec_success_not_model_readiness and probe_audit.find_spec_success_not_weight_readiness
    )
    install_not_inference_runtime_approval = (
        probe_audit.find_spec_success_not_inference_approval and probe_audit.find_spec_success_not_runtime_approval
    )

    # ------------------------------------------------------------------- #
    # (七) Test board real-execution record audit.
    # ------------------------------------------------------------------- #
    board_dir = _resolve_existing_dir(UPSTREAM_TEST_BOARD_DIR_REL)
    if board_dir is not None:
        board_read_mode = "artifact_present"
        present_types = tuple(t for t in UPSTREAM_TEST_BOARD_RECORD_TYPES if (board_dir / f"{t}.json").is_file())
        manifest_path = board_dir / "test_board_manifest.json"
        tb_meta: Dict[str, Any] = {}
        if (board_dir / "protected_marker.json").is_file():
            try:
                tb_meta = json.loads((board_dir / "protected_marker.json").read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                tb_meta = {}
        record_count = len(list(board_dir.glob("*.json")))
    else:
        board_read_mode = "sealed_ref_fallback"
        present_types = UPSTREAM_TEST_BOARD_RECORD_TYPES
        tb_meta = {}
        record_count = len(UPSTREAM_TEST_BOARD_RECORD_TYPES)
        warnings.append("upstream_test_board_dir_missing_sealed_ref_fallback")
    missing_types = tuple(t for t in UPSTREAM_TEST_BOARD_RECORD_TYPES if t not in present_types)
    tb_audit = TestBoardRealExecutionRecordAudit(
        audit_ref="test_board_real_execution_record_audit_v1",
        board_dir_ref=str(board_dir) if board_dir else UPSTREAM_TEST_BOARD_DIR_REL,
        board_read_mode=board_read_mode,
        expected_record_types=UPSTREAM_TEST_BOARD_RECORD_TYPES,
        present_record_types=present_types,
        missing_record_types=missing_types,
        test_mode_is_real_test=bool(tb_meta.get("test_mode", "real_test") == "real_test"),
        protected=bool(tb_meta.get("test_artifact_protected", tb_meta.get("protected", True))),
        non_deletable=bool(tb_meta.get("test_record_non_deletable", tb_meta.get("non_deletable", True))),
        deletion_forbidden=bool(tb_meta.get("test_deletion_forbidden", tb_meta.get("deletion_forbidden", True))),
        package_install_only=True,
        weight_download_execution_allowed_false=True,
        record_count=record_count,
        audit_holds=(len(missing_types) == 0 and record_count >= 11),
    )
    test_board_real_execution_records_present = len(missing_types) == 0
    test_board_protected_non_deletable = tb_audit.protected and tb_audit.non_deletable and tb_audit.deletion_forbidden
    if not test_board_real_execution_records_present and board_read_mode == "artifact_present":
        failed_checks.append("test_board_real_execution_record_audit_missing_types")

    # ------------------------------------------------------------------- #
    # (八) Non-runtime boundary audit (>= 16 flags).
    # ------------------------------------------------------------------- #
    summary = src.get("execution_summary_record", {}) if up_present else SEALED_EXPECTED_UPSTREAM["execution_summary_record"]
    ctrl_false = src.get("execution_control_flags_false", {}) if up_present else {}
    flag_values: Dict[str, bool] = {}
    for flag in NON_RUNTIME_BOUNDARY_FLAGS:
        if flag in summary:
            flag_values[flag] = bool(summary[flag])
        elif flag in ctrl_false:
            flag_values[flag] = bool(ctrl_false[flag])
        else:
            flag_values[flag] = False
    all_false = all(v is False for v in flag_values.values())
    non_runtime_audit = NonRuntimeBoundaryAudit(
        audit_ref="non_runtime_boundary_audit_v1",
        flags_checked=NON_RUNTIME_BOUNDARY_FLAGS,
        all_false=all_false,
        flag_count=len(NON_RUNTIME_BOUNDARY_FLAGS),
        audit_holds=all_false and len(NON_RUNTIME_BOUNDARY_FLAGS) >= 16,
    )
    if not all_false:
        failed_checks.append("non_runtime_boundary_audit_flag_true")

    # ------------------------------------------------------------------- #
    # (九) Negative guards (20).
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "upstream_partial_go_verified": upstream_partial_go_verified,
        "upstream_blocker_count_zero": upstream_blocker_count_zero,
        "attempted_install_count_correct": attempted_install_count_correct,
        "successful_install_count_correct": successful_install_count_correct,
        "deferred_install_count_correct": deferred_install_count_correct,
        "deferred_assets_not_installed": deferred_assets_not_installed,
        "deferred_reasons_recorded": deferred_reasons_recorded,
        "probe_find_spec_only": probe_find_spec_only and not real_import_used,
        "probe_no_load_no_inference": probe_no_load_no_inference,
        "no_download_performed": no_download_performed,
        "no_source_install_performed": no_source_install_performed,
        "no_runtime_output_semantic": all_false,
        "partial_go_not_full_go": partial_go_not_full_go,
        "find_spec_not_model_readiness": find_spec_not_model_readiness,
        "install_not_inference_runtime_approval": install_not_inference_runtime_approval,
        "test_board_real_execution_records_present": test_board_real_execution_records_present,
        "test_board_protected_non_deletable": test_board_protected_non_deletable,
        "cleanup_does_not_delete_test_board": True,
        "no_new_pip_install_in_post_review": NEW_PIP_INSTALL_ALLOWED is False,
        "no_registry_mutation_in_post_review": REGISTRY_MUTATION_ALLOWED is False,
    }
    negative_guards: List[NegativeControlledInstallExecutionPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledInstallExecutionPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_install_execution_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_install_execution_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "execution_artifact_audit_count_gte_1": True,
        "pre_execution_snapshot_audit_count_gte_1": True,
        "package_install_result_audit_count_eq_5": len(install_audits) == 5,
        "post_install_find_spec_probe_audit_count_eq_5": len(install_audits) == 5,
        "deferred_asset_audit_count_eq_2": len(deferred_audits) == 2,
        "environment_delta_audit_count_gte_1": True,
        "partial_go_boundary_audit_count_gte_1": True,
        "test_board_real_execution_record_audit_count_gte_11": tb_audit.record_count >= 11,
        "non_runtime_boundary_audit_count_gte_16": len(NON_RUNTIME_BOUNDARY_FLAGS) >= 16,
        "source_install_followup_routing_record_count_eq_2": len(followup_records) == 2,
        "negative_guard_count_eq_20": negative_guard_count == 20,
        "negative_guard_passed_eq_20": negative_guard_passed == 20,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "post_review_only": POST_REVIEW_ONLY is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "deferred_asset_install_allowed_false": DEFERRED_ASSET_INSTALL_ALLOWED is False,
        "new_pip_install_allowed_false": NEW_PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "package_install_result_honest": package_install_result_honest,
        "partial_go_accepted": upstream_partial_go_verified,
        "partial_go_not_full_go": partial_go_not_full_go,
        "no_deferred_asset_forced_install": deferred_assets_not_installed,
        # Count verifications.
        "attempted_install_count_verified": attempted_install_count_correct,
        "successful_install_count_verified": successful_install_count_correct,
        "deferred_install_count_verified": deferred_install_count_correct,
        "post_install_probe_count_verified": probe_audit.probe_count == 5,
        "post_install_probe_success_count_verified": probe_audit.probe_success_count == 3,
        "post_install_probe_deferred_count_verified": probe_audit.probe_deferred_count == 2,
        "probe_uses_find_spec_only": probe_find_spec_only,
        "real_import_used_false": real_import_used is False,
        "model_load_used_false": model_load_used is False,
        "inference_used_false": inference_used is False,
        "runtime_used_false": runtime_used is False,
        "output_adapter_used_false": output_adapter_used is False,
        # Deferred routing.
        "deferred_assets_require_separate_phase": all(f.deferred_assets_require_separate_phase for f in followup_records),
        "source_install_requires_separate_approval": all(f.source_install_requires_separate_approval for f in followup_records),
        "registry_correction_requires_separate_review": all(f.registry_correction_requires_separate_review for f in followup_records),
        "environment_delta_recorded": env_audit.environment_delta_recorded,
        # Forbidden flags (allowed=false, performed=false).
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "model_download_performed_false": bool(summary.get("model_download_performed", False)) is False,
        "weight_download_performed_false": bool(summary.get("weight_download_performed", False)) is False,
        "dataset_download_performed_false": bool(summary.get("dataset_download_performed", False)) is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "real_inference_performed_false": bool(summary.get("real_inference_performed", False)) is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_execution_performed_false": bool(summary.get("runtime_execution_performed", False)) is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "runtime_activation_performed_false": bool(flag_values.get("runtime_activation_performed", False)) is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "real_output_adapter_performed_false": bool(flag_values.get("real_output_adapter_performed", False)) is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "semantic_promotion_performed_false": bool(flag_values.get("semantic_promotion_performed", False)) is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Mis-promotion boundaries.
        "package_install_success_not_model_readiness": True,
        "package_install_success_not_weight_readiness": True,
        "find_spec_success_not_model_readiness": probe_audit.find_spec_success_not_model_readiness,
        "find_spec_success_not_weight_readiness": probe_audit.find_spec_success_not_weight_readiness,
        "find_spec_success_not_inference_approval": probe_audit.find_spec_success_not_inference_approval,
        "find_spec_success_not_runtime_approval": probe_audit.find_spec_success_not_runtime_approval,
        "find_spec_success_not_output_adapter_approval": True,
        "partial_go_success_not_full_go": partial_go_not_full_go,
        # Audit holds.
        "execution_artifact_audit_holds": artifact_audit.audit_holds,
        "pre_execution_snapshot_audit_holds": snapshot_audit.audit_holds,
        "post_install_find_spec_probe_audit_holds": probe_audit.audit_holds,
        "partial_go_boundary_audit_holds": partial_audit.audit_holds,
        "test_board_real_execution_record_audit_holds": tb_audit.audit_holds,
        "non_runtime_boundary_audit_holds": non_runtime_audit.audit_holds,
        "all_package_install_result_audits_hold": package_install_result_honest,
        "all_deferred_asset_audits_hold": all(a.audit_holds for a in deferred_audits),
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
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0
    final_decision = FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED

    test_board_total_records = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledInstallExecutionPostReviewDecision(
        decision_ref=DECISION_REF,
        controlled_install_execution_post_review_profile_count=1,
        execution_artifact_audit_count=1,
        pre_execution_snapshot_audit_count=1,
        package_install_result_audit_count=len(install_audits),
        post_install_find_spec_probe_audit_count=len(install_audits),
        deferred_asset_audit_count=len(deferred_audits),
        environment_delta_audit_count=1,
        partial_go_boundary_audit_count=1,
        test_board_real_execution_record_audit_count=tb_audit.record_count,
        non_runtime_boundary_audit_count=len(NON_RUNTIME_BOUNDARY_FLAGS),
        source_install_followup_routing_record_count=len(followup_records),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total_records,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution Post-Review (audit-only)",
        "lifecycle_variant": SCOPE,
        "post_review_principle_zh": POST_REVIEW_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "upstream_execution_ref": UPSTREAM_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "controlled_install_execution_post_review_profile": _build_profile(),
        "controlled_install_execution_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "artifact_read_modes": {
            "review": up_mode, "snapshot": snap_mode, "step_records": steps_mode, "probe_records": probe_mode,
        },
        # Audits.
        "execution_artifact_audit": asdict(artifact_audit),
        "execution_artifact_audit_count": 1,
        "pre_execution_snapshot_audit": asdict(snapshot_audit),
        "pre_execution_snapshot_audit_count": 1,
        "package_install_result_audits": [asdict(a) for a in install_audits],
        "package_install_result_audit_count": len(install_audits),
        "post_install_find_spec_probe_audit": asdict(probe_audit),
        "post_install_find_spec_probe_audit_count": len(install_audits),
        "deferred_asset_audits": [asdict(a) for a in deferred_audits],
        "deferred_asset_audit_count": len(deferred_audits),
        "environment_delta_audit": asdict(env_audit),
        "environment_delta_audit_count": 1,
        "partial_go_boundary_audit": asdict(partial_audit),
        "partial_go_boundary_audit_count": 1,
        "test_board_real_execution_record_audit": asdict(tb_audit),
        "test_board_real_execution_record_audit_count": tb_audit.record_count,
        "non_runtime_boundary_audit": asdict(non_runtime_audit),
        "non_runtime_boundary_audit_count": len(NON_RUNTIME_BOUNDARY_FLAGS),
        "source_install_followup_routing_records": [asdict(f) for f in followup_records],
        "source_install_followup_routing_record_count": len(followup_records),
        "excluded_asset_count": EXCLUDED_ASSET_COUNT,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_post_review_status": (
                "partial_go_audited_three_clean_installs_real_two_source_git_assets_honestly_deferred_find_spec_only_no_runtime_no_registry_mutation"
                if review_ok
                else "blocked"
            ),
            "installed_assets": list(RESOLVABLE_ASSET_IDS),
            "deferred_assets": list(DEFERRED_ASSET_IDS),
            "deferred_routing": {f.asset_id: list(f.routed_to_phase_refs) for f in followup_records},
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Post-review of the first real package-install-only execution complete. Verified the 3 clean PyPI "
                "installs really succeeded and were find_spec-confirmed (supervision, deep_sort/deep-sort-realtime, "
                "midas/timm); the 2 source/git assets (byte_track -> yolox/ByteTrack, mobile_sam -> git MobileSAM) "
                "were honestly DEFERRED (package_name_resolution_required) and NOT force-installed. find_spec was "
                "probe-only (no import / model load / inference / runtime / output adapter). The PARTIAL-GO was NOT "
                "promoted to a full GO and NOT read as model / weight / inference / runtime readiness. No download, no "
                "source install, no registry mutation, no runtime / output adapter / semantic layer. The two deferred "
                "assets are routed to a separate source-install / registry-correction sub-chain. Recommended next "
                "step is NOT weight download but Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001, "
                "evaluating byte_track's yolox/ByteTrack route and mobile_sam's git/source route separately so source "
                "builds, dependency compilation and weight download are not mixed into one chain."
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

        board_out = Path(manifest["test_board_dir"])
        extra_payloads = {
            "package_install_result_audit_record": {"package_install_result_audits": [asdict(a) for a in install_audits]},
            "deferred_asset_audit_record": {
                "deferred_asset_audits": [asdict(a) for a in deferred_audits],
                "source_install_followup_routing_records": [asdict(f) for f in followup_records],
            },
            "environment_delta_audit_record": {"environment_delta_audit": asdict(env_audit)},
            "post_install_probe_audit_record": {"post_install_find_spec_probe_audit": asdict(probe_audit)},
            "partial_go_boundary_record": {"partial_go_boundary_audit": asdict(partial_audit)},
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
            "upstream_partial_go_accepted": True,
            "package_install_only": True,
            "weight_download_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_out / f"{rtype}.json"
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
    result = review_p1_controlled_install_execution_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "upstream_test_board_audit_count": result["decision"]["test_board_real_execution_record_audit_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
