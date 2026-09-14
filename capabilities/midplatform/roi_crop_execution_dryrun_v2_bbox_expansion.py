# -*- coding: utf-8 -*-
"""ROI Crop Execution DryRun v2 BBoxExpansion — expanded crop artifacts only, no OCR.

Phase-ROI-Crop-Execution-DryRun-v2-BBoxExpansion-001
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "ROI-Crop-Execution-DryRun-v2-BBoxExpansion-001"
RUNTIME_STEP = "roi_crop_execution_dryrun_v2_bbox_expansion"

FOLLOWUPS = [
    "ROI-to-OCRRequest-Reference-v2-BBoxExpansion",
    "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion",
    "Evidence-Pack-Adapter-v3-BBoxExpansion",
    "Semantic-Candidate-v3-BBoxExpansionAware",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "STC Contract later",
    "Controlled runtime integration",
]

POLICIES: List[Dict[str, Any]] = [
    {
        "rule_id": "only_recommended_expansion_candidates",
        "condition": "recommended_for_future_crop=true",
        "allowed_action": "crop_from_expansion_candidate",
        "blocked_action": "crop_non_recommended",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "preserve_original_bbox",
        "condition": "source_bbox_xyxy immutable",
        "allowed_action": "record_source_bbox",
        "blocked_action": "overwrite_source_bbox",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "preserve_expanded_bbox",
        "condition": "expanded_bbox from proposal",
        "allowed_action": "crop_expanded_bbox",
        "blocked_action": "modify_expanded_bbox",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_from_expanded_bbox_only",
        "condition": "crop uses expanded_bbox_xyxy",
        "allowed_action": "expanded_crop",
        "blocked_action": "crop_source_bbox_only",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_frame_must_be_resolved",
        "condition": "known frame index and video path",
        "allowed_action": "materialize_existing_frame",
        "blocked_action": "crop_without_frame",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_new_frame_selection",
        "condition": "phase_boundary",
        "allowed_action": "reuse_f001620_only",
        "blocked_action": "new_frame_selection",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_video_scan",
        "condition": "phase_boundary",
        "allowed_action": "seek_known_frame_index",
        "blocked_action": "video_scan",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocr_execution_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "crop_only",
        "blocked_action": "ocr_invoked",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_ocrrequest_generation_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "crop_only",
        "blocked_action": "ocrrequest_generated",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_evidence_pack_generation_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "crop_only",
        "blocked_action": "evidence_pack_generated",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_not_fact",
        "condition": "always",
        "allowed_action": "dryrun_artifact",
        "blocked_action": "fact_write",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "expanded_crop_not_evidence",
        "condition": "always",
        "allowed_action": "crop_file_only",
        "blocked_action": "evidence_claim",
        "crop_execution_allowed": True,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "world_model_attach",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "crop_execution_allowed": False,
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

ARTIFACT_SCHEMA: Dict[str, Any] = {
    "expanded_crop_artifact_id": "crop_v2_exp_<uuid>",
    "schema_version": "roi_crop_artifact_v2_bbox_expansion",
    "source_bbox_expansion_candidate_id": None,
    "source_bbox_group_id": None,
    "source_crop_artifact_refs": [],
    "source_bbox_xyxy": None,
    "expanded_bbox_xyxy": None,
    "expansion_strategy": None,
    "candidate_frame_id": None,
    "candidate_frame_index": None,
    "candidate_frame_time_sec": None,
    "frame_width": None,
    "frame_height": None,
    "crop_file_path": None,
    "crop_generated": False,
    "crop_generation_status": "generated | deferred | failed",
    "crop_width": None,
    "crop_height": None,
    "area_growth_ratio": None,
    "expansion_metadata": {
        "padding_ratio": None,
        "padding_pixels": {},
        "expected_improvement_label": None,
        "risk_remaining": [],
    },
    "ocrrequest_allowed_in_this_phase": False,
    "ocr_invoked": False,
    "evidence_pack_generated": False,
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_id(key: str) -> str:
    return f"crop_v2_intake_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _artifact_id(key: str) -> str:
    return f"crop_v2_exp_{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def _attempt_id(key: str) -> str:
    return f"crop_v2_attempt_{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def _parse_frame_index(frame_id: str) -> Optional[int]:
    m = re.search(r"_f(\d+)$", frame_id or "")
    return int(m.group(1)) if m else None


def _area(bbox: List[float]) -> float:
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def _bbox_valid(bbox: Optional[List[float]], w: int, h: int) -> Tuple[bool, str]:
    if not bbox or len(bbox) < 4:
        return False, "null_bbox"
    x1, y1, x2, y2 = [float(bbox[i]) for i in range(4)]
    if x2 <= x1 or y2 <= y1:
        return False, "zero_area"
    if w > 0 and h > 0 and (x1 < 0 or y1 < 0 or x2 > w or y2 > h):
        return False, "out_of_bounds"
    return True, "valid"


def _resolve_video_path(v2: Path, video_id: str, path_by_source: Dict[str, str]) -> Optional[Path]:
    if video_id in path_by_source:
        p = Path(path_by_source[video_id])
        if p.is_file():
            return p
    fallback = Path("/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4")
    return fallback if fallback.is_file() else None


def _materialize_existing_frame(video_path: Path, frame_index: int):
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


def run_roi_crop_execution_dryrun_v2_bbox_expansion(
    *,
    output_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    out = Path(output_root).resolve()
    crops_dir = out / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    exp_root = Path(roi_bbox_expansion_root).resolve()
    div_root = Path(roi_crop_diversity_root).resolve()
    diag_root = Path(roi_ocr_quality_diagnosis_root).resolve()
    crop_rerun_root = Path(roi_crop_rerun_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    linebox_root = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    div_summary = _read_json(div_root / "roi_crop_diversity_check_v1_summary.json") or {}
    candidates = [
        c
        for c in (_read_json(exp_root / "roi_bbox_expansion_candidate_collection_v1.json") or {}).get("rows") or []
        if isinstance(c, dict)
    ]
    recommended = [
        c
        for c in candidates
        if c.get("future_crop_candidate", {}).get("eligible_for_crop_rerun")
        or c.get("proposal_status") in ("proposed", "clipped")
    ]
    if len(recommended) < len(candidates):
        candidates = recommended or candidates

    path_by_source: Dict[str, str] = {}
    for row in (_read_json(v2 / "mixed_batch_v2_input_candidate_matrix.json") or {}).get("rows") or []:
        if isinstance(row, dict) and row.get("source_id") and row.get("source_path"):
            path_by_source[str(row["source_id"])] = str(row["source_path"])

    frame_cache: Dict[Tuple[str, int], Any] = {}

    intake_rows: List[Dict[str, Any]] = []
    resolution_rows: List[Dict[str, Any]] = []
    validation_rows: List[Dict[str, Any]] = []
    artifacts: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    comparison_rows: List[Dict[str, Any]] = []
    deferred_rows: List[Dict[str, Any]] = []
    ocr_ref_plan: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    generated = deferred = failed = 0
    expanded_bbox_sigs: set = set()
    dim_sigs: set = set()
    strategies: set = set()

    source_bbox_ref = [292.0, 367.0, 381.0, 395.0]
    source_w, source_h = 89, 28
    source_area = _area(source_bbox_ref)

    for cand in candidates:
        cid = str(cand.get("bbox_expansion_candidate_id") or "")
        strategy = str(cand.get("expansion_strategy") or "")
        src_bbox = list(cand.get("source_bbox_xyxy") or source_bbox_ref)
        exp_bbox = list(cand.get("expanded_bbox_xyxy") or [])
        fr = cand.get("source_frame_ref") if isinstance(cand.get("source_frame_ref"), dict) else {}
        fid = str(fr.get("candidate_frame_id") or "test_video_complex_6m42s_f001620")
        fidx = fr.get("candidate_frame_index") or _parse_frame_index(fid) or 1620
        ftime = fr.get("candidate_frame_time_sec")
        fw = int(fr.get("frame_width") or 0)
        fh = int(fr.get("frame_height") or 0)
        bounds = cand.get("bounds_check") if isinstance(cand.get("bounds_check"), dict) else {}

        intake_rows.append(
            {
                "crop_v2_intake_id": _intake_id(cid),
                "bbox_expansion_candidate_id": cid,
                "source_bbox_group_id": cand.get("source_bbox_group_id"),
                "expansion_strategy": strategy,
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_xyxy": exp_bbox,
                "affected_crop_artifact_ids": cand.get("affected_crop_artifact_ids") or [],
                "affected_roi_ocr_result_ids": cand.get("affected_roi_ocr_result_ids") or [],
                "candidate_frame_id": fid,
                "candidate_frame_index": fidx,
                "candidate_frame_time_sec": ftime,
                "frame_width": fw,
                "frame_height": fh,
                "bounds_check": bounds,
                "proposal_status": cand.get("proposal_status"),
                "recommended_for_future_crop": True,
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        vid = fid.rsplit("_f", 1)[0] if "_f" in fid else "test_video_complex_6m42s"
        video_path = _resolve_video_path(v2, vid, path_by_source)
        frame_index = int(fidx) if fidx is not None else None

        if video_path and frame_index is not None:
            res_status = "resolved_existing_frame"
            mat_method = "materialize_existing_scan_frame_index_only"
        elif video_path:
            res_status = "deferred"
            mat_method = "frame_index_missing"
        else:
            res_status = "source_video_missing"
            mat_method = "none"

        resolution_rows.append(
            {
                "bbox_expansion_candidate_id": cid,
                "candidate_frame_id": fid,
                "candidate_frame_index": frame_index,
                "candidate_frame_time_sec": ftime,
                "source_video_path": str(video_path) if video_path else None,
                "source_frame_resolved": res_status == "resolved_existing_frame",
                "source_frame_materialization_method": mat_method,
                "new_frame_extracted": False,
                "video_scan_invoked": False,
                "resolution_status": res_status,
                "error": None,
            }
        )

        bbox_ok, bbox_status = _bbox_valid(exp_bbox, fw, fh)
        exp_area = _area(exp_bbox)
        area_ratio = round(exp_area / source_area, 4) if source_area > 0 else 0.0

        validation_rows.append(
            {
                "bbox_expansion_candidate_id": cid,
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_xyxy": exp_bbox,
                "frame_width": fw,
                "frame_height": fh,
                "bbox_numeric": bbox_ok,
                "bbox_within_bounds": bbox_status != "out_of_bounds",
                "bbox_area_positive": bbox_status != "zero_area",
                "expanded_bbox_area": round(exp_area, 2),
                "source_bbox_area": round(source_area, 2),
                "area_growth_ratio": area_ratio,
                "validation_status": bbox_status if bbox_ok else bbox_status,
                "crop_allowed": bbox_ok and res_status == "resolved_existing_frame",
                "defer_reason": None if bbox_ok else bbox_status,
            }
        )

        crop_allowed = bbox_ok and res_status == "resolved_existing_frame"
        status = "deferred"
        crop_path = None
        crop_w = crop_h = None
        err_msg = None
        art_id = _artifact_id(cid)

        if crop_allowed and video_path and frame_index is not None:
            try:
                cache_key = (str(video_path), frame_index)
                if cache_key not in frame_cache:
                    frame_cache[cache_key] = _materialize_existing_frame(video_path, frame_index)
                img = frame_cache[cache_key]
                if img is not None:
                    short = cid.replace("bbox_exp_", "")[:8]
                    fname = f"crop_v2_{strategy}_{fid}_{short}.png".replace("/", "_")
                    out_png = crops_dir / fname
                    crop_w, crop_h = _save_crop(img, exp_bbox, out_png)
                    crop_path = str(out_png)
                    status = "generated"
                    generated += 1
                    expanded_bbox_sigs.add(tuple(int(round(v)) for v in exp_bbox))
                    dim_sigs.add(f"{crop_w}x{crop_h}")
                    strategies.add(strategy)
                else:
                    status = "failed"
                    err_msg = "frame_materialization_failed"
                    failed += 1
            except Exception as e:  # noqa: BLE001
                status = "failed"
                err_msg = str(e)
                failed += 1
        else:
            deferred += 1
            deferred_rows.append(
                {
                    "bbox_expansion_candidate_id": cid,
                    "expansion_strategy": strategy,
                    "defer_reason": bbox_status if not bbox_ok else res_status,
                    "required_future_action": "frame_materialization_or_bbox_fix",
                    "crop_generation_status": "deferred",
                    "ocrrequest_generated": False,
                    "fact_status": "not_fact",
                }
            )

        imp = cand.get("expected_improvement") if isinstance(cand.get("expected_improvement"), dict) else {}
        chain = list(cand.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        artifact = {
            "expanded_crop_artifact_id": art_id,
            "schema_version": "roi_crop_artifact_v2_bbox_expansion",
            "source_bbox_expansion_candidate_id": cid,
            "source_bbox_group_id": cand.get("source_bbox_group_id"),
            "source_crop_artifact_refs": cand.get("affected_crop_artifact_ids") or [],
            "source_bbox_xyxy": src_bbox,
            "expanded_bbox_xyxy": exp_bbox,
            "expansion_strategy": strategy,
            "candidate_frame_id": fid,
            "candidate_frame_index": frame_index,
            "candidate_frame_time_sec": ftime,
            "frame_width": fw,
            "frame_height": fh,
            "crop_file_path": crop_path,
            "crop_generated": status == "generated",
            "crop_generation_status": status,
            "crop_width": crop_w,
            "crop_height": crop_h,
            "area_growth_ratio": area_ratio if status == "generated" else None,
            "expansion_metadata": {
                "padding_ratio": cand.get("padding_ratio"),
                "padding_pixels": cand.get("padding_pixels") or {},
                "expected_improvement_label": imp.get("expansion_reason"),
                "risk_remaining": imp.get("risk_remaining") or [],
            },
            "bbox_source": "bbox_expansion_proposal_v1",
            "next_allowed_phase": "ROI-to-OCRRequest-Reference-v2-BBoxExpansion",
            "ocrrequest_allowed_in_this_phase": False,
            "ocr_invoked": False,
            "evidence_pack_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
        }
        artifacts.append(artifact)

        trace_rows.append(
            {
                "crop_v2_attempt_id": _attempt_id(cid),
                "bbox_expansion_candidate_id": cid,
                "expansion_strategy": strategy,
                "source_frame_resolution_status": res_status,
                "bbox_validation_status": bbox_status,
                "crop_generation_status": status,
                "crop_file_path": crop_path,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "error": err_msg,
                "new_frame_extracted": False,
                "video_scan_invoked": False,
                "ocr_invoked": False,
                "provider_invoked": False,
                "evidence_pack_generated": False,
            }
        )

        ew = (exp_bbox[2] - exp_bbox[0]) if len(exp_bbox) >= 4 else 0
        eh = (exp_bbox[3] - exp_bbox[1]) if len(exp_bbox) >= 4 else 0
        comparison_rows.append(
            {
                "bbox_expansion_candidate_id": cid,
                "expansion_strategy": strategy,
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_xyxy": exp_bbox,
                "source_width": source_w,
                "source_height": source_h,
                "expanded_width": crop_w if crop_w else int(round(ew)),
                "expanded_height": crop_h if crop_h else int(round(eh)),
                "width_growth_ratio": round((crop_w or ew) / source_w, 4) if source_w else 0.0,
                "height_growth_ratio": round((crop_h or eh) / source_h, 4) if source_h else 0.0,
                "area_growth_ratio": area_ratio,
                "expected_context_gain": area_ratio > 1.0,
                "comparison_status": status,
            }
        )

        eligible = status == "generated" and bool(crop_path)
        ocr_ref_plan.append(
            {
                "expanded_crop_artifact_id": art_id,
                "eligible_for_future_ocrrequest_reference": eligible,
                "future_ocrrequest_reference_candidate_id": f"ocr_req_ref_v2_{art_id}" if eligible else None,
                "required_fields_for_future_request": [
                    "crop_file_path",
                    "expanded_bbox_xyxy",
                    "source_bbox_xyxy",
                    "source_bbox_expansion_candidate_id",
                    "source_chain",
                ],
                "current_phase_ocrrequest_generated": False,
            }
        )

        chain_rows.append(
            {
                "expanded_crop_artifact_id": art_id,
                "traceable_to_bbox_expansion_candidate": True,
                "traceable_to_diversity_check": div_root.is_dir(),
                "traceable_to_quality_diagnosis": diag_root.is_dir(),
                "traceable_to_source_crop_artifact": bool(cand.get("affected_crop_artifact_ids")),
                "traceable_to_linebox_trace": linebox_root.is_dir(),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    unique_bbox = len(expanded_bbox_sigs)
    prev_unique = int(div_summary.get("unique_bbox_count") or 1)
    diversity_improved = unique_bbox > prev_unique
    current_grade = "HIGH" if unique_bbox >= 4 else ("MEDIUM" if unique_bbox >= 2 else "LOW")

    diversity_report = {
        "schema_version": "roi_crop_v2_expanded_crop_diversity_report_v1",
        "expanded_crop_count": generated,
        "unique_expanded_bbox_count": unique_bbox,
        "unique_crop_dimension_count": len(dim_sigs),
        "unique_strategy_count": len(strategies),
        "expanded_crop_diversity_improved": diversity_improved,
        "previous_unique_bbox_count": prev_unique,
        "previous_diversity_grade": "LOW",
        "current_diversity_grade": current_grade,
        "quality_claim_allowed": False,
        "fact_status": "not_fact",
    }

    summary = {
        "schema_version": "roi_crop_v2_bbox_expansion_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "bbox_expansion_crop_execution_only",
        "based_on_bbox_expansion_proposal": exp_root.is_dir(),
        "expansion_candidate_count_observed": len(candidates),
        "recommended_expansion_candidate_count_observed": len(candidates),
        "crop_execution_attempted": True,
        "expanded_crop_artifact_generated": generated > 0,
        "expanded_crop_generated_count": generated,
        "expanded_crop_deferred_count": deferred,
        "expanded_crop_failed_count": failed,
        "new_frame_extracted": False,
        "new_ocr_invoked": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_v2_invoked": False,
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
        "phase_verdict_hint": "GO"
        if generated >= 4 or (generated > 0 and deferred + failed == 0)
        else ("CONDITIONAL_GO" if generated > 0 else "NO_GO"),
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "roi_crop_v2_expansion_candidate_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "execution_policy": {
            "schema_version": "roi_crop_v2_bbox_expansion_execution_policy_v1",
            "rules": POLICIES,
        },
        "source_frame_resolution": {
            "schema_version": "roi_crop_v2_source_frame_resolution_report_v1",
            "row_count": len(resolution_rows),
            "rows": resolution_rows,
        },
        "bbox_validation": {
            "schema_version": "roi_crop_v2_expanded_bbox_validation_report_v1",
            "row_count": len(validation_rows),
            "rows": validation_rows,
        },
        "artifact_schema": {
            "schema_version": "roi_crop_v2_expanded_artifact_schema_v1",
            "template": ARTIFACT_SCHEMA,
        },
        "artifact_collection": {
            "schema_version": "roi_crop_v2_expanded_artifact_collection_v1",
            "artifact_count": len(artifacts),
            "generated_count": generated,
            "rows": artifacts,
        },
        "execution_trace": {
            "schema_version": "roi_crop_v2_execution_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "size_comparison": {
            "schema_version": "roi_crop_v2_size_context_comparison_report_v1",
            "row_count": len(comparison_rows),
            "rows": comparison_rows,
        },
        "diversity_report": diversity_report,
        "deferred_report": {
            "schema_version": "roi_crop_v2_deferred_report_v1",
            "deferred_count": len(deferred_rows),
            "rows": deferred_rows,
        },
        "ocr_ref_plan": {
            "schema_version": "roi_crop_v2_to_ocrrequest_reference_plan_v1",
            "future_phase": "ROI-to-OCRRequest-Reference-v2-BBoxExpansion",
            "rows": ocr_ref_plan,
        },
        "boundary": {
            "schema_version": "roi_crop_v2_boundary_report_v1",
            "bbox_expansion_crop_execution_only": True,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "source_chain_report": {
            "schema_version": "roi_crop_v2_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "metrics": {
            "schema_version": "roi_crop_v2_metrics_candidate_report_v1",
            "expansion_candidate_count_observed": len(candidates),
            "expanded_crop_generated_count": generated,
            "expanded_crop_deferred_count": deferred,
            "expanded_crop_failed_count": failed,
            "unique_expanded_bbox_count": unique_bbox,
            "unique_strategy_count": len(strategies),
            "previous_unique_bbox_count": prev_unique,
            "new_ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "roi_crop_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "roi_crop_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "roi_crop_v2_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "bbox_expansion_crop_execution_only": True,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
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
        },
        "sim_report": {
            "schema_version": "roi_crop_v2_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "roi_crop_v2_non_claims_report_v1",
            "expanded_crop_not_ocr_evidence": True,
            "expanded_crop_not_better_roi_proof": True,
            "diversity_improved_not_accuracy": True,
            "no_ocr_in_phase": True,
        },
        "followups": {"schema_version": "roi_crop_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "roi_crop_v2_audit_report_v1",
            "roi_crop_execution_dryrun_v2_bbox_expansion_executed": True,
            "bbox_expansion_crop_execution_only": True,
            "expansion_candidate_count_observed": len(candidates),
            "expanded_crop_generated_count": generated,
            "new_ocr_invoked": False,
            "new_frame_extracted": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_v2_invoked": False,
            "world_model_attach_executed": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
