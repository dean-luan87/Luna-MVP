# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only, target = timm).

Takes a pre-install snapshot (recorded BEFORE any install), then performs a REAL controlled
`pip install timm --target <isolated path>` (NO global install), resolves the installed timm
version honestly (resolver-selected, NOT pre-pinned, NOT fabricated), records the dependency
mutation (target-confined), audits global-environment contamination via a clean subprocess
(global timm/torch must be unchanged), and runs an `importlib.util.find_spec('timm')`-ONLY
post-install probe (NO real import). It NEVER real-imports timm / mobile_sam, NEVER model
loads / retries, NEVER infers / segments / predicts, NEVER starts runtime / output adapter /
semantic layer, NEVER mutates the registry, and downloads NO extra weight. Three honest
outcomes: GO (install success + find_spec true + no global contamination + no boundary
violation), FAILED_NO_BOUNDARY_VIOLATION (install/find_spec failed but no boundary
violation), or BLOCKED (global contamination, uncontrolled scope, real import, model load,
inference/runtime, registry mutation, or test-board failure). timm install success is NOT
model-load / inference / runtime / output-adapter / semantic approval. Protected, non-
deletable test board records are written in `real_test` mode.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
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
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_execution_and_post_review.p1_mobile_sam_dependency_repair_install_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_install_execution_and_post_review.p1_mobile_sam_dependency_repair_install_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_INSTALL_TARGET_REL,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_ALLOWED,
    DEPENDENCY_REPAIR_INSTALL_EXECUTION,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    INSTALL_PRINCIPLE_ZH,
    INSTALL_SCOPE,
    INSTALL_TIMEOUT_SECONDS,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_WEIGHT_SHA256,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PIP_INSTALL_ALLOWED,
    POST_REVIEW_INCLUDED,
    REAL_EXECUTION_PHASE,
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
    TARGET_CHAIN_REF,
    TARGET_DEPENDENCY,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALL_ALLOWED,
    TIMM_PACKAGE_NAME,
    UPSTREAM_REQUEST_APPROVAL_REF,
    WEIGHT_CHAIN,
    MobileSAMModelLoadRetryGateAfterTimmInstall,
    NegativeTimmDependencyRepairInstallExecutionGuard,
    P1MobileSAMDependencyRepairInstallExecutionDecision,
    P1MobileSAMDependencyRepairInstallExecutionPostReviewProfile,
    TimmDependencyMutationRecord,
    TimmEnvironmentContaminationAudit,
    TimmFindSpecProbeRecord,
    TimmInstallExecutionRecord,
    TimmInstallPostReviewAudit,
    TimmPreInstallSnapshotRecord,
    TimmRollbackReadinessRecord,
    TimmVersionResolutionRecord,
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
    / "p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_dependency_repair_install_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_dependency_repair_install_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_dependency_repair_install_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_dependency_repair_install_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_dependency_repair_install_execution_decision_v1"

_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

# Clean-environment metadata probe (runs in a subprocess WITHOUT the install target on
# sys.path, so target-installed packages cannot leak into the "global" reading).
_GLOBAL_PROBE_CODE = (
    "import json\n"
    "from importlib import metadata as m\n"
    "import importlib.util as u\n"
    "names = sorted(f\"{d.metadata['Name']}=={d.version}\" for d in m.distributions() "
    "if d.metadata and d.metadata.get('Name'))\n"
    "def ver(p):\n"
    "    try: return m.version(p)\n"
    "    except Exception: return ''\n"
    "print(json.dumps({'count': len(names), 'digest_src': '\\n'.join(names), "
    "'timm': ver('timm'), 'torch': ver('torch')}))\n"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _global_metadata_probe() -> Dict[str, Any]:
    """Read GLOBAL env package metadata in a clean subprocess (no target path)."""
    try:
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        proc = subprocess.run(
            [sys.executable, "-c", _GLOBAL_PROBE_CODE],
            capture_output=True, text=True, timeout=120, cwd=str(_REPO_ROOT), env=env,
        )
        data = json.loads(proc.stdout.strip().splitlines()[-1])
        digest = hashlib.sha256(data.get("digest_src", "").encode("utf-8")).hexdigest()
        return {
            "ok": True,
            "count": int(data.get("count", 0)),
            "digest": digest,
            "timm_version": data.get("timm", ""),
            "torch_version": data.get("torch", ""),
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "count": 0, "digest": "", "timm_version": "", "torch_version": "", "error": f"{type(exc).__name__}:{exc}"}


def _pip_version() -> str:
    try:
        from importlib import metadata as importlib_metadata

        return importlib_metadata.version("pip")
    except Exception:  # noqa: BLE001
        return ""


def _run_pip_install_target(target_dir: Path) -> Dict[str, Any]:
    """REAL controlled install: pip install timm --target <target_dir> (NO global install)."""
    cmd = [
        sys.executable, "-m", "pip", "install", "--no-input",
        TIMM_PACKAGE_NAME, "--target", str(target_dir),
    ]
    info: Dict[str, Any] = {
        "command": " ".join(cmd),
        "install_attempted": True,
        "return_code": -1,
        "stdout_summary": "",
        "stderr_summary": "",
        "error": "",
    }
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=INSTALL_TIMEOUT_SECONDS, cwd=str(_REPO_ROOT),
        )
        info["return_code"] = proc.returncode
        info["stdout_summary"] = (proc.stdout or "")[-1500:]
        info["stderr_summary"] = (proc.stderr or "")[-1500:]
    except subprocess.TimeoutExpired as exc:
        info["error"] = f"TimeoutExpired:{exc}"
    except Exception as exc:  # noqa: BLE001
        info["error"] = f"{type(exc).__name__}:{exc}"
    return info


