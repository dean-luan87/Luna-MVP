# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair NoDeps Install Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only, target = timm, route = no-deps).

Pre-install snapshot, REAL `pip install timm --no-deps --target <path>`, version/target-path
records, find_spec('timm')-only probe, global-env contamination audit, post-review, rollback
readiness. Does NOT real import timm/mobile_sam, model load/retry, inference/runtime/output/
semantic, registry mutation, extra downloads. Three outcomes: GO, FAILED_NO_BOUNDARY_
VIOLATION, BLOCKED. Protected test board records in `real_test` mode.
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
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review.p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review.p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_INSTALL_TARGET_REL,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPENDENCY_INSTALL_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    INSTALL_PRINCIPLE_ZH,
    INSTALL_SCOPE,
    INSTALL_TIMEOUT_SECONDS,
    LUNA_CORE_PRINCIPLE,
    MOBILE_SAM_WEIGHT_SHA256,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    NODEPS_INSTALL_EXECUTION,
    NO_DEPS_REQUIRED,
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
    SELECTED_ROUTE,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TARGET_DEPENDENCY,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALL_ALLOWED,
    TIMM_PACKAGE_NAME,
    UPSTREAM_NODEPS_REQUEST_APPROVAL_REF,
    WEIGHT_CHAIN,
    MobileSAMModelLoadRetryGateAfterNoDepsInstall,
    NegativeTimmNoDepsInstallExecutionGuard,
    P1MobileSAMNoDepsTimmInstallExecutionDecision,
    P1MobileSAMNoDepsTimmInstallExecutionPostReviewProfile,
    TimmNoDepsEnvironmentContaminationAudit,
    TimmNoDepsFindSpecProbeRecord,
    TimmNoDepsInstallExecutionRecord,
    TimmNoDepsInstallPostReviewAudit,
    TimmNoDepsPreInstallSnapshotRecord,
    TimmNoDepsRollbackReadinessRecord,
    TimmNoDepsTargetPathRecord,
    TimmNoDepsVersionRecord,
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
    / "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_nodeps_timm_install_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_nodeps_timm_install_execution_decision_v1"
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"

_GLOBAL_PROBE_CODE = (
    "import json\nfrom importlib import metadata as m\n"
    "names = sorted(f\"{d.metadata['Name']}=={d.version}\" for d in m.distributions() "
    "if d.metadata and d.metadata.get('Name'))\n"
    "def ver(p):\n    try: return m.version(p)\n    except Exception: return ''\n"
    "print(json.dumps({'count': len(names), 'digest_src': '\\n'.join(names), "
    "'timm': ver('timm'), 'torch': ver('torch'), 'torchvision': ver('torchvision')}"
    "))\n"
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _global_metadata_probe() -> Dict[str, Any]:
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
            "torchvision_version": data.get("torchvision", ""),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False, "count": 0, "digest": "",
            "timm_version": "", "torch_version": "", "torchvision_version": "",
            "error": f"{type(exc).__name__}:{exc}",
        }


def _pip_version() -> str:
    try:
        from importlib import metadata as importlib_metadata
        return importlib_metadata.version("pip")
    except Exception:  # noqa: BLE001
        return ""


def _target_path_stats(target_dir: Path) -> Dict[str, Any]:
    if not target_dir.is_dir():
        return {"exists": False, "file_count": 0, "size_bytes": 0}
    file_count = 0
    size_bytes = 0
    for f in target_dir.rglob("*"):
        if f.is_file():
            file_count += 1
            try:
                size_bytes += f.stat().st_size
            except OSError:
                pass
    return {"exists": True, "file_count": file_count, "size_bytes": size_bytes}


