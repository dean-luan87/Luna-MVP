#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
    ap.add_argument("--lowquality-partial-root", required=True)
    ap.add_argument("--previous-full-chain-root", required=True)
    ap.add_argument("--testboard-expansion-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    lp = _require_abs(args.lowquality_partial_root, "--lowquality-partial-root")
    prev = _require_abs(args.previous_full_chain_root, "--previous-full-chain-root")
    tb = _require_abs(args.testboard_expansion_root, "--testboard-expansion-root")

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_full_chain_runner_update_5cases_v0 import (
        run_cross_modal_vision_ocr_testboard_full_chain_runner_update_5cases_v0,
    )

    (
        summary,
        run_plan,
        case_run_matrix,
        planned_matrix,
        expected_vs_observed,
        risk_coverage,
        boundary_doc,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_full_chain_runner_update_5cases_v0(
        lowquality_partial_root=str(lp),
        previous_full_chain_root=str(prev),
        testboard_expansion_root=str(tb),
        work_root=out / "_case_work",
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_run_plan.json", run_plan)
    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_case_run_matrix.json", case_run_matrix)
    _write_json(
        out / "cross_modal_vision_ocr_testboard_full_chain_5cases_planned_only_matrix.json",
        planned_matrix,
    )
    _write_json(
        out / "cross_modal_vision_ocr_testboard_full_chain_5cases_expected_vs_observed_report.json",
        expected_vs_observed,
    )
    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_risk_coverage_report.json", risk_coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_boundary_matrix.json", boundary_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_full_chain_5cases_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_full_chain_5cases_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR TestBoard Full-Chain Runner Update (5 Cases)",
                "",
                f"- selected_case_count: {summary.get('selected_case_count')}",
                f"- planned_only_case_count: {summary.get('planned_only_case_count')}",
                "",
                "View update only; prior 3 cases from full-chain runner; LOW_QUALITY/PARTIAL from partial execution.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "selected_case_count": summary.get("selected_case_count"),
                "planned_only_case_count": summary.get("planned_only_case_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
