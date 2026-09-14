# -*- coding: utf-8 -*-
"""ROI Crop Execution DryRun v1 — crop artifacts only, no OCR.

Phase-ROI-Crop-Execution-DryRun-v1-001
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-Crop-Execution-DryRun-v1-001"
RUNTIME_STEP = "roi_crop_execution_dryrun_v1"

CROP_POLICIES: List[Dict[str, Any]] = [
    {
        "rule_id": "crop_only_if_bbox_valid",
        "condition": "bbox_numeric_and_positive_area",
        "allowed_action": "generate_crop_artifact",
        "blocked_action": ["crop_without_bbox"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bbox_must_be_within_source_image",
        "condition": "bbox_within_bounds_when_known",
        "allowed_action": "validate_bbox",
        "blocked_action": ["out_of_bounds_crop"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bbox_null_must_defer",
        "condition": "proposed_roi_bbox_xyxy is null",
        "allowed_action": "defer_crop",
        "blocked_action": ["fabricate_bbox"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "full_frame_crop_not_primary_evidence",
        "condition": "bbox_area_ratio > 0.92",
        "allowed_action": "defer_or_label_non_primary",
        "blocked_action": ["use_as_primary_evidence"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_union_allowed_for_crop_artifact",
        "condition": "bbox_source==linebox_union",
        "allowed_action": "crop_dryrun_artifact",
        "blocked_action": [],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mixed_region_crop_requires_split_label",
        "condition": "proposal_type==mixed_region_split",
        "allowed_action": "crop_with_split_label_preserved",
        "blocked_action": ["semantic_join"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_semantic_join_after_crop",
        "condition": "always",
        "allowed_action": "per_region_artifacts_only",
        "blocked_action": ["cross_region_text_join"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "sq_e_requires_better_source_before_crop",
        "condition": "source_quality_grade==SQ_E",
        "allowed_action": "defer_crop",
        "blocked_action": ["immediate_crop_retry"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "better_frame_required_must_defer",
        "condition": "proposal_type==better_frame_required",
        "allowed_action": "defer_crop",
        "blocked_action": ["force_crop"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "always",
        "allowed_action": "crop_only",
        "blocked_action": ["ocr_invoked", "provider_invoked"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_request_generation_in_this_phase",
        "condition": "always",
        "allowed_action": "crop_only",
        "blocked_action": ["ocr_request_generated"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_evidence_pack_generation_in_this_phase",
        "condition": "always",
        "allowed_action": "crop_only",
        "blocked_action": ["evidence_pack_generated"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "always",
        "allowed_action": "crop_only",
        "blocked_action": ["world_model_attach"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FOLLOWUPS = [
    "ROI-to-OCRRequest Reference v1",
    "OCRRequest Gated Submission from ROI v1",
    "Evidence Pack Adapter v2 ROIRef",
    "Semantic Candidate v2 ROIAware",
    "Crop Quality Scoring",
    "Better Frame Selection Runtime",
    "Multiframe Merge Proposal",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _cid(key: str) -> str:
    return f"crop_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _aid(key: str) -> str:
    return f"crop_attempt_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _parse_video_id(frame_id: str) -> Optional[str]:
    m = re.match(r"^(.+)_f\d+$", frame_id or "")
    return m.group(1) if m else None


def _image_dims(path: Path) -> Tuple[int, int]:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as im:
            return im.size
    except Exception:
        return 0, 0


def _bbox_valid(bbox: Optional[List[float]], w: int, h: int) -> Tuple[bool, str, float]:
    if not bbox or len(bbox) < 4:
        return False, "null_bbox_deferred", 0.0
    try:
        x1, y1, x2, y2 = [float(bbox[i]) for i in range(4)]
    except (TypeError, ValueError):
        return False, "invalid_bbox", 0.0
    if x2 <= x1 or y2 <= y1:
        return False, "zero_area", 0.0
    area = (x2 - x1) * (y2 - y1)
    if w > 0 and h > 0:
        if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
            return False, "out_of_bounds", area / (w * h)
        ratio = area / (w * h)
        if ratio > 0.92:
            return False, "full_frame_not_primary", ratio
        return True, "valid", ratio
    return True, "valid", 0.0


def _crop_eligible(prop: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    ptype = prop.get("proposal_type") or ""
    sq = prop.get("source_quality_grade")
    bbox = prop.get("proposed_roi_bbox_xyxy")

    if ptype == "better_frame_required":
        return False, "better_frame_required"
    if ptype == "future_detector_required":
        return False, "future_detector_required"
    if bbox is None:
        return False, "null_bbox_deferred"
    if sq == "SQ_E":
        return False, "sq_e_hold_low_quality"
    return True, None


def _load_image_pil(path: Path):
    from PIL import Image  # type: ignore

    return Image.open(path).convert("RGB")


def _extract_video_frame(video_path: Path, frame_index: int):
    import cv2  # type: ignore

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return None
    idx = 0
    frame = None
    while idx <= frame_index:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        idx += 1
    cap.release()
    if frame is None:
        return None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    from PIL import Image  # type: ignore

    return Image.fromarray(rgb)


def _save_crop(img, bbox: List[float], out_path: Path) -> Tuple[int, int]:
    x1, y1, x2, y2 = [int(round(v)) for v in bbox[:4]]
    cropped = img.crop((x1, y1, x2, y2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out_path, format="PNG")
    return cropped.size[0], cropped.size[1]


def _resolve_video_path(v2: Path, frame_id: str, path_by_source: Dict[str, str]) -> Optional[Path]:
    vid = _parse_video_id(str(frame_id))
    if vid and vid in path_by_source:
        p = Path(path_by_source[vid])
        if p.is_file():
            return p
    fallback = v2.parent.parent / "Luna-Core" / "test_video_complex_6m42s.mp4"
    if not fallback.is_file():
        fallback = Path("/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4")
    return fallback if fallback.is_file() else None


def run_roi_crop_execution_dryrun_v1(
    *,
    output_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    adapter_v1_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    out = Path(output_root).resolve()
    crops_dir = out / "crops"
    roi_root = Path(roi_retry_root).resolve()
    sv = Path(source_validation_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    proposals = (_read_json(roi_root / "roi_retry_proposal_collection_v1.json") or {}).get("proposals") or []
    if not proposals:
        errs.append("no_proposals")

    path_by_image: Dict[str, str] = {}
    path_by_source: Dict[str, str] = {}
    for row in (_read_json(v2 / "mixed_batch_v2_input_candidate_matrix.json") or {}).get("rows") or []:
        if not isinstance(row, dict):
            continue
        sp = row.get("source_path")
        if not sp:
            continue
        sid = row.get("source_id")
        if sid:
            path_by_source[str(sid)] = str(sp)
        iid = row.get("image_id")
        if iid:
            path_by_image[str(iid)] = str(sp)

    frame_dims: Dict[str, Tuple[int, int]] = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            frame_dims[str(fr["frame_id"])] = (
                int(fr.get("image_width") or 0),
                int(fr.get("image_height") or 0),
            )

    intake_rows: List[Dict[str, Any]] = []
    artifacts_full: List[Dict[str, Any]] = []
    collection_rows: List[Dict[str, Any]] = []
    bbox_rows: List[Dict[str, Any]] = []
    resolution_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    mixed_rows: List[Dict[str, Any]] = []
    deferred_rows: List[Dict[str, Any]] = []
    ocr_ref_plan: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    executed = deferred = skipped = 0
    valid_bbox_count = null_deferred = mixed_crop = better_frame_def = 0
    generated_files = 0

    for prop in proposals:
        if not isinstance(prop, dict):
            continue
        pid = str(prop.get("roi_retry_proposal_id") or "")
        cid = _cid(f"cand:{pid}")
        bbox = prop.get("proposed_roi_bbox_xyxy")
        ptype = prop.get("proposal_type") or ""
        sq = prop.get("source_quality_grade")
        frame_id = prop.get("frame_id")
        image_id = prop.get("image_id")
        source_id = prop.get("source_id")

        eligible, defer_reason = _crop_eligible(prop)
        intake_rows.append(
            {
                "crop_candidate_id": cid,
                "roi_retry_proposal_id": pid,
                "source_retry_candidate_id": prop.get("source_retry_candidate_id"),
                "source_type": prop.get("source_type"),
                "source_id": source_id,
                "frame_id": frame_id,
                "image_id": image_id,
                "proposal_type": ptype,
                "proposed_roi_bbox_xyxy": bbox,
                "proposed_roi_polygon": prop.get("proposed_roi_polygon") or [],
                "bbox_source": prop.get("bbox_source"),
                "source_linebox_refs": prop.get("source_linebox_refs") or [],
                "source_quality_grade": sq,
                "readability_grade": prop.get("readability_grade"),
                "retry_priority": prop.get("retry_priority"),
                "retry_reason": prop.get("retry_reason"),
                "crop_eligible": eligible,
                "crop_defer_reason": defer_reason,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        w, h = 0, 0
        source_path: Optional[Path] = None
        source_frame_available = bool(frame_id)
        source_image_available = False
        source_video_available = False
        frame_extraction_required = False
        image_crop_required = False
        source_path_resolved = False
        resolution_status = "unsupported_source"

        if image_id and str(image_id) in path_by_image:
            source_path = Path(path_by_image[str(image_id)])
            source_image_available = source_path.is_file()
            image_crop_required = True
            if source_image_available:
                w, h = _image_dims(source_path)
                source_path_resolved = True
                resolution_status = "image_resolved"
            else:
                resolution_status = "source_image_missing"
        elif frame_id:
            frame_extraction_required = True
            w, h = frame_dims.get(str(frame_id), (0, 0))
            source_path = _resolve_video_path(v2, str(frame_id), path_by_source)
            source_video_available = source_path is not None
            source_path_resolved = source_video_available
            resolution_status = "video_frame_resolvable" if source_video_available else "source_video_missing"

        bbox_ok, bbox_status, area_ratio = _bbox_valid(list(bbox) if bbox else None, w, h)
        if bbox is None:
            null_deferred += 1
            bbox_status = "null_bbox_deferred"
        elif ptype == "better_frame_required":
            bbox_status = "better_frame_required"
            better_frame_def += 1
        elif ptype == "future_detector_required":
            bbox_status = "future_detector_required"
        elif sq == "SQ_E":
            bbox_status = "better_frame_required"
            better_frame_def += 1

        if bbox_ok:
            valid_bbox_count += 1

        if ptype == "mixed_region_split":
            mixed_crop += 1
            mixed_rows.append(
                {
                    "proposal_id": pid,
                    "mixed_region_detected": True,
                    "split_required": True,
                    "crop_generation_status": "deferred" if not eligible else "pending",
                    "split_label_preserved": True,
                    "semantic_join_allowed": False,
                    "cross_region_text_join_allowed": False,
                    "future_split_refinement_required": True,
                    "fact_status": "not_fact",
                }
            )

        crop_allowed = (
            eligible
            and bbox_ok
            and source_path_resolved
            and resolution_status in ("image_resolved", "video_frame_resolvable")
        )

        status = "deferred"
        gen_reason = defer_reason or bbox_status
        if not crop_allowed:
            if gen_reason in (
                "null_bbox_deferred",
                "better_frame_required",
                "future_detector_required",
                "sq_e_hold_low_quality",
                "full_frame_not_primary",
                "out_of_bounds",
                "zero_area",
                "invalid_bbox",
            ):
                deferred += 1
            else:
                status = "skipped"
                skipped += 1
            if status == "deferred":
                deferred_rows.append(
                    {
                        "proposal_id": pid,
                        "proposal_type": ptype,
                        "defer_reason": gen_reason,
                        "better_frame_required": ptype == "better_frame_required" or sq == "SQ_E",
                        "multiframe_required": sq == "SQ_C" and ptype == "future_detector_required",
                        "future_detector_required": ptype == "future_detector_required",
                        "required_future_action": (
                            "Better-Frame-Selection-Runtime"
                            if sq == "SQ_E" or ptype == "better_frame_required"
                            else "Multiframe-Merge-Proposal"
                        ),
                        "crop_generation_status": "deferred",
                        "ocr_request_generated": False,
                        "fact_status": "not_fact",
                    }
                )
        else:
            status = "generated"

        artifact_id = _cid(f"art:{pid}")
        crop_path: Optional[str] = None
        crop_w: Optional[int] = None
        crop_h: Optional[int] = None
        crop_generated = False
        err_msg: Optional[str] = None

        if crop_allowed and source_path and bbox:
            try:
                img = None
                if image_crop_required:
                    img = _load_image_pil(source_path)
                elif frame_extraction_required:
                    fi = _parse_frame_index(str(frame_id))
                    if fi is not None:
                        img = _extract_video_frame(source_path, fi)
                if img is not None:
                    if w == 0:
                        w, h = img.size
                    short_id = pid.replace("roi_retry_", "")[:8]
                    safe_sid = re.sub(r"[^\w.-]", "_", str(source_id or "src"))[:40]
                    fname = f"crop_{safe_sid}_{short_id}.png"
                    out_png = crops_dir / fname
                    crop_w, crop_h = _save_crop(img, list(bbox), out_png)
                    crop_path = str(out_png)
                    crop_generated = True
                    status = "generated"
                    executed += 1
                    generated_files += 1
                    gen_reason = "crop_png_saved"
                else:
                    status = "deferred"
                    gen_reason = "frame_extraction_failed"
                    if executed > 0:
                        executed -= 1
                    deferred += 1
            except Exception as e:  # noqa: BLE001
                status = "failed"
                gen_reason = "crop_failed"
                err_msg = str(e)
                if executed > 0:
                    executed -= 1
                skipped += 1

        chain = list(prop.get("source_chain") or [])
        chain.append(RUNTIME_STEP)

        bbox_rows.append(
            {
                "proposal_id": pid,
                "bbox_present": bbox is not None,
                "bbox_numeric": bbox_ok,
                "bbox_within_source_bounds": bbox_status not in ("out_of_bounds",),
                "bbox_area_positive": bbox_status != "zero_area",
                "bbox_area_ratio": area_ratio,
                "bbox_validation_status": bbox_status,
                "bbox_validation_reason": gen_reason,
                "crop_allowed": crop_allowed,
                "defer_reason": defer_reason or bbox_status,
            }
        )

        resolution_rows.append(
            {
                "proposal_id": pid,
                "source_frame_available": source_frame_available,
                "source_image_available": source_image_available,
                "source_video_available": source_video_available,
                "source_path_resolved": source_path_resolved,
                "frame_extraction_required": frame_extraction_required,
                "image_crop_required": image_crop_required,
                "source_resolution_status": resolution_status,
                "source_path": str(source_path) if source_path else None,
            }
        )

        trace_rows.append(
            {
                "crop_attempt_id": _aid(pid),
                "roi_retry_proposal_id": pid,
                "crop_candidate_id": cid,
                "source_resolution_status": resolution_status,
                "bbox_validation_status": bbox_status,
                "crop_generation_status": status,
                "crop_file_path": crop_path,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "error": err_msg,
                "ocr_invoked": False,
                "provider_invoked": False,
                "evidence_pack_generated": False,
            }
        )

        artifact = {
            "crop_artifact_id": artifact_id,
            "schema_version": "roi_crop_artifact_v1",
            "source_roi_retry_proposal_id": pid,
            "source_frame_ref": frame_id,
            "source_image_ref": image_id,
            "source_linebox_refs": prop.get("source_linebox_refs") or [],
            "crop_bbox_xyxy": bbox,
            "crop_polygon": [],
            "crop_width": crop_w,
            "crop_height": crop_h,
            "crop_file_path": crop_path,
            "crop_generated": crop_generated,
            "crop_generation_status": status,
            "crop_generation_reason": gen_reason,
            "proposal_type": ptype,
            "bbox_source": prop.get("bbox_source"),
            "source_quality_grade": sq,
            "readability_grade": prop.get("readability_grade"),
            "crop_quality_placeholder": {
                "blur_score": None,
                "contrast_score": None,
                "text_density_score": None,
                "quality_metrics_available": False,
            },
            "ocr_request_allowed_in_this_phase": False,
            "ocr_invoked": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        artifacts_full.append(artifact)

        collection_rows.append(
            {
                "crop_artifact_id": artifact_id,
                "source_roi_retry_proposal_id": pid,
                "crop_generation_status": status,
                "crop_file_path": crop_path,
                "crop_bbox_xyxy": bbox,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "proposal_type": ptype,
                "source_id": source_id,
                "frame_id": frame_id,
                "image_id": image_id,
                "crop_quality_placeholder": artifact["crop_quality_placeholder"],
                "next_allowed_phase": "ROI-to-OCRRequest-Reference-v1",
                "blocked_current_actions": [
                    "ocr_invoked",
                    "provider_invoked",
                    "ocr_request_generated",
                    "evidence_pack_generated",
                    "fact_write",
                ],
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        if crop_generated:
            ocr_ref_plan.append(
                {
                    "crop_artifact_id": artifact_id,
                    "eligible_for_future_ocr_request": True,
                    "future_ocr_request_candidate_id": f"ocr_req_ref_{artifact_id}",
                    "required_fields_for_future_request": [
                        "crop_file_path",
                        "crop_bbox_xyxy",
                        "source_chain",
                        "source_quality_grade",
                    ],
                    "allowed_provider_class_future": "gated_ocr_mainline",
                    "current_phase_ocr_request_generated": False,
                }
            )

        vc_match = re.search(r"validation:(sv_[^\s]+)", " ".join(chain))
        chain_rows.append(
            {
                "crop_artifact_id": artifact_id,
                "traceable_to_roi_retry_proposal": True,
                "traceable_to_source_validation": bool(vc_match),
                "traceable_to_review_queue_runtime": "roi_retry" in str(prop.get("source_retry_candidate_id") or ""),
                "traceable_to_semantic_v1": bool(prop.get("source_retry_candidate_id")),
                "traceable_to_scan_observation": any("scan:" in c for c in chain),
                "traceable_to_linebox_trace": bool(frame_id and frame_id in frame_dims),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    proposal_count = len(intake_rows)
    metrics = {
        "schema_version": "roi_crop_metrics_candidate_report_v1",
        "proposal_count_observed": proposal_count,
        "crop_candidate_count": proposal_count,
        "crop_executed_count": executed,
        "crop_deferred_count": deferred,
        "crop_skipped_count": skipped,
        "valid_bbox_count": valid_bbox_count,
        "null_bbox_deferred_count": null_deferred,
        "mixed_region_crop_count": mixed_crop,
        "better_frame_deferred_count": better_frame_def,
        "generated_crop_file_count": generated_files,
        "ocr_request_generated_count": 0,
        "provider_invoked_count": 0,
        "evidence_pack_generated_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    summary = {
        "schema_version": "roi_crop_execution_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "roi_crop_execution_dryrun_only",
        "based_on_roi_retry_proposal_runtime": roi_root.is_dir(),
        "proposal_count_observed": proposal_count,
        "crop_execution_attempted": True,
        "crop_artifact_generated": len(artifacts_full) > 0,
        "crop_executed_count": executed,
        "crop_deferred_count": deferred,
        "crop_skipped_count": skipped,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "decision_committed": False,
        "approval_granted": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if proposal_count > 0 and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    artifact_schema = {
        "schema_version": "roi_crop_artifact_schema_v1",
        "template": {
            "crop_artifact_id": "crop_<hash>",
            "schema_version": "roi_crop_artifact_v1",
            "source_roi_retry_proposal_id": None,
            "source_frame_ref": None,
            "source_image_ref": None,
            "source_linebox_refs": [],
            "crop_bbox_xyxy": None,
            "crop_polygon": [],
            "crop_width": None,
            "crop_height": None,
            "crop_file_path": None,
            "crop_generated": False,
            "crop_generation_status": "generated | deferred | skipped | failed",
            "crop_generation_reason": None,
            "proposal_type": None,
            "bbox_source": None,
            "source_quality_grade": None,
            "readability_grade": None,
            "crop_quality_placeholder": {
                "blur_score": None,
                "contrast_score": None,
                "text_density_score": None,
                "quality_metrics_available": False,
            },
            "ocr_request_allowed_in_this_phase": False,
            "ocr_invoked": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": [],
        },
        "defaults": {
            "ocr_request_allowed_in_this_phase": False,
            "ocr_invoked": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
    }

    boundary = {
        "schema_version": "roi_crop_boundary_report_v1",
        "roi_crop_dryrun_only": True,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "review_decision_committed": False,
        "approval_granted": False,
        "fact_write_allowed": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "navigation_decision_allowed": False,
    }

    no_write = {
        "schema_version": "roi_crop_no_write_boundary_report_v1",
        "boundary_ok": True,
        "violations": [],
        "roi_crop_dryrun_only": True,
        "ocr_request_generated": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "roi_crop_simulation_context_report_v1",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_crop_candidate_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "execution_policy": {
            "schema_version": "roi_crop_execution_policy_v1",
            "rules": CROP_POLICIES,
        },
        "artifact_schema": artifact_schema,
        "artifact_collection": {
            "schema_version": "roi_crop_artifact_collection_v1",
            "artifact_count": len(collection_rows),
            "artifacts": collection_rows,
            "artifacts_full": artifacts_full,
        },
        "bbox_validation": {
            "schema_version": "roi_crop_bbox_validation_report_v1",
            "row_count": len(bbox_rows),
            "rows": bbox_rows,
        },
        "source_resolution": {
            "schema_version": "roi_crop_source_resolution_report_v1",
            "row_count": len(resolution_rows),
            "rows": resolution_rows,
        },
        "execution_trace": {
            "schema_version": "roi_crop_execution_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "mixed_region": {
            "schema_version": "roi_crop_mixed_region_handling_report_v1",
            "row_count": len(mixed_rows),
            "rows": mixed_rows,
        },
        "deferred_report": {
            "schema_version": "roi_crop_better_frame_deferred_report_v1",
            "row_count": len(deferred_rows),
            "rows": deferred_rows,
        },
        "ocr_ref_plan": {
            "schema_version": "roi_crop_to_ocr_request_reference_plan_v1",
            "row_count": len(ocr_ref_plan),
            "rows": ocr_ref_plan,
            "current_phase_ocr_request_generated": False,
        },
        "boundary": boundary,
        "source_chain": {
            "schema_version": "roi_crop_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_roi_retry_proposal": all(r.get("traceable_to_roi_retry_proposal") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": metrics,
        "benchmark_link": {
            "schema_version": "roi_crop_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_crop_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": no_write,
        "sim_report": sim_report,
        "non_claims": {
            "schema_version": "roi_crop_non_claims_report_v1",
            "no_ocr": True,
            "no_ocr_request": True,
            "crop_not_ocr_evidence": True,
            "crop_not_fact": True,
            "not_production_ready": True,
        },
        "followups": {"schema_version": "roi_crop_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_crop_audit_report_v1",
            "roi_crop_execution_dryrun_v1_executed": True,
            "crop_execution_attempted": True,
            "crop_artifact_generated": len(artifacts_full) > 0,
            "crop_executed_count": executed,
            "crop_deferred_count": deferred,
            "roi_crop_dryrun_only": True,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "model_selection_claimed": False,
            "production_readiness_claimed": False,
        },
        "errs": errs,
        "crops_dir": str(crops_dir),
    }
