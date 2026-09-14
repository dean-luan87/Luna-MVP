# -*- coding: utf-8 -*-
"""MobileSAM image runner skeleton v1 — test-only segmentation."""

from __future__ import annotations

import gc
import importlib
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review.p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_types_v1 import (
    MOBILE_SAM_BUILD_KEY,
    MOBILE_SAM_CODE_PATH_REL,
    MOBILE_SAM_IMPORT_ROOT,
    MOBILE_SAM_WEIGHT_FILE_PATH,
    TIMM_INSTALL_TARGET_REL,
)
from capabilities.midplatform.model_test_lens.scene_aware_segmentation.segmentation_prompt_policy_runtime_v1 import (
    SUBWAY_DEFAULT_BOXES,
    build_scene_aware_runner_context,
)

# scene_prompt_set_subway_platform_v1 — station_direction_sign / station_name_board / route_map_or_line_info
_SUBWAY_STATION_PROMPT_IDS = tuple(SUBWAY_DEFAULT_BOXES.keys())
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    artifact_roots,
    repo_root,
    resolve_path,
)


def _norm_box_to_pixels(norm_box: List[float], width: int, height: int) -> List[int]:
    x1, y1, x2, y2 = norm_box
    return [
        int(round(x1 * width)),
        int(round(y1 * height)),
        int(round(x2 * width)),
        int(round(y2 * height)),
    ]


def check_mobilesam_readiness() -> Dict[str, Any]:
    code_path = resolve_path(MOBILE_SAM_CODE_PATH_REL)
    timm_target = resolve_path(TIMM_INSTALL_TARGET_REL)
    weight_abs = resolve_path(MOBILE_SAM_WEIGHT_FILE_PATH)
    return {
        "code_path": str(code_path),
        "code_exists": code_path.is_dir(),
        "timm_target": str(timm_target),
        "timm_exists": timm_target.is_dir(),
        "weight_path": str(weight_abs),
        "weight_exists": weight_abs.is_file(),
        "ready": code_path.is_dir() and timm_target.is_dir() and weight_abs.is_file(),
    }


