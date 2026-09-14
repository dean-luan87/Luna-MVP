#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Tile-Coverage-And-Truncation-Policy-001 — Coverage / truncation semantics smoke (no real OCR).

Re-runs tile bridge (LUNA_ENABLE_OCR_TILE_PLANNER_V0=true) and writes coverage artifacts + verifiers.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
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


def _gen_png(path: Path, w: int, h: int) -> None:
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (int(w), int(h)), (30, 100, 70)).save(path, format="PNG")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--width", type=int, default=3000)
    ap.add_argument("--height", type=int, default=5334)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    img = out / "tile_coverage_input.png"
    _gen_png(img, args.width, args.height)

    os.environ.setdefault("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "true")
    os.environ.setdefault("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true")
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_OCR_TILE_PLANNER_V0"] = "true"

    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    req = OCRRequestV0(image_path=str(img), input_type="image_path", latency_budget_ms=8000)
    result = run_ocr_mainline_bridge_v0(
        req,
        governance_config_path=gov,
        workspace_root=ws,
        normalization_pipeline_enabled=True,
        normalization_work_dir=out / "_tile_work",
    )

    _write_json(out / "ocr_mainline_bridge_request.json", req.to_dict())
    _write_json(out / "ocr_mainline_bridge_result.json", result)

    pack = result.get("ocr_provider_input_pack") if isinstance(result.get("ocr_provider_input_pack"), dict) else {}
    tile_plan = result.get("tile_plan") if isinstance(result.get("tile_plan"), dict) else {}
    mtx = result.get("coordinate_transform_matrix") if isinstance(result.get("coordinate_transform_matrix"), dict) else {}
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}
    tc = pack.get("tile_coverage") if isinstance(pack.get("tile_coverage"), dict) else {}

    _write_json(out / "ocr_provider_input_pack.json", pack)
    _write_json(out / "ocr_tile_plan.json", tile_plan)
    _write_json(out / "ocr_tile_coordinate_transform_matrix.json", mtx)
    _write_json(out / "ocr_tile_planner_audit_report.json", aud)

    _write_json(out / "ocr_tile_coverage_summary.json", tc)
    _write_json(out / "ocr_tile_coverage_matrix.json", mtx)
    _write_json(out / "ocr_tile_uncovered_regions.json", {"schema": "ocr_tile_uncovered_regions_v0", "uncovered_regions": tile_plan.get("uncovered_regions")})
    trunc_rep = {
        "schema": "ocr_tile_truncation_policy_report_v0",
        "truncated_to_budget": bool(tile_plan.get("truncated_to_budget")),
        "truncated_to_max_tile_count_sync": bool(tile_plan.get("truncated_to_max_tile_count_sync")),
        "max_tile_count_applied": tile_plan.get("max_tile_count_applied"),
        "tile_budget_type": tile_plan.get("tile_budget_type"),
        "async_completion_available": tile_plan.get("async_completion_available"),
        "processing_policy": pack.get("processing_policy"),
    }
    _write_json(out / "ocr_tile_truncation_policy_report.json", trunc_rep)
    _write_json(out / "ocr_tile_coverage_audit_report.json", aud)

    notes = [
        "# Phase-OCR-Tile-Coverage-And-Truncation-Policy-001",
        "",
        f"- **output_root**: `{out}`",
        "",
        "See `ocr_tile_coverage_summary.json` and `ocr_tile_truncation_policy_report.json`.",
        "",
    ]
    (out / "ocr_tile_coverage_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    for vp in (
        ws / "tools/evaluation/ocr/verify_ocr_tile_planner_smoke_v0.py",
        ws / "tools/evaluation/ocr/verify_ocr_tile_coverage_policy_smoke_v0.py",
    ):
        if vp.is_file():
            subprocess.run([sys.executable, str(vp), "--smoke-root", str(out)], check=False)

    print(json.dumps({"tile_coverage_smoke_root": str(out), "status": result.get("status")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