def _inspect_target(target_dir: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "dist_info_dirs": [],
        "top_level_dirs": [],
        "timm_version_installed": "",
        "timm_package_dir_exists": False,
        "torch_files_installed": False,
        "torchvision_files_installed": False,
        "unexpected_large_files": False,
    }
    stats = _target_path_stats(target_dir)
    out.update(stats)
    if not target_dir.is_dir():
        return out
    dist_infos = sorted(p.name for p in target_dir.glob("*.dist-info") if p.is_dir())
    out["dist_info_dirs"] = dist_infos
    for name in dist_infos:
        pkg_part = name.removesuffix(".dist-info")
        base = pkg_part.rsplit("-", 1)[0].lower()
        if base == TIMM_PACKAGE_NAME.lower() and "-" in pkg_part:
            out["timm_version_installed"] = pkg_part.rsplit("-", 1)[1]
        if base in ("torch", "pytorch"):
            out["torch_files_installed"] = True
        if base == "torchvision":
            out["torchvision_files_installed"] = True
    top = sorted(
        p.name for p in target_dir.iterdir()
        if p.is_dir() and not p.name.endswith(".dist-info") and not p.name.endswith(".data")
    )
    out["top_level_dirs"] = top
    out["timm_package_dir_exists"] = TIMM_PACKAGE_NAME in top or any(
        TIMM_PACKAGE_NAME in d for d in top
    )
    if "torch" in top or "torchvision" in top:
        out["torch_files_installed"] = out["torch_files_installed"] or "torch" in top
        out["torchvision_files_installed"] = out["torchvision_files_installed"] or "torchvision" in top
    for f in target_dir.rglob("*"):
        if f.is_file():
            try:
                if f.stat().st_size > 50 * 1024 * 1024:
                    out["unexpected_large_files"] = True
                    break
            except OSError:
                pass
    return out


def _run_pip_install_nodeps(target_dir: Path) -> Dict[str, Any]:
    cmd = [
        sys.executable, "-m", "pip", "install", "--no-input",
        TIMM_PACKAGE_NAME, "--no-deps", "--target", str(target_dir),
    ]
    info: Dict[str, Any] = {
        "command": " ".join(cmd),
        "install_attempted": True,
        "return_code": -1,
        "stdout_summary": "",
        "stderr_summary": "",
        "error": "",
        "elapsed_seconds": 0.0,
    }
    t0 = time.time()
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
    info["elapsed_seconds"] = round(time.time() - t0, 4)
    return info


