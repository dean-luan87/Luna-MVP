#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001 runner."""

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
    ap.add_argument("--duplicate-conflicting-root", required=True)
    ap.add_argument("--testboard-expansion-root", required=True)
    ap.add_argument("--vision-roi-bridge-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    dup = _require_abs(args.duplicate_conflicting_root, "--duplicate-conflicting-root")
    tb = _require_abs(args.testboard_expansion_root, "--testboard-expansion-root")
    bridge = _require_abs(args.vision_roi_bridge_root, "--vision-roi-bridge-root")

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0 import (
        run_cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0,
    )

    (
        summary,
        case_report,
        rejection_matrix,
        execution_doc,
        planned_doc,
        expected_doc,
        risk_report,
        boundary_doc,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0(
        duplicate_conflicting_root=str(dup),
        testboard_expansion_root=str(tb),
        vision_roi_bridge_root=str(bridge),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_report.json", case_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_matrix.json", rejection_matrix)
    _write_json(
        out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_execution_matrix.json",
        execution_doc,
    )
    _write_json(
        out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_planned_only_matrix.json",
        planned_doc,
    )
    _write_json(
        out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_expected_vs_observed_report.json",
        expected_doc,
    )
    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_risk_report.json", risk_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_boundary_matrix.json", boundary_doc)
    _write_json(out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR TestBoard NonText ROI Rejection",
                "",
                f"- executed_case_count: {summary.get('executed_case_count')}",
                f"- planned_only_case_count: {summary.get('planned_only_case_count')}",
                "",
                "NON_TEXT_ROI_REJECTED: rejected_before_ocr; no OCRRequest; no provider invoke.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "executed_case_count": summary.get("executed_case_count"),
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