def run_mobilesam_image_runner(
    *,
    image_path: Path,
    output_dir: Path,
    job_id: str,
    max_prompts: int = 10,
    file_name: str = "",
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    readiness = check_mobilesam_readiness()
    if not readiness["ready"]:
        return {
            "status": "failed_no_boundary_violation",
            "status_reason": "mobilesam_dependencies_missing",
            "no_boundary_violation": True,
            "failure_recorded": True,
            "readiness": readiness,
            "candidate_outputs": [],
            "prompt_results": [],
            "metrics": {},
        }

    code_path = Path(readiness["code_path"])
    timm_target = Path(readiness["timm_target"])
    weight_abs = Path(readiness["weight_path"])
    mask_dir = output_dir / "candidate_masks"
    mask_dir.mkdir(parents=True, exist_ok=True)

    load_info: Dict[str, Any] = {
        "import_attempted": False,
        "import_success": False,
        "checkpoint_load_success": False,
        "checkpoint_load_error": "",
    }
    prompt_results: List[Dict[str, Any]] = []
    candidate_outputs: List[Dict[str, Any]] = []

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

        model = sam_model_registry[MOBILE_SAM_BUILD_KEY](checkpoint=str(weight_abs))
        load_info["checkpoint_load_success"] = True

        import numpy as np
        from PIL import Image  # noqa: WPS433

        with Image.open(image_path) as im:
            width, height = im.size
            img = np.array(im.convert("RGB"))

        predictor = SamPredictor(model)
        predictor.set_image(img)

        scene_ctx = build_scene_aware_runner_context(
            image_path=image_path,
            file_name=file_name or image_path.name,
            max_prompts=max_prompts,
        )
        specs = scene_ctx["prompt_execution_plan"]
        success_count = 0
        for spec in specs:
            norm_box = list(spec["normalized_box_approx"])
            pixel_box = _norm_box_to_pixels(norm_box, width, height)
            center = [(pixel_box[0] + pixel_box[2]) // 2, (pixel_box[1] + pixel_box[3]) // 2]
            result: Dict[str, Any] = {
                "prompt_id": spec["prompt_id"],
                "prompt_target_label": spec["prompt_target_label"],
                "source_prompt_hint": spec.get("source_prompt_hint"),
                "display_task_semantic": spec.get("display_task_semantic"),
                "semantic_label": spec.get("semantic_label", "candidate_only"),
                "prompt_is_not_fact": True,
                "ocr_route_candidate": bool(spec.get("ocr_route_candidate")),
                "pixel_box": pixel_box,
                "success": False,
                "score": 0.0,
                "mask_ref": None,
            }
            try:
                masks, scores, _ = predictor.predict(box=np.array(pixel_box)[None, :], multimask_output=True)
                if masks is None or len(masks) == 0:
                    masks, scores, _ = predictor.predict(
                        point_coords=np.array([center]),
                        point_labels=np.array([1]),
                        multimask_output=True,
                    )
                if masks is not None and len(masks) > 0:
                    best_idx = int(np.argmax(scores))
                    mask = masks[best_idx]
                    score = float(scores[best_idx])
                    mask_name = f"{job_id}_{spec['prompt_id']}_candidate_mask.png"
                    mask_path = mask_dir / mask_name
                    Image.fromarray((mask.astype("uint8") * 255)).save(mask_path)
                    result["success"] = True
                    result["score"] = score
                    result["mask_ref"] = str(mask_path.relative_to(repo_root()))
                    success_count += 1
                    candidate_outputs.append({
                        "output_id": spec["prompt_id"],
                        "output_type": "candidate_mask",
                        "mask_ref": result["mask_ref"],
                        "score": score,
                        "candidate_only": True,
                        "source_prompt_hint": spec.get("source_prompt_hint"),
                        "display_task_semantic": spec.get("display_task_semantic"),
                        "prompt_is_not_fact": True,
                        "ocr_route_candidate": bool(spec.get("ocr_route_candidate")),
                    })
            except Exception as exc:  # noqa: BLE001
                result["error"] = str(exc)
            prompt_results.append(result)

        if success_count == 0:
            return {
                "status": "failed_no_boundary_violation",
                "status_reason": "all_prompts_failed",
                "no_boundary_violation": True,
                "failure_recorded": True,
                "load_info": load_info,
                "prompt_results": prompt_results,
                "candidate_outputs": candidate_outputs,
                "metrics": {"prompt_success_count": 0, "prompt_attempt_count": len(specs)},
            }

        return {
            "status": "completed",
            "status_reason": "mobilesam_segmentation_completed",
            "no_boundary_violation": True,
            "failure_recorded": False,
            "load_info": load_info,
            "scene_profile_candidate": scene_ctx["scene_profile_candidate"],
            "segmentation_prompt_policy": scene_ctx["segmentation_prompt_policy"],
            "prompt_results": prompt_results,
            "candidate_outputs": candidate_outputs,
            "metrics": {
                "prompt_attempt_count": len(specs),
                "prompt_success_count": success_count,
                "overall_success_rate": success_count / len(specs),
                "image_width": width,
                "image_height": height,
                "scene_type_candidate": scene_ctx["scene_profile_candidate"].get("scene_type_candidate"),
                "prompt_set_id": scene_ctx["segmentation_prompt_policy"].get("prompt_set_id"),
            },
            "mask_dir": str(mask_dir.relative_to(repo_root())),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed_no_boundary_violation",
            "status_reason": f"mobilesam_runner_exception:{exc}",
            "no_boundary_violation": True,
            "failure_recorded": True,
            "load_info": load_info,
            "traceback": traceback.format_exc(),
            "candidate_outputs": candidate_outputs,
            "prompt_results": prompt_results,
            "metrics": {},
        }
    finally:
        model = None
        gc.collect()
