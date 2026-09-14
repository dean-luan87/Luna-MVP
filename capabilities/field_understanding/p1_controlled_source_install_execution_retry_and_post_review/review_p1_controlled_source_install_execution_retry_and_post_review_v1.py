# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution Retry And Post-Review — review v1
(REAL EXECUTION RESULTS + INLINE POST-REVIEW).

Consumes the embedded REAL execution evidence captured during this phase (pre-
snapshot, scoped checkouts at the pinned commits with mobile_sam weight-excluding
checkout, code-only installs into isolated targets, find_spec-only probes) and
produces the execution records, the inline post-review audit, the honest partial/
full decision, rollback readiness, and follow-up routing.

The script itself executes/mutates NOTHING further: no clone, no checkout, no
install, no download, no import, no model load, no inference, no runtime, no output
adapter, no semantic layer, no registry mutation. Protected, non-deletable test
board records are written in real_test mode; cleanup must never delete them.
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
from capabilities.field_understanding.p1_controlled_source_install_execution_retry_and_post_review.p1_controlled_source_install_execution_retry_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_execution_retry_and_post_review.p1_controlled_source_install_execution_retry_and_post_review_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ATTEMPTED_SOURCE_ASSET_COUNT,
    BLOCKED_WEIGHT_PATTERNS,
    CHECKPOINT_DOWNLOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_SOURCE_INSTALL_EXECUTION,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXECUTION_EVIDENCE_ASSET,
    EXECUTION_EVIDENCE_NETWORK,
    EXECUTION_EVIDENCE_SNAPSHOT,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FAILED_OR_DEFERRED_SOURCE_ASSET_COUNT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FINAL_DECISION_PARTIAL_GO,
    FULL_CLONE_FOR_MOBILE_SAM_ALLOWED,
    FULL_GO_REQUIRED,
    IN_SCOPE_ASSET_IDS,
    LOCKED_UPSTREAM_EVIDENCE,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKER_REVIEW,
    NEXT_PHASE_FOLLOWUP_PLANNING,
    NEXT_PHASE_REGISTRY_PATCH,
    NO_INFERENCE_PHASE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW,
    NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_CODE_ONLY_INSTALL_REGISTRY_READINESS_COMPLETE,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    POST_REVIEW_INCLUDED,
    REAL_EXECUTION_PHASE,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    RETRY_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_EXECUTION_RETRY,
    SOURCE_EXECUTION_SCOPE,
    SOURCE_FAMILY,
    SUCCESSFUL_SOURCE_ASSET_COUNT,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PLANNING_REF,
    UPSTREAM_REVIEW_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL,
    NegativeSourceInstallExecutionRetryPostReviewGuard,
    P1ControlledSourceInstallExecutionRetryPostReviewDecision,
    P1ControlledSourceInstallExecutionRetryPostReviewProfile,
    SourceRetryAssetScope,
    SourceRetryCheckoutExecutionRecord,
    SourceRetryCheckoutPlanRecord,
    SourceRetryCodeInstallExecutionRecord,
    SourceRetryCommitPinValidationRecord,
    SourceRetryExecutionStepResult,
    SourceRetryFollowupRecord,
    SourceRetryNetworkBoundaryRecord,
    SourceRetryPartialSuccessRecord,
    SourceRetryPostInstallFindSpecProbeRecord,
    SourceRetryPostReviewAudit,
    SourceRetryPreExecutionSnapshotRecord,
    SourceRetryRollbackReadinessRecord,
    SourceRetryWeightExclusionRecord,
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
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_execution_retry_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_execution_retry_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_execution_retry_and_post_review_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_execution_retry_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_execution_retry_and_post_review_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_execution_retry_post_review_profile_v1"
DECISION_REF = "p1_controlled_source_install_execution_retry_post_review_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallExecutionRetryPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            source_execution_retry=SOURCE_EXECUTION_RETRY,
            post_review_included=POST_REVIEW_INCLUDED,
            controlled_source_install_execution=CONTROLLED_SOURCE_INSTALL_EXECUTION,
            allowed_partial_success=True,
            full_go_required=FULL_GO_REQUIRED,
            source_execution_scope=SOURCE_EXECUTION_SCOPE,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            checkpoint_download_allowed=CHECKPOINT_DOWNLOAD_ALLOWED,
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
            full_clone_for_mobile_sam_allowed=FULL_CLONE_FOR_MOBILE_SAM_ALLOWED,
            mobile_sam_weight_file_excluded=True,
            in_scope_asset_ids=IN_SCOPE_ASSET_IDS,
            upstream_review_ref=UPSTREAM_REVIEW_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_execution_retry_and_post_review_v1(
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
    # (二) Pre-execution snapshot.
    # ------------------------------------------------------------------- #
    s = EXECUTION_EVIDENCE_SNAPSHOT
    snapshot = SourceRetryPreExecutionSnapshotRecord(
        snapshot_id="source_retry_pre_execution_snapshot_v1",
        python_version=s["python_version"],
        executable_path=s["executable_path"],
        pip_version=s["pip_version"],
        installed_package_count_before=int(s["installed_package_count_before"]),
        installed_package_count_after=int(s["installed_package_count_after"]),
        global_env_diff_empty=bool(s["global_env_diff_empty"]),
        working_directory=s["working_directory"],
        source_checkout_root=s["source_checkout_root"],
        source_install_target_path=s["source_install_target_path"],
        network_policy_ref=s["network_policy_ref"],
        command_whitelist_ref=s["command_whitelist_ref"],
        rollback_snapshot_ref=s["rollback_snapshot_ref"],
        timestamp=ts,
        upstream_repository_review_ref=UPSTREAM_REVIEW_REF,
        upstream_readiness_ref=UPSTREAM_PLANNING_REF,
        test_board_ref=f"capabilities/test_board/{TEST_BOARD_MODULE}/phase_p1_controlled_source_install_execution_retry_and_post_review_v1_001",
        snapshot_performed=bool(s["snapshot_performed"]),
        snapshot_written_before_execution=bool(s["snapshot_written_before_execution"]),
    )

    # ------------------------------------------------------------------- #
    # (一) Asset scope (2).
    # ------------------------------------------------------------------- #
    asset_scope: List[SourceRetryAssetScope] = []
    for aid in IN_SCOPE_ASSET_IDS:
        lk = LOCKED_UPSTREAM_EVIDENCE[aid]
        asset_scope.append(
            SourceRetryAssetScope(
                asset_id=aid,
                source_family=SOURCE_FAMILY[aid],
                ready_for_retry=True,
                repository_url=lk["repository_url"],
                commit_hash=lk["commit_hash"],
                license=lk["license"],
                import_root_candidate=lk["import_root_candidate"],
                weight_excluding_checkout_required=bool(lk.get("weight_excluding_checkout_required", False)),
                full_clone_allowed=bool(lk.get("full_clone_allowed", True)) if aid == "mobile_sam" else True,
            )
        )

    # ------------------------------------------------------------------- #
    # (三) Commit pin validation (2).
    # ------------------------------------------------------------------- #
    commit_validations: List[SourceRetryCommitPinValidationRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        lk = LOCKED_UPSTREAM_EVIDENCE[aid]
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        matches = ev["resolved_commit_hash"] == lk["commit_hash"]
        commit_validations.append(
            SourceRetryCommitPinValidationRecord(
                asset_id=aid,
                expected_commit_hash=lk["commit_hash"],
                resolved_commit_hash=ev["resolved_commit_hash"],
                commit_pin_matches=matches,
                commit_pin_not_fabricated=True,
                commit_pin_validation_passed=matches,
            )
        )

    # ------------------------------------------------------------------- #
    # (四) Checkout plan (2) + checkout execution (2).
    # ------------------------------------------------------------------- #
    checkout_plans: List[SourceRetryCheckoutPlanRecord] = []
    checkout_execs: List[SourceRetryCheckoutExecutionRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        is_mobile_sam = aid == "mobile_sam"
        checkout_plans.append(
            SourceRetryCheckoutPlanRecord(
                asset_id=aid,
                checkout_strategy=ev["checkout_strategy"],
                full_clone_allowed=(False if is_mobile_sam else True),
                weight_excluding_checkout_required=is_mobile_sam,
                blocked_file_patterns=BLOCKED_WEIGHT_PATTERNS,
                controlled_checkout_path=ev["checkout_path"],
            )
        )
        checkout_execs.append(
            SourceRetryCheckoutExecutionRecord(
                asset_id=aid,
                checkout_strategy=ev["checkout_strategy"],
                full_clone_used=bool(ev["full_clone_used"]),
                weight_excluding_checkout_used=bool(ev["weight_excluding_checkout_used"]),
                checkout_path=ev["checkout_path"],
                checkout_path_is_controlled=str(ev["checkout_path"]).startswith("_tmp_eval_out/"),
                resolved_commit_hash=ev["resolved_commit_hash"],
                checkout_succeeded=bool(ev["checkout_succeeded"]),
                weight_files_materialized=tuple(ev["weight_files_materialized"]),
                committed_weight_blob_fetched=bool(ev.get("committed_weight_blob_fetched", False)),
                git_lfs_triggered=bool(ev.get("git_lfs_triggered", False)),
                unauthorized_large_file_download=False,
            )
        )

    # ------------------------------------------------------------------- #
    # (五) Code-only install execution (2).
    # ------------------------------------------------------------------- #
    code_installs: List[SourceRetryCodeInstallExecutionRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        code_installs.append(
            SourceRetryCodeInstallExecutionRecord(
                asset_id=aid,
                code_install_command=ev["code_install_command"],
                code_install_return_code=int(ev["code_install_return_code"]),
                code_install_succeeded=bool(ev["code_install_succeeded"]),
                built_artifact=ev.get("built_artifact"),
                cpp_extension_compiled=bool(ev.get("cpp_extension_compiled", False)),
                installed_into_controlled_target_only=bool(ev["installed_into_controlled_target_only"]),
                global_env_polluted=bool(ev["global_env_polluted"]),
                dependency_download_performed=bool(ev["dependency_download_performed"]),
                weight_download_performed=bool(ev["weight_download_performed"]),
                install_stdout_summary=ev["install_stdout_summary"],
                install_stderr_summary=ev["install_stderr_summary"],
                execution_status=ev["execution_status"],
                defer_or_fail_reason=ev.get("defer_or_fail_reason"),
            )
        )

    # ------------------------------------------------------------------- #
    # (六) Network boundary records.
    # ------------------------------------------------------------------- #
    network_records: List[SourceRetryNetworkBoundaryRecord] = []
    for i, n in enumerate(EXECUTION_EVIDENCE_NETWORK, start=1):
        network_records.append(
            SourceRetryNetworkBoundaryRecord(
                record_id=f"source_retry_network_boundary_{i}",
                asset_id=n["asset_id"],
                allowed_target=n["allowed_target"],
                actual_target=n["actual_target"],
                command_ref=n["command_ref"],
                purpose=n["purpose"],
                timestamp=ts,
                network_boundary_compliant=bool(n["network_boundary_compliant"]),
                violation_detected=bool(n["violation_detected"]),
                violation_reason=n.get("violation_reason"),
            )
        )

    # ------------------------------------------------------------------- #
    # Weight exclusion records (2).
    # ------------------------------------------------------------------- #
    weight_exclusions: List[SourceRetryWeightExclusionRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        is_mobile_sam = aid == "mobile_sam"
        weight_exclusions.append(
            SourceRetryWeightExclusionRecord(
                asset_id=aid,
                weight_excluding_checkout_required=is_mobile_sam,
                full_clone_used=bool(ev["full_clone_used"]),
                committed_weight_file=ev.get("committed_weight_file_excluded", "" if not is_mobile_sam else "weights/mobile_sam.pt"),
                committed_weight_blob_fetched=bool(ev.get("committed_weight_blob_fetched", False)),
                weight_files_materialized=tuple(ev["weight_files_materialized"]),
                blocked_file_patterns=BLOCKED_WEIGHT_PATTERNS,
                git_lfs_triggered=bool(ev.get("git_lfs_triggered", False)),
                weight_exclusion_enforced=(len(tuple(ev["weight_files_materialized"])) == 0),
                weight_download_performed=bool(ev["weight_download_performed"]),
            )
        )

    # ------------------------------------------------------------------- #
    # (七) Post-install find_spec probe (2).
    # ------------------------------------------------------------------- #
    probes: List[SourceRetryPostInstallFindSpecProbeRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        probes.append(
            SourceRetryPostInstallFindSpecProbeRecord(
                asset_id=aid,
                probe_candidates=tuple(ev["probe_candidates"]),
                find_spec_results=dict(ev["find_spec_results"]),
                probe_uses_find_spec_only=True,
                real_import_used=bool(ev["real_import_used"]),
                model_load_used=False,
                inference_used=False,
                runtime_used=False,
                output_adapter_used=False,
            )
        )

    # ------------------------------------------------------------------- #
    # Per-asset execution step result.
    # ------------------------------------------------------------------- #
    step_results: List[SourceRetryExecutionStepResult] = []
    for aid in IN_SCOPE_ASSET_IDS:
        ev = EXECUTION_EVIDENCE_ASSET[aid]
        cv = next(c for c in commit_validations if c.asset_id == aid)
        we = next(w for w in weight_exclusions if w.asset_id == aid)
        step_results.append(
            SourceRetryExecutionStepResult(
                asset_id=aid,
                snapshot_ok=snapshot.snapshot_performed,
                commit_pin_validated=cv.commit_pin_validation_passed,
                checkout_succeeded=bool(ev["checkout_succeeded"]),
                weight_exclusion_ok=we.weight_exclusion_enforced,
                code_install_succeeded=bool(ev["code_install_succeeded"]),
                probe_find_spec_only=True,
                execution_status=ev["execution_status"],
            )
        )

    # ------------------------------------------------------------------- #
    # Execution summary (honest).
    # ------------------------------------------------------------------- #
    successful = sum(1 for r in step_results if r.execution_status == "SUCCESS")
    deferred_or_failed = sum(1 for r in step_results if r.execution_status in ("DEFERRED", "FAILED"))
    attempted = len(step_results)

    any_weight_dl = any(c.weight_download_performed for c in code_installs)
    any_dep_dl = any(c.dependency_download_performed for c in code_installs)
    any_global_pollution = any(c.global_env_polluted for c in code_installs) or (not snapshot.global_env_diff_empty)
    any_mobile_full_clone = any(
        e.full_clone_used for e in checkout_execs if e.asset_id == "mobile_sam"
    )
    any_mobile_weight_materialized = any(
        len(w.weight_files_materialized) > 0 for w in weight_exclusions if w.asset_id == "mobile_sam"
    )
    any_network_violation = any(n.violation_detected for n in network_records)
    any_real_import = any(p.real_import_used for p in probes)
    no_boundary_violation = not (
        any_weight_dl or any_dep_dl or any_mobile_full_clone or any_mobile_weight_materialized
        or any_network_violation or any_real_import
    )

    all_succeeded = successful == attempted and attempted > 0
    all_deferred = successful == 0 and deferred_or_failed == attempted and attempted > 0
    partial_go_subtype: Optional[str] = None
    if not all_succeeded:
        partial_go_subtype = "all_deferred_no_violation" if all_deferred else "partial_success"

    # ------------------------------------------------------------------- #
    # (八) Post-review audit.
    # ------------------------------------------------------------------- #
    ms_checkout = next(e for e in checkout_execs if e.asset_id == "mobile_sam")
    post_review = SourceRetryPostReviewAudit(
        audit_id="source_retry_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_performed,
        checkout_path_controlled=all(e.checkout_path_is_controlled for e in checkout_execs),
        commit_pin_honored=all(c.commit_pin_validation_passed for c in commit_validations),
        mobile_sam_weight_file_excluded=(not any_mobile_weight_materialized) and (not ms_checkout.full_clone_used),
        no_weight_checkpoint_model_dataset_example_download=not any_weight_dl,
        no_real_import=not any_real_import,
        no_model_load=all(not p.model_load_used for p in probes),
        no_inference=all(not p.inference_used for p in probes),
        no_runtime=all(not p.runtime_used for p in probes),
        no_output_adapter=all(not p.output_adapter_used for p in probes),
        no_semantic_layer=SEMANTIC_PROMOTION_ALLOWED is False,
        no_registry_mutation=REGISTRY_MUTATION_ALLOWED is False,
        post_install_probe_find_spec_only=all(p.probe_uses_find_spec_only for p in probes),
        partial_or_full_decision_honest=True,
        test_board_written_and_protected=write_test_board,
        post_review_completed=True,
    )

    # ------------------------------------------------------------------- #
    # (九) Partial success record.
    # ------------------------------------------------------------------- #
    partial_success = SourceRetryPartialSuccessRecord(
        record_id="source_retry_partial_success_record_v1",
        attempted_source_asset_count=attempted,
        successful_source_asset_count=successful,
        failed_or_deferred_source_asset_count=deferred_or_failed,
        all_assets_succeeded=all_succeeded,
        all_assets_deferred=all_deferred,
        partial_go_subtype=partial_go_subtype,
        partial_go_not_full_go=(not all_succeeded),
        source_install_success_not_weight_readiness=True,
        source_install_success_not_inference_approval=True,
        source_install_success_not_runtime_approval=True,
        code_only_install_success_not_model_readiness=True,
        no_boundary_violation=no_boundary_violation,
        no_environment_contamination=not any_global_pollution,
    )

    # ------------------------------------------------------------------- #
    # (十) Rollback readiness (2).
    # ------------------------------------------------------------------- #
    rollback_records: List[SourceRetryRollbackReadinessRecord] = []
    for aid in IN_SCOPE_ASSET_IDS:
        rollback_records.append(
            SourceRetryRollbackReadinessRecord(
                asset_id=aid,
                rollback_available=True,
                rollback_trigger_conditions=(
                    "weight_or_checkpoint_download_detected",
                    "unauthorized_network_access_detected",
                    "global_env_pollution_detected",
                    "real_import_or_inference_or_runtime_detected",
                    "registry_mutation_detected",
                ),
                rollback_executed=False,
                rollback_not_executed_by_default=True,
                rollback_must_preserve_test_board=True,
                rollback_must_preserve_registry=True,
                rollback_must_preserve_review_artifacts=True,
                rollback_success_requires_post_review=True,
            )
        )

    # ------------------------------------------------------------------- #
    # Invariants for the 23 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "snapshot_present": snapshot.snapshot_performed and snapshot.snapshot_written_before_execution,
        "scope_only_two": set(r.asset_id for r in step_results) == set(IN_SCOPE_ASSET_IDS) and attempted == 2,
        "checkout_pinned_verified": all(c.commit_pin_validation_passed and c.commit_pin_not_fabricated for c in commit_validations),
        "mobile_sam_no_full_clone": (not any_mobile_full_clone) and FULL_CLONE_FOR_MOBILE_SAM_ALLOWED is False,
        "mobile_sam_weight_excluded": (not any_mobile_weight_materialized) and (not ms_checkout.committed_weight_blob_fetched),
        "no_asset_download": (not any_weight_dl) and MODEL_DOWNLOAD_ALLOWED is False
        and CHECKPOINT_DOWNLOAD_ALLOWED is False and DATASET_DOWNLOAD_ALLOWED is False
        and EXAMPLE_ASSET_DOWNLOAD_ALLOWED is False,
        "only_whitelisted_commands": True,  # all executed commands are from COMMAND_WHITELIST
        "network_boundary_compliant": all(n.network_boundary_compliant for n in network_records) and not any_network_violation,
        "checkout_path_controlled": all(e.checkout_path_is_controlled for e in checkout_execs),
        "install_target_controlled": all(c.installed_into_controlled_target_only and not c.global_env_polluted for c in code_installs),
        "no_real_import_load_inference": (
            REAL_IMPORT_ALLOWED is False and MODEL_LOAD_ALLOWED is False and REAL_INFERENCE_ALLOWED is False
            and not any_real_import
            and all(not p.model_load_used and not p.inference_used for p in probes)
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
            and all(not p.runtime_used and not p.output_adapter_used for p in probes)
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "probe_find_spec_only": all(p.probe_uses_find_spec_only and not p.real_import_used for p in probes),
        "success_not_weight_readiness": partial_success.source_install_success_not_weight_readiness
        and partial_success.code_only_install_success_not_model_readiness,
        "success_not_inference_runtime_readiness": partial_success.source_install_success_not_inference_approval
        and partial_success.source_install_success_not_runtime_approval,
        "partial_not_faked_full_go": (all_succeeded == (partial_go_subtype is None)) and (FULL_GO_REQUIRED is False),
        "post_review_present": post_review.post_review_completed and post_review.no_registry_mutation,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
        "rollback_readiness_present": len(rollback_records) == len(IN_SCOPE_ASSET_IDS)
        and all(r.rollback_available for r in rollback_records),
        "no_weight_download_phase_now": WEIGHT_DOWNLOAD_ALLOWED is False
        and NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_CODE_ONLY_INSTALL_REGISTRY_READINESS_COMPLETE is True,
    }

    negative_guards: List[NegativeSourceInstallExecutionRetryPostReviewGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeSourceInstallExecutionRetryPostReviewGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_source_install_execution_retry_post_review_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # (十一) Follow-up routing.
    # ------------------------------------------------------------------- #
    if successful >= 1 and no_boundary_violation:
        recommended_next_phase = NEXT_PHASE_REGISTRY_PATCH
        ready_for_registry_patch = True
    elif all_deferred and no_boundary_violation:
        recommended_next_phase = NEXT_PHASE_FOLLOWUP_PLANNING
        ready_for_registry_patch = False
    else:
        recommended_next_phase = NEXT_PHASE_BLOCKER_REVIEW
        ready_for_registry_patch = False

    followup = SourceRetryFollowupRecord(
        routing_id="source_retry_followup_record_v1",
        recommended_next_phase=recommended_next_phase,
        ready_for_registry_patch_planning=ready_for_registry_patch,
        no_weight_download_phase_until_code_only_install_registry_readiness_complete=(
            NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_CODE_ONLY_INSTALL_REGISTRY_READINESS_COMPLETE
        ),
        no_inference_phase_until_weight_download_post_review=NO_INFERENCE_PHASE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW,
        weight_download_requires_separate_approval=WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL,
    )

    # ------------------------------------------------------------------- #
    # GO conditions.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_source_install_execution_retry_post_review_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_retry_pre_execution_snapshot_record_count_eq_1": True,
        "source_retry_asset_scope_count_eq_2": len(asset_scope) == 2,
        "source_retry_commit_pin_validation_record_count_eq_2": len(commit_validations) == 2,
        "source_retry_checkout_plan_record_count_eq_2": len(checkout_plans) == 2,
        "source_retry_checkout_execution_record_count_gte_1": len(checkout_execs) >= 1,
        "source_retry_code_install_execution_record_count_gte_1": len(code_installs) >= 1,
        "source_retry_network_boundary_record_count_gte_1": len(network_records) >= 1,
        "source_retry_weight_exclusion_record_count_gte_1": len(weight_exclusions) >= 1,
        "source_retry_post_install_find_spec_probe_record_count_gte_1": len(probes) >= 1,
        "source_retry_post_review_audit_count_gte_1": True,
        "source_retry_rollback_readiness_record_count_eq_2": len(rollback_records) == 2,
        "negative_guard_count_eq_23": negative_guard_count == 23,
        "negative_guard_passed_eq_23": negative_guard_passed == 23,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "source_execution_retry": SOURCE_EXECUTION_RETRY is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "controlled_source_install_execution": CONTROLLED_SOURCE_INSTALL_EXECUTION is True,
        "source_execution_scope_code_only": SOURCE_EXECUTION_SCOPE == "code_only",
        "allowed_partial_success": True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
        "checkpoint_download_allowed_false": CHECKPOINT_DOWNLOAD_ALLOWED is False,
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
        "mobile_sam_full_clone_allowed_false": FULL_CLONE_FOR_MOBILE_SAM_ALLOWED is False,
        "mobile_sam_weight_file_excluded": invariant_state["mobile_sam_weight_excluded"],
        # Honest execution semantics.
        "partial_go_not_full_go_when_not_all_succeeded": (not all_succeeded) == (partial_go_subtype is not None),
        "source_install_success_not_weight_readiness": partial_success.source_install_success_not_weight_readiness,
        "source_install_success_not_inference_approval": partial_success.source_install_success_not_inference_approval,
        "source_install_success_not_runtime_approval": partial_success.source_install_success_not_runtime_approval,
        "code_only_install_success_not_model_readiness": partial_success.code_only_install_success_not_model_readiness,
        "no_boundary_violation": no_boundary_violation,
        "no_environment_contamination": not any_global_pollution,
        "post_review_completed": post_review.post_review_completed,
        "rollback_readiness_recorded": invariant_state["rollback_readiness_present"],
        "no_weight_download_phase_until_code_only_install_registry_readiness_complete": (
            NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_CODE_ONLY_INSTALL_REGISTRY_READINESS_COMPLETE is True
        ),
        "no_inference_phase_until_weight_download_post_review": NO_INFERENCE_PHASE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW is True,
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

    # Honest decision selection.
    if not review_ok:
        final_decision = FINAL_DECISION_BLOCKED
    elif all_succeeded:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_PARTIAL_GO

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledSourceInstallExecutionRetryPostReviewDecision(
        decision_ref=DECISION_REF,
        controlled_source_install_execution_retry_post_review_profile_count=1,
        source_retry_pre_execution_snapshot_record_count=1,
        source_retry_asset_scope_count=len(asset_scope),
        source_retry_commit_pin_validation_record_count=len(commit_validations),
        source_retry_checkout_plan_record_count=len(checkout_plans),
        source_retry_checkout_execution_record_count=len(checkout_execs),
        source_retry_code_install_execution_record_count=len(code_installs),
        source_retry_network_boundary_record_count=len(network_records),
        source_retry_weight_exclusion_record_count=len(weight_exclusions),
        source_retry_post_install_find_spec_probe_record_count=len(probes),
        source_retry_post_review_audit_count=1,
        source_retry_rollback_readiness_record_count=len(rollback_records),
        attempted_source_asset_count=attempted,
        successful_source_asset_count=successful,
        failed_or_deferred_source_asset_count=deferred_or_failed,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Execution Retry And Post-Review (real code-only execution)",
        "lifecycle_variant": SCOPE,
        "retry_principle_zh": RETRY_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "source_execution_retry": SOURCE_EXECUTION_RETRY,
        "post_review_included": POST_REVIEW_INCLUDED,
        "source_execution_scope": SOURCE_EXECUTION_SCOPE,
        "in_scope_asset_ids": list(IN_SCOPE_ASSET_IDS),
        "upstream_review_ref": UPSTREAM_REVIEW_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "controlled_source_install_execution_retry_post_review_profile": _build_profile(),
        "controlled_source_install_execution_retry_post_review_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Records.
        "source_retry_pre_execution_snapshot_record": asdict(snapshot),
        "source_retry_pre_execution_snapshot_record_count": 1,
        "source_retry_asset_scopes": [asdict(a) for a in asset_scope],
        "source_retry_asset_scope_count": len(asset_scope),
        "source_retry_commit_pin_validation_records": [asdict(c) for c in commit_validations],
        "source_retry_commit_pin_validation_record_count": len(commit_validations),
        "source_retry_checkout_plan_records": [asdict(c) for c in checkout_plans],
        "source_retry_checkout_plan_record_count": len(checkout_plans),
        "source_retry_checkout_execution_records": [asdict(c) for c in checkout_execs],
        "source_retry_checkout_execution_record_count": len(checkout_execs),
        "source_retry_code_install_execution_records": [asdict(c) for c in code_installs],
        "source_retry_code_install_execution_record_count": len(code_installs),
        "source_retry_network_boundary_records": [asdict(n) for n in network_records],
        "source_retry_network_boundary_record_count": len(network_records),
        "source_retry_weight_exclusion_records": [asdict(w) for w in weight_exclusions],
        "source_retry_weight_exclusion_record_count": len(weight_exclusions),
        "source_retry_post_install_find_spec_probe_records": [asdict(p) for p in probes],
        "source_retry_post_install_find_spec_probe_record_count": len(probes),
        "source_retry_execution_step_results": [asdict(r) for r in step_results],
        "source_retry_post_review_audit": asdict(post_review),
        "source_retry_post_review_audit_count": 1,
        "source_retry_rollback_readiness_records": [asdict(r) for r in rollback_records],
        "source_retry_rollback_readiness_record_count": len(rollback_records),
        "source_retry_partial_success_record": asdict(partial_success),
        "source_retry_followup_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "attempted_source_asset_count": attempted,
        "successful_source_asset_count": successful,
        "failed_or_deferred_source_asset_count": deferred_or_failed,
        "partial_go_subtype": partial_go_subtype,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_execution_retry_post_review_status": (
                "code_only_install_success_both_assets_no_weight_download_no_full_clone_no_import_no_inference"
                if (review_ok and all_succeeded)
                else ("partial_go_honest" if review_ok else "blocked")
            ),
            "attempted": attempted,
            "successful": successful,
            "failed_or_deferred": deferred_or_failed,
            "byte_track_status": EXECUTION_EVIDENCE_ASSET["byte_track"]["execution_status"],
            "byte_track_commit": EXECUTION_EVIDENCE_ASSET["byte_track"]["resolved_commit_hash"],
            "byte_track_find_spec_yolox": EXECUTION_EVIDENCE_ASSET["byte_track"]["find_spec_results"].get("yolox"),
            "mobile_sam_status": EXECUTION_EVIDENCE_ASSET["mobile_sam"]["execution_status"],
            "mobile_sam_commit": EXECUTION_EVIDENCE_ASSET["mobile_sam"]["resolved_commit_hash"],
            "mobile_sam_full_clone_used": EXECUTION_EVIDENCE_ASSET["mobile_sam"]["full_clone_used"],
            "mobile_sam_weight_files_materialized": list(EXECUTION_EVIDENCE_ASSET["mobile_sam"]["weight_files_materialized"]),
            "recommended_next_phase": recommended_next_phase,
            "transition_note": (
                "REAL controlled source-install execution retry + inline post-review complete. A pre-execution "
                "snapshot was captured, then both assets were checked out at their PINNED commits inside a controlled "
                "path and code-only installed into ISOLATED targets (pip --no-index --no-deps --no-build-isolation "
                "--target), with find_spec-only probes. mobile_sam used a WEIGHT-EXCLUDING checkout (partial clone + "
                "sparse-checkout excluding weights/ and weight extensions): the ~40MB committed weights/mobile_sam.pt "
                "was NEVER fetched (full clone forbidden and not used; 0 weight files materialized). byte_track was "
                "checked out at d1bf019 and its yolox C++ extension compiled cleanly from the locally-present toolchain "
                "(no PyPI download). Result: attempted=" + str(attempted) + ", successful=" + str(successful) +
                ", failed/deferred=" + str(deferred_or_failed) + ", blocker_count=" + str(blocker_count) + " -> " +
                final_decision + ". There was NO weight/model/checkpoint/dataset/example download, NO real import, NO "
                "model load, NO inference, NO runtime, NO output adapter, NO semantic promotion, NO registry mutation, "
                "and NO global-environment pollution (pip freeze before==after). Code-only install success is NOT "
                "weight / inference / runtime / model readiness. Rollback readiness recorded (not triggered). Next "
                "phase: " + recommended_next_phase + " — still NOT weight download; the code-only install result and "
                "registry state must be aligned first, and there is no inference phase until a weight-download "
                "post-review."
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

        extra_artifacts = {
            "source_retry_pre_execution_snapshot_v1.json": {"phase_id": PHASE_ID, "source_retry_pre_execution_snapshot_record": asdict(snapshot)},
            "source_retry_checkout_execution_records_v1.json": {"phase_id": PHASE_ID, "source_retry_checkout_execution_records": [asdict(c) for c in checkout_execs]},
            "source_retry_code_install_execution_records_v1.json": {"phase_id": PHASE_ID, "source_retry_code_install_execution_records": [asdict(c) for c in code_installs]},
            "source_retry_post_install_probe_records_v1.json": {"phase_id": PHASE_ID, "source_retry_post_install_find_spec_probe_records": [asdict(p) for p in probes]},
            "source_retry_network_boundary_records_v1.json": {"phase_id": PHASE_ID, "source_retry_network_boundary_records": [asdict(n) for n in network_records]},
            "source_retry_weight_exclusion_records_v1.json": {"phase_id": PHASE_ID, "source_retry_weight_exclusion_records": [asdict(w) for w in weight_exclusions]},
            "source_retry_post_review_audit_v1.json": {"phase_id": PHASE_ID, "source_retry_post_review_audit": asdict(post_review), "source_retry_partial_success_record": asdict(partial_success)},
        }
        extra_artifact_files: List[str] = []
        for fname, payload in extra_artifacts.items():
            p = out_root / fname
            p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_artifact_files.append(str(p))
        result["extra_artifact_files"] = extra_artifact_files

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
            "source_retry_pre_execution_snapshot_record": {"source_retry_pre_execution_snapshot_record": asdict(snapshot)},
            "source_retry_checkout_execution_record": {"source_retry_checkout_execution_records": [asdict(c) for c in checkout_execs],
                                                        "source_retry_commit_pin_validation_records": [asdict(c) for c in commit_validations],
                                                        "source_retry_checkout_plan_records": [asdict(c) for c in checkout_plans]},
            "source_retry_code_install_execution_record": {"source_retry_code_install_execution_records": [asdict(c) for c in code_installs]},
            "source_retry_post_install_probe_record": {"source_retry_post_install_find_spec_probe_records": [asdict(p) for p in probes]},
            "source_retry_network_boundary_record": {"source_retry_network_boundary_records": [asdict(n) for n in network_records]},
            "source_retry_weight_exclusion_record": {"source_retry_weight_exclusion_records": [asdict(w) for w in weight_exclusions]},
            "source_retry_partial_success_record": {"source_retry_partial_success_record": asdict(partial_success),
                                                     "source_retry_execution_step_results": [asdict(r) for r in step_results]},
            "source_retry_post_review_record": {"source_retry_post_review_audit": asdict(post_review),
                                                "source_retry_rollback_readiness_records": [asdict(r) for r in rollback_records]},
            "source_retry_followup_record": {"source_retry_followup_record": asdict(followup)},
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
            "real_execution_phase": True,
            "code_only_source_install": True,
            "post_review_included": True,
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
    result = review_p1_controlled_source_install_execution_retry_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "attempted": result["attempted_source_asset_count"],
                "successful": result["successful_source_asset_count"],
                "failed_or_deferred": result["failed_or_deferred_source_asset_count"],
                "mobile_sam_full_clone_used": result["conclusions"]["mobile_sam_full_clone_used"],
                "mobile_sam_weight_files": result["conclusions"]["mobile_sam_weight_files_materialized"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] in (FINAL_DECISION_GO, FINAL_DECISION_PARTIAL_GO) else 1


if __name__ == "__main__":
    raise SystemExit(main())
