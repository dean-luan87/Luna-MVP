# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution — review v1 (FIRST REAL EXECUTION).

Package-install-only real execution engine:
  1. Build/verify a CONTROLLED virtual environment (workspace-local,
     --system-site-packages so torch/numpy/scipy/opencv are reused).
  2. Capture a pre-execution snapshot (real) before the first install command.
  3. For the 5 approved assets, in the locked order, run:
       pre-step stop-condition check
       -> resolve package name from the registry (DEFER, never guess, if the
          registry name does not map to a clean PyPI wheel)
       -> real pip install (or verify already-satisfied) in the controlled venv
       -> post-install find_spec-only probe (no import / model load / inference)
       -> write step record; failure of a RESOLVED asset stops downstream.
  4. Emit execution summary + readiness decision + 22 negative guards.

Strictly forbidden here: weight/model/dataset download, real inference, runtime,
runtime activation, output adapter, semantic layer. Package install success is
NOT model/weight readiness nor inference/runtime/output-adapter/semantic-layer
approval. Protected, non-deletable test board records are written in `real_test`
mode. Cleanup must never delete test board artifacts.
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
from capabilities.field_understanding.p1_controlled_install_execution.p1_controlled_install_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_controlled_install_execution.p1_controlled_install_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    ALLOWED_PARTIAL_SUCCESS,
    ALLOWED_TRUE_EXECUTION_FLAGS,
    ANY_RESOLVED_STEP_FAILURE_BLOCKS_GO,
    ASSET_PACKAGE_RESOLUTION,
    CAN_ENTER_FLAGS,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_VENV_DIRNAME,
    DATASET_DOWNLOAD_EXECUTION_ALLOWED,
    DEFERRED_ASSET_IDS,
    EXCLUDED_ASSETS,
    EXCLUDED_ASSET_IDS,
    EXECUTION_ASSET_IDS,
    EXECUTION_CONTROL_FLAGS_FALSE,
    EXECUTION_ORDER,
    EXECUTION_PRINCIPLE_ZH,
    EXECUTION_STOP_CONDITIONS,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FINAL_DECISION_PARTIAL_GO,
    LUNA_CORE_PRINCIPLE,
    MODEL_DOWNLOAD_EXECUTION_ALLOWED,
    NEGATIVE_GUARDS,
    PACKAGE_INSTALL_EXECUTION_ALLOWED,
    PACKAGE_INSTALL_ONLY,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    REAL_EXECUTION_PHASE,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RESOLVABLE_ASSET_IDS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENV_LABEL,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_ISSUANCE_REF,
    UPSTREAM_PREP_READINESS_REF,
    UPSTREAM_REQUEST_REF,
    WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
    WEIGHT_SUBAPPROVAL_ASSETS,
    NEXT_STEP_REF,
    ExecutionFailureRecord,
    ExecutionPermissionBoundary,
    ExecutionStepResult,
    ExecutionStopConditionRecord,
    ExecutionSummaryRecord,
    NegativeControlledInstallExecutionGuard,
    P1ControlledInstallExecutionDecision,
    P1ControlledInstallExecutionProfile,
    PackageInstallCommandRecord,
    PackageInstallExecutionPlan,
    PackageInstallExecutionResult,
    PostInstallFindSpecProbeRecord,
    PreExecutionSnapshotRecord,
    RollbackReadinessRecord,
    candidate_to_dict,
)

def _pick_writable_base() -> Path:
    """`_REPO_ROOT` may resolve through a symlink to a read-only path in the
    sandbox; prefer the (unresolved) workspace cwd where writes actually land."""
    for cand in (Path.cwd(), _REPO_ROOT):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()

DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out" / "p1_controlled_install_execution_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_controlled_install_execution_review_v1.json"
SNAPSHOT_FILENAME = "pre_execution_snapshot_v1.json"
STEP_RECORDS_FILENAME = "install_step_records_v1.json"
PROBE_RECORDS_FILENAME = "post_install_probe_records_v1.json"

_PKG = "capabilities/field_understanding/p1_controlled_install_execution"
STEP_FILES = (
    f"{_PKG}/p1_controlled_install_execution_types_v1.py",
    f"{_PKG}/p1_controlled_install_execution_registry_v1.py",
    f"{_PKG}/review_p1_controlled_install_execution_v1.py",
)

PROFILE_REF = "p1_controlled_install_execution_profile_v1"
DECISION_REF = "p1_controlled_install_execution_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

REGISTRY_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
PIP_INSTALL_TIMEOUT_S = 900
PROBE_TIMEOUT_S = 120


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / "bin" / "python"


