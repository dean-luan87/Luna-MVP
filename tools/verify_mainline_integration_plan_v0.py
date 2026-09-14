#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-IntegrationPlan-001 — Verifier for integration plan outputs.
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
    ap.add_argument("--status-review-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    sr = Path(args.status_review_root).expanduser().resolve()
    root = Path(args.output_root).expanduser().resolve()
    blockers: List[str] = []

    if not sr.is_dir():
        blockers.append("A_status_review_not_dir")

    required = [
        "mainline_integration_plan_summary.json",
        "mainline_next_phase_order_matrix.json",
        "mainline_option_comparison_matrix.json",
        "mainline_dependency_matrix.json",
        "mainline_blocked_action_matrix.json",
        "mainline_recommended_execution_sequence.json",
        "mainline_integration_plan_notes.md",
    ]
    if not root.is_dir():
        blockers.append("output_not_dir")
    else:
        for fn in required:
            if not (root / fn).is_file():
                blockers.append(f"missing:{fn}")

    if not blockers and (root / "mainline_option_comparison_matrix.json").is_file():
        oc = _read_json(root / "mainline_option_comparison_matrix.json")
        opts = oc.get("options") if isinstance(oc, dict) else None
        ids = {o.get("id") for o in opts} if isinstance(opts, list) else set()
        for need in ("A", "B", "C", "D", "E"):
            if need not in ids:
                blockers.append(f"B_option_missing:{need}")

    if not blockers and (root / "mainline_recommended_execution_sequence.json").is_file():
        seq = _read_json(root / "mainline_recommended_execution_sequence.json")
        steps = seq.get("ordered_phases") if isinstance(seq, dict) else None
        if not isinstance(steps, list) or len(steps) < 5:
            blockers.append("C_execution_sequence_incomplete")
        flat = json.dumps(seq, ensure_ascii=False)
        if "VoiceInteraction" not in flat and "B" not in flat:
            blockers.append("D_voice_not_represented")
        if "OCRBridge" not in flat and "shadow" not in flat.lower():
            blockers.append("E_ocr_bridge_shadow_not_represented")
        if "Evaluation" not in flat and "D" not in flat:
            blockers.append("F_evaluation_not_represented")
        if "PaddleOCR" not in flat and "C" not in flat:
            blockers.append("G_paddle_not_represented")

    if not blockers and (root / "mainline_integration_plan_summary.json").is_file():
        sm = _read_json(root / "mainline_integration_plan_summary.json")
        c = sm.get("constraints") or {}
        if c.get("implementation_performed") is not False:
            blockers.append("H_implementation_claimed")
        if c.get("provider_invoked") is not False:
            blockers.append("I_provider_invoked")
        if c.get("runtime_integration") is not False:
            blockers.append("J_runtime_integration")
        if c.get("midplatform_invocation") is not False:
            blockers.append("K_midplatform")
        if c.get("whitebox_integration") is not False:
            blockers.append("L_whitebox")
        if not str(sm.get("recommended_next_phase_after_this_plan") or "").strip():
            blockers.append("M_missing_recommended_next")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-Mainline-IntegrationPlan-001",
        "verdict": verdict,
        "blockers": blockers,
        "status_review_root": str(sr),
        "output_root": str(root),
    }
    (root / "mainline_integration_plan_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
