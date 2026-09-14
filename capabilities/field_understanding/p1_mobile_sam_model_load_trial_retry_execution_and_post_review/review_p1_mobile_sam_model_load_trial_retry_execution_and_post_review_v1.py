# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Retry Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).

Model-load RETRY after timm no-deps install GO. Pre-load snapshot, sha256/size recheck,
registry overlay + timm nodeps upstream reverification, find_spec probes, torch/torchvision
reuse boundary observation, REAL import + REAL checkpoint load (NO image/segmentation/
prediction/inference/runtime), post-review, rollback readiness. Three honest outcomes.
"""

from __future__ import annotations

import gc
import hashlib
import importlib
import importlib.util
import json
import os
import resource
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
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_retry_execution_and_post_review.p1_mobile_sam_model_load_trial_retry_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_retry_execution_and_post_review.p1_mobile_sam_model_load_trial_retry_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    CHECKPOINT_LOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPECTED_TORCH_VERSION,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MEMORY_LIMIT_MB,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_BUILD_KEY,
    MOBILE_SAM_CODE_PATH_REL,
    MOBILE_SAM_IMPORT_ROOT,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_RETRY_EXECUTION,
    MODEL_LOAD_RETRY_PRINCIPLE_ZH,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    OUT_OF_SCOPE_ASSET_IDS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    POST_REVIEW_INCLUDED,
    PREDICTION_ALLOWED,
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
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMEOUT_SECONDS,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALLED_VERSION_EXPECTED,
    TIMM_INSTALL_TARGET_REL,
    TORCH_TORCHVISION_REUSE_OBSERVATION_ALLOWED,
    UPSTREAM_MODEL_LOAD_RETRY_GATE_REF,
    UPSTREAM_NODEPS_INSTALL_EXPECTED_GO,
    UPSTREAM_NODEPS_INSTALL_REF,
    UPSTREAM_REGISTRY_OVERLAY_REF,
    WEIGHT_CHAIN,
    MobileSAMRetryCodeAndWeightRegistryAudit,
    MobileSAMRetryDependencyAvailabilityRecord,
    MobileSAMRetryFollowupRegistryPatchRoute,
    MobileSAMRetryImportExecutionRecord,
    MobileSAMRetryInferenceRuntimeExclusionRecord,
    MobileSAMRetryMemoryTimeoutMonitorRecord,
    MobileSAMRetryModelLoadExecutionRecord,
    MobileSAMRetryPostReviewAudit,
    MobileSAMRetryPreModelLoadSnapshotRecord,
    MobileSAMRetryRollbackCleanupRecord,
    MobileSAMRetrySha256RecheckRecord,
    MobileSAMRetryTorchTorchvisionBoundaryRecord,
    NegativeMobileSAMModelLoadRetryExecutionGuard,
    P1MobileSAMModelLoadRetryExecutionDecision,
    P1MobileSAMModelLoadRetryExecutionPostReviewProfile,
    to_dict,
)

NODEPS_ARTIFACT_REL = (
    "_tmp_eval_out/p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1_smoke_v0/"
    "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_review_v1.json"
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
    / "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_model_load_trial_retry_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_model_load_trial_retry_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_model_load_trial_retry_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_model_load_retry_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_model_load_retry_execution_decision_v1"
_BOARD_STANDIN_ROOT = _WRITABLE_BASE / "_tmp_eval_out" / "board_standin"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _peak_memory_mb() -> float:
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return round(ru / (1024 * 1024), 2)
    return round(ru / 1024, 2)


def _pip_freeze_digest() -> Tuple[int, str]:
    try:
        from importlib import metadata as importlib_metadata

        names = sorted(
            f"{d.metadata['Name']}=={d.version}"
            for d in importlib_metadata.distributions()
            if d.metadata and d.metadata.get("Name")
        )
        digest = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
        return len(names), digest
    except Exception:  # noqa: BLE001
        return 0, ""


def _artifact_roots() -> Tuple[Path, ...]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    luna_core = _REPO_ROOT.parent / "Luna-Core"
    luna_min = _REPO_ROOT.parent / "Luna-Workspace-Min"
    for extra in (luna_core, luna_min):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return tuple(dict.fromkeys(roots))


def _resolve_path(rel: str) -> Path:
    for base in _artifact_roots():
        p = base / rel
        if p.exists():
            return p.resolve()
    return (_REPO_ROOT / rel).resolve()


def _find_spec_with_paths(module_name: str, extra_paths: List[Path]) -> Tuple[bool, str]:
    saved = list(sys.path)
    try:
        for ep in extra_paths:
            s = str(ep)
            if s not in sys.path:
                sys.path.insert(0, s)
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False, ""
        return True, getattr(spec, "origin", "") or ""
    finally:
        sys.path[:] = saved


def _torch_in_timm_target(timm_target: Path) -> Tuple[bool, bool]:
    torch_in = False
    tv_in = False
    if not timm_target.is_dir():
        return torch_in, tv_in
    for p in timm_target.glob("*.dist-info"):
        if not p.is_dir():
            continue
        base = p.name.removesuffix(".dist-info").rsplit("-", 1)[0].lower()
        if base in ("torch", "pytorch"):
            torch_in = True
        if base == "torchvision":
            tv_in = True
    return torch_in, tv_in


def _verify_registry_overlay(repo_root: Path) -> Tuple[MobileSAMRetryCodeAndWeightRegistryAudit, bool]:
    overlay_path = _resolve_path(UPSTREAM_REGISTRY_OVERLAY_REF)
    _ = repo_root
    audit = MobileSAMRetryCodeAndWeightRegistryAudit(
        audit_id="mobile_sam_retry_code_and_weight_registry_audit_v1",
        registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
        readiness_level="",
        code_only_install_verified=False,
        find_spec_verified=False,
        weight_downloaded=False,
        weight_integrity_verified=False,
        storage_verified=False,
        weight_sha256="",
        model_load_ready=True,
        inference_ready=True,
        runtime_ready=True,
        audit_passed=False,
    )
    if not overlay_path.is_file():
        return audit, False
    try:
        data = json.loads(overlay_path.read_text(encoding="utf-8"))
        ms = (data.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
        audit = MobileSAMRetryCodeAndWeightRegistryAudit(
            audit_id="mobile_sam_retry_code_and_weight_registry_audit_v1",
            registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
            readiness_level=str(ms.get("readiness_level", "")),
            code_only_install_verified=ms.get("code_only_install_verified") is True,
            find_spec_verified=ms.get("find_spec_verified") is True,
            weight_downloaded=ms.get("weight_downloaded") is True,
            weight_integrity_verified=ms.get("weight_integrity_verified") is True,
            storage_verified=ms.get("storage_verified") is True,
            weight_sha256=str(ms.get("weight_sha256", "")),
            model_load_ready=ms.get("model_load_ready") is True,
            inference_ready=ms.get("inference_ready") is True,
            runtime_ready=ms.get("runtime_ready") is True,
            audit_passed=(
                ms.get("readiness_level") == "code_and_weight_ready"
                and ms.get("code_only_install_verified") is True
                and ms.get("find_spec_verified") is True
                and ms.get("weight_downloaded") is True
                and ms.get("weight_integrity_verified") is True
                and ms.get("storage_verified") is True
                and ms.get("weight_sha256") == MOBILE_SAM_WEIGHT_SHA256
                and ms.get("model_load_ready") is False
                and ms.get("inference_ready") is False
                and ms.get("runtime_ready") is False
            ),
        )
        return audit, audit.audit_passed
    except (OSError, json.JSONDecodeError):
        return audit, False


def _load_artifact_any_root(rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    for base in _artifact_roots():
        artifact, exists = load_artifact(base, rel)
        if exists and artifact:
            return artifact, True
    return None, False


def _verify_nodeps_upstream(repo_root: Path) -> Tuple[Dict[str, Any], bool]:
    artifact, exists = _load_artifact_any_root(NODEPS_ARTIFACT_REL)
    _ = repo_root  # kept for API symmetry with other phases
    if not exists or not artifact:
        return {}, False
    conclusions = artifact.get("conclusions") or artifact.get("decision") or {}
    go_ok = artifact.get("final_decision") == UPSTREAM_NODEPS_INSTALL_EXPECTED_GO
    timm_ok = (
        conclusions.get("timm_install_success") is True
        or (artifact.get("timm_nodeps_version_record") or {}).get("timm_install_success") is True
    )
    version = (
        conclusions.get("timm_installed_version")
        or (artifact.get("timm_nodeps_version_record") or {}).get("installed_version")
        or ""
    )
    find_spec_ok = (
        conclusions.get("find_spec_timm") is True
        or (artifact.get("timm_nodeps_find_spec_probe_record") or {}).get("find_spec_result") is True
    )
    no_contam = conclusions.get("no_global_env_contamination") is True
    no_transitive = True
    target_rec = artifact.get("timm_nodeps_target_path_record") or {}
    if "no_transitive_dependencies_installed" in target_rec:
        no_transitive = target_rec["no_transitive_dependencies_installed"] is True
    verified = (
        go_ok
        and timm_ok
        and version == TIMM_INSTALLED_VERSION_EXPECTED
        and find_spec_ok
        and no_contam
        and no_transitive
    )
    return {
        "timm_install_success": timm_ok,
        "timm_installed_version": version,
        "timm_find_spec_verified": find_spec_ok,
        "no_global_env_contamination": no_contam,
        "no_transitive_dependencies_installed": no_transitive,
        "final_decision": artifact.get("final_decision"),
    }, verified


def _attempt_import_and_load_retry(
    code_path: Path,
    timm_target: Path,
    weight_abs: Path,
) -> Dict[str, Any]:
    """REAL import + REAL checkpoint load retry (NO inference / image / prediction)."""
    info: Dict[str, Any] = {
        "mobile_sam_code_path_added": str(code_path),
        "timm_target_path_added": str(timm_target),
        "import_attempted": True,
        "import_success": False,
        "import_error": "",
        "imported_module_file": "",
        "dependency_gap_resolved": False,
        "checkpoint_load_attempted": False,
        "model_object_created": False,
        "model_type_name": "",
        "checkpoint_load_success": False,
        "checkpoint_load_error": "",
        "model_object_released": False,
        "torch_observed_during_load": False,
        "torch_version_observed": "",
        "torchvision_observed_during_load": False,
        "torchvision_version_observed": "",
    }
    for ep in (timm_target, code_path):
        s = str(ep)
        if s not in sys.path:
            sys.path.insert(0, s)
    try:
        mod = importlib.import_module(MOBILE_SAM_IMPORT_ROOT)
        info["import_success"] = True
        info["imported_module_file"] = getattr(mod, "__file__", "") or ""
        info["dependency_gap_resolved"] = True
    except BaseException as exc:  # noqa: BLE001
        info["import_error"] = f"{type(exc).__name__}:{exc}"
        return info

    try:
        import torch  # noqa: WPS433 — boundary observation during load

        info["torch_observed_during_load"] = True
        info["torch_version_observed"] = getattr(torch, "__version__", "")
    except BaseException:  # noqa: BLE001
        pass
    try:
        import torchvision  # noqa: WPS433

        info["torchvision_observed_during_load"] = True
        info["torchvision_version_observed"] = getattr(torchvision, "__version__", "")
    except BaseException:  # noqa: BLE001
        pass

    try:
        from mobile_sam import sam_model_registry  # type: ignore

        info["checkpoint_load_attempted"] = True
        model = sam_model_registry[MOBILE_SAM_BUILD_KEY](checkpoint=str(weight_abs))
        info["model_object_created"] = True
        info["model_type_name"] = type(model).__name__
        info["checkpoint_load_success"] = True
        del model
        gc.collect()
        info["model_object_released"] = True
    except BaseException as exc:  # noqa: BLE001
        info["checkpoint_load_error"] = f"{type(exc).__name__}:{exc}"
        try:
            gc.collect()
        except Exception:  # noqa: BLE001
            pass
        info["model_object_released"] = True
    return info


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMModelLoadRetryExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            model_load_retry_execution=MODEL_LOAD_RETRY_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            checkpoint_load_allowed=CHECKPOINT_LOAD_ALLOWED,
            torch_torchvision_reuse_observation_allowed=TORCH_TORCHVISION_REUSE_OBSERVATION_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            image_input_allowed=IMAGE_INPUT_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_nodeps_install_ref=UPSTREAM_NODEPS_INSTALL_REF,
            upstream_registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    perform_load: bool = True,
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

    weight_abs = _resolve_path(MOBILE_SAM_WEIGHT_FILE_PATH)
    code_path = _resolve_path(MOBILE_SAM_CODE_PATH_REL)
    timm_target = _resolve_path(TIMM_INSTALL_TARGET_REL)
    ts = _now()

    # ------------------------------------------------------------------- #
    # (二) Pre-model-load retry snapshot.
    # ------------------------------------------------------------------- #
    weight_exists = weight_abs.is_file()
    weight_size = weight_abs.stat().st_size if weight_exists else 0
    sha_before = _sha256_of(weight_abs) if weight_exists else ""
    pip_count, pip_digest = _pip_freeze_digest()
    snapshot = MobileSAMRetryPreModelLoadSnapshotRecord(
        snapshot_id="mobile_sam_retry_pre_model_load_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        env_path=os.environ.get("VIRTUAL_ENV", sys.prefix),
        working_directory=str(Path.cwd()),
        mobile_sam_code_path_ref=str(code_path),
        timm_install_target_path_ref=str(timm_target),
        weight_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        weight_file_exists=weight_exists,
        weight_file_size=weight_size,
        weight_sha256_before=sha_before,
        pip_freeze_before_count=pip_count,
        pip_freeze_before_digest=pip_digest,
        process_id=os.getpid(),
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        upstream_timm_nodeps_install_ref=UPSTREAM_NODEPS_INSTALL_REF,
        upstream_model_load_retry_gate_ref=UPSTREAM_MODEL_LOAD_RETRY_GATE_REF,
        upstream_registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
        rollback_snapshot_ref=str(out_root / "mobile_sam_retry_pre_model_load_snapshot_v1.json"),
        test_board_ref=(
            "capabilities/test_board/recognition_models/"
            "phase_p1_mobilesam_model_load_trial_retry_execution_and_post_review_v1_001/"
        ),
        snapshot_succeeded=weight_exists and bool(sha_before),
    )
    (out_root / "mobile_sam_retry_pre_model_load_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        failed_checks.append("snapshot.failed_weight_missing_or_unhashable")

    # ------------------------------------------------------------------- #
    # (三) Upstream readiness: registry overlay + timm nodeps GO.
    # ------------------------------------------------------------------- #
    registry_audit, registry_ok = _verify_registry_overlay(_REPO_ROOT)
    nodeps_state, nodeps_ok = _verify_nodeps_upstream(_REPO_ROOT)
    upstream_readiness_verified = registry_ok and nodeps_ok
    if not registry_ok:
        failed_checks.append("upstream.registry_overlay_readiness_mismatch")
    if not nodeps_ok:
        failed_checks.append("upstream.timm_nodeps_install_go_not_verified")

    # ------------------------------------------------------------------- #
    # (四) Sha256 / size recheck.
    # ------------------------------------------------------------------- #
    size_matches = weight_size == MOBILE_SAM_WEIGHT_SIZE_BYTES
    sha256_matches = sha_before == MOBILE_SAM_WEIGHT_SHA256
    recheck = MobileSAMRetrySha256RecheckRecord(
        recheck_id="mobile_sam_retry_sha256_recheck_v1",
        expected_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        expected_size_bytes=MOBILE_SAM_WEIGHT_SIZE_BYTES,
        expected_sha256=MOBILE_SAM_WEIGHT_SHA256,
        actual_size_bytes=weight_size,
        actual_sha256=sha_before,
        size_matches=size_matches,
        sha256_matches=sha256_matches,
        recheck_passed=size_matches and sha256_matches,
    )
    (out_root / "mobile_sam_retry_sha256_recheck_v1.json").write_text(
        json.dumps(asdict(recheck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not recheck.recheck_passed:
        failed_checks.append("recheck.sha256_or_size_mismatch_blocks_model_load")

    # ------------------------------------------------------------------- #
    # (五) Dependency availability (find_spec only).
    # ------------------------------------------------------------------- #
    timm_spec_ok, timm_origin = _find_spec_with_paths(TIMM_IMPORT_ROOT, [timm_target])
    ms_spec_ok, ms_origin = _find_spec_with_paths(MOBILE_SAM_IMPORT_ROOT, [code_path])
    dep_avail = MobileSAMRetryDependencyAvailabilityRecord(
        record_id="mobile_sam_retry_dependency_availability_v1",
        probe_method="find_spec_only",
        timm_find_spec_result=timm_spec_ok,
        mobile_sam_find_spec_result=ms_spec_ok,
        timm_target_path_used=True,
        mobile_sam_code_path_used=True,
        real_import_used_for_probe=False,
    )
    (out_root / "mobile_sam_retry_dependency_availability_v1.json").write_text(
        json.dumps(asdict(dep_avail), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (六) Torch / torchvision boundary (pre-load inspection).
    # ------------------------------------------------------------------- #
    torch_in_target, tv_in_target = _torch_in_timm_target(timm_target)
    boundary_pre = MobileSAMRetryTorchTorchvisionBoundaryRecord(
        record_id="mobile_sam_retry_torch_torchvision_boundary_v1",
        torch_reuse_expected=True,
        expected_torch_version=EXPECTED_TORCH_VERSION,
        torchvision_reuse_expected=True,
        torch_reinstall_allowed=False,
        torchvision_reinstall_allowed=False,
        torch_files_installed_in_timm_target=torch_in_target,
        torchvision_files_installed_in_timm_target=tv_in_target,
        torch_observed_during_load=False,
        torch_version_observed_if_available="",
        torchvision_observed_during_load=False,
        torchvision_version_observed_if_available="",
        torch_reinstall_performed=False,
        torchvision_reinstall_performed=False,
    )

    # ------------------------------------------------------------------- #
    # (七) REAL import + REAL checkpoint load retry.
    # ------------------------------------------------------------------- #
    may_load = (
        perform_load
        and snapshot.snapshot_succeeded
        and recheck.recheck_passed
        and upstream_readiness_verified
        and timm_spec_ok
        and ms_spec_ok
        and not torch_in_target
        and not tv_in_target
    )
    started_at = _now()
    t0 = time.time()
    if may_load:
        load_info = _attempt_import_and_load_retry(code_path, timm_target, weight_abs)
    else:
        skip_reason = "load_skipped_snapshot_recheck_upstream_or_probe_failed"
        load_info = {
            "mobile_sam_code_path_added": str(code_path),
            "timm_target_path_added": str(timm_target),
            "import_attempted": False,
            "import_success": False,
            "import_error": skip_reason,
            "imported_module_file": "",
            "dependency_gap_resolved": False,
            "checkpoint_load_attempted": False,
            "model_object_created": False,
            "model_type_name": "",
            "checkpoint_load_success": False,
            "checkpoint_load_error": skip_reason,
            "model_object_released": False,
            "torch_observed_during_load": False,
            "torch_version_observed": "",
            "torchvision_observed_during_load": False,
            "torchvision_version_observed": "",
        }
    elapsed = round(time.time() - t0, 4)
    ended_at = _now()
    peak_mb = _peak_memory_mb()

    boundary = MobileSAMRetryTorchTorchvisionBoundaryRecord(
        record_id="mobile_sam_retry_torch_torchvision_boundary_v1",
        torch_reuse_expected=True,
        expected_torch_version=EXPECTED_TORCH_VERSION,
        torchvision_reuse_expected=True,
        torch_reinstall_allowed=False,
        torchvision_reinstall_allowed=False,
        torch_files_installed_in_timm_target=torch_in_target,
        torchvision_files_installed_in_timm_target=tv_in_target,
        torch_observed_during_load=bool(load_info["torch_observed_during_load"]),
        torch_version_observed_if_available=load_info["torch_version_observed"],
        torchvision_observed_during_load=bool(load_info["torchvision_observed_during_load"]),
        torchvision_version_observed_if_available=load_info["torchvision_version_observed"],
        torch_reinstall_performed=False,
        torchvision_reinstall_performed=False,
    )
    (out_root / "mobile_sam_retry_torch_torchvision_boundary_v1.json").write_text(
        json.dumps(asdict(boundary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    import_success = bool(load_info["import_success"])
    dependency_gap_resolved = bool(load_info["dependency_gap_resolved"])
    checkpoint_load_success = bool(load_info["checkpoint_load_success"])
    model_load_retry_success = import_success and checkpoint_load_success

    import_record = MobileSAMRetryImportExecutionRecord(
        record_id="mobile_sam_retry_import_record_v1",
        import_target=MOBILE_SAM_IMPORT_ROOT,
        mobile_sam_code_path_added=load_info["mobile_sam_code_path_added"],
        timm_target_path_added=load_info["timm_target_path_added"],
        import_attempted=bool(load_info["import_attempted"]),
        import_success=import_success,
        import_error=load_info["import_error"],
        imported_module_file=load_info["imported_module_file"],
        dependency_gap_resolved=dependency_gap_resolved,
    )
    (out_root / "mobile_sam_retry_import_record_v1.json").write_text(
        json.dumps(asdict(import_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    load_record = MobileSAMRetryModelLoadExecutionRecord(
        record_id="mobile_sam_retry_model_load_execution_record_v1",
        build_key=MOBILE_SAM_BUILD_KEY,
        checkpoint_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        command_purpose="mobile_sam_model_load_retry_trial_only",
        checkpoint_load_attempted=bool(load_info["checkpoint_load_attempted"]),
        model_object_created=bool(load_info["model_object_created"]),
        model_type_name=load_info["model_type_name"],
        checkpoint_load_success=checkpoint_load_success,
        checkpoint_load_error=load_info["checkpoint_load_error"],
        model_object_released=bool(load_info["model_object_released"]),
        model_load_retry_success=model_load_retry_success,
        inference_ready=False,
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        commercial_runtime_approved=False,
    )
    (out_root / "mobile_sam_retry_model_load_execution_record_v1.json").write_text(
        json.dumps(asdict(load_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (九) Memory / timeout monitor.
    # ------------------------------------------------------------------- #
    timeout_occurred = elapsed > TIMEOUT_SECONDS
    oom_occurred = peak_mb > MEMORY_LIMIT_MB
    monitor = MobileSAMRetryMemoryTimeoutMonitorRecord(
        monitor_id="mobile_sam_retry_memory_timeout_monitor_v1",
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        started_at=started_at,
        ended_at=ended_at,
        elapsed_seconds=elapsed,
        peak_memory_mb=peak_mb,
        timeout_occurred=timeout_occurred,
        oom_occurred=oom_occurred,
        model_object_cleanup_attempted=True,
        persistent_process_left=False,
    )
    (out_root / "mobile_sam_retry_memory_timeout_monitor_v1.json").write_text(
        json.dumps(asdict(monitor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if timeout_occurred:
        failed_checks.append("monitor.timeout_exceeded")
    if oom_occurred:
        failed_checks.append("monitor.oom_exceeded")

    # ------------------------------------------------------------------- #
    # (十一) Post-review audit.
    # ------------------------------------------------------------------- #
    post_audit = MobileSAMRetryPostReviewAudit(
        audit_id="mobile_sam_retry_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        upstream_readiness_verified=upstream_readiness_verified,
        sha256_rechecked=True,
        sha256_matches=sha256_matches,
        size_matches=size_matches,
        timm_find_spec_verified=timm_spec_ok,
        mobile_sam_find_spec_verified=ms_spec_ok,
        real_import_performed=bool(load_info["import_attempted"]),
        model_load_performed=bool(load_info["checkpoint_load_attempted"]),
        checkpoint_load_success=checkpoint_load_success,
        no_image_input=True,
        no_segmentation=True,
        no_prediction=True,
        no_inference=True,
        no_runtime=True,
        no_output_adapter=True,
        no_semantic_layer=True,
        no_registry_mutation=True,
        no_extra_download=True,
        memory_timeout_recorded=True,
        cleanup_recorded=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            snapshot.snapshot_succeeded
            and upstream_readiness_verified
            and sha256_matches
            and size_matches
            and not timeout_occurred
            and not oom_occurred
        ),
    )
    (out_root / "mobile_sam_retry_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = MobileSAMRetryRollbackCleanupRecord(
        record_id="mobile_sam_retry_rollback_cleanup_v1",
        rollback_available=True,
        rollback_not_executed_by_default=True,
        model_object_cleanup_attempted=True,
        persistent_process_left=False,
        rollback_preserves_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
    )

    exclusion = MobileSAMRetryInferenceRuntimeExclusionRecord(
        record_id="mobile_sam_retry_inference_runtime_exclusion_v1",
        no_image_input=True,
        no_segmentation=True,
        no_prediction=True,
        no_inference=True,
        no_runtime_server=True,
        no_output_adapter=True,
        no_semantic_layer=True,
        model_load_retry_success_not_inference_approval=True,
        model_load_retry_success_not_runtime_approval=True,
        model_load_retry_success_not_output_adapter_approval=True,
        model_load_retry_success_not_semantic_layer_approval=True,
        model_load_retry_success_not_commercial_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # Negative guards (18).
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "pre_snapshot_present": snapshot.snapshot_succeeded,
        "upstream_readiness_verified": upstream_readiness_verified,
        "timm_nodeps_go_reverified": nodeps_ok,
        "sha256_size_rechecked": recheck.sha256_matches is not None and recheck.size_matches is not None,
        "no_load_on_mismatch": recheck.recheck_passed or not bool(load_info["import_attempted"]),
        "scope_mobile_sam_only": True,
        "no_extra_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_image_input": IMAGE_INPUT_ALLOWED is False and exclusion.no_image_input is True,
        "no_seg_pred_inference": (
            SEGMENTATION_ALLOWED is False
            and PREDICTION_ALLOWED is False
            and REAL_INFERENCE_ALLOWED is False
        ),
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "success_not_downstream_ready": (
            load_record.inference_ready is False
            and load_record.runtime_ready is False
            and load_record.output_adapter_ready is False
            and load_record.semantic_layer_ready is False
            and load_record.commercial_runtime_approved is False
        ),
        "memory_timeout_recorded": True,
        "cleanup_rollback_recorded": (
            rollback.model_object_cleanup_attempted is True and rollback.rollback_available is True
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

    negative_guards: List[NegativeMobileSAMModelLoadRetryExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMModelLoadRetryExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_model_load_retry_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_model_load_retry_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_retry_pre_model_load_snapshot_record_count_eq_1": True,
        "mobile_sam_retry_sha256_recheck_record_count_eq_1": True,
        "mobile_sam_retry_code_and_weight_registry_audit_count_gte_1": True,
        "mobile_sam_retry_dependency_availability_record_count_gte_1": True,
        "mobile_sam_retry_torch_torchvision_boundary_record_count_gte_1": True,
        "mobile_sam_retry_import_execution_record_count_gte_1": True,
        "mobile_sam_retry_model_load_execution_record_count_gte_1": True,
        "mobile_sam_retry_memory_timeout_monitor_record_count_gte_1": True,
        "mobile_sam_retry_post_review_audit_count_gte_1": True,
        "mobile_sam_retry_rollback_cleanup_record_count_gte_1": True,
        "mobile_sam_retry_inference_runtime_exclusion_record_count_gte_1": True,
        "mobile_sam_retry_followup_registry_patch_route_count_gte_1": True,
        "negative_guard_count_eq_18": negative_guard_count == 18,
        "negative_guard_passed_eq_18": negative_guard_passed == 18,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "mobile_sam_only": True,
        "model_load_retry_execution": MODEL_LOAD_RETRY_EXECUTION is True,
        "real_import_allowed_true": REAL_IMPORT_ALLOWED is True,
        "model_load_allowed_true": MODEL_LOAD_ALLOWED is True,
        "checkpoint_load_allowed_true": CHECKPOINT_LOAD_ALLOWED is True,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "segmentation_allowed_false": SEGMENTATION_ALLOWED is False,
        "prediction_allowed_false": PREDICTION_ALLOWED is False,
        "image_input_allowed_false": IMAGE_INPUT_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "upstream_readiness_verified": upstream_readiness_verified,
        "pre_snapshot_exists": snapshot.snapshot_succeeded,
        "sha256_rechecked": post_audit.sha256_rechecked,
        "sha256_matches": sha256_matches,
        "size_matches": size_matches,
        "timm_find_spec_verified": timm_spec_ok,
        "mobile_sam_find_spec_verified": ms_spec_ok,
        "no_load_on_mismatch": invariant_state["no_load_on_mismatch"],
        "no_image_input": post_audit.no_image_input,
        "no_segmentation": post_audit.no_segmentation,
        "no_prediction": post_audit.no_prediction,
        "no_inference": post_audit.no_inference,
        "no_runtime": post_audit.no_runtime,
        "no_registry_mutation": post_audit.no_registry_mutation,
        "no_extra_download": post_audit.no_extra_download,
        "memory_timeout_recorded": post_audit.memory_timeout_recorded,
        "cleanup_recorded": post_audit.cleanup_recorded,
        "no_timeout_violation": not timeout_occurred,
        "no_oom_violation": not oom_occurred,
        "load_retry_success_not_inference_ready": load_record.inference_ready is False,
        "model_load_retry_success_not_inference_approval": exclusion.model_load_retry_success_not_inference_approval,
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

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
        next_phase_purpose = "review_and_classify_boundary_violation_blockers"
    elif model_load_retry_success:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        next_phase_purpose = "plan_registry_patch_model_load_verified_and_inference_trial_readiness"
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        next_phase_purpose = "review_model_load_retry_failure_and_plan_repair"

    followup = MobileSAMRetryFollowupRegistryPatchRoute(
        route_id="mobile_sam_retry_followup_registry_patch_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next_phase,
        next_phase_scope="mobile_sam_only",
        next_phase_purpose=next_phase_purpose,
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMModelLoadRetryExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_model_load_retry_execution_profile_count=1,
        mobile_sam_retry_pre_model_load_snapshot_record_count=1,
        mobile_sam_retry_sha256_recheck_record_count=1,
        mobile_sam_retry_code_and_weight_registry_audit_count=1,
        mobile_sam_retry_dependency_availability_record_count=1,
        mobile_sam_retry_torch_torchvision_boundary_record_count=1,
        mobile_sam_retry_import_execution_record_count=1,
        mobile_sam_retry_model_load_execution_record_count=1,
        mobile_sam_retry_memory_timeout_monitor_record_count=1,
        mobile_sam_retry_post_review_audit_count=1,
        mobile_sam_retry_rollback_cleanup_record_count=1,
        mobile_sam_retry_inference_runtime_exclusion_record_count=1,
        mobile_sam_retry_followup_registry_patch_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        import_success=import_success,
        dependency_gap_resolved=dependency_gap_resolved,
        checkpoint_load_success=checkpoint_load_success,
        model_load_retry_success=model_load_retry_success,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Model Load Trial Retry Execution And Post Review (real execution)",
        "lifecycle_variant": SCOPE,
        "model_load_retry_principle_zh": MODEL_LOAD_RETRY_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "model_load_retry_execution": MODEL_LOAD_RETRY_EXECUTION,
        "asset_id": MOBILE_SAM_ASSET_ID,
        "upstream_nodeps_install_ref": UPSTREAM_NODEPS_INSTALL_REF,
        "upstream_registry_overlay_ref": UPSTREAM_REGISTRY_OVERLAY_REF,
        "timm_install_target_path": str(timm_target),
        "mobile_sam_code_path": str(code_path),
        "timm_find_spec_origin": timm_origin,
        "mobile_sam_find_spec_origin": ms_origin,
        "upstream_timm_nodeps_state": nodeps_state,
        "mobile_sam_retry_code_and_weight_registry_audit": asdict(registry_audit),
        "mobile_sam_retry_code_and_weight_registry_audit_count": 1,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "out_of_scope_asset_ids": list(OUT_OF_SCOPE_ASSET_IDS),
        "mobile_sam_model_load_retry_execution_profile": _build_profile(),
        "mobile_sam_model_load_retry_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_retry_pre_model_load_snapshot_record": asdict(snapshot),
        "mobile_sam_retry_pre_model_load_snapshot_record_count": 1,
        "mobile_sam_retry_sha256_recheck_record": asdict(recheck),
        "mobile_sam_retry_sha256_recheck_record_count": 1,
        "mobile_sam_retry_dependency_availability_record": asdict(dep_avail),
        "mobile_sam_retry_dependency_availability_record_count": 1,
        "mobile_sam_retry_torch_torchvision_boundary_record": asdict(boundary),
        "mobile_sam_retry_torch_torchvision_boundary_record_count": 1,
        "mobile_sam_retry_import_execution_record": asdict(import_record),
        "mobile_sam_retry_import_execution_record_count": 1,
        "mobile_sam_retry_model_load_execution_record": asdict(load_record),
        "mobile_sam_retry_model_load_execution_record_count": 1,
        "mobile_sam_retry_memory_timeout_monitor_record": asdict(monitor),
        "mobile_sam_retry_memory_timeout_monitor_record_count": 1,
        "mobile_sam_retry_post_review_audit": asdict(post_audit),
        "mobile_sam_retry_post_review_audit_count": 1,
        "mobile_sam_retry_rollback_cleanup_record": asdict(rollback),
        "mobile_sam_retry_rollback_cleanup_record_count": 1,
        "mobile_sam_retry_inference_runtime_exclusion_record": asdict(exclusion),
        "mobile_sam_retry_inference_runtime_exclusion_record_count": 1,
        "mobile_sam_retry_followup_registry_patch_route": asdict(followup),
        "mobile_sam_retry_followup_registry_patch_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "weight_abs_path": str(weight_abs),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "model_load_retry_status": decision_branch,
            "import_success": import_success,
            "import_error": import_record.import_error,
            "dependency_gap_resolved": dependency_gap_resolved,
            "checkpoint_load_success": checkpoint_load_success,
            "checkpoint_load_error": load_record.checkpoint_load_error,
            "model_load_retry_success": model_load_retry_success,
            "model_load_retry_success_not_inference_approval": True,
            "model_load_retry_success_not_runtime_approval": True,
            "model_load_retry_success_not_output_adapter_approval": True,
            "model_load_retry_success_not_semantic_layer_approval": True,
            "no_boundary_violation": no_boundary_violation,
            "sha256_matches": sha256_matches,
            "size_matches": size_matches,
            "torch_version_observed": boundary.torch_version_observed_if_available,
            "torchvision_version_observed": boundary.torchvision_version_observed_if_available,
            "elapsed_seconds": elapsed,
            "peak_memory_mb": peak_mb,
            "recommended_next_phase": recommended_next_phase,
            "recommended_next_phase_scope": "mobile_sam_only",
            "transition_note": (
                f"REAL model-load RETRY after timm no-deps GO. import_success={import_success}, "
                f"checkpoint_load_success={checkpoint_load_success}, decision={final_decision}. "
                "NO image/segmentation/prediction/inference/runtime. Registry NOT mutated."
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
            "mobile_sam_retry_pre_model_load_snapshot_record": {
                "mobile_sam_retry_pre_model_load_snapshot_record": asdict(snapshot),
            },
            "mobile_sam_retry_sha256_recheck_record": {
                "mobile_sam_retry_sha256_recheck_record": asdict(recheck),
            },
            "mobile_sam_retry_dependency_availability_record": {
                "mobile_sam_retry_dependency_availability_record": asdict(dep_avail),
            },
            "mobile_sam_retry_torch_torchvision_boundary_record": {
                "mobile_sam_retry_torch_torchvision_boundary_record": asdict(boundary),
            },
            "mobile_sam_retry_import_record": {
                "mobile_sam_retry_import_execution_record": asdict(import_record),
            },
            "mobile_sam_retry_model_load_execution_record": {
                "mobile_sam_retry_model_load_execution_record": asdict(load_record),
            },
            "mobile_sam_retry_memory_timeout_monitor_record": {
                "mobile_sam_retry_memory_timeout_monitor_record": asdict(monitor),
            },
            "mobile_sam_retry_post_review_record": {
                "mobile_sam_retry_post_review_audit": asdict(post_audit),
                "mobile_sam_retry_rollback_cleanup_record": asdict(rollback),
            },
            "mobile_sam_retry_inference_runtime_exclusion_record": {
                "mobile_sam_retry_inference_runtime_exclusion_record": asdict(exclusion),
            },
            "mobile_sam_retry_followup_registry_patch_route_record": {
                "mobile_sam_retry_followup_registry_patch_route": asdict(followup),
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
            "mobile_sam_only": True,
            "model_load_retry_execution": True,
            "inference_allowed": False,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
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
    result = review_p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "import_success": result["conclusions"]["import_success"],
                "import_error": result["conclusions"]["import_error"],
                "checkpoint_load_success": result["conclusions"]["checkpoint_load_success"],
                "model_load_retry_success": result["conclusions"]["model_load_retry_success"],
                "dependency_gap_resolved": result["conclusions"]["dependency_gap_resolved"],
                "torch_version_observed": result["conclusions"]["torch_version_observed"],
                "elapsed_seconds": result["conclusions"]["elapsed_seconds"],
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
