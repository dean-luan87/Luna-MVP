#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Design-001 — Build design-only OcrEvidencePackV0 from OCR-007 routing pack.

No MidPlatform, no OCR provider, no runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import (  # noqa: E402
    build_ocr_evidence_pack_from_eval_routing_pack_v0,
    load_non_ocr_types_from_boundary_map_v0,
)
from capabilities.ocr_bridge.ocr_evidence_pack_validator_v0 import validate_ocr_evidence_pack_v0  # noqa: E402
from capabilities.ocr_bridge.ocr_midplatform_forwarding_contract_v0 import (  # noqa: E402
    decide_midplatform_forwarding_v0,
    merge_forwarding_into_pack_midplatform_contract,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eligibility-gate-root", required=True, help="OCR-007 output root containing ocr_evidence_routing_pack.json")
    ap.add_argument("--boundary-eval-root", default="", help="Override boundary eval root (default: read from ocr_eligibility_gate_summary.json)")
    ap.add_argument("--output-root", default="", help="Absolute output directory (default under ~/LunaRuntime/logs/ocr_bridge_design_001_<UTC>)")
    args = ap.parse_args()

    eg = _require_abs(args.eligibility_gate_root, "--eligibility-gate-root")
    summ_path = eg / "ocr_eligibility_gate_summary.json"
    if summ_path.is_file():
        summary = json.loads(summ_path.read_text(encoding="utf-8"))
        ber = str(summary.get("boundary_eval_root") or "")
    else:
        summary = {}
        ber = ""

    if args.boundary_eval_root.strip():
        boundary_root = _require_abs(args.boundary_eval_root, "--boundary-eval-root")
    elif ber:
        boundary_root = Path(ber).expanduser().resolve()
    else:
        raise SystemExit("ERROR: missing boundary_eval_root; pass --boundary-eval-root or ensure ocr_eligibility_gate_summary.json exists")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / f"ocr_bridge_design_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    rp_path = eg / "ocr_evidence_routing_pack.json"
    if not rp_path.is_file():
        raise SystemExit(f"ERROR: missing {rp_path}")
    routing_pack = json.loads(rp_path.read_text(encoding="utf-8"))

    non_ocr = load_non_ocr_types_from_boundary_map_v0(boundary_root / "ocr_capability_boundary_map.json")

    pack = build_ocr_evidence_pack_from_eval_routing_pack_v0(
        routing_pack=routing_pack,
        eligibility_gate_root=str(eg),
        boundary_eval_root=str(boundary_root),
    )

    val_report = validate_ocr_evidence_pack_v0(pack=pack, non_ocr_types=non_ocr)
    decision = decide_midplatform_forwarding_v0(
        pack=pack,
        validation_passed=bool(val_report.get("validation_passed")),
        non_ocr_types=non_ocr,
    )
    merge_forwarding_into_pack_midplatform_contract(pack, decision)

    trace = out_root / "ocr_bridge_design_trace.jsonl"
    replay = out_root / "ocr_bridge_design_replay.jsonl"
    for p in (trace, replay):
        if p.is_file():
            p.unlink()

    ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    for bucket in (
        "eligible_text_evidence",
        "conditional_text_evidence",
        "symbol_evidence",
        "glyph_evidence",
        "layout_evidence",
        "rejected_or_uncertain_evidence",
    ):
        for it in pack.get(bucket) or []:
            _append_jsonl(
                trace,
                {"ts": ts, "phase": "Phase-OCRBridge-Design-001", "bucket": bucket, "evidence_id": it.get("evidence_id")},
            )
            _append_jsonl(replay, {"evidence_id": it.get("evidence_id"), "bucket": bucket})

    notes = out_root / "bridge_design_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Bridge Design-001 — Evidence pack from evaluation routing",
                "",
                f"- **eligibility_gate_root**: `{eg}`",
                f"- **boundary_eval_root**: `{boundary_root}`",
                f"- **output_root**: `{out_root}`",
                "",
                "This pack is **design-only**. Source refs use `eval:*` URIs from Evaluation Tools output, not runtime.",
                "",
                f"- **validation_passed**: `{val_report.get('validation_passed')}`",
                f"- **forwarding_mode**: `{decision.get('forwarding_mode')}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    _write_json(out_root / "ocr_evidence_pack_example.json", pack)
    _write_json(out_root / "ocr_midplatform_forwarding_decision_example.json", decision)
    _write_json(out_root / "ocr_evidence_pack_validation_report.json", val_report)

    print(json.dumps({"output_root": str(out_root), "pack_id": pack.get("pack_id")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
