#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Evaluation-Chain-Closure-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--roots-json", default="", help="Optional JSON map phase_key -> root")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_chain_closure_v0 import (
        DEFAULT_CHAIN_ROOTS,
        run_cross_modal_vision_ocr_chain_closure_v0,
    )

    roots: Dict[str, str] = dict(DEFAULT_CHAIN_ROOTS)
    if args.roots_json.strip():
        rp = Path(args.roots_json).expanduser()
        if not rp.is_absolute():
            rp = (WS_ROOT / rp).resolve()
        custom = json.loads(_require_abs(str(rp), "--roots-json").read_text(encoding="utf-8"))
        if isinstance(custom, dict):
            roots.update({str(k): str(v) for k, v in custom.items()})

    summary, phase_matrix, lineage, no_write, capability, non_claims, followups, audit, errs = (
        run_cross_modal_vision_ocr_chain_closure_v0(chain_roots=roots)
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "cross_modal_vision_ocr_chain_closure_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_phase_matrix.json", phase_matrix)
    _write_json(out / "cross_modal_vision_ocr_lineage_matrix.json", lineage)
    _write_json(out / "cross_modal_vision_ocr_no_write_boundary_matrix.json", no_write)
    _write_json(out / "cross_modal_vision_ocr_capability_closure_report.json", capability)
    _write_json(out / "cross_modal_vision_ocr_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_open_followups.json", followups)
    _write_json(out / "cross_modal_vision_ocr_chain_closure_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_chain_closure_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR Evaluation Chain Closure",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- chain_status: {summary.get('final_closure', {}).get('chain_status')}",
                f"- final_write_status: {summary.get('final_closure', {}).get('final_write_status')}",
                f"- no_write_all_phases_ok: {summary.get('no_write_all_phases_ok')}",
                "",
                "Read-only archive; no new capabilities; no writes.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "no_write_all_phases_ok": summary.get("no_write_all_phases_ok"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
