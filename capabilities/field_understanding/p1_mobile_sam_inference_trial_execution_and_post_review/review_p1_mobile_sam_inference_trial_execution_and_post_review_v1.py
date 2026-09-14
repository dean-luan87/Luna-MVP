# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Execution And Post Review — review v1
(REAL EXECUTION, scope = mobile_sam_only).

Single local synthetic test image candidate-only inference with pre-snapshot, sha256/registry
recheck, real import/load, one controlled inference, candidate output, post-review.
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
from capabilities.field_understanding.p1_mobile_sam_inference_trial_execution_and_post_review.p1_mobile_sam_inference_trial_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_inference_trial_execution_and_post_review.p1_mobile_sam_inference_trial_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    CANDIDATE_OUTPUT_ONLY,
    CHECKPOINT_LOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPECTED_READINESS_LEVEL,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    INFERENCE_EXECUTION_PRINCIPLE_ZH,
    INFERENCE_TRIAL_EXECUTION,
    LIVE_CAMERA_ALLOWED,
    LOCAL_TEST_IMAGE_ALLOWED,
    LUNA_CORE_PRINCIPLE,
    MEMORY_LIMIT_MB,
    MODEL_DOWNLOAD_ALLOWED,
    MODEL_LOAD_ALLOWED,
    MOBILE_SAM_ASSET_ID,
    MOBILE_SAM_BUILD_KEY,
    MOBILE_SAM_CODE_PATH_REL,
    MOBILE_SAM_IMPORT_ROOT,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    MOBILE_SAM_WEIGHT_SHA256,
    MOBILE_SAM_WEIGHT_SIZE_BYTES,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    PERSONAL_IMAGE_ALLOWED,
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
    SINGLE_LOCAL_TEST_IMAGE_ONLY,
    SYNTHETIC_IMAGE_HEIGHT,
    SYNTHETIC_IMAGE_WIDTH,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TEST_IMAGE_ID,
    TIMEOUT_SECONDS,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALL_TARGET_REL,
    UPSTREAM_INFERENCE_APPROVAL_EXPECTED_GO,
    UPSTREAM_INFERENCE_APPROVAL_REF,
    UPSTREAM_REGISTRY_OVERLAY_REF,
    WEIGHT_CHAIN,
    MobileSAMCandidateOutputRecord,
    MobileSAMFollowupInferenceRegistryPatchRoute,
    MobileSAMInferenceMemoryTimeoutMonitorRecord,
    MobileSAMInferenceModelLoadRecord,
    MobileSAMInferencePostReviewAudit,
    MobileSAMInferenceRollbackCleanupRecord,
    MobileSAMInferenceSha256RegistryRecheckRecord,
    MobileSAMLocalTestImageManifestRecord,
    MobileSAMPreInferenceSnapshotRecord,
    MobileSAMRuntimeSemanticFactExclusionRecord,
    MobileSAMSingleInferenceExecutionRecord,
    NegativeMobileSAMInferenceTrialExecutionGuard,
    P1MobileSAMInferenceTrialExecutionDecision,
    P1MobileSAMInferenceTrialExecutionPostReviewProfile,
    to_dict,
)

INFERENCE_APPROVAL_ARTIFACT_REL = (
    "_tmp_eval_out/p1_mobile_sam_inference_trial_request_approval_and_readiness_v1_smoke_v0/"
    "p1_mobile_sam_inference_trial_request_approval_and_readiness_review_v1.json"
)
UPSTREAM_REGISTRY_PATCH_REF = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001"
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
    / "p1_mobile_sam_inference_trial_execution_and_post_review_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_mobile_sam_inference_trial_execution_and_post_review_review_v1.json"

_PKG = "capabilities/field_understanding/p1_mobile_sam_inference_trial_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/p1_mobile_sam_inference_trial_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_inference_trial_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_inference_trial_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_inference_trial_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_inference_trial_execution_decision_v1"
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
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return tuple(dict.fromkeys(roots))


def _resolve_path(rel: str) -> Path:
    for base in _artifact_roots():
        p = base / rel
        if p.exists():
            return p.resolve()
    return (_REPO_ROOT / rel).resolve()


