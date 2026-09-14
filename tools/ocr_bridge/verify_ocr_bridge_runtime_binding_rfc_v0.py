#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Implementation-RFC-001 — Verifier for OCR bridge runtime binding RFC outputs.
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
    ap.add_argument("--review-root", required=True)
    ap.add_argument("--rfc-output-root", required=True)
    args = ap.parse_args()

    dr = Path(args.design_root).expanduser().resolve()
    rr = Path(args.review_root).expanduser().resolve()
    root = Path(args.rfc_output_root).expanduser().resolve()

    blockers: List[str] = []

    if not dr.is_dir():
        blockers.append("A_design_root_not_dir")
    elif not (dr / "ocr_evidence_pack_example.json").is_file():
        blockers.append("A_design_pack_missing")

    if not rr.is_dir():
        blockers.append("B_review_root_not_dir")
    elif not (rr / "ocr_bridge_interface_freeze_summary.json").is_file():
        blockers.append("B_review_summary_missing")

    required = [
        "ocr_bridge_runtime_binding_rfc_summary.json",
        "ocr_bridge_runtime_binding_candidate_matrix.json",
        "ocr_bridge_runtime_source_ref_plan_matrix.json",
        "ocr_bridge_runtime_flag_matrix.json",
        "ocr_bridge_shadow_only_strategy_matrix.json",
        "ocr_bridge_abort_rollback_matrix.json",
        "ocr_bridge_runtime_binding_rfc_notes.md",
    ]
    if not root.is_dir():
        blockers.append("rfc_output_not_dir")
    else:
        for fn in required:
            if not (root / fn).is_file():
                blockers.append(f"missing:{fn}")

    if not blockers and (root / "ocr_bridge_runtime_flag_matrix.json").is_file():
        fm = _read_json(root / "ocr_bridge_runtime_flag_matrix.json")
        dd = fm.get("derived_defaults") or {}
        if dd.get("forward_midplatform_default") is not False:
            blockers.append("H_forward_midplatform_default_not_false")
        if dd.get("fact_text_layer_candidates_default") is not False:
            blockers.append("I_fact_text_default_not_false")
        if dd.get("global_kill_exists") is not True:
            blockers.append("J_global_kill_missing")

    if not blockers and (root / "ocr_bridge_runtime_binding_rfc_summary.json").is_file():
        sm = _read_json(root / "ocr_bridge_runtime_binding_rfc_summary.json")
        c = sm.get("constraints") or {}
        if c.get("runtime_implementation_modules_modified") is True:
            blockers.append("K_runtime_implementation_modules_modified")
        if c.get("runtime_integration") is not False:
            blockers.append("L_runtime_integration_not_false")
        if c.get("midplatform_call") is not False:
            blockers.append("M_midplatform_not_false")
        if c.get("whitebox_integration") is not False:
            blockers.append("N_whitebox_not_false")
        if sm.get("verdict") != "GO":
            blockers.append("O_rfc_verdict_not_go")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-OCRBridge-Implementation-RFC-001",
        "verdict": verdict,
        "blockers": blockers,
        "design_root": str(dr),
        "review_root": str(rr),
        "rfc_output_root": str(root),
    }
    (root / "ocr_bridge_runtime_binding_rfc_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
