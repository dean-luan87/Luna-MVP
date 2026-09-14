#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001 — multi ROI pack → RapidOCR per unit → lift → merged bridge_pack."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_multi_roi_canvas(path: Path, *, width: int, height: int) -> Tuple[int, int, List[List[int]]]:
    """2200×2200 white canvas; text only inside three fixed ROIs."""
    from PIL import Image, ImageDraw, ImageFont

    w, h = int(width), int(height)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font: Any = None
    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            font = ImageFont.truetype(fp, 48)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()

    rois: List[Tuple[Tuple[int, int, int, int], str]] = [
        ((300, 400, 1000, 700), "LUNA ROI ONE"),
        ((1100, 900, 1900, 1200), "中文区域二"),
        ((500, 1400, 1600, 1700), "ROI THREE 123"),
    ]
    roi_boxes: List[List[int]] = []
    for (x0, y0, x1, y1), label in rois:
        roi_boxes.append([x0, y0, x1, y1])
        tx = x0 + 20
        ty = y0 + 30
        draw.text((tx, ty), label, fill=(0, 0, 0), font=font)

    img.save(path, format="PNG")
    return w, h, roi_boxes


class _EnvFrame:
    def __init__(self, updates: Dict[str, str]) -> None:
        self.updates = updates
        self._prev: Dict[str, Any] = {}

    def __enter__(self) -> "_EnvFrame":
        for k, v in self.updates.items():
            self._prev[k] = os.environ.get(k, _MISSING)
            os.environ[k] = v
        return self

    def __exit__(self, *args: object) -> None:
        for k, old in self._prev.items():
            if old is _MISSING:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old


