#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Review-001 — Verifier for OCR bridge interface freeze review outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design-root", required=True)
    ap.add_argument("--review-output-root", required=True)
    ap.add_argument("--luna-core-root", default=REPO_ROOT)
    args = ap.parse_args()

    dr = Path(args.design_root).expanduser().resolve()
    rr = Path(args.review_output_root).expanduser().resolve()
    lc = Path(args.luna_core_root).expanduser().resolve()

    blockers: List[str] = []

    if not dr.is_dir():
        blockers.append("A_design_root_not_dir")
    elif not (dr / "ocr_evidence_pack_example.json").is_file():
        blockers.append("B_missing_evidence_pack_example")

    required_out = [
        "ocr_bridge_interface_freeze_summary.json",
        "ocr_bridge_required_fields_matrix.json",
        "ocr_bridge_forwarding_mode_matrix.json",
        "ocr_bridge_fact_text_entry_policy_matrix.json",
        "ocr_bridge_future_runtime_source_refs_matrix.json",
        "ocr_bridge_review_notes.md",
    ]
    if not rr.is_dir():
        blockers.append("review_output_not_dir")
    else:
        for fn in required_out:
            if not (rr / fn).is_file():
                blockers.append(f"missing_output:{fn}")

    freeze = lc / "docs" / "architecture" / "ocr_bridge" / "LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md"
    if not freeze.is_file():
        blockers.append("missing_freeze_doc_in_repo")
    else:
        t = freeze.read_text(encoding="utf-8")
        if "raw_text_joined" not in t:
            blockers.append("G_freeze_doc_missing_raw_text_joined")
        if not any(x in t for x in ("禁止", "不得", "不接")):
            blockers.append("G_freeze_doc_missing_prohibition")

    gov = lc / "docs" / "architecture" / "ocr_bridge" / "LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md"
    if not gov.is_file():
        blockers.append("missing_governance_authority_doc")
    else:
        gt = gov.read_text(encoding="utf-8")
        if "MidPlatform has authority over OCR evidence interpretation" not in gt:
            blockers.append("G_missing_midplatform_authority_english_line")
        if "OCR provider has no authority to write facts" not in gt:
            blockers.append("G_missing_ocr_no_fact_authority_english_line")

    if not blockers and (rr / "ocr_bridge_interface_freeze_summary.json").is_file():
        summ = _read_json(rr / "ocr_bridge_interface_freeze_summary.json")
        if summ.get("midplatform_raw_text_joined_direct_input_forbidden_doc") is not True:
            blockers.append("G_forbidden_statement_not_confirmed")
        if summ.get("eval_placeholder_top_refs_ok") is not True:
            blockers.append("H_eval_markers_not_confirmed")
        if summ.get("runtime_refs_not_forged_ok") is not True:
            blockers.append("I_runtime_refs_forged_or_bad_urls")
        if summ.get("hard_audit_clean") is not True:
            blockers.append("JKL_hard_audit_not_clean")
        if summ.get("verdict") != "GO":
            blockers.append("M_review_verdict_not_go")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-OCRBridge-Review-001",
        "verdict": verdict,
        "blockers": blockers,
        "design_root": str(dr),
        "review_output_root": str(rr),
    }
    (rr / "ocr_bridge_interface_freeze_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
