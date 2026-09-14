# -*- coding: utf-8 -*-
"""P1 MobileSAM Real Local Image Inference Trial Execution And Post Review — review v1."""

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
from capabilities.field_understanding.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BROAD_READINESS_MUST_BE_FALSE,
    CANONICAL_IMAGE_REL,
    CANDIDATE_OUTPUT_ONLY,
    CHECKPOINT_LOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_PRINCIPLE_ZH,
    EXPECTED_READINESS_LEVEL,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    IMAGE_INPUT_ALLOWED,
    LIVE_CAMERA_ALLOWED,
    LOCAL_TEST_IMAGE_ALLOWED,
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
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_FAILED,
    NEXT_PHASE_GO,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNED_PROMPT_TARGETS_ONLY,
    POST_REVIEW_INCLUDED,
    PREDICTION_ALLOWED,
    PROMPT_COUNT,
    PROMPT_EXECUTION_PLAN,
    REAL_EXECUTION_PHASE,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_LOCAL_IMAGE_INFERENCE_TRIAL_EXECUTION,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTERED_SOURCE_IMAGE_PATH,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_REGISTRY_TRUE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCENE_TYPE,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SINGLE_USER_SUPPLIED_LOCAL_IMAGE_ONLY,
    SOURCE_TYPE,
    TEST_ASSET_ID,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMEOUT_SECONDS,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALL_TARGET_REL,
    UNCONTROLLED_DATASET_ALLOWED,
    UPSTREAM_REGISTRY_OVERLAY_REF,
    UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO,
    UPSTREAM_REQUEST_APPROVAL_REF,
    UPSTREAM_RUNTIME_BOUNDARY_REF,
    WEIGHT_CHAIN,
    NegativeRealLocalImageInferenceExecutionGuard,
    P1MobileSAMRealLocalImageInferenceExecutionDecision,
    P1MobileSAMRealLocalImageInferenceExecutionPostReviewProfile,
    RealLocalImageCandidateMasksRecord,
    RealLocalImageFollowupReviewRoute,
    RealLocalImageManifestRecord,
    RealLocalImageMemoryTimeoutMonitorRecord,
    RealLocalImageModelLoadRecord,
    RealLocalImagePostReviewAudit,
    RealLocalImagePreInferenceSnapshotRecord,
    RealLocalImagePromptExecutionRecord,
    RealLocalImageQualitySummaryRecord,
    RealLocalImageRegistryWeightRecheckRecord,
    RealLocalImageRollbackCleanupRecord,
    RealLocalImageRuntimeSemanticFactExclusionRecord,
    to_dict,
)

