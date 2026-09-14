# -*- coding: utf-8 -*-
"""Scan existing videos for text-bearing frame candidates (scan-only).

Phase-RealVideo-Text-Bearing-Existing-Video-Candidate-Scan-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "RealVideo-Text-Bearing-Existing-Video-Candidate-Scan-001"

SUMMARY_SCHEMA = "realvideo_text_bearing_existing_video_candidate_scan_summary_v0"
VIDEO_REPORT_SCHEMA = "realvideo_text_bearing_existing_video_scan_report_v0"
CANDIDATES_SCHEMA = "realvideo_text_bearing_frame_candidates_v0"
BOUNDARY_SCHEMA = "realvideo_text_bearing_existing_video_scan_no_write_boundary_report_v0"
AUDIT_SCHEMA = "realvideo_text_bearing_existing_video_scan_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _join_text(ocr_result: Any) -> Tuple[str, int, float]:
    if not ocr_result:
        return "", 0, 0.0
    parts: List[str] = []
    scores: List[float] = []
    for item in ocr_result:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        text = str(item[1] or "").strip()
        if text:
            parts.append(text)
        if len(item) >= 3 and item[2] is not None:
            try:
                scores.append(float(item[2]))
            except (TypeError, ValueError):
                pass
    joined = " ".join(parts).strip()
    avg_score = sum(scores) / len(scores) if scores else 0.0
    return joined, len(parts), avg_score


def run_existing_video_candidate_scan_v0(
    *,
    video_path: str,
    output_root: str,
    text_bearing_sample_planning_root: Optional[str] = None,
    sample_interval_sec: float = 3.0,
    max_samples: int = 250,
    max_width: int = 1280,
    save_candidate_frames: bool = True,
    top_k_save: int = 12,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    vpath = Path(video_path).resolve()
    out = Path(output_root).resolve()
    planning_root = Path(text_bearing_sample_planning_root).resolve() if text_bearing_sample_planning_root else None

    if not vpath.is_file():
        return {}, {}, {}, {}, {}, [f"video_not_found:{vpath}"]

    try:
        import cv2  # type: ignore
    except ImportError:
        return {}, {}, {}, {}, {}, ["opencv_not_available"]

    try:
        from rapidocr_onnxruntime import RapidOCR  # type: ignore
    except ImportError:
        return {}, {}, {}, {}, {}, ["rapidocr_not_available"]

    cap = cv2.VideoCapture(str(vpath))
    if not cap.isOpened():
        return {}, {}, {}, {}, {}, [f"video_open_failed:{vpath}"]

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration_sec = total_frames / fps if fps > 0 and total_frames > 0 else 0.0
    interval_frames = max(1, int(round(fps * max(0.5, sample_interval_sec))))

    ocr = RapidOCR()
    frames_dir = out / "candidate_frames"
    if save_candidate_frames:
        frames_dir.mkdir(parents=True, exist_ok=True)

    candidates: List[Dict[str, Any]] = []
    sampled = 0
    text_bearing_count = 0
    empty_count = 0

    frame_idx = 0
    while frame_idx < total_frames and sampled < max_samples:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok or frame is None:
            frame_idx += interval_frames
            continue

        h, w = frame.shape[:2]
        if w > max_width:
            scale = max_width / w
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

        result, _ = ocr(frame)
        text_joined, line_count, avg_score = _join_text(result)
        empty_text = len(text_joined.strip()) == 0
        if empty_text:
            empty_count += 1
        else:
            text_bearing_count += 1

        timestamp_ms = int((frame_idx / fps) * 1000) if fps > 0 else 0
        cand = {
            "candidate_id": f"rv_scan_{vpath.stem}_f{frame_idx:08d}",
            "video_path": str(vpath),
            "frame_index": frame_idx,
            "timestamp_ms": timestamp_ms,
            "timestamp_sec": round(frame_idx / fps, 3) if fps > 0 else 0.0,
            "text_joined": text_joined,
            "ocr_line_count": line_count,
            "avg_confidence": round(avg_score, 4),
            "empty_text": empty_text,
            "text_bearing_candidate": not empty_text,
            "scan_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        candidates.append(cand)
        sampled += 1
        frame_idx += interval_frames

    cap.release()

    candidates.sort(key=lambda c: (-len(c.get("text_joined") or ""), -float(c.get("avg_confidence") or 0)))
    if save_candidate_frames:
        for i, cand in enumerate(candidates[:top_k_save]):
            if not cand.get("text_bearing_candidate"):
                continue
            cap2 = cv2.VideoCapture(str(vpath))
            cap2.set(cv2.CAP_PROP_POS_FRAMES, int(cand["frame_index"]))
            ok, fr = cap2.read()
            cap2.release()
            if ok and fr is not None:
                h, w = fr.shape[:2]
                if w > max_width:
                    scale = max_width / w
                    fr = cv2.resize(fr, (int(w * scale), int(h * scale)))
                png = frames_dir / f"{cand['candidate_id']}.png"
                cv2.imwrite(str(png), fr)
                cand["saved_frame_ref"] = str(png)

    planning_summary = _read_json(
        planning_root / "realvideo_ocr_text_bearing_sample_planning_summary.json"
    ) if planning_root else None

    video_report = {
        "schema_version": VIDEO_REPORT_SCHEMA,
        "video_path": str(vpath),
        "video_id": vpath.stem,
        "fps": round(fps, 3),
        "total_frames": total_frames,
        "duration_sec": round(duration_sec, 3),
        "sample_interval_sec": sample_interval_sec,
        "interval_frames": interval_frames,
        "frames_sampled": sampled,
        "text_bearing_candidate_count": text_bearing_count,
        "empty_text_frame_count": empty_count,
        "text_bearing_ratio": round(text_bearing_count / sampled, 4) if sampled else 0.0,
        "recommended_for_text_bearing_framesample": text_bearing_count > 0,
        "top_candidates_preview": [
            {
                "frame_index": c["frame_index"],
                "timestamp_sec": c["timestamp_sec"],
                "text_preview": (c.get("text_joined") or "")[:120],
                "ocr_line_count": c.get("ocr_line_count"),
            }
            for c in candidates[:10]
            if c.get("text_bearing_candidate")
        ],
    }

    candidates_doc = {
        "schema_version": CANDIDATES_SCHEMA,
        "candidate_count": len(candidates),
        "text_bearing_candidate_count": text_bearing_count,
        "candidates": candidates,
    }

    boundary = {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "scan_only": True,
        "video_loaded": True,
        "frame_sampled_for_scan": True,
        "ocr_used_for_scan_heuristic": True,
        "reference_chain_updated": False,
        "fusion_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "benchmark_result_claimed": False,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "existing_video_candidate_scan_executed": True,
        "scan_only": True,
        "video_loaded": True,
        "rapidocr_used_for_scan": True,
        "ocr_evidence_reference_chain_written": False,
        "fusion_invoked": False,
        "midplatform_fact_written": False,
    }

    phase_hint = "GO" if text_bearing_count > 0 and not errs else "CONDITIONAL_GO" if sampled and not errs else "NO_GO"
    if sampled == 0:
        errs.append("no_frames_sampled")
        phase_hint = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "scan_scope": "existing_video_text_bearing_candidate_scan_only",
        "based_on_text_bearing_sample_planning": planning_root.is_dir() if planning_root else False,
        "video_path": str(vpath),
        "frames_sampled": sampled,
        "text_bearing_candidate_count": text_bearing_count,
        "empty_text_frame_count": empty_count,
        "recommended_for_text_bearing_framesample": text_bearing_count > 0,
        "prior_planning_verdict": (planning_summary or {}).get("phase_verdict_hint"),
        "sample_interval_sec": sample_interval_sec,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return summary, video_report, candidates_doc, boundary, audit, errs
