#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-StatusReview-001 — Verifier for mainline status review outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "mainline_status_review_summary.json",
        "mainline_phase_status_matrix.json",
        "mainline_runtime_connection_matrix.json",
        "mainline_design_vs_runtime_matrix.json",
        "mainline_evaluation_tools_matrix.json",
        "mainline_ocr_bridge_status_matrix.json",
        "mainline_voice_status_matrix.json",
        "mainline_next_step_recommendation.json",
        "mainline_docs_consistency_warning_report.json",
        "mainline_status_review_notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"A_missing:{fn}")

    if not blockers:
        pm = _read_json(root / "mainline_phase_status_matrix.json")
        rows = pm.get("rows") if isinstance(pm, dict) else None
        if not isinstance(rows, list) or not rows:
            blockers.append("B_empty_phase_matrix")
        else:
            flat = json.dumps(pm, ensure_ascii=False)
            if "YOLO" not in flat:
                blockers.append("B_yolo_not_represented")
            if "OCR" not in flat and "012" not in flat:
                blockers.append("C_ocr_not_represented")
            if "Evaluation Tools" not in flat:
                blockers.append("D_evaluation_not_represented")
            if "OCRBridge" not in flat:
                blockers.append("E_ocr_bridge_not_represented")
            if "Voice" not in flat:
                blockers.append("F_voice_not_represented")

        rm = _read_json(root / "mainline_runtime_connection_matrix.json")
        exp = (rm.get("expected_for_this_review_phase") or {}) if isinstance(rm, dict) else {}
        if exp.get("any_midplatform_connected") is not False:
            blockers.append("H_midplatform_expectation")
        if exp.get("any_whitebox_connected") is not False:
            blockers.append("I_whitebox_expectation")
        if exp.get("review_tool_provider_invoked") is not False:
            blockers.append("K_provider_invoked_expectation")

        agg = (rm.get("aggregate") or {}) if isinstance(rm, dict) else {}
        if agg.get("any_midplatform_connected") is True:
            blockers.append("H_midplatform_aggregate_true")
        if agg.get("any_whitebox_connected") is True:
            blockers.append("I_whitebox_aggregate_true")
        if agg.get("any_provider_invoked_by_this_review_tool") is True:
            blockers.append("K_provider_aggregate_true")
        if agg.get("world_write_invoked_any") is True:
            blockers.append("J_world_write_invoked_any")

        sm = _read_json(root / "mainline_status_review_summary.json")
        if sm.get("review_tool_invoked_provider") is not False:
            blockers.append("K_summary_provider_invoked")
        if sm.get("review_tool_modified_runtime") is not False:
            blockers.append("G_summary_runtime_modified")

        nx = _read_json(root / "mainline_next_step_recommendation.json")
        if not isinstance(nx, dict) or "recommended_next_step" not in nx:
            blockers.append("L_missing_next_step")

        dw = _read_json(root / "mainline_docs_consistency_warning_report.json")
        if not isinstance(dw, dict) or "warnings" not in dw:
            blockers.append("M_missing_docs_warning_report")

        if str(sm.get("verdict") or "") not in ("GO", "CONDITIONAL_GO"):
            blockers.append("O_verdict_not_goish")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"phase": "Phase-Mainline-StatusReview-001", "verdict": verdict, "blockers": blockers, "output_root": str(root)}
    (root / "mainline_status_review_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
