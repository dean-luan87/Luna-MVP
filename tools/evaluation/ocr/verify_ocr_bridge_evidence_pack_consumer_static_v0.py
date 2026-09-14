#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001 — Verifier for consumer static test outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--consumer-static-root",
        required=True,
        help="Output root of test_ocr_bridge_evidence_pack_consumer_static_v0.py",
    )
    args = ap.parse_args()

    root = _require_abs(args.consumer_static_root, "--consumer-static-root")
    blockers: List[str] = []

    sum_p = root / "ocr_bridge_pack_consumer_static_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_consumer_static_summary")
        summary: Dict[str, Any] = {}
    else:
        summary = _read_json(sum_p)

    bridge_root = Path(str(summary.get("bridge_alignment_output_root") or "")).expanduser()
    if summary and (not bridge_root.is_absolute() or not bridge_root.is_dir()):
        blockers.append("invalid_bridge_alignment_output_root_in_summary")

    if summary.get("bridge_alignment_summary_verdict") != "GO":
        blockers.append(f"bridge_alignment_summary_not_go:{summary.get('bridge_alignment_summary_verdict')}")
    if summary.get("bridge_alignment_verifier_verdict") != "GO":
        blockers.append(f"bridge_alignment_verifier_not_go:{summary.get('bridge_alignment_verifier_verdict')}")

    if summary.get("consumer_static_verdict") != "GO":
        blockers.append(f"consumer_static_verdict_not_go:{summary.get('consumer_static_verdict')}")

    errs = summary.get("errors") if isinstance(summary.get("errors"), list) else []
    if errs:
        blockers.append(f"summary_errors:{errs}")

    if int(summary.get("eligible_text_evidence_total_count") or 0) <= 0:
        blockers.append("eligible_text_evidence_count_not_positive")

    for name in (
        "ocr_bridge_pack_consumer_static_field_access_matrix.json",
        "ocr_bridge_pack_consumer_static_item_walk_report.json",
        "ocr_bridge_pack_consumer_static_provisional_field_report.json",
        "ocr_bridge_pack_consumer_static_source_chain_report.json",
        "ocr_bridge_pack_consumer_static_audit_report.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing_output:{name}")

    matrix_p = root / "ocr_bridge_pack_consumer_static_field_access_matrix.json"
    if matrix_p.is_file():
        mdoc = _read_json(matrix_p)
        rows = mdoc.get("rows") if isinstance(mdoc.get("rows"), list) else []
        for r in rows:
            if not isinstance(r, dict):
                continue
            if r.get("field") == "text" and r.get("accessible") is not True:
                blockers.append(f"matrix_text_not_accessible:pack_{r.get('pack_index')}:item_{r.get('item_index')}")
            if r.get("field") == "confidence" and r.get("accessible") is not True:
                blockers.append(f"matrix_confidence_not_accessible:pack_{r.get('pack_index')}:item_{r.get('item_index')}")
            if r.get("field") in ("polygon", "score", "reading_order_index") and r.get("present") and r.get("accessible") is not True:
                blockers.append(
                    f"matrix_provisional_lost:{r.get('field')}:pack_{r.get('pack_index')}:item_{r.get('item_index')}"
                )

    aud_p = root / "ocr_bridge_pack_consumer_static_audit_report.json"
    if aud_p.is_file():
        aud = _read_json(aud_p)
        for k in (
            "network_request_invoked",
            "paddleocr_invoked",
            "ocr_inference_invoked",
            "ocr_routing_changed",
            "rapidocr_replaced",
            "runtime_integration",
            "whitebox_integration",
            "midplatform_invoked",
            "world_model_written",
            "midplatform_semantics_written",
        ):
            if aud.get(k) is True:
                blockers.append(f"consumer_audit_true:{k}")

    verdict = "NO_GO" if blockers else "GO"

    rep = {
        "schema": "ocr_bridge_pack_consumer_static_verifier_report_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001",
        "consumer_static_root": str(root),
        "bridge_alignment_output_root": str(bridge_root) if bridge_root.is_dir() else str(summary.get("bridge_alignment_output_root") or ""),
        "verdict": verdict,
        "blockers": sorted(set(blockers)),
    }
    (root / "ocr_bridge_pack_consumer_static_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"consumer_static_root": str(root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
