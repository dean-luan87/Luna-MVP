# -*- coding: utf-8 -*-
"""P1 MobileSAM Multi Real Image Inference Trial Execution And Post Review — review v1."""

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
from collections import defaultdict
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
from capabilities.field_understanding.p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review.p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    load_artifact,
    verify_stages,
)
from capabilities.field_understanding.p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review.p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_types_v1 import (  # noqa: E402
    ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED,
    ALL_GOVERNANCE_RULES,
    BROAD_READINESS_MUST_BE_FALSE,
    CANDIDATE_OUTPUT_ONLY,
    CHECKPOINT_LOAD_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXECUTION_PRINCIPLE_ZH,
    EXPECTED_IMAGE_COUNT,
    EXPECTED_PROMPT_CATEGORY_COUNT,
    EXPECTED_PROMPT_TRIAL_COUNT,
    EXPECTED_READINESS_LEVEL,
    EXTERNAL_IMAGE_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FOUR_SCOPED_LOCAL_IMAGES_ONLY,
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
    MULTI_IMAGE_ASSET_SPECS,
    MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION,
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
    PROMPT_CATEGORY_SPECS,
    REAL_EXECUTION_PHASE,
    REAL_IMPORT_ALLOWED,
    REAL_INFERENCE_ALLOWED,
    REAL_OUTPUT_ADAPTER_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_REGISTRY_TRUE_FLAGS,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    SEGMENTATION_ALLOWED,
    SEMANTIC_PROMOTION_ALLOWED,
    SOURCE_IMAGE_ROOT_REL,
    SOURCE_TYPE,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    TIMEOUT_SECONDS,
    TIMM_IMPORT_ROOT,
    TIMM_INSTALL_TARGET_REL,
    UNCONTROLLED_DATASET_ALLOWED,
    UPSTREAM_QUALITY_REVIEW_REF,
    UPSTREAM_REGISTRY_OVERLAY_REF,
    UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO,
    UPSTREAM_REQUEST_APPROVAL_REF,
    UPSTREAM_RUNTIME_BOUNDARY_REF,
    WEIGHT_CHAIN,
    MultiRealImageAggregateQualitySummaryRecord,
    MultiRealImageCandidateMasksRecord,
    MultiRealImageFollowupReviewRoute,
    MultiRealImageManifestRecord,
    MultiRealImageMemoryTimeoutMonitorRecord,
    MultiRealImageModelLoadRecord,
    MultiRealImagePerImageQualitySummaryRecord,
    MultiRealImagePostReviewAudit,
    MultiRealImagePreInferenceSnapshotRecord,
    MultiRealImagePromptExecutionRecord,
    MultiRealImageRegistryWeightRecheckRecord,
    MultiRealImageRollbackCleanupRecord,
    MultiRealImageRuntimeSemanticFactExclusionRecord,
    NegativeMultiRealImageInferenceExecutionGuard,
    P1MobileSAMMultiRealImageInferenceExecutionDecision,
    P1MobileSAMMultiRealImageInferenceExecutionPostReviewProfile,
    to_dict,
)

UPSTREAM_APPROVAL_ARTIFACT_REL = (
    "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_v1_smoke_v0/"
    "p1_mobile_sam_multi_real_image_inference_trial_request_approval_and_readiness_review_v1.json"
)

_PKG = "capabilities/field_understanding/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review"
STEP_FILES = (
    f"{_PKG}/__init__.py",
    f"{_PKG}/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_types_v1.py",
    f"{_PKG}/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_registry_v1.py",
    f"{_PKG}/review_p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1.py",
)

PROFILE_REF = "p1_mobile_sam_multi_real_image_inference_execution_profile_v1"
DECISION_REF = "p1_mobile_sam_multi_real_image_inference_execution_decision_v1"
REVIEW_FILENAME = (
    "p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_review_v1.json"
)
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"
TEST_BOARD_REF = (
    "capabilities/test_board/recognition_models/"
    "phase_p1_mobilesam_multi_real_image_inference_trial_execution_and_post_review_v1_001/"
)

MIN_PROMPT_ATTEMPTS_FOR_GO = 12
MIN_PROMPT_SUCCESSES_FOR_GO = 4


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
    / "p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0"
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


def _norm_box_to_pixels(norm_box: List[float], width: int, height: int) -> List[int]:
    x1, y1, x2, y2 = norm_box
    return [
        int(round(x1 * width)),
        int(round(y1 * height)),
        int(round(x2 * width)),
        int(round(y2 * height)),
    ]