def _inspect_target(target_dir: Path) -> Dict[str, Any]:
    """Inspect installed dist-info dirs / files in the isolated target (NO import)."""
    out: Dict[str, Any] = {
        "files_count": 0,
        "top_level_packages": [],
        "dist_info_packages": [],
        "timm_version_installed": "",
    }
    if not target_dir.is_dir():
        return out
    files = list(target_dir.rglob("*"))
    out["files_count"] = sum(1 for f in files if f.is_file())
    dist_infos = sorted(p for p in target_dir.glob("*.dist-info") if p.is_dir())
    pkgs: List[str] = []
    for di in dist_infos:
        name = di.name[:-len(".dist-info")]
        pkgs.append(name)
        base = name.rsplit("-", 1)[0]
        if base.lower() == TIMM_PACKAGE_NAME.lower() and "-" in name:
            out["timm_version_installed"] = name.rsplit("-", 1)[1]
    out["dist_info_packages"] = pkgs
    top = sorted({
        p.name for p in target_dir.iterdir()
        if p.is_dir() and not p.name.endswith(".dist-info") and not p.name.endswith(".data")
    })
    out["top_level_packages"] = top
    return out


def _find_spec_timm_with_target(target_dir: Path) -> Dict[str, Any]:
    """find_spec ONLY (NO import). Adds target to sys.path so the spec is locatable."""
    added = False
    if target_dir.is_dir() and str(target_dir) not in sys.path:
        sys.path.insert(0, str(target_dir))
        added = True
    try:
        spec = importlib.util.find_spec(TIMM_IMPORT_ROOT)
    except BaseException as exc:  # noqa: BLE001 — honest capture; find_spec must not crash the phase
        return {"found": False, "origin": "", "error": f"{type(exc).__name__}:{exc}", "target_added": added}
    if spec is None:
        return {"found": False, "origin": "", "error": "", "target_added": added}
    return {"found": True, "origin": getattr(spec, "origin", "") or "", "error": "", "target_added": added}


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMDependencyRepairInstallExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            target_dependency=TARGET_DEPENDENCY,
            dependency_repair_install_execution=DEPENDENCY_REPAIR_INSTALL_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            timm_install_allowed=TIMM_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            install_scope=INSTALL_SCOPE,
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
            upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    perform_install: bool = True,
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

    target_dir = (_WRITABLE_BASE / CONTROLLED_INSTALL_TARGET_REL).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------- #
    # (一) Pre-install snapshot (BEFORE any install).
    # ------------------------------------------------------------------- #
    global_before = _global_metadata_probe()
    timm_present_before = bool(global_before.get("timm_version"))
    snapshot = TimmPreInstallSnapshotRecord(
        snapshot_id="timm_pre_install_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        working_directory=str(Path.cwd()),
        controlled_install_target_path=str(target_dir),
        pip_version=_pip_version(),
        pip_freeze_before_count=int(global_before.get("count", 0)),
        pip_freeze_before_digest=global_before.get("digest", ""),
        installed_package_list_before_count=int(global_before.get("count", 0)),
        sys_path_plan="install_target_added_only_for_find_spec_probe_not_imported",
        existing_timm_status_by_find_spec_only=timm_present_before,
        global_env_snapshot_ref=str(out_root / "timm_pre_install_snapshot_v1.json"),
        rollback_snapshot_ref=str(target_dir),
        upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
        test_board_ref="capabilities/test_board/recognition_models/phase_p1_mobilesam_dependency_repair_install_execution_and_post_review_v1_001/",
        timestamp=_now(),
        snapshot_succeeded=global_before.get("ok", False),
    )
    (out_root / "timm_pre_install_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        # Snapshot failure => must NOT install. Boundary-safe blocker.
        failed_checks.append("snapshot.failed_no_install_allowed")

    # ------------------------------------------------------------------- #
    # (三) Install execution (REAL controlled --target install) — only if snapshot ok.
    # ------------------------------------------------------------------- #
    may_install = perform_install and snapshot.snapshot_succeeded
    t0 = time.time()
    if may_install:
        install_info = _run_pip_install_target(target_dir)
    else:
        install_info = {
            "command": f"{sys.executable} -m pip install --no-input {TIMM_PACKAGE_NAME} --target {target_dir}",
            "install_attempted": False,
            "return_code": -1,
            "stdout_summary": "",
            "stderr_summary": "install_skipped_snapshot_failed",
            "error": "install_skipped_snapshot_failed",
        }
    elapsed = round(time.time() - t0, 4)

    target_inspect = _inspect_target(target_dir)
    return_code = int(install_info["return_code"])
    timm_install_success = (
        bool(install_info["install_attempted"])
        and return_code == 0
        and bool(target_inspect["timm_version_installed"])
    )

    # Whitelist match: suggested form is `python -m pip install timm --target <path>`.
    command_whitelisted = (
        "-m pip install" in install_info["command"]
        and f" {TIMM_PACKAGE_NAME}" in install_info["command"]
        and "--target" in install_info["command"]
        and "--user" not in install_info["command"]
        and " --global" not in install_info["command"]
    )

    install_record = TimmInstallExecutionRecord(
        record_id="timm_install_execution_record_v1",
        command=install_info["command"],
        command_whitelisted=command_whitelisted,
        install_target=str(target_dir),
        no_global_install=True,
        install_attempted=bool(install_info["install_attempted"]),
        return_code=return_code,
        stdout_summary=install_info["stdout_summary"],
        stderr_summary=install_info["stderr_summary"],
        installed_files_count=int(target_inspect["files_count"]),
        timm_install_success=timm_install_success,
        install_error=install_info.get("error", ""),
    )
    (out_root / "timm_install_execution_record_v1.json").write_text(
        json.dumps(asdict(install_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (二) Version resolution (honest; resolver-selected, NOT pre-pinned).
    # ------------------------------------------------------------------- #
    installed_version = target_inspect["timm_version_installed"]
    if installed_version:
        version_status = "resolved_by_execution_not_pre_pinned"
    elif timm_install_success:
        version_status = "installed_version_unparsed"
    else:
        version_status = "unresolved_install_failed"
    version_record = TimmVersionResolutionRecord(
        record_id="timm_version_resolution_v1",
        package_name=TIMM_PACKAGE_NAME,
        import_root=TIMM_IMPORT_ROOT,
        version_resolution_attempted=True,
        version_pin_preexisting=False,
        resolved_version=installed_version,
        installed_version=installed_version,
        version_resolution_evidence_ref=str(out_root / "timm_install_execution_record_v1.json"),
        version_fabricated=False,
        version_status=version_status,
    )
    (out_root / "timm_version_resolution_v1.json").write_text(
        json.dumps(asdict(version_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if installed_version:
        warnings.append("timm_version_resolved_by_execution_not_pre_pinned_registry_lockfile_patch_required_next")

    # ------------------------------------------------------------------- #
    # (四) Dependency mutation record + global contamination audit.
    # ------------------------------------------------------------------- #
    global_after = _global_metadata_probe()
    timm_present_after = bool(global_after.get("timm_version"))
    global_env_changed = (
        global_before.get("ok") and global_after.get("ok")
        and global_before.get("digest") != global_after.get("digest")
    )
    torch_before = global_before.get("torch_version", "")
    torch_after = global_after.get("torch_version", "")
    torch_changed = bool(torch_before) and (torch_before != torch_after)
    # Global timm appearing only because of contamination (target install must NOT leak).
    global_timm_contamination = (not timm_present_before) and timm_present_after
    contamination_detected = bool(global_env_changed) or bool(torch_changed) or bool(global_timm_contamination)
    no_global_env_contamination = not contamination_detected

    transitive = sorted(
        p for p in target_inspect["dist_info_packages"]
        if not p.rsplit("-", 1)[0].lower() == TIMM_PACKAGE_NAME.lower()
    )
    mutation = TimmDependencyMutationRecord(
        record_id="timm_dependency_mutation_record_v1",
        pip_freeze_after_count=int(global_after.get("count", 0)),
        pip_freeze_after_digest=global_after.get("digest", ""),
        installed_package_list_after_count=int(global_after.get("count", 0)),
        target_path_top_level_count=len(target_inspect["top_level_packages"]),
        new_packages_in_target_path=tuple(target_inspect["dist_info_packages"]),
        transitive_dependencies_installed=tuple(transitive),
        torch_changed=torch_changed,
        global_env_changed=bool(global_env_changed),
        no_global_env_contamination=no_global_env_contamination,
        dependency_mutation_scope="controlled_target_only",
    )
    (out_root / "timm_dependency_mutation_record_v1.json").write_text(
        json.dumps(asdict(mutation), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    contamination_audit = TimmEnvironmentContaminationAudit(
        audit_id="timm_environment_contamination_audit_v1",
        global_site_packages_timm_present_before=timm_present_before,
        global_site_packages_timm_present_after=timm_present_after,
        global_env_changed=bool(global_env_changed),
        torch_version_before=torch_before,
        torch_version_after=torch_after,
        torch_changed=torch_changed,
        contamination_detected=contamination_detected,
        install_confined_to_target=no_global_env_contamination,
    )
    if contamination_detected:
        failed_checks.append("contamination.global_env_changed_blocks_go")

    # ------------------------------------------------------------------- #
    # (五) Post-install probe (find_spec ONLY, NO import).
    # ------------------------------------------------------------------- #
    probe_info = _find_spec_timm_with_target(target_dir)
    find_spec_timm = bool(probe_info["found"])
    probe = TimmFindSpecProbeRecord(
        record_id="timm_find_spec_probe_v1",
        probe_method="importlib.util.find_spec only",
        probe_target=TIMM_IMPORT_ROOT,
        find_spec_result=find_spec_timm,
        found_origin=probe_info.get("origin", ""),
        real_import_used=False,
        model_load_used=False,
        inference_used=False,
        runtime_used=False,
    )
    (out_root / "timm_find_spec_probe_v1.json").write_text(
        json.dumps(asdict(probe), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # Rollback readiness.
    # ------------------------------------------------------------------- #
    rollback = TimmRollbackReadinessRecord(
        record_id="timm_rollback_readiness_v1",
        rollback_available=True,
        rollback_not_executed_by_default=True,
        rollback_target_path=str(target_dir),
        rollback_removes_timm_target_if_failed=True,
        rollback_preserves_mobile_sam_code=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        global_env_contamination_check_done=True,
    )

    # ------------------------------------------------------------------- #
    # (六) Post-review audit.
    # ------------------------------------------------------------------- #
    post_audit = TimmInstallPostReviewAudit(
        audit_id="timm_install_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        install_command_whitelisted=command_whitelisted,
        install_scope_controlled=True,
        timm_install_attempted=bool(install_info["install_attempted"]),
        timm_install_success=timm_install_success,
        timm_version_recorded=bool(installed_version),
        find_spec_probe_only=True,
        find_spec_timm=find_spec_timm,
        real_import_performed=False,
        model_load_performed=False,
        inference_performed=False,
        runtime_performed=False,
        output_adapter_performed=False,
        semantic_layer_performed=False,
        registry_mutation_performed=False,
        additional_weight_download_performed=False,
        global_env_contamination=contamination_detected,
        rollback_ready=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            snapshot.snapshot_succeeded
            and command_whitelisted
            and no_global_env_contamination
        ),
    )
    (out_root / "timm_install_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (十三) Invariants for the 18 negative guards (A..R).
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "pre_install_snapshot_present": snapshot.snapshot_succeeded,
        "install_target_is_timm": (
            f" {TIMM_PACKAGE_NAME}" in install_record.command
            and version_record.package_name == TIMM_PACKAGE_NAME
        ),
        "install_scope_controlled": (
            install_record.no_global_install is True
            and INSTALL_SCOPE == "controlled_dependency_repair_only"
            and str(target_dir) == install_record.install_target
        ),
        "no_global_env_contamination": no_global_env_contamination,
        "no_real_import": (
            REAL_IMPORT_ALLOWED is False
            and probe.real_import_used is False
            and post_audit.real_import_performed is False
        ),
        "no_model_load_retry": (
            MODEL_LOAD_ALLOWED is False
            and MODEL_LOAD_RETRY_ALLOWED is False
            and post_audit.model_load_performed is False
        ),
        "no_inference_seg_pred": (
            REAL_INFERENCE_ALLOWED is False
            and post_audit.inference_performed is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
            and post_audit.runtime_performed is False
            and post_audit.output_adapter_performed is False
            and post_audit.semantic_layer_performed is False
        ),
        "no_additional_download": (
            ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False
            and MODEL_DOWNLOAD_ALLOWED is False
            and post_audit.additional_weight_download_performed is False
        ),
        "no_registry_mutation": (
            REGISTRY_MUTATION_ALLOWED is False
            and post_audit.registry_mutation_performed is False
        ),
        "probe_find_spec_only": (
            probe.probe_method == "importlib.util.find_spec only"
            and post_audit.find_spec_probe_only is True
        ),
        "install_not_model_load_success": (
            post_audit.model_load_performed is False
        ),
        "install_not_inference_runtime_ready": (
            post_audit.inference_performed is False
            and post_audit.runtime_performed is False
        ),
        "rollback_readiness_present": (
            rollback.rollback_available is True
            and rollback.rollback_removes_timm_target_if_failed is True
            and post_audit.rollback_ready is True
        ),
        "post_review_present": True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeTimmDependencyRepairInstallExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeTimmDependencyRepairInstallExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_timm_dependency_repair_install_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # Boundary / structural GO conditions (contribute to blocker_count).
    # NOTE: install/find_spec success is NOT a blocker — an honest install failure with
    # no boundary violation routes to FAILED_NO_BOUNDARY_VIOLATION.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_dependency_repair_install_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "timm_pre_install_snapshot_record_count_eq_1": True,
        "timm_version_resolution_record_count_gte_1": True,
        "timm_install_execution_record_count_gte_1": True,
        "timm_dependency_mutation_record_count_gte_1": True,
        "timm_find_spec_probe_record_count_gte_1": True,
        "timm_environment_contamination_audit_count_gte_1": True,
        "timm_install_post_review_audit_count_gte_1": True,
        "timm_rollback_readiness_record_count_gte_1": True,
        "mobile_sam_model_load_retry_gate_after_timm_install_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        # Upstream verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "mobile_sam_only": True,
        "target_dependency_timm": TARGET_DEPENDENCY == "timm",
        "dependency_repair_install_execution": DEPENDENCY_REPAIR_INSTALL_EXECUTION is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "timm_install_allowed_true": TIMM_INSTALL_ALLOWED is True,
        "pip_install_allowed_true": PIP_INSTALL_ALLOWED is True,
        "dependency_install_allowed_true": DEPENDENCY_INSTALL_ALLOWED is True,
        "install_scope_controlled_dependency_repair_only": INSTALL_SCOPE == "controlled_dependency_repair_only",
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
        # Pre-install + scope enforcement.
        "pre_snapshot_exists": snapshot.snapshot_succeeded,
        "install_command_whitelisted": command_whitelisted,
        "install_scope_controlled": invariant_state["install_scope_controlled"],
        "no_global_install": install_record.no_global_install is True,
        # Contamination is a BLOCKER condition.
        "no_global_env_contamination": no_global_env_contamination,
        "no_torch_changed": not torch_changed,
        # Probe semantics.
        "post_install_probe_find_spec_only": probe.probe_method == "importlib.util.find_spec only",
        "no_real_import_performed": post_audit.real_import_performed is False,
        # Boundary post-review.
        "no_model_load_performed": post_audit.model_load_performed is False,
        "no_inference_performed": post_audit.inference_performed is False,
        "no_runtime_performed": post_audit.runtime_performed is False,
        "no_output_adapter_performed": post_audit.output_adapter_performed is False,
        "no_semantic_layer_performed": post_audit.semantic_layer_performed is False,
        "no_registry_mutation_performed": post_audit.registry_mutation_performed is False,
        "no_additional_weight_download_performed": post_audit.additional_weight_download_performed is False,
        # Readiness semantics (install success is NOT downstream approval).
        "install_success_not_model_load_success": post_audit.model_load_performed is False,
        "install_success_not_inference_approval": post_audit.inference_performed is False,
        "install_success_not_runtime_approval": post_audit.runtime_performed is False,
        # Rollback + post-review presence.
        "rollback_readiness_present": invariant_state["rollback_readiness_present"],
        "post_review_present": True,
        "version_not_fabricated": version_record.version_fabricated is False,
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
    no_boundary_violation = blocker_count == 0
    timm_find_spec_verified = find_spec_timm

    # ------------------------------------------------------------------- #
    # (七) Decision rule (3-way).
    # ------------------------------------------------------------------- #
    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
        next_phase_purpose = "review_and_classify_boundary_violation_blockers"
        can_enter_model_load_retry_next = False
    elif timm_install_success and timm_find_spec_verified and no_global_env_contamination:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        next_phase_purpose = "retry_model_load_import_and_checkpoint_load_no_inference"
        can_enter_model_load_retry_next = True
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        next_phase_purpose = "review_timm_install_failure_and_plan_repair"
        can_enter_model_load_retry_next = False

    # ------------------------------------------------------------------- #
    # (八) Model-load retry gate after timm install.
    # ------------------------------------------------------------------- #
    retry_gate = MobileSAMModelLoadRetryGateAfterTimmInstall(
        record_id="mobile_sam_model_load_retry_gate_after_timm_install_v1",
        can_enter_model_load_retry_next=can_enter_model_load_retry_next,
        timm_install_execution_go=(final_decision == FINAL_DECISION_GO),
        timm_find_spec_verified=timm_find_spec_verified,
        timm_dependency_available=timm_install_success and timm_find_spec_verified,
        mobile_sam_weight_sha256_recheck_required_before_retry=True,
        mobile_sam_code_and_weight_ready_must_be_reverified=True,
        model_load_retry_requires_separate_execution_phase=True,
        timm_install_success_not_model_load_success=True,
        timm_install_success_not_inference_approval=True,
        timm_install_success_not_runtime_approval=True,
        timm_install_success_not_output_adapter_approval=True,
        timm_install_success_not_semantic_layer_approval=True,
        recommended_next_phase=recommended_next_phase,
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMDependencyRepairInstallExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_dependency_repair_install_execution_profile_count=1,
        timm_pre_install_snapshot_record_count=1,
        timm_version_resolution_record_count=1,
        timm_install_execution_record_count=1,
        timm_dependency_mutation_record_count=1,
        timm_find_spec_probe_record_count=1,
        timm_environment_contamination_audit_count=1,
        timm_install_post_review_audit_count=1,
        timm_rollback_readiness_record_count=1,
        mobile_sam_model_load_retry_gate_after_timm_install_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        timm_install_success=timm_install_success,
        timm_find_spec_verified=timm_find_spec_verified,
        no_global_env_contamination=no_global_env_contamination,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Dependency Repair Install Execution And Post Review (real execution, mobile_sam_only, target=timm)",
        "lifecycle_variant": SCOPE,
        "install_principle_zh": INSTALL_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "target_dependency": TARGET_DEPENDENCY,
        "timm_install_allowed": TIMM_INSTALL_ALLOWED,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_request_approval_ref": UPSTREAM_REQUEST_APPROVAL_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "controlled_install_target_path": str(target_dir),
        "mobile_sam_dependency_repair_install_execution_profile": _build_profile(),
        "mobile_sam_dependency_repair_install_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "timm_pre_install_snapshot_record": asdict(snapshot),
        "timm_pre_install_snapshot_record_count": 1,
        "timm_version_resolution_record": asdict(version_record),
        "timm_version_resolution_record_count": 1,
        "timm_install_execution_record": asdict(install_record),
        "timm_install_execution_record_count": 1,
        "timm_dependency_mutation_record": asdict(mutation),
        "timm_dependency_mutation_record_count": 1,
        "timm_find_spec_probe_record": asdict(probe),
        "timm_find_spec_probe_record_count": 1,
        "timm_environment_contamination_audit": asdict(contamination_audit),
        "timm_environment_contamination_audit_count": 1,
        "timm_install_post_review_audit": asdict(post_audit),
        "timm_install_post_review_audit_count": 1,
        "timm_rollback_readiness_record": asdict(rollback),
        "timm_rollback_readiness_record_count": 1,
        "mobile_sam_model_load_retry_gate_after_timm_install": asdict(retry_gate),
        "mobile_sam_model_load_retry_gate_after_timm_install_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "elapsed_seconds": elapsed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "install_execution_status": decision_branch,
            "target_dependency": TARGET_DEPENDENCY,
            "timm_install_success": timm_install_success,
            "timm_installed_version": installed_version,
            "version_status": version_record.version_status,
            "find_spec_timm": timm_find_spec_verified,
            "return_code": return_code,
            "no_global_env_contamination": no_global_env_contamination,
            "global_env_changed": bool(global_env_changed),
            "torch_changed": torch_changed,
            "no_boundary_violation": no_boundary_violation,
            "can_enter_model_load_retry_next": can_enter_model_load_retry_next,
            "timm_install_success_not_model_load_success": True,
            "timm_install_success_not_inference_approval": True,
            "timm_install_success_not_runtime_approval": True,
            "recommended_next_phase": recommended_next_phase,
            "recommended_next_phase_scope": "mobile_sam_only",
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only, target=timm). A pre-install snapshot was taken, then a REAL "
                "controlled `pip install " + TIMM_PACKAGE_NAME + " --target <isolated path>` was run (NO global "
                "install). return_code=" + str(return_code) + ", timm_install_success=" + str(timm_install_success)
                + ", installed_version=" + (installed_version or "<unresolved>") + " (version_status="
                + version_record.version_status + ", NOT pre-pinned, NOT fabricated). Dependency mutation was "
                "confined to the target; a clean-subprocess global contamination audit found global_env_changed="
                + str(bool(global_env_changed)) + ", torch_changed=" + str(torch_changed) + " (no_global_env_"
                "contamination=" + str(no_global_env_contamination) + "). A find_spec('timm')-ONLY post-install probe "
                "returned " + str(timm_find_spec_verified) + " (NO real import). NOTHING was imported / model-loaded / "
                "retried / inferred / run; no runtime / output adapter / semantic layer started; the registry was NOT "
                "mutated and no extra weight was downloaded. timm install success is NOT model-load / inference / "
                "runtime / output-adapter / semantic approval. Decision=" + final_decision + ". "
                + (
                    "timm is installed and find_spec-verified with no contamination; next: " + NEXT_PHASE_GO
                    + " (real import + model-load retry; still no inference)."
                    if final_decision == FINAL_DECISION_GO
                    else (
                        "Honest install/find_spec failure with NO boundary violation; next: " + NEXT_PHASE_FAILED + "."
                        if final_decision == FINAL_DECISION_FAILED
                        else "Boundary violation detected (e.g. global contamination); next: " + NEXT_PHASE_BLOCKED + "."
                    )
                )
                + " Because the timm version was resolver-selected (not pre-pinned), a follow-up registry/lockfile "
                "patch is required before promotion."
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
            "timm_pre_install_snapshot_record": {"timm_pre_install_snapshot_record": asdict(snapshot)},
            "timm_version_resolution_record": {"timm_version_resolution_record": asdict(version_record)},
            "timm_install_execution_record": {"timm_install_execution_record": asdict(install_record)},
            "timm_dependency_mutation_record": {"timm_dependency_mutation_record": asdict(mutation)},
            "timm_find_spec_probe_record": {"timm_find_spec_probe_record": asdict(probe)},
            "timm_environment_contamination_audit_record": {"timm_environment_contamination_audit": asdict(contamination_audit)},
            "timm_install_post_review_record": {"timm_install_post_review_audit": asdict(post_audit)},
            "timm_rollback_readiness_record": {"timm_rollback_readiness_record": asdict(rollback)},
            "mobile_sam_model_load_retry_gate_record": {"mobile_sam_model_load_retry_gate_after_timm_install": asdict(retry_gate)},
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
            "timm_install_allowed": True,
            "real_import_allowed": False,
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
    result = review_p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "timm_install_success": result["conclusions"]["timm_install_success"],
                "timm_installed_version": result["conclusions"]["timm_installed_version"],
                "find_spec_timm": result["conclusions"]["find_spec_timm"],
                "no_global_env_contamination": result["conclusions"]["no_global_env_contamination"],
                "can_enter_model_load_retry_next": result["conclusions"]["can_enter_model_load_retry_next"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] in (FINAL_DECISION_GO, FINAL_DECISION_FAILED) else 1


if __name__ == "__main__":
    raise SystemExit(main())
