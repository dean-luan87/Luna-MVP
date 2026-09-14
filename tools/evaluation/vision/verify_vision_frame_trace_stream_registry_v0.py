#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-FrameTrace-StreamRegistry-001."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if isinstance(o, dict):
            rows.append(o)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True, help="Absolute path to frame trace / registry output root.")
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    reg_p = root / "vision_stream_registry.json"
    tr_p = root / "vision_frame_trace.jsonl"
    lin_p = root / "vision_frame_lineage_matrix.json"
    con_p = root / "vision_sampling_consistency_report.json"
    aud_p = root / "vision_frame_trace_audit_report.json"

    for label, p in (
        ("vision_stream_registry", reg_p),
        ("vision_frame_trace", tr_p),
        ("vision_frame_lineage_matrix", lin_p),
        ("vision_sampling_consistency_report", con_p),
        ("vision_frame_trace_audit_report", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    traces: List[Dict[str, Any]] = []

    if not blockers:
        reg = _read_json(reg_p)
        if not str(reg.get("stream_id") or "").strip():
            blockers.append("registry_missing_stream_id")
        if not str(reg.get("source_video_ref") or "").strip():
            blockers.append("registry_missing_source_video_ref")
        if int(reg.get("sampled_frame_count") or 0) <= 0:
            blockers.append("registry_sampled_frame_count_not_positive")

        traces = _load_jsonl(tr_p)
        sc = int(reg.get("sampled_frame_count") or 0)
        if len(traces) != sc:
            blockers.append(f"trace_line_count_mismatch:got_{len(traces)}_expected_{sc}")

        fids: List[str] = []
        for i, t in enumerate(traces):
            fid = str(t.get("frame_id") or "")
            fids.append(fid)
            if not fid.strip():
                blockers.append(f"trace_empty_frame_id:{i}")
            fp = str(t.get("frame_fingerprint") or "").strip()
            if not fp:
                blockers.append(f"trace_empty_fingerprint:{i}")
            ir = str(t.get("image_ref") or "").strip()
            if not ir:
                blockers.append(f"trace_empty_image_ref:{i}")
            elif not Path(ir).is_file():
                blockers.append(f"trace_missing_image_ref:{i}")

        if len(fids) != len(set(fids)):
            blockers.append("duplicate_frame_id_in_trace")

        lin = _read_json(lin_p)
        rows = lin.get("rows") if isinstance(lin.get("rows"), list) else []
        if not rows:
            blockers.append("lineage_rows_empty")

        con = _read_json(con_p)
        if con.get("passed") is not True:
            blockers.append(f"sampling_consistency_failed:{con.get('issues')}")

        aud = _read_json(aud_p)
        if aud.get("stream_registry_generated") is not True:
            blockers.append("audit_stream_registry_generated_not_true")
        if aud.get("frame_trace_generated") is not True:
            blockers.append("audit_frame_trace_generated_not_true")
        for k in (
            "real_camera_invoked",
            "yolo_invoked",
            "ocr_invoked",
            "vlm_invoked",
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "ai_interpretation_invoked",
            "navigation_decision_invoked",
        ):
            if aud.get(k) is not False:
                blockers.append(f"audit_flag_not_false:{k}")

    if blockers:
        verdict = "NO_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "vision_frame_trace_stream_registry_verifier_report_v0",
        "phase": "Phase-Vision-FrameTrace-StreamRegistry-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_frame_trace_stream_registry_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
