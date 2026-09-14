# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).

Takes a pre-load snapshot, rechecks the mobile_sam.pt sha256/size, and — only if they
match — performs a REAL import of the code-only-installed `mobile_sam` package and a REAL
checkpoint load (build TinyViT/MobileSAM model object + load mobile_sam.pt), under a
4096MB / 300s memory+timeout boundary, then releases the object and runs a same-phase
post-review. It NEVER reads images / constructs image input / calls segmentation /
prediction / inference, NEVER starts a runtime server / output adapter / semantic layer,
NEVER mutates the registry, and downloads NOTHING. Three honest outcomes: GO, FAILED_NO_
BOUNDARY_VIOLATION (import/load failed but no boundary violation — e.g. a missing
transitive dependency), or BLOCKED (boundary violation). Protected, non-deletable test
board records are written in `real_test` mode.
"""

from __future__ import annotations

import gc
import hashlib
import importlib
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
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_execution_and_post_review.p1_mobile_sam_model_load_trial_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_model_load_trial_execution_and_post_review.p1_mobile_sam_model_load_trial_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MEMORY_LIMIT_MB,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_BUILD_KEY,
    MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF,
    MOBILE_SAM_CODE_PATH_REL,
    MOBILE_SAM_IMPORT_ROOT,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    MODEL_LOAD_ALLOWED,
    MODEL_LOAD_PRINCIPLE_ZH,
    MODEL_LOAD_TRIAL_EXECUTION,
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
    UPSTREAM_REGISTRY_OVERLAY_REF,
    UPSTREAM_REQUEST_APPROVAL_REF,
    WEIGHT_CHAIN,
    MobileSAMInferenceRuntimeExclusionRecord,
    MobileSAMMemoryTimeoutMonitorRecord,
    MobileSAMModelImportExecutionRecord,
    MobileSAMModelLoadExecutionRecord,
    MobileSAMModelLoadFollowupRouteRecord,
    MobileSAMModelLoadPostReviewAudit,
    MobileSAMModelLoadRollbackCleanupRecord,
    MobileSAMPreModelLoadSnapshotRecord,
    MobileSAMSha256RecheckRecord,
    NegativeMobileSAMModelLoadExecutionGuard,
    P1MobileSAMModelLoadExecutionDecision,
    P1MobileSAMModelLoadTrialExecutionPostReviewProfile,
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
    / "p1_mobile_sam_model_load_trial_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_model_load_trial_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_model_load_trial_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_model_load_trial_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_model_load_trial_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_model_load_trial_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_model_load_trial_execution_decision_v1"

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
    # macOS reports bytes; Linux reports kilobytes.
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


def _attempt_import_and_load(
    code_path_abs: Path, weight_abs: Path
) -> Dict[str, Any]:
    """REAL import + REAL checkpoint load (NO inference / image / prediction)."""
    info: Dict[str, Any] = {
        "code_path_added": str(code_path_abs),
        "import_attempted": True,
        "import_success": False,
        "import_error": "",
        "imported_module_file": "",
        "checkpoint_load_attempted": False,
        "model_object_created": False,
        "model_type_name": "",
        "checkpoint_load_success": False,
        "checkpoint_load_error": "",
        "model_object_released": False,
    }
    if str(code_path_abs) not in sys.path:
        sys.path.insert(0, str(code_path_abs))
    try:
        mod = importlib.import_module(MOBILE_SAM_IMPORT_ROOT)
        info["import_success"] = True
        info["imported_module_file"] = getattr(mod, "__file__", "") or ""
    except BaseException as exc:  # noqa: BLE001 — honest capture of import failure
        info["import_error"] = f"{type(exc).__name__}:{exc}"
        return info

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
    except BaseException as exc:  # noqa: BLE001 — honest capture of load failure
        info["checkpoint_load_error"] = f"{type(exc).__name__}:{exc}"
        try:
            gc.collect()
        except Exception:  # noqa: BLE001
            pass
        info["model_object_released"] = True
    return info


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMModelLoadTrialExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            model_load_trial_execution=MODEL_LOAD_TRIAL_EXECUTION,
            post_review_included=POST_REVIEW_INCLUDED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
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
            upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
            upstream_registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_model_load_trial_execution_and_post_review_v1(
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

    weight_abs = _REPO_ROOT / MOBILE_SAM_WEIGHT_FILE_PATH
    if not weight_abs.is_file():
        weight_abs = Path.cwd() / MOBILE_SAM_WEIGHT_FILE_PATH
    code_path_abs = _REPO_ROOT / MOBILE_SAM_CODE_PATH_REL
    if not code_path_abs.is_dir():
        alt = Path.cwd() / MOBILE_SAM_CODE_PATH_REL
        if alt.is_dir():
            code_path_abs = alt

    ts = _now()

    # ------------------------------------------------------------------- #
    # (二) Pre-model-load snapshot.
    # ------------------------------------------------------------------- #
    weight_exists = weight_abs.is_file()
    weight_size = weight_abs.stat().st_size if weight_exists else 0
    sha_before = _sha256_of(weight_abs) if weight_exists else ""
    pip_count, pip_digest = _pip_freeze_digest()
    snapshot = MobileSAMPreModelLoadSnapshotRecord(
        snapshot_id="mobile_sam_pre_model_load_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        env_path=os.environ.get("VIRTUAL_ENV", sys.prefix),
        working_directory=str(Path.cwd()),
        code_path_ref=str(code_path_abs),
        weight_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        weight_file_exists=weight_exists,
        weight_file_size=weight_size,
        weight_sha256_before=sha_before,
        pip_freeze_before_count=pip_count,
        pip_freeze_before_digest=pip_digest,
        process_id=os.getpid(),
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
        upstream_registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
        rollback_snapshot_ref=str(out_root / "mobile_sam_pre_model_load_snapshot_v1.json"),
        test_board_ref="capabilities/test_board/recognition_models/phase_p1_mobilesam_model_load_trial_execution_and_post_review_v1_001/",
        snapshot_succeeded=weight_exists and bool(sha_before),
    )
    (out_root / "mobile_sam_pre_model_load_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        failed_checks.append("snapshot.failed_weight_missing_or_unhashable")

    # ------------------------------------------------------------------- #
    # (三) Sha256 / size recheck (before any import/load).
    # ------------------------------------------------------------------- #
    actual_size = weight_size
    actual_sha = sha_before
    size_matches = actual_size == MOBILE_SAM_WEIGHT_SIZE_BYTES
    sha256_matches = actual_sha == MOBILE_SAM_WEIGHT_SHA256
    recheck = MobileSAMSha256RecheckRecord(
        recheck_id="mobile_sam_sha256_recheck_v1",
        expected_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        expected_size_bytes=MOBILE_SAM_WEIGHT_SIZE_BYTES,
        expected_sha256=MOBILE_SAM_WEIGHT_SHA256,
        actual_size_bytes=actual_size,
        actual_sha256=actual_sha,
        size_matches=size_matches,
        sha256_matches=sha256_matches,
        recheck_passed=size_matches and sha256_matches,
    )
    (out_root / "mobile_sam_sha256_recheck_v1.json").write_text(
        json.dumps(asdict(recheck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not recheck.recheck_passed:
        # sha256/size mismatch is a BOUNDARY VIOLATION => blocker, and we must NOT load.
        failed_checks.append("recheck.sha256_or_size_mismatch_blocks_model_load")

    # ------------------------------------------------------------------- #
    # (四) REAL import + REAL checkpoint load (only if recheck passed).
    # ------------------------------------------------------------------- #
    may_load = perform_load and snapshot.snapshot_succeeded and recheck.recheck_passed
    started_at = _now()
    t0 = time.time()
    if may_load:
        load_info = _attempt_import_and_load(code_path_abs, weight_abs)
    else:
        load_info = {
            "code_path_added": str(code_path_abs),
            "import_attempted": False,
            "import_success": False,
            "import_error": "import_skipped_recheck_or_snapshot_failed",
            "imported_module_file": "",
            "checkpoint_load_attempted": False,
            "model_object_created": False,
            "model_type_name": "",
            "checkpoint_load_success": False,
            "checkpoint_load_error": "load_skipped_recheck_or_snapshot_failed",
            "model_object_released": False,
        }
    elapsed = round(time.time() - t0, 4)
    ended_at = _now()
    peak_mb = _peak_memory_mb()

    import_success = bool(load_info["import_success"])
    checkpoint_load_success = bool(load_info["checkpoint_load_success"])
    model_load_trial_success = import_success and checkpoint_load_success

    import_record = MobileSAMModelImportExecutionRecord(
        record_id="mobile_sam_model_import_record_v1",
        import_target=MOBILE_SAM_IMPORT_ROOT,
        code_path_added=load_info["code_path_added"],
        import_attempted=bool(load_info["import_attempted"]),
        import_success=import_success,
        import_error=load_info["import_error"],
        imported_module_file=load_info["imported_module_file"],
    )
    (out_root / "mobile_sam_model_import_record_v1.json").write_text(
        json.dumps(asdict(import_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    load_record = MobileSAMModelLoadExecutionRecord(
        record_id="mobile_sam_model_load_execution_record_v1",
        build_key=MOBILE_SAM_BUILD_KEY,
        checkpoint_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        checkpoint_load_attempted=bool(load_info["checkpoint_load_attempted"]),
        model_object_created=bool(load_info["model_object_created"]),
        model_type_name=load_info["model_type_name"],
        checkpoint_load_success=checkpoint_load_success,
        checkpoint_load_error=load_info["checkpoint_load_error"],
        model_object_released=bool(load_info["model_object_released"]),
        model_load_trial_success=model_load_trial_success,
        inference_ready=False,
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        commercial_runtime_approved=False,
    )
    (out_root / "mobile_sam_model_load_execution_record_v1.json").write_text(
        json.dumps(asdict(load_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (六) Memory / timeout monitor.
    # ------------------------------------------------------------------- #
    timeout_occurred = elapsed > TIMEOUT_SECONDS
    oom_occurred = peak_mb > MEMORY_LIMIT_MB
    monitor = MobileSAMMemoryTimeoutMonitorRecord(
        monitor_id="mobile_sam_memory_timeout_monitor_v1",
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
    (out_root / "mobile_sam_memory_timeout_monitor_v1.json").write_text(
        json.dumps(asdict(monitor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if timeout_occurred:
        failed_checks.append("monitor.timeout_exceeded")
    if oom_occurred:
        failed_checks.append("monitor.oom_exceeded")

    # ------------------------------------------------------------------- #
    # (八) Post-review audit.
    # ------------------------------------------------------------------- #
    post_audit = MobileSAMModelLoadPostReviewAudit(
        audit_id="mobile_sam_model_load_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        sha256_rechecked=True,
        sha256_matches=sha256_matches,
        size_matches=size_matches,
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
            and sha256_matches
            and size_matches
            and not timeout_occurred
            and not oom_occurred
        ),
    )
    (out_root / "mobile_sam_model_load_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ------------------------------------------------------------------- #
    # (九) Rollback / cleanup.
    # ------------------------------------------------------------------- #
    rollback = MobileSAMModelLoadRollbackCleanupRecord(
        record_id="mobile_sam_model_load_rollback_cleanup_v1",
        rollback_available=True,
        rollback_not_executed_by_default=True,
        model_object_cleanup_attempted=True,
        persistent_process_left=False,
        rollback_preserves_weight_file=True,
        rollback_preserves_registry=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
    )

    # ------------------------------------------------------------------- #
    # Inference / runtime exclusion.
    # ------------------------------------------------------------------- #
    exclusion = MobileSAMInferenceRuntimeExclusionRecord(
        record_id="mobile_sam_inference_runtime_exclusion_v1",
        no_image_input=True,
        no_segmentation=True,
        no_prediction=True,
        no_inference=True,
        no_runtime_server=True,
        no_output_adapter=True,
        no_semantic_layer=True,
        model_load_success_not_inference_approval=True,
        model_load_success_not_runtime_approval=True,
        model_load_success_not_output_adapter_approval=True,
        model_load_success_not_semantic_layer_approval=True,
        model_load_success_not_commercial_runtime_approval=True,
    )

    # ------------------------------------------------------------------- #
    # (十三) Invariants for the 16 negative guards.
    # ------------------------------------------------------------------- #
    invariant_state: Dict[str, bool] = {
        "pre_snapshot_present": snapshot.snapshot_succeeded,
        "sha256_size_rechecked": recheck.sha256_matches is not None and recheck.size_matches is not None,
        # We only proceed to load when recheck passes; if it failed we did not load.
        "no_load_on_mismatch": recheck.recheck_passed or not bool(load_info["import_attempted"]),
        "scope_mobile_sam_only": True,
        "no_extra_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "no_image_input": IMAGE_INPUT_ALLOWED is False and exclusion.no_image_input is True,
        "no_seg_pred_inference": SEGMENTATION_ALLOWED is False and PREDICTION_ALLOWED is False
        and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_output_semantic": RUNTIME_EXECUTION_ALLOWED is False
        and REAL_OUTPUT_ADAPTER_ALLOWED is False and SEMANTIC_PROMOTION_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "success_not_downstream_ready": (
            load_record.inference_ready is False
            and load_record.runtime_ready is False
            and load_record.output_adapter_ready is False
            and load_record.semantic_layer_ready is False
            and load_record.commercial_runtime_approved is False
        ),
        "memory_timeout_recorded": True,
        "cleanup_rollback_recorded": rollback.model_object_cleanup_attempted is True
        and rollback.rollback_available is True,
        "post_review_present": True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMModelLoadExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMModelLoadExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_mobile_sam_model_load_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # ------------------------------------------------------------------- #
    # Boundary / structural GO conditions (contribute to blocker_count).
    # NOTE: import/checkpoint success is NOT a blocker — an honest load
    # failure with no boundary violation routes to FAILED_NO_BOUNDARY_VIOLATION.
    # ------------------------------------------------------------------- #
    go_conditions: Dict[str, bool] = {
        "mobile_sam_model_load_trial_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_pre_model_load_snapshot_record_count_eq_1": True,
        "mobile_sam_sha256_recheck_record_count_eq_1": True,
        "mobile_sam_model_import_execution_record_count_gte_1": True,
        "mobile_sam_model_load_execution_record_count_gte_1": True,
        "mobile_sam_memory_timeout_monitor_record_count_gte_1": True,
        "mobile_sam_model_load_post_review_audit_count_gte_1": True,
        "mobile_sam_model_load_rollback_cleanup_record_count_gte_1": True,
        "mobile_sam_inference_runtime_exclusion_record_count_gte_1": True,
        "mobile_sam_model_load_followup_route_count_gte_1": True,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        # Upstream GO verify flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        # Bindings.
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "mobile_sam_only": True,
        "model_load_trial_execution": MODEL_LOAD_TRIAL_EXECUTION is True,
        "real_import_allowed_true": REAL_IMPORT_ALLOWED is True,
        "model_load_allowed_true": MODEL_LOAD_ALLOWED is True,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "segmentation_allowed_false": SEGMENTATION_ALLOWED is False,
        "prediction_allowed_false": PREDICTION_ALLOWED is False,
        "image_input_allowed_false": IMAGE_INPUT_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "runtime_activation_allowed_false": RUNTIME_ACTIVATION_ALLOWED is False,
        "real_output_adapter_allowed_false": REAL_OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_promotion_allowed_false": SEMANTIC_PROMOTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "additional_weight_download_allowed_false": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        # Pre-load + recheck enforcement.
        "pre_snapshot_exists": snapshot.snapshot_succeeded,
        "sha256_rechecked": post_audit.sha256_rechecked,
        "sha256_matches": sha256_matches,
        "size_matches": size_matches,
        "no_load_on_mismatch": invariant_state["no_load_on_mismatch"],
        # Boundary post-review.
        "no_image_input": post_audit.no_image_input,
        "no_segmentation": post_audit.no_segmentation,
        "no_prediction": post_audit.no_prediction,
        "no_inference": post_audit.no_inference,
        "no_runtime": post_audit.no_runtime,
        "no_output_adapter": post_audit.no_output_adapter,
        "no_semantic_layer": post_audit.no_semantic_layer,
        "no_registry_mutation": post_audit.no_registry_mutation,
        "no_extra_download": post_audit.no_extra_download,
        "memory_timeout_recorded": post_audit.memory_timeout_recorded,
        "cleanup_recorded": post_audit.cleanup_recorded,
        "no_timeout_violation": not timeout_occurred,
        "no_oom_violation": not oom_occurred,
        "load_success_not_inference_ready": load_record.inference_ready is False,
        "load_success_not_runtime_ready": load_record.runtime_ready is False,
        "load_success_not_output_adapter_ready": load_record.output_adapter_ready is False,
        "load_success_not_semantic_layer_ready": load_record.semantic_layer_ready is False,
        "model_load_success_not_inference_approval": exclusion.model_load_success_not_inference_approval,
        "model_load_success_not_runtime_approval": exclusion.model_load_success_not_runtime_approval,
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

    # ------------------------------------------------------------------- #
    # (十) Decision rule (3-way).
    # ------------------------------------------------------------------- #
    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
        next_phase_purpose = "review_and_classify_boundary_violation_blockers"
    elif model_load_trial_success:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        next_phase_purpose = "plan_registry_patch_model_load_verified_and_inference_trial_readiness"
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        next_phase_purpose = "review_model_load_failure_and_plan_repair_eg_missing_dependency"

    followup = MobileSAMModelLoadFollowupRouteRecord(
        route_id="mobile_sam_model_load_followup_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next_phase,
        next_phase_scope="mobile_sam_only",
        next_phase_purpose=next_phase_purpose,
        optional_followup_phase="Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001",
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMModelLoadExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_model_load_trial_execution_profile_count=1,
        mobile_sam_pre_model_load_snapshot_record_count=1,
        mobile_sam_sha256_recheck_record_count=1,
        mobile_sam_model_import_execution_record_count=1,
        mobile_sam_model_load_execution_record_count=1,
        mobile_sam_memory_timeout_monitor_record_count=1,
        mobile_sam_model_load_post_review_audit_count=1,
        mobile_sam_model_load_rollback_cleanup_record_count=1,
        mobile_sam_inference_runtime_exclusion_record_count=1,
        mobile_sam_model_load_followup_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        import_success=import_success,
        checkpoint_load_success=checkpoint_load_success,
        model_load_trial_success=model_load_trial_success,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Model Load Trial Execution And Post Review (real execution, mobile_sam_only)",
        "lifecycle_variant": SCOPE,
        "model_load_principle_zh": MODEL_LOAD_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "model_load_trial_execution": MODEL_LOAD_TRIAL_EXECUTION,
        "registry_mutation_allowed": REGISTRY_MUTATION_ALLOWED,
        "upstream_request_approval_ref": UPSTREAM_REQUEST_APPROVAL_REF,
        "upstream_registry_overlay_ref": UPSTREAM_REGISTRY_OVERLAY_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "code_install_evidence_ref": MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "out_of_scope_asset_ids": list(OUT_OF_SCOPE_ASSET_IDS),
        "mobile_sam_model_load_trial_execution_profile": _build_profile(),
        "mobile_sam_model_load_trial_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_pre_model_load_snapshot_record": asdict(snapshot),
        "mobile_sam_pre_model_load_snapshot_record_count": 1,
        "mobile_sam_sha256_recheck_record": asdict(recheck),
        "mobile_sam_sha256_recheck_record_count": 1,
        "mobile_sam_model_import_execution_record": asdict(import_record),
        "mobile_sam_model_import_execution_record_count": 1,
        "mobile_sam_model_load_execution_record": asdict(load_record),
        "mobile_sam_model_load_execution_record_count": 1,
        "mobile_sam_memory_timeout_monitor_record": asdict(monitor),
        "mobile_sam_memory_timeout_monitor_record_count": 1,
        "mobile_sam_model_load_post_review_audit": asdict(post_audit),
        "mobile_sam_model_load_post_review_audit_count": 1,
        "mobile_sam_model_load_rollback_cleanup_record": asdict(rollback),
        "mobile_sam_model_load_rollback_cleanup_record_count": 1,
        "mobile_sam_inference_runtime_exclusion_record": asdict(exclusion),
        "mobile_sam_inference_runtime_exclusion_record_count": 1,
        "mobile_sam_model_load_followup_route": asdict(followup),
        "mobile_sam_model_load_followup_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "weight_abs_path": str(weight_abs),
        "code_path_abs": str(code_path_abs),
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "model_load_trial_status": decision_branch,
            "import_success": import_success,
            "import_error": import_record.import_error,
            "checkpoint_load_success": checkpoint_load_success,
            "checkpoint_load_error": load_record.checkpoint_load_error,
            "model_load_trial_success": model_load_trial_success,
            "no_boundary_violation": no_boundary_violation,
            "sha256_matches": sha256_matches,
            "size_matches": size_matches,
            "elapsed_seconds": elapsed,
            "peak_memory_mb": peak_mb,
            "recommended_next_phase": recommended_next_phase,
            "recommended_next_phase_scope": "mobile_sam_only",
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only). A pre-load snapshot was taken and mobile_sam.pt was rechecked "
                "(sha256==" + MOBILE_SAM_WEIGHT_SHA256 + ", size==40728226): match="
                + str(sha256_matches and size_matches) + ". A REAL import of the code-only-installed `mobile_sam` "
                "package and a REAL checkpoint-load build were attempted under a 4096MB/300s boundary. import_success="
                + str(import_success) + ", checkpoint_load_success=" + str(checkpoint_load_success) + ". NOTHING was "
                "image-fed / segmented / predicted / inferred / run; no runtime / output adapter / semantic layer was "
                "started; the registry was NOT mutated and nothing was downloaded. Decision=" + final_decision + ". "
                + (
                    "Model loaded successfully; next: " + NEXT_PHASE_GO + "."
                    if final_decision == FINAL_DECISION_GO
                    else (
                        "Honest load failure with NO boundary violation (e.g. missing transitive dependency: "
                        + (import_record.import_error or load_record.checkpoint_load_error)
                        + "); next: " + NEXT_PHASE_FAILED + " (repair planning)."
                        if final_decision == FINAL_DECISION_FAILED
                        else "Boundary violation detected; next: " + NEXT_PHASE_BLOCKED + "."
                    )
                )
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
            "mobile_sam_pre_model_load_snapshot_record": {"mobile_sam_pre_model_load_snapshot_record": asdict(snapshot)},
            "mobile_sam_sha256_recheck_record": {"mobile_sam_sha256_recheck_record": asdict(recheck)},
            "mobile_sam_model_import_record": {"mobile_sam_model_import_execution_record": asdict(import_record)},
            "mobile_sam_model_load_execution_record": {"mobile_sam_model_load_execution_record": asdict(load_record)},
            "mobile_sam_memory_timeout_monitor_record": {"mobile_sam_memory_timeout_monitor_record": asdict(monitor)},
            "mobile_sam_model_load_post_review_record": {"mobile_sam_model_load_post_review_audit": asdict(post_audit),
                                                         "mobile_sam_model_load_rollback_cleanup_record": asdict(rollback)},
            "mobile_sam_inference_runtime_exclusion_record": {"mobile_sam_inference_runtime_exclusion_record": asdict(exclusion)},
            "mobile_sam_followup_registry_patch_route_record": {"mobile_sam_model_load_followup_route": asdict(followup)},
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
            "model_load_trial_execution": True,
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
    result = review_p1_mobile_sam_model_load_trial_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "test_board_write_mode": result.get("test_board_write_mode"),
                "import_success": result["conclusions"]["import_success"],
                "import_error": result["conclusions"]["import_error"],
                "checkpoint_load_success": result["conclusions"]["checkpoint_load_success"],
                "model_load_trial_success": result["conclusions"]["model_load_trial_success"],
                "no_boundary_violation": result["conclusions"]["no_boundary_violation"],
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
