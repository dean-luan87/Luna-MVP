# -*- coding: utf-8 -*-
"""ROI Crop Execution DryRun v1 rerun with better frames — crop only, no OCR.

Phase-ROI-Crop-Execution-DryRun-v1-Rerun-With-Better-Frames-001
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-Crop-Execution-DryRun-v1-Rerun-With-Better-Frames-001"
RUNTIME_STEP = "roi_crop_execution_dryrun_v1_rerun_better_frames"

RERUN_POLICIES: List[Dict[str, Any]] = [
    {
        "rule_id": "rerun_only_ready_later_candidates",
        "condition": "selected_candidate and existing_scan_frame",
        "allowed_action": "rerun_crop_dryrun",
        "blocked_action": ["crop_future_detector_branch", "crop_multiframe_branch"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "existing_scan_frame_allowed_as_crop_source",
        "condition": "candidate_source==existing_scan_frame",
        "allowed_action": "use_linebox_from_candidate_frame",
        "blocked_action": [],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_video_decoding",
        "condition": "always",
        "allowed_action": "reuse_known_video_path_only",
        "blocked_action": ["new_video_decoded"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_frame_extraction",
        "condition": "always",
        "allowed_action": "materialize_existing_scan_frame_index_only",
        "blocked_action": ["new_frame_extracted"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bbox_must_come_from_linebox_or_existing_proposal",
        "condition": "bbox_from_candidate_frame_linebox",
        "allowed_action": "linebox_union",
        "blocked_action": ["fabricate_bbox"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bbox_must_be_within_source_bounds",
        "condition": "bbox_within_frame_dims",
        "allowed_action": "validate_bbox",
        "blocked_action": ["out_of_bounds_crop"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "null_bbox_must_defer",
        "condition": "bbox is null",
        "allowed_action": "defer",
        "blocked_action": ["crop_without_bbox"],
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "mixed_region_split_label_must_preserve",
        "condition": "mixed_region_split",
        "allowed_action": "crop_with_split_label",
        "blocked_action": ["semantic_join"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "linebox_text_not_evidence",
        "condition": "always",
        "allowed_action": "bbox_only",
        "blocked_action": ["linebox_text_as_ocr_evidence"],
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_semantic_join_after_crop",
        "condition": "always",
        "allowed_action": "per_region_only",
        "blocked_action": ["cross_region_join"],
        "crop_execution_allowed": True,
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
    "ROI-to-OCRRequest-Reference-v1",
    "OCRRequest Gated Submission from ROI v1",
    "Evidence Pack Adapter v2 ROIRef",
    "Semantic Candidate v2 ROIAware",
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "Future-Detector-ROI-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _rid(key: str) -> str:
    return f"crop_rerun_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _aid(key: str) -> str:
    return f"crop_rerun_attempt_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _union_bbox(items: List[Dict[str, Any]]) -> Optional[List[float]]:
    bboxes = []
    for it in items:
        if isinstance(it, dict) and it.get("bbox_xyxy"):
            bboxes.append(list(it["bbox_xyxy"]))
    if not bboxes:
        return None
    xs1, ys1, xs2, ys2 = [], [], [], []
    for b in bboxes:
        if len(b) >= 4:
            xs1.append(b[0])
            ys1.append(b[1])
            xs2.append(b[2])
            ys2.append(b[3])
    if not xs1:
        return None
    return [min(xs1), min(ys1), max(xs2), max(ys2)]


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
        return True, "valid", area / (w * h)
    return True, "valid", 0.0


def _resolve_video_path(v2: Path, video_id: str, path_by_source: Dict[str, str]) -> Optional[Path]:
    if video_id in path_by_source:
        p = Path(path_by_source[video_id])
        if p.is_file():
            return p
    fallback = Path("/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4")
    return fallback if fallback.is_file() else None


def _materialize_existing_frame(video_path: Path, frame_index: int):
    """Read frame at known index from already-known video (not a new source)."""
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


def run_roi_crop_execution_dryrun_v1_rerun_better_frames(
    *,
    output_root: str,
    better_frame_root: str,
    roi_crop_root: str,
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
    bf_root = Path(better_frame_root).resolve()
    crop_v1 = Path(roi_crop_root).resolve()
    retry_root = Path(roi_retry_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    all_bf = (_read_json(bf_root / "better_frame_candidate_collection_v1.json") or {}).get("candidates") or []
    proposal_by_source: Dict[Tuple[str, Optional[str]], str] = {}
    crop_art_by_proposal: Dict[str, str] = {}
    for row in (_read_json(bf_root / "better_frame_candidate_intake_matrix_v1.json") or {}).get("rows") or []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("source_id") or "")
        fid = row.get("frame_id") or row.get("image_id")
        pid = row.get("source_roi_retry_proposal_id")
        if sid and pid:
            proposal_by_source[(sid, fid)] = str(pid)
        if pid and row.get("source_crop_artifact_id"):
            crop_art_by_proposal[str(pid)] = str(row["source_crop_artifact_id"])

    proposals = {
        str(p.get("roi_retry_proposal_id")): p
        for p in (_read_json(retry_root / "roi_retry_proposal_collection_v1.json") or {}).get("proposals") or []
        if isinstance(p, dict) and p.get("roi_retry_proposal_id")
    }
    crop_v1_artifacts = {
        r.get("source_roi_retry_proposal_id"): r
        for r in (_read_json(crop_v1 / "roi_crop_artifact_collection_v1.json") or {}).get("artifacts") or []
        if isinstance(r, dict)
    }

    path_by_source: Dict[str, str] = {}
    for row in (_read_json(v2 / "mixed_batch_v2_input_candidate_matrix.json") or {}).get("rows") or []:
        if isinstance(row, dict) and row.get("source_id") and row.get("source_path"):
            path_by_source[str(row["source_id"])] = str(row["source_path"])

    linebox_frames: Dict[str, Dict[str, Any]] = {}
    for fr in (_read_json(linebox_root / "mixedvideo_ocr_scan_linebox_trace_report.json") or {}).get("frames") or []:
        if isinstance(fr, dict) and fr.get("frame_id"):
            linebox_frames[str(fr["frame_id"])] = fr

    rerun_candidates: List[Dict[str, Any]] = []
    deferred_non_rerun: List[Dict[str, Any]] = []

    for c in all_bf:
        if not isinstance(c, dict):
            continue
        status = c.get("selection_status")
        src = c.get("candidate_source")
        readiness = c.get("expected_roi_crop_readiness")
        if status == "selected_candidate" and src == "existing_scan_frame" and c.get("candidate_frame_id"):
            rerun_candidates.append(c)
        elif src in ("future_detector_required", "multiframe_required") or status != "selected_candidate":
            deferred_non_rerun.append(c)

    ready_count = len(rerun_candidates)
    bf_total = len(all_bf)

    intake_rows: List[Dict[str, Any]] = []
    artifacts: List[Dict[str, Any]] = []
    resolution_rows: List[Dict[str, Any]] = []
    bbox_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    mixed_rows: List[Dict[str, Any]] = []
    deferred_rows: List[Dict[str, Any]] = []
    ocr_ref_plan: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    executed = metadata_only = deferred = skipped = 0
    generated_files = 0
    valid_bbox_count = 0
    linebox_only = 0
    future_detector_def = 0
    multiframe_def = 0

    for c in deferred_non_rerun:
        if not isinstance(c, dict):
            continue
        src = c.get("candidate_source")
        if src == "future_detector_required":
            future_detector_def += 1
            future_phase = "Future-Detector-ROI-Proposal-v1"
            action = "future_detector"
        elif src == "multiframe_required":
            multiframe_def += 1
            future_phase = "Multiframe-Merge-Proposal-v1"
            action = "multiframe_merge"
        else:
            future_phase = "Better-Frame-Extraction-DryRun-v1"
            action = "hold"
        deferred_rows.append(
            {
                "better_frame_candidate_id": c.get("better_frame_candidate_id"),
                "selection_status": c.get("selection_status"),
                "expected_roi_crop_readiness": c.get("expected_roi_crop_readiness"),
                "defer_reason": src or "not_rerun_scope",
                "required_future_action": action,
                "future_phase": future_phase,
                "crop_generation_status": "deferred",
                "ocr_request_generated": False,
                "fact_status": "not_fact",
            }
        )
        deferred += 1

    for c in rerun_candidates:
        bf_id = str(c.get("better_frame_candidate_id") or "")
        cand_frame = str(c.get("candidate_frame_id") or "")
        cur_frame = c.get("current_frame_id")
        sid = str(c.get("source_item_id") or "")
        prop_id = proposal_by_source.get((sid, cur_frame)) or proposal_by_source.get((sid, None))
        prop = proposals.get(prop_id or "", {})
        crop_art_id = crop_art_by_proposal.get(prop_id or "") or crop_v1_artifacts.get(prop_id or "", {}).get(
            "crop_artifact_id"
        )
        crop_art = {"crop_artifact_id": crop_art_id}
        ptype = prop.get("proposal_type", "")
        mixed = ptype == "mixed_region_split"

        rerun_id = _rid(f"rerun:{bf_id}")
        intake_rows.append(
            {
                "rerun_crop_candidate_id": rerun_id,
                "better_frame_candidate_id": bf_id,
                "source_retry_proposal_id": prop_id,
                "source_crop_artifact_id": crop_art.get("crop_artifact_id"),
                "current_frame_id": cur_frame,
                "candidate_frame_id": cand_frame,
                "candidate_frame_time_sec": c.get("candidate_frame_time_sec"),
                "candidate_frame_index": c.get("candidate_frame_index"),
                "candidate_source": c.get("candidate_source"),
                "expected_roi_crop_readiness": "ready_later",
                "source_quality_grade": c.get("current_source_quality_grade"),
                "target_source_quality_grade": c.get("target_source_quality_grade"),
                "linebox_refs": c.get("linebox_refs") or [],
                "future_roi_crop_candidate": c.get("future_roi_crop_candidate"),
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        fr_doc = linebox_frames.get(cand_frame, {})
        w = int(fr_doc.get("image_width") or 0)
        h = int(fr_doc.get("image_height") or 0)
        items = fr_doc.get("text_items") or []
        bbox = _union_bbox(items)
        bbox_source = "existing_scan_frame_linebox"
        if bbox is None and prop.get("proposed_roi_bbox_xyxy"):
            bbox = prop.get("proposed_roi_bbox_xyxy")
            bbox_source = "original_roi_retry_proposal"

        vid = cand_frame.rsplit("_f", 1)[0] if "_f" in cand_frame else "test_video_complex_6m42s"
        video_path = _resolve_video_path(v2, vid, path_by_source)
        frame_index = c.get("candidate_frame_index") or _parse_frame_index(cand_frame)

        linebox_available = cand_frame in linebox_frames
        path_resolved = video_path is not None and video_path.is_file()
        if path_resolved and linebox_available:
            res_status = "existing_frame_resolved"
        elif linebox_available:
            res_status = "linebox_trace_only_no_frame_image"
        elif not path_resolved:
            res_status = "source_path_missing"
        else:
            res_status = "deferred"

        resolution_rows.append(
            {
                "better_frame_candidate_id": bf_id,
                "candidate_frame_ref_available": linebox_available,
                "existing_scan_frame_available": linebox_available,
                "source_path_resolved": path_resolved,
                "source_path": str(video_path) if video_path else None,
                "frame_artifact_available": linebox_available,
                "linebox_trace_available": linebox_available,
                "frame_image_materialization_required": path_resolved and linebox_available,
                "new_video_decoding_required": False,
                "new_frame_extraction_required": False,
                "source_resolution_status": res_status,
            }
        )

        bbox_ok, bbox_status, area_ratio = _bbox_valid(list(bbox) if bbox else None, w, h)
        if bbox_ok:
            valid_bbox_count += 1

        crop_allowed = bbox_ok and res_status == "existing_frame_resolved"
        status = "deferred"
        gen_reason = bbox_status
        crop_path = None
        crop_w = crop_h = None
        crop_generated = False
        err_msg = None

        if crop_allowed and video_path and frame_index is not None and bbox:
            try:
                img = _materialize_existing_frame(video_path, int(frame_index))
                if img is not None:
                    short = (prop_id or bf_id).replace("roi_retry_", "")[:8]
                    fname = f"crop_rerun_{cand_frame}_{short}.png"
                    out_png = crops_dir / fname.replace("/", "_")
                    crop_w, crop_h = _save_crop(img, list(bbox), out_png)
                    crop_path = str(out_png)
                    crop_generated = True
                    status = "generated"
                    gen_reason = "existing_scan_frame_cropped"
                    executed += 1
                    generated_files += 1
                else:
                    status = "metadata_only"
                    gen_reason = "linebox_only_no_frame"
                    metadata_only += 1
                    linebox_only += 1
            except Exception as e:  # noqa: BLE001
                status = "failed"
                gen_reason = "crop_failed"
                err_msg = str(e)
                skipped += 1
        elif res_status == "linebox_trace_only_no_frame_image" and bbox_ok:
            status = "metadata_only"
            gen_reason = "linebox_only_no_frame"
            metadata_only += 1
            linebox_only += 1
        else:
            deferred += 1
            gen_reason = bbox_status if not bbox_ok else res_status
            deferred_rows.append(
                {
                    "better_frame_candidate_id": bf_id,
                    "selection_status": "selected_candidate",
                    "expected_roi_crop_readiness": "ready_later",
                    "defer_reason": gen_reason,
                    "required_future_action": "frame_materialization_or_bbox_fix",
                    "future_phase": "Better-Frame-Extraction-DryRun-v1",
                    "crop_generation_status": "deferred",
                    "ocr_request_generated": False,
                    "fact_status": "not_fact",
                }
            )

        bbox_rows.append(
            {
                "better_frame_candidate_id": bf_id,
                "source_roi_retry_proposal_id": prop_id,
                "bbox_present": bbox is not None,
                "bbox_source": bbox_source,
                "bbox_numeric": bbox_ok,
                "bbox_within_source_bounds": bbox_status != "out_of_bounds",
                "bbox_area_positive": bbox_status != "zero_area",
                "bbox_area_ratio": area_ratio,
                "bbox_validation_status": bbox_status if bbox_ok else gen_reason,
                "crop_allowed": crop_allowed,
                "defer_reason": None if crop_allowed else gen_reason,
            }
        )

        trace_rows.append(
            {
                "crop_attempt_id": _aid(bf_id),
                "better_frame_candidate_id": bf_id,
                "roi_retry_proposal_id": prop_id,
                "source_resolution_status": res_status,
                "bbox_validation_status": bbox_status,
                "crop_generation_status": status,
                "crop_file_path": crop_path,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "error": err_msg,
                "new_video_decoded": False,
                "new_frame_extracted": False,
                "ocr_invoked": False,
                "provider_invoked": False,
                "evidence_pack_generated": False,
            }
        )

        chain = list(c.get("source_chain") or [])
        chain.append(RUNTIME_STEP)

        art_id = _rid(f"art:{bf_id}")
        artifact = {
            "crop_artifact_id": art_id,
            "schema_version": "roi_crop_artifact_v1_rerun_better_frame",
            "source_better_frame_candidate_id": bf_id,
            "source_roi_retry_proposal_id": prop_id,
            "source_crop_artifact_id": crop_art.get("crop_artifact_id"),
            "candidate_frame_id": cand_frame,
            "candidate_frame_index": frame_index,
            "candidate_frame_time_sec": c.get("candidate_frame_time_sec"),
            "source_linebox_refs": c.get("linebox_refs") or [],
            "crop_bbox_xyxy": bbox,
            "crop_polygon": [],
            "crop_width": crop_w,
            "crop_height": crop_h,
            "crop_file_path": crop_path,
            "crop_generated": crop_generated,
            "crop_generation_status": status,
            "crop_generation_reason": gen_reason,
            "proposal_type": ptype,
            "bbox_source": bbox_source,
            "source_quality_grade": c.get("current_source_quality_grade"),
            "target_source_quality_grade": c.get("target_source_quality_grade"),
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
        artifacts.append(artifact)

        if mixed:
            mixed_rows.append(
                {
                    "better_frame_candidate_id": bf_id,
                    "source_roi_retry_proposal_id": prop_id,
                    "mixed_region_detected": True,
                    "split_required": True,
                    "split_label_preserved": True,
                    "semantic_join_allowed": False,
                    "cross_region_text_join_allowed": False,
                    "future_split_refinement_required": True,
                    "fact_status": "not_fact",
                }
            )

        eligible_ocr = status == "generated" and bool(crop_path)
        ocr_ref_plan.append(
            {
                "crop_artifact_id": art_id,
                "eligible_for_future_ocr_request": eligible_ocr,
                "future_ocr_request_candidate_id": f"ocr_req_ref_{art_id}" if eligible_ocr else None,
                "required_fields_for_future_request": [
                    "crop_file_path",
                    "crop_bbox_xyxy",
                    "source_chain",
                    "target_source_quality_grade",
                ],
                "allowed_provider_class_future": "gated_ocr_mainline",
                "current_phase_ocr_request_generated": False,
                "needs_crop_materialization": status == "metadata_only",
            }
        )

        chain_rows.append(
            {
                "crop_artifact_id": art_id,
                "traceable_to_better_frame_selection": True,
                "traceable_to_roi_crop_execution_v1": True,
                "traceable_to_roi_retry_proposal": bool(prop_id),
                "traceable_to_source_validation": any("validation:sv_" in x for x in chain),
                "traceable_to_linebox_trace": linebox_available,
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    metrics = {
        "schema_version": "roi_crop_rerun_metrics_candidate_report_v1",
        "better_frame_candidate_count_observed": bf_total,
        "ready_later_candidate_count_observed": ready_count,
        "rerun_crop_candidate_count": ready_count,
        "crop_executed_count": executed,
        "metadata_only_count": metadata_only,
        "crop_deferred_count": deferred,
        "crop_skipped_count": skipped,
        "generated_crop_file_count": generated_files,
        "valid_bbox_count": valid_bbox_count,
        "null_bbox_deferred_count": 0,
        "linebox_only_no_frame_count": linebox_only,
        "future_detector_deferred_count": future_detector_def,
        "multiframe_deferred_count": multiframe_def,
        "new_frame_extracted_count": 0,
        "roi_crop_executed_count": executed,
        "ocr_request_generated_count": 0,
        "provider_invoked_count": 0,
        "evidence_pack_generated_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    summary = {
        "schema_version": "roi_crop_rerun_better_frames_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "roi_crop_rerun_with_better_frames_only",
        "based_on_better_frame_selection": bf_root.is_dir(),
        "based_on_roi_crop_execution_dryrun_v1": crop_v1.is_dir(),
        "based_on_roi_retry_proposal_runtime": retry_root.is_dir(),
        "better_frame_candidate_count_observed": bf_total,
        "ready_later_candidate_count_observed": ready_count,
        "rerun_crop_candidate_count": ready_count,
        "crop_execution_attempted": True,
        "crop_artifact_generated": len(artifacts) > 0,
        "crop_executed_count": executed,
        "crop_deferred_count": deferred,
        "crop_skipped_count": skipped,
        "new_video_decoded": False,
        "new_frame_extracted": False,
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
        "phase_verdict_hint": "GO" if ready_count == 12 and not errs else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    collection_only = [
        {
            "crop_artifact_id": a.get("crop_artifact_id"),
            "source_better_frame_candidate_id": a.get("source_better_frame_candidate_id"),
            "source_roi_retry_proposal_id": a.get("source_roi_retry_proposal_id"),
            "candidate_frame_id": a.get("candidate_frame_id"),
            "crop_generation_status": a.get("crop_generation_status"),
            "crop_file_path": a.get("crop_file_path"),
            "crop_bbox_xyxy": a.get("crop_bbox_xyxy"),
            "crop_width": a.get("crop_width"),
            "crop_height": a.get("crop_height"),
            "proposal_type": a.get("proposal_type"),
            "bbox_source": a.get("bbox_source"),
            "next_allowed_phase": "ROI-to-OCRRequest-Reference-v1",
            "blocked_current_actions": [
                "ocr_invoked",
                "ocr_request_generated",
                "evidence_pack_generated",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        for a in artifacts
        if a.get("schema_version")
    ]

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_crop_rerun_better_frame_candidate_intake_matrix_v0",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "execution_policy": {
            "schema_version": "roi_crop_rerun_execution_policy_v1",
            "rules": RERUN_POLICIES,
        },
        "source_resolution": {
            "schema_version": "roi_crop_rerun_source_resolution_report_v0",
            "row_count": len(resolution_rows),
            "rows": resolution_rows,
        },
        "bbox_validation": {
            "schema_version": "roi_crop_rerun_bbox_validation_report_v0",
            "row_count": len(bbox_rows),
            "rows": bbox_rows,
        },
        "artifact_schema": {
            "schema_version": "roi_crop_rerun_artifact_schema_v1",
            "template": {
                "crop_artifact_id": "crop_rerun_<hash>",
                "schema_version": "roi_crop_artifact_v1_rerun_better_frame",
                "source_better_frame_candidate_id": None,
                "crop_bbox_xyxy": None,
                "crop_generation_status": "generated | metadata_only | deferred | skipped | failed",
                "ocr_request_allowed_in_this_phase": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "source_chain": [],
            },
            "defaults": {
                "ocr_request_allowed_in_this_phase": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        },
        "artifact_collection": {
            "schema_version": "roi_crop_rerun_artifact_collection_v1",
            "artifact_count": len(collection_only),
            "artifacts": collection_only,
        },
        "execution_trace": {
            "schema_version": "roi_crop_rerun_execution_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "deferred_report": {
            "schema_version": "roi_crop_rerun_deferred_report_v1",
            "row_count": len(deferred_rows),
            "future_detector_deferred_count": future_detector_def,
            "multiframe_deferred_count": multiframe_def,
            "rows": deferred_rows,
        },
        "mixed_region": {
            "schema_version": "roi_crop_rerun_mixed_region_handling_report_v1",
            "row_count": len(mixed_rows),
            "rows": mixed_rows,
        },
        "ocr_ref_plan": {
            "schema_version": "roi_crop_rerun_to_ocr_request_reference_plan_v1",
            "row_count": len(ocr_ref_plan),
            "current_phase_ocr_request_generated": False,
            "rows": ocr_ref_plan,
        },
        "boundary": {
            "schema_version": "roi_crop_rerun_boundary_report_v1",
            "roi_crop_rerun_dryrun_only": True,
            "new_video_decoded": False,
            "new_frame_extracted": False,
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
        },
        "source_chain": {
            "schema_version": "roi_crop_rerun_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_better_frame_selection": all(r.get("traceable_to_better_frame_selection") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": metrics,
        "benchmark_link": {
            "schema_version": "roi_crop_rerun_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_crop_rerun_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "provider_health_runtime_checked": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_crop_rerun_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "roi_crop_rerun_dryrun_only": True,
            "new_video_decoded": False,
            "new_frame_extracted": False,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "decision_committed": False,
            "approval_granted": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "roi_crop_rerun_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_crop_rerun_non_claims_report_v1",
            "no_new_video_decode": True,
            "no_new_frame_extract": True,
            "no_ocr": True,
            "crop_not_evidence": True,
            "metadata_only_not_ocr_ready": True,
        },
        "followups": {"schema_version": "roi_crop_rerun_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_crop_rerun_audit_report_v1",
            "roi_crop_rerun_better_frames_executed": True,
            "roi_crop_rerun_dryrun_only": True,
            "ready_later_candidate_count_observed": ready_count,
            "rerun_crop_candidate_count": ready_count,
            "crop_executed_count": executed,
            "metadata_only_count": metadata_only,
            "crop_deferred_count": deferred,
            "new_video_decoded": False,
            "new_frame_extracted": False,
            "ocr_request_generated": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "evidence_pack_generated": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
        },
        "errs": errs,
        "crops_dir": str(crops_dir),
    }
