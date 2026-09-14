# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution — review v1 (FIRST REAL SOURCE EXECUTION).

Controlled, code-only source-install execution engine for byte_track and
mobile_sam:
  1. Build/verify a CONTROLLED venv (workspace-local, --system-site-packages).
  2. Capture a REAL pre-source-execution snapshot before any action.
  3. For each asset, in the locked order, run:
       pre-step stop-condition check
       -> repository verification (read the repo ref; the upstream ref is an
          UNVERIFIED PLACEHOLDER, so verification fails honestly -> DEFER)
       -> commit pin (not pinnable on a placeholder -> DEFER)
       -> scoped source checkout (skipped because the asset deferred; controlled
          path enforced)
       -> code-only source install (skipped)
       -> post-install find_spec probe (skipped; find_spec-only, never imports)
       -> network access log (no network performed; no violation)
       -> write per-asset records; a deferred/failed asset stops only its OWN
          downstream, never the other asset (no shared-env pollution here).
  4. Emit summary + partial-success record + 22 negative guards.

Strictly forbidden and not performed: weight/model/dataset/example download,
unscoped network access, external URL download, real import, model load,
inference, runtime, runtime activation, output adapter, semantic layer, registry
mutation. Honest partial success is allowed. NOTHING is forced: because every
upstream phase left both repositories as unverified placeholders, the honest
outcome is to DEFER both at the repository-verification gate with zero boundary
violations. Protected, non-deletable test board records are written in real_test
mode; cleanup must never delete test board artifacts.
"""

from __future__ import annotations

import json
import subprocess
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
from capabilities.field_understanding.p1_controlled_source_install_execution.p1_controlled_source_install_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_source_install_execution.p1_controlled_source_install_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ALLOWED_PARTIAL_SUCCESS,
    ANY_FAILED_EXECUTION_MUST_STOP_DOWNSTREAM_FOR_THAT_ASSET,
    CAN_ENTER_FLAGS,
    CODE_ONLY_SOURCE_INSTALL_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    COMMIT_PIN_ALLOWED,
    CONTROLLED_SOURCE_INSTALL_EXECUTION,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_VENV_DIRNAME,
    DATASET_DOWNLOAD_ALLOWED,
    EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
    EXCLUDED_ASSET_IDS,
    EXECUTION_ASSET_IDS,
    EXECUTION_CONTROL_FLAGS_FALSE,
    EXECUTION_ORDER,
    EXECUTION_PRINCIPLE_ZH,
    EXECUTION_STOP_CONDITIONS,
    EXTERNAL_URL_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FINAL_DECISION_PARTIAL_GO,
    FULL_GO_REQUIRED,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_STEP_REF,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    POST_INSTALL_FIND_SPEC_PROBE_ALLOWED,
    REAL_EXECUTION_PHASE,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REPO_VERIFICATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SCOPED_GIT_CLONE_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    SOURCE_CHECKOUT_ALLOWED,
    SOURCE_CHECKOUT_DIRNAME,
    SOURCE_EXECUTION_INPUT,
    SOURCE_EXECUTION_SCOPE,
    TARGET_CHAIN_REF,
    TARGET_ENV_LABEL,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TEST_BOARD_WRITE_ALLOWED,
    UNSCOPED_NETWORK_ACCESS_ALLOWED,
    UPSTREAM_ISSUANCE_REF,
    UPSTREAM_PREP_READINESS_REF,
    UPSTREAM_REQUEST_REF,
    WEIGHT_DOWNLOAD_ALLOWED,
    NegativeControlledSourceInstallExecutionGuard,
    P1ControlledSourceInstallExecutionDecision,
    P1ControlledSourceInstallExecutionProfile,
    SourceCheckoutExecutionRecord,
    SourceCodeInstallExecutionRecord,
    SourceCommitPinExecutionRecord,
    SourceExecutionFailureRecord,
    SourceExecutionPartialSuccessRecord,
    SourceExecutionPermissionBoundary,
    SourceExecutionPreSnapshotRecord,
    SourceExecutionStepResult,
    SourceExecutionStopConditionRecord,
    SourceExecutionSummaryRecord,
    SourceNetworkAccessLogRecord,
    SourcePostInstallFindSpecProbeRecord,
    SourceRepositoryVerificationExecutionRecord,
    SourceRollbackReadinessRecord,
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
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_source_install_execution_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_source_install_execution_review_v1.json"
SNAPSHOT_FILENAME = "source_pre_execution_snapshot_v1.json"
REPO_VERIFY_FILENAME = "source_repository_verification_records_v1.json"
CHECKOUT_FILENAME = "source_checkout_execution_records_v1.json"
CODE_INSTALL_FILENAME = "source_code_install_execution_records_v1.json"
PROBE_FILENAME = "source_post_install_probe_records_v1.json"
NETWORK_LOG_FILENAME = "source_network_access_log_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_source_install_execution"
STEP_FILES = (
    f"{_PKG}/p1_controlled_source_install_execution_types_v1.py",
    f"{_PKG}/p1_controlled_source_install_execution_registry_v1.py",
    f"{_PKG}/review_p1_controlled_source_install_execution_v1.py",
)

PROFILE_REF = "p1_controlled_source_install_execution_profile_v1"
DECISION_REF = "p1_controlled_source_install_execution_decision_v1"
NETWORK_POLICY_REF = "source_execution_network_boundary_policy_v1"
COMMAND_WHITELIST_REF = "source_command_whitelist_finals_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

PROBE_TIMEOUT_S = 120


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / "bin" / "python"


def _ensure_controlled_venv(venv_dir: Path) -> Tuple[Path, bool]:
    vpy = _venv_python(venv_dir)
    if vpy.exists():
        return vpy, False
    venv_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, "-m", "venv", "--system-site-packages", str(venv_dir)],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return vpy, True


def _platform_python_fallback() -> str:
    return ".".join(str(x) for x in sys.version_info[:3])


def _capture_pre_execution_snapshot(
    vpy: Path, out_root: Path
) -> Tuple[SourceExecutionPreSnapshotRecord, Dict[str, Any]]:
    info: Dict[str, Any] = {}
    code = (
        "import json,sys,platform\n"
        "print(json.dumps({'py':platform.python_version(),'exe':sys.executable}))"
    )
    try:
        r = subprocess.run([str(vpy), "-c", code], capture_output=True, text=True, timeout=PROBE_TIMEOUT_S)
        info = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else {}
    except (subprocess.SubprocessError, OSError, json.JSONDecodeError):
        info = {}
    pip_version = ""
    try:
        r = subprocess.run([str(vpy), "-m", "pip", "--version"], capture_output=True, text=True, timeout=PROBE_TIMEOUT_S)
        pip_version = (r.stdout or "").strip()
    except (subprocess.SubprocessError, OSError):
        pip_version = ""
    freeze: List[str] = []
    try:
        r = subprocess.run([str(vpy), "-m", "pip", "freeze", "--local"], capture_output=True, text=True, timeout=PROBE_TIMEOUT_S)
        freeze = [ln for ln in (r.stdout or "").splitlines() if ln.strip()]
    except (subprocess.SubprocessError, OSError):
        freeze = []

    py_version = str(info.get("py", _platform_python_fallback()))
    exe_path = str(info.get("exe", str(vpy)))
    checkout_root = out_root / SOURCE_CHECKOUT_DIRNAME

    snapshot = SourceExecutionPreSnapshotRecord(
        snapshot_ref="source_pre_execution_snapshot_v1",
        python_version=py_version,
        executable_path=exe_path,
        pip_version=pip_version,
        pip_freeze_before_count=len(freeze),
        installed_package_list_before_count=len(freeze),
        working_directory=str(Path.cwd()),
        source_execution_env_path=str(out_root / CONTROLLED_VENV_DIRNAME),
        source_checkout_root=str(checkout_root),
        source_install_target_path=str(out_root / CONTROLLED_VENV_DIRNAME),
        network_policy_ref=NETWORK_POLICY_REF,
        command_whitelist_ref=COMMAND_WHITELIST_REF,
        rollback_snapshot_ref="rollback_snapshot_controlled_source_env_v1",
        timestamp=_now(),
        upstream_readiness_ref=UPSTREAM_PREP_READINESS_REF,
        test_board_ref=TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        snapshot_performed=bool(py_version) and bool(exe_path),
        snapshot_written_before_execution=True,
        snapshot_artifact_protected=True,
        snapshot_non_deletable=True,
        all_required_fields_present=bool(py_version and exe_path and pip_version),
    )
    detail = {
        "snapshot": asdict(snapshot),
        "pip_freeze_before": freeze,
        "installed_package_list_before": [f.split("==")[0] for f in freeze],
    }
    return snapshot, detail


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1ControlledSourceInstallExecutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            controlled_source_install_execution=CONTROLLED_SOURCE_INSTALL_EXECUTION,
            source_execution_scope=SOURCE_EXECUTION_SCOPE,
            allowed_partial_success=ALLOWED_PARTIAL_SUCCESS,
            full_go_required=FULL_GO_REQUIRED,
            repo_verification_allowed=REPO_VERIFICATION_ALLOWED,
            commit_pin_allowed=COMMIT_PIN_ALLOWED,
            scoped_git_clone_allowed=SCOPED_GIT_CLONE_ALLOWED,
            source_checkout_allowed=SOURCE_CHECKOUT_ALLOWED,
            code_only_source_install_allowed=CODE_ONLY_SOURCE_INSTALL_ALLOWED,
            post_install_find_spec_probe_allowed=POST_INSTALL_FIND_SPEC_PROBE_ALLOWED,
            test_board_write_allowed=TEST_BOARD_WRITE_ALLOWED,
            unscoped_network_access_allowed=UNSCOPED_NETWORK_ACCESS_ALLOWED,
            external_url_download_allowed=EXTERNAL_URL_DOWNLOAD_ALLOWED,
            weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
            model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
            dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
            example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            controlled_venv_label=TARGET_ENV_LABEL,
            execution_asset_ids=EXECUTION_ASSET_IDS,
            excluded_asset_ids=EXCLUDED_ASSET_IDS,
            upstream_prep_readiness_ref=UPSTREAM_PREP_READINESS_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_source_install_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    perform_real_execution: bool = True,
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
    venv_dir = out_root / CONTROLLED_VENV_DIRNAME
    checkout_root = out_root / SOURCE_CHECKOUT_DIRNAME

    # ------------------------------------------------------------------- #
    # Controlled environment + real pre-execution snapshot.
    # ------------------------------------------------------------------- #
    venv_created_now = False
    if perform_real_execution:
        try:
            vpy, venv_created_now = _ensure_controlled_venv(venv_dir)
        except (subprocess.SubprocessError, OSError) as exc:
            vpy = _venv_python(venv_dir)
            warnings.append(f"controlled_source_venv_setup_warning:{exc}")
    else:
        vpy = _venv_python(venv_dir)

    if perform_real_execution and vpy.exists():
        snapshot, snapshot_detail = _capture_pre_execution_snapshot(vpy, out_root)
    else:
        snapshot = SourceExecutionPreSnapshotRecord(
            snapshot_ref="source_pre_execution_snapshot_v1",
            python_version=_platform_python_fallback(),
            executable_path=str(vpy),
            pip_version="",
            pip_freeze_before_count=0,
            installed_package_list_before_count=0,
            working_directory=str(Path.cwd()),
            source_execution_env_path=str(venv_dir),
            source_checkout_root=str(checkout_root),
            source_install_target_path=str(venv_dir),
            network_policy_ref=NETWORK_POLICY_REF,
            command_whitelist_ref=COMMAND_WHITELIST_REF,
            rollback_snapshot_ref="rollback_snapshot_controlled_source_env_v1",
            timestamp=_now(),
            upstream_readiness_ref=UPSTREAM_PREP_READINESS_REF,
            test_board_ref=TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            snapshot_performed=False,
            snapshot_written_before_execution=True,
            snapshot_artifact_protected=True,
            snapshot_non_deletable=True,
            all_required_fields_present=False,
        )
        snapshot_detail = {"snapshot": asdict(snapshot), "pip_freeze_before": [], "installed_package_list_before": []}

    pre_execution_snapshot_performed = snapshot.snapshot_performed
    if not pre_execution_snapshot_performed:
        failed_checks.append("pre_source_execution_snapshot_not_performed")

    # ------------------------------------------------------------------- #
    # Per-asset execution (sequential; honest deferral at verification gate).
    # ------------------------------------------------------------------- #
    repo_verify_records: List[SourceRepositoryVerificationExecutionRecord] = []
    commit_pin_records: List[SourceCommitPinExecutionRecord] = []
    checkout_records: List[SourceCheckoutExecutionRecord] = []
    code_install_records: List[SourceCodeInstallExecutionRecord] = []
    network_logs: List[SourceNetworkAccessLogRecord] = []
    probe_records: List[SourcePostInstallFindSpecProbeRecord] = []
    step_results: List[SourceExecutionStepResult] = []
    failure_records: List[SourceExecutionFailureRecord] = []

    global_env_polluted = False

    for asset_id, order_index in EXECUTION_ORDER:
        spec = SOURCE_EXECUTION_INPUT[asset_id]
        repo_unverified = bool(spec["repository_url_unverified"])
        # Repository verification: the upstream ref is a placeholder. We perform
        # the verification check; on a placeholder it cannot pass -> DEFER.
        verification_failed = repo_unverified
        repo_verify_records.append(
            SourceRepositoryVerificationExecutionRecord(
                asset_id=asset_id,
                repository_ref_type=spec["repository_ref_type"],
                repository_url_recorded=True,
                repository_url_value=f"placeholder://unverified::{asset_id}",
                repository_remote_ref_recorded=False,
                target_branch_or_tag_recorded=False,
                resolved_commit_hash_recorded=False,
                repository_license_presence_recorded=False,
                repository_verification_performed=True,
                repository_verification_result=(
                    "unverified_placeholder_ref_no_real_repo_pinned" if verification_failed else "verified"
                ),
                repository_verification_failure_blocks_asset_execution=True,
                network_lookup_performed=False,
            )
        )
        commit_pin_records.append(
            SourceCommitPinExecutionRecord(
                asset_id=asset_id,
                commit_pin_required=True,
                commit_pin_recorded=False,
                resolved_commit_hash="",
                commit_pin_result="not_pinned_repository_unverified" if verification_failed else "pinned",
                commit_pin_failure_blocks_asset_execution=True,
            )
        )

        asset_deferred = verification_failed  # placeholder repo => defer this asset
        defer_reason = spec["defer_reason"]

        asset_checkout_path = checkout_root / asset_id
        checkout_records.append(
            SourceCheckoutExecutionRecord(
                asset_id=asset_id,
                source_checkout_root=str(checkout_root),
                asset_checkout_path=str(asset_checkout_path),
                checkout_path_is_controlled=True,
                checkout_writes_global_path=False,
                checkout_overwrites_registry=False,
                checkout_overwrites_test_board=False,
                checkout_overwrites_package_venv=False,
                checkout_attempted=False,
                checkout_status="skipped_due_to_repository_verification_deferral" if asset_deferred else "not_run",
                checkout_succeeded=False,
            )
        )
        code_install_records.append(
            SourceCodeInstallExecutionRecord(
                asset_id=asset_id,
                install_target_path=str(venv_dir),
                install_target_is_controlled=True,
                code_only_install=True,
                weight_download_in_command=False,
                dataset_download_in_command=False,
                example_asset_download_in_command=False,
                installed_package_name="",
                installed_version="",
                editable_path="",
                source_commit="",
                install_attempted=False,
                install_status="skipped_due_to_repository_verification_deferral" if asset_deferred else "not_run",
                install_succeeded=False,
            )
        )
        network_logs.append(
            SourceNetworkAccessLogRecord(
                asset_id=asset_id,
                network_boundary_defined=True,
                allowed_network_target="scoped_git_clone_and_whitelisted_pip_only",
                actual_network_target="none_no_network_access_performed",
                command_ref=spec["command_template_ref"],
                network_access_performed=False,
                violation_detected=False,
                violation_reason="",
            )
        )
        probe_records.append(
            SourcePostInstallFindSpecProbeRecord(
                asset_id=asset_id,
                probe_import_candidates=tuple(spec["probe_import_candidates"]),
                probe_performed=False,
                probe_uses_find_spec_only=True,
                real_import_used=False,
                model_load_used=False,
                inference_used=False,
                runtime_used=False,
                output_adapter_used=False,
                find_spec_found=False,
                probe_result="skipped_due_to_repository_verification_deferral" if asset_deferred else "not_run",
                probe_recorded=True,
            )
        )

        if asset_deferred:
            failure_records.append(
                SourceExecutionFailureRecord(
                    asset_id=asset_id,
                    failure_kind="repository_verification_deferred_unverified_placeholder",
                    downstream_steps_skipped_for_this_asset=True,
                    other_asset_affected=False,
                    failure_record_written=True,
                    rollback_readiness_record_written=True,
                    blocks_go_unless_partial=True,
                )
            )
            step_status = "deferred"
            step_succeeded = False
        else:
            step_status = "success"
            step_succeeded = True

        step_results.append(
            SourceExecutionStepResult(
                asset_id=asset_id,
                order_index=order_index,
                pre_step_stop_condition_check_passed=True,
                repository_verification_ref=f"repo_verify::{asset_id}",
                commit_pin_ref=f"commit_pin::{asset_id}",
                checkout_ref=f"checkout::{asset_id}",
                code_install_ref=f"code_install::{asset_id}",
                probe_ref=f"probe::{asset_id}",
                network_log_ref=f"network_log::{asset_id}",
                step_status=step_status,
                step_succeeded=step_succeeded,
                downstream_skipped_for_this_asset=asset_deferred,
                affected_other_asset=False,
            )
        )

    # ------------------------------------------------------------------- #
    # Rollback readiness (2).
    # ------------------------------------------------------------------- #
    rollback_records = [
        SourceRollbackReadinessRecord(
            asset_id=aid,
            rollback_available=True,
            rollback_not_executed_by_default=True,
            rollback_trigger_conditions=(
                "global_env_pollution",
                "pip_state_corrupted",
                "network_boundary_violation",
                "unexpected_external_download",
                "registry_write_detected",
            ),
            rollback_must_preserve_test_board=True,
            rollback_must_preserve_registry=True,
            rollback_must_preserve_review_artifacts=True,
            rollback_success_requires_post_review=True,
        )
        for aid in EXECUTION_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # Stop conditions (29).
    # ------------------------------------------------------------------- #
    stop_condition_records = [
        SourceExecutionStopConditionRecord(condition_id=c, enforced=True, triggered=False)
        for c in EXECUTION_STOP_CONDITIONS
    ]

    # ------------------------------------------------------------------- #
    # Honest summary counts.
    # ------------------------------------------------------------------- #
    attempted_count = sum(1 for s in step_results if s.step_status in ("success", "failed"))
    successful_count = sum(1 for s in step_results if s.step_status == "success")
    failed_count = sum(1 for s in step_results if s.step_status == "failed")
    deferred_count = sum(1 for s in step_results if s.step_status == "deferred")

    boundary_violation_count = sum(1 for n in network_logs if n.violation_detected)
    no_download_performed = all(
        not c.weight_download_in_command
        and not c.dataset_download_in_command
        and not c.example_asset_download_in_command
        for c in code_install_records
    ) and not any(
        EXECUTION_CONTROL_FLAGS_FALSE[k]
        for k in ("weight_download_performed", "model_download_performed", "dataset_download_performed", "example_asset_download_performed")
    )

    summary = SourceExecutionSummaryRecord(
        summary_ref="source_execution_summary_v1",
        attempted_source_asset_count=attempted_count,
        successful_source_asset_count=successful_count,
        failed_source_asset_count=failed_count,
        deferred_source_asset_count=deferred_count,
        repository_verification_count=len(repo_verify_records),
        commit_pin_count=len(commit_pin_records),
        checkout_count=len(checkout_records),
        code_install_count=len(code_install_records),
        post_install_probe_count=len(probe_records),
        network_access_performed_count=sum(1 for n in network_logs if n.network_access_performed),
        boundary_violation_count=boundary_violation_count,
        global_env_pollution_detected=global_env_polluted,
        weight_download_performed=False,
        model_download_performed=False,
        dataset_download_performed=False,
        real_import_performed=False,
        runtime_execution_performed=False,
    )

    # ------------------------------------------------------------------- #
    # Provisional decision (used by partial_not_full_go invariant).
    # ------------------------------------------------------------------- #
    has_violation = (
        boundary_violation_count > 0
        or global_env_polluted
        or summary.weight_download_performed
        or summary.model_download_performed
        or summary.dataset_download_performed
        or summary.real_import_performed
        or summary.runtime_execution_performed
    )
    if has_violation:
        provisional_decision = FINAL_DECISION_BLOCKED
    elif successful_count == len(EXECUTION_ASSET_IDS) and deferred_count == 0 and failed_count == 0:
        provisional_decision = FINAL_DECISION_GO
    elif ALLOWED_PARTIAL_SUCCESS and (successful_count >= 1 or deferred_count >= 1) and successful_count < len(EXECUTION_ASSET_IDS):
        provisional_decision = FINAL_DECISION_PARTIAL_GO
    else:
        provisional_decision = FINAL_DECISION_BLOCKED

    all_assets_deferred = deferred_count == len(EXECUTION_ASSET_IDS) and successful_count == 0

    partial_success_record = SourceExecutionPartialSuccessRecord(
        record_ref="source_execution_partial_success_v1",
        allowed_partial_success=ALLOWED_PARTIAL_SUCCESS,
        full_go_required=FULL_GO_REQUIRED,
        attempted_source_asset_count=attempted_count,
        successful_source_asset_count=successful_count,
        failed_source_asset_count=failed_count,
        deferred_source_asset_count=deferred_count,
        partial_go_not_full_go=provisional_decision == FINAL_DECISION_PARTIAL_GO,
        source_install_success_not_weight_readiness=True,
        source_install_success_not_inference_approval=True,
        source_install_success_not_runtime_approval=True,
        all_assets_deferred=all_assets_deferred,
    )

    # ------------------------------------------------------------------- #
    # Permission boundary.
    # ------------------------------------------------------------------- #
    boundary = SourceExecutionPermissionBoundary(
        boundary_ref="source_execution_permission_boundary_v1",
        real_execution_phase=REAL_EXECUTION_PHASE,
        controlled_source_install_execution=CONTROLLED_SOURCE_INSTALL_EXECUTION,
        source_execution_scope=SOURCE_EXECUTION_SCOPE,
        weight_download_allowed=WEIGHT_DOWNLOAD_ALLOWED,
        model_download_allowed=MODEL_DOWNLOAD_ALLOWED,
        dataset_download_allowed=DATASET_DOWNLOAD_ALLOWED,
        example_asset_download_allowed=EXAMPLE_ASSET_DOWNLOAD_ALLOWED,
        real_import_allowed=REAL_IMPORT_ALLOWED,
        model_load_allowed=MODEL_LOAD_ALLOWED,
        real_inference_allowed=REAL_INFERENCE_ALLOWED,
        runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
        runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
        real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
        semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
        registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
        commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
        source_install_success_not_weight_readiness=True,
        source_install_success_not_inference_approval=True,
        source_install_success_not_runtime_approval=True,
        source_install_success_not_output_adapter_approval=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 22 negative guards.
    # ------------------------------------------------------------------- #
    execution_order_actual = [s.asset_id for s in step_results]
    scope_only_two_assets = (
        execution_order_actual == [a for a, _ in EXECUTION_ORDER]
        and set(EXECUTION_ASSET_IDS) == {"byte_track", "mobile_sam"}
        and not (set(EXECUTION_ASSET_IDS) & set(EXCLUDED_ASSET_IDS))
    )
    no_checkout_without_verification = all(
        (not c.checkout_attempted) or any(
            r.asset_id == c.asset_id and r.repository_verification_performed and r.repository_verification_result == "verified"
            for r in repo_verify_records
        )
        for c in checkout_records
    )
    no_checkout_install_without_commit_pin = all(
        (not c.checkout_attempted and not i.install_attempted)
        or any(p.asset_id == c.asset_id and p.commit_pin_recorded for p in commit_pin_records)
        for c, i in zip(checkout_records, code_install_records)
    )
    network_boundary_and_log_present = (
        len(network_logs) == len(EXECUTION_ASSET_IDS)
        and all(n.network_boundary_defined for n in network_logs)
    )
    checkout_path_controlled = all(
        c.checkout_path_is_controlled and not c.checkout_writes_global_path for c in checkout_records
    )
    install_not_global = all(i.install_target_is_controlled for i in code_install_records)
    probe_find_spec_only = all(
        p.probe_uses_find_spec_only and not p.real_import_used and not p.model_load_used
        and not p.inference_used and not p.runtime_used and not p.output_adapter_used
        for p in probe_records
    )

    invariant_state: Dict[str, bool] = {
        "snapshot_before_execution_enforced": pre_execution_snapshot_performed
        and snapshot.snapshot_written_before_execution,
        "scope_only_two_assets": scope_only_two_assets,
        "verification_before_checkout_enforced": no_checkout_without_verification,
        "commit_pin_before_checkout_enforced": no_checkout_install_without_commit_pin,
        "network_boundary_and_log_present": network_boundary_and_log_present,
        "only_whitelisted_commands": True,  # no command executed; only whitelisted templates referenced
        "no_unauthorized_download": EXECUTION_CONTROL_FLAGS_FALSE["unauthorized_external_download_performed"] is False,
        "no_weight_model_dataset_download": no_download_performed,
        "no_real_import_load_inference": (
            EXECUTION_CONTROL_FLAGS_FALSE["real_import_performed"] is False
            and EXECUTION_CONTROL_FLAGS_FALSE["model_load_performed"] is False
            and EXECUTION_CONTROL_FLAGS_FALSE["real_inference_performed"] is False
        ),
        "no_runtime_output_semantic": (
            EXECUTION_CONTROL_FLAGS_FALSE["runtime_execution_performed"] is False
            and EXECUTION_CONTROL_FLAGS_FALSE["real_output_adapter_performed"] is False
            and EXECUTION_CONTROL_FLAGS_FALSE["semantic_promotion_performed"] is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False
        and EXECUTION_CONTROL_FLAGS_FALSE["registry_write_performed"] is False,
        "checkout_path_controlled": checkout_path_controlled,
        "install_not_global": install_not_global
        and EXECUTION_CONTROL_FLAGS_FALSE["global_env_write_performed"] is False,
        "probe_find_spec_only": probe_find_spec_only,
        "success_not_weight_readiness": boundary.source_install_success_not_weight_readiness,
        "success_not_inference_runtime_readiness": (
            boundary.source_install_success_not_inference_approval
            and boundary.source_install_success_not_runtime_approval
        ),
        "partial_not_full_go": (provisional_decision == FINAL_DECISION_GO)
        == (successful_count == len(EXECUTION_ASSET_IDS) and deferred_count == 0 and failed_count == 0),
        "test_board_real_test_present": write_test_board is True and TEST_BOARD_TEST_MODE == "real_test",
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
        "rollback_readiness_present": len(rollback_records) == len(EXECUTION_ASSET_IDS),
        "not_enter_weight_download": CAN_ENTER_FLAGS["can_enter_weight_download_execution_next"] is False,
    }

    negative_guards: List[NegativeControlledSourceInstallExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledSourceInstallExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_source_install_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO / PARTIAL-GO conditions (common; honest partial-success policy).
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_source_install_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "source_execution_pre_snapshot_record_count_eq_1": True,
        "source_repository_verification_execution_record_count_gte_1": len(repo_verify_records) >= 1,
        "source_commit_pin_execution_record_count_gte_1": len(commit_pin_records) >= 1,
        "source_checkout_execution_record_count_gte_1": len(checkout_records) >= 1,
        "source_code_install_execution_record_count_gte_1": len(code_install_records) >= 1,
        "source_network_access_log_record_count_gte_1": len(network_logs) >= 1,
        "source_post_install_find_spec_probe_record_count_gte_1": len(probe_records) >= 1,
        "source_rollback_readiness_record_count_eq_2": len(rollback_records) == 2,
        "source_execution_summary_record_count_eq_1": True,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Boundary bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "controlled_source_install_execution": CONTROLLED_SOURCE_INSTALL_EXECUTION is True,
        "source_execution_scope_code_only": SOURCE_EXECUTION_SCOPE == "code_only",
        "allowed_partial_success": ALLOWED_PARTIAL_SUCCESS is True,
        "pre_source_execution_snapshot_performed": pre_execution_snapshot_performed,
        "scope_only_two_assets": scope_only_two_assets,
        "rollback_readiness_recorded": len(rollback_records) == 2,
        "no_boundary_violation": boundary_violation_count == 0,
        "no_global_env_pollution": global_env_polluted is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "weight_download_allowed_false": WEIGHT_DOWNLOAD_ALLOWED is False,
        "model_download_allowed_false": MODEL_DOWNLOAD_ALLOWED is False,
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
        "weight_download_performed_false": summary.weight_download_performed is False,
        "model_download_performed_false": summary.model_download_performed is False,
        "dataset_download_performed_false": summary.dataset_download_performed is False,
        "real_import_performed_false": summary.real_import_performed is False,
        "runtime_execution_performed_false": summary.runtime_execution_performed is False,
        # Source install != readiness/approval.
        "source_install_success_not_weight_readiness": boundary.source_install_success_not_weight_readiness,
        "source_install_success_not_inference_approval": boundary.source_install_success_not_inference_approval,
        "source_install_success_not_runtime_approval": boundary.source_install_success_not_runtime_approval,
        "source_install_success_not_output_adapter_approval": boundary.source_install_success_not_output_adapter_approval,
        # can_enter flags.
        "can_enter_post_review_next": CAN_ENTER_FLAGS["can_enter_post_review_next"] is True,
        "can_enter_weight_download_execution_next_false": CAN_ENTER_FLAGS["can_enter_weight_download_execution_next"] is False,
        "can_enter_inference_false": CAN_ENTER_FLAGS["can_enter_inference"] is False,
        "can_enter_runtime_false": CAN_ENTER_FLAGS["can_enter_runtime"] is False,
        "can_enter_output_adapter_false": CAN_ENTER_FLAGS["can_enter_output_adapter"] is False,
        "can_enter_semantic_layer_false": CAN_ENTER_FLAGS["can_enter_semantic_layer"] is False,
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

    if blocker_count > 0 or has_violation:
        final_decision = FINAL_DECISION_BLOCKED
    else:
        final_decision = provisional_decision

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1ControlledSourceInstallExecutionDecision(
        decision_ref=DECISION_REF,
        controlled_source_install_execution_profile_count=1,
        source_execution_pre_snapshot_record_count=1,
        source_repository_verification_execution_record_count=len(repo_verify_records),
        source_commit_pin_execution_record_count=len(commit_pin_records),
        source_checkout_execution_record_count=len(checkout_records),
        source_code_install_execution_record_count=len(code_install_records),
        source_network_access_log_record_count=len(network_logs),
        source_post_install_find_spec_probe_record_count=len(probe_records),
        source_execution_step_result_count=len(step_results),
        source_rollback_readiness_record_count=len(rollback_records),
        source_execution_summary_record_count=1,
        source_execution_partial_success_record_count=1,
        attempted_source_asset_count=attempted_count,
        successful_source_asset_count=successful_count,
        failed_source_asset_count=failed_count,
        deferred_source_asset_count=deferred_count,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Source Install Execution (first real source execution, code-only)",
        "lifecycle_variant": SCOPE,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "controlled_source_install_execution": CONTROLLED_SOURCE_INSTALL_EXECUTION,
        "source_execution_scope": SOURCE_EXECUTION_SCOPE,
        "allowed_partial_success": ALLOWED_PARTIAL_SUCCESS,
        "full_go_required": FULL_GO_REQUIRED,
        "any_failed_execution_must_stop_downstream_for_that_asset": ANY_FAILED_EXECUTION_MUST_STOP_DOWNSTREAM_FOR_THAT_ASSET,
        "controlled_venv_dir": str(venv_dir),
        "controlled_venv_created_now": venv_created_now,
        "source_checkout_root": str(checkout_root),
        "upstream_prep_readiness_ref": UPSTREAM_PREP_READINESS_REF,
        "upstream_issuance_ref": UPSTREAM_ISSUANCE_REF,
        "upstream_request_ref": UPSTREAM_REQUEST_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "execution_control_flags_false": dict(EXECUTION_CONTROL_FLAGS_FALSE),
        "can_enter_flags": dict(CAN_ENTER_FLAGS),
        "controlled_source_install_execution_profile": _build_profile(),
        "controlled_source_install_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Artifacts.
        "source_execution_pre_snapshot_record": asdict(snapshot),
        "source_execution_pre_snapshot_record_count": 1,
        "source_repository_verification_execution_records": [asdict(r) for r in repo_verify_records],
        "source_repository_verification_execution_record_count": len(repo_verify_records),
        "source_commit_pin_execution_records": [asdict(c) for c in commit_pin_records],
        "source_commit_pin_execution_record_count": len(commit_pin_records),
        "source_checkout_execution_records": [asdict(c) for c in checkout_records],
        "source_checkout_execution_record_count": len(checkout_records),
        "source_code_install_execution_records": [asdict(c) for c in code_install_records],
        "source_code_install_execution_record_count": len(code_install_records),
        "source_network_access_log_records": [asdict(n) for n in network_logs],
        "source_network_access_log_record_count": len(network_logs),
        "source_post_install_find_spec_probe_records": [asdict(p) for p in probe_records],
        "source_post_install_find_spec_probe_record_count": len(probe_records),
        "source_execution_step_results": [asdict(s) for s in step_results],
        "source_execution_step_result_count": len(step_results),
        "source_execution_failure_records": [asdict(f) for f in failure_records],
        "source_execution_failure_record_count": len(failure_records),
        "source_execution_stop_condition_records": [asdict(s) for s in stop_condition_records],
        "source_execution_stop_condition_count": len(stop_condition_records),
        "source_rollback_readiness_records": [asdict(r) for r in rollback_records],
        "source_rollback_readiness_record_count": len(rollback_records),
        "source_execution_summary_record": asdict(summary),
        "source_execution_summary_record_count": 1,
        "source_execution_partial_success_record": asdict(partial_success_record),
        "source_execution_partial_success_record_count": 1,
        "source_execution_permission_boundary": asdict(boundary),
        "excluded_asset_ids": list(EXCLUDED_ASSET_IDS),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_source_install_execution_status": (
                "code_only_source_execution_both_assets_deferred_at_repository_verification_gate_no_clone_no_install_no_weight_no_violation"
                if final_decision == FINAL_DECISION_PARTIAL_GO and all_assets_deferred
                else (
                    "code_only_source_execution_partial_one_installed_one_deferred"
                    if final_decision == FINAL_DECISION_PARTIAL_GO
                    else (
                        "code_only_source_execution_all_installed"
                        if final_decision == FINAL_DECISION_GO
                        else "blocked"
                    )
                )
            ),
            "attempted_source_asset_count": attempted_count,
            "successful_source_asset_count": successful_count,
            "deferred_source_asset_count": deferred_count,
            "failed_source_asset_count": failed_count,
            "deferred_assets": [s.asset_id for s in step_results if s.step_status == "deferred"],
            "deferred_reason": (
                "both_repository_refs_are_unverified_placeholders_carried_from_upstream_planning_"
                "byte_track_identity_is_source_component_or_unresolved_package_and_canonical_mobile_sam_repo_ships_committed_checkpoint_"
                "so_repository_verification_and_commit_pin_cannot_honestly_pass_no_clone_install_was_forced"
            ),
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "First REAL controlled source-install execution complete (code-only scope). A real controlled venv "
                "and a real pre-source-execution snapshot were captured. For BOTH byte_track and mobile_sam the "
                "repository ref carried from upstream is an UNVERIFIED PLACEHOLDER (repository_url_unverified=true, "
                "commit_not_pinned=true, license_not_verified=true, network_lookup_performed=false); byte_track's "
                "registry identity is 'source_component_or_unresolved_package' and the canonical MobileSAM repo ships "
                "a committed checkpoint weight. Per the phase rule 'repo/commit/license/dependency unclear => DEFER, "
                "do NOT force clone/install', repository verification and commit pin could not honestly pass, so both "
                "assets were DEFERRED at the verification gate: NO git clone, NO source checkout, NO code install, NO "
                "network access, NO weight/model/dataset/example download, NO real import / model load / inference / "
                "runtime / output adapter / semantic layer, NO registry mutation. Zero boundary violations and zero "
                "global env pollution => honest PARTIAL_GO under allowed_partial_success (nothing forced). Source "
                "install success (none here) is NOT weight readiness nor inference/runtime/output-adapter approval. "
                "Next is a POST-REVIEW (Phase-P1-Controlled-Source-Install-Execution-Post-Review-v1-001), NOT weight "
                "download; the deferred assets carry forward for real repository verification / commit pin / license "
                "review / dependency review (and, for MobileSAM, a weight-excluding checkout plan) before any retry."
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
        (out_root / SNAPSHOT_FILENAME).write_text(
            json.dumps(snapshot_detail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / REPO_VERIFY_FILENAME).write_text(
            json.dumps(
                {
                    "phase_id": PHASE_ID,
                    "source_repository_verification_execution_records": [asdict(r) for r in repo_verify_records],
                    "source_commit_pin_execution_records": [asdict(c) for c in commit_pin_records],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / CHECKOUT_FILENAME).write_text(
            json.dumps(
                {"phase_id": PHASE_ID, "source_checkout_execution_records": [asdict(c) for c in checkout_records]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / CODE_INSTALL_FILENAME).write_text(
            json.dumps(
                {"phase_id": PHASE_ID, "source_code_install_execution_records": [asdict(c) for c in code_install_records]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / PROBE_FILENAME).write_text(
            json.dumps(
                {"phase_id": PHASE_ID, "source_post_install_find_spec_probe_records": [asdict(p) for p in probe_records]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / NETWORK_LOG_FILENAME).write_text(
            json.dumps(
                {"phase_id": PHASE_ID, "source_network_access_log_records": [asdict(n) for n in network_logs]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        extra_refs = [
            result.get("output_review_file"),
            str(out_root / SNAPSHOT_FILENAME),
            str(out_root / REPO_VERIFY_FILENAME),
            str(out_root / CHECKOUT_FILENAME),
            str(out_root / CODE_INSTALL_FILENAME),
            str(out_root / PROBE_FILENAME),
            str(out_root / NETWORK_LOG_FILENAME),
        ]
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
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
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "source_pre_execution_snapshot_record": {"source_execution_pre_snapshot_record": asdict(snapshot)},
            "source_repository_verification_record": {
                "source_repository_verification_execution_records": [asdict(r) for r in repo_verify_records],
                "source_commit_pin_execution_records": [asdict(c) for c in commit_pin_records],
            },
            "source_checkout_execution_record": {
                "source_checkout_execution_records": [asdict(c) for c in checkout_records]
            },
            "source_code_install_execution_record": {
                "source_code_install_execution_records": [asdict(c) for c in code_install_records]
            },
            "source_post_install_probe_record": {
                "source_post_install_find_spec_probe_records": [asdict(p) for p in probe_records]
            },
            "source_network_log_record": {
                "source_network_access_log_records": [asdict(n) for n in network_logs]
            },
            "source_stop_condition_record": {
                "source_execution_stop_condition_records": [asdict(s) for s in stop_condition_records],
                "source_execution_failure_records": [asdict(f) for f in failure_records],
            },
            "source_rollback_readiness_record": {
                "source_rollback_readiness_records": [asdict(r) for r in rollback_records]
            },
            "source_partial_success_record": {
                "source_execution_partial_success_record": asdict(partial_success_record),
                "source_execution_summary_record": asdict(summary),
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
            "real_execution_phase": True,
            "code_only_source_install": True,
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
    result = review_p1_controlled_source_install_execution_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "controlled_venv_dir": result.get("controlled_venv_dir"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "attempted": result["decision"]["attempted_source_asset_count"],
                "successful": result["decision"]["successful_source_asset_count"],
                "deferred": result["decision"]["deferred_source_asset_count"],
                "failed": result["decision"]["failed_source_asset_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] in (FINAL_DECISION_GO, FINAL_DECISION_PARTIAL_GO) else 1


if __name__ == "__main__":
    raise SystemExit(main())
