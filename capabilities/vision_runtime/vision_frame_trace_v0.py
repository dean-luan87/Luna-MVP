# -*- coding: utf-8 -*-
"""Vision frame trace events, lineage matrix, sampling consistency (read-only)."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List

from capabilities.vision_runtime.vision_stream_registry_v0 import build_vision_stream_registry_v0


def _safe_int(v: Any, *, default: int = 0) -> int:
    if v is None:
        return default
    return int(v)


def load_video_frame_envelopes_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def build_frame_trace_event_v0(
    *,
    envelope: Dict[str, Any],
    trace_id: str,
    event_type: str = "frame_sampled",
) -> Dict[str, Any]:
    sd = envelope.get("sampling_decision") if isinstance(envelope.get("sampling_decision"), dict) else {}
    reason_codes = list(sd.get("reason_codes") or [])
    anchor = envelope.get("stcm_anchor")
    if not isinstance(anchor, dict):
        anchor = {
            "observed_at_ms": _safe_int(envelope.get("timestamp_ms")),
            "valid_until_ms": None,
            "coordinate_space": "frame_pixel",
        }
    return {
        "schema_version": "vision_frame_trace_event_v0",
        "event_type": event_type,
        "trace_id": trace_id,
        "stream_id": str(envelope.get("stream_id") or ""),
        "frame_id": str(envelope.get("frame_id") or ""),
        "frame_index": _safe_int(envelope.get("frame_index")),
        "timestamp_ms": _safe_int(envelope.get("timestamp_ms")),
        "image_ref": str(envelope.get("image_ref") or ""),
        "frame_fingerprint": str(envelope.get("frame_fingerprint") or ""),
        "sampling_reason_codes": reason_codes,
        "stcm_anchor": dict(anchor),
    }


def build_frame_lineage_matrix_v0(envelopes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Order by ``frame_index``; chain ``previous_frame_id`` / ``next_frame_id``."""
    ordered = sorted(envelopes, key=lambda e: _safe_int(e.get("frame_index")))
    rows: List[Dict[str, Any]] = []
    for i, env in enumerate(ordered):
        fid = str(env.get("frame_id") or "")
        prev_id = str(ordered[i - 1].get("frame_id") or "") if i > 0 else None
        next_id = str(ordered[i + 1].get("frame_id") or "") if i + 1 < len(ordered) else None
        rows.append(
            {
                "frame_id": fid,
                "stream_id": str(env.get("stream_id") or ""),
                "source_video_ref": str(env.get("source_video_ref") or ""),
                "frame_index": _safe_int(env.get("frame_index")),
                "timestamp_ms": _safe_int(env.get("timestamp_ms")),
                "image_ref": str(env.get("image_ref") or ""),
                "frame_fingerprint": str(env.get("frame_fingerprint") or ""),
                "previous_frame_id": prev_id,
                "next_frame_id": next_id,
                "sampled": True,
            }
        )
    return {"schema": "vision_frame_lineage_matrix_v0", "rows": rows}


