#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-ImageInput-Normalization-Pipeline-001 — Smoke A (small) + B (large), stub only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

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
    Image.new("RGB", (int(w), int(h)), (50, 80, 120)).save(path, format="PNG")


def _run_one(
    *,
    case_id: str,
    width: int,
    height: int,
    out_dir: Path,
    ws: Path,
    gov: Path,
) -> Dict[str, Any]:
    cdir = out_dir / case_id
    cdir.mkdir(parents=True, exist_ok=True)
    img = cdir / "input.png"
    _gen_png(img, width, height)
    os.environ.setdefault("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "true")
    os.environ.setdefault("LUNA_ENABLE_OCR_STUB_PROVIDER_V0", "true")
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"

    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    req = OCRRequestV0(image_path=str(img), input_type="image_path", latency_budget_ms=5000)
    res = run_ocr_mainline_bridge_v0(
        req,
        governance_config_path=gov,
        workspace_root=ws,
        normalization_pipeline_enabled=True,
        normalization_work_dir=cdir / "_work",
    )
    _write_json(cdir / "ocr_mainline_bridge_request.json", req.to_dict())
    _write_json(cdir / "ocr_mainline_bridge_result.json", res)
    _write_json(cdir / "ocr_mainline_bridge_audit_report.json", res.get("audit") or {})
    if res.get("metadata_probe"):
        _write_json(cdir / "ocr_image_metadata_probe.json", res["metadata_probe"])
    if res.get("input_decision"):
        _write_json(cdir / "ocr_image_input_decision.json", res["input_decision"])
    if res.get("coordinate_transform_matrix"):
        _write_json(cdir / "ocr_coordinate_transform_matrix.json", res["coordinate_transform_matrix"])
    if res.get("ocr_provider_input_pack"):
        _write_json(cdir / "ocr_provider_input_pack.json", res["ocr_provider_input_pack"])
    return {"case_id": case_id, "result": res}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (ws / "configs/ocr/ocr_image_input_governance_v0.example.json")
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    small = _run_one(case_id="small", width=512, height=512, out_dir=out, ws=ws, gov=gov)
    large = _run_one(case_id="large", width=3000, height=5334, out_dir=out, ws=ws, gov=gov)

    def _probe(c: Dict[str, Any]) -> Any:
        return (c.get("result") or {}).get("metadata_probe")

    def _dec(c: Dict[str, Any]) -> Any:
        return (c.get("result") or {}).get("input_decision")

    def _ct(c: Dict[str, Any]) -> Any:
        return (c.get("result") or {}).get("coordinate_transform_matrix")

    def _pack(c: Dict[str, Any]) -> Any:
        return (c.get("result") or {}).get("ocr_provider_input_pack")

    agg_probe = {"schema": "ocr_image_metadata_probe_bundle_v0", "cases": [{"case_id": small["case_id"], "probe": _probe(small)}, {"case_id": large["case_id"], "probe": _probe(large)}]}
    agg_dec = {"schema": "ocr_image_input_decision_bundle_v0", "cases": [{"case_id": small["case_id"], "decision": _dec(small)}, {"case_id": large["case_id"], "decision": _dec(large)}]}
    agg_ct = {"schema": "ocr_coordinate_transform_matrix_bundle_v0", "cases": [{"case_id": small["case_id"], "matrix": _ct(small)}, {"case_id": large["case_id"], "matrix": _ct(large)}]}
    agg_pack = {"schema": "ocr_provider_input_pack_bundle_v0", "cases": [{"case_id": small["case_id"], "pack": _pack(small)}, {"case_id": large["case_id"], "pack": _pack(large)}]}

    _write_json(out / "ocr_image_metadata_probe.json", agg_probe)
    _write_json(out / "ocr_image_input_decision.json", agg_dec)
    _write_json(out / "ocr_coordinate_transform_matrix.json", agg_ct)
    _write_json(out / "ocr_provider_input_pack.json", agg_pack)

    aud_merged = {
        "schema": "ocr_image_input_normalization_audit_bundle_v0",
        "small": (small["result"].get("audit") or {}),
        "large": (large["result"].get("audit") or {}),
    }
    _write_json(out / "ocr_image_input_normalization_audit_report.json", aud_merged)

    summary = {
        "schema": "ocr_image_input_normalization_summary_v0",
        "phase": "Phase-OCR-ImageInput-Normalization-Pipeline-001",
        "output_root": str(out),
        "small_status": (small["result"].get("status")),
        "large_status": (large["result"].get("status")),
        "small_gate": (small["result"].get("input_gate") or {}).get("gate_verdict"),
        "large_gate": (large["result"].get("input_gate") or {}).get("gate_verdict"),
        "large_original_direct": (large["result"].get("audit") or {}).get("original_image_used_directly"),
        "large_downscale_applied": (large["result"].get("audit") or {}).get("downscale_applied"),
    }
    _write_json(out / "ocr_image_input_normalization_summary.json", summary)

    notes = [
        "# Phase-OCR-ImageInput-Normalization-Pipeline-001",
        "",
        f"- **output_root**: `{out}`",
        f"- **small**: `{out / 'small'}` status={small['result'].get('status')}",
        f"- **large**: `{out / 'large'}` status={large['result'].get('status')}",
        "",
    ]
    (out / "ocr_image_input_normalization_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    vp = ws / "tools/evaluation/ocr/verify_ocr_image_input_normalization_smoke_v0.py"
    if vp.is_file():
        import subprocess

        subprocess.run([sys.executable, str(vp), "--smoke-root", str(out)], check=False)

    print(json.dumps({"normalization_smoke_root": str(out), "small": summary["small_status"], "large": summary["large_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