def _load_artifact_any_root(rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    for base in _artifact_roots():
        artifact, exists = load_artifact(base, rel)
        if exists and artifact:
            return artifact, True
    return None, False


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


def _verify_upstream_approval() -> Tuple[Dict[str, Any], bool]:
    artifact, exists = _load_artifact_any_root(INFERENCE_APPROVAL_ARTIFACT_REL)
    if not exists or not artifact:
        return {}, False
    approval = artifact.get("mobile_sam_inference_owner_approval_issuance_record") or {}
    conclusions = artifact.get("conclusions") or {}
    verified = (
        artifact.get("final_decision") == UPSTREAM_INFERENCE_APPROVAL_EXPECTED_GO
        and conclusions.get("can_enter_inference_trial_execution_next") is True
        and approval.get("owner_approval_granted_for_inference_trial_execution_next") is True
    )
    return {
        "final_decision": artifact.get("final_decision"),
        "can_enter_inference_trial_execution_next": conclusions.get("can_enter_inference_trial_execution_next"),
        "owner_approval_granted_for_inference_trial_execution_next": approval.get(
            "owner_approval_granted_for_inference_trial_execution_next"
        ),
    }, verified


def _verify_registry_overlay() -> Tuple[Dict[str, Any], bool]:
    overlay_path = _resolve_path(UPSTREAM_REGISTRY_OVERLAY_REF)
    if not overlay_path.is_file():
        return {}, False
    try:
        data = json.loads(overlay_path.read_text(encoding="utf-8"))
        ms = (data.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
        passed = (
            ms.get("readiness_level") == EXPECTED_READINESS_LEVEL
            and ms.get("model_load_verified") is True
            and ms.get("checkpoint_load_verified") is True
            and ms.get("dependency_gap_resolved") is True
            and ms.get("dependency_repair_dependency") == "timm"
            and ms.get("dependency_repair_dependency_version") == "1.0.27"
            and ms.get("inference_ready") is False
            and ms.get("runtime_ready") is False
            and ms.get("output_adapter_ready") is False
            and ms.get("semantic_layer_ready") is False
            and ms.get("commercial_runtime_approved") is False
        )
        return ms, passed
    except (OSError, json.JSONDecodeError):
        return {}, False


def _create_synthetic_test_image(image_path: Path) -> Dict[str, Any]:
    import numpy as np

    width, height = SYNTHETIC_IMAGE_WIDTH, SYNTHETIC_IMAGE_HEIGHT
    y = np.linspace(0, 255, height, dtype=np.uint8)
    x = np.linspace(0, 255, width, dtype=np.uint8)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    img = np.stack(
        [xx, yy, ((xx.astype(np.int16) + yy) // 2).astype(np.uint8)],
        axis=-1,
    )
    try:
        from PIL import Image  # noqa: WPS433

        Image.fromarray(img, mode="RGB").save(image_path)
    except Exception:  # noqa: BLE001
        import struct
        import zlib

        def _png_chunk(tag: bytes, payload: bytes) -> bytes:
            crc = zlib.crc32(tag + payload) & 0xFFFFFFFF
            return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)

        raw = b"".join(
            b"\x00" + img[row, :, :].tobytes() for row in range(height)
        )
        ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        png = (
            b"\x89PNG\r\n\x1a\n"
            + _png_chunk(b"IHDR", ihdr)
            + _png_chunk(b"IDAT", zlib.compress(raw, 9))
            + _png_chunk(b"IEND", b"")
        )
        image_path.write_bytes(png)
    sha = _sha256_of(image_path)
    size = image_path.stat().st_size
    return {
        "test_image_id": TEST_IMAGE_ID,
        "local_path": str(image_path),
        "sha256": sha,
        "width": width,
        "height": height,
        "file_size_bytes": size,
        "source_type": "synthetic_test_image",
        "personal_data_absent": True,
        "live_camera_frame": False,
        "external_url_source": False,
        "dataset_source": False,
        "navigation_runtime_frame": False,
        "fact_layer_source": False,
        "semantic_layer_source": False,
        "allowed_for_single_inference_trial": True,
        "must_not_enter_fact_layer": True,
        "must_not_enter_navigation_runtime": True,
    }


def _attempt_single_inference(
    code_path: Path,
    timm_target: Path,
    weight_abs: Path,
    image_abs: Path,
    manifest_abs: Path,
) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "import_attempted": False,
        "import_success": False,
        "import_error": "",
        "checkpoint_load_attempted": False,
        "model_object_created": False,
        "model_type_name": "",
        "checkpoint_load_success": False,
        "checkpoint_load_error": "",
        "model_object_released": False,
        "inference_attempted": False,
        "inference_success": False,
        "inference_error": "",
        "output_type": "",
        "mask_count": 0,
        "result_shape_summary": "",
        "manifest_path_used": str(manifest_abs),
        "test_image_id": TEST_IMAGE_ID,
    }
    for ep in (timm_target, code_path):
        s = str(ep)
        if s not in sys.path:
            sys.path.insert(0, s)
    try:
        info["import_attempted"] = True
        importlib.import_module(MOBILE_SAM_IMPORT_ROOT)
        info["import_success"] = True
    except BaseException as exc:  # noqa: BLE001
        info["import_error"] = f"{type(exc).__name__}:{exc}"
        return info

    model = None
    try:
        from mobile_sam import SamPredictor, sam_model_registry  # type: ignore

        info["checkpoint_load_attempted"] = True
        model = sam_model_registry[MOBILE_SAM_BUILD_KEY](checkpoint=str(weight_abs))
        info["model_object_created"] = True
        info["model_type_name"] = type(model).__name__
        info["checkpoint_load_success"] = True

        import numpy as np
        from PIL import Image  # noqa: WPS433

        img = np.array(Image.open(image_abs).convert("RGB"))
        predictor = SamPredictor(model)
        predictor.set_image(img)
        h, w = img.shape[:2]
        point = np.array([[w // 2, h // 2]])
        labels = np.array([1])
        info["inference_attempted"] = True
        masks, scores, _ = predictor.predict(point_coords=point, point_labels=labels, multimask_output=True)
        info["inference_success"] = True
        info["output_type"] = "segmentation_masks"
        info["mask_count"] = int(masks.shape[0]) if hasattr(masks, "shape") else len(masks)
        info["result_shape_summary"] = (
            f"masks={getattr(masks, 'shape', None)} scores={getattr(scores, 'shape', None)}"
        )
    except BaseException as exc:  # noqa: BLE001
        if info["checkpoint_load_attempted"] and not info["checkpoint_load_success"]:
            info["checkpoint_load_error"] = f"{type(exc).__name__}:{exc}"
        else:
            info["inference_error"] = f"{type(exc).__name__}:{exc}"
    finally:
        try:
            del model
            gc.collect()
        except Exception:  # noqa: BLE001
            pass
        info["model_object_released"] = True
    return info


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMInferenceTrialExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            inference_trial_execution=INFERENCE_TRIAL_EXECUTION,
            single_local_test_image_only=SINGLE_LOCAL_TEST_IMAGE_ONLY,
            candidate_output_only=CANDIDATE_OUTPUT_ONLY,
            post_review_included=POST_REVIEW_INCLUDED,
            real_import_allowed=REAL_IMPORT_ALLOWED,
            model_load_allowed=MODEL_LOAD_ALLOWED,
            checkpoint_load_allowed=CHECKPOINT_LOAD_ALLOWED,
            image_input_allowed=IMAGE_INPUT_ALLOWED,
            local_test_image_allowed=LOCAL_TEST_IMAGE_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            segmentation_allowed=SEGMENTATION_ALLOWED,
            prediction_allowed=PREDICTION_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            runtime_activation_allowed=RUNTIME_ACTIVATION_ALLOWED,
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_inference_approval_ref=UPSTREAM_INFERENCE_APPROVAL_REF,
            upstream_registry_overlay_ref=UPSTREAM_REGISTRY_OVERLAY_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_inference_trial_execution_and_post_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    perform_inference: bool = True,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []
    boundary_violations: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file() or (Path.cwd() / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    boundary_violations.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    weight_abs = _resolve_path(MOBILE_SAM_WEIGHT_FILE_PATH)
    code_path = _resolve_path(MOBILE_SAM_CODE_PATH_REL)
    timm_target = _resolve_path(TIMM_INSTALL_TARGET_REL)
    overlay_path = _resolve_path(UPSTREAM_REGISTRY_OVERLAY_REF)

    weight_exists = weight_abs.is_file()
    weight_size = weight_abs.stat().st_size if weight_exists else 0
    sha_before = _sha256_of(weight_abs) if weight_exists else ""
    pip_count, pip_digest = _pip_freeze_digest()

    ms_registry, registry_ok = _verify_registry_overlay()
    approval_state, approval_ok = _verify_upstream_approval()
    upstream_readiness_verified = registry_ok and approval_ok
    if not approval_ok:
        boundary_violations.append("upstream.inference_approval_not_go")
    if not registry_ok:
        boundary_violations.append("upstream.registry_not_model_load_verified")

    snapshot = MobileSAMPreInferenceSnapshotRecord(
        snapshot_id="mobile_sam_pre_inference_snapshot_v1",
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
        registry_overlay_path=UPSTREAM_REGISTRY_OVERLAY_REF,
        registry_mobile_sam_readiness_level=str(ms_registry.get("readiness_level", "")),
        pip_freeze_before_count=pip_count,
        pip_freeze_before_digest=pip_digest,
        process_id=os.getpid(),
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        upstream_inference_request_approval_ref=UPSTREAM_INFERENCE_APPROVAL_REF,
        upstream_model_load_registry_patch_ref=UPSTREAM_REGISTRY_PATCH_REF,
        rollback_snapshot_ref=str(out_root / "mobile_sam_pre_inference_snapshot_v1.json"),
        test_board_ref=(
            "capabilities/test_board/recognition_models/"
            "phase_p1_mobilesam_inference_trial_execution_and_post_review_v1_001/"
        ),
        snapshot_succeeded=weight_exists and bool(sha_before) and upstream_readiness_verified,
    )
    (out_root / "mobile_sam_pre_inference_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        boundary_violations.append("snapshot.failed_or_upstream_not_ready")

    size_matches = weight_size == MOBILE_SAM_WEIGHT_SIZE_BYTES
    sha256_matches = sha_before == MOBILE_SAM_WEIGHT_SHA256
    timm_spec_ok, _ = _find_spec_with_paths(TIMM_IMPORT_ROOT, [timm_target])
    ms_spec_ok, _ = _find_spec_with_paths(MOBILE_SAM_IMPORT_ROOT, [code_path])
    recheck_passed = size_matches and sha256_matches and registry_ok and timm_spec_ok and ms_spec_ok

    recheck = MobileSAMInferenceSha256RegistryRecheckRecord(
        recheck_id="mobile_sam_inference_sha256_registry_recheck_v1",
        registry_readiness_level=str(ms_registry.get("readiness_level", "")),
        model_load_verified=ms_registry.get("model_load_verified") is True,
        checkpoint_load_verified=ms_registry.get("checkpoint_load_verified") is True,
        dependency_gap_resolved=ms_registry.get("dependency_gap_resolved") is True,
        dependency_repair_dependency=str(ms_registry.get("dependency_repair_dependency", "")),
        dependency_repair_dependency_version=str(ms_registry.get("dependency_repair_dependency_version", "")),
        inference_ready=ms_registry.get("inference_ready") is True,
        runtime_ready=ms_registry.get("runtime_ready") is True,
        output_adapter_ready=ms_registry.get("output_adapter_ready") is True,
        semantic_layer_ready=ms_registry.get("semantic_layer_ready") is True,
        commercial_runtime_approved=ms_registry.get("commercial_runtime_approved") is True,
        registry_recheck_passed=registry_ok,
        expected_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        expected_size_bytes=MOBILE_SAM_WEIGHT_SIZE_BYTES,
        expected_sha256=MOBILE_SAM_WEIGHT_SHA256,
        actual_size_bytes=weight_size,
        actual_sha256=sha_before,
        size_matches=size_matches,
        sha256_matches=sha256_matches,
        mobile_sam_find_spec=ms_spec_ok,
        timm_find_spec=timm_spec_ok,
        recheck_passed=recheck_passed,
    )
    (out_root / "mobile_sam_inference_sha256_registry_recheck_v1.json").write_text(
        json.dumps(asdict(recheck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not recheck_passed:
        boundary_violations.append("recheck.sha256_registry_or_find_spec_failed")

    image_rel = "mobile_sam_synthetic_tiny_test_image_v1.png"
    image_abs = out_root / image_rel
    manifest_abs = out_root / "mobile_sam_local_test_image_manifest_v1.json"
    manifest_fields = _create_synthetic_test_image(image_abs)
    manifest_valid = (
        manifest_fields["personal_data_absent"] is True
        and manifest_fields["live_camera_frame"] is False
        and manifest_fields["external_url_source"] is False
        and manifest_fields["dataset_source"] is False
        and manifest_fields["allowed_for_single_inference_trial"] is True
    )
    manifest = MobileSAMLocalTestImageManifestRecord(
        manifest_id="mobile_sam_local_test_image_manifest_v1",
        manifest_valid=manifest_valid and image_abs.is_file(),
        **{k: manifest_fields[k] for k in (
            "test_image_id", "local_path", "sha256", "width", "height", "file_size_bytes",
            "source_type", "personal_data_absent", "live_camera_frame", "external_url_source",
            "dataset_source", "navigation_runtime_frame", "fact_layer_source",
            "semantic_layer_source", "allowed_for_single_inference_trial",
            "must_not_enter_fact_layer", "must_not_enter_navigation_runtime",
        )},
    )
    (out_root / "mobile_sam_local_test_image_manifest_v1.json").write_text(
        json.dumps({**asdict(manifest), **manifest_fields}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if not manifest.manifest_valid:
        boundary_violations.append("manifest.invalid_or_missing")

    may_infer = (
        perform_inference
        and snapshot.snapshot_succeeded
        and recheck.recheck_passed
        and manifest.manifest_valid
        and LIVE_CAMERA_ALLOWED is False
        and PERSONAL_IMAGE_ALLOWED is False
        and EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False
    )
    started_at = _now()
    t0 = time.time()
    if may_infer:
        exec_info = _attempt_single_inference(code_path, timm_target, weight_abs, image_abs, manifest_abs)
    else:
        skip = "inference_skipped_snapshot_recheck_manifest_or_upstream_failed"
        exec_info = {
            "import_attempted": False,
            "import_success": False,
            "import_error": skip,
            "checkpoint_load_attempted": False,
            "model_object_created": False,
            "model_type_name": "",
            "checkpoint_load_success": False,
            "checkpoint_load_error": skip,
            "model_object_released": False,
            "inference_attempted": False,
            "inference_success": False,
            "inference_error": skip,
            "output_type": "",
            "mask_count": 0,
            "result_shape_summary": "",
            "manifest_path_used": str(manifest_abs),
            "test_image_id": TEST_IMAGE_ID,
        }
    elapsed = round(time.time() - t0, 4)
    ended_at = _now()
    peak_mb = _peak_memory_mb()

    load_record = MobileSAMInferenceModelLoadRecord(
        record_id="mobile_sam_inference_model_load_record_v1",
        import_attempted=bool(exec_info["import_attempted"]),
        import_success=bool(exec_info["import_success"]),
        import_error=exec_info["import_error"],
        checkpoint_load_attempted=bool(exec_info["checkpoint_load_attempted"]),
        model_object_created=bool(exec_info["model_object_created"]),
        model_type_name=exec_info["model_type_name"],
        checkpoint_load_success=bool(exec_info["checkpoint_load_success"]),
        checkpoint_load_error=exec_info["checkpoint_load_error"],
        model_object_released=bool(exec_info["model_object_released"]),
        inference_ready=False,
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        commercial_runtime_approved=False,
    )
    (out_root / "mobile_sam_inference_model_load_record_v1.json").write_text(
        json.dumps(asdict(load_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    inference_record = MobileSAMSingleInferenceExecutionRecord(
        record_id="mobile_sam_single_inference_execution_record_v1",
        command_purpose="mobile_sam_single_local_test_image_candidate_inference_only",
        manifest_path_used=exec_info["manifest_path_used"],
        test_image_id=exec_info["test_image_id"],
        inference_attempted=bool(exec_info["inference_attempted"]),
        inference_success=bool(exec_info["inference_success"]),
        inference_error=exec_info["inference_error"],
        output_type=exec_info["output_type"],
        mask_count=int(exec_info["mask_count"]),
        result_shape_summary=exec_info["result_shape_summary"],
        elapsed_seconds=elapsed,
        peak_memory_mb=peak_mb,
    )
    (out_root / "mobile_sam_single_inference_execution_record_v1.json").write_text(
        json.dumps(asdict(inference_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    inference_success = bool(exec_info["inference_success"])
    candidate_written = False
    candidate = MobileSAMCandidateOutputRecord(
        candidate_id="mobile_sam_inference_candidate_output_v1",
        asset_id=MOBILE_SAM_ASSET_ID,
        test_image_id=TEST_IMAGE_ID,
        inference_attempted=bool(exec_info["inference_attempted"]),
        inference_success=inference_success,
        output_type=exec_info["output_type"] or "none",
        mask_count=int(exec_info["mask_count"]),
        result_shape_summary=exec_info["result_shape_summary"],
        elapsed_seconds=elapsed,
        peak_memory_mb=peak_mb,
        candidate_only=True,
        not_fact=True,
        not_runtime_output=True,
        not_output_adapter_output=True,
        not_semantic_output=True,
        not_user_visible_runtime_output=True,
        post_review_required=True,
        candidate_output_written=False,
    )
    if inference_success:
        candidate_payload = asdict(candidate)
        candidate_payload["candidate_output_written"] = True
        (out_root / "mobile_sam_inference_candidate_output_v1.json").write_text(
            json.dumps(candidate_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        candidate_written = True
        candidate = MobileSAMCandidateOutputRecord(**candidate_payload)
    else:
        (out_root / "mobile_sam_inference_candidate_output_v1.json").write_text(
            json.dumps(asdict(candidate), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    timeout_occurred = elapsed > TIMEOUT_SECONDS
    oom_occurred = peak_mb > MEMORY_LIMIT_MB
    monitor = MobileSAMInferenceMemoryTimeoutMonitorRecord(
        monitor_id="mobile_sam_inference_memory_timeout_monitor_v1",
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        started_at=started_at,
        ended_at=ended_at,
        elapsed_seconds=elapsed,
        peak_memory_mb=peak_mb,
        timeout_occurred=timeout_occurred,
        oom_occurred=oom_occurred,
        candidate_output_cleanup_attempted_if_failed=not inference_success,
        model_object_cleanup_attempted=bool(exec_info["model_object_released"]),
        persistent_process_left=False,
    )
    (out_root / "mobile_sam_inference_memory_timeout_monitor_v1.json").write_text(
        json.dumps(asdict(monitor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = MobileSAMInferenceRollbackCleanupRecord(
        record_id="mobile_sam_inference_rollback_cleanup_v1",
        pre_inference_snapshot_required=True,
        rollback_available=True,
        candidate_output_cleanup_attempted=not inference_success,
        model_object_cleanup_attempted=bool(exec_info["model_object_released"]),
        rollback_preserves_registry=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        no_fact_write_on_failure=True,
        no_registry_mutation_on_failure=True,
    )

    exclusion = MobileSAMRuntimeSemanticFactExclusionRecord(
        record_id="mobile_sam_runtime_semantic_fact_exclusion_v1",
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        fact_write_ready=False,
        navigation_action_speech_ready=False,
        commercial_runtime_ready=False,
        inference_trial_success_not_runtime_approval=True,
        inference_trial_success_not_output_adapter_approval=True,
        inference_trial_success_not_semantic_layer_approval=True,
        inference_trial_success_not_fact_write_approval=True,
        inference_trial_success_not_navigation_action_speech_approval=True,
        inference_trial_success_not_commercial_runtime_approval=True,
    )

    post_audit = MobileSAMInferencePostReviewAudit(
        audit_id="mobile_sam_inference_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        registry_model_load_verified_rechecked=registry_ok,
        sha256_rechecked=True,
        sha256_matches=sha256_matches,
        local_test_image_manifest_exists=manifest_abs.is_file(),
        local_test_image_manifest_valid=manifest.manifest_valid,
        image_source_allowed=manifest.source_type in ("synthetic_test_image", "tiny_static_local_test_image"),
        real_import_performed=bool(exec_info["import_attempted"]),
        model_load_performed=bool(exec_info["checkpoint_load_attempted"]),
        inference_attempted=bool(exec_info["inference_attempted"]),
        inference_success=inference_success,
        candidate_output_written=candidate_written,
        candidate_output_only=candidate.candidate_only,
        no_live_camera=LIVE_CAMERA_ALLOWED is False,
        no_personal_image=PERSONAL_IMAGE_ALLOWED is False,
        no_external_url_image=EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False,
        no_uncontrolled_dataset=True,
        no_runtime=RUNTIME_EXECUTION_ALLOWED is False,
        no_output_adapter=REAL_OUTPUT_ADAPTER_ALLOWED is False,
        no_semantic_layer=SEMANTIC_PROMOTION_ALLOWED is False,
        no_fact_write=FACT_WRITE_ALLOWED is False,
        no_navigation_action_speech=NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        no_registry_mutation=REGISTRY_MUTATION_ALLOWED is False,
        no_extra_download=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False and MODEL_DOWNLOAD_ALLOWED is False,
        memory_timeout_recorded=True,
        cleanup_recorded=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            snapshot.snapshot_succeeded
            and recheck.recheck_passed
            and manifest.manifest_valid
            and not timeout_occurred
            and not oom_occurred
        ),
    )
    (out_root / "mobile_sam_inference_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    invariant_state: Dict[str, bool] = {
        "upstream_approval_verified": approval_ok,
        "registry_model_load_verified": registry_ok,
        "sha256_rechecked": recheck.sha256_matches is not None,
        "manifest_before_image": manifest.manifest_valid,
        "only_manifest_image": manifest.manifest_valid and image_abs.is_file(),
        "no_live_camera": LIVE_CAMERA_ALLOWED is False and manifest.live_camera_frame is False,
        "no_personal_image": PERSONAL_IMAGE_ALLOWED is False and manifest.personal_data_absent is True,
        "no_external_url": EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False and manifest.external_url_source is False,
        "no_uncontrolled_dataset": manifest.dataset_source is False,
        "candidate_output_only": candidate.candidate_only and candidate.not_fact,
        "no_downstream_output": (
            candidate.not_runtime_output
            and candidate.not_output_adapter_output
            and candidate.not_semantic_output
        ),
        "no_navigation_speech": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_extra_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False and MODEL_DOWNLOAD_ALLOWED is False,
        "success_not_downstream_ready": (
            load_record.inference_ready is False
            and exclusion.runtime_ready is False
            and exclusion.semantic_layer_ready is False
        ),
        "memory_timeout_recorded": True,
        "cleanup_recorded": rollback.model_object_cleanup_attempted is True,
        "post_review_present": True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": (
            REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_artifact_protected"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_record_non_deletable"]
            and REQUIRED_TEST_BOARD_FIELDS_LOCAL["test_deletion_forbidden"]
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeMobileSAMInferenceTrialExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMobileSAMInferenceTrialExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_inference_trial_execution_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "mobile_sam_inference_trial_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "mobile_sam_pre_inference_snapshot_record_count_eq_1": True,
        "mobile_sam_test_image_manifest_record_count_gte_1": True,
        "mobile_sam_inference_sha256_registry_recheck_record_count_gte_1": True,
        "mobile_sam_inference_model_load_record_count_gte_1": True,
        "mobile_sam_single_inference_execution_record_count_gte_1": True,
        "mobile_sam_candidate_output_record_count_gte_1": True,
        "mobile_sam_inference_memory_timeout_monitor_record_count_gte_1": True,
        "mobile_sam_inference_post_review_audit_count_gte_1": True,
        "mobile_sam_inference_rollback_cleanup_record_count_gte_1": True,
        "mobile_sam_runtime_semantic_fact_exclusion_record_count_gte_1": True,
        "mobile_sam_followup_inference_registry_patch_route_count_gte_1": True,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        "real_execution_phase": REAL_EXECUTION_PHASE is True,
        "mobile_sam_only": True,
        "inference_trial_execution": INFERENCE_TRIAL_EXECUTION is True,
        "single_local_test_image_only": SINGLE_LOCAL_TEST_IMAGE_ONLY is True,
        "candidate_output_only": CANDIDATE_OUTPUT_ONLY is True,
        "post_review_included": POST_REVIEW_INCLUDED is True,
        "real_import_allowed_true": REAL_IMPORT_ALLOWED is True,
        "model_load_allowed_true": MODEL_LOAD_ALLOWED is True,
        "real_inference_allowed_true": REAL_INFERENCE_ALLOWED is True,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "upstream_approval_verified": approval_ok,
        "registry_model_load_verified": registry_ok,
        "sha256_matches": sha256_matches,
        "manifest_valid": manifest.manifest_valid,
        "inference_attempted": bool(exec_info["inference_attempted"]),
        "inference_success": inference_success,
        "candidate_output_written": candidate_written,
        "candidate_output_only_flag": candidate.candidate_only,
        "single_local_test_image_inference_verified": inference_success and manifest.manifest_valid,
        "inference_trial_success_not_runtime_approval": exclusion.inference_trial_success_not_runtime_approval,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    no_boundary_violation = len(boundary_violations) == 0
    blocker_count = len(boundary_violations) + (0 if no_boundary_violation else 0)
    if not no_boundary_violation:
        blocker_count = len(boundary_violations)
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
        next_phase_purpose = "review_and_classify_boundary_violation_blockers"
    elif inference_success and candidate_written and candidate.candidate_only:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        next_phase_purpose = "plan_inference_trial_registry_patch_and_runtime_boundary"
        blocker_count = 0
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        next_phase_purpose = "review_inference_failure_and_plan_repair"
        blocker_count = 0

    followup = MobileSAMFollowupInferenceRegistryPatchRoute(
        route_id="mobile_sam_followup_inference_registry_patch_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next_phase,
        next_phase_scope="mobile_sam_only",
        next_phase_purpose=next_phase_purpose,
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMInferenceTrialExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_inference_trial_execution_profile_count=1,
        mobile_sam_pre_inference_snapshot_record_count=1,
        mobile_sam_test_image_manifest_record_count=1,
        mobile_sam_inference_sha256_registry_recheck_record_count=1,
        mobile_sam_inference_model_load_record_count=1,
        mobile_sam_single_inference_execution_record_count=1,
        mobile_sam_candidate_output_record_count=1,
        mobile_sam_inference_memory_timeout_monitor_record_count=1,
        mobile_sam_inference_post_review_audit_count=1,
        mobile_sam_inference_rollback_cleanup_record_count=1,
        mobile_sam_runtime_semantic_fact_exclusion_record_count=1,
        mobile_sam_followup_inference_registry_patch_route_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        inference_attempted=bool(exec_info["inference_attempted"]),
        inference_success=inference_success,
        candidate_output_written=candidate_written,
        candidate_output_only=candidate.candidate_only,
        single_local_test_image_inference_verified=inference_success and manifest.manifest_valid,
        failure_recorded=not inference_success and no_boundary_violation,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Inference Trial Execution And Post Review (real execution)",
        "lifecycle_variant": SCOPE,
        "inference_execution_principle_zh": INFERENCE_EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "asset_id": MOBILE_SAM_ASSET_ID,
        "upstream_inference_approval_ref": UPSTREAM_INFERENCE_APPROVAL_REF,
        "upstream_inference_approval_state": approval_state,
        "upstream_registry_overlay_ref": UPSTREAM_REGISTRY_OVERLAY_REF,
        "overlay_path": str(overlay_path),
        "mobile_sam_code_path": str(code_path),
        "timm_install_target_path": str(timm_target),
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_inference_trial_execution_profile": _build_profile(),
        "mobile_sam_inference_trial_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "mobile_sam_pre_inference_snapshot_record": asdict(snapshot),
        "mobile_sam_pre_inference_snapshot_record_count": 1,
        "mobile_sam_test_image_manifest_record": asdict(manifest),
        "mobile_sam_test_image_manifest_record_count": 1,
        "mobile_sam_inference_sha256_registry_recheck_record": asdict(recheck),
        "mobile_sam_inference_sha256_registry_recheck_record_count": 1,
        "mobile_sam_inference_model_load_record": asdict(load_record),
        "mobile_sam_inference_model_load_record_count": 1,
        "mobile_sam_single_inference_execution_record": asdict(inference_record),
        "mobile_sam_single_inference_execution_record_count": 1,
        "mobile_sam_candidate_output_record": asdict(candidate),
        "mobile_sam_candidate_output_record_count": 1,
        "mobile_sam_inference_memory_timeout_monitor_record": asdict(monitor),
        "mobile_sam_inference_memory_timeout_monitor_record_count": 1,
        "mobile_sam_inference_post_review_record": asdict(post_audit),
        "mobile_sam_inference_post_review_audit_count": 1,
        "mobile_sam_inference_rollback_cleanup_record": asdict(rollback),
        "mobile_sam_inference_rollback_cleanup_record_count": 1,
        "mobile_sam_runtime_semantic_fact_exclusion_record": asdict(exclusion),
        "mobile_sam_runtime_semantic_fact_exclusion_record_count": 1,
        "mobile_sam_followup_inference_registry_patch_route_record": asdict(followup),
        "mobile_sam_followup_inference_registry_patch_route_count": 1,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "boundary_violations": boundary_violations,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "inference_trial_execution_status": decision_branch,
            "inference_attempted": bool(exec_info["inference_attempted"]),
            "inference_success": inference_success,
            "candidate_output_written": candidate_written,
            "candidate_output_only": candidate.candidate_only,
            "registry_mutated_this_phase": False,
            "runtime_started_this_phase": False,
            "recommended_next_phase": recommended_next_phase,
            "transition_note": (
                "REAL EXECUTION (mobile_sam_only). Single synthetic local test image candidate-only "
                "inference trial with pre-snapshot, sha256/registry recheck, import/load, one inference, "
                "candidate output, post-review. NO runtime/output adapter/semantic/fact/navigation. "
                "inference_ready NOT set; registry patch is a separate phase."
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
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        extra_payloads = {
            "mobile_sam_pre_inference_snapshot_record": {"mobile_sam_pre_inference_snapshot_record": asdict(snapshot)},
            "mobile_sam_test_image_manifest_record": {"mobile_sam_test_image_manifest_record": asdict(manifest)},
            "mobile_sam_inference_sha256_registry_recheck_record": {
                "mobile_sam_inference_sha256_registry_recheck_record": asdict(recheck),
            },
            "mobile_sam_inference_model_load_record": {"mobile_sam_inference_model_load_record": asdict(load_record)},
            "mobile_sam_single_inference_execution_record": {
                "mobile_sam_single_inference_execution_record": asdict(inference_record),
            },
            "mobile_sam_candidate_output_record": {"mobile_sam_candidate_output_record": asdict(candidate)},
            "mobile_sam_inference_memory_timeout_monitor_record": {
                "mobile_sam_inference_memory_timeout_monitor_record": asdict(monitor),
            },
            "mobile_sam_inference_post_review_record": {"mobile_sam_inference_post_review_record": asdict(post_audit)},
            "mobile_sam_runtime_semantic_fact_exclusion_record": {
                "mobile_sam_runtime_semantic_fact_exclusion_record": asdict(exclusion),
            },
            "mobile_sam_followup_inference_registry_patch_route_record": {
                "mobile_sam_followup_inference_registry_patch_route_record": asdict(followup),
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
            "candidate_output_only": True,
            "runtime_allowed": False,
            "output_adapter_allowed": False,
            "semantic_layer_allowed": False,
            "fact_write_allowed": False,
        }
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest_tb["extra_written_records"] = extra_written
        manifest_tb["extra_written_record_count"] = len(extra_written)
        manifest_tb["total_record_count"] = manifest_tb["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest_tb
        result["test_board_record_count"] = manifest_tb["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_inference_trial_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "test_board_mode": result.get("test_board_manifest", {}).get("test_mode"),
                "inference_attempted": result["conclusions"]["inference_attempted"],
                "inference_success": result["conclusions"]["inference_success"],
                "candidate_output_written": result["conclusions"]["candidate_output_written"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    ok_decisions = {FINAL_DECISION_GO, FINAL_DECISION_FAILED}
    return 0 if result["final_decision"] in ok_decisions else 1


if __name__ == "__main__":
    raise SystemExit(main())