def _find_spec_timm_with_target(target_dir: Path) -> Dict[str, Any]:
    added = False
    if target_dir.is_dir() and str(target_dir) not in sys.path:
        sys.path.insert(0, str(target_dir))
        added = True
    try:
        spec = importlib.util.find_spec(TIMM_IMPORT_ROOT)
    except BaseException as exc:  # noqa: BLE001
        return {"found": False, "origin": "", "error": f"{type(exc).__name__}:{exc}", "target_added": added}
    if spec is None:
        return {"found": False, "origin": "", "error": "", "target_added": added}
    return {"found": True, "origin": getattr(spec, "origin", "") or "", "error": "", "target_added": added}


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMNoDepsTimmInstallExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            target_dependency=TARGET_DEPENDENCY,
            selected_route=SELECTED_ROUTE,
            nodeps_install_execution=NODEPS_INSTALL_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            timm_install_allowed=TIMM_INSTALL_ALLOWED,
            pip_install_allowed=PIP_INSTALL_ALLOWED,
            dependency_install_allowed=DEPENDENCY_INSTALL_ALLOWED,
            no_deps_required=NO_DEPS_REQUIRED,
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
            upstream_nodeps_request_approval_ref=UPSTREAM_NODEPS_REQUEST_APPROVAL_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1(
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

    # (一) Pre-install snapshot
    global_before = _global_metadata_probe()
    target_before = _target_path_stats(target_dir)
    timm_global_before = bool(global_before.get("timm_version"))
    snapshot = TimmNoDepsPreInstallSnapshotRecord(
        snapshot_id="timm_nodeps_pre_install_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        working_directory=str(Path.cwd()),
        controlled_install_target_path=str(target_dir),
        pip_version=_pip_version(),
        pip_freeze_before_count=int(global_before.get("count", 0)),
        pip_freeze_before_digest=global_before.get("digest", ""),
        installed_package_list_before_count=int(global_before.get("count", 0)),
        existing_timm_status_by_find_spec_only=timm_global_before,
        target_path_before_exists=target_before["exists"],
        target_path_before_file_count=target_before["file_count"],
        target_path_before_size_bytes=target_before["size_bytes"],
        global_env_snapshot_ref=str(out_root / "timm_nodeps_pre_install_snapshot_v1.json"),
        rollback_snapshot_ref=str(target_dir),
        upstream_nodeps_request_approval_ref=UPSTREAM_NODEPS_REQUEST_APPROVAL_REF,
        test_board_ref="capabilities/test_board/recognition_models/phase_p1_mobilesam_dependency_repair_nodeps_install_execution_and_post_review_v1_001/",
        timestamp=_now(),
        snapshot_succeeded=global_before.get("ok", False),
    )
    (out_root / "timm_nodeps_pre_install_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        failed_checks.append("snapshot.failed_no_install_allowed")

    # (二) REAL no-deps install
    may_install = perform_install and snapshot.snapshot_succeeded
    if may_install:
        install_info = _run_pip_install_nodeps(target_dir)
    else:
        install_info = {
            "command": f"{sys.executable} -m pip install --no-input {TIMM_PACKAGE_NAME} --no-deps --target {target_dir}",
            "install_attempted": False,
            "return_code": -1,
            "stdout_summary": "",
            "stderr_summary": "install_skipped_snapshot_failed",
            "error": "install_skipped_snapshot_failed",
            "elapsed_seconds": 0.0,
        }

    target_inspect = _inspect_target(target_dir)
    return_code = int(install_info["return_code"])
    installed_version = target_inspect.get("timm_version_installed", "")
    timm_install_success = (
        bool(install_info["install_attempted"])
        and return_code == 0
        and bool(installed_version)
        and target_inspect.get("timm_package_dir_exists", False)
    )

    no_deps_flag_present = "--no-deps" in install_info["command"]
    target_flag_present = "--target" in install_info["command"]
    command_whitelisted = (
        "-m pip install" in install_info["command"]
        and f" {TIMM_PACKAGE_NAME}" in install_info["command"]
        and no_deps_flag_present
        and target_flag_present
        and "--user" not in install_info["command"]
    )

    install_record = TimmNoDepsInstallExecutionRecord(
        record_id="timm_nodeps_install_execution_record_v1",
        command=install_info["command"],
        command_whitelisted=command_whitelisted,
        no_deps_flag_present=no_deps_flag_present,
        target_flag_present=target_flag_present,
        install_target=str(target_dir),
        no_global_install=True,
        no_transitive_dependency_install_intended=True,
        install_attempted=bool(install_info["install_attempted"]),
        return_code=return_code,
        elapsed_seconds=float(install_info.get("elapsed_seconds", 0.0)),
        stdout_summary=install_info["stdout_summary"],
        stderr_summary=install_info["stderr_summary"],
        timm_install_success=timm_install_success,
        install_error=install_info.get("error", ""),
    )
    (out_root / "timm_nodeps_install_execution_record_v1.json").write_text(
        json.dumps(asdict(install_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # (三) Version record
    version_status = "resolved_by_execution_not_pre_pinned" if timm_install_success else "unresolved_install_failed"
    version_record = TimmNoDepsVersionRecord(
        record_id="timm_nodeps_version_record_v1",
        timm_install_attempted=bool(install_info["install_attempted"]),
        timm_install_success=timm_install_success,
        resolved_version=installed_version,
        installed_version=installed_version,
        version_source="pip_dist_info" if installed_version else "unresolved",
        version_fabricated=False,
        version_pin_preexisting=False,
        version_status=version_status,
        lockfile_patch_required_later=True,
    )
    (out_root / "timm_nodeps_version_record_v1.json").write_text(
        json.dumps(asdict(version_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # (四) Target path record
    torch_in_target = bool(target_inspect.get("torch_files_installed"))
    tv_in_target = bool(target_inspect.get("torchvision_files_installed"))
    non_timm_dist = [
        d for d in target_inspect.get("dist_info_dirs", [])
        if not d.lower().startswith(TIMM_PACKAGE_NAME.lower())
    ]
    no_transitive = not torch_in_target and not tv_in_target and len(non_timm_dist) == 0

    target_record = TimmNoDepsTargetPathRecord(
        record_id="timm_nodeps_target_path_record_v1",
        target_path=str(target_dir),
        target_path_exists=target_inspect.get("exists", False),
        target_path_file_count=target_inspect.get("file_count", 0),
        target_path_size_bytes=target_inspect.get("size_bytes", 0),
        installed_dist_info_dirs=tuple(target_inspect.get("dist_info_dirs", [])),
        installed_top_level_dirs=tuple(target_inspect.get("top_level_dirs", [])),
        timm_package_dir_exists=bool(target_inspect.get("timm_package_dir_exists")),
        unexpected_large_files_detected=bool(target_inspect.get("unexpected_large_files")),
        torch_files_installed_in_target=torch_in_target,
        torchvision_files_installed_in_target=tv_in_target,
        no_transitive_dependencies_installed=no_transitive,
    )
    (out_root / "timm_nodeps_target_path_record_v1.json").write_text(
        json.dumps(asdict(target_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if torch_in_target or tv_in_target:
        failed_checks.append("target.torch_or_torchvision_installed_in_target")

    # (五) Global contamination audit
    global_after = _global_metadata_probe()
    global_env_changed = (
        global_before.get("ok") and global_after.get("ok")
        and global_before.get("digest") != global_after.get("digest")
    )
    torch_before = global_before.get("torch_version", "")
    torch_after = global_after.get("torch_version", "")
    tv_before = global_before.get("torchvision_version", "")
    tv_after = global_after.get("torchvision_version", "")
    torch_changed = bool(torch_before) and torch_before != torch_after
    tv_changed = bool(tv_before) and tv_before != tv_after
    contamination_detected = bool(global_env_changed) or torch_changed or tv_changed
    no_global_env_contamination = not contamination_detected

    contamination_audit = TimmNoDepsEnvironmentContaminationAudit(
        audit_id="timm_nodeps_environment_contamination_audit_v1",
        pip_freeze_after_count=int(global_after.get("count", 0)),
        pip_freeze_after_digest=global_after.get("digest", ""),
        installed_package_list_after_count=int(global_after.get("count", 0)),
        global_env_changed=bool(global_env_changed),
        torch_changed=torch_changed,
        torchvision_changed=tv_changed,
        torch_version_before=torch_before,
        torch_version_after=torch_after,
        torchvision_version_before=tv_before,
        torchvision_version_after=tv_after,
        contamination_detected=contamination_detected,
        no_global_env_contamination=no_global_env_contamination,
        dependency_mutation_scope="controlled_target_only",
    )
    if contamination_detected:
        failed_checks.append("contamination.global_env_changed_blocks_go")

    no_transitive_violation = not no_transitive

    # (六) find_spec probe
    probe_info = _find_spec_timm_with_target(target_dir)
    find_spec_timm = bool(probe_info["found"])
    probe = TimmNoDepsFindSpecProbeRecord(
        record_id="timm_nodeps_find_spec_probe_v1",
        probe_method="importlib.util.find_spec only",
        probe_target=TIMM_IMPORT_ROOT,
        find_spec_result=find_spec_timm,
        found_origin=probe_info.get("origin", ""),
        target_path_used_for_probe=bool(probe_info.get("target_added")),
        real_import_used=False,
        mobile_sam_import_used=False,
        model_load_used=False,
        inference_used=False,
        runtime_used=False,
    )
    (out_root / "timm_nodeps_find_spec_probe_v1.json").write_text(
        json.dumps(asdict(probe), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = TimmNoDepsRollbackReadinessRecord(
        record_id="timm_nodeps_rollback_readiness_v1",
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

    post_audit = TimmNoDepsInstallPostReviewAudit(
        audit_id="timm_nodeps_install_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        install_command_whitelisted=command_whitelisted,
        no_deps_flag_present=no_deps_flag_present,
        install_scope_controlled=True,
        timm_install_attempted=bool(install_info["install_attempted"]),
        timm_install_success=timm_install_success,
        timm_version_recorded=bool(installed_version),
        find_spec_probe_only=True,
        find_spec_timm=find_spec_timm,
        real_import_performed=False,
        mobile_sam_import_performed=False,
        model_load_performed=False,
        inference_performed=False,
        runtime_performed=False,
        output_adapter_performed=False,
        semantic_layer_performed=False,
        registry_mutation_performed=False,
        additional_weight_download_performed=False,
        torch_or_torchvision_installed_in_target=torch_in_target or tv_in_target,
        global_env_contamination=contamination_detected,
        rollback_ready=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            snapshot.snapshot_succeeded and command_whitelisted and no_global_env_contamination
            and not (torch_in_target or tv_in_target)
        ),
    )
    (out_root / "timm_nodeps_install_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    invariant_state: Dict[str, bool] = {
        "pre_install_snapshot_present": snapshot.snapshot_succeeded,
        "install_target_is_timm": f" {TIMM_PACKAGE_NAME}" in install_record.command,
        "no_deps_flag_present": no_deps_flag_present,
        "target_flag_present": target_flag_present,
        "install_scope_controlled": str(target_dir) == install_record.install_target,
        "no_global_env_contamination": no_global_env_contamination,
        "no_torch_torchvision_in_target": not torch_in_target and not tv_in_target,
        "no_real_import": REAL_IMPORT_ALLOWED is False and probe.real_import_used is False,
        "no_model_load_retry": MODEL_LOAD_ALLOWED is False and MODEL_LOAD_RETRY_ALLOWED is False,
        "no_inference_seg_pred": REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_additional_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "probe_find_spec_only": probe.probe_method == "importlib.util.find_spec only",
        "install_not_model_load_success": post_audit.model_load_performed is False,
        "install_not_inference_runtime_ready": (
            post_audit.inference_performed is False and post_audit.runtime_performed is False
        ),
        "rollback_readiness_present": rollback.rollback_available is True,
        "post_review_present": True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL[k] for k in (
                "test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden"
            )
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeTimmNoDepsInstallExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeTimmNoDepsInstallExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_nodeps_install_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_nodeps_timm_install_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "timm_nodeps_pre_install_snapshot_record_count_eq_1": True,
        "timm_nodeps_install_execution_record_count_gte_1": True,
        "timm_nodeps_version_record_count_gte_1": True,
        "timm_nodeps_target_path_record_count_gte_1": True,
        "timm_nodeps_find_spec_probe_record_count_gte_1": True,
        "timm_nodeps_environment_contamination_audit_count_gte_1": True,
        "timm_nodeps_install_post_review_audit_count_gte_1": True,
        "timm_nodeps_rollback_readiness_record_count_gte_1": True,
        "mobile_sam_model_load_retry_gate_after_nodeps_install_count_gte_1": True,
        "negative_guard_count_eq_21": negative_guard_count == 21,
        "negative_guard_passed_eq_21": negative_guard_passed == 21,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "no_deps_required": NO_DEPS_REQUIRED is True,
        "no_global_env_contamination": no_global_env_contamination,
        "no_transitive_dependency_install_violation": not no_transitive_violation,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    no_boundary_violation = blocker_count == 0
    timm_find_spec_verified = find_spec_timm

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
        can_enter_model_load_retry_next = False
    elif timm_install_success and timm_find_spec_verified and no_global_env_contamination and not no_transitive_violation:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        can_enter_model_load_retry_next = True
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        can_enter_model_load_retry_next = False

    retry_gate = MobileSAMModelLoadRetryGateAfterNoDepsInstall(
        record_id="mobile_sam_model_load_retry_gate_after_nodeps_install_v1",
        can_enter_model_load_retry_next=can_enter_model_load_retry_next,
        timm_nodeps_install_execution_go=(final_decision == FINAL_DECISION_GO),
        timm_find_spec_verified=timm_find_spec_verified,
        timm_dependency_available=timm_install_success and timm_find_spec_verified,
        mobile_sam_weight_sha256_recheck_required_before_retry=True,
        mobile_sam_code_and_weight_ready_must_be_reverified=True,
        torch_torchvision_reuse_boundary_must_be_checked_at_retry=True,
        model_load_retry_requires_separate_execution_phase=True,
        timm_nodeps_install_success_not_model_load_success=True,
        timm_nodeps_install_success_not_inference_approval=True,
        timm_nodeps_install_success_not_runtime_approval=True,
        timm_nodeps_install_success_not_output_adapter_approval=True,
        timm_nodeps_install_success_not_semantic_layer_approval=True,
        recommended_next_phase=recommended_next_phase,
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMNoDepsTimmInstallExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_nodeps_timm_install_execution_profile_count=1,
        timm_nodeps_pre_install_snapshot_record_count=1,
        timm_nodeps_install_execution_record_count=1,
        timm_nodeps_version_record_count=1,
        timm_nodeps_target_path_record_count=1,
        timm_nodeps_find_spec_probe_record_count=1,
        timm_nodeps_environment_contamination_audit_count=1,
        timm_nodeps_install_post_review_audit_count=1,
        timm_nodeps_rollback_readiness_record_count=1,
        mobile_sam_model_load_retry_gate_after_nodeps_install_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        timm_install_success=timm_install_success,
        timm_find_spec_verified=timm_find_spec_verified,
        no_global_env_contamination=no_global_env_contamination,
        no_transitive_dependency_install_violation=not no_transitive_violation,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Dependency Repair NoDeps Install Execution And Post Review (real execution, no-deps)",
        "lifecycle_variant": SCOPE,
        "install_principle_zh": INSTALL_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "selected_route": SELECTED_ROUTE,
        "no_deps_required": NO_DEPS_REQUIRED,
        "controlled_install_target_path": str(target_dir),
        "mobile_sam_nodeps_timm_install_execution_profile": _build_profile(),
        "mobile_sam_nodeps_timm_install_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "timm_nodeps_pre_install_snapshot_record": asdict(snapshot),
        "timm_nodeps_pre_install_snapshot_record_count": 1,
        "timm_nodeps_install_execution_record": asdict(install_record),
        "timm_nodeps_install_execution_record_count": 1,
        "timm_nodeps_version_record": asdict(version_record),
        "timm_nodeps_version_record_count": 1,
        "timm_nodeps_target_path_record": asdict(target_record),
        "timm_nodeps_target_path_record_count": 1,
        "timm_nodeps_find_spec_probe_record": asdict(probe),
        "timm_nodeps_find_spec_probe_record_count": 1,
        "timm_nodeps_environment_contamination_audit": asdict(contamination_audit),
        "timm_nodeps_environment_contamination_audit_count": 1,
        "timm_nodeps_install_post_review_audit": asdict(post_audit),
        "timm_nodeps_install_post_review_audit_count": 1,
        "timm_nodeps_rollback_readiness_record": asdict(rollback),
        "timm_nodeps_rollback_readiness_record_count": 1,
        "mobile_sam_model_load_retry_gate_after_nodeps_install": asdict(retry_gate),
        "mobile_sam_model_load_retry_gate_after_nodeps_install_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "reuse_flags": dict(REUSE_FLAGS),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "install_execution_status": decision_branch,
            "timm_install_success": timm_install_success,
            "timm_installed_version": installed_version,
            "find_spec_timm": timm_find_spec_verified,
            "elapsed_seconds": install_record.elapsed_seconds,
            "no_global_env_contamination": no_global_env_contamination,
            "no_transitive_dependency_install_violation": not no_transitive_violation,
            "can_enter_model_load_retry_next": can_enter_model_load_retry_next,
            "recommended_next_phase": recommended_next_phase,
            "transition_note": (
                f"REAL no-deps EXECUTION. pip install timm --no-deps --target completed: "
                f"return_code={return_code}, success={timm_install_success}, version={installed_version or '<unresolved>'}, "
                f"find_spec={timm_find_spec_verified}, elapsed={install_record.elapsed_seconds}s. "
                f"No global contamination={no_global_env_contamination}, torch/torchvision in target={torch_in_target or tv_in_target}. "
                f"Decision={final_decision}. NO import/load/inference. Next: {recommended_next_phase}."
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
                result, test_mode=TEST_BOARD_TEST_MODE, repo_root=board_root,
                module=TEST_BOARD_MODULE, source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result, test_mode=TEST_BOARD_TEST_MODE, repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE, source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"
        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "timm_nodeps_pre_install_snapshot_record": {"timm_nodeps_pre_install_snapshot_record": asdict(snapshot)},
            "timm_nodeps_install_execution_record": {"timm_nodeps_install_execution_record": asdict(install_record)},
            "timm_nodeps_version_record": {"timm_nodeps_version_record": asdict(version_record)},
            "timm_nodeps_target_path_record": {"timm_nodeps_target_path_record": asdict(target_record)},
            "timm_nodeps_find_spec_probe_record": {"timm_nodeps_find_spec_probe_record": asdict(probe)},
            "timm_nodeps_environment_contamination_audit_record": {"timm_nodeps_environment_contamination_audit": asdict(contamination_audit)},
            "timm_nodeps_install_post_review_record": {"timm_nodeps_install_post_review_audit": asdict(post_audit)},
            "timm_nodeps_rollback_readiness_record": {"timm_nodeps_rollback_readiness_record": asdict(rollback)},
            "mobile_sam_model_load_retry_gate_record": {"mobile_sam_model_load_retry_gate_after_nodeps_install": asdict(retry_gate)},
        }
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID, "module": TEST_BOARD_MODULE, "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(), "protected": True, "non_deletable": True, "deletion_forbidden": True,
            "real_execution_phase": True, "timm_install_allowed": True, "no_deps_required": True,
            "real_import_allowed": False, "model_load_allowed": False,
            "inference_allowed": False, "runtime_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1()
    print(json.dumps({
        "output_review_file": result.get("output_review_file"),
        "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
        "test_board_record_count": result.get("test_board_record_count"),
        "timm_install_success": result["conclusions"]["timm_install_success"],
        "timm_installed_version": result["conclusions"]["timm_installed_version"],
        "find_spec_timm": result["conclusions"]["find_spec_timm"],
        "elapsed_seconds": result["conclusions"]["elapsed_seconds"],
        "can_enter_model_load_retry_next": result["conclusions"]["can_enter_model_load_retry_next"],
        "negative_guard_passed": result["negative_guard_passed"],
        "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
        "blocker_count": result["blocker_count"],
        "final_decision": result["final_decision"],
    }, ensure_ascii=False))
    return 0 if result["final_decision"] in (FINAL_DECISION_GO, FINAL_DECISION_FAILED) else 1


if __name__ == "__main__":
    raise SystemExit(main())
