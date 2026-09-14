#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Mainline-Minimal-Bridge-001 — Smoke runner for OCR minimal mainline bridge (stub only).

Does not invoke PaddleOCR, RapidOCR, or production routing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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


def _ensure_smoke_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        Image.new("RGB", (512, 512), (220, 220, 220)).save(path, format="PNG")
    except Exception as e:
        raise SystemExit(f"ERROR: cannot create smoke image (PIL required): {e}") from e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument(
        "--governance-config",
        default="",
        help="Defaults to configs/ocr/ocr_image_input_governance_v0.example.json under workspace-root",
    )
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--image", default="", help="Absolute path to input image; if omitted, a 512x512 PNG is created under output-root")
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    if args.image.strip():
        img = _require_abs(args.image, "--image")
    else:
        img = out / "_smoke_input.png"
        _ensure_smoke_image(img)

    os.environ.setdefault("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "true")
    os.environ.setdefault("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true")
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"

    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    req = OCRRequestV0(
        image_path=str(img),
        input_type="image_path",
        latency_budget_ms=3000,
    )
    result = run_ocr_mainline_bridge_v0(
        req,
        governance_config_path=gov,
        workspace_root=ws,
        normalization_work_dir=out / "_norm_work",
    )

    _write_json(out / "ocr_mainline_bridge_request.json", req.to_dict())
    _write_json(out / "ocr_mainline_bridge_result.json", result)
    audit = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    _write_json(out / "ocr_mainline_bridge_audit_report.json", audit)
    summary = {
        "schema": "ocr_mainline_bridge_smoke_summary_v0",
        "phase": "Phase-OCR-Mainline-Minimal-Bridge-001",
        "workspace_root": str(ws),
        "governance_config": str(gov),
        "input_image_path": str(img),
        "output_root": str(out),
        "bridge_status": result.get("status"),
        "gate_verdict": (result.get("input_gate") or {}).get("gate_verdict"),
    }
    _write_json(out / "ocr_mainline_bridge_smoke_summary.json", summary)

    notes = [
        "# Phase-OCR-Mainline-Minimal-Bridge-001 — Smoke",
        "",
        f"- **output_root**: `{out}`",
        f"- **input_image_path**: `{img}`",
        f"- **status**: `{result.get('status')}`",
        "",
        "Stub-only; no PaddleOCR / no routing / no MidPlatform.",
        "",
    ]
    (out / "ocr_mainline_bridge_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    vp = ws / "tools/evaluation/ocr/verify_ocr_mainline_bridge_smoke_v0.py"
    if vp.is_file():
        import subprocess

        subprocess.run([sys.executable, str(vp), "--smoke-root", str(out), "--request-json", str(out / "ocr_mainline_bridge_request.json")], check=False)

    print(json.dumps({"smoke_output_root": str(out), "status": result.get("status")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
