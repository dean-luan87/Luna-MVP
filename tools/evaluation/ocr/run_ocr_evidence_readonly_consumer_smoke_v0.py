#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001 — read multi-ROI bridge_pack via read-only consumer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--bridge-pack",
        default="",
        help="Absolute path to ocr_lightweight_provider_multi_roi_bridge_pack.json (or any bridge_pack JSON)",
    )
    ap.add_argument(
        "--result-json",
        default="",
        help="Optional absolute path to mainline result JSON (for source_chain only)",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    bp_default = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_lightweight_provider_multi_roi_smoke_v0/"
        "ocr_lightweight_provider_multi_roi_bridge_pack.json"
    )
    bp_path = Path(args.bridge_pack).expanduser() if args.bridge_pack.strip() else bp_default
    if not bp_path.is_absolute():
        bp_path = (WS_ROOT / bp_path).resolve()
    bp_path = _require_abs(str(bp_path), "--bridge-pack (resolved)")
    if not bp_path.is_file():
        raise SystemExit(f"ERROR: bridge_pack not found: {bp_path}")

    res_path: Optional[Path] = None
    if args.result_json.strip():
        res_path = Path(args.result_json).expanduser()
        if not res_path.is_absolute():
            res_path = (WS_ROOT / res_path).resolve()
        res_path = _require_abs(str(res_path), "--result-json")
        if not res_path.is_file():
            raise SystemExit(f"ERROR: result json not found: {res_path}")
    else:
        cand = bp_path.parent / "ocr_lightweight_provider_multi_roi_result.json"
        if cand.is_file():
            res_path = cand

    bridge_pack = _read_json(bp_path)
    chain: List[str] = []
    if res_path and res_path.is_file():
        res = _read_json(res_path)
        sc = res.get("source_chain")
        if isinstance(sc, list):
            chain = [str(x) for x in sc]

    from capabilities.ocr_runtime.ocr_evidence_readonly_consumer_v0 import run_ocr_evidence_readonly_consume_v0

    summary, view, audit, val_errs = run_ocr_evidence_readonly_consume_v0(bridge_pack, source_reference_chain=chain or None)
    summary["input_bridge_pack_path"] = str(bp_path)
    summary["optional_result_json_path"] = str(res_path) if res_path else None

    by_roi = view.get("evidence_by_roi") if isinstance(view.get("evidence_by_roi"), dict) else {}
    geom = view.get("evidence_geometry_matrix") if isinstance(view.get("evidence_geometry_matrix"), list) else []

    chain_summary = view.get("source_reference_chain_summary") if isinstance(view.get("source_reference_chain_summary"), dict) else {}

    _write_json(out / "ocr_evidence_readonly_consumer_summary.json", summary)
    _write_json(out / "ocr_evidence_readonly_consumer_view.json", view)
    _write_json(out / "ocr_evidence_by_roi_matrix.json", by_roi)
    _write_json(out / "ocr_evidence_geometry_matrix.json", geom)
    _write_json(out / "ocr_evidence_source_chain_summary.json", chain_summary)
    _write_json(out / "ocr_evidence_readonly_consumer_audit_report.json", audit)

    (out / "ocr_evidence_readonly_consumer_notes.md").write_text(
        "# Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001\n\n"
        "Reads `ocr_evidence_pack_candidate_v0` **bridge_pack** (default: multi-ROI smoke output), "
        "builds a **read-only consumer_view** with ROI grouping and geometry matrix. "
        "No MidPlatform / Scene Delta / WorldModel writes; no AI interpretation.\n",
        encoding="utf-8",
    )

    if val_errs:
        _write_json(
            out / "ocr_evidence_readonly_consumer_validation_errors.json",
            {"errors": val_errs},
        )
    print(
        json.dumps(
            {
                "ocr_evidence_readonly_consumer_smoke_root": str(out),
                "input_bridge_pack": str(bp_path),
                "status": "success" if not val_errs else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not val_errs else 3


if __name__ == "__main__":
    raise SystemExit(main())