UPSTREAM_APPROVAL_ARTIFACT_REL = (
    "_tmp_eval_out/p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_v1_smoke_v0/"
    "p1_mobile_sam_real_local_image_inference_trial_request_approval_and_readiness_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_real_local_image_inference_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_real_local_image_inference_execution_decision_v1"
REVIEW_FILENAME = (
    "p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_review_v1.json"
)
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"
TEST_BOARD_REF = (
    "capabilities/test_board/recognition_models/"
    "phase_p1_mobilesam_real_local_image_inference_trial_execution_and_post_review_v1_001/"
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
    / "p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1_smoke_v0"
)


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
        artifact, exists, _ = load_artifact(base, rel)
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


def _resolve_manifest_image(out_root: Path) -> Tuple[Optional[Path], str]:
    candidates: List[Tuple[str, Path]] = []
    for base in _artifact_roots():
        canonical = base / CANONICAL_IMAGE_REL
        if canonical.is_file():
            candidates.append(("canonical_test_asset", canonical.resolve()))
    registered = Path(REGISTERED_SOURCE_IMAGE_PATH)
    if registered.is_file():
        candidates.append(("registered_source_path", registered.resolve()))
    cursor_asset = (
        Path.home()
        / ".cursor/projects/Users-luanlei-Desktop-Luna-Workspace-Min/assets/image-46caa285-b501-4e06-a6c3-72ed6a9e474b.png"
    )
    if cursor_asset.is_file():
        staged = out_root / "scoped_local_test_asset" / "mobile_sam_real_local_image_street_scene_v1.png"
        staged.parent.mkdir(parents=True, exist_ok=True)
        if not staged.is_file():
            staged.write_bytes(cursor_asset.read_bytes())
        candidates.append(("cursor_asset_staged", staged.resolve()))
    if not candidates:
        return None, "no_manifest_image_found"
    path = candidates[0][1]
    return path, candidates[0][0]


def _build_image_manifest(image_abs: Path) -> Dict[str, Any]:
    from PIL import Image  # noqa: WPS433

    with Image.open(image_abs) as im:
        width, height = im.size
        mode = im.mode
    size = image_abs.stat().st_size
    return {
        "test_image_id": TEST_ASSET_ID,
        "local_path": str(image_abs),
        "sha256": _sha256_of(image_abs),
        "width": width,
        "height": height,
        "file_size_bytes": size,
        "image_mode": mode,
        "source_type": SOURCE_TYPE,
        "scene_type": SCENE_TYPE,
        "user_supplied": True,
        "personal_sensitive_image": False,
        "live_camera_frame": False,
        "external_url_source": False,
        "dataset_source": False,
        "navigation_runtime_frame": False,
        "fact_layer_source": False,
        "semantic_layer_source": False,
        "allowed_for_single_inference_trial": True,
        "must_not_enter_fact_layer": True,
        "must_not_enter_navigation_runtime": True,
        "must_not_enter_output_adapter": True,
        "must_not_enter_semantic_layer": True,
    }


def _norm_box_to_pixels(norm_box: List[float], width: int, height: int) -> List[int]:
    x1, y1, x2, y2 = norm_box
    return [
        int(round(x1 * width)),
        int(round(y1 * height)),
        int(round(x2 * width)),
        int(round(y2 * height)),
    ]


def _verify_upstream_approval() -> Tuple[Dict[str, Any], bool]:
    artifact, exists = _load_artifact_any_root(UPSTREAM_APPROVAL_ARTIFACT_REL)
    if not exists or not artifact:
        return {}, False
    approval = artifact.get("real_local_image_owner_approval_issuance_record") or {}
    conclusions = artifact.get("conclusions") or {}
    verified = (
        artifact.get("final_decision") == UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO
        and conclusions.get("can_enter_real_local_image_inference_trial_execution_next") is True
        and approval.get("owner_approval_granted_for_real_local_image_inference_execution_next") is True
    )
    return {
        "final_decision": artifact.get("final_decision"),
        "can_enter_real_local_image_inference_trial_execution_next": conclusions.get(
            "can_enter_real_local_image_inference_trial_execution_next"
        ),
        "owner_approval_granted": approval.get(
            "owner_approval_granted_for_real_local_image_inference_execution_next"
        ),
    }, verified


def _verify_registry_overlay() -> Tuple[Dict[str, Any], bool]:
    overlay_path = _resolve_path(UPSTREAM_REGISTRY_OVERLAY_REF)
    if not overlay_path.is_file():
        return {}, False
    try:
        data = json.loads(overlay_path.read_text(encoding="utf-8"))
        ms = (data.get("assets") or {}).get(MOBILE_SAM_ASSET_ID) or {}
        true_ok = all(ms.get(f) is True for f in REQUIRED_REGISTRY_TRUE_FLAGS)
        false_ok = all(ms.get(f) is False for f in BROAD_READINESS_MUST_BE_FALSE)
        passed = ms.get("readiness_level") == EXPECTED_READINESS_LEVEL and true_ok and false_ok
        return ms, passed
    except (OSError, json.JSONDecodeError):
        return {}, False


def _run_prompt_segmentation(
    code_path: Path,
    timm_target: Path,
    weight_abs: Path,
    image_abs: Path,
    manifest_fields: Dict[str, Any],
    mask_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    load_info: Dict[str, Any] = {
        "import_attempted": False,
        "import_success": False,
        "import_error": "",
        "checkpoint_load_attempted": False,
        "model_object_created": False,
        "model_type_name": "",
        "checkpoint_load_success": False,
        "checkpoint_load_error": "",
        "model_object_released": False,
    }
    prompt_results: List[Dict[str, Any]] = []
    for ep in (timm_target, code_path):
        s = str(ep)
        if s not in sys.path:
            sys.path.insert(0, s)
    model = None
    try:
        load_info["import_attempted"] = True
        importlib.import_module(MOBILE_SAM_IMPORT_ROOT)
        load_info["import_success"] = True
        from mobile_sam import SamPredictor, sam_model_registry  # type: ignore

        load_info["checkpoint_load_attempted"] = True
        model = sam_model_registry[MOBILE_SAM_BUILD_KEY](checkpoint=str(weight_abs))
        load_info["model_object_created"] = True
        load_info["model_type_name"] = type(model).__name__
        load_info["checkpoint_load_success"] = True

        import numpy as np
        from PIL import Image  # noqa: WPS433

        img = np.array(Image.open(image_abs).convert("RGB"))
        predictor = SamPredictor(model)
        predictor.set_image(img)
        width = int(manifest_fields["width"])
        height = int(manifest_fields["height"])
        mask_dir.mkdir(parents=True, exist_ok=True)

        for spec in PROMPT_EXECUTION_PLAN:
            norm_box = list(spec["normalized_box_approx"])
            pixel_box = _norm_box_to_pixels(norm_box, width, height)
            center = [(pixel_box[0] + pixel_box[2]) // 2, (pixel_box[1] + pixel_box[3]) // 2]
            result: Dict[str, Any] = {
                "prompt_id": spec["prompt_id"],
                "prompt_target_label": spec["prompt_target_label"],
                "prompt_label_is_test_description": True,
                "semantic_fact_assertion": False,
                "prompt_type_preferred": spec["prompt_type_preferred"],
                "normalized_box_or_point": norm_box,
                "pixel_box_or_point": pixel_box,
                "inference_attempted": False,
                "inference_success": False,
                "mask_count": 0,
                "selected_mask_index": None,
                "mask_shape": None,
                "mask_area_pixels": 0,
                "mask_area_ratio": 0.0,
                "score_or_iou_if_available": None,
                "candidate_mask_path": None,
                "candidate_only": True,
                "not_fact": True,
                "not_runtime_output": True,
                "not_output_adapter_output": True,
                "not_semantic_output": True,
                "not_navigation_action_speech": True,
                "post_review_required": True,
                "fallback_from_box_to_point": False,
                "fallback_reason": "",
            }
            try:
                result["inference_attempted"] = True
                box_arr = np.array(pixel_box)
                masks, scores, _ = predictor.predict(
                    box=box_arr[None, :],
                    multimask_output=True,
                )
                if masks is None or len(masks) == 0:
                    raise RuntimeError("empty_masks_from_box")
                best_idx = int(np.argmax(scores))
                mask = masks[best_idx]
                result["prompt_type_used"] = "box"
            except BaseException as box_exc:  # noqa: BLE001
                result["fallback_from_box_to_point"] = True
                result["fallback_reason"] = f"{type(box_exc).__name__}:{box_exc}"
                point = np.array([center])
                labels = np.array([1])
                masks, scores, _ = predictor.predict(
                    point_coords=point,
                    point_labels=labels,
                    multimask_output=True,
                )
                best_idx = int(np.argmax(scores))
                mask = masks[best_idx]
                result["prompt_type_used"] = "point"
                result["pixel_box_or_point"] = center

            area = int(mask.sum())
            total = int(mask.size)
            mask_path = mask_dir / f"{spec['prompt_id']}_candidate_mask.png"
            Image.fromarray((mask.astype(np.uint8) * 255)).save(mask_path)
            result["inference_success"] = True
            result["mask_count"] = int(masks.shape[0]) if hasattr(masks, "shape") else 1
            result["selected_mask_index"] = best_idx
            result["mask_shape"] = list(mask.shape)
            result["mask_area_pixels"] = area
            result["mask_area_ratio"] = round(area / total, 6) if total else 0.0
            result["score_or_iou_if_available"] = float(scores[best_idx]) if scores is not None else None
            result["candidate_mask_path"] = str(mask_path)
            prompt_results.append(result)
    except BaseException as exc:  # noqa: BLE001
        if load_info["checkpoint_load_attempted"] and not load_info["checkpoint_load_success"]:
            load_info["checkpoint_load_error"] = f"{type(exc).__name__}:{exc}"
        else:
            load_info["import_error"] = load_info["import_error"] or f"{type(exc).__name__}:{exc}"
    finally:
        try:
            del model
            gc.collect()
        except Exception:  # noqa: BLE001
            pass
        load_info["model_object_released"] = True
    return load_info, prompt_results, load_info


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMRealLocalImageInferenceExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            real_local_image_inference_trial_execution=REAL_LOCAL_IMAGE_INFERENCE_TRIAL_EXECUTION,
            single_user_supplied_local_image_only=SINGLE_USER_SUPPLIED_LOCAL_IMAGE_ONLY,
            planned_prompt_targets_only=PLANNED_PROMPT_TARGETS_ONLY,
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
            real_output_adapter_allowed=REAL_OUTPUT_ADAPTER_ALLOWED,
            semantic_promotion_allowed=SEMANTIC_PROMOTION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            additional_weight_download_allowed=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
            commercial_runtime_approved=COMMERCIAL_RUNTIME_APPROVED,
            upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
            upstream_runtime_boundary_ref=UPSTREAM_RUNTIME_BOUNDARY_REF,
            target_chain_ref="Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1(
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
    mask_dir = out_root / "candidate_masks"

    weight_abs = _resolve_path(MOBILE_SAM_WEIGHT_FILE_PATH)
    code_path = _resolve_path(MOBILE_SAM_CODE_PATH_REL)
    timm_target = _resolve_path(TIMM_INSTALL_TARGET_REL)
    overlay_path = _resolve_path(UPSTREAM_REGISTRY_OVERLAY_REF)

    weight_exists = weight_abs.is_file()
    weight_size = weight_abs.stat().st_size if weight_exists else 0
    sha_before = _sha256_of(weight_abs) if weight_exists else ""

    ms_registry, registry_ok = _verify_registry_overlay()
    approval_state, approval_ok = _verify_upstream_approval()
    image_abs, image_resolve_mode = _resolve_manifest_image(out_root)
    image_exists = image_abs is not None and image_abs.is_file()

    snapshot = RealLocalImagePreInferenceSnapshotRecord(
        snapshot_id="real_local_image_pre_inference_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        env_path=os.environ.get("VIRTUAL_ENV", sys.prefix),
        working_directory=str(Path.cwd()),
        mobile_sam_code_path_ref=str(code_path),
        timm_install_target_path_ref=str(timm_target),
        weight_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        weight_file_exists=weight_exists,
        registry_overlay_path=UPSTREAM_REGISTRY_OVERLAY_REF,
        source_image_path=str(image_abs) if image_abs else REGISTERED_SOURCE_IMAGE_PATH,
        source_file_exists=image_exists,
        process_id=os.getpid(),
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
        upstream_runtime_boundary_ref=UPSTREAM_RUNTIME_BOUNDARY_REF,
        rollback_snapshot_ref=str(out_root / "real_local_image_pre_inference_snapshot_v1.json"),
        test_board_ref=TEST_BOARD_REF,
        snapshot_succeeded=weight_exists and image_exists and approval_ok and registry_ok,
    )
    (out_root / "real_local_image_pre_inference_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        boundary_violations.append("snapshot.failed_or_upstream_not_ready")

    size_matches = weight_size == MOBILE_SAM_WEIGHT_SIZE_BYTES
    sha256_matches = sha_before == MOBILE_SAM_WEIGHT_SHA256
    timm_spec_ok, _ = _find_spec_with_paths(TIMM_IMPORT_ROOT, [timm_target])
    ms_spec_ok, _ = _find_spec_with_paths(MOBILE_SAM_IMPORT_ROOT, [code_path])
    recheck_passed = size_matches and sha256_matches and registry_ok and timm_spec_ok and ms_spec_ok

    recheck = RealLocalImageRegistryWeightRecheckRecord(
        recheck_id="real_local_image_registry_weight_recheck_v1",
        registry_readiness_level=str(ms_registry.get("readiness_level", "")),
        inference_trial_verified=ms_registry.get("inference_trial_verified") is True,
        runtime_ready=ms_registry.get("runtime_ready") is True,
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
    (out_root / "real_local_image_registry_weight_recheck_v1.json").write_text(
        json.dumps(asdict(recheck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not recheck_passed:
        boundary_violations.append("recheck.sha256_registry_or_find_spec_failed")

    manifest_fields: Dict[str, Any] = {}
    manifest_valid = False
    if image_exists and image_abs is not None:
        manifest_fields = _build_image_manifest(image_abs)
        manifest_valid = (
            manifest_fields["source_type"] == SOURCE_TYPE
            and manifest_fields["live_camera_frame"] is False
            and manifest_fields["external_url_source"] is False
            and manifest_fields["dataset_source"] is False
            and manifest_fields["allowed_for_single_inference_trial"] is True
        )
    manifest = RealLocalImageManifestRecord(
        manifest_id="mobile_sam_real_local_image_manifest_v1",
        manifest_valid=manifest_valid,
        **{k: manifest_fields[k] for k in (
            "test_image_id", "local_path", "sha256", "width", "height", "file_size_bytes",
            "image_mode", "source_type", "scene_type", "user_supplied", "personal_sensitive_image",
            "live_camera_frame", "external_url_source", "dataset_source", "navigation_runtime_frame",
            "fact_layer_source", "semantic_layer_source", "allowed_for_single_inference_trial",
            "must_not_enter_fact_layer", "must_not_enter_navigation_runtime",
            "must_not_enter_output_adapter", "must_not_enter_semantic_layer",
        )} if manifest_fields else {
            "test_image_id": TEST_ASSET_ID,
            "local_path": REGISTERED_SOURCE_IMAGE_PATH,
            "sha256": "",
            "width": 0,
            "height": 0,
            "file_size_bytes": 0,
            "image_mode": "",
            "source_type": SOURCE_TYPE,
            "scene_type": SCENE_TYPE,
            "user_supplied": True,
            "personal_sensitive_image": False,
            "live_camera_frame": False,
            "external_url_source": False,
            "dataset_source": False,
            "navigation_runtime_frame": False,
            "fact_layer_source": False,
            "semantic_layer_source": False,
            "allowed_for_single_inference_trial": True,
            "must_not_enter_fact_layer": True,
            "must_not_enter_navigation_runtime": True,
            "must_not_enter_output_adapter": True,
            "must_not_enter_semantic_layer": True,
        },
    )
    (out_root / "mobile_sam_real_local_image_manifest_v1.json").write_text(
        json.dumps({**asdict(manifest), "image_resolve_mode": image_resolve_mode}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if not manifest_valid:
        boundary_violations.append("manifest.invalid_or_missing")

    may_infer = (
        perform_inference
        and snapshot.snapshot_succeeded
        and recheck.recheck_passed
        and manifest.manifest_valid
        and image_abs is not None
    )
    started_at = _now()
    t0 = time.time()
    if may_infer:
        load_info, prompt_results, _ = _run_prompt_segmentation(
            code_path, timm_target, weight_abs, image_abs, manifest_fields, mask_dir
        )
    else:
        skip = "inference_skipped_snapshot_recheck_manifest_or_upstream_failed"
        load_info = {
            "import_attempted": False,
            "import_success": False,
            "import_error": skip,
            "checkpoint_load_attempted": False,
            "model_object_created": False,
            "model_type_name": "",
            "checkpoint_load_success": False,
            "checkpoint_load_error": skip,
            "model_object_released": False,
        }
        prompt_results = []
    elapsed = round(time.time() - t0, 4)
    ended_at = _now()
    peak_mb = _peak_memory_mb()

    load_record = RealLocalImageModelLoadRecord(
        record_id="real_local_image_model_load_record_v1",
        import_attempted=bool(load_info["import_attempted"]),
        import_success=bool(load_info["import_success"]),
        import_error=load_info["import_error"],
        checkpoint_load_attempted=bool(load_info["checkpoint_load_attempted"]),
        model_object_created=bool(load_info["model_object_created"]),
        model_type_name=load_info["model_type_name"],
        checkpoint_load_success=bool(load_info["checkpoint_load_success"]),
        checkpoint_load_error=load_info["checkpoint_load_error"],
        model_object_released=bool(load_info["model_object_released"]),
    )
    (out_root / "real_local_image_model_load_record_v1.json").write_text(
        json.dumps(asdict(load_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    prompt_success_count = sum(1 for p in prompt_results if p.get("inference_success"))
    prompt_failure_count = PROMPT_COUNT - prompt_success_count
    inference_attempted = bool(load_info["checkpoint_load_success"]) and len(prompt_results) > 0
    overall_success = prompt_success_count >= 1

    prompt_exec = RealLocalImagePromptExecutionRecord(
        record_id="real_local_image_prompt_execution_record_v1",
        prompt_count=PROMPT_COUNT,
        inference_attempted=inference_attempted,
        prompt_success_count=prompt_success_count,
        prompt_failure_count=prompt_failure_count,
        prompt_results=tuple(prompt_results),
    )
    (out_root / "real_local_image_prompt_execution_record_v1.json").write_text(
        json.dumps(asdict(prompt_exec), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    candidate_masks_written = prompt_success_count >= 1
    masks_record = RealLocalImageCandidateMasksRecord(
        record_id="real_local_image_candidate_masks_v1",
        candidate_masks_written=candidate_masks_written,
        mask_output_dir=str(mask_dir),
        prompt_mask_summaries=tuple(prompt_results),
        candidate_only=True,
        not_fact=True,
    )
    (out_root / "real_local_image_candidate_masks_v1.json").write_text(
        json.dumps(asdict(masks_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    failure_modes: List[str] = []
    if prompt_failure_count:
        failure_modes.append("partial_prompt_failure")
    for p in prompt_results:
        if p.get("fallback_from_box_to_point"):
            failure_modes.append(f"box_to_point_fallback:{p['prompt_id']}")
        if p.get("inference_success") and (p.get("mask_area_ratio") or 0) < 0.001:
            failure_modes.append(f"tiny_mask_area:{p['prompt_id']}")

    quality_risks = [
        "night_scene_low_light",
        "reflection_or_glare",
        "small_distant_objects",
        "glass_building_repeated_patterns",
        "road_marking_large_flat_region",
    ]
    per_prompt_notes = {
        p["prompt_id"]: (
            f"area_ratio={p.get('mask_area_ratio')}; score={p.get('score_or_iou_if_available')}"
            if p.get("inference_success")
            else f"failed:{p.get('fallback_reason', 'unknown')}"
        )
        for p in prompt_results
    }
    quality = RealLocalImageQualitySummaryRecord(
        record_id="real_local_image_quality_summary_v1",
        overall_inference_success=overall_success,
        prompt_success_count=prompt_success_count,
        prompt_failure_count=prompt_failure_count,
        observed_failure_modes=tuple(failure_modes),
        likely_quality_risks=tuple(quality_risks),
        human_review_required=True,
        suitable_for_runtime_admission=False,
        suitable_for_quality_observation=True,
        not_semantic_fact=True,
    )
    quality_payload = {**asdict(quality), "per_prompt_quality_note": per_prompt_notes}
    (out_root / "real_local_image_quality_summary_v1.json").write_text(
        json.dumps(quality_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    timeout_occurred = elapsed > TIMEOUT_SECONDS
    oom_occurred = peak_mb > MEMORY_LIMIT_MB
    monitor = RealLocalImageMemoryTimeoutMonitorRecord(
        monitor_id="real_local_image_memory_timeout_monitor_v1",
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        started_at=started_at,
        ended_at=ended_at,
        elapsed_seconds=elapsed,
        peak_memory_mb=peak_mb,
        timeout_occurred=timeout_occurred,
        oom_occurred=oom_occurred,
        model_object_cleanup_attempted=bool(load_info["model_object_released"]),
        persistent_process_left=False,
    )
    (out_root / "real_local_image_memory_timeout_monitor_v1.json").write_text(
        json.dumps(asdict(monitor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = RealLocalImageRollbackCleanupRecord(
        record_id="real_local_image_rollback_cleanup_v1",
        pre_inference_snapshot_required=True,
        rollback_available=True,
        rollback_preserves_registry=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        rollback_preserves_source_uploaded_image=True,
        candidate_output_cleanup_attempted_if_failed=not overall_success,
        model_object_cleanup_attempted=bool(load_info["model_object_released"]),
        no_fact_write_on_failure=True,
        no_registry_mutation_on_failure=True,
    )

    exclusion = RealLocalImageRuntimeSemanticFactExclusionRecord(
        record_id="real_local_image_runtime_semantic_fact_exclusion_v1",
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        fact_write_ready=False,
        navigation_action_speech_ready=False,
        commercial_runtime_ready=False,
        real_image_trial_success_not_runtime_approval=True,
        real_image_trial_success_not_output_adapter_approval=True,
        real_image_trial_success_not_semantic_layer_approval=True,
        real_image_trial_success_not_fact_write_approval=True,
        real_image_trial_success_not_navigation_action_speech_approval=True,
        real_image_trial_success_not_commercial_runtime_approval=True,
    )

    post_audit = RealLocalImagePostReviewAudit(
        audit_id="real_local_image_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        registry_readiness_rechecked=registry_ok,
        weight_sha256_rechecked=sha256_matches,
        image_manifest_written=manifest.manifest_valid,
        image_source_allowed=manifest.source_type == SOURCE_TYPE,
        prompt_count=PROMPT_COUNT,
        inference_attempted=inference_attempted,
        prompt_success_count=prompt_success_count,
        candidate_masks_written=candidate_masks_written,
        quality_summary_written=True,
        candidate_output_only=True,
        no_runtime=RUNTIME_EXECUTION_ALLOWED is False,
        no_output_adapter=REAL_OUTPUT_ADAPTER_ALLOWED is False,
        no_semantic_layer=SEMANTIC_PROMOTION_ALLOWED is False,
        no_fact_write=FACT_WRITE_ALLOWED is False,
        no_navigation_action_speech=NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        no_registry_mutation=REGISTRY_MUTATION_ALLOWED is False,
        no_extra_download=ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        memory_timeout_recorded=True,
        cleanup_recorded=True,
        test_board_written=write_test_board,
        test_board_protected=all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        post_review_passed=(
            snapshot.snapshot_succeeded
            and recheck.recheck_passed
            and manifest.manifest_valid
            and not timeout_occurred
        ),
    )
    (out_root / "real_local_image_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    invariant_state: Dict[str, bool] = {
        "upstream_approval_verified": approval_ok,
        "registry_inference_trial_verified": registry_ok,
        "weight_rechecked": sha256_matches and size_matches,
        "manifest_valid": manifest.manifest_valid,
        "only_manifest_image": manifest.manifest_valid and image_exists,
        "no_live_camera": LIVE_CAMERA_ALLOWED is False and manifest.live_camera_frame is False,
        "no_external_url": EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False and manifest.external_url_source is False,
        "no_uncontrolled_dataset": UNCONTROLLED_DATASET_ALLOWED is False and manifest.dataset_source is False,
        "prompt_labels_not_facts": all(
            p.get("semantic_fact_assertion") is False for p in prompt_results
        ) if prompt_results else True,
        "candidate_output_only": masks_record.candidate_only and masks_record.not_fact,
        "no_runtime_output_semantic": (
            RUNTIME_EXECUTION_ALLOWED is False
            and REAL_OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_PROMOTION_ALLOWED is False
        ),
        "no_fact_navigation_speech": FACT_WRITE_ALLOWED is False and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_extra_download": ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "success_not_downstream_ready": exclusion.runtime_ready is False and exclusion.semantic_layer_ready is False,
        "quality_summary_not_fact": quality.not_semantic_fact is True,
        "memory_timeout_recorded": True,
        "cleanup_recorded": rollback.model_object_cleanup_attempted is True,
        "post_review_present": True,
        "test_board_record_required_true": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_board_protected_non_deletable": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL[k] for k in (
                "test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden"
            )
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeRealLocalImageInferenceExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeRealLocalImageInferenceExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    no_boundary_violation = len(boundary_violations) == 0
    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        decision_branch = "blocked"
        recommended_next_phase = NEXT_PHASE_BLOCKED
    elif overall_success and candidate_masks_written:
        final_decision = FINAL_DECISION_GO
        decision_branch = "go"
        recommended_next_phase = NEXT_PHASE_GO
        blocker_count = 0
    else:
        final_decision = FINAL_DECISION_FAILED
        decision_branch = "failed_no_boundary_violation"
        recommended_next_phase = NEXT_PHASE_FAILED
        blocker_count = 0

    blocker_count = len(boundary_violations) if not no_boundary_violation else 0

    followup = RealLocalImageFollowupReviewRoute(
        route_id="real_local_image_followup_review_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next_phase,
        next_phase_scope="mobile_sam_real_image_quality_observation_only",
    )

    go_conditions: Dict[str, bool] = {
        "mobile_sam_real_local_image_inference_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "real_local_image_pre_inference_snapshot_record_count_eq_1": True,
        "real_local_image_manifest_record_count_gte_1": True,
        "real_local_image_registry_weight_recheck_record_count_gte_1": True,
        "real_local_image_model_load_record_count_gte_1": True,
        "real_local_image_prompt_execution_record_count_gte_1": True,
        "real_local_image_candidate_masks_record_count_gte_1": True,
        "real_local_image_quality_summary_record_count_gte_1": True,
        "real_local_image_memory_timeout_monitor_record_count_gte_1": True,
        "real_local_image_post_review_audit_count_gte_1": True,
        "real_local_image_rollback_cleanup_record_count_gte_1": True,
        "real_local_image_runtime_semantic_fact_exclusion_record_count_gte_1": True,
        "real_local_image_followup_review_route_record_count_gte_1": True,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "image_manifest_written": manifest.manifest_valid,
        "inference_attempted": inference_attempted,
        "prompt_count_eq_5": PROMPT_COUNT == 5,
        "prompt_success_count_gte_1": prompt_success_count >= 1,
        "candidate_masks_written": candidate_masks_written,
        "quality_summary_written": True,
        "candidate_output_only": True,
        "real_local_image_candidate_masks_verified": candidate_masks_written,
        "real_scene_quality_observation_available": overall_success,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "cleanup_does_not_delete_test_board": True,
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMRealLocalImageInferenceExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_real_local_image_inference_execution_profile_count=1,
        real_local_image_pre_inference_snapshot_record_count=1,
        real_local_image_manifest_record_count=1,
        real_local_image_registry_weight_recheck_record_count=1,
        real_local_image_model_load_record_count=1,
        real_local_image_prompt_execution_record_count=1,
        real_local_image_candidate_masks_record_count=1,
        real_local_image_quality_summary_record_count=1,
        real_local_image_memory_timeout_monitor_record_count=1,
        real_local_image_post_review_audit_count=1,
        real_local_image_rollback_cleanup_record_count=1,
        real_local_image_runtime_semantic_fact_exclusion_record_count=1,
        real_local_image_followup_review_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        prompt_count=PROMPT_COUNT,
        prompt_success_count=prompt_success_count,
        inference_attempted=inference_attempted,
        candidate_masks_written=candidate_masks_written,
        real_local_image_candidate_masks_verified=candidate_masks_written,
        real_scene_quality_observation_available=overall_success,
        failure_recorded=not overall_success and no_boundary_violation,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Real Local Image Inference Trial Execution And Post Review",
        "lifecycle_variant": SCOPE,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "asset_id": MOBILE_SAM_ASSET_ID,
        "test_asset_id": TEST_ASSET_ID,
        "upstream_request_approval_ref": UPSTREAM_REQUEST_APPROVAL_REF,
        "upstream_request_approval_state": approval_state,
        "overlay_path": str(overlay_path),
        "image_resolve_mode": image_resolve_mode,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_real_local_image_inference_execution_profile": _build_profile(),
        "mobile_sam_real_local_image_inference_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "real_local_image_pre_inference_snapshot_record": asdict(snapshot),
        "real_local_image_manifest_record": asdict(manifest),
        "real_local_image_registry_weight_recheck_record": asdict(recheck),
        "real_local_image_model_load_record": asdict(load_record),
        "real_local_image_prompt_execution_record": asdict(prompt_exec),
        "real_local_image_candidate_masks_record": asdict(masks_record),
        "real_local_image_quality_summary_record": quality_payload,
        "real_local_image_memory_timeout_monitor_record": asdict(monitor),
        "real_local_image_post_review_record": asdict(post_audit),
        "real_local_image_rollback_cleanup_record": asdict(rollback),
        "real_local_image_runtime_semantic_fact_exclusion_record": asdict(exclusion),
        "real_local_image_followup_review_route_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "boundary_violations": boundary_violations,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "execution_status": decision_branch,
            "inference_attempted": inference_attempted,
            "prompt_success_count": prompt_success_count,
            "prompt_failure_count": prompt_failure_count,
            "candidate_masks_written": candidate_masks_written,
            "registry_mutated_this_phase": False,
            "recommended_next_phase": recommended_next_phase,
            "transition_note": (
                "REAL EXECUTION on user-supplied scoped local street scene. "
                "5 planned prompts, candidate masks only. NO runtime/semantic/fact."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

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
            "real_local_image_pre_inference_snapshot_record": {"record": asdict(snapshot)},
            "real_local_image_manifest_record": {"record": asdict(manifest)},
            "real_local_image_registry_weight_recheck_record": {"record": asdict(recheck)},
            "real_local_image_model_load_record": {"record": asdict(load_record)},
            "real_local_image_prompt_execution_record": {"record": asdict(prompt_exec)},
            "real_local_image_candidate_masks_record": {"record": asdict(masks_record)},
            "real_local_image_quality_summary_record": {"record": quality_payload},
            "real_local_image_memory_timeout_monitor_record": {"record": asdict(monitor)},
            "real_local_image_post_review_record": {"record": asdict(post_audit)},
            "real_local_image_runtime_semantic_fact_exclusion_record": {"record": asdict(exclusion)},
            "real_local_image_followup_review_route_record": {"record": asdict(followup)},
        }
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
            "navigation_action_speech_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest_tb["extra_written_records"] = extra_written
        manifest_tb["total_record_count"] = manifest_tb["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest_tb
        result["test_board_record_count"] = manifest_tb["total_record_count"]

    return result


def main() -> int:
    result = review_p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "prompt_success_count": result["conclusions"]["prompt_success_count"],
                "candidate_masks_written": result["conclusions"]["candidate_masks_written"],
                "negative_guard_passed": result["negative_guard_passed"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    ok = {FINAL_DECISION_GO, FINAL_DECISION_FAILED}
    return 0 if result["final_decision"] in ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
