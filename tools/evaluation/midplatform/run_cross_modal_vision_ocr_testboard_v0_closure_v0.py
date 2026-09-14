#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001 runner."""

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
    ap.add_argument("--testboard-expansion-root", required=True)
    ap.add_argument("--full-chain-3-root", required=True)
    ap.add_argument("--lowquality-partial-root", required=True)
    ap.add_argument("--full-chain-5-root", required=True)
    ap.add_argument("--mixed-cnen-falsepositive-root", required=True)
    ap.add_argument("--full-chain-7-root", required=True)
    ap.add_argument("--duplicate-conflicting-root", required=True)
    ap.add_argument("--non-text-rejection-root", required=True)
    ap.add_argument("--full-chain-10-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_v0_closure_v0 import (
        run_cross_modal_vision_ocr_testboard_v0_closure_v0,
    )

    (
        summary,
        case_coverage,
        risk_coverage,
        rejection_coverage,
        full_chain_alignment,
        boundary,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_testboard_v0_closure_v0(
        testboard_expansion_root=str(_require_abs(args.testboard_expansion_root, "--testboard-expansion-root")),
        full_chain_3_root=str(_require_abs(args.full_chain_3_root, "--full-chain-3-root")),
        lowquality_partial_root=str(_require_abs(args.lowquality_partial_root, "--lowquality-partial-root")),
        full_chain_5_root=str(_require_abs(args.full_chain_5_root, "--full-chain-5-root")),
        mixed_cnen_falsepositive_root=str(_require_abs(args.mixed_cnen_falsepositive_root, "--mixed-cnen-falsepositive-root")),
        full_chain_7_root=str(_require_abs(args.full_chain_7_root, "--full-chain-7-root")),
        duplicate_conflicting_root=str(_require_abs(args.duplicate_conflicting_root, "--duplicate-conflicting-root")),
        non_text_rejection_root=str(_require_abs(args.non_text_rejection_root, "--non-text-rejection-root")),
        full_chain_10_root=args.full_chain_10_root.strip() or None,
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_testboard_v0_closure_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_case_coverage_matrix.json", case_coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_risk_coverage_report.json", risk_coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_rejection_coverage_report.json", rejection_coverage)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_full_chain_alignment_report.json", full_chain_alignment)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix.json", boundary)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_open_followups.json", followups)
    _write_json(out / "cross_modal_vision_ocr_testboard_v0_closure_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_testboard_v0_closure_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Vision OCR TestBoard v0 Closure",
                "",
                f"- testboard_status: {summary.get('testboard_status')}",
                f"- executed_case_count: {summary.get('executed_case_count')}",
                "",
                "Aggregate-only closure; no OCR re-run; TestBoard v0 frozen.",
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
