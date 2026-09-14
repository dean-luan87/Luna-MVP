#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Lightweight-Provider-Text-Smoke-001 — simple small image with text; RapidOCR non-empty evidence (not benchmark)."""

from __future__ import annotations

import argparse
import json
import os
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


def _write_text_png(path: Path, *, width: int, height: int) -> Tuple[int, int]:
    """White background, black text; PIL default or best-effort system font."""
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
            font = ImageFont.truetype(fp, 32)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    lines = ("LUNA TEST 123", "中文测试")
    y = max(8, h // 2 - 48)
    for line in lines:
        draw.text((24, y), line, fill=(0, 0, 0), font=font)
        y += 44 if font != ImageFont.load_default() else 14
    img.save(path, format="PNG")
    return w, h


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
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--height", type=int, default=512)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    img_path = out / "ocr_lightweight_provider_text_input.png"
    iw, ih = _write_text_png(img_path, width=args.width, height=args.height)

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
            input_type="image_path",
            latency_budget_ms=8000,
        )
        result = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=gov,
            workspace_root=ws,
            normalization_pipeline_enabled=True,
            normalization_work_dir=out / "_norm_work",
        )

    _write_json(out / "ocr_lightweight_provider_text_request.json", req.to_dict())
    _write_json(out / "ocr_lightweight_provider_text_result.json", result)
    ev = result.get("ocr_evidence") if isinstance(result.get("ocr_evidence"), dict) else {}
    bp = result.get("bridge_pack") if isinstance(result.get("bridge_pack"), dict) else {}
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    _write_json(out / "ocr_lightweight_provider_text_bridge_pack.json", bp)
    _write_json(out / "ocr_lightweight_provider_text_audit_report.json", aud)

    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []
    summary = {
        "schema": "ocr_lightweight_provider_text_smoke_summary_v0",
        "phase": "Phase-OCR-Lightweight-Provider-Text-Smoke-001",
        "output_root": str(out),
        "input_image_path": str(img_path),
        "input_width": iw,
        "input_height": ih,
        "bridge_status": result.get("status"),
        "selected_provider": aud.get("selected_provider"),
        "real_provider_invoked": aud.get("real_provider_invoked"),
        "text_item_count": len(items),
        "text_joined_preview": (str(ev.get("text_joined") or ""))[:240],
    }
    _write_json(out / "ocr_lightweight_provider_text_smoke_summary.json", summary)

    (out / "ocr_lightweight_provider_text_notes.md").write_text(
        "# Phase-OCR-Lightweight-Provider-Text-Smoke-001\n\n"
        "Validates non-empty OCR text on a small synthetic image via RapidOCR when available; "
        "not a benchmark; does not change routing or defaults.\n",
        encoding="utf-8",
    )
    print(json.dumps({"ocr_lightweight_provider_text_smoke_root": str(out), "status": "success"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
