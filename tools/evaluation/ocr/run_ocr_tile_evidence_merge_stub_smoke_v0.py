#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Tile-Evidence-Merge-Stub-001 — multi-tile stub evidence merge smoke."""

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
    Image.new("RGB", (int(w), int(h)), (20, 60, 90)).save(path, format="PNG")


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

    img = out / "tile_merge_input.png"
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
        normalization_work_dir=out / "_work",
    )

    _write_json(out / "ocr_mainline_bridge_request.json", req.to_dict())
    _write_json(out / "ocr_mainline_bridge_result.json", result)

    ev = result.get("ocr_evidence") if isinstance(result.get("ocr_evidence"), dict) else {}
    bp = result.get("bridge_pack") if isinstance(result.get("bridge_pack"), dict) else {}
    merge = result.get("ocr_tile_evidence_merge_stub") if isinstance(result.get("ocr_tile_evidence_merge_stub"), dict) else {}
    aud = result.get("audit") if isinstance(result.get("audit"), dict) else {}

    items = ev.get("tile_evidence_items") if isinstance(ev.get("tile_evidence_items"), list) else merge.get("tile_evidence_items") or []

    summary = {
        "schema": "ocr_tile_evidence_merge_stub_summary_v0",
        "phase": "Phase-OCR-Tile-Evidence-Merge-Stub-001",
        "output_root": str(out),
        "input_width": int(args.width),
        "input_height": int(args.height),
        "bridge_status": result.get("status"),
        "tile_evidence_item_count": len(items),
        "materialized_tile_count": (result.get("ocr_provider_input_pack") or {}).get("tile_coverage", {}).get("materialized_tile_count"),
        "evidence_scope": ev.get("evidence_scope"),
        "text_joined_preview": (str(ev.get("text_joined") or ""))[:120],
    }
    _write_json(out / "ocr_tile_evidence_merge_stub_summary.json", summary)
    _write_json(out / "ocr_tile_evidence_items.json", {"schema": "ocr_tile_evidence_items_v0", "tile_evidence_items": items})

    coord_mtx: list = []
    for it in items:
        if isinstance(it, dict):
            coord_mtx.append(
                {
                    "tile_id": it.get("tile_id"),
                    "original_bbox": it.get("original_bbox"),
                    "original_polygon": it.get("original_polygon"),
                    "coordinate_transform_applied": it.get("coordinate_transform_applied"),
                }
            )
    _write_json(out / "ocr_tile_evidence_coordinate_matrix.json", {"schema": "ocr_tile_evidence_coordinate_matrix_v0", "items": coord_mtx})
    _write_json(out / "ocr_tile_evidence_merged_result.json", merge if merge else ev)
    _write_json(out / "ocr_tile_evidence_bridge_pack.json", bp)
    _write_json(out / "ocr_tile_evidence_source_chain.json", {"schema": "ocr_tile_evidence_source_chain_v0", "source_chain": result.get("source_chain")})
    _write_json(out / "ocr_tile_evidence_audit_report.json", aud)

    (out / "ocr_tile_evidence_merge_stub_notes.md").write_text(
        "# Phase-OCR-Tile-Evidence-Merge-Stub-001\n\nStub-only multi-tile merge; no real OCR.\n",
        encoding="utf-8",
    )

    vp = ws / "tools/evaluation/ocr/verify_ocr_tile_evidence_merge_stub_smoke_v0.py"
    if vp.is_file():
        subprocess.run([sys.executable, str(vp), "--smoke-root", str(out)], check=False)

    print(json.dumps({"tile_evidence_merge_smoke_root": str(out), "status": result.get("status")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
