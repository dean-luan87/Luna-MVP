#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001 — large canvas + ROI text → crop ROI pack → RapidOCR lightweight."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

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


def _write_roi_canvas_png(
    path: Path,
    *,
    width: int,
    height: int,
    roi_xyxy: Tuple[int, int, int, int],
) -> Tuple[int, int, Tuple[int, int, int, int]]:
    """White canvas; text only inside ROI bbox (xyxy)."""
    from PIL import Image, ImageDraw, ImageFont

    w, h = int(width), int(height)
    x0, y0, x1, y1 = roi_xyxy
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
            font = ImageFont.truetype(fp, 56)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    lines = ("LUNA ROI TEST 123", "中文ROI测试")
    tx = x0 + 24
    ty = y0 + 40
    line_gap = 90 if font != ImageFont.load_default() else 20
    for line in lines:
        draw.text((tx, ty), line, fill=(0, 0, 0), font=font)
        ty += line_gap
    img.save(path, format="PNG")
    return w, h, (x0, y0, x1, y1)


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
    ap.add_argument("--roi", default="400,500,1200,800", help="ROI xyxy comma-separated")
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    parts = [p.strip() for p in str(args.roi).split(",")]
    if len(parts) != 4:
        raise SystemExit("ERROR: --roi must be x0,y0,x1,y1")
    roi_xyxy = (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))

    gov_src = (
        Path(args.governance_config).expanduser()
        if args.governance_config.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()

    gov = out / "ocr_lightweight_provider_roi_input_governance.json"
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
                "evidence_notes": {"purpose": "embedded_lightweight_roi_smoke_v0"},
            },
        )
    gov = _require_abs(str(gov), "governance under output-root")

    img_path = out / "ocr_lightweight_provider_roi_input_original.png"
    ow, oh, roi_t = _write_roi_canvas_png(img_path, width=args.width, height=args.height, roi_xyxy=roi_xyxy)
    roi_ref_str = f"{roi_t[0]},{roi_t[1]},{roi_t[2]},{roi_t[3]}"

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
            input_type="roi",
            roi_refs=[roi_ref_str],
            latency_budget_ms=12000,
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
    u0 = units[0] if units and isinstance(units[0], dict) else {}
    roi_src = str(u0.get("image_ref") or "")
    roi_out = out / "ocr_lightweight_provider_roi_input_roi.png"
    if roi_src and Path(roi_src).is_file():
        shutil.copy2(Path(roi_src), roi_out)

    nw, nh = int(u0.get("width") or 0), int(u0.get("height") or 0)

    _write_json(out / "ocr_lightweight_provider_roi_input_request.json", req.to_dict())
    _write_json(out / "ocr_lightweight_provider_roi_input_result.json", result)
    _write_json(out / "ocr_lightweight_provider_roi_input_pack.json", pack)
    ev = result.get("ocr_evidence") if isinstance(result.get("ocr_evidence"), dict) else {}
    bp = result.get("bridge_pack") if isinstance(result.get("bridge_pack"), dict) else {}
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    tf = pack.get("coordinate_transform") if isinstance(pack.get("coordinate_transform"), dict) else {}
    _write_json(out / "ocr_lightweight_provider_roi_input_bridge_pack.json", bp)
    _write_json(out / "ocr_lightweight_provider_roi_input_audit_report.json", aud)

    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []
    summary = {
        "schema": "ocr_lightweight_provider_roi_input_summary_v0",
        "phase": "Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001",
        "output_root": str(out),
        "governance_config": str(gov),
        "original_image_path": str(img_path),
        "original_width": ow,
        "original_height": oh,
        "roi_bbox_xyxy": list(roi_t),
        "roi_crop_path_in_pack": roi_src,
        "roi_image_saved": str(roi_out) if roi_out.is_file() else "",
        "normalized_unit_width": nw,
        "normalized_unit_height": nh,
        "unit_type": u0.get("unit_type"),
        "bridge_status": result.get("status"),
        "downscale_applied": aud.get("downscale_applied"),
        "original_image_used_directly": aud.get("original_image_used_directly"),
        "coordinate_transform_recorded": aud.get("coordinate_transform_recorded"),
        "selected_provider": aud.get("selected_provider"),
        "real_provider_invoked": aud.get("real_provider_invoked"),
        "text_item_count": len(items),
        "text_joined_preview": (str(ev.get("text_joined") or ""))[:280],
        "coordinate_transform": {
            "mode": tf.get("mode"),
            "offset_x": tf.get("offset_x"),
            "offset_y": tf.get("offset_y"),
            "roi_source_width": tf.get("roi_source_width"),
            "roi_source_height": tf.get("roi_source_height"),
            "transformed_width": tf.get("transformed_width"),
            "transformed_height": tf.get("transformed_height"),
            "scale_x": tf.get("scale_x"),
            "scale_y": tf.get("scale_y"),
        },
    }
    _write_json(out / "ocr_lightweight_provider_roi_input_summary.json", summary)

    (out / "ocr_lightweight_provider_roi_input_notes.md").write_text(
        "# Phase-OCR-Lightweight-Provider-ROI-Input-Smoke-001\n\n"
        "Large white canvas with text **only inside** the requested ROI → normalization **ROI branch** "
        "(`unit_type=roi`, optional inner downscale when ROI max edge exceeds `LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX`) "
        "→ RapidOCR lightweight. Not a benchmark; no MidPlatform; no routing change; PaddleOCR disabled.\n",
        encoding="utf-8",
    )
    print(json.dumps({"ocr_lightweight_provider_roi_input_smoke_root": str(out), "status": "success"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