_MISSING = object()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--width", type=int, default=2200)
    ap.add_argument("--height", type=int, default=2200)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov_src = (
        Path(args.governance_config).expanduser()
        if args.governance_config.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()

    gov = out / "ocr_lightweight_provider_multi_roi_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        _write_json(
            gov,
            {
                "schema_version": "ocr_image_input_governance_v0",
                "image_input_gate": {"enabled": True, "full_image_realtime_allowed": False, "roi_first_required": True},
                "size_limits": {
                    "max_width_realtime": 2048,
                    "max_height_realtime": 2048,
                    "max_megapixels_realtime": 4.0,
                    "max_megapixels_heavy_local": 8.0,
                    "max_megapixels_requires_tiling": 8.0,
                },
                "downscale_policy": {
                    "enabled": True,
                    "preferred_max_side": 512,
                    "fallback_max_side": 512,
                    "preserve_aspect_ratio": True,
                    "record_downscale_ratio": True,
                },
                "tiling_policy": {
                    "enabled": True,
                    "tile_max_side": 1600,
                    "tile_overlap_ratio": 0.12,
                    "max_tile_count_sync": 4,
                    "max_tile_count_async": 16,
                    "requires_coordinate_reconstruction": True,
                    "requires_duplicate_text_merge": True,
                },
                "source_chain_policy": {
                    "record_original_image_ref": True,
                    "record_transformed_image_ref": True,
                    "record_tile_ref": True,
                    "record_coordinate_transform": True,
                },
                "stcm_policy": {
                    "large_image_default_async": True,
                    "expired_tile_result_cannot_drive_action": True,
                    "timeout_must_notify_orchestrator": True,
                },
                "forbidden_actions": {
                    "send_oversized_full_image_to_realtime_ocr": True,
                    "drop_coordinate_mapping": True,
                    "force_reading_order_without_confidence": True,
                    "direct_midplatform_write": True,
                    "direct_world_model_write": True,
                },
                "evidence_notes": {"purpose": "embedded_lightweight_multi_roi_smoke_v0"},
            },
        )
    gov = _require_abs(str(gov), "governance under output-root")

    img_path = out / "ocr_lightweight_provider_multi_roi_original.png"
    ow, oh, roi_boxes = _write_multi_roi_canvas(img_path, width=args.width, height=args.height)
    roi_refs = [f"{b[0]},{b[1]},{b[2]},{b[3]}" for b in roi_boxes]

    env_updates = {
        "LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0": "true",
        "LUNA_ENABLE_OCR_STUB_PROVIDER_V0": "true",
        "LUNA_ENABLE_OCR_REAL_PROVIDER_V0": "true",
        "LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0": "true",
        "LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0": "false",
        "LUNA_ENABLE_OCR_TILE_PLANNER_V0": "false",
    }

    with _EnvFrame(env_updates):
        from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
        from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

        req = OCRRequestV0(
            image_path=str(img_path),
            input_type="roi_list",
            roi_refs=roi_refs,
            latency_budget_ms=15000,
            allow_full_image=False,
            allow_heavy_ocr=False,
            allow_remote=False,
        )
        result = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=gov,
            workspace_root=ws,
            normalization_pipeline_enabled=True,
            normalization_work_dir=out / "_norm_work",
        )

    pack = result.get("ocr_provider_input_pack") if isinstance(result.get("ocr_provider_input_pack"), dict) else {}
    units = pack.get("input_units") if isinstance(pack.get("input_units"), list) else []
    ev = result.get("ocr_evidence") if isinstance(result.get("ocr_evidence"), dict) else {}
    bp = result.get("bridge_pack") if isinstance(result.get("bridge_pack"), dict) else {}
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    ctm = result.get("coordinate_transform_matrix") if isinstance(result.get("coordinate_transform_matrix"), dict) else {}

    lift_matrix = {
        "schema": "ocr_lightweight_provider_multi_roi_coordinate_lift_matrix_v0",
        "coordinate_transform_matrix": ctm,
        "text_items_geometry": [
            {
                "unit_id": it.get("unit_id"),
                "roi_id": it.get("roi_id"),
                "source_unit_ref": it.get("source_unit_ref"),
                "local_bbox": it.get("local_bbox"),
                "original_bbox": it.get("original_bbox"),
                "coordinate_lift_applied": it.get("coordinate_lift_applied"),
            }
            for it in (ev.get("text_items") or [])
            if isinstance(it, dict)
        ],
    }

    per_roi = ev.get("per_roi_provider_status") if isinstance(ev.get("per_roi_provider_status"), list) else []
    if not per_roi and isinstance(result.get("provider_result"), dict):
        per_roi = (result["provider_result"].get("provider_raw_ref") or {}).get("per_roi_provider_status") or []

    summary = {
        "schema": "ocr_lightweight_provider_multi_roi_smoke_summary_v0",
        "phase": "Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001",
        "output_root": str(out),
        "original_image_path": str(img_path),
        "original_width": ow,
        "original_height": oh,
        "roi_list_xyxy": roi_boxes,
        "input_units_count": len(units),
        "processing_strategy": (pack.get("processing_policy") or {}).get("strategy") if isinstance(pack.get("processing_policy"), dict) else None,
        "selected_provider": aud.get("selected_provider"),
        "text_joined_preview": (str(ev.get("text_joined") or ""))[:400],
        "per_roi_provider_status": per_roi,
        "roi_unit_count": aud.get("roi_unit_count"),
        "multi_roi_processed": aud.get("multi_roi_processed"),
        "reading_order_candidate": ev.get("reading_order_candidate"),
    }

    _write_json(out / "ocr_lightweight_provider_multi_roi_smoke_summary.json", summary)
    _write_json(out / "ocr_lightweight_provider_multi_roi_request.json", req.to_dict())
    _write_json(out / "ocr_lightweight_provider_multi_roi_input_pack.json", pack)
    _write_json(out / "ocr_lightweight_provider_multi_roi_result.json", result)
    _write_json(out / "ocr_lightweight_provider_multi_roi_bridge_pack.json", bp)
    _write_json(out / "ocr_lightweight_provider_multi_roi_coordinate_lift_matrix.json", lift_matrix)
    _write_json(out / "ocr_lightweight_provider_multi_roi_audit_report.json", aud)

    (out / "ocr_lightweight_provider_multi_roi_notes.md").write_text(
        "# Phase-OCR-Lightweight-Provider-Multi-ROI-Smoke-001\n\n"
        "Three disjoint ROIs on a 2200×2200 canvas → `roi_list` pack with multiple `roi` units → "
        "RapidOCR invoked **per unit** → coordinate lift per ROI → merged `bridge_pack.eligible_text_evidence`. "
        "Reading order is **roi_order_then_provider_order** placeholder only (no layout semantics). "
        "No MidPlatform; no PaddleOCR; no Scene Delta.\n",
        encoding="utf-8",
    )
    print(json.dumps({"ocr_lightweight_provider_multi_roi_smoke_root": str(out), "status": "success"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