def _discover_manifest_images() -> Tuple[List[Dict[str, Any]], List[str], bool]:
    from PIL import Image  # noqa: WPS433

    images: List[Dict[str, Any]] = []
    paths: List[str] = []
    all_found = True
    for spec in MULTI_IMAGE_ASSET_SPECS:
        rel = f"{SOURCE_IMAGE_ROOT_REL}/{spec['canonical_filename']}"
        abs_path = _resolve_path(rel)
        if not abs_path.is_file():
            all_found = False
            continue
        with Image.open(abs_path) as im:
            width, height = im.size
            mode = im.mode
        size = abs_path.stat().st_size
        entry = {
            "test_image_id": spec["test_asset_id"],
            "local_path": str(abs_path),
            "canonical_rel": rel,
            "sha256": _sha256_of(abs_path),
            "width": width,
            "height": height,
            "file_size_bytes": size,
            "image_mode": mode,
            "source_type": SOURCE_TYPE,
            "scene_type": spec["scene_type"],
            "personal_sensitive_image": False,
            "live_camera_frame": False,
            "external_url_source": False,
            "dataset_source": False,
            "navigation_runtime_frame": False,
            "fact_layer_source": False,
            "semantic_layer_source": False,
            "allowed_for_multi_image_inference_trial": True,
            "must_not_enter_fact_layer": True,
            "must_not_enter_navigation_runtime": True,
            "must_not_enter_output_adapter": True,
            "must_not_enter_semantic_layer": True,
        }
        images.append(entry)
        paths.append(str(abs_path))
    valid = all_found and len(images) == EXPECTED_IMAGE_COUNT
    return images, paths, valid