def build_sampling_consistency_report_v0(
    *,
    summary: Dict[str, Any],
    sampling_report: Dict[str, Any],
    envelopes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    issues: List[str] = []
    sampled_expected = int(sampling_report.get("sampled_frame_count") or summary.get("sampled_frame_count") or 0)
    n = len(envelopes)
    if n != sampled_expected:
        issues.append(f"envelope_count_mismatch:got_{n}_expected_{sampled_expected}")

    indices = [_safe_int(e.get("frame_index")) for e in envelopes]
    if len(indices) != len(set(indices)):
        issues.append("duplicate_frame_index_in_envelopes")

    ref_order = list(sampling_report.get("sampled_indices") or [])
    sorted_env = sorted(envelopes, key=lambda e: _safe_int(e.get("frame_index")))
    actual_indices = [_safe_int(e.get("frame_index")) for e in sorted_env]
    if ref_order and actual_indices != ref_order[: len(actual_indices)]:
        issues.append(f"frame_index_order_mismatch:expected_prefix_{ref_order[: len(actual_indices)]}_got_{actual_indices}")

    ids = [str(e.get("frame_id") or "") for e in envelopes]
    if len(ids) != len(set(ids)):
        issues.append("duplicate_frame_id")

    for i, e in enumerate(envelopes):
        fp = str(e.get("frame_fingerprint") or "").strip()
        if not fp:
            issues.append(f"empty_fingerprint:{i}")
        ir = str(e.get("image_ref") or "").strip()
        if not ir:
            issues.append(f"empty_image_ref:{i}")
        elif not Path(ir).is_file():
            issues.append(f"missing_image_file:{i}:{ir}")

    mono = all(
        _safe_int(sorted_env[j].get("frame_index")) < _safe_int(sorted_env[j + 1].get("frame_index"))
        for j in range(len(sorted_env) - 1)
    ) if len(sorted_env) > 1 else True
    if not mono:
        issues.append("frame_index_not_strictly_increasing")

    return {
        "schema": "vision_sampling_consistency_report_v0",
        "passed": len(issues) == 0,
        "issues": issues,
        "summary_sampled_frame_count": int(summary.get("sampled_frame_count") or 0),
        "report_sampled_frame_count": int(sampling_report.get("sampled_frame_count") or 0),
        "envelope_count": n,
    }


def build_vision_frame_trace_audit_v0() -> Dict[str, Any]:
    return {
        "schema": "vision_frame_trace_audit_v0",
        "stream_registry_generated": True,
        "frame_trace_generated": True,
        "real_camera_invoked": False,
        "yolo_invoked": False,
        "ocr_invoked": False,
        "vlm_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
    }


def run_vision_frame_trace_stream_registry_from_ingest_v0(
    ingest_root: Path,
    output_root: Path,
) -> Dict[str, Any]:
    """Read ingest artifacts; write registry, trace JSONL, lineage, consistency, audit, summary."""
    ingest_root = Path(ingest_root).resolve()
    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    summary_path = ingest_root / "video_frame_ingest_summary.json"
    sampling_path = ingest_root / "video_frame_sampling_report.json"
    env_path = ingest_root / "video_frame_envelopes.jsonl"

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    sampling_report = json.loads(sampling_path.read_text(encoding="utf-8"))
    envelopes = load_video_frame_envelopes_jsonl(env_path)

    stream_id = str(summary.get("stream_id") or "")
    source_video_ref = str(summary.get("source_video_ref") or "")
    total_frames_seen = int(summary.get("total_frames_seen") or 0)
    sampled_frame_count = int(summary.get("sampled_frame_count") or len(envelopes))

    fps = float(envelopes[0].get("fps_source") or 0.0) if envelopes else 0.0
    w = int(envelopes[0].get("width") or 0) if envelopes else 0
    h = int(envelopes[0].get("height") or 0) if envelopes else 0
    if w <= 0 or h <= 0:
        gen = summary.get("generated_test_video")
        if isinstance(gen, dict):
            w = int(gen.get("width") or w)
            h = int(gen.get("height") or h)
            fps = float(gen.get("fps") or fps or 0.0)

    sampling_policy_ref = str(sampling_path.resolve())

    registry = build_vision_stream_registry_v0(
        stream_id=stream_id,
        source_video_ref=source_video_ref,
        fps_source=fps,
        width=w,
        height=h,
        total_frames_seen=total_frames_seen,
        sampled_frame_count=sampled_frame_count,
        sampling_policy_ref=sampling_policy_ref,
        envelopes=envelopes,
        source_type="offline_video",
        created_from_phase="Vision-VideoFrame-Minimal-Ingest-001",
    )

    trace_path = output_root / "vision_frame_trace.jsonl"
    trace_lines: List[Dict[str, Any]] = []
    with trace_path.open("w", encoding="utf-8") as f:
        for env in sorted(envelopes, key=lambda e: _safe_int(e.get("frame_index"))):
            tid = f"vft_{uuid.uuid4().hex}"
            ev = build_frame_trace_event_v0(envelope=env, trace_id=tid)
            trace_lines.append(ev)
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    lineage = build_frame_lineage_matrix_v0(envelopes)
    consistency = build_sampling_consistency_report_v0(
        summary=summary, sampling_report=sampling_report, envelopes=envelopes
    )
    audit = build_vision_frame_trace_audit_v0()

    out_summary = {
        "schema": "vision_frame_trace_stream_registry_summary_v0",
        "phase": "Phase-Vision-FrameTrace-StreamRegistry-001",
        "video_ingest_root": str(ingest_root),
        "output_root": str(output_root),
        "upstream_phase": "Vision-VideoFrame-Minimal-Ingest-001",
        "stream_id": stream_id,
        "source_video_ref": source_video_ref,
        "sampled_frame_count": sampled_frame_count,
        "frame_trace_line_count": len(trace_lines),
        "sampling_consistency_passed": bool(consistency.get("passed")),
    }

    return {
        "summary": out_summary,
        "registry": registry,
        "lineage": lineage,
        "consistency": consistency,
        "audit": audit,
        "paths": {
            "vision_stream_registry": str((output_root / "vision_stream_registry.json").resolve()),
            "vision_frame_trace": str(trace_path.resolve()),
            "vision_frame_lineage_matrix": str((output_root / "vision_frame_lineage_matrix.json").resolve()),
            "vision_sampling_consistency_report": str((output_root / "vision_sampling_consistency_report.json").resolve()),
            "vision_frame_trace_audit_report": str((output_root / "vision_frame_trace_audit_report.json").resolve()),
        },
    }
