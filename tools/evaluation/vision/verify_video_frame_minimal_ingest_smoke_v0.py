#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Phase-Vision-VideoFrame-Minimal-Ingest-001 smoke."""

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


def _load_envelopes(p: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []
    missing_img = 0

    if not root.is_dir():
        blockers.append("output_root_missing")

    sum_p = root / "video_frame_ingest_summary.json"
    sp_p = root / "video_frame_sampling_report.json"
    env_p = root / "video_frame_envelopes.jsonl"
    mx_p = root / "video_frame_matrix.json"
    aud_p = root / "video_frame_audit_report.json"

    for label, p in (
        ("summary", sum_p),
        ("sampling_report", sp_p),
        ("envelopes", env_p),
        ("matrix", mx_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    envelopes: List[Dict[str, Any]] = []

    if not blockers:
        sp = _read_json(sp_p)
        aud = _read_json(aud_p)

        if int(sp.get("sampled_frame_count") or 0) <= 0:
            blockers.append("sampled_frame_count_not_positive")

        try:
            envelopes = _load_envelopes(env_p)
        except Exception as e:
            blockers.append(f"envelopes_parse_error:{e}")

        if not blockers and len(envelopes) != int(sp.get("sampled_frame_count") or -1):
            blockers.append("envelope_line_count_mismatch_sampling_report")

        req_env = (
            "frame_id",
            "stream_id",
            "frame_index",
            "timestamp_ms",
            "width",
            "height",
            "image_ref",
        )
        for i, env in enumerate(envelopes):
            if not isinstance(env, dict):
                blockers.append(f"envelope_not_object:{i}")
                break
            for k in req_env:
                if k not in env or env.get(k) in (None, ""):
                    blockers.append(f"envelope_missing:{i}:{k}")
            ir = env.get("image_ref")
            if isinstance(ir, str) and ir.strip():
                if not Path(ir).is_file():
                    missing_img += 1
            else:
                missing_img += 1

        audit_keys = (
            "real_camera_invoked",
            "yolo_invoked",
            "ocr_invoked",
            "vlm_invoked",
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "ai_interpretation_invoked",
            "navigation_decision_invoked",
        )
        for k in audit_keys:
            if aud.get(k) is not False:
                blockers.append(f"audit_flag_not_false:{k}")

        if aud.get("video_ingest_executed") is not True:
            blockers.append("video_ingest_executed_not_true")

    if blockers:
        verdict = "NO_GO"
    elif missing_img > 0:
        soft.append(f"missing_image_ref_files:{missing_img}")
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "video_frame_minimal_ingest_verifier_report_v0",
        "phase": "Phase-Vision-VideoFrame-Minimal-Ingest-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "video_frame_minimal_ingest_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
