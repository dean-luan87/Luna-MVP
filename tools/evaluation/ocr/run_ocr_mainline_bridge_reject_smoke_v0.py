#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Mainline-InputGate-Reject-Smoke-001 — Oversized image must REJECT before provider.

No real OCR, no routing, no MidPlatform.
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


def _generate_oversized_png(path: Path, width: int, height: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        Image.new("RGB", (int(width), int(height)), (40, 40, 40)).save(path, format="PNG")
    except Exception as e:
        raise SystemExit(f"ERROR: cannot generate oversized PNG: {e}") from e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--width", type=int, default=3000)
    ap.add_argument("--height", type=int, default=5334)
    ap.add_argument("--image-out", default="", help="Absolute path to write generated PNG; default under output-root")
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    if args.image_out.strip():
        img = _require_abs(args.image_out, "--image-out")
    else:
        img = out / "_reject_oversized_input.png"
    _generate_oversized_png(img, args.width, args.height)

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
        allow_full_image=False,
        allow_heavy_ocr=False,
        allow_remote=False,
    )
    result = run_ocr_mainline_bridge_v0(
        req,
        governance_config_path=gov,
        workspace_root=ws,
        normalization_pipeline_enabled=False,
    )

    _write_json(out / "ocr_mainline_bridge_reject_request.json", req.to_dict())
    _write_json(out / "ocr_mainline_bridge_reject_result.json", result)
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    _write_json(out / "ocr_mainline_bridge_reject_audit_report.json", aud)

    ig = result.get("input_gate") if isinstance(result.get("input_gate"), dict) else {}
    summary = {
        "schema": "ocr_mainline_bridge_reject_smoke_summary_v0",
        "phase": "Phase-OCR-Mainline-InputGate-Reject-Smoke-001",
        "workspace_root": str(ws),
        "governance_config": str(gov),
        "generated_image_path": str(img),
        "image_width": args.width,
        "image_height": args.height,
        "allow_full_image": False,
        "output_root": str(out),
        "gate_verdict": ig.get("gate_verdict"),
        "oversized": ig.get("oversized"),
        "recommended_input_strategy": ig.get("recommended_input_strategy"),
        "bridge_status": result.get("status"),
    }
    _write_json(out / "ocr_mainline_bridge_reject_smoke_summary.json", summary)

    notes = [
        "# Phase-OCR-Mainline-InputGate-Reject-Smoke-001",
        "",
        f"- **output_root**: `{out}`",
        f"- **image**: `{img}` ({args.width}x{args.height})",
        f"- **gate_verdict**: `{ig.get('gate_verdict')}`",
        f"- **bridge status**: `{result.get('status')}`",
        "",
        "Expect REJECT before stub provider; no MOCK_TEXT evidence.",
        "",
    ]
    (out / "ocr_mainline_bridge_reject_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    vp = ws / "tools/evaluation/ocr/verify_ocr_mainline_bridge_reject_smoke_v0.py"
    if vp.is_file():
        import subprocess

        subprocess.run([sys.executable, str(vp), "--smoke-root", str(out)], check=False)

    print(json.dumps({"reject_smoke_output_root": str(out), "status": result.get("status")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