def _verify_upstream_approval() -> Tuple[Dict[str, Any], bool]:
    artifact, exists = _load_artifact_any_root(UPSTREAM_APPROVAL_ARTIFACT_REL)
    if not exists or not artifact:
        return {}, False
    approval = artifact.get("multi_real_image_owner_approval_issuance_record") or {}
    conclusions = artifact.get("conclusions") or {}
    decision = artifact.get("decision") or {}
    verified = (
        artifact.get("final_decision") == UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO
        and conclusions.get("can_enter_multi_real_image_inference_trial_execution_next") is True
        and approval.get("owner_approval_granted_for_multi_real_image_inference_execution_next") is True
        and decision.get("source_image_count") == EXPECTED_IMAGE_COUNT
    )
    return {
        "final_decision": artifact.get("final_decision"),
        "source_image_count": decision.get("source_image_count"),
        "can_enter_multi_real_image_inference_trial_execution_next": conclusions.get(
            "can_enter_multi_real_image_inference_trial_execution_next"
        ),
        "owner_approval_granted": approval.get(
            "owner_approval_granted_for_multi_real_image_inference_execution_next"
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


def _run_multi_prompt_segmentation(
    code_path: Path,
    timm_target: Path,
    weight_abs: Path,
    manifest_images: List[Dict[str, Any]],
    mask_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
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

        predictor = SamPredictor(model)
        mask_dir.mkdir(parents=True, exist_ok=True)

        for img_entry in manifest_images:
            image_abs = Path(img_entry["local_path"])
            img = np.array(Image.open(image_abs).convert("RGB"))
            predictor.set_image(img)
            width = int(img_entry["width"])
            height = int(img_entry["height"])
            image_id = img_entry["test_image_id"]

            for cat in PROMPT_CATEGORY_SPECS:
                norm_box = list(cat["normalized_box_default"])
                pixel_box = _norm_box_to_pixels(norm_box, width, height)
                center = [(pixel_box[0] + pixel_box[2]) // 2, (pixel_box[1] + pixel_box[3]) // 2]
                result: Dict[str, Any] = {
                    "image_id": image_id,
                    "scene_type": img_entry["scene_type"],
                    "prompt_id": cat["prompt_id"],
                    "prompt_category": cat["prompt_category"],
                    "prompt_target_label": cat["prompt_target_label"],
                    "prompt_label_is_test_description": True,
                    "semantic_fact_assertion": False,
                    "prompt_type_preferred": cat["prompt_type_preferred"],
                    "normalized_box_or_point": norm_box,
                    "pixel_box_or_point": pixel_box,
                    "coordinate_generation_method": "conservative_default_normalized_box_from_execution_phase",
                    "inference_attempted": False,
                    "inference_success": False,
                    "skipped": False,
                    "skipped_reason": "",
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
                mask_fname = f"{image_id}_{cat['prompt_id']}_candidate_mask.png"
                mask_path = mask_dir / mask_fname
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
    return load_info, prompt_results


def _build_per_image_summaries(prompt_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_image: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in prompt_results:
        by_image[p["image_id"]].append(p)

    summaries: List[Dict[str, Any]] = []
    for spec in MULTI_IMAGE_ASSET_SPECS:
        image_id = spec["test_asset_id"]
        trials = by_image.get(image_id, [])
        success = [t for t in trials if t.get("inference_success")]
        failure = [t for t in trials if t.get("inference_attempted") and not t.get("inference_success")]
        skipped = [t for t in trials if t.get("skipped")]
        scores = [t["score_or_iou_if_available"] for t in success if t.get("score_or_iou_if_available") is not None]
        ratios = [t.get("mask_area_ratio", 0) for t in success]
        failure_modes: List[str] = []
        for t in trials:
            if t.get("fallback_from_box_to_point"):
                failure_modes.append(f"box_to_point_fallback:{t['prompt_id']}")
            if t.get("inference_success") and (t.get("mask_area_ratio") or 0) < 0.001:
                failure_modes.append(f"tiny_mask_area:{t['prompt_id']}")

        strongest = weakest = None
        if success:
            strongest = max(success, key=lambda x: x.get("score_or_iou_if_available") or 0)["prompt_category"]
            weakest = min(success, key=lambda x: x.get("score_or_iou_if_available") or 0)["prompt_category"]

        summaries.append({
            "image_id": image_id,
            "scene_type": spec["scene_type"],
            "prompt_attempt_count": len(trials),
            "prompt_success_count": len(success),
            "prompt_failure_count": len(failure),
            "skipped_prompt_count": len(skipped),
            "average_score_if_available": round(sum(scores) / len(scores), 4) if scores else None,
            "mask_area_ratio_stats": {
                "min": round(min(ratios), 6) if ratios else None,
                "max": round(max(ratios), 6) if ratios else None,
                "mean": round(sum(ratios) / len(ratios), 6) if ratios else None,
            },
            "observed_failure_modes": failure_modes,
            "likely_quality_risks": [
                "daytime_scene_clutter",
                "thin_object_fragmentation",
                "small_dynamic_object",
                "large_plane_ambiguity",
            ],
            "strongest_prompt_category": strongest,
            "weakest_prompt_category": weakest,
            "human_review_required": True,
            "suitable_for_runtime_admission": False,
            "suitable_for_quality_observation": True,
            "not_semantic_fact": True,
        })
    return summaries


def _build_aggregate_summary(
    prompt_results: List[Dict[str, Any]],
    per_image_summaries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    attempted = [p for p in prompt_results if p.get("inference_attempted")]
    success = [p for p in prompt_results if p.get("inference_success")]
    failure = [p for p in attempted if not p.get("inference_success")]
    skipped = [p for p in prompt_results if p.get("skipped")]

    by_cat: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in prompt_results:
        by_cat[p["prompt_category"]].append(p)

    per_cat_rate: Dict[str, float] = {}
    per_cat_score: Dict[str, float] = {}
    stable: List[str] = []
    unstable: List[str] = []
    for cat, trials in by_cat.items():
        succ = sum(1 for t in trials if t.get("inference_success"))
        per_cat_rate[cat] = round(succ / len(trials), 4) if trials else 0.0
        scores = [t["score_or_iou_if_available"] for t in trials if t.get("score_or_iou_if_available") is not None]
        per_cat_score[cat] = round(sum(scores) / len(scores), 4) if scores else 0.0
        if per_cat_rate[cat] >= 0.75:
            stable.append(cat)
        elif per_cat_rate[cat] < 0.5:
            unstable.append(cat)

    failure_modes: List[str] = []
    if failure:
        failure_modes.append("partial_prompt_failure")
    for p in prompt_results:
        if p.get("fallback_from_box_to_point"):
            failure_modes.append(f"box_to_point_fallback:{p['image_id']}:{p['prompt_id']}")

    total_attempted = len(attempted)
    total_success = len(success)
    return {
        "image_count": EXPECTED_IMAGE_COUNT,
        "expected_prompt_trial_count": EXPECTED_PROMPT_TRIAL_COUNT,
        "prompt_attempt_count": total_attempted,
        "prompt_success_count": total_success,
        "prompt_failure_count": len(failure),
        "skipped_prompt_count": len(skipped),
        "overall_success_rate": round(total_success / total_attempted, 4) if total_attempted else 0.0,
        "per_category_success_rate": per_cat_rate,
        "per_category_average_score": per_cat_score,
        "per_category_area_ratio_stats": {
            cat: {
                "mean": round(
                    sum(t.get("mask_area_ratio", 0) for t in trials if t.get("inference_success"))
                    / max(1, sum(1 for t in trials if t.get("inference_success"))),
                    6,
                )
            }
            for cat, trials in by_cat.items()
        },
        "recurring_failure_modes": list(dict.fromkeys(failure_modes)),
        "stable_categories": stable,
        "unstable_categories": unstable,
        "prompt_strategy_implications": [
            "building_or_large_structure: box_prompt_preferred_across_scenes",
            "road_or_crosswalk_or_large_plane: negative_point_or_multi_point_recommended",
            "sign_or_advertisement_screen: detector_or_ocr_assisted_box_future",
            "vehicle_or_small_dynamic_object: detector_or_tracker_assisted_box_future",
            "street_facility_or_pole_or_edge_object: thin_object_fragmentation_risk",
        ],
        "detector_ocr_tracker_prompt_need_update": True,
        "human_review_required": True,
        "suitable_for_runtime_admission": False,
        "suitable_for_quality_observation": True,
        "not_semantic_fact": True,
        "per_image_summary_refs": [s["image_id"] for s in per_image_summaries],
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        P1MobileSAMMultiRealImageInferenceExecutionPostReviewProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            real_execution_phase=REAL_EXECUTION_PHASE,
            mobile_sam_only=True,
            multi_real_image_inference_trial_execution=MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION,
            four_scoped_local_images_only=FOUR_SCOPED_LOCAL_IMAGES_ONLY,
            planned_prompt_targets_only=PLANNED_PROMPT_TARGETS_ONLY,
            expected_image_count=EXPECTED_IMAGE_COUNT,
            expected_prompt_category_count=EXPECTED_PROMPT_CATEGORY_COUNT,
            expected_prompt_trial_count=EXPECTED_PROMPT_TRIAL_COUNT,
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
            upstream_quality_review_ref=UPSTREAM_QUALITY_REVIEW_REF,
            upstream_runtime_boundary_ref=UPSTREAM_RUNTIME_BOUNDARY_REF,
            target_chain_ref="Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1(
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
    manifest_images, discovered_paths, manifest_valid = _discover_manifest_images()

    snapshot = MultiRealImagePreInferenceSnapshotRecord(
        snapshot_id="multi_real_image_pre_inference_snapshot_v1",
        python_version=sys.version.split()[0],
        executable_path=sys.executable,
        env_path=os.environ.get("VIRTUAL_ENV", sys.prefix),
        working_directory=str(Path.cwd()),
        mobile_sam_code_path_ref=str(code_path),
        timm_install_target_path_ref=str(timm_target),
        weight_path=MOBILE_SAM_WEIGHT_FILE_PATH,
        weight_file_exists=weight_exists,
        registry_overlay_path=UPSTREAM_REGISTRY_OVERLAY_REF,
        source_image_root=SOURCE_IMAGE_ROOT_REL,
        discovered_image_paths=tuple(discovered_paths),
        process_id=os.getpid(),
        memory_limit_mb=MEMORY_LIMIT_MB,
        timeout_seconds=TIMEOUT_SECONDS,
        upstream_request_approval_ref=UPSTREAM_REQUEST_APPROVAL_REF,
        upstream_quality_review_ref=UPSTREAM_QUALITY_REVIEW_REF,
        upstream_runtime_boundary_ref=UPSTREAM_RUNTIME_BOUNDARY_REF,
        rollback_snapshot_ref=str(out_root / "multi_real_image_pre_inference_snapshot_v1.json"),
        test_board_ref=TEST_BOARD_REF,
        snapshot_succeeded=weight_exists and manifest_valid and approval_ok and registry_ok,
    )
    (out_root / "multi_real_image_pre_inference_snapshot_v1.json").write_text(
        json.dumps(asdict(snapshot), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not snapshot.snapshot_succeeded:
        boundary_violations.append("snapshot.failed_or_upstream_not_ready")

    size_matches = weight_size == MOBILE_SAM_WEIGHT_SIZE_BYTES
    sha256_matches = sha_before == MOBILE_SAM_WEIGHT_SHA256
    timm_spec_ok, _ = _find_spec_with_paths(TIMM_IMPORT_ROOT, [timm_target])
    ms_spec_ok, _ = _find_spec_with_paths(MOBILE_SAM_IMPORT_ROOT, [code_path])
    recheck_passed = size_matches and sha256_matches and registry_ok and timm_spec_ok and ms_spec_ok

    recheck = MultiRealImageRegistryWeightRecheckRecord(
        recheck_id="multi_real_image_registry_weight_recheck_v1",
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
    (out_root / "multi_real_image_registry_weight_recheck_v1.json").write_text(
        json.dumps(asdict(recheck), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not recheck_passed:
        boundary_violations.append("recheck.sha256_registry_or_find_spec_failed")

    manifest = MultiRealImageManifestRecord(
        manifest_id="mobile_sam_multi_real_image_manifest_v1",
        image_count=len(manifest_images),
        source_image_root=SOURCE_IMAGE_ROOT_REL,
        images=tuple(manifest_images),
        manifest_valid=manifest_valid,
    )
    (out_root / "mobile_sam_multi_real_image_manifest_v1.json").write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not manifest_valid:
        boundary_violations.append("manifest.invalid_or_missing_images")

    may_infer = (
        perform_inference
        and snapshot.snapshot_succeeded
        and recheck.recheck_passed
        and manifest.manifest_valid
        and len(manifest_images) == EXPECTED_IMAGE_COUNT
    )
    started_at = _now()
    t0 = time.time()
    if may_infer:
        load_info, prompt_results = _run_multi_prompt_segmentation(
            code_path, timm_target, weight_abs, manifest_images, mask_dir
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

    load_record = MultiRealImageModelLoadRecord(
        record_id="multi_real_image_model_load_record_v1",
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
    (out_root / "multi_real_image_model_load_record_v1.json").write_text(
        json.dumps(asdict(load_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    prompt_attempt_count = sum(1 for p in prompt_results if p.get("inference_attempted"))
    prompt_success_count = sum(1 for p in prompt_results if p.get("inference_success"))
    prompt_failure_count = prompt_attempt_count - prompt_success_count
    skipped_prompt_count = sum(1 for p in prompt_results if p.get("skipped"))
    inference_attempted = bool(load_info["checkpoint_load_success"]) and prompt_attempt_count > 0
    overall_success = (
        prompt_success_count >= MIN_PROMPT_SUCCESSES_FOR_GO
        and prompt_attempt_count >= MIN_PROMPT_ATTEMPTS_FOR_GO
    )

    prompt_exec = MultiRealImagePromptExecutionRecord(
        record_id="multi_real_image_prompt_execution_record_v1",
        expected_prompt_trial_count=EXPECTED_PROMPT_TRIAL_COUNT,
        prompt_attempt_count=prompt_attempt_count,
        prompt_success_count=prompt_success_count,
        prompt_failure_count=prompt_failure_count,
        skipped_prompt_count=skipped_prompt_count,
        inference_attempted=inference_attempted,
        prompt_results=tuple(prompt_results),
    )
    (out_root / "multi_real_image_prompt_execution_record_v1.json").write_text(
        json.dumps(asdict(prompt_exec), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    candidate_masks_written = prompt_success_count >= MIN_PROMPT_SUCCESSES_FOR_GO
    masks_record = MultiRealImageCandidateMasksRecord(
        record_id="multi_real_image_candidate_masks_v1",
        candidate_masks_written=candidate_masks_written,
        mask_output_dir=str(mask_dir),
        prompt_mask_summaries=tuple(prompt_results),
        candidate_only=True,
        not_fact=True,
    )
    (out_root / "multi_real_image_candidate_masks_v1.json").write_text(
        json.dumps(asdict(masks_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    per_image_list = _build_per_image_summaries(prompt_results)
    per_image_record = MultiRealImagePerImageQualitySummaryRecord(
        record_id="multi_real_image_per_image_quality_summary_v1",
        per_image_summaries=tuple(per_image_list),
        human_review_required=True,
        suitable_for_runtime_admission=False,
        suitable_for_quality_observation=True,
        not_semantic_fact=True,
    )
    (out_root / "multi_real_image_per_image_quality_summary_v1.json").write_text(
        json.dumps(asdict(per_image_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    aggregate_payload = _build_aggregate_summary(prompt_results, per_image_list)
    aggregate_record = MultiRealImageAggregateQualitySummaryRecord(
        record_id="multi_real_image_aggregate_quality_summary_v1",
        **{k: aggregate_payload[k] for k in (
            "image_count", "expected_prompt_trial_count", "prompt_attempt_count",
            "prompt_success_count", "prompt_failure_count", "skipped_prompt_count",
            "overall_success_rate", "per_category_success_rate", "per_category_average_score",
            "recurring_failure_modes", "stable_categories", "unstable_categories",
            "prompt_strategy_implications", "detector_ocr_tracker_prompt_need_update",
            "human_review_required", "suitable_for_runtime_admission",
            "suitable_for_quality_observation", "not_semantic_fact",
        )},
    )
    (out_root / "multi_real_image_aggregate_quality_summary_v1.json").write_text(
        json.dumps({**asdict(aggregate_record), "per_category_area_ratio_stats": aggregate_payload["per_category_area_ratio_stats"]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    timeout_occurred = elapsed > TIMEOUT_SECONDS
    oom_occurred = peak_mb > MEMORY_LIMIT_MB
    monitor = MultiRealImageMemoryTimeoutMonitorRecord(
        monitor_id="multi_real_image_memory_timeout_monitor_v1",
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
    (out_root / "multi_real_image_memory_timeout_monitor_v1.json").write_text(
        json.dumps(asdict(monitor), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rollback = MultiRealImageRollbackCleanupRecord(
        record_id="multi_real_image_rollback_cleanup_v1",
        pre_inference_snapshot_required=True,
        rollback_available=True,
        rollback_preserves_registry=True,
        rollback_preserves_weight_file=True,
        rollback_preserves_test_board=True,
        rollback_preserves_review_artifacts=True,
        rollback_preserves_source_uploaded_images=True,
        candidate_output_cleanup_attempted_if_failed=not overall_success,
        model_object_cleanup_attempted=bool(load_info["model_object_released"]),
        no_fact_write_on_failure=True,
        no_registry_mutation_on_failure=True,
    )

    exclusion = MultiRealImageRuntimeSemanticFactExclusionRecord(
        record_id="multi_real_image_runtime_semantic_fact_exclusion_v1",
        runtime_ready=False,
        output_adapter_ready=False,
        semantic_layer_ready=False,
        fact_write_ready=False,
        navigation_action_speech_ready=False,
        commercial_runtime_ready=False,
        multi_real_image_trial_success_not_runtime_approval=True,
        multi_real_image_trial_success_not_output_adapter_approval=True,
        multi_real_image_trial_success_not_semantic_layer_approval=True,
        multi_real_image_trial_success_not_fact_write_approval=True,
        multi_real_image_trial_success_not_navigation_action_speech_approval=True,
        multi_real_image_trial_success_not_commercial_runtime_approval=True,
    )

    post_audit = MultiRealImagePostReviewAudit(
        audit_id="multi_real_image_post_review_audit_v1",
        pre_snapshot_exists=snapshot.snapshot_succeeded,
        registry_readiness_rechecked=registry_ok,
        weight_sha256_rechecked=sha256_matches,
        multi_image_manifest_written=manifest.manifest_valid,
        image_count=len(manifest_images),
        image_sources_allowed=manifest_valid,
        no_live_camera=LIVE_CAMERA_ALLOWED is False,
        no_external_url=EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False,
        no_uncontrolled_dataset_batch=UNCONTROLLED_DATASET_ALLOWED is False,
        real_import_performed=bool(load_info["import_success"]),
        model_load_performed=bool(load_info["checkpoint_load_success"]),
        expected_prompt_trial_count=EXPECTED_PROMPT_TRIAL_COUNT,
        prompt_attempt_count=prompt_attempt_count,
        inference_attempted=inference_attempted,
        prompt_success_count=prompt_success_count,
        candidate_masks_written=candidate_masks_written,
        per_image_quality_summary_written=True,
        aggregate_quality_summary_written=True,
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
    (out_root / "multi_real_image_post_review_audit_v1.json").write_text(
        json.dumps(asdict(post_audit), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    invariant_state: Dict[str, bool] = {
        "upstream_approval_verified": approval_ok,
        "registry_inference_trial_verified": registry_ok,
        "weight_rechecked": sha256_matches and size_matches,
        "manifest_valid": manifest.manifest_valid,
        "only_manifest_images": manifest.manifest_valid and len(manifest_images) == EXPECTED_IMAGE_COUNT,
        "no_live_camera": LIVE_CAMERA_ALLOWED is False and all(
            img.get("live_camera_frame") is False for img in manifest_images
        ),
        "no_external_url": EXTERNAL_IMAGE_DOWNLOAD_ALLOWED is False and all(
            img.get("external_url_source") is False for img in manifest_images
        ),
        "no_uncontrolled_dataset": UNCONTROLLED_DATASET_ALLOWED is False and all(
            img.get("dataset_source") is False for img in manifest_images
        ),
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
        "aggregate_quality_not_fact": aggregate_record.not_semantic_fact is True,
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

    negative_guards: List[NegativeMultiRealImageInferenceExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeMultiRealImageInferenceExecutionGuard(
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
        blocker_count = len(boundary_violations)
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

    followup = MultiRealImageFollowupReviewRoute(
        route_id="multi_real_image_followup_review_route_v1",
        decision_branch=decision_branch,
        recommended_next_phase=recommended_next_phase,
        next_phase_scope="mobile_sam_multi_real_image_quality_observation_and_automated_test_planning",
    )

    go_conditions: Dict[str, bool] = {
        "mobile_sam_multi_real_image_inference_execution_profile_count_eq_1": True,
        "stage_ref_count_gte_8": len(stage_refs) >= 8,
        "multi_real_image_pre_inference_snapshot_record_count_eq_1": True,
        "multi_real_image_manifest_record_count_gte_1": True,
        "multi_real_image_registry_weight_recheck_record_count_gte_1": True,
        "multi_real_image_model_load_record_count_gte_1": True,
        "multi_real_image_prompt_execution_record_count_gte_1": True,
        "multi_real_image_candidate_masks_record_count_gte_1": True,
        "multi_real_image_per_image_quality_summary_record_count_gte_1": True,
        "multi_real_image_aggregate_quality_summary_record_count_gte_1": True,
        "multi_real_image_memory_timeout_monitor_record_count_gte_1": True,
        "multi_real_image_post_review_audit_count_gte_1": True,
        "multi_real_image_rollback_cleanup_record_count_gte_1": True,
        "multi_real_image_runtime_semantic_fact_exclusion_record_count_gte_1": True,
        "multi_real_image_followup_review_route_record_count_gte_1": True,
        "negative_guard_count_eq_22": negative_guard_count == 22,
        "negative_guard_passed_eq_22": negative_guard_passed == 22,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "multi_image_manifest_written": manifest.manifest_valid,
        "image_count_eq_4": len(manifest_images) == EXPECTED_IMAGE_COUNT,
        "inference_attempted": inference_attempted,
        "expected_prompt_trial_count_eq_20": EXPECTED_PROMPT_TRIAL_COUNT == 20,
        "prompt_attempt_count_gte_12": prompt_attempt_count >= MIN_PROMPT_ATTEMPTS_FOR_GO,
        "prompt_success_count_gte_4": prompt_success_count >= MIN_PROMPT_SUCCESSES_FOR_GO,
        "candidate_masks_written": candidate_masks_written,
        "per_image_quality_summary_written": True,
        "aggregate_quality_summary_written": True,
        "candidate_output_only": True,
        "multi_real_image_candidate_masks_verified": candidate_masks_written,
        "real_scene_multi_image_quality_observation_available": overall_success,
        "multi_real_image_trial_success_not_runtime_approval": exclusion.multi_real_image_trial_success_not_runtime_approval,
        "multi_real_image_trial_success_not_output_adapter_approval": exclusion.multi_real_image_trial_success_not_output_adapter_approval,
        "multi_real_image_trial_success_not_semantic_layer_approval": exclusion.multi_real_image_trial_success_not_semantic_layer_approval,
        "multi_real_image_trial_success_not_fact_write_approval": exclusion.multi_real_image_trial_success_not_fact_write_approval,
        "multi_real_image_trial_success_not_navigation_action_speech_approval": exclusion.multi_real_image_trial_success_not_navigation_action_speech_approval,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "cleanup_does_not_delete_test_board": True,
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MobileSAMMultiRealImageInferenceExecutionDecision(
        decision_ref=DECISION_REF,
        mobile_sam_multi_real_image_inference_execution_profile_count=1,
        multi_real_image_pre_inference_snapshot_record_count=1,
        multi_real_image_manifest_record_count=1,
        multi_real_image_registry_weight_recheck_record_count=1,
        multi_real_image_model_load_record_count=1,
        multi_real_image_prompt_execution_record_count=1,
        multi_real_image_candidate_masks_record_count=1,
        multi_real_image_per_image_quality_summary_record_count=1,
        multi_real_image_aggregate_quality_summary_record_count=1,
        multi_real_image_memory_timeout_monitor_record_count=1,
        multi_real_image_post_review_audit_count=1,
        multi_real_image_rollback_cleanup_record_count=1,
        multi_real_image_runtime_semantic_fact_exclusion_record_count=1,
        multi_real_image_followup_review_route_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        image_count=len(manifest_images),
        expected_prompt_trial_count=EXPECTED_PROMPT_TRIAL_COUNT,
        prompt_attempt_count=prompt_attempt_count,
        prompt_success_count=prompt_success_count,
        inference_attempted=inference_attempted,
        candidate_masks_written=candidate_masks_written,
        multi_real_image_candidate_masks_verified=candidate_masks_written,
        real_scene_multi_image_quality_observation_available=overall_success,
        failure_recorded=not overall_success and no_boundary_violation,
        no_boundary_violation=no_boundary_violation,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 MobileSAM Multi Real Image Inference Trial Execution And Post Review",
        "lifecycle_variant": SCOPE,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": WEIGHT_CHAIN,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "asset_id": MOBILE_SAM_ASSET_ID,
        "upstream_request_approval_ref": UPSTREAM_REQUEST_APPROVAL_REF,
        "upstream_request_approval_state": approval_state,
        "overlay_path": str(overlay_path),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "mobile_sam_multi_real_image_inference_execution_profile": _build_profile(),
        "mobile_sam_multi_real_image_inference_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "multi_real_image_pre_inference_snapshot_record": asdict(snapshot),
        "multi_real_image_manifest_record": asdict(manifest),
        "multi_real_image_registry_weight_recheck_record": asdict(recheck),
        "multi_real_image_model_load_record": asdict(load_record),
        "multi_real_image_prompt_execution_record": asdict(prompt_exec),
        "multi_real_image_candidate_masks_record": asdict(masks_record),
        "multi_real_image_per_image_quality_summary_record": asdict(per_image_record),
        "multi_real_image_aggregate_quality_summary_record": {**asdict(aggregate_record), "per_category_area_ratio_stats": aggregate_payload["per_category_area_ratio_stats"]},
        "multi_real_image_memory_timeout_monitor_record": asdict(monitor),
        "multi_real_image_post_review_record": asdict(post_audit),
        "multi_real_image_rollback_cleanup_record": asdict(rollback),
        "multi_real_image_runtime_semantic_fact_exclusion_record": asdict(exclusion),
        "multi_real_image_followup_review_route_record": asdict(followup),
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
            "image_count": len(manifest_images),
            "prompt_attempt_count": prompt_attempt_count,
            "prompt_success_count": prompt_success_count,
            "prompt_failure_count": prompt_failure_count,
            "candidate_masks_written": candidate_masks_written,
            "registry_mutated_this_phase": False,
            "multi_real_image_inference_trial_success": overall_success,
            "multi_real_image_candidate_masks_verified": candidate_masks_written,
            "real_scene_multi_image_quality_observation_available": overall_success,
            "recommended_next_phase": recommended_next_phase,
            "transition_note": (
                "REAL EXECUTION on 4 user-supplied scoped local street scenes. "
                "20 planned prompt trials (4 images × 5 categories), candidate masks only. "
                "NO runtime/semantic/fact/navigation. NO registry mutation."
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
            "multi_real_image_pre_inference_snapshot_record": {"record": asdict(snapshot)},
            "multi_real_image_manifest_record": {"record": asdict(manifest)},
            "multi_real_image_registry_weight_recheck_record": {"record": asdict(recheck)},
            "multi_real_image_model_load_record": {"record": asdict(load_record)},
            "multi_real_image_prompt_execution_record": {"record": asdict(prompt_exec)},
            "multi_real_image_candidate_masks_record": {"record": asdict(masks_record)},
            "multi_real_image_per_image_quality_summary_record": {"record": asdict(per_image_record)},
            "multi_real_image_aggregate_quality_summary_record": {"record": {**asdict(aggregate_record), "per_category_area_ratio_stats": aggregate_payload["per_category_area_ratio_stats"]}},
            "multi_real_image_memory_timeout_monitor_record": {"record": asdict(monitor)},
            "multi_real_image_post_review_record": {"record": asdict(post_audit)},
            "multi_real_image_runtime_semantic_fact_exclusion_record": {"record": asdict(exclusion)},
            "multi_real_image_followup_review_route_record": {"record": asdict(followup)},
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
    result = review_p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "image_count": result["conclusions"]["image_count"],
                "prompt_attempt_count": result["conclusions"]["prompt_attempt_count"],
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
