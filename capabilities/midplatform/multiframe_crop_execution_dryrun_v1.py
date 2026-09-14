# -*- coding: utf-8 -*-
"""Multiframe Crop Execution DryRun v1 — projection crops from tracklet only, no OCR.

Phase-Multiframe-Crop-Execution-DryRun-v1-001
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Multiframe-Crop-Execution-DryRun-v1-001"
RUNTIME_STEP = "multiframe_crop_execution_dryrun_v1"

FOLLOWUPS = [
    "OCRRequest-Gated-Submission-from-Multiframe-v1",
    "Evidence-Pack-Adapter-v4-Multiframe",
    "Semantic-Candidate-v4-MultiframeAware",
    "Source-Validation-v2-Rerun-after-Multiframe",
    "Multiframe-Consensus-Policy-v1",
    "Crop-Quality-Scoring-v1",
    "Text-Detector-DryRun-v1",
    "Frame-Quality-Scoring-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "consume_projected_regions_only",
        "condition": "text_region_projected_region_matrix_v1 present",
        "allowed_action": "multiframe_crop_from_projection",
        "blocked_action": "detector_bbox_crop",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "projected_region_not_detected_region",
        "condition": "detected_region=false on all intake rows",
        "allowed_action": "projection_crop_artifact",
        "blocked_action": "detected_region_claim",
        "required_next_action": "Text-Detector-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_from_projection_allowed",
        "condition": "frame artifact file exists and bbox valid",
        "allowed_action": "generate_crop_png",
        "blocked_action": "mock_crop",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "projection_crop_not_evidence",
        "condition": "always",
        "allowed_action": "crop_file_only",
        "blocked_action": "ocr_evidence_claim",
        "required_next_action": "Evidence-Pack-Adapter-v4-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "detector_invocation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "object_detector_invocation",
        "required_next_action": "Text-Detector-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "ocr_execution_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "ocr_invocation",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "ocrrequest_generation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "ocrrequest_readiness_plan",
        "blocked_action": "ocrrequest_generated",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "evidence_pack_generation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "evidence_pack_generated",
        "required_next_action": "Evidence-Pack-Adapter-v4-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "semantic_generation_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "semantic_candidate_generated",
        "required_next_action": "Semantic-Candidate-v4-MultiframeAware",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "source_validation_rerun_forbidden",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "source_validation_rerun",
        "required_next_action": "Source-Validation-v2-Rerun-after-Multiframe",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_blocker_not_resolved_in_this_phase",
        "condition": "always",
        "allowed_action": "blocker_carryover",
        "blocked_action": "same_frame_blocker_resolve",
        "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "phase_boundary",
        "allowed_action": "none",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_artifact_not_fact",
        "condition": "always",
        "allowed_action": "dryrun_artifacts",
        "blocked_action": "fact_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

CROP_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "multiframe_crop_artifact_id": "mf_crop_<uuid>",
    "schema_version": "multiframe_crop_artifact_v1",
    "tracklet_candidate_ref": None,
    "candidate_frame_ref": None,
    "frame_artifact_ref": None,
    "source_frame_ref": {
        "frame_index": None,
        "frame_time_sec": None,
        "frame_offset_from_source": None,
    },
    "projection_context": {
        "projection_method": None,
        "projection_is_approximate": True,
        "detected_region": False,
        "region_confidence": None,
    },
    "bbox_context": {
        "bbox_type": "source_bbox | expanded_bbox",
        "source_bbox_xyxy": None,
        "projected_bbox_xyxy": None,
        "expanded_bbox_strategy": None,
        "crop_bbox_xyxy": None,
    },
    "crop_output": {
        "crop_file_path": None,
        "crop_width": None,
        "crop_height": None,
        "crop_generated": False,
        "crop_status": "generated | deferred | failed",
    },
    "quality_placeholder": {
        "crop_quality_score_computed": False,
        "lightweight_placeholder": True,
        "crop_area": None,
        "crop_aspect_ratio": None,
        "small_crop_risk": None,
        "blur_score": None,
        "brightness_score": None,
    },
    "ocr_allowed_in_this_phase": False,
    "ocrrequest_allowed_in_this_phase": False,
    "fact_status": "not_fact",
    "write_allowed": False,
    "source_chain": [],
}

FUTURE_PHASES: List[Dict[str, Any]] = [
    {
        "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        "purpose": "gate OCRRequest from multiframe crop artifacts",
        "required_input": ["multiframe_crop_artifact_collection_v1", "frame trace"],
        "expected_output": ["ocrrequest_plan", "gated_submission_matrix"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Evidence-Pack-Adapter-v4-Multiframe",
        "purpose": "adapt multiframe crops into evidence pack v4",
        "required_input": ["ocr_results_after_multiframe", "crop artifacts"],
        "expected_output": ["evidence_pack_v4_dryrun"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v4-MultiframeAware",
        "purpose": "semantic candidate aware of multiframe context",
        "required_input": ["evidence_pack_v4", "tracklet metadata"],
        "expected_output": ["semantic_candidate_v4"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-Rerun-after-Multiframe",
        "purpose": "rerun SV after multiframe path",
        "required_input": ["semantic_v4", "multiframe crops"],
        "expected_output": ["sv_rerun_report"],
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Multiframe-Consensus-Policy-v1",
        "purpose": "policy for independent consensus across frames",
        "required_input": ["sv_rerun", "blocker state"],
        "expected_output": ["consensus_policy_report"],
        "not_in_current_phase": True,
    },
]


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _stable_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}{h}"


def _bbox_equal(a: List[float], b: List[float], eps: float = 0.5) -> bool:
    if len(a) < 4 or len(b) < 4:
        return False
    return all(abs(float(a[i]) - float(b[i])) <= eps for i in range(4))


def _clip_bbox(bbox: List[float], fw: int, fh: int) -> Tuple[List[float], bool]:
    x1, y1, x2, y2 = [float(v) for v in bbox[:4]]
    ox1, oy1, ox2, oy2 = x1, y1, x2, y2
    x1 = max(0.0, min(x1, float(fw)))
    x2 = max(0.0, min(x2, float(fw)))
    y1 = max(0.0, min(y1, float(fh)))
    y2 = max(0.0, min(y2, float(fh)))
    clipped = (x1, y1, x2, y2) != (ox1, oy1, ox2, oy2)
    if x2 <= x1 or y2 <= y1:
        return [x1, y1, x2, y2], clipped
    return [x1, y1, x2, y2], clipped


def _bbox_valid(bbox: List[float], fw: int, fh: int) -> Tuple[bool, str]:
    if len(bbox) < 4:
        return False, "invalid_bbox"
    x1, y1, x2, y2 = [float(v) for v in bbox[:4]]
    if x2 <= x1 or y2 <= y1:
        return False, "zero_area"
    if x1 < 0 or y1 < 0 or x2 > fw or y2 > fh:
        return False, "out_of_bounds"
    return True, "valid"


def _area(bbox: List[float]) -> float:
    x1, y1, x2, y2 = [float(v) for v in bbox[:4]]
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def _load_frame_image(path: Path):
    from PIL import Image  # type: ignore

    return Image.open(path).convert("RGB")


def _save_crop(img, bbox: List[float], out_path: Path) -> Tuple[int, int]:
    x1, y1, x2, y2 = [int(round(v)) for v in bbox[:4]]
    cropped = img.crop((x1, y1, x2, y2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out_path, format="PNG")
    return cropped.size[0], cropped.size[1]


def _image_stats(img) -> Tuple[Optional[float], Optional[float]]:
    try:
        import numpy as np  # type: ignore

        arr = np.asarray(img.convert("L"), dtype=np.float32)
        brightness = float(arr.mean()) if arr.size else None
        gx = np.abs(np.diff(arr, axis=1)).mean() if arr.shape[1] > 1 else 0.0
        gy = np.abs(np.diff(arr, axis=0)).mean() if arr.shape[0] > 1 else 0.0
        blur = float((gx + gy) / 2.0)
        return brightness, blur
    except Exception:  # noqa: BLE001
        return None, None


def _bbox_type_and_strategy(
    projected: List[float], source: List[float], expanded_set: List[List[float]]
) -> Tuple[str, Optional[str]]:
    if _bbox_equal(projected, source):
        return "source_bbox", "source_bbox_identity"
    for i, eb in enumerate(expanded_set):
        if _bbox_equal(projected, list(eb)):
            return "expanded_bbox", f"expanded_bbox_index_{i}"
    return "expanded_bbox", "expanded_bbox_unlisted"


def run_multiframe_crop_execution_dryrun_v1(
    *,
    output_root: str,
    text_region_tracklet_root: str,
    better_frame_root: str,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    semantic_v3_root: str,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    out = Path(output_root).resolve()
    crops_dir = out / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    tr_root = Path(text_region_tracklet_root).resolve()
    bf_root = Path(better_frame_root).resolve()
    mf_root = Path(multiframe_merge_proposal_root).resolve()
    sv_root = Path(source_validation_v2_root).resolve()
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    projected_doc = _read_json(tr_root / "text_region_projected_region_matrix_v1.json")
    tracklet_coll = _read_json(tr_root / "text_region_tracklet_candidate_collection_v1.json")
    tr_summary = _read_json(tr_root / "text_region_tracklet_dryrun_v1_summary.json")
    artifacts_doc = _read_json(bf_root / "better_frame_artifact_collection.json")
    drift_doc = _read_json(tr_root / "text_region_drift_risk_report_v1.json")

    projected_rows = [r for r in (projected_doc.get("rows") or []) if isinstance(r, dict)]
    candidates = [c for c in (tracklet_coll.get("candidates") or []) if isinstance(c, dict)]
    tracklet = candidates[0] if candidates else {}
    tracklet_id = str(tracklet.get("tracklet_candidate_id") or "tr_tracklet_unknown")
    region_id = str(tracklet.get("multiframe_candidate_region_id") or "mf_region_unknown")

    art_by_id: Dict[str, Dict[str, Any]] = {}
    for art in artifacts_doc.get("artifacts") or []:
        if isinstance(art, dict) and art.get("frame_artifact_id"):
            art_by_id[str(art["frame_artifact_id"])] = art

    drift_rep = (drift_doc.get("reports") or [{}])[0] if isinstance(drift_doc.get("reports"), list) else {}
    drift_risk = str(drift_rep.get("drift_risk") or "medium")

    intake_rows: List[Dict[str, Any]] = []
    validation_rows: List[Dict[str, Any]] = []
    artifacts: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    quality_rows: List[Dict[str, Any]] = []
    readiness_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    generated = deferred = failed = 0
    ready_for_ocrrequest = 0
    frame_cache: Dict[str, Any] = {}

    for idx, row in enumerate(projected_rows):
        src_bbox = list(row.get("source_bbox_xyxy") or [])
        proj_bbox = list(row.get("projected_bbox_xyxy") or [])
        expanded_set = [list(b) for b in (row.get("expanded_bbox_candidates") or []) if isinstance(b, (list, tuple))]
        faid = str(row.get("frame_artifact_id") or "")
        art = art_by_id.get(faid, {})
        fp = str(art.get("frame_file_path") or "")
        fw = int(art.get("frame_width") or 0)
        fh = int(art.get("frame_height") or 0)
        bbox_type, exp_strategy = _bbox_type_and_strategy(proj_bbox, src_bbox, expanded_set)

        proj_id = _stable_id("mf_proj_", tracklet_id, faid, str(proj_bbox), str(idx))
        crop_intake_id = _stable_id("mf_intake_", proj_id)
        crop_art_id = _stable_id("mf_crop_", proj_id)

        intake_rows.append(
            {
                "crop_intake_id": crop_intake_id,
                "tracklet_candidate_id": row.get("tracklet_candidate_id") or tracklet_id,
                "multiframe_candidate_region_id": region_id,
                "projected_region_id": proj_id,
                "candidate_frame_ref_id": row.get("candidate_frame_ref_id"),
                "frame_artifact_id": faid,
                "frame_index": row.get("frame_index"),
                "frame_time_sec": row.get("frame_time_sec"),
                "frame_offset_from_source": row.get("frame_offset_from_source"),
                "frame_file_path": fp,
                "projection_method": row.get("projection_method") or "static_bbox_projection",
                "projected_bbox_xyxy": proj_bbox,
                "bbox_type": bbox_type,
                "source_bbox_xyxy": src_bbox,
                "expanded_bbox_candidates": expanded_set,
                "projection_is_approximate": True,
                "detected_region": False,
                "region_confidence": row.get("region_confidence"),
                "intake_status": "accepted" if fp else "rejected_missing_file",
                "eligible_for_multiframe_crop": bool(fp),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        clipped_bbox, clipped = _clip_bbox(proj_bbox, fw, fh) if fw and fh else (proj_bbox, False)
        bbox_ok, bbox_status = _bbox_valid(clipped_bbox, fw, fh) if fw and fh else (False, "frame_dims_missing")

        validation_rows.append(
            {
                "projected_region_id": proj_id,
                "frame_width": fw,
                "frame_height": fh,
                "projected_bbox_xyxy": proj_bbox,
                "bbox_within_bounds": bbox_status != "out_of_bounds",
                "clipped": clipped,
                "clipped_bbox_xyxy": clipped_bbox,
                "bbox_valid_for_crop": bbox_ok,
                "validation_status": bbox_status if fw and fh else "frame_dims_missing",
                "fact_status": "not_fact",
            }
        )

        status = "deferred"
        crop_path: Optional[str] = None
        crop_w = crop_h = None
        err: Optional[str] = None
        crop_generated_flag = False

        if not fp or not Path(fp).is_file():
            deferred += 1
            err = "frame_file_missing"
        elif not fw or not fh:
            deferred += 1
            err = "frame_dims_missing"
        elif not bbox_ok:
            if clipped and _area(clipped_bbox) > 0:
                bbox_ok = True
            else:
                failed += 1
                status = "failed"
                err = bbox_status

        if bbox_ok and fp and Path(fp).is_file():
            try:
                if fp not in frame_cache:
                    frame_cache[fp] = _load_frame_image(Path(fp))
                img = frame_cache[fp]
                fname = f"{crop_art_id}_fi{row.get('frame_index')}_{bbox_type}.png"
                out_png = crops_dir / fname.replace("/", "_")
                crop_w, crop_h = _save_crop(img, clipped_bbox, out_png)
                crop_path = str(out_png)
                status = "generated"
                crop_generated_flag = True
                generated += 1
            except Exception as e:  # noqa: BLE001
                status = "failed"
                err = str(e)
                failed += 1

        brightness, blur = (None, None)
        small_crop_risk = None
        aspect = None
        crop_area = None
        if crop_generated_flag and crop_path:
            try:
                cimg = _load_frame_image(Path(crop_path))
                brightness, blur = _image_stats(cimg)
                crop_area = float(crop_w or 0) * float(crop_h or 0)
                aspect = round((crop_w or 1) / max(crop_h or 1, 1), 4)
                small_crop_risk = (crop_w or 0) < 40 or (crop_h or 0) < 20
            except Exception:  # noqa: BLE001
                pass

        source_chain = [
            RUNTIME_STEP,
            "Text-Region-Tracklet-DryRun-v1",
            "Better-Frame-Extraction-DryRun-v1",
            "Multiframe-Merge-Proposal-v1",
        ]

        artifact = {
            "multiframe_crop_artifact_id": crop_art_id,
            "schema_version": "multiframe_crop_artifact_v1",
            "tracklet_candidate_id": tracklet_id,
            "multiframe_candidate_region_id": region_id,
            "projected_region_id": proj_id,
            "candidate_frame_ref_id": row.get("candidate_frame_ref_id"),
            "frame_artifact_id": faid,
            "frame_index": row.get("frame_index"),
            "frame_time_sec": row.get("frame_time_sec"),
            "frame_offset_from_source": row.get("frame_offset_from_source"),
            "frame_file_path": fp,
            "projection_method": row.get("projection_method") or "static_bbox_projection",
            "projection_is_approximate": True,
            "detected_region": False,
            "region_confidence": row.get("region_confidence"),
            "bbox_type": bbox_type,
            "source_bbox_xyxy": src_bbox,
            "projected_bbox_xyxy": proj_bbox,
            "crop_bbox_xyxy": clipped_bbox,
            "expanded_bbox_strategy": exp_strategy,
            "crop_file_path": crop_path,
            "crop_width": crop_w,
            "crop_height": crop_h,
            "crop_status": status,
            "crop_generated": crop_generated_flag,
            "clipped": clipped,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": source_chain,
        }
        artifacts.append(artifact)

        trace_rows.append(
            {
                "crop_execution_id": _stable_id("mf_cex_", crop_art_id),
                "projected_region_id": proj_id,
                "multiframe_crop_artifact_id": crop_art_id,
                "frame_artifact_id": faid,
                "frame_file_path": fp,
                "crop_bbox_xyxy": clipped_bbox,
                "crop_status": status,
                "crop_file_path": crop_path,
                "clipped": clipped,
                "error": err,
                "detector_invoked": False,
                "text_detector_invoked": False,
                "ocr_invoked": False,
                "provider_invoked": False,
                "ocrrequest_generated": False,
            }
        )

        quality_rows.append(
            {
                "multiframe_crop_artifact_id": crop_art_id,
                "crop_width": crop_w,
                "crop_height": crop_h,
                "crop_area": crop_area,
                "crop_aspect_ratio": aspect,
                "small_crop_risk": small_crop_risk,
                "lightweight_placeholder": True,
                "blur_score": blur,
                "brightness_score": brightness,
                "crop_quality_claim_allowed": False,
                "required_future_phase": "Crop-Quality-Scoring-v1",
            }
        )

        ready = crop_generated_flag and bool(crop_path) and Path(crop_path).is_file()
        if ready:
            ready_for_ocrrequest += 1
        readiness_rows.append(
            {
                "multiframe_crop_artifact_id": crop_art_id,
                "crop_file_path": crop_path,
                "crop_status": status,
                "ready_for_ocrrequest_multiframe": ready,
                "readiness_status": "ready_placeholder" if ready else "not_ready",
                "ocrrequest_allowed_now": False,
                "required_input_for_future_ocrrequest": [
                    "crop_file_path",
                    "frame_index",
                    "bbox_type",
                    "projection_method",
                ],
                "blocker_codes": ["same_frame_blocker_still_active", "ocrrequest_gated_future_phase"],
                "future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
            }
        )

        chain_rows.append(
            {
                "multiframe_crop_artifact_id": crop_art_id,
                "traceable_to_text_region_tracklet": tr_root.is_dir(),
                "traceable_to_better_frame_extraction": bf_root.is_dir(),
                "traceable_to_multiframe_proposal": mf_root.is_dir(),
                "traceable_to_source_validation_v2": sv_root.is_dir(),
                "traceable_to_semantic_candidate_v3": sem_root.is_dir(),
                "traceable_to_evidence_pack_v3": ep_root.is_dir(),
                "traceable_to_linebox_trace": Path(linebox_sq_root).resolve().is_dir(),
                "source_chain_preserved": True,
            }
        )

    crop_count = len(artifacts)
    unique_frames = len({a.get("frame_index") for a in artifacts})
    unique_bbox = len({tuple(a.get("crop_bbox_xyxy") or []) for a in artifacts})
    bbox_types = {a.get("bbox_type") for a in artifacts}
    source_bbox_count = sum(1 for a in artifacts if a.get("bbox_type") == "source_bbox")
    expanded_bbox_count = sum(1 for a in artifacts if a.get("bbox_type") == "expanded_bbox")
    offsets = [a.get("frame_offset_from_source") for a in artifacts if a.get("frame_offset_from_source") is not None]
    sizes = [f"{a.get('crop_width')}x{a.get('crop_height')}" for a in artifacts if a.get("crop_generated")]

    frame_artifact_count = int(tr_summary.get("frame_artifact_count_observed") or 6)
    projected_count = len(projected_rows)

    phase_hint = "GO"
    if generated == 0 and deferred + failed == projected_count:
        phase_hint = "CONDITIONAL_GO"
    elif generated == 0:
        phase_hint = "NO_GO"

    summary = {
        "schema_version": "multiframe_crop_execution_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "dryrun_scope": "multiframe_crop_execution_dryrun_only",
        "based_on_text_region_tracklet": tr_root.is_dir(),
        "based_on_better_frame_extraction": bf_root.is_dir(),
        "frame_artifact_count_observed": frame_artifact_count,
        "tracklet_candidate_count_observed": int(tracklet_coll.get("tracklet_candidate_count") or 1),
        "projected_region_count_observed": projected_count,
        "multiframe_crop_plan_generated": True,
        "multiframe_crop_execution_attempted": True,
        "multiframe_crop_artifact_generated": generated > 0,
        "multiframe_crop_artifact_count": crop_count,
        "multiframe_crop_deferred_count": deferred,
        "multiframe_crop_failed_count": failed,
        "ocr_invoked": False,
        "provider_invoked": False,
        "ocrrequest_generated": False,
        "evidence_pack_generated": False,
        "semantic_candidate_generated": False,
        "source_validation_rerun_invoked": False,
        "same_frame_blocker_resolved": False,
        "same_frame_blocker_still_active": True,
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
        "phase_verdict_hint": phase_hint,
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "multiframe_crop_tracklet_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "multiframe_crop_execution_rule_matrix_v1", "rules": RULES},
        "crop_schema": {
            "schema_version": "multiframe_crop_artifact_schema_v1",
            "template": CROP_ARTIFACT_SCHEMA,
        },
        "crop_collection": {
            "schema_version": "multiframe_crop_artifact_collection_v1",
            "crop_artifact_count": crop_count,
            "artifacts": artifacts,
        },
        "execution_trace": {
            "schema_version": "multiframe_crop_execution_trace_v1",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "bbox_validation": {
            "schema_version": "multiframe_crop_bbox_validation_report_v1",
            "row_count": len(validation_rows),
            "rows": validation_rows,
        },
        "quality_placeholder": {
            "schema_version": "multiframe_crop_quality_placeholder_report_v1",
            "row_count": len(quality_rows),
            "rows": quality_rows,
        },
        "diversity": {
            "schema_version": "multiframe_crop_diversity_report_v1",
            "crop_artifact_count": crop_count,
            "unique_frame_index_count": unique_frames,
            "unique_bbox_count": unique_bbox,
            "unique_bbox_type_count": len(bbox_types),
            "source_bbox_crop_count": source_bbox_count,
            "expanded_bbox_crop_count": expanded_bbox_count,
            "frame_offset_distribution": dict((str(o), offsets.count(o)) for o in sorted(set(offsets))),
            "crop_size_distribution": dict((s, sizes.count(s)) for s in sorted(set(sizes))),
            "crop_diversity_improved_candidate": unique_frames > 1,
            "diversity_claim_allowed": False,
            "independent_consensus_allowed_now": False,
            "same_frame_blocker_resolved": False,
        },
        "projection_risk": {
            "schema_version": "multiframe_projection_risk_carryover_report_v1",
            "projection_crop_count": crop_count,
            "projection_is_approximate_count": crop_count,
            "detected_region_count": 0,
            "projection_not_detection": True,
            "region_drift_risk": drift_risk,
            "cross_region_merge_risk": "low",
            "viewpoint_shift_risk": "medium",
            "requires_future_detection_or_quality_gate": True,
            "required_next_action": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        },
        "ocr_readiness": {
            "schema_version": "multiframe_ocrrequest_readiness_report_v1",
            "row_count": len(readiness_rows),
            "rows": readiness_rows,
            "ocrrequest_allowed_now": False,
        },
        "same_frame_carryover": {
            "schema_version": "multiframe_crop_same_frame_blocker_carryover_report_v1",
            "same_frame_consensus_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
            "independent_consensus_allowed_now": False,
            "multiframe_crops_prepared_but_not_validated": True,
            "required_future_phase": "OCRRequest-Gated-Submission-from-Multiframe-v1",
        },
        "future_plan": {
            "schema_version": "multiframe_future_ocr_ep_sv_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "source_chain_report": {
            "schema_version": "multiframe_crop_source_chain_report_v1",
            "row_count": len(chain_rows),
            "rows": chain_rows,
        },
        "boundary": {
            "schema_version": "multiframe_crop_boundary_report_v1",
            "multiframe_crop_execution_dryrun_only": True,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "multiframe_crop_metrics_candidate_report_v1",
            "projected_region_count_observed": projected_count,
            "crop_intake_count": len(intake_rows),
            "crop_artifact_count": crop_count,
            "crop_generated_count": generated,
            "crop_deferred_count": deferred,
            "crop_failed_count": failed,
            "unique_frame_index_count": unique_frames,
            "unique_bbox_count": unique_bbox,
            "source_bbox_crop_count": source_bbox_count,
            "expanded_bbox_crop_count": expanded_bbox_count,
            "ready_for_ocrrequest_count": ready_for_ocrrequest,
            "detector_invoked_count": 0,
            "text_detector_invoked_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "evidence_pack_generated_count": 0,
            "semantic_candidate_generated_count": 0,
            "source_validation_rerun_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "multiframe_crop_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "multiframe_crop_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "multiframe_crop_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "multiframe_crop_execution_dryrun_only": True,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
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
            "schema_version": "multiframe_crop_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "multiframe_crop_non_claims_report_v1",
            "claims": [
                "no_ocr_in_this_phase",
                "no_ocrrequest_in_this_phase",
                "multiframe_crop_not_ocr_evidence",
                "projection_crop_not_detected_text_region",
                "crop_diversity_not_independent_consensus",
                "crop_readiness_not_validation_passed",
                "same_frame_blocker_not_resolved",
                "no_source_validation_rerun",
                "no_world_model_write",
                "no_scene_delta",
                "not_benchmark",
                "not_provider_comparison",
                "not_navigation_ready",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "multiframe_crop_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "multiframe_crop_audit_report_v1",
            "multiframe_crop_execution_dryrun_v1_executed": True,
            "multiframe_crop_execution_dryrun_only": True,
            "projected_region_count_observed": projected_count,
            "crop_artifact_count": crop_count,
            "crop_generated_count": generated,
            "ready_for_ocrrequest_count": ready_for_ocrrequest,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "vision_model_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "same_frame_blocker_still_active": True,
            "same_frame_blocker_resolved": False,
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
    }
