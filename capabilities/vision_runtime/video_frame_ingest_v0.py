# -*- coding: utf-8 -*-
"""Offline video frame decode, resize, envelope materialization (no ML)."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.vision_runtime.video_frame_audit_v0 import build_default_video_frame_audit_v0
from capabilities.vision_runtime.video_frame_envelope_v0 import build_video_frame_envelope_v0, fingerprint_png_bytes
from capabilities.vision_runtime.video_frame_sampling_policy_v0 import VideoFrameSamplingParamsV0, run_sampling_plan_v0


def _try_import_cv2():  # pragma: no cover - import guard
    try:
        import cv2  # type: ignore

        return cv2
    except Exception:
        return None


def generate_test_video_mp4_v0(
    out_path: Path,
    *,
    width: int = 640,
    height: int = 480,
    fps: float = 10.0,
    duration_sec: float = 3.0,
) -> Dict[str, Any]:
    """Write a short MP4 with frame index text (OpenCV VideoWriter)."""
    import numpy as np

    cv2 = _try_import_cv2()
    if cv2 is None:
        raise RuntimeError("opencv-python (cv2) is required for test video generation")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    w, h = int(width), int(height)
    n_frames = int(max(1, round(float(duration_sec) * float(fps))))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, float(fps), (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"VideoWriter failed to open: {out_path}")

    for i in range(n_frames):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        frame[:, :] = (40, 40, 40)
        label = f"frame {i}"
        cv2.putText(frame, label, (24, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (220, 220, 60), 2, cv2.LINE_AA)
        writer.write(frame)
    writer.release()

    return {
        "path": str(out_path.resolve()),
        "width": w,
        "height": h,
        "fps": float(fps),
        "frame_count": n_frames,
        "duration_sec": float(duration_sec),
    }


def count_video_frames_v0(video_path: Path) -> Tuple[int, float]:
    cv2 = _try_import_cv2()
    if cv2 is None:
        raise RuntimeError("opencv-python (cv2) is required for video ingest")
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"VideoCapture failed: {video_path}")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    cap.release()
    if n <= 0:
        cap2 = cv2.VideoCapture(str(video_path))
        n2 = 0
        while True:
            ok, _ = cap2.read()
            if not ok:
                break
            n2 += 1
        cap2.release()
        n = n2
    return n, fps


def ingest_video_frames_offline_v0(
    video_path: Path,
    output_root: Path,
    params: VideoFrameSamplingParamsV0,
    *,
    stream_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Decode video, sample frames, write PNGs + envelopes + matrix + sampling report."""
    cv2 = _try_import_cv2()
    if cv2 is None:
        raise RuntimeError("opencv-python (cv2) is required for video ingest")

    video_path = Path(video_path).resolve()
    output_root = Path(output_root).resolve()
    frames_dir = output_root / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    total, fps_decl = count_video_frames_v0(video_path)
    if total <= 0:
        raise RuntimeError("Could not determine frame count for video")

    sampled_indices, sampling_report = run_sampling_plan_v0(total_frames_in_source=total, params=params)
    sampling_report["sample_stride"] = int(sampling_report["sampling_stride"])
    want = set(sampled_indices)
    sid = stream_id or f"stream_{uuid.uuid4().hex[:16]}"

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"VideoCapture failed: {video_path}")
    fps_eff = fps_decl if fps_decl > 1e-3 else 10.0
    sampling_report["fps_effective"] = fps_eff

    envelopes: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    idx = 0
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        if idx in want:
            h0, w0 = bgr.shape[:2]
            tw, th = int(params.max_width), int(params.max_height)
            scale = min(tw / max(w0, 1), th / max(h0, 1), 1.0)
            nw, nh = max(1, int(w0 * scale)), max(1, int(h0 * scale))
            if (nw, nh) != (w0, h0):
                bgr = cv2.resize(bgr, (nw, nh), interpolation=cv2.INTER_AREA)
            h1, w1 = bgr.shape[:2]
            png_path = frames_dir / f"frame_{idx:06d}.png"
            if not cv2.imwrite(str(png_path), bgr):
                raise RuntimeError(f"cv2.imwrite failed: {png_path}")
            png_bytes = png_path.read_bytes()
            fp = fingerprint_png_bytes(png_bytes)
            ts_ms = int(round(1000.0 * float(idx) / max(fps_eff, 1e-6)))
            fid = f"{sid}_f{idx:06d}"
            env = build_video_frame_envelope_v0(
                frame_id=fid,
                stream_id=sid,
                source_video_ref=str(video_path),
                frame_index=idx,
                timestamp_ms=ts_ms,
                width=w1,
                height=h1,
                fps_source=fps_eff,
                image_ref=str(png_path.resolve()),
                frame_fingerprint=fp,
                sampled=True,
                reason_codes=["stride_and_cap_policy", "offline_file_decode"],
                observed_at_ms=ts_ms,
                valid_until_ms=None,
            )
            envelopes.append(env)
            matrix_rows.append(
                {
                    "frame_id": fid,
                    "frame_index": idx,
                    "width": w1,
                    "height": h1,
                    "image_ref": str(png_path.resolve()),
                    "sampled": True,
                }
            )
        idx += 1

    cap.release()

    env_path = output_root / "video_frame_envelopes.jsonl"
    with env_path.open("w", encoding="utf-8") as f:
        for e in envelopes:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    matrix = {"schema": "video_frame_matrix_v0", "rows": matrix_rows}
    audit = build_default_video_frame_audit_v0(video_ingest_executed=True)
    summary = {
        "schema": "video_frame_ingest_summary_v0",
        "phase": "Phase-Vision-VideoFrame-Minimal-Ingest-001",
        "source_video_ref": str(video_path),
        "stream_id": sid,
        "total_frames_seen": int(sampling_report["total_frames_seen"]),
        "sampled_frame_count": int(sampling_report["sampled_frame_count"]),
        "skipped_frame_count": int(sampling_report["skipped_frame_count"]),
        "sample_stride": int(params.sample_stride),
        "output_root": str(output_root),
        "envelopes_path": str(env_path.resolve()),
        "audit": audit,
    }

    return {
        "summary": summary,
        "sampling_report": sampling_report,
        "matrix": matrix,
        "envelopes": envelopes,
        "audit": audit,
    }
