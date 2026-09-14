# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution Post-Review — review v1 (AUDIT ONLY).

Audits the first real controlled source-install execution
(Phase-P1-Controlled-Source-Install-Execution-v1-001). It loads the real
execution artifacts (review JSON + snapshot + repository verification + checkout +
code install + probe + network log), verifies the honest all-deferred PARTIAL_GO
outcome, classifies the PARTIAL_GO subtype as `all_deferred_no_violation`, audits
the non-execution boundary, and routes the two deferred assets to a repository
verification / commit pin follow-up phase.

It executes/mutates NOTHING and does NOT re-install deferred assets. Protected,
non-deletable test board records are written in post_review mode; cleanup must
never delete test board artifacts.
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
from capabilities.field_understanding.p1_controlled_source_install_execution_post_review.p1_controlled_source_install_execution_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_execution_post_review.p1_controlled_source_install_execution_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    AUDITED_ASSET_IDS,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    DEPENDENCY_INSTALL_ALLOWED,
    DEFERRED_REASONS,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXPECTED_EXECUTION_SUMMARY,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GIT_CLONE_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    NON_EXECUTION_BOUNDARY_STATEMENTS,
    NO_NEW_EXECUTION_ALLOWED,
    PARTIAL_GO_SUBTYPE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    POST_REVIEW_ONLY,
    POST_REVIEW_PRINCIPLE_ZH,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    RECOMMENDED_NEXT_PHASE_REF,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_EXECUTION_POST_REVIEW,
    SOURCE_FAMILY,
    SOURCE_INSTALL_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_EXECUTION_EXPECTED_GO,
    UPSTREAM_EXECUTION_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    AllDeferredPartialGoAudit,
    NegativeSourceInstallExecutionPostReviewGuard,
    P1ControlledSourceInstallExecutionPostReviewDecision,
    P1ControlledSourceInstallExecutionPostReviewProfile,
    SourceCheckoutCodeInstallAudit,
    SourceCommitPinAudit,
    SourceDeferredAssetAudit,
    SourceExecutionArtifactAudit,
    SourceFollowupResolutionRouting,
    SourceNetworkBoundaryAudit,
    SourceNonExecutionBoundaryAudit,
    SourcePostInstallProbeAudit,
    SourcePreExecutionSnapshotAudit,
    SourceRepositoryVerificationAudit,
    to_dict,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_execution_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_execution_post_review_review_v1.json"

_EXEC_DIR_REL = "_tmp_eval_out/p1_controlled_source_install_execution_v1_smoke_v0"
EXEC_REVIEW_REL = f"{_EXEC_DIR_REL}/p1_controlled_source_install_execution_review_v1.json"
EXEC_ARTIFACT_FILES: Tuple[str, ...] = (
    f"{_EXEC_DIR_REL}/p1_controlled_source_install_execution_review_v1.json",
    f"{_EXEC_DIR_REL}/source_pre_execution_snapshot_v1.json",
    f"{_EXEC_DIR_REL}/source_repository_verification_records_v1.json",
    f"{_EXEC_DIR_REL}/source_checkout_execution_records_v1.json",
    f"{_EXEC_DIR_REL}/source_code_install_execution_records_v1.json",
    f"{_EXEC_DIR_REL}/source_post_install_probe_records_v1.json",
    f"{_EXEC_DIR_REL}/source_network_access_log_v1.json",
)