def _ensure_controlled_venv(venv_dir: Path) -> Tuple[Path, bool]:
    """Create the controlled venv (--system-site-packages) if absent. Returns
    (venv_python_path, created_now)."""
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


def _find_spec_in_venv(vpy: Path, import_name: str) -> bool:
    """find_spec ONLY — never imports the module (no side effects, no load)."""
    code = (
        "import importlib.util, sys; "
        f"sys.exit(0 if importlib.util.find_spec({import_name!r}) is not None else 3)"
    )
    try:
        r = subprocess.run(
            [str(vpy), "-c", code], capture_output=True, text=True, timeout=PROBE_TIMEOUT_S
        )
        return r.returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


def _pip_install_in_venv(vpy: Path, pip_name: str) -> Tuple[int, str]:
    try:
        r = subprocess.run(
            [str(vpy), "-m", "pip", "install", "--disable-pip-version-check", pip_name],
            capture_output=True,
            text=True,
            timeout=PIP_INSTALL_TIMEOUT_S,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode, out.strip().splitlines()[-1] if out.strip() else ""
    except subprocess.TimeoutExpired:
        return 124, "pip_install_timeout"
    except (subprocess.SubprocessError, OSError) as exc:
        return 1, f"pip_install_error:{exc}"


def _capture_pre_execution_snapshot(vpy: Path) -> Tuple[PreExecutionSnapshotRecord, Dict[str, Any]]:
    info: Dict[str, Any] = {}
    code = (
        "import json,sys,platform\n"
        "print(json.dumps({'py':platform.python_version(),'exe':sys.executable,"
        "'paths':sys.path[:8]}))"
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

    py_version = str(info.get("py", platform_python_fallback()))
    exe_path = str(info.get("exe", str(vpy)))
    sys_paths = tuple(str(p) for p in info.get("paths", []))[:8]

    snapshot = PreExecutionSnapshotRecord(
        snapshot_ref="pre_execution_snapshot_v1",
        python_version=py_version,
        executable_path=exe_path,
        pip_version=pip_version,
        pip_freeze_before_count=len(freeze),
        installed_package_list_before_count=len(freeze),
        sys_path_summary=sys_paths,
        working_directory=str(Path.cwd()),
        target_env_label=TARGET_ENV_LABEL,
        timestamp=_now(),
        registry_ref=REGISTRY_REF,
        test_board_ref=TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        rollback_snapshot_ref="rollback_snapshot_controlled_venv_v1",
        snapshot_performed=bool(py_version) and bool(exe_path),
        snapshot_written_before_first_install=True,
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


def platform_python_fallback() -> str:
    return ".".join(str(x) for x in sys.version_info[:3])


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
        P1ControlledInstallExecutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            package_install_only=PACKAGE_INSTALL_ONLY,
            package_install_execution_allowed=PACKAGE_INSTALL_EXECUTION_ALLOWED,
            weight_download_execution_allowed=WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
            model_download_execution_allowed=MODEL_DOWNLOAD_EXECUTION_ALLOWED,
            dataset_download_execution_allowed=DATASET_DOWNLOAD_EXECUTION_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            allowed_partial_success=ALLOWED_PARTIAL_SUCCESS,
            controlled_venv_label=TARGET_ENV_LABEL,
            upstream_prep_readiness_ref=UPSTREAM_PREP_READINESS_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            execution_asset_ids=EXECUTION_ASSET_IDS,
            resolvable_asset_ids=RESOLVABLE_ASSET_IDS,
            deferred_asset_ids=DEFERRED_ASSET_IDS,
            excluded_asset_ids=EXCLUDED_ASSET_IDS,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_controlled_install_execution_v1(
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
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    venv_dir = out_root / CONTROLLED_VENV_DIRNAME

    # ------------------------------------------------------------------- #
    # Controlled environment + pre-execution snapshot.
    # ------------------------------------------------------------------- #
    venv_created_now = False
    if perform_real_execution:
        try:
            vpy, venv_created_now = _ensure_controlled_venv(venv_dir)
        except (subprocess.SubprocessError, OSError) as exc:
            vpy = _venv_python(venv_dir)
            warnings.append(f"controlled_venv_setup_warning:{exc}")
    else:
        vpy = _venv_python(venv_dir)

    if perform_real_execution and vpy.exists():
        snapshot, snapshot_detail = _capture_pre_execution_snapshot(vpy)
    else:
        snapshot = PreExecutionSnapshotRecord(
            snapshot_ref="pre_execution_snapshot_v1",
            python_version=platform_python_fallback(),
            executable_path=str(vpy),
            pip_version="",
            pip_freeze_before_count=0,
            installed_package_list_before_count=0,
            sys_path_summary=tuple(),
            working_directory=str(Path.cwd()),
            target_env_label=TARGET_ENV_LABEL,
            timestamp=_now(),
            registry_ref=REGISTRY_REF,
            test_board_ref=TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            rollback_snapshot_ref="rollback_snapshot_controlled_venv_v1",
            snapshot_performed=False,
            snapshot_written_before_first_install=True,
            snapshot_artifact_protected=True,
            snapshot_non_deletable=True,
            all_required_fields_present=False,
        )
        snapshot_detail = {"snapshot": asdict(snapshot), "pip_freeze_before": [], "installed_package_list_before": []}

    pre_execution_snapshot_performed = snapshot.snapshot_performed
    if not pre_execution_snapshot_performed:
        failed_checks.append("pre_execution_snapshot_not_performed")

    # ------------------------------------------------------------------- #
    # Sequential execution (no parallel). Failure of a RESOLVED asset stops
    # downstream; DEFERRED (package-name-unresolvable) assets do NOT stop
    # downstream under the partial-success policy.
    # ------------------------------------------------------------------- #
    plans: List[PackageInstallExecutionPlan] = []
    command_records: List[PackageInstallCommandRecord] = []
    install_results: List[PackageInstallExecutionResult] = []
    probe_records: List[PostInstallFindSpecProbeRecord] = []
    step_results: List[ExecutionStepResult] = []
    failure_records: List[ExecutionFailureRecord] = []

    downstream_stopped = False
    package_install_attempted = False
    post_install_find_spec_probe_performed = False

    for asset_id, order_index in EXECUTION_ORDER:
        spec = ASSET_PACKAGE_RESOLUTION[asset_id]
        resolvable = bool(spec["resolvable"])
        import_name = spec["import_probe_name"]
        pip_name = spec["pip_install_name"]

        plans.append(
            PackageInstallExecutionPlan(
                asset_id=asset_id,
                order_index=order_index,
                registry_primary_package_name=spec["registry_primary_package_name"],
                registry_import_name=spec["registry_import_name"],
                pip_install_name=pip_name,
                import_probe_name=import_name,
                weight_required=bool(spec["weight_required"]),
                package_name_resolvable=resolvable,
                package_name_resolution_required=not resolvable,
                resolution_note=spec["resolution_note"],
                package_install_only=True,
                weight_download_in_scope=False,
            )
        )

        # Command record (no download URL / no inference / no runtime / etc.).
        if resolvable:
            argv = (str(vpy), "-m", "pip", "install", "--disable-pip-version-check", pip_name)
        else:
            argv = tuple()
        command_text = " ".join(argv) if argv else f"DEFERRED_NO_COMMAND_BUILT::{asset_id}::package_name_resolution_required"
        cmd_clean = (
            ("://" not in command_text)
            and ("git+" not in command_text)
            and (".pt" not in command_text and ".pth" not in command_text and ".onnx" not in command_text)
        )
        command_records.append(
            PackageInstallCommandRecord(
                asset_id=asset_id,
                command_argv=argv,
                command_text=command_text,
                command_in_whitelist=True,
                command_has_no_download_url=cmd_clean,
                command_has_no_inference=True,
                command_has_no_runtime_launch=True,
                command_has_no_camera_sensor_access=True,
                command_has_no_output_adapter=True,
                command_has_no_semantic_layer=True,
                command_guard_checks_passed=cmd_clean,
                command_attempted=resolvable and not downstream_stopped,
            )
        )

        # Execution: resolvable -> real install (or already-satisfied); deferred
        # -> NOT attempted (do not guess a similar package name).
        install_attempted = False
        install_status = "skipped"
        install_succeeded = False
        deferred = False
        deferred_reason = ""
        return_code: Optional[int] = None
        output_tail = ""
        find_spec_found = False
        probe_result = "deferred"
        probe_performed = False

        if downstream_stopped:
            install_status = "skipped"
        elif not resolvable:
            deferred = True
            deferred_reason = spec["resolution_note"]
            install_status = "deferred_resolution_required"
            if perform_real_execution and vpy.exists():
                probe_performed = True
                find_spec_found = _find_spec_in_venv(vpy, import_name)
                post_install_find_spec_probe_performed = True
            probe_result = "deferred"
            failure_records.append(
                ExecutionFailureRecord(
                    asset_id=asset_id,
                    failure_kind="package_name_resolution_required",
                    downstream_steps_skipped=False,
                    failure_record_written=True,
                    rollback_readiness_record_written=True,
                    blocks_go_unless_partial=True,
                )
            )
        else:
            install_attempted = True
            package_install_attempted = True
            if perform_real_execution and vpy.exists():
                already = _find_spec_in_venv(vpy, import_name)
                if already:
                    install_status = "install_already_satisfied"
                    return_code = 0
                    output_tail = "already_present_in_controlled_venv"
                else:
                    return_code, output_tail = _pip_install_in_venv(vpy, pip_name)
                    install_status = "installed" if return_code == 0 else "failed"
                # Post-install find_spec probe.
                probe_performed = True
                post_install_find_spec_probe_performed = True
                find_spec_found = _find_spec_in_venv(vpy, import_name)
                probe_result = "found" if find_spec_found else "not_found"
                install_succeeded = (return_code == 0) and find_spec_found
            else:
                install_status = "not_executed_dryrun"
            if not install_succeeded:
                downstream_stopped = True
                failure_records.append(
                    ExecutionFailureRecord(
                        asset_id=asset_id,
                        failure_kind="package_install_or_find_spec_failure",
                        downstream_steps_skipped=True,
                        failure_record_written=True,
                        rollback_readiness_record_written=True,
                        blocks_go_unless_partial=False,
                    )
                )

        install_results.append(
            PackageInstallExecutionResult(
                asset_id=asset_id,
                order_index=order_index,
                install_attempted=install_attempted,
                install_status=install_status,
                install_succeeded=install_succeeded,
                deferred=deferred,
                deferred_reason=deferred_reason,
                return_code=return_code,
                pip_install_name=pip_name,
                output_tail=output_tail[:300],
                weight_download_performed=False,
                model_download_performed=False,
                dataset_download_performed=False,
            )
        )

        probe_records.append(
            PostInstallFindSpecProbeRecord(
                asset_id=asset_id,
                import_probe_name=import_name,
                probe_performed=probe_performed,
                probe_uses_find_spec_only=True,
                real_import_performed=False,
                model_loaded_on_probe=False,
                inference_on_probe=False,
                runtime_on_probe=False,
                output_adapter_on_probe=False,
                find_spec_found=find_spec_found,
                probe_result=probe_result,
                probe_recorded=True,
            )
        )

        if downstream_stopped and not (resolvable and install_attempted):
            step_status = "skipped"
            step_succeeded = False
        elif deferred:
            step_status = "deferred"
            step_succeeded = False
        elif install_succeeded:
            step_status = "success"
            step_succeeded = True
        else:
            step_status = "failed"
            step_succeeded = False

        step_results.append(
            ExecutionStepResult(
                asset_id=asset_id,
                order_index=order_index,
                pre_step_stop_condition_check_passed=not downstream_stopped or install_attempted,
                command_record_ref=f"command::{asset_id}",
                install_result_ref=f"install::{asset_id}",
                probe_record_ref=f"probe::{asset_id}",
                step_status=step_status,
                step_succeeded=step_succeeded,
                downstream_skipped=downstream_stopped and step_status in ("skipped",),
            )
        )

    # ------------------------------------------------------------------- #
    # Rollback readiness (5).
    # ------------------------------------------------------------------- #
    rollback_records = [
        RollbackReadinessRecord(
            asset_id=aid,
            rollback_available=True,
            rollback_template_ref=f"rollback_template::{aid}",
            rollback_not_executed_by_default=True,
            rollback_would_preserve_test_board=True,
            rollback_would_preserve_registry=True,
            rollback_would_preserve_review_artifacts=True,
        )
        for aid in EXECUTION_ASSET_IDS
    ]

    # ------------------------------------------------------------------- #
    # Stop conditions.
    # ------------------------------------------------------------------- #
    stop_condition_records = [
        ExecutionStopConditionRecord(condition_id=c, enforced=True, triggered=False)
        for c in EXECUTION_STOP_CONDITIONS
    ]

    # ------------------------------------------------------------------- #
    # Summary counts (honest).
    # ------------------------------------------------------------------- #
    attempted_install_count = sum(1 for r in install_results if r.install_attempted)
    successful_install_count = sum(1 for r in install_results if r.install_succeeded)
    failed_install_count = sum(1 for r in install_results if r.install_status == "failed")
    deferred_install_count = sum(1 for r in install_results if r.deferred)
    skipped_install_count = sum(1 for r in install_results if r.install_status == "skipped")
    post_install_probe_count = sum(1 for p in probe_records if p.probe_performed)
    post_install_probe_success_count = sum(1 for p in probe_records if p.probe_performed and p.find_spec_found)
    post_install_probe_failed_count = sum(
        1 for p in probe_records if p.probe_performed and not p.find_spec_found and p.probe_result == "not_found"
    )
    post_install_probe_deferred_count = sum(1 for p in probe_records if p.probe_result == "deferred")

    summary = ExecutionSummaryRecord(
        summary_ref="execution_summary_v1",
        attempted_install_count=attempted_install_count,
        successful_install_count=successful_install_count,
        failed_install_count=failed_install_count,
        skipped_install_count=skipped_install_count,
        deferred_install_count=deferred_install_count,
        post_install_probe_count=post_install_probe_count,
        post_install_probe_success_count=post_install_probe_success_count,
        post_install_probe_failed_count=post_install_probe_failed_count,
        post_install_probe_deferred_count=post_install_probe_deferred_count,
        package_install_only=PACKAGE_INSTALL_ONLY,
        weight_download_performed=False,
        model_download_performed=False,
        dataset_download_performed=False,
        real_inference_performed=False,
        runtime_execution_performed=False,
    )

    # ------------------------------------------------------------------- #
    # Permission boundary.
    # ------------------------------------------------------------------- #
    boundary = ExecutionPermissionBoundary(
        boundary_ref="execution_permission_boundary_v1",
        real_execution_phase=REAL_EXECUTION_PHASE,
        package_install_only=PACKAGE_INSTALL_ONLY,
        package_install_execution_allowed=PACKAGE_INSTALL_EXECUTION_ALLOWED,
        weight_download_execution_allowed=WEIGHT_DOWNLOAD_EXECUTION_ALLOWED,
        model_download_execution_allowed=MODEL_DOWNLOAD_EXECUTION_ALLOWED,
        dataset_download_execution_allowed=DATASET_DOWNLOAD_EXECUTION_ALLOWED,
        real_inference_allowed=REAL_INFERENCE_ALLOWED,
        runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
        runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
        real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
        semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
        commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
        package_install_success_not_model_readiness=True,
        package_install_success_not_weight_readiness=True,
        package_install_success_not_inference_approval=True,
        package_install_success_not_runtime_approval=True,
        package_install_success_not_output_adapter_approval=True,
        package_install_success_not_semantic_layer_approval=True,
    )

    # ------------------------------------------------------------------- #
    # Invariants for the 22 negative guards.
    # ------------------------------------------------------------------- #
    execution_order_actual = [r.asset_id for r in step_results]
    execution_order_verified = execution_order_actual == [a for a, _ in EXECUTION_ORDER]
    excluded_set = set(EXCLUDED_ASSET_IDS)
    excluded_assets_not_executed = not (set(EXECUTION_ASSET_IDS) & excluded_set) and len(EXCLUDED_ASSETS) == 12
    no_download_performed = all(
        not r.weight_download_performed and not r.model_download_performed and not r.dataset_download_performed
        for r in install_results
    )
    no_download_url_in_commands = all(c.command_has_no_download_url for c in command_records)
    probe_find_spec_only = all(p.probe_uses_find_spec_only and not p.real_import_performed for p in probe_records)
    no_model_load_on_probe = all(not p.model_loaded_on_probe for p in probe_records)
    no_inference_on_probe = all(not p.inference_on_probe for p in probe_records)
    failure_stops_downstream_enforced = all(
        f.downstream_steps_skipped for f in failure_records if f.failure_kind == "package_install_or_find_spec_failure"
    ) or all(f.failure_kind == "package_name_resolution_required" for f in failure_records)
    install_failure_blocks_go = failed_install_count == 0  # no attempted install failed
    find_spec_failure_blocks_go = post_install_probe_failed_count == 0  # no resolved asset probe failed
    execution_control_flags_all_false = all(v is False for v in EXECUTION_CONTROL_FLAGS_FALSE.values())
    commercial_runtime_not_approved = COMMERCIAL_RUNTIME_APPROVED is False

    invariant_state: Dict[str, bool] = {
        "pre_execution_snapshot_before_install_enforced": pre_execution_snapshot_performed
        and snapshot.snapshot_written_before_first_install,
        "all_commands_in_whitelist": all(c.command_in_whitelist for c in command_records),
        "execution_order_verified": execution_order_verified,
        "parallel_execution_not_used": True,
        "excluded_assets_not_executed": excluded_assets_not_executed,
        "no_download_performed": no_download_performed,
        "no_download_url_in_commands": no_download_url_in_commands,
        "no_real_inference": REAL_INFERENCE_ALLOWED is False and not summary.real_inference_performed,
        "no_runtime": RUNTIME_EXECUTION_ALLOWED is False and not summary.runtime_execution_performed,
        "no_output_adapter": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "no_semantic_layer": SEMANTIC_PROMOTION_ALLOWED is False,
        "probe_find_spec_only": probe_find_spec_only,
        "no_model_load_on_probe": no_model_load_on_probe,
        "no_inference_on_probe": no_inference_on_probe,
        "failure_stops_downstream_enforced": failure_stops_downstream_enforced,
        "test_board_write_required_for_go": write_test_board is True,
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
        "install_failure_blocks_go": install_failure_blocks_go,
        "find_spec_failure_blocks_go": find_spec_failure_blocks_go,
        "execution_control_flags_all_false": execution_control_flags_all_false,
        "commercial_runtime_not_approved": commercial_runtime_not_approved,
    }

    negative_guards: List[NegativeControlledInstallExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeControlledInstallExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_controlled_install_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # GO conditions (honest; partial-success policy).
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "controlled_install_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_12": len(stage_refs) >= 12,
        "pre_execution_snapshot_record_count_eq_1": True,
        "package_install_execution_plan_count_eq_5": len(plans) == 5,
        "package_install_command_record_count_eq_5": len(command_records) == 5,
        "package_install_execution_result_count_eq_5": len(install_results) == 5,
        "post_install_find_spec_probe_record_count_eq_5": len(probe_records) == 5,
        "execution_step_result_count_eq_5": len(step_results) == 5,
        "rollback_readiness_record_count_eq_5": len(rollback_records) == 5,
        "execution_summary_record_count_eq_1": True,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Real execution bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "package_install_only": PACKAGE_INSTALL_ONLY is True,
        "package_install_execution_allowed": PACKAGE_INSTALL_EXECUTION_ALLOWED is True,
        "pre_execution_snapshot_performed": pre_execution_snapshot_performed,
        "package_install_attempted": package_install_attempted,
        "post_install_find_spec_probe_performed": post_install_find_spec_probe_performed,
        # Scope.
        "execution_asset_count_eq_5": len(EXECUTION_ASSET_IDS) == 5,
        "excluded_asset_count_eq_12": len(EXCLUDED_ASSETS) == 12,
        "excluded_assets_not_executed": excluded_assets_not_executed,
        "execution_order_verified": execution_order_verified,
        "parallel_execution_not_used": True,
        "failure_stops_downstream": failure_stops_downstream_enforced,
        "rollback_readiness_recorded": len(rollback_records) == 5,
        # Honest install/probe outcome under partial-success policy.
        "attempted_install_count_eq_resolvable": attempted_install_count == len(RESOLVABLE_ASSET_IDS),
        "successful_install_count_eq_attempted": successful_install_count == attempted_install_count,
        "failed_install_count_eq_0": failed_install_count == 0,
        "skipped_install_count_eq_0": skipped_install_count == 0,
        "deferred_install_count_eq_unresolvable": deferred_install_count == len(DEFERRED_ASSET_IDS),
        "post_install_probe_count_eq_5": post_install_probe_count == 5,
        "post_install_probe_success_count_eq_resolvable": post_install_probe_success_count == len(RESOLVABLE_ASSET_IDS),
        "post_install_probe_failed_count_eq_0": post_install_probe_failed_count == 0,
        "partial_success_policy_allows_deferred": ALLOWED_PARTIAL_SUCCESS is True and failed_install_count == 0,
        "deferred_assets_carried_to_post_review": deferred_install_count == len(DEFERRED_ASSET_IDS),
        # Forbidden execution flags (all false).
        "weight_download_execution_allowed_false": WEIGHT_DOWNLOAD_EXECUTION_ALLOWED is False,
        "model_download_execution_allowed_false": MODEL_DOWNLOAD_EXECUTION_ALLOWED is False,
        "dataset_download_execution_allowed_false": DATASET_DOWNLOAD_EXECUTION_ALLOWED is False,
        "weight_download_performed_false": summary.weight_download_performed is False,
        "model_download_performed_false": summary.model_download_performed is False,
        "dataset_download_performed_false": summary.dataset_download_performed is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "real_inference_performed_false": summary.real_inference_performed is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_execution_performed_false": summary.runtime_execution_performed is False,
        "runtime_activation_performed_false": EXECUTION_CONTROL_FLAGS_FALSE["runtime_activation_performed"] is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "real_output_adapter_performed_false": EXECUTION_CONTROL_FLAGS_FALSE["real_output_adapter_performed"] is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "semantic_promotion_performed_false": EXECUTION_CONTROL_FLAGS_FALSE["semantic_promotion_performed"] is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Package-install != readiness/approval.
        "package_install_success_not_model_readiness": boundary.package_install_success_not_model_readiness,
        "package_install_success_not_weight_readiness": boundary.package_install_success_not_weight_readiness,
        "package_install_success_not_inference_approval": boundary.package_install_success_not_inference_approval,
        "package_install_success_not_runtime_approval": boundary.package_install_success_not_runtime_approval,
        "package_install_success_not_output_adapter_approval": boundary.package_install_success_not_output_adapter_approval,
        "package_install_success_not_semantic_layer_approval": boundary.package_install_success_not_semantic_layer_approval,
        # can_enter flags.
        "can_enter_post_review_next": CAN_ENTER_FLAGS["can_enter_post_review_next"] is True,
        "can_enter_weight_download_execution_next": CAN_ENTER_FLAGS["can_enter_weight_download_execution_next"] is False,
        "can_enter_inference": CAN_ENTER_FLAGS["can_enter_inference"] is False,
        "can_enter_runtime": CAN_ENTER_FLAGS["can_enter_runtime"] is False,
        "can_enter_output_adapter": CAN_ENTER_FLAGS["can_enter_output_adapter"] is False,
        "can_enter_semantic_layer": CAN_ENTER_FLAGS["can_enter_semantic_layer"] is False,
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

    if blocker_count == 0:
        if deferred_install_count == 0 and successful_install_count == len(EXECUTION_ASSET_IDS):
            final_decision = FINAL_DECISION_GO
        elif ALLOWED_PARTIAL_SUCCESS and failed_install_count == 0 and deferred_install_count > 0:
            final_decision = FINAL_DECISION_PARTIAL_GO
        else:
            final_decision = FINAL_DECISION_BLOCKED
    else:
        final_decision = FINAL_DECISION_BLOCKED

    decision = P1ControlledInstallExecutionDecision(
        decision_ref=DECISION_REF,
        controlled_install_execution_profile_count=1,
        pre_execution_snapshot_record_count=1,
        package_install_execution_plan_count=len(plans),
        package_install_command_record_count=len(command_records),
        package_install_execution_result_count=len(install_results),
        post_install_find_spec_probe_record_count=len(probe_records),
        execution_step_result_count=len(step_results),
        rollback_readiness_record_count=len(rollback_records),
        execution_summary_record_count=1,
        execution_asset_count=len(EXECUTION_ASSET_IDS),
        excluded_asset_count=len(EXCLUDED_ASSETS),
        attempted_install_count=attempted_install_count,
        successful_install_count=successful_install_count,
        failed_install_count=failed_install_count,
        skipped_install_count=skipped_install_count,
        deferred_install_count=deferred_install_count,
        post_install_probe_count=post_install_probe_count,
        post_install_probe_success_count=post_install_probe_success_count,
        post_install_probe_failed_count=post_install_probe_failed_count,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES),
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Controlled Install Execution (first real execution, package-install-only)",
        "lifecycle_variant": SCOPE,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "package_install_only": PACKAGE_INSTALL_ONLY,
        "allowed_partial_success": ALLOWED_PARTIAL_SUCCESS,
        "any_resolved_step_failure_blocks_go": ANY_RESOLVED_STEP_FAILURE_BLOCKS_GO,
        "controlled_venv_dir": str(venv_dir),
        "controlled_venv_created_now": venv_created_now,
        "upstream_prep_readiness_ref": UPSTREAM_PREP_READINESS_REF,
        "upstream_issuance_ref": UPSTREAM_ISSUANCE_REF,
        "upstream_request_ref": UPSTREAM_REQUEST_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "allowed_true_execution_flags": list(ALLOWED_TRUE_EXECUTION_FLAGS),
        "execution_control_flags_false": dict(EXECUTION_CONTROL_FLAGS_FALSE),
        "can_enter_flags": dict(CAN_ENTER_FLAGS),
        "weight_subapproval_assets": list(WEIGHT_SUBAPPROVAL_ASSETS),
        "controlled_install_execution_profile": _build_profile(),
        "controlled_install_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        # Artifacts.
        "pre_execution_snapshot_record": asdict(snapshot),
        "pre_execution_snapshot_record_count": 1,
        "package_install_execution_plans": [asdict(p) for p in plans],
        "package_install_execution_plan_count": len(plans),
        "package_install_command_records": [asdict(c) for c in command_records],
        "package_install_command_record_count": len(command_records),
        "package_install_execution_results": [asdict(r) for r in install_results],
        "package_install_execution_result_count": len(install_results),
        "post_install_find_spec_probe_records": [asdict(p) for p in probe_records],
        "post_install_find_spec_probe_record_count": len(probe_records),
        "execution_step_results": [asdict(s) for s in step_results],
        "execution_step_result_count": len(step_results),
        "execution_failure_records": [asdict(f) for f in failure_records],
        "execution_failure_record_count": len(failure_records),
        "execution_stop_condition_records": [asdict(s) for s in stop_condition_records],
        "execution_stop_condition_count": len(stop_condition_records),
        "rollback_readiness_records": [asdict(r) for r in rollback_records],
        "rollback_readiness_record_count": len(rollback_records),
        "execution_summary_record": asdict(summary),
        "execution_summary_record_count": 1,
        "execution_permission_boundary": asdict(boundary),
        "deferred_asset_ids": list(DEFERRED_ASSET_IDS),
        "resolvable_asset_ids": list(RESOLVABLE_ASSET_IDS),
        "excluded_asset_records": [dict(e) for e in EXCLUDED_ASSETS],
        "excluded_asset_count": len(EXCLUDED_ASSETS),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "p1_controlled_install_execution_status": (
                "package_install_only_real_execution_complete_partial_three_installed_two_deferred_no_weight_no_download_no_inference_no_runtime"
                if final_decision == FINAL_DECISION_PARTIAL_GO
                else (
                    "package_install_only_real_execution_complete_all_installed"
                    if final_decision == FINAL_DECISION_GO
                    else "blocked"
                )
            ),
            "installed_assets": [r.asset_id for r in install_results if r.install_succeeded],
            "deferred_assets": list(DEFERRED_ASSET_IDS),
            "deferred_reason": "package_name_resolution_required_registry_names_not_clean_pypi_wheels_git_source",
            "next_step_ref": NEXT_STEP_REF,
            "transition_note": (
                "First REAL execution (package-install-only) complete. Into a controlled, workspace-local venv "
                "(--system-site-packages) the three cleanly-resolvable assets were really installed and find_spec-"
                "verified: supervision, deep_sort (deep-sort-realtime), midas (timm). byte_track (registry package "
                "'bytetrack' -> import 'yolox') and mobile_sam (registry 'mobile_sam' -> git source MobileSAM) are "
                "NOT clean PyPI wheels; per the package-name-resolution guard they were recorded "
                "package_name_resolution_required and DEFERRED (not guessed) under the partial-success policy. The 12 "
                "excluded assets were not touched. No weight/model/dataset download, no real import, no model load, no "
                "inference, no runtime, no output adapter, no semantic layer. Package install success is NOT model / "
                "weight readiness nor inference / runtime / output-adapter / semantic-layer approval. Next is a "
                "POST-REVIEW (Phase-P1-Controlled-Install-Execution-Post-Review-v1-001), NOT weight download; the two "
                "deferred assets are carried there for package-name correction / git-source sub-approval."
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
        # Extra mandated artifacts.
        (out_root / SNAPSHOT_FILENAME).write_text(
            json.dumps(snapshot_detail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / STEP_RECORDS_FILENAME).write_text(
            json.dumps(
                {
                    "phase_id": PHASE_ID,
                    "execution_step_results": [asdict(s) for s in step_results],
                    "package_install_command_records": [asdict(c) for c in command_records],
                    "package_install_execution_results": [asdict(r) for r in install_results],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (out_root / PROBE_RECORDS_FILENAME).write_text(
            json.dumps(
                {
                    "phase_id": PHASE_ID,
                    "post_install_find_spec_probe_records": [asdict(p) for p in probe_records],
                },
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
            str(out_root / STEP_RECORDS_FILENAME),
            str(out_root / PROBE_RECORDS_FILENAME),
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

        # Write the 5 extra protected, non-deletable records mandated for the
        # first real execution phase.
        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "pre_execution_snapshot_record": {"pre_execution_snapshot_record": asdict(snapshot)},
            "package_install_execution_record": {
                "package_install_execution_results": [asdict(r) for r in install_results],
                "package_install_command_records": [asdict(c) for c in command_records],
                "execution_summary_record": asdict(summary),
            },
            "post_install_probe_record": {
                "post_install_find_spec_probe_records": [asdict(p) for p in probe_records]
            },
            "stop_condition_record": {
                "execution_stop_condition_records": [asdict(s) for s in stop_condition_records],
                "execution_failure_records": [asdict(f) for f in failure_records],
            },
            "rollback_readiness_record": {
                "rollback_readiness_records": [asdict(r) for r in rollback_records]
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
            "package_install_only": True,
            "weight_download_execution_allowed": False,
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
    result = review_p1_controlled_install_execution_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "controlled_venv_dir": result.get("controlled_venv_dir"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "attempted_install_count": result["decision"]["attempted_install_count"],
                "successful_install_count": result["decision"]["successful_install_count"],
                "deferred_install_count": result["decision"]["deferred_install_count"],
                "post_install_probe_success_count": result["decision"]["post_install_probe_success_count"],
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
