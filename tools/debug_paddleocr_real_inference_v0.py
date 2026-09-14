#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _load(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--sample-ids", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    manifest = _load(args.dataset_manifest if os.path.isabs(args.dataset_manifest) else os.path.abspath(os.path.join(REPO_ROOT, args.dataset_manifest)))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out, exist_ok=True)
    sample_ids = [x.strip() for x in str(args.sample_ids).split(",") if x.strip()]
    sample_map = {str(s.get("sample_id")): s for s in (manifest.get("samples") or []) if isinstance(s, dict)}

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0
    adapter = PaddleOCRAdapterV0(enable_real_inference=True, config_profile="config_baseline")

    per_raw: Dict[str, Any] = {}
    per_norm: Dict[str, Any] = {}
    input_report: List[Dict[str, Any]] = []
    lat_breakdown: Dict[str, float] = {}
    coord = {"status": "polygon_to_xyxy_aabb", "bbox_present_samples": 0}
    model_path_report: Dict[str, Any] = {}

    for sid in sample_ids:
        s = sample_map.get(sid)
        if not s:
            continue
        img = str(s.get("image_path") or "")
        img_abs = img if os.path.isabs(img) else os.path.abspath(os.path.join(REPO_ROOT, img))
        r = adapter.recognize_image(image_path=img_abs, frame_id=str(s.get("frame_id") or sid), timestamp_ms=int(s.get("timestamp_ms") or 0))
        per_raw[sid] = r
        per_norm[sid] = {
            "sample_id": sid,
            "raw_text_joined": r.get("raw_text_joined"),
            "candidate_count": len(r.get("raw_text_candidates") or []),
            "candidates": r.get("raw_text_candidates"),
        }
        lat_breakdown[sid] = float(r.get("latency_ms") or 0.0)
        if any(isinstance(c, dict) and c.get("bbox") is not None for c in (r.get("raw_text_candidates") or [])):
            coord["bbox_present_samples"] += 1
        if not model_path_report:
            model_path_report = (r.get("provider_details") or {}).get("model_path_report") or {}
        input_report.append({"sample_id": sid, "image_path": img, "image_exists": os.path.isfile(img_abs)})

    _write(os.path.join(out, "per_sample_raw_paddle_output.json"), per_raw)
    _write(os.path.join(out, "per_sample_normalized_candidates.json"), per_norm)
    _write(os.path.join(out, "model_path_report.json"), model_path_report)
    _write(os.path.join(out, "coordinate_conversion_report.json"), coord)
    _write(os.path.join(out, "input_image_report.json"), input_report)
    _write(os.path.join(out, "latency_breakdown.json"), lat_breakdown)
    summary = {
        "phase": "Phase-ModelOCR-006B",
        "sample_ids": sample_ids,
        "model_path_report_ref": "model_path_report.json",
        "coordinate_conversion_report_ref": "coordinate_conversion_report.json",
        "input_image_report_ref": "input_image_report.json",
        "latency_breakdown_ref": "latency_breakdown.json",
    }
    _write(os.path.join(out, "debug_summary.json"), summary)
    with open(os.path.join(out, "debug_notes.md"), "w", encoding="utf-8") as nf:
        nf.write("## PaddleOCR debug\n\n- raw output captured\n- normalization captured\n- no semantic output\n")
    print(json.dumps({"ok": True, "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