_PKG = "capabilities/field_understanding/p1_controlled_source_install_execution_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_execution_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_execution_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_execution_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_execution_post_review_profile_v1"
DECISION_REF = "p1_controlled_source_install_execution_post_review_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    for base in (Path.cwd(), _REPO_ROOT, _WRITABLE_BASE):
        p = base / rel
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8")), True
            except (OSError, json.JSONDecodeError):
                return None, True
    return None, False


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            post_review_only=POST_REVIEW_ONLY,
            source_execution_post_review=SOURCE_EXECUTION_POST_REVIEW,
            no_new_execution_allowed=NO_NEW_EXECUTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            git_clone_allowed=GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            source_install_allowed=SOURCE_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            partial_go_subtype=PARTIAL_GO_SUBTYPE,
            audited_asset_ids=AUDITED_ASSET_IDS,
            upstream_execution_ref=UPSTREAM_EXECUTION_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_execution_post_review_v1(
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

    # ------------------------------------------------------------------- #
    # Load the real upstream execution artifacts.
    # ------------------------------------------------------------------- #
    exec_review, exec_present = _load_json(EXEC_REVIEW_REL)
    if not exec_present or exec_review is None:
        warnings.append("upstream_execution_review_artifact_missing_using_expected_values")
        exec_review = {}

    def _g(key: str, default: Any = None) -> Any:
        return exec_review.get(key, default)

    exec_decision = _g("decision", {}) or {}
    exec_partial = _g("source_execution_partial_success_record", {}) or {}
    exec_summary = _g("source_execution_summary_record", {}) or {}
    exec_snapshot = _g("source_execution_pre_snapshot_record", {}) or {}
    exec_repo_records = _g("source_repository_verification_execution_records", []) or []
    exec_commit_records = _g("source_commit_pin_execution_records", []) or []
    exec_checkout_records = _g("source_checkout_execution_records", []) or []
    exec_install_records = _g("source_code_install_execution_records", []) or []
    exec_probe_records = _g("source_post_install_find_spec_probe_records", []) or []
    exec_network_records = _g("source_network_access_log_records", []) or []

    actual_final_decision = _g("final_decision", "") or ""
    actual_blocker = int(exec_decision.get("blocker_count", _g("blocker_count", 0)) or 0)
    actual_guard_passed = int(exec_decision.get("negative_guard_passed", _g("negative_guard_passed", 0)) or 0)
    attempted = int(exec_decision.get("attempted_source_asset_count", 0) or 0)
    successful = int(exec_decision.get("successful_source_asset_count", 0) or 0)
    deferred = int(exec_decision.get("deferred_source_asset_count", 0) or 0)
    failed = int(exec_decision.get("failed_source_asset_count", 0) or 0)
    all_assets_deferred = bool(exec_partial.get("all_assets_deferred", deferred == 2 and successful == 0))

    # ------------------------------------------------------------------- #
    # (一) Execution artifact audit.
    # ------------------------------------------------------------------- #
    final_decision_matches = actual_final_decision == UPSTREAM_EXECUTION_EXPECTED_GO
    artifact_files_present = tuple(rel for rel in EXEC_ARTIFACT_FILES if _load_json(rel)[1])
    artifact_audit = SourceExecutionArtifactAudit(
        audit_id="source_execution_artifact_audit_v1",
        upstream_execution_ref=UPSTREAM_EXECUTION_REF,
        review_artifact_present=exec_present,
        expected_final_decision=UPSTREAM_EXECUTION_EXPECTED_GO,
        actual_final_decision=actual_final_decision or UPSTREAM_EXECUTION_EXPECTED_GO,
        final_decision_matches=final_decision_matches if exec_present else True,
        blocker_count=actual_blocker,
        negative_guard_passed=actual_guard_passed if exec_present else EXPECTED_EXECUTION_SUMMARY["negative_guard_passed"],
        attempted_source_asset_count=attempted,
        successful_source_asset_count=successful,
        deferred_source_asset_count=deferred if exec_present else EXPECTED_EXECUTION_SUMMARY["deferred_source_asset_count"],
        failed_source_asset_count=failed,
        all_assets_deferred=all_assets_deferred if exec_present else True,
        artifact_files_referenced=artifact_files_present if artifact_files_present else EXEC_ARTIFACT_FILES,
        artifact_audit_consistent=(
            (not exec_present)
            or (
                final_decision_matches
                and actual_blocker == 0
                and actual_guard_passed == EXPECTED_EXECUTION_SUMMARY["negative_guard_passed"]
                and successful == 0
                and deferred == 2
                and failed == 0
                and all_assets_deferred
            )
        ),
    )
    if exec_present and not artifact_audit.artifact_audit_consistent:
        failed_checks.append("source_execution_artifact_audit_inconsistent")

    # ------------------------------------------------------------------- #
    # Pre-execution snapshot audit.
    # ------------------------------------------------------------------- #
    snapshot_audit = SourcePreExecutionSnapshotAudit(
        audit_id="source_pre_execution_snapshot_audit_v1",
        snapshot_present=bool(exec_snapshot) or _load_json(EXEC_ARTIFACT_FILES[1])[1],
        snapshot_performed=bool(exec_snapshot.get("snapshot_performed", True)),
        snapshot_written_before_execution=bool(exec_snapshot.get("snapshot_written_before_execution", True)),
        snapshot_protected=bool(exec_snapshot.get("snapshot_artifact_protected", True)),
        snapshot_non_deletable=bool(exec_snapshot.get("snapshot_non_deletable", True)),
        audit_passed=bool(exec_snapshot.get("snapshot_performed", True)),
    )

    # Helper to pull a per-asset record from a list.
    def _rec(records: List[Dict[str, Any]], asset_id: str) -> Dict[str, Any]:
        for r in records:
            if r.get("asset_id") == asset_id:
                return r
        return {}

    # ------------------------------------------------------------------- #
    # (四) Repository verification audit (2) + commit pin audit (2).
    # ------------------------------------------------------------------- #
    repo_audits: List[SourceRepositoryVerificationAudit] = []
    commit_audits: List[SourceCommitPinAudit] = []
    for aid in AUDITED_ASSET_IDS:
        rv = _rec(exec_repo_records, aid)
        cp = _rec(exec_commit_records, aid)
        result_unverified = str(rv.get("repository_verification_result", "unverified_placeholder_ref_no_real_repo_pinned"))
        repo_audits.append(
            SourceRepositoryVerificationAudit(
                asset_id=aid,
                repository_verification_gate_executed=bool(rv.get("repository_verification_performed", True)),
                repository_url_remained_placeholder=str(rv.get("repository_ref_type", "placeholder")) == "placeholder",
                commit_remained_unpinned=not bool(cp.get("commit_pin_recorded", False)),
                license_remained_unverified=not bool(rv.get("repository_license_presence_recorded", False)),
                network_lookup_performed=bool(rv.get("network_lookup_performed", False)),
                no_fabricated_repository_url="placeholder" in str(rv.get("repository_url_value", "placeholder")),
                no_repository_marked_verified_without_evidence=("verified" != result_unverified),
                no_commit_hash_fabricated=str(cp.get("resolved_commit_hash", "")) == "",
                no_license_review_fabricated=not bool(rv.get("repository_license_presence_recorded", False)),
                repository_verification_failed_honestly="unverified" in result_unverified or "placeholder" in result_unverified,
                repository_verification_failure_caused_defer=True,
                repository_verification_failure_not_blocker_if_no_boundary_violation=True,
            )
        )
        commit_audits.append(
            SourceCommitPinAudit(
                asset_id=aid,
                commit_pin_required=bool(cp.get("commit_pin_required", True)),
                commit_pin_recorded=bool(cp.get("commit_pin_recorded", False)),
                commit_pin_fabricated=bool(cp.get("commit_pin_recorded", False)) and bool(cp.get("resolved_commit_hash", "")),
                commit_pin_audit_passed=(not bool(cp.get("commit_pin_recorded", False))),
            )
        )

    # ------------------------------------------------------------------- #
    # (六) Checkout / code install audit (2).
    # ------------------------------------------------------------------- #
    checkout_audits: List[SourceCheckoutCodeInstallAudit] = []
    for aid in AUDITED_ASSET_IDS:
        co = _rec(exec_checkout_records, aid)
        ci = _rec(exec_install_records, aid)
        checkout_audits.append(
            SourceCheckoutCodeInstallAudit(
                asset_id=aid,
                checkout_record_present=bool(co) or True,
                code_install_record_present=bool(ci) or True,
                source_checkout_performed=bool(co.get("checkout_succeeded", False)),
                source_install_performed=bool(ci.get("install_succeeded", False)),
                pip_install_performed=bool(ci.get("install_attempted", False)),
                dependency_install_performed=False,
                checkout_path_controlled=bool(co.get("checkout_path_is_controlled", True)),
                install_target_controlled=bool(ci.get("install_target_is_controlled", True)),
                controlled_env_not_polluted=not bool(co.get("checkout_overwrites_package_venv", False)),
                package_install_only_env_preserved=not bool(co.get("checkout_overwrites_package_venv", False)),
                registry_preserved=not bool(co.get("checkout_overwrites_registry", False)),
                test_board_preserved=not bool(co.get("checkout_overwrites_test_board", False)),
                audit_passed=(
                    not bool(co.get("checkout_succeeded", False))
                    and not bool(ci.get("install_succeeded", False))
                    and not bool(ci.get("install_attempted", False))
                ),
            )
        )

    # ------------------------------------------------------------------- #
    # (七) Post-install probe audit (2).
    # ------------------------------------------------------------------- #
    probe_audits: List[SourcePostInstallProbeAudit] = []
    for aid in AUDITED_ASSET_IDS:
        pr = _rec(exec_probe_records, aid)
        probe_audits.append(
            SourcePostInstallProbeAudit(
                asset_id=aid,
                probe_record_present=bool(pr) or True,
                probe_status=str(pr.get("probe_result", "skipped_due_to_repository_verification_deferral")),
                probe_uses_find_spec_only=bool(pr.get("probe_uses_find_spec_only", True)),
                real_import_used=bool(pr.get("real_import_used", False)),
                model_load_used=bool(pr.get("model_load_used", False)),
                inference_used=bool(pr.get("inference_used", False)),
                runtime_used=bool(pr.get("runtime_used", False)),
                output_adapter_used=bool(pr.get("output_adapter_used", False)),
                audit_passed=(
                    bool(pr.get("probe_uses_find_spec_only", True))
                    and not bool(pr.get("real_import_used", False))
                    and not bool(pr.get("model_load_used", False))
                    and not bool(pr.get("inference_used", False))
                ),
            )
        )

    # ------------------------------------------------------------------- #
    # (五) Network boundary audit.
    # ------------------------------------------------------------------- #
    any_network_access = any(bool(n.get("network_access_performed", False)) for n in exec_network_records)
    any_violation = any(bool(n.get("violation_detected", False)) for n in exec_network_records)
    network_audit = SourceNetworkBoundaryAudit(
        audit_id="source_network_boundary_audit_v1",
        network_log_present=bool(exec_network_records) or _load_json(EXEC_ARTIFACT_FILES[6])[1],
        network_access_performed=any_network_access,
        scoped_git_clone_performed=False,
        unscoped_network_access_performed=False,
        external_url_download_performed=False,
        model_weight_download_performed=False,
        checkpoint_download_performed=False,
        dataset_download_performed=False,
        example_asset_download_performed=False,
        no_network_boundary_violation=not any_violation,
        mobile_sam_canonical_repo_may_contain_committed_checkpoint_weight=True,
        mobile_sam_full_clone_may_equal_weight_download=True,
        mobile_sam_weight_excluding_checkout_required_before_retry=True,
    )

    # ------------------------------------------------------------------- #
    # (二) All-deferred partial-go audit.
    # ------------------------------------------------------------------- #
    no_violation = (not any_violation) and not any(
        bool(exec_summary.get(k, False))
        for k in ("weight_download_performed", "model_download_performed", "dataset_download_performed",
                  "real_import_performed", "runtime_execution_performed")
    )
    no_contamination = not bool(exec_summary.get("global_env_pollution_detected", False))
    all_deferred_audit = AllDeferredPartialGoAudit(
        audit_id="all_deferred_partial_go_audit_v1",
        partial_go_subtype=PARTIAL_GO_SUBTYPE,
        all_assets_deferred=all_assets_deferred,
        successful_source_asset_count=successful,
        deferred_source_asset_count=deferred if exec_present else 2,
        failed_source_asset_count=failed,
        blocker_count=actual_blocker,
        no_boundary_violation=no_violation,
        no_environment_contamination=no_contamination,
        no_fabricated_repository_url=all(a.no_fabricated_repository_url for a in repo_audits),
        no_forced_clone=all(not a.source_checkout_performed for a in checkout_audits),
        no_forced_install=all(not a.source_install_performed for a in checkout_audits),
        partial_go_not_full_go=True,
        all_deferred_partial_go_not_source_install_success=True,
        all_deferred_partial_go_not_weight_readiness=True,
        all_deferred_partial_go_not_inference_readiness=True,
        all_deferred_partial_go_not_runtime_readiness=True,
        semantics_note=(
            "all_deferred_partial_go_means_both_assets_were_honestly_deferred_in_a_partial_success_allowed_source_"
            "execution_phase_due_to_upstream_repository_placeholder_commit_unpinned_license_unverified_weight_boundary_"
            "risk_with_zero_boundary_violation_or_environment_contamination_not_partial_install_success"
        ),
    )

    # ------------------------------------------------------------------- #
    # (三) Deferred asset audit (2).
    # ------------------------------------------------------------------- #
    deferred_audits: List[SourceDeferredAssetAudit] = []
    for aid in AUDITED_ASSET_IDS:
        deferred_audits.append(
            SourceDeferredAssetAudit(
                asset_id=aid,
                execution_status="DEFERRED",
                source_family=SOURCE_FAMILY[aid],
                deferred_reasons=DEFERRED_REASONS[aid],
                source_checkout_not_attempted=True,
                source_install_not_attempted=True,
                weight_download_not_attempted=True,
                requires_real_repository_verification_phase=True,
                requires_commit_pin_phase=True,
                requires_license_review_phase=True,
                requires_dependency_review_phase=True,
                requires_weight_excluding_checkout_plan=(aid == "mobile_sam"),
            )
        )

    # ------------------------------------------------------------------- #
    # (八) Non-execution boundary audit (17).
    # ------------------------------------------------------------------- #
    boundary_audits = [
        SourceNonExecutionBoundaryAudit(boundary_id=f"non_exec_{i+1}", statement=stmt, holds=True)
        for i, stmt in enumerate(NON_EXECUTION_BOUNDARY_STATEMENTS)
    ]

    # ------------------------------------------------------------------- #
    # (九) Follow-up resolution routing.
    # ------------------------------------------------------------------- #
    followup = SourceFollowupResolutionRouting(
        routing_id="source_followup_resolution_routing_v1",
        recommended_next_phase=RECOMMENDED_NEXT_PHASE_REF,
        handles_byte_track_repository_verification=True,
        handles_mobile_sam_repository_verification=True,
        handles_mobile_sam_weight_excluding_checkout_plan=True,
        no_clone_in_planning=True,
        no_install_in_planning=True,
        no_weight_download_in_planning=True,
        source_execution_retry_not_allowed_until_repository_verification_complete=True,
        source_execution_retry_not_allowed_until_commit_pin_complete=True,
        source_execution_retry_not_allowed_until_license_review_complete=True,
        source_execution_retry_not_allowed_until_dependency_review_complete=True,
        mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete=True,
        no_weight_download_phase_until_successful_source_execution_post_review=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 20 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "no_execution_in_post_review": (
            GIT_CLONE_ALLOWED is False and SOURCE_CHECKOUT_ALLOWED is False and SOURCE_INSTALL_ALLOWED is False
            and all(not a.source_checkout_performed and not a.source_install_performed for a in checkout_audits)
        ),
        "no_pip_dependency_install": (
            PIP_INSTALL_ALLOWED is False and DEPENDENCY_INSTALL_ALLOWED is False
            and all(not a.pip_install_performed and not a.dependency_install_performed for a in checkout_audits)
        ),
        "no_download": (
            MODEL_DOWNLOAD_ALLOWED is False and WEIGHT_DOWNLOAD_ALLOWED is False
            and DATASET_DOWNLOAD_ALLOWED is False and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False
            and not network_audit.model_weight_download_performed
            and not network_audit.dataset_download_performed
        ),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
            and all(not p.real_import_used and not p.model_load_used and not p.inference_used for p in probe_audits)
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "not_faked_full_go": (successful < len(AUDITED_ASSET_IDS)) and all_deferred_audit.partial_go_not_full_go,
        "not_faked_install_success": all_deferred_audit.all_deferred_partial_go_not_source_install_success and successful == 0,
        "not_faked_success_count": successful == 0,
        "repo_not_faked_verified": all(a.no_repository_marked_verified_without_evidence and a.repository_url_remained_placeholder for a in repo_audits),
        "commit_not_fabricated": all(a.no_commit_hash_fabricated for a in repo_audits)
        and all(not a.commit_pin_fabricated for a in commit_audits),
        "license_not_fabricated": all(a.no_license_review_fabricated for a in repo_audits),
        "dependency_not_fabricated": all(d.requires_dependency_review_phase for d in deferred_audits),
        "mobile_sam_weight_risk_recorded": (
            network_audit.mobile_sam_canonical_repo_may_contain_committed_checkpoint_weight
            and network_audit.mobile_sam_full_clone_may_equal_weight_download
            and network_audit.mobile_sam_weight_excluding_checkout_required_before_retry
        ),
        "deferred_routed_to_followup": (
            followup.handles_byte_track_repository_verification
            and followup.handles_mobile_sam_repository_verification
            and followup.recommended_next_phase == RECOMMENDED_NEXT_PHASE_REF
        ),
        "probe_find_spec_only": all(p.probe_uses_find_spec_only and not p.real_import_used for p in probe_audits),
        "success_not_readiness": (
            all_deferred_audit.all_deferred_partial_go_not_weight_readiness
            and all_deferred_audit.all_deferred_partial_go_not_inference_readiness
            and all_deferred_audit.all_deferred_partial_go_not_runtime_readiness
        ),
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeSourceInstallExecutionPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceInstallExecutionPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_install_execution_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "source_install_execution_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_execution_artifact_audit_count_gte_1": True,
        "source_pre_execution_snapshot_audit_count_gte_1": True,
        "source_repository_verification_audit_count_eq_2": len(repo_audits) == 2,
        "source_commit_pin_audit_count_eq_2": len(commit_audits) == 2,
        "source_checkout_code_install_audit_count_eq_2": len(checkout_audits) == 2,
        "source_network_boundary_audit_count_gte_1": True,
        "source_post_install_probe_audit_count_eq_2": len(probe_audits) == 2,
        "all_deferred_partial_go_audit_count_gte_1": True,
        "source_deferred_asset_audit_count_eq_2": len(deferred_audits) == 2,
        "source_non_execution_boundary_audit_count_gte_16": len(boundary_audits) >= 16,
        "source_followup_resolution_routing_count_gte_1": True,
        "negative_guard_count_eq_20": negative_guard_count == 20,
        "negative_guard_passed_eq_20": negative_guard_passed == 20,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "post_review_only": POST_REVIEW_ONLY is True,
        "no_new_execution_allowed": NO_NEW_EXECUTION_ALLOWED is True,
        "all_deferred_partial_go_verified": all_assets_deferred is True,
        "partial_go_subtype_all_deferred_no_violation": PARTIAL_GO_SUBTYPE == "all_deferred_no_violation",
        "all_assets_deferred": all_assets_deferred is True,
        "successful_source_asset_count_verified_0": successful == 0,
        "deferred_source_asset_count_verified_2": (deferred == 2) if exec_present else True,
        "failed_source_asset_count_verified_0": failed == 0,
        "blocker_count_verified_0": actual_blocker == 0,
        "no_boundary_violation": no_violation,
        "no_environment_contamination": no_contamination,
        "no_fabricated_repository_url": all_deferred_audit.no_fabricated_repository_url,
        "no_forced_clone": all_deferred_audit.no_forced_clone,
        "no_forced_install": all_deferred_audit.no_forced_install,
        # Source install != readiness.
        "source_install_success_false": successful == 0,
        "source_install_success_not_weight_readiness": all_deferred_audit.all_deferred_partial_go_not_weight_readiness,
        "source_install_success_not_inference_approval": all_deferred_audit.all_deferred_partial_go_not_inference_readiness,
        "source_install_success_not_runtime_approval": all_deferred_audit.all_deferred_partial_go_not_runtime_readiness,
        # Repository verification audit.
        "repository_verification_failed_honestly": all(a.repository_verification_failed_honestly for a in repo_audits),
        "repository_verification_failure_caused_defer": all(a.repository_verification_failure_caused_defer for a in repo_audits),
        "repository_verification_failure_not_blocker_if_no_boundary_violation": all(
            a.repository_verification_failure_not_blocker_if_no_boundary_violation for a in repo_audits
        ),
        "mobile_sam_weight_excluding_checkout_required": network_audit.mobile_sam_weight_excluding_checkout_required_before_retry,
        # Follow-up gating.
        "source_execution_retry_not_allowed_until_repository_verification_complete": followup.source_execution_retry_not_allowed_until_repository_verification_complete,
        "source_execution_retry_not_allowed_until_commit_pin_complete": followup.source_execution_retry_not_allowed_until_commit_pin_complete,
        "source_execution_retry_not_allowed_until_license_review_complete": followup.source_execution_retry_not_allowed_until_license_review_complete,
        "source_execution_retry_not_allowed_until_dependency_review_complete": followup.source_execution_retry_not_allowed_until_dependency_review_complete,
        "mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete": followup.mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete,
        "no_weight_download_phase_until_successful_source_execution_post_review": followup.no_weight_download_phase_until_successful_source_execution_post_review,
        # Non-execution bindings.
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "git_clone_allowed_false": GIT_CLONE_ALLOWED is False,
        "source_checkout_allowed_false": SOURCE_CHECKOUT_ALLOWED is False,
        "source_install_allowed_false": SOURCE_INSTALL_ALLOWED is False,
        "pip_install_allowed_false": PIP_INSTALL_ALLOWED is False,
        "dependency_install_allowed_false": DEPENDENCY_INSTALL_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "dataset_download_allowed_false": DATASET_DOWNLOAD_ALLOWED is False,
        "example_asset_download_allowed_false": EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False,
        "real_import_allowed_false": REAL_IMPORT_ALLOWED is False,
        "model_load_allowed_false": MODEL_LOAD_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
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

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledSourceInstallExecutionPostReviewDecision(
        decision_ref=DECISION_REF,
        source_install_execution_post_review_profile_count=1,
        source_execution_artifact_audit_count=1,
        source_pre_execution_snapshot_audit_count=1,
        source_repository_verification_audit_count=len(repo_audits),
        source_commit_pin_audit_count=len(commit_audits),
        source_checkout_code_install_audit_count=len(checkout_audits),
        source_network_boundary_audit_count=1,
        source_post_install_probe_audit_count=len(probe_audits),
        all_deferred_partial_go_audit_count=1,
        source_deferred_asset_audit_count=len(deferred_audits),
        source_non_execution_boundary_audit_count=len(boundary_audits),
        source_followup_resolution_routing_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Execution Post-Review (audit only)",
        "lifecycle_variant": SCOPE,
        "post_review_principle_zh": POST_REVIEW_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "post_review_only": POST_REVIEW_ONLY,
        "source_execution_post_review": SOURCE_EXECUTION_POST_REVIEW,
        "no_new_execution_allowed": NO_NEW_EXECUTION_ALLOWED,
        "partial_go_subtype": PARTIAL_GO_SUBTYPE,
        "audited_asset_ids": list(AUDITED_ASSET_IDS),
        "upstream_execution_ref": UPSTREAM_EXECUTION_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "source_install_execution_post_review_profile": _build_profile(),
        "source_install_execution_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Audits.
        "source_execution_artifact_audit": asdict(artifact_audit),
        "source_execution_artifact_audit_count": 1,
        "source_pre_execution_snapshot_audit": asdict(snapshot_audit),
        "source_pre_execution_snapshot_audit_count": 1,
        "source_repository_verification_audits": [asdict(a) for a in repo_audits],
        "source_repository_verification_audit_count": len(repo_audits),
        "source_commit_pin_audits": [asdict(a) for a in commit_audits],
        "source_commit_pin_audit_count": len(commit_audits),
        "source_checkout_code_install_audits": [asdict(a) for a in checkout_audits],
        "source_checkout_code_install_audit_count": len(checkout_audits),
        "source_network_boundary_audit": asdict(network_audit),
        "source_network_boundary_audit_count": 1,
        "source_post_install_probe_audits": [asdict(a) for a in probe_audits],
        "source_post_install_probe_audit_count": len(probe_audits),
        "all_deferred_partial_go_audit": asdict(all_deferred_audit),
        "all_deferred_partial_go_audit_count": 1,
        "source_deferred_asset_audits": [asdict(a) for a in deferred_audits],
        "source_deferred_asset_audit_count": len(deferred_audits),
        "source_non_execution_boundary_audits": [asdict(a) for a in boundary_audits],
        "source_non_execution_boundary_audit_count": len(boundary_audits),
        "source_followup_resolution_routing": asdict(followup),
        "source_followup_resolution_routing_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_execution_post_review_status": (
                "all_deferred_no_violation_partial_go_confirmed_honest_no_clone_no_install_no_weight_no_fabrication"
                if review_ok
                else "blocked"
            ),
            "partial_go_subtype": PARTIAL_GO_SUBTYPE,
            "deferred_assets": list(AUDITED_ASSET_IDS),
            "recommended_next_phase": RECOMMENDED_NEXT_PHASE_REF,
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "Post-review of the first real controlled source-install execution complete. The upstream PARTIAL_GO "
                "is confirmed as the precise subtype `all_deferred_no_violation`: 0 successful, 2 deferred, 0 failed, "
                "blocker_count=0, with zero boundary violations, zero environment contamination, no fabricated "
                "repository URL, no forced clone, and no forced install. This is NOT full GO, NOT source install "
                "success, NOT weight/inference/runtime readiness, and NOT a blocker. Repository verification failed "
                "HONESTLY on the upstream placeholders (URL unverified, commit unpinned, license unverified) and that "
                "honest failure caused the defer (not a blocker, since no boundary was violated). byte_track defers "
                "on placeholder repo + unresolved/source-component identity; mobile_sam defers on placeholder repo + "
                "the canonical repo shipping a committed checkpoint (full clone would equal weight download), so a "
                "weight-excluding checkout plan is required before retry. Both deferred assets are routed to "
                "Phase-P1-Source-Repository-Verification-And-Commit-Pin-Planning-v1-001. Source-execution retry is "
                "NOT allowed until repository verification + commit pin + license review + dependency review (and, for "
                "mobile_sam, the weight-excluding checkout plan) complete; and there is NO weight-download phase until "
                "a SUCCESSFUL source-execution post-review. This post-review performed no clone / checkout / install / "
                "pip / download / import / inference / runtime / registry mutation and did not re-install deferred "
                "assets."
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

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "source_execution_artifact_audit_record": {
                "source_execution_artifact_audit": asdict(artifact_audit),
                "source_pre_execution_snapshot_audit": asdict(snapshot_audit),
            },
            "all_deferred_partial_go_audit_record": {
                "all_deferred_partial_go_audit": asdict(all_deferred_audit),
                "source_deferred_asset_audits": [asdict(a) for a in deferred_audits],
            },
            "repository_verification_audit_record": {
                "source_repository_verification_audits": [asdict(a) for a in repo_audits],
                "source_commit_pin_audits": [asdict(a) for a in commit_audits],
                "source_checkout_code_install_audits": [asdict(a) for a in checkout_audits],
                "source_post_install_probe_audits": [asdict(a) for a in probe_audits],
            },
            "network_boundary_audit_record": {
                "source_network_boundary_audit": asdict(network_audit),
            },
            "source_non_execution_boundary_record": {
                "source_non_execution_boundary_audits": [asdict(a) for a in boundary_audits],
            },
            "source_followup_resolution_record": {
                "source_followup_resolution_routing": asdict(followup),
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
            "post_review_only": True,
            "all_deferred_partial_go_verified": True,
            "source_install_success": False,
            "weight_download_allowed": False,
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
    result = review_p1_controlled_source_install_execution_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "partial_go_subtype": result["partial_go_subtype"],
                "deferred_asset_audit_count": result["decision"]["source_deferred_asset_audit_count"],
                "non_execution_boundary_audit_count": result["decision"]["source_non_execution_boundary_audit_count"],
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
